"""The fixed Unit 21 campaign: measured solves, checked records and fresh output.

Timing measures instrumented solves, not certificates or output. Completion means
a successful return plus a validated ledger, not durable or atomic publication.
Mathematical decisions remain in the previously closed solver dependencies.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import re
import stat
import sys
import time
from contextlib import contextmanager
from dataclasses import asdict, fields
from pathlib import Path

from exactfrac.certificate import build_certificate, serialize_certificate
from exactfrac.corpus import build_corpus, recipe_ids
from exactfrac.instance import Instance
from exactfrac.solve import SolveResult
from exactfrac.telemetry import (
    AlgorithmStats,
    RunMetadata,
    RunRecord,
    WorkStats,
    solve_with_telemetry,
)
from exactfrac_verify.check import verify_certificate

__all__ = ("main",)

_ROUTES = ("Standard", "Accelerated")
_USAGE = b"usage: reproduce.py --help | --all [--instances PATH] [--output PATH]\n"
_SOURCE_PATHS = tuple(sorted((
    "exactfrac/__init__.py", "exactfrac/_telemetry.py", "exactfrac/branch.py",
    "exactfrac/certificate.py", "exactfrac/cli.py", "exactfrac/corpus.py",
    "exactfrac/experiments.py", "exactfrac/families.py", "exactfrac/flow.py",
    "exactfrac/instance.py", "exactfrac/oracle.py", "exactfrac/parity_cut.py",
    "exactfrac/rational.py", "exactfrac/shore.py", "exactfrac/sign_routing.py",
    "exactfrac/solve.py", "exactfrac/telemetry.py", "exactfrac/witness.py",
    "exactfrac_verify/__init__.py", "exactfrac_verify/brute.py",
    "exactfrac_verify/check.py", "experiments/reproduce.py",
)))
_WORK_FIELDS = (
    "outer_iterations", "oracle_calls", "newton_updates", "newton_queries",
    "newton_candidates", "lookahead_queries", "lookahead_accepted", "lookahead_rejected",
    "lookahead_terminal", "newton_terminal", "initialization_returns", "early_returns",
    "atomic_families_enumerated", "atomic_families_examined", "atomic_families_feasible",
    "parity_cut_calls", "ordinary_min_cut_calls", "max_flow_calls", "augmentations",
    "bfs_scans", "flow_peak_generated_value", "flow_peak_bits", "peak_numerator_bits",
    "peak_denominator_bits", "peak_integer_bits",
)
_INPUT_NUMBERS = ("n", "m", "Q_bits", "max_q_bits", "max_f_bits", "input_integer_bits_sum")
_SUMMARY_HEADER = (
    "recipe", "solver", *_INPUT_NUMBERS, "repeat_count", "median_solve_ns",
    "attaining_candidate", *_WORK_FIELDS, "output_numerator_bits", "output_denominator_bits",
)
_BRANCH_HEADER = ("recipe", "solver", "branch", "feasible", *_WORK_FIELDS)
_COMPARISON_HEADER = (
    "recipe", "standard_median_solve_ns", "accelerated_median_solve_ns",
    "standard_oracle_calls", "accelerated_oracle_calls", "standard_max_flow_calls",
    "accelerated_max_flow_calls", "standard_peak_integer_bits", "accelerated_peak_integer_bits",
)
_PROTOCOL = {
    "routes": list(_ROUTES), "recipe_order": "ascii", "warmups": 1, "measured_repeats": 3,
    "route_order": "standard-first-iff-(recipe-index+round)-even", "warmup_round": -1,
    "measured_rounds": [0, 1, 2], "execution": "serial-single-process", "telemetry": True,
    "timeout_ns": None, "timing_interval": "solve-with-telemetry-return",
    "timing_excludes": ["input", "metadata", "certificates", "verification",
                       "serialization", "output"],
}


def _need(ok, message, error=RuntimeError):
    if not ok:
        raise error(message)


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _bits(value):
    return max(1, abs(value).bit_length())


def _integer(value):
    """Serialize through bounded chunks; direct decimal conversions have at most nine digits."""
    if -1_000_000_000 < value < 1_000_000_000:
        return str(value).encode("ascii")
    negative = value < 0
    value = abs(value)
    chunks = []
    while value:
        value, remainder = divmod(value, 1_000_000_000)
        chunks.append(remainder)
    text = str(chunks[-1]) + "".join(f"{chunk:09d}" for chunk in reversed(chunks[:-1]))
    return (("-" if negative else "") + text).encode("ascii")


def _wire(value):
    """Canonical JSON, retaining ordinary integer tokens at every nesting level."""
    if value is None:
        return b"null"
    if type(value) is bool:
        return b"true" if value else b"false"
    if type(value) is int:
        return _integer(value)
    if type(value) is float:
        _need(math.isfinite(value), "nonfinite environmental number")
        return json.dumps(value, allow_nan=False).encode("ascii")
    if type(value) is str:
        return json.dumps(value, ensure_ascii=True).encode("ascii")
    if type(value) in (list, tuple):
        return b"[" + b",".join(_wire(item) for item in value) + b"]"
    _need(type(value) is dict and all(type(key) is str for key in value),
          "invalid record projection")
    return b"{" + b",".join(
        _wire(key) + b":" + _wire(value[key]) for key in sorted(value)
    ) + b"}"


def _json_bytes(value):
    return _wire(value) + b"\n"


def _decode(raw, *, error=ValueError, environmental=False):
    """Duplicate-aware JSON parsing without full-token large-integer conversion."""
    def integer(token):
        _need(re.fullmatch(r"0|-?[1-9][0-9]*", token) is not None,
              "invalid integer token", error)
        negative = token.startswith("-")
        digits = token[1:] if negative else token
        if len(digits) <= 9:
            return int(token)
        result = 0
        for start in range(0, len(digits), 9):
            chunk = digits[start:start + 9]
            result = result * 10 ** len(chunk) + int(chunk)
        return -result if negative else result

    def pairs(items):
        result = {}
        for key, value in items:
            _need(key not in result, "duplicate decoded object key", error)
            result[key] = value
        return result

    def invalid(_token):
        raise error("invalid numeric token")

    def floating(token):
        value = float(token)
        _need(math.isfinite(value), "nonfinite number", error)
        return value

    try:
        text = raw.decode("utf-8")
        return json.loads(text, parse_int=integer, object_pairs_hook=pairs,
                          parse_constant=invalid,
                          parse_float=floating if environmental else invalid)
    except (UnicodeError, json.JSONDecodeError):
        raise error("invalid JSON encoding or syntax") from None


def _directory(path, error=ValueError):
    for item in (path, *path.parents):
        _need(stat.S_ISDIR(item.lstat().st_mode), "non-directory or redirected path", error)


def _stamp(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)


def _read(path, error=ValueError):
    _directory(path.parent, error)
    before = path.lstat()
    _need(stat.S_ISREG(before.st_mode) and not before.st_mode & 0o111,
          "nonregular, redirected or executable input", error)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                         | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(descriptor, "rb") as stream:
        opened = os.fstat(stream.fileno())
        raw = stream.read()
        after = os.fstat(stream.fileno())
    _need(_stamp(before) == _stamp(opened) == _stamp(after) == _stamp(path.lstat()),
          "file changed while being read", error)
    return raw


def _absolute(text):
    path = Path(text)
    _need(".." not in path.parts, "parent traversal is not allowed", ValueError)
    return path if path.is_absolute() else Path.cwd() / path


def _output_path(path, root, inputs):
    _need(not path.is_relative_to(inputs) and not inputs.is_relative_to(path),
          "output overlaps input", ValueError)
    _need(not root.is_relative_to(path), "output contains source root", ValueError)
    if path.is_relative_to(root):
        _need(path.is_relative_to(root / "results") and path != root / "results",
              "in-source output must be a new results child", ValueError)
    _need(not os.path.lexists(path), "output already exists", ValueError)
    for parent in path.parents:
        if os.path.lexists(parent):
            _need(stat.S_ISDIR(parent.lstat().st_mode),
                  "output parent is not an unredirected directory", ValueError)


def _source(root):
    images = {name: _read(root / name) for name in _SOURCE_PATHS}
    entries = [{"path": name, "sha256": _sha(images[name])} for name in _SOURCE_PATHS]
    fingerprint = b"exactfrac-unit21-source/1\n" + b"".join(
        item["path"].encode("ascii") + b"\0" + item["sha256"].encode("ascii") + b"\n"
        for item in entries
    )
    digest = _sha(fingerprint)
    return images, {"entries": entries, "sha256": digest,
                    "code_version": "exactfrac-source-sha256:" + digest}


def _origins(root, images):
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] not in ("exactfrac", "exactfrac_verify"):
            continue
        relative = (name.replace(".", "/") + "/__init__.py"
                    if name in ("exactfrac", "exactfrac_verify")
                    else name.replace(".", "/") + ".py")
        _need(relative in images, "unregistered loaded project module")
        expected = str(root / relative)
        _need(getattr(module, "__file__", None) == expected,
              "loaded project file is outside the bound source")
        spec = getattr(module, "__spec__", None)
        _need(spec is not None and spec.origin == expected,
              "loaded project spec is outside the bound source")


def _manifest(raw, error=ValueError):
    obj = _decode(raw, error=error)
    _need(type(obj) is dict and set(obj) == {"format", "entries"}, "manifest schema", error)
    _need(obj["format"] == "exactfrac-corpus-manifest/1"
          and type(obj["entries"]) is list, "manifest format or entries", error)
    previous = ""
    identities = set()
    for row in obj["entries"]:
        _need(type(row) is dict and set(row) == {"suite", "recipe", "path", "bytes", "sha256"},
              "manifest entry schema", error)
        for key in ("suite", "recipe", "path", "sha256"):
            _need(type(row[key]) is str, "manifest string type", error)
        _need(re.fullmatch(r"unit[1-9][0-9]*-v[1-9][0-9]*", row["suite"]) is not None,
              "manifest suite identifier", error)
        _need(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", row["recipe"]) is not None,
              "manifest recipe identifier", error)
        _need(row["path"] == row["suite"] + "/" + row["recipe"] + ".json",
              "manifest path equation", error)
        _need(type(row["bytes"]) is int and row["bytes"] > 0, "manifest length type", error)
        _need(re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None,
              "manifest digest", error)
        key = (row["suite"], row["recipe"])
        _need(row["path"] > previous and key not in identities,
              "manifest order or duplicate identity", error)
        previous = row["path"]
        identities.add(key)
    return obj["entries"]


def _build():
    ids = recipe_ids()
    _need(type(ids) is tuple and len(ids) == 655
          and all(type(name) is str for name in ids), "closed recipe registry type/count")
    _need(ids == tuple(sorted(set(ids))) and all(
        re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) is not None for name in ids
    ), "closed recipe registry order/identities")
    records = build_corpus()
    _need(type(records) is tuple and len(records) == len(ids) + 1, "closed corpus return count")
    _need(all(type(row) is tuple and len(row) == 2
              and type(row[0]) is str and type(row[1]) is bytes for row in records),
          "closed corpus record types")
    names = ("MANIFEST", *("unit20-v1/" + name + ".json" for name in ids))
    _need(tuple(row[0] for row in records) == names, "closed corpus record order")
    payloads = dict(records)
    rows = _manifest(payloads["MANIFEST"], RuntimeError)
    expected = [dict(suite="unit20-v1", recipe=name, path=path,
                     bytes=len(payloads[path]), sha256=_sha(payloads[path]))
                for name, path in zip(ids, names[1:], strict=True)]
    _need(rows == expected, "closed corpus manifest consistency")
    return ids, payloads, expected


def _inputs(path):
    _directory(path)
    ids, built, expected = _build()
    raw = _read(path / "MANIFEST")
    rows = _manifest(raw)
    _need([row for row in rows if row["suite"] == "unit20-v1"] == expected,
          "owned manifest projection differs from closed corpus", ValueError)
    owned = path / "unit20-v1"
    _directory(owned)
    _need({p.name for p in owned.iterdir()} == {name + ".json" for name in ids},
          "owned input membership", ValueError)
    images = {"MANIFEST": raw}
    items = {}
    for row in expected:
        content = _read(path / row["path"])
        _need(content == built[row["path"]], "owned payload differs from closed corpus", ValueError)
        instance = Instance.from_dict(_decode(content))
        _need(type(instance) is Instance, "Instance.from_dict returned a non-Instance")
        images[row["path"]] = content
        metadata = {key: row[key] for key in ("suite", "path", "bytes", "sha256")}
        metadata.update(n=instance.n, m=instance.m, Q_bits=_bits(instance.Q),
                        max_q_bits=max(_bits(q) for _, _, q in instance.edges),
                        max_f_bits=max(_bits(f) for f in instance.f),
                        input_integer_bits_sum=_bits(instance.n) + _bits(instance.m)
                        + sum(_bits(x) for edge in instance.edges for x in edge)
                        + sum(_bits(f) for f in instance.f))
        items[row["recipe"]] = (instance, content, metadata)
    return ids, images, items


def _environment():
    version = platform.python_version()
    host_platform = platform.platform()
    cpu = platform.processor()
    clock = time.get_clock_info("perf_counter")
    _need(type(version) is str and bool(version) and type(host_platform) is str
          and bool(host_platform) and type(cpu) is str, "invalid environment discovery")
    _need(clock.monotonic is True and type(clock.adjustable) is bool
          and type(clock.resolution) is float and math.isfinite(clock.resolution)
          and clock.resolution > 0, "invalid monotone clock information")
    return {
        "python_version": version, "platform": host_platform, "cpu": cpu or None,
        "clock": {"name": "perf_counter_ns", "monotonic": clock.monotonic,
                  "adjustable": clock.adjustable, "resolution_s": clock.resolution},
        "int_max_str_digits": sys.get_int_max_str_digits(),
        "recursion_limit": sys.getrecursionlimit(), "hash_seed": os.environ.get("PYTHONHASHSEED"),
    }


def _write(stream, raw):
    position = 0
    while position < len(raw):
        count = stream.write(memoryview(raw)[position:])
        _need(type(count) is int and 0 < count <= len(raw) - position,
              "binary output write returned an invalid count")
        position += count


def _flush(stream):
    _need(stream.flush() is None, "binary output flush returned an invalid value")


@contextmanager
def _exclusive(path):
    _directory(path.parent, RuntimeError)
    stream = path.open("xb")
    try:
        yield stream
        _flush(stream)
    finally:
        _need(stream.close() is None, "binary output close returned an invalid value")


def _write_file(path, raw):
    with _exclusive(path) as stream:
        _write(stream, raw)


def _schedule(ids):
    for index, name in enumerate(ids):
        for round_id in (-1, 0, 1, 2):
            routes = _ROUTES if (index + round_id) % 2 == 0 else tuple(reversed(_ROUTES))
            for route in routes:
                yield name, route, "warmup" if round_id == -1 else "measured", max(0, round_id)


def _sample(instance, route, phase):
    if phase == "warmup":
        returned = solve_with_telemetry(instance, route)
        elapsed = None
    else:
        start = time.perf_counter_ns()
        _need(type(start) is int and start >= 0, "invalid start-clock return")
        returned = solve_with_telemetry(instance, route)
        end = time.perf_counter_ns()
        _need(type(end) is int and end >= start, "invalid end-clock return")
        elapsed = end - start
    _need(type(returned) is tuple and len(returned) == 2, "invalid telemetry return shape")
    result, algorithm = returned
    _need(type(result) is SolveResult and type(algorithm) is AlgorithmStats,
          "invalid telemetry result or diagnostics type")
    _need(algorithm.native.branch_solver == route, "telemetry route differs from request")
    _need((algorithm.native.attaining_candidate == "Empty") == (result.witness is None),
          "telemetry Empty status differs from result")
    _need((algorithm.output_numerator_bits, algorithm.output_denominator_bits)
          == (_bits(result.value.N), _bits(result.value.D)), "telemetry raw output widths differ")
    return result, algorithm, elapsed


def _certificate(instance, result, raw):
    certificate = build_certificate(instance, result)
    _need(type(certificate) is dict, "certificate builder returned a non-dictionary")
    _need(certificate.get("N") == result.value.N and certificate.get("D") == result.value.D
          and type(certificate.get("empty")) is bool
          and certificate["empty"] == (result.witness is None),
          "certificate builder contradicted the retained result")
    data = serialize_certificate(instance, certificate)
    _need(type(data) is bytes, "certificate serializer returned non-bytes")
    _need(verify_certificate(raw, data) is None, "checker violated its None return promise")
    return data


def _csv(values):
    return b",".join(
        b"true" if item is True else b"false" if item is False
        else _integer(item) if type(item) is int else item.encode("ascii")
        for item in values
    ) + b"\n"


def _reports(measured, ids):
    groups = {}
    for row in measured:
        key = (row["recipe"], row["solver"])
        groups.setdefault(key, []).append(row)
    _need(set(groups) == {(name, route) for name in ids for route in _ROUTES},
          "report recipe/route groups differ")
    summary, branches, comparison = [_csv(_SUMMARY_HEADER)], [_csv(_BRANCH_HEADER)], [
        _csv(_COMPARISON_HEADER)]
    medians = {}
    for name in ids:
        for route in _ROUTES:
            rows = groups[(name, route)]
            _need([row["repeat"] for row in rows] == [0, 1, 2],
                  "report measured repeats differ")
            first = rows[0]
            algorithm = first["record"]["algorithm"]
            _need(all(row["phase"] == "measured" and type(row["elapsed_ns"]) is int
                      and row["elapsed_ns"] >= 0 and row["input"] == first["input"]
                      and row["certificate"] == first["certificate"]
                      and row["record"]["algorithm"] == algorithm for row in rows),
                  "report repeated records disagree")
            median = sorted(row["elapsed_ns"] for row in rows)[1]
            medians[(name, route)] = median
            summary.append(_csv((
                name, route, *(first["input"][key] for key in _INPUT_NUMBERS), 3, median,
                algorithm["native"]["attaining_candidate"],
                *(algorithm["total"][key] for key in _WORK_FIELDS),
                algorithm["output_numerator_bits"], algorithm["output_denominator_bits"],
            )))
            for branch in algorithm["branches"]:
                branches.append(_csv((name, route, branch["branch"], branch["feasible"],
                                      *(branch["work"][key] for key in _WORK_FIELDS))))
        standard = groups[(name, "Standard")][0]["record"]["algorithm"]["total"]
        accelerated = groups[(name, "Accelerated")][0]["record"]["algorithm"]["total"]
        comparison.append(_csv((
            name, medians[(name, "Standard")], medians[(name, "Accelerated")],
            *(work[key] for key in ("oracle_calls", "max_flow_calls", "peak_integer_bits")
              for work in (standard, accelerated)),
        )))
    return {"summary.csv": b"".join(summary), "branches.csv": b"".join(branches),
            "comparison.csv": b"".join(comparison)}


def _raw_rows(path, expected):
    raw = _read(path, RuntimeError)
    _need(raw == b"".join(expected), "persisted raw records differ from observed records")
    rows = [_decode(line, error=RuntimeError, environmental=True)
            for line in raw.splitlines(keepends=True)]
    _need(len(rows) == len(expected), "persisted record count differs")
    return raw, rows


def _recheck(root, sources, inputs, input_images, output, artifacts):
    _origins(root, sources)
    for name, raw in sources.items():
        _need(_read(root / name, RuntimeError) == raw, "source changed during campaign")
    owned = inputs / "unit20-v1"
    _directory(owned, RuntimeError)
    _need({path.name for path in owned.iterdir()}
          == {Path(name).name for name in input_images if name != "MANIFEST"},
          "owned input membership changed during campaign")
    for name, raw in input_images.items():
        _need(_read(inputs / name, RuntimeError) == raw, "input changed during campaign")
    _directory(output, RuntimeError)
    _need({path.name for path in output.iterdir()}
          == {"certificates", *(name for name in artifacts if "/" not in name)},
          "output top-level membership differs")
    _directory(output / "certificates", RuntimeError)
    _need({path.name for path in (output / "certificates").iterdir()}
          == {name.split("/", 1)[1] for name in artifacts if name.startswith("certificates/")},
          "output certificate membership differs")
    for name, raw in artifacts.items():
        _need(_read(output / name, RuntimeError) == raw, "persisted output bytes differ")


def _campaign(root, inputs, output):
    _directory(root)
    _output_path(output, root, inputs)
    sources, source_identity = _source(root)
    _origins(root, sources)
    ids, input_images, items = _inputs(inputs)
    environment = _environment()
    _need(tuple(item.name for item in fields(WorkStats)) == _WORK_FIELDS,
          "closed work field registry differs")
    info = {
        "format": "exactfrac-experiment-info/1", "campaign": "unit21-v1",
        "protocol": _PROTOCOL, "environment": environment, "source": source_identity,
        "inputs": {"suite": "unit20-v1", "recipes": len(ids),
                   "manifest_sha256": _sha(input_images["MANIFEST"])},
    }
    # Existing parents are preserved; the output leaf is never reused.
    output.parent.mkdir(parents=True, exist_ok=True)
    _directory(output.parent)
    output.mkdir()
    (output / "certificates").mkdir()
    artifacts = {"run-info.json": _json_bytes(info)}
    _write_file(output / "run-info.json", artifacts["run-info.json"])
    observed, row_bytes = {}, {"warmup": [], "measured": []}
    checked = 0
    with _exclusive(output / "warmups.jsonl") as warmups, _exclusive(output / "runs.jsonl") as runs:
        for name, route, phase, repeat in _schedule(ids):
            instance, raw, input_metadata = items[name]
            result, algorithm, elapsed = _sample(instance, route, phase)
            certificate = _certificate(instance, result, raw)
            checked += 1
            key = (name, route)
            prior = observed.get(key)
            if prior is not None:
                _need((result, algorithm, certificate) == prior,
                      "same-route result, diagnostics or certificate changed on repetition")
            else:
                _need(phase == "warmup", "measured call preceded its warmup")
                observed[key] = (result, algorithm, certificate)
                other = observed.get((name, "Accelerated" if route == "Standard" else "Standard"))
                if other is not None:
                    a, b = result.value, other[0].value
                    _need(a.N * b.D == b.N * a.D, "solver routes disagree numerically")
            cert_path = f"certificates/{name}.{route}.json"
            if phase == "warmup":
                artifacts[cert_path] = certificate
                _write_file(output / cert_path, certificate)
            wall = None if elapsed is None else elapsed / 1_000_000_000
            _need(wall is None or math.isfinite(wall), "nonfinite elapsed seconds")
            record = RunRecord(algorithm, RunMetadata(
                wall, environment["python_version"], environment["platform"], environment["cpu"],
                source_identity["code_version"], input_metadata["sha256"],
            ))
            row = {
                "format": "exactfrac-run/1", "campaign": "unit21-v1", "recipe": name,
                "solver": route, "phase": phase, "repeat": repeat, "input": input_metadata,
                "certificate": {"path": cert_path, "bytes": len(certificate),
                                "sha256": _sha(certificate)},
                "elapsed_ns": elapsed, "record": asdict(record),
            }
            encoded = _json_bytes(row)
            _write(warmups if phase == "warmup" else runs, encoded)
            row_bytes[phase].append(encoded)
    # Reports use the persisted, validated measured records; no second solve pass.
    warm_raw, warm_rows = _raw_rows(output / "warmups.jsonl", row_bytes["warmup"])
    run_raw, measured = _raw_rows(output / "runs.jsonl", row_bytes["measured"])
    _need(len(observed) == 2 * len(ids) and len(warm_rows) == len(observed)
          and len(measured) == 3 * len(observed) and checked == len(warm_rows) + len(measured),
          "observed campaign counts are incomplete")
    artifacts.update({"warmups.jsonl": warm_raw, "runs.jsonl": run_raw})
    for name, raw in _reports(measured, ids).items():
        _write_file(output / name, raw)
        artifacts[name] = raw
    _recheck(root, sources, inputs, input_images, output, artifacts)
    complete = {
        "format": "exactfrac-experiment-complete/1", "campaign": "unit21-v1",
        "source_sha256": source_identity["sha256"], "recipes": len(items),
        "warmup_solves": len(warm_rows), "measured_solves": len(measured),
        "checked_certificates": checked,
        "files": [{"path": name, "bytes": len(raw), "sha256": _sha(raw)}
                  for name, raw in sorted(artifacts.items())],
    }
    _write_file(output / "COMPLETE.json", _json_bytes(complete))
    return 0


def main(argv: list[str] | None = None) -> int:
    """Execute the fixed --all campaign, or return pure help/usage."""
    if argv is None:
        argv = sys.argv[1:]
    if type(argv) is not list or any(type(token) is not str for token in argv):
        raise ValueError("argv must be a list of built-in strings or None")
    if argv == ["--help"]:
        stream = sys.stdout.buffer
        _write(stream, _USAGE)
        _flush(stream)
        return 0
    options = {}
    valid = bool(argv) and argv[0] == "--all" and len(argv) % 2 == 1
    if valid:
        for flag, operand in zip(argv[1::2], argv[2::2], strict=True):
            if (flag not in ("--instances", "--output") or flag in options or not operand
                    or operand.startswith("-") or "\0" in operand):
                valid = False
                break
            options[flag] = operand
    if not valid:
        stream = sys.stderr.buffer
        _write(stream, _USAGE)
        _flush(stream)
        return 2
    root = Path(__file__).absolute().parents[1]
    inputs = _absolute(options["--instances"]) if "--instances" in options else root / "instances"
    output = _absolute(options["--output"]) if "--output" in options else root / "results/unit21-v1"
    return _campaign(root, inputs, output)
