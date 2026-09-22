"""Unit 21 EP1--EP20: independent consumer, scripted schedule, bounded real calls.

Expected data come from the committed Phase C fixture blocks. The full scripted
schedule is not an experiment campaign. Only three preregistered tiny instances
use real telemetry in the bounded integration test. No test retimes the owned
historical campaign, and no source/result directory is globally hash-pinned.
"""

from __future__ import annotations

import ast
import base64
import builtins
import copy
import dataclasses
import gc
import hashlib
import importlib
import inspect
import io
import json
import math
import os
import platform
import re
import runpy
import stat
import subprocess
import sys
import time
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from typing import get_type_hints

import pytest

import exactfrac.experiments as experiments

_ROOT = Path(__file__).resolve().parents[1]
_ROUTES = ("Standard", "Accelerated")
_MISSING = object()

# Independent immutable fixture identities, not a whole-catalogue or repo pin.
_FIXTURE_IDENTITIES = {
    "CENSUS.json": {
        "bytes": 1057,
        "sha256": "e2f7cceaff71ee18d0b878f0dda2a49f9a5421220ff9edade7acbbd29dbadc16"
    },
    "FAULT_DECLARATIONS.json": {
        "bytes": 16457,
        "sha256": "79943f129d0896821935fc0523481ca0bea6bd4b262a25e01b9b5f715e7779ec"
    },
    "FIELD_REGISTRY.json": {
        "bytes": 3472,
        "sha256": "71e877b9812070cf1ec96b7207411f5c8ffffa84d8829037a433cb57b5d47932"
    },
    "INPUT_EXPECTATIONS.json": {
        "bytes": 350371,
        "sha256": "d90b810d8ba587a1c95495cb231bb5be22e197e958083ec9e7449114ae0cd3f2"
    },
    "SCHEDULE.tsv": {
        "bytes": 296159,
        "sha256": "4d40c71d688455ce86fdcf2fecd085b7143330aa80875f57da6a20ff1c3b1b59"
    },
    "SOURCE_FINGERPRINT.bin": {
        "bytes": 1951,
        "sha256": "2d5063b59fcebb0f413d642f4897faed4aef2db9a63470c19e395d3d2dc3aa05"
    },
    "SOURCE_FIXTURE.json": {
        "bytes": 3167,
        "sha256": "852ed4cf6fa9498d5e0976ebdb0aaaa2d53f3a9ec746023a24275681d8cd2db7"
    },
    "SYNTHETIC_ALGORITHMS.json": {
        "bytes": 22900,
        "sha256": "b8bbcbbeeb159df276d3f353fb86c49bdf62c45c466cdb35fca248d47df98d19"
    },
    "SYNTHETIC_CALL_SCRIPT.json": {
        "bytes": 7375,
        "sha256": "ad900eb250ce8be19722fb287b079479fc61bc780fc36710d40b35bfea6e2e08"
    },
    "SYNTHETIC_ESCAPING.json": {
        "bytes": 100,
        "sha256": "5417aa8ff2a761367db513804a6f7fc6e0c91c0e9c36478ca600c46f38473f51"
    },
    "SYNTHETIC_GIANT_ROW.jsonl": {
        "bytes": 19276,
        "sha256": "eacddea72459b6244c84cfcebe4ee67534646e36e3239983cb82c2043248c229"
    },
    "SYNTHETIC_RUNS.jsonl": {
        "bytes": 83409,
        "sha256": "7a99909015625f61d009a82ba9e19cb9b39eb592b57a4e9dd47e3d890de2288b"
    },
    "SYNTHETIC_RUN_INFO.json": {
        "bytes": 3483,
        "sha256": "52a6b2e38f74e2169bb8378f7668b9c558c52d710427f728c2f09aede0ced888"
    },
    "SYNTHETIC_WARMUPS.jsonl": {
        "bytes": 27795,
        "sha256": "98153f3c795f25e799e67891532aacd347b47acf71f1164e60401b24218fb8b9"
    },
    "SYNTHETIC_branches.csv": {
        "bytes": 2099,
        "sha256": "fb6fd0965fb8ce71043c1c56a76e053066c14b717dd65aa661fd2a64ff1f6966"
    },
    "SYNTHETIC_comparison.csv": {
        "bytes": 345,
        "sha256": "91f33e4f2d3c20f89d04b7c1fd5f4d1f2824228aaa67ca0beecd380b2447665a"
    },
    "SYNTHETIC_summary.csv": {
        "bytes": 1367,
        "sha256": "be1630b93b7183fab134e4cf85b85fadde3e32bbfa53b5e0a0decce2549b12a8"
    },
    "TIMING_TRAPS.json": {
        "bytes": 754,
        "sha256": "bb7bc9932a635c3d5b1fb5ecc39457525e62723bfda37e467bb48e18a56aecff"
    },
    "WIRE_SCHEMAS.json": {
        "bytes": 4208,
        "sha256": "fbffd151e1020ebbb6a8db7b48bfceaac861e0648bf0c06889303736dcb220ef"
    },
    "certificates/edge-q01-f01-01.Accelerated.json": {
        "bytes": 62,
        "sha256": "96ecf951be97360f4e27c6a3ce9d959936807f52f0faf2d9156a77cac0d66fde"
    },
    "certificates/edge-q01-f01-01.Standard.json": {
        "bytes": 62,
        "sha256": "96ecf951be97360f4e27c6a3ce9d959936807f52f0faf2d9156a77cac0d66fde"
    },
    "certificates/struct-cycle-n04-b00001-fdegree.Accelerated.json": {
        "bytes": 85,
        "sha256": "d44a7c4a6290567d67bb1101c91bf08a8eb5d76bf7a570e3fc375e7a782d0077"
    },
    "certificates/struct-cycle-n04-b00001-fdegree.Standard.json": {
        "bytes": 83,
        "sha256": "37743820166bb85c058502f2c212d6f7a8231d6202e46325d982ca87840fdf87"
    },
    "certificates/tri-q1-1-1-f1-1-1.Accelerated.json": {
        "bytes": 82,
        "sha256": "2eb8c8cda039c0b4335d7f49a1e1722b2320253f30560647e697dd42393687a9"
    },
    "certificates/tri-q1-1-1-f1-1-1.Standard.json": {
        "bytes": 82,
        "sha256": "2eb8c8cda039c0b4335d7f49a1e1722b2320253f30560647e697dd42393687a9"
    },
    "inputs/edge-q01-f01-01.json": {
        "bytes": 68,
        "sha256": "389e145ac421044db6be19237d20b2112c832610c52c4d0be523fef2ab526589"
    },
    "inputs/struct-cycle-n04-b00001-fdegree.json": {
        "bytes": 96,
        "sha256": "6aa50220c883136c833d8d737eef577bd2dc57e801dee88b1f5076e313e90622"
    },
    "inputs/tri-q1-1-1-f1-1-1.json": {
        "bytes": 86,
        "sha256": "345ee6d9d1471d32bbb4c66a6ab8725618c309f6af0372c29cee3a3ccd11f70e"
    }
}


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _require(ok, guard):
    if not ok:
        raise AssertionError(guard)


def _decimal(token):
    _require(re.fullmatch(r"0|-?[1-9][0-9]*", token) is not None, "integer-token")
    negative = token.startswith("-")
    digits = token[1:] if negative else token
    value = 0
    for start in range(0, len(digits), 9):
        chunk = digits[start:start + 9]
        value = value * 10 ** len(chunk) + int(chunk)
    return -value if negative else value


def _digits(value):
    if value < 0:
        return "-" + _digits(-value)
    parts = []
    while value:
        value, chunk = divmod(value, 1_000_000_000)
        parts.append(chunk)
    return "0" if not parts else str(parts[-1]) + "".join(
        f"{part:09d}" for part in reversed(parts[:-1])
    )


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate-decoded-key")
        result[key] = value
    return result


def _constant(_):
    raise AssertionError("nonfinite-token")


def _decode(raw):
    return json.loads(raw, parse_int=_decimal, object_pairs_hook=_pairs,
                      parse_constant=_constant)


def _wire(value):
    """Independent test codec, including ordinary enormous integer tokens."""
    if value is None:
        return b"null"
    if type(value) is bool:
        return b"true" if value else b"false"
    if type(value) is int:
        return _digits(value).encode("ascii")
    if type(value) is float:
        _require(math.isfinite(value), "finite-float")
        return json.dumps(value, allow_nan=False).encode("ascii")
    if type(value) is str:
        return json.dumps(value, ensure_ascii=True).encode("ascii")
    if type(value) in (list, tuple):
        return b"[" + b",".join(_wire(item) for item in value) + b"]"
    _require(type(value) is dict, "wire-object-type")
    return b"{" + b",".join(
        _wire(key) + b":" + _wire(value[key]) for key in sorted(value)
    ) + b"}"


def _json_bytes(value):
    return _wire(value) + b"\n"


def _bank():
    raw = (_ROOT / "docs/ORACLE_CATALOG.md").read_bytes()
    pattern = (
        rb"<!-- U21-FIXTURE ([^\n ]+) encoding=(raw|base64) "
        rb"bytes=([0-9]+) sha256=([0-9a-f]{64}) -->\n```[^\n]+\n(.*?)\n```\n"
    )
    bank = {}
    for match in re.finditer(pattern, raw, re.S):
        name, encoding, length, digest, data = match.groups()
        name = name.decode("ascii")
        if name not in _FIXTURE_IDENTITIES:
            continue
        _require(name not in bank, "duplicate-fixture")
        value = base64.b64decode(data, validate=True) if encoding == b"base64" else data + b"\n"
        identity = {"bytes": len(value), "sha256": _sha(value)}
        _require(identity == _FIXTURE_IDENTITIES[name], "independent-fixture-identity")
        _require((len(value), _sha(value)) == (int(length), digest.decode()), "block-header")
        bank[name] = value
    _require(set(bank) == set(_FIXTURE_IDENTITIES), "required-fixtures")
    return bank


def _schedule(bank):
    rows = []
    for line in bank["SCHEDULE.tsv"].decode("ascii").splitlines()[1:]:
        sequence, index, recipe, round_id, route, phase, repeat = line.split("\t")
        rows.append({"sequence": int(sequence), "recipe_index": int(index),
                     "recipe": recipe, "round": int(round_id), "solver": route,
                     "phase": phase, "repeat": int(repeat)})
    return rows


def _expression(text, bits):
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.Name) and node.id == "T" and bits >= 2:
            return 1 << (bits - 2)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return a + b
            if isinstance(node.op, ast.Sub):
                return a - b
            if isinstance(node.op, ast.Mult):
                return a * b
        raise AssertionError("unregistered-expression")
    return visit(ast.parse(text, mode="eval").body)


def _independent_certificate(obj):
    """Finite shore/endpoint reference; never invokes a production solver."""
    best = None
    for mask in range(1, 1 << obj["n"]):
        capacity = sum(value for v, value in enumerate(obj["f"]) if mask & (1 << v))
        internal = 0
        boundary = []
        for j, (u, v, q) in enumerate(obj["edges"]):
            left, right = bool(mask & (1 << u)), bool(mask & (1 << v))
            if left and right:
                internal += q
            if left != right:
                boundary.append((j, q))
        bound = sum(q for _, q in boundary)
        low = 2 if capacity == 1 else (1 if capacity % 2 == 0 else 0)
        high = bound if (capacity + bound) % 2 else bound - 1
        for selected in (low, high):
            if not 0 <= selected <= bound or capacity + selected < 3:
                continue
            if (capacity + selected) % 2 == 0:
                continue
            numerator, denominator = 2 * (internal + selected), capacity + selected - 1
            if best is not None and numerator * best["D"] <= best["N"] * denominator:
                continue
            remaining, counts = selected, []
            for j, q in boundary:
                amount = min(remaining, q)
                remaining -= amount
                if amount:
                    counts.append([j, amount])
            _require(remaining == 0, "independent-boundary-lift")
            best = {"format": "exactfrac-certificate/1", "empty": False,
                    "N": numerator, "D": denominator,
                    "U": [v for v in range(obj["n"]) if mask & (1 << v)], "y": counts}
    return best or {"format": "exactfrac-certificate/1", "empty": True, "N": 0, "D": 1}


def _project(name):
    return name.split(".")[0] in ("exactfrac", "exactfrac_verify")


def _algorithm(modules, row):
    telemetry = modules["telemetry"]
    native = row["native"]
    cls = getattr(modules["branch"], native["branch_solver"] + "BranchStats")
    branches = tuple(cls(**{**item, "oracle_stats": modules["oracle"].BranchOracleStats(
        **item["oracle_stats"])}) for item in native["branch_stats"])
    return telemetry.AlgorithmStats(
        modules["solve"].SolveStats(
            native["branch_solver"], branches, native["attaining_candidate"]),
        telemetry.WorkStats(**row["total"]), telemetry.WorkStats(**row["nonbranch"]),
        tuple(telemetry.BranchTelemetry(item["branch"], item["feasible"],
                                       telemetry.WorkStats(**item["work"]))
              for item in row["branches"]),
        row["output_numerator_bits"], row["output_denominator_bits"],
    )


def _result(modules, obj, certificate):
    witness = None
    if not certificate["empty"]:
        counts = [0] * len(obj["edges"])
        for index, value in certificate["y"]:
            counts[index] = value
        witness = modules["witness"].Witness(
            sum(1 << v for v in certificate["U"]), tuple(counts)
        )
    return modules["solve"].SolveResult(
        modules["witness"].ExactValue(certificate["N"], certificate["D"]), witness
    )


def _snapshot(root):
    images = {}
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        _require(stat.S_ISDIR(mode) or (stat.S_ISREG(mode) and not mode & 0o111),
                 "snapshot-nonregular-or-executable")
        if stat.S_ISREG(mode):
            images[path.relative_to(root).as_posix()] = path.read_bytes()
    return images


class _Session:
    """Test-only dependency spies; public main is the sole runner entry."""

    def __init__(self, root, bank, modules, patches):
        self.root, self.bank, self.modules, self.patches = root, bank, modules, patches
        self.inputs = root / "instances"
        self.output = root / "results/unit21-v1"
        self.schedule = _schedule(bank)
        self.expectations = _decode(bank["INPUT_EXPECTATIONS.json"])
        self.expected = {row["recipe"]: row for row in self.expectations}
        self.selected = _decode(bank["SYNTHETIC_CALL_SCRIPT.json"])["selected_ids"]
        self.script = {row["sequence"]: row for row in _decode(
            bank["SYNTHETIC_CALL_SCRIPT.json"])["calls"]}
        self.templates = {(row["recipe"], row["solver"]): row["algorithm"]
                          for row in _decode(bank["SYNTHETIC_ALGORITHMS.json"])}
        self.calls, self.checks, self.events, self.record_objects = [], [], [], []
        self.certificates, self.returned, self.objects, self.solutions = {}, {}, {}, {}
        self.real_calls = 0
        self.allow_real = False
        self.real_ids = set()
        self.giant = False
        self.failure = None
        self.bad_return = None
        self.on_stage = None
        self.clock_open = False
        self.current = None
        self.discovered = Counter()
        self.corpus_access = Counter()
        self.original_solve = modules["telemetry"].solve_with_telemetry
        self.original_build = modules["certificate"].build_certificate
        self.original_serialize = modules["certificate"].serialize_certificate
        self.original_check = modules["check"].verify_certificate
        self.source_names = sorted(row["path"] for row in _decode(
            bank["SOURCE_FIXTURE.json"])["closed_entries"])
        self.source_names.extend(("exactfrac/experiments.py", "experiments/reproduce.py"))
        self.source_names.sort()
        self.source_images = {name: (root / name).read_bytes() for name in self.source_names}
        self.settings = (sys.get_int_max_str_digits(), sys.getrecursionlimit(), list(sys.path))
        self.initial_input_images = _snapshot(self.inputs)

    def hit(self, stage):
        if self.on_stage is not None:
            self.on_stage(stage, self)
        if self.failure is not None and self.failure[0] == stage:
            raise self.failure[1]
        if self.bad_return is not None and self.bad_return[0] == stage:
            return self.bad_return[1]
        return _MISSING

    def discover(self, name, value):
        self.discovered[name] += 1
        answer = self.hit(name)
        return value if answer is _MISSING else answer

    def _data(self, rid):
        if rid not in self.objects:
            self.objects[rid] = _decode(self.initial_input_images["unit20-v1/" + rid + ".json"])
        return self.objects[rid]

    def elapsed(self, row):
        if row["phase"] == "warmup":
            return None
        selected = self.script.get(row["sequence"])
        if selected is not None:
            return selected["elapsed_ns"]
        return (11, 0, 5)[row["repeat"]] + (2 if row["solver"] == "Accelerated" else 0)

    def clock(self):
        stage = "clock-end" if self.clock_open else "clock-start"
        injected = self.hit(stage)
        if injected is not _MISSING:
            return injected
        if self.clock_open:
            row = self.current
            self.clock_open = False
            self.events.append(("clock-end", row["sequence"]))
            return 1_000_000 + row["sequence"] * 1000 + self.elapsed(row)
        _require(len(self.calls) < len(self.schedule), "extra-clock")
        row = self.schedule[len(self.calls)]
        _require(row["phase"] == "measured", "warmup-was-clocked")
        self.clock_open = True
        self.events.append(("clock-start", row["sequence"]))
        return 1_000_000 + row["sequence"] * 1000

    def solve(self, instance, branch_solver):
        _require(len(self.calls) < len(self.schedule), "extra-solve")
        row = self.schedule[len(self.calls)]
        self.current = row
        _require(branch_solver == row["solver"], "observed-route-order")
        obj = self._data(row["recipe"])
        _require((instance.n, instance.edges, instance.f) == (
            obj["n"], tuple(map(tuple, obj["edges"])), tuple(obj["f"])), "scheduled-instance")
        _require(self.clock_open == (row["phase"] == "measured"), "solve-clock-boundary")
        self.events.append(("solve-enter", row["sequence"]))
        self.calls.append(dict(row))
        injected = self.hit("solve")
        if injected is not _MISSING:
            return injected
        rid, route = row["recipe"], row["solver"]
        if rid in self.real_ids:
            self.allow_real = True
            try:
                result, algorithm = self.original_solve(instance, route)
            finally:
                self.allow_real = False
            self.real_calls += 1
        else:
            key = (rid, route)
            if key not in self.solutions:
                cert_name = f"certificates/{rid}.{route}.json"
                cert = (_decode(self.bank[cert_name]) if cert_name in self.bank
                        else _independent_certificate(obj))
                result = _result(self.modules, obj, cert)
                template_key = key if key in self.templates else (
                    "struct-cycle-n04-b00001-fdegree", route)
                template = copy.deepcopy(self.templates[template_key])
                nb = template["nonbranch"]
                nb["peak_numerator_bits"] = max(
                    nb["peak_numerator_bits"], result.value.N.bit_length())
                nb["peak_denominator_bits"] = max(
                    nb["peak_denominator_bits"], result.value.D.bit_length())
                nb["peak_integer_bits"] = max(nb.values())
                schema = _decode(self.bank["WIRE_SCHEMAS.json"])
                for field in schema["peak_fields"]:
                    template["total"][field] = max(
                        nb[field], *(part["work"][field] for part in template["branches"])
                    ) if template["branches"] else nb[field]
                template["output_numerator_bits"] = max(1, result.value.N.bit_length())
                template["output_denominator_bits"] = max(1, result.value.D.bit_length())
                if self.giant and rid == self.selected[1] and route == "Accelerated":
                    template = (
                        _decode(self.bank["SYNTHETIC_GIANT_ROW.jsonl"])["record"]["algorithm"])
                algorithm = _algorithm(self.modules, template)
                self.solutions[key] = (result, algorithm)
            result, algorithm = self.solutions[key]
        self.returned[row["sequence"]] = (result, algorithm)
        self.events.append(("solve-return", row["sequence"]))
        changed = self.hit("solve-return")
        return (result, algorithm) if changed is _MISSING else changed

    def build(self, instance, result):
        _require(not self.clock_open, "certificate-inside-clock")
        self.events.append(("build", self.current["sequence"]))
        injected = self.hit("build")
        return self.original_build(instance, result) if injected is _MISSING else injected

    def serialize(self, instance, certificate):
        _require(not self.clock_open, "serialization-inside-clock")
        injected = self.hit("serialize")
        raw = self.original_serialize(instance, certificate) if injected is _MISSING else injected
        self.events.append(("serialize", self.current["sequence"]))
        if type(raw) is bytes:
            self.certificates[(self.current["recipe"], self.current["solver"])] = raw
        return raw

    def check(self, instance_bytes, certificate_bytes):
        _require(not self.clock_open, "checker-inside-clock")
        row = self.current
        expected = self.initial_input_images["unit20-v1/" + row["recipe"] + ".json"]
        _require(instance_bytes == expected, "checker-retained-validated-buffer")
        self.checks.append(dict(row))
        self.events.append(("check", row["sequence"]))
        injected = self.hit("checker")
        if injected is not _MISSING:
            return injected
        return self.original_check(instance_bytes, certificate_bytes)

    def install(self):
        p = self.patches
        for name in ("recipe_ids", "build_corpus"):
            original_corpus = getattr(self.modules["corpus"], name)

            def corpus_call(*args, _name=name, _original=original_corpus, **kwargs):
                self.corpus_access[_name] += 1
                changed = self.hit(_name)
                return _original(*args, **kwargs) if changed is _MISSING else changed
            p.setattr(self.modules["corpus"], name, corpus_call)
        p.setattr(self.modules["telemetry"], "solve_with_telemetry", self.solve)
        p.setattr(self.modules["certificate"], "build_certificate", self.build)
        p.setattr(self.modules["certificate"], "serialize_certificate", self.serialize)
        p.setattr(self.modules["check"], "verify_certificate", self.check)
        p.setattr(time, "perf_counter_ns", self.clock)
        p.setattr(time, "get_clock_info", lambda name: self.discover(
            "clock-info", SimpleNamespace(monotonic=True, adjustable=False, resolution=1e-9)))
        p.setattr(platform, "python_version", lambda: self.discover(
            "python-version", "SYNTHETIC-PYTHON"))
        p.setattr(platform, "platform", lambda: self.discover("platform", "SYNTHETIC-PLATFORM"))
        p.setattr(platform, "processor", lambda: self.discover("cpu", ""))
        original = self.modules["telemetry"].RunRecord.__post_init__
        session = self

        def record_post(record):
            _require(not session.clock_open, "record-construction-inside-clock")
            session.hit("record")
            original(record)
            session.record_objects.append(record)
        p.setattr(self.modules["telemetry"].RunRecord, "__post_init__", record_post)

    def invoke(self, argv=None):
        if argv is None:
            argv = ["--all"]
        original_argv, original_path = list(argv), list(sys.path)
        original_settings = (sys.get_int_max_str_digits(), sys.getrecursionlimit())
        original_environment = dict(os.environ)
        original_gc = (gc.isenabled(), gc.get_threshold())
        try:
            with pytest.MonkeyPatch.context() as policies:
                policies.setattr(sys, "set_int_max_str_digits", _no_access)
                policies.setattr(sys, "setrecursionlimit", _no_access)
                policies.setattr(gc, "enable", _no_access)
                policies.setattr(gc, "disable", _no_access)
                policies.setattr(gc, "set_threshold", _no_access)
                stdout, stderr = _Sink(), _Sink()
                policies.setattr(sys, "stdout", stdout)
                policies.setattr(sys, "stderr", stderr)
                response = self.runner.main(argv)
                _require(type(response) is int and response == 0, "successful-main-return")
                _require(sys.stdout is stdout and sys.stderr is stderr, "standard-stream-rebinding")
                _require(not stdout.data and not stderr.data, "successful-campaign-must-be-silent")
                _require(not stdout.closed and not stderr.closed, "standard-stream-closure")
                return response
        finally:
            _require(dict(os.environ) == original_environment, "environment-mutated")
            _require((gc.isenabled(), gc.get_threshold()) == original_gc, "gc-policy-mutated")
            _require(argv == original_argv, "argv-mutated")
            _require(sys.path == original_path, "sys-path-not-restored")
            _require((sys.get_int_max_str_digits(), sys.getrecursionlimit()) == original_settings,
                     "interpreter-settings-mutated")


@contextmanager
def _sandbox(tmp_path, bank, *, install=True):
    root = tmp_path / "source"
    root.mkdir()
    names = [row["path"] for row in _decode(bank["SOURCE_FIXTURE.json"])["closed_entries"]]
    names.extend(("exactfrac/experiments.py", "experiments/reproduce.py"))
    for name in names:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((_ROOT / name).read_bytes())
    source_inputs = root / "instances/unit20-v1"
    source_inputs.mkdir(parents=True)
    rows = _decode(bank["INPUT_EXPECTATIONS.json"])
    entries = []
    for row in rows:
        item = row["input"]
        raw = (_ROOT / "instances" / item["path"]).read_bytes()
        _require((len(raw), _sha(raw)) == (item["bytes"], item["sha256"]), "immutable-owned-input")
        (root / "instances" / item["path"]).write_bytes(raw)
        entries.append({key: (row["recipe"] if key == "recipe" else item[key])
                        for key in ("suite", "recipe", "path", "bytes", "sha256")})
    (root / "instances/MANIFEST").write_bytes(_json_bytes({
        "format": "exactfrac-corpus-manifest/1", "entries": entries}))
    saved = {name: module for name, module in sys.modules.copy().items() if _project(name)}
    old_path = list(sys.path)
    for name in saved:
        del sys.modules[name]
    sys.path.insert(0, str(root))
    importlib.invalidate_caches()
    try:
        with pytest.MonkeyPatch.context() as patches:
            modules = {name: importlib.import_module("exactfrac." + name)
                       for name in ("instance", "branch", "oracle", "solve", "witness",
                                    "telemetry", "certificate", "corpus")}
            modules["check"] = importlib.import_module("exactfrac_verify.check")
            session = _Session(root, bank, modules, patches)
            if install:
                session.install()
            with pytest.MonkeyPatch.context() as import_patches:
                def import_io(*_args, **_kwargs):
                    raise AssertionError("import-data-access")
                import_patches.setattr(builtins, "open", import_io)
                import_patches.setattr(io, "open", import_io)
                import_patches.setattr(os, "open", import_io)
                session.runner = importlib.import_module("exactfrac.experiments")
            _require(not session.calls and not session.discovered and not session.corpus_access,
                     "import-experiment-or-discovery")
            _require(Path(session.runner.__file__) == root / "exactfrac/experiments.py",
                     "sandbox-origin")
            old_profile = sys.getprofile()

            def profile(frame, event, _arg):
                if (event == "call" and not session.allow_real
                        and frame.f_code.co_name in ("solve", "solve_with_telemetry",
                            "solve_branch_standard", "solve_branch_accelerated", "exact_branch_min")
                        and str(root) in frame.f_code.co_filename):
                    raise AssertionError("unregistered-real-solver-call-in-scripted-test")
            sys.setprofile(profile)
            try:
                yield session
            finally:
                sys.setprofile(old_profile)
    finally:
        for name in list(sys.modules):
            if _project(name):
                del sys.modules[name]
        sys.modules.update(saved)
        sys.path[:] = old_path
        importlib.invalidate_caches()


def _keys(obj, names, guard):
    _require(type(obj) is dict and set(obj) == set(names), guard)


def _nonnegative(value, guard):
    _require(type(value) is int and value >= 0, guard)


def _source_identity(images):
    entries = [{"path": name, "sha256": _sha(images[name])} for name in sorted(images)]
    raw = b"exactfrac-unit21-source/1\n" + b"".join(
        row["path"].encode("ascii") + b"\0" + row["sha256"].encode("ascii") + b"\n"
        for row in entries
    )
    digest = _sha(raw)
    return {"entries": entries, "sha256": digest,
            "code_version": "exactfrac-source-sha256:" + digest}


def _algorithm_guard(algorithm, route, empty, bank):
    registry = _decode(bank["FIELD_REGISTRY.json"])
    schema = _decode(bank["WIRE_SCHEMAS.json"])
    _keys(algorithm, registry["AlgorithmStats"]["fields"], "algorithm-fields")
    native = algorithm["native"]
    _keys(native, registry["SolveStats"]["fields"], "native-fields")
    _require(native["branch_solver"] == route, "native-route")
    _require((native["attaining_candidate"] == "Empty") == empty, "native-empty")
    _require(native["attaining_candidate"] in ("Empty", "Baseline", "L0", "L1", "H0", "H1", "H2"),
             "native-attainment")
    _require(type(native["branch_stats"]) is list, "native-branches-type")
    _require(type(algorithm["branches"]) is list, "branches-type")
    _require(len(native["branch_stats"]) == len(algorithm["branches"]) == (0 if empty else 4),
             "all-four-branches")
    work_names = registry["WorkStats"]["fields"]
    for work in (algorithm["total"], algorithm["nonbranch"],
                 *(part["work"] for part in algorithm["branches"])):
        _keys(work, work_names, "work-fields")
        for value in work.values():
            _nonnegative(value, "work-exact-int")
        _require(work["newton_candidates"] == work["newton_updates"] + work["newton_queries"],
                 "newton-accounting")
        _require(work["lookahead_queries"] == sum(work[key] for key in (
            "lookahead_accepted", "lookahead_rejected", "lookahead_terminal")),
                 "lookahead-accounting")
        _require(work["max_flow_calls"] == work["ordinary_min_cut_calls"],
                 "ordinary-flow-accounting")
    for index, (branch, native_branch) in enumerate(zip(
            algorithm["branches"], native["branch_stats"], strict=True)):
        _keys(branch, registry["BranchTelemetry"]["fields"], "branch-fields")
        _require(type(branch["branch"]) is int and branch["branch"] == index, "branch-order")
        _require(type(branch["feasible"]) is bool, "branch-feasible-boolean")
        _keys(native_branch, registry[route + "BranchStats"]["fields"], "route-native-fields")
        _keys(native_branch["oracle_stats"], registry["BranchOracleStats"]["fields"],
              "oracle-fields")
        for key, value in native_branch.items():
            if key != "oracle_stats":
                _nonnegative(value, "native-exact-int")
        for value in native_branch["oracle_stats"].values():
            _nonnegative(value, "native-oracle-exact-int")
    buckets = [algorithm["nonbranch"], *(part["work"] for part in algorithm["branches"])]
    for name in work_names:
        expected = (sum(bucket[name] for bucket in buckets) if name in schema["event_fields"]
                    else max(bucket[name] for bucket in buckets))
        _require(algorithm["total"][name] == expected, "sum-events-max-peaks")
    for name in ("output_numerator_bits", "output_denominator_bits"):
        _require(type(algorithm[name]) is int and algorithm[name] >= 1, "output-width")


def _csv_line(values):
    return ",".join(
        "true" if value is True else "false" if value is False
        else _digits(value) if type(value) is int else value for value in values
    ).encode("ascii") + b"\n"


def _expected_tables(measured, bank):
    schema = _decode(bank["WIRE_SCHEMAS.json"])
    fields = _decode(bank["FIELD_REGISTRY.json"])["WorkStats"]["fields"]
    grouped = {}
    for row in measured:
        grouped.setdefault((row["recipe"], row["solver"]), []).append(row)
    summary = [_csv_line(schema["headers"]["summary"])]
    branches = [_csv_line(schema["headers"]["branches"])]
    comparison = [_csv_line(schema["headers"]["comparison"])]
    medians = {}
    for rid in sorted({rid for rid, _ in grouped}):
        for route in _ROUTES:
            rows = grouped[(rid, route)]
            _require(len(rows) == 3, "three-measured-repeats")
            row, algorithm = rows[0], rows[0]["record"]["algorithm"]
            median = sorted(part["elapsed_ns"] for part in rows)[1]
            medians[(rid, route)] = median
            summary.append(_csv_line([
                rid, route, *(row["input"][name] for name in (
                    "n", "m", "Q_bits", "max_q_bits", "max_f_bits", "input_integer_bits_sum")),
                3, median, algorithm["native"]["attaining_candidate"],
                *(algorithm["total"][name] for name in fields),
                algorithm["output_numerator_bits"], algorithm["output_denominator_bits"],
            ]))
            for branch in algorithm["branches"]:
                branches.append(_csv_line([rid, route, branch["branch"], branch["feasible"],
                                           *(branch["work"][name] for name in fields)]))
        std = grouped[(rid, "Standard")][0]["record"]["algorithm"]["total"]
        acc = grouped[(rid, "Accelerated")][0]["record"]["algorithm"]["total"]
        comparison.append(_csv_line([
            rid, medians[(rid, "Standard")], medians[(rid, "Accelerated")],
            *(value[name] for name in ("oracle_calls", "max_flow_calls", "peak_integer_bits")
              for value in (std, acc)),
        ]))
    return {"summary.csv": b"".join(summary), "branches.csv": b"".join(branches),
            "comparison.csv": b"".join(comparison)}


def _certificate_guard(obj, certificate):
    """Independent compact witness arithmetic, not a call to the runner/solver."""
    empty = certificate.get("empty")
    _require(type(empty) is bool, "certificate-empty-type")
    _keys(certificate, ("format", "empty", "N", "D") if empty else
          ("format", "empty", "N", "D", "U", "y"), "certificate-schema")
    _require(certificate["format"] == "exactfrac-certificate/1", "certificate-format")
    _require(type(certificate["N"]) is int and type(certificate["D"]) is int
             and certificate["D"] > 0, "certificate-raw-integers")
    if empty:
        _require(sum(edge[2] for edge in obj["edges"]) == 1 and
                 (certificate["N"], certificate["D"]) == (0, 1), "independent-empty-C0")
        return
    vertices = certificate["U"]
    _require(type(vertices) is list and bool(vertices) and
             all(type(v) is int and 0 <= v < obj["n"] for v in vertices), "certificate-shore")
    _require(vertices == sorted(set(vertices)), "certificate-shore-order")
    chosen = set(vertices)
    counts = certificate["y"]
    _require(type(counts) is list, "certificate-count-list")
    prior, total = -1, 0
    for pair in counts:
        _require(type(pair) is list and len(pair) == 2 and
                 all(type(value) is int for value in pair), "certificate-count-shape")
        index, count = pair
        _require(prior < index < len(obj["edges"]), "certificate-edge-order")
        u, v, q = obj["edges"][index]
        _require((u in chosen) != (v in chosen) and 0 < count <= q, "certificate-boundary-count")
        prior, total = index, total + count
    capacity = sum(obj["f"][v] for v in vertices)
    internal = sum(q for u, v, q in obj["edges"] if u in chosen and v in chosen)
    _require(capacity + total >= 3 and (capacity + total) % 2 == 1,
             "independent-certificate-admissibility")
    _require((certificate["N"], certificate["D"]) ==
             (2 * (internal + total), capacity + total - 1), "independent-certificate-attainment")


def _audit_output(files, bank, source_images, input_images, observed=None, *, historical=False):
    """Independent owning consumer; not a production result parser/API."""
    schema = _decode(bank["WIRE_SCHEMAS.json"])
    expected = {row["recipe"]: row for row in _decode(bank["INPUT_EXPECTATIONS.json"])}
    schedule = _schedule(bank)
    names = {"run-info.json", "warmups.jsonl", "runs.jsonl", "summary.csv", "branches.csv",
             "comparison.csv", "COMPLETE.json"}
    names.update(f"certificates/{rid}.{route}.json" for rid in expected for route in _ROUTES)
    _require(set(files) == names, "owned-output-membership")
    info = _decode(files["run-info.json"])
    _keys(info, schema["info"], "info-schema")
    _require(files["run-info.json"] == _json_bytes(info), "info-canonical-wire")
    _require((info["format"], info["campaign"]) == (
        "exactfrac-experiment-info/1", "unit21-v1"), "info-version")
    _require(info["protocol"] == _decode(bank["SYNTHETIC_RUN_INFO.json"])["protocol"],
             "fixed-protocol")
    source = _source_identity(source_images)
    _require(info["source"] == source, "source-fingerprint")
    _require(info["inputs"] == {"suite": "unit20-v1", "recipes": 655,
                                "manifest_sha256": (info["inputs"]["manifest_sha256"] if historical
                                                    else _sha(input_images["MANIFEST"]))},
             "input-provenance")
    _require(type(info["inputs"]["manifest_sha256"]) is str and
             re.fullmatch(r"[0-9a-f]{64}", info["inputs"]["manifest_sha256"]) is not None,
             "manifest-provenance-shape")
    environment = info["environment"]
    _keys(environment, schema["environment"], "environment-fields")
    clock = environment["clock"]
    _keys(clock, schema["clock"], "clock-fields")
    _require(clock["name"] == "perf_counter_ns" and clock["monotonic"] is True, "monotone-clock")
    _require(type(clock["adjustable"]) is bool, "adjustable-type")
    _require(type(clock["resolution_s"]) is float and math.isfinite(clock["resolution_s"])
             and clock["resolution_s"] > 0, "clock-resolution")
    for name in ("python_version", "platform"):
        _require(type(environment[name]) is str and bool(environment[name]), "environment-string")
    _require(environment["cpu"] is None or (type(environment["cpu"]) is str
                                            and bool(environment["cpu"])), "cpu-type")
    _require(environment["hash_seed"] is None or type(environment["hash_seed"]) is str, "seed-type")
    for name in ("int_max_str_digits", "recursion_limit"):
        _nonnegative(environment[name], "settings-int")
    certificates = {}
    for rid, expectation in expected.items():
        item = expectation["input"]
        input_raw = input_images[item["path"]]
        _require((len(input_raw), _sha(input_raw)) == (item["bytes"], item["sha256"]),
                 "independent-owned-input-bytes")
        obj = _decode(input_raw)
        for route in _ROUTES:
            certificate = _decode(files[f"certificates/{rid}.{route}.json"])
            _certificate_guard(obj, certificate)
            certificates[(rid, route)] = certificate
    ordered, by_key = {}, {}
    registry = _decode(bank["FIELD_REGISTRY.json"])
    for filename, phase in (("warmups.jsonl", "warmup"), ("runs.jsonl", "measured")):
        raw = files[filename]
        _require(raw.endswith(b"\n"), "jsonl-final-LF")
        lines = raw.splitlines(keepends=True)
        rows = [_decode(line) for line in lines]
        want = [row for row in schedule if row["phase"] == phase]
        _require(len(rows) == len(want), "observed-run-count")
        for line, row, scheduled in zip(lines, rows, want, strict=True):
            _require(line == _json_bytes(row), "row-canonical-wire")
            _keys(row, schema["run"], "run-schema")
            rid, route = scheduled["recipe"], scheduled["solver"]
            _require((row["format"], row["campaign"], row["recipe"], row["solver"],
                      row["phase"], row["repeat"])
                     == ("exactfrac-run/1", "unit21-v1", rid, route, phase, scheduled["repeat"]),
                     "raw-schedule-identity")
            _require(type(row["repeat"]) is int, "repeat-exact-int")
            _require(row["input"] == expected[rid]["input"], "independent-input-row")
            for name, value in row["input"].items():
                if name not in ("suite", "path", "sha256"):
                    _nonnegative(value, "input-metadata-exact-int")
            _keys(row["certificate"], schema["certificate"], "certificate-reference-fields")
            cert_path = f"certificates/{rid}.{route}.json"
            cert_raw = files[cert_path]
            _require(row["certificate"] == {"path": cert_path, "bytes": len(cert_raw),
                                            "sha256": _sha(cert_raw)},
                     "certificate-reference-binding")
            cert = certificates[(rid, route)]
            want_empty = expected[rid]["empty"]
            _require(type(cert["empty"]) is bool and cert["empty"] == want_empty,
                     "independent-empty")
            _require(type(cert["N"]) is int and type(cert["D"]) is int and cert["D"] > 0,
                     "certificate-integer-pair")
            _require(cert["N"] * _expression(
                         expected[rid]["D_expression"], expected[rid]["expression_bits"])
                     == cert["D"] * _expression(
                         expected[rid]["N_expression"], expected[rid]["expression_bits"]),
                     "independent-optimum-not-C0-alone")
            _keys(row["record"], registry["RunRecord"]["fields"], "run-record-fields")
            metadata = row["record"]["metadata"]
            _keys(metadata, registry["RunMetadata"]["fields"], "metadata-fields")
            elapsed = row["elapsed_ns"]
            if phase == "warmup":
                _require(elapsed is None and metadata["wall_clock_s"] is None, "untimed-warmup")
            else:
                _nonnegative(elapsed, "elapsed-exact-int")
                _require(type(metadata["wall_clock_s"]) is float
                         and math.isfinite(metadata["wall_clock_s"])
                         and metadata["wall_clock_s"] == elapsed / 1_000_000_000,
                         "elapsed-conversion")
            want_metadata = {key: environment[key] for key in ("python_version", "platform", "cpu")}
            want_metadata.update(code_version=source["code_version"],
                                 instance_sha256=expected[rid]["input"]["sha256"],
                                 wall_clock_s=(
                                     None if phase == "warmup" else elapsed / 1_000_000_000))
            _require(metadata == want_metadata, "metadata-bindings")
            algorithm = row["record"]["algorithm"]
            _algorithm_guard(algorithm, route, want_empty, bank)
            _require((algorithm["output_numerator_bits"], algorithm["output_denominator_bits"])
                     == (max(1, abs(cert["N"]).bit_length()), max(1, cert["D"].bit_length())),
                     "raw-pair-width")
            key = (rid, route)
            if key in by_key:
                _require(algorithm == by_key[key], "same-route-repeat-identity")
            else:
                by_key[key] = algorithm
            if observed is not None:
                _require(algorithm == observed[scheduled["sequence"]],
                         "retained-actual-AlgorithmStats")
            ordered[scheduled["sequence"]] = row
    for name, want in _expected_tables([ordered[row["sequence"]] for row in schedule
                                       if row["phase"] == "measured"], bank).items():
        _require(files[name] == want, "exact-independent-table:" + name)
    complete = _decode(files["COMPLETE.json"])
    _keys(complete, schema["complete"], "complete-schema")
    ledger = [{"path": name, "bytes": len(raw), "sha256": _sha(raw)}
              for name, raw in sorted(files.items()) if name != "COMPLETE.json"]
    want_complete = {"format": "exactfrac-experiment-complete/1", "campaign": "unit21-v1",
                     "source_sha256": source["sha256"], "recipes": 655,
                     "warmup_solves": 1310, "measured_solves": 3930,
                     "checked_certificates": 5240, "files": ledger}
    _require(complete == want_complete, "complete-ledger-and-observed-counts")
    _require(files["COMPLETE.json"] == _json_bytes(complete), "complete-canonical-wire")
    for name in ("recipes", "warmup_solves", "measured_solves", "checked_certificates"):
        _nonnegative(complete[name], "complete-count-type")
    for row in complete["files"]:
        _nonnegative(row["bytes"], "ledger-byte-type")
    return ordered


class _OutputIO:
    """Inject independently of whether the runner uses streams or os.write."""

    def __init__(self, session, *, stage=None, value=_MISSING, exception=None, target="runs.jsonl"):
        self.session, self.stage, self.value, self.exception = session, stage, value, exception
        self.target = target
        self.paths, self.active, self.events = {}, set(), []
        self.hits = 0
        self.open = builtins.open
        self.io_open = io.open
        self.fdopen = os.fdopen
        self.os_open, self.write, self.close, self.fsync = os.open, os.write, os.close, os.fsync

    def affect(self, stage, name, raw=None):
        self.events.append((stage, name))
        if name == "COMPLETE.json" and stage == "open":
            _require(not self.active, "completion-before-closing-artifacts")
            _require(len(self.session.calls) == len(self.session.checks) == 5240,
                     "completion-before-all-verified-calls")
        if name != self.target or stage != self.stage:
            return _MISSING
        self.hits += 1
        if self.exception is not None:
            raise self.exception
        if self.value == "short":
            return max(1, len(raw) // 3)
        if self.value == "too-large":
            return len(raw) + 1
        return self.value

    def name(self, path):
        if isinstance(path, int):
            return self.paths.get(path)
        p = Path(path)
        if not p.is_absolute():
            p = Path.cwd() / p
        return (p.relative_to(self.session.output).as_posix()
                if p.is_relative_to(self.session.output) else None)

    def stream_open(self, original, path, mode="r", *args, **kwargs):
        name = self.name(path)
        writing = any(char in mode for char in "wxa+")
        if name is not None and writing and not isinstance(path, int):
            _require("x" in mode, "output-stream-not-exclusive")
            self.affect("open", name)
        stream = original(path, mode, *args, **kwargs)
        if name is None or not writing:
            return stream
        if isinstance(path, int):
            self.active.discard(path)
            self.paths.pop(path, None)
        self.active.add(id(stream))
        monitor = self

        class Stream:
            def __getattr__(self, attr):
                return getattr(stream, attr)

            def __enter__(self):
                return self

            def __exit__(self, *_):
                self.close()
                return False

            def write(self, raw):
                changed = monitor.affect("write", name, raw)
                if changed is _MISSING:
                    return stream.write(raw)
                if monitor.value == "short":
                    return stream.write(raw[:changed])
                return changed

            def flush(self):
                changed = monitor.affect("flush", name)
                return stream.flush() if changed is _MISSING else changed

            def close(self):
                if monitor.stage == "flush":
                    monitor.affect("flush", name)  # implicit stream flush during close
                changed = monitor.affect("close", name)
                answer = stream.close() if changed is _MISSING else changed
                monitor.active.discard(id(stream))
                return answer
        return Stream()

    def install(self):
        patches = self.session.patches
        patches.setattr(builtins, "open", lambda *a, **k: self.stream_open(self.open, *a, **k))
        patches.setattr(io, "open", lambda *a, **k: self.stream_open(self.io_open, *a, **k))
        patches.setattr(os, "fdopen", lambda *a, **k: self.stream_open(self.fdopen, *a, **k))

        def open_fd(path, flags, *args, **kwargs):
            name = self.name(path)
            writing = bool(flags & (os.O_WRONLY | os.O_RDWR))
            if name is not None and writing:
                self.affect("open", name)
                _require(bool(flags & os.O_EXCL), "output-files-not-exclusive")
            fd = self.os_open(path, flags, *args, **kwargs)
            if name is not None and writing:
                self.paths[fd] = name
                self.active.add(fd)
            return fd

        def write_fd(fd, raw):
            name = self.paths.get(fd)
            if name is None:
                return self.write(fd, raw)
            changed = self.affect("write", name, raw)
            if changed is _MISSING:
                return self.write(fd, raw)
            return self.write(fd, raw[:changed]) if self.value == "short" else changed

        def close_fd(fd):
            name = self.paths.get(fd)
            changed = _MISSING if name is None else self.affect("close", name)
            answer = self.close(fd) if changed is _MISSING else changed
            self.active.discard(fd)
            self.paths.pop(fd, None)
            return answer

        patches.setattr(os, "open", open_fd)
        patches.setattr(os, "write", write_fd)
        patches.setattr(os, "close", close_fd)


def _check_success(session):
    _require(session.calls == session.schedule, "5240-observed-scripted-identities")
    _require(session.checks == session.schedule, "5240-per-call-checker-identities")
    _require(not session.clock_open, "unclosed-clock-interval")
    _require(len(session.record_objects) >= 5240, "actual-RunRecord-construction")
    for index, event in enumerate(session.events):
        if event[0] == "clock-start":
            _require(session.events[index + 1] == ("solve-enter", event[1]), "start-not-immediate")
        if event[0] == "solve-return" and session.schedule[event[1]]["phase"] == "measured":
            _require(session.events[index + 1] == ("clock-end", event[1]), "end-not-immediate")
    _require(session.discovered == Counter({"python-version": 1, "platform": 1, "cpu": 1,
                                           "clock-info": 1}), "environment-discovery-once")
    _require(all((session.root / name).read_bytes() == raw
                 for name, raw in session.source_images.items()),
             "source-mutated-by-runner")
    _require(_snapshot(session.inputs) == session.initial_input_images, "inputs-mutated-by-runner")
    _require({p.relative_to(session.output).as_posix() for p in session.output.rglob("*")
              if p.is_dir()} == {"certificates"}, "owned-output-directory-membership")
    files = _snapshot(session.output)
    _require(all(files[f"certificates/{rid}.{route}.json"] == raw
                 for (rid, route), raw in session.certificates.items()),
             "emitted-checked-certificate-bytes")
    observed = {sequence: _decode(_wire(dataclasses.asdict(value[1])))
                for sequence, value in session.returned.items()}
    rows = _audit_output(
        files, session.bank, session.source_images, session.initial_input_images, observed)
    for sequence, row in rows.items():
        _require(row["elapsed_ns"] == session.elapsed(session.schedule[sequence]),
                 "fake-clock-exact-elapsed")
    return {"files": files, "source": session.source_images, "inputs": session.initial_input_images,
            "observed": observed, "rows": rows, "bank": session.bank,
            "real_calls": session.real_calls}


@pytest.fixture(scope="module")
def bank():
    return _bank()


@pytest.fixture(scope="module")
def scripted(tmp_path_factory, bank):
    with _sandbox(tmp_path_factory.mktemp("u21-scripted"), bank) as session:
        monitor = _OutputIO(session)
        monitor.install()
        assert session.invoke() == 0
        result = _check_success(session)
        assert monitor.events[-1][1] == "COMPLETE.json"
        assert sum(event == ("open", "COMPLETE.json") for event in monitor.events) == 1
        result["events"] = list(session.events)
        return result


class _String(str):
    pass


class _List(list):
    pass


class _Sink:
    def __init__(self, *, short=False, bad=_MISSING, error=None, flush_error=None):
        self.buffer = self
        self.data = bytearray()
        self.closed = False
        self.short, self.bad, self.error, self.flush_error = short, bad, error, flush_error
        self.flushes = 0

    def write(self, raw):
        _require(type(raw) in (bytes, bytearray, memoryview), "binary-standard-stream")
        if self.error is not None:
            raise self.error
        if self.bad is not _MISSING:
            return len(raw) + 1 if self.bad == "oversize" else self.bad
        amount = min(3, len(raw)) if self.short else len(raw)
        self.data.extend(raw[:amount])
        return amount

    def flush(self):
        self.flushes += 1
        if self.flush_error is not None:
            raise self.flush_error
        return None

    def close(self):
        self.closed = True
        raise AssertionError("runner-closed-standard-stream")


def _no_access(*_args, **_kwargs):
    raise AssertionError("public-boundary-access-before-validation")


@contextmanager
def _boundary_streams(session, stdout=None, stderr=None):
    stdout, stderr = stdout or _Sink(), stderr or _Sink()
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(sys, "stdout", stdout)
        patch.setattr(sys, "stderr", stderr)
        patch.setattr(builtins, "open", _no_access)
        patch.setattr(io, "open", _no_access)
        patch.setattr(os, "open", _no_access)
        session.failure = ("recipe_ids", AssertionError("early-corpus"))
        session.on_stage = lambda stage, _: _no_access() if stage in (
            "solve", "python-version", "platform", "cpu", "clock-info", "clock-start") else None
        try:
            yield stdout, stderr
            _require(sys.stdout is stdout and sys.stderr is stderr, "standard-stream-rebinding")
            _require(not stdout.closed and not stderr.closed, "standard-stream-closure")
        finally:
            session.failure = None
            session.on_stage = None


def _no_complete(session):
    assert not (session.output / "COMPLETE.json").exists()


def _replace(session, module, name, value):
    old = getattr(module, name)
    session.patches.setattr(module, name, value)
    for alias, item in list(vars(session.runner).items()):
        if item is old:
            session.patches.setattr(session.runner, alias, value)


def test_public_interface_and_runtime_dependency_direction():
    assert type(experiments.__all__) is tuple and experiments.__all__ == ("main",)
    assert inspect.isfunction(experiments.main)
    signature = inspect.signature(experiments.main)
    assert tuple(signature.parameters) == ("argv",)
    parameter = signature.parameters["argv"]
    assert parameter.default is None
    assert parameter.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert get_type_hints(experiments.main) == {"argv": list[str] | None, "return": int}
    public = [name for name, obj in vars(experiments).items()
              if inspect.isfunction(obj) and obj.__module__ == experiments.__name__
              and not name.startswith("_")]
    assert public == ["main"]
    for path in (_ROOT / "exactfrac/experiments.py", _ROOT / "experiments/reproduce.py"):
        tree = ast.parse(path.read_bytes())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert not (node.module or "").startswith(("tests", "test_"))
                if (node.module or "").startswith(("exactfrac", "exactfrac_verify")) or node.level:
                    assert all(not name.name.startswith("_") for name in node.names)
            if isinstance(node, ast.Import):
                assert all(not name.name.startswith(("tests", "test_")) for name in node.names)


@pytest.mark.parametrize("value", [False, 1, "--help", b"--help", (), {}, iter(()),
                                   _List(["--help"]), [_String("--help")], [None],
                                   [1], [Path("--help")]])
def test_exact_argv_types_reject_before_access(tmp_path, bank, value):
    with _sandbox(tmp_path, bank) as session, _boundary_streams(session):
        with pytest.raises(ValueError) as error:
            session.runner.main(value)
        assert type(error.value) is ValueError


def test_usage_is_fixed_binary_non_echoing_and_help_is_pure(tmp_path, bank):
    invalid = [[], ["SECRET_INPUT"], ["--all", "--all"], ["--all=1"],
               ["--help", "--all"], ["--all", "--help"], ["--instances", "x", "--all"],
               ["--all", "--instances"], ["--all", "--output"], ["--all", "--output", ""],
               ["--all", "--output=x"], ["--all", "--output", "-x"],
               ["--all", "--instances", "a\x00b"], ["--all", "extra"],
               ["--all", "--instances", "x", "--instances", "y"],
               ["--all", "--output", "x", "--output", "y"], ["--all", "--seed", "73"]]
    with _sandbox(tmp_path, bank) as session:
        message = None
        for argv in invalid:
            with _boundary_streams(session, stderr=_Sink(short=True)) as (out, err):
                before = list(argv)
                assert session.runner.main(argv) == 2
                assert argv == before and not out.data and err.data
                assert err.flushes > 0 and b"SECRET_INPUT" not in err.data
                if message is None:
                    message = bytes(err.data)
                assert bytes(err.data) == message
        with _boundary_streams(session, stdout=_Sink(short=True)) as (out, err):
            assert session.runner.main(["--help"]) == 0
            assert not err.data and out.flushes > 0
            for word in (b"--help", b"--all", b"--instances", b"--output"):
                assert word in out.data
        with _boundary_streams(session) as (out, err):
            session.patches.setattr(sys, "argv", ["ignored", "--help"])
            before = list(sys.argv)
            assert session.runner.main() == 0
            assert sys.argv == before and out.data and not err.data


@pytest.mark.parametrize("value", [None, False, 0, -1, "oversize"])
def test_invalid_standard_binary_write_return(tmp_path, bank, value):
    with (
        _sandbox(tmp_path, bank) as session,
        _boundary_streams(session, stdout=_Sink(bad=value)),
        pytest.raises(RuntimeError),
    ):
        session.runner.main(["--help"])


@pytest.mark.parametrize("where", ["write", "flush"])
def test_standard_stream_exception_identity(tmp_path, bank, where):
    sentinel = OSError("synthetic stream failure")
    sink = _Sink(error=sentinel) if where == "write" else _Sink(flush_error=sentinel)
    with _sandbox(tmp_path, bank) as session, _boundary_streams(session, stdout=sink):
        with pytest.raises(OSError) as error:
            session.runner.main(["--help"])
        assert error.value is sentinel


def test_invalid_standard_flush_return(tmp_path, bank):
    sink = _Sink()
    sink.flush = lambda: 0
    with (
        _sandbox(tmp_path, bank) as session,
        _boundary_streams(session, stdout=sink),
        pytest.raises(RuntimeError),
    ):
        session.runner.main(["--help"])


def test_import_wrapper_guard_and_same_main(tmp_path, bank):
    with _sandbox(tmp_path, bank) as session:
        assert not session.calls and not session.discovered and not session.corpus_access
        with _boundary_streams(session) as (out, err):
            namespace = runpy.run_path(str(session.root / "experiments/reproduce.py"),
                                      run_name="import_only")
            assert not out.data and not err.data
            assert "__name__" in namespace
        calls = []
        session.patches.setattr(session.runner, "main", lambda: calls.append("same-main") or 7)
        before = list(sys.path)
        with pytest.raises(SystemExit) as error:
            runpy.run_path(str(session.root / "experiments/reproduce.py"), run_name="__main__")
        assert error.value.code == 7 and calls == ["same-main"]
        assert sys.path == before


@pytest.mark.parametrize("change", ["bool-bytes", "float-bytes", "string-bytes", "negative-bytes",
    "missing-row", "extra-owned-row", "duplicate-row", "reorder", "wrong-hash", "wrong-length",
    "wrong-path", "nested-path", "backslash-path", "suite-leading-zero", "recipe-uppercase",
    "extra-root-key", "extra-entry-key", "bad-format", "missing-root-key", "missing-entry-key"])
def test_manifest_rejection_precedes_solve_and_output(tmp_path, bank, change):
    with _sandbox(tmp_path, bank) as session:
        path = session.inputs / "MANIFEST"
        obj = _decode(path.read_bytes())
        row = obj["entries"][0]
        if change in ("bool-bytes", "float-bytes", "string-bytes", "negative-bytes"):
            row["bytes"] = {"bool-bytes": True, "float-bytes": 96.0,
                            "string-bytes": "96", "negative-bytes": -1}[change]
        elif change == "missing-row":
            obj["entries"].pop()
        elif change == "extra-owned-row":
            extra = dict(obj["entries"][-1], recipe="zz-extra", path="unit20-v1/zz-extra.json")
            obj["entries"].append(extra)
        elif change == "duplicate-row":
            obj["entries"].insert(0, dict(row))
        elif change == "reorder":
            obj["entries"][0:2] = reversed(obj["entries"][0:2])
        elif change == "wrong-hash":
            row["sha256"] = "0" * 64
        elif change == "wrong-length":
            row["bytes"] += 1
        elif change == "wrong-path":
            row["path"] = "../escape.json"
        elif change == "nested-path":
            row["path"] = "unit20-v1/nested/" + row["recipe"] + ".json"
        elif change == "backslash-path":
            row["path"] = row["path"].replace("/", "\\")
        elif change == "suite-leading-zero":
            row["suite"] = "unit020-v1"
        elif change == "recipe-uppercase":
            row["recipe"] = row["recipe"].upper()
        elif change == "extra-root-key":
            obj["extra"] = 1
        elif change == "extra-entry-key":
            row["extra"] = 1
        elif change == "bad-format":
            obj["format"] = "unknown"
        elif change == "missing-root-key":
            obj.pop("format")
        elif change == "missing-entry-key":
            row.pop("bytes")
        path.write_bytes(_json_bytes(obj))
        with pytest.raises(ValueError) as error:
            session.invoke()
        assert type(error.value) is ValueError
        assert not session.calls and not session.output.exists()


@pytest.mark.parametrize("fault", [
    "decoded-duplicate-root", "decoded-duplicate-entry", "negative-zero",
                                   "exponent", "NaN", "trailing-data", "invalid-utf8", "BOM"])
def test_manifest_lexical_json_traps(tmp_path, bank, fault):
    with _sandbox(tmp_path, bank) as session:
        path = session.inputs / "MANIFEST"
        raw = path.read_bytes()
        if fault == "decoded-duplicate-root":
            raw = raw.replace(b'{', b'{"f\\u006frmat":"exactfrac-corpus-manifest/1",', 1)
        elif fault == "decoded-duplicate-entry":
            raw = raw.replace(b'"bytes":', b'"b\\u0079tes":96,"bytes":', 1)
        elif fault in ("negative-zero", "exponent", "NaN"):
            token = {"negative-zero": b"-0", "exponent": b"9.6e1", "NaN": b"NaN"}[fault]
            raw, count = re.subn(rb'"bytes":[0-9]+', b'"bytes":' + token, raw, count=1)
            assert count == 1
        elif fault == "invalid-utf8":
            raw = b"\xff" + raw
        elif fault == "BOM":
            raw = b"\xef\xbb\xbf" + raw
        else:
            raw += b"{}"
        path.write_bytes(raw)
        with pytest.raises(ValueError) as error:
            session.invoke()
        assert type(error.value) is ValueError
        assert not session.calls and not session.output.exists()


def test_coherent_altered_payload_is_not_its_own_oracle(tmp_path, bank):
    with _sandbox(tmp_path, bank) as session:
        manifest = _decode((session.inputs / "MANIFEST").read_bytes())
        row = manifest["entries"][0]
        path = session.inputs / row["path"]
        obj = _decode(path.read_bytes())
        obj["f"][0] = 1
        changed = _json_bytes(obj)
        assert changed != path.read_bytes()
        path.write_bytes(changed)
        row.update(bytes=len(changed), sha256=_sha(changed))
        (session.inputs / "MANIFEST").write_bytes(_json_bytes(manifest))
        with pytest.raises(ValueError):
            session.invoke()
        assert not session.calls and not session.output.exists()


@pytest.mark.parametrize("fault", ["payload-symlink", "owned-parent-symlink", "manifest-symlink",
    "executable", "extra", "nested", "missing", "renamed", "fifo", "input-parent-symlink"])
def test_input_filesystem_fail_closed(tmp_path, bank, fault):
    with _sandbox(tmp_path, bank) as session:
        owned = session.inputs / "unit20-v1"
        payload = owned / (session.expectations[0]["recipe"] + ".json")
        native_missing = False
        if fault == "payload-symlink":
            target = tmp_path / "redirected.json"
            payload.rename(target)
            payload.symlink_to(target)
        elif fault == "owned-parent-symlink":
            target = tmp_path / "redirected-owned"
            owned.rename(target)
            owned.symlink_to(target, target_is_directory=True)
        elif fault == "manifest-symlink":
            target = tmp_path / "redirected-manifest"
            (session.inputs / "MANIFEST").rename(target)
            (session.inputs / "MANIFEST").symlink_to(target)
        elif fault == "executable":
            payload.chmod(0o744)
        elif fault == "extra":
            (owned / "extra.json").write_bytes(b"{}\n")
        elif fault == "nested":
            (owned / "nested").mkdir()
            payload.rename(owned / "nested" / payload.name)
        elif fault == "missing":
            payload.rename(tmp_path / payload.name)
            native_missing = True
        elif fault == "renamed":
            payload.rename(owned / "renamed.json")
        elif fault == "fifo":
            payload.unlink()
            os.mkfifo(payload)
        else:
            target = tmp_path / "actual-inputs"
            session.inputs.rename(target)
            session.inputs.symlink_to(target, target_is_directory=True)
        with pytest.raises((ValueError, FileNotFoundError) if native_missing else ValueError):
            session.invoke()
        assert not session.calls and not session.output.exists()


@pytest.mark.parametrize("target", [
    "existing-empty", "existing-file", "output-symlink", "parent-symlink",
                                    "source", "inputs", "git", "tests", "ancestor", "dotdot"])
def test_output_lexical_and_ownership_rejection(tmp_path, bank, target):
    with _sandbox(tmp_path, bank) as session:
        out = tmp_path / "external"
        if target == "existing-empty":
            out.mkdir()
        elif target == "existing-file":
            out.write_bytes(b"preserve\n")
        elif target == "output-symlink":
            out.symlink_to(tmp_path / "absent")
        elif target == "parent-symlink":
            (tmp_path / "real-parent").mkdir()
            (tmp_path / "alias").symlink_to(tmp_path / "real-parent", target_is_directory=True)
            out = tmp_path / "alias/new"
        else:
            out = {"source": session.root / "exactfrac/new", "inputs": session.inputs / "new",
                   "git": session.root / ".git/new", "tests": session.root / "tests/new",
                   "ancestor": tmp_path, "dotdot": tmp_path / "unmade/../fresh"}[target]
        with pytest.raises(ValueError) as error:
            session.invoke(["--all", "--output", str(out)])
        assert type(error.value) is ValueError and not session.calls
        if target == "existing-file":
            assert out.read_bytes() == b"preserve\n"
        if target == "existing-empty":
            assert list(out.iterdir()) == []


@pytest.mark.parametrize("fault", ["list-registry", "omitted-registry", "tuple-subclass-registry",
                                    "list-build", "truncated-build", "bad-leaf-build"])
def test_closed_generator_normal_return_promises(tmp_path, bank, fault):
    with _sandbox(tmp_path, bank) as session:
        corpus = session.modules["corpus"]
        registry = corpus.recipe_ids()
        records = corpus.build_corpus()
        if fault.endswith("registry"):
            value = list(registry) if fault == "list-registry" else registry[:-1]
            if fault == "tuple-subclass-registry":
                class Tuple(tuple):
                    pass
                value = Tuple(registry)
            _replace(session, corpus, "recipe_ids", lambda: value)
        else:
            value = list(records) if fault == "list-build" else records[:-1]
            if fault == "bad-leaf-build":
                value = (("MANIFEST", bytearray(records[0][1])), *records[1:])
            _replace(session, corpus, "build_corpus", lambda: value)
        with pytest.raises(RuntimeError):
            session.invoke()
        assert not session.calls and not session.output.exists()


@pytest.mark.parametrize("stage", ["recipe_ids", "build_corpus", "solve", "build", "serialize",
                                    "checker", "record", "clock-start", "clock-end"])
@pytest.mark.parametrize("exception_type", [
    MemoryError, RecursionError, OSError, KeyboardInterrupt])
def test_dependency_exception_object_is_not_translated(tmp_path, bank, stage, exception_type):
    sentinel = exception_type("synthetic dependency failure")
    with _sandbox(tmp_path, bank) as session:
        session.failure = (stage, sentinel)
        with pytest.raises(exception_type) as error:
            session.invoke()
        assert error.value is sentinel
        _no_complete(session)
        assert all((session.root / name).read_bytes() == raw
                   for name, raw in session.source_images.items())
        assert _snapshot(session.inputs) == session.initial_input_images


@pytest.mark.parametrize("stage,value", [("solve", None), ("solve", []), ("solve", (None, None)),
    ("solve", (None, None, None)), ("build", []), ("serialize", bytearray(b"{}")),
    ("checker", False), ("checker", 0), ("clock-start", True), ("clock-start", -1),
    ("clock-start", 1.0), ("clock-end", None), ("clock-end", 0)])
def test_bad_normal_return_is_runtime_error_not_failed_row(tmp_path, bank, stage, value):
    with _sandbox(tmp_path, bank) as session:
        session.bad_return = (stage, value)
        with pytest.raises(RuntimeError):
            session.invoke()
        _no_complete(session)


def test_closed_instance_exception_identity(tmp_path, bank):
    sentinel = ValueError("closed Instance validation")
    with _sandbox(tmp_path, bank) as session:
        cls = session.modules["instance"].Instance

        def invalid(_cls, *_args, **_kwargs):
            raise sentinel
        session.patches.setattr(cls, "from_dict", classmethod(invalid))
        with pytest.raises(ValueError) as error:
            session.invoke()
        assert error.value is sentinel and not session.calls
        assert not session.output.exists()


@pytest.mark.parametrize("drift", ["source-after-solve", "input-after-check", "foreign-module-file",
                                  "foreign-module-spec"])
def test_source_input_and_import_identity_drift(tmp_path, bank, drift):
    with _sandbox(tmp_path, bank) as session:
        changed = []
        if drift.startswith("foreign-module"):
            module = session.modules["witness"]
            if drift == "foreign-module-file":
                session.patches.setattr(module, "__file__", str(tmp_path / "foreign.py"))
            else:
                session.patches.setattr(module.__spec__, "origin", str(tmp_path / "foreign.py"))
        else:
            def alter(stage, current):
                desired = "solve" if drift == "source-after-solve" else "checker"
                if stage == desired and not changed:
                    path = (current.root / "exactfrac/witness.py" if drift == "source-after-solve"
                            else current.inputs / current.expectations[0]["input"]["path"])
                    path.write_bytes(path.read_bytes() + b"\n")
                    changed.append(path)
            session.on_stage = alter
        with pytest.raises(RuntimeError):
            session.invoke()
        _no_complete(session)
        if drift.startswith("foreign-module"):
            assert not session.calls
        else:
            assert len(changed) == 1


def test_retained_bytes_are_not_swapped_after_input_validation(tmp_path, bank):
    with _sandbox(tmp_path, bank) as session:
        calls = []

        def alter(stage, current):
            if stage == "solve" and not calls:
                path = current.inputs / current.expectations[0]["input"]["path"]
                path.write_bytes(b"not the validated instance\n")
                calls.append(path)
        session.on_stage = alter
        with pytest.raises(RuntimeError):
            session.invoke()
        _no_complete(session)
        assert calls
        # The checker spy independently requires its input equals the retained bytes.
        assert session.checks


def test_scripted_schedule_counters_and_exact_tables(scripted, bank):
    files = scripted["files"]
    assert scripted["real_calls"] == 0
    selected = set(_decode(bank["SYNTHETIC_CALL_SCRIPT.json"])["selected_ids"])
    for name in ("summary.csv", "branches.csv", "comparison.csv"):
        lines = files[name].splitlines(keepends=True)
        projection = lines[0] + b"".join(line for line in lines[1:]
                                          if line.split(b",", 1)[0].decode() in selected)
        assert projection == bank["SYNTHETIC_" + name]
    for name, phase in (("SYNTHETIC_WARMUPS.jsonl", "warmup"),
                        ("SYNTHETIC_RUNS.jsonl", "measured")):
        expected_rows = [_decode(line) for line in bank[name].splitlines()]
        actual_rows = [row for _, row in sorted(scripted["rows"].items())
                       if row["recipe"] in selected and row["phase"] == phase]
        for actual, expected in zip(actual_rows, expected_rows, strict=True):
            expected["record"]["metadata"]["code_version"] = (
                _source_identity(scripted["source"])["code_version"])
            assert actual == expected
    std = _decode(files["certificates/struct-cycle-n04-b00001-fdegree.Standard.json"])
    acc = _decode(files["certificates/struct-cycle-n04-b00001-fdegree.Accelerated.json"])
    assert (std["N"], std["D"]) != (acc["N"], acc["D"])
    assert std["N"] * acc["D"] == acc["N"] * std["D"]
    print("EXACTFRAC_UNIT21_SCRIPTED_SCHEDULE " + json.dumps({
        "scripted_calls": 5240, "warmups": 1310, "measured": 3930, "actual_solver_calls": 0,
        "selected_fixture_calls": 24, "kind": "synthetic test, not initial campaign"},
        sort_keys=True))


def test_valid_foreign_aggregate_and_cwd_independence(tmp_path, bank):
    with _sandbox(tmp_path, bank) as session:
        path = session.inputs / "MANIFEST"
        manifest = _decode(path.read_bytes())
        manifest["entries"].append({"suite": "unit99-v1", "recipe": "foreign",
                                    "path": "unit99-v1/foreign.json",
                                     "bytes": 1, "sha256": "0" * 64})
        path.write_bytes((json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode())
        session.initial_input_images = _snapshot(session.inputs)
        working = tmp_path / "different-cwd"
        working.mkdir()
        session.patches.chdir(working)
        # A relative child is legal; parent traversal is separately rejected.
        session.output = working / "new-output"
        assert session.invoke([
            "--all", "--output", "new-output", "--instances", str(session.inputs)]) == 0
        _check_success(session)
        assert not (session.inputs / "unit99-v1").exists()


def test_default_paths_use_source_root_not_cwd(tmp_path, bank):
    with _sandbox(tmp_path, bank) as session:
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        session.patches.chdir(elsewhere)
        unrelated = {
            "experiments/README.md": b"future editable documentation\n",
            "docs/future.md": b"not a source fingerprint member\n",
            "results/foreign-run/preserved.txt": b"do not remove this output\n",
            "future_unused.py": b"# Inert unrelated test fixture, never imported.\n",
        }
        for name, raw in unrelated.items():
            path = session.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        assert session.invoke(["--all"]) == 0
        assert all((session.root / name).read_bytes() == raw for name, raw in unrelated.items())
        _check_success(session)
        assert not (elsewhere / "results").exists()


def test_bounded_actual_telemetry_integration_not_full_campaign(tmp_path, bank):
    with _sandbox(tmp_path, bank) as session:
        session.real_ids = set(session.selected)
        assert session.invoke() == 0
        _check_success(session)
        assert session.real_calls == 24
        assert len(session.calls) - session.real_calls == 5216
        print("EXACTFRAC_UNIT21_BOUNDED_REAL " + json.dumps({
            "actual_inputs": 3, "actual_telemetry_calls": session.real_calls,
            "scripted_other_calls": 5216, "kind": "bounded composition, not initial campaign"},
            sort_keys=True))


def test_giant_native_integer_is_unquoted_and_exact(tmp_path, bank):
    with _sandbox(tmp_path, bank) as session:
        session.giant = True
        assert session.invoke() == 0
        result = _check_success(session)
        expected = _decode(bank["SYNTHETIC_GIANT_ROW.jsonl"])
        matching = [row for row in result["rows"].values() if
                    (row["recipe"], row["solver"], row["phase"], row["repeat"])
                    == (expected["recipe"], expected["solver"],
                        expected["phase"], expected["repeat"])]
        assert len(matching) == 1
        assert matching[0]["record"]["algorithm"] == expected["record"]["algorithm"]
        assert len(re.findall(rb"[0-9]{4401}", result["files"]["runs.jsonl"])) >= 1


def _rebind_ledger(files):
    marker = _decode(files["COMPLETE.json"])
    marker["files"] = [{"path": name, "bytes": len(raw), "sha256": _sha(raw)}
                       for name, raw in sorted(files.items()) if name != "COMPLETE.json"]
    files["COMPLETE.json"] = _json_bytes(marker)


@pytest.mark.parametrize("fault", [
    "missing-artifact", "extra-artifact", "coherent-csv", "coherent-run-drop",
    "coherent-run-reorder", "coherent-native-field", "coherent-peak-sum", "coherent-branch-drop",
    "coherent-input-hash", "coherent-certificate-ref", "coherent-raw-integer-string",
    "coherent-warmup-clock", "coherent-source", "duplicate-decoded-key",
    "coherent-certificate-witness", "marker-self-reference", "marker-wrong-count"])
def test_independent_consumer_detects_coherent_corruption(scripted, fault):
    files = dict(scripted["files"])
    if fault == "missing-artifact":
        files.pop("comparison.csv")
    elif fault == "extra-artifact":
        files["extra.json"] = b"{}\n"
    elif fault == "coherent-csv":
        lines = files["summary.csv"].splitlines(keepends=True)
        fields = lines[1].decode().rstrip("\n").split(",")
        fields[9] = _digits(int(fields[9]) + 1)
        lines[1] = _csv_line(fields)
        files["summary.csv"] = b"".join(lines)
    elif fault == "coherent-certificate-witness":
        path = next(name for name in sorted(files) if name.startswith("certificates/"))
        certificate = _decode(files[path])
        certificate["U"] = [0, 1]
        files[path] = _json_bytes(certificate)
        for name in ("warmups.jsonl", "runs.jsonl"):
            rows = [_decode(line) for line in files[name].splitlines()]
            for row in rows:
                if row["certificate"]["path"] == path:
                    row["certificate"].update(bytes=len(files[path]), sha256=_sha(files[path]))
            files[name] = b"".join(_json_bytes(row) for row in rows)
    elif fault in ("marker-self-reference", "marker-wrong-count"):
        pass  # Alter the marker after the other-file ledger is rebound below.
    elif fault == "coherent-source":
        info = _decode(files["run-info.json"])
        info["source"]["sha256"] = "0" * 64
        files["run-info.json"] = _json_bytes(info)
    elif fault == "duplicate-decoded-key":
        files["run-info.json"] = files["run-info.json"].replace(
            b'{', b'{"campa\\u0069gn":"unit21-v1",', 1)
    else:
        name = "warmups.jsonl" if fault == "coherent-warmup-clock" else "runs.jsonl"
        rows = [_decode(line) for line in files[name].splitlines()]
        row = rows[0]
        if fault == "coherent-run-drop":
            rows.pop()
        elif fault == "coherent-run-reorder":
            rows[0], rows[1] = rows[1], rows[0]
        elif fault == "coherent-native-field":
            row["record"]["algorithm"]["native"]["branch_stats"][0]["invented"] = 0
        elif fault == "coherent-peak-sum":
            row["record"]["algorithm"]["total"]["peak_integer_bits"] += 1
        elif fault == "coherent-branch-drop":
            row["record"]["algorithm"]["branches"].pop()
        elif fault == "coherent-input-hash":
            row["input"]["sha256"] = "0" * 64
        elif fault == "coherent-certificate-ref":
            row["certificate"]["bytes"] += 1
        elif fault == "coherent-raw-integer-string":
            row["elapsed_ns"] = "1"
        else:
            row["elapsed_ns"] = 0
        files[name] = b"".join(_json_bytes(part) for part in rows)
    _rebind_ledger(files)
    if fault in ("marker-self-reference", "marker-wrong-count"):
        marker = _decode(files["COMPLETE.json"])
        if fault == "marker-self-reference":
            marker["files"].append({"path": "COMPLETE.json", "bytes": len(files["COMPLETE.json"]),
                                    "sha256": _sha(files["COMPLETE.json"])})
        else:
            marker["checked_certificates"] = 5239
        files["COMPLETE.json"] = _json_bytes(marker)
    with pytest.raises(AssertionError):
        _audit_output(files, scripted["bank"], scripted["source"],
                      scripted["inputs"], scripted["observed"])


@pytest.mark.parametrize("stage", ["open", "write", "flush", "close"])
def test_output_failure_never_publishes_complete(tmp_path, bank, stage):
    with _sandbox(tmp_path, bank) as session:
        sentinel = OSError("synthetic output failure")
        monitor = _OutputIO(session, stage=stage, exception=sentinel)
        monitor.install()
        if stage == "flush":
            # fd-only implementations have no stream.flush; fsync is their flush seam.
            def failed_fsync(fd):
                if monitor.paths.get(fd) == "runs.jsonl":
                    monitor.hits += 1
                    raise sentinel
                return monitor.fsync(fd)
            session.patches.setattr(os, "fsync", failed_fsync)
        try:
            result = session.invoke()
        except OSError as error:
            assert error is sentinel and monitor.hits >= 1
            if stage == "write":
                assert monitor.hits == 1
            _no_complete(session)
        else:
            # Raw descriptors have no buffered flush operation; do not mandate fsync/durability.
            assert stage == "flush" and monitor.hits == 0 and result == 0
            assert any(event == ("write", "runs.jsonl") for event in monitor.events)
            _check_success(session)


@pytest.mark.parametrize("value", [None, False, 0, -1, "too-large"])
def test_output_bad_normal_write_return_is_runtime_error(tmp_path, bank, value):
    with _sandbox(tmp_path, bank) as session:
        monitor = _OutputIO(session, stage="write", value=value)
        monitor.install()
        with pytest.raises(RuntimeError):
            session.invoke()
        assert monitor.hits >= 1
        _no_complete(session)


def test_positive_short_output_writes_are_completed(tmp_path, bank):
    with _sandbox(tmp_path, bank) as session:
        monitor = _OutputIO(session, stage="write", value="short")
        monitor.install()
        assert session.invoke() == 0
        assert monitor.hits > 3930
        _check_success(session)


def test_completed_historical_output_is_read_only_not_retimed(bank):
    root = _ROOT / "results/unit21-v1"
    if not root.exists():
        return  # Initial actual campaign is a separate, explicitly authorized Phase E action.
    names = [row["path"] for row in _decode(bank["SOURCE_FIXTURE.json"])["closed_entries"]]
    names.extend(("exactfrac/experiments.py", "experiments/reproduce.py"))
    assert {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_dir()} == {
        "certificates"}
    files = _snapshot(root)
    inputs = {"MANIFEST": (_ROOT / "instances/MANIFEST").read_bytes()}
    for row in _decode(bank["INPUT_EXPECTATIONS.json"]):
        inputs[row["input"]["path"]] = (_ROOT / "instances" / row["input"]["path"]).read_bytes()
    # Recorded aggregate provenance is historical, not an enduring current aggregate hash pin.
    info = _decode(files["run-info.json"])
    historical_inputs = dict(inputs)
    original_hash = info["inputs"]["manifest_sha256"]
    _require(re.fullmatch(r"[0-9a-f]{64}", original_hash) is not None,
             "historical-input-provenance")
    # Canonical data and diagnostics are audited without calling the producer main.
    current_source = {name: (_ROOT / name).read_bytes() for name in names}
    _audit_output(files, bank, current_source, historical_inputs, historical=True)
    assert files == _snapshot(root)


@pytest.mark.parametrize("fault", [
    "raw-attainment-repeat", "algorithm-repeat", "cross-route-value"])
def test_repeat_and_cross_route_consistency_is_not_assumed(tmp_path, bank, fault):
    with _sandbox(tmp_path, bank) as session:
        chosen = next(row for row in session.expectations
                      if row["recipe"] == "bits-bipartite-n04-b00008-qflat-funit")
        target = 2 if fault != "cross-route-value" else 8 * chosen["recipe_index"] + 1
        changed = []

        def corrupt(stage, current):
            if stage != "solve-return" or current.current["sequence"] != target or changed:
                return
            result, algorithm = current.returned[target]
            rid = current.current["recipe"]
            obj = current._data(rid)
            if fault == "algorithm-repeat":
                data = dataclasses.asdict(algorithm)
                data["nonbranch"]["peak_integer_bits"] = data["total"]["peak_integer_bits"] + 1
                data["total"]["peak_integer_bits"] = data["nonbranch"]["peak_integer_bits"]
                algorithm = _algorithm(current.modules, data)
            else:
                cert = ({"format": "exactfrac-certificate/1", "empty": False,
                         "N": 4, "D": 4, "U": [0, 2], "y": [[1, 1]]}
                        if fault == "raw-attainment-repeat" else
                        {"format": "exactfrac-certificate/1", "empty": False,
                         "N": 4, "D": 2, "U": [0], "y": [[0, 2]]})
                result = _result(current.modules, obj, cert)
                data = dataclasses.asdict(algorithm)
                data["output_numerator_bits"] = result.value.N.bit_length()
                data["output_denominator_bits"] = result.value.D.bit_length()
                algorithm = _algorithm(current.modules, data)
                instance = current.modules["instance"].Instance.from_dict(obj)
                raw = current.original_serialize(instance, current.original_build(instance, result))
                assert current.original_check(current.initial_input_images[
                    "unit20-v1/" + rid + ".json"], raw) is None
            current.bad_return = ("solve-return", (result, algorithm))
            changed.append(target)
        session.on_stage = corrupt
        with pytest.raises(RuntimeError):
            session.invoke()
        assert changed == [target]
        _no_complete(session)


@pytest.mark.parametrize("kind", ["absent-parent", "reverse-flags"])
def test_valid_external_output_and_optional_order(tmp_path, bank, kind):
    with _sandbox(tmp_path, bank) as session:
        session.output = tmp_path / "external/parents/new-run"
        args = (["--all", "--instances", str(session.inputs), "--output", str(session.output)]
                if kind == "reverse-flags" else
                ["--all", "--output", str(session.output), "--instances", str(session.inputs)])
        assert session.invoke(args) == 0
        _check_success(session)


@pytest.mark.parametrize("field,value", [("monotonic", False), ("monotonic", 1), ("adjustable", 0),
    ("resolution", 0.0), ("resolution", float("inf")), ("resolution", float("nan"))])
def test_invalid_clock_information_precludes_success(tmp_path, bank, field, value):
    with _sandbox(tmp_path, bank) as session:
        obj = SimpleNamespace(monotonic=True, adjustable=False, resolution=1e-9)
        setattr(obj, field, value)
        session.bad_return = ("clock-info", obj)
        with pytest.raises(RuntimeError):
            session.invoke()
        _no_complete(session)


_FRESH_WORKER = r'''
import importlib.util
import json
import os
from pathlib import Path
import sys
request = json.loads(sys.stdin.buffer.read())
root = Path(request["root"])
sys.path.insert(0, str(root))
spec = importlib.util.spec_from_file_location("unit21_frozen_test_consumer", request["test"])
consumer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(consumer)
bank = consumer._bank()
with consumer._sandbox(Path(request["scratch"]), bank) as session:
    session.giant = True
    assert session.invoke() == 0
    result = consumer._check_success(session)
    projection = b"".join(result["files"][name] for name in sorted(result["files"])
                          if name not in ("run-info.json", "COMPLETE.json"))
    info = consumer._decode(result["files"]["run-info.json"])
    assert info["environment"]["hash_seed"] == os.environ["PYTHONHASHSEED"]
    assert info["environment"]["int_max_str_digits"] == sys.get_int_max_str_digits()
    assert session.real_calls == 0
    print("EXACTFRAC_UNIT21_FRESH_PROCESS " + json.dumps({
        "result": "PASS", "seed": os.environ["PYTHONHASHSEED"],
        "limit": sys.get_int_max_str_digits(), "recursion_limit": sys.getrecursionlimit(),
        "source_sha256": consumer._source_identity(result["source"])["sha256"],
        "deterministic_projection_sha256": consumer._sha(projection),
        "scripted_calls": len(session.calls), "actual_solver_calls": session.real_calls,
        "giant_integer_digits": 4401,
    }, sort_keys=True))
'''


def test_fresh_process_limits_and_hash_seeds(tmp_path):
    results = []
    for limit in (640, 4300):
        for seed in (1, 73):
            scratch = tmp_path / f"limit{limit}-seed{seed}"
            scratch.mkdir()
            request = {"root": str(_ROOT), "test": str(Path(__file__).resolve()),
                       "scratch": str(scratch)}
            env = {"PATH": os.defpath, "PYTHONHASHSEED": str(seed), "PYTHONDONTWRITEBYTECODE": "1",
                   "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"}
            process = subprocess.run(
                [sys.executable, "-P", "-B", "-u", "-X", f"int_max_str_digits={limit}",
                 "-c", _FRESH_WORKER], input=_json_bytes(request), capture_output=True,
                cwd=scratch, env=env, check=False,
            )
            assert process.returncode == 0, process.stderr.decode("utf-8", errors="replace")
            assert process.stderr == b""
            prefix = b"EXACTFRAC_UNIT21_FRESH_PROCESS "
            records = [_decode(line[len(prefix):]) for line in process.stdout.splitlines()
                       if line.startswith(prefix)]
            assert len(records) == 1
            row = records[0]
            assert row["result"] == "PASS" and row["seed"] == str(seed) and row["limit"] == limit
            assert row["scripted_calls"] == 5240 and row["actual_solver_calls"] == 0
            results.append(row)
    assert len({row["deterministic_projection_sha256"] for row in results}) == 1
    assert len({row["source_sha256"] for row in results}) == 1
    print("EXACTFRAC_UNIT21_FRESH_PROCESSES " + json.dumps(results, sort_keys=True))


def test_scoped_fixture_and_source_identities_do_not_freeze_future_roots(scripted, bank):
    registry = _decode(bank["SOURCE_FIXTURE.json"])
    assert len(registry["closed_entries"]) == 20
    source = _source_identity(scripted["source"])
    assert len(source["entries"]) == 22
    assert all(row["path"].endswith(".py") for row in source["entries"])
    assert not any(row["path"].startswith(("results/", "docs/", "tests/"))
                   for row in source["entries"])
    declarations = _decode(bank["FAULT_DECLARATIONS.json"])
    assert len(declarations) == 42
    # These are prospective declarations, not assertions that a campaign or mutation audit ran.


def test_same_route_certificate_bytes_must_match_warmup(tmp_path, bank):
    with _sandbox(tmp_path, bank) as session:
        changed = []

        def corrupt(stage, current):
            if stage == "serialize" and current.current["sequence"] == 2 and not changed:
                obj = current._data(current.current["recipe"])
                instance = current.modules["instance"].Instance.from_dict(obj)
                cert = {"format": "exactfrac-certificate/1", "empty": False,
                        "N": 4, "D": 4, "U": [0, 2], "y": [[1, 1]]}
                raw = current.original_serialize(instance, cert)
                assert current.original_check(current.initial_input_images[
                    "unit20-v1/" + current.current["recipe"] + ".json"], raw) is None
                current.bad_return = ("serialize", raw)
                changed.append(2)
        session.on_stage = corrupt
        with pytest.raises(RuntimeError):
            session.invoke()
        assert changed == [2]
        _no_complete(session)


@pytest.mark.parametrize("stage", ["write", "flush", "close"])
def test_marker_io_failure_cannot_be_returned_as_success(tmp_path, bank, stage):
    with _sandbox(tmp_path, bank) as session:
        sentinel = OSError("synthetic COMPLETE publication failure")
        monitor = _OutputIO(session, stage=stage, exception=sentinel, target="COMPLETE.json")
        monitor.install()
        if stage == "flush":
            def fail_fsync(fd):
                if monitor.paths.get(fd) == "COMPLETE.json":
                    monitor.hits += 1
                    raise sentinel
                return monitor.fsync(fd)
            session.patches.setattr(os, "fsync", fail_fsync)
        try:
            result = session.invoke()
        except OSError as error:
            assert error is sentinel and monitor.hits >= 1
            assert len(session.calls) == len(session.checks) == 5240
            # A parseable marker may remain after flush/close failure.
            # It is NOT a successful invocation.
        else:
            assert stage == "flush" and monitor.hits == 0 and result == 0
            _check_success(session)  # unbuffered descriptors have no mandatory fsync operation


@pytest.mark.parametrize("fault", ["missing", "executable", "symlink"])
def test_source_member_filesystem_rejection_before_solve(tmp_path, bank, fault):
    with _sandbox(tmp_path, bank) as session:
        source = session.root / "exactfrac/witness.py"
        if fault == "missing":
            source.rename(tmp_path / "preserved-witness.py")
        elif fault == "executable":
            source.chmod(0o744)
        else:
            target = tmp_path / "preserved-witness.py"
            source.rename(target)
            source.symlink_to(target)
        expected = FileNotFoundError if fault == "missing" else ValueError
        with pytest.raises(expected):
            session.invoke()
        assert not session.calls and not session.output.exists()


def test_direct_script_fresh_process_help_and_usage_do_not_run_campaign(tmp_path):
    worker = r"""
import builtins
import importlib
import io
import json
import os
from pathlib import Path
import runpy
import sys
import time
import platform
request = json.loads(sys.stdin.buffer.read())
root = Path(request["root"])
sys.path.insert(0, str(root))
runner = importlib.import_module("exactfrac.experiments")
def blocked(*args, **kwargs):
    raise AssertionError("direct script attempted validation/discovery/campaign")
for name in ("recipe_ids", "build_corpus", "generate_instance"):
    corpus = importlib.import_module("exactfrac.corpus")
    old = getattr(corpus, name)
    setattr(corpus, name, blocked)
    for alias, value in list(vars(runner).items()):
        if value is old:
            setattr(runner, alias, blocked)
for module_name, name in (("exactfrac.telemetry", "solve_with_telemetry"),
                          ("exactfrac.solve", "solve")):
    module = importlib.import_module(module_name)
    old = getattr(module, name)
    setattr(module, name, blocked)
    for alias, value in list(vars(runner).items()):
        if value is old:
            setattr(runner, alias, blocked)
for name in ("python_version", "platform", "processor"):
    setattr(platform, name, blocked)
time.perf_counter_ns = blocked
time.get_clock_info = blocked
builtins.open = blocked
io.open = blocked
os.open = blocked
sys.argv[:] = [str(root / "experiments/reproduce.py"), *request["args"]]
old_path = list(sys.path)
try:
    runpy.run_path(str(root / "experiments/reproduce.py"), run_name="__main__")
finally:
    assert sys.path == old_path
"""
    names = [row["path"] for row in _decode(_bank()["SOURCE_FIXTURE.json"])["closed_entries"]]
    names += ["exactfrac/experiments.py", "experiments/reproduce.py"]
    original_source = {name: (_ROOT / name).read_bytes() for name in names}
    output = _ROOT / "results/unit21-v1"
    before = _snapshot(output) if output.exists() else None
    env = {"PATH": os.defpath, "PYTHONDONTWRITEBYTECODE": "1"}
    for args, expected in ((["--help"], 0), (["PRIVATE_MUST_NOT_ECHO"], 2)):
        process = subprocess.run(
            [sys.executable, "-I", "-B", "-u", "-c", worker],
            input=_json_bytes({"root": str(_ROOT), "args": args}),
            capture_output=True, cwd=tmp_path, env=env, check=False,
        )
        assert process.returncode == expected
        if expected == 0:
            assert b"--all" in process.stdout and not process.stderr
        else:
            assert process.stderr and not process.stdout
            assert b"PRIVATE_MUST_NOT_ECHO" not in process.stderr
    assert original_source == {name: (_ROOT / name).read_bytes() for name in names}
    assert before == (_snapshot(output) if output.exists() else None)
