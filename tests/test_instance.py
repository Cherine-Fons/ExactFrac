"""RED tests for the governed production graph-instance layer.

This module consumes the committed production-instance authority and ORACLE-013 through
ORACLE-018.  It tests only responsibilities owned by ``exactfrac.instance``:

- canonical compact-instance construction;
- raw-record normalization and aggregation;
- exact derived graph data;
- strict ``exactfrac-instance/1`` object serialization;
- malformed-versus-unsupported exception classification;
- immutable stored state, module surface, exactness, determinism, and isolation.

Shore helpers and every downstream solver layer remain outside this unit.

The first run of this file is intentionally RED at import time because
``exactfrac/instance.py`` does not yet exist.  That missing-module failure is the required
preimplementation checkpoint, not a defect in this test file.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import itertools
import subprocess
import sys
from collections.abc import Callable
from fractions import Fraction

import pytest

import exactfrac

instance = importlib.import_module("exactfrac.instance")

Edge = tuple[int, int, int]

CANONICAL_EDGES: tuple[Edge, ...] = (
    (0, 1, 5),
    (0, 3, 2),
    (1, 2, 4),
    (2, 3, 3),
)
CANONICAL_F = (2, 4, 6, 5)
CANONICAL_SUPPORT_EDGES = ((0, 1), (0, 3), (1, 2), (2, 3))
CANONICAL_Q = (5, 2, 4, 3)
CANONICAL_TOTAL = 14
CANONICAL_DEGREES = (7, 9, 7, 5)
CANONICAL_LABELS = ("north", 17, "south", 23)

RAW_A: tuple[Edge, ...] = (
    (3, 2, 1),
    (1, 0, 2),
    (2, 1, 4),
    (0, 3, 2),
    (0, 1, 3),
    (2, 3, 2),
)
RAW_B: tuple[Edge, ...] = (
    (1, 2, 1),
    (3, 0, 2),
    (0, 1, 3),
    (3, 2, 2),
    (2, 1, 3),
    (1, 0, 2),
    (2, 3, 1),
)

LARGE_MULTIPLICITY = 1 << 4096


class IntSubclass(int):
    """Representative nonexact integer object from ORACLE-016."""


class StrSubclass(str):
    """Representative nonexact string-label object."""


class TupleSubclass(tuple):
    """Representative nonexact tuple container."""


class ListSubclass(list):
    """Representative nonexact list container."""


class DictSubclass(dict):
    """Representative nonexact dictionary container."""


def _canonical_instance(
    labels: tuple[str | int, ...] | None = None,
) -> instance.Instance:
    """Construct the hand-derived ORACLE-013 instance."""

    return instance.Instance(
        n=4,
        edges=CANONICAL_EDGES,
        f=CANONICAL_F,
        labels=labels,
    )


def _unlabeled_payload() -> dict[str, object]:
    """Return a fresh exact ORACLE-015 unlabeled object."""

    return {
        "format": "exactfrac-instance/1",
        "n": 4,
        "edges": [
            [0, 1, 5],
            [0, 3, 2],
            [1, 2, 4],
            [2, 3, 3],
        ],
        "f": [2, 4, 6, 5],
    }


def _labeled_payload() -> dict[str, object]:
    """Return a fresh exact ORACLE-015 labeled object."""

    payload = _unlabeled_payload()
    payload["labels"] = ["north", 17, "south", 23]
    return payload


def _replace_payload_value(key: str, value: object) -> dict[str, object]:
    payload = _unlabeled_payload()
    payload[key] = value
    return payload


def _payload_without(key: str) -> dict[str, object]:
    payload = _unlabeled_payload()
    del payload[key]
    return payload


def _payload_with_unknown_key() -> dict[str, object]:
    payload = _unlabeled_payload()
    payload["unknown"] = 1
    return payload


def _payload_with_edge(index: int, edge: object) -> dict[str, object]:
    payload = _unlabeled_payload()
    edges = payload["edges"]
    assert type(edges) is list
    edges[index] = edge
    return payload


def _assert_exact_exception(
    expected: type[BaseException],
    operation: Callable[[], object],
) -> None:
    """Assert the exact exception class, not merely a common superclass."""

    with pytest.raises(expected) as exc_info:
        operation()

    assert type(exc_info.value) is expected


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


def _assert_assignment_rejected(
    target: object,
    name: str,
    replacement: object,
) -> None:
    """Require failed assignment without fixing one implementation-specific exception."""

    before = getattr(target, name)

    with pytest.raises((AttributeError, TypeError)):
        setattr(target, name, replacement)

    assert getattr(target, name) == before


# ---------------------------------------------------------------------------
# I1 / I12 — canonical active instance and exact derived data
# ---------------------------------------------------------------------------


def test_oracle_013_canonical_active_instance_and_exact_derived_data() -> None:
    """ORACLE-013: canonical fields and every derived quantity are exact."""

    result = _canonical_instance()

    assert result.n == 4
    assert result.edges == CANONICAL_EDGES
    assert result.f == CANONICAL_F
    assert result.labels is None
    assert result.m == 4
    assert result.support_edges == CANONICAL_SUPPORT_EDGES
    assert result.q == CANONICAL_Q
    assert result.Q == CANONICAL_TOTAL
    assert result.d_q == CANONICAL_DEGREES

    assert type(result.n) is int
    assert type(result.edges) is tuple
    assert all(type(edge) is tuple for edge in result.edges)
    assert all(type(value) is int for edge in result.edges for value in edge)
    assert type(result.f) is tuple
    assert all(type(value) is int for value in result.f)
    assert type(result.m) is int
    assert type(result.support_edges) is tuple
    assert all(type(edge) is tuple for edge in result.support_edges)
    assert type(result.q) is tuple
    assert all(type(value) is int for value in result.q)
    assert type(result.Q) is int
    assert type(result.d_q) is tuple
    assert all(type(value) is int for value in result.d_q)


def test_oracle_001_valid_active_empty_family_control_constructs() -> None:
    """A valid active Q=1 graph is not invalid or unsupported at construction."""

    result = instance.Instance(
        n=2,
        edges=((0, 1, 1),),
        f=(1, 1),
    )

    assert result.Q == 1
    assert result.d_q == (1, 1)


def test_edge_alias_is_the_ruled_three_integer_tuple_alias() -> None:
    """The public Edge alias has the exact governed shape."""

    assert instance.Edge == tuple[int, int, int]


def test_canonical_instances_have_value_equality() -> None:
    """Round-trip and normalization comparisons require structural value equality."""

    first = _canonical_instance()
    second = _canonical_instance()

    assert first == second
    assert first is not second


def test_authoritative_state_is_exactly_the_four_ruled_slots() -> None:
    """Derived graph values may not become independently mutable stored state."""

    result = _canonical_instance()

    assert frozenset(_stored_slot_names(type(result))) == {"n", "edges", "f", "labels"}
    assert len(_stored_slot_names(type(result))) == 4
    assert not hasattr(result, "__dict__")
    assert not hasattr(result, "full_mask")


def test_stored_and_derived_sequence_values_are_immutable_tuples() -> None:
    """Canonical and derived sequence state is tuple-backed."""

    result = _canonical_instance(CANONICAL_LABELS)

    assert type(result.edges) is tuple
    assert all(type(edge) is tuple for edge in result.edges)
    assert type(result.f) is tuple
    assert type(result.labels) is tuple
    assert type(result.support_edges) is tuple
    assert type(result.q) is tuple
    assert type(result.d_q) is tuple


@pytest.mark.parametrize(
    ("name", "replacement"),
    (
        pytest.param("n", 5, id="n"),
        pytest.param("edges", ((0, 1, 1),), id="edges"),
        pytest.param("f", (1, 1, 1, 1), id="f"),
        pytest.param("labels", ("a", "b", "c", "d"), id="labels"),
    ),
)
def test_authoritative_fields_reject_assignment(name: str, replacement: object) -> None:
    """The canonical object is frozen after successful validation."""

    _assert_assignment_rejected(_canonical_instance(CANONICAL_LABELS), name, replacement)


def test_slotted_instance_rejects_new_attributes() -> None:
    """Arbitrary state cannot be attached after construction."""

    result = _canonical_instance()

    with pytest.raises((AttributeError, TypeError)):
        result.extra_state = 1  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    ("name", "replacement"),
    (
        pytest.param("m", 99, id="m"),
        pytest.param("support_edges", (), id="support-edges"),
        pytest.param("q", (), id="q"),
        pytest.param("Q", 99, id="total-multiplicity"),
        pytest.param("d_q", (), id="degree-tuple"),
    ),
)
def test_derived_properties_reject_independent_assignment(
    name: str,
    replacement: object,
) -> None:
    """Derived graph values cannot become a second mutable source of truth."""

    _assert_assignment_rejected(_canonical_instance(), name, replacement)


# ---------------------------------------------------------------------------
# I2 / I3 / I9 / I12 — raw normalization and deterministic edge references
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "records",
    (
        pytest.param(RAW_A, id="raw-a"),
        pytest.param(tuple(reversed(RAW_A)), id="raw-a-reversed-order"),
        pytest.param(RAW_B, id="raw-b"),
    ),
)
def test_oracle_014_raw_forms_normalize_to_oracle_013(
    records: tuple[Edge, ...],
) -> None:
    """Every ruled raw form yields one canonical object and edge_ref order."""

    normalized = instance.Instance.from_records(4, records, CANONICAL_F)

    assert normalized == _canonical_instance()
    assert normalized.edges == CANONICAL_EDGES
    assert normalized.support_edges == CANONICAL_SUPPORT_EDGES
    assert normalized.q == CANONICAL_Q
    assert normalized.Q == CANONICAL_TOTAL
    assert normalized.d_q == CANONICAL_DEGREES


def test_every_permutation_of_raw_a_has_the_same_canonical_result() -> None:
    """External raw-record order cannot alter canonical graph identity."""

    expected = _canonical_instance()

    for records in itertools.permutations(RAW_A):
        assert instance.Instance.from_records(4, records, CANONICAL_F) == expected


def test_reversed_and_repeated_raw_pairs_aggregate_by_exact_addition() -> None:
    """Repeated unordered pairs combine without explicit-copy expansion."""

    result = instance.Instance.from_records(
        3,
        (
            (1, 0, 2),
            (0, 1, 3),
            (2, 1, 4),
        ),
        (1, 5, 4),
    )

    assert result.edges == ((0, 1, 5), (1, 2, 4))
    assert result.q == (5, 4)
    assert result.Q == 9
    assert result.d_q == (5, 9, 4)


def test_raw_normalization_preserves_labels_without_using_them_algorithmically() -> None:
    """Labels survive normalization but do not affect the canonical edge result."""

    labeled = instance.Instance.from_records(4, RAW_A, CANONICAL_F, CANONICAL_LABELS)
    unlabeled = instance.Instance.from_records(4, RAW_A, CANONICAL_F)

    assert labeled.labels == CANONICAL_LABELS
    assert unlabeled.labels is None
    assert labeled.n == unlabeled.n
    assert labeled.edges == unlabeled.edges
    assert labeled.f == unlabeled.f
    assert labeled.m == unlabeled.m
    assert labeled.support_edges == unlabeled.support_edges
    assert labeled.q == unlabeled.q
    assert labeled.Q == unlabeled.Q
    assert labeled.d_q == unlabeled.d_q


def test_enormous_multiplicity_remains_one_compact_support_record() -> None:
    """ORACLE-018: magnitude does not become one object or loop iteration per copy."""

    direct = instance.Instance(
        n=2,
        edges=((0, 1, LARGE_MULTIPLICITY),),
        f=(1, 1),
    )
    normalized = instance.Instance.from_records(
        2,
        ((1, 0, LARGE_MULTIPLICITY),),
        (1, 1),
    )

    for result in (direct, normalized):
        assert result.m == 1
        assert result.edges == ((0, 1, LARGE_MULTIPLICITY),)
        assert result.support_edges == ((0, 1),)
        assert result.q == (LARGE_MULTIPLICITY,)
        assert result.Q == LARGE_MULTIPLICITY
        assert result.d_q == (LARGE_MULTIPLICITY, LARGE_MULTIPLICITY)

    assert LARGE_MULTIPLICITY.bit_length() == 4097


# ---------------------------------------------------------------------------
# I13 / I14 — strict versioned object serialization and labels
# ---------------------------------------------------------------------------


def test_oracle_015_unlabeled_to_dict_is_exact() -> None:
    """The unlabeled JSON-ready object has the exact ruled schema and order."""

    payload = _canonical_instance().to_dict()

    assert payload == _unlabeled_payload()
    assert tuple(payload) == ("format", "n", "edges", "f")
    assert set(payload) == {"format", "n", "edges", "f"}
    assert type(payload) is dict
    assert type(payload["edges"]) is list
    assert all(type(edge) is list for edge in payload["edges"])
    assert type(payload["f"]) is list
    assert "labels" not in payload


def test_oracle_015_labeled_to_dict_is_exact() -> None:
    """The optional labels field is emitted last and preserves dense-index alignment."""

    payload = _canonical_instance(CANONICAL_LABELS).to_dict()

    assert payload == _labeled_payload()
    assert tuple(payload) == ("format", "n", "edges", "f", "labels")
    assert set(payload) == {"format", "n", "edges", "f", "labels"}
    assert type(payload["labels"]) is list


@pytest.mark.parametrize(
    "payload_factory",
    (
        pytest.param(_unlabeled_payload, id="unlabeled"),
        pytest.param(_labeled_payload, id="labeled"),
    ),
)
def test_oracle_015_from_dict_round_trip(
    payload_factory: Callable[[], dict[str, object]],
) -> None:
    """Strict canonical object deserialization reconstructs the exact instance."""

    payload = payload_factory()
    result = instance.Instance.from_dict(payload)

    assert result.to_dict() == payload
    assert instance.Instance.from_dict(result.to_dict()) == result


def test_from_dict_detaches_instance_state_from_mutable_input_lists() -> None:
    """Mutating the source object after loading cannot mutate the Instance."""

    payload = _labeled_payload()
    result = instance.Instance.from_dict(payload)

    edges = payload["edges"]
    f_values = payload["f"]
    labels = payload["labels"]
    assert type(edges) is list
    assert type(f_values) is list
    assert type(labels) is list
    assert type(edges[0]) is list

    edges[0][2] = 999
    f_values[0] = 999
    labels[0] = "changed"

    assert result.edges == CANONICAL_EDGES
    assert result.f == CANONICAL_F
    assert result.labels == CANONICAL_LABELS


def test_to_dict_returns_detached_mutable_json_containers() -> None:
    """Mutating an emitted object cannot mutate the immutable Instance."""

    result = _canonical_instance(CANONICAL_LABELS)
    payload = result.to_dict()

    edges = payload["edges"]
    f_values = payload["f"]
    labels = payload["labels"]
    assert type(edges) is list
    assert type(f_values) is list
    assert type(labels) is list
    assert type(edges[0]) is list

    edges[0][2] = 999
    f_values[0] = 999
    labels[0] = "changed"

    assert result.edges == CANONICAL_EDGES
    assert result.f == CANONICAL_F
    assert result.labels == CANONICAL_LABELS
    assert result.to_dict() == _labeled_payload()


def test_different_valid_labels_leave_all_graph_data_unchanged() -> None:
    """Label values are metadata and never alter canonical mathematics."""

    first = _canonical_instance(("a", "b", "c", "d"))
    second = _canonical_instance((10, 20, 30, 40))

    for name in ("n", "edges", "f", "m", "support_edges", "q", "Q", "d_q"):
        assert getattr(first, name) == getattr(second, name)

    assert first.labels != second.labels


def test_mixed_exact_string_and_integer_labels_are_valid() -> None:
    """The label domain permits mixed exact built-in str and int values."""

    result = instance.Instance(
        n=2,
        edges=((0, 1, 1),),
        f=(1, 1),
        labels=("1", 1),
    )

    assert result.labels == ("1", 1)


# ---------------------------------------------------------------------------
# I10 — exact exception hierarchy
# ---------------------------------------------------------------------------


def test_exception_classes_are_distinct_value_error_siblings() -> None:
    """Malformed and unsupported states have distinct exact exception classes."""

    assert issubclass(instance.InvalidInstance, ValueError)
    assert issubclass(instance.UnsupportedInstance, ValueError)
    assert instance.InvalidInstance is not instance.UnsupportedInstance
    assert not issubclass(instance.InvalidInstance, instance.UnsupportedInstance)
    assert not issubclass(instance.UnsupportedInstance, instance.InvalidInstance)
    assert instance.InvalidInstance.__base__ is ValueError
    assert instance.UnsupportedInstance.__base__ is ValueError


# ---------------------------------------------------------------------------
# I4--I7 / I10 / I11 / I14 — canonical-constructor rejection matrix
# ---------------------------------------------------------------------------


CANONICAL_INVALID_CASES = (
    pytest.param({"n": True, "edges": ((0, 1, 2),), "f": (1, 1)}, id="n-bool"),
    pytest.param({"n": 2.0, "edges": ((0, 1, 2),), "f": (1, 1)}, id="n-float"),
    pytest.param(
        {"n": IntSubclass(2), "edges": ((0, 1, 2),), "f": (1, 1)},
        id="n-int-subclass",
    ),
    pytest.param({"n": 0, "edges": ((0, 1, 2),), "f": (1, 1)}, id="n-zero"),
    pytest.param({"n": -1, "edges": ((0, 1, 2),), "f": (1, 1)}, id="n-negative"),
    pytest.param({"n": 2, "edges": [(0, 1, 2)], "f": (1, 1)}, id="edges-list"),
    pytest.param(
        {"n": 2, "edges": TupleSubclass(((0, 1, 2),)), "f": (1, 1)},
        id="edges-tuple-subclass",
    ),
    pytest.param({"n": 2, "edges": ([0, 1, 2],), "f": (1, 1)}, id="edge-list"),
    pytest.param(
        {"n": 2, "edges": (TupleSubclass((0, 1, 2)),), "f": (1, 1)},
        id="edge-tuple-subclass",
    ),
    pytest.param({"n": 2, "edges": ((0, 1),), "f": (1, 1)}, id="edge-short"),
    pytest.param({"n": 2, "edges": ((0, 1, 2, 99),), "f": (1, 1)}, id="edge-long"),
    pytest.param({"n": 2, "edges": ((-1, 1, 2),), "f": (1, 1)}, id="endpoint-negative"),
    pytest.param({"n": 2, "edges": ((0, 2, 2),), "f": (1, 1)}, id="endpoint-range"),
    pytest.param({"n": 2, "edges": ((False, 1, 2),), "f": (1, 1)}, id="endpoint-bool"),
    pytest.param({"n": 2, "edges": ((0.0, 1, 2),), "f": (1, 1)}, id="endpoint-float"),
    pytest.param(
        {"n": 2, "edges": ((Fraction(0, 1), 1, 2),), "f": (1, 1)},
        id="endpoint-fraction",
    ),
    pytest.param(
        {"n": 2, "edges": ((IntSubclass(0), 1, 2),), "f": (1, 1)},
        id="endpoint-int-subclass",
    ),
    pytest.param({"n": 2, "edges": ((0, 0, 2),), "f": (1, 1)}, id="loop"),
    pytest.param({"n": 2, "edges": ((1, 0, 2),), "f": (1, 1)}, id="reversed"),
    pytest.param(
        {"n": 2, "edges": ((0, 1, 1), (0, 1, 1)), "f": (1, 1)},
        id="repeated-pair",
    ),
    pytest.param(
        {"n": 3, "edges": ((1, 2, 1), (0, 1, 1)), "f": (1, 1, 1)},
        id="out-of-order",
    ),
    pytest.param({"n": 2, "edges": ((0, 1, 0),), "f": (1, 1)}, id="q-zero"),
    pytest.param({"n": 2, "edges": ((0, 1, -1),), "f": (1, 1)}, id="q-negative"),
    pytest.param({"n": 2, "edges": ((0, 1, True),), "f": (1, 1)}, id="q-bool"),
    pytest.param({"n": 2, "edges": ((0, 1, 1.0),), "f": (1, 1)}, id="q-float"),
    pytest.param(
        {"n": 2, "edges": ((0, 1, Fraction(1, 1)),), "f": (1, 1)},
        id="q-fraction",
    ),
    pytest.param(
        {"n": 2, "edges": ((0, 1, IntSubclass(1)),), "f": (1, 1)},
        id="q-int-subclass",
    ),
    pytest.param({"n": 2, "edges": ((0, 1, "1"),), "f": (1, 1)}, id="q-string"),
    pytest.param({"n": 2, "edges": (), "f": (1, 1)}, id="empty-support"),
    pytest.param({"n": 2, "edges": ((0, 1, 2),), "f": [1, 1]}, id="f-list"),
    pytest.param(
        {"n": 2, "edges": ((0, 1, 2),), "f": TupleSubclass((1, 1))},
        id="f-tuple-subclass",
    ),
    pytest.param({"n": 2, "edges": ((0, 1, 2),), "f": (1,)}, id="f-short"),
    pytest.param({"n": 2, "edges": ((0, 1, 2),), "f": (1, 1, 1)}, id="f-long"),
    pytest.param({"n": 2, "edges": ((0, 1, 2),), "f": (0, 1)}, id="f-zero"),
    pytest.param({"n": 2, "edges": ((0, 1, 2),), "f": (-1, 1)}, id="f-negative"),
    pytest.param({"n": 2, "edges": ((0, 1, 2),), "f": (True, 1)}, id="f-bool"),
    pytest.param({"n": 2, "edges": ((0, 1, 2),), "f": (1.0, 1)}, id="f-float"),
    pytest.param(
        {"n": 2, "edges": ((0, 1, 2),), "f": (Fraction(1, 1), 1)},
        id="f-fraction",
    ),
    pytest.param(
        {"n": 2, "edges": ((0, 1, 2),), "f": (IntSubclass(1), 1)},
        id="f-int-subclass",
    ),
    pytest.param({"n": 2, "edges": ((0, 1, 2),), "f": ("1", 1)}, id="f-string"),
    pytest.param(
        {"n": 2, "edges": ((0, 1, 2),), "f": (1, 1), "labels": ["a", "b"]},
        id="labels-list",
    ),
    pytest.param(
        {
            "n": 2,
            "edges": ((0, 1, 2),),
            "f": (1, 1),
            "labels": TupleSubclass(("a", "b")),
        },
        id="labels-tuple-subclass",
    ),
    pytest.param(
        {"n": 2, "edges": ((0, 1, 2),), "f": (1, 1), "labels": ("a",)},
        id="labels-length",
    ),
    pytest.param(
        {"n": 2, "edges": ((0, 1, 2),), "f": (1, 1), "labels": ("a", "a")},
        id="labels-duplicate",
    ),
    pytest.param(
        {"n": 2, "edges": ((0, 1, 2),), "f": (1, 1), "labels": (True, "b")},
        id="label-bool",
    ),
    pytest.param(
        {"n": 2, "edges": ((0, 1, 2),), "f": (1, 1), "labels": (1.0, "b")},
        id="label-float",
    ),
    pytest.param(
        {
            "n": 2,
            "edges": ((0, 1, 2),),
            "f": (1, 1),
            "labels": (Fraction(1, 1), "b"),
        },
        id="label-fraction",
    ),
    pytest.param(
        {
            "n": 2,
            "edges": ((0, 1, 2),),
            "f": (1, 1),
            "labels": (IntSubclass(1), "b"),
        },
        id="label-int-subclass",
    ),
    pytest.param(
        {
            "n": 2,
            "edges": ((0, 1, 2),),
            "f": (1, 1),
            "labels": (StrSubclass("a"), "b"),
        },
        id="label-str-subclass",
    ),
    pytest.param(
        {"n": 2, "edges": ((0, 1, 2),), "f": (1, 1), "labels": ((1,), "b")},
        id="label-tuple",
    ),
)


@pytest.mark.parametrize("kwargs", CANONICAL_INVALID_CASES)
def test_canonical_constructor_rejects_exact_oracle_016_cases(
    kwargs: dict[str, object],
) -> None:
    """ORACLE-016: every malformed canonical input is exact InvalidInstance."""

    _assert_exact_exception(
        instance.InvalidInstance,
        lambda: instance.Instance(**kwargs),
    )


# ---------------------------------------------------------------------------
# I4--I7 / I10 / I11 — raw-normalization rejection matrix
# ---------------------------------------------------------------------------


RAW_INVALID_CASES = (
    pytest.param({"n": 2, "records": [(0, 1, 2)], "f": (1, 1)}, id="records-list"),
    pytest.param(
        {"n": 2, "records": TupleSubclass(((0, 1, 2),)), "f": (1, 1)},
        id="records-tuple-subclass",
    ),
    pytest.param({"n": 2, "records": ([0, 1, 2],), "f": (1, 1)}, id="record-list"),
    pytest.param(
        {"n": 2, "records": (TupleSubclass((0, 1, 2)),), "f": (1, 1)},
        id="record-tuple-subclass",
    ),
    pytest.param({"n": 2, "records": ((0, 1),), "f": (1, 1)}, id="record-short"),
    pytest.param({"n": 2, "records": ((0, 1, 2, 3),), "f": (1, 1)}, id="record-long"),
    pytest.param({"n": 2, "records": ((0, 0, 2),), "f": (1, 1)}, id="loop"),
    pytest.param({"n": 2, "records": ((-1, 1, 2),), "f": (1, 1)}, id="endpoint-negative"),
    pytest.param({"n": 2, "records": ((0, 2, 2),), "f": (1, 1)}, id="endpoint-range"),
    pytest.param({"n": 2, "records": ((True, 1, 2),), "f": (1, 1)}, id="endpoint-bool"),
    pytest.param({"n": 2, "records": ((0.0, 1, 2),), "f": (1, 1)}, id="endpoint-float"),
    pytest.param(
        {"n": 2, "records": ((Fraction(0, 1), 1, 2),), "f": (1, 1)},
        id="endpoint-fraction",
    ),
    pytest.param(
        {"n": 2, "records": ((IntSubclass(0), 1, 2),), "f": (1, 1)},
        id="endpoint-int-subclass",
    ),
    pytest.param({"n": 2, "records": ((0, 1, 0),), "f": (1, 1)}, id="q-zero"),
    pytest.param({"n": 2, "records": ((0, 1, -1),), "f": (1, 1)}, id="q-negative"),
    pytest.param({"n": 2, "records": ((0, 1, True),), "f": (1, 1)}, id="q-bool"),
    pytest.param({"n": 2, "records": ((0, 1, 1.0),), "f": (1, 1)}, id="q-float"),
    pytest.param(
        {"n": 2, "records": ((0, 1, Fraction(1, 1)),), "f": (1, 1)},
        id="q-fraction",
    ),
    pytest.param(
        {"n": 2, "records": ((0, 1, IntSubclass(1)),), "f": (1, 1)},
        id="q-int-subclass",
    ),
    pytest.param({"n": 2, "records": ((0, 1, "1"),), "f": (1, 1)}, id="q-string"),
    pytest.param({"n": 2, "records": (), "f": (1, 1)}, id="empty-support"),
    pytest.param({"n": True, "records": ((0, 1, 2),), "f": (1, 1)}, id="n-bool"),
    pytest.param({"n": 2.0, "records": ((0, 1, 2),), "f": (1, 1)}, id="n-float"),
    pytest.param(
        {"n": IntSubclass(2), "records": ((0, 1, 2),), "f": (1, 1)},
        id="n-int-subclass",
    ),
    pytest.param({"n": 0, "records": ((0, 1, 2),), "f": (1, 1)}, id="n-zero"),
    pytest.param({"n": -1, "records": ((0, 1, 2),), "f": (1, 1)}, id="n-negative"),
    pytest.param({"n": 2, "records": ((0, 1, 2),), "f": [1, 1]}, id="f-list"),
    pytest.param(
        {"n": 2, "records": ((0, 1, 2),), "f": TupleSubclass((1, 1))},
        id="f-tuple-subclass",
    ),
    pytest.param({"n": 2, "records": ((0, 1, 2),), "f": (1,)}, id="f-short"),
    pytest.param({"n": 2, "records": ((0, 1, 2),), "f": (1, 1, 1)}, id="f-long"),
    pytest.param({"n": 2, "records": ((0, 1, 2),), "f": (0, 1)}, id="f-zero"),
    pytest.param({"n": 2, "records": ((0, 1, 2),), "f": (-1, 1)}, id="f-negative"),
    pytest.param({"n": 2, "records": ((0, 1, 2),), "f": (True, 1)}, id="f-bool"),
    pytest.param({"n": 2, "records": ((0, 1, 2),), "f": (1.0, 1)}, id="f-float"),
    pytest.param(
        {"n": 2, "records": ((0, 1, 2),), "f": (Fraction(1, 1), 1)},
        id="f-fraction",
    ),
    pytest.param(
        {"n": 2, "records": ((0, 1, 2),), "f": (IntSubclass(1), 1)},
        id="f-int-subclass",
    ),
    pytest.param({"n": 2, "records": ((0, 1, 2),), "f": ("1", 1)}, id="f-string"),
    pytest.param(
        {"n": 2, "records": ((0, 1, 2),), "f": (1, 1), "labels": ["a", "b"]},
        id="labels-list",
    ),
    pytest.param(
        {
            "n": 2,
            "records": ((0, 1, 2),),
            "f": (1, 1),
            "labels": TupleSubclass(("a", "b")),
        },
        id="labels-tuple-subclass",
    ),
    pytest.param(
        {"n": 2, "records": ((0, 1, 2),), "f": (1, 1), "labels": ("a",)},
        id="labels-length",
    ),
    pytest.param(
        {"n": 2, "records": ((0, 1, 2),), "f": (1, 1), "labels": ("a", "a")},
        id="labels-duplicate",
    ),
    pytest.param(
        {"n": 2, "records": ((0, 1, 2),), "f": (1, 1), "labels": (True, "b")},
        id="label-bool",
    ),
    pytest.param(
        {"n": 2, "records": ((0, 1, 2),), "f": (1, 1), "labels": (1.0, "b")},
        id="label-float",
    ),
    pytest.param(
        {
            "n": 2,
            "records": ((0, 1, 2),),
            "f": (1, 1),
            "labels": (Fraction(1, 1), "b"),
        },
        id="label-fraction",
    ),
    pytest.param(
        {
            "n": 2,
            "records": ((0, 1, 2),),
            "f": (1, 1),
            "labels": (IntSubclass(1), "b"),
        },
        id="label-int-subclass",
    ),
    pytest.param(
        {
            "n": 2,
            "records": ((0, 1, 2),),
            "f": (1, 1),
            "labels": (StrSubclass("a"), "b"),
        },
        id="label-str-subclass",
    ),
    pytest.param(
        {"n": 2, "records": ((0, 1, 2),), "f": (1, 1), "labels": ((1,), "b")},
        id="label-tuple",
    ),
    pytest.param(
        {"n": 2, "records": ((0, 1, 2),), "f": (1, 1), "labels": (object(), "b")},
        id="label-object",
    ),
)


@pytest.mark.parametrize("kwargs", RAW_INVALID_CASES)
def test_from_records_rejects_exact_oracle_016_cases(
    kwargs: dict[str, object],
) -> None:
    """ORACLE-016: malformed raw input is exact InvalidInstance."""

    _assert_exact_exception(
        instance.InvalidInstance,
        lambda: instance.Instance.from_records(**kwargs),
    )


# ---------------------------------------------------------------------------
# I13 — strict-deserialization rejection matrix
# ---------------------------------------------------------------------------


SERIALIZED_INVALID_FACTORIES = (
    pytest.param(lambda: [], id="outer-list"),
    pytest.param(lambda: DictSubclass(_unlabeled_payload()), id="outer-dict-subclass"),
    pytest.param(lambda: _payload_without("format"), id="missing-format"),
    pytest.param(lambda: _payload_without("n"), id="missing-n"),
    pytest.param(lambda: _payload_without("edges"), id="missing-edges"),
    pytest.param(lambda: _payload_without("f"), id="missing-f"),
    pytest.param(_payload_with_unknown_key, id="unknown-key"),
    pytest.param(
        lambda: _replace_payload_value("format", "exactfrac-instance/2"),
        id="wrong-format",
    ),
    pytest.param(lambda: _replace_payload_value("format", 1), id="nonstring-format"),
    pytest.param(lambda: _replace_payload_value("n", True), id="n-bool"),
    pytest.param(lambda: _replace_payload_value("n", 4.0), id="n-float"),
    pytest.param(
        lambda: _replace_payload_value("n", IntSubclass(4)),
        id="n-int-subclass",
    ),
    pytest.param(lambda: _replace_payload_value("n", 0), id="n-zero"),
    pytest.param(lambda: _replace_payload_value("n", -1), id="n-negative"),
    pytest.param(
        lambda: _replace_payload_value("edges", tuple(CANONICAL_EDGES)),
        id="edges-tuple",
    ),
    pytest.param(
        lambda: _replace_payload_value(
            "edges",
            ListSubclass(_unlabeled_payload()["edges"]),
        ),
        id="edges-list-subclass",
    ),
    pytest.param(lambda: _replace_payload_value("edges", []), id="empty-support"),
    pytest.param(lambda: _payload_with_edge(0, (0, 1, 5)), id="edge-tuple"),
    pytest.param(
        lambda: _payload_with_edge(0, ListSubclass([0, 1, 5])),
        id="edge-list-subclass",
    ),
    pytest.param(lambda: _payload_with_edge(0, [0, 1]), id="edge-short"),
    pytest.param(lambda: _payload_with_edge(0, [0, 1, 5, 9]), id="edge-long"),
    pytest.param(lambda: _payload_with_edge(0, [-1, 1, 5]), id="endpoint-negative"),
    pytest.param(lambda: _payload_with_edge(0, [0, 4, 5]), id="endpoint-range"),
    pytest.param(lambda: _payload_with_edge(0, [False, 1, 5]), id="endpoint-bool"),
    pytest.param(lambda: _payload_with_edge(0, [0.0, 1, 5]), id="endpoint-float"),
    pytest.param(
        lambda: _payload_with_edge(0, [Fraction(0, 1), 1, 5]),
        id="endpoint-fraction",
    ),
    pytest.param(
        lambda: _payload_with_edge(0, [IntSubclass(0), 1, 5]),
        id="endpoint-int-subclass",
    ),
    pytest.param(lambda: _payload_with_edge(0, [0, 0, 5]), id="edge-loop"),
    pytest.param(lambda: _payload_with_edge(0, [1, 0, 5]), id="edge-reversed"),
    pytest.param(
        lambda: _replace_payload_value(
            "edges",
            [[0, 1, 2], [0, 1, 3], [1, 2, 4], [2, 3, 3]],
        ),
        id="edge-repeat",
    ),
    pytest.param(
        lambda: _replace_payload_value(
            "edges",
            [[0, 3, 2], [0, 1, 5], [1, 2, 4], [2, 3, 3]],
        ),
        id="edge-order",
    ),
    pytest.param(lambda: _payload_with_edge(0, [0, 1, 0]), id="q-zero"),
    pytest.param(lambda: _payload_with_edge(0, [0, 1, -1]), id="q-negative"),
    pytest.param(lambda: _payload_with_edge(0, [0, 1, True]), id="q-bool"),
    pytest.param(lambda: _payload_with_edge(0, [0, 1, 5.0]), id="q-float"),
    pytest.param(
        lambda: _payload_with_edge(0, [0, 1, Fraction(5, 1)]),
        id="q-fraction",
    ),
    pytest.param(
        lambda: _payload_with_edge(0, [0, 1, IntSubclass(5)]),
        id="q-int-subclass",
    ),
    pytest.param(lambda: _payload_with_edge(0, [0, 1, "5"]), id="q-string"),
    pytest.param(lambda: _replace_payload_value("f", tuple(CANONICAL_F)), id="f-tuple"),
    pytest.param(
        lambda: _replace_payload_value("f", ListSubclass(CANONICAL_F)),
        id="f-list-subclass",
    ),
    pytest.param(lambda: _replace_payload_value("f", [2, 4, 6]), id="f-short"),
    pytest.param(lambda: _replace_payload_value("f", [2, 4, 6, 5, 1]), id="f-long"),
    pytest.param(lambda: _replace_payload_value("f", [0, 4, 6, 5]), id="f-zero"),
    pytest.param(lambda: _replace_payload_value("f", [-1, 4, 6, 5]), id="f-negative"),
    pytest.param(lambda: _replace_payload_value("f", [True, 4, 6, 5]), id="f-bool"),
    pytest.param(lambda: _replace_payload_value("f", [2.0, 4, 6, 5]), id="f-float"),
    pytest.param(
        lambda: _replace_payload_value("f", [Fraction(2, 1), 4, 6, 5]),
        id="f-fraction",
    ),
    pytest.param(
        lambda: _replace_payload_value("f", [IntSubclass(2), 4, 6, 5]),
        id="f-int-subclass",
    ),
    pytest.param(lambda: _replace_payload_value("f", ["2", 4, 6, 5]), id="f-string"),
    pytest.param(lambda: {**_unlabeled_payload(), "labels": None}, id="labels-none"),
    pytest.param(
        lambda: {**_unlabeled_payload(), "labels": CANONICAL_LABELS},
        id="labels-tuple",
    ),
    pytest.param(
        lambda: {**_unlabeled_payload(), "labels": ListSubclass(CANONICAL_LABELS)},
        id="labels-list-subclass",
    ),
    pytest.param(
        lambda: {**_unlabeled_payload(), "labels": ["north"]},
        id="labels-short",
    ),
    pytest.param(
        lambda: {
            **_unlabeled_payload(),
            "labels": ["north", 17, "south", 23, "extra"],
        },
        id="labels-long",
    ),
    pytest.param(
        lambda: {**_unlabeled_payload(), "labels": ["north", 17, "north", 23]},
        id="labels-duplicate",
    ),
    pytest.param(
        lambda: {**_unlabeled_payload(), "labels": ["north", True, "south", 23]},
        id="label-bool",
    ),
    pytest.param(
        lambda: {**_unlabeled_payload(), "labels": ["north", 1.0, "south", 23]},
        id="label-float",
    ),
    pytest.param(
        lambda: {
            **_unlabeled_payload(),
            "labels": ["north", Fraction(17, 1), "south", 23],
        },
        id="label-fraction",
    ),
    pytest.param(
        lambda: {
            **_unlabeled_payload(),
            "labels": ["north", IntSubclass(17), "south", 23],
        },
        id="label-int-subclass",
    ),
    pytest.param(
        lambda: {
            **_unlabeled_payload(),
            "labels": [StrSubclass("north"), 17, "south", 23],
        },
        id="label-str-subclass",
    ),
    pytest.param(
        lambda: {**_unlabeled_payload(), "labels": ["north", (17,), "south", 23]},
        id="label-tuple",
    ),
    pytest.param(
        lambda: {**_unlabeled_payload(), "labels": ["north", object(), "south", 23]},
        id="label-object",
    ),
)


@pytest.mark.parametrize("payload_factory", SERIALIZED_INVALID_FACTORIES)
def test_from_dict_rejects_exact_oracle_016_cases(
    payload_factory: Callable[[], object],
) -> None:
    """ORACLE-016: strict object deserialization never repairs malformed input."""

    _assert_exact_exception(
        instance.InvalidInstance,
        lambda: instance.Instance.from_dict(payload_factory()),
    )


# ---------------------------------------------------------------------------
# I8 / I10 — unsupported active regime and malformed-before-active order
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "operation",
    (
        pytest.param(
            lambda: instance.Instance(2, ((0, 1, 2),), (3, 1)),
            id="canonical-nonisolated-active-failure",
        ),
        pytest.param(
            lambda: instance.Instance(3, ((0, 1, 2),), (1, 1, 1)),
            id="canonical-isolated-vertex",
        ),
        pytest.param(
            lambda: instance.Instance.from_records(2, ((1, 0, 2),), (3, 1)),
            id="raw-active-failure",
        ),
        pytest.param(
            lambda: instance.Instance.from_dict(
                {
                    "format": "exactfrac-instance/1",
                    "n": 2,
                    "edges": [[0, 1, 2]],
                    "f": [3, 1],
                }
            ),
            id="serialized-active-failure",
        ),
    ),
)
def test_oracle_017_structurally_valid_active_failures_are_exact_unsupported(
    operation: Callable[[], object],
) -> None:
    """Only a structurally valid active-condition failure is UnsupportedInstance."""

    _assert_exact_exception(instance.UnsupportedInstance, operation)


@pytest.mark.parametrize(
    "operation",
    (
        pytest.param(
            lambda: instance.Instance(3, ((1, 0, 2),), (1, 1, 1)),
            id="reversed-edge-plus-isolated-vertex",
        ),
        pytest.param(
            lambda: instance.Instance.from_records(3, ((0, 0, 2),), (1, 1, 1)),
            id="loop-plus-isolated-vertices",
        ),
        pytest.param(
            lambda: instance.Instance(2, ((0, 1, 0),), (3, 1)),
            id="zero-multiplicity-plus-active-failure",
        ),
        pytest.param(
            lambda: instance.Instance.from_dict(
                {
                    "format": "wrong-format",
                    "n": 2,
                    "edges": [[0, 1, 2]],
                    "f": [3, 1],
                }
            ),
            id="wrong-format-plus-active-failure",
        ),
    ),
)
def test_oracle_017_malformed_validation_precedes_active_check(
    operation: Callable[[], object],
) -> None:
    """Malformed input may never be relabeled as merely unsupported."""

    _assert_exact_exception(instance.InvalidInstance, operation)


# ---------------------------------------------------------------------------
# I15 / R3 / R4 / D1 — public surface, isolation, and exact source discipline
# ---------------------------------------------------------------------------


def test_oracle_018_exact_public_surface_and_export_free_package_root() -> None:
    """The instance unit exports only the four ruled names."""

    assert tuple(instance.__all__) == (
        "Edge",
        "Instance",
        "InvalidInstance",
        "UnsupportedInstance",
    )

    for name in instance.__all__:
        assert not hasattr(exactfrac, name)


@pytest.mark.parametrize(
    "name",
    (
        "validate_shore",
        "shore_from_list",
        "shore_to_list",
        "shore_complement",
        "AtomicFamily",
        "Witness",
        "ExactBranchMin",
        "SolveBranchStandard",
        "SolveBranchAccelerated",
        "StrongCompactMSPD",
    ),
)
def test_oracle_018_downstream_public_names_are_absent(name: str) -> None:
    """The graph-instance unit does not absorb shore or downstream solver APIs."""

    assert not hasattr(instance, name)


def _parsed_instance_source() -> ast.Module:
    return ast.parse(inspect.getsource(instance))


def _imported_modules(tree: ast.AST) -> tuple[str, ...]:
    imported: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level
            imported.append(prefix + (node.module or ""))

    return tuple(imported)


def test_instance_imports_only_standard_library_modules() -> None:
    """The production reference core remains free of third-party dependencies."""

    imported = _imported_modules(_parsed_instance_source())
    roots = {
        name.lstrip(".").split(".", maxsplit=1)[0]
        for name in imported
        if name.lstrip(".")
    }

    assert not any(name.startswith(".") and name != "._telemetry" for name in imported)
    assert roots <= set(sys.stdlib_module_names) | {"__future__", "_telemetry"}


def test_instance_source_and_fresh_import_are_verifier_isolated() -> None:
    """Production instance import may not acquire an exactfrac_verify dependency."""

    imported = _imported_modules(_parsed_instance_source())
    forbidden = [
        name
        for name in imported
        if name.lstrip(".") == "exactfrac_verify"
        or name.lstrip(".").startswith("exactfrac_verify.")
    ]

    assert forbidden == []

    script = """
import sys
import exactfrac.instance

bad = [
    name
    for name in sys.modules
    if name == "exactfrac_verify" or name.startswith("exactfrac_verify.")
]
raise SystemExit(1 if bad else 0)
"""

    completed = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_instance_source_defines_no_ruled_downstream_machinery() -> None:
    """Source structure preserves the graph-instance-only responsibility seam."""

    tree = _parsed_instance_source()
    definitions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef)
    }
    forbidden_exact = {
        "validate_shore",
        "shore_from_list",
        "shore_to_list",
        "shore_complement",
        "AtomicFamily",
        "Witness",
        "ExactValue",
        "ExactBranchMin",
        "SolveBranchStandard",
        "SolveBranchAccelerated",
        "StrongCompactMSPD",
    }
    forbidden_fragments = (
        "shore",
        "family",
        "witness",
        "argmin",
        "sign_route",
        "parity_cut",
        "branch",
        "raw_pair",
        "rational_pair",
    )

    assert definitions.isdisjoint(forbidden_exact)
    assert [
        name
        for name in definitions
        if any(fragment in name.lower() for fragment in forbidden_fragments)
    ] == []


def test_instance_correctness_path_contains_no_fraction_float_or_true_division() -> None:
    """R3/R4: the production instance path is exact integer logic."""

    tree = _parsed_instance_source()

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
            assignments: tuple[ast.expr, ...] = ()
            value: ast.AST | None = None

            if isinstance(node, ast.Assign):
                assignments = tuple(node.targets)
                value = node.value
            elif isinstance(node, ast.AnnAssign):
                assignments = (node.target,)
                value = node.value

            if value is None or not _is_known_set_expression(value, known):
                continue

            for target in assignments:
                for name in _assigned_names(target):
                    if name not in known:
                        known.add(name)
                        changed = True

    return known


def test_instance_source_does_not_derive_algorithmic_order_from_set_iteration() -> None:
    """D1: sets may support membership, but set iteration may not govern order."""

    tree = _parsed_instance_source()
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
                and any(_is_known_set_expression(arg, set_names) for arg in node.args)
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
