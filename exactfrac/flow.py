"""Exact directed Edmonds--Karp minimum-cut reference backend.

The public entry point accepts a directed network with exact nonnegative integer
capacities and returns the exact minimum-cut value together with the
inclusionwise-minimal minimum source shore. The implementation fixes every
normalization and residual-adjacency order so results and structural counters
are deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass

Arc = tuple[int, int, int]

__all__ = ["FlowStats", "MinCutResult", "minimum_cut"]


@dataclass(frozen=True, slots=True)
class FlowStats:
    """Immutable deterministic diagnostics for one minimum-cut computation."""

    augmentations: int
    bfs_scans: int
    peak_generated_value: int


@dataclass(frozen=True, slots=True)
class MinCutResult:
    """Exact directed minimum-cut result."""

    value: int
    source_shore: int
    stats: FlowStats


@dataclass(slots=True)
class _ResidualEntry:
    """One mutable directed entry in the private residual network."""

    head: int
    reverse_index: int
    capacity: int


def _require_exact_int(value: object, name: str) -> int:
    """Return ``value`` after enforcing the flow-local exact-integer rule."""

    if type(value) is not int:
        raise TypeError(f"{name} must be an exact int")
    return value


def _validate_and_normalize(
    n: object,
    source: object,
    sink: object,
    arcs: object,
) -> tuple[int, int, int, tuple[Arc, ...]]:
    """Validate, discard loops, sort raw nonloops, and aggregate parallel arcs.

    For ``E_in`` supplied records, normalization uses
    ``O(E_in log(E_in + 1))`` comparisons and ``O(E_in)`` exact additions. The
    returned ``E`` arcs are the canonical nonloop ordered pairs consumed by the
    residual backend.
    """

    checked_n = _require_exact_int(n, "n")
    checked_source = _require_exact_int(source, "source")
    checked_sink = _require_exact_int(sink, "sink")

    if checked_n < 2:
        raise ValueError("n must be at least two")
    if not 0 <= checked_source < checked_n:
        raise ValueError("source is out of range")
    if not 0 <= checked_sink < checked_n:
        raise ValueError("sink is out of range")
    if checked_source == checked_sink:
        raise ValueError("source and sink must be distinct")

    if type(arcs) is not tuple:
        raise TypeError("arcs must be a tuple")

    nonloop_records: list[Arc] = []

    for arc in arcs:
        if type(arc) is not tuple:
            raise TypeError("every arc must be a tuple")
        if len(arc) != 3:
            raise ValueError("every arc must have exactly three entries")

        raw_tail, raw_head, raw_capacity = arc
        tail = _require_exact_int(raw_tail, "arc tail")
        head = _require_exact_int(raw_head, "arc head")
        capacity = _require_exact_int(raw_capacity, "capacity")

        if not 0 <= tail < checked_n:
            raise ValueError("arc tail is out of range")
        if not 0 <= head < checked_n:
            raise ValueError("arc head is out of range")
        if capacity < 0:
            raise ValueError("capacity must be nonnegative")

        if tail != head:
            nonloop_records.append((tail, head, capacity))

    nonloop_records.sort()
    normalized: list[Arc] = []

    for tail, head, capacity in nonloop_records:
        if normalized and normalized[-1][:2] == (tail, head):
            previous_capacity = normalized[-1][2]
            normalized[-1] = (tail, head, previous_capacity + capacity)
        else:
            normalized.append((tail, head, capacity))

    return checked_n, checked_source, checked_sink, tuple(normalized)


def minimum_cut(
    n: int,
    source: int,
    sink: int,
    arcs: tuple[Arc, ...],
) -> MinCutResult:
    """Return the exact inclusionwise-minimal directed minimum source shore.

    Each canonical original arc contributes a forward residual entry followed
    by its paired reverse entry. Breadth-first searches scan those entries in
    fixed insertion order, mark vertices on first discovery, and stop when the
    sink is first discovered. The first failed search runs to exhaustion and
    supplies the returned minimum source shore without a second search.

    The normalized ``E = 0`` branch performs no breadth-first search. For
    canonical positive-arc input, the Edmonds--Karp phase uses
    ``O(N + N E^2)`` arithmetic and comparison operations. Search records and
    the queue are initialized once; epochs avoid an ``O(N)`` reset per search.
    """

    checked_n, checked_source, checked_sink, normalized = _validate_and_normalize(
        n,
        source,
        sink,
        arcs,
    )

    if not normalized:
        return MinCutResult(
            value=0,
            source_shore=1 << checked_source,
            stats=FlowStats(
                augmentations=0,
                bfs_scans=0,
                peak_generated_value=0,
            ),
        )

    adjacency: list[list[_ResidualEntry]] = [[] for _ in range(checked_n)]
    peak_generated_value = 0

    for tail, head, capacity in normalized:
        forward_index = len(adjacency[tail])
        reverse_index = len(adjacency[head])

        adjacency[tail].append(
            _ResidualEntry(
                head=head,
                reverse_index=reverse_index,
                capacity=capacity,
            )
        )
        adjacency[head].append(
            _ResidualEntry(
                head=tail,
                reverse_index=forward_index,
                capacity=0,
            )
        )

        if capacity > peak_generated_value:
            peak_generated_value = capacity

    seen_epoch = [0] * checked_n
    parent_vertex = [0] * checked_n
    parent_entry = [0] * checked_n
    queue = [0] * checked_n

    epoch = 0
    bfs_scans = 0
    augmentations = 0
    value = 0
    source_shore = 0

    def search() -> tuple[bool, int]:
        """Find one shortest residual path or return the reached-vertex count."""

        nonlocal bfs_scans, epoch

        epoch += 1
        queue_head = 0
        queue_tail = 1
        queue[0] = checked_source
        seen_epoch[checked_source] = epoch

        while queue_head < queue_tail:
            vertex = queue[queue_head]
            queue_head += 1

            for entry_index, entry in enumerate(adjacency[vertex]):
                bfs_scans += 1

                if entry.capacity <= 0 or seen_epoch[entry.head] == epoch:
                    continue

                seen_epoch[entry.head] = epoch
                parent_vertex[entry.head] = vertex
                parent_entry[entry.head] = entry_index

                if entry.head == checked_sink:
                    return True, queue_tail

                queue[queue_tail] = entry.head
                queue_tail += 1

        return False, queue_tail

    while True:
        found, reached_count = search()

        if not found:
            for reached_index in range(reached_count):
                source_shore |= 1 << queue[reached_index]
            break

        vertex = checked_sink
        previous = parent_vertex[vertex]
        entry = adjacency[previous][parent_entry[vertex]]
        bottleneck = entry.capacity
        vertex = previous

        while vertex != checked_source:
            previous = parent_vertex[vertex]
            entry = adjacency[previous][parent_entry[vertex]]

            if entry.capacity < bottleneck:
                bottleneck = entry.capacity

            vertex = previous

        if bottleneck > peak_generated_value:
            peak_generated_value = bottleneck

        vertex = checked_sink

        while vertex != checked_source:
            previous = parent_vertex[vertex]
            entry = adjacency[previous][parent_entry[vertex]]
            reverse = adjacency[entry.head][entry.reverse_index]

            entry.capacity -= bottleneck
            reverse.capacity += bottleneck

            if entry.capacity > peak_generated_value:
                peak_generated_value = entry.capacity
            if reverse.capacity > peak_generated_value:
                peak_generated_value = reverse.capacity

            vertex = previous

        value += bottleneck
        augmentations += 1

        if value > peak_generated_value:
            peak_generated_value = value

    return MinCutResult(
        value=value,
        source_shore=source_shore,
        stats=FlowStats(
            augmentations=augmentations,
            bfs_scans=bfs_scans,
            peak_generated_value=peak_generated_value,
        ),
    )
