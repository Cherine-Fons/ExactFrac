"""Serial, checked irregular follow-up under DESIGN D21B-I7--I16 and main R2.

This consumer does not optimize, enumerate shores, or infer oracle expectations.
It invokes the closed public telemetry solver once per registered position. A
pilot and a main invocation have distinct schedules, records, and result roots.
The human pilot review/F7 boundary belongs to the controlled invocation process,
not to a hidden CLI authorization mechanism.
"""

from __future__ import annotations

import contextlib
import dataclasses
import hashlib
import itertools
import json
import math
import os
import platform
import re
import stat
import sys
import time
from pathlib import Path as _Path

from exactfrac_verify.check import verify_certificate as _verify_certificate

from .branch import AcceleratedBranchStats as _AcceleratedBranchStats
from .branch import StandardBranchStats as _StandardBranchStats
from .certificate import build_certificate as _build_certificate
from .certificate import serialize_certificate as _serialize_certificate
from .corpus_irregular import build_corpus as _build_corpus
from .corpus_irregular import recipe_ids as _recipe_ids
from .instance import Instance as _Instance
from .oracle import BranchOracleStats as _BranchOracleStats
from .solve import SolveResult as _SolveResult
from .solve import SolveStats as _SolveStats
from .telemetry import AlgorithmStats as _AlgorithmStats
from .telemetry import BranchTelemetry as _BranchTelemetry
from .telemetry import RunMetadata as _RunMetadata
from .telemetry import RunRecord as _RunRecord
from .telemetry import WorkStats as _WorkStats
from .telemetry import solve_with_telemetry as _solve_with_telemetry
from .witness import ExactValue as _ExactValue
from .witness import Witness as _Witness

__all__ = ("main",)

_USAGE = (
    b"usage: reproduce_irregular.py --help | (--pilot | --all) "
    b"[--instances PATH] [--output PATH]\n"
)
_HELP = _USAGE + (
    b"ExactFrac irregular follow-up; fresh roots only; "
    b"pilot precedes the author-frozen campaign.\n"
)
_ROUTES = ("Standard", "Accelerated")
_SOURCE_PATHS = (
    "exactfrac/__init__.py", "exactfrac/_telemetry.py", "exactfrac/branch.py",
    "exactfrac/certificate.py", "exactfrac/cli.py", "exactfrac/corpus.py",
    "exactfrac/corpus_irregular.py", "exactfrac/experiments.py",
    "exactfrac/experiments_irregular.py", "exactfrac/families.py", "exactfrac/flow.py",
    "exactfrac/instance.py", "exactfrac/oracle.py", "exactfrac/parity_cut.py",
    "exactfrac/rational.py", "exactfrac/shore.py", "exactfrac/sign_routing.py",
    "exactfrac/solve.py", "exactfrac/telemetry.py", "exactfrac/witness.py",
    "exactfrac_verify/__init__.py", "exactfrac_verify/brute.py", "exactfrac_verify/check.py",
    "experiments/reproduce.py", "experiments/reproduce_irregular.py",
)
_WORK = (
    "outer_iterations", "oracle_calls", "newton_updates", "newton_queries",
    "newton_candidates", "lookahead_queries", "lookahead_accepted", "lookahead_rejected",
    "lookahead_terminal", "newton_terminal", "initialization_returns", "early_returns",
    "atomic_families_enumerated", "atomic_families_examined", "atomic_families_feasible",
    "parity_cut_calls", "ordinary_min_cut_calls", "max_flow_calls", "augmentations", "bfs_scans",
    "flow_peak_generated_value", "flow_peak_bits", "peak_numerator_bits", "peak_denominator_bits",
    "peak_integer_bits",
)
_NATIVE_TYPES = (
    _ExactValue, _Witness, _SolveResult, _SolveStats, _BranchOracleStats,
    _StandardBranchStats, _AcceleratedBranchStats, _WorkStats, _BranchTelemetry,
    _AlgorithmStats, _RunMetadata, _RunRecord,
)


def _require(ok, message, error=RuntimeError):
    if not ok:
        raise error(message)


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _bits(value):
    return max(1, abs(value).bit_length())


def _decimal(value):
    """Representation work only; no full-magnitude decimal conversion."""
    if value == 0:
        return b"0"
    negative = value < 0
    magnitude = abs(value)
    chunks = []
    while magnitude:
        magnitude, chunk = divmod(magnitude, 1_000_000_000)
        chunks.append(chunk)
    leading = str(chunks.pop()).encode("ascii")
    trailing = b"".join(f"{chunk:09d}".encode("ascii") for chunk in reversed(chunks))
    return (b"-" if negative else b"") + leading + trailing


def _json_bytes(value):
    """Canonical recursive ASCII serialization for run records, not certificates."""
    if value is None:
        return b"null"
    if type(value) is bool:
        return b"true" if value else b"false"
    if type(value) is int:
        return _decimal(value)
    if type(value) is float:
        _require(math.isfinite(value), "nonfinite environmental number")
        return json.dumps(value, allow_nan=False).encode("ascii")
    if type(value) is str:
        return json.dumps(value, ensure_ascii=True).encode("ascii")
    if type(value) in (list, tuple):
        return b"[" + b",".join(_json_bytes(item) for item in value) + b"]"
    _require(type(value) is dict, "invalid normal object for serialization")
    _require(all(type(key) is str for key in value), "invalid normal object keys")
    return b"{" + b",".join(
        _json_bytes(key) + b":" + _json_bytes(value[key]) for key in sorted(value)
    ) + b"}"


def _parse_int(token):
    if re.fullmatch(r"0|-?[1-9][0-9]*", token) is None:
        raise ValueError("noncanonical integer token")
    negative = token.startswith("-")
    digits = token[1:] if negative else token
    value = 0
    for offset in range(0, len(digits), 9):
        chunk = digits[offset:offset + 9]
        value = value * 10 ** len(chunk) + int(chunk)
    return -value if negative else value


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate decoded JSON key")
        value[key] = item
    return value


def _no_number(_token):
    raise ValueError("floating or nonfinite input number")


def _finite_number(token):
    number = float(token)
    if not math.isfinite(number):
        raise ValueError("nonfinite output number")
    return number


def _parse(raw, *, environmental=False):
    _require(type(raw) is bytes and not raw.startswith(b"\xef\xbb\xbf"),
             "input must be UTF-8 without a BOM", ValueError)
    try:
        return json.loads(
            raw.decode("utf-8"), parse_int=_parse_int,
            parse_float=_finite_number if environmental else _no_number,
            parse_constant=_no_number, object_pairs_hook=_unique_object,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("invalid single UTF-8 JSON document") from error


def _manifest(raw):
    document = _parse(raw)
    _require(type(document) is dict and set(document) == {"format", "entries"},
             "invalid aggregate object", ValueError)
    _require(document["format"] == "exactfrac-corpus-manifest/1"
             and type(document["format"]) is str and type(document["entries"]) is list,
             "invalid aggregate header", ValueError)
    last = ""
    for entry in document["entries"]:
        _require(type(entry) is dict
                 and set(entry) == {"suite", "recipe", "path", "bytes", "sha256"},
                 "invalid aggregate entry fields", ValueError)
        _require(all(type(entry[key]) is str for key in ("suite", "recipe", "path", "sha256")),
                 "invalid aggregate string types", ValueError)
        _require(re.fullmatch(r"unit[1-9][0-9]*-v[1-9][0-9]*", entry["suite"]) is not None,
                 "invalid suite identifier", ValueError)
        _require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["recipe"]) is not None,
                 "invalid recipe identifier", ValueError)
        _require(entry["path"] == entry["suite"] + "/" + entry["recipe"] + ".json",
                 "invalid aggregate path equation", ValueError)
        _require(entry["path"] > last, "aggregate paths are not strictly ordered", ValueError)
        last = entry["path"]
        _require(type(entry["bytes"]) is int and entry["bytes"] > 0,
                 "invalid payload byte count", ValueError)
        _require(re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) is not None,
                 "invalid payload hash", ValueError)
    return document["entries"]


def _lexical(path):
    path = _Path(path)
    _require(".." not in path.parts, "parent traversal is not supported", ValueError)
    return path.absolute()


def _parents(path, error=ValueError):
    for parent in reversed((path.parent, *path.parent.parents)):
        try:
            mode = parent.lstat().st_mode
        except FileNotFoundError:
            continue
        _require(stat.S_ISDIR(mode), "path parent is not a real directory", error)


def _directory(path, error=ValueError):
    _parents(path, error)
    _require(stat.S_ISDIR(path.lstat().st_mode), "path is not a real directory", error)


def _read(path, error=ValueError):
    _parents(path, error)
    mode = path.lstat().st_mode
    _require(stat.S_ISREG(mode) and not mode & 0o111,
             "file must be regular, nonexecutable and nonsymlink", error)
    with path.open("rb") as stream:
        return stream.read()


def _paths(root, input_arg, output_arg, mode):
    inputs = _lexical(root / "instances" if input_arg is None else input_arg)
    output = _lexical(
        root / "results" / ("unit21-v2-pilot" if mode == "pilot" else "unit21-v2")
        if output_arg is None else output_arg
    )
    _directory(root)
    _directory(inputs)
    _parents(output)
    _require(not os.path.lexists(output), "output leaf already exists", ValueError)
    _require(not (output == inputs or output in inputs.parents or inputs in output.parents),
             "output and inputs overlap", ValueError)
    _require(not (output == root or output in root.parents),
             "output contains the source tree", ValueError)
    if root in output.parents:
        _require(root / "results" in output.parents, "output is outside results", ValueError)
    return inputs, output


def _source_origins(root):
    origins = {}
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] not in ("exactfrac", "exactfrac_verify"):
            continue
        path = name.replace(".", "/")
        path += "/__init__.py" if name in ("exactfrac", "exactfrac_verify") else ".py"
        _require(path in _SOURCE_PATHS, "loaded project module is outside the source roster")
        expected = str(root / path)
        actual = getattr(module, "__file__", None)
        origin = getattr(getattr(module, "__spec__", None), "origin", None)
        _require(actual == expected and origin == expected,
                 "loaded project module has a conflicting origin")
        origins[name] = module
    return origins


def _source_snapshot(root):
    images = {name: _read(root / name, RuntimeError) for name in _SOURCE_PATHS}
    origins = _source_origins(root)
    entries = [{"path": name, "sha256": _sha(raw)} for name, raw in images.items()]
    fingerprint = b"exactfrac-unit21b-source/1\n" + b"".join(
        (item["path"] + "\0" + item["sha256"] + "\n").encode("ascii") for item in entries
    )
    digest = _sha(fingerprint)
    return images, origins, {
        "entries": entries, "sha256": digest, "code_version": "exactfrac-source-sha256:" + digest,
    }


def _generator_product():
    registry = _recipe_ids()
    _require(type(registry) is tuple and all(type(name) is str for name in registry),
             "generator registry has invalid normal types")
    expected = tuple(sorted(
        f"irregular-n{n:02d}-t{tau:03d}-b{b:05d}-f{capacity_mode}-{seed}"
        for n, tau, b, capacity_mode, seed in itertools.product(
            (6, 8, 12, 16), (64, 128), (1, 8, 64), ("alternating", "random"),
            tuple(f"p{i:02d}" for i in range(1, 6)) + tuple(f"s{i:02d}" for i in range(1, 21)),
        )
    ))
    _require(registry == expected, "generator registry contradicts the adopted inventory")
    product = _build_corpus()
    _require(type(product) is tuple and len(product) == len(registry) + 1,
             "generator product has invalid normal size/type")
    for record in product:
        _require(type(record) is tuple and len(record) == 2
                 and type(record[0]) is str and type(record[1]) is bytes,
                 "generator product has an invalid normal leaf")
    _require(tuple(record[0] for record in product) == (
        "MANIFEST", *("unit21-v2/" + name + ".json" for name in registry),
    ), "generator product paths contradict the registry")
    try:
        entries = _manifest(product[0][1])
    except ValueError as error:
        raise RuntimeError("generator returned a malformed normal manifest") from error
    payloads = dict(product[1:])
    expected_entries = [
        {"suite": "unit21-v2", "recipe": rid, "path": "unit21-v2/" + rid + ".json",
         "bytes": len(payloads["unit21-v2/" + rid + ".json"]),
         "sha256": _sha(payloads["unit21-v2/" + rid + ".json"])} for rid in registry
    ]
    _require(entries == expected_entries, "generator manifest contradicts its payloads")
    return registry, entries, payloads


def _load_inputs(inputs):
    manifest_raw = _read(inputs / "MANIFEST")
    entries = _manifest(manifest_raw)
    registry, expected_entries, expected = _generator_product()
    projection = [entry for entry in entries if entry["suite"] == "unit21-v2"]
    _require(projection == expected_entries, "owned manifest projection differs", ValueError)
    owned = inputs / "unit21-v2"
    _directory(owned)
    names = {path.name for path in owned.iterdir()}
    _require(names == {rid + ".json" for rid in registry}, "owned leaf inventory differs",
             ValueError)
    retained, objects = {}, {}
    for entry in projection:
        name = entry["path"]
        raw = _read(inputs / name)
        _require(len(raw) == entry["bytes"] and _sha(raw) == entry["sha256"]
                 and raw == expected[name], "owned input bytes differ", ValueError)
        retained[name] = raw
        objects[entry["recipe"]] = _parse(raw)
    return registry, projection, manifest_raw, retained, objects


def _discover():
    python_version = platform.python_version()
    system = platform.platform()
    processor = platform.processor()
    clock = time.get_clock_info("perf_counter")
    _require(type(python_version) is str and bool(python_version)
             and type(system) is str and bool(system) and type(processor) is str,
             "environment discovery violated its string promises")
    _require(type(clock.monotonic) is bool and type(clock.adjustable) is bool
             and type(clock.resolution) is float
             and math.isfinite(clock.resolution) and clock.resolution > 0,
             "clock information violated its normal promises")
    integer_limit = sys.get_int_max_str_digits()
    recursion_limit = sys.getrecursionlimit()
    seed = os.environ.get("PYTHONHASHSEED")
    _require(type(integer_limit) is int and integer_limit >= 0
             and type(recursion_limit) is int and recursion_limit > 0
             and (seed is None or type(seed) is str), "invalid observed environment")
    return {
        "python_version": python_version, "platform": system, "cpu": processor or None,
        "clock": {"name": "perf_counter_ns", "monotonic": clock.monotonic,
                  "adjustable": clock.adjustable, "resolution_s": clock.resolution},
        "int_max_str_digits": integer_limit, "recursion_limit": recursion_limit, "hash_seed": seed,
    }


def _protocol(mode):
    pilot = mode == "pilot"
    return {
        "routes": list(_ROUTES), "recipe_order": "ascii", "warmups": 0 if pilot else 1,
        "measured_repeats": 0 if pilot else 3,
        "route_order": ("standard-first-iff-recipe-index-even" if pilot else
                        "standard-first-iff-(recipe-index+round)-even"),
        "warmup_round": None if pilot else -1, "measured_rounds": [] if pilot else [0, 1, 2],
        "execution": "serial-single-process", "telemetry": True, "timeout_ns": None,
        "timing_interval": ("pilot-operational-solve-with-telemetry-return" if pilot else
                            "solve-with-telemetry-return"),
        "timing_excludes": ["input", "metadata", "certificates", "verification",
                            "serialization", "output"],
        "mode": "pilot" if pilot else "campaign",
        "pilot_cell_timing": ("first-instance-construction-through-last-row-flush"
                              if pilot else None),
    }


def _write_all(stream, raw):
    position = 0
    while position < len(raw):
        count = stream.write(raw[position:])
        _require(type(count) is int and 0 < count <= len(raw) - position,
                 "invalid normal binary write count")
        position += count
    _require(stream.flush() is None, "invalid normal binary flush return")


def _write_file(root, name, raw, expected):
    with (root / name).open("xb") as stream:
        _write_all(stream, raw)
    expected[name] = (len(raw), _sha(raw))


def _project(value):
    if type(value) in _NATIVE_TYPES:
        return {field.name: _project(getattr(value, field.name))
                for field in dataclasses.fields(type(value))}
    if type(value) is tuple:
        return [_project(item) for item in value]
    _require(value is None or type(value) in (str, bool, int, float),
             "invalid normal native projection type")
    return value


def _revalidate(value):
    """Reconstruct normal records, rejecting forged slots and subclass carriers.

    Only ValueError from this deliberate record-validation operation is
    translated. Exceptions from the actual solver, certificate APIs, checker,
    clock, filesystem and environment calls are not caught here.
    """
    selected = type(value)
    if selected in _NATIVE_TYPES:
        try:
            values = {field.name: _revalidate(getattr(value, field.name))
                      for field in dataclasses.fields(selected)}
        except AttributeError as error:
            raise RuntimeError("missing normal native field") from error
        try:
            return selected(**values)
        except ValueError as error:
            raise RuntimeError("contradictory normal native record") from error
    if selected is tuple:
        return tuple(_revalidate(item) for item in value)
    _require(value is None or selected in (int, str, bool, float),
             "invalid normal native record type")
    return value


def _response(response, route):
    _require(type(response) is tuple and len(response) == 2,
             "telemetry returned an invalid normal response")
    result, stats = response
    _require(type(result) is _SolveResult and type(stats) is _AlgorithmStats,
             "telemetry returned invalid normal record types")
    result_copy, stats_copy = _revalidate(result), _revalidate(stats)
    _require(stats.native.branch_solver == route, "normal response route differs")
    _require((stats.native.attaining_candidate == "Empty") == (result.witness is None),
             "normal Empty state differs")
    _require(stats.output_numerator_bits == _bits(result.value.N)
             and stats.output_denominator_bits == _bits(result.value.D),
             "normal output bit lengths differ")
    _require(result.value.N >= 0, "normal result numerator must be nonnegative")
    return result, stats, result_copy, stats_copy


def _geometry(instance):
    """Support-sized descriptor bookkeeping, not an optimization oracle."""
    n, edges, capacities = instance.n, instance.edges, instance.f
    degrees = [0] * n
    for left, right, q in edges:
        degrees[left] += q
        degrees[right] += q
    tplus = sum(1 << v for v in range(n) if (capacities[v] + degrees[v]) & 1)
    tf = sum(1 << v for v in range(n) if capacities[v] & 1)
    p = tuple(v for v in range(n) if degrees[v] > capacities[v])
    a = tuple(v for v in range(n) if capacities[v] >= 2)
    w = tuple(v for v in range(n) if capacities[v] == 1)
    counts = [[0, 0, 0] for _ in range(4)]

    def descriptor(branch, terminals, parity, inside, outside):
        counts[branch][0] += 1
        union = inside | outside
        if inside & outside:
            return
        if not terminals & ~union and (inside & terminals).bit_count() % 2 != parity:
            return
        size = 2 + n - union.bit_count()
        counts[branch][1] += 1
        counts[branch][2] += size * size - 3 * size + 3

    descriptor(0, tplus, 1, 0, 0)
    for vertex in p:
        for left, right, _q in edges:
            descriptor(1, tplus, 0, (1 << vertex) | (1 << left), 1 << right)
            descriptor(1, tplus, 0, (1 << vertex) | (1 << right), 1 << left)
    for vertex in a:
        descriptor(2, tf, 1, 1 << vertex, 0)
    for u, v, vertex in itertools.combinations(w, 3):
        descriptor(2, tf, 1, (1 << u) | (1 << v) | (1 << vertex), 0)
    for left, right, _q in edges:
        descriptor(3, tf, 0, 1 << left, 1 << right)
        descriptor(3, tf, 0, 1 << right, 1 << left)
    return tuple(tuple(row) for row in counts)


def _check_geometry(stats, geometry):
    for branch in stats.branches:
        r, feasible, backend = geometry[branch.branch]
        work = branch.work
        calls = work.oracle_calls
        _require(work.atomic_families_enumerated == r,
                 "descriptor enumeration disagrees with input geometry")
        _require(work.atomic_families_examined == calls * r,
                 "descriptor examination disagrees with input geometry")
        _require(work.atomic_families_feasible == work.parity_cut_calls == calls * feasible,
                 "feasibility disagrees with input geometry")
        _require(work.ordinary_min_cut_calls == work.max_flow_calls == calls * backend,
                 "ordinary cuts disagree with reduced-family geometry")
        _require(branch.feasible == bool(feasible), "branch feasibility disagrees with geometry")


def _input_metadata(rid, raw, obj):
    _tag, _n, tau, b, capacity, seed = rid.split("-")
    edges, f = obj["edges"], obj["f"]
    n_value, m = obj["n"], len(edges)
    support = b"exactfrac-unit21b-support/1\n" + _decimal(n_value) + b"\n" + b"".join(
        _decimal(u) + b"," + _decimal(v) + b"\n" for u, v, _q in edges
    )
    return {
        "suite": "unit21-v2", "path": "unit21-v2/" + rid + ".json",
        "bytes": len(raw), "sha256": _sha(raw), "n": n_value, "m": m,
        "Q_bits": _bits(sum(q for _u, _v, q in edges)),
        "max_q_bits": max(_bits(q) for _u, _v, q in edges),
        "max_f_bits": max(_bits(value) for value in f),
        "input_integer_bits_sum": _bits(n_value) + _bits(m)
        + sum(_bits(u) + _bits(v) + _bits(q) for u, v, q in edges)
        + sum(_bits(value) for value in f),
        "cell": rid.rsplit("-", 1)[0], "tau": int(tau[1:]), "b": int(b[1:]),
        "capacity_mode": capacity[1:], "seed": seed, "support_sha256": _sha(support),
    }


def _elapsed(start, end):
    _require(type(start) is int and type(end) is int and end >= start,
             "clock returned invalid readings or a negative interval")
    return end - start


def _same_structure(left, right):
    if type(left) is not type(right):
        return False
    if type(right) is dict:
        return set(left) == set(right) and all(
            _same_structure(left[key], right[key]) for key in right
        )
    if type(right) in (list, tuple):
        return len(left) == len(right) and all(
            _same_structure(a, b) for a, b in zip(left, right, strict=True)
        )
    return left == right


def _certificate(instance, result, raw_input):
    certificate = _build_certificate(instance, result)
    expected = {
        "format": "exactfrac-certificate/1", "empty": result.witness is None,
        "N": result.value.N, "D": result.value.D,
    }
    if result.witness is not None:
        witness = result.witness
        expected["U"] = [v for v in range(instance.n) if witness.U & (1 << v)]
        expected["y"] = [[ref, count] for ref, count in enumerate(witness.y) if count]
    _require(_same_structure(certificate, expected),
             "certificate builder returned a contradictory normal object")
    raw = _serialize_certificate(instance, certificate)
    expected_bytes = b"{" + b",".join(
        _json_bytes(key) + b":" + _json_bytes(value) for key, value in expected.items()
    ) + b"}\n"
    _require(type(raw) is bytes and raw == expected_bytes,
             "certificate serializer violated its exact normal byte promise")
    _require(_verify_certificate(raw_input, raw) is None,
             "independent checker returned a non-None normal response")
    return raw


def _csv_bytes(header, rows):
    def cell(value):
        if type(value) is bool:
            return b"true" if value else b"false"
        if type(value) is int:
            return _decimal(value)
        _require(type(value) is str and not any(c in value for c in ",\r\n\""),
                 "CSV value requires unsupported quoting")
        return value.encode("ascii")
    return b",".join(name.encode("ascii") for name in header) + b"\n" + b"".join(
        b",".join(cell(value) for value in row) + b"\n" for row in rows
    )


def _fraction(numerator, denominator):
    divisor = math.gcd(numerator, denominator)
    return {"N": numerator // divisor, "D": denominator // divisor}


def _median_pair(values):
    ordered = sorted(values)
    size = len(ordered)
    if size == 0:
        return None
    if size % 2:
        return {"N": ordered[size // 2], "D": 1}
    return _fraction(ordered[size // 2 - 1] + ordered[size // 2], 2)


def _findings(pairs, checked):
    cells = sorted({pair["cell"] for pair in pairs})
    active = [pair for pair in pairs if pair["lookahead"] > 0]
    active_cells = {pair["cell"] for pair in active}
    median = _median_pair([
        pair["accelerated_oracle_calls"] - pair["standard_oracle_calls"] for pair in active
    ])
    outcome = ("untestable" if not active else "supported"
               if len(active_cells) >= 18 and median["N"] < 0 else "not supported")
    calls, times = ({"accelerated": 0, "tie": 0, "standard": 0} for _ in range(2))
    fewer_not_faster, more_calls = [], []
    for pair in pairs:
        sc, ac = pair["standard_oracle_calls"], pair["accelerated_oracle_calls"]
        st, at = pair["standard_median_solve_ns"], pair["accelerated_median_solve_ns"]
        calls["accelerated" if ac < sc else "standard" if ac > sc else "tie"] += 1
        times["accelerated" if at < st else "standard" if at > st else "tie"] += 1
        if ac < sc and at >= st:
            fewer_not_faster.append(pair["recipe"])
        if ac > sc:
            more_calls.append(pair["recipe"])
    slowest = sorted(pairs, key=lambda p: (
        -max(p["standard_median_solve_ns"], p["accelerated_median_solve_ns"]), p["recipe"],
    ))[:10]
    largest = sorted(pairs, key=lambda p: (
        -max(p["standard_peak_integer_bits"], p["accelerated_peak_integer_bits"]), p["recipe"],
    ))[:10]
    return {
        "format": "exactfrac-irregular-findings/1", "campaign": "unit21-v2",
        "h5": {"outcome": outcome, "active_cells": len(active_cells), "total_cells": len(cells),
               "eligible_recipes": len(active), "paired_difference_median": median,
               "zero_event_cells": [cell for cell in cells if cell not in active_cells]},
        "oracle_call_wins": calls, "time_wins": times, "fewer_calls_not_faster": fewer_not_faster,
        "more_calls": more_calls,
        "slowest_ten": [{key: pair[key] for key in (
            "recipe", "standard_median_solve_ns", "accelerated_median_solve_ns",
        )} for pair in slowest],
        "largest_integer_ten": [{key: pair[key] for key in (
            "recipe", "standard_peak_integer_bits", "accelerated_peak_integer_bits",
        )} for pair in largest],
        "h2_checked_solves": checked,
    }


def _tables(mode, rows, cell_times):
    if mode == "pilot":
        header = (
            "cell", "recipe", "solver", "n", "m", "tau", "b", "capacity_mode", "seed",
            "max_q_bits", "solve_elapsed_ns", "oracle_calls", "lookahead_queries",
            "ordinary_min_cut_calls", "peak_integer_bits",
        )
        solves = []
        cells = {}
        for row in rows:
            inp, total = row["input"], row["record"]["algorithm"]["total"]
            solves.append([
                inp["cell"], row["recipe"], row["solver"], inp["n"], inp["m"], inp["tau"],
                inp["b"], inp["capacity_mode"], inp["seed"], inp["max_q_bits"], row["elapsed_ns"],
                *(total[key] for key in ("oracle_calls", "lookahead_queries",
                                        "ordinary_min_cut_calls", "peak_integer_bits")),
            ])
            cells.setdefault(inp["cell"], []).append(row)
        cell_rows = []
        for cell, records in sorted(cells.items()):
            inp = records[0]["input"]
            cell_rows.append([
                cell, inp["n"], inp["tau"], inp["b"], inp["capacity_mode"],
                len({row["recipe"] for row in records}), len(records), cell_times[cell],
            ])
        return {
            "pilot-solves.csv": _csv_bytes(header, solves),
            "pilot-cells.csv": _csv_bytes((
                "cell", "n", "tau", "b", "capacity_mode", "recipes", "solver_calls",
                "cell_elapsed_ns",
            ), cell_rows),
        }
    measured = {}
    for row in rows:
        if row["phase"] == "measured":
            measured.setdefault((row["recipe"], row["solver"]), []).append(row)
    recipes = sorted({key[0] for key in measured})
    summaries, branches, pairs = [], [], []
    joined = {}
    for rid in recipes:
        for route in _ROUTES:
            samples = measured[rid, route]
            _require(len(samples) == 3 and [row["repeat"] for row in samples] == [0, 1, 2],
                     "measured table group is incomplete")
            row = samples[0]
            inp, alg = row["input"], row["record"]["algorithm"]
            median = sorted(sample["elapsed_ns"] for sample in samples)[1]
            summaries.append([
                rid, route, *(inp[key] for key in (
                    "cell", "tau", "b", "capacity_mode", "seed", "support_sha256", "n", "m",
                    "Q_bits", "max_q_bits", "max_f_bits", "input_integer_bits_sum",
                )), 3, median, alg["native"]["attaining_candidate"],
                *(alg["total"][key] for key in _WORK),
                alg["output_numerator_bits"], alg["output_denominator_bits"],
            ])
            for branch in alg["branches"]:
                branches.append([
                    rid, route, branch["branch"], branch["feasible"],
                    *(branch["work"][key] for key in _WORK),
                ])
            joined[rid, route] = (median, alg["total"], inp)
        st, sw, inp = joined[rid, "Standard"]
        at, aw, _inp = joined[rid, "Accelerated"]
        pairs.append({
            "recipe": rid, "cell": inp["cell"], "standard_median_solve_ns": st,
            "accelerated_median_solve_ns": at,
            "standard_oracle_calls": sw["oracle_calls"],
            "accelerated_oracle_calls": aw["oracle_calls"],
            "standard_max_flow_calls": sw["max_flow_calls"],
            "accelerated_max_flow_calls": aw["max_flow_calls"],
            "standard_peak_integer_bits": sw["peak_integer_bits"],
            "accelerated_peak_integer_bits": aw["peak_integer_bits"],
            "lookahead": aw["lookahead_queries"],
        })
    comparison_header = (
        "recipe", "standard_median_solve_ns", "accelerated_median_solve_ns",
        "standard_oracle_calls", "accelerated_oracle_calls", "standard_max_flow_calls",
        "accelerated_max_flow_calls", "standard_peak_integer_bits", "accelerated_peak_integer_bits",
    )
    coverage = []
    for cell in sorted({pair["cell"] for pair in pairs}):
        selected = [pair for pair in pairs if pair["cell"] == cell]
        inp = joined[selected[0]["recipe"], "Standard"][2]
        count = sum(pair["lookahead"] > 0 for pair in selected)
        _require(len(selected) == 20, "coverage requires every main seed")
        coverage.append([
            cell, inp["n"], inp["tau"], inp["b"], inp["capacity_mode"], 20, count, count, 20,
        ])
    return {
        "summary.csv": _csv_bytes((
            "recipe", "solver", "cell", "tau", "b", "capacity_mode", "seed", "support_sha256",
            "n", "m", "Q_bits", "max_q_bits", "max_f_bits", "input_integer_bits_sum",
            "repeat_count", "median_solve_ns", "attaining_candidate", *_WORK,
            "output_numerator_bits", "output_denominator_bits",
        ), summaries),
        "branches.csv": _csv_bytes(("recipe", "solver", "branch", "feasible", *_WORK), branches),
        "comparison.csv": _csv_bytes(comparison_header, (
            [pair[key] for key in comparison_header] for pair in pairs
        )),
        "coverage.csv": _csv_bytes((
            "cell", "n", "tau", "b", "capacity_mode", "seeds", "active_seeds", "coverage_N",
            "coverage_D",
        ), coverage),
        "findings.json": _json_bytes(_findings(pairs, len(rows))) + b"\n",
    }


def _read_outputs(output, expected):
    observed = {}
    _directory(output, RuntimeError)
    for parent, directories, files in os.walk(output, followlinks=False):
        for name in directories:
            path = _Path(parent) / name
            _require(path == output / "certificates", "unexpected owned output directory")
            _directory(path, RuntimeError)
        for name in files:
            path = _Path(parent) / name
            relative = path.relative_to(output).as_posix()
            _require(relative in expected, "unexpected owned output file")
            raw = _read(path, RuntimeError)
            _require((len(raw), _sha(raw)) == expected[relative], "owned output bytes drifted")
            observed[relative] = raw
    _require(set(observed) == set(expected), "owned output inventory is incomplete")
    return observed


def _conserve(root, images, origins, inputs, manifest_raw, retained):
    _require(_source_origins(root) == origins, "loaded source-module identity drifted")
    for name, raw in images.items():
        _require(_read(root / name, RuntimeError) == raw, "source image drifted")
    _require(_read(inputs / "MANIFEST", RuntimeError) == manifest_raw, "aggregate input drifted")
    _directory(inputs / "unit21-v2", RuntimeError)
    _require({path.name for path in (inputs / "unit21-v2").iterdir()}
             == {name.split("/")[1] for name in retained}, "owned input inventory drifted")
    for name, raw in retained.items():
        _require(_read(inputs / name, RuntimeError) == raw, "owned input image drifted")


def _run(root, inputs, output, mode):
    images, origins, source = _source_snapshot(root)
    registry, _entries, manifest_raw, retained, objects = _load_inputs(inputs)
    selected = tuple(
        rid for rid in registry
        if rid.rsplit("-", 1)[1][0] == ("p" if mode == "pilot" else "s")
        and (mode == "pilot" or objects[rid]["n"] in (6, 8, 12))
    )
    environment = _discover()
    campaign = "unit21-v2-pilot" if mode == "pilot" else "unit21-v2"
    info = {
        "format": "exactfrac-experiment-info/1", "campaign": campaign, "protocol": _protocol(mode),
        "environment": environment, "source": source,
        "inputs": {"suite": "unit21-v2", "recipes": len(selected), "owned_recipes": len(registry),
                   "manifest_sha256": _sha(manifest_raw)},
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()
    (output / "certificates").mkdir()
    expected = {}
    _write_file(output, "run-info.json", _json_bytes(info) + b"\n", expected)
    log_names = ("pilot.jsonl",) if mode == "pilot" else ("warmups.jsonl", "runs.jsonl")
    hashes = {name: hashlib.sha256() for name in log_names}
    lengths = dict.fromkeys(log_names, 0)
    row_identities = {name: [] for name in log_names}
    cell_times = {}
    counts = {"pilot": 0, "warmup": 0, "measured": 0}
    with contextlib.ExitStack() as stack:
        logs = {name: stack.enter_context((output / name).open("xb")) for name in log_names}
        for index, rid in enumerate(selected):
            cell = rid.rsplit("-", 1)[0]
            if mode == "pilot" and index % 5 == 0:
                cell_start = time.perf_counter_ns()
                _require(type(cell_start) is int, "invalid pilot-cell starting clock")
            # No Instance or descriptor geometry is constructed before this cell's start.
            instance = _Instance.from_dict(objects[rid])
            _require(type(instance) is _Instance, "Instance constructor returned a non-Instance")
            geometry = _geometry(instance)
            raw_input = retained["unit21-v2/" + rid + ".json"]
            input_meta = _input_metadata(rid, raw_input, objects[rid])
            baseline = {}
            rounds = (0,) if mode == "pilot" else (-1, 0, 1, 2)
            for round_index in rounds:
                routes = _ROUTES if (index + round_index) % 2 == 0 else _ROUTES[::-1]
                phase = ("pilot" if mode == "pilot" else
                         "warmup" if round_index == -1 else "measured")
                values = {}
                for route in routes:
                    if phase == "warmup":
                        response = _solve_with_telemetry(instance, route)
                        elapsed = None
                    else:
                        start = time.perf_counter_ns()
                        response = _solve_with_telemetry(instance, route)
                        end = time.perf_counter_ns()
                        elapsed = _elapsed(start, end)
                    result, stats, result_copy, stats_copy = _response(response, route)
                    _check_geometry(stats, geometry)
                    certificate = _certificate(instance, result, raw_input)
                    if phase != "measured":
                        baseline[route] = (result_copy, stats_copy, certificate)
                    else:
                        _require(baseline[route] == (result_copy, stats_copy, certificate),
                                 "same-route repeat differs from its warmup")
                    values[route] = (result.value.N, result.value.D)
                    if len(values) == 2:
                        sn, sd = values["Standard"]
                        an, ad = values["Accelerated"]
                        _require(sd > 0 and ad > 0 and sn * ad == an * sd,
                                 "route quotients disagree")
                    wall_clock = None if elapsed is None else elapsed / 1_000_000_000
                    metadata = _RunMetadata(
                        wall_clock, environment["python_version"], environment["platform"],
                        environment["cpu"], source["code_version"], input_meta["sha256"],
                    )
                    record = _RunRecord(stats, metadata)
                    _require(type(record) is _RunRecord, "invalid normal RunRecord")
                    certificate_path = "certificates/" + rid + "." + route + ".json"
                    if phase != "measured":
                        _write_file(output, certificate_path, certificate, expected)
                    row = {
                        "format": "exactfrac-run/1", "campaign": campaign, "recipe": rid,
                        "solver": route, "phase": phase, "repeat": max(0, round_index),
                        "input": input_meta,
                        "certificate": {"path": certificate_path, "bytes": len(certificate),
                                        "sha256": _sha(certificate)},
                        "elapsed_ns": elapsed, "record": _project(record),
                    }
                    raw = _json_bytes(row) + b"\n"
                    name = ("pilot.jsonl" if mode == "pilot" else
                            "warmups.jsonl" if phase == "warmup" else "runs.jsonl")
                    _write_all(logs[name], raw)
                    hashes[name].update(raw)
                    lengths[name] += len(raw)
                    row_identities[name].append(_sha(raw))
                    counts[phase] += 1
            if mode == "pilot" and index % 5 == 4:
                cell_end = time.perf_counter_ns()
                cell_times[cell] = _elapsed(cell_start, cell_end)
    for name in log_names:
        expected[name] = lengths[name], hashes[name].hexdigest()
    files = _read_outputs(output, expected)
    rows = []
    for name in log_names:
        lines = files[name].splitlines(keepends=True)
        _require([_sha(line) for line in lines] == row_identities[name],
                 "saved row identities differ from checked call sequence")
        for line in lines:
            row = _parse(line, environmental=True)
            _require(_json_bytes(row) + b"\n" == line, "saved row is not canonical")
            certificate = row["certificate"]
            actual = files[certificate["path"]]
            _require((len(actual), _sha(actual))
                     == (certificate["bytes"], certificate["sha256"]),
                     "saved certificate does not match its checked row")
            rows.append(row)
    tables = _tables(mode, rows, cell_times)
    for name, raw in tables.items():
        _write_file(output, name, raw, expected)
    files = _read_outputs(output, expected)
    for name, raw in _tables(mode, rows, cell_times).items():
        _require(files[name] == raw, "saved table does not reconstruct from retained raw rows")
    _conserve(root, images, origins, inputs, manifest_raw, retained)
    expected_counts = ({"pilot": 480, "warmup": 0, "measured": 0} if mode == "pilot" else
                       {"pilot": 0, "warmup": 1440, "measured": 4320})
    _require(counts == expected_counts and sum(counts.values()) == len(rows),
             "actual checked call counts are incomplete")
    _require(len(files) == (484 if mode == "pilot" else 1448),
             "complete mode-specific output inventory differs")
    complete = {
        "format": "exactfrac-irregular-complete/1", "campaign": campaign,
        "source_sha256": source["sha256"], "recipes": len(selected),
        "warmup_solves": counts["warmup"], "measured_solves": counts["measured"],
        "pilot_solves": counts["pilot"], "checked_certificates": sum(counts.values()),
        "files": [{"path": name, "bytes": len(raw), "sha256": _sha(raw)}
                  for name, raw in sorted(files.items())],
    }
    _write_file(output, "COMPLETE.json", _json_bytes(complete) + b"\n", {})
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run exactly one full pilot or campaign; invalid Python types fail before I/O."""
    args = sys.argv[1:] if argv is None else argv
    if type(args) is not list or any(type(arg) is not str for arg in args):
        raise ValueError("argv must be an exact list of built-in strings or None")
    if args == ["--help"]:
        _write_all(sys.stdout.buffer, _HELP)
        return 0
    valid = bool(args) and args[0] in ("--pilot", "--all") and len(args) % 2 == 1
    options = {}
    if valid:
        for index in range(1, len(args), 2):
            flag, value = args[index:index + 2]
            if (flag not in ("--instances", "--output") or flag in options
                    or not value or value.startswith("-") or "\0" in value):
                valid = False
                break
            options[flag] = value
    if not valid:
        _write_all(sys.stderr.buffer, _USAGE)
        return 2
    mode = "pilot" if args[0] == "--pilot" else "main"
    root = _lexical(_Path(__file__).parent.parent)
    inputs, output = _paths(root, options.get("--instances"), options.get("--output"), mode)
    return _run(root, inputs, output, mode)
