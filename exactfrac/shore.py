"""Finite-universe integer shore masks for ExactFrac."""

from __future__ import annotations

# ORACLE-022 fixes this public export sequence; do not alphabetize it.
__all__ = (  # noqa: RUF022
    "Shore",
    "full_mask",
    "validate_shore",
    "shore_from_list",
    "shore_to_list",
    "shore_complement",
)

Shore = int


def _validate_n(n: object) -> int:
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive built-in int")
    return n


def full_mask(n: int) -> Shore:
    """Return the complete shore mask for the vertex universe ``0..n-1``."""

    checked_n = _validate_n(n)
    return (1 << checked_n) - 1


def validate_shore(n: int, shore: object) -> Shore:
    """Validate and return one finite-universe shore mask unchanged."""

    checked_n = _validate_n(n)
    if type(shore) is not int:
        raise ValueError("shore must be a built-in int")

    maximum = (1 << checked_n) - 1
    if shore < 0 or shore > maximum:
        raise ValueError("shore has a bit outside the vertex universe")

    return shore


def shore_from_list(n: int, vertices: object) -> Shore:
    """Decode one strict increasing vertex-index list into a shore mask."""

    checked_n = _validate_n(n)
    if type(vertices) is not list:
        raise ValueError("serialized shore must be a built-in list")

    shore = 0
    previous = -1

    for vertex in vertices:
        if type(vertex) is not int:
            raise ValueError("shore members must be built-in ints")
        if vertex < 0 or vertex >= checked_n:
            raise ValueError("shore member is outside the vertex universe")
        if vertex <= previous:
            raise ValueError("shore members must be strictly increasing")

        shore |= 1 << vertex
        previous = vertex

    return shore


def shore_to_list(n: int, shore: object) -> list[int]:
    """Encode one valid shore mask as a fresh increasing vertex-index list."""

    checked_n = _validate_n(n)
    checked_shore = validate_shore(checked_n, shore)
    return [vertex for vertex in range(checked_n) if checked_shore & (1 << vertex)]


def shore_complement(n: int, shore: object) -> Shore:
    """Return the complement of a shore relative to its finite vertex universe."""

    checked_n = _validate_n(n)
    checked_shore = validate_shore(checked_n, shore)
    return ((1 << checked_n) - 1) ^ checked_shore
