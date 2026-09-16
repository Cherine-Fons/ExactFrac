"""Unit 16 consuming tests fixed against committed human oracles before telemetry.

The direct telemetry import is the sole intended collection failure at RED.
Reference source strings are never executed. Measured runs and legacy calls are
separate observations; finite checks do not establish a universal complexity bound.
"""
from __future__ import annotations

import ast
import dataclasses
import inspect
import math
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path

import pytest

# isort: split
import exactfrac.telemetry as telemetry

# isort: split
from _telemetry_source_audit import (
    ADAPTER_RECIPES,
    PRIMITIVES,
    ROOT,
    _coefficient_statement_covers,
    _mark_coefficient_bound_statement,
    assert_inventory_complete,
    assert_source,
    assert_test_adaptation,
    at_path,
    audit_legacy,
    canonical,
    functions,
    inventory_from_sources,
    inventory_sources,
    legacy_bytes,
    load_reference,
    load_tables,
    row_digest,
    tables_from,
)

# isort: split
from exactfrac import _telemetry as primitive

# isort: split
from exactfrac import branch, families, flow, oracle, parity_cut, rational, sign_routing
from exactfrac import solve as global_solver
from exactfrac.instance import Instance
from exactfrac_verify import brute

TABLES = load_tables()
U15 = tables_from((ROOT / "docs/ORACLE_CATALOG.md").read_text(encoding="utf-8"), "U15_")
WORK_FIELDS = tuple(row[1] for row in TABLES["U16_WORK_FIELDS"])
INPUTS = tuple(("U15:" + r[0], r[2], r[3], r[4], r[5]) for r in U15["U15_INPUTS"]) + tuple(
    ("U16:" + r[0], *r[1:]) for r in TABLES["U16_INPUTS"]
)
COVERS = {(r[0], r[1]): r[2:] for r in TABLES["U16_COVERS"]}
ROUTES = ("Standard", "Accelerated")
FIELDS = {
    "WorkStats": WORK_FIELDS,
    "BranchTelemetry": ("branch", "feasible", "work"),
    "AlgorithmStats": ("native", "total", "nonbranch", "branches",
                       "output_numerator_bits", "output_denominator_bits"),
    "RunMetadata": ("wall_clock_s", "python_version", "platform", "cpu", "code_version",
                    "instance_sha256"),
    "RunRecord": ("algorithm", "metadata"),
}


def _bits(value):
    assert type(value) is int
    return max(1, abs(value).bit_length())


def _instance(row):
    _, n, edges, f, labels = row
    return Instance(n, tuple(map(tuple, edges)), tuple(f),
                    labels=None if labels is None else tuple(labels))


def _named(name):
    return _instance(next(r for r in INPUTS if r[0] == "U16:" + name))


def _raw(result):
    return result.value.N, result.value.D


def _tuple(work):
    return tuple(getattr(work, f) for f in WORK_FIELDS)


def _work(values):
    return telemetry.WorkStats(*values)


def _aggregate(parts):
    return tuple(sum(getattr(p, f) for p in parts) if i < 20 else max(getattr(p, f) for p in parts)
                 for i, f in enumerate(WORK_FIELDS))


def _verify(instance, result):
    if result.witness is None:
        assert instance.Q == 1 and _raw(result) == (0, 1)
        return
    other = brute.BruteInstance(instance.n, instance.edges, instance.f)
    witness = brute.Witness(result.witness.U, result.witness.y)
    assert brute.witness_is_admissible(other, witness)
    assert brute.witness_raw_value(other, witness) == _raw(result)


def _native_fields(route, native):
    if route == "Standard":
        return (native.outer_iterations, native.oracle_calls, native.newton_updates,
                0, native.newton_updates, 0, 0, 0, 0, 0, 0, 0)
    terminal = native.lookahead_queries - native.lookahead_accepted - native.lookahead_rejected
    feasible = native.oracle_calls != 1
    return (native.outer_iterations, native.oracle_calls, 0, native.newton_queries,
            native.newton_queries, native.lookahead_queries, native.lookahead_accepted,
            native.lookahead_rejected, terminal, native.early_returns - terminal,
            int(feasible and native.outer_iterations == 0), native.early_returns)


def _assert_stats(key, instance, result, stats, native):
    assert type(stats) is telemetry.AlgorithmStats and stats.native is native
    assert stats.branch_solver == native.branch_solver
    assert stats.attaining_branch == native.attaining_candidate
    assert (stats.output_numerator_bits, stats.output_denominator_bits) == tuple(
        map(_bits, _raw(result))
    )
    assert type(stats.branches) is tuple
    assert tuple(b.branch for b in stats.branches) == (
        () if result.witness is None else (0, 1, 2, 3)
    )
    assert _tuple(stats.nonbranch)[:22] == (0,) * 22
    assert _tuple(stats.total) == _aggregate([stats.nonbranch, *(b.work for b in stats.branches)])
    for b, previous in zip(stats.branches, native.branch_stats, strict=True):
        assert type(b) is telemetry.BranchTelemetry and type(b.work) is telemetry.WorkStats
        prepared, nonempty, _, per_query = COVERS[key, b.branch]
        w, o = b.work, previous.oracle_stats
        assert _tuple(w)[:12] == _native_fields(native.branch_solver, previous)
        assert b.feasible is (nonempty > 0)
        assert w.peak_numerator_bits >= 1 and w.peak_denominator_bits >= 1
        if not b.feasible:
            assert (w.peak_numerator_bits, w.peak_denominator_bits) == (1, 1)
        assert w.atomic_families_enumerated == prepared
        assert w.atomic_families_examined == o.atomic_families_examined == prepared * w.oracle_calls
        assert w.atomic_families_feasible == o.atomic_families_feasible == nonempty * w.oracle_calls
        assert w.parity_cut_calls == o.parity_cut_calls == w.atomic_families_feasible
        assert w.ordinary_min_cut_calls == o.ordinary_min_cut_calls == per_query * w.oracle_calls
        assert w.max_flow_calls == o.max_flow_calls == w.ordinary_min_cut_calls
        assert (w.augmentations, w.bfs_scans, w.flow_peak_generated_value) == (
            o.flow_augmentations, o.flow_bfs_scans, o.flow_peak_generated_value,
        )
        assert w.flow_peak_bits == (
            0 if w.max_flow_calls == 0 else _bits(w.flow_peak_generated_value)
        )
        assert w.peak_integer_bits >= max(
            w.peak_numerator_bits, w.peak_denominator_bits, w.flow_peak_bits
        )
    assert stats.total.peak_numerator_bits >= stats.output_numerator_bits
    assert stats.total.peak_denominator_bits >= stats.output_denominator_bits
    assert stats.total.peak_integer_bits >= max(stats.total.peak_numerator_bits,
                                               stats.total.peak_denominator_bits)


def _replace_entry(monkeypatch, replacement):
    """Intercept the single legacy call without prescribing its imported alias."""
    original = global_solver.solve
    names = [name for name, value in vars(telemetry).items() if value is original]
    if names:
        for name in names:
            monkeypatch.setattr(telemetry, name, replacement)
    else:
        assert any(value is global_solver for value in vars(telemetry).values())
        monkeypatch.setattr(global_solver, "solve", replacement)
    return original


def _probe(monkeypatch, action, route="Standard"):
    original = global_solver.solve
    calls = []

    def instrumented(instance, choice):
        action()
        answer = original(instance, choice)
        calls.append(answer)
        return answer

    with monkeypatch.context() as patch:
        _replace_entry(patch, instrumented)
        result, stats = telemetry.solve_with_telemetry(_named("Q1"), route)
    assert len(calls) == 1 and result is calls[0][0] and stats.native is calls[0][1]
    return result, stats


def _synthetic_stats():
    rows = dict(TABLES["U16_AGGREGATION"])
    native = []
    branches = []
    for j in range(4):
        w = rows["branch" + str(j)]
        o = oracle.BranchOracleStats(w[13], w[14], w[15], w[16], w[18], w[19], w[20])
        native.append(branch.StandardBranchStats(w[1], w[0], w[2], o))
        branches.append(telemetry.BranchTelemetry(j, j != 2, _work(w)))
    return telemetry.AlgorithmStats(
        global_solver.SolveStats("Standard", tuple(native), "Baseline"),
        _work(rows["total"]), _work(rows["nonbranch"]), tuple(branches), 1, 1,
    )


def _metadata():
    return telemetry.RunMetadata(None, "3.14.6", "darwin", None, "reference", "0" * 64)


@pytest.mark.parametrize("row", INPUTS, ids=[r[0] for r in INPUTS])
def test_te02_te08_all_registered_inputs_both_real_routes(row, monkeypatch):
    key = row[0]
    instance = _instance(row)
    values = []
    for route in ROUTES:
        legacy = global_solver.solve(instance, route)
        original = global_solver.solve
        answers = []

        def once(i, r, _instance=instance, _route=route, _original=original, _answers=answers):
            assert i is _instance and r == _route
            answer = _original(i, r)
            _answers.append(answer)
            return answer

        with monkeypatch.context() as patch:
            _replace_entry(patch, once)
            result, stats = telemetry.solve_with_telemetry(instance, route)
        assert len(answers) == 1
        assert result is answers[0][0] and stats.native is answers[0][1]
        assert (result, stats.native) == legacy
        _verify(instance, result)
        _assert_stats(key, instance, result, stats, answers[0][1])
        repeat_result, repeat_stats = telemetry.solve_with_telemetry(instance, route)
        assert repeat_result == result and repeat_stats == stats
        values.append(Fraction(*_raw(result)))
    assert values[0] == values[1]


def test_te01_exact_record_layout_required_arguments_and_immutability():
    stats = _synthetic_stats()
    samples = {
        "WorkStats": stats.total, "BranchTelemetry": stats.branches[0],
        "AlgorithmStats": stats, "RunMetadata": _metadata(),
        "RunRecord": telemetry.RunRecord(stats, _metadata()),
    }
    for name, expected_fields in FIELDS.items():
        cls, sample = getattr(telemetry, name), samples[name]
        assert dataclasses.is_dataclass(cls)
        assert tuple(f.name for f in dataclasses.fields(cls)) == expected_fields
        assert cls.__dataclass_params__.frozen and not cls.__dataclass_params__.order
        assert not hasattr(sample, "__dict__")
        signature = inspect.signature(cls)
        assert tuple(signature.parameters) == expected_fields
        assert all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
                   and p.default is inspect.Parameter.empty for p in signature.parameters.values())
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(sample, expected_fields[0], None)
        with pytest.raises(TypeError):
            cls()
        with pytest.raises(TypeError):
            cls(*(getattr(sample, f) for f in expected_fields), None)
        with pytest.raises(TypeError):
            cls(**{f: getattr(sample, f) for f in expected_fields}, unexpected=None)
    signature = inspect.signature(telemetry.solve_with_telemetry)
    assert tuple(signature.parameters) == ("instance", "branch_solver")
    assert all(p.default is inspect.Parameter.empty
               and p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
               for p in signature.parameters.values())
    assert stats.branch_solver == stats.native.branch_solver
    assert stats.attaining_branch == stats.native.attaining_candidate


class IntSubclass(int):
    pass


class StrSubclass(str):
    pass


class FloatSubclass(float):
    pass


class BoolDuck:
    def __bool__(self):
        raise AssertionError("public data must not be coerced")


def _bad(symbol, stats):
    values = {
        "TRUE": True, "INT_SUBCLASS": IntSubclass(0), "-1": -1, "4": 4,
        "STR_ZERO": "0", "FLOAT_ZERO": 0.0, "INT_ZERO": 0, "ZERO": 0,
        "NONE": None, "BOOL_DUCK": BoolDuck(), "TUPLE": (),
        "STR_SUBCLASS": StrSubclass("Standard"), "FLOAT_SUBCLASS": FloatSubclass(0.0),
        "NEGATIVE_FLOAT": -0.5, "NAN": math.nan, "POS_INF": math.inf, "NEG_INF": -math.inf,
        "EMPTY_STRING": "", "UPPERCASE_HASH": "A" * 64, "63_HEX": "0" * 63,
        "65_HEX": "0" * 65, "NONHEX": "g" * 64, "standard": "standard", "AUTO": "AUTO",
        "INSTANCE_DUCK": BoolDuck(),
    }
    if symbol in values:
        return values[symbol]
    if symbol == "WORK_SUBCLASS":
        cls = type("WorkSubclass", (telemetry.WorkStats,), {})
        return cls(*_tuple(stats.total))
    if symbol == "SOLVESTATS_SUBCLASS":
        cls = type("SolveStatsSubclass", (global_solver.SolveStats,), {})
        return cls("Standard", stats.native.branch_stats, "Baseline")
    if symbol == "INSTANCE_SUBCLASS":
        return object.__new__(type("InstanceSubclass", (Instance,), {}))
    if symbol == "LIST":
        return list(stats.branches)
    if symbol == "ITERATOR":
        return iter(stats.branches)
    if symbol == "MISSING_BRANCH":
        return stats.branches[:-1]
    if symbol == "DUPLICATE_BRANCH":
        return (stats.branches[0],) * 4
    if symbol == "REVERSED_BRANCHES":
        return stats.branches[::-1]
    if symbol in {"SUM_PEAKS", "MAX_COUNTS", "WRONG_NATIVE_MAPPING"}:
        parts = [stats.nonbranch, *(b.work for b in stats.branches)]
        field, value = {
            "SUM_PEAKS": ("peak_integer_bits", sum(w.peak_integer_bits for w in parts)),
            "MAX_COUNTS": ("outer_iterations", max(w.outer_iterations for w in parts)),
            "WRONG_NATIVE_MAPPING": ("newton_queries", 1),
        }[symbol]
        return dataclasses.replace(stats.total, **{field: value})
    if symbol in {"NONZERO_ORACLE_CALLS", "NONZERO_PREPARATION"}:
        field = "oracle_calls" if symbol == "NONZERO_ORACLE_CALLS" else "atomic_families_enumerated"
        return dataclasses.replace(stats.nonbranch, **{field: 1})
    raise AssertionError("unhandled registered rejection " + symbol)


@pytest.mark.parametrize(
    "row", TABLES["U16_REJECTIONS"], ids=[r[0] for r in TABLES["U16_REJECTIONS"]]
)
def test_te01_te08_te20_all_registered_rejections(row):
    _, target, field, symbol, exception, _ = row
    stats = _synthetic_stats()
    expected = TypeError if exception == "TypeError" else ValueError
    with pytest.raises(expected) as raised:
        if target == "public signatures":
            if symbol == "MISSING_ARGUMENT":
                telemetry.solve_with_telemetry(_named("Q1"))
            elif symbol == "EXTRA_POSITIONAL":
                telemetry.solve_with_telemetry(_named("Q1"), "Standard", None)
            else:
                telemetry.solve_with_telemetry(_named("Q1"), "Standard", unexpected=None)
        elif target == "RunRecord":
            telemetry.RunRecord(None if symbol == "BAD_ALGORITHM" else stats,
                                None if symbol == "BAD_METADATA" else _metadata())
        elif target == "solve_with_telemetry":
            args = {"instance": _named("Q1"), "branch_solver": "Standard"}
            args[field] = _bad(symbol, stats)
            telemetry.solve_with_telemetry(**args)
        else:
            base = {"WorkStats": stats.branches[0].work, "BranchTelemetry": stats.branches[0],
                    "AlgorithmStats": stats, "RunMetadata": _metadata()}[target]
            bad = (StrSubclass("0" * 64) if symbol == "STR_SUBCLASS"
                   and field == "instance_sha256" else _bad(symbol, stats))
            dataclasses.replace(base, **{field: bad})
    assert type(raised.value) is expected


def test_te01_public_validation_precedes_all_graph_access(monkeypatch):
    calls = []
    _replace_entry(monkeypatch, lambda *args: calls.append(args))
    with pytest.raises(ValueError) as raised:
        telemetry.solve_with_telemetry(object.__new__(Instance), "AUTO")
    assert type(raised.value) is ValueError and calls == []
    with pytest.raises(ValueError) as raised:
        telemetry.solve_with_telemetry(BoolDuck(), BoolDuck())
    assert type(raised.value) is ValueError and calls == []


@pytest.mark.parametrize("row", TABLES["U16_INPUTS"], ids=[r[0] for r in TABLES["U16_INPUTS"]])
def test_te03_te07_registered_real_traces_and_all_native_fields(row, monkeypatch):
    key = row[0]
    instance = _instance(("U16:" + key, *row[1:]))
    original = branch.exact_branch_min
    for route in ROUTES:
        seen = []

        def query(context, j, parameter, _seen=seen):
            result, native = original(context, j, parameter)
            reply = None if result is None else (result.shore, result.c, result.h, result.residual)
            _seen.append((j, tuple(parameter), reply))
            return result, native

        with monkeypatch.context() as patch:
            patch.setattr(branch, "exact_branch_min", query)
            result, stats = telemetry.solve_with_telemetry(instance, route)
        wanted = [(r[2], tuple(r[5]), None if r[6] is None else tuple(r[6]))
                  for r in TABLES["U16_GRAPH_TRACES"] if r[:2] == [key, route]]
        assert seen == wanted
        reference = next(r for r in TABLES["U16_GLOBAL_REFERENCE"] if r[:2] == [key, route])
        assert _raw(result) == tuple(reference[2])
        assert stats.attaining_branch == reference[6]
        for b in stats.branches:
            cr = next(r for r in TABLES["U16_BRANCH_COUNTERS"] if r[:3] == [key, route, b.branch])
            observed = _tuple(b.work)
            assert observed[:12] == tuple(cr[3])
            assert observed[12:18] == (*cr[4:9], cr[8])
            backend = next(
                r for r in TABLES["U16_NATIVE_BACKEND"] if r[:3] == [key, route, b.branch]
            )
            assert observed[18:22] == tuple(backend[3:7])


@pytest.mark.parametrize(
    "row", TABLES["U16_BITS"], ids=[str(i) for i in range(len(TABLES["U16_BITS"]))]
)
def test_te09_integer_tap_bit_convention_and_identity(row, monkeypatch):
    value, bits = row
    assert primitive._tap_int(value) is value
    baseline = telemetry.solve_with_telemetry(_named("Q1"), "Standard")[1]

    def action():
        assert primitive._tap_int(value) is value

    _, measured = _probe(monkeypatch, action)
    assert measured.nonbranch.peak_integer_bits == max(bits, baseline.nonbranch.peak_integer_bits)


@pytest.mark.parametrize(
    "row", TABLES["U16_PAIR_STREAMS"], ids=[r[0] for r in TABLES["U16_PAIR_STREAMS"]]
)
def test_te09_te14_raw_pair_streams_and_no_normalization(row, monkeypatch):
    _, scalars, pairs, peak, numerator_peak, denominator_peak, _, _ = row
    base = telemetry.solve_with_telemetry(_named("Q1"), "Standard")[1]

    def action():
        for value in scalars:
            assert primitive._tap_int(value) is value
        for values in pairs:
            pair = tuple(values)
            assert primitive._tap_pair(pair) is pair

    result, measured = _probe(monkeypatch, action)
    assert _raw(result) == (0, 1)
    assert measured.output_numerator_bits == measured.output_denominator_bits == 1
    assert measured.nonbranch.peak_integer_bits == max(peak, base.nonbranch.peak_integer_bits)
    assert measured.nonbranch.peak_numerator_bits == max(
        numerator_peak, base.nonbranch.peak_numerator_bits
    )
    assert measured.nonbranch.peak_denominator_bits == max(
        denominator_peak, base.nonbranch.peak_denominator_bits
    )


@pytest.mark.parametrize("row", [r for r in TABLES["U16_ARITHMETIC"] if r[0].startswith((
    "residual-cancel", "reflect-cancel", "reflect-denominator",
    "comparison-left", "comparison-right",
))], ids=lambda r: r[0])
def test_te11_real_rational_operations_observe_cancelling_products(row, monkeypatch):
    key, _, pairs, expected, _, peak, _ = row
    env = dict(pairs)
    results = []

    def action():
        if key.startswith("residual"):
            results.append(rational.residual_numerator((env["A"], env["B"]), env["c"], env["h"]))
        elif key.startswith("reflect-cancel"):
            results.append(rational.pair_reflect((env["A"], env["B"]), (env["C"], env["D"]))[0])
        elif key.startswith("reflect-denominator"):
            results.append(rational.pair_reflect((0, env["B"]), (0, env["D"]))[1])
        elif key.startswith("comparison-left"):
            results.append(rational.compare_pairs((env["N"], 1), (0, env["E"])))
        else:
            results.append(rational.compare_pairs((0, env["D"]), (env["M"], 1)))

    _, measured = _probe(monkeypatch, action)
    assert results == ([1] if key.startswith("comparison-left") else
                       [-1] if key.startswith("comparison-right") else [expected])
    assert measured.nonbranch.peak_integer_bits == peak
    assert measured.total.flow_peak_generated_value == measured.total.flow_peak_bits == 0
    assert measured.output_numerator_bits == measured.output_denominator_bits == 1


@pytest.mark.parametrize(
    "row", TABLES["U16_SUM_STREAMS"], ids=[r[0] for r in TABLES["U16_SUM_STREAMS"]]
)
def test_te12_signed_prefixes_and_executed_dominance(row, monkeypatch):
    _, terms, prefixes, final, valid, peak, _ = row
    assert (all(x >= 0 for x in terms), sum(terms)) == (valid, final)
    if valid:
        assert max(prefixes) == final
    seen = []

    def action():
        value = 0
        primitive._observe_ints(value)
        seen.append(value)
        for term in terms:
            value += term
            primitive._observe_ints(value)
            seen.append(value)

    base = telemetry.solve_with_telemetry(_named("Q1"), "Standard")[1]
    _, measured = _probe(monkeypatch, action)
    assert seen == list(prefixes)
    assert measured.nonbranch.peak_integer_bits == max(peak, base.nonbranch.peak_integer_bits)


@pytest.mark.parametrize(
    "row", TABLES["U16_FLOW_CASES"], ids=[r[0] for r in TABLES["U16_FLOW_CASES"]]
)
def test_te07_te13_local_flow_definition_and_numeric_measurement(row, monkeypatch):
    _, n, s, t, arcs, value, shore, aug, scans, peak, _ = row
    cuts = [(sum(c for a, b, c in arcs if U >> a & 1 and not U >> b & 1), U)
            for U in range(1 << n) if U >> s & 1 and not U >> t & 1]
    optimum = min(v for v, _ in cuts)
    least = (1 << n) - 1
    for v, U in cuts:
        if v == optimum:
            least &= U
    assert (value, shore) == (optimum, least)
    observed = []

    def action():
        observed.append(flow.minimum_cut(n, s, t, tuple(map(tuple, arcs))))

    _, stats = _probe(monkeypatch, action)
    result = observed[0]
    assert (result.value, result.source_shore, result.stats.augmentations,
            result.stats.bfs_scans, result.stats.peak_generated_value) == (
                value, shore, aug, scans, peak
            )
    assert stats.nonbranch.peak_integer_bits >= max(_bits(n), _bits(shore), _bits(peak))
    # This deliberately injected local call is not a native global branch event.
    assert stats.native.branch_stats == ()


@pytest.mark.parametrize(
    "row", TABLES["U16_REDUCTIONS"], ids=[r[0] for r in TABLES["U16_REDUCTIONS"]]
)
def test_te13_local_reduced_coordinates_and_masks(row, monkeypatch):
    _, n, T, pi, inside, outside, classes, _, terminal, count = row
    family = families.AtomicFamily(T, pi, inside, outside)
    network = sign_routing.SignRoutedNetwork(n, (), 0, 0)
    result = []

    def action():
        result.append(parity_cut.reduce_atomic_family(network, family))

    _, stats = _probe(monkeypatch, action)
    if count:
        assert result[0].classes == tuple(classes) and result[0].terminal_mask == terminal
        assert stats.total.peak_integer_bits >= max(map(_bits, classes))
    else:
        assert result == [None]


def test_te09_synthetic_zero_flow_and_aggregate_construction():
    stats = _synthetic_stats()
    assert _tuple(stats.total) == tuple(dict(TABLES["U16_AGGREGATION"])["total"])
    assert _tuple(stats.total) == _aggregate([stats.nonbranch, *(b.work for b in stats.branches)])
    zero = [0] * len(WORK_FIELDS)
    assert _work(zero).flow_peak_bits == 0
    zero[16] = zero[17] = zero[21] = zero[24] = 1
    assert _work(zero).flow_peak_bits == 1
    bad = list(zero)
    bad[21] = 0
    with pytest.raises(ValueError):
        _work(bad)


def test_te13_huge_labels_do_not_enter_algorithm_statistics():
    for route in ROUTES:
        unlabeled = telemetry.solve_with_telemetry(_named("DOUBLE"), route)
        labeled = telemetry.solve_with_telemetry(_named("LABEL-4096"), route)
        assert unlabeled == labeled
        assert labeled[1].total.peak_integer_bits < 4096


def test_te15_injected_numeric_maximum_cannot_change_mathematical_decisions(monkeypatch):
    instance = _named("REJECT0")
    for route in ROUTES:
        expected = global_solver.solve(instance, route)
        original = global_solver.solve
        canary = 1 << 2048
        calls = []

        def with_large_record(i, r, _canary=canary, _original=original, _calls=calls):
            primitive._observe_ints(_canary)
            answer = _original(i, r)
            _calls.append(answer)
            return answer

        with monkeypatch.context() as patch:
            _replace_entry(patch, with_large_record)
            result, stats = telemetry.solve_with_telemetry(instance, route)
        assert len(calls) == 1 and result is calls[0][0] and stats.native is calls[0][1]
        assert (result, stats.native) == expected
        assert stats.nonbranch.peak_integer_bits == 2049
        assert stats.total.peak_integer_bits == 2049


def test_te16_nested_rejection_before_second_call_and_successive_cleanup(monkeypatch):
    instance = _named("DOUBLE")
    original = global_solver.solve
    calls = []

    def nested(i, route):
        calls.append((i, route))
        with pytest.raises(ValueError) as raised:
            telemetry.solve_with_telemetry(i, route)
        assert type(raised.value) is ValueError
        return original(i, route)

    for route in ROUTES:
        base = telemetry.solve_with_telemetry(instance, route)
        with monkeypatch.context() as patch:
            _replace_entry(patch, nested)
            observed = telemetry.solve_with_telemetry(instance, route)
        assert observed == base == telemetry.solve_with_telemetry(instance, route)
    assert len(calls) == 2


@pytest.mark.parametrize("seam", ("entry", "oracle", "recorder"))
def test_te16_dependency_exception_identity_and_recorder_cleanup(seam, monkeypatch):
    instance = _named("DOUBLE")
    before = telemetry.solve_with_telemetry(instance, "Accelerated")
    failure = RuntimeError("unique recorder/dependency failure")

    def broken(*_args, **_kwargs):
        raise failure

    with monkeypatch.context() as patch:
        if seam == "entry":
            _replace_entry(patch, broken)
        elif seam == "oracle":
            patch.setattr(branch, "exact_branch_min", broken)
        else:
            # Patch every existing imported binding of this one leaf tap as a test seam.
            old = primitive._tap_int
            for module in (primitive, rational, global_solver, flow, families, oracle,
                           sign_routing, parity_cut, telemetry):
                for name, value in tuple(vars(module).items()):
                    if value is old:
                        patch.setattr(module, name, broken)
        with pytest.raises(RuntimeError) as raised:
            telemetry.solve_with_telemetry(instance, "Accelerated")
        assert raised.value is failure
    assert global_solver.solve(instance, "Accelerated") == (before[0], before[1].native)
    assert telemetry.solve_with_telemetry(instance, "Accelerated") == before


def test_te16_separate_thread_measurements_have_disjoint_state():
    jobs = [(_named("DOUBLE"), "Standard"), (_named("ZERO"), "Accelerated"),
            (_named("REJECT0"), "Standard"), (_named("ACCEPT3"), "Accelerated")]
    wanted = [telemetry.solve_with_telemetry(*job) for job in jobs]
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(telemetry.solve_with_telemetry, *job) for job in jobs]
        observed = [future.result() for future in futures]
    assert observed == wanted
    assert [telemetry.solve_with_telemetry(*job) for job in jobs] == wanted


def test_te17_te18_complete_source_erasure_and_exact_legacy_adapters():
    report = audit_legacy(require_sites=True)
    assert report == {"direct_sites": 237, "post_stores": 25,
                      "legacy_files": 27, "guard_functions": 17}
    assert len({row["path"] for row in ADAPTER_RECIPES}) == 11
    assert (ROOT / "exactfrac/branch.py").read_bytes() == legacy_bytes("exactfrac/branch.py")


@pytest.mark.parametrize(
    "fault", ("comparison", "extra-evaluation", "missing-site", "arbitrary-import")
)
def test_te17_erasure_rejects_controlled_source_faults(fault):
    tables, reference = load_tables(), load_reference()
    name = "exactfrac/rational.py"
    source = (ROOT / name).read_text(encoding="utf-8")
    assert_source(name, source.encode(), tables, reference)
    def replace_node(node, replacement):
        lines = source.splitlines(keepends=True)
        start = sum(map(len, lines[:node.lineno - 1])) + node.col_offset
        end = sum(map(len, lines[:node.end_lineno - 1])) + node.end_col_offset
        return source[:start] + replacement + source[end:]

    message = None
    if fault == "comparison":
        tree = ast.parse(source)
        candidate = next(n for n in ast.walk(tree) if isinstance(n, ast.Compare)
                         and isinstance(n.ops[0], ast.LtE))
        old = ast.get_source_segment(source, candidate)
        mutated = replace_node(candidate, old.replace("<=", "<", 1))
    elif fault == "extra-evaluation":
        mutated = source + "\n_observe_ints(open('unapproved'))\n"
    elif fault == "arbitrary-import":
        mutated = source + "\nfrom ._telemetry import arbitrary_hook\n"
    else:
        tree = ast.parse(source)
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                        and n.name == "residual_numerator")
        tap = next(n for n in ast.walk(function) if isinstance(n, ast.Call)
                   and isinstance(n.func, ast.Name) and n.func.id == "_tap_int"
                   and isinstance(n.args[0], ast.BinOp) and isinstance(n.args[0].op, ast.Mult))
        mutated = replace_node(tap, ast.get_source_segment(source, tap.args[0]))
        message = "unobserved scalar site"
    with pytest.raises(AssertionError, match=message):
        assert_source(name, mutated.encode(), tables, reference)


def test_te18_test_delta_checker_rejects_changed_math_and_changed_historical_hash():
    for name, original, changed in (
        ("tests/test_branch.py", '"exactfrac._telemetry"', '"exactfrac.unapproved"'),
        ("tests/test_branch_accelerated.py", "_COMPATIBILITY_SHA256", "_REFRESHED_SHA256"),
    ):
        source = (ROOT / name).read_bytes()
        assert_test_adaptation(name, source)
        assert original.encode() in source
        with pytest.raises(AssertionError):
            assert_test_adaptation(name, source.replace(original.encode(), changed.encode(), 1))


def test_te19_leaf_import_isolation_and_no_runtime_source_tools():
    script = r'''
import importlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
module = importlib.import_module('exactfrac._telemetry')
project = {n: str(pathlib.Path(m.__file__).resolve()) for n,m in sys.modules.copy().items()
           if n == 'exactfrac' or n.startswith('exactfrac.') or n.startswith('exactfrac_verify')}
assert set(project) == {'exactfrac', 'exactfrac._telemetry'}
assert project['exactfrac._telemetry'] == str(root/'exactfrac/_telemetry.py')
print(json.dumps(project, sort_keys=True))
'''
    run = subprocess.run([sys.executable, "-I", "-B", "-c", script, str(ROOT)],
                         cwd=ROOT, capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stdout + run.stderr
    source = Path(primitive.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source, feature_version=(3, 11))
    allowed = {"__future__", "contextvars", "contextlib", "dataclasses", "typing"}
    prohibited = {"open", "eval", "exec", "compile", "__import__", "settrace", "setprofile",
                  "perf_counter", "time", "monotonic", "inspect", "dis", "pickle"}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert node.level == 0 and node.module in allowed
        if isinstance(node, ast.Import):
            assert all(a.name in allowed for a in node.names)
        if isinstance(node, ast.Call):
            name = (
                node.func.id if isinstance(node.func, ast.Name)
                else getattr(node.func, "attr", None)
            )
            assert name not in prohibited
    for name in PRIMITIVES:
        assert callable(getattr(primitive, name))


def test_te20_metadata_is_supplied_not_discovered(monkeypatch):
    stats = _synthetic_stats()
    before = dataclasses.asdict(stats)
    samples = (telemetry.RunMetadata(None, "p", "q", None, "c", "0" * 64),
               telemetry.RunMetadata(0.0, "different", "platform", "cpu", "v2", "f" * 64))
    with monkeypatch.context() as patch:
        def forbidden(*_args, **_kwargs):
            raise AssertionError("record constructor tried environmental discovery")
        patch.setattr(subprocess, "run", forbidden)
        patch.setattr(Path, "read_bytes", forbidden)
        patch.setattr(Path, "read_text", forbidden)
        for sample in samples:
            rebuilt = telemetry.RunMetadata(*(getattr(sample, f) for f in FIELDS["RunMetadata"]))
            record = telemetry.RunRecord(stats, rebuilt)
            assert record.algorithm is stats and record.metadata is rebuilt
    assert dataclasses.asdict(stats) == before
    assert samples[0] != samples[1]


def test_te10_te21_te22_manifest_registry_and_no_new_math():
    assert len(INPUTS) == 389 and len(COVERS) == 1556
    for source, count, fingerprint, _ in TABLES["U16_REGISTRY"]:
        rows = U15[source] if source == "U15_INPUTS" else TABLES[source]
        assert (len(rows), row_digest(rows)) == (count, fingerprint)
    assert len(TABLES["U16_SCALAR_SITES"]) == 366
    assert len(TABLES["U16_ITERATOR_SITES"]) == 27
    assert len(TABLES["U16_EVENTS"]) == 26
    assert len(TABLES["U16_MUTATIONS"]) == 30
    assert {r[0] for r in TABLES["U16_COVERAGE"]} == {"TE" + str(i) for i in range(1, 24)}
    source = Path(telemetry.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source, feature_version=(3, 11))
    forbidden = {"solve_branch_standard", "solve_branch_accelerated", "exact_branch_min",
                 "enumerate_atomic_families", "minimum_cut", "minimum_parity_cut",
                 "settrace", "setprofile", "eval", "exec", "compile", "__import__",
                 "perf_counter", "monotonic", "time", "getrusage", "open"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = (
                node.func.id if isinstance(node.func, ast.Name)
                else getattr(node.func, "attr", None)
            )
            assert name not in forbidden
        assert not isinstance(node, (ast.AsyncFunctionDef, ast.Await))
    # Every mutable mathematical change still has to pass exact reference erasure.
    assert canonical(ast.parse(legacy_bytes("exactfrac/branch.py"))) == canonical(
        ast.parse((ROOT / "exactfrac/branch.py").read_bytes())
    )


@pytest.mark.parametrize(
    "row", TABLES["U16_ARITHMETIC"], ids=[r[0] for r in TABLES["U16_ARITHMETIC"]]
)
def test_te11_all_literal_arithmetic_streams_against_leaf(row, monkeypatch):
    key, expression, environment, expected, sequence, peak, _ = row
    values = dict(environment)
    tree = ast.parse(expression, mode="eval")
    observed = []

    def walk(node):
        if isinstance(node, ast.Name):
            value = values[node.id]
        elif isinstance(node, ast.Constant):
            value = node.value
        elif isinstance(node, ast.UnaryOp):
            assert isinstance(node.op, ast.USub)
            value = -walk(node.operand)
        else:
            assert isinstance(node, ast.BinOp)
            left, right = walk(node.left), walk(node.right)
            if isinstance(node.op, ast.Add):
                value = left + right
            elif isinstance(node.op, ast.Sub):
                value = left - right
            elif isinstance(node.op, ast.Mult):
                value = left * right
            else:
                assert isinstance(node.op, ast.LShift)
                value = left << right
        observed.append(value)
        assert primitive._tap_int(value) is value
        return value

    def action():
        assert walk(tree.body) == expected, key

    _, stats = _probe(monkeypatch, action)
    assert observed == list(sequence)
    assert stats.nonbranch.peak_integer_bits == peak


@pytest.mark.parametrize("row", TABLES["U16_ABSTRACT_COUNTERS"],
                         ids=[r[0] + "-" + r[1] for r in TABLES["U16_ABSTRACT_COUNTERS"]])
def test_te04_te05_abstract_scalar_streams_drive_actual_mapper(row, monkeypatch):
    key, route, first12, expected_root = row
    instance = _named("EQUALITY")
    context = oracle.BranchOracleContext(instance)
    traces = [r for r in TABLES["U16_ABSTRACT_TRACES"] if r[:2] == [key, route]]
    replies = []
    native_rows = []
    prepared = [r[1][12] for r in TABLES["U16_AGGREGATION"][:4]]
    output = global_solver.solve(instance, route)[0]

    def scripted_query(ctx, j, parameter):
        assert ctx is context
        index = len([r for r in replies if r[0] == j])
        record = traces[index]
        assert tuple(parameter) == tuple(record[4])
        reply = record[5]
        result = None if reply is None else oracle.BranchOracleResult(*reply)
        replies.append((j, index))
        return result, (oracle.BranchOracleStats(prepared[j], 0, 0, 0, 0, 0, 0) if reply is None
                        else oracle.BranchOracleStats(prepared[j], prepared[j], prepared[j],
                                                      3 * prepared[j], 0, 0, 0))

    def scripted_solve(i, choice):
        assert i is instance and choice == route
        primitive._record_prepared_sizes(*prepared)
        for j in range(4):
            with primitive._branch_scope(j):
                selected = (
                    branch.solve_branch_standard if route == "Standard"
                    else branch.solve_branch_accelerated
                )
                result, native = selected(context, j)
                native_rows.append(native)
                if result is not None:
                    primitive._tap_pair(result.root)
        return output, global_solver.SolveStats(route, tuple(native_rows), "Baseline")

    with monkeypatch.context() as patch:
        patch.setattr(branch, "exact_branch_min", scripted_query)
        _replace_entry(patch, scripted_solve)
        result, stats = telemetry.solve_with_telemetry(instance, route)
    assert result is output
    assert len(replies) == 4 * len(traces)
    assert len(stats.branches) == 4
    for j, record in enumerate(stats.branches):
        assert record.branch == j
        assert _tuple(record.work)[:12] == tuple(first12)
        assert record.feasible is (expected_root is not None)
        assert stats.native.branch_stats[j] is native_rows[j]
        assert record.work.atomic_families_enumerated == prepared[j]
        assert record.work.atomic_families_examined == native_rows[j].oracle_calls * prepared[j]
        assert record.work.flow_peak_bits == int(expected_root is not None)
    # Deliberately scripted domains are not added to the real-input census.


def test_te03_te06_branch_ownership_and_preparation_observation(monkeypatch):
    instance = _named("DOUBLE")
    for route in ROUTES:
        before = telemetry.solve_with_telemetry(instance, route)
        method = "solve_branch_standard" if route == "Standard" else "solve_branch_accelerated"
        original = getattr(global_solver, method)
        preparation = families.enumerate_atomic_families
        calls = []
        prepare_calls = []

        def prepare(*args, _calls=prepare_calls, _original=preparation):
            result = _original(*args)
            _calls.append(result)
            return result

        def with_branch_marker(ctx, j, _original=original, _calls=calls):
            marker = 1 << (1024 + j)
            primitive._observe_ints(marker)
            _calls.append(j)
            return _original(ctx, j)

        with monkeypatch.context() as patch:
            patch.setattr(global_solver, method, with_branch_marker)
            # Observe the actual preexisting imported preparation binding.
            patch.setattr(oracle, "enumerate_atomic_families", prepare)
            result, stats = telemetry.solve_with_telemetry(instance, route)
        assert calls == [0, 1, 2, 3] and len(prepare_calls) == 1
        assert result == before[0] and stats.native == before[1].native
        assert stats.nonbranch == before[1].nonbranch
        assert [b.work.peak_integer_bits for b in stats.branches] == [1025, 1026, 1027, 1028]
        assert [b.work.atomic_families_enumerated for b in stats.branches] == list(
            map(len, prepare_calls[0])
        )


@pytest.mark.parametrize("route", ROUTES)
def test_te03_baseline_h2_and_zero_h0_are_really_measured(route, monkeypatch):
    for target, name, field in (("baseline", "DOUBLE", "nonbranch"),
                                ("H2", "DOUBLE", "nonbranch"),
                                ("zero-H0", "ZERO", "branch2")):
        instance = _named(name)
        expected = global_solver.solve(instance, route)
        original = global_solver._baseline if target == "baseline" else (
            global_solver._first_copies if target == "H2" else global_solver._endpoint
        )
        invoked = []

        def marked(*args, _original=original, _invoked=invoked, _target=target):
            answer = _original(*args)
            use = (_target == "baseline" or (_target == "H2" and args[2] == 2)
                   or (_target == "zero-H0" and args[1] == 2 and answer[0].N == 0))
            if use:
                primitive._observe_ints(1 << 768)
                _invoked.append(True)
            return answer

        attribute = {"baseline": "_baseline", "H2": "_first_copies", "zero-H0": "_endpoint"}[target]
        with monkeypatch.context() as patch:
            patch.setattr(global_solver, attribute, marked)
            result, stats = telemetry.solve_with_telemetry(instance, route)
        assert invoked == [True]
        assert (result, stats.native) == expected
        selected = stats.nonbranch if field == "nonbranch" else stats.branches[2].work
        assert selected.peak_integer_bits == stats.total.peak_integer_bits == 769
        others = [stats.nonbranch, *(b.work for b in stats.branches)]
        assert all(w.peak_integer_bits < 769 for w in others if w is not selected)


def test_te15_disabled_taps_and_record_bookkeeping_do_not_enter_math_peak(monkeypatch):
    integer = (1 << 521) - 1
    pair = (integer, 17)
    assert primitive._tap_int(integer) is integer
    assert primitive._tap_pair(pair) is pair
    assert primitive._tap_numerator(integer, pair[1]) is integer
    primitive._observe_ints(integer)
    primitive._observe_pair_values(*pair)
    # Record-only constructor arithmetic is excluded even inside a measured interval.
    fields = list(dict(TABLES["U16_AGGREGATION"])["total"])
    fields[:20] = [value * (1 << 2048) for value in fields[:20]]
    before = telemetry.solve_with_telemetry(_named("Q1"), "Standard")

    def action():
        record = _work(fields)
        assert _tuple(record) == tuple(fields)

    after = _probe(monkeypatch, action)
    assert after == before


@pytest.mark.parametrize("fault", ("bare-none", "short-tuple", "wrong-result", "wrong-native"))
def test_te16_normally_returned_invalid_dependency_records_fail_closed(fault, monkeypatch):
    instance = _named("DOUBLE")
    baseline = telemetry.solve_with_telemetry(instance, "Standard")
    result, native = global_solver.solve(instance, "Standard")
    replies = {"bare-none": None, "short-tuple": (result,),
               "wrong-result": (None, native), "wrong-native": (result, None)}
    calls = []

    def malformed(*_args):
        calls.append(True)
        return replies[fault]

    with monkeypatch.context() as patch:
        _replace_entry(patch, malformed)
        with pytest.raises(RuntimeError) as raised:
            telemetry.solve_with_telemetry(instance, "Standard")
        assert type(raised.value) is RuntimeError
    assert calls == [True]
    assert telemetry.solve_with_telemetry(instance, "Standard") == baseline


def test_te07_te09_zero_terminal_performs_no_ordinary_cut(monkeypatch):
    # Concrete member of the catalogue's generic zero-terminal scenario.
    problem = parity_cut.ParityCutProblem(1, (3, 4), (), 0)
    answers = []

    def forbidden(*_args, **_kwargs):
        raise AssertionError("zero-terminal parity query invoked ordinary flow")

    def action():
        answers.append(parity_cut.minimum_parity_cut(problem))

    with monkeypatch.context() as patch:
        patch.setattr(parity_cut, "minimum_cut", forbidden)
        _, stats = _probe(patch, action)
    assert answers == [(None, parity_cut.ParityCutStats(0, 0, 0, 0))]
    assert stats.total.ordinary_min_cut_calls == stats.total.max_flow_calls == 0
    assert stats.total.flow_peak_generated_value == stats.total.flow_peak_bits == 0


# Authorized consuming correction: all discovery starts from source and the stated rule.
def _inventory_expression(text):
    node = ast.parse(text).body[0]
    return canonical(node.value if isinstance(node, ast.Expr) else node)


@pytest.mark.parametrize(
    "row", TABLES["U16MC_RULE_FIXTURES"], ids=[r[0] for r in TABLES["U16MC_RULE_FIXTURES"]],
)
def test_te10_manifest_rule_manual_syntax_fixtures(row):
    _, source, scalars, iterators = row
    found = inventory_from_sources({"probe": source})
    actual = Counter((r[1], _inventory_expression(r[8])) for r in found["scalars"])
    expected = Counter((owner, _inventory_expression(text)) for owner, text in scalars)
    assert actual == expected
    assert Counter((r[1], r[4], r[5]) for r in found["iterators"]) == Counter(map(tuple, iterators))


def test_te10_corrected_inventory_is_complete_from_authenticated_source():
    sources = inventory_sources(load_reference(), TABLES)
    assert assert_inventory_complete(sources, TABLES) == {
        "functions": 102, "scalar_sites": 366, "iterator_sites": 27,
        "enumeration_uses_manifest": False,
    }
    assert [r[0] for r in TABLES["U16_SCALAR_SITES"][:333]] == [
        f"S{i:04d}" for i in range(1, 334)
    ]
    assert TABLES["U16_SCALAR_SITES"][333:] == TABLES["U16MC_SCALAR_ADDITIONS"]
    assert TABLES["U16_ITERATOR_SITES"][25:] == TABLES["U16MC_ITERATOR_ADDITIONS"]
    assert sum(r[10] in {"TAP_SCALAR", "TAP_SUM_FINAL"} for r in TABLES["U16_SCALAR_SITES"]) == 237
    assert sum(r[10] == "OBSERVE_POST_STORE" for r in TABLES["U16_SCALAR_SITES"]) == 25


@pytest.mark.parametrize("site", [r[0] for r in TABLES["U16MC_SCALAR_ADDITIONS"]])
def test_te10_completeness_rejects_each_added_scalar_omission(site):
    mutated = {**TABLES, "U16_SCALAR_SITES": [
        r for r in TABLES["U16_SCALAR_SITES"] if r[0] != site
    ]}
    with pytest.raises(AssertionError, match="scalar coverage mismatch"):
        assert_inventory_complete(inventory_sources(load_reference(), TABLES), mutated)


@pytest.mark.parametrize("position", (25, 26))
def test_te10_completeness_rejects_each_added_iterator_omission(position):
    mutated = {**TABLES, "U16_ITERATOR_SITES": [
        row for i, row in enumerate(TABLES["U16_ITERATOR_SITES"]) if i != position
    ]}
    with pytest.raises(AssertionError, match="iterator coverage mismatch"):
        assert_inventory_complete(inventory_sources(load_reference(), TABLES), mutated)


@pytest.mark.parametrize("fault", (
    "original-incomplete", "same-count-path", "same-count-ast", "duplicate-occurrence",
    "duplicate-id", "omitted-function", "same-count-iterator", "recomputed-fingerprint",
))
def test_te10_completeness_rejects_self_consistent_but_incomplete_tables(fault):
    mutated = {**TABLES, **{
        name: [list(row) for row in TABLES[name]]
        for name in ("U16_SCALAR_SITES", "U16_FUNCTIONS", "U16_ITERATOR_SITES", "U16_FINGERPRINTS")
    }}
    message = "scalar coverage mismatch"
    if fault == "original-incomplete":
        mutated["U16_SCALAR_SITES"] = mutated["U16_SCALAR_SITES"][:333]
        mutated["U16_ITERATOR_SITES"] = mutated["U16_ITERATOR_SITES"][:25]
    elif fault == "same-count-path":
        mutated["U16_SCALAR_SITES"][-1][7] += ".invented"
    elif fault == "same-count-ast":
        mutated["U16_SCALAR_SITES"][-1][8] = "0" * 64
    elif fault == "duplicate-occurrence":
        mutated["U16_SCALAR_SITES"][-1] = ["S9999", *mutated["U16_SCALAR_SITES"][-2][1:]]
        message = "duplicate scalar identity"
    elif fault == "duplicate-id":
        mutated["U16_SCALAR_SITES"][-1][0] = mutated["U16_SCALAR_SITES"][0][0]
        message = "duplicate scalar site ID"
    elif fault == "omitted-function":
        mutated["U16_FUNCTIONS"].pop(0)
        message = "function coverage mismatch"
    elif fault == "same-count-iterator":
        mutated["U16_ITERATOR_SITES"][-1][5] = "range(999)"
        message = "iterator coverage mismatch"
    else:
        mutated["U16_SCALAR_SITES"].pop()
        for row in mutated["U16_FINGERPRINTS"]:
            if row[0] == "U16_SCALAR_SITES":
                row[1:] = [len(mutated[row[0]]), row_digest(mutated[row[0]])]
    with pytest.raises(AssertionError, match=message):
        assert_inventory_complete(inventory_sources(load_reference(), TABLES), mutated)


def test_te10_rule_fixture_detects_untyped_args_exclusion(monkeypatch):
    # Reintroduce only the original traversal defect in a test-local function binding.
    namespace = inventory_from_sources.__globals__
    correct = namespace["_inventory_inside_body"]

    def wrong(node, ancestors):
        return correct(node, ancestors) and not any(field == "args" for _, field in ancestors)

    row = next(r for r in TABLES["U16MC_RULE_FIXTURES"] if r[0] == "signature-vs-call")
    with monkeypatch.context() as patch:
        patch.setitem(namespace, "_inventory_inside_body", wrong)
        with pytest.raises(AssertionError):
            test_te10_manifest_rule_manual_syntax_fixtures(row)
    test_te10_manifest_rule_manual_syntax_fixtures(row)


# Narrowly authorized alternative for the two branch_coefficients generator bounds.
def _bound_observation_variant(form):
    """Construct parsed-only instrumented source; never execute reference strings."""
    module = "sign_routing"
    original = legacy_bytes("exactfrac/sign_routing.py").decode()
    tree = ast.parse(original)
    owned = functions(tree)
    targets = {
        id(at_path(owned[r[2]], r[7])): r[10]
        for r in TABLES["U16_SCALAR_SITES"] if r[1] == module
    }
    # Locate the two specific generators before instrumentation changes node nesting.
    low_path = "body[7].body[1].value.args[0].generators[0]"
    high_path = "body[7].orelse[0].value.args[0].generators[0]"
    coefficient = owned["branch_coefficients"]
    selection = coefficient.body[7]
    low = at_path(coefficient, low_path)
    high = at_path(coefficient, high_path)
    ranges = (low.iter, high.iter)
    enumerate_loop = owned["build_sign_routed_network"].body[9]

    class Observe(ast.NodeTransformer):
        def generic_visit(self, node):
            action = targets.get(id(node))
            super().generic_visit(node)
            if action in {"TAP_SCALAR", "TAP_SUM_FINAL"}:
                return ast.Call(ast.Name("_tap_int", ast.Load()), [node], [])
            if action == "OBSERVE_POST_STORE":
                value = ast.parse(ast.unparse(node.target), mode="eval").body
                event = ast.Expr(ast.Call(ast.Name("_observe_ints", ast.Load()), [value], []))
                return [node, event]
            return node

    Observe().visit(tree)
    for call in ranges:
        if form in {"inline", "both"} or (
            form == "low-inline-and-statement" and call is low.iter
        ) or (form == "high-inline-and-statement" and call is high.iter):
            call.args[0] = ast.Call(ast.Name("_tap_int", ast.Load()), [call.args[0]], [])
    enumerate_loop.body.insert(0, ast.parse("_observe_ints(vertex)").body[0])
    position = coefficient.body.index(selection)
    statement_forms = {
        "statement", "both", "low-inline-and-statement", "high-inline-and-statement",
        "different-operand", "extra-evaluation", "reassignment-between", "reassignment-low",
        "reassignment-high", "delete-high", "conditional-before", "different-scope",
    }
    if form in statement_forms:
        operand = "denominator" if form == "different-operand" else "instance.n"
        if form == "extra-evaluation":
            operand = "instance.n + 0"
        event = ast.parse(f"_observe_ints({operand})").body[0]
        if form == "conditional-before":
            event = ast.If(ast.parse("branch == 0", mode="eval").body, [event], [])
        if form == "different-scope":
            event = ast.With([
                ast.withitem(ast.parse("_branch_scope(branch)", mode="eval").body)
            ], [event])
        coefficient.body.insert(position, event)
        if form == "reassignment-between":
            coefficient.body.insert(position + 1, ast.parse("instance = instance").body[0])
        if form == "reassignment-low":
            selection.body.insert(0, ast.parse("instance = instance").body[0])
        if form in {"reassignment-high", "delete-high"}:
            code = "instance.n = instance.n" if form == "reassignment-high" else "del instance.n"
            selection.orelse.insert(0, ast.parse(code).body[0])
    elif form == "after-generator":
        for arm in (selection.body, selection.orelse):
            gamma_position = next(
                i for i, node in enumerate(arm)
                if isinstance(node, ast.Assign) and ast.unparse(node.targets[0]) == "gamma"
            )
            arm.insert(gamma_position + 1, ast.parse("_observe_ints(instance.n)").body[0])
    elif form in {"opposite-low", "opposite-high"}:
        arm = selection.orelse if form == "opposite-low" else selection.body
        arm.insert(0, ast.parse("_observe_ints(instance.n)").body[0])
    elif form != "inline":
        raise AssertionError("unregistered bound-observation fixture")
    # Keep byte-frozen constructors/properties in the original module untouched.
    text = original
    for name in ("branch_coefficients", "build_sign_routed_network", "recover_objective"):
        old = functions(ast.parse(original))[name]
        old_text = ast.get_source_segment(original, old)
        new_text = ast.unparse(ast.fix_missing_locations(owned[name]))
        assert text.count(old_text) == 1
        text = text.replace(old_text, new_text, 1)
    imports = "from ._telemetry import _branch_scope, _observe_ints, _tap_int\n"
    return text.replace(
        "from .instance import Instance\n", imports + "from .instance import Instance\n",
    )


@pytest.mark.parametrize("form", (
    "inline", "statement", "both", "low-inline-and-statement", "high-inline-and-statement",
))
def test_te17_diter_exact_inline_and_preceding_statement_forms(form):
    source = _bound_observation_variant(form).encode()
    result = assert_source("exactfrac/sign_routing.py", source, TABLES, load_reference())
    assert result == {"direct_sites": 19, "post_stores": 1}
    assert len(TABLES["U16_FUNCTIONS"]) == 102
    assert len(TABLES["U16_SCALAR_SITES"]) == 366
    assert len(TABLES["U16_ITERATOR_SITES"]) == 27
    assert sum(r[10] in {"TAP_SCALAR", "TAP_SUM_FINAL"} for r in TABLES["U16_SCALAR_SITES"]) == 237
    assert sum(r[10] == "OBSERVE_POST_STORE" for r in TABLES["U16_SCALAR_SITES"]) == 25


@pytest.mark.parametrize("fault", (
    "after-generator", "opposite-low", "opposite-high", "different-operand",
    "reassignment-between", "reassignment-low", "reassignment-high", "delete-high",
    "conditional-before", "different-scope", "extra-evaluation",
))
def test_te17_diter_statement_rejects_wrong_placement_operand_scope_and_reassignment(fault):
    # A valid control must pass before any negative variant is credited.
    test_te17_diter_exact_inline_and_preceding_statement_forms("statement")
    source = _bound_observation_variant(fault)
    current = functions(ast.parse(source))
    _mark_coefficient_bound_statement("sign_routing", current)
    assert not any(
        getattr(node, "_u16_preceding_coefficient_bound", False)
        for node in ast.walk(current["branch_coefficients"])
    )
    with pytest.raises(AssertionError):
        assert_source("exactfrac/sign_routing.py", source.encode(), TABLES, load_reference())


@pytest.mark.parametrize("fault", ("module", "function", "iterator-path", "operand", "binder"))
def test_te17_diter_statement_cannot_discharge_another_registered_site(fault):
    # Check the bound/site guard independently of source conservation or table hashing.
    tree = ast.parse(legacy_bytes("exactfrac/sign_routing.py"))
    erased = functions(tree)
    erased["branch_coefficients"].body[7]._u16_preceding_coefficient_bound = True
    rows = [r for r in TABLES["U16_ITERATOR_SITES"]
            if r[0] == "sign_routing" and r[1] == "branch_coefficients"]
    assert len(rows) == 2
    for original in rows:
        row = list(original)
        stop = ast.parse("instance.n", mode="eval").body
        assert _coefficient_statement_covers("sign_routing", row, erased, stop)
        module = "sign_routing"
        if fault == "module":
            module = row[0] = "flow"
        elif fault == "function":
            row[1] = "build_sign_routed_network"
        elif fault == "iterator-path":
            row[3] = "body[9]"
        elif fault == "operand":
            stop = ast.parse("denominator", mode="eval").body
        else:
            row[4] = "other_vertex"
        assert not _coefficient_statement_covers(module, row, erased, stop)
