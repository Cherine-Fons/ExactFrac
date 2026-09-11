"""Exact Standard and Accelerated branch roots with separate query diagnostics.

Implement alg:standard-branch and alg:branch under DESIGN 4.10 and 4.11.
A returned root is the transformed branch minimum, not an endpoint density,
global result, witness, or certificate. Raw pairs are never normalized.
"""

from __future__ import annotations

from dataclasses import dataclass

from .oracle import (
    BranchOracleContext,
    BranchOracleResult,
    BranchOracleStats,
    exact_branch_min,
)
from .rational import (
    RawPair,
    compare_pairs,
    make_pair,
    pair_add_one,
    pair_reflect,
    residual_numerator,
    validate_pair,
)

__all__ = (
    "AcceleratedBranchStats",
    "BranchResult",
    "StandardBranchStats",
    "solve_branch_accelerated",
    "solve_branch_standard",
)


@dataclass(frozen=True, slots=True)
class BranchResult:
    """Raw root and original shore; standalone construction checks only shape."""

    root: RawPair
    shore: int

    def __post_init__(self) -> None:
        validate_pair(self.root)
        if type(self.shore) is not int or self.shore <= 0:
            raise ValueError("shore must be a positive built-in int")


@dataclass(frozen=True, slots=True)
class StandardBranchStats:
    """Per-solve diagnostics; construction does not certify an observed run."""

    oracle_calls: int
    outer_iterations: int
    newton_updates: int
    oracle_stats: BranchOracleStats

    def __post_init__(self) -> None:
        for value in (self.oracle_calls, self.outer_iterations, self.newton_updates):
            if type(value) is not int or value < 0:
                raise ValueError("counts must be nonnegative built-in ints")
        if type(self.oracle_stats) is not BranchOracleStats:
            raise ValueError("oracle_stats must be an exact BranchOracleStats")


def _checked_query(
    context: BranchOracleContext,
    branch: int,
    parameter: RawPair,
) -> tuple[BranchOracleResult | None, BranchOracleStats]:
    """Bind a normally returned oracle reply to its submitted raw parameter."""
    response = exact_branch_min(context, branch, parameter)
    if type(response) is not tuple or len(response) != 2:
        raise RuntimeError("oracle response must be an exact two-element tuple")
    result, diagnostics = response
    if result is not None and type(result) is not BranchOracleResult:
        raise RuntimeError("oracle result has an unexpected type")
    if type(diagnostics) is not BranchOracleStats:
        raise RuntimeError("oracle diagnostics have an unexpected type")
    if result is not None:
        if result.shore > (1 << context.instance.n) - 1:
            raise RuntimeError("oracle shore is outside the original universe")
        check_raw = residual_numerator(parameter, result.c, result.h)
        if check_raw != result.residual:
            raise RuntimeError("oracle residual is not bound to the submitted parameter")
    return result, diagnostics


def _add_diagnostics(
    total: BranchOracleStats,
    current: BranchOracleStats,
) -> BranchOracleStats:
    """Add six closed counters and retain the maximum flow-only generated value."""
    return BranchOracleStats(
        total.atomic_families_examined + current.atomic_families_examined,
        total.atomic_families_feasible + current.atomic_families_feasible,
        total.parity_cut_calls + current.parity_cut_calls,
        total.ordinary_min_cut_calls + current.ordinary_min_cut_calls,
        total.flow_augmentations + current.flow_augmentations,
        total.flow_bfs_scans + current.flow_bfs_scans,
        max(total.flow_peak_generated_value, current.flow_peak_generated_value),
    )


def solve_branch_standard(
    context: BranchOracleContext,
    branch: int,
) -> tuple[BranchResult | None, StandardBranchStats]:
    """Return the transformed minimum and an attaining shore, or infeasibility.

    Query the mandatory zero seed, initialize at its literal ratio plus one,
    and reset each negative-residual iterate to the returned fresh source pair.
    Only exact zero terminates. The submitted terminal pair and the current
    terminal shore remain separately authoritative. Dependency exceptions
    propagate unchanged; no partial result is returned after an internal error.

    Preparation is paid by the supplied context, not repeated here. Retained
    outer state is a bounded number of integer records, not constant byte size.
    No trace, magnitude-based iteration limit, or additional tie rule is used.
    """
    if type(context) is not BranchOracleContext:
        raise ValueError("context must be an exact BranchOracleContext")
    if type(branch) is not int or branch not in (0, 1, 2, 3):
        raise ValueError("branch must be a built-in int in (0, 1, 2, 3)")

    seed, oracle_stats = _checked_query(context, branch, (0, 1))
    oracle_calls = 1
    outer_iterations = newton_updates = 0
    if seed is None:
        return None, StandardBranchStats(1, 0, 0, oracle_stats)

    seed_pair = make_pair(seed.c, seed.h)
    parameter = pair_add_one(seed_pair)
    first_loop = True

    while True:
        result, diagnostics = _checked_query(context, branch, parameter)
        oracle_calls += 1
        outer_iterations += 1
        oracle_stats = _add_diagnostics(oracle_stats, diagnostics)
        if result is None:
            raise RuntimeError("a feasible branch became infeasible after the seed")
        raw = result.residual
        if first_loop:
            if raw >= 0:
                raise RuntimeError("the initial K query must have negative residual")
        elif raw > 0:
            raise RuntimeError("a later Standard query has positive residual")
        if raw == 0:
            return BranchResult(parameter, result.shore), StandardBranchStats(
                oracle_calls, outer_iterations, newton_updates, oracle_stats,
            )

        next_parameter = make_pair(result.c, result.h)
        if compare_pairs(next_parameter, parameter) >= 0:
            raise RuntimeError("a negative-residual reset must strictly decrease")
        parameter = next_parameter
        newton_updates += 1
        first_loop = False


@dataclass(frozen=True, slots=True)
class AcceleratedBranchStats:
    """Structural per-solve diagnostics, not an execution or optimality certificate."""

    oracle_calls: int
    outer_iterations: int
    newton_queries: int
    lookahead_queries: int
    lookahead_accepted: int
    lookahead_rejected: int
    early_returns: int
    oracle_stats: BranchOracleStats

    def __post_init__(self) -> None:
        for value in (
            self.oracle_calls, self.outer_iterations, self.newton_queries,
            self.lookahead_queries, self.lookahead_accepted,
            self.lookahead_rejected, self.early_returns,
        ):
            if type(value) is not int or value < 0:
                raise ValueError("counts must be nonnegative built-in ints")
        if type(self.oracle_stats) is not BranchOracleStats:
            raise ValueError("oracle_stats must be an exact BranchOracleStats")


def solve_branch_accelerated(
    context: BranchOracleContext,
    branch: int,
) -> tuple[BranchResult | None, AcceleratedBranchStats]:
    """Return the transformed branch minimum and an attaining original shore.

    Initialize at the mandatory seed's fresh ratio, without Standard's plus one.
    Query each fresh Newton point before reflecting the current point about it.
    Reject positive look-ahead residuals by retaining the already-queried Newton
    pair and reply; accept negative ones. Exact zero returns the submitted pair
    with that query's shore. Closed dependencies own arithmetic and minimization.

    Retain only bounded outer state; do not rebuild the supplied prepared context,
    normalize raw pairs, add a tie preference, or enforce a numerical work limit.
    Diagnostics include rejected-query work and never control mathematical choices.
    Dependency exceptions propagate unchanged; internal seam failures return no result.
    """
    if type(context) is not BranchOracleContext:
        raise ValueError("context must be an exact BranchOracleContext")
    if type(branch) is not int or branch not in (0, 1, 2, 3):
        raise ValueError("branch must be a built-in int in (0, 1, 2, 3)")

    seed, diagnostics = _checked_query(context, branch, (0, 1))
    oracle_stats = _add_diagnostics(BranchOracleStats(0, 0, 0, 0, 0, 0, 0), diagnostics)
    oracle_calls = 1
    outer_iterations = newton_queries = lookahead_queries = 0
    lookahead_accepted = lookahead_rejected = 0
    if seed is None:
        return None, AcceleratedBranchStats(1, 0, 0, 0, 0, 0, 0, oracle_stats)

    parameter = make_pair(seed.c, seed.h)
    result, diagnostics = _checked_query(context, branch, parameter)
    oracle_calls += 1
    oracle_stats = _add_diagnostics(oracle_stats, diagnostics)
    if result is None:
        raise RuntimeError("a feasible branch became infeasible at initialization")
    if result.residual > 0:
        raise RuntimeError("the initial Accelerated query has positive residual")

    while result.residual < 0:
        outer_iterations += 1
        newton = make_pair(result.c, result.h)
        if compare_pairs(newton, parameter) >= 0:
            raise RuntimeError("the Newton point must strictly decrease")
        newton_result, diagnostics = _checked_query(context, branch, newton)
        oracle_calls += 1
        newton_queries += 1
        oracle_stats = _add_diagnostics(oracle_stats, diagnostics)
        if newton_result is None:
            raise RuntimeError("a feasible branch became infeasible at Newton")
        if newton_result.residual > 0:
            raise RuntimeError("a Newton query has positive residual")
        if newton_result.residual == 0:
            return BranchResult(newton, newton_result.shore), AcceleratedBranchStats(
                oracle_calls, outer_iterations, newton_queries, lookahead_queries,
                lookahead_accepted, lookahead_rejected, 1, oracle_stats,
            )

        reflected = pair_reflect(newton, parameter)
        if compare_pairs(reflected, newton) >= 0:
            raise RuntimeError("the reflected point must strictly precede Newton")
        reflected_result, diagnostics = _checked_query(context, branch, reflected)
        oracle_calls += 1
        lookahead_queries += 1
        oracle_stats = _add_diagnostics(oracle_stats, diagnostics)
        if reflected_result is None:
            raise RuntimeError("a feasible branch became infeasible at reflection")
        if reflected_result.residual == 0:
            return BranchResult(reflected, reflected_result.shore), AcceleratedBranchStats(
                oracle_calls, outer_iterations, newton_queries, lookahead_queries,
                lookahead_accepted, lookahead_rejected, 1, oracle_stats,
            )

        if reflected_result.residual < 0:
            next_parameter, next_result = reflected, reflected_result
            lookahead_accepted += 1
        else:
            next_parameter, next_result = newton, newton_result
            lookahead_rejected += 1
        if compare_pairs(next_parameter, parameter) >= 0:
            raise RuntimeError("the retained Accelerated state must strictly decrease")
        parameter, result = next_parameter, next_result

    return BranchResult(parameter, result.shore), AcceleratedBranchStats(
        oracle_calls, outer_iterations, newton_queries, lookahead_queries,
        lookahead_accepted, lookahead_rejected, 0, oracle_stats,
    )
