"""Exact raw rational-pair primitives for the production solver."""

from __future__ import annotations

from ._telemetry import _observe_pair_values, _tap_int, _tap_numerator, _tap_pair

RawPair = tuple[int, int]

__all__ = (
    "RawPair",
    "compare_pairs",
    "make_pair",
    "pair_add_one",
    "pair_reflect",
    "pair_sign",
    "residual_numerator",
    "validate_pair",
)


def _require_exact_int(value: object) -> int:
    if type(value) is not int:
        raise ValueError("expected an exact built-in int")
    return value


def make_pair(numerator: int, denominator: int) -> RawPair:
    """Construct a raw pair with a strictly positive denominator."""
    checked_numerator = _require_exact_int(numerator)
    checked_denominator = _require_exact_int(denominator)
    if checked_denominator <= 0:
        raise ValueError("denominator must be positive")
    return _tap_pair((checked_numerator, checked_denominator))


def validate_pair(pair: RawPair) -> None:
    """Validate the exact raw-pair representation."""
    if type(pair) is not tuple or _tap_int(len(pair)) != 2:
        raise ValueError("pair must be an exact two-element tuple")

    numerator, denominator = pair
    _require_exact_int(numerator)
    checked_denominator = _require_exact_int(denominator)

    if checked_denominator <= 0:
        raise ValueError("denominator must be positive")
    _observe_pair_values(numerator, checked_denominator)


def compare_pairs(left: RawPair, right: RawPair) -> int:
    """Compare two represented rational values by exact cross multiplication."""
    validate_pair(left)
    validate_pair(right)

    left_numerator, left_denominator = left
    right_numerator, right_denominator = right

    left_cross = _tap_int(left_numerator * right_denominator)
    right_cross = _tap_int(right_numerator * left_denominator)
    return _tap_int((left_cross > right_cross) - (left_cross < right_cross))


def pair_sign(pair: RawPair) -> int:
    """Return the exact sign of a valid raw pair."""
    validate_pair(pair)
    numerator = pair[0]
    return (numerator > 0) - (numerator < 0)


def pair_add_one(pair: RawPair) -> RawPair:
    """Return the literal unreduced raw pair representing pair + 1."""
    validate_pair(pair)
    numerator, denominator = pair
    return _tap_pair((_tap_int(numerator + denominator), denominator))


def pair_reflect(newton: RawPair, current: RawPair) -> RawPair:
    """Return the literal raw pair for 2*newton - current."""
    validate_pair(newton)
    validate_pair(current)

    newton_numerator, newton_denominator = newton
    current_numerator, current_denominator = current

    return _tap_pair((
        _tap_int(_tap_int(_tap_int(2 * newton_numerator) * current_denominator)
        - _tap_int(current_numerator * newton_denominator)),
        _tap_int(newton_denominator * current_denominator),
    ))


def residual_numerator(parameter: RawPair, c: int, h: int) -> int:
    """Return the exact numerator B*c - A*h at parameter A/B."""
    validate_pair(parameter)
    checked_c = _require_exact_int(c)
    checked_h = _require_exact_int(h)

    numerator, denominator = parameter
    return _tap_numerator(
        _tap_int(_tap_int(denominator * checked_c) - _tap_int(numerator * checked_h)), denominator,
    )
