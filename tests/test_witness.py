"""RED tests for the governed production Witness and ExactValue layer.

This module consumes the committed Unit 08 authority and ORACLE-030 through ORACLE-037.
It tests only responsibilities owned by ``exactfrac.witness``:

- immutable structural ``Witness(U, y)`` and ``ExactValue(N, D)`` records;
- exact graph-shore sums on canonical production instances;
- strict dense/sparse boundary-count conversion;
- full compact-witness admissibility validation;
- raw unreduced witness-attaining value evaluation;
- exact built-in ``ValueError`` rejection boundaries;
- label independence, large-integer exactness, compact work, and source isolation;
- an independent tiny-instance acceptance/value/conversion audit.

Numerical rational-pair comparison, branch logic, witness reconstruction, certificate
construction/serialization, independent certificate checking, and global optimization
remain outside this unit.

The first run of this file is intentionally RED at import time because
``exactfrac/witness.py`` does not yet exist. That missing-module failure is the required
preimplementation checkpoint, not a defect in this test file.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import os
import subprocess
import sys
from collections.abc import Callable, Iterator
from dataclasses import FrozenInstanceError, fields
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import get_type_hints

import pytest

import exactfrac

instance_module = importlib.import_module("exactfrac.instance")
brute = importlib.import_module("exactfrac_verify.brute")
witness = importlib.import_module("exactfrac.witness")

Instance = instance_module.Instance
Operation = Callable[[], object]

EXPECTED_ALL = (
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

MIXED_EDGES = (
    (0, 1, 2),
    (0, 2, 3),
    (0, 3, 1),
    (1, 2, 4),
    (1, 3, 2),
    (2, 3, 5),
)
MIXED_F = (2, 3, 4, 5)
MIXED_SUM_ROWS = (
    (0, 0, 0, 0, 0),
    (1, 2, 0, 6, 6),
    (2, 3, 0, 8, 8),
    (3, 5, 2, 10, 14),
    (4, 4, 0, 12, 12),
    (5, 6, 3, 12, 18),
    (6, 7, 4, 12, 20),
    (7, 9, 9, 8, 26),
    (8, 5, 0, 8, 8),
    (9, 7, 1, 12, 14),
    (10, 8, 2, 12, 16),
    (11, 10, 5, 12, 22),
    (12, 9, 5, 10, 20),
    (13, 11, 9, 8, 26),
    (14, 12, 11, 6, 28),
    (15, 14, 17, 0, 34),
)

CONVERSION_ROWS = (
    (3, (0, 2, 0, 1, 1, 0), [[1, 2], [3, 1], [4, 1]]),
    (3, (0, 2, 0, 0, 0, 0), [[1, 2]]),
    (3, (0, 3, 1, 4, 2, 0), [[1, 3], [2, 1], [3, 4], [4, 2]]),
    (3, (0, 0, 0, 0, 0, 0), []),
    (0, (0, 0, 0, 0, 0, 0), []),
    (15, (0, 0, 0, 0, 0, 0), []),
)

ACCEPTED_ROWS = (
    (
        "unit-witness",
        3,
        ((0, 1, 1), (0, 2, 1), (1, 2, 1)),
        (1, 1, 2),
        4,
        (0, 1, 0),
        [[1, 1]],
        (2, 0, 2, 2),
        1,
        (2, 2),
    ),
    (
        "unit-competitor",
        3,
        ((0, 1, 1), (0, 2, 1), (1, 2, 1)),
        (1, 1, 2),
        3,
        (0, 1, 0),
        [[1, 1]],
        (2, 1, 2, 4),
        1,
        (4, 2),
    ),
    ("tie-left", 2, ((0, 1, 2),), (1, 1), 1, (2,), [[0, 2]], (1, 0, 2, 2), 2, (4, 2)),
    ("tie-right", 2, ((0, 1, 2),), (1, 1), 2, (2,), [[0, 2]], (1, 0, 2, 2), 2, (4, 2)),
    ("zero-not-empty", 2, ((0, 1, 3),), (3, 3), 1, (0,), [], (3, 0, 3, 3), 0, (0, 2)),
    (
        "mixed-partial",
        4,
        MIXED_EDGES,
        MIXED_F,
        3,
        (0, 2, 0, 1, 1, 0),
        [[1, 2], [3, 1], [4, 1]],
        (5, 2, 10, 14),
        4,
        (12, 8),
    ),
    (
        "mixed-none",
        4,
        MIXED_EDGES,
        MIXED_F,
        3,
        (0, 0, 0, 0, 0, 0),
        [],
        (5, 2, 10, 14),
        0,
        (4, 4),
    ),
    (
        "mixed-all-boundary",
        4,
        MIXED_EDGES,
        MIXED_F,
        3,
        (0, 3, 1, 4, 2, 0),
        [[1, 3], [2, 1], [3, 4], [4, 2]],
        (5, 2, 10, 14),
        10,
        (24, 14),
    ),
)

CORPUS_EXPECTED = {
    2: {
        "instances": 5,
        "all_shores": 20,
        "nonempty_shores": 15,
        "generic_selections": 38,
        "nonempty_selections": 33,
        "admissible": 10,
        "parity_rejected": 17,
        "lower_rejected": 6,
        "zero_value_admissible": 0,
    },
    3: {
        "instances": 324,
        "all_shores": 2592,
        "nonempty_shores": 2268,
        "generic_selections": 12888,
        "nonempty_selections": 12564,
        "admissible": 5907,
        "parity_rejected": 6294,
        "lower_rejected": 363,
        "zero_value_admissible": 249,
    },
}
CORPUS_TOTAL = {
    "instances": 329,
    "all_shores": 2612,
    "nonempty_shores": 2283,
    "generic_selections": 12926,
    "nonempty_selections": 12597,
    "admissible": 5917,
    "parity_rejected": 6311,
    "lower_rejected": 369,
    "zero_value_admissible": 249,
}


class IntSubclass(int):
    """Representative nonexact integer object."""


class TupleSubclass(tuple):
    """Representative nonexact tuple object."""


class ListSubclass(list):
    """Representative nonexact list object."""


class CoercibleOne:
    """Object that would coerce to one if coercion were attempted."""

    def __int__(self) -> int:
        return 1

    def __index__(self) -> int:
        return 1


class PoisonOne:
    """Object exposing forbidden conversion if implementation attempts coercion."""

    def __int__(self) -> int:
        raise AssertionError("integer coercion must not be attempted")

    def __index__(self) -> int:
        raise AssertionError("index coercion must not be attempted")


class DuckInstance:
    """Duck-typed object that must not cross the exact Instance boundary."""

    n = 2
    edges = ((0, 1, 2),)
    f = (1, 1)


class PoisonWitnessLike:
    """Witness-like object whose payload must not be inspected when its type is wrong."""

    def __getattribute__(self, name: str) -> object:
        if name.startswith("__"):
            return object.__getattribute__(self, name)
        raise AssertionError("nonexact witness payload must not be inspected")


def make_mixed(labels: tuple[str | int, ...] | None = None) -> Instance:
    return Instance(4, MIXED_EDGES, MIXED_F, labels)


def direct_sums(value: Instance, U: int) -> tuple[int, int, int, int]:
    members = {vertex for vertex in range(value.n) if U & (1 << vertex)}
    s_value = sum(value.f[vertex] for vertex in members)
    internal = 0
    boundary = 0
    for left, right, multiplicity in value.edges:
        left_in = left in members
        right_in = right in members
        if left_in and right_in:
            internal += multiplicity
        elif left_in != right_in:
            boundary += multiplicity
    degree_sum = sum(value.d_q[vertex] for vertex in members)
    return s_value, internal, boundary, degree_sum


def direct_sparse(value: Instance, U: int, y: tuple[int, ...]) -> list[list[int]]:
    members = {vertex for vertex in range(value.n) if U & (1 << vertex)}
    output: list[list[int]] = []
    for edge_ref, (left, right, multiplicity) in enumerate(value.edges):
        count = y[edge_ref]
        crosses = (left in members) != (right in members)
        assert 0 <= count <= multiplicity
        assert crosses or count == 0
        if count > 0:
            output.append([edge_ref, count])
    return output


def legal_dense_selections(value: Instance, U: int) -> Iterator[tuple[int, ...]]:
    members = {vertex for vertex in range(value.n) if U & (1 << vertex)}
    coordinate_ranges: list[range | tuple[int, ...]] = []
    for left, right, multiplicity in value.edges:
        if (left in members) != (right in members):
            coordinate_ranges.append(range(multiplicity + 1))
        else:
            coordinate_ranges.append((0,))
    yield from product(*coordinate_ranges)


def is_directly_admissible(value: Instance, U: int, y: tuple[int, ...]) -> bool:
    if U == 0:
        return False
    s_value, _, _, _ = direct_sums(value, U)
    total = s_value + sum(y)
    return total >= 3 and total % 2 == 1


def direct_raw_value(value: Instance, U: int, y: tuple[int, ...]) -> tuple[int, int]:
    s_value, internal, _, _ = direct_sums(value, U)
    selected = sum(y)
    return 2 * (internal + selected), s_value + selected - 1


def assert_exact_value_error(operation: Operation) -> None:
    with pytest.raises(ValueError) as exc_info:
        operation()
    assert type(exc_info.value) is ValueError


def malformed_ints() -> tuple[object, ...]:
    return (
        True,
        False,
        1.0,
        Fraction(1, 1),
        IntSubclass(1),
        "1",
        None,
        CoercibleOne(),
        PoisonOne(),
    )


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


def corpus_instances(n: int) -> Iterator[Instance]:
    pairs = tuple(combinations(range(n), 2))
    for multiplicities in product((0, 1, 2), repeat=len(pairs)):
        edges = tuple(
            (left, right, multiplicity)
            for (left, right), multiplicity in zip(pairs, multiplicities, strict=True)
            if multiplicity > 0
        )
        if not edges:
            continue
        degrees = [0] * n
        for left, right, multiplicity in edges:
            degrees[left] += multiplicity
            degrees[right] += multiplicity
        if any(degree == 0 for degree in degrees):
            continue
        f_ranges = tuple(range(1, degree + 1) for degree in degrees)
        for f_values in product(*f_ranges):
            yield Instance(n, edges, f_values)


def aggregate_counts(counts: list[dict[str, int]]) -> dict[str, int]:
    keys = tuple(CORPUS_TOTAL)
    return {key: sum(item[key] for item in counts) for key in keys}


def count_corpus(value_n: int) -> dict[str, int]:
    counts = {key: 0 for key in CORPUS_TOTAL}
    for value in corpus_instances(value_n):
        counts["instances"] += 1
        for U in range(1 << value.n):
            counts["all_shores"] += 1
            if U != 0:
                counts["nonempty_shores"] += 1
            for dense in legal_dense_selections(value, U):
                counts["generic_selections"] += 1
                if U == 0:
                    continue
                counts["nonempty_selections"] += 1
                s_value, internal, _, _ = direct_sums(value, U)
                total = s_value + sum(dense)
                if total % 2 == 0:
                    counts["parity_rejected"] += 1
                elif total < 3:
                    counts["lower_rejected"] += 1
                else:
                    counts["admissible"] += 1
                    if internal == 0 and sum(dense) == 0:
                        counts["zero_value_admissible"] += 1
    return counts


def test_public_surface_signatures_and_type_hints() -> None:
    assert witness.__all__ == EXPECTED_ALL
    assert tuple(field.name for field in fields(witness.ExactValue)) == ("N", "D")
    assert tuple(field.name for field in fields(witness.Witness)) == ("U", "y")
    assert witness.ExactValue.__slots__ == ("N", "D")
    assert witness.Witness.__slots__ == ("U", "y")

    expected_parameters = {
        "shore_f": ("instance", "U"),
        "shore_e_q": ("instance", "U"),
        "shore_b_q": ("instance", "U"),
        "shore_d_q": ("instance", "U"),
        "dense_y_to_sparse": ("instance", "U", "y"),
        "sparse_y_to_dense": ("instance", "U", "entries"),
        "validate_witness": ("instance", "witness"),
        "witness_value": ("instance", "witness"),
    }
    for name, parameters in expected_parameters.items():
        assert tuple(inspect.signature(getattr(witness, name)).parameters) == parameters

    assert get_type_hints(witness.ExactValue) == {"N": int, "D": int}
    assert get_type_hints(witness.Witness) == {"U": int, "y": tuple[int, ...]}
    assert get_type_hints(witness.shore_f)["return"] is int
    assert get_type_hints(witness.shore_e_q)["return"] is int
    assert get_type_hints(witness.shore_b_q)["return"] is int
    assert get_type_hints(witness.shore_d_q)["return"] is int
    assert get_type_hints(witness.dense_y_to_sparse)["return"] == list[list[int]]
    assert get_type_hints(witness.sparse_y_to_dense)["return"] == tuple[int, ...]
    assert get_type_hints(witness.validate_witness)["return"] is type(None)
    assert get_type_hints(witness.witness_value)["return"] is witness.ExactValue


def test_package_root_remains_export_free() -> None:
    for name in EXPECTED_ALL:
        assert not hasattr(exactfrac, name)


def test_exact_value_structural_equality_hash_and_no_ordering() -> None:
    equal_left = witness.ExactValue(2, 2)
    equal_right = witness.ExactValue(2, 2)
    reduced = witness.ExactValue(1, 1)
    zero_raw = witness.ExactValue(0, 2)
    zero_other = witness.ExactValue(0, 1)

    assert equal_left == equal_right
    assert hash(equal_left) == hash(equal_right)
    assert equal_left != reduced
    assert zero_raw != zero_other
    assert len({equal_left, reduced}) == 2
    assert equal_left.N == 2 and equal_left.D == 2
    assert reduced.N == 1 and reduced.D == 1

    with pytest.raises(TypeError):
        _ = witness.ExactValue(3, 10) < witness.ExactValue(2, 3)


def test_exact_value_test_side_numerical_controls() -> None:
    cases = (
        ((2, 2), (1, 1), True),
        ((0, 2), (0, 1), True),
        ((-2, 2), (-1, 1), True),
        ((12, 8), (3, 2), True),
        ((2, 2), (2, 2), True),
        ((3, 10), (2, 3), False),
    )
    for left, right, numerically_equal in cases:
        left_value = witness.ExactValue(*left)
        right_value = witness.ExactValue(*right)
        observed = left_value.N * right_value.D == right_value.N * left_value.D
        assert observed is numerically_equal
        assert (left_value == right_value) is (left == right)


def test_record_immutability_slots_and_structural_witness_equality() -> None:
    first = witness.Witness(3, (0, 2, 0, 1, 1, 0))
    second = witness.Witness(U=3, y=(0, 2, 0, 1, 1, 0))
    different = witness.Witness(3, (0, 2, 0, 0, 1, 0))

    assert first == second
    assert hash(first) == hash(second)
    assert first != different
    assert not hasattr(first, "__dict__")
    assert not hasattr(witness.ExactValue(2, 2), "__dict__")

    with pytest.raises(FrozenInstanceError):
        first.U = 1  # type: ignore[misc]
    with pytest.raises((FrozenInstanceError, AttributeError, TypeError)):
        first.extra = 1  # type: ignore[attr-defined]


def test_witness_constructor_valid_shape_controls() -> None:
    assert witness.Witness(1, ()).U == 1
    assert witness.Witness(1 << 100, ()).U == 1 << 100
    value = witness.Witness(3, (0, 2, 0, 1, 1, 0))
    assert value.y == (0, 2, 0, 1, 1, 0)


def test_witness_constructor_exact_rejections() -> None:
    for bad_u in (0, -1, *malformed_ints()):
        assert_exact_value_error(lambda bad_u=bad_u: witness.Witness(bad_u, ()))

    bad_outer_values = (
        [],
        TupleSubclass(()),
        range(0),
        iter(()),
        "",
        None,
    )
    for bad_y in bad_outer_values:
        assert_exact_value_error(lambda bad_y=bad_y: witness.Witness(1, bad_y))

    for bad_coordinate in (-1, *malformed_ints()):
        candidate = (0, bad_coordinate, 0)
        assert_exact_value_error(lambda candidate=candidate: witness.Witness(1, candidate))


def test_exact_value_constructor_exact_rejections() -> None:
    for bad_n in malformed_ints():
        assert_exact_value_error(lambda bad_n=bad_n: witness.ExactValue(bad_n, 1))
    for bad_d in (0, -1, *malformed_ints()):
        assert_exact_value_error(lambda bad_d=bad_d: witness.ExactValue(1, bad_d))

    assert witness.ExactValue(-2, 2) == witness.ExactValue(-2, 2)
    assert witness.ExactValue(0, 2) == witness.ExactValue(0, 2)


def test_instance_keyed_functions_require_exact_instance_first() -> None:
    mixed = make_mixed()

    class InstanceSubclass(Instance):
        pass

    subclass = InstanceSubclass(4, MIXED_EDGES, MIXED_F)
    verifier_instance = brute.BruteInstance(2, ((0, 1, 2),), (1, 1))
    invalid_instances = (None, {}, subclass, verifier_instance, DuckInstance())

    operations = (
        lambda bad: witness.shore_f(bad, 0),
        lambda bad: witness.shore_e_q(bad, 0),
        lambda bad: witness.shore_b_q(bad, 0),
        lambda bad: witness.shore_d_q(bad, 0),
        lambda bad: witness.dense_y_to_sparse(bad, 0, ()),
        lambda bad: witness.sparse_y_to_dense(bad, 0, []),
        lambda bad: witness.validate_witness(bad, PoisonWitnessLike()),
        lambda bad: witness.witness_value(bad, PoisonWitnessLike()),
    )
    for bad in invalid_instances:
        for operation in operations:
            assert_exact_value_error(lambda bad=bad, operation=operation: operation(bad))

    assert witness.shore_f(mixed, 0) == 0


def test_bare_shore_masks_are_exact_and_finite_universe_bounded() -> None:
    mixed = make_mixed()
    functions = (
        witness.shore_f,
        witness.shore_e_q,
        witness.shore_b_q,
        witness.shore_d_q,
    )
    for function in functions:
        assert type(function(mixed, 0)) is int
        assert type(function(mixed, 15)) is int
        for bad_u in (-1, 16, *malformed_ints()):
            assert_exact_value_error(lambda function=function, bad_u=bad_u: function(mixed, bad_u))

    for bad_u in (-1, 16, *malformed_ints()):
        assert_exact_value_error(
            lambda bad_u=bad_u: witness.dense_y_to_sparse(
                mixed,
                bad_u,
                (0, 0, 0, 0, 0, 0),
            )
        )
        assert_exact_value_error(
            lambda bad_u=bad_u: witness.sparse_y_to_dense(mixed, bad_u, [])
        )


def test_mixed_graph_shore_sums_all_masks() -> None:
    mixed = make_mixed()
    for U, s_value, internal, boundary, degree_sum in MIXED_SUM_ROWS:
        assert witness.shore_f(mixed, U) == s_value
        assert witness.shore_e_q(mixed, U) == internal
        assert witness.shore_b_q(mixed, U) == boundary
        assert witness.shore_d_q(mixed, U) == degree_sum
        assert direct_sums(mixed, U) == (s_value, internal, boundary, degree_sum)


def test_degree_identity_all_mixed_masks() -> None:
    mixed = make_mixed()
    for U in range(16):
        internal = witness.shore_e_q(mixed, U)
        boundary = witness.shore_b_q(mixed, U)
        degree_sum = witness.shore_d_q(mixed, U)
        assert degree_sum == 2 * internal + boundary


def test_dense_to_sparse_literal_rows() -> None:
    mixed = make_mixed()
    for U, dense, expected in CONVERSION_ROWS:
        actual = witness.dense_y_to_sparse(mixed, U, dense)
        assert actual == expected
        assert actual == direct_sparse(mixed, U, dense)
        assert type(actual) is list
        assert all(type(record) is list and len(record) == 2 for record in actual)


def test_sparse_to_dense_literal_rows_and_round_trips() -> None:
    mixed = make_mixed()
    for U, dense, sparse in CONVERSION_ROWS:
        decoded = witness.sparse_y_to_dense(mixed, U, [record.copy() for record in sparse])
        assert decoded == dense
        assert type(decoded) is tuple
        assert witness.dense_y_to_sparse(mixed, U, decoded) == sparse


def test_conversion_detachment_and_failure_nonmutation() -> None:
    mixed = make_mixed()
    dense = (0, 2, 0, 1, 1, 0)
    holder = witness.Witness(3, dense)
    first = witness.dense_y_to_sparse(mixed, 3, dense)
    second = witness.dense_y_to_sparse(mixed, 3, dense)

    assert first == second == [[1, 2], [3, 1], [4, 1]]
    assert first is not second
    assert all(left is not right for left, right in zip(first, second, strict=True))

    first[0][1] = 99
    first.pop()
    assert dense == (0, 2, 0, 1, 1, 0)
    assert holder.y == dense
    assert second == [[1, 2], [3, 1], [4, 1]]
    assert witness.dense_y_to_sparse(mixed, 3, dense) == [[1, 2], [3, 1], [4, 1]]

    source = [[1, 2], [3, 1], [4, 1]]
    decoded = witness.sparse_y_to_dense(mixed, 3, source)
    source[0][1] = 3
    source.pop()
    assert decoded == dense

    invalid = [[1, 4]]
    snapshot = [record.copy() for record in invalid]
    assert_exact_value_error(lambda: witness.sparse_y_to_dense(mixed, 3, invalid))
    assert invalid == snapshot


def test_conversion_is_not_full_admissibility() -> None:
    mixed = make_mixed()
    even_dense = (0, 1, 0, 0, 0, 0)
    assert witness.dense_y_to_sparse(mixed, 3, even_dense) == [[1, 1]]
    assert witness.sparse_y_to_dense(mixed, 3, [[1, 1]]) == even_dense
    bad_witness = witness.Witness(3, even_dense)
    assert_exact_value_error(lambda: witness.validate_witness(mixed, bad_witness))
    assert_exact_value_error(lambda: witness.witness_value(mixed, bad_witness))

    full_dense = (0, 0, 0, 0, 0, 0)
    assert witness.dense_y_to_sparse(mixed, 15, full_dense) == []
    assert witness.sparse_y_to_dense(mixed, 15, []) == full_dense
    assert_exact_value_error(
        lambda: witness.validate_witness(mixed, witness.Witness(15, full_dense))
    )


def test_dense_rejection_matrix() -> None:
    mixed = make_mixed()
    invalid_dense = (
        (0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0),
        (0, -1, 0, 0, 0, 0),
        (0, 4, 0, 0, 0, 0),
        (1, 0, 0, 1, 0, 0),
        (0, 1, 0, 0, 0, 1),
    )
    for dense in invalid_dense:
        assert_exact_value_error(lambda dense=dense: witness.dense_y_to_sparse(mixed, 3, dense))

    for bad_outer in ([], TupleSubclass((0,) * 6), range(6), iter((0,) * 6), "000000", None):
        assert_exact_value_error(
            lambda bad_outer=bad_outer: witness.dense_y_to_sparse(mixed, 3, bad_outer)
        )

    for bad_coordinate in malformed_ints():
        dense = (0, bad_coordinate, 0, 0, 0, 0)
        assert_exact_value_error(lambda dense=dense: witness.dense_y_to_sparse(mixed, 3, dense))

    for U in (0, 15):
        assert_exact_value_error(
            lambda U=U: witness.dense_y_to_sparse(mixed, U, (1, 0, 0, 0, 0, 0))
        )


def test_sparse_rejection_matrix() -> None:
    mixed = make_mixed()
    invalid_sparse: tuple[object, ...] = (
        (),
        ListSubclass([]),
        iter([]),
        "",
        None,
        [()],
        [(1, 1)],
        [ListSubclass([1, 1])],
        [[]],
        [[1]],
        [[1, 1, 1]],
        [[-1, 1]],
        [[6, 1]],
        [[1, 1], [1, 1]],
        [[3, 1], [1, 1]],
        [[1, 0]],
        [[1, -1]],
        [[1, 4]],
        [[0, 1]],
        [[5, 1]],
    )
    for entries in invalid_sparse:
        assert_exact_value_error(
            lambda entries=entries: witness.sparse_y_to_dense(mixed, 3, entries)
        )

    for bad_integer in malformed_ints():
        assert_exact_value_error(
            lambda bad_integer=bad_integer: witness.sparse_y_to_dense(
                mixed,
                3,
                [[bad_integer, 1]],
            )
        )
        assert_exact_value_error(
            lambda bad_integer=bad_integer: witness.sparse_y_to_dense(
                mixed,
                3,
                [[1, bad_integer]],
            )
        )


def test_validate_witness_accepts_catalogued_rows() -> None:
    for row in ACCEPTED_ROWS:
        row_id, n, edges, f_values, U, dense, _, expected_sums, selected, _ = row
        value = Instance(n, edges, f_values)
        candidate = witness.Witness(U, dense)
        assert direct_sums(value, U) == expected_sums, row_id
        assert sum(dense) == selected, row_id
        assert witness.validate_witness(value, candidate) is None, row_id
        assert candidate == witness.Witness(U, dense), row_id


def test_witness_value_returns_literal_unreduced_rows() -> None:
    for row in ACCEPTED_ROWS:
        row_id, n, edges, f_values, U, dense, sparse, _, _, raw = row
        value = Instance(n, edges, f_values)
        candidate = witness.Witness(U, dense)
        observed = witness.witness_value(value, candidate)
        assert observed == witness.ExactValue(*raw), row_id
        assert direct_raw_value(value, U, dense) == (observed.N, observed.D), row_id
        assert witness.dense_y_to_sparse(value, U, dense) == sparse, row_id
        assert candidate == witness.Witness(U, dense), row_id


def test_zero_valued_witness_is_not_empty() -> None:
    value = Instance(2, ((0, 1, 3),), (3, 3))
    candidate = witness.Witness(1, (0,))
    assert witness.validate_witness(value, candidate) is None
    observed = witness.witness_value(value, candidate)
    assert observed == witness.ExactValue(0, 2)
    assert observed != witness.ExactValue(0, 1)
    assert witness.dense_y_to_sparse(value, 1, candidate.y) == []
    assert candidate.U == 1 and candidate.y == (0,)


def test_admissibility_guard_isolation() -> None:
    mixed = make_mixed()
    parity_only = witness.Witness(3, (0, 1, 0, 0, 0, 0))
    assert witness.shore_f(mixed, 3) + sum(parity_only.y) == 6
    assert_exact_value_error(lambda: witness.validate_witness(mixed, parity_only))

    tie = Instance(2, ((0, 1, 2),), (1, 1))
    lower_only = witness.Witness(1, (0,))
    assert witness.shore_f(tie, 1) + sum(lower_only.y) == 1
    assert_exact_value_error(lambda: witness.validate_witness(tie, lower_only))

    full = witness.Witness(15, (0, 0, 0, 0, 0, 0))
    assert witness.shore_f(mixed, 15) + sum(full.y) == 14
    assert_exact_value_error(lambda: witness.validate_witness(mixed, full))


def test_validator_and_evaluator_reject_graph_invalid_shape_valid_witnesses() -> None:
    mixed = make_mixed()
    invalid = (
        witness.Witness(1, ()),
        witness.Witness(1 << 100, ()),
        witness.Witness(3, (0, 4, 0, 0, 0, 0)),
        witness.Witness(3, (1, 0, 0, 1, 0, 0)),
        witness.Witness(3, (0, 1, 0, 0, 0, 1)),
    )
    for candidate in invalid:
        assert_exact_value_error(
            lambda candidate=candidate: witness.validate_witness(mixed, candidate)
        )
        assert_exact_value_error(
            lambda candidate=candidate: witness.witness_value(mixed, candidate)
        )


def test_validator_and_evaluator_require_exact_witness_type() -> None:
    mixed = make_mixed()

    class WitnessSubclass(witness.Witness):
        pass

    subclass = WitnessSubclass(3, (0, 0, 0, 0, 0, 0))
    invalid = (None, (), {}, subclass, PoisonWitnessLike())
    for candidate in invalid:
        assert_exact_value_error(
            lambda candidate=candidate: witness.validate_witness(mixed, candidate)
        )
        assert_exact_value_error(
            lambda candidate=candidate: witness.witness_value(mixed, candidate)
        )


def test_labels_do_not_change_sums_conversions_or_values() -> None:
    mixed_variants = (
        make_mixed(),
        make_mixed(("a", "b", "c", "d")),
        make_mixed((10, 20, 30, 40)),
    )
    dense = (0, 2, 0, 1, 1, 0)
    for value in mixed_variants:
        assert tuple(witness.shore_f(value, U) for U in range(16)) == tuple(
            row[1] for row in MIXED_SUM_ROWS
        )
        assert witness.dense_y_to_sparse(value, 3, dense) == [[1, 2], [3, 1], [4, 1]]
        candidate = witness.Witness(3, dense)
        assert witness.validate_witness(value, candidate) is None
        assert witness.witness_value(value, candidate) == witness.ExactValue(12, 8)


def test_large_integer_exactness_and_literal_preservation() -> None:
    for exponent in (1, 2, 8, 64, 4096):
        large = 1 << exponent
        edge = ((0, 1, large + 1),)

        small_f = Instance(2, edge, (1, 1))
        partial = witness.Witness(1, (large,))
        assert witness.validate_witness(small_f, partial) is None
        assert witness.dense_y_to_sparse(small_f, 1, partial.y) == [[0, large]]
        assert witness.witness_value(small_f, partial) == witness.ExactValue(2 * large, large)

        large_f = Instance(2, edge, (large + 1, large + 1))
        large_partial = witness.Witness(1, (large,))
        assert witness.validate_witness(large_f, large_partial) is None
        assert witness.witness_value(large_f, large_partial) == witness.ExactValue(
            2 * large,
            2 * large,
        )

        zero = witness.Witness(1, (0,))
        assert witness.validate_witness(large_f, zero) is None
        assert witness.witness_value(large_f, zero) == witness.ExactValue(0, large)


def test_source_exactness_import_boundary_and_no_numeric_shortcuts() -> None:
    source_path = Path(witness.__file__).resolve()
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    allowed_imports = {"__future__", "dataclasses", "instance", "shore"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = {alias.name for alias in node.names}
            assert names <= {"dataclasses"}
        elif isinstance(node, ast.ImportFrom):
            assert node.module in allowed_imports
            if node.module in {"instance", "shore"}:
                assert node.level == 1
        elif isinstance(node, ast.Constant):
            assert type(node.value) is not float
        elif isinstance(node, ast.BinOp):
            assert not isinstance(node.op, ast.Div)
        elif isinstance(node, ast.Call):
            function = node.func
            if isinstance(function, ast.Name):
                assert function.id not in {"Fraction", "float", "gcd"}
            elif isinstance(function, ast.Attribute):
                assert function.attr not in {"Fraction", "gcd"}


def test_source_does_not_iterate_over_unordered_sets_or_numeric_magnitudes() -> None:
    source = Path(witness.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    set_names = _known_set_names(tree)
    set_violations: list[tuple[int, str]] = []
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
                set_violations.append((node.lineno, "for"))
        elif isinstance(node, ast.comprehension):
            if _is_known_set_expression(node.iter, set_names):
                set_violations.append((getattr(node, "lineno", 0), "comprehension"))
        elif isinstance(node, ast.YieldFrom):
            if _is_known_set_expression(node.value, set_names):
                set_violations.append((node.lineno, "yield-from"))
        elif isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Name)
                and node.func.id in consuming_calls
                and any(_is_known_set_expression(argument, set_names) for argument in node.args)
            ):
                set_violations.append((node.lineno, node.func.id))
            elif (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in set_names
                and node.func.attr == "pop"
            ):
                set_violations.append((node.lineno, "set.pop"))

    assert set_violations == []

    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "range"
            and node.args
        ):
            continue

        argument = node.args[0]
        if isinstance(argument, ast.Name):
            assert argument.id not in {
                "multiplicity",
                "count",
                "selected",
                "N",
                "D",
            }
        if isinstance(argument, ast.Attribute):
            assert argument.attr != "Q"
        if isinstance(argument, ast.Subscript):
            source_value = argument.value
            if isinstance(source_value, ast.Attribute):
                assert source_value.attr != "q"


def test_fresh_process_import_isolation() -> None:
    repository = Path(__file__).resolve().parents[1]
    script = r'''
import importlib
import pathlib
import sys

forbidden = {
    "exactfrac_verify",
    "exactfrac.families",
    "exactfrac.flow",
    "exactfrac.oracle",
    "exactfrac.branch",
    "exactfrac.solve",
    "exactfrac.certificate",
}
before = set(sys.modules)
module = importlib.import_module("exactfrac.witness")
after = set(sys.modules)
new_forbidden = sorted(name for name in forbidden if name in after - before)
print(pathlib.Path(module.__file__).resolve())
print("NEW_FORBIDDEN=" + ",".join(new_forbidden))
'''
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(repository)}
    completed = subprocess.run(
        [sys.executable, "-c", script],
        cwd=repository,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    lines = completed.stdout.splitlines()
    assert Path(lines[0]) == repository / "exactfrac" / "witness.py"
    assert lines[1] == "NEW_FORBIDDEN="


def test_tiny_corpus_independent_counts() -> None:
    per_n = [count_corpus(2), count_corpus(3)]
    assert per_n[0] == CORPUS_EXPECTED[2]
    assert per_n[1] == CORPUS_EXPECTED[3]
    assert aggregate_counts(per_n) == CORPUS_TOTAL
    assert CORPUS_TOTAL["nonempty_selections"] == (
        CORPUS_TOTAL["admissible"]
        + CORPUS_TOTAL["parity_rejected"]
        + CORPUS_TOTAL["lower_rejected"]
    )
    assert CORPUS_TOTAL["generic_selections"] == (
        CORPUS_TOTAL["nonempty_selections"] + CORPUS_TOTAL["instances"]
    )


def test_tiny_corpus_production_acceptance_and_raw_values() -> None:
    observed_instances = 0
    observed_selections = 0
    observed_admissible = 0
    observed_zero = 0

    for n in (2, 3):
        for value in corpus_instances(n):
            observed_instances += 1
            for U in range(1, 1 << value.n):
                for dense in legal_dense_selections(value, U):
                    observed_selections += 1
                    candidate = witness.Witness(U, dense)
                    expected = is_directly_admissible(value, U, dense)
                    if expected:
                        observed_admissible += 1
                        assert witness.validate_witness(value, candidate) is None
                        raw = direct_raw_value(value, U, dense)
                        assert witness.witness_value(value, candidate) == witness.ExactValue(*raw)
                        if raw[0] == 0:
                            observed_zero += 1
                    else:
                        assert_exact_value_error(
                            lambda value=value, candidate=candidate: witness.validate_witness(
                                value,
                                candidate,
                            )
                        )
                        assert_exact_value_error(
                            lambda value=value, candidate=candidate: witness.witness_value(
                                value,
                                candidate,
                            )
                        )

    assert observed_instances == 329
    assert observed_selections == 12597
    assert observed_admissible == 5917
    assert observed_zero == 249


def test_tiny_corpus_sums_and_conversion_outputs() -> None:
    observed_generic = 0
    for n in (2, 3):
        for value in corpus_instances(n):
            for U in range(1 << value.n):
                expected_sums = direct_sums(value, U)
                assert witness.shore_f(value, U) == expected_sums[0]
                assert witness.shore_e_q(value, U) == expected_sums[1]
                assert witness.shore_b_q(value, U) == expected_sums[2]
                assert witness.shore_d_q(value, U) == expected_sums[3]

                for dense in legal_dense_selections(value, U):
                    observed_generic += 1
                    sparse = direct_sparse(value, U, dense)
                    assert witness.dense_y_to_sparse(value, U, dense) == sparse
                    copied = [record.copy() for record in sparse]
                    assert witness.sparse_y_to_dense(value, U, copied) == dense

    assert observed_generic == 12926


def test_tiny_expanded_copy_projection_matches_compact_counts() -> None:
    checked = 0
    for n in (2, 3):
        for value in corpus_instances(n):
            for U in range(1 << value.n):
                members = {vertex for vertex in range(value.n) if U & (1 << vertex)}
                copies: list[int] = []
                for edge_ref, (left, right, multiplicity) in enumerate(value.edges):
                    if (left in members) != (right in members):
                        copies.extend([edge_ref] * multiplicity)

                projected: set[tuple[int, ...]] = set()
                for choices in product((0, 1), repeat=len(copies)):
                    dense = [0] * value.m
                    for chosen, edge_ref in zip(choices, copies, strict=True):
                        if chosen:
                            dense[edge_ref] += 1
                    projected.add(tuple(dense))

                compact = set(legal_dense_selections(value, U))
                assert projected == compact
                checked += 1

    assert checked == 2612
