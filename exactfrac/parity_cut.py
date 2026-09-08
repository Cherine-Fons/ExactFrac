"""Exact forced-family contraction and reference parity-cut minimization.

Original preimages, reduced problem shores, and ordinary-query shores have
separate vertex universes. Only ordinary queries use the closed flow backend.
"""

from __future__ import annotations

from dataclasses import dataclass

from .families import AtomicFamily
from .flow import minimum_cut
from .shore import validate_shore
from .sign_routing import SignRoutedNetwork

__all__ = (
    "ParityCutProblem",
    "ParityCutResult",
    "ParityCutStats",
    "lift_source_shore",
    "minimum_parity_cut",
    "reduce_atomic_family",
)


def _require_nonnegative_int(value: object, name: str) -> None:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative built-in int")


def _validate_classes(vertex_count: int, classes: tuple[int, ...]) -> None:
    if type(classes) is not tuple or len(classes) < 2:
        raise ValueError("classes must be a built-in tuple with at least two entries")
    original_full = (1 << vertex_count) - 1
    source_bit = 1 << vertex_count
    sink_bit = 1 << (vertex_count + 1)
    anchor_bit = 1 << (vertex_count + 2)
    augmented_full = (1 << (vertex_count + 3)) - 1
    covered = 0
    previous_singleton = 0
    for index, group in enumerate(classes):
        if type(group) is not int or group <= 0 or group > augmented_full:
            raise ValueError("each class must be a positive finite built-in int mask")
        if group & covered:
            raise ValueError("class preimages must be disjoint")
        if index >= 2:
            if group > original_full or group.bit_count() != 1 or group <= previous_singleton:
                raise ValueError("free classes must be increasing original-vertex singletons")
            previous_singleton = group
        covered |= group
    if not classes[0] & source_bit or classes[0] & sink_bit:
        raise ValueError("class zero must contain original source and exclude original sink")
    if not classes[1] & sink_bit or classes[1] & (source_bit | anchor_bit):
        raise ValueError("class one must contain original sink and exclude source and anchor")
    required = (1 << (vertex_count + 2)) - 1
    if covered & required != required:
        raise ValueError("classes must cover all original vertices and fixed terminals")


def _validate_arcs(node_count: int, arcs: tuple[tuple[int, int, int], ...]) -> None:
    if type(arcs) is not tuple:
        raise ValueError("arcs must be a built-in tuple")
    previous = (-1, -1)
    for arc in arcs:
        if type(arc) is not tuple or len(arc) != 3:
            raise ValueError("each arc must be a built-in three-tuple")
        tail, head, capacity = arc
        if type(tail) is not int or type(head) is not int or type(capacity) is not int:
            raise ValueError("all arc entries must be built-in ints")
        if not 0 <= tail < node_count or not 0 <= head < node_count or tail == head:
            raise ValueError("arc endpoints must be distinct reduced vertices")
        if capacity < 0:
            raise ValueError("arc capacity must be nonnegative")
        key = (tail, head)
        if key <= previous:
            raise ValueError("arc endpoint pairs must be strictly increasing")
        previous = key


@dataclass(frozen=True, slots=True)
class ParityCutProblem:
    """Validated reduced directed graph with canonical original-preimage classes."""

    vertex_count: int
    classes: tuple[int, ...]
    arcs: tuple[tuple[int, int, int], ...]
    terminal_mask: int

    def __post_init__(self) -> None:
        if type(self.vertex_count) is not int or self.vertex_count < 1:
            raise ValueError("vertex_count must be a positive built-in int")
        _validate_classes(self.vertex_count, self.classes)
        _validate_arcs(self.node_count, self.arcs)
        _require_nonnegative_int(self.terminal_mask, "terminal_mask")
        if self.terminal_mask.bit_length() > self.node_count or self.terminal_mask.bit_count() & 1:
            raise ValueError("terminal_mask must be finite and have even cardinality")

    @property
    def source(self) -> int:
        return 0

    @property
    def sink(self) -> int:
        return 1

    @property
    def node_count(self) -> int:
        return len(self.classes)


@dataclass(frozen=True, slots=True)
class ParityCutResult:
    """Unshifted cut value and source shore in reduced-problem coordinates."""

    cut_value: int
    source_shore: int

    def __post_init__(self) -> None:
        _require_nonnegative_int(self.cut_value, "cut_value")
        _require_nonnegative_int(self.source_shore, "source_shore")
        if not self.source_shore & 1 or self.source_shore & 2:
            raise ValueError("source_shore must contain source and exclude sink")


@dataclass(frozen=True, slots=True)
class ParityCutStats:
    """Separate exact call count and aggregates of flow-only diagnostics."""

    mincut_calls: int
    flow_augmentations: int
    flow_bfs_scans: int
    flow_peak_generated_value: int

    def __post_init__(self) -> None:
        _require_nonnegative_int(self.mincut_calls, "mincut_calls")
        _require_nonnegative_int(self.flow_augmentations, "flow_augmentations")
        _require_nonnegative_int(self.flow_bfs_scans, "flow_bfs_scans")
        _require_nonnegative_int(self.flow_peak_generated_value, "flow_peak_generated_value")


def _preimage_map(classes: tuple[int, ...], universe_size: int) -> list[int]:
    """Map each partition member once; work is linear in the explicit universe."""
    mapping = [0] * universe_size
    for index, group in enumerate(classes):
        remaining = group
        while remaining:
            bit = remaining & -remaining
            mapping[bit.bit_length() - 1] = index
            remaining ^= bit
    return mapping


def _transport_arcs(
    arcs: tuple[tuple[int, int, int], ...], mapping: list[int],
) -> tuple[tuple[int, int, int], ...]:
    """Drop mapped loops; sort and sum encountered pairs, including zero pairs."""
    mapped = []
    for tail, head, capacity in arcs:
        new_tail, new_head = mapping[tail], mapping[head]
        if new_tail != new_head:
            mapped.append((new_tail, new_head, capacity))
    mapped.sort()
    merged: list[tuple[int, int, int]] = []
    for tail, head, capacity in mapped:
        if merged and merged[-1][:2] == (tail, head):
            merged[-1] = (tail, head, merged[-1][2] + capacity)
        else:
            merged.append((tail, head, capacity))
    return tuple(merged)


def _lift_classes(classes: tuple[int, ...], source_shore: int) -> int:
    """Lift a valid class-index mask to the universe of its preimages."""
    lifted = 0
    for index, group in enumerate(classes):
        if source_shore & (1 << index):
            lifted |= group
    return lifted


def reduce_atomic_family(
    network: SignRoutedNetwork, family: AtomicFamily,
) -> ParityCutProblem | None:
    """Contract a feasible finite atomic family without changing cut values."""
    if type(network) is not SignRoutedNetwork:
        raise ValueError("network must be an exact SignRoutedNetwork")
    if type(family) is not AtomicFamily:
        raise ValueError("family must be an exact AtomicFamily")
    n = network.vertex_count
    validate_shore(n, family.T)
    validate_shore(n, family.I)
    validate_shore(n, family.O)
    if not family.is_nonempty:
        return None

    source_group = family.I | (1 << n)
    sink_group = family.O | (1 << (n + 1))
    tokens = family.T
    if family.pi == 0:
        anchor = 1 << (n + 2)
        source_group |= anchor
        tokens |= anchor
    groups = [source_group, sink_group]
    occupied = family.I | family.O
    for vertex in range(n):
        bit = 1 << vertex
        if not occupied & bit:
            groups.append(bit)
    classes = tuple(groups)
    mapping = _preimage_map(classes, n + 3)
    arcs = _transport_arcs(network.arcs, mapping)
    terminal_mask = 0
    for index, group in enumerate(classes):
        if (group & tokens).bit_count() & 1:
            terminal_mask |= 1 << index
    if terminal_mask.bit_count() & 1:
        terminal_mask ^= 2
    return ParityCutProblem(n, classes, arcs, terminal_mask)


def lift_source_shore(problem: ParityCutProblem, source_shore: int) -> int:
    """Lift either parity of reduced source shore and discard auxiliary bits."""
    if type(problem) is not ParityCutProblem:
        raise ValueError("problem must be an exact ParityCutProblem")
    validate_shore(problem.node_count, source_shore)
    if not source_shore & 1 or source_shore & 2:
        raise ValueError("source_shore must contain source and exclude sink")
    return _lift_classes(problem.classes, source_shore) & ((1 << problem.vertex_count) - 1)


def _pair_classes(node_count: int, inside: int, outside: int) -> tuple[int, ...]:
    """Preimages in problem coordinates for one ordinary two-element query."""
    groups = [1 | (1 << inside), 2 | (1 << outside)]
    for vertex in range(2, node_count):
        if vertex not in (inside, outside):
            groups.append(1 << vertex)
    return tuple(groups)


def minimum_parity_cut(
    problem: ParityCutProblem,
) -> tuple[ParityCutResult | None, ParityCutStats]:
    """Process all compatible GR pairs using the closed least ordinary cuts.

    One temporary graph is processed at a time. Values are unshifted; selection
    uses strict improvement only, independently of the aggregated diagnostics.
    """
    if type(problem) is not ParityCutProblem:
        raise ValueError("problem must be an exact ParityCutProblem")
    if problem.terminal_mask == 0:
        return None, ParityCutStats(0, 0, 0, 0)

    node_count = problem.node_count
    best: ParityCutResult | None = None
    calls = augmentations = scans = peak = 0
    for inside in range(node_count):
        if inside == 1:
            continue
        for outside in range(1, node_count):
            if inside == outside:
                continue
            classes = _pair_classes(node_count, inside, outside)
            mapping = _preimage_map(classes, node_count)
            arcs = _transport_arcs(problem.arcs, mapping)
            ordinary = minimum_cut(len(classes), 0, 1, arcs)
            calls += 1
            augmentations += ordinary.stats.augmentations
            scans += ordinary.stats.bfs_scans
            peak = max(peak, ordinary.stats.peak_generated_value)
            lifted = _lift_classes(classes, ordinary.source_shore)
            if ((lifted & problem.terminal_mask).bit_count() & 1) and (
                best is None or ordinary.value < best.cut_value
            ):
                best = ParityCutResult(ordinary.value, lifted)
    if best is None:
        raise RuntimeError("nonzero even terminals produced no parity candidate")
    return best, ParityCutStats(calls, augmentations, scans, peak)
