"""StrongCompactMSPD global composition and original compact witness reconstruction.

Implement alg:global under DESIGN 4.12. The selected closed branch solver owns
branch optimality. This wrapper binds each original endpoint to its branch root,
compares raw witness-attaining values, and retains the first strict maximum.
Diagnostics are separate; no record here is an independent optimality certificate.
"""

from __future__ import annotations

from dataclasses import dataclass

from .branch import (
    AcceleratedBranchStats,
    BranchResult,
    StandardBranchStats,
    solve_branch_accelerated,
    solve_branch_standard,
)
from .instance import Instance
from .oracle import BranchOracleContext
from .rational import compare_pairs
from .witness import ExactValue, Witness, shore_b_q, shore_d_q, shore_f, witness_value

__all__ = ("SolveResult", "SolveStats", "solve")


def _selected_stats_type(branch_solver: str) -> type[StandardBranchStats | AcceleratedBranchStats]:
    """Validate the explicit public selection without coercion or graph access."""
    if type(branch_solver) is not str or branch_solver not in ("Standard", "Accelerated"):
        raise ValueError('branch_solver must be an exact str: "Standard" or "Accelerated"')
    return StandardBranchStats if branch_solver == "Standard" else AcceleratedBranchStats


@dataclass(frozen=True, slots=True)
class SolveResult:
    """Raw mathematical result; standalone construction checks record types only."""

    value: ExactValue
    witness: Witness | None

    def __post_init__(self) -> None:
        if type(self.value) is not ExactValue:
            raise ValueError("value must be an exact ExactValue")
        if self.witness is not None and type(self.witness) is not Witness:
            raise ValueError("witness must be an exact Witness or None")
        if self.witness is None and (self.value.N != 0 or self.value.D != 1):
            raise ValueError("an Empty result requires the literal raw value (0, 1)")


@dataclass(frozen=True, slots=True)
class SolveStats:
    """Retained closed diagnostics and provenance, not an execution certificate."""

    branch_solver: str
    branch_stats: tuple[StandardBranchStats | AcceleratedBranchStats, ...]
    attaining_candidate: str

    def __post_init__(self) -> None:
        selected_type = _selected_stats_type(self.branch_solver)
        if type(self.branch_stats) is not tuple:
            raise ValueError("branch_stats must be an exact tuple")
        for record in self.branch_stats:
            if type(record) is not selected_type:
                raise ValueError("every branch record must have the selected exact stats type")
        if type(self.attaining_candidate) is not str or self.attaining_candidate not in (
            "Empty", "Baseline", "L0", "L1", "H0", "H1", "H2",
        ):
            raise ValueError("attaining_candidate must be an exact recognized str")


def _baseline_shore(instance: Instance, degrees: tuple[int, ...]) -> int:
    """Refine lem:empty by category priority, then increasing vertex index."""
    for vertex, capacity in enumerate(instance.f):
        if not capacity & 1:
            return 1 << vertex
    for vertex, capacity in enumerate(instance.f):
        if capacity >= 3:
            return 1 << vertex
    for vertex, capacity in enumerate(instance.f):
        if capacity == 1 and degrees[vertex] >= 2:
            return 1 << vertex

    # The remaining source case is a unit matching with at least two edges.
    for vertex, capacity in enumerate(instance.f):
        if capacity != 1 or degrees[vertex] != 1:
            raise RuntimeError("the baseline's remaining case is not a unit matching")
    if instance.m < 2:
        raise RuntimeError("the matching baseline requires at least two support edges")
    covered = 0
    for left, right, multiplicity in instance.edges:
        endpoints = (1 << left) | (1 << right)
        if multiplicity != 1 or covered & endpoints:
            raise RuntimeError("the matching baseline requires disjoint unit edges")
        covered |= endpoints
    if covered != (1 << instance.n) - 1:
        raise RuntimeError("the matching baseline must cover the original vertex universe")
    return (1 << instance.edges[0][0]) | (1 << instance.edges[1][0])


def _all_boundary(instance: Instance, U: int, omit_one: bool) -> tuple[int, ...]:
    """Take all crossing copies, optionally omitting one from the first edge."""
    counts = [0] * instance.m
    remaining = int(omit_one)
    for edge_ref, (left, right, multiplicity) in enumerate(instance.edges):
        if bool(U & (1 << left)) != bool(U & (1 << right)):
            counts[edge_ref] = multiplicity - remaining
            remaining = 0
    if remaining:
        raise RuntimeError("omitting one copy requires an actual crossing edge")
    return tuple(counts)


def _first_copies(instance: Instance, U: int, total: int) -> tuple[int, ...]:
    """Take one or two copies by a support scan, never a multiplicity-sized loop."""
    counts = [0] * instance.m
    remaining = total
    for edge_ref, (left, right, multiplicity) in enumerate(instance.edges):
        if bool(U & (1 << left)) != bool(U & (1 << right)):
            taken = min(multiplicity, remaining)
            counts[edge_ref] = taken
            remaining -= taken
    if remaining:
        raise RuntimeError("the endpoint requires more incident copies than the scan found")
    return tuple(counts)


def _evaluate(instance: Instance, witness: Witness) -> ExactValue:
    """Accept only the normally returned closed evaluator record; exceptions pass through."""
    value = witness_value(instance, witness)
    if type(value) is not ExactValue:
        raise RuntimeError("witness_value returned an unexpected record type")
    return value


def _baseline(instance: Instance, degrees: tuple[int, ...]) -> tuple[ExactValue, Witness]:
    """Upgrade the feasibility shore using lem:unit, then retain its actual raw value."""
    U = _baseline_shore(instance, degrees)
    s = shore_f(instance, U)
    b = shore_b_q(instance, U)
    odd = (s + b) & 1
    if (odd and s + b < 3) or (not odd and (b < 1 or s + b < 4)):
        raise RuntimeError("the baseline shore violates the unit-witness prerequisites")
    witness = Witness(U, _all_boundary(instance, U, not odd))
    value = _evaluate(instance, witness)
    if compare_pairs((value.N, value.D), (1, 1)) < 0:
        raise RuntimeError("the constructive baseline has value below one")
    return value, witness


def _endpoint(instance: Instance, branch: int, result: BranchResult) -> tuple[ExactValue, Witness]:
    """Reconstruct and numerically bind one original endpoint, not another optimum."""
    U = result.shore
    if not 0 < U < 1 << instance.n:
        raise RuntimeError("the branch shore is outside the original nonempty universe")
    s = shore_f(instance, U)
    b = shore_b_q(instance, U)
    d = shore_d_q(instance, U)
    if branch == 0:
        valid = (s + b) & 1 and s + b >= 3 and d + 1 - s > 0
        numerator, denominator = d + b, s + b - 1
    elif branch == 1:
        valid = not ((s + b) & 1) and b >= 1 and d > s and s + b >= 4
        numerator, denominator = d + b - 2, s + b - 2
    elif branch == 2:
        valid = (s & 1) and s >= 3
        numerator, denominator = d - b, s - 1
    else:
        valid = not (s & 1) and s >= 2 and b >= 1
        numerator, denominator = d - b + 2, s
    if not valid:
        raise RuntimeError("the branch shore violates its original endpoint domain")

    if branch < 2:
        counts = _all_boundary(instance, U, branch == 1)
    elif branch == 2:
        counts = (0,) * instance.m
    else:
        counts = _first_copies(instance, U, 1)
    witness = Witness(U, counts)
    value = _evaluate(instance, witness)
    if (numerator, denominator) != (value.N, value.D):
        raise RuntimeError("the evaluated raw endpoint differs from its literal source formula")
    A, B = result.root
    if branch < 2:
        bound = value.N > value.D and A * (value.N - value.D) == B * value.D
    else:
        bound = A * value.D == -B * value.N
    if not bound:
        raise RuntimeError("the branch root is not numerically bound to the reconstructed endpoint")
    return value, witness


def solve(instance: Instance, branch_solver: str) -> tuple[SolveResult, SolveStats]:
    """Return the global raw optimum and its original compact attaining witness.

    Validate public types before graph use. For Q >= 2, prepare once, retain a
    constructive baseline, traverse all four selected branches, then construct
    and compare direct H2 even when dominated. Keep only bounded candidate state
    beyond the prepared context and support-sized reconstruction workspace.
    No dependency exception is translated or used to return a partial result.
    """
    if type(instance) is not Instance:
        raise ValueError("instance must be an exact production Instance")
    selected_type = _selected_stats_type(branch_solver)
    if instance.Q == 1:
        return SolveResult(ExactValue(0, 1), None), SolveStats(branch_solver, (), "Empty")

    context = BranchOracleContext(instance)
    degrees = instance.d_q
    best_value, best_witness = _baseline(instance, degrees)
    origin = "Baseline"
    selected_solver = (
        solve_branch_standard if branch_solver == "Standard" else solve_branch_accelerated
    )
    records = []
    for branch in (0, 1, 2, 3):
        response = selected_solver(context, branch)
        if type(response) is not tuple or len(response) != 2:
            raise RuntimeError("a branch reply must be an exact two-element tuple")
        result, diagnostics = response
        if result is not None and type(result) is not BranchResult:
            raise RuntimeError("a branch reply has an unexpected result type")
        if type(diagnostics) is not selected_type:
            raise RuntimeError("a branch reply has the wrong selected diagnostics type")
        records.append(diagnostics)
        if result is None:
            continue
        value, witness = _endpoint(instance, branch, result)
        if compare_pairs((value.N, value.D), (best_value.N, best_value.D)) > 0:
            best_value, best_witness = value, witness
            origin = ("L0", "L1", "H0", "H1")[branch]

    for vertex, capacity in enumerate(instance.f):
        if capacity == 1 and degrees[vertex] >= 2:
            U = 1 << vertex
            witness = Witness(U, _first_copies(instance, U, 2))
            value = _evaluate(instance, witness)
            if (value.N, value.D) != (4, 2):
                raise RuntimeError("the direct H2 witness must attain the literal raw value (4, 2)")
            if compare_pairs((value.N, value.D), (best_value.N, best_value.D)) > 0:
                best_value, best_witness = value, witness
                origin = "H2"
            break
    return SolveResult(best_value, best_witness), SolveStats(branch_solver, tuple(records), origin)
