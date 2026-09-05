"""Deterministic atomic-family descriptors for ExactFrac branch domains."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .instance import Instance
from .shore import validate_shore

__all__ = (
    "AtomicFamily",
    "enumerate_atomic_families",
)


@dataclass(frozen=True, slots=True)
class AtomicFamily:
    """One immutable family descriptor ``F(T, pi; I, O)``."""

    T: int
    pi: int
    # DESIGN section 4.3A.2 fixes these source-faithful field names.
    I: int  # noqa: E741
    O: int  # noqa: E741

    def __post_init__(self) -> None:
        for value in (self.T, self.I, self.O):
            if type(value) is not int or value < 0:
                raise ValueError("family masks must be nonnegative built-in ints")

        if type(self.pi) is not int or self.pi not in (0, 1):
            raise ValueError("family parity must be the built-in int 0 or 1")

    @property
    def is_nonempty(self) -> bool:
        """Return whether at least one shore satisfies this descriptor."""

        if self.I & self.O:
            return False

        occupied_terminals = self.T & (self.I | self.O)
        free_terminals = self.T ^ occupied_terminals
        forced_parity = (self.I & self.T).bit_count() & 1
        return bool(free_terminals) or forced_parity == self.pi


def _checked_family(
    n: int,
    terminal: int,
    parity: int,
    forced_in: int,
    forced_out: int,
) -> AtomicFamily:
    """Construct one generated descriptor after universe-range validation."""

    validate_shore(n, terminal)
    validate_shore(n, forced_in)
    validate_shore(n, forced_out)
    return AtomicFamily(terminal, parity, forced_in, forced_out)


def _derived_classifications(
    value: Instance,
) -> tuple[int, int, tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Compute ``T_plus``, ``T_f``, ``P``, ``A``, and ``W`` in dense order."""

    degrees = value.d_q
    terminal_plus = 0
    terminal_f = 0
    p_vertices: list[int] = []
    a_vertices: list[int] = []
    w_vertices: list[int] = []

    for vertex in range(value.n):
        f_value = value.f[vertex]
        degree = degrees[vertex]
        bit = 1 << vertex

        if (f_value + degree) & 1:
            terminal_plus |= bit
        if f_value & 1:
            terminal_f |= bit
        if degree > f_value:
            p_vertices.append(vertex)
        if f_value >= 2:
            a_vertices.append(vertex)
        if f_value == 1:
            w_vertices.append(vertex)

    return (
        terminal_plus,
        terminal_f,
        tuple(p_vertices),
        tuple(a_vertices),
        tuple(w_vertices),
    )


def enumerate_atomic_families(
    value: Instance,
) -> tuple[tuple[AtomicFamily, ...], ...]:
    """Return deterministic atomic-family tuples for branches ``D0`` through ``D3``."""

    if type(value) is not Instance:
        raise ValueError("value must be an exact production Instance")

    terminal_plus, terminal_f, p_vertices, a_vertices, w_vertices = (
        _derived_classifications(value)
    )

    d0 = (
        _checked_family(value.n, terminal_plus, 1, 0, 0),
    )

    d1: list[AtomicFamily] = []
    for p_vertex in p_vertices:
        p_bit = 1 << p_vertex
        for u, v, _ in value.edges:
            u_bit = 1 << u
            v_bit = 1 << v
            d1.append(
                _checked_family(
                    value.n,
                    terminal_plus,
                    0,
                    p_bit | u_bit,
                    v_bit,
                )
            )
            d1.append(
                _checked_family(
                    value.n,
                    terminal_plus,
                    0,
                    p_bit | v_bit,
                    u_bit,
                )
            )

    d2: list[AtomicFamily] = []
    for vertex in a_vertices:
        d2.append(
            _checked_family(value.n, terminal_f, 1, 1 << vertex, 0)
        )

    for u, v, w in combinations(w_vertices, 3):
        forced_in = (1 << u) | (1 << v) | (1 << w)
        d2.append(_checked_family(value.n, terminal_f, 1, forced_in, 0))

    d3: list[AtomicFamily] = []
    for u, v, _ in value.edges:
        u_bit = 1 << u
        v_bit = 1 << v
        d3.append(_checked_family(value.n, terminal_f, 0, u_bit, v_bit))
        d3.append(_checked_family(value.n, terminal_f, 0, v_bit, u_bit))

    return d0, tuple(d1), tuple(d2), tuple(d3)
