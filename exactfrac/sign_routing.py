"""Exact branch coefficients and uncontracted nonnegative sign-routing networks."""

from __future__ import annotations

from dataclasses import dataclass

from ._telemetry import _observe_ints, _tap_int
from .instance import Instance
from .rational import RawPair, validate_pair

__all__ = (
    "SignRoutedNetwork",
    "SignRoutingCoefficients",
    "branch_coefficients",
    "build_sign_routed_network",
    "recover_objective",
)


def _require_int(value: object, name: str) -> None:
    """Reject non-integer objects without invoking their conversion hooks."""
    if type(value) is not int:
        raise ValueError(f"{name} must be an exact built-in int")


@dataclass(frozen=True, slots=True)
class SignRoutingCoefficients:
    """Literal coefficients of a cut term, vertex terms, and a separate constant."""

    a: int
    gamma: tuple[int, ...]
    constant: int

    def __post_init__(self) -> None:
        _require_int(self.a, "a")
        if self.a < 0:
            raise ValueError("a must be nonnegative")
        if type(self.gamma) is not tuple:
            raise ValueError("gamma must be an exact tuple")
        for coefficient in self.gamma:
            _require_int(coefficient, "gamma entry")
        _require_int(self.constant, "constant")


@dataclass(frozen=True, slots=True)
class SignRoutedNetwork:
    """Immutable original capacity arcs; construction alone asserts no provenance."""

    vertex_count: int
    arcs: tuple[tuple[int, int, int], ...]
    negative_shift: int
    constant: int

    def __post_init__(self) -> None:
        _require_int(self.vertex_count, "vertex_count")
        if self.vertex_count < 1:
            raise ValueError("vertex_count must be positive")
        if type(self.arcs) is not tuple:
            raise ValueError("arcs must be an exact tuple")
        node_count = self.vertex_count + 2
        for arc in self.arcs:
            if type(arc) is not tuple or len(arc) != 3:
                raise ValueError("each arc must be an exact three-element tuple")
            tail, head, capacity = arc
            _require_int(tail, "arc tail")
            _require_int(head, "arc head")
            _require_int(capacity, "arc capacity")
            if not 0 <= tail < node_count or not 0 <= head < node_count:
                raise ValueError("arc endpoint is outside the network")
            if tail == head:
                raise ValueError("self-loops are not valid network records")
            if capacity < 0:
                raise ValueError("arc capacity must be nonnegative")
        _require_int(self.negative_shift, "negative_shift")
        if self.negative_shift < 0:
            raise ValueError("negative_shift must be nonnegative")
        _require_int(self.constant, "constant")

    @property
    def node_count(self) -> int:
        """Return the original vertex count plus the two fixed terminals."""
        return self.vertex_count + 2

    @property
    def source(self) -> int:
        """Return the fixed source index."""
        return self.vertex_count

    @property
    def sink(self) -> int:
        """Return the fixed sink index."""
        return self.vertex_count + 1


def branch_coefficients(
    instance: Instance,
    branch: int,
    parameter: RawPair,
) -> SignRoutingCoefficients:
    """Expand the selected raw branch residual without checking shore feasibility."""
    if type(instance) is not Instance:
        raise ValueError("instance must be an exact production Instance")
    _require_int(branch, "branch")
    if branch not in (0, 1, 2, 3):
        raise ValueError("branch must be 0, 1, 2, or 3")
    validate_pair(parameter)

    numerator, denominator = parameter
    degrees = instance.d_q
    _observe_ints(instance.n)
    if branch < 2:
        combined = _tap_int(numerator + denominator)
        gamma = tuple(
            _tap_int(
                _tap_int(combined * instance.f[vertex]) - _tap_int(numerator * degrees[vertex])
            )
            for vertex in range(instance.n)
        )
        constant = _tap_int(-combined) if branch == 0 else _tap_int(_tap_int(-2) * denominator)
    else:
        gamma = tuple(
            _tap_int(
                _tap_int(_tap_int(-denominator) * degrees[vertex])
                - _tap_int(numerator * instance.f[vertex])
            )
            for vertex in range(instance.n)
        )
        constant = numerator if branch == 2 else _tap_int(_tap_int(-2) * denominator)
    return SignRoutingCoefficients(denominator, gamma, constant)


def build_sign_routed_network(
    instance: Instance,
    coefficients: SignRoutingCoefficients,
) -> SignRoutedNetwork:
    """Emit support pairs then vertex-order spoke pairs, retaining every zero arc."""
    if type(instance) is not Instance:
        raise ValueError("instance must be an exact production Instance")
    if type(coefficients) is not SignRoutingCoefficients:
        raise ValueError("coefficients must be an exact SignRoutingCoefficients")
    if _tap_int(len(coefficients.gamma)) != instance.n:
        raise ValueError("gamma length must equal the original vertex count")

    source = instance.n
    sink = _tap_int(source + 1)
    arcs: list[tuple[int, int, int]] = []
    for u, v, multiplicity in instance.edges:
        capacity = _tap_int(coefficients.a * multiplicity)
        arcs.append((u, v, capacity))
        arcs.append((v, u, capacity))

    negative_shift = 0
    for vertex, coefficient in enumerate(coefficients.gamma):
        _observe_ints(vertex)
        if coefficient >= 0:
            arcs.append((vertex, sink, coefficient))
            arcs.append((sink, vertex, coefficient))
        else:
            capacity = _tap_int(-coefficient)
            arcs.append((source, vertex, capacity))
            arcs.append((vertex, source, capacity))
            negative_shift += capacity
            _observe_ints(negative_shift)

    return SignRoutedNetwork(instance.n, tuple(arcs), negative_shift, coefficients.constant)


def recover_objective(network: SignRoutedNetwork, cut_value: int) -> int:
    """Remove the routing shift and add the constant; assert no cut or minimum."""
    if type(network) is not SignRoutedNetwork:
        raise ValueError("network must be an exact SignRoutedNetwork")
    _require_int(cut_value, "cut_value")
    if cut_value < 0:
        raise ValueError("cut_value must be nonnegative")
    return _tap_int(_tap_int(cut_value - network.negative_shift) + network.constant)
