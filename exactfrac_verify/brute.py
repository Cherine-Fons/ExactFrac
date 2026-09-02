"""Independent exhaustive verifier for tiny canonical ExactFrac instances.

This module is deliberately solver-blind. It accepts already-canonical compact
instance data and evaluates the compact definition directly. It does not
normalize external input records and it does not import from ``exactfrac``.

The brute-force routines are intended only for tiny instances used as
definition-level ground truth.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

Edge = tuple[int, int, int]
RawValue = tuple[int, int]


@dataclass(frozen=True, slots=True)
class BruteInstance:
    """Minimal canonical compact instance for definition-level verification."""

    n: int
    edges: tuple[Edge, ...]
    f: tuple[int, ...]

    def __post_init__(self) -> None:
        """Validate canonical fixture invariants without normalizing raw input."""

        if type(self.n) is not int or self.n < 1:
            raise ValueError("n must be a positive integer")

        if type(self.edges) is not tuple or not self.edges:
            raise ValueError("edges must be a nonempty tuple")

        if type(self.f) is not tuple or len(self.f) != self.n:
            raise ValueError("f must be a tuple of length n")

        for capacity in self.f:
            if type(capacity) is not int or capacity < 1:
                raise ValueError("every f value must be a positive integer")

        previous_pair: tuple[int, int] | None = None

        for edge in self.edges:
            if type(edge) is not tuple or len(edge) != 3:
                raise ValueError("every edge must be a canonical (u, v, q) tuple")

            u, v, multiplicity = edge

            if (
                type(u) is not int
                or type(v) is not int
                or type(multiplicity) is not int
            ):
                raise ValueError("edge entries must be integers")

            if not 0 <= u < v < self.n:
                raise ValueError("edges must satisfy 0 <= u < v < n")

            if multiplicity < 1:
                raise ValueError("edge multiplicity must be positive")

            pair = (u, v)

            if previous_pair is not None and pair <= previous_pair:
                raise ValueError("edges must be strictly ordered with no duplicates")

            previous_pair = pair

    @property
    def degrees(self) -> tuple[int, ...]:
        """Return multiplicity-weighted support degrees."""

        degrees = [0] * self.n

        for u, v, multiplicity in self.edges:
            degrees[u] += multiplicity
            degrees[v] += multiplicity

        return tuple(degrees)

    @property
    def total_multiplicity(self) -> int:
        """Return Q = sum_e q_e."""

        return sum(multiplicity for _, _, multiplicity in self.edges)

    @property
    def full_mask(self) -> int:
        """Return the shore mask containing every vertex."""

        return (1 << self.n) - 1


@dataclass(frozen=True, slots=True)
class Witness:
    """Compact witness consisting only of shore U and dense count vector y."""

    shore: int
    y: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class BruteResult:
    """Exact brute-force optimum and one deterministic attaining witness."""

    value: RawValue
    witness: Witness | None


def _shore_in_range(instance: BruteInstance, shore: int) -> bool:
    return type(shore) is int and 0 <= shore <= instance.full_mask


def _require_valid_shore(instance: BruteInstance, shore: int) -> None:
    if not _shore_in_range(instance, shore):
        raise ValueError("shore contains an out-of-range bit")


def _vertex_inside(shore: int, vertex: int) -> bool:
    return bool(shore & (1 << vertex))


def _edge_crosses(shore: int, u: int, v: int) -> bool:
    return _vertex_inside(shore, u) != _vertex_inside(shore, v)


def _edge_internal(shore: int, u: int, v: int) -> bool:
    return _vertex_inside(shore, u) and _vertex_inside(shore, v)


def _f_shore(instance: BruteInstance, shore: int) -> int:
    return sum(
        instance.f[vertex]
        for vertex in range(instance.n)
        if _vertex_inside(shore, vertex)
    )


def _internal_multiplicity(instance: BruteInstance, shore: int) -> int:
    return sum(
        multiplicity
        for u, v, multiplicity in instance.edges
        if _edge_internal(shore, u, v)
    )


def iter_nonempty_shores(instance: BruteInstance) -> Iterator[int]:
    """Yield all nonempty shores in deterministic increasing-mask order."""

    yield from range(1, instance.full_mask + 1)


def shore_from_list(instance: BruteInstance, vertices: Sequence[int]) -> int:
    """Build a shore bitmask from an explicit vertex-index sequence."""

    shore = 0

    for vertex in vertices:
        if type(vertex) is not int or not 0 <= vertex < instance.n:
            raise ValueError("vertex index is out of range")

        bit = 1 << vertex

        if shore & bit:
            raise ValueError("vertex index appears more than once")

        shore |= bit

    return shore


def shore_to_list(instance: BruteInstance, shore: int) -> list[int]:
    """Serialize a valid shore bitmask as increasing vertex indices."""

    _require_valid_shore(instance, shore)

    return [
        vertex
        for vertex in range(instance.n)
        if _vertex_inside(shore, vertex)
    ]


def shore_complement(instance: BruteInstance, shore: int) -> int:
    """Return the complement relative to the instance vertex universe."""

    _require_valid_shore(instance, shore)
    return instance.full_mask ^ shore


def iter_boundary_y(
    instance: BruteInstance,
    shore: int,
) -> Iterator[tuple[int, ...]]:
    """Yield every dense compact y supported on the shore boundary.

    Noncrossing coordinates are fixed at zero. Crossing coordinate e ranges
    independently over 0..q_e.
    """

    _require_valid_shore(instance, shore)

    choices = []

    for u, v, multiplicity in instance.edges:
        if _edge_crosses(shore, u, v):
            choices.append(range(multiplicity + 1))
        else:
            choices.append((0,))

    for selection in product(*choices):
        yield tuple(selection)


def witness_is_admissible(
    instance: BruteInstance,
    witness: Witness,
) -> bool:
    """Check the compact admissibility conditions directly from the definition."""

    shore = witness.shore
    y = witness.y

    if not _shore_in_range(instance, shore) or shore == 0:
        return False

    if type(y) is not tuple or len(y) != len(instance.edges):
        return False

    selected_total = 0

    for edge_ref, (u, v, multiplicity) in enumerate(instance.edges):
        count = y[edge_ref]

        if type(count) is not int:
            return False

        if _edge_crosses(shore, u, v):
            if not 0 <= count <= multiplicity:
                return False
            selected_total += count
        elif count != 0:
            return False

    admissibility_total = _f_shore(instance, shore) + selected_total

    return admissibility_total >= 3 and admissibility_total % 2 == 1


def witness_raw_value(
    instance: BruteInstance,
    witness: Witness,
) -> RawValue:
    """Return the unreduced witness-attaining pair (N, D).

    This independently re-evaluates the raw formulas used by the production
    contract. Mathematical comparison remains the responsibility of
    ``witness_ratio`` and uses ``Fraction``.
    """

    if not witness_is_admissible(instance, witness):
        raise ValueError("witness is not admissible")

    selected_total = sum(witness.y)
    internal = _internal_multiplicity(instance, witness.shore)

    numerator = 2 * (internal + selected_total)
    denominator = _f_shore(instance, witness.shore) + selected_total - 1

    return numerator, denominator


def witness_ratio(
    instance: BruteInstance,
    witness: Witness,
) -> Fraction:
    """Return the exact mathematical ratio attained by an admissible witness."""

    numerator, denominator = witness_raw_value(instance, witness)
    return Fraction(numerator, denominator)


def brute_force(instance: BruteInstance) -> BruteResult:
    """Return the exact compact optimum and first maximizing witness encountered.

    Enumeration order is deterministic:

    1. increasing nonempty shore masks;
    2. dense boundary counts in canonical edge order, with the final coordinate
       changing fastest under ``itertools.product``.

    Equal objective values do not replace the incumbent.
    """

    best_ratio: Fraction | None = None
    best_result: BruteResult | None = None

    for shore in iter_nonempty_shores(instance):
        for y in iter_boundary_y(instance, shore):
            witness = Witness(shore=shore, y=y)

            if not witness_is_admissible(instance, witness):
                continue

            raw_value = witness_raw_value(instance, witness)
            ratio = Fraction(*raw_value)

            if best_ratio is None or ratio > best_ratio:
                best_ratio = ratio
                best_result = BruteResult(
                    value=raw_value,
                    witness=witness,
                )

    if best_result is None:
        return BruteResult(
            value=(0, 1),
            witness=None,
        )

    return best_result