"""Deterministic recording-only measurements for one exact global solve.

The legacy solver retains all optimization decisions. Public records validate
shape and consistency, not the authenticity or optimality of an execution.
Environmental metadata is supplied separately and is never discovered here.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from math import isfinite

from ._telemetry import _measurement, _observe_ints, _observe_pair_values
from .branch import AcceleratedBranchStats, StandardBranchStats
from .instance import Instance
from .solve import SolveResult, SolveStats, solve

__all__ = (
    "AlgorithmStats",
    "BranchTelemetry",
    "RunMetadata",
    "RunRecord",
    "WorkStats",
    "solve_with_telemetry",
)


def _nonnegative(value: int) -> None:
    if type(value) is not int or value < 0:
        raise ValueError("counts and peaks must be nonnegative built-in ints")


def _bits(value: int) -> int:
    return max(1, abs(value).bit_length())


@dataclass(frozen=True, slots=True)
class WorkStats:
    """Native event counts and exact observation peaks for one bucket or aggregate."""

    outer_iterations: int
    oracle_calls: int
    newton_updates: int
    newton_queries: int
    newton_candidates: int
    lookahead_queries: int
    lookahead_accepted: int
    lookahead_rejected: int
    lookahead_terminal: int
    newton_terminal: int
    initialization_returns: int
    early_returns: int
    atomic_families_enumerated: int
    atomic_families_examined: int
    atomic_families_feasible: int
    parity_cut_calls: int
    ordinary_min_cut_calls: int
    max_flow_calls: int
    augmentations: int
    bfs_scans: int
    flow_peak_generated_value: int
    flow_peak_bits: int
    peak_numerator_bits: int
    peak_denominator_bits: int
    peak_integer_bits: int

    def __post_init__(self) -> None:
        for item in fields(WorkStats):
            _nonnegative(getattr(self, item.name))
        if self.newton_candidates != self.newton_updates + self.newton_queries:
            raise ValueError("Newton event mapping is inconsistent")
        if self.lookahead_queries != (
            self.lookahead_accepted + self.lookahead_rejected + self.lookahead_terminal
        ):
            raise ValueError("look-ahead query outcomes are inconsistent")
        if self.early_returns != self.lookahead_terminal + self.newton_terminal:
            raise ValueError("in-loop terminal counts are inconsistent")
        if self.atomic_families_feasible > self.atomic_families_examined:
            raise ValueError("feasible examinations exceed all examinations")
        if self.parity_cut_calls != self.atomic_families_feasible:
            raise ValueError("parity calls must equal feasible descriptor examinations")
        if self.ordinary_min_cut_calls != self.max_flow_calls:
            raise ValueError("the closed backend uses one flow per ordinary cut")
        if self.max_flow_calls == 0:
            if any((self.augmentations, self.bfs_scans, self.flow_peak_generated_value)):
                raise ValueError("flow work is present without an ordinary flow call")
            expected_flow_bits = 0
        else:
            expected_flow_bits = _bits(self.flow_peak_generated_value)
        if self.flow_peak_bits != expected_flow_bits:
            raise ValueError("flow peak distinguishes no flow from observed zero")
        if self.peak_integer_bits < max(
            self.peak_numerator_bits, self.peak_denominator_bits, self.flow_peak_bits,
        ):
            raise ValueError("the whole integer peak must include its recorded subpeaks")


@dataclass(frozen=True, slots=True)
class BranchTelemetry:
    branch: int
    feasible: bool
    work: WorkStats

    def __post_init__(self) -> None:
        if type(self.branch) is not int or self.branch not in (0, 1, 2, 3):
            raise ValueError("branch must be an exact index in (0, 1, 2, 3)")
        if type(self.feasible) is not bool:
            raise ValueError("feasible must be an exact bool")
        if type(self.work) is not WorkStats:
            raise ValueError("work must be an exact WorkStats")


def _native_events(
    route: str, native: StandardBranchStats | AcceleratedBranchStats, feasible: bool,
) -> tuple[int, ...]:
    """Validate, then copy the two native event conventions without merging meanings."""
    if route == "Standard":
        if type(native) is not StandardBranchStats:
            raise ValueError("the native record does not match the selected solver")
        if feasible:
            if native.oracle_calls != 1 + native.outer_iterations:
                raise ValueError("Standard oracle/outer counts differ")
            if native.outer_iterations != native.newton_updates + 1:
                raise ValueError("Standard reset/terminal counts differ")
        elif (native.oracle_calls, native.outer_iterations, native.newton_updates) != (1, 0, 0):
            raise ValueError("infeasible Standard branch must stop at its seed")
        return (
            native.outer_iterations, native.oracle_calls, native.newton_updates,
            0, native.newton_updates, 0, 0, 0, 0, 0, 0, 0,
        )
    if type(native) is not AcceleratedBranchStats:
        raise ValueError("the native record does not match the selected solver")
    terminal = native.lookahead_queries - native.lookahead_accepted - native.lookahead_rejected
    newton_terminal = native.early_returns - terminal
    initialization = int(feasible and native.outer_iterations == 0)
    if feasible:
        if native.oracle_calls != 2 + native.newton_queries + native.lookahead_queries:
            raise ValueError("Accelerated oracle counts differ")
        if native.outer_iterations != native.newton_queries:
            raise ValueError("Accelerated outer/Newton counts differ")
        if terminal not in (0, 1) or newton_terminal not in (0, 1):
            raise ValueError("Accelerated terminal outcomes differ")
        if initialization + native.early_returns != 1:
            raise ValueError("a feasible branch must return once")
    elif (native.oracle_calls, native.outer_iterations, native.newton_queries,
          native.lookahead_queries, native.lookahead_accepted, native.lookahead_rejected,
          native.early_returns) != (1, 0, 0, 0, 0, 0, 0):
        raise ValueError("infeasible Accelerated branch must stop at its seed")
    return (
        native.outer_iterations, native.oracle_calls, 0, native.newton_queries,
        native.newton_queries, native.lookahead_queries, native.lookahead_accepted,
        native.lookahead_rejected, terminal, newton_terminal, initialization, native.early_returns,
    )


def _native_work(native: StandardBranchStats | AcceleratedBranchStats) -> tuple[int, ...]:
    observed = native.oracle_stats
    return (
        observed.atomic_families_examined, observed.atomic_families_feasible,
        observed.parity_cut_calls, observed.ordinary_min_cut_calls, observed.max_flow_calls,
        observed.flow_augmentations, observed.flow_bfs_scans, observed.flow_peak_generated_value,
        0 if observed.max_flow_calls == 0 else _bits(observed.flow_peak_generated_value),
    )


def _values(work: WorkStats) -> tuple[int, ...]:
    return tuple(getattr(work, item.name) for item in fields(WorkStats))


def _aggregate(parts: tuple[WorkStats, ...]) -> WorkStats:
    return WorkStats(*(
        sum(getattr(part, item.name) for part in parts)
        if index < 20 else max(getattr(part, item.name) for part in parts)
        for index, item in enumerate(fields(WorkStats))
    ))


@dataclass(frozen=True, slots=True)
class AlgorithmStats:
    native: SolveStats
    total: WorkStats
    nonbranch: WorkStats
    branches: tuple[BranchTelemetry, ...]
    output_numerator_bits: int
    output_denominator_bits: int

    def __post_init__(self) -> None:
        if type(self.native) is not SolveStats:
            raise ValueError("native must be an exact SolveStats")
        if type(self.total) is not WorkStats or type(self.nonbranch) is not WorkStats:
            raise ValueError("total and nonbranch must be exact WorkStats")
        if type(self.branches) is not tuple:
            raise ValueError("branches must be an exact tuple")
        for part in self.branches:
            if type(part) is not BranchTelemetry:
                raise ValueError("branch entries must be exact BranchTelemetry")
        for value in (self.output_numerator_bits, self.output_denominator_bits):
            if type(value) is not int or value < 1:
                raise ValueError("output bit lengths must be positive built-in ints")
        empty = self.native.attaining_candidate == "Empty"
        if len(self.branches) != (0 if empty else 4):
            raise ValueError("a nonempty solve has exactly four branch records")
        if len(self.native.branch_stats) != len(self.branches):
            raise ValueError("native and measured branch counts differ")
        if tuple(part.branch for part in self.branches) != (() if empty else (0, 1, 2, 3)):
            raise ValueError("branch records must retain their fixed original order")
        if any(_values(self.nonbranch)[:22]):
            raise ValueError("nonbranch work contains peaks, not branch event counts")
        for part, native in zip(self.branches, self.native.branch_stats, strict=True):
            event = _native_events(self.native.branch_solver, native, part.feasible)
            if (
                _values(part.work)[:12] != event
                or _values(part.work)[13:22] != _native_work(native)
            ):
                raise ValueError("measured counts do not match retained native diagnostics")
            work = part.work
            if work.atomic_families_examined != work.oracle_calls * work.atomic_families_enumerated:
                raise ValueError("prepared cardinality and query examinations differ")
            if part.feasible != (work.atomic_families_feasible > 0):
                raise ValueError("branch feasibility differs from its native descriptor work")
            if work.oracle_calls == 0 or work.atomic_families_feasible % work.oracle_calls:
                raise ValueError("feasible cover count must remain fixed across queries")
        if self.total != _aggregate((self.nonbranch, *(part.work for part in self.branches))):
            raise ValueError("total must sum events and maximize peaks over every bucket")
        if self.total.peak_numerator_bits < self.output_numerator_bits:
            raise ValueError("output numerator is missing from the recorded peak")
        if self.total.peak_denominator_bits < self.output_denominator_bits:
            raise ValueError("output denominator is missing from the recorded peak")

    @property
    def branch_solver(self) -> str:
        return self.native.branch_solver

    @property
    def attaining_branch(self) -> str:
        return self.native.attaining_candidate


@dataclass(frozen=True, slots=True)
class RunMetadata:
    wall_clock_s: float | None
    python_version: str
    platform: str
    cpu: str | None
    code_version: str
    instance_sha256: str

    def __post_init__(self) -> None:
        if self.wall_clock_s is not None and (
            type(self.wall_clock_s) is not float
            or not isfinite(self.wall_clock_s) or self.wall_clock_s < 0
        ):
            raise ValueError("wall_clock_s must be a supplied finite nonnegative float or None")
        for value in (self.python_version, self.platform, self.code_version, self.instance_sha256):
            if type(value) is not str or not value:
                raise ValueError("metadata text must be a nonempty built-in str")
        if self.cpu is not None and (type(self.cpu) is not str or not self.cpu):
            raise ValueError("cpu must be nonempty text or None")
        if len(self.instance_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.instance_sha256
        ):
            raise ValueError("instance_sha256 must be lower-case 64-digit hexadecimal")


@dataclass(frozen=True, slots=True)
class RunRecord:
    algorithm: AlgorithmStats
    metadata: RunMetadata

    def __post_init__(self) -> None:
        if type(self.algorithm) is not AlgorithmStats or type(self.metadata) is not RunMetadata:
            raise ValueError("run records require exact algorithm and metadata records")


def solve_with_telemetry(
    instance: Instance, branch_solver: str,
) -> tuple[SolveResult, AlgorithmStats]:
    """Measure one legacy call without altering its mathematical or native objects."""
    if type(instance) is not Instance:
        raise ValueError("instance must be an exact Instance")
    if type(branch_solver) is not str or branch_solver not in ("Standard", "Accelerated"):
        raise ValueError("branch_solver must be exactly Standard or Accelerated")
    with _measurement() as recorder:
        _observe_ints(instance.n, len(instance.edges))
        for capacity in instance.f:
            _observe_ints(capacity)
        for left, right, multiplicity in instance.edges:
            _observe_ints(left, right, multiplicity)
        response = solve(instance, branch_solver)
        if type(response) is not tuple or len(response) != 2:
            raise RuntimeError("the legacy solve returned an invalid response shape")
        result, native = response
        if type(result) is not SolveResult or type(native) is not SolveStats:
            raise RuntimeError("the legacy solve returned invalid record types")
        if native.branch_solver != branch_solver or recorder.active_branch is not None:
            raise RuntimeError("the legacy route or observation scope is inconsistent")
        _observe_pair_values(result.value.N, result.value.D)
        empty = result.witness is None
        if (native.attaining_candidate == "Empty") != empty:
            raise RuntimeError("the legacy result and native Empty state differ")
        if empty:
            if recorder.prepared is not None or recorder.visited or native.branch_stats:
                raise RuntimeError("an Empty run must not prepare or execute branches")
        elif recorder.prepared is None or recorder.visited != [0, 1, 2, 3]:
            raise RuntimeError("a nonempty run must prepare once and measure every branch")
        # All record arithmetic below is bookkeeping and cannot affect the completed solve.
        try:
            branch_records = []
            for index, record in enumerate(native.branch_stats):
                feasible = record.oracle_stats.atomic_families_feasible > 0
                peaks = recorder.branches[index]
                work = WorkStats(
                    *_native_events(branch_solver, record, feasible), recorder.prepared[index],
                    *_native_work(record), peaks.numerator, peaks.denominator, peaks.integer,
                )
                branch_records.append(BranchTelemetry(index, feasible, work))
            peaks = recorder.nonbranch
            nonbranch = WorkStats(*((0,) * 22), peaks.numerator, peaks.denominator, peaks.integer)
            branches = tuple(branch_records)
            total = _aggregate((nonbranch, *(part.work for part in branches)))
            stats = AlgorithmStats(
                native, total, nonbranch, branches, _bits(result.value.N), _bits(result.value.D),
            )
        except (ValueError, AttributeError, IndexError, TypeError) as error:
            raise RuntimeError(
                "inconsistent returned diagnostics or observation records"
            ) from error
        return result, stats
