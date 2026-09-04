"""RED tests for the governed production shore-representation layer.

This module consumes the committed shore authority and ORACLE-019 through ORACLE-022.
It tests only responsibilities owned by ``exactfrac.shore``:

- finite-universe integer shore masks;
- exact universe and mask validation;
- universe-relative complement;
- strict sorted-index-list encoding and decoding;
- representation-level membership, cardinality, union, intersection, and parity identities;
- exact plain-``ValueError`` rejection;
- public surface, graph independence, exactness, determinism, and compactness.

Graph-dependent shore sums, atomic families, witnesses, certificates, rational-pair
arithmetic, cut reductions, branch logic, and the global solver remain outside this unit.

The first run of this file is intentionally RED at import time because
``exactfrac/shore.py`` does not yet exist. That missing-module failure is the required
preimplementation checkpoint, not a defect in this test file.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import subprocess
import sys
from collections.abc import Callable, Iterator
from fractions import Fraction
from pathlib import Path

import pytest

import exactfrac

shore = importlib.import_module("exactfrac.shore")

FIVE_N = 5
FIVE_FULL = 31
MIXED_U = 21
MIXED_T = 14
MIXED_INTERSECTION = 4
MIXED_COMPLEMENT = 10

LARGE_N = 4096
LARGE_FULL = (1 << LARGE_N) - 1
LARGE_U = (1 << 0) | (1 << 2048) | (1 << 4095)
LARGE_VERTICES = [0, 2048, 4095]
LARGE_COMPLEMENT = LARGE_FULL ^ LARGE_U


class IntSubclass(int):
    """Representative nonexact integer object from ORACLE-021."""


class ListSubclass(list):
    """Representative nonexact list container from ORACLE-021."""


class CoercibleInteger:
    """Object that must be rejected rather than coerced through integer protocols."""

    def __int__(self) -> int:
        return 1

    def __index__(self) -> int:
        return 1


class IterableVertices:
    """Iterable that must be rejected rather than consumed as a serialized shore list."""

    def __iter__(self) -> Iterator[int]:
        return iter((0, 2, 4))


class ProtocolBomb:
    """Object whose conversion and comparison protocols must never be consulted."""

    def __int__(self) -> int:
        raise AssertionError("integer coercion was attempted")

    def __index__(self) -> int:
        raise AssertionError("index coercion was attempted")

    def __lt__(self, other: object) -> bool:
        raise AssertionError(f"comparison was attempted against {other!r}")

    def __le__(self, other: object) -> bool:
        raise AssertionError(f"comparison was attempted against {other!r}")

    def __gt__(self, other: object) -> bool:
        raise AssertionError(f"comparison was attempted against {other!r}")

    def __ge__(self, other: object) -> bool:
        raise AssertionError(f"comparison was attempted against {other!r}")


Operation = Callable[[], object]


def _members(n: int, mask: int) -> list[int]:
    """Return the independently specified sorted member list for one shore."""

    return [vertex for vertex in range(n) if mask & (1 << vertex)]


def _assert_exact_value_error(operation: Operation, context: str) -> None:
    """Require exact built-in ValueError rather than a subclass or another error."""

    with pytest.raises(ValueError) as exc_info:
        operation()

    assert type(exc_info.value) is ValueError, context


def _parsed_shore_source() -> ast.Module:
    """Parse the exact production shore source for static boundary checks."""

    return ast.parse(inspect.getsource(shore))


def _imported_modules(tree: ast.AST) -> tuple[str, ...]:
    """Collect module names imported by the production shore source."""

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


def _contains_mask_extent(node: ast.AST) -> bool:
    """Detect obvious attempts to iterate over all numeric shore values."""

    for descendant in ast.walk(node):
        if isinstance(descendant, ast.LShift):
            return True
        if (
            isinstance(descendant, ast.Call)
            and isinstance(descendant.func, ast.Name)
            and descendant.func.id == "full_mask"
        ):
            return True
    return False


# ---------------------------------------------------------------------------
# ORACLE-019 — exact empty, full, mixed, and one-vertex shore values
# ---------------------------------------------------------------------------


def test_oracle_019_five_vertex_mixed_mask_values() -> None:
    """Membership, cardinality, union, intersection, parity, and complement are exact."""

    assert shore.full_mask(FIVE_N) == FIVE_FULL
    assert type(shore.full_mask(FIVE_N)) is int
    assert shore.validate_shore(FIVE_N, MIXED_U) == MIXED_U
    assert shore.validate_shore(FIVE_N, MIXED_T) == MIXED_T

    assert tuple(bool(MIXED_U & (1 << vertex)) for vertex in range(FIVE_N)) == (
        True,
        False,
        True,
        False,
        True,
    )
    assert MIXED_U.bit_count() == 3
    assert MIXED_T.bit_count() == 3
    assert MIXED_U & MIXED_T == MIXED_INTERSECTION
    assert _members(FIVE_N, MIXED_U & MIXED_T) == [2]
    assert (MIXED_U & MIXED_T).bit_count() == 1
    assert (MIXED_U & MIXED_T).bit_count() & 1 == 1
    assert MIXED_U | MIXED_T == FIVE_FULL
    assert _members(FIVE_N, MIXED_U | MIXED_T) == [0, 1, 2, 3, 4]

    complement = shore.shore_complement(FIVE_N, MIXED_U)
    assert complement == MIXED_COMPLEMENT
    assert _members(FIVE_N, complement) == [1, 3]
    assert complement.bit_count() == 2
    assert MIXED_U & complement == 0
    assert MIXED_U | complement == FIVE_FULL
    assert shore.shore_complement(FIVE_N, complement) == MIXED_U
    assert (MIXED_U & complement).bit_count() & 1 == 0
    assert ~MIXED_U == -22


def test_oracle_019_empty_full_and_one_vertex_boundaries() -> None:
    """Generic shore validity includes empty and complete shores, including n=1."""

    assert shore.validate_shore(5, 0) == 0
    assert shore.validate_shore(5, 31) == 31
    assert shore.shore_to_list(5, 0) == []
    assert shore.shore_to_list(5, 31) == [0, 1, 2, 3, 4]
    assert shore.shore_complement(5, 0) == 31
    assert shore.shore_complement(5, 31) == 0

    assert shore.full_mask(1) == 1
    assert shore.validate_shore(1, 0) == 0
    assert shore.validate_shore(1, 1) == 1
    assert shore.shore_to_list(1, 0) == []
    assert shore.shore_to_list(1, 1) == [0]
    assert shore.shore_from_list(1, []) == 0
    assert shore.shore_from_list(1, [0]) == 1
    assert shore.shore_complement(1, 0) == 1
    assert shore.shore_complement(1, 1) == 0


def test_oracle_019_strict_serialization_values_and_detachment() -> None:
    """The exact sorted-list encodings round-trip and every emitted list is fresh."""

    cases = (
        (0, []),
        (21, [0, 2, 4]),
        (10, [1, 3]),
        (31, [0, 1, 2, 3, 4]),
    )

    for mask, expected in cases:
        first = shore.shore_to_list(5, mask)
        second = shore.shore_to_list(5, mask)
        context = f"mask={mask}"

        assert first == expected, context
        assert second == expected, context
        assert type(first) is list, context
        assert type(second) is list, context
        assert first is not second, context
        assert shore.shore_from_list(5, expected.copy()) == mask, context

        first.append(999)
        assert shore.shore_to_list(5, mask) == expected, context


def test_oracle_019_bare_python_complement_is_not_a_valid_shore() -> None:
    """Bare ``~U`` is negative and cannot cross the finite-universe helper boundary."""

    assert ~MIXED_U == -22

    for helper_name, operation in (
        ("validate_shore", lambda: shore.validate_shore(FIVE_N, ~MIXED_U)),
        ("shore_to_list", lambda: shore.shore_to_list(FIVE_N, ~MIXED_U)),
        ("shore_complement", lambda: shore.shore_complement(FIVE_N, ~MIXED_U)),
    ):
        _assert_exact_value_error(operation, helper_name)


# ---------------------------------------------------------------------------
# ORACLE-020 — exhaustive small-universe identities without pytest explosion
# ---------------------------------------------------------------------------


def test_oracle_020_all_254_valid_masks_inside_one_exhaustive_test() -> None:
    """Exercise every valid shore for n=1,...,7 without 254 collected test cases."""

    case_count = 0

    for n in range(1, 8):
        full = (1 << n) - 1
        assert shore.full_mask(n) == full, f"n={n}"

        for mask in range(full + 1):
            case_count += 1
            context = f"n={n}, U={mask}"
            expected_members = _members(n, mask)
            complement = full ^ mask

            assert shore.validate_shore(n, mask) == mask, context
            assert shore.shore_to_list(n, mask) == expected_members, context
            assert shore.shore_from_list(n, expected_members.copy()) == mask, context
            assert mask.bit_count() == len(expected_members), context
            assert shore.shore_complement(n, mask) == complement, context
            assert shore.shore_complement(n, complement) == mask, context
            assert mask & complement == 0, context
            assert mask | complement == full, context

            first = shore.shore_to_list(n, mask)
            second = shore.shore_to_list(n, mask)
            assert first == second, context
            assert first is not second, context
            first.append(n)
            assert shore.shore_to_list(n, mask) == expected_members, context

            for helper_name, operation in (
                ("validate_shore", lambda n=n, mask=mask: shore.validate_shore(n, ~mask)),
                ("shore_to_list", lambda n=n, mask=mask: shore.shore_to_list(n, ~mask)),
                (
                    "shore_complement",
                    lambda n=n, mask=mask: shore.shore_complement(n, ~mask),
                ),
            ):
                _assert_exact_value_error(operation, f"{context}, {helper_name}")

    assert case_count == 254


def test_oracle_020_all_21844_ordered_pairs_inside_one_exhaustive_test() -> None:
    """Exercise every ordered pair for n=1,...,7 without 21,844 pytest cases."""

    pair_count = 0

    for n in range(1, 8):
        full = (1 << n) - 1

        for left in range(full + 1):
            left_members = _members(n, left)
            left_set = set(left_members)

            for right in range(full + 1):
                pair_count += 1
                context = f"n={n}, U={left}, T={right}"
                right_members = _members(n, right)
                right_set = set(right_members)
                union = left | right
                intersection = left & right
                expected_union = sorted(left_set | right_set)
                expected_intersection = sorted(left_set & right_set)

                assert shore.shore_to_list(n, union) == expected_union, context
                assert shore.shore_to_list(n, intersection) == expected_intersection, context
                assert intersection.bit_count() == len(expected_intersection), context
                assert intersection.bit_count() & 1 == len(expected_intersection) & 1, context

                for vertex in range(n):
                    assert bool(left & (1 << vertex)) == (vertex in left_set), context
                    assert bool(right & (1 << vertex)) == (vertex in right_set), context

    assert pair_count == 21_844


# ---------------------------------------------------------------------------
# ORACLE-021 — exact built-in ValueError rejection matrix
# ---------------------------------------------------------------------------


def test_oracle_021_every_public_helper_rejects_each_invalid_n_exactly() -> None:
    """All public helpers own the same exact positive-built-in-int universe boundary."""

    bad_values = (
        0,
        -1,
        True,
        False,
        1.0,
        Fraction(1, 1),
        IntSubclass(1),
        CoercibleInteger(),
        "1",
        None,
    )
    helpers: tuple[tuple[str, Callable[[object], object]], ...] = (
        ("full_mask", lambda value: shore.full_mask(value)),
        ("validate_shore", lambda value: shore.validate_shore(value, 0)),
        ("shore_to_list", lambda value: shore.shore_to_list(value, 0)),
        ("shore_from_list", lambda value: shore.shore_from_list(value, [])),
        ("shore_complement", lambda value: shore.shore_complement(value, 0)),
    )

    for bad_n in bad_values:
        for helper_name, helper in helpers:
            _assert_exact_value_error(
                lambda bad_n=bad_n, helper=helper: helper(bad_n),
                f"{helper_name}, n={bad_n!r}",
            )


def test_oracle_021_every_mask_helper_rejects_each_invalid_shore_exactly() -> None:
    """Negative, high-bit, nonexact, and coercible shore values are invalid."""

    bad_values = (
        -1,
        32,
        1 << 100,
        True,
        False,
        21.0,
        Fraction(21, 1),
        IntSubclass(21),
        CoercibleInteger(),
        "21",
        None,
        ProtocolBomb(),
    )
    helpers: tuple[tuple[str, Callable[[object], object]], ...] = (
        ("validate_shore", lambda value: shore.validate_shore(5, value)),
        ("shore_to_list", lambda value: shore.shore_to_list(5, value)),
        ("shore_complement", lambda value: shore.shore_complement(5, value)),
    )

    for bad_shore in bad_values:
        for helper_name, helper in helpers:
            _assert_exact_value_error(
                lambda bad_shore=bad_shore, helper=helper: helper(bad_shore),
                f"{helper_name}, U={bad_shore!r}",
            )


def test_oracle_021_bare_complements_are_rejected_by_every_mask_helper() -> None:
    """Every bare Python complement is outside the finite shore universe."""

    for mask in (0, 1, 10, 21, 31):
        assert ~mask == -mask - 1

        for helper_name, operation in (
            ("validate_shore", lambda mask=mask: shore.validate_shore(5, ~mask)),
            ("shore_to_list", lambda mask=mask: shore.shore_to_list(5, ~mask)),
            ("shore_complement", lambda mask=mask: shore.shore_complement(5, ~mask)),
        ):
            _assert_exact_value_error(operation, f"{helper_name}, U=~{mask}")


def test_oracle_021_strict_decoder_rejects_nonexact_outer_containers() -> None:
    """The serialized shore boundary accepts exact built-in lists only."""

    invalid_containers = (
        (),
        (0, 2, 4),
        range(3),
        "024",
        None,
        ListSubclass([0, 2, 4]),
        iter([0, 2, 4]),
        IterableVertices(),
    )

    for vertices in invalid_containers:
        _assert_exact_value_error(
            lambda vertices=vertices: shore.shore_from_list(5, vertices),
            f"vertices={vertices!r}",
        )


def test_oracle_021_strict_decoder_rejects_invalid_members_and_order() -> None:
    """Member typing, range, uniqueness, and increasing order are all strict."""

    invalid_lists = (
        [True],
        [1.0],
        [Fraction(1, 1)],
        [IntSubclass(1)],
        [CoercibleInteger()],
        ["1"],
        [None],
        [ProtocolBomb()],
        [-1],
        [5],
        [0, 0],
        [0, 2, 2],
        [2, 1],
        [0, 3, 2],
    )

    for vertices in invalid_lists:
        _assert_exact_value_error(
            lambda vertices=vertices: shore.shore_from_list(5, vertices),
            f"vertices={vertices!r}",
        )


def test_oracle_021_valid_strict_decoding_controls() -> None:
    """Strict validation still accepts every catalogued canonical list control."""

    assert shore.shore_from_list(5, []) == 0
    assert shore.shore_from_list(5, [0]) == 1
    assert shore.shore_from_list(5, [0, 2, 4]) == 21
    assert shore.shore_from_list(5, [0, 1, 2, 3, 4]) == 31


def test_oracle_021_invalid_n_is_rejected_without_secondary_protocol_coercion() -> None:
    """Malformed universe values cannot trigger coercion of later arguments."""

    bomb = ProtocolBomb()

    for helper_name, operation in (
        ("validate_shore", lambda: shore.validate_shore(0, bomb)),
        ("shore_to_list", lambda: shore.shore_to_list(0, bomb)),
        ("shore_from_list", lambda: shore.shore_from_list(0, [bomb])),
        ("shore_complement", lambda: shore.shore_complement(0, bomb)),
    ):
        _assert_exact_value_error(operation, helper_name)


# ---------------------------------------------------------------------------
# ORACLE-022 — public surface, isolation, source discipline, and large n
# ---------------------------------------------------------------------------


def test_oracle_022_exact_public_surface_and_export_free_package_root() -> None:
    """The shore module exports only the six ruled names."""

    assert tuple(shore.__all__) == (
        "Shore",
        "full_mask",
        "validate_shore",
        "shore_from_list",
        "shore_to_list",
        "shore_complement",
    )
    assert shore.Shore is int

    for name in shore.__all__:
        assert not hasattr(exactfrac, name)


def test_oracle_022_no_redundant_or_downstream_api_is_exposed() -> None:
    """Shore owns finite-subset mechanics and no consumer-specific machinery."""

    forbidden_names = (
        "contains",
        "membership",
        "cardinality",
        "intersection_parity",
        "f_of_shore",
        "e_q",
        "b_q",
        "d_q",
        "AtomicFamily",
        "Witness",
        "ExactValue",
        "ExactBranchMin",
        "SolveBranchStandard",
        "SolveBranchAccelerated",
        "StrongCompactMSPD",
    )

    for name in forbidden_names:
        assert not hasattr(shore, name)


def test_oracle_022_source_is_graph_independent_and_stdlib_only() -> None:
    """The source imports neither graph instances nor the independent verifier."""

    tree = _parsed_shore_source()
    imported = _imported_modules(tree)

    assert not any(name.startswith(".") for name in imported)

    roots = {
        name.lstrip(".").split(".", maxsplit=1)[0]
        for name in imported
        if name.lstrip(".")
    }
    assert roots <= set(sys.stdlib_module_names) | {"__future__"}
    assert "exactfrac" not in roots
    assert "exactfrac_verify" not in roots
    assert all(name != "exactfrac.instance" for name in imported)

    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    assert "Instance" not in names
    assert "InvalidInstance" not in names
    assert "UnsupportedInstance" not in names


def test_oracle_022_fresh_process_import_isolation() -> None:
    """A clean shore import acquires neither instance nor verifier dependencies."""

    root = Path(__file__).resolve().parents[1]
    script = """
import sys
import exactfrac.shore
bad = [
    name for name in sys.modules
    if name == 'exactfrac.instance'
    or name.startswith('exactfrac.instance.')
    or name == 'exactfrac_verify'
    or name.startswith('exactfrac_verify.')
]
raise SystemExit(1 if bad else 0)
"""
    completed = subprocess.run(
        [sys.executable, "-c", script],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_oracle_022_correctness_path_contains_no_fraction_float_or_true_division() -> None:
    """R3/R4: the production shore path uses exact integer and bit operations only."""

    tree = _parsed_shore_source()
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
            or (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "isclose"
            )
        )
    ]

    assert fraction_imports == []
    assert fraction_references == []
    assert float_literals == []
    assert float_calls == []
    assert true_divisions == []
    assert tolerance_calls == []


def test_oracle_022_source_does_not_derive_order_from_set_iteration() -> None:
    """D1: set iteration may not govern output order or control-flow order."""

    tree = _parsed_shore_source()
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


def test_oracle_022_source_has_no_obvious_all_shores_range() -> None:
    """No helper may loop over ``range(1 << n)`` or ``range(full_mask(n))``."""

    tree = _parsed_shore_source()
    violations = [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "range"
        and any(_contains_mask_extent(argument) for argument in node.args)
    ]

    assert violations == []


def test_oracle_022_large_universe_remains_compact_and_exact() -> None:
    """The 4096-vertex fixture uses one integer mask rather than all shore values."""

    assert shore.full_mask(LARGE_N) == LARGE_FULL
    assert LARGE_FULL.bit_length() == 4096
    assert shore.validate_shore(LARGE_N, LARGE_U) == LARGE_U
    assert LARGE_U.bit_count() == 3
    assert LARGE_U.bit_length() == 4096
    assert shore.shore_to_list(LARGE_N, LARGE_U) == LARGE_VERTICES
    assert shore.shore_from_list(LARGE_N, LARGE_VERTICES.copy()) == LARGE_U
    assert shore.shore_complement(LARGE_N, LARGE_U) == LARGE_COMPLEMENT
    assert LARGE_COMPLEMENT.bit_count() == 4093
    assert LARGE_COMPLEMENT.bit_length() == 4095
    assert LARGE_U & LARGE_COMPLEMENT == 0
    assert LARGE_U | LARGE_COMPLEMENT == LARGE_FULL
    assert shore.shore_complement(LARGE_N, LARGE_COMPLEMENT) == LARGE_U
    assert shore.shore_to_list(LARGE_N, LARGE_FULL) == list(range(LARGE_N))
    assert shore.shore_to_list(LARGE_N, LARGE_COMPLEMENT) == [
        vertex for vertex in range(LARGE_N) if vertex not in (0, 2048, 4095)
    ]
