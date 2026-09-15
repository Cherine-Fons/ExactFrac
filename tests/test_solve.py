"""Unit 15 consuming tests: DESIGN 4.12, TEST_PLAN 35/36, ORACLE-108--116.

Human catalogue tables are fixed authority; no private handoff path is read.
Every registered input invokes both real branch selections. Transparent spies
observe original candidates; independent brute records verify raw attainment.
Fault injections below are synthetic consumer-boundary controls, not graph claims.
Production must be absent during Phase D; importing exactfrac.solve is the RED.
"""

from __future__ import annotations

import ast
import dataclasses
import enum
import hashlib
import inspect
import json
import subprocess
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import get_type_hints

import pytest

# isort: split
# Keep the intentional missing-module import in its own sorting block.
import exactfrac.solve as global_solver

# isort: split
from exactfrac.branch import AcceleratedBranchStats, BranchResult, StandardBranchStats
from exactfrac.instance import Instance
from exactfrac.oracle import BranchOracleStats
from exactfrac.witness import ExactValue, Witness
from exactfrac_verify import brute

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ("Standard", "Accelerated")
ORIGINS = ("Empty", "Baseline", "L0", "L1", "H0", "H1", "H2")
BRANCH_NAMES = ("L0", "L1", "H0", "H1")


def _tables():
    """Read only the registered human tables; never a private JSON mirror."""
    text = (ROOT / "docs/ORACLE_CATALOG.md").read_text(encoding="utf-8")
    tables = {}
    current = None
    headers = None
    for line in text.splitlines():
        if line.startswith("### Fixture table: U15_"):
            current = line.split(": ", 1)[1]
            assert current not in tables
            tables[current] = []
            headers = None
        elif current and line.startswith("| "):
            cells = [cell.strip() for cell in line[1:-1].split("|")]
            if headers is None:
                headers = tuple(cells)
            elif not all(cell == "---" for cell in cells):
                assert len(cells) == len(headers)
                assert all(cell.startswith("`") and cell.endswith("`") for cell in cells)
                tables[current].append(tuple(ast.literal_eval(cell[1:-1]) for cell in cells))
        elif current and line.strip():
            current = None
    return tables


def _stream_hash(rows):
    return hashlib.sha256(b"".join(
        (json.dumps(row, ensure_ascii=True, separators=(",", ":")) + "\n").encode()
        for row in rows
    )).hexdigest()


TABLES = _tables()
INPUTS = {row[0]: row for row in TABLES["U15_INPUTS"]}
BASELINES = {row[0]: row for row in TABLES["U15_BASELINES"]}
GLOBALS = {row[0]: row for row in TABLES["U15_GLOBAL"]}
OPTIMA = {(row[0], row[1]): row for row in TABLES["U15_OPTIMA"]}
SHORES = {(row[0], row[1], row[2]): row for row in TABLES["U15_SHORES"]}
H2 = {row[0]: row for row in TABLES["U15_H2"]}
STRUCTURE = {row[0]: row for row in TABLES["U15_STRUCTURE"]}


def _instance(key):
    _, _, n, edges, f, labels = INPUTS[key]
    return Instance(n, edges, f, labels)


def _independent(instance):
    return brute.BruteInstance(instance.n, instance.edges, instance.f)


def _pair(value):
    assert type(value) is ExactValue
    return value.N, value.D


def _witness_record(witness, value):
    assert type(witness) is Witness
    return witness.U, witness.y, _pair(value)


def _verify(instance, witness, value):
    """Pass primitive records only across the independent-verifier boundary."""
    independent = _independent(instance)
    other = brute.Witness(witness.U, witness.y)
    assert brute.witness_is_admissible(independent, other)
    assert brute.witness_raw_value(independent, other) == _pair(value)
    assert 0 <= value.N <= 2 * sum(q for _, _, q in instance.edges)
    assert 2 <= value.D <= 2 * sum(q for _, _, q in instance.edges) - 1
    return Fraction(value.N, value.D)


def _stats(route, number=0):
    inner = BranchOracleStats(*(number for _ in range(7)))
    if route == "Standard":
        return StandardBranchStats(number, number, number, inner)
    return AcceleratedBranchStats(*(number for _ in range(7)), inner)


def _selected(route):
    return "solve_branch_standard" if route == "Standard" else "solve_branch_accelerated"


def _forbidden(*_args, **_kwargs):
    raise AssertionError("dependency must not be invoked at this boundary")


def _exact_error(kind, function, *args, **kwargs):
    with pytest.raises(kind) as caught:
        function(*args, **kwargs)
    assert type(caught.value) is kind


class _Str(str):
    pass


class _Tuple(tuple):
    pass


class _Instance(Instance):
    pass


class _Value(ExactValue):
    pass


class _Witness(Witness):
    pass


class _StandardStats(StandardBranchStats):
    pass


class _AcceleratedStats(AcceleratedBranchStats):
    pass


class _Choice(enum.Enum):
    STANDARD = "Standard"


class _StringChoice(enum.StrEnum):
    STANDARD = "Standard"


class _Marker(Exception):
    pass


def _signature(function, names):
    signature = inspect.signature(function)
    assert tuple(signature.parameters) == names
    for parameter in signature.parameters.values():
        assert parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert parameter.default is inspect.Parameter.empty


def test_gl1_public_surface_and_record_contracts():
    assert global_solver.__all__ == ("SolveResult", "SolveStats", "solve")
    _signature(global_solver.solve, ("instance", "branch_solver"))
    _signature(global_solver.SolveResult, ("value", "witness"))
    _signature(global_solver.SolveStats, ("branch_solver", "branch_stats", "attaining_candidate"))
    assert get_type_hints(global_solver.solve) == {
        "instance": Instance, "branch_solver": str,
        "return": tuple[global_solver.SolveResult, global_solver.SolveStats],
    }
    assert get_type_hints(global_solver.SolveResult) == {
        "value": ExactValue, "witness": Witness | None,
    }
    assert get_type_hints(global_solver.SolveStats) == {
        "branch_solver": str,
        "branch_stats": tuple[StandardBranchStats | AcceleratedBranchStats, ...],
        "attaining_candidate": str,
    }
    value, witness = ExactValue(-3, 7), Witness(1, ())
    result = global_solver.SolveResult(value, witness)
    assert result.value is value and result.witness is witness
    assert result == global_solver.SolveResult(value, witness)
    assert result != global_solver.SolveResult(ExactValue(-6, 14), witness)
    assert global_solver.SolveResult(ExactValue(0, 1), witness).witness is witness
    for cls, record, fields in (
        (global_solver.SolveResult, result, ("value", "witness")),
        (global_solver.SolveStats, global_solver.SolveStats("Standard", (), "H2"),
         ("branch_solver", "branch_stats", "attaining_candidate")),
    ):
        assert dataclasses.is_dataclass(cls)
        assert tuple(field.name for field in dataclasses.fields(cls)) == fields
        assert tuple(cls.__slots__) == fields
        assert cls.__dataclass_params__.frozen and not cls.__dataclass_params__.order
        assert not hasattr(record, "__dict__")
        assert hash(record) == hash(record)
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(record, fields[0], None)
        with pytest.raises(TypeError):
            _ = record < record
    _exact_error(TypeError, global_solver.solve, _instance("C000"))
    _exact_error(TypeError, global_solver.solve, _instance("C000"), "Standard", 1)
    _exact_error(TypeError, global_solver.SolveResult, value)
    _exact_error(TypeError, global_solver.SolveStats, "Standard", ())


@pytest.mark.parametrize("route", ROUTES)
def test_gl16_standalone_diagnostics_have_no_history_equations(route):
    stat = _stats(route, 9)
    for records, origin in (((stat,), "Empty"), ((), "H2"), ((stat,) * 5, "L0")):
        result = global_solver.SolveStats(route, records, origin)
        assert result.branch_stats is records
        assert all(record is stat for record in result.branch_stats)
        assert result.attaining_candidate == origin
        assert result == global_solver.SolveStats(route, records, origin)


def _rejection(key, monkeypatch):
    """Explicit constructors for every registered malformed boundary request."""
    selection_values = {
        "none": None, "bool": True, "int": 0, "float": 1.0, "bytes": b"Standard",
        "lower": "standard", "upper": "STANDARD", "accelerated-lower": "accelerated",
        "leading": " Standard", "trailing": "Accelerated ", "empty": "",
        "str-subclass": _Str("Standard"), "enum": _Choice.STANDARD,
        "str-enum": _StringChoice.STANDARD, "callable": global_solver.solve_branch_standard,
    }
    for prefix, entry in (("REJ-solve-", "solve"), ("REJ-SolveStats-", "stats")):
        if key.startswith(prefix):
            suffix = key.removeprefix(prefix)
            if suffix in selection_values:
                if entry == "solve":
                    monkeypatch.setattr(Instance, "Q", property(_forbidden))
                    return global_solver.solve, (_instance("C000"), selection_values[suffix])
                return global_solver.SolveStats, (selection_values[suffix], (), "Empty")
    instance_args = {
        "none": None, "bool": True, "dict": {}, "tuple": (),
        "independent": brute.BruteInstance(2, ((0, 1, 1),), (1, 1)),
        "subclass": _Instance(2, ((0, 1, 1),), (1, 1)),
    }
    if key.startswith("REJ-instance-"):
        return global_solver.solve, (instance_args[key.removeprefix("REJ-instance-")], "Standard")
    if key == "REJ-validation-order":
        return global_solver.solve, (None, object())
    if key.startswith("REJ-value-"):
        value = {"none": None, "tuple": (0, 1), "subclass": _Value(0, 1)}[
            key.removeprefix("REJ-value-")
        ]
        return global_solver.SolveResult, (value, object())
    result_args = {
        "rescaled-empty": (ExactValue(0, 2), None),
        "nonzero-empty": (ExactValue(1, 1), None),
        "independent-witness": (ExactValue(0, 1), brute.Witness(1, ())),
        "tuple-witness": (ExactValue(0, 1), (1, ())),
        "witness-subclass": (ExactValue(0, 1), _Witness(1, ())),
    }
    if key.startswith("REJ-result-"):
        return global_solver.SolveResult, result_args[key.removeprefix("REJ-result-")]
    standard, accelerated = _stats("Standard"), _stats("Accelerated")
    bad_stats = {
        "list": ("Standard", [], "Empty"),
        "tuple-subclass": ("Standard", _Tuple(), "Empty"),
        "entry-none": ("Standard", (None,), "Empty"),
        "mixed": ("Standard", (standard, accelerated), "L0"),
        "wrong-standard": ("Standard", (accelerated,), "Empty"),
        "wrong-accelerated": ("Accelerated", (standard,), "Empty"),
        "entry-subclass": ("Standard", (_StandardStats(0, 0, 0, standard.oracle_stats),), "L0"),
        "origin-none": ("Standard", (), None),
        "origin-subclass": ("Standard", (), _Str("Baseline")),
        "origin-lower": ("Standard", (), "baseline"),
        "origin-unknown": ("Standard", (), "L2"),
    }
    return global_solver.SolveStats, bad_stats[key.removeprefix("REJ-stats-")]


@pytest.mark.parametrize("row", TABLES["U15_REJECTIONS"], ids=lambda row: row[0])
def test_gl1_gl2_registered_exact_public_rejections(row, monkeypatch):
    function, args = _rejection(row[0], monkeypatch)
    for name in ("BranchOracleContext", "solve_branch_standard", "solve_branch_accelerated"):
        monkeypatch.setattr(global_solver, name, _forbidden)
    _exact_error(ValueError, function, *args)


@pytest.mark.parametrize("route", ROUTES)
def test_gl3_genuine_empty_constructs_no_graph_dependency(route, monkeypatch):
    for name in ("BranchOracleContext", "solve_branch_standard", "solve_branch_accelerated",
                 "Witness", "witness_value", "compare_pairs", "shore_f", "shore_b_q", "shore_d_q"):
        monkeypatch.setattr(global_solver, name, _forbidden)
    instance = _instance("C000")
    result, stats = global_solver.solve(instance, route)
    assert type(result) is global_solver.SolveResult
    assert _pair(result.value) == (0, 1) and result.witness is None
    assert stats == global_solver.SolveStats(route, (), "Empty")
    independent = brute.brute_force(_independent(instance))
    assert independent.value == (0, 1) and independent.witness is None


class _Observation:
    """Test-owned transparent dependency spies, never a production trace API."""

    def __init__(self, patch, instance, route):
        self.instance = instance
        self.route = route
        self.events = []
        self.replies = []
        self.contexts = []
        self.wrapper_degrees = 0
        context_type = global_solver.BranchOracleContext
        branch_function = getattr(global_solver, _selected(route))
        evaluator = global_solver.witness_value
        compare = global_solver.compare_pairs
        degree_property = Instance.d_q

        def context(argument):
            assert argument is instance
            result = context_type(argument)
            self.contexts.append(result)
            self.events.append(("context", result))
            return result

        def branch(context, j):
            assert context is self.contexts[0]
            assert context.instance is instance
            self.events.append(("branch", j))
            result = branch_function(context, j)
            self.replies.append((j, *result))
            return result

        def evaluate(argument, witness):
            assert argument is instance
            value = evaluator(argument, witness)
            _verify(instance, witness, value)
            self.events.append(("value", witness, value))
            return value

        def comparison(left, right):
            sign = compare(left, right)
            difference = Fraction(*left) - Fraction(*right)
            assert sign == (difference > 0) - (difference < 0)
            self.events.append(("compare", left, right, sign))
            return sign

        def degrees(argument):
            if sys._getframe(1).f_globals is global_solver.__dict__:
                self.wrapper_degrees += 1
            return degree_property.__get__(argument, Instance)

        patch.setattr(global_solver, "BranchOracleContext", context)
        patch.setattr(global_solver, _selected(route), branch)
        patch.setattr(global_solver, _selected(ROUTES[1 - ROUTES.index(route)]), _forbidden)
        patch.setattr(global_solver, "witness_value", evaluate)
        patch.setattr(global_solver, "compare_pairs", comparison)
        patch.setattr(Instance, "d_q", property(degrees))

    def check(self, key, result, stats):
        assert type(result) is global_solver.SolveResult
        assert type(stats) is global_solver.SolveStats
        assert stats.branch_solver == self.route
        structure = STRUCTURE[key]
        assert len(self.contexts) == structure[1]
        positions = [i for i, event in enumerate(self.events) if event[0] == "value"]
        assert len(positions) == structure[3]
        if structure[5]:
            assert self.replies == [] and positions == [] and self.wrapper_degrees == 0
            assert _pair(result.value) == (0, 1) and result.witness is None
            assert stats.branch_stats == () and stats.attaining_candidate == "Empty"
            return ()
        assert self.wrapper_degrees == 1
        assert [j for j, _, _ in self.replies] == [0, 1, 2, 3]
        assert tuple(self.contexts[0].instance.edges) == self.instance.edges
        assert len(stats.branch_stats) == 4
        assert all(stats.branch_stats[j] is diagnostics for j, _, diagnostics in self.replies)
        expected = [("Baseline", BASELINES[key][2:5])]
        per_branch = []
        for j, reply, _ in self.replies:
            optimum = OPTIMA[key, j]
            if reply is None:
                assert optimum[2] is None
                per_branch.append(None)
                continue
            assert type(reply) is BranchResult
            assert reply.shore in optimum[3]
            row = SHORES[key, j, reply.shore]
            _, _, U, _, _, _, _, y, raw, _ = row
            N, D = raw
            A, B = reply.root
            if j < 2:
                assert N > D and A * (N - D) == B * D
            else:
                assert A * D == -B * N
            assert Fraction(N, D) == Fraction(*optimum[2])
            expected.append((BRANCH_NAMES[j], (U, y, raw)))
            per_branch.append(Fraction(N, D))
        if H2[key][1] is not None:
            expected.append(("H2", H2[key][1]))
        assert len(expected) == len(positions)
        incumbent = None
        winner = None
        candidate_comparisons = 0
        for k, (origin, reference) in enumerate(expected):
            position = positions[k]
            _, witness, value = self.events[position]
            assert _witness_record(witness, value) == reference
            prior_branches = [event[1] for event in self.events[:position] if event[0] == "branch"]
            if origin == "Baseline":
                assert prior_branches == []
                assert value.N >= value.D
                incumbent = _pair(value)
                winner = origin, witness, value
            else:
                if origin == "H2":
                    assert prior_branches == [0, 1, 2, 3]
                    assert _pair(value) == (4, 2)
                    assert H2[key][3] <= 0
                else:
                    assert prior_branches == list(range(BRANCH_NAMES.index(origin) + 1))
                stop = positions[k + 1] if k + 1 < len(positions) else len(self.events)
                comparisons = [event for event in self.events[position + 1:stop]
                               if event[0] == "compare"
                               and event[1:3] == (_pair(value), incumbent)]
                assert comparisons, (key, origin, "missing original endpoint comparison")
                candidate_comparisons += 1
                if Fraction(*_pair(value)) > Fraction(*incumbent):
                    incumbent = _pair(value)
                    winner = origin, witness, value
            assert Fraction(*incumbent) >= Fraction(*_pair(value))
            _verify(self.instance, winner[1], winner[2])
        assert candidate_comparisons == structure[4]
        assert stats.attaining_candidate == winner[0] == GLOBALS[key][3]
        assert result.witness is winner[1] and result.value is winner[2]
        assert _witness_record(result.witness, result.value) in GLOBALS[key][4]
        assert Fraction(*incumbent) == Fraction(*GLOBALS[key][1])
        return tuple(per_branch)


@pytest.mark.parametrize("key", tuple(INPUTS))
def test_gl4_gl15_every_registered_input_both_real_routes(key, monkeypatch):
    """379 paired cases; at least 758 real global calls, not a pytest count claim."""
    instance = _instance(key)
    snapshot = instance.to_dict()
    outcomes = []
    branches = []
    for route in ROUTES:
        with monkeypatch.context() as patch:
            observation = _Observation(patch, instance, route)
            result, stats = global_solver.solve(instance, route)
            branches.append(observation.check(key, result, stats))
            outcomes.append(result)
        assert instance.to_dict() == snapshot
    assert Fraction(*_pair(outcomes[0].value)) == Fraction(*_pair(outcomes[1].value))
    assert branches[0] == branches[1]
    if INPUTS[key][1] != "magnitude":
        independent = brute.brute_force(_independent(instance))
        for result in outcomes:
            assert Fraction(*_pair(result.value)) == Fraction(*independent.value)
            assert (result.witness is None) == (independent.witness is None)
    # No equality demand for cross-route witness objects or raw pair scales.


def test_gl13_gl21_registry_fingerprints_and_core_definition():
    assert len(INPUTS) == 379
    assert Counter(row[1] for row in INPUTS.values()) == {"core": 329, "named": 22, "magnitude": 28}
    assert _stream_hash(TABLES["U15_FINGERPRINTS"]) == (
        "f54e98f268255556585c6c88a94aeb5cc7841957731ccf22ac0f804de1e4b0f1"
    )
    for table, count, digest in TABLES["U15_FINGERPRINTS"]:
        assert len(TABLES[table]) == count
        assert _stream_hash(TABLES[table]) == digest
    generated = []
    for n in (2, 3):
        pairs = tuple(combinations(range(n), 2))
        for counts in product((0, 1, 2), repeat=len(pairs)):
            edges = tuple((u, v, q) for (u, v), q in zip(pairs, counts, strict=True) if q)
            degrees = tuple(sum(q for u, v, q in edges if vertex in (u, v)) for vertex in range(n))
            if not all(degrees):
                continue
            for f in product(*(range(1, degree + 1) for degree in degrees)):
                generated.append((n, edges, f, None))
    assert generated == [row[2:] for row in INPUTS.values() if row[1] == "core"]
    assert {row[1] for row in BASELINES.values()} == {
        "even", "odd-ge3", "unit-degree2", "matching",
    }
    assert {row[3] for row in GLOBALS.values()} == set(ORIGINS) - {"H2"}
    assert {row[2] for row in H2.values()} == {None, "one-edge", "split"}


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize("row", TABLES["U15_ROOT_BINDING"], ids=lambda row: row[0])
def test_gl9_scaled_roots_and_original_shore_binding(route, row, monkeypatch):
    _, key, branch_index, shore, root, outcome, raw = row
    instance = _instance(key)
    original = getattr(global_solver, _selected(route))
    evaluator = global_solver.witness_value
    reached = []
    evaluated = []

    def selected(context, j):
        result, stats = original(context, j)
        if j == branch_index:
            reached.append(j)
            return BranchResult(root, shore), stats
        return result, stats

    def evaluate(argument, witness):
        value = evaluator(argument, witness)
        evaluated.append(_witness_record(witness, value))
        _verify(argument, witness, value)
        return value

    monkeypatch.setattr(global_solver, _selected(route), selected)
    monkeypatch.setattr(global_solver, "witness_value", evaluate)
    if outcome == "RuntimeError":
        _exact_error(RuntimeError, global_solver.solve, instance, route)
    else:
        result, _ = global_solver.solve(instance, route)
        _verify(instance, result.witness, result.value)
        assert any(shore == U and pair == raw for U, _, pair in evaluated)
    assert reached == [branch_index]


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize("key", ("C020", "N-H1-WINNER"))
def test_gl16_diagnostics_do_not_change_mathematical_choices(route, key, monkeypatch):
    instance = _instance(key)
    original = getattr(global_solver, _selected(route))
    replies = []

    def selected(context, j):
        response = original(context, j)
        replies.append(response)
        return response

    monkeypatch.setattr(global_solver, _selected(route), selected)
    first, first_stats = global_solver.solve(instance, route)
    replacements = tuple(_stats(route, 10**100 + j) for j in range(4))

    def changed(_context, j):
        return replies[j][0], replacements[j]

    monkeypatch.setattr(global_solver, _selected(route), changed)
    second, second_stats = global_solver.solve(instance, route)
    assert first == second and first_stats.attaining_candidate == second_stats.attaining_candidate
    assert all(second_stats.branch_stats[j] is replacements[j] for j in range(4))
    _verify(instance, second.witness, second.value)


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize("row", TABLES["U15_FAULTS"][:18], ids=lambda row: row[0])
def test_gl7_explicit_broken_dependency_promises(route, row, monkeypatch):
    key, input_key, j_target, shore, _, _ = row
    instance = _instance(input_key)
    original = getattr(global_solver, _selected(route))
    evaluator = global_solver.witness_value
    phase = []
    reached = []

    def selected(context, j):
        phase.append(j)
        result, stats = original(context, j)
        if j != j_target:
            return result, stats
        reached.append("branch")
        if key == "FAULT-REPLY-LIST":
            return [result, stats]
        if key == "FAULT-REPLY-LENGTH":
            return (result,)
        if key == "FAULT-REPLY-RESULT":
            return ExactValue(1, 1), stats
        if key == "FAULT-REPLY-STATS":
            return result, _stats(ROUTES[1 - ROUTES.index(route)])
        if key == "FAULT-REPLY-NONE":
            return None
        if shore is not None:
            root = (SHORES[input_key, j, shore][9]
                    if key.startswith("FAULT-EVALUATOR-") else (0, 1))
            return BranchResult(root, shore), stats
        return result, stats

    def evaluate(argument, witness):
        value = evaluator(argument, witness)
        if not phase and key == "FAULT-BASELINE-SUBUNIT":
            reached.append("baseline")
            return ExactValue(0, 2)
        if phase == [0] and key.startswith("FAULT-EVALUATOR-"):
            reached.append("endpoint")
            if key.endswith("TYPE"):
                return value.N, value.D
            # Preserve numerical binding so only the literal raw-formula guard
            # detects this fault; a later root mismatch cannot mask that omission.
            return ExactValue(2 * value.N, 2 * value.D)
        if (phase == [0, 1, 2, 3] and witness.U == 1 and sum(witness.y) == 2
                and key == "FAULT-H2-RAW"):
            reached.append("H2")
            return ExactValue(2, 1)
        return value

    monkeypatch.setattr(global_solver, _selected(route), selected)
    monkeypatch.setattr(global_solver, "witness_value", evaluate)
    _exact_error(RuntimeError, global_solver.solve, instance, route)
    assert reached
    if key.startswith("FAULT-EVALUATOR-"):
        assert "endpoint" in reached
    elif key == "FAULT-BASELINE-SUBUNIT":
        assert reached == ["baseline"]
    elif key == "FAULT-H2-RAW":
        assert "H2" in reached


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize(
    "fault", ("tuple-subclass", "three-elements", "stats-subclass", "result-subclass"),
)
def test_gl7_additional_exact_reply_shapes(route, fault, monkeypatch):
    original = getattr(global_solver, _selected(route))
    reached = []

    class ResultSubclass(BranchResult):
        pass

    def selected(context, j):
        result, stats = original(context, j)
        reached.append(j)
        if fault == "tuple-subclass":
            return _Tuple((result, stats))
        if fault == "three-elements":
            return result, stats, None
        if fault == "result-subclass":
            return ResultSubclass(result.root, result.shore), stats
        cls = _StandardStats if route == "Standard" else _AcceleratedStats
        values = [getattr(stats, field.name) for field in dataclasses.fields(stats)]
        return result, cls(*values)

    monkeypatch.setattr(global_solver, _selected(route), selected)
    _exact_error(RuntimeError, global_solver.solve, _instance("C002"), route)
    assert reached == [0]


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize("row", TABLES["U15_FAULTS"][18:], ids=lambda row: row[0])
def test_gl7_synthetic_source_prerequisite_failures(route, row, monkeypatch):
    """Explicit property faults; no forged Instance or graph-optimality claim."""
    key, input_key, _, _, _, _ = row
    instance = _instance(input_key)
    original_degrees = Instance.d_q
    original_edges = Instance.edges
    original_branch = getattr(global_solver, _selected(route))
    entered = []
    after_branches = []

    if key == "FAULT-MATCHING-PROMISE":
        def degrees(argument):
            if sys._getframe(1).f_globals is global_solver.__dict__:
                entered.append("degrees")
                return (1,) * argument.n
            return original_degrees.__get__(argument, Instance)
        monkeypatch.setattr(Instance, "d_q", property(degrees))
    elif key == "FAULT-UNIT-PREREQUISITE":
        def bad_sum(*_args):
            entered.append("sum")
            return 0
        monkeypatch.setattr(global_solver, "shore_b_q", bad_sum)
    else:
        # Keep the real instance and baseline/earlier endpoints intact. After the
        # last solver reply (synthetic None), expose too few copies to the wrapper
        # only. Closed dependencies still see the actual canonical slot contents.
        def selected(context, j):
            response = original_branch(context, j)
            if j == 3:
                after_branches.append(True)
                return None, response[1]
            return response

        def edges(argument):
            actual = original_edges.__get__(argument, Instance)
            if after_branches and sys._getframe(1).f_globals is global_solver.__dict__:
                entered.append("copies")
                return tuple((u, v, 1) for u, v, _ in actual)
            return actual

        monkeypatch.setattr(global_solver, _selected(route), selected)
        monkeypatch.setattr(Instance, "edges", property(edges))
    _exact_error(RuntimeError, global_solver.solve, instance, route)
    assert entered


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize("row", TABLES["U15_EXCEPTIONS"], ids=lambda row: row[0])
@pytest.mark.parametrize("exception_type", (ValueError, RuntimeError, _Marker))
def test_gl17_dependency_exceptions_propagate_by_identity(route, row, exception_type, monkeypatch):
    _, key, seam, _, _ = row
    instance = _instance(key)
    marker = exception_type(row[0], route)
    phase = []
    hit = []
    original = getattr(global_solver, _selected(route))

    def selected(context, j):
        phase.append(j)
        if seam == f"branch-{j}":
            hit.append(seam)
            raise marker
        return original(context, j)

    monkeypatch.setattr(global_solver, _selected(route), selected)
    monkeypatch.setattr(global_solver, _selected(ROUTES[1 - ROUTES.index(route)]), _forbidden)
    if not seam.startswith("branch-"):
        stage, name = seam.split("-", 1) if "-" in seam else ("context", "BranchOracleContext")
        original_dependency = getattr(global_solver, name)

        def injected(*args, **kwargs):
            eligible = (
                stage == "context"
                or (stage == "baseline" and not phase)
                or (stage == "endpoint" and phase == [0])
            )
            # H2 follows H1; use its independently fixed witness/quotient to avoid
            # raising at the preceding branch endpoint instead of the intended seam.
            if stage == "H2":
                expected = H2[key][1]
                if name == "Witness":
                    eligible = phase == [0, 1, 2, 3] and tuple(args) == expected[:2]
                elif name == "witness_value":
                    eligible = phase == [0, 1, 2, 3] and (args[1].U, args[1].y) == expected[:2]
                else:
                    eligible = phase == [0, 1, 2, 3] and args[0] == (4, 2)
            if eligible:
                hit.append(seam)
                raise marker
            return original_dependency(*args, **kwargs)

        if name == "Witness":
            real_init = global_solver.Witness.__init__

            def injected_init(record, U, y):
                eligible = (
                    (stage == "baseline" and not phase)
                    or (stage == "endpoint" and phase == [0])
                    or (stage == "H2" and phase == [0, 1, 2, 3]
                        and (U, y) == H2[key][1][:2])
                )
                if eligible:
                    hit.append(seam)
                    raise marker
                real_init(record, U, y)

            monkeypatch.setattr(global_solver.Witness, "__init__", injected_init)
        else:
            monkeypatch.setattr(global_solver, name, injected)
    with pytest.raises(exception_type) as caught:
        global_solver.solve(instance, route)
    assert caught.value is marker and hit == [seam]


@pytest.mark.parametrize("key", ("N-EVEN-PRIORITY", "N-LABEL-STR", "N-LABEL-MIX", "C020"))
def test_gl18_repetition_interleaving_labels_and_no_mutable_aliases(key):
    instance = _instance(key)
    snapshot = instance.to_dict()
    saved = {route: global_solver.solve(instance, route) for route in ROUTES}
    for route in ("Accelerated", "Standard", "Standard", "Accelerated"):
        result, stats = global_solver.solve(instance, route)
        assert (result, stats) == saved[route]
        _verify(instance, result.witness, result.value)
        assert instance.to_dict() == snapshot
        without_labels = Instance(instance.n, instance.edges, instance.f)
        plain_result, plain_stats = global_solver.solve(without_labels, route)
        assert (plain_result, plain_stats) == saved[route]


@pytest.mark.parametrize("row", TABLES["U15_COMPARISONS"], ids=lambda row: row[0])
def test_gl10_registered_comparison_traps(row):
    """Pure comparator controls; actual graph choices tested in paired corpus."""
    _, left, right, sign, _, _ = row
    assert global_solver.compare_pairs(left, right) == sign
    a, b = Fraction(*left), Fraction(*right)
    assert sign == (a > b) - (a < b)


def test_gl19_direct_import_exactness_and_compact_source_controls():
    tree = ast.parse(Path(global_solver.__file__).read_text(encoding="utf-8"))
    allowed = {
        "__future__": {"annotations"}, "dataclasses": {"dataclass"},
        "instance": {"Instance"}, "oracle": {"BranchOracleContext"},
        "branch": {"BranchResult", "StandardBranchStats", "AcceleratedBranchStats",
                   "solve_branch_standard", "solve_branch_accelerated"},
        "rational": {"compare_pairs"},
        "witness": {"ExactValue", "Witness", "shore_f", "shore_b_q", "shore_d_q", "witness_value"},
    }
    forbidden_calls = {"float", "set", "frozenset", "open", "eval", "exec", "compile",
                       "__import__", "gcd", "Fraction", "Decimal", "round"}
    for node in ast.walk(tree):
        assert not isinstance(node, (ast.Import, ast.Div, ast.FloorDiv, ast.Set, ast.SetComp))
        if isinstance(node, ast.Constant):
            assert type(node.value) is not float
        if isinstance(node, ast.ImportFrom):
            module = node.module.removeprefix("exactfrac.")
            assert module in allowed
            assert {name.name for name in node.names} <= allowed[module]
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                assert node.func.id not in forbidden_calls
            if isinstance(node.func, ast.Name) and node.func.id == "range":
                for argument in node.args:
                    assert not any(
                        isinstance(part, (ast.Pow, ast.LShift)) for part in ast.walk(argument)
                    )
                    assert not any(isinstance(part, ast.Attribute) and part.attr in {"q", "f", "Q"}
                                   for part in ast.walk(argument))
        if isinstance(node, ast.Attribute):
            assert node.attr != "families"
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            assert not any(isinstance(part, ast.Call) and isinstance(part.func, ast.Name)
                           and part.func.id == node.name for part in ast.walk(node))
    for name, value in vars(global_solver).items():
        if not name.startswith("__"):
            assert not isinstance(value, (list, dict, set)), (name, "mutable module state")
    # Verify the independently closed implementation remains solver-blind.
    verifier_tree = ast.parse(Path(brute.__file__).read_text(encoding="utf-8"))
    for node in ast.walk(verifier_tree):
        if isinstance(node, ast.Import):
            assert all(not name.name.startswith("exactfrac") for name in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert not (node.module or "").startswith("exactfrac")


def test_gl19_fresh_process_direct_import_isolation():
    program = '''
import builtins, importlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
original = builtins.__import__
seen = []
def guarded(name, globals=None, locals=None, fromlist=(), level=0):
    if globals and globals.get('__name__') == 'exactfrac.solve':
        seen.append((name, fromlist, level))
    return original(name, globals, locals, fromlist, level)
builtins.__import__ = guarded
module = importlib.import_module('exactfrac.solve')
assert module.__all__ == ('SolveResult', 'SolveStats', 'solve')
assert not any(name.startswith('exactfrac_verify') for name in sys.modules)
origins = {}
for name, item in tuple(sys.modules.items()):
    if name == 'exactfrac' or name.startswith('exactfrac.'):
        origin = pathlib.Path(item.__file__).resolve()
        assert origin.is_relative_to(root / 'exactfrac')
        origins[name] = str(origin)
print(json.dumps({'direct': seen, 'origins': origins}, sort_keys=True))
'''
    run = subprocess.run(
        [sys.executable, "-I", "-B", "-c", program, str(ROOT)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    observed = json.loads(run.stdout)
    assert "exactfrac.solve" in observed["origins"]
    allowed = {"__future__", "dataclasses", "instance", "branch", "oracle", "rational", "witness"}
    assert all(name.removeprefix("exactfrac.") in allowed for name, _, _ in observed["direct"])
