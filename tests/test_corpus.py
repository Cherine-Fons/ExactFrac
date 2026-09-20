"""Unit 20: independent recipe, byte, mathematical and owning-scope obligations.

DESIGN D20-C1--C10 and TEST_PLAN CP1--CP18 govern. Named Phase C tables,
not a production checksum, supply expectations. This file imports the missing
production module before reading any catalogue or future corpus path: Phase D
must be a missing-module collection RED. Generator mutation executions belong
to the separate Phase E audit; temporary consumer faults below are not labelled
production mutants. No enduring hash pin covers the evolving root MANIFEST,
README, other suites, experiments, results or future release artifacts.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import inspect
import itertools
import json
import math
import os
import re
import stat
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import get_type_hints

import exactfrac.corpus as corpus

# Keep the required missing-module import ahead of other project imports in RED and GREEN.
# isort: split
import pytest

from exactfrac.certificate import build_certificate, serialize_certificate
from exactfrac.instance import Instance
from exactfrac.solve import solve
from exactfrac_verify.check import verify_certificate

_ROOT = Path(__file__).resolve().parents[1]
_SUITE = "unit20-v1"
_COLUMNS = (
    "recipe", "path", "n", "bits", "m", "bytes", "sha256", "Q", "d", "f",
    "empty", "N", "D", "mask", "Y",
)
_FAMILIES = ("path", "cycle", "complete", "bipartite", "matching")
# Historical reproduction product ONLY: never compared to the evolving on-disk MANIFEST.
_INITIAL_SIZE = 126935
_INITIAL_SHA = "866541ba2ab7a4d5f2a1e6a4cb0a24da769392e8bb8747a8fe1997a8bb8640d8"
_INVENTORY_SHA = "86693898debcbd171e22eb7bcb2b8647ae76e5dad874acd70cdf2dfd40a5e439"


class _GuardError(AssertionError):
    """Named independent-consumer guard, not a production public error class."""


def _require(ok, guard):
    if not ok:
        raise _GuardError(guard)


def _table(catalogue, name):
    heading = "### Fixture table: " + name + "\n\n"
    _require(catalogue.count(heading) == 1, "unique-table:" + name)
    lines = catalogue.split(heading, 1)[1].splitlines()
    _require(lines[0].startswith("| ") and lines[1].startswith("| ---"), "table-header")
    rows = []
    for line in lines[2:]:
        if not line.startswith("| "):
            break
        cells = line[2:-2].split(" | ")
        _require(all(c.startswith("`") and c.endswith("`") for c in cells), "literal-cell")
        rows.append(tuple(ast.literal_eval(c[1:-1]) for c in cells))
    return tuple(rows)


def _registry():
    """Independent grid, not production membership and not payload deduplication."""
    ids = []
    for q in range(1, 6):
        for a, b in itertools.product(range(1, q + 1), repeat=2):
            ids.append(f"edge-q{q:02d}-f{a:02d}-{b:02d}")
    for a, b, c in itertools.product(range(3), repeat=3):
        ds = (a + b, a + c, b + c)
        for x, y, z in itertools.product(*(range(1, d + 1) for d in ds)):
            ids.append(f"tri-q{a}-{b}-{c}-f{x}-{y}-{z}")
    for family, n, bits, fm in itertools.product(
        _FAMILIES, (4, 6, 8), (1, 8), ("unit", "half", "near", "degree"),
    ):
        ids.append(f"struct-{family}-n{n:02d}-b{bits:05d}-f{fm}")
    for family, bits, qm, fm in itertools.product(
        _FAMILIES, (1, 8, 64, 256, 4096, 16384), ("flat", "ramp"), ("unit", "degree"),
    ):
        ids.append(f"bits-{family}-n04-b{bits:05d}-q{qm}-f{fm}")
    for n, bits, fm, seed in itertools.product(
        (4, 6, 8), (1, 8, 64), ("half", "alternating"), (1, 73),
    ):
        ids.append(f"seeded-n{n:02d}-b{bits:05d}-f{fm}-s{seed:02d}")
    result = tuple(sorted(ids))
    _require(len(result) == len(set(result)) == 655, "reference-registry")
    _require(
        Counter(r.split("-", 1)[0] for r in result)
        == {"edge": 55, "tri": 324, "struct": 120, "bits": 120, "seeded": 36},
        "reference-strata",
    )
    return result


def _plain(rid, seed_hash=None):
    """Pair predicates and bounded literal ID fields; independent of generator."""
    if rid.startswith("edge-"):
        match = re.fullmatch(r"edge-q([0-9]+)-f([0-9]+)-([0-9]+)", rid)
        q, a, b = map(int, match.groups())
        return {"format": "exactfrac-instance/1", "n": 2, "edges": [[0, 1, q]], "f": [a, b]}
    if rid.startswith("tri-"):
        match = re.fullmatch(r"tri-q([0-9]+)-([0-9]+)-([0-9]+)-f([0-9]+)-([0-9]+)-([0-9]+)", rid)
        a, b, c, x, y, z = map(int, match.groups())
        edges = [e for e in ([0, 1, a], [0, 2, b], [1, 2, c]) if e[2]]
        return {"format": "exactfrac-instance/1", "n": 3, "edges": edges, "f": [x, y, z]}
    parts = rid.split("-")
    if parts[0] == "seeded":
        family, n, bits = "seeded", int(parts[1][1:]), int(parts[2][1:])
        fm, seed, qm = parts[3][1:], int(parts[4][1:]), "ramp"
    else:
        family, n, bits = parts[1], int(parts[2][1:]), int(parts[3][1:])
        fm, seed = parts[-1][1:], 0
        qm = parts[4][1:] if parts[0] == "bits" else "flat"
    pairs = []
    for u, v in itertools.combinations(range(n), 2):
        adjacent = v == u + 1
        backbone = adjacent or (u == 0 and v == n - 1)
        take = (
            family == "complete"
            or (family == "path" and adjacent)
            or (family == "cycle" and backbone)
            or (family == "matching" and adjacent and u % 2 == 0)
            or (family == "bipartite" and u < n // 2 <= v)
        )
        if family == "seeded":
            message = f"exactfrac-u20-seeded/1\n{seed}\n{n}\n{u}\n{v}\n".encode("ascii")
            digest = hashlib.sha256(message).digest() if seed_hash is None else seed_hash(message)
            take = backbone or digest[0] < 64
        if take:
            pairs.append((u, v))
    half = 1 << (bits - 1)
    edges = [
        [u, v, (1 << bits) - 1 if qm == "flat" else half + (j + seed) % half]
        for j, (u, v) in enumerate(pairs)
    ]
    ds = [sum(q for u, v, q in edges if vertex in (u, v)) for vertex in range(n)]
    fs = []
    for vertex, degree in enumerate(ds):
        if fm == "unit":
            f = 1
        elif fm == "half":
            f = degree // 2 + degree % 2
        elif fm == "near":
            f = max(1, degree - 1)
        elif fm == "alternating":
            f = degree if vertex % 2 else 1
        else:
            _require(fm == "degree", "reference-fmode")
            f = degree
        fs.append(f)
    return {"format": "exactfrac-instance/1", "n": n, "edges": edges, "f": fs}


def _decimal3(value):
    _require(type(value) is int and value >= 0, "reference-integer")
    chunks = []
    while value:
        value, remainder = divmod(value, 1000)
        chunks.append(str(remainder).rjust(3, "0"))
    return "".join(reversed(chunks)).lstrip("0") or "0"


def _encode(value):
    if type(value) is int:
        return _decimal3(value)
    if type(value) is str:
        return json.dumps(value, ensure_ascii=True)
    if type(value) is list:
        return "[" + ",".join(_encode(v) for v in value) + "]"
    if type(value) is dict:
        return "{" + ",".join(_encode(k) + ":" + _encode(v) for k, v in value.items()) + "}"
    raise _GuardError("reference-encoding-type")


def _parse_integer(token):
    _require(re.fullmatch(r"0|[1-9][0-9]*", token) is not None, "integer-token")
    total = 0
    for start in range(0, len(token), 6):
        chunk = token[start:start + 6]
        total = total * 10 ** len(chunk) + int(chunk)
    return total


def _forbid_number(_token):
    raise _GuardError("number-kind")


def _pairs(items):
    result = {}
    for key, value in items:
        _require(key not in result, "duplicate-key")
        result[key] = value
    return result


def _json(raw):
    _require(type(raw) is bytes, "json-bytes")
    try:
        return json.loads(
            raw.decode("ascii"), object_pairs_hook=_pairs, parse_int=_parse_integer,
            parse_float=_forbid_number, parse_constant=_forbid_number,
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise _GuardError("json-syntax") from exc


def _active(obj):
    _require(type(obj) is dict and list(obj) == ["format", "n", "edges", "f"], "instance-keys")
    _require(obj["format"] == "exactfrac-instance/1", "instance-format")
    n, edges, fs = obj["n"], obj["edges"], obj["f"]
    _require(type(n) is int and n > 0, "instance-n")
    _require(type(edges) is list and bool(edges), "instance-edges")
    _require(type(fs) is list and len(fs) == n, "instance-f")
    ds, last = [0] * n, (-1, -1)
    for edge in edges:
        _require(type(edge) is list and len(edge) == 3, "edge-shape")
        _require(all(type(x) is int for x in edge), "edge-integers")
        u, v, q = edge
        _require(0 <= u < v < n and q > 0 and (u, v) > last, "edge-order-values")
        ds[u] += q
        ds[v] += q
        last = u, v
    _require(all(type(f) is int and 1 <= f <= d for f, d in zip(fs, ds, strict=True)), "active")
    return ds


def _decode_payload(raw):
    obj = _json(raw)
    _active(obj)
    _require((_encode(obj) + "\n").encode("ascii") == raw, "payload-canonical-bytes")
    return obj


def _expression(text, bits):
    if re.fullmatch(r"0|[1-9][0-9]*", text):
        _require(len(text) <= 9, "bounded-literal")
        return int(text)
    match = re.fullmatch(r"(?:(0|[1-9][0-9]*)\*)?T([+-][1-9][0-9]*)?", text)
    _require(match is not None and bits >= 64, "oracle-expression")
    coefficient = int(match[1]) if match[1] else 1
    constant = int(match[2]) if match[2] else 0
    _require(0 < coefficient < 10**9 and abs(constant) < 10**9, "bounded-expression")
    return coefficient * 2 ** (bits - 2) + constant


def _expected_manifest(rows):
    # Independent field assembly, not the production encoder or its emitted hashes.
    entries = [
        '{"suite":"unit20-v1","recipe":"' + r["recipe"] + '","path":"' + r["path"]
        + '","bytes":' + str(r["bytes"]) + ',"sha256":"' + r["sha256"] + '"}'
        for r in rows
    ]
    return ('{"format":"exactfrac-corpus-manifest/1","entries":['
            + ",".join(entries) + "]}\n").encode("ascii")


def _references():
    catalogue = (_ROOT / "docs/ORACLE_CATALOG.md").read_text(encoding="utf-8")
    table = _table(catalogue, "U20_RECIPES")
    _require(all(len(row) == len(_COLUMNS) for row in table), "recipe-table-width")
    rows = [dict(zip(_COLUMNS, row, strict=True)) for row in table]
    _require(tuple(r["recipe"] for r in rows) == _registry(), "declared-registry")
    objects, payloads = {}, {}
    for row in rows:
        rid = row["recipe"]
        obj = _plain(rid)
        degrees = _active(obj)
        raw = (_encode(obj) + "\n").encode("ascii")
        _require(_decode_payload(raw) == obj, "independent-codec-roundtrip")
        _require(row["path"] == _SUITE + "/" + rid + ".json", "declared-path")
        _require(len(raw) == row["bytes"], "declared-length")
        _require(hashlib.sha256(raw).hexdigest() == row["sha256"], "declared-sha256")
        _require((row["n"], row["m"]) == (obj["n"], len(obj["edges"])), "declared-n-m")
        def read(text, bits=row["bits"]):
            return _expression(text, bits)

        _require(read(row["Q"]) == sum(e[2] for e in obj["edges"]), "declared-Q")
        _require(tuple(map(read, row["d"])) == tuple(degrees), "declared-degrees")
        _require(tuple(map(read, row["f"])) == tuple(obj["f"]), "declared-capacities")
        if row["bits"]:
            _require({e[2].bit_length() for e in obj["edges"]} == {row["bits"]}, "q-width")
        objects[rid], payloads[rid] = obj, raw
    manifest = _expected_manifest(rows)
    _require(len(manifest) == _INITIAL_SIZE, "historical-initial-size")
    _require(hashlib.sha256(manifest).hexdigest() == _INITIAL_SHA, "historical-initial-sha256")
    inventory = "".join(
        r["path"] + "\t" + str(r["bytes"]) + "\t" + r["sha256"] + "\n" for r in rows
    ).encode("ascii")
    _require(hashlib.sha256(inventory).hexdigest() == _INVENTORY_SHA, "scope-fingerprint")
    _require(len(set(payloads.values())) == 599, "equal-payloads-retained")
    return rows, objects, payloads, manifest


@pytest.fixture(scope="module")
def reference():
    return _references()


def _equivalent(first, second):
    if first is None or second is None:
        return first is None and second is None
    return first[1] > 0 and second[1] > 0 and first[0] * second[1] == second[0] * first[1]


def _better(pair, old):
    return old is None or pair[0] * old[1] > old[0] * pair[1]


def _shore_data(obj, mask):
    s = sum(f for v, f in enumerate(obj["f"]) if mask >> v & 1)
    internal = sum(q for u, v, q in obj["edges"] if mask >> u & 1 and mask >> v & 1)
    boundary = [(j, q) for j, (u, v, q) in enumerate(obj["edges"])
                if (mask >> u & 1) != (mask >> v & 1)]
    return s, internal, boundary


def _endpoints(obj):
    best, locals_, counts = None, {}, Counter()
    for mask in range(1, 1 << obj["n"]):
        s, internal, boundary = _shore_data(obj, mask)
        maximum = sum(q for _, q in boundary)
        low = max(0, 3 - s)
        low += (s + low + 1) % 2
        high = maximum - (s + maximum + 1) % 2
        counts["shores"] += 1
        local = None
        if low <= high:
            counts["feasible_shores"] += 1
            for total in ((low,) if low == high else (low, high)):
                pair = 2 * (internal + total), s + total - 1
                _require(pair[1] > 0 and (s + total) % 2 == 1, "endpoint-admissible")
                counts["endpoint_evaluations"] += 1
                if _better(pair, local):
                    local = pair
                if _better(pair, best):
                    best = pair
        else:
            counts["infeasible_shores"] += 1
        locals_[mask] = local
    return best, locals_, counts


def _micro_models(obj, locals_):
    _require(sum(e[2] for e in obj["edges"]) <= 6, "bounded-copy-control")
    counts = Counter(inputs=1)
    for mask, endpoint in locals_.items():
        s, internal, boundary = _shore_data(obj, mask)
        compact, scalar, expanded = set(), set(), set()
        vector_counts, actual_counts = {}, Counter()
        values = [None, None, None]
        for vector in itertools.product(*(range(q + 1) for _, q in boundary)):
            counts["compact_vectors_examined"] += 1
            total = sum(vector)
            if s + total >= 3 and (s + total) % 2:
                counts["compact_admissible"] += 1
                compact.add(total)
                vector_counts[vector] = math.prod(
                    math.comb(q, y) for (_, q), y in zip(boundary, vector, strict=True)
                )
                pair = 2 * (internal + total), s + total - 1
                if _better(pair, values[0]):
                    values[0] = pair
        for total in range(sum(q for _, q in boundary) + 1):
            counts["scalar_totals_examined"] += 1
            if s + total >= 3 and (s + total) % 2:
                counts["scalar_admissible"] += 1
                scalar.add(total)
                pair = 2 * (internal + total), s + total - 1
                if _better(pair, values[1]):
                    values[1] = pair
        copies = [(j, k) for j, (_, q) in enumerate(boundary) for k in range(q)]
        for flags in itertools.product((0, 1), repeat=len(copies)):
            counts["expanded_subsets_examined"] += 1
            total = sum(flags)
            if s + total >= 3 and (s + total) % 2:
                counts["expanded_admissible"] += 1
                expanded.add(total)
                vector = tuple(
                    sum(flag for (edge, _), flag in zip(copies, flags, strict=True) if edge == j)
                    for j in range(len(boundary))
                )
                actual_counts[vector] += 1
                pair = 2 * (internal + total), s + total - 1
                if _better(pair, values[2]):
                    values[2] = pair
        _require(compact == scalar == expanded, "three-attainable-total-sets")
        _require(dict(actual_counts) == vector_counts, "binomial-copy-multiplicity")
        _require(all(_equivalent(value, endpoint) for value in values), "three-shore-optima")
        counts["shores_compared"] += 1
    return counts


def _parse_manifest(raw):
    obj = _json(raw)
    _require(type(obj) is dict and set(obj) == {"format", "entries"}, "manifest-root")
    _require(obj["format"] == "exactfrac-corpus-manifest/1", "manifest-format")
    entries = obj["entries"]
    _require(type(entries) is list, "manifest-entries")
    previous, identities = "", set()
    for entry in entries:
        _require(type(entry) is dict and set(entry) == {
            "suite", "recipe", "path", "bytes", "sha256",
        }, "entry-fields")
        suite, recipe, path = entry["suite"], entry["recipe"], entry["path"]
        _require(all(type(x) is str for x in (suite, recipe, path, entry["sha256"])), "entry-str")
        _require(re.fullmatch(r"unit[1-9][0-9]*-v[1-9][0-9]*", suite) is not None, "suite-grammar")
        _require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", recipe) is not None, "recipe-grammar")
        _require(path == suite + "/" + recipe + ".json", "path-equation")
        _require(type(entry["bytes"]) is int and entry["bytes"] > 0, "byte-count")
        _require(re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) is not None, "digest-grammar")
        _require(path > previous and (suite, recipe) not in identities, "entry-order-identity")
        previous = path
        identities.add((suite, recipe))
    return entries


def _directory(path):
    for parent in (path, *path.parents):
        _require(stat.S_ISDIR(parent.lstat().st_mode), "directory-redirection")


def _regular(path):
    _directory(path.parent)
    mode = path.lstat().st_mode
    _require(stat.S_ISREG(mode) and not mode & 0o111, "file-kind")
    return path.read_bytes()


def _owning_scope(root, rows, payloads):
    """Read-only consumer of an evolving aggregate; checks only owned data semantics."""
    _directory(root)
    manifest_before = _regular(root / "MANIFEST")
    entries = _parse_manifest(manifest_before)
    actual = [entry for entry in entries if entry["suite"] == _SUITE]
    expected = [
        {"suite": _SUITE, **{key: row[key] for key in ("recipe", "path", "bytes", "sha256")}}
        for row in rows
    ]
    _require(actual == expected, "owning-projection")
    owned = root / _SUITE
    _directory(owned)
    _require({p.name for p in owned.iterdir()} == {
        row["recipe"] + ".json" for row in rows
    }, "owning-file-membership")
    for row in rows:
        raw = _regular(root / row["path"])
        _require(raw == payloads[row["recipe"]], "owning-independent-bytes")
        _require(len(raw) == row["bytes"], "owning-size")
        _require(hashlib.sha256(raw).hexdigest() == row["sha256"], "owning-sha256")
    _require(_regular(root / "MANIFEST") == manifest_before, "consumer-manifest-nonmutation")
    return entries


def _write_reference(root, reference):
    rows, _, payloads, manifest = reference
    root.mkdir()
    (root / _SUITE).mkdir()
    (root / "MANIFEST").write_bytes(manifest)
    for row in rows:
        (root / row["path"]).write_bytes(payloads[row["recipe"]])
    return root


def _temporary_snapshot(root):
    # A before/after observation of this private test fixture, not an enduring live pin.
    result = {}
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        value = path.read_bytes() if stat.S_ISREG(mode) else b""
        result[path.relative_to(root).as_posix()] = mode, value
    return result


def _check_registry(candidate):
    result = candidate.recipe_ids()
    _require(type(result) is tuple and all(type(r) is str for r in result), "registry-types")
    _require(result == _registry(), "production-registry")


def _check_payload(candidate, rid, expected):
    raw = candidate.generate_instance(rid)
    _require(type(raw) is bytes, "payload-exact-bytes-type")
    _require(raw == expected, "independent-production-bytes:" + rid)
    _decode_payload(raw)
    return raw


def _check_build(candidate, reference):
    rows, _, payloads, initial = reference
    records = candidate.build_corpus()
    _require(type(records) is tuple and len(records) == 656, "build-container")
    _require(all(type(row) is tuple and len(row) == 2 for row in records), "build-records")
    _require(all(type(p) is str and type(b) is bytes for p, b in records), "build-leaves")
    expected = (
        ("MANIFEST", initial),
        *((row["path"], payloads[row["recipe"]]) for row in rows),
    )
    _require(records == expected, "initial-build-bytes")
    _require(len(_parse_manifest(records[0][1])) == 655, "initial-build-row-count")
    return records


def test_public_surface():
    assert type(corpus.__all__) is tuple
    assert corpus.__all__ == ("build_corpus", "generate_instance", "recipe_ids")
    public = {name for name, value in vars(corpus).items()
              if not name.startswith("_") and callable(value)}
    assert public == set(corpus.__all__)
    assert not any(
        not name.startswith("_") and type(value) in (dict, list, set, bytearray)
        for name, value in vars(corpus).items()
    )
    specs = {
        "recipe_ids": ({"return": tuple[str, ...]}, ()),
        "generate_instance": ({"recipe_id": str, "return": bytes}, ("recipe_id",)),
        "build_corpus": ({"return": tuple[tuple[str, bytes], ...]}, ()),
    }
    for name, (expected_annotations, parameters) in specs.items():
        function = getattr(corpus, name)
        assert inspect.isfunction(function)
        assert get_type_hints(function) == expected_annotations
        signature = inspect.signature(function)
        assert tuple(signature.parameters) == parameters
        assert function.__defaults__ is None and function.__kwdefaults__ is None
        assert all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
                   and p.default is inspect.Parameter.empty for p in signature.parameters.values())


class _StringSubclass(str):
    pass


class _Hostile:
    def __str__(self):
        raise AssertionError("unexpected coercion")

    def __hash__(self):
        raise AssertionError("unexpected hashing")

    def __eq__(self, _other):
        raise AssertionError("unexpected equality")


def test_invalid_recipe_domain(capsys):
    valid = "edge-q01-f01-01"
    bad = (
        None, False, True, 1, 1.0, b"edge-q01-f01-01", ["sentinel"],
        {"sentinel": [1, 2]}, (), _Hostile(),
        _StringSubclass(valid), Path(valid), "", valid.upper(), " " + valid, valid + "\n",
        "edge-q1-f01-01", "edge-q01-f1-01", "edge-q01-f01-001", "edge-q00-f01-01",
        "edge-q06-f01-01", "edge-q01-f02-01", "edge-q01-f01-0\uff11", "edge-q01-f01-01\x00",
        "../" + valid, "/" + valid, "unit20-v1/" + valid + ".json", valid + ".json",
        "seeded-n04-b00008-fhalf-s00", "seeded-n04-b00008-fhalf-s02",
        "seeded-n04-b00008-fhalf-s1", "bits-cycle-n04-b16385-qramp-fdegree",
        "tri-q0-0-0-f1-1-1", "struct-path-n05-b00008-fdegree",
    )
    before = (sys.get_int_max_str_digits(), sys.getrecursionlimit(), dict(os.environ))
    for value in bad:
        saved = copy.deepcopy(value) if type(value) in (list, dict) else None
        with pytest.raises(ValueError) as caught:
            corpus.generate_instance(value)
        assert type(caught.value) is ValueError
        if saved is not None:
            assert value == saved
    assert before == (sys.get_int_max_str_digits(), sys.getrecursionlimit(), dict(os.environ))
    output = capsys.readouterr()
    assert output.out == output.err == ""


def test_complete_inventory_and_immutable_build(reference):
    _check_registry(corpus)
    first = _check_build(corpus, reference)
    assert _check_build(corpus, reference) == first
    assert corpus.recipe_ids() == _registry()


def test_all_payloads_and_closed_instance_boundary(reference):
    rows, objects, payloads, _ = reference
    for row in rows:
        rid = row["recipe"]
        raw = _check_payload(corpus, rid, payloads[rid])
        assert corpus.generate_instance(recipe_id=rid) == raw
        obj = _decode_payload(raw)
        assert obj == objects[rid]
        instance = Instance(obj["n"], tuple(map(tuple, obj["edges"])), tuple(obj["f"]))
        assert instance.n == obj["n"] and sum(e[2] for e in obj["edges"]) == instance.Q
        assert instance.m == row["m"] and instance.d_q == tuple(_active(obj))
    assert len(rows) == 655


def test_full_endpoint_and_micro_cross_model_references(reference):
    rows, objects, _, _ = reference
    counts, micro, empty = Counter(), Counter(), []
    for row in rows:
        rid, bits = row["recipe"], row["bits"]
        obj = objects[rid]
        value, locals_, work = _endpoints(obj)
        counts.update(work)
        expected = None if row["empty"] else (
            _expression(row["N"], bits), _expression(row["D"], bits),
        )
        assert _equivalent(value, expected), rid
        if value is None:
            empty.append(rid)
        else:
            s, internal, boundary = _shore_data(obj, row["mask"])
            total = _expression(row["Y"], bits)
            assert 0 < row["mask"] < 1 << obj["n"]
            assert 0 <= total <= sum(q for _, q in boundary)
            assert s + total >= 3 and (s + total) % 2
            assert expected == (2 * (internal + total), s + total - 1)
        if rid.startswith(("edge-", "tri-")):
            micro.update(_micro_models(obj, locals_))
    assert empty == ["edge-q01-f01-01"]
    assert counts == {
        "shores": 21549, "feasible_shores": 20704, "infeasible_shores": 845,
        "endpoint_evaluations": 39056,
    }
    assert micro == {
        "inputs": 379, "shores_compared": 2433, "compact_vectors_examined": 13179,
        "compact_admissible": 6183, "scalar_totals_examined": 8787, "scalar_admissible": 3981,
        "expanded_subsets_examined": 21487, "expanded_admissible": 10349,
    }
    print("EXACTFRAC_UNIT20_TEST_REFERENCE " + json.dumps({
        "recipes": len(rows), "endpoint": dict(counts), "micro": dict(micro),
    }, sort_keys=True))


def _certificate_attainment(obj, result):
    pair = result.value.N, result.value.D
    witness = result.witness
    if witness is None:
        assert sum(edge[2] for edge in obj["edges"]) == 1 and pair == (0, 1)
        return None
    assert type(witness.U) is int and 0 < witness.U < 1 << obj["n"]
    assert type(witness.y) is tuple and len(witness.y) == len(obj["edges"])
    s, internal, boundary = _shore_data(obj, witness.U)
    cross = {j for j, _ in boundary}
    for j, count in enumerate(witness.y):
        assert type(count) is int and 0 <= count <= obj["edges"][j][2]
        assert j in cross or count == 0
    total = sum(witness.y)
    assert s + total >= 3 and (s + total) % 2
    assert pair == (2 * (internal + total), s + total - 1)
    return pair


def test_both_closed_solvers_384_inputs_768_solves(reference):
    rows, objects, payloads, _ = reference
    selected = [r for r in rows if r["recipe"].startswith(("edge-", "tri-"))
                or r["recipe"] in {
                    f"bits-{family}-n04-b16384-qramp-fdegree" for family in _FAMILIES
                }]
    inputs = solves = certificates = 0
    for row in selected:
        rid, obj = row["recipe"], objects[row["recipe"]]
        raw = _check_payload(corpus, rid, payloads[rid])
        instance = Instance(obj["n"], tuple(map(tuple, obj["edges"])), tuple(obj["f"]))
        expected = None if row["empty"] else (
            _expression(row["N"], row["bits"]), _expression(row["D"], row["bits"]),
        )
        values = []
        for route in ("Standard", "Accelerated"):
            result, _stats = solve(instance, route)
            solves += 1
            value = _certificate_attainment(obj, result)
            assert _equivalent(value, expected), (rid, route)
            certificate = build_certificate(instance, result)
            encoded = serialize_certificate(instance, certificate)
            assert verify_certificate(raw, encoded) is None
            certificates += 1
            values.append(value)
        assert _equivalent(*values), rid
        inputs += 1
    assert (inputs, solves, certificates) == (384, 768, 768)
    print("EXACTFRAC_UNIT20_TEST_DUAL_SOLVER " + json.dumps({
        "inputs": inputs, "actual_solves": solves, "checked_certificates": certificates,
    }, sort_keys=True))


def test_same_route_repetition_and_numeric_tie_semantics(reference):
    _, objects, payloads, _ = reference
    count = 0
    for rid in ("tri-q1-1-1-f1-1-1", "bits-cycle-n04-b16384-qramp-fdegree"):
        obj = objects[rid]
        instance = Instance(obj["n"], tuple(map(tuple, obj["edges"])), tuple(obj["f"]))
        for route in ("Standard", "Accelerated"):
            first, first_stats = solve(instance, route)
            second, second_stats = solve(instance, route)
            count += 2
            assert first == second and first_stats == second_stats
            encoded = serialize_certificate(instance, build_certificate(instance, first))
            assert verify_certificate(payloads[rid], encoded) is None
    assert count == 8  # Separate repetition work, not included in the 768-solve campaign.
    assert _equivalent((2, 2), (4, 4))
    assert not _equivalent((0, 2), None)


def test_live_aggregate_owning_projection(reference):
    rows, _, payloads, _ = reference
    _owning_scope(_ROOT / "instances", rows, payloads)


def test_future_extension_and_formatting_nonmutation(tmp_path, reference):
    rows, _, payloads, initial = reference
    root = _write_reference(tmp_path / "instances", reference)
    _owning_scope(root, rows, payloads)
    foreign = b"foreign suite fixture; no scientific claim\n"
    (root / "unit21-v1").mkdir()
    (root / "unit21-v1/control.json").write_bytes(foreign)
    obj = _json(initial)
    obj["entries"].append({
        "suite": "unit21-v1", "recipe": "control", "path": "unit21-v1/control.json",
        "bytes": len(foreign), "sha256": hashlib.sha256(foreign).hexdigest(),
    })
    obj["entries"].sort(key=lambda r: r["path"])
    changed = json.dumps(obj, indent=2, sort_keys=True).encode("ascii")
    (root / "MANIFEST").write_bytes(changed)
    (root / "README.md").write_text("Later authorized documentation.\n", encoding="utf-8")
    (root / "NOTES.txt").write_text("Unrelated root documentation.\n", encoding="utf-8")
    before = _temporary_snapshot(root)
    entries = _owning_scope(root, rows, payloads)
    assert any(e["suite"] == "unit21-v1" for e in entries)
    assert _temporary_snapshot(root) == before
    assert changed != initial  # Positive counterexample to a global-MANIFEST identity check.


def _manifest_fault(initial, fault):
    obj = _json(initial)
    row = obj["entries"][0]
    guards = {
        "root-extra": "manifest-root", "root-missing": "manifest-root",
        "root-type": "manifest-root", "format": "manifest-format",
        "entries-type": "manifest-entries", "entry-extra": "entry-fields",
        "entry-missing": "entry-fields", "entry-type": "entry-fields",
        "bool-count": "byte-count", "str-count": "byte-count", "zero-count": "byte-count",
        "float-count": "number-kind", "exponent-count": "number-kind",
        "negative-zero": "integer-token", "negative-count": "integer-token",
        "duplicate-root": "duplicate-key", "escaped-duplicate": "duplicate-key",
        "duplicate-entry": "duplicate-key", "upper-sha": "digest-grammar",
        "short-sha": "digest-grammar", "bad-sha": "digest-grammar",
        "suite-leading-zero": "suite-grammar", "suite-zero": "suite-grammar",
        "version-leading-zero": "suite-grammar", "recipe-upper": "recipe-grammar",
        "recipe-underscore": "recipe-grammar", "recipe-double-hyphen": "recipe-grammar",
        "path-absolute": "path-equation", "path-traversal": "path-equation",
        "path-backslash": "path-equation", "path-nested": "path-equation",
        "path-encoded": "path-equation", "path-suffix": "path-equation",
        "path-wrong-recipe": "path-equation", "duplicate-row": "entry-order-identity",
        "reorder": "entry-order-identity", "suite-type": "entry-str",
        "recipe-type": "entry-str", "path-type": "entry-str", "sha-type": "entry-str",
    }
    if fault == "root-extra":
        obj["extra"] = 1
    elif fault == "root-missing":
        del obj["format"]
    elif fault == "root-type":
        obj = []
    elif fault == "format":
        obj["format"] = "exactfrac-corpus-manifest/2"
    elif fault == "entries-type":
        obj["entries"] = {}
    elif fault == "entry-extra":
        row["extra"] = 1
    elif fault == "entry-missing":
        del row["bytes"]
    elif fault == "entry-type":
        obj["entries"][0] = []
    elif fault in {"bool-count", "str-count", "zero-count", "negative-count"}:
        row["bytes"] = {"bool-count": True, "str-count": "1",
                        "zero-count": 0, "negative-count": -1}[fault]
    elif fault in {"float-count", "exponent-count", "negative-zero"}:
        token = {"float-count": b"1.0", "exponent-count": b"1e3", "negative-zero": b"-0"}[fault]
        old = str(row["bytes"]).encode("ascii")
        return initial.replace(b'"bytes":' + old, b'"bytes":' + token, 1), guards[fault]
    elif fault in {"duplicate-root", "escaped-duplicate"}:
        key = b'"format"' if fault == "duplicate-root" else b'"for\\u006dat"'
        return b"{" + key + b':"exactfrac-corpus-manifest/1",' + initial[1:], guards[fault]
    elif fault == "duplicate-entry":
        return initial.replace(b'"suite":', b'"suite":"unit20-v1","suite":', 1), guards[fault]
    elif fault in {"upper-sha", "short-sha", "bad-sha"}:
        row["sha256"] = {"upper-sha": "A" * 64, "short-sha": "0" * 63,
                         "bad-sha": "g" * 64}[fault]
    elif fault in {"suite-leading-zero", "suite-zero", "version-leading-zero"}:
        row["suite"] = {"suite-leading-zero": "unit020-v1", "suite-zero": "unit0-v1",
                        "version-leading-zero": "unit20-v01"}[fault]
    elif fault in {"recipe-upper", "recipe-underscore", "recipe-double-hyphen"}:
        row["recipe"] = {"recipe-upper": "Recipe", "recipe-underscore": "a_b",
                         "recipe-double-hyphen": "a--b"}[fault]
    elif fault.startswith("path-") and fault != "path-type":
        row["path"] = {
            "path-absolute": "/" + row["path"], "path-traversal": "../" + row["path"],
            "path-backslash": row["path"].replace("/", "\\"),
            "path-nested": _SUITE + "/nested/" + row["recipe"] + ".json",
            "path-encoded": row["path"].replace("/", "%2f"),
            "path-suffix": row["path"] + ".bak", "path-wrong-recipe": _SUITE + "/other.json",
        }[fault]
    elif fault == "duplicate-row":
        obj["entries"].insert(1, copy.deepcopy(row))
    elif fault == "reorder":
        obj["entries"][0], obj["entries"][1] = obj["entries"][1], obj["entries"][0]
    elif fault.endswith("-type"):
        row[{"suite-type": "suite", "recipe-type": "recipe",
             "path-type": "path", "sha-type": "sha256"}[fault]] = 1
    else:
        raise AssertionError("unregistered test fault")
    return json.dumps(obj, separators=(",", ":")).encode("ascii"), guards[fault]


@pytest.mark.parametrize("fault", (
    "root-extra", "root-missing", "root-type", "format", "entries-type", "entry-extra",
    "entry-missing", "entry-type", "bool-count", "str-count", "zero-count", "float-count",
    "exponent-count", "negative-zero", "negative-count", "duplicate-root", "escaped-duplicate",
    "duplicate-entry", "upper-sha", "short-sha", "bad-sha", "suite-leading-zero", "suite-zero",
    "version-leading-zero", "recipe-upper", "recipe-underscore", "recipe-double-hyphen",
    "path-absolute", "path-traversal", "path-backslash", "path-nested", "path-encoded",
    "path-suffix", "path-wrong-recipe", "duplicate-row", "reorder", "suite-type", "recipe-type",
    "path-type", "sha-type",
))
def test_manifest_parser_guard_isolation(reference, fault):
    initial = reference[3]
    assert len(_parse_manifest(initial)) == 655
    raw, guard = _manifest_fault(initial, fault)
    with pytest.raises(_GuardError) as caught:
        _parse_manifest(raw)
    assert str(caught.value) == guard


@pytest.mark.parametrize("fault,guard", (
    ("missing-file", "owning-file-membership"), ("extra-file", "owning-file-membership"),
    ("renamed-file", "owning-file-membership"), ("nested-file", "owning-file-membership"),
    ("changed-file", "owning-independent-bytes"), ("executable", "file-kind"),
    ("file-symlink", "file-kind"), ("owned-dir-symlink", "directory-redirection"),
    ("root-symlink", "directory-redirection"), ("fifo", "file-kind"),
    ("missing-own-row", "owning-projection"), ("extra-own-row", "owning-projection"),
    ("coherent-wrong-payload", "owning-projection"),
))
def test_owned_namespace_guard_isolation(tmp_path, reference, fault, guard):
    rows, objects, payloads, initial = reference
    root = _write_reference(tmp_path / "instances", reference)
    _owning_scope(root, rows, payloads)
    rid = "edge-q02-f01-01"
    path = root / _SUITE / (rid + ".json")
    if fault == "missing-file":
        path.unlink()
    elif fault == "extra-file":
        (root / _SUITE / "extra.json").write_bytes(b"{}\n")
    elif fault == "renamed-file":
        path.rename(path.with_name("renamed.json"))
    elif fault == "nested-file":
        nested = root / _SUITE / "nested"
        nested.mkdir()
        path.rename(nested / path.name)
    elif fault == "changed-file":
        path.write_bytes(payloads[rid] + b"\n")
    elif fault == "executable":
        path.chmod(0o755)
    elif fault == "file-symlink":
        target = tmp_path / "outside.json"
        path.rename(target)
        path.symlink_to(target)
    elif fault in {"owned-dir-symlink", "root-symlink"}:
        link = root / _SUITE if fault == "owned-dir-symlink" else root
        target = tmp_path / "redirected"
        link.rename(target)
        link.symlink_to(target, target_is_directory=True)
    elif fault == "fifo":
        path.unlink()
        os.mkfifo(path)
    else:
        obj = _json(initial)
        if fault == "missing-own-row":
            obj["entries"] = [r for r in obj["entries"] if r["recipe"] != rid]
        elif fault == "extra-own-row":
            raw = b"{}\n"
            (root / _SUITE / "extra.json").write_bytes(raw)
            obj["entries"].append({
                "suite": _SUITE, "recipe": "extra", "path": _SUITE + "/extra.json",
                "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            })
            obj["entries"].sort(key=lambda r: r["path"])
        else:
            wrong = copy.deepcopy(objects[rid])
            wrong["f"][1] = 2
            _active(wrong)  # Valid active input, but NOT this recipe's registered input.
            raw = (_encode(wrong) + "\n").encode("ascii")
            path.write_bytes(raw)
            for row in obj["entries"]:
                if row["recipe"] == rid:
                    row["bytes"], row["sha256"] = len(raw), hashlib.sha256(raw).hexdigest()
        (root / "MANIFEST").write_bytes(json.dumps(obj).encode("ascii"))
        _parse_manifest(_regular(root / "MANIFEST"))  # Earlier schema guard passes.
    with pytest.raises(_GuardError) as caught:
        _owning_scope(root, rows, payloads)
    assert str(caught.value) == guard


def test_consumer_mutants_do_not_freeze_or_rewrite_foreign_data(tmp_path, reference):
    rows, _, payloads, initial = reference
    for mode in ("global-manifest-freeze", "drop-foreign-rows", "root-inventory-freeze"):
        root = _write_reference(tmp_path / mode, reference)
        obj = _json(initial)
        raw = b"{}\n"
        (root / "unit21-v1").mkdir()
        (root / "unit21-v1/control.json").write_bytes(raw)
        obj["entries"].append({
            "suite": "unit21-v1", "recipe": "control", "path": "unit21-v1/control.json",
            "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
        })
        obj["entries"].sort(key=lambda r: r["path"])
        (root / "MANIFEST").write_bytes(json.dumps(obj, indent=2).encode("ascii"))
        (root / "README.md").write_bytes(b"Future documentation.\n")
        before = _temporary_snapshot(root)
        _owning_scope(root, rows, payloads)  # Pristine integration control accepts extension.
        assert _temporary_snapshot(root) == before
        with pytest.raises(_GuardError) as caught:
            if mode == "global-manifest-freeze":
                _require(_regular(root / "MANIFEST") == initial, mode)
            elif mode == "root-inventory-freeze":
                _require({p.name for p in root.iterdir()} == {"MANIFEST", _SUITE}, mode)
            else:
                (root / "MANIFEST").write_bytes(initial)
                _owning_scope(root, rows, payloads)  # Own scope alone cannot detect foreign loss.
                _require(_temporary_snapshot(root) == before, mode)
        assert str(caught.value) == mode


def _source_contract(raw):
    tree = ast.parse(raw)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name.split(".", 1)[0] in sys.stdlib_module_names
                       for alias in node.names), "stdlib imports only"
            assert not any(alias.name.split(".", 1)[0] in {"fractions", "decimal"}
                           for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0 and node.module is not None
            assert node.module.split(".", 1)[0] in sys.stdlib_module_names
            assert node.module.split(".", 1)[0] not in {"fractions", "decimal"}
            assert all(alias.name != "*" for alias in node.names)
        elif isinstance(node, ast.BinOp):
            assert not isinstance(node.op, ast.Div), "no true division"
        elif isinstance(node, ast.Constant):
            assert type(node.value) not in (float, complex)
        elif isinstance(node, ast.Call):
            name = node.func.id if isinstance(node.func, ast.Name) else (
                node.func.attr if isinstance(node.func, ast.Attribute) else ""
            )
            assert name not in {
                "eval", "exec", "compile", "__import__", "import_module", "float", "hash",
                "set_int_max_str_digits", "setrecursionlimit", "settrace", "setprofile",
            }, "forbidden generator operation: " + name
    return tree


def test_source_stdlib_exactness_and_dependency_boundary():
    source = Path(corpus.__file__).read_bytes()
    _source_contract(source)


# Runs the actual future source standalone, not a substitute generator. No project
# package, catalogue or handoff import is possible in the child. Source/data arrive
# over stdin; the child uses -S -P and a fresh nonrepository working directory.
_GENERATION_WORKER = r'''
import ast
import builtins
import copy
import datetime
import hashlib
import importlib
import json
import os
import random
import secrets
import sys
import time
import types

request = json.loads(sys.stdin.buffer.read())
source = request["source"]
filename = request["filename"]
scenario = request["scenario"]
expected = request["records"]
ids = request["ids"]
settings = (sys.get_int_max_str_digits(), sys.getrecursionlimit())
assert settings[0] == request["limit"]
assert not any(n.split(".")[0] in {"exactfrac", "exactfrac_verify", "tests"}
               for n in sys.modules)
code = compile(source, filename, "exec")
imports = set()
for node in ast.walk(ast.parse(source)):
    if isinstance(node, ast.Import):
        imports.update(alias.name for alias in node.names)
    elif isinstance(node, ast.ImportFrom):
        assert node.level == 0 and node.module
        imports.add(node.module)
for name in sorted(imports):
    assert name.split(".")[0] in sys.stdlib_module_names
    importlib.import_module(name)

active = False

def block(*args, **kwargs):
    raise RuntimeError("generator attempted a blocked operation")

def audit(event, args):
    if not active:
        return
    if event == "open" or event.startswith(("os.", "socket.", "subprocess.", "ctypes.")):
        block()
    if event in {"exec", "compile"} and not (event == "exec" and args[0] is code):
        block()
    if event == "import" and args[0] not in sys.modules:
        block()

sys.addaudithook(audit)
original_import = builtins.__import__

def controlled_import(name, globals=None, locals=None, fromlist=(), level=0):
    assert level == 0 and name in imports, "undeclared or dynamic import: " + name
    return original_import(name, globals, locals, fromlist, level)

real_sha256, real_new = hashlib.sha256, hashlib.new
control = {"injections": 0, "hash_calls": 0, "fail_enabled": False}
error = {"memory": MemoryError, "recursion": RecursionError, "oserror": OSError}.get(scenario)
sentinel = error("unit20 injected operational failure") if error else None
message = b"exactfrac-u20-seeded/1\n1\n4\n0\n2\n"

class Digest:
    def __init__(self, data=b"", **kwargs):
        self.raw = bytes(data)
        self.inner = real_sha256(data, **kwargs)

    def update(self, data):
        self.raw += bytes(data)
        self.inner.update(data)

    def digest(self):
        value = self.inner.digest()
        if scenario == "boundary" and self.raw == message:
            control["injections"] += 1
            return bytes([64]) + value[1:]
        return value

    def hexdigest(self):
        return self.digest().hex()

    def copy(self):
        result = Digest()
        result.raw, result.inner = self.raw, self.inner.copy()
        return result

    def __getattr__(self, name):
        return getattr(self.inner, name)


def patched_sha256(data=b"", **kwargs):
    control["hash_calls"] += 1
    if control["fail_enabled"] and control["hash_calls"] == 7:
        control["injections"] += 1
        raise sentinel
    return Digest(data, **kwargs)


def patched_new(name, data=b"", **kwargs):
    if name.lower().replace("-", "") == "sha256":
        return patched_sha256(data, **kwargs)
    return real_new(name, data, **kwargs)

if scenario != "all":
    hashlib.sha256, hashlib.new = patched_sha256, patched_new

original_environment = os.environ
before_environment = dict(original_environment)

class NoEnvironment:
    __getitem__ = __setitem__ = __delitem__ = __iter__ = __len__ = block
    get = keys = values = items = copy = update = setdefault = pop = block

os.environ = NoEnvironment()
if hasattr(os, "environb"):
    os.environb = NoEnvironment()
for name in ("getenv", "getenvb", "putenv", "unsetenv", "urandom", "getrandom", "getcwd"):
    if hasattr(os, name):
        setattr(os, name, block)
for name in ("time", "time_ns", "monotonic", "monotonic_ns", "perf_counter",
             "perf_counter_ns", "process_time", "process_time_ns", "sleep"):
    if hasattr(time, name):
        setattr(time, name, block)
for name in ("random", "seed", "getrandbits", "randint", "randrange", "choice",
             "choices", "shuffle", "sample", "Random", "SystemRandom"):
    setattr(random, name, block)
random._urandom = block
for name in ("choice", "randbelow", "randbits", "token_bytes", "token_hex", "token_urlsafe"):
    setattr(secrets, name, block)

class NoDateTime(datetime.datetime):
    now = utcnow = today = classmethod(block)

class NoDate(datetime.date):
    today = classmethod(block)

datetime.datetime, datetime.date = NoDateTime, NoDate
sys.set_int_max_str_digits = sys.setrecursionlimit = block
module = types.ModuleType("_unit20_actual_standalone_generator")
module.__file__ = filename
module.__dict__["__builtins__"] = dict(vars(builtins), __import__=controlled_import,
                                       open=block, print=block, input=block)

def state():
    return copy.deepcopy({k: v for k, v in vars(module).items()
                          if not k.startswith("__") and type(v) in
                          (dict, list, set, tuple, bytes, bytearray, int, str)})

def check_records(records):
    assert type(records) is tuple and len(records) == len(expected)
    observed = []
    for record in records:
        assert type(record) is tuple and len(record) == 2
        path, raw = record
        assert type(path) is str and type(raw) is bytes
        observed.append([path, len(raw), real_sha256(raw).hexdigest()])
    assert observed == expected

active = True
exec(code, module.__dict__)
before_state = state()
assert type(module.recipe_ids()) is tuple and module.recipe_ids() == tuple(ids)
if error:
    control["hash_calls"] = 0
    control["fail_enabled"] = True
    caught = None
    try:
        value = module.build_corpus()
    except BaseException as exc:
        caught = exc
    if control["injections"]:
        assert caught is sentinel, "same operational exception required; never partial success"
    else:
        assert caught is None
        check_records(value)  # No dependency call: no fabricated injection claim.
    control["fail_enabled"] = False
elif scenario == "boundary":
    rid = "seeded-n04-b00008-fhalf-s01"
    result = module.generate_instance(rid)
    assert type(result) is bytes and result.hex() == request["boundary_hex"]
    assert control["injections"] > 0, "threshold intervention did not reach actual SHA call"
else:
    first = module.build_corpus()
    check_records(first)
    for rid, (_, length, digest) in zip(ids, expected[1:], strict=True):
        value = module.generate_instance(rid)
        assert type(value) is bytes and len(value) == length
        assert real_sha256(value).hexdigest() == digest
    check_records(module.build_corpus())
    assert state() == before_state, "generator changed persistent built-in state"
assert state() == before_state, "generator mutated module state"
assert (sys.get_int_max_str_digits(), sys.getrecursionlimit()) == settings
active = False
os.environ = original_environment
assert dict(original_environment) == before_environment
assert not any(n.split(".")[0] in {"exactfrac", "exactfrac_verify", "tests"}
               for n in sys.modules)
report = {"result": "PASS", "scenario": scenario, "limit": settings[0],
          "recursion_limit": settings[1], "hash_seed": original_environment["PYTHONHASHSEED"],
          "source_sha256": real_sha256(source.encode("utf-8")).hexdigest(),
          "injections": control["injections"], "records": len(expected),
          "settings_unchanged": True, "project_imports": []}
sys.stdout.write("EXACTFRAC_UNIT20_GENERATOR_PROCESS " + json.dumps(report, sort_keys=True) + "\n")
'''


def _process_request(reference, limit, scenario):
    rows, _, _, initial = reference
    source = Path(corpus.__file__).read_text(encoding="utf-8")
    _source_contract(source)
    records = [["MANIFEST", len(initial), hashlib.sha256(initial).hexdigest()]]
    records.extend([r["path"], r["bytes"], r["sha256"]] for r in rows)
    # Only (0,2) is intercepted by the child. Other pairs retain real SHA values.
    target = b"exactfrac-u20-seeded/1\n1\n4\n0\n2\n"

    def boundary_hash(raw):
        digest = hashlib.sha256(raw).digest()
        return bytes([64]) + digest[1:] if raw == target else digest

    obj = _plain("seeded-n04-b00008-fhalf-s01", seed_hash=boundary_hash)
    return {
        "source": source, "filename": str(Path(corpus.__file__).resolve()),
        "scenario": scenario, "limit": limit, "records": records,
        "ids": [row["recipe"] for row in rows],
        "boundary_hex": (_encode(obj) + "\n").encode("ascii").hex(),
    }


def _run_process(tmp_path, reference, limit, seed, scenario):
    request = _process_request(reference, limit, scenario)
    env = {"PATH": os.defpath, "PYTHONHASHSEED": str(seed), "PYTHONDONTWRITEBYTECODE": "1"}
    response = subprocess.run(
        [sys.executable, "-S", "-P", "-B", "-u", "-X", f"int_max_str_digits={limit}",
         "-c", _GENERATION_WORKER],
        input=json.dumps(request).encode("ascii"), capture_output=True,
        cwd=tmp_path, env=env, check=False,
    )
    assert response.returncode == 0, response.stderr.decode("utf-8", errors="replace")
    assert response.stderr == b""
    lines = response.stdout.decode("ascii").splitlines()
    assert len(lines) == 1 and lines[0].startswith("EXACTFRAC_UNIT20_GENERATOR_PROCESS ")
    report = json.loads(lines[0].split(" ", 1)[1])
    assert report["result"] == "PASS" and report["limit"] == limit
    assert report["hash_seed"] == str(seed) and report["records"] == 656
    assert report["project_imports"] == [] and report["settings_unchanged"] is True
    assert report["source_sha256"] == hashlib.sha256(request["source"].encode()).hexdigest()
    print(lines[0])
    return report


@pytest.mark.parametrize("limit,seed", itertools.product((640, 4300), (1, 73)))
def test_fresh_process_full_generation_purity_and_settings(tmp_path, reference, limit, seed):
    _run_process(tmp_path, reference, limit, seed, "all")


def test_private_exact_sha_threshold_control(tmp_path, reference):
    report = _run_process(tmp_path, reference, 640, 1, "boundary")
    assert report["injections"] > 0


@pytest.mark.parametrize("scenario", ("memory", "recursion", "oserror"))
def test_operational_sha_failure_is_not_partial_success(tmp_path, reference, scenario):
    _run_process(tmp_path, reference, 640, 73, scenario)
