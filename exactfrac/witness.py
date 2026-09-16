"""Immutable witness records and exact witness evaluation for ExactFrac."""

from __future__ import annotations

from dataclasses import dataclass

from ._telemetry import _observe_ints, _observe_pair_values, _tap_int
from .instance import Instance
from .shore import validate_shore

__all__ = (
    "ExactValue",
    "Witness",
    "dense_y_to_sparse",
    "shore_b_q",
    "shore_d_q",
    "shore_e_q",
    "shore_f",
    "sparse_y_to_dense",
    "validate_witness",
    "witness_value",
)


@dataclass(frozen=True, slots=True)
class ExactValue:
    """One raw unreduced numerator-denominator record."""

    N: int
    D: int

    def __post_init__(self) -> None:
        if type(self.N) is not int:
            raise ValueError("N must be a built-in int")
        if type(self.D) is not int or self.D <= 0:
            raise ValueError("D must be a positive built-in int")


@dataclass(frozen=True, slots=True)
class Witness:
    """One immutable compact witness record ``(U, y)``."""

    U: int
    y: tuple[int, ...]

    def __post_init__(self) -> None:
        if type(self.U) is not int or self.U <= 0:
            raise ValueError("U must be a positive built-in int")
        if type(self.y) is not tuple:
            raise ValueError("y must be an exact tuple")
        for count in self.y:
            if type(count) is not int or count < 0:
                raise ValueError("every y coordinate must be a nonnegative built-in int")


def _require_instance(instance: object) -> Instance:
    if type(instance) is not Instance:
        raise ValueError("instance must be an exact production Instance")
    return instance


def _checked_instance_shore(instance: object, U: object) -> tuple[Instance, int]:
    checked_instance = _require_instance(instance)
    checked_shore = validate_shore(checked_instance.n, U)
    return checked_instance, checked_shore


def _crosses(U: int, left: int, right: int) -> bool:
    return bool(_tap_int(U & (_tap_int(1 << left)))) != bool(_tap_int(U & (_tap_int(1 << right))))


def _validate_dense(
    instance: Instance,
    U: int,
    y: object,
) -> tuple[int, ...]:
    if type(y) is not tuple or _tap_int(len(y)) != instance.m:
        raise ValueError("dense y must be an exact tuple of length m")

    # Shape validation precedes every graph-dependent bound/boundary check.
    for count in y:
        if type(count) is not int or count < 0:
            raise ValueError("every dense y coordinate must be a nonnegative built-in int")

    for edge_ref, (left, right, multiplicity) in enumerate(instance.edges):
        _observe_ints(edge_ref)
        count = y[edge_ref]
        if count > multiplicity:
            raise ValueError("dense y coordinate exceeds edge multiplicity")
        if not _crosses(U, left, right) and count != 0:
            raise ValueError("nonboundary dense y coordinates must be zero")

    return y


def shore_f(instance: Instance, U: int) -> int:
    """Return ``f(U)`` for one valid shore, including the empty shore."""

    checked_instance, checked_shore = _checked_instance_shore(instance, U)
    total = 0
    for vertex in range(_tap_int(checked_instance.n)):
        if _tap_int(checked_shore & (_tap_int(1 << vertex))):
            total += checked_instance.f[vertex]
            _observe_ints(total)
    return total


def shore_e_q(instance: Instance, U: int) -> int:
    """Return the internal compact multiplicity ``e_q(U)``."""

    checked_instance, checked_shore = _checked_instance_shore(instance, U)
    total = 0
    for left, right, multiplicity in checked_instance.edges:
        if (
            _tap_int(checked_shore & (_tap_int(1 << left)))
            and _tap_int(checked_shore & (_tap_int(1 << right)))
        ):
            total += multiplicity
            _observe_ints(total)
    return total


def shore_b_q(instance: Instance, U: int) -> int:
    """Return the boundary compact multiplicity ``b_q(U)``."""

    checked_instance, checked_shore = _checked_instance_shore(instance, U)
    total = 0
    for left, right, multiplicity in checked_instance.edges:
        if _crosses(checked_shore, left, right):
            total += multiplicity
            _observe_ints(total)
    return total


def shore_d_q(instance: Instance, U: int) -> int:
    """Return the multiplicity-weighted degree sum ``d_q(U)``."""

    checked_instance, checked_shore = _checked_instance_shore(instance, U)
    degrees = checked_instance.d_q
    total = 0
    for vertex in range(_tap_int(checked_instance.n)):
        if _tap_int(checked_shore & (_tap_int(1 << vertex))):
            total += degrees[vertex]
            _observe_ints(total)
    return total


def dense_y_to_sparse(
    instance: Instance,
    U: int,
    y: tuple[int, ...],
) -> list[list[int]]:
    """Encode a valid boundary selection, not full admissibility or attainment.

    The empty and full shores accept only zero counts. An empty sparse result
    means zero selected copies, not an empty admissible family.
    """

    checked_instance, checked_shore = _checked_instance_shore(instance, U)
    checked_y = _validate_dense(checked_instance, checked_shore, y)
    return [
        [edge_ref, count]
        for edge_ref, count in enumerate(checked_y)
        if count > 0
    ]


def sparse_y_to_dense(
    instance: Instance,
    U: int,
    entries: list[list[int]],
) -> tuple[int, ...]:
    """Decode a valid boundary selection, not full admissibility or attainment.

    Records must already be canonical. No sorting, merging, or coercion is
    performed. Missing references decode to zero; [] is not an Empty result.
    """

    checked_instance, checked_shore = _checked_instance_shore(instance, U)
    if type(entries) is not list:
        raise ValueError("sparse y must be an exact list")

    previous = -1

    for record in entries:
        if type(record) is not list or len(record) != 2:
            raise ValueError("each sparse y record must be an exact two-entry list")

        edge_ref, count = record
        if type(edge_ref) is not int or type(count) is not int:
            raise ValueError("sparse y values must be built-in ints")
        if edge_ref < 0 or edge_ref >= checked_instance.m:
            raise ValueError("sparse y edge_ref is outside canonical edge order")
        if edge_ref <= previous:
            raise ValueError("sparse y edge_ref values must be strictly increasing")
        if count <= 0:
            raise ValueError("sparse y counts must be strictly positive")

        left, right, multiplicity = checked_instance.edges[edge_ref]
        if count > multiplicity:
            raise ValueError("sparse y count exceeds edge multiplicity")
        if not _crosses(checked_shore, left, right):
            raise ValueError("sparse y may reference only boundary edges")

        previous = edge_ref

    # Build the output only after every supplied record has been validated.
    dense = [0] * checked_instance.m
    for edge_ref, count in entries:
        dense[edge_ref] = count
    return tuple(dense)


def validate_witness(instance: Instance, witness: Witness) -> None:
    """Validate one compact witness against an exact production instance."""

    checked_instance = _require_instance(instance)
    if type(witness) is not Witness:
        raise ValueError("witness must be an exact Witness")

    checked_shore = validate_shore(checked_instance.n, witness.U)
    if checked_shore == 0:
        raise ValueError("a witness shore must be nonempty")
    _validate_dense(checked_instance, checked_shore, witness.y)

    total = _tap_int(shore_f(checked_instance, checked_shore) + _tap_int(sum(witness.y)))
    if _tap_int(total % 2) == 0:
        raise ValueError("witness admissibility total must be odd")
    if total < 3:
        raise ValueError("witness admissibility total must be at least three")


def witness_value(instance: Instance, witness: Witness) -> ExactValue:
    """Return the literal raw value attained by one admissible compact witness."""

    checked_instance = _require_instance(instance)
    if type(witness) is not Witness:
        raise ValueError("witness must be an exact Witness")

    validate_witness(checked_instance, witness)
    selected = _tap_int(sum(witness.y))
    numerator = _tap_int(2 * (_tap_int(shore_e_q(checked_instance, witness.U) + selected)))
    denominator = _tap_int(_tap_int(shore_f(checked_instance, witness.U) + selected) - 1)
    _observe_pair_values(numerator, denominator)
    return ExactValue(numerator, denominator)
