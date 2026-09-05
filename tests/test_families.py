"""RED tests for the governed production atomic-family layer.

This module consumes the committed atomic-family authority and ORACLE-023 through
ORACLE-029. It tests only responsibilities owned by ``exactfrac.families``:

- immutable ``AtomicFamily(T, pi, I, O)`` descriptors;
- the exact derived nonemptiness predicate;
- graph-derived ``T_plus``, ``T_f``, ``P``, ``A``, and ``W`` masks;
- deterministic D0--D3 family enumeration;
- exact descriptor counts, duplicate retention, and empty-family retention;
- literal ``prop:branch-transform`` domain equality against generated family unions;
- exact plain-``ValueError`` rejection;
- public surface, solver/verifier isolation, exactness, and structural complexity.

Residual arithmetic, sign routing, parity-cut reduction, branch minimization, branch
iteration, witnesses, certificates, and global optimization remain outside this unit.

The first run of this file is intentionally RED at import time because
``exactfrac/families.py`` does not yet exist. That missing-module failure is the required
preimplementation checkpoint, not a defect in this test file.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import math
import subprocess
import sys
from collections import Counter
from collections.abc import Callable
from dataclasses import FrozenInstanceError, fields
from fractions import Fraction
from itertools import product
from pathlib import Path

import pytest

import exactfrac

instance = importlib.import_module("exactfrac.instance")
brute = importlib.import_module("exactfrac_verify.brute")
families = importlib.import_module("exactfrac.families")

RawFamily = tuple[int, int, int, int]
Branches = tuple[tuple[families.AtomicFamily, ...], ...]
Operation = Callable[[], object]

SPARSE_EDGES = ((0, 1, 1),)
SPARSE_F = (1, 1)

RICH_EDGES = (
    (0, 2, 2),
    (1, 2, 2),
    (2, 4, 1),
    (3, 4, 1),
)
RICH_F = (1, 1, 1, 1, 2)
RICH_LABELS = ("v0", "v1", "v2", "v3", "v4")

RICH_D0_RAW: tuple[RawFamily, ...] = (
    (3, 1, 0, 0),
)

RICH_D1_RAW: tuple[RawFamily, ...] = (
    (3, 0, 1, 4),
    (3, 0, 5, 1),
    (3, 0, 3, 4),
    (3, 0, 5, 2),
    (3, 0, 5, 16),
    (3, 0, 17, 4),
    (3, 0, 9, 16),
    (3, 0, 17, 8),
    (3, 0, 3, 4),
    (3, 0, 6, 1),
    (3, 0, 2, 4),
    (3, 0, 6, 2),
    (3, 0, 6, 16),
    (3, 0, 18, 4),
    (3, 0, 10, 16),
    (3, 0, 18, 8),
    (3, 0, 5, 4),
    (3, 0, 4, 1),
    (3, 0, 6, 4),
    (3, 0, 4, 2),
    (3, 0, 4, 16),
    (3, 0, 20, 4),
    (3, 0, 12, 16),
    (3, 0, 20, 8),
)

RICH_D2_RAW: tuple[RawFamily, ...] = (
    (15, 1, 16, 0),
    (15, 1, 7, 0),
    (15, 1, 11, 0),
    (15, 1, 13, 0),
    (15, 1, 14, 0),
)

RICH_D3_RAW: tuple[RawFamily, ...] = (
    (15, 0, 1, 4),
    (15, 0, 4, 1),
    (15, 0, 2, 4),
    (15, 0, 4, 2),
    (15, 0, 4, 16),
    (15, 0, 16, 4),
    (15, 0, 8, 16),
    (15, 0, 16, 8),
)

RICH_EXPECTED_RAW = (
    RICH_D0_RAW,
    RICH_D1_RAW,
    RICH_D2_RAW,
    RICH_D3_RAW,
)

RICH_DOMAIN_MASKS = (
    frozenset({1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, 30}),
    frozenset({3, 4, 7, 11, 12, 15, 19, 20, 23, 27, 28}),
    frozenset({7, 11, 13, 14, 17, 18, 20, 23, 24, 27, 29, 30}),
    frozenset({3, 5, 6, 9, 10, 12, 15, 16, 19, 21, 22, 25, 26, 28}),
)

RICH_COVER_COUNTS = (
    {
        1: 1,
        2: 1,
        5: 1,
        6: 1,
        9: 1,
        10: 1,
        13: 1,
        14: 1,
        17: 1,
        18: 1,
        21: 1,
        22: 1,
        25: 1,
        26: 1,
        29: 1,
        30: 1,
    },
    {
        3: 4,
        4: 3,
        7: 3,
        11: 6,
        12: 4,
        15: 6,
        19: 8,
        20: 3,
        23: 3,
        27: 6,
        28: 2,
    },
    {
        7: 1,
        11: 1,
        13: 1,
        14: 1,
        17: 1,
        18: 1,
        20: 1,
        23: 2,
        24: 1,
        27: 2,
        29: 2,
        30: 2,
    },
    {
        3: 2,
        5: 2,
        6: 2,
        9: 2,
        10: 2,
        12: 4,
        15: 2,
        16: 2,
        19: 4,
        21: 2,
        22: 2,
        25: 2,
        26: 2,
        28: 2,
    },
)

MAGNITUDE_D0_RAW: tuple[RawFamily, ...] = (
    (1, 1, 0, 0),
)

MAGNITUDE_D1_RAW: tuple[RawFamily, ...] = (
    (1, 0, 1, 2),
    (1, 0, 3, 1),
    (1, 0, 1, 4),
    (1, 0, 5, 1),
    (1, 0, 3, 4),
    (1, 0, 5, 2),
    (1, 0, 3, 2),
    (1, 0, 2, 1),
    (1, 0, 3, 4),
    (1, 0, 6, 1),
    (1, 0, 2, 4),
    (1, 0, 6, 2),
    (1, 0, 5, 2),
    (1, 0, 6, 1),
    (1, 0, 5, 4),
    (1, 0, 4, 1),
    (1, 0, 6, 4),
    (1, 0, 4, 2),
)

MAGNITUDE_D2_RAW: tuple[RawFamily, ...] = (
    (1, 1, 2, 0),
    (1, 1, 4, 0),
)

MAGNITUDE_D3_RAW: tuple[RawFamily, ...] = (
    (1, 0, 1, 2),
    (1, 0, 2, 1),
    (1, 0, 1, 4),
    (1, 0, 4, 1),
    (1, 0, 2, 4),
    (1, 0, 4, 2),
)

MAGNITUDE_EXPECTED_RAW = (
    MAGNITUDE_D0_RAW,
    MAGNITUDE_D1_RAW,
    MAGNITUDE_D2_RAW,
    MAGNITUDE_D3_RAW,
)


class IntSubclass(int):
    """Representative nonexact integer object from ORACLE-028."""


class CoercibleInteger:
    """Object that must be rejected rather than coerced."""

    def __int__(self) -> int:
        return 1

    def __index__(self) -> int:
        return 1


class InstanceSubclass(instance.Instance):
    """Representative nonexact production-instance object."""


def _sparse_instance(
    labels: tuple[str | int, ...] | None = None,
) -> instance.Instance:
    """Construct the ORACLE-024 active instance."""

    return instance.Instance(
        n=2,
        edges=SPARSE_EDGES,
        f=SPARSE_F,
        labels=labels,
    )


def _rich_instance(
    labels: tuple[str | int, ...] | None = None,
) -> instance.Instance:
    """Construct the ORACLE-025 active instance."""

    return instance.Instance(
        n=5,
        edges=RICH_EDGES,
        f=RICH_F,
        labels=labels,
    )


def _magnitude_instance(
    level: int,
    labels: tuple[str | int, ...] | None = None,
) -> instance.Instance:
    """Construct one ORACLE-027 magnitude-family instance."""

    return instance.Instance(
        n=3,
        edges=(
            (0, 1, level),
            (0, 2, level),
            (1, 2, level),
        ),
        f=(1, level, level),
        labels=labels,
    )


def _raw_family(family: families.AtomicFamily) -> RawFamily:
    """Expose one descriptor as its four governed integer fields."""

    return family.T, family.pi, family.I, family.O


def _raw_branches(branches: Branches) -> tuple[tuple[RawFamily, ...], ...]:
    """Expose all four branch tuples without constructing expected descriptors."""

    return tuple(tuple(_raw_family(family) for family in branch) for branch in branches)


def _family_contains_raw(
    raw_family: RawFamily,
    shore: int,
) -> bool:
    """Evaluate the mathematical family-membership predicate independently."""

    terminal, parity, forced_in, forced_out = raw_family
    return (
        (shore & forced_in) == forced_in
        and (shore & forced_out) == 0
        and ((shore & terminal).bit_count() & 1) == parity
    )


def _family_exists_by_enumeration(
    n: int,
    raw_family: RawFamily,
) -> bool:
    """Decide nonemptiness directly by enumerating all shores of one tiny universe."""

    return any(_family_contains_raw(raw_family, shore) for shore in range(1 << n))


def _brute_instance(value: instance.Instance) -> brute.BruteInstance:
    """Create the independent verifier's canonical mathematical instance."""

    return brute.BruteInstance(
        n=value.n,
        edges=value.edges,
        f=value.f,
    )


def _shore_quantities(
    value: brute.BruteInstance,
    shore: int,
) -> tuple[int, int, int, int]:
    """Compute literal branch quantities without the production family layer."""

    s = sum(
        value.f[vertex]
        for vertex in range(value.n)
        if shore & (1 << vertex)
    )
    e = sum(
        multiplicity
        for u, v, multiplicity in value.edges
        if shore & (1 << u) and shore & (1 << v)
    )
    b = sum(
        multiplicity
        for u, v, multiplicity in value.edges
        if bool(shore & (1 << u)) != bool(shore & (1 << v))
    )
    d = 2 * e + b
    return s, e, b, d


def _literal_domains(
    value: instance.Instance,
) -> tuple[frozenset[int], ...]:
    """Evaluate prop:branch-transform literally on brute-enumerated nonempty shores."""

    verifier_instance = _brute_instance(value)
    domains = [set() for _ in range(4)]

    for shore in brute.iter_nonempty_shores(verifier_instance):
        s, _, b, d = _shore_quantities(verifier_instance, shore)
        conditions = (
            ((s + b) & 1) == 1,
            ((s + b) & 1) == 0 and b >= 1 and d - s > 0,
            (s & 1) == 1 and s >= 3,
            (s & 1) == 0 and b >= 1,
        )

        for branch_index, condition in enumerate(conditions):
            if condition:
                domains[branch_index].add(shore)

    return tuple(frozenset(domain) for domain in domains)


def _family_unions_and_counts(
    n: int,
    branches: Branches,
) -> tuple[tuple[frozenset[int], ...], tuple[dict[int, int], ...]]:
    """Evaluate every descriptor on every shore, including the empty shore."""

    unions: list[frozenset[int]] = []
    cover_counts: list[dict[int, int]] = []

    for branch in branches:
        counts: Counter[int] = Counter()

        for family in branch:
            raw = _raw_family(family)

            for shore in range(1 << n):
                if _family_contains_raw(raw, shore):
                    counts[shore] += 1

        unions.append(frozenset(counts))
        cover_counts.append(dict(counts))

    return tuple(unions), tuple(cover_counts)


def _derived_classifications(
    value: instance.Instance,
) -> tuple[int, int, tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Compute T_plus, T_f, P, A, and W without the production family module."""

    terminal_plus = sum(
        1 << vertex
        for vertex in range(value.n)
        if (value.f[vertex] + value.d_q[vertex]) & 1
    )
    terminal_f = sum(
        1 << vertex
        for vertex in range(value.n)
        if value.f[vertex] & 1
    )
    p_vertices = tuple(
        vertex
        for vertex in range(value.n)
        if value.d_q[vertex] > value.f[vertex]
    )
    a_vertices = tuple(
        vertex
        for vertex in range(value.n)
        if value.f[vertex] >= 2
    )
    w_vertices = tuple(
        vertex
        for vertex in range(value.n)
        if value.f[vertex] == 1
    )
    return terminal_plus, terminal_f, p_vertices, a_vertices, w_vertices


def _actual_and_upper_counts(value: instance.Instance) -> tuple[int, int]:
    """Compute the exact emitted count and the source upper bound independently."""

    _, _, p_vertices, a_vertices, w_vertices = _derived_classifications(value)
    actual = (
        1
        + 2 * len(p_vertices) * value.m
        + len(a_vertices)
        + math.comb(len(w_vertices), 3)
        + 2 * value.m
    )
    upper = (
        1
        + 2 * value.m * value.n
        + value.n
        + math.comb(value.n, 3)
        + 2 * value.m
    )
    return actual, upper


def _assert_exact_value_error(operation: Operation, context: str) -> None:
    """Require exact built-in ValueError rather than a subclass."""

    with pytest.raises(ValueError) as exc_info:
        operation()

    assert type(exc_info.value) is ValueError, context


def _stored_slot_names(cls: type[object]) -> tuple[str, ...]:
    """Collect nonimplementation slot names across the class hierarchy."""

    names: list[str] = []

    for base in reversed(cls.__mro__):
        raw_slots = base.__dict__.get("__slots__", ())
        slots = (raw_slots,) if isinstance(raw_slots, str) else tuple(raw_slots)

        for name in slots:
            if name not in {"__dict__", "__weakref__"} and name not in names:
                names.append(name)

    return tuple(names)


def _parsed_family_source() -> ast.Module:
    """Parse the exact production family source for static checks."""

    return ast.parse(inspect.getsource(families))


def _imported_modules(tree: ast.AST) -> tuple[str, ...]:
    """Collect module names imported by production family source."""

    imported: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append("." * node.level + (node.module or ""))

    return tuple(imported)


def _assigned_names(target: ast.expr) -> tuple[str, ...]:
    if isinstance(target, ast.Name):
        return (target.id,)
    if isinstance(target, ast.Tuple | ast.List):
        return tuple(name for item in target.elts for name in _assigned_names(item))
    return ()


def _is_known_set_expression(node: ast.AST, set_names: set[str]) -> bool:
    if isinstance(node, ast.Set | ast.SetComp):
        return True
    if isinstance(node, ast.Name):
        return node.id in set_names
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in {"set", "frozenset"}:
            return True
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in set_names
            and node.func.attr
            in {"copy", "union", "intersection", "difference", "symmetric_difference"}
        ):
            return True
    if isinstance(node, ast.BinOp) and isinstance(
        node.op,
        ast.BitOr | ast.BitAnd | ast.BitXor | ast.Sub,
    ):
        return _is_known_set_expression(node.left, set_names) or _is_known_set_expression(
            node.right,
            set_names,
        )
    return False


def _known_set_names(tree: ast.AST) -> set[str]:
    known: set[str] = set()
    changed = True

    while changed:
        changed = False

        for node in ast.walk(tree):
            targets: tuple[ast.expr, ...] = ()
            value: ast.AST | None = None

            if isinstance(node, ast.Assign):
                targets = tuple(node.targets)
                value = node.value
            elif isinstance(node, ast.AnnAssign):
                targets = (node.target,)
                value = node.value

            if value is None or not _is_known_set_expression(value, known):
                continue

            for target in targets:
                for name in _assigned_names(target):
                    if name not in known:
                        known.add(name)
                        changed = True

    return known


def _magnitude_references(node: ast.AST) -> set[str]:
    """Return names suggesting a loop bound controlled by numeric graph magnitudes."""

    references: set[str] = set()

    for descendant in ast.walk(node):
        if isinstance(descendant, ast.Name):
            references.add(descendant.id)
        elif isinstance(descendant, ast.Attribute):
            references.add(descendant.attr)

    return references & {
        "Q",
        "capacity",
        "count",
        "d_q",
        "f",
        "level",
        "multiplicity",
        "q",
    }


# ---------------------------------------------------------------------------
# ORACLE-023 — exact AtomicFamily semantics and nonemptiness
# ---------------------------------------------------------------------------


def test_oracle_023_direct_nonemptiness_cases() -> None:
    """The ten hand-derived descriptor cases have their exact statuses."""

    cases = (
        ((5, 0, 1, 2), True),
        ((5, 1, 1, 2), True),
        ((5, 1, 1, 4), True),
        ((5, 0, 1, 4), False),
        ((5, 0, 3, 2), False),
        ((5, 1, 3, 2), False),
        ((0, 0, 2, 1), True),
        ((0, 1, 2, 1), False),
        ((1 << 100, 0, 0, 0), True),
        ((1 << 100, 1, 0, 0), True),
    )

    for raw, expected in cases:
        family = families.AtomicFamily(*raw)
        assert type(family.is_nonempty) is bool
        assert family.is_nonempty is expected, raw
        if raw[0].bit_length() <= 3:
            assert family.is_nonempty == _family_exists_by_enumeration(3, raw)


def test_oracle_023_exhaustive_nonemptiness_counts() -> None:
    """All 9,360 tiny descriptors agree with direct shore enumeration."""

    expected_rows = {
        1: (16, 7, 9, 4, 5),
        2: (128, 47, 81, 56, 25),
        3: (1024, 307, 717, 592, 125),
        4: (8192, 1967, 6225, 5600, 625),
    }
    totals = [0, 0, 0, 0, 0]

    for n, expected in expected_rows.items():
        all_count = 0
        nonempty_count = 0
        overlap_empty_count = 0
        parity_empty_count = 0

        masks = range(1 << n)

        for terminal, forced_in, forced_out, parity in product(
            masks,
            masks,
            masks,
            (0, 1),
        ):
            raw = (terminal, parity, forced_in, forced_out)
            family = families.AtomicFamily(*raw)
            enumerated = _family_exists_by_enumeration(n, raw)

            assert family.is_nonempty is enumerated, (n, raw)

            all_count += 1
            nonempty_count += int(enumerated)

            if not enumerated and forced_in & forced_out:
                overlap_empty_count += 1
            elif not enumerated:
                parity_empty_count += 1

        empty_count = all_count - nonempty_count
        actual = (
            all_count,
            nonempty_count,
            empty_count,
            overlap_empty_count,
            parity_empty_count,
        )
        assert actual == expected, n

        for index, value in enumerate(actual):
            totals[index] += value

    assert tuple(totals) == (9360, 2328, 7032, 6252, 780)


def test_oracle_023_descriptor_state_is_derived_and_immutable() -> None:
    """Only T, pi, I, O are authoritative stored fields."""

    family = families.AtomicFamily(5, 1, 1, 4)

    assert tuple(field.name for field in fields(families.AtomicFamily)) == (
        "T",
        "pi",
        "I",
        "O",
    )
    assert _stored_slot_names(families.AtomicFamily) == ("T", "pi", "I", "O")
    assert not hasattr(family, "__dict__")
    assert isinstance(families.AtomicFamily.is_nonempty, property)

    for forbidden in ("empty", "infeasible", "feasible", "free_terminal"):
        assert not hasattr(family, forbidden)

    before_hash = hash(family)

    with pytest.raises((FrozenInstanceError, AttributeError, TypeError)):
        family.T = 0

    assert family == families.AtomicFamily(5, 1, 1, 4)
    assert hash(family) == before_hash


# ---------------------------------------------------------------------------
# ORACLE-024 — sparse active instance and retained empty descriptors
# ---------------------------------------------------------------------------


def test_oracle_024_sparse_exact_sequence_and_empty_statuses() -> None:
    """The sparse instance returns exactly three retained empty descriptors."""

    value = _sparse_instance()
    branches = families.enumerate_atomic_families(value)

    assert type(branches) is tuple
    assert len(branches) == 4
    assert all(type(branch) is tuple for branch in branches)
    assert all(
        type(family) is families.AtomicFamily
        for branch in branches
        for family in branch
    )

    assert _raw_branches(branches) == (
        ((0, 1, 0, 0),),
        (),
        (),
        (
            (3, 0, 1, 2),
            (3, 0, 2, 1),
        ),
    )
    assert tuple(map(len, branches)) == (1, 0, 0, 2)
    assert all(
        not family.is_nonempty
        for branch in branches
        for family in branch
    )

    actual, upper = _actual_and_upper_counts(value)
    assert actual == 3
    assert upper == 9
    assert sum(map(len, branches)) == actual
    assert actual < upper


def test_oracle_024_sparse_literal_domains_equal_family_unions() -> None:
    """Every transformed sparse domain and every generated union is empty."""

    value = _sparse_instance()
    branches = families.enumerate_atomic_families(value)

    literal_domains = _literal_domains(value)
    family_unions, cover_counts = _family_unions_and_counts(value.n, branches)

    assert literal_domains == (
        frozenset(),
        frozenset(),
        frozenset(),
        frozenset(),
    )
    assert family_unions == literal_domains
    assert cover_counts == ({}, {}, {}, {})
    assert all(0 not in union for union in family_unions)


# ---------------------------------------------------------------------------
# ORACLE-025 — rich derived masks, exact order, counts, duplicates, empties
# ---------------------------------------------------------------------------


def test_oracle_025_rich_derived_masks_and_exact_sequence() -> None:
    """The rich instance returns the complete governed D0--D3 sequence."""

    value = _rich_instance()
    branches = families.enumerate_atomic_families(value)

    assert value.d_q == (2, 2, 5, 1, 2)
    assert _derived_classifications(value) == (
        3,
        15,
        (0, 1, 2),
        (4,),
        (0, 1, 2, 3),
    )
    assert tuple(map(len, branches)) == (1, 24, 5, 8)
    assert _raw_branches(branches) == RICH_EXPECTED_RAW


def test_oracle_025_rich_duplicate_and_empty_descriptors_are_retained() -> None:
    """D1 retains its exact duplicate and exact seven empty positions."""

    branches = families.enumerate_atomic_families(_rich_instance())
    d1 = branches[1]

    empty_indices = tuple(
        index
        for index, family in enumerate(d1)
        if not family.is_nonempty
    )
    assert empty_indices == (1, 3, 9, 11, 16, 18, 21)

    assert _raw_family(d1[2]) == (3, 0, 3, 4)
    assert d1[2] == d1[8]
    assert sum(family == d1[2] for family in d1) == 2


def test_oracle_025_rich_exact_count_and_source_upper_bound() -> None:
    """R_actual is 38 while the source n-based expression is the upper bound 64."""

    value = _rich_instance()
    branches = families.enumerate_atomic_families(value)
    actual, upper = _actual_and_upper_counts(value)

    assert actual == 38
    assert upper == 64
    assert sum(map(len, branches)) == actual
    assert actual < upper


def test_oracle_025_generated_masks_remain_inside_the_instance_universe() -> None:
    """Every generated T, I, and O mask is a valid five-vertex shore mask."""

    value = _rich_instance()
    full = (1 << value.n) - 1

    for branch in families.enumerate_atomic_families(value):
        for family in branch:
            assert type(family.T) is int
            assert type(family.pi) is int
            assert type(family.I) is int
            assert type(family.O) is int
            assert 0 <= family.T <= full
            assert family.pi in (0, 1)
            assert 0 <= family.I <= full
            assert 0 <= family.O <= full


# ---------------------------------------------------------------------------
# ORACLE-026 — anti-circular literal domain equality and overlap
# ---------------------------------------------------------------------------


def test_cover() -> None:
    """prop:domain-decomp equals literal prop:branch-transform on both fixtures."""

    for value, expected in (
        (
            _sparse_instance(),
            (
                frozenset(),
                frozenset(),
                frozenset(),
                frozenset(),
            ),
        ),
        (_rich_instance(), RICH_DOMAIN_MASKS),
    ):
        branches = families.enumerate_atomic_families(value)
        literal_domains = _literal_domains(value)
        family_unions, _ = _family_unions_and_counts(value.n, branches)

        assert literal_domains == expected
        assert family_unions == literal_domains
        assert all(0 not in union for union in family_unions)


def test_oracle_026_rich_cover_multiplicities_preserve_overlap() -> None:
    """Exact union equality does not turn the overlapping cover into a partition."""

    value = _rich_instance()
    branches = families.enumerate_atomic_families(value)
    family_unions, cover_counts = _family_unions_and_counts(value.n, branches)

    assert family_unions == RICH_DOMAIN_MASKS
    assert cover_counts == RICH_COVER_COUNTS

    assert max(cover_counts[0].values()) == 1
    assert max(cover_counts[1].values()) == 8
    assert max(cover_counts[2].values()) == 2
    assert max(cover_counts[3].values()) == 4


def test_oracle_026_automatic_side_condition_minima() -> None:
    """The complete rich table exercises the proof's automatic lower endpoints."""

    value = _rich_instance()
    verifier_instance = _brute_instance(value)
    domains = _literal_domains(value)

    d0_min = min(
        _shore_quantities(verifier_instance, shore)[0]
        + _shore_quantities(verifier_instance, shore)[2]
        for shore in domains[0]
    )
    d1_min = min(
        _shore_quantities(verifier_instance, shore)[0]
        + _shore_quantities(verifier_instance, shore)[2]
        for shore in domains[1]
    )
    d2_min_s = min(
        _shore_quantities(verifier_instance, shore)[0]
        for shore in domains[2]
    )

    assert (d0_min, d1_min, d2_min_s) == (3, 4, 3)


# ---------------------------------------------------------------------------
# ORACLE-027 — classification-controlled magnitude and label invariance
# ---------------------------------------------------------------------------


def test_oracle_027_magnitude_and_labels_preserve_exact_sequence() -> None:
    """A 4097-bit magnitude change and optional labels leave descriptors unchanged."""

    large_level = 1 << 4096
    values = (
        _magnitude_instance(2),
        _magnitude_instance(2, ("v0", "v1", "v2")),
        _magnitude_instance(large_level),
        _magnitude_instance(large_level, ("v0", "v1", "v2")),
    )

    assert large_level.bit_length() == 4097

    raw_results = tuple(
        _raw_branches(families.enumerate_atomic_families(value))
        for value in values
    )
    assert all(result == MAGNITUDE_EXPECTED_RAW for result in raw_results)

    for value in values:
        assert _derived_classifications(value) == (
            1,
            1,
            (0, 1, 2),
            (1, 2),
            (0,),
        )
        branches = families.enumerate_atomic_families(value)
        actual, upper = _actual_and_upper_counts(value)
        assert tuple(map(len, branches)) == (1, 18, 2, 6)
        assert actual == 27
        assert upper == 29
        assert sum(map(len, branches)) == actual


def test_oracle_027_repeated_calls_are_equal_and_fresh() -> None:
    """Enumeration is deterministic and returns fresh immutable tuple structure."""

    value = _rich_instance()
    first = families.enumerate_atomic_families(value)
    second = families.enumerate_atomic_families(value)

    assert first == second
    assert _raw_branches(first) == RICH_EXPECTED_RAW


# ---------------------------------------------------------------------------
# ORACLE-028 — exact plain-ValueError rejection matrix
# ---------------------------------------------------------------------------


def test_oracle_028_invalid_mask_fields_raise_exact_value_error() -> None:
    """Each malformed T, I, or O value is rejected without coercion."""

    invalid_values = (
        -1,
        True,
        False,
        1.0,
        Fraction(1, 1),
        IntSubclass(1),
        "1",
        None,
        CoercibleInteger(),
    )

    for field_name in ("T", "I", "O"):
        for bad_value in invalid_values:
            values: dict[str, object] = {
                "T": 1,
                "pi": 0,
                "I": 0,
                "O": 0,
            }
            values[field_name] = bad_value

            _assert_exact_value_error(
                lambda values=values: families.AtomicFamily(**values),
                f"{field_name} accepted {bad_value!r}",
            )


def test_oracle_028_invalid_parity_raises_exact_value_error() -> None:
    """Parity must be the exact built-in integer 0 or 1."""

    invalid_values = (
        -1,
        2,
        True,
        False,
        0.0,
        1.0,
        Fraction(0, 1),
        Fraction(1, 1),
        IntSubclass(0),
        IntSubclass(1),
        "0",
        None,
        CoercibleInteger(),
    )

    for bad_value in invalid_values:
        _assert_exact_value_error(
            lambda bad_value=bad_value: families.AtomicFamily(1, bad_value, 0, 0),
            f"pi accepted {bad_value!r}",
        )

    assert families.AtomicFamily(1, 0, 0, 0).pi == 0
    assert families.AtomicFamily(1, 1, 0, 0).pi == 1


def test_oracle_028_overlap_and_high_bits_are_valid_direct_descriptors() -> None:
    """Direct construction accepts overlap and masks without an ambient universe."""

    overlap = families.AtomicFamily(1, 0, 1, 1)
    assert overlap.is_nonempty is False

    controls = (
        families.AtomicFamily(1 << 100, 0, 0, 0),
        families.AtomicFamily(0, 0, 1 << 100, 0),
        families.AtomicFamily(0, 0, 0, 1 << 100),
    )
    assert tuple(_raw_family(value) for value in controls) == (
        (1 << 100, 0, 0, 0),
        (0, 0, 1 << 100, 0),
        (0, 0, 0, 1 << 100),
    )


def test_oracle_028_invalid_enumerator_arguments_raise_exact_value_error() -> None:
    """The enumerator accepts only an exact production Instance."""

    sparse = _sparse_instance()
    subclass_value = InstanceSubclass(
        n=sparse.n,
        edges=sparse.edges,
        f=sparse.f,
    )
    verifier_value = brute.BruteInstance(
        n=sparse.n,
        edges=sparse.edges,
        f=sparse.f,
    )
    invalid_values = (
        None,
        object(),
        {},
        sparse.to_dict(),
        subclass_value,
        verifier_value,
    )

    for bad_value in invalid_values:
        _assert_exact_value_error(
            lambda bad_value=bad_value: families.enumerate_atomic_families(bad_value),
            f"enumerator accepted {type(bad_value).__name__}",
        )


# ---------------------------------------------------------------------------
# ORACLE-029 — public surface, isolation, exactness, and complexity boundary
# ---------------------------------------------------------------------------


def test_oracle_029_public_surface_and_package_root_boundary() -> None:
    """The module exposes exactly the ruled two-name surface."""

    assert tuple(families.__all__) == (
        "AtomicFamily",
        "enumerate_atomic_families",
    )

    for name in families.__all__:
        assert not hasattr(exactfrac, name)

    assert not any(
        name in families.__all__
        for name in (
            "contains",
            "family_contains",
            "is_member",
            "ExactBranchMin",
            "Witness",
            "ExactValue",
            "StrongCompactMSPD",
        )
    )


def test_oracle_029_no_custom_exception_class_is_defined() -> None:
    """The family module introduces no exception subclass of its own."""

    custom_exceptions = [
        value
        for value in vars(families).values()
        if isinstance(value, type)
        and value.__module__ == families.__name__
        and issubclass(value, BaseException)
    ]
    assert custom_exceptions == []


def test_oracle_029_static_import_and_exactness_boundary() -> None:
    """Family source imports only ruled modules and contains no approximate arithmetic."""

    tree = _parsed_family_source()
    imported = _imported_modules(tree)

    allowed_relative = {".instance", ".shore"}
    allowed_absolute = {"exactfrac.instance", "exactfrac.shore"}

    for imported_name in imported:
        canonical = imported_name.lstrip(".")

        if imported_name in allowed_relative or canonical in allowed_absolute:
            continue

        root = canonical.split(".", maxsplit=1)[0]
        assert root in sys.stdlib_module_names or canonical == "__future__", imported_name

    assert not any(
        imported_name.lstrip(".") == "exactfrac_verify"
        or imported_name.lstrip(".").startswith("exactfrac_verify.")
        for imported_name in imported
    )

    fraction_imports = [
        node
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.Import)
            and any(alias.name == "fractions" for alias in node.names)
        )
        or (isinstance(node, ast.ImportFrom) and node.module == "fractions")
    ]
    fraction_references = [
        node
        for node in ast.walk(tree)
        if (isinstance(node, ast.Name) and node.id == "Fraction")
        or (isinstance(node, ast.Attribute) and node.attr == "Fraction")
    ]
    float_literals = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and type(node.value) is float
    ]
    float_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "float"
    ]
    true_divisions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
    ]
    tolerance_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and (
            (isinstance(node.func, ast.Name) and node.func.id == "isclose")
            or (isinstance(node.func, ast.Attribute) and node.func.attr == "isclose")
        )
    ]

    assert fraction_imports == []
    assert fraction_references == []
    assert float_literals == []
    assert float_calls == []
    assert true_divisions == []
    assert tolerance_calls == []


def test_oracle_029_no_algorithmic_set_iteration() -> None:
    """No output or control-flow order may derive from Python set iteration."""

    tree = _parsed_family_source()
    set_names = _known_set_names(tree)
    violations: list[tuple[int, str]] = []
    consuming_calls = {
        "all",
        "any",
        "enumerate",
        "filter",
        "iter",
        "list",
        "map",
        "max",
        "min",
        "next",
        "reversed",
        "sorted",
        "sum",
        "tuple",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.For | ast.AsyncFor):
            if _is_known_set_expression(node.iter, set_names):
                violations.append((node.lineno, "for"))
        elif isinstance(node, ast.comprehension):
            if _is_known_set_expression(node.iter, set_names):
                violations.append((getattr(node, "lineno", 0), "comprehension"))
        elif isinstance(node, ast.YieldFrom):
            if _is_known_set_expression(node.value, set_names):
                violations.append((node.lineno, "yield-from"))
        elif isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Name)
                and node.func.id in consuming_calls
                and any(_is_known_set_expression(argument, set_names) for argument in node.args)
            ):
                violations.append((node.lineno, node.func.id))
            elif (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in set_names
                and node.func.attr == "pop"
            ):
                violations.append((node.lineno, "set.pop"))

    assert violations == []


def test_oracle_029_no_magnitude_controlled_loop_or_raw_reaggregation() -> None:
    """Loop structure is support-sized and raw instance normalization is not repeated."""

    tree = _parsed_family_source()
    magnitude_loops: list[tuple[int, tuple[str, ...]]] = []

    for node in ast.walk(tree):
        iterator: ast.AST | None = None

        if isinstance(node, ast.For | ast.AsyncFor | ast.comprehension):
            iterator = node.iter

        if not (
            isinstance(iterator, ast.Call)
            and isinstance(iterator.func, ast.Name)
            and iterator.func.id == "range"
        ):
            continue

        references = set().union(
            *(_magnitude_references(argument) for argument in iterator.args),
        )
        if references:
            magnitude_loops.append((getattr(node, "lineno", 0), tuple(sorted(references))))

    forbidden_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"from_dict", "from_records"}
    ]

    assert magnitude_loops == []
    assert forbidden_calls == []


def test_oracle_029_responsibility_boundary() -> None:
    """The module defines descriptors only, not downstream solver machinery."""

    tree = _parsed_family_source()
    definitions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef)
    }
    forbidden_fragments = (
        "argmin",
        "branch_min",
        "certificate",
        "exact_value",
        "parity_cut",
        "residual",
        "sign_route",
        "solve_branch",
        "strong_compact",
        "witness",
    )

    assert not [
        name
        for name in definitions
        if any(fragment in name.lower() for fragment in forbidden_fragments)
    ]


def test_oracle_029_fresh_process_does_not_import_verifier() -> None:
    """Importing production families must not import exactfrac_verify."""

    root = Path(__file__).resolve().parents[1]
    script = """
import sys
import exactfrac
import exactfrac.families

bad = [
    name for name in sys.modules
    if name == "exactfrac_verify" or name.startswith("exactfrac_verify.")
]
exports = [
    name for name in ("AtomicFamily", "enumerate_atomic_families")
    if hasattr(exactfrac, name)
]
raise SystemExit(1 if bad or exports else 0)
"""

    completed = subprocess.run(
        [sys.executable, "-c", script],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
