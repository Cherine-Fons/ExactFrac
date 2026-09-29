"""Unit 21B runner consumer under the prospective balanced-main R2 amendment.

Independent readers/reconstruction use the registered Phase C fixtures. Runtime
runner scenarios use authenticated temporary source copies and scripted telemetry;
they are NOT real pilot/main observations. The separately named micro-composition
test alone may call the real solver, on the two adopted preexisting inputs only.
No production module, pilot, campaign, F7 approval or new gate is supplied here.
"""

from __future__ import annotations

import ast
import base64
import builtins
import collections
import contextlib
import copy
import csv
import dataclasses
import dis
import functools
import hashlib
import importlib
import inspect
import io
import itertools
import json
import math
import os
import platform
import re
import stat
import subprocess
import sys
import tempfile
import time
import types
import typing
import zipfile
from pathlib import Path, PurePosixPath

import pytest

import exactfrac.experiments_irregular as runner

_ROOT = Path(__file__).resolve().parents[1]
_MODULE = "exactfrac.experiments_irregular"
_HEADER = b"## Unit 21B \xe2\x80\x94 Phase C independent irregular oracle, R1\n"
_FENCE = re.compile(
    rb"^<!-- U21B-FIXTURE ([^ \n]+) (raw|base64) ([0-9]+) ([0-9a-f]{64}) -->\n"
    rb"```[^\n]*\n(.*?)^```\n", re.MULTILINE | re.DOTALL,
)
_ROUTES = ("Standard", "Accelerated")
_SEEDS = tuple(f"p{i:02d}" for i in range(1, 6)) + tuple(f"s{i:02d}" for i in range(1, 21))
_REGISTRY = tuple(sorted(
    f"irregular-n{n:02d}-t{tau:03d}-b{b:05d}-f{mode}-{seed}"
    for n, tau, b, mode, seed in itertools.product(
        (6, 8, 12, 16), (64, 128), (1, 8, 64), ("alternating", "random"), _SEEDS,
    )
))
_CELLS = tuple(sorted({rid.rsplit("-", 1)[0] for rid in _REGISTRY}))
_MAIN_CELLS = tuple(cell for cell in _CELLS if int(cell.split("-")[1][1:]) in (6, 8, 12))
# Fixed fixture-local pins, not enduring catalogue/source/aggregate directory pins.
_FIXTURE_PINS = {'DESCRIPTOR_BOUNDARY_CASES.json': (834,
        '43d3aaf722e879e71a1bbe4090e28ab9736ea2d104bf6213dea7b1eaaff1aecc'),
 'FAULT_DECLARATIONS.json': (125051,
                             '19433d9596ddea76f121313d6c2a4ddec56c2a34636b400bd38b6360f8bf4132'),
 'FIELD_REGISTRY.json': (5939,
                         '4e2af40a8a5acf8bc3233fb8a094cc004510e2239a1f7c44d022a2a7ddbfa240'),
 'H3_ARITHMETIC_CASES.json': (1165,
                              '575c66d4cdce04c4581ad1c4bb5977cc0134504a390cb9e504c10584a891975b'),
 'H3_ROUTE_MEDIAN_CASES.json': (6320,
                                '75542c1f39c5306c932f415c5f378b47a6a22b5b40c71ea41fff12627e3dda06'),
 'H5_BOUNDARY_CASES.json': (3510648,
                            'd0233be24f16753c9adab3e0d6a5b20379e97980edf2127584fb714882eb095f'),
 'HELP.txt': (184, '19038b30d3e8c26317f36281b06b9769c5e1fc0afa613adc1e9a0a990cf29bef'),
 'INVENTORY.tsv': (370655, '1ac23b1a169a6edfb46ec502e2420a71a3d3932007e5d9b70316e948fb430822'),
 'MAIN_SCHEDULE.tsv': (913919,
                       '846e957b84159959fc011a03c3006bd8d6a1cb5595a515d5a02db6cb9e5364fa'),
 'OWN_MANIFEST': (271414, '8f34e232966fc5142cc281655f28dfe858ccd610aecb0ecdb5d2b9f61d6510a0'),
 'PILOT_SCHEDULE.tsv': (58059,
                        '90770cc26e1f7ae960d5c5c94c47791642afd31dcb4cc2f7fb7416b749923576'),
 'PROTOCOLS.json': (1324, 'cd3f7fde7075b5c811d1d0d78b950d3eece1266856476b4b6d08c9d7363078df'),
 'REFERENCE_ROWS.jsonl': (2893425,
                          'f1a2afa6d5adf6185056cccf377c1125a6c12b9a2256538afd5550a4f4991510'),
 'SOURCE_PATHS.json': (1721,
                       '445b589da4a5a2fc0e0c72d6d13cfa1c8b2af5e0cbdcf2561e2a22e186f691b3'),
 'SYNTHETIC_EMPTY_ALGORITHMS.json': (2806,
        '4f88801f52d64c28fa0e15f49da2649b5c746b8c6be89a2ec1ff14b9fdc5a554'),
 'SYNTHETIC_ESCAPING_ROW.jsonl': (6349,
        '3edede9c0c60846a1c86f3451f3ee3a0f8d76a643818c19b921919c7a5974f42'),
 'SYNTHETIC_GIANT_ROW.jsonl': (19162,
                               '3c0badda7467cd917a7a72126f73a871cac853df010405af0a49067dae5bcaf2'),
 'SYNTHETIC_META.json': (703,
                         '8c672ff5db2b9b9fd239b037f16df074e0f835d5c60e45daa1932a34b5eaf7aa'),
 'SYNTHETIC_PILOT_CELL_CLOCKS.json': (7865,
        'a1f2b148a54b14ecf3d5c1faf83a0c369b9bf025d6131415023af7f2fb46e696'),
 'SYNTHETIC_SOURCE_FINGERPRINT.bin': (2247,
        '909efa2bd4553ad0361079d4f320835de363ef384e00bc10c544ad5438300e4e'),
 'SYNTHETIC_SOURCE_IMAGES.json': (4534,
        'c0f9c039ba2211fc4c2b81819a467e583dc8f3f7c955add1c01e329c5f45fc7a'),
 'SYNTHETIC_WIRE_BANK.zip': (2658913,
                             'a7a3f5b2455845fafc1e28b0f1cc03b9809dfeac57b3128a10b4103b866462dc'),
 'SYNTHETIC_WIRE_BANK_INDEX.json': (416053,
        '89ea7254f413cd14383ff2cff6dfe68199bf6d78f4f5f3d066f3b5517f13206b'),
 'TIMING_TRAPS.json': (912, '05b886aaf1aada4610dccfa794a56b6ecb4ec6d267c454956e7e7a87c5c50988'),
 'TINY_CERTIFICATE_CASES.json': (2987,
                                 '813365cb65e2aef709add2f5332dbaba2a824c46fbaae4c1fb524d1c16dc07e3'
                                     ),
 'USAGE.txt': (92, '3353fa2a96af3cc6781f03f7a430ce573c5b68aec732e851f3a54eb0b5a670b0'),
 'WIRE_SCHEMAS.json': (7466,
                       '654c6900d670afb473ecd87ceffdb884b305a106cb32d47605db6520be73118e')}


def _need(condition, guard):
    if not condition:
        raise AssertionError(guard)


def _identity(raw):
    return len(raw), hashlib.sha256(raw).hexdigest()


def _same(actual, expected, guard):
    _need(type(actual) is type(expected), guard)
    if type(expected) is dict:
        _need(set(actual) == set(expected), guard)
        for key in expected:
            _same(actual[key], expected[key], guard)
    elif type(expected) in (tuple, list):
        _need(len(actual) == len(expected), guard)
        for left, right in zip(actual, expected, strict=True):
            _same(left, right, guard)
    else:
        _need(actual == expected, guard)


def _keys(obj, expected, guard):
    _need(type(obj) is dict and set(obj) == set(expected), guard)


def _count(value, guard, minimum=0):
    _need(type(value) is int and value >= minimum, guard)


def _pairs_unique(items):
    result = {}
    for key, value in items:
        _need(key not in result, "duplicate-decoded-key")
        result[key] = value
    return result


def _integer(token):
    _need(re.fullmatch(r"0|-?[1-9][0-9]*", token) is not None, "canonical-integer-token")
    negative = token.startswith("-")
    digits = token[1:] if negative else token
    value = 0
    for start in range(0, len(digits), 9):
        piece = digits[start:start + 9]
        value = value * 10 ** len(piece) + int(piece)
    return -value if negative else value


def _finite(token):
    value = float(token)
    _need(math.isfinite(value), "finite-json")
    return value


def _no_constant(_token):
    raise AssertionError("finite-json")


def _parse(raw, canonical=False):
    _need(type(raw) is bytes and not raw.startswith(b"\xef\xbb\xbf"), "wire-bytes-no-bom")
    try:
        value = json.loads(
            raw.decode("utf-8"), parse_int=_integer, parse_float=_finite,
            parse_constant=_no_constant, object_pairs_hook=_pairs_unique,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise AssertionError("single-valid-json-document") from error
    if canonical:
        _same(raw, _encode(value) + b"\n", "canonical-ascii-json")
    return value


def _decimal(value):
    _need(type(value) is int, "decimal-exact-int")
    if value == 0:
        return b"0"
    negative, magnitude = value < 0, abs(value)
    pieces = []
    while magnitude:
        magnitude, piece = divmod(magnitude, 1_000_000_000)
        pieces.append(piece)
    text = str(pieces.pop()) + "".join(f"{piece:09d}" for piece in reversed(pieces))
    return ("-" if negative else "").encode() + text.encode("ascii")


def _encode(value):
    if value is None:
        return b"null"
    if type(value) is bool:
        return b"true" if value else b"false"
    if type(value) is int:
        return _decimal(value)
    if type(value) is float:
        _need(math.isfinite(value), "finite-json")
        return json.dumps(value, allow_nan=False).encode("ascii")
    if type(value) is str:
        return json.dumps(value, ensure_ascii=True).encode("ascii")
    if type(value) in (tuple, list):
        return b"[" + b",".join(_encode(item) for item in value) + b"]"
    _need(type(value) is dict and all(type(k) is str for k in value), "json-object-types")
    return b"{" + b",".join(
        _encode(key) + b":" + _encode(value[key]) for key in sorted(value)
    ) + b"}"


def _read_bank(data):
    _need(data.count(_HEADER) == 1, "unique-phase-c-appendix")
    appendix = data.split(_HEADER, 1)[1].split(b"\n## ", 1)[0]
    required = set(_FIXTURE_PINS) | {"inputs/" + rid + ".json" for rid in _REGISTRY}
    result = {}
    for match in _FENCE.finditer(appendix):
        name, encoding, length, digest, raw = match.groups()
        name = name.decode("ascii")
        if name not in required:
            continue
        _need(name not in result, "duplicate-fixture")
        if encoding == b"base64":
            raw = base64.b64decode(b"".join(raw.split()), validate=True)
        _same(_identity(raw), (int(length), digest.decode()), "fixture-fence-identity")
        if name in _FIXTURE_PINS:
            _same(_identity(raw), _FIXTURE_PINS[name], "fixed-fixture-identity")
        result[name] = raw
    _same(set(result), required, "complete-runner-fixture-membership")
    return result


@functools.cache
def _bank():
    return _read_bank((_ROOT / "docs/ORACLE_CATALOG.md").read_bytes())


_R2_HEADER = (
    "## Unit 21B — prospective balanced main oracle revision R2, September 26, 2026\n"
).encode()
_R2_FENCE = re.compile(
    rb"^<!-- U21B-MAIN-R2-FIXTURE ([^ \n]+) (raw|base64) ([0-9]+) ([0-9a-f]{64}) -->\n"
    rb"```[^\n]*\n(.*?)^```\n", re.MULTILINE | re.DOTALL,
)
_R2_FIXTURE_PINS = {
    'CENSUS.json': (
        795, "dab9d8fbf354f1630f91f1e5d7d742c6b5254eff5434beca4975c834f1eec526",
    ),
    'EXCLUDED_MAIN_SELECTION.json': (
        10202, "f5d591ddc0338456526c191e17dc957ebb7a797b9361e90b2ff7238fc18d531d",
    ),
    'FAULT_DECLARATIONS.json': (
        115612, "f1089853f4e34069d748ec89640fad55cf80034d4df83b6360bf9b3424e96a33",
    ),
    'FAULT_VERSION_MAP.json': (
        51509, "81fb5b4a6c011817cf566933adcb6b2f5f10409c05b8a59f5ad58ad012100684",
    ),
    'H3_ARITHMETIC_CASES.json': (
        1165, "575c66d4cdce04c4581ad1c4bb5977cc0134504a390cb9e504c10584a891975b",
    ),
    'H3_ROUTE_MEDIAN_CASES.json': (
        4800, "a6b368a0af8af4f0e42b2bdb31ae10ab184cae59bab082958481c9bd3a229d76",
    ),
    'H3_SERIES.json': (
        79402, "7ef525b3c6473e8253d7065d89e6180aae2dccb222aa6972355da19d635946c0",
    ),
    'H5_BOUNDARY_CASES.json': (
        2624694, "0026757d87e4686dbd2373686be7e2e420813c6957f784a97085d9018c7db3b1",
    ),
    'MAIN_CELLS.json': (
        1388, "f6360b9b229eca4fd15ba9e3562c125aa5b60335bdc8c0323d847b5ac8a9d8b0",
    ),
    'MAIN_SCHEDULE.tsv': (
        684959, "d6b4b92bd40d87f891229bd1eab3a6b384b0d47b65751b4ea9be32c48d0bfd06",
    ),
    'MAIN_SELECTION.json': (
        30602, "3e45cf3bbcabaf7e58478e44b0199085785173273497bea3dd5cd52129832060",
    ),
    'OUTPUT_CENSUS.json': (
        736, "dcd7d3875280bda08ce90f5785e95579fbbd56a4a7f8a70457949f7797936026",
    ),
    'PILOT_LINEAGE_BINDING.json': (
        95535, "61a20c896f063958893abc362a115a860776a715674d5b1fc9e26fdd80cc75a6",
    ),
    'PILOT_SOURCE_SNAPSHOT_IDENTITY.json': (
        383, "500770933eecebf30576e64048653cafd28f8afc4723f85782b33d47ab43cafd",
    ),
    'PRESERVED_INPUT_BINDINGS.json': (
        321403, "26db4405026667c3651d18865a195187b883e53ce693c55de0ae3d52523ef9e5",
    ),
    'PROTOCOLS.json': (
        1324, "cd3f7fde7075b5c811d1d0d78b950d3eece1266856476b4b6d08c9d7363078df",
    ),
    'SOURCE_PATHS.json': (
        1721, "445b589da4a5a2fc0e0c72d6d13cfa1c8b2af5e0cbdcf2561e2a22e186f691b3",
    ),
    'SYNTHETIC_WIRE_BANK.zip': (
        2184698, "d72bcefa33eec6741db1fed8ca43182a55058b9c3176a466193aebacc23bdcf5",
    ),
    'SYNTHETIC_WIRE_BANK_INDEX.json': (
        333304, "afc8711a3c82e3c6d8e80dec9e459954b1b13553df93baba1cb771f6b5d06a66",
    ),
    'WIRE_SCHEMAS.json': (
        7466, "654c6900d670afb473ecd87ceffdb884b305a106cb32d47605db6520be73118e",
    ),
    'examples/main/COMPLETE.json': (
        242244, "378493b491395044f334aabb3e1dac24e9e41821b704de93a9661ca86f5d6b9d",
    ),
    'examples/main/coverage.csv': (
        2378, "a744942fef6ad70c1b1f31fdb88033debee09b1218fd3a573683fe3beccadd14",
    ),
    'examples/main/findings.json': (
        16423, "f47afcae4fbf9b7db999b7e7849a19797ef504ebded79daa045b1bbe019fed4c",
    ),
    'examples/main/run-info.json': (
        3908, "ccb805a1d019fbc03ae23cf8bd3ed1b4108c96b76d0f254a32e73b23e502c9d0",
    ),
}


def _read_r2_bank(data):
    _same(data.count(_R2_HEADER), 1, "unique-main-r2-appendix")
    appendix = data.split(_R2_HEADER, 1)[1].split(b"\n## ", 1)[0]
    result = {}
    for match in _R2_FENCE.finditer(appendix):
        name, encoding, length, digest, raw = match.groups()
        name = name.decode("ascii")
        _need(name in _R2_FIXTURE_PINS, "declared-main-r2-fixture")
        _need(name not in result, "duplicate-main-r2-fixture")
        if encoding == b"base64":
            raw = base64.b64decode(b"".join(raw.split()), validate=True)
        _same(_identity(raw), (int(length), digest.decode()), "main-r2-fence-identity")
        _same(_identity(raw), _R2_FIXTURE_PINS[name], "fixed-main-r2-fixture-identity")
        result[name] = raw
    _same(set(result), set(_R2_FIXTURE_PINS), "complete-main-r2-fixtures")
    return result


@functools.cache
def _r2_bank():
    return _read_r2_bank((_ROOT / "docs/ORACLE_CATALOG.md").read_bytes())


@functools.cache
def _schema():
    return _parse(_bank()["WIRE_SCHEMAS.json"])


@functools.cache
def _references():
    rows = [_parse(line) for line in _bank()["REFERENCE_ROWS.jsonl"].splitlines()]
    _same(tuple(row["recipe"] for row in rows), _REGISTRY, "reference-order")
    return {row["recipe"]: row for row in rows}


def _input(rid):
    raw = _bank()["inputs/" + rid + ".json"]
    ref = _references()[rid]
    _same(_identity(raw), (ref["input_bytes"], ref["input_sha256"]), "independent-input-binding")
    return raw


@functools.cache
def _wire_bank():
    index = _parse(_r2_bank()["SYNTHETIC_WIRE_BANK_INDEX.json"])["entries"]
    with zipfile.ZipFile(io.BytesIO(_r2_bank()["SYNTHETIC_WIRE_BANK.zip"])) as archive:
        names = archive.namelist()
        _same(len(names), len(set(names)), "wire-bank-no-duplicate")
        _same(names, [entry["path"] for entry in index], "wire-bank-fixed-membership")
        result = {}
        for entry in index:
            path = PurePosixPath(entry["path"])
            _need(not path.is_absolute() and ".." not in path.parts, "wire-bank-path")
            raw = archive.read(entry["path"])
            _same(_identity(raw), (entry["bytes"], entry["sha256"]), "wire-bank-entry")
            result[entry["path"]] = raw
    return result


def _mode_files(mode):
    prefix = mode + "/"
    return {name[len(prefix):]: raw for name,
        raw in _wire_bank().items() if name.startswith(prefix)}


def _selected(mode):
    _need(mode in ("main", "pilot"), "test-mode")
    letter = "s" if mode == "main" else "p"
    return tuple(
        rid for rid in _REGISTRY if rid.rsplit("-", 1)[1].startswith(letter)
        and (mode == "pilot" or int(rid.split("-")[1][1:]) in (6, 8, 12))
    )


def _schedule(mode):
    result = []
    for index, rid in enumerate(_selected(mode)):
        for round_number in ((-1, 0, 1, 2) if mode == "main" else (0,)):
            routes = _ROUTES if (index + round_number) % 2 == 0 else _ROUTES[::-1]
            phase = "pilot" if mode == "pilot" else ("warmup" if round_number == -1 else "measured")
            for route in routes:
                result.append((rid, route, phase, max(0, round_number)))
    return tuple(result)


def _support_hash(obj):
    raw = b"exactfrac-unit21b-support/1\n" + _decimal(obj["n"]) + b"\n"
    raw += b"".join(_decimal(u) + b"," + _decimal(v) + b"\n" for u, v, _q in obj["edges"])
    return hashlib.sha256(raw).hexdigest()


@functools.cache
def _input_metadata(rid):
    raw = _input(rid)
    obj, ref = _parse(raw), _references()[rid]
    def bits(value):
        return max(1, abs(value).bit_length())
    n, edges, capacities = obj["n"], obj["edges"], obj["f"]
    return {
        "suite": "unit21-v2", "path": "unit21-v2/" + rid + ".json",
        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
        "n": n, "m": len(edges), "Q_bits": bits(sum(e[2] for e in edges)),
        "max_q_bits": max(bits(e[2]) for e in edges),
        "max_f_bits": max(map(bits, capacities)),
        "input_integer_bits_sum": bits(n) + bits(len(edges))
        + sum(bits(v) for edge in edges for v in edge) + sum(map(bits, capacities)),
        **{key: ref[key] for key in ("cell", "tau", "b", "capacity_mode", "seed")},
        "support_sha256": _support_hash(obj),
    }


def _descriptor(n, terminals, parity, inside, outside):
    feasible = not (inside & outside) and (
        bool(terminals & ~(inside | outside)) or (inside & terminals).bit_count() % 2 == parity
    )
    reduced = 2 + n - (inside | outside).bit_count() if feasible else None
    cuts = reduced * reduced - 3 * reduced + 3 if feasible else 0
    return bool(feasible), reduced, cuts


def _geometry(obj):
    n, edges, f = obj["n"], obj["edges"], obj["f"]
    degrees = [0] * n
    for u, v, q in edges:
        degrees[u] += q
        degrees[v] += q
    plus = sum(1 << v for v in range(n) if (f[v] + degrees[v]) % 2)
    tf = sum(1 << v for v in range(n) if f[v] % 2)
    p = [v for v in range(n) if degrees[v] > f[v]]
    a = [v for v in range(n) if f[v] >= 2]
    w = [v for v in range(n) if f[v] == 1]
    descriptors = [[(plus, 1, 0, 0)], [], [], []]
    for vtx in p:
        for u, v, _q in edges:
            descriptors[1].extend(((plus, 0, (1 << vtx) | (1 << u), 1 << v),
                                   (plus, 0, (1 << vtx) | (1 << v), 1 << u)))
    descriptors[2].extend((tf, 1, 1 << v, 0) for v in a)
    descriptors[2].extend((tf, 1, sum(1 << v for v in triple), 0)
                          for triple in itertools.combinations(w, 3))
    for u, v, _q in edges:
        descriptors[3].extend(((tf, 0, 1 << u, 1 << v), (tf, 0, 1 << v, 1 << u)))
    branches = []
    for j, desc in enumerate(descriptors):
        outcomes = [_descriptor(n, *d) for d in desc]
        histogram = collections.Counter(reduced for ok, reduced, _calls in outcomes if ok)
        descriptor_wire = [[*d, ok, reduced] for d, (ok, reduced, _cuts)
                           in zip(desc, outcomes, strict=True)]
        branches.append({
            "descriptor_sha256": hashlib.sha256(_encode(descriptor_wire) + b"\n").hexdigest(),
            "branch": j, "r": len(desc), "s": sum(ok for ok, _n, _a in outcomes),
            "A": sum(calls for _ok, _n, calls in outcomes),
            "N_histogram": {str(key): histogram[key] for key in sorted(histogram)},
        })
    _same(tuple(b["r"] for b in branches),
          (1, 2 * len(p) * len(edges), len(a) + math.comb(len(w), 3), 2 * len(edges)),
          "complete-descriptor-cardinality")
    return {"Tplus": plus, "Tf": tf, "P": p, "A_vertices": a, "W": w,
            "branches": branches}, descriptors


@functools.cache
def _geometry_check(rid):
    actual, descriptors = _geometry(_parse(_input(rid)))
    fixed = copy.deepcopy(_references()[rid]["geometry"])
    _same(actual, fixed, "independent-descriptor-geometry")
    return actual, descriptors


def _classes():
    # Public record classes only. No optimization routine is called by this reader.
    locations = {
        "branch": ("StandardBranchStats", "AcceleratedBranchStats"),
        "oracle": ("BranchOracleStats",), "solve": ("SolveStats", "SolveResult"),
        "telemetry": ("WorkStats", "BranchTelemetry", "AlgorithmStats", "RunMetadata", "RunRecord"),
        "instance": ("Instance",), "witness": ("ExactValue", "Witness"),
    }
    return {name: getattr(importlib.import_module("exactfrac." + module), name)
            for module, names in locations.items() for name in names}


def _native_construct(cls, *args, guard, **kwargs):
    """Bind a reader rejection to closed public record algebra, not missing keys.

    Only malformed data errors from the closed record constructor are named here.
    This independent wire reader does not change producer exception contracts.
    Native resource/I/O/interrupt exceptions are deliberately not translated.
    """
    try:
        return cls(*args, **kwargs)
    except (TypeError, ValueError) as error:
        raise AssertionError(guard) from error


def _algorithm_object(obj, classes=None):
    classes = _classes() if classes is None else classes
    schema = _schema()
    _keys(obj, schema["algorithm"], "exact-algorithm-fields")
    native = obj["native"]
    _keys(native, schema["native"], "exact-native-fields")
    route = native["branch_solver"]
    _need(type(route) is str and route in _ROUTES, "native-selected-route")
    _need(type(native["attaining_candidate"]) is str, "native-attaining-type")
    _need(type(native["branch_stats"]) is list, "native-branch-list")
    branch_type = "StandardBranchStats" if route == "Standard" else "AcceleratedBranchStats"
    native_rows = []
    for row in native["branch_stats"]:
        _keys(row, schema["standard_branch" if route == "Standard" else "accelerated_branch"],
              "native-branch-fields")
        _keys(row["oracle_stats"], schema["branch_oracle"], "oracle-native-fields")
        for name, value in row.items():
            if name != "oracle_stats":
                _count(value, "native-branch-count")
        for value in row["oracle_stats"].values():
            _count(value, "native-oracle-count")
        kwargs = dict(row)
        kwargs["oracle_stats"] = _native_construct(
            classes["BranchOracleStats"], **row["oracle_stats"], guard="native-oracle-algebra",
        )
        native_rows.append(_native_construct(classes[branch_type], **kwargs,
            guard="native-branch-algebra"))
    def work(raw):
        _keys(raw, schema["work"], "all-work-fields")
        for value in raw.values():
            _count(value, "exact-work-count")
        return _native_construct(classes["WorkStats"], **raw, guard="native-work-algebra")
    _need(type(obj["branches"]) is list, "telemetry-branch-list")
    branch_rows = []
    for row in obj["branches"]:
        _keys(row, schema["branch"], "branch-schema")
        _need(type(row["branch"]) is int and row["branch"] in (0, 1, 2, 3), "branch-index")
        _need(type(row["feasible"]) is bool, "branch-feasible-bool")
        branch_rows.append(_native_construct(
            classes["BranchTelemetry"], row["branch"], row["feasible"], work(row["work"]),
            guard="native-branch-telemetry-algebra",
        ))
    for name in ("output_numerator_bits", "output_denominator_bits"):
        _count(obj[name], "output-bit-count", 1)
    native_obj = _native_construct(
        classes["SolveStats"], route, tuple(native_rows), native["attaining_candidate"],
        guard="native-solve-algebra",
    )
    return _native_construct(
        classes["AlgorithmStats"], native_obj, work(obj["total"]), work(obj["nonbranch"]),
        tuple(branch_rows), obj["output_numerator_bits"], obj["output_denominator_bits"],
        guard="native-algorithm-algebra",
    )


def _metadata_object(obj, classes=None):
    classes = _classes() if classes is None else classes
    _keys(obj, _schema()["metadata"], "all-metadata-fields")
    wall = obj["wall_clock_s"]
    _need(wall is None or (type(wall) is float and math.isfinite(wall) and wall >= 0),
          "metadata-finite-seconds")
    for name in ("python_version", "platform", "code_version", "instance_sha256"):
        _need(type(obj[name]) is str and bool(obj[name]), "metadata-nonempty-text")
    _need(obj["cpu"] is None or (type(obj["cpu"]) is str and bool(obj["cpu"])), "metadata-cpu")
    _need(re.fullmatch("[0-9a-f]{64}", obj["instance_sha256"]) is not None,
        "metadata-instance-hash")
    return _native_construct(classes["RunMetadata"], **obj, guard="native-metadata-algebra")


def _projection(value):
    if dataclasses.is_dataclass(value):
        return {field.name: _projection(getattr(value,
            field.name)) for field in dataclasses.fields(value)}
    if type(value) in (list, tuple):
        return [_projection(part) for part in value]
    return value


def _h2(algorithm, geometry):
    _algorithm_object(algorithm)
    parts = algorithm["branches"]
    if algorithm["native"]["attaining_candidate"] == "Empty":
        _same(parts, [], "empty-has-no-branches")
        for name in _schema()["event_fields"]:
            _same(algorithm["total"][name], 0, "empty-no-branch-events")
        return
    _same([part["branch"] for part in parts], [0, 1, 2, 3], "all-four-branches")
    for part, geo in zip(parts, geometry["branches"], strict=True):
        work = part["work"]
        calls = work["oracle_calls"]
        _same(work["atomic_families_enumerated"], geo["r"], "h2-enumerated")
        _same(work["atomic_families_examined"], calls * geo["r"], "h2-examined")
        for field in ("atomic_families_feasible", "parity_cut_calls"):
            _same(work[field], calls * geo["s"], "h2-feasible")
        for field in ("ordinary_min_cut_calls", "max_flow_calls"):
            _same(work[field], calls * geo["A"], "h2-reduced-cut-carrier")
        _same(part["feasible"], geo["s"] > 0, "h2-branch-feasibility")
        if not part["feasible"]:
            _same(calls, 1, "infeasible-seed-count")
    sources = [algorithm["nonbranch"], *(row["work"] for row in parts)]
    for index, field in enumerate(_schema()["work"]):
        values = [source[field] for source in sources]
        expected = sum(values) if index < 20 else max(values)
        _same(algorithm["total"][field], expected, "sum-events-max-peaks")


def _certificate_value(raw):
    cert = _parse(raw)
    _count(cert["N"], "certificate-N")
    _count(cert["D"], "certificate-D", 1)
    return cert["N"], cert["D"]


def _numerical_agreement(left, right):
    for n, d in (left, right):
        _count(n, "raw-numerator")
        _count(d, "raw-denominator", 1)
    _same(left[0] * right[1], right[0] * left[1], "cross-route-numerical-agreement")


def _row(raw, mode, files, source, environment=None):
    obj = _parse(raw, canonical=True)
    schema = _schema()
    _keys(obj, schema["run"], "exact-outer-row")
    rid, route = obj["recipe"], obj["solver"]
    _need(type(rid) is str and rid in _selected(mode), "mode-domain-recipe")
    _need(type(route) is str and route in _ROUTES, "selected-route")
    _same(obj["format"], "exactfrac-run/1", "run-format")
    _same(obj["campaign"], "unit21-v2" + ("-pilot" if mode == "pilot" else ""), "campaign")
    _need(obj["phase"] in (("pilot",) if mode == "pilot" else ("warmup", "measured")), "raw-phase")
    _count(obj["repeat"], "repeat-exact-int")
    _need(obj["repeat"] in ((0,) if obj["phase"] != "measured" else (0, 1, 2)), "repeat-domain")
    _keys(obj["input"], schema["input"], "exact-input-fields")
    _same(obj["input"], _input_metadata(rid), "input-metadata-and-actual-bits")
    # Equality alone is insufficient for bool/int leaves.
    for key, value in _input_metadata(rid).items():
        _same(obj["input"][key], value, "input-leaf-types")
    cert = obj["certificate"]
    _keys(cert, schema["certificate"], "certificate-reference-fields")
    _same(cert["path"], f"certificates/{rid}.{route}.json", "certificate-path-binding")
    _count(cert["bytes"], "certificate-byte-count", 1)
    _need(type(cert["sha256"]) is str and re.fullmatch("[0-9a-f]{64}", cert["sha256"]) is not None,
          "certificate-hash-format")
    _need(cert["path"] in files, "certificate-file-present")
    _same(_identity(files[cert["path"]]), (cert["bytes"], cert["sha256"]),
        "certificate-content-binding")
    _keys(obj["record"], schema["record"], "actual-run-record-schema")
    algorithm, metadata = obj["record"]["algorithm"], obj["record"]["metadata"]
    # Validate exact nested structures before dereferencing or comparing joins.
    classes = _classes()
    algorithm_record = _algorithm_object(algorithm, classes)
    metadata_record = _metadata_object(metadata, classes)
    _same(algorithm["native"]["branch_solver"], route, "native-route-binding")
    _same(metadata["instance_sha256"], obj["input"]["sha256"], "metadata-input-binding")
    _same(metadata["code_version"], source["code_version"], "metadata-source-binding")
    if obj["phase"] == "warmup":
        _same(obj["elapsed_ns"], None, "untimed-warmup")
        _same(metadata["wall_clock_s"], None, "untimed-warmup-metadata")
    else:
        _count(obj["elapsed_ns"], "exact-integer-elapsed")
        _same(metadata["wall_clock_s"], obj["elapsed_ns"] / 1_000_000_000, "wall-clock-seconds")
    if environment is not None:
        for field in ("python_version", "platform", "cpu"):
            _same(metadata[field], environment[field], "metadata-environment")
    record = _native_construct(classes["RunRecord"], algorithm_record, metadata_record,
                               guard="native-run-record-algebra")
    _same(_projection(record), obj["record"], "native-run-record-projection")
    geometry, _desc = _geometry_check(rid)
    _h2(algorithm, geometry)
    return obj


def _csv(header, rows):
    def field(value):
        if type(value) is bool:
            return b"true" if value else b"false"
        if type(value) is int:
            return _decimal(value)
        _need(type(value) is str and not any(c in value for c in ",\r\n\""), "unquoted-csv-field")
        return value.encode("ascii")
    return b",".join(name.encode("ascii") for name in header) + b"\n" + b"".join(
        b",".join(field(row[name]) for name in header) + b"\n" for row in rows
    )


def _reduced(n, d):
    _need(type(n) is int and type(d) is int and d > 0, "exact-rational")
    common = math.gcd(n, d)
    return {"N": n // common, "D": d // common}


def _median(values):
    _need(bool(values), "nonempty-median")
    values = sorted(values)
    middle = len(values) // 2
    return _reduced(values[middle], 1) if len(values) % 2 else _reduced(
        values[middle - 1] + values[middle], 2,
    )


def _findings(pairs, checked):
    _same(tuple(row["recipe"] for row in pairs), _selected("main"), "complete-main-comparison")
    active = [row for row in pairs if row["lookahead"] > 0]
    active_cells = {row["cell"] for row in active}
    median = _median([row["accelerated_oracle_calls"] - row["standard_oracle_calls"]
                      for row in active]) if active else None
    outcome = "untestable" if not active else (
        "supported" if len(active_cells) >= 18 and median["N"] < 0 else "not supported"
    )
    h5 = {"outcome": outcome, "active_cells": len(active_cells), "total_cells": 36,
          "eligible_recipes": len(active), "paired_difference_median": median,
          "zero_event_cells": [cell for cell in _MAIN_CELLS if cell not in active_cells]}
    def wins(suffix):
        counts = {"accelerated": 0, "tie": 0, "standard": 0}
        for pair in pairs:
            a, s = pair["accelerated_" + suffix], pair["standard_" + suffix]
            counts["accelerated" if a < s else ("standard" if a > s else "tie")] += 1
        return counts
    def top(suffix):
        chosen = sorted(pairs, key=lambda p: (-max(p["standard_" + suffix],
                                                 p["accelerated_" + suffix]), p["recipe"]))[:10]
        return [{k: p[k] for k in ("recipe", "standard_" + suffix, "accelerated_" + suffix)}
                for p in chosen]
    result = {
        "format": "exactfrac-irregular-findings/1", "campaign": "unit21-v2", "h5": h5,
        "oracle_call_wins": wins("oracle_calls"), "time_wins": wins("median_solve_ns"),
        "fewer_calls_not_faster": [p["recipe"] for p in pairs
                                  if p["accelerated_oracle_calls"] < p["standard_oracle_calls"]
                                  and p["accelerated_median_solve_ns"] >= p[
                                      "standard_median_solve_ns"]],
        "more_calls": [p["recipe"] for p in pairs
                       if p["accelerated_oracle_calls"] > p["standard_oracle_calls"]],
        "slowest_ten": top("median_solve_ns"), "largest_integer_ten": top("peak_integer_bits"),
        "h2_checked_solves": checked,
    }
    coverage = []
    for cell in _MAIN_CELLS:
        rows = [p for p in pairs if p["cell"] == cell]
        _same(len(rows), 20, "recipe-level-cell-denominator")
        ref = _references()[rows[0]["recipe"]]
        count = sum(row["lookahead"] > 0 for row in rows)
        coverage.append({"cell": cell, **{k: ref[k] for k in ("n", "tau", "b", "capacity_mode")},
                         "seeds": 20, "active_seeds": count, "coverage_N": count, "coverage_D": 20})
    return result, coverage


def _tables(mode, rows, cell_times=None):
    headers = _schema()["headers"]
    if mode == "pilot":
        solves = []
        for row in rows:
            item = {key: row["input"][key] for key in (
                "cell", "n", "m", "tau", "b", "capacity_mode", "seed", "max_q_bits",
            )}
            item.update(recipe=row["recipe"], solver=row["solver"],
                solve_elapsed_ns=row["elapsed_ns"])
            item.update({k: row["record"]["algorithm"]["total"][k] for k in (
                "oracle_calls", "lookahead_queries", "ordinary_min_cut_calls", "peak_integer_bits",
            )})
            solves.append(item)
        _need(cell_times is not None, "independently-recorded-pilot-cell-clocks-required")
        cells = []
        for cell in _CELLS:
            selected = [row for row in rows if row["input"]["cell"] == cell]
            _same(len(selected), 10, "actual-pilot-cell-calls")
            _same(len({row["recipe"] for row in selected}), 5, "actual-pilot-cell-recipes")
            cells.append({"cell": cell, **{k: selected[0]["input"][k]
                          for k in ("n", "tau", "b", "capacity_mode")},
                          "recipes": 5, "solver_calls": len(selected),
                              "cell_elapsed_ns": cell_times[cell]})
        return {"pilot-solves.csv": _csv(headers["pilot-solves"], solves),
                "pilot-cells.csv": _csv(headers["pilot-cells"], cells)}
    summaries, branches, pairs = [], [], []
    measured = collections.defaultdict(list)
    for row in rows:
        if row["phase"] == "measured":
            measured[row["recipe"], row["solver"]].append(row)
    for rid in _selected("main"):
        by_route = {}
        for route in _ROUTES:
            group = measured[rid, route]
            _same([row["repeat"] for row in group], [0, 1, 2], "all-three-measured-repeats")
            algorithm = group[0]["record"]["algorithm"]
            for row in group[1:]:
                _same(row["record"]["algorithm"], algorithm, "same-route-diagnostics")
            item = {key: value for key, value in group[0]["input"].items()
                    if key in headers["summary"]}
            item.update(recipe=rid, solver=route, repeat_count=3,
                        median_solve_ns=sorted(row["elapsed_ns"] for row in group)[1],
                        attaining_candidate=algorithm["native"]["attaining_candidate"])
            item.update(algorithm["total"])
            item.update({k: algorithm[k] for k in ("output_numerator_bits",
                "output_denominator_bits")})
            summaries.append(item)
            by_route[route] = item
            for part in algorithm["branches"]:
                branches.append({"recipe": rid, "solver": route, "branch": part["branch"],
                                 "feasible": part["feasible"], **part["work"]})
        pair = {"recipe": rid, "cell": by_route["Standard"]["cell"],
                "lookahead": by_route["Accelerated"]["lookahead_queries"]}
        for route in _ROUTES:
            for key in ("median_solve_ns", "oracle_calls", "max_flow_calls", "peak_integer_bits"):
                pair[route.lower() + "_" + key] = by_route[route][key]
        pairs.append(pair)
    findings, coverage = _findings(pairs, len(rows))
    return {"summary.csv": _csv(headers["summary"], summaries),
            "branches.csv": _csv(headers["branches"], branches),
            "comparison.csv": _csv(headers["comparison"], pairs),
            "coverage.csv": _csv(headers["coverage"], coverage),
            "findings.json": _encode(findings) + b"\n"}


def _source(images):
    registry = _parse(_bank()["SOURCE_PATHS.json"])
    _same(sorted(images), registry["ordered_paths"], "fixed-25-source-images")
    entries = [{"path": name,
        "sha256": hashlib.sha256(images[name]).hexdigest()} for name in sorted(images)]
    framing = registry["prefix"].encode() + b"".join(
        entry["path"].encode() + b"\0" + entry["sha256"].encode() + b"\n" for entry in entries
    )
    digest = hashlib.sha256(framing).hexdigest()
    return {"entries": entries, "sha256": digest,
        "code_version": "exactfrac-source-sha256:" + digest}


def _validate_source(source):
    _keys(source, _schema()["source"], "source-schema")
    paths = _parse(_bank()["SOURCE_PATHS.json"])
    _need(type(source["entries"]) is list, "source-entries-list")
    for row in source["entries"]:
        _keys(row, ("path", "sha256"), "source-entry-fields")
        _need(type(row["path"]) is str, "source-path-text")
        _need(type(row["sha256"]) is str and re.fullmatch("[0-9a-f]{64}", row["sha256"]),
            "source-hash")
    _same([row["path"] for row in source["entries"]], paths["ordered_paths"], "fixed-source-list")
    framing = paths["prefix"].encode() + b"".join(
        row["path"].encode() + b"\0" + row["sha256"].encode() + b"\n" for row in source["entries"]
    )
    _same(source["sha256"], hashlib.sha256(framing).hexdigest(), "source-fingerprint-tag-framing")
    _same(source["code_version"], "exactfrac-source-sha256:" + source["sha256"], "source-version")


def _mode_artifact_names(mode):
    """Mode inventory is determined before consuming possibly missing artifacts."""
    _need(mode in ("pilot", "main"), "inventory-declared-mode")
    names = ({"pilot.jsonl", "pilot-solves.csv", "pilot-cells.csv"} if mode == "pilot" else
             {"warmups.jsonl", "runs.jsonl", "summary.csv", "branches.csv",
              "comparison.csv", "coverage.csv", "findings.json"})
    return names | {"run-info.json", "COMPLETE.json"} | {
        f"certificates/{rid}.{route}.json" for rid in _selected(mode) for route in _ROUTES
    }


def _require_mode_inventory(files, mode):
    _same(set(files), _mode_artifact_names(mode), "mode-output-inventory")


def _audit_files(files, mode, cell_times=None, expected_source=None, expected_manifest=None,
                 checker=None, require_optimum=False):
    """Independent output consumption; synthetic inputs are never called observations."""
    _require_mode_inventory(files, mode)
    schema = _schema()
    info = _parse(files["run-info.json"], canonical=True)
    _keys(info, schema["info"], "run-info-schema")
    campaign = "unit21-v2" + ("-pilot" if mode == "pilot" else "")
    _same(info["format"], "exactfrac-experiment-info/1", "run-info-format")
    _same(info["campaign"], campaign, "run-info-campaign")
    _same(info["protocol"],
        _parse(_bank()["PROTOCOLS.json"])["campaign" if mode == "main" else "pilot"],
            "fixed-mode-protocol")
    _keys(info["environment"], schema["environment"], "environment-schema-no-private-extras")
    env = info["environment"]
    _keys(env["clock"], schema["clock"], "clock-schema")
    _same(env["clock"]["name"], "perf_counter_ns", "clock-name")
    for field in ("monotonic", "adjustable"):
        _need(type(env["clock"][field]) is bool, "clock-flag-types")
    _need(type(env["clock"]["resolution_s"]) is float
          and math.isfinite(env["clock"]["resolution_s"]) and env["clock"]["resolution_s"] > 0,
          "positive-finite-resolution")
    for key in ("int_max_str_digits", "recursion_limit"):
        _count(env[key], "environment-limit-int")
    _need(env["hash_seed"] is None or type(env["hash_seed"]) is str, "hash-seed-observation")
    for key in ("python_version", "platform"):
        _need(type(env[key]) is str and bool(env[key]), "nonempty-environment-text")
    _need(env["cpu"] is None or (type(env["cpu"]) is str and bool(env["cpu"])), "cpu-or-null")
    _validate_source(info["source"])
    if expected_source is not None:
        _same(info["source"], expected_source, "actual-source-content")
    _keys(info["inputs"], schema["inputs"], "run-info-input-fields")
    _same(info["inputs"]["suite"], "unit21-v2", "run-info-suite")
    _same(info["inputs"]["recipes"], len(_selected(mode)), "mode-selected-count")
    _same(info["inputs"]["owned_recipes"], len(_REGISTRY), "full-owned-count")
    if expected_manifest is not None:
        _same(info["inputs"]["manifest_sha256"], hashlib.sha256(expected_manifest).hexdigest(),
              "actual-aggregate-provenance-not-acceptance-pin")
    streams = ("pilot.jsonl",) if mode == "pilot" else ("warmups.jsonl", "runs.jsonl")
    rows = []
    for name in streams:
        _need(files[name].endswith(b"\n") and b"\n\n" not in files[name], "raw-lines-lf")
        current = [_row(line + b"\n", mode, files, info["source"], env)
                   for line in files[name].splitlines()]
        phase = "pilot" if mode == "pilot" else (
            "warmup" if name == "warmups.jsonl" else "measured")
        _same(tuple((r["recipe"], r["solver"], r["phase"], r["repeat"]) for r in current),
              tuple(p for p in _schedule(mode) if p[2] == phase), "full-phase-position-order")
        rows.extend(current)
    _same(len(rows), len(_schedule(mode)), "actual-successful-position-count")
    baselines, values = {}, {}
    for row in rows:
        key = row["recipe"], row["solver"]
        cert = files[row["certificate"]["path"]]
        values[key] = _certificate_value(cert)
        if checker is not None:
            _same(checker(_input(row["recipe"]), cert), None, "independent-checker-normal-return")
        if require_optimum:
            optimum = _references()[row["recipe"]]["reference_a"]["optimum"]
            _numerical_agreement(values[key], (optimum["N"], optimum["D"]))
        if row["phase"] == "warmup":
            baselines[key] = (row["record"]["algorithm"], cert)
        elif mode == "main":
            _same((row["record"]["algorithm"], cert), baselines[key], "warmup-repeat-identity")
    for rid in _selected(mode):
        _numerical_agreement(values[rid, "Standard"], values[rid, "Accelerated"])
    expected_tables = _tables(mode, rows, cell_times)
    for name, raw in expected_tables.items():
        _same(files[name], raw, "raw-to-" + name)
    certificate_names = {f"certificates/{rid}.{route}.json" for rid in _selected(
        mode) for route in _ROUTES}
    expected_names = set(streams) | set(expected_tables) | certificate_names | {"run-info.json",
        "COMPLETE.json"}
    _same(set(files), expected_names, "mode-output-inventory")
    complete = _parse(files["COMPLETE.json"], canonical=True)
    _keys(complete, schema["complete"], "complete-schema")
    counts = collections.Counter(row["phase"] for row in rows)
    expected = {
        "format": "exactfrac-irregular-complete/1", "campaign": campaign,
        "source_sha256": info["source"]["sha256"], "recipes": len(_selected(mode)),
        "warmup_solves": counts["warmup"], "measured_solves": counts["measured"],
        "pilot_solves": counts["pilot"], "checked_certificates": len(rows),
        "files": [{"path": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
                  for name, raw in sorted(files.items()) if name != "COMPLETE.json"],
    }
    _same(complete, expected, "complete-observed-counts-and-exact-ledger")
    for key in ("recipes", "warmup_solves", "measured_solves", "pilot_solves",
        "checked_certificates"):
        _count(complete[key], "complete-exact-count-types")
    return rows


def _regular_bytes(path):
    for parent in (path.parent, *path.parent.parents):
        _need(stat.S_ISDIR(parent.lstat().st_mode), "test-source-parent-not-symlink")
    mode = path.lstat().st_mode
    _need(stat.S_ISREG(mode) and not mode & 0o111, "test-source-regular-nonexecutable")
    return path.read_bytes()


@contextlib.contextmanager
def _sandbox(tmp_path):
    """Copies real candidate bytes only; never synthesizes missing production files."""
    paths = _parse(_bank()["SOURCE_PATHS.json"])["ordered_paths"]
    images = {name: _regular_bytes(_ROOT / name) for name in paths}
    before = {name: _identity(raw) for name, raw in images.items()}
    saved_modules = {name: module for name, module in sys.modules.items()
                     if name.split(".")[0] in ("exactfrac", "exactfrac_verify")}
    old_path, old_bytecode = list(sys.path), sys.dont_write_bytecode
    with tempfile.TemporaryDirectory(prefix="u21b-runner-consumer.", dir=tmp_path) as temporary:
        root = Path(temporary) / "source"
        for name, raw in images.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(raw)
        inputs = root / "instances"
        (inputs / "unit21-v2").mkdir(parents=True)
        (inputs / "MANIFEST").write_bytes(_bank()["OWN_MANIFEST"])
        for rid in _REGISTRY:
            (inputs / "unit21-v2" / (rid + ".json")).write_bytes(_input(rid))
        try:
            for name in saved_modules:
                sys.modules.pop(name)
            sys.path.insert(0, str(root))
            sys.dont_write_bytecode = True
            module = importlib.import_module(_MODULE)
            classes = _classes()
            # Consumers may use public certificate/checker classes; this is not a solve.
            certificate = importlib.import_module("exactfrac.certificate")
            check = importlib.import_module("exactfrac_verify.check")
            telemetry = importlib.import_module("exactfrac.telemetry")
            with pytest.MonkeyPatch.context() as patch:
                box = types.SimpleNamespace(
                    root=root, inputs=inputs, images=images, source=_source(images),
                    module=module, classes=classes, certificate=certificate,
                    checker=check, telemetry=telemetry, patch=patch,
                    output=root / "results" / "consumer-attempt",
                )
                _same(Path(module.__file__), root / "exactfrac/experiments_irregular.py",
                    "sandbox-origin")
                yield box
        finally:
            for name in tuple(sys.modules):
                if name.split(".")[0] in ("exactfrac", "exactfrac_verify"):
                    sys.modules.pop(name)
            sys.modules.update(saved_modules)
            sys.path[:] = old_path
            sys.dont_write_bytecode = old_bytecode
            for name, identity in before.items():
                _same(_identity(_regular_bytes(_ROOT / name)), identity,
                    "original-source-not-mutated")


def _patch_public(box, module, name, replacement):
    """Patch the public seam independent of `from` versus module import style."""
    original = getattr(module, name)
    projects = [candidate for module_name, candidate in tuple(sys.modules.items())
                if module_name.split(".")[0] in ("exactfrac", "exactfrac_verify")
                and isinstance(candidate, types.ModuleType)]
    for candidate in projects:
        for alias, value in tuple(vars(candidate).items()):
            if value is original:
                box.patch.setattr(candidate, alias, replacement)
    box.patch.setattr(module, name, replacement)
    return original


def _result_from_certificate(instance, raw, classes):
    certificate = _parse(raw)
    value = classes["ExactValue"](certificate["N"], certificate["D"])
    if certificate["empty"]:
        return classes["SolveResult"](value, None)
    y = [0] * len(instance.edges)
    for ref, count in certificate["y"]:
        y[ref] = count
    witness = classes["Witness"](sum(1 << v for v in certificate["U"]), tuple(y))
    return classes["SolveResult"](value, witness)


@functools.cache
def _fixed_rows(mode):
    files = _mode_files(mode)
    names = ("pilot.jsonl",) if mode == "pilot" else ("warmups.jsonl", "runs.jsonl")
    result = {}
    for name in names:
        for raw in files[name].splitlines():
            row = _parse(raw)
            key = row["recipe"], row["solver"], row["phase"], row["repeat"]
            _need(key not in result, "fixture-position-unique")
            result[key] = row
    _same(set(result), set(_schedule(mode)), "fixture-complete-position-set")
    return result


def _decision_algorithm(original, geometry, route, desired_calls, lookahead):
    """Valid synthetic records preserving a decision fixture's paired difference.

    Decision-only fixtures are NOT passed off as AlgorithmStats. A common positive
    offset makes both route totals attainable by the closed structural validators;
    geometry and every affected native/work/total field are rebuilt together.
    These remain artificial diagnostics, never inferred production behavior.
    """
    result = copy.deepcopy(original)
    work_fields = _schema()["work"]
    counts = [2 if g["s"] else 1 for g in geometry["branches"]]
    first = next(i for i, g in enumerate(geometry["branches"]) if g["s"])
    counts[first] += desired_calls - sum(counts)
    _need(counts[first] >= (4 if lookahead and route == "Accelerated" else 2),
        "valid-scripted-total")
    native = []
    for index, (part, geo, calls) in enumerate(zip(result["branches"], geometry["branches"],
        counts, strict=True)):
        feasible = geo["s"] > 0
        work = {field: 0 for field in work_fields}
        for field in _schema()["peak_fields"]:
            work[field] = part["work"][field]
        events = {"oracle_calls": calls, "outer_iterations": 0}
        if route == "Standard":
            outer = calls - 1 if feasible else 0
            updates = calls - 2 if feasible else 0
            events.update(outer_iterations=outer, newton_updates=updates)
            work.update(outer_iterations=outer, newton_updates=updates, newton_candidates=updates)
        else:
            la = lookahead if index == first and feasible else 0
            queries = calls - 2 - la if feasible else 0
            early = int(feasible and calls > 2)
            events.update(outer_iterations=queries, newton_queries=queries,
                          lookahead_queries=la, lookahead_accepted=0,
                          lookahead_rejected=la, early_returns=early)
            work.update(outer_iterations=queries, newton_queries=queries, newton_candidates=queries,
                        lookahead_queries=la, lookahead_rejected=la, early_returns=early,
                        newton_terminal=early, initialization_returns=int(feasible and calls == 2))
        work.update(oracle_calls=calls, atomic_families_enumerated=geo["r"],
                    atomic_families_examined=calls * geo["r"],
                        atomic_families_feasible=calls * geo["s"],
                    parity_cut_calls=calls * geo["s"], ordinary_min_cut_calls=calls * geo["A"],
                    max_flow_calls=calls * geo["A"])
        events["oracle_stats"] = {
            "atomic_families_examined": work["atomic_families_examined"],
            "atomic_families_feasible": work["atomic_families_feasible"],
            "parity_cut_calls": work["parity_cut_calls"],
                "ordinary_min_cut_calls": work["max_flow_calls"],
            "flow_augmentations": 0, "flow_bfs_scans": 0,
            "flow_peak_generated_value": work["flow_peak_generated_value"],
        }
        part["work"] = work
        native.append(events)
    result["native"]["branch_stats"] = native
    sources = [result["nonbranch"], *(b["work"] for b in result["branches"])]
    result["total"] = {
        key: (sum(s[key] for s in sources) if i < 20 else max(s[key] for s in sources))
        for i, key in enumerate(work_fields)
    }
    _h2(result, geometry)
    _same(result["total"]["oracle_calls"], desired_calls, "scripted-call-total")
    _same(result["total"]["lookahead_queries"], lookahead, "scripted-lookahead-total")
    return result


class _SolveIntervalWatch:
    """Observe excluded work, not an allowlist of permissible Python syntax.

    Arithmetic, I/O, hashing, serialization and aggregation are forbidden outside
    the single telemetry call while its clock pair is active. Dispatch, indexing,
    argument packing and exception/control transfer are not themselves classified
    as geometry. Public dependency spies supply the other semantic events. These
    finite runtime checks supplement, rather than replace, the IR20 source audit.
    """

    def __init__(self, script, source_paths):
        self.script = script
        self.source_paths = frozenset(self.filename(str(path)) for path in source_paths)
        self.helper_path = __file__
        self.active, self.allowed, self.aborted = False, False, False
        self.instructions, self.frames = {}, {}
        self.rejections = []
        self.installed = False
        self.old_trace, self.old_profile = None, None

    @staticmethod
    def filename(name):
        # co_filename is provenance, not a path to open. Preserve virtual-control
        # tags; normalize ordinary spelling without stat/read/resolve operations.
        if name.startswith("<") and name.endswith(">"):
            return name
        return os.path.normcase(os.path.abspath(os.path.normpath(name)))

    def responsible(self, frame):
        helper = self.filename(self.helper_path)
        while frame is not None:
            filename = self.filename(frame.f_code.co_filename)
            if filename == helper:
                return False
            if filename in self.source_paths:
                return True
            frame = frame.f_back
        return False

    def watching(self):
        return self.active and not self.allowed and not self.aborted

    def _remember(self, frame, delegate):
        if frame not in self.frames:
            self.frames[frame] = types.SimpleNamespace(
                delegate=delegate, lines=frame.f_trace_lines, opcodes=frame.f_trace_opcodes,
            )
        return self.frames[frame]

    def _install(self):
        if self.installed or not self.watching():
            return
        self.old_trace, self.old_profile = sys.gettrace(), sys.getprofile()
        self.installed = True
        sys.settrace(self.trace)
        sys.setprofile(self.profile)
        frame = sys._getframe(1)
        try:
            while frame is not None:
                if self.filename(frame.f_code.co_filename) in self.source_paths:
                    self._remember(frame, frame.f_trace)
                    frame.f_trace = self.trace
                    frame.f_trace_opcodes = True
                frame = frame.f_back
        finally:
            del frame

    def _restore(self):
        if not self.installed:
            return
        self.installed = False
        sys.settrace(self.old_trace)
        sys.setprofile(self.old_profile)
        for frame, state in tuple(self.frames.items()):
            frame.f_trace = state.delegate
            frame.f_trace_lines = state.lines
            frame.f_trace_opcodes = state.opcodes
        self.frames.clear()

    def start(self):
        self.active, self.aborted = True, False
        self._install()

    def end(self):
        self.active = False
        self._restore()

    def abort(self):
        # Do not replace the designated invalid-return/native-exception outcome
        # with an assertion during its exception propagation or cleanup.
        self.aborted = True
        self._restore()

    @contextlib.contextmanager
    def permitted_call(self):
        _need(not self.allowed, "single-nonnested-telemetry-call")
        self.allowed = True
        self._restore()
        normal = False
        try:
            yield
            normal = True
        finally:
            self.allowed = False
            if not normal:
                self.aborted = True
            self._install()

    def reject(self, kind, detail):
        self.rejections.append((kind, detail))
        raise AssertionError("solve-only-interval:" + kind)

    @staticmethod
    def material_opcode(instruction):
        # Python 3.14 folds subscripting into BINARY_OP. Reading a preassembled
        # argument is not arithmetic, on either side of that bytecode change.
        return (
            instruction.opname == "BINARY_OP" and instruction.argrepr != "[]"
        ) or instruction.opname in {"UNARY_NEGATIVE", "UNARY_INVERT", "UNARY_POSITIVE"}

    @staticmethod
    def excluded_library(module):
        root = module.split(".", 1)[0] if type(module) is str else ""
        return root in {
            "_hashlib", "_sha2", "_sha256", "_sha512", "_blake2", "hashlib",
            "_io", "io", "posix", "nt", "os", "pathlib", "genericpath", "posixpath", "ntpath",
            "json", "_json", "csv", "_csv", "base64", "binascii",
            "statistics", "math", "cmath", "decimal", "fractions",
        }

    def _forward(self, state, frame, event, argument):
        delegate = state.delegate
        deliver = (delegate is not None and
                   (event != "line" or state.lines) and
                   (event != "opcode" or state.opcodes))
        if deliver:
            frame.f_trace_lines, frame.f_trace_opcodes = state.lines, state.opcodes
            frame.f_trace = None if event == "call" else delegate
            replacement = delegate(frame, event, argument)
            # Preserve both returned callbacks and explicit local-trace changes.
            # A local callback returning None otherwise leaves its trace in place.
            state.delegate = replacement if replacement is not None else frame.f_trace
            state.lines, state.opcodes = frame.f_trace_lines, frame.f_trace_opcodes

    def trace(self, frame, event, argument):
        if not self.responsible(frame):
            return self.old_trace(frame, event, argument) if self.old_trace is not None else None
        state = self._remember(frame, self.old_trace if event == "call" else frame.f_trace)
        self._forward(state, frame, event, argument)
        if self.watching():
            if event == "call" and self.excluded_library(frame.f_globals.get("__name__")):
                self.reject("library-call", frame.f_globals.get("__name__"))
            if event == "opcode":
                code = frame.f_code
                if code not in self.instructions:
                    self.instructions[code] = {
                        part.offset: part for part in dis.get_instructions(code, show_caches=True)
                    }
                instruction = self.instructions[code][frame.f_lasti]
                if self.material_opcode(instruction):
                    self.reject("arithmetic", instruction.argrepr or instruction.opname)
        frame.f_trace_lines = state.lines
        frame.f_trace_opcodes = state.opcodes or self.watching()
        if event == "return":
            self.frames.pop(frame, None)
            frame.f_trace_lines, frame.f_trace_opcodes = state.lines, state.opcodes
            return state.delegate
        return self.trace

    def profile(self, frame, event, value):
        if self.old_profile is not None:
            self.old_profile(frame, event, value)
        if event != "c_call" or not self.watching() or not self.responsible(frame):
            return
        module = getattr(value, "__module__", "")
        owner = getattr(value, "__self__", None)
        name = getattr(value, "__name__", "")
        if (self.excluded_library(module) or self.excluded_library(type(owner).__module__) or
                value in (sum, min, max, sorted, any, all, divmod, pow, abs, round) or
                (isinstance(owner, (str, bytes, bytearray)) and
                 name in {"encode", "decode", "join", "format", "format_map"})):
            self.reject("c-call", name)

    @contextlib.contextmanager
    def observe(self):
        _need(not self.installed, "observer-not-already-installed")
        try:
            yield
        finally:
            self.active = False
            self._restore()


# Virtual snippets below exercise the consumer observer, not a producer, private
# runner hook or optimizer. They create no file and install no fake module.
_TIMING_CONTROL_FORMS = {
    "direct": "value = task()",
    "conditional": "value = task() if flag else task()",
    "mapping-lookup": 'value = dispatch["selected"]()',
    "argument-packing": "value = task(*arguments, **keywords)",
    "transparent-wrapper": "value = transparent()",
    "lambda-wrapper": "value = forward()",
    "callable-object": "value = callable_object()",
    "prebuilt-partial": "value = partial_task()",
    "attribute-selection": 'value = getattr(callable_object, "run")()',
}
_TIMING_EXCLUDED_WORK = {
    "input": "leaf.read_bytes()",
    "hashing": 'hashlib.sha256(b"input").digest()',
    "serialization": "json.dumps([a, b])",
    "inline-geometry": "temporary = a * b",
    "geometry-loop": "for vertex in range(a):\n    temporary = vertex + b",
    "report-aggregation": "temporary = sum((a, b))",
}


def _timing_self_control(tmp_path, form="direct", fault=None, side="before", native=False,
                         previous_callbacks=False, lexical_alias=False, outer_source=False):
    virtual = "<u21b-nonproducer-observer-control>"
    source_name = str(tmp_path / "virtual_source.py") if lexical_alias else virtual
    code_name = str(tmp_path / "unused" / ".." / "virtual_source.py") if lexical_alias else virtual
    watch = _SolveIntervalWatch(None, [source_name])
    before_global = sys.gettrace(), sys.getprofile()
    reads, tasks, tracing, profiling = [], [], [], []
    sentinel = OSError("consumer-only-native-sentinel")
    leaf = tmp_path / "observer-input"
    leaf.write_bytes(b"consumer-only input\n")
    def clock():
        reads.append(len(reads))
        if len(reads) == 1:
            watch.start()
        else:
            watch.end()
        return len(reads)
    def task():
        with watch.permitted_call():
            tasks.append("elementary-task-not-a-solver")
            value = sum(i * i for i in range(13))
            hashlib.sha256(json.dumps({"value": value}).encode()).digest()
            if native:
                raise sentinel
            return value
    def old_local(frame, event, _argument):
        if frame.f_code.co_filename == code_name:
            tracing.append((frame.f_code.co_name, event))
        return old_local
    def old_trace(frame, event, argument):
        if frame.f_code.co_filename == code_name:
            return old_local(frame, event, argument)
        return None
    def old_profile(frame, event, _argument):
        if frame.f_code.co_filename == code_name:
            profiling.append((frame.f_code.co_name, event))
    operation = "" if fault is None else _TIMING_EXCLUDED_WORK[fault] + "\n"
    code = (
        "def transparent():\n    return task()\n"
        "class Callable:\n"
        "    def __call__(self):\n        return task()\n"
        "    def run(self):\n        return task()\n"
        "def case():\n"
        "    flag = True\n    dispatch = {'selected': task}\n"
        "    arguments, keywords = (), {}\n    forward = lambda: task()\n"
        "    callable_object = Callable()\n    partial_task = functools.partial(task)\n"
        "    own = sys._getframe()\n"
        "    before = (own.f_trace, own.f_trace_lines, own.f_trace_opcodes)\n"
        "    start = clock()\n" +
        ("".join("    " + line + "\n" for line in operation.splitlines(
            )) if side == "before" else "") +
        "    " + _TIMING_CONTROL_FORMS[form] + "\n" +
        ("".join("    " + line + "\n" for line in operation.splitlines(
            )) if side == "after" else "") +
        "    end = clock()\n"
        "    after = (own.f_trace, own.f_trace_lines, own.f_trace_opcodes)\n"
        "    return value, end-start, before, after\n"
    )
    namespace = {"clock": clock, "task": task, "hashlib": hashlib, "json": json,
                 "leaf": leaf, "a": 7, "b": 11, "functools": functools, "sys": sys}
    source_watch = (_CellSourceTrace(types.SimpleNamespace(cell_active="control-cell"),
                                     {source_name: code.encode()}) if outer_source else None)
    exec(compile(code, code_name, "exec"), namespace)
    caught, result = None, None
    if previous_callbacks:
        sys.settrace(old_trace)
        sys.setprofile(old_profile)
    expected_hooks = sys.gettrace(), sys.getprofile()
    try:
        try:
            source_scope = source_watch.observe(
                ) if source_watch is not None else contextlib.nullcontext()
            with source_scope, watch.observe():
                result = namespace["case"]()
        except (AssertionError, OSError) as error:
            caught = error
        _same((sys.gettrace(), sys.getprofile()), expected_hooks, "prior-global-hooks-restored")
    finally:
        sys.settrace(before_global[0])
        sys.setprofile(before_global[1])
    _need(not watch.frames and not watch.installed, "no-retained-or-armed-frame-trace")
    if native:
        _need(caught is sentinel, "native-error-identity-not-observer-mask")
        _same(watch.rejections, [], "native-unwind-not-a-timing-rejection")
    elif fault is not None:
        _need(type(caught) is AssertionError and str(caught).startswith("solve-only-interval:"),
              "intended-timing-guard-not-earlier-failure")
        _same(len(watch.rejections), 1, "single-timing-fault-attribution")
    else:
        _same(caught, None, "dispatch-neutral-observer-positive")
        _same((reads, tasks), ([0, 1], ["elementary-task-not-a-solver"]), "control-call-counts")
        _same(result[2], result[3], "suspended-local-trace-and-flags-restored")
    if previous_callbacks:
        _need(("case", "call") in tracing, "prior-local-trace-remains-active")
        _need(("case", "call") in profiling, "prior-profile-remains-active")
        if fault is None:
            _need(("case", "return") in tracing, "prior-local-trace-valid-return")
            _need(("case", "return") in profiling, "prior-profile-valid-return")
        # A deliberately raised trace/profile guard aborts its frame's event
        # stream. Do not invent a terminal callback on a rejected control.
        # Global/local restoration is separately required above on every path.
    if source_watch is not None:
        _need(not source_watch.frames and not source_watch.installed,
            "source-observer-restored-after-nested-watch")
        _need(bool(source_watch.report()["files"][0]["operations"]),
            "source-operations-observed-with-nested-watch")
    return {"rejections": watch.rejections, "clock_calls": len(reads), "tasks": len(tasks)}


@pytest.mark.parametrize("form", tuple(_TIMING_CONTROL_FORMS))
@pytest.mark.parametrize("previous_callbacks", [False, True])
def test_timing_observer_preserves_valid_dispatch_and_existing_callbacks(tmp_path, form,
    previous_callbacks):
    _timing_self_control(tmp_path, form=form, previous_callbacks=previous_callbacks)


@pytest.mark.parametrize("fault", tuple(_TIMING_EXCLUDED_WORK))
@pytest.mark.parametrize("side", ["before", "after"])
def test_timing_observer_detects_one_excluded_operation(tmp_path, fault, side):
    _timing_self_control(tmp_path, fault=fault, side=side)


def test_timing_observer_preserves_native_exception_and_normalized_source_identity(tmp_path):
    _timing_self_control(tmp_path, native=True, previous_callbacks=True)
    _timing_self_control(tmp_path, lexical_alias=True)
    _timing_self_control(tmp_path, fault="inline-geometry", lexical_alias=True)
    # This is a classification control for the documented 3.14 representation,
    # not execution of a 3.14 interpreter or a fabricated opcode trace.
    _same(_SolveIntervalWatch.material_opcode(types.SimpleNamespace(opname="BINARY_OP",
        argrepr="[]")),
          False, "3.14-subscript-is-not-arithmetic")
    _same(_SolveIntervalWatch.material_opcode(types.SimpleNamespace(opname="BINARY_OP",
        argrepr="+")),
          True, "arithmetic-remains-observed")


_CALLBACK_CONTROL_MODES = (
    "global-no-local", "local-none-return", "local-no-lines", "local-opcodes",
    "delegate-replacement", "explicit-local-disable", "local-flag-change",
)


def _callback_continuity_control(mode):
    """Compare prior callbacks' actual event stream with and without the watch."""
    source = "<u21b-nonproducer-callback-control>"
    code = (
        "def forward():\n    return task()\n"
        "def case():\n"
        "    start = clock()\n"
        "    answer = forward()\n"
        "    end = clock()\n"
        "    return answer, end-start\n"
    )
    compiled = compile(code, source, "exec")
    before = sys.gettrace(), sys.getprofile()
    def run(observed):
        events, profiles, clocks = [], [], []
        watch = _SolveIntervalWatch(None, [source])
        def clock():
            clocks.append(len(clocks))
            if observed:
                if len(clocks) == 1:
                    watch.start()
                else:
                    watch.end()
            return len(clocks)
        def task():
            with watch.permitted_call():
                return sum(i * i for i in range(11))
        def record(label, frame, event):
            if frame.f_code.co_filename == source:
                events.append((label, frame.f_code.co_name, event, frame.f_lineno,
                               frame.f_lasti if event == "opcode" else None))
        def replacement(frame, event, _argument):
            record("replacement", frame, event)
            return replacement
        def local(frame, event, _argument):
            record("local", frame, event)
            if mode == "local-none-return":
                return None
            if mode == "delegate-replacement" and event == "line" and frame.f_lineno == 5:
                return replacement
            if mode == "explicit-local-disable" and event == "line" and frame.f_lineno == 5:
                frame.f_trace = None
                return None
            if mode == "local-flag-change" and event == "line" and frame.f_lineno == 5:
                frame.f_trace_lines = False
                frame.f_trace_opcodes = True
            return local
        def tracing(frame, event, argument):
            if frame.f_code.co_filename != source:
                return None
            record("global", frame, event)
            if mode == "global-no-local":
                return None
            if mode == "local-no-lines":
                frame.f_trace_lines = False
            if mode == "local-opcodes":
                frame.f_trace_opcodes = True
            return local
        def profiling(frame, event, _argument):
            if frame.f_code.co_filename == source:
                profiles.append((frame.f_code.co_name, event, frame.f_lineno))
        namespace = {"clock": clock, "task": task}
        exec(compiled, namespace)
        # Install an actually enabled opcode tracer in both arms. Otherwise a
        # runtime's lazy opcode activation can make the nominal baseline vacuous.
        installing = sys._getframe()
        previous_opcode_flag = installing.f_trace_opcodes
        try:
            installing.f_trace_opcodes = True
            sys.settrace(tracing)
        finally:
            installing.f_trace_opcodes = previous_opcode_flag
            del installing
        sys.setprofile(profiling)
        try:
            with watch.observe():
                # Establish an already-active prior tracer/profile pair in both
                # arms before comparing it. Warmup is an elementary control only.
                requested = observed
                observed = False
                namespace["case"]()
                events.clear()
                profiles.clear()
                clocks.clear()
                observed = requested
                value = namespace["case"]()
            _same((sys.gettrace(), sys.getprofile()), (tracing, profiling),
                "callbacks-still-installed")
        finally:
            sys.settrace(before[0])
            sys.setprofile(before[1])
        _same(watch.rejections, [], "callback-control-is-pristine")
        _need(not watch.frames and not watch.installed, "callback-control-restored-all-frames")
        return value, events, profiles
    plain = run(False)
    observed = run(True)
    _same(observed, plain, "prior-callback-event-stream-unaltered")
    if mode in {"local-opcodes", "local-flag-change"}:
        _need(any(item[2] == "opcode" for item in plain[1]), "prior-opcode-tracer-actually-active")
    return {"mode": mode, "trace_events": len(plain[1]), "profile_events": len(plain[2])}


@pytest.mark.parametrize("mode", _CALLBACK_CONTROL_MODES)
def test_timing_observer_preserves_callback_event_stream_and_flag_changes(mode):
    _callback_continuity_control(mode)


class _CellSourceTrace(_SolveIntervalWatch):
    """Actual source positions for the existing IR20 semantic audit.

    This is observation, not a geometry classifier. No private function name,
    constructor spelling or producer-side marker is required. A reviewer must
    identify the geometry's actual source operations and use their observed
    cell/clock positions; unclassified source is never called a semantic kill.
    """

    def __init__(self, script, images):
        super().__init__(script, images)
        self.images = {_SolveIntervalWatch.filename(str(name)): raw for name, raw in images.items()}
        self.ordinal = 0
        self.hits = {}
        self.marks = []

    def trace(self, frame, event, argument):
        path = self.filename(frame.f_code.co_filename)
        if path not in self.source_paths:
            return self.old_trace(frame, event, argument) if self.old_trace is not None else None
        state = self._remember(frame, self.old_trace if event == "call" else frame.f_trace)
        self._forward(state, frame, event, argument)
        if event == "opcode":
            code = frame.f_code
            if code not in self.instructions:
                self.instructions[code] = {
                    part.offset: part for part in dis.get_instructions(code, show_caches=True)
                }
            instruction = self.instructions[code][frame.f_lasti]
            self.ordinal += 1
            key = (path, code.co_qualname, instruction.offset, self.script.cell_active)
            if key not in self.hits:
                position = instruction.positions
                self.hits[key] = {
                    "qualname": code.co_qualname, "offset": instruction.offset,
                    "line": position.lineno, "end_line": position.end_lineno,
                    "column": position.col_offset, "end_column": position.end_col_offset,
                    "opcode": instruction.opname, "argument": instruction.argrepr,
                    "cell": self.script.cell_active, "first": self.ordinal,
                    "last": self.ordinal, "visits": 0,
                }
            entry = self.hits[key]
            entry["last"] = self.ordinal
            entry["visits"] += 1
        frame.f_trace_lines = state.lines
        frame.f_trace_opcodes = True
        if event == "return":
            self.frames.pop(frame, None)
            frame.f_trace_lines, frame.f_trace_opcodes = state.lines, state.opcodes
            return state.delegate
        return self.trace

    def profile(self, frame, event, argument):
        if self.old_profile is not None:
            self.old_profile(frame, event, argument)

    def mark(self, kind, index):
        self.ordinal += 1
        self.marks.append({"kind": kind, "position": index, "order": self.ordinal,
                           "cell": self.script.cell_active})

    @contextlib.contextmanager
    def observe(self):
        _need(not self.installed, "cell-source-observer-not-already-installed")
        self.active = True
        try:
            self._install()
            yield
        finally:
            self.active = False
            self._restore()

    def report(self):
        files = []
        for path, raw in sorted(self.images.items()):
            # Only a fixed source suffix or virtual control label is reported.
            name = next((suffix for suffix in ("exactfrac/experiments_irregular.py",
                                                "experiments/reproduce_irregular.py")
                         if path.endswith("/" + suffix)), "virtual-control")
            files.append({"path": name, "sha256": hashlib.sha256(raw).hexdigest(),
                          "operations": sorted((dict(value) for key, value in self.hits.items()
                                                if key[0] == path),
                                                    key=lambda value: value["first"])})
        return {"format": "exactfrac-consumer-cell-source-observation/1",
                "classification": "source-attribution-evidence; IR20 semantic review required",
                "marks": list(self.marks), "files": files}


class _InstanceStartWatch:
    """Observe public construction before work starts; do not prescribe a factory.

    Raw-data geometry has no universal public call boundary. Its actual source
    locations are retained by the separate source-attribution consumer for IR20;
    this watcher makes no claim to classify arbitrary arithmetic as geometry.
    """

    def __init__(self, script, source_paths):
        self.script = script
        self.paths = frozenset(_SolveIntervalWatch.filename(str(path)) for path in source_paths)
        self.depth = 0
        self.observer_codes = {type(self).entry.__wrapped__.__code__}
        self.bindings = {}
        self.events = []
        self.by_input = collections.defaultdict(list)
        for rid, obj in script.objects.items():
            self.by_input[(obj["n"], tuple(map(tuple, obj["edges"])), tuple(obj["f"]))].append(rid)
        self.install(script.box.patch, script.box.classes["Instance"])

    def from_runner(self):
        frame = sys._getframe(2)
        try:
            while frame is not None:
                path = _SolveIntervalWatch.filename(frame.f_code.co_filename)
                if path in self.paths:
                    return True
                if (path == _SolveIntervalWatch.filename(__file__)
                        and frame.f_code not in self.observer_codes):
                    return False
                frame = frame.f_back
            return False
        finally:
            del frame

    @contextlib.contextmanager
    def entry(self, spelling):
        outer = self.depth == 0 and self.from_runner()
        if outer:
            if self.script.mode == "pilot":
                _need(self.script.cell_active is not None, "pilot-cell-before-construction")
            self.script.event("instance", self.script.cell_active)
            self.events.append((spelling, self.script.cell_active))
        self.depth += 1
        try:
            yield outer
        finally:
            self.depth -= 1

    def bind(self, instance):
        _need(type(instance) is self.script.box.classes["Instance"], "constructor-exact-instance")
        key = instance.n, instance.edges, instance.f
        matches = self.by_input.get(key, ())
        _need(bool(matches), "instance-uses-retained-decoded-input")
        if self.script.mode == "pilot":
            _need(any(rid.rsplit("-", 1)[0] == self.script.cell_active for rid in matches),
                  "cell-instance-input-binding")
        # Retain the object itself as well as id: an id cannot be recycled into a
        # spurious construction record. Equal payloads remain distinct recipes.
        self.bindings[id(instance)] = instance, self.script.cell_active

    def require(self, instance, rid):
        if self.script.mode != "pilot":
            return
        value = self.bindings.get(id(instance))
        _need(value is not None and value[0] is instance, "pilot-instance-construction-observed")
        _same(value[1], rid.rsplit("-", 1)[0], "pilot-cell-instance-reuse")

    def install(self, patch, cls):
        original_init = cls.__init__
        original_dict = cls.from_dict.__func__
        original_records = cls.from_records.__func__

        def initialize(instance, *args, **kwargs):
            with self.entry("Instance") as outer:
                result = original_init(instance, *args, **kwargs)
                if outer:
                    self.bind(instance)
                return result

        def from_dict(kind, data):
            with self.entry("from_dict") as outer:
                result = original_dict(kind, data)
                if outer:
                    self.bind(result)
                return result

        def from_records(kind, *args, **kwargs):
            with self.entry("from_records") as outer:
                result = original_records(kind, *args, **kwargs)
                if outer:
                    self.bind(result)
                return result

        self.observer_codes.update((initialize.__code__, from_dict.__code__, from_records.__code__))
        patch.setattr(cls, "__init__", initialize)
        patch.setattr(cls, "from_dict", classmethod(from_dict))
        patch.setattr(cls, "from_records", classmethod(from_records))


class _Script:
    """A full-position public-seam script, with no call-through to any solver."""

    def __init__(self, box, mode, decision=None, giant=False, zero_intervals=False):
        self.box, self.mode = box, mode
        self.positions, self.rows = _schedule(mode), _fixed_rows(mode)
        self.files = _mode_files(mode)
        self.inputs = {rid: _input(rid) for rid in _REGISTRY}
        self.objects = {rid: _parse(self.inputs[rid]) for rid in _REGISTRY}
        self.decision = None if decision is None else {p["recipe"]: p for p in decision["pairs"]}
        self.giant = _parse(_bank()["SYNTHETIC_GIANT_ROW.jsonl"]) if giant else None
        self.zero_intervals = zero_intervals
        self.record_positions = []
        self.calls, self.checked, self.built, self.serialized, self.records = [], [], [], [], []
        self.events, self.discovery = [], collections.Counter()
        self.instances, self.clock_index = {}, 0
        self.clock_active, self.cell_active = False, None
        self.return_fault = None
        self.raise_at = None
        self.exception = None
        self.after_check = None
        self.checker_return_fault = None
        self.checker_returns = []
        self.clock_fault = None
        self.cell_source = None
        self.clock_events = []
        self.cell_times = {}
        clocks = {x["cell"]: x for x in _parse(_bank()["SYNTHETIC_PILOT_CELL_CLOCKS.json"])}
        moment = 0
        for index, position in enumerate(self.positions):
            _rid, _route, phase, _repeat = position
            cell = self.rows[position]["input"]["cell"]
            if mode == "pilot" and index % 10 == 0:
                c = clocks[cell]
                self.clock_events.append(("cell-start", index, c["start_ns"]))
                self.cell_times[cell] = c["end_ns"] - c["start_ns"]
                moment = c["start_ns"] + 100
            if phase != "warmup":
                elapsed = self.elapsed(position)
                self.clock_events.extend((("solve-start", index, moment), ("solve-end", index,
                    moment + elapsed)))
                moment += elapsed + 1
            if mode == "pilot" and index % 10 == 9:
                self.clock_events.append(("cell-end", index, clocks[cell]["end_ns"]))
        self._install()

    def elapsed(self, position):
        rid, route, phase, _repeat = position
        if phase == "warmup":
            return None
        if self.zero_intervals:
            return 0
        if self.decision is not None:
            return self.decision[rid][route.lower() + "_median_solve_ns"]
        return self.rows[position]["elapsed_ns"]

    def event(self, name, detail=None):
        _need(not self.clock_active, "solve-interval-excludes-" + name)
        self.events.append((name, detail))
        if self.raise_at == name:
            raise self.exception

    def clock(self):
        _need(self.clock_index < len(self.clock_events), "no-extra-clock-read")
        kind, index, value = self.clock_events[self.clock_index]
        if self.cell_source is not None:
            self.cell_source.mark(kind, index)
        self.clock_index += 1
        if kind == "solve-start":
            _same(len(self.calls), index, "clock-immediately-before-position")
            self.clock_active = True
            self.boundary.start()
        elif kind == "solve-end":
            _same(len(self.calls), index + 1, "clock-immediately-after-position")
            _need(self.clock_active, "paired-solve-clock")
            self.clock_active = False
            self.boundary.end()
        elif kind == "cell-start":
            _same(len(self.calls), index, "cell-start-position")
            self.cell_active = self.rows[self.positions[index]]["input"]["cell"]
            _need(not any(x[0] == "instance" and x[1] == self.cell_active for x in self.events),
                  "cell-start-before-first-instance")
        else:
            _same(len(self.checked), index + 1, "cell-end-after-last-check")
            _need(any(event == ("row-flush", index) for event in self.events),
                "cell-end-after-last-row-flush")
            self.output_monitor.cell_end(index)
            self.cell_active = None
        self.events.append((kind, index))
        if self.raise_at == "clock":
            self.boundary.abort()
            raise self.exception
        if self.clock_fault is not None:
            value = self.clock_fault(kind, index, value)
            if type(value) is not int:
                self.boundary.abort()
        return value

    def solve(self, instance, branch_solver):
        with self.boundary.permitted_call():
            return self._solve_response(instance, branch_solver)

    def _solve_response(self, instance, branch_solver):
        route = branch_solver
        index = len(self.calls)
        _need(index < len(self.positions), "no-extra-telemetry-call")
        rid, expected_route, phase, _repeat = self.positions[index]
        _same(route, expected_route, "exact-scripted-route-order")
        _need(type(instance) is self.box.classes["Instance"], "actual-instance-type")
        self.construction.require(instance, rid)
        obj = self.objects[rid]
        _same((instance.n, instance.edges, instance.f),
              (obj["n"], tuple(map(tuple, obj["edges"])), tuple(obj["f"])), "scripted-input-order")
        self.instances[id(instance)] = instance
        _same(self.clock_active, phase != "warmup", "warmup-has-no-clock")
        self.calls.append((rid, route, phase, self.positions[index][3]))
        if self.raise_at == "solve":
            raise self.exception
        row = self.rows[self.positions[index]]
        algorithm = row["record"]["algorithm"]
        if self.giant is not None and (rid, route) == (self.giant["recipe"], self.giant["solver"]):
            algorithm = self.giant["record"]["algorithm"]
        if self.decision is not None:
            pair = self.decision[rid]
            algorithm = _decision_algorithm(
                algorithm, _references()[rid]["geometry"], route,
                pair[route.lower() + "_oracle_calls"] + 100,
                pair["lookahead"] if route == "Accelerated" else 0,
            )
        result = _result_from_certificate(instance, self.files[row["certificate"]["path"]],
            self.box.classes)
        stats = _algorithm_object(algorithm, self.box.classes)
        response = (result, stats)
        return self.return_fault(index, response) if self.return_fault is not None else response

    def _install(self):
        box = self.box
        self.boundary = _SolveIntervalWatch(self, [box.root / name for name in box.images])
        box.boundary = self.boundary
        _patch_public(box, box.telemetry, "solve_with_telemetry", self.solve)
        # A bare solve or any secondary optimization is an immediate fixture failure.
        def never_solve(*_args, **_kwargs):
            raise AssertionError("prohibited-real-or-second-solve-in-scripted-scenario")
        for module_name, name in (("telemetry", "solve"), ("solve", "solve"), ("branch",
            "solve_branch_standard"),
                                  ("branch", "solve_branch_accelerated")):
            module = importlib.import_module("exactfrac." + module_name)
            _patch_public(box, module, name, never_solve)
        self.construction = _InstanceStartWatch(
            self, [box.root / "exactfrac/experiments_irregular.py",
                   box.root / "experiments/reproduce_irregular.py"],
        )
        build = box.certificate.build_certificate
        def build_spy(instance, result):
            self.event("certificate-build")
            self.built.append((instance, result))
            return build(instance, result)
        _patch_public(box, box.certificate, "build_certificate", build_spy)
        serialize = box.certificate.serialize_certificate
        def serialize_spy(instance, certificate):
            self.event("certificate-serialize")
            raw = serialize(instance, certificate)
            self.serialized.append(raw)
            return raw
        _patch_public(box, box.certificate, "serialize_certificate", serialize_spy)
        check = box.checker.verify_certificate
        def check_spy(instance, certificate):
            raw = instance
            self.event("checker")
            index = len(self.checked)
            _need(index < len(self.positions), "unexpected-checker-call")
            rid = self.positions[index][0]
            _same(raw, self.inputs[rid], "checked-retained-input-buffer")
            # The real independent C0 checker is retained. It is not an optimizer.
            response = check(raw, certificate)
            _same(response, None, "actual-c0-checker")
            self.checked.append((raw, certificate))
            if self.after_check is not None:
                self.after_check(index)
            selected = False if self.raise_at == "checker-false" else response
            if self.checker_return_fault is not None:
                selected = self.checker_return_fault(index, selected)
            self.checker_returns.append((index, selected))
            return selected
        _patch_public(box, box.checker, "verify_certificate", check_spy)
        original_record = box.classes["RunRecord"].__post_init__
        def record_spy(record):
            self.event("run-record")
            original_record(record)
            self.records.append(record)
            self.record_positions.append(len(self.calls) - 1)
        box.patch.setattr(box.classes["RunRecord"], "__post_init__", record_spy)
        _patch_public(box, time, "perf_counter_ns", self.clock)
        for name, value in (("python_version", "SYNTHETIC-PYTHON"),
                            ("platform", "SYNTHETIC-PLATFORM"), ("processor", "")):
            def discover(*_args, _name=name, _value=value, **_kwargs):
                self.event("environment", _name)
                self.discovery[_name] += 1
                return _value
            _patch_public(box, platform, name, discover)
        def clock_info(name):
            self.event("environment", "clock_info")
            _same(name, "perf_counter", "clock-info-name")
            self.discovery["clock_info"] += 1
            return types.SimpleNamespace(monotonic=True, adjustable=False, resolution=1e-9)
        _patch_public(box, time, "get_clock_info", clock_info)
        self.environment = {
            "python_version": "SYNTHETIC-PYTHON", "platform": "SYNTHETIC-PLATFORM", "cpu": None,
            "clock": {"name": "perf_counter_ns", "monotonic": True, "adjustable": False,
                "resolution_s": 1e-9},
            "int_max_str_digits": sys.get_int_max_str_digits(),
                "recursion_limit": sys.getrecursionlimit(),
            "hash_seed": os.environ.get("PYTHONHASHSEED"),
        }

    def finished(self):
        _same(tuple(self.calls), self.positions, "complete-observed-scripted-schedule")
        _same(len(self.checked), len(self.positions), "one-real-c0-check-per-position")
        _same(len(self.built), len(self.positions), "one-certificate-build-per-position")
        _same(len(self.serialized), len(self.positions), "one-serialization-per-position")
        # End-of-run validation may legitimately construct additional native
        # records. Require per-position construction, not exactly N constructors.
        _same(set(self.record_positions), set(range(len(self.positions))),
              "actual-run-record-covers-every-position")
        _need(all(type(record) is self.box.classes["RunRecord"] for record in self.records),
              "all-observed-run-records-have-exact-type")
        _same(self.clock_index, len(self.clock_events), "complete-clock-schedule")
        _same(dict(self.discovery), {"python_version": 1, "platform": 1, "processor": 1,
            "clock_info": 1},
              "once-per-invocation-environment-discovery")
        _need(not self.clock_active and self.cell_active is None, "all-intervals-closed")


class _ObservedFile:
    def __init__(self, monitor, stream, path, writing, descriptor, closefd):
        self.monitor, self.stream, self.path, self.writing = monitor, stream, path, writing
        self.descriptor, self.closefd = descriptor, closefd
        self.closed_ok = False

    def __getattr__(self, name):
        return getattr(self.stream, name)

    def __enter__(self):
        self.stream.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

    def __iter__(self):
        return iter(self.stream)

    def write(self, raw):
        with self.monitor.operation("write", self.path) as outer:
            # A buffering layer can pass a memoryview to a raw stream. Observing
            # that public I/O buffer does not change the producer's wire bytes.
            offered = self.monitor.buffer_bytes(raw)
            if outer:
                self.monitor.trigger("write", self.path)
                if self.monitor.bad_write:
                    self.monitor.bad_write_hits.append(self.path)
                    return self.monitor.bad_write[0]
                if self.monitor.short_write:
                    raw = offered[:max(1, len(offered) // 2)]
            count = self.stream.write(raw)
            if (type(count) is int and 0 < count <= len(offered)
                    and isinstance(self.stream, io.RawIOBase)):
                self.monitor.settled(self.path)
            return count

    def flush(self):
        with self.monitor.operation("flush", self.path) as outer:
            result = self.stream.flush()
            if self.writing:
                self.monitor.settled(self.path)
            if outer:
                self.monitor.flush_hits.append(self.path)
                self.monitor.trigger("flush", self.path)
                if self.monitor.bad_flush:
                    self.monitor.bad_flush_hits.append(self.path)
                    return self.monitor.bad_flush[0]
            return result

    def close(self):
        if self.stream.closed:
            return None
        with self.monitor.operation("close", self.path) as outer:
            result = self.stream.close()
            if self.writing:
                # Successful close drains its buffer; no fictional flush call.
                self.monitor.settled(self.path)
            self.closed_ok = True
            if self.closefd:
                self.monitor.descriptor_closed(self.descriptor)
            if outer:
                self.monitor.trigger("close", self.path)
            return result

    def seek(self, *args, **kwargs):
        with self.monitor.operation("seek", self.path):
            result = self.stream.seek(*args, **kwargs)
            if self.writing:
                self.monitor.row_streams.pop(self.path, None)
            return result

    def truncate(self, *args, **kwargs):
        with self.monitor.operation("truncate", self.path):
            result = self.stream.truncate(*args, **kwargs)
            if self.writing:
                self.monitor.row_streams.pop(self.path, None)
            return result

    def detach(self):
        # detach transfers ownership rather than closing the underlying raw
        # object. That raw handle/descriptor must still close before COMPLETE.
        with self.monitor.operation("detach", self.path):
            raw = self.stream.detach()
            if self.writing:
                self.monitor.settled(self.path)
            self.closed_ok = True
            return raw


class _OutputMonitor:
    """Observe real binary streams/descriptors without prescribing a private API.

    A direct os.write has no user-space buffer and therefore no buffered flush
    return to mutate. Flush tests must distinguish that completed positive path
    from a reached flush seam; close failures remain applicable to both backends.
    """

    def __init__(self, box, script):
        self.box, self.script = box, script
        self.handles, self.opened, self.descriptors = [], [], {}
        self.directory_fd_paths, self.pending_streams = {}, []
        self.flushed_bytes, self.flushed_by_path = {}, {}
        self.operation_depth = 0
        self.row_streams = {}
        self.flushed_positions = set()
        self.position_indices = {p: i for i, p in enumerate(script.positions)}
        self.fail_stage, self.fail_name, self.exception = None, None, None
        self.failures, self.flush_hits, self.bad_write_hits, self.bad_flush_hits = [], [], [], []
        self.bad_write, self.bad_flush, self.short_write = (), (), False
        self.complete_seen = False
        self.creation_failure = None
        self.creation_failures, self.permission_calls = [], []
        self.preexisting_ancestors = frozenset(
            path for path in box.output.parents if os.path.lexists(path)
        )
        original_builtin, original_io = builtins.open, io.open
        original_raw, original_buffered = io.FileIO, io.BufferedWriter
        low_io = importlib.import_module("_io")
        self.unobserved_open = original_builtin
        original_os_open, original_write, original_close = os.open, os.write, os.close
        original_mkdir, original_chmod, original_fchmod = os.mkdir, os.chmod, os.fchmod
        original_dup, original_dup2 = os.dup, os.dup2
        original_closerange, original_lseek = os.closerange, os.lseek
        original_writev = getattr(os, "writev", None)

        def stream_open(original, raw_constructor=False):
            def opened(file, mode="r", *args, **kwargs):
                state = self.descriptors.get(file) if type(file) is int else None
                path = (state.path if state is not None else
                        None if isinstance(file, int) else self.resolve(file))
                watched = path is not None and self.is_output(path)
                writing = any(c in mode for c in "wax+")
                pending = None
                if watched:
                    if state is None:
                        self.script.event("output-open", path)
                        self.trigger("open", path)
                        if writing:
                            _need("x" in mode and (raw_constructor or "b" in mode),
                                  "exclusive-binary-output")
                            self.creation(path)
                        pending = types.SimpleNamespace(path=path, writing=writing)
                    else:
                        _need(raw_constructor or "b" in mode, "descriptor-binary-output")
                if pending is not None:
                    self.pending_streams.append(pending)
                try:
                    stream = original(file, mode, *args, **kwargs)
                finally:
                    if pending is not None:
                        _need(self.pending_streams.pop() is pending, "balanced-opener-observation")
                if not watched or isinstance(stream, _ObservedFile):
                    return stream
                fd = stream.fileno()
                current = self.descriptors.get(fd)
                if current is None:
                    current = self.register_descriptor(fd, path, writing)
                else:
                    _same(current.path, path, "output-opener-target-conserved")
                # file=fd can intentionally leave descriptor ownership with its
                # caller. Track the stream and the still-live descriptor separately.
                close_index = 0 if raw_constructor else 4
                closefd = kwargs.get("closefd",
                    args[close_index] if len(args) > close_index else True)
                handle = _ObservedFile(self, stream, path, writing, fd, closefd)
                self.handles.append(handle)
                return handle
            return opened

        def descriptor_open(path, flags, mode=0o777, *, dir_fd=None):
            absolute = self.resolve(path, dir_fd)
            writing = bool(flags & (
                os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
            watched = self.is_output(absolute)
            pending = self.pending_streams[-1] if self.pending_streams else None
            if pending is not None:
                _same(absolute, pending.path, "output-opener-target-conserved")
            if watched:
                if pending is None:
                    self.script.event("output-open", absolute)
                    self.trigger("open", absolute)
                if writing:
                    _need(flags & os.O_EXCL and flags & os.O_CREAT and
                          not flags & (os.O_TRUNC | os.O_APPEND), "exclusive-descriptor-output")
                    if pending is None:
                        self.creation(absolute)
            fd = original_os_open(path, flags, mode, dir_fd=dir_fd)
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                self.directory_fd_paths[fd] = absolute
            if watched:
                self.register_descriptor(fd, absolute, writing)
            return fd

        def descriptor_write(fd, raw):
            state = self.descriptors.get(fd)
            if state is None:
                return original_write(fd, raw)
            with self.operation("write", state.path) as outer:
                offered = self.buffer_bytes(raw)
                if outer:
                    self.trigger("write", state.path)
                    if self.bad_write:
                        self.bad_write_hits.append(state.path)
                        return self.bad_write[0]
                    if self.short_write:
                        raw = offered[:max(1, len(offered) // 2)]
                result = original_write(fd, raw)
                if type(result) is int and 0 < result <= len(offered):
                    self.settled(state.path)
                return result

        def descriptor_writev(fd, buffers):
            state = self.descriptors.get(fd)
            if state is None:
                return original_writev(fd, buffers)
            with self.operation("write", state.path) as outer:
                pieces = tuple(self.buffer_bytes(part) for part in buffers)
                offered = sum(map(len, pieces))
                if outer:
                    self.trigger("write", state.path)
                    if self.bad_write:
                        self.bad_write_hits.append(state.path)
                        return self.bad_write[0]
                    if self.short_write:
                        pieces = (b"".join(pieces)[:max(1, offered // 2)],)
                result = original_writev(fd, pieces)
                if type(result) is int and 0 < result <= offered:
                    self.settled(state.path)
                return result

        def descriptor_close(fd):
            state = self.descriptors.get(fd)
            if state is None:
                result = original_close(fd)
                self.descriptor_closed(fd)
                return result
            with self.operation("close", state.path) as outer:
                result = original_close(fd)
                self.descriptor_closed(fd)
                if state.writing:
                    self.settled(state.path)
                if outer:
                    self.trigger("close", state.path)
                return result

        def descriptor_range_close(low, high):
            states = [(fd, state) for fd, state in sorted(self.descriptors.items())
                      if low <= fd < high]
            for _fd, state in states:
                self.script.event("output-close", state.path)
            result = original_closerange(low, high)
            for fd in tuple(self.directory_fd_paths):
                if low <= fd < high:
                    self.descriptor_closed(fd)
            for fd, state in states:
                self.descriptor_closed(fd)
                if state.writing:
                    self.settled(state.path)
                self.trigger("close", state.path)
            return result

        def descriptor_seek(fd, position, how):
            state = self.descriptors.get(fd)
            result = original_lseek(fd, position, how)
            if state is not None and state.writing:
                self.row_streams.pop(state.path, None)
            return result

        def buffered_writer(raw, buffer_size=io.DEFAULT_BUFFER_SIZE):
            # io.BufferedWriter is a valid composition over both an observed
            # FileIO and an observed open(..., buffering=0). Keep the raw handle
            # separately so detach/closefd=False cannot invent descriptor closure.
            stream = original_buffered(raw, buffer_size)
            state = self.descriptors.get(stream.fileno())
            if state is None:
                return stream
            closefd = raw.closefd if isinstance(raw, _ObservedFile) else getattr(raw, "closefd",
                True)
            handle = _ObservedFile(self, stream, state.path, True, stream.fileno(), closefd)
            self.handles.append(handle)
            return handle

        def duplicate_state(old, new):
            if old in self.directory_fd_paths:
                self.directory_fd_paths[new] = self.directory_fd_paths[old]
            if old in self.descriptors:
                state = self.descriptors[old]
                self.register_descriptor(new, state.path, state.writing)
            return new

        def duplicate(fd):
            return duplicate_state(fd, original_dup(fd))

        def duplicate_to(fd, fd2, inheritable=True):
            # Preserve POSIX dup2(fd, fd); replacing another live fd closes it.
            result = original_dup2(fd, fd2, inheritable=inheritable)
            if fd != fd2:
                self.descriptor_closed(fd2)
                duplicate_state(fd, fd2)
            return result

        def make_directory(path, mode=0o777, *, dir_fd=None):
            absolute = self.resolve(path, dir_fd)
            if self.is_output(absolute):
                self.script.event("output-mkdir", absolute)
                if absolute == self.box.output and self.creation_failure is not None:
                    error = self.creation_failure
                    self.creation_failure = None
                    self.creation_failures.append(absolute)
                    raise error
            return original_mkdir(path, mode, dir_fd=dir_fd)

        def permissions(path, mode, *, dir_fd=None, follow_symlinks=True):
            absolute = self.resolve(path, dir_fd)
            self.permission_calls.append(("chmod", absolute))
            _need(absolute not in self.preexisting_ancestors, "no-existing-output-parent-chmod")
            return original_chmod(path, mode, dir_fd=dir_fd, follow_symlinks=follow_symlinks)

        def descriptor_permissions(fd, mode):
            path = (self.directory_fd_paths.get(fd) or
                    (self.descriptors[fd].path if fd in self.descriptors else None))
            self.permission_calls.append(("fchmod", path))
            _need(path is not None, "permission-descriptor-observed")
            _need(path not in self.preexisting_ancestors, "no-existing-output-parent-chmod")
            return original_fchmod(fd, mode)

        for owner, name, value in (
            (builtins, "open", stream_open(original_builtin)),
            (io, "open", stream_open(original_io)),
            (io, "FileIO", stream_open(original_raw, raw_constructor=True)),
            (io, "BufferedWriter", buffered_writer),
            (low_io, "open", stream_open(original_io)),
            (low_io, "FileIO", stream_open(original_raw, raw_constructor=True)),
            (low_io, "BufferedWriter", buffered_writer),
            (os, "open", descriptor_open), (os, "write", descriptor_write),
            (os, "close", descriptor_close), (os, "closerange", descriptor_range_close),
            (os, "dup", duplicate), (os, "lseek", descriptor_seek),
            (os, "dup2", duplicate_to), (os, "mkdir", make_directory),
            (os, "chmod", permissions), (os, "fchmod", descriptor_permissions),
        ):
            _patch_public(box, owner, name, value)
        if original_writev is not None:
            _patch_public(box, os, "writev", descriptor_writev)
        script.output_monitor = self

    def resolve(self, path, dir_fd=None):
        if type(path) is int:
            _need(path in self.directory_fd_paths or path in self.descriptors,
                  "observer-path-descriptor-was-opened-in-scope")
            return (self.directory_fd_paths[path] if path in self.directory_fd_paths
                    else self.descriptors[path].path)
        pathname = Path(os.fsdecode(path))
        if pathname.is_absolute() or dir_fd is None:
            return pathname.absolute()
        _need(dir_fd in self.directory_fd_paths, "observer-directory-fd-was-opened-in-scope")
        return self.directory_fd_paths[dir_fd] / pathname

    def register_descriptor(self, fd, path, writing):
        _need(fd not in self.descriptors, "descriptor-registration-is-unique")
        state = types.SimpleNamespace(path=path, writing=writing, closed_ok=False)
        self.descriptors[fd] = state
        self.handles.append(state)
        return state

    def descriptor_closed(self, fd):
        self.directory_fd_paths.pop(fd, None)
        state = self.descriptors.pop(fd, None)
        if state is not None:
            state.closed_ok = True

    def is_output(self, path):
        return path == self.box.output or self.box.output in path.parents

    @staticmethod
    def buffer_bytes(raw):
        # Mirror the binary buffer accepted by the stdlib, without a str codec.
        return bytes(memoryview(raw))

    @contextlib.contextmanager
    def operation(self, stage, path):
        outer = self.operation_depth == 0
        self.operation_depth += 1
        try:
            if outer:
                self.script.event("output-" + stage, path)
            yield outer
        finally:
            self.operation_depth -= 1

    def settled(self, path):
        # Read bytes actually visible after a drain, not concatenated write
        # arguments. For a log, read only new bytes and parse each row once;
        # rereading the full 7,680-position trace at every flush is quadratic.
        is_log = path.name in ("pilot.jsonl", "warmups.jsonl", "runs.jsonl")
        with self.unobserved_open(path, "rb") as stream:
            if not is_log or not self.position_indices:
                self.flushed_bytes[path] = stream.read()
                return
            state = self.row_streams.get(path)
            size = os.fstat(stream.fileno()).st_size
            if state is None or size < state.offset:
                state = types.SimpleNamespace(offset=0, partial=b"", positions=set())
                self.row_streams[path] = state
            stream.seek(state.offset)
            new = stream.read()
        state.offset += len(new)
        combined = state.partial + new
        cutoff = combined.rfind(b"\n") + 1
        state.partial = combined[cutoff:]
        old = set(state.positions)
        for line in combined[:cutoff].splitlines(keepends=True):
            row = _parse(line)
            position = row["recipe"], row["solver"], row["phase"], row["repeat"]
            _need(position in self.position_indices, "flushed-row-is-an-actual-position")
            index = self.position_indices[position]
            _need(index < len(self.script.checked), "row-flush-follows-its-checker")
            _need(index not in state.positions, "flushed-row-position-is-unique")
            state.positions.add(index)
        self.flushed_by_path[path] = state.positions
        self.flushed_positions = set().union(*self.flushed_by_path.values())
        for index in sorted(state.positions - old):
            self.script.events.append(("row-flush", index))

    def cell_end(self, index):
        for position in range(index - 9, index + 1):
            _need(position in self.flushed_positions, "cell-end-after-every-complete-row-flush")
            rid, route, _phase, _repeat = self.script.positions[position]
            path = self.box.output / "certificates" / (rid + "." + route + ".json")
            _same(self.flushed_bytes.get(path), self.script.checked[position][1],
                  "cell-end-after-every-certificate-flush")

    def creation(self, path):
        _need(not self.complete_seen, "complete-created-last")
        if path.name == "COMPLETE.json":
            _need(all(h.closed_ok for h in self.handles if h.writing), "complete-after-prior-close")
            _same(len(self.script.checked), len(self.script.positions), "complete-after-all-checks")
            self.complete_seen = True
        self.opened.append(path)

    def trigger(self, stage, path):
        if self.fail_stage == stage and (self.fail_name is None or path.name == self.fail_name):
            error = self.exception
            # Snapshot actual bytes before raising, using the pre-monitor reader.
            # This must not register a new producer output-read or mask its error.
            try:
                with self.unobserved_open(path, "rb") as stream:
                    partial = stream.read()
            except FileNotFoundError:
                partial = None
            if (path.name == "COMPLETE.json" and stage in ("flush", "close")
                    and self.fail_name == "COMPLETE.json"):
                # Select the registered *late* marker failure. A harmless early
                # flush or duplicated-descriptor release is not that seam.
                try:
                    _parse(partial)
                except AssertionError:
                    return
            self.fail_stage = None
            self.failures.append((stage, path, partial))
            raise error

    def finished(self):
        _need(self.complete_seen, "complete-marker-observed")
        _need(all(h.closed_ok for h in self.handles), "all-output-streams-closed")


def _output_files(root):
    _need(root.is_dir() and not root.is_symlink(), "output-root-kind")
    result = {}
    for parent, directories, files in os.walk(root):
        for name in directories:
            _need(stat.S_ISDIR((Path(parent) / name).lstat().st_mode), "output-parent-not-symlink")
        for name in files:
            path = Path(parent) / name
            result[path.relative_to(root).as_posix()] = _regular_bytes(path)
    return result


def _invoke(box, mode, extras=(), argv=None):
    original_path = list(sys.path)
    settings = sys.get_int_max_str_digits(), sys.getrecursionlimit()
    command = ["--all" if mode == "main" else "--pilot", "--instances", str(box.inputs),
               "--output", str(box.output), *extras] if argv is None else argv
    watch = getattr(box, "boundary", None)
    observation = contextlib.nullcontext() if watch is None else watch.observe()
    source_watch = getattr(box, "cell_source", None)
    source_observation = contextlib.nullcontext(
        ) if source_watch is None else source_watch.observe()
    try:
        with source_observation, observation:
            result = box.module.main(command)
    finally:
        _same(sys.path, original_path, "runner-sys-path-restored")
        _same((sys.get_int_max_str_digits(), sys.getrecursionlimit()), settings,
            "settings-conserved")
    return result


def _execute_scripted_case(tmp_path, mode, decision=None, giant=False, short_write=False,
                           manifest_transform=None, alternate=False, zero_intervals=False,
                           invocation="absolute", unrelated=False, source_attribution=False):
    with _sandbox(tmp_path) as box:
        if manifest_transform is not None:
            manifest = manifest_transform(_parse((box.inputs / "MANIFEST").read_bytes()))
            (box.inputs / "MANIFEST").write_bytes(manifest)
        if alternate:
            box.output = box.root.parent / "disjoint-output"
        caller = box.root.parent / "caller"
        caller.mkdir()
        if invocation == "default":
            box.output = box.root / "results" / (
                "unit21-v2-pilot" if mode == "pilot" else "unit21-v2")
            argv = ["--pilot" if mode == "pilot" else "--all"]
        elif invocation.startswith("relative"):
            relocated = caller / "inputs"
            box.inputs.rename(relocated)
            box.inputs = relocated
            box.output = caller / "fresh-output"
            options = ["--instances", "inputs", "--output", "fresh-output"]
            if invocation == "relative-output-first":
                options = options[2:] + options[:2]
            argv = ["--pilot" if mode == "pilot" else "--all", *options]
        else:
            _same(invocation, "absolute", "declared-invocation-form")
            argv = None
        if unrelated:
            (box.inputs / "unrelated").mkdir()
            (box.inputs / "unrelated" / "keep").write_bytes(b"unowned-content\n")
            (box.inputs / "unrelated-file").write_bytes(b"also-unowned\n")
        script = _Script(box, mode, decision=decision, giant=giant, zero_intervals=zero_intervals)
        monitor = _OutputMonitor(box, script)
        if source_attribution:
            _same(mode, "pilot", "cell-source-observation-is-pilot-only")
            script.cell_source = _CellSourceTrace(script, {
                box.root / name: box.images[name] for name in (
                    "exactfrac/experiments_irregular.py", "experiments/reproduce_irregular.py",
                )
            })
            box.cell_source = script.cell_source
        monitor.short_write = short_write
        with contextlib.chdir(caller), _standard_streams() as (out, err):
            _same(_invoke(box, mode, argv=argv), 0, "successful-scripted-return")
            _same((bytes(out.data), bytes(err.data)), (b"", b""), "successful-run-is-silent")
        script.finished()
        monitor.finished()
        files = _output_files(box.output)
        rows = _audit_files(files, mode, script.cell_times if mode == "pilot" else None,
                            expected_source=box.source,
                            expected_manifest=(box.inputs / "MANIFEST").read_bytes())
        _same(_parse(files["run-info.json"])["environment"], script.environment,
            "observed-limited-environment")
        for row in rows:
            position = row["recipe"], row["solver"], row["phase"], row["repeat"]
            _same(row["elapsed_ns"], script.elapsed(position), "scripted-integer-time-retention")
        if decision is not None:
            _same(_parse(files["findings.json"])["h5"], decision["expected_h5"],
                "scripted-h5-boundary")
        if giant:
            rid, route = script.giant["recipe"], script.giant["solver"]
            chosen = [row for row in rows if (row["recipe"], row["solver"]) == (rid, route)]
            _need(bool(chosen), "giant-row-was-exercised")
            for row in chosen:
                _same(row["record"]["algorithm"], script.giant["record"]["algorithm"],
                    "giant-native-record-retained")
        if unrelated:
            _same((box.inputs / "unrelated" / "keep").read_bytes(), b"unowned-content\n",
                  "unrelated-directory-preserved")
            _same((box.inputs / "unrelated-file").read_bytes(), b"also-unowned\n",
                  "unrelated-file-preserved")
        report = {"mode": mode, "scripted_calls": len(script.calls), "real_solver_calls": 0,
                  "actual_c0_checks": len(script.checked), "source": box.source["sha256"]}
        if source_attribution:
            report["cell_source_observation"] = script.cell_source.report()
        return report


class _BytesSink:
    """Observable standard binary stream; deliberately has no text fallback."""

    def __init__(self, short=False, bad_write=(), bad_flush=(), error=None, stage=None):
        self.data = bytearray()
        self.short, self.bad_write, self.bad_flush = short, bad_write, bad_flush
        self.error, self.stage = error, stage
        self.flushed, self.closed = 0, False

    def write(self, raw):
        _need(type(raw) is bytes, "standard-stream-binary-bytes")
        if self.stage == "write":
            raise self.error
        if self.bad_write:
            return self.bad_write[0]
        count = max(1, len(raw) // 2) if self.short and raw else len(raw)
        self.data.extend(raw[:count])
        return count

    def flush(self):
        self.flushed += 1
        if self.stage == "flush":
            raise self.error
        return self.bad_flush[0] if self.bad_flush else None

    def close(self):
        self.closed = True
        raise AssertionError("runner-must-not-close-standard-stream")


@contextlib.contextmanager
def _standard_streams(stdout=None, stderr=None):
    stdout = _BytesSink() if stdout is None else stdout
    stderr = _BytesSink() if stderr is None else stderr
    out, err = types.SimpleNamespace(buffer=stdout), types.SimpleNamespace(buffer=stderr)
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(sys, "stdout", out)
        patch.setattr(sys, "stderr", err)
        try:
            yield stdout, stderr
        finally:
            _need(sys.stdout is out and sys.stderr is err, "standard-streams-not-rebound")
            _need(not stdout.closed and not stderr.closed, "standard-streams-not-closed")


@contextlib.contextmanager
def _no_activity(module):
    """Argument/help guards may not start filesystem/discovery/clock/solver work."""
    def forbidden(*_args, **_kwargs):
        raise AssertionError("argument-or-help-started-external-activity")
    telemetry = importlib.import_module("exactfrac.telemetry")
    with pytest.MonkeyPatch.context() as patch:
        box = types.SimpleNamespace(module=module, patch=patch)
        for dependency, name in (
            (builtins, "open"), (io, "open"), (os, "open"), (os, "stat"), (os, "lstat"),
            (os, "mkdir"), (os, "scandir"), (os, "listdir"), (time, "perf_counter_ns"),
            (time, "get_clock_info"), (platform, "python_version"), (platform, "platform"),
            (platform, "processor"),
        ):
            _patch_public(box, dependency, name, forbidden)
        _patch_public(box, telemetry, "solve_with_telemetry", forbidden)
        yield


def test_public_surface_and_signature():
    _same(runner.__all__, ("main",), "runner-only-public-entry-point")
    _need(callable(runner.main), "main-callable")
    signature = inspect.signature(runner.main)
    _same(tuple(signature.parameters), ("argv",), "single-argv-parameter")
    parameter = signature.parameters["argv"]
    _same(parameter.kind, inspect.Parameter.POSITIONAL_OR_KEYWORD, "argv-call-convention")
    _same(parameter.default, None, "argv-default")
    _same(typing.get_type_hints(runner.main), {"argv": list[str] | None, "return": int},
        "main-annotations")
    _same(Path(runner.__file__).resolve(), _ROOT / "exactfrac/experiments_irregular.py",
        "local-runner-origin")


@pytest.mark.parametrize("argument", [(), "--help", b"--help", 1, True, {}, [1], [False],
    [b"--help"]])
def test_main_python_argument_types_fail_before_activity(argument):
    with _standard_streams() as (out, err), _no_activity(runner):
        with pytest.raises(ValueError) as failure:
            runner.main(argument)
        _need(type(failure.value) is ValueError, "plain-value-error-for-python-argument")
        _same((bytes(out.data), bytes(err.data)), (b"", b""),
            "invalid-python-argument-is-not-usage")


def test_main_rejects_list_and_string_subclasses():
    class ListSubclass(list):
        pass
    class StringSubclass(str):
        pass
    for argument in (ListSubclass(["--help"]), [StringSubclass("--help")]):
        with _standard_streams(), _no_activity(runner), pytest.raises(ValueError) as failure:
            runner.main(argument)
        _need(type(failure.value) is ValueError, "exact-argv-types")


_BAD_ARGV = (
    [], ["--all", "--pilot"], ["--pilot", "--all"], ["--help", "--all"],
    ["--all", "--help"], ["--instances", "x", "--all"], ["--all", "--all"],
    ["--pilot", "--pilot"], ["--all", "extra"], ["--all", "--output"],
    ["--all", "--instances"], ["--pilot", "--output", ""], ["--all", "--output", "-x"],
    ["--all", "--output=x"], ["--all", "--timeout", "1"], ["--all", "--seed", "p01"],
    ["--all", "--force"], ["--all", "--resume"], ["--all", "--repeats", "1"],
    ["--all", "--output", "x", "--output", "y"],
    ["--pilot", "--instances", "x", "--instances", "y"],
    ["--all", "--instances", "a\x00b"], ["--help\x00"], ["--all", "--", "x"],
)


@pytest.mark.parametrize("argument", _BAD_ARGV)
def test_usage_is_exact_and_precedes_activity(argument):
    expected = _bank()["USAGE.txt"]
    with _standard_streams(stderr=_BytesSink(short=True)) as (out, err), _no_activity(runner):
        _same(runner.main(argument), 2, "usage-return-code")
        _same((bytes(out.data), bytes(err.data)), (b"", expected), "fixed-non-echoing-usage")
        _need(err.flushed > 0, "usage-stream-flushed")


@pytest.mark.parametrize("form", ["positional", "keyword", "sys-argv"])
def test_help_exact_short_writes_and_no_activity(form, monkeypatch):
    expected = _bank()["HELP.txt"]
    monkeypatch.setattr(sys, "argv", ["arbitrary-caller-name", "--help"])
    with _standard_streams(stdout=_BytesSink(short=True)) as (out, err), _no_activity(runner):
        result = (runner.main(["--help"]) if form == "positional" else
                  runner.main(argv=["--help"]) if form == "keyword" else runner.main())
        _same(result, 0, "help-return-code")
        _same((bytes(out.data), bytes(err.data)), (expected, b""), "exact-help")
        _need(out.flushed > 0, "help-stream-flushed")


@pytest.mark.parametrize("value", [None, False, True, 0, -1, 1.0, "1", 10**6])
def test_standard_stream_invalid_write_promises_are_runtime_error(value):
    with _standard_streams(stdout=_BytesSink(bad_write=(value,))), _no_activity(runner):
        with pytest.raises(RuntimeError) as failure:
            runner.main(["--help"])
        _need(type(failure.value) is RuntimeError, "normal-write-promise-classification")


@pytest.mark.parametrize("value", [False, True, 0, 1, "ok"])
def test_standard_stream_invalid_flush_promises_are_runtime_error(value):
    with _standard_streams(stdout=_BytesSink(bad_flush=(value,))), _no_activity(runner):
        with pytest.raises(RuntimeError) as failure:
            runner.main(["--help"])
        _need(type(failure.value) is RuntimeError, "normal-flush-promise-classification")


@pytest.mark.parametrize("stage", ["write", "flush"])
@pytest.mark.parametrize("exception_type", [OSError, MemoryError, RecursionError,
    KeyboardInterrupt])
def test_standard_stream_native_exception_identity(stage, exception_type):
    error = exception_type("declared-test-sentinel")
    with _standard_streams(stdout=_BytesSink(error=error, stage=stage)), _no_activity(runner):
        with pytest.raises(exception_type) as failure:
            runner.main(["--help"])
        _need(failure.value is error, "standard-stream-exception-identity")


def test_registered_schedules_are_independently_reconstructed():
    for mode, name in (("pilot", "PILOT_SCHEDULE.tsv"), ("main", "MAIN_SCHEDULE.tsv")):
        bank = _r2_bank() if mode == "main" else _bank()
        rows = list(csv.DictReader(io.StringIO(bank[name].decode("ascii")), delimiter="\t"))
        expected = _schedule(mode)
        _same(len(rows), len(expected), "registered-schedule-length")
        for index, (row, position) in enumerate(zip(rows, expected, strict=True)):
            rid, route, phase, repeat = position
            _same((row["recipe"], row["solver"], row["phase"], _integer(row["repeat"])),
                  (rid, route, phase, repeat), "independent-position-" + str(index))
        counts = collections.Counter(p[2] for p in expected)
        _same(dict(counts), {"pilot": 480} if mode == "pilot" else {"warmup": 1440,
            "measured": 4320},
              "separate-fixed-schedule-partitions")


def test_all_registered_input_geometries_without_optimization():
    for rid in _REGISTRY:
        _geometry_check(rid)


def test_descriptor_boundaries_with_exhaustive_shores_only():
    for case in _parse(_bank()["DESCRIPTOR_BOUNDARY_CASES.json"]):
        n, inside, outside, terminals, parity = (case[k] for k in ("n", "I", "O", "T", "pi"))
        matches = [mask for mask in range(1 << n)
                   if mask & inside == inside and not mask & outside
                   and (mask & terminals).bit_count() % 2 == parity]
        _same(matches, case["matching_masks"], "descriptor-exhaustive-shores")
        descriptor = _descriptor(n, terminals, parity, inside, outside)
        _same(descriptor[:2], (case["feasible"], case["N_F"]), "descriptor-feasibility-size")
        cuts = 0 if not matches else case["N_F"] ** 2 - 3 * case["N_F"] + 3
        _same(cuts, case["ordinary_cuts_per_query"], "descriptor-cut-identity")


def test_complete_native_field_registry_and_empty_work():
    classes = _classes()
    for name, expected in _parse(_bank()["FIELD_REGISTRY.json"]).items():
        cls = classes[name]
        _same([field.name for field in dataclasses.fields(cls)], expected["fields"],
            "native-fields-" + name)
        _same(cls.__annotations__, expected["annotations"], "native-annotations-" + name)
    for entry in _parse(_bank()["SYNTHETIC_EMPTY_ALGORITHMS.json"]):
        algorithm = entry["algorithm"]
        actual = _algorithm_object(algorithm, classes)
        _same(_projection(actual), algorithm, "empty-exact-native-carrier")
        _same(actual.branches, (), "empty-has-no-invented-branches")


def test_registered_wire_artifacts_and_all_derived_tables():
    clocks = _parse(_bank()["SYNTHETIC_PILOT_CELL_CLOCKS.json"])
    times = {row["cell"]: row["end_ns"] - row["start_ns"] for row in clocks}
    for mode in ("pilot", "main"):
        _audit_files(_mode_files(mode), mode, times if mode == "pilot" else None)


def test_h5_all_registered_boundaries_and_timing_invariance():
    for case in _parse(_r2_bank()["H5_BOUNDARY_CASES.json"]):
        findings, coverage = _findings(case["pairs"], 5760)
        _same(findings["h5"], case["expected_h5"], "fixed-h5-boundary-" + case["id"])
        _same(len(coverage), 36, "all-coverage-cells-including-zero")
        _need(all(row["coverage_D"] == 20 for row in coverage),
            "unreduced-recipe-coverage-denominator")
        changed = copy.deepcopy(case["pairs"])
        for index, row in enumerate(changed):
            row["standard_median_solve_ns"] = index * 7
            row["accelerated_median_solve_ns"] = (len(changed) - index) * 11
        _same(_findings(changed, 5760)[0]["h5"], findings["h5"],
            "timing-cannot-change-primary-outcome")


def _h3_slope(values):
    _same(len(values), 3, "h3-complete-triple")
    _need(all(type(value) is int for value in values), "h3-exact-response")
    return _reduced(3 * sum(b * y for b, y in zip((1, 8, 64), values, strict=True))
                    - 73 * sum(values), 7154)


def _rational_median(values):
    # Fraction is test-only exact arithmetic, never a new production fit or output.
    from fractions import Fraction
    ordered = sorted(Fraction(value["N"], value["D"]) for value in values)
    _need(bool(ordered), "nonempty-rational-median")
    middle = len(ordered) // 2
    result = ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2
    return {"N": result.numerator, "D": result.denominator}


def test_h3_fixed_support_series_and_separate_exact_arithmetic():
    series = collections.defaultdict(list)
    for rid in _selected("main"):
        ref = _references()[rid]
        key = ref["n"], ref["tau"], ref["capacity_mode"], ref["seed"]
        series[key].append((ref["b"], _support_hash(_parse(_input(rid)))))
    _same(len(series), 240, "all-main-matched-triples")
    for values in series.values():
        _same([b for b, _support in sorted(values)], [1, 8, 64], "fixed-b-not-observed-bit-width")
        _same(len({support for _b, support in values}), 1, "matched-support")
    for case in _parse(_bank()["H3_ARITHMETIC_CASES.json"]):
        _same(_h3_slope(case["y"]), case["expected_slope"], "fixed-exact-h3-arithmetic")
    for route in _ROUTES:
        case = _parse(_r2_bank()["H3_ROUTE_MEDIAN_CASES.json"])[route]
        _same(len(case["triples"]), 240, "all-h3-route-carriers")
        _same(_rational_median([_h3_slope(v) for v in case["triples"]]), case["expected_median"],
              "separate-route-exact-even-median")


def test_c0_attainment_is_not_an_optimality_or_raw_tie_rule():
    check = importlib.import_module("exactfrac_verify.check").verify_certificate
    cases = _parse(_bank()["TINY_CERTIFICATE_CASES.json"])
    for case in cases:
        raw, certificate = case["input_ascii"].encode("ascii"), case["certificate_ascii"].encode(
            "ascii")
        _same(_identity(raw)[1], case["input_sha256"], "tiny-input-pin")
        _same(_identity(certificate)[1], case["certificate_sha256"], "tiny-certificate-pin")
        _same(check(raw, certificate), None, "actual-c0-attainment-only")
    suboptimal = next(case for case in cases if case["id"] == "triangle-suboptimal-C0")
    certificate = _parse(suboptimal["certificate_ascii"].encode("ascii"))
    optimum = suboptimal["expected_optimum"]
    _need(certificate["N"] * optimum["D"] < optimum["N"] * certificate["D"],
        "c0-does-not-prove-optimality")
    tied = [case for case in cases if case["id"].startswith("cycle-tied-raw-")]
    left, right = [_parse(case["certificate_ascii"].encode("ascii")) for case in tied]
    _need(left != right and left["N"] * right["D"] == right["N"] * left["D"],
        "raw-tied-witness-freedom")


@pytest.mark.parametrize("raw", [b'{"x":1,"x":2}', b'{"x":1,"\\u0078":2}', b'{"x":01}',
                                     b'{"x":+1}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1e999}',
                                     b'\xef\xbb\xbf{}', b'{}{}', b'\xff'])
def test_independent_strict_wire_reader_hostile_controls(raw):
    with pytest.raises((ValueError, AssertionError, UnicodeError)):
        _parse(raw)


def test_giant_integer_and_escaping_carriers_without_limit_changes():
    settings = sys.get_int_max_str_digits(), sys.getrecursionlimit()
    for name in ("SYNTHETIC_GIANT_ROW.jsonl", "SYNTHETIC_ESCAPING_ROW.jsonl"):
        raw = _bank()[name]
        obj = _parse(raw, canonical=True)
        _same(_encode(obj) + b"\n", raw, "independent-giant-escaping-roundtrip")
        algorithm = _algorithm_object(obj["record"]["algorithm"])
        _same(_projection(algorithm), obj["record"]["algorithm"], "giant-native-integer-retained")
    _same((sys.get_int_max_str_digits(), sys.getrecursionlimit()), settings,
        "numeric-settings-unchanged")


@pytest.mark.parametrize("mode", ["pilot", "main"])
def test_full_runner_schedule_is_scripted_not_a_real_campaign(tmp_path, mode):
    result = _execute_scripted_case(tmp_path, mode)
    _same(result["real_solver_calls"], 0, "scripted-is-not-real")


def test_scripted_pilot_positive_short_output_writes(tmp_path):
    _execute_scripted_case(tmp_path, "pilot", short_write=True)


def test_scripted_main_giant_native_integer_path(tmp_path):
    _execute_scripted_case(tmp_path, "main", giant=True)


@pytest.mark.parametrize("case_index", list(range(10)))
def test_scripted_main_h5_boundary_has_observed_calls(tmp_path, case_index):
    decision = _parse(_r2_bank()["H5_BOUNDARY_CASES.json"])[case_index]
    _execute_scripted_case(tmp_path, "main", decision=decision)


def _foreign_and_whitespace(manifest):
    # Foreign metadata is valid; the foreign file is intentionally absent and must not be opened.
    manifest = copy.deepcopy(manifest)
    manifest["entries"].append({"suite": "unit99-v1", "recipe": "foreign-q01",
        "path": "unit99-v1/foreign-q01.json",
                                "bytes": 1, "sha256": hashlib.sha256(b"x").hexdigest()})
    manifest["entries"].sort(key=lambda entry: entry["path"])
    # No owned payload byte changes; aggregate spelling is intentionally not canonical.
    return json.dumps(dict(reversed(tuple(manifest.items()))), indent=2,
        sort_keys=False).encode("ascii") + b"\n"


def test_scripted_pilot_accepts_valid_foreign_metadata_and_disjoint_retry(tmp_path):
    _execute_scripted_case(tmp_path, "pilot", manifest_transform=_foreign_and_whitespace,
        alternate=True)


@pytest.mark.parametrize("fault", ["tuple-size", "list-instead-of-tuple", "wrong-result",
    "wrong-stats"])
def test_scripted_invalid_normal_telemetry_promises(tmp_path, fault):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        def corrupt(_index, response):
            return {"tuple-size": response[:1], "list-instead-of-tuple": list(response),
                    "wrong-result": (object(), response[1]), "wrong-stats": (response[0],
                        object())}[fault]
        script.return_fault = corrupt
        with pytest.raises(RuntimeError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is RuntimeError, "invalid-normal-telemetry-classification")
        _need(not (box.output / "COMPLETE.json").exists(), "failed-telemetry-not-complete")


@pytest.mark.parametrize("value", [True, False, 0.5, None])
def test_scripted_invalid_clock_types(tmp_path, value):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        script.clock_fault = lambda _kind, _index, _value: value
        with pytest.raises(RuntimeError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is RuntimeError, "clock-normal-promise-classification")
        _need(not (box.output / "COMPLETE.json").exists(), "invalid-clock-not-complete")


def test_scripted_negative_elapsed_is_rejected(tmp_path):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        script.clock_fault = lambda kind, _index, value: -1 if kind == "solve-end" else value
        with pytest.raises(RuntimeError):
            _invoke(box, "pilot")
        _need(not (box.output / "COMPLETE.json").exists(), "negative-duration-not-complete")


def test_scripted_checker_false_is_not_success(tmp_path):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        script.raise_at = "checker-false"
        with pytest.raises(RuntimeError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is RuntimeError, "checker-normal-false-not-success")
        _need(not (box.output / "COMPLETE.json").exists(), "false-checker-no-complete")


@pytest.mark.parametrize("stage", ["solve", "checker", "certificate-build",
    "certificate-serialize", "clock"])
@pytest.mark.parametrize("exception_type", [OSError, MemoryError, RecursionError,
    KeyboardInterrupt])
def test_scripted_dependency_native_exceptions_propagate_unchanged(tmp_path, stage, exception_type):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        error = exception_type("declared-native-dependency-sentinel")
        script.raise_at, script.exception = stage, error
        with pytest.raises(exception_type) as failure:
            _invoke(box, "pilot")
        _need(failure.value is error, "native-dependency-exception-identity")
        _need(not (box.output / "COMPLETE.json").exists(), "dependency-failure-no-complete")


@pytest.mark.parametrize("fault", ["absent", "extra-leaf", "nested", "different-bytes",
    "executable", "symlink", "directory"])
def test_pilot_validates_unselected_main_leaf_before_execution(tmp_path, fault):
    with _sandbox(tmp_path) as box:
        rid = _selected("main")[-1]
        leaf = box.inputs / "unit21-v2" / (rid + ".json")
        if fault == "absent":
            leaf.unlink()
        elif fault == "extra-leaf":
            (leaf.parent / "unregistered.json").write_bytes(b"{}\n")
        elif fault == "nested":
            (leaf.parent / "unregistered-directory").mkdir()
        elif fault == "different-bytes":
            leaf.write_bytes(leaf.read_bytes() + b" ")
        elif fault == "executable":
            leaf.chmod(0o755)
        elif fault == "symlink":
            target = box.root.parent / "same-input-bytes"
            target.write_bytes(leaf.read_bytes())
            leaf.unlink()
            leaf.symlink_to(target)
        else:
            leaf.unlink()
            leaf.mkdir()
        script = _Script(box, "pilot")
        expected_error = (ValueError, OSError) if fault == "absent" else ValueError
        with pytest.raises(expected_error):
            _invoke(box, "pilot")
        _same(script.calls, [], "entire-projection-before-any-solve")
        _need(not box.output.exists(), "entire-projection-before-output-creation")


@pytest.mark.parametrize("fault", ["duplicate-key", "missing-owned", "duplicate-entry",
    "reordered", "wrong-length",
                                    "bool-length", "wrong-hash", "foreign-bad-path",
                                        "foreign-bad-hash"])
def test_aggregate_manifest_faults_precede_output_and_schedule(tmp_path, fault):
    with _sandbox(tmp_path) as box:
        path = box.inputs / "MANIFEST"
        obj = _parse(path.read_bytes())
        if fault == "duplicate-key":
            raw = path.read_bytes().replace(b'"format":', b'"format":"duplicate","format":', 1)
        else:
            if fault == "missing-owned":
                obj["entries"].pop()
            elif fault == "duplicate-entry":
                obj["entries"].insert(0, copy.deepcopy(obj["entries"][0]))
            elif fault == "reordered":
                obj["entries"][:2] = obj["entries"][1::-1]
            elif fault in ("wrong-length", "bool-length", "wrong-hash"):
                key, value = {"wrong-length": ("bytes", 0), "bool-length": ("bytes", True),
                              "wrong-hash": ("sha256", "0" * 64)}[fault]
                obj["entries"][-1][key] = value
            else:
                obj = _parse(_foreign_and_whitespace(obj))
                entry = obj["entries"][-1]
                entry[
                    "path" if fault == "foreign-bad-path" else "sha256"
                        ] = "../escape" if fault == "foreign-bad-path" else "G" * 64
            raw = _encode(obj) + b"\n"
        path.write_bytes(raw)
        script = _Script(box, "pilot")
        with pytest.raises(ValueError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is ValueError, "malformed-external-manifest-classification")
        _same(script.calls, [], "bad-aggregate-before-schedule")
        _need(not box.output.exists(), "bad-aggregate-before-output")


@pytest.mark.parametrize("fault", ["existing-empty", "existing-nonempty", "existing-file",
    "source-code", "tests",
                                    "git", "inputs", "source-ancestor", "parent-symlink",
                                        "leaf-symlink", "dotdot"])
def test_forbidden_output_paths_are_not_repaired_or_overwritten(tmp_path, fault):
    with _sandbox(tmp_path) as box:
        sentinel = b"preserve-existing-attempt-verbatim\n"
        if fault.startswith("existing-"):
            if fault == "existing-file":
                box.output.parent.mkdir(parents=True)
                box.output.write_bytes(sentinel)
            else:
                box.output.mkdir(parents=True)
                if fault == "existing-nonempty":
                    (box.output / "sentinel").write_bytes(sentinel)
        elif fault in ("source-code", "tests", "git", "inputs"):
            box.output = {"source-code": box.root / "exactfrac/new-output",
                "tests": box.root / "tests/new-output",
                          "git": box.root / ".git/new-output",
                              "inputs": box.inputs / "new-output"}[fault]
        elif fault == "source-ancestor":
            box.output = box.root.parent
        elif fault in ("parent-symlink", "leaf-symlink"):
            target = box.root.parent / "external-target"
            target.mkdir()
            (box.root / "results").mkdir()
            link = box.root / "results/link"
            link.symlink_to(target, target_is_directory=True)
            box.output = link if fault == "leaf-symlink" else link / "new-output"
        else:
            box.output = box.root / "results/../new-output"
        script = _Script(box, "pilot")
        with pytest.raises(ValueError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is ValueError, "invalid-output-path-classification")
        _same(script.calls, [], "invalid-output-before-solve")
        if fault == "existing-file":
            _same(box.output.read_bytes(), sentinel, "old-file-preserved")
        if fault == "existing-nonempty":
            _same((box.output / "sentinel").read_bytes(), sentinel, "old-attempt-preserved")


def _completed_scripted_output(box, script, monitor):
    script.finished()
    monitor.finished()
    files = _output_files(box.output)
    rows = _audit_files(
        files, script.mode, script.cell_times if script.mode == "pilot" else None,
        expected_source=box.source,
        expected_manifest=(box.inputs / "MANIFEST").read_bytes(),
    )
    _same(_parse(files["run-info.json"])["environment"], script.environment,
          "observed-limited-environment")
    for row in rows:
        position = row["recipe"], row["solver"], row["phase"], row["repeat"]
        _same(row["elapsed_ns"], script.elapsed(position), "scripted-integer-time-retention")
    return files, rows


@pytest.mark.parametrize("stage", ["open", "write", "flush", "close"])
@pytest.mark.parametrize("marker", [False, True])
def test_output_native_failure_preserves_failed_attempt(tmp_path, stage, marker):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        monitor = _OutputMonitor(box, script)
        error = OSError("declared-output-failure")
        monitor.fail_stage, monitor.exception = stage, error
        monitor.fail_name = "COMPLETE.json" if marker else "pilot.jsonl"
        caught = None
        with _standard_streams() as (out, err):
            try:
                result = _invoke(box, "pilot")
            except OSError as failure:
                caught = failure
            _same((bytes(out.data), bytes(err.data)), (b"", b""),
                "no-output-failure-message-translation")
        if caught is None:
            # There is no buffered flush return on a pure descriptor backend.
            # This is an observed complete positive case, NOT a mutant kill or
            # a swallowed failure. Close/write failures still run independently.
            _same(stage, "flush", "required-native-output-seam-was-reached")
            _same(monitor.failures, [], "no-injection-is-not-exception-evidence")
            _need(not any(path.name == monitor.fail_name for path in monitor.flush_hits),
                  "unreached-flush-is-only-an-unbuffered-positive")
            _same(result, 0, "unbuffered-output-positive-return")
            _completed_scripted_output(box, script, monitor)
            return
        _need(caught is error, "output-exception-identity")
        _same(len(monitor.failures), 1, "one-intended-native-seam-reached")
        observed_stage, path, partial = monitor.failures[0]
        _same((observed_stage, path.name), (stage, monitor.fail_name),
            "actual-native-failure-stage")
        _need(box.output.is_dir(), "failed-attempt-directory-preserved")
        if partial is not None:
            _need(path.read_bytes().startswith(partial), "failed-output-byte-prefix-preserved")
        if not marker:
            _need(not (box.output / "COMPLETE.json").exists(), "incomplete-attempt-no-early-marker")
        elif stage in ("flush", "close"):
            # Here the injected error demonstrably follows an actual parseable
            # marker. A valid ledger does not replace successful invocation return.
            _need(type(partial) is bytes, "marker-bytes-existed-at-late-failure")
            _same(_parse(partial)["format"], "exactfrac-irregular-complete/1",
                  "late-failure-after-parseable-marker")
            _same(path.read_bytes(), partial, "late-failed-marker-bytes-preserved")
            script.finished()
            _audit_files(_output_files(box.output), "pilot", script.cell_times,
                         expected_source=box.source,
                         expected_manifest=(box.inputs / "MANIFEST").read_bytes())


@pytest.mark.parametrize("target", ["source", "input"])
def test_before_complete_drift_invalidates_attempt_without_cleanup(tmp_path, target):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        monitor = _OutputMonitor(box, script)
        def drift(index):
            if index == len(script.positions) - 1:
                path = (box.root / "exactfrac/experiments_irregular.py" if target == "source"
                        else box.inputs / "unit21-v2" / (_selected("main")[-1] + ".json"))
                path.write_bytes(path.read_bytes() + b" ")
        script.after_check = drift
        with pytest.raises(RuntimeError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is RuntimeError, "postvalidation-drift-is-runtime-error")
        _need(not monitor.complete_seen, "drift-detected-before-marker-creation")
        _need(box.output.exists(), "drift-failed-attempt-preserved")


def _renew_complete_hashes(files):
    changed = dict(files)
    marker = _parse(changed["COMPLETE.json"])
    # Mutant hashes are deliberately made consistent so a ledger-only guard is insufficient.
    marker["files"] = [{"path": name, "bytes": len(raw), "sha256": _identity(raw)[1]}
                       for name, raw in sorted(changed.items()) if name != "COMPLETE.json"]
    changed["COMPLETE.json"] = _encode(marker) + b"\n"
    return changed


@pytest.mark.parametrize("name", ["summary.csv", "branches.csv", "comparison.csv", "coverage.csv",
    "findings.json"])
def test_coherent_table_and_completion_hash_mutants_fail_independent_derivation(name):
    files = _mode_files("main")
    changed = dict(files)
    if name == "findings.json":
        obj = _parse(changed[name])
        obj["h5"]["outcome"] = "invented-outcome"
        changed[name] = _encode(obj) + b"\n"
    else:
        lines = changed[name].splitlines(keepends=True)
        # ASCII-valid mutation keeps a complete CSV shape and updated ledger.
        cells = lines[1].rstrip(b"\n").split(b",")
        cells[-1] = b"999999999999999999999"
        lines[1] = b",".join(cells) + b"\n"
        changed[name] = b"".join(lines)
    changed = _renew_complete_hashes(changed)
    with pytest.raises(AssertionError) as failure:
        _audit_files(changed, "main")
    _need("raw-to-" in str(failure.value), "mutation-must-hit-raw-to-table-guard-not-ledger")


def test_future_bounded_real_micro_composition_only(record_property):
    """Four real calls when this future GREEN test runs; never run by preparation helpers."""
    classes = _classes()
    telemetry = importlib.import_module("exactfrac.telemetry")
    certificate_module = importlib.import_module("exactfrac.certificate")
    check = importlib.import_module("exactfrac_verify.check").verify_certificate
    cases = {case["id"]: case for case in _parse(_bank()["TINY_CERTIFICATE_CASES.json"])}
    adopted = (("edge-q01-f01-01", "Empty-unit-edge"), ("tri-q1-1-1-f1-1-1", "triangle-full-shore"))
    observed = []
    for recipe, name in adopted:
        case = cases[name]
        raw = case["input_ascii"].encode("ascii")
        for route in _ROUTES:
            instance = classes["Instance"].from_dict(_parse(raw))
            # The sole optimization call in this scenario; no warmup, clock or follow-up solve.
            response = telemetry.solve_with_telemetry(instance, route)
            observed.append((recipe, route))
            _need(type(response) is tuple and len(response) == 2, "actual-micro-return")
            result, algorithm = response
            _need(type(result) is classes["SolveResult"] and type(algorithm) is classes[
                "AlgorithmStats"], "micro-native-types")
            encoded = certificate_module.serialize_certificate(instance,
                certificate_module.build_certificate(instance, result))
            _same(check(raw, encoded), None, "micro-real-independent-c0")
            value = _parse(encoded)
            expected = case["expected_optimum"]
            _same(value["N"] * expected["D"], expected["N"] * value["D"],
                "micro-definition-optimum")
            metadata = classes["RunMetadata"](None, "micro-composition", "test-only", None,
                                              "test-only", _identity(raw)[1])
            record = classes["RunRecord"](algorithm, metadata)
            _need(type(record) is classes["RunRecord"], "micro-actual-run-record")
            _h2(_projection(algorithm), _geometry(_parse(raw))[0])
    _same(observed, [(recipe, route) for recipe, _name in adopted for route in _ROUTES],
        "bounded-real-call-inventory")
    record_property("unit21b_real_micro_calls", len(observed))
    record_property("unit21b_irregular_real_calls", 0)


_PURITY_PROGRAM = r'''
import base64
import builtins
import importlib
import io
import json
import os
from pathlib import Path
import platform
import runpy
import sys
import time
root, expected_help = Path(sys.argv[1]), base64.b64decode(sys.argv[2])
sys.path.insert(0, str(root))
initial_path = list(sys.path)
settings = (sys.get_int_max_str_digits(), sys.getrecursionlimit())
def forbidden(*args, **kwargs):
    raise AssertionError("fresh-process-runtime-side-effect")
class Sink:
    def __init__(self):
        self.buffer = io.BytesIO()
    def write(self, value):
        raise AssertionError("unexpected-text-output")
    def flush(self):
        return None
originals = []
for owner, name in ((builtins, "open"), (io, "open"), (os, "open"),
                    (platform, "python_version"), (platform, "platform"),
                    (platform, "processor"), (time, "perf_counter_ns"),
                    (time, "get_clock_info")):
    originals.append((owner, name, getattr(owner, name)))
    setattr(owner, name, forbidden)
out, err, previous_out, previous_err = Sink(), Sink(), sys.stdout, sys.stderr
sys.stdout, sys.stderr = out, err
try:
    module = importlib.import_module("exactfrac.experiments_irregular")
    assert module.__file__ == str(root / "exactfrac/experiments_irregular.py")
    assert out.buffer.getvalue() == err.buffer.getvalue() == b""
    assert sys.path == initial_path
    assert module.main(["--help"]) == 0
    assert out.buffer.getvalue() == expected_help and err.buffer.getvalue() == b""
    out.buffer.seek(0)
    out.buffer.truncate()
    runpy.run_path(str(root / "experiments/reproduce_irregular.py"),
        run_name="consumer_import_only")
    assert out.buffer.getvalue() == err.buffer.getvalue() == b""
    assert sys.path == initial_path
    sys.argv = ["reproduce_irregular.py", "--help"]
    try:
        runpy.run_path(str(root / "experiments/reproduce_irregular.py"), run_name="__main__")
    except SystemExit as error:
        assert type(error.code) is int and error.code == 0
    else:
        raise AssertionError("wrapper-must-exit-with-main-result")
    assert out.buffer.getvalue() == expected_help and err.buffer.getvalue() == b""
    assert sys.path == initial_path
    assert (sys.get_int_max_str_digits(), sys.getrecursionlimit()) == settings
    assert sys.stdout is out and sys.stderr is err
    assert not out.buffer.closed and not err.buffer.closed
finally:
    sys.stdout, sys.stderr = previous_out, previous_err
    for owner, name, value in originals:
        setattr(owner, name, value)
print(json.dumps({"import_help_wrapper": "PASS", "real_solver_calls": 0,
                  "int_max_str_digits": settings[0],
                      "hash_seed": os.environ.get("PYTHONHASHSEED")}, sort_keys=True))
'''


@pytest.mark.parametrize("digits, seed", [(640, "0"), (640, "1"), (4300, "0"), (4300, "1")])
def test_fresh_process_import_help_wrapper_and_settings(tmp_path, digits, seed):
    environment = dict(os.environ)
    environment.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED=seed)
    for key in ("PYTHONPATH", "PYTHONHOME", "PYTEST_ADDOPTS", "PYTEST_PLUGINS"):
        environment.pop(key, None)
    child = subprocess.run(
        [sys.executable, "-B", "-X", "int_max_str_digits=" + str(digits), "-c", _PURITY_PROGRAM,
         str(_ROOT), base64.b64encode(_bank()["HELP.txt"]).decode("ascii")],
        cwd=tmp_path, env=environment, stdin=subprocess.DEVNULL,
        capture_output=True, check=False,
    )
    _same(child.returncode, 0, "fresh-process-import-help-wrapper-exit")
    _same(child.stderr, b"", "fresh-process-no-stderr")
    _same(_parse(child.stdout), {"import_help_wrapper": "PASS", "real_solver_calls": 0,
                                "int_max_str_digits": digits, "hash_seed": seed},
                                    "fresh-process-observed-settings")


def _source_public_exports():
    """Closed export lists plus the two adopted new public surfaces; no import."""
    paths = _parse(_bank()["SOURCE_PATHS.json"])["ordered_paths"]
    exports = {"exactfrac": (), "exactfrac_verify": (),
               "exactfrac.corpus_irregular": ("build_corpus", "generate_instance", "recipe_ids"),
               "exactfrac.experiments_irregular": ("main",)}
    forbidden = {"exactfrac._telemetry", "exactfrac.cli", "exactfrac.corpus",
                 "exactfrac.experiments", "exactfrac_verify.brute"}
    for name in paths:
        if not name.startswith(("exactfrac/", "exactfrac_verify/")) or not name.endswith(".py"):
            continue
        module = name[:-3].replace("/", ".").removesuffix(".__init__")
        if module in exports or module in forbidden:
            continue
        tree = ast.parse(_regular_bytes(_ROOT / name), filename=name)
        declarations = [node.value for node in tree.body if isinstance(node, ast.Assign)
                        and any(isinstance(target, ast.Name) and target.id == "__all__"
                                for target in node.targets)]
        _same(len(declarations), 1, "closed-public-export-declaration")
        exports[module] = tuple(ast.literal_eval(declarations[0]))
    return exports


def _source_direction(raw, owner, exports):
    """Resolve source imports and finite aliases without executing candidate code.

    Local variable spelling is not API visibility. Public objects may be locally
    named with an underscore; project-private objects remain private when aliased.
    Computed targets that cannot be resolved are reported for the existing IR20
    full-source audit, never mislabeled as checked or as a semantic mutant kill.
    """
    observed, unresolved = [], []
    project_roots = {"exactfrac", "exactfrac_verify"}
    metadata = {"__file__", "__spec__", "__name__", "__package__", "__path__", "__dict__",
                "__class__", "__module__", "__qualname__", "__annotations__",
                    "__dataclass_fields__"}

    def validate(name, node):
        root = name.split(".", 1)[0]
        if root not in project_roots:
            _need(root in sys.stdlib_module_names or root == "builtins",
                "public-only-source-direction")
            return
        components = name.split(".")
        module = max((candidate for candidate in exports
                      if name == candidate or name.startswith(candidate + ".")), key=len)
        tail = components[len(module.split(".")):]
        if tail:
            _need(tail[0] in exports[module] or tail[0] in metadata, "public-only-source-direction")
            _need(not any(part.startswith("_") and part not in metadata for part in tail),
                  "public-only-source-direction")
        observed.append({"line": node.lineno, "resolved": name})

    class Direction(ast.NodeVisitor):
        def __init__(self, aliases=None, constants=None):
            self.aliases = {} if aliases is None else dict(aliases)
            self.constants = {} if constants is None else dict(constants)

        def literal(self, node):
            if isinstance(node, ast.Constant):
                return node.value
            if isinstance(node, ast.Name):
                return self.constants.get(node.id)
            if isinstance(node, (ast.Tuple, ast.List)):
                values = [self.literal(part) for part in node.elts]
                return values if all(value is not None for value in values) else None
            if isinstance(node, ast.Dict):
                pairs = [(self.literal(key), self.literal(value))
                         for key, value in zip(node.keys, node.values, strict=True)]
                if all(type(key) is str and value is not None for key, value in pairs):
                    return dict(pairs)
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                left, right = self.literal(node.left), self.literal(node.right)
                return left + right if type(left) is str and type(right) is str else None
            return None

        def relative(self, name, level=0, package=None):
            if not level and not name.startswith("."):
                return name
            if not level:
                level = len(name) - len(name.lstrip("."))
                name = name[level:]
            parts = owner.split(".")[:-1] if package is None else package.split(".")
            _need(level <= len(parts), "source-relative-import-level")
            return ".".join(parts[:len(parts) - level + 1] + ([name] if name else []))

        def import_request(self, node, function):
            """Return (requested module, fromlist) only for resolved imports."""
            if not node.args:
                return None
            name = self.literal(node.args[0])
            if type(name) is not str:
                return None
            def argument(index, key, default):
                expression = next((part.value for part in node.keywords if part.arg == key), None)
                if expression is not None:
                    return self.literal(expression)
                return self.literal(node.args[index]) if len(node.args) > index else default
            if function == "importlib.import_module":
                if name.startswith("."):
                    package = argument(1, "package", None)
                    if type(package) is not str or not package:
                        return None
                    name = self.relative(name, package=package)
                return name, None
            level = argument(4, "level", 0)
            if type(level) is not int or level < 0:
                return None
            if level:
                namespace = argument(1, "globals", None)
                package = namespace.get("__package__") if type(namespace) is dict else None
                if type(package) is not str or not package:
                    return None
                name = self.relative(name, level, package)
            return name, argument(3, "fromlist", [])

        def qualified(self, node):
            if isinstance(node, ast.Name):
                return self.aliases.get(node.id, "builtins." + node.id if node.id in
                                        {"getattr", "vars", "__import__"} else None)
            if isinstance(node, ast.Attribute):
                base = self.qualified(node.value)
                return base + "." + node.attr if base is not None else None
            if isinstance(node, ast.Subscript):
                base, key = self.qualified(node.value), self.literal(node.slice)
                if base is not None and base.endswith(".__dict__") and type(key) is str:
                    return base.removesuffix(".__dict__") + "." + key
            if isinstance(node, ast.Call):
                function = self.qualified(node.func)
                if function == "builtins.getattr" and len(node.args) >= 2:
                    base, key = self.qualified(node.args[0]), self.literal(node.args[1])
                    if base is not None and type(key) is str:
                        return base + "." + key
                if function == "builtins.vars" and len(node.args) == 1:
                    base = self.qualified(node.args[0])
                    return base + ".__dict__" if base is not None else None
                if function is not None and function.endswith(".__dict__.get") and node.args:
                    key = self.literal(node.args[0])
                    if type(key) is str:
                        return function.removesuffix(".__dict__.get") + "." + key
                if function in {"importlib.import_module", "builtins.__import__"}:
                    request = self.import_request(node, function)
                    if request is not None:
                        name, fromlist = request
                        if function == "importlib.import_module":
                            return name
                        if type(fromlist) in (list, tuple):
                            return name if fromlist else name.split(".", 1)[0]
            return None

        def visit_Import(self, node):
            for alias in node.names:
                validate(alias.name, node)
                self.aliases[alias.asname or alias.name.split(".")[0]] = (
                    alias.name if alias.asname else alias.name.split(".")[0])

        def visit_ImportFrom(self, node):
            module = self.relative(node.module or "", node.level)
            validate(module, node)
            for alias in node.names:
                if alias.name == "*":
                    if module in exports:
                        for name in exports[module]:
                            self.aliases[name] = module + "." + name
                    else:
                        unresolved.append({"line": node.lineno, "kind": "stdlib-star-import"})
                    continue
                target = module + "." + alias.name
                validate(target, node)
                self.aliases[alias.asname or alias.name] = target

        def visit_Attribute(self, node):
            target = self.qualified(node)
            if target is not None:
                validate(target, node)
            self.generic_visit(node)

        def visit_Subscript(self, node):
            target = self.qualified(node)
            if target is not None:
                validate(target, node)
            self.generic_visit(node)

        def visit_Call(self, node):
            function = self.qualified(node.func)
            target = self.qualified(node)
            if target is not None:
                validate(target, node)
            if function in {"importlib.import_module", "builtins.__import__"}:
                request = self.import_request(node, function)
                if request is None:
                    unresolved.append({"line": node.lineno, "kind": "computed-module-target"})
                else:
                    requested, fromlist = request
                    validate(requested, node)
                    if function == "builtins.__import__":
                        if type(fromlist) in (list, tuple):
                            for part in fromlist:
                                if type(part) is str and part != "*":
                                    validate(requested + "." + part, node)
                        else:
                            unresolved.append({"line": node.lineno, "kind": "computed-fromlist"})
            if function == "builtins.getattr" and target is None and node.args:
                base = self.qualified(node.args[0])
                if base is not None and base.split(".", 1)[0] in project_roots:
                    unresolved.append({"line": node.lineno, "kind": "computed-project-attribute"})
            self.generic_visit(node)

        def bind(self, target, value):
            if isinstance(target, ast.Name):
                name = self.qualified(value)
                literal = self.literal(value)
                self.aliases.pop(target.id, None)
                self.constants.pop(target.id, None)
                if name is not None:
                    self.aliases[target.id] = name
                if literal is not None:
                    self.constants[target.id] = literal
            elif isinstance(target, (ast.Tuple, ast.List)) and isinstance(value, (ast.Tuple,
                ast.List)):
                if len(target.elts) == len(value.elts):
                    for left, right in zip(target.elts, value.elts, strict=True):
                        self.bind(left, right)

        def visit_Assign(self, node):
            self.visit(node.value)
            for target in node.targets:
                self.bind(target, node.value)

        def visit_AnnAssign(self, node):
            if node.value is not None:
                self.visit(node.value)
                self.bind(node.target, node.value)
            self.visit(node.annotation)

        def visit_FunctionDef(self, node):
            for expression in (*node.decorator_list, *node.args.defaults,
                               *(value for value in node.args.kw_defaults if value is not None)):
                self.visit(expression)
            child = Direction(self.aliases, self.constants)
            parameters = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
            parameters += [item for item in (node.args.vararg, node.args.kwarg) if item is not None]
            for parameter in parameters:
                child.aliases.pop(parameter.arg, None)
                child.constants.pop(parameter.arg, None)
            for statement in node.body:
                child.visit(statement)

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_ClassDef(self, node):
            for expression in (*node.bases, *node.decorator_list):
                self.visit(expression)
            child = Direction(self.aliases, self.constants)
            for statement in node.body:
                child.visit(statement)

    Direction().visit(ast.parse(raw, filename=owner))
    return {"resolved_project_uses": observed, "requires_source_audit": unresolved}


def test_source_import_boundaries_and_wrapper_are_separate_from_observations(record_property):
    paths = _parse(_bank()["SOURCE_PATHS.json"])["ordered_paths"]
    _same(len(paths), 25, "exact-source-path-cardinality")
    _same(paths, sorted(paths), "ascii-source-path-order")
    exports = _source_public_exports()
    reports = {}
    for name in ("exactfrac/experiments_irregular.py", "experiments/reproduce_irregular.py"):
        reports[name] = _source_direction(_regular_bytes(_ROOT / name), name[:-3].replace("/",
            "."), exports)
    # Unresolved computed targets are explicit IR20 review material, not a syntax
    # ban, an assertion of publicness, or a substitute for actual mutant execution.
    record_property("source_direction_review", json.dumps(reports, sort_keys=True))


_SOURCE_IMPORT_POSITIVES = (
    "from .telemetry import solve_with_telemetry as _call\n",
    "from exactfrac import telemetry as t\ncall = t.solve_with_telemetry\n",
    "import exactfrac.telemetry\ncall = exactfrac.telemetry.solve_with_telemetry\n",
    "import exactfrac.telemetry as t\ncall = getattr(t, 'solve_with_telemetry')\n",
    "from importlib import import_module as load\nt = load('exactfrac.telemetry')\n",
    "from . import corpus_irregular as generator\ncall = generator.recipe_ids\n",
    "import exactfrac.telemetry as t\nversion = t.__file__\n",
    "import exactfrac.telemetry as t\ndef local(t):\n    return t._ordinary_local_field\n",
    "import exactfrac.telemetry as t\nt = object()\nvalue = t._ordinary_local_field\n",
    "from importlib import import_module\nt = import_module('.parser', 'email')\n",
    "t = __import__('exactfrac.telemetry')\ncall = t.telemetry.solve_with_telemetry\n",
    (
        "t = __import__('telemetry', {'__package__': 'exactfrac'}, fromlist=['solve_with_te"
        "lemetry'], level=1)\ncall = t.solve_with_telemetry\n"
    ),
)
_SOURCE_IMPORT_FAULTS = (
    "from .experiments import main as harmless\n",
    "from . import experiments as harmless\n",
    "import exactfrac.experiments as harmless\n",
    "from .telemetry import _private_codec as public_name\n",
    "import exactfrac.telemetry as t\npublic_name = t._private_codec\n",
    "import exactfrac.telemetry as t\ncopy = t\npublic_name = copy._private_codec\n",
    "import exactfrac.telemetry as t\npublic_name = getattr(t, '_private_codec')\n",
    "import exactfrac.telemetry as t\npublic_name = vars(t)['_private_codec']\n",
    "import exactfrac.telemetry as t\npublic_name = t.__dict__['_private_codec']\n",
    "import importlib as loader\nmodule = loader.import_module('exactfrac.experiments')\n",
    "from importlib import import_module as load\nmodule = load('.experiments', 'exactfrac')\n",
    "module = __import__('exactfrac', fromlist=['experiments'])\n",
    "from ._telemetry import _tap_int as visible\n",
    "from exactfrac_verify.check import _parse as visible\n",
    "import handoffs.audit as ordinary\n",
    "from tests import fixtures as ordinary\n",
    "t = __import__('experiments', {'__package__': 'exactfrac'}, fromlist=['main'], level=1)\n",
    "t = __import__('exactfrac.telemetry')\ncall = t.telemetry._private_codec\n",
)


@pytest.mark.parametrize("source", _SOURCE_IMPORT_POSITIVES)
def test_source_direction_accepts_public_aliases_and_resolves_relative_imports(source):
    report = _source_direction(source, "exactfrac.experiments_irregular", _source_public_exports())
    _same(report["requires_source_audit"], [], "literal-source-control-fully-resolved")


@pytest.mark.parametrize("source", _SOURCE_IMPORT_FAULTS)
def test_source_direction_rejects_one_private_or_disallowed_import(source):
    exports = _source_public_exports()
    _source_direction("from .telemetry import solve_with_telemetry\n",
        "exactfrac.experiments_irregular", exports)
    with pytest.raises(AssertionError) as error:
        _source_direction(source, "exactfrac.experiments_irregular", exports)
    _same(str(error.value), "public-only-source-direction", "intended-source-guard-not-syntax")


def test_source_direction_identifies_unresolved_dynamic_targets_without_claiming_a_kill():
    exports = _source_public_exports()
    for source in (
        "from importlib import import_module\nmodule = import_module(runtime_name)\n",
        (
            "from importlib import import_module\nmodule = import_module('.telemetry', runt"
            'ime_package)\n'
        ),
        "module = __import__('telemetry', globals(), fromlist=['solve_with_telemetry'], level=1)\n",
        "import exactfrac.telemetry as t\ncall = getattr(t, runtime_attribute)\n",
    ):
        report = _source_direction(source, "exactfrac.experiments_irregular", exports)
        _need(bool(report["requires_source_audit"]), "dynamic-source-observation-needs-audit")


@pytest.mark.parametrize("bad", [None, False, True, 0, -1, 1.0, "1", 10**30])
def test_output_invalid_normal_write_counts_are_runtime_error(tmp_path, bad):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        monitor = _OutputMonitor(box, script)
        monitor.bad_write = (bad,)
        with pytest.raises(RuntimeError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is RuntimeError, "output-invalid-normal-write-promise")
        _need(bool(monitor.bad_write_hits), "invalid-normal-write-result-actually-returned")
        _need(not monitor.complete_seen, "invalid-output-write-cannot-complete")


@pytest.mark.parametrize("bad", [False, True, 0, 1, "ok"])
def test_output_invalid_normal_flush_returns_are_runtime_error(tmp_path, bad):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        monitor = _OutputMonitor(box, script)
        monitor.bad_flush = (bad,)
        caught = None
        try:
            result = _invoke(box, "pilot")
        except RuntimeError as failure:
            caught = failure
        if caught is None:
            _same(monitor.bad_flush_hits, [], "unreached-flush-return-is-not-mutant-evidence")
            _same(monitor.flush_hits, [], "unbuffered-case-has-no-flush-result")
            _same(result, 0, "unbuffered-no-flush-result-positive-return")
            _completed_scripted_output(box, script, monitor)
            return
        _need(type(caught) is RuntimeError, "output-invalid-normal-flush-promise")
        _need(bool(monitor.bad_flush_hits), "invalid-normal-flush-result-actually-returned")
        _need(not monitor.complete_seen, "invalid-output-flush-cannot-complete")


@pytest.mark.parametrize("invocation", ["default", "relative", "relative-output-first"])
def test_scripted_pilot_path_resolution_from_disjoint_cwd(tmp_path, invocation):
    """Complete scripted invocation; default paths never depend on caller cwd."""
    _execute_scripted_case(tmp_path, "pilot", invocation=invocation)


def test_scripted_pilot_retains_unrelated_aggregate_root_content(tmp_path):
    _execute_scripted_case(tmp_path, "pilot", unrelated=True,
                           manifest_transform=_foreign_and_whitespace)


@pytest.mark.parametrize("mode", ["pilot", "main"])
def test_scripted_all_zero_solve_intervals_are_retained(tmp_path, mode):
    _execute_scripted_case(tmp_path, mode, zero_intervals=True)


@pytest.mark.parametrize("fault", ["root-file", "root-symlink", "parent-symlink", "dotdot"])
def test_input_path_rejection_precedes_schedule_and_output(tmp_path, fault):
    with _sandbox(tmp_path) as box:
        redirected = box.root.parent / "redirected"
        if fault == "root-file":
            redirected.write_bytes(b"not-a-directory\n")
            box.inputs = redirected
        elif fault == "root-symlink":
            redirected.symlink_to(box.inputs, target_is_directory=True)
            box.inputs = redirected
        elif fault == "parent-symlink":
            redirected.symlink_to(box.root, target_is_directory=True)
            box.inputs = redirected / "instances"
        else:
            box.inputs = box.inputs / ".." / "instances"
        script = _Script(box, "pilot")
        with pytest.raises(ValueError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is ValueError, "invalid-external-input-path")
        _same(script.calls, [], "input-path-before-solve")
        _need(not box.output.exists(), "input-path-before-output")


@pytest.mark.parametrize("fault", ["wrong-type", "mutable-leaf"])
def test_runner_classifies_normal_generator_promise_failures(tmp_path, fault):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        generator = importlib.import_module("exactfrac.corpus_irregular")
        observed = []
        # No internal API or mandatory choice among the three public functions
        # is invented: corrupt the actual normal response at whichever is used.
        pristine = {
            "recipe_ids": _REGISTRY,
            "build_corpus": (("MANIFEST", _bank()["OWN_MANIFEST"]), *(
                ("unit21-v2/" + rid + ".json", _input(rid)) for rid in _REGISTRY
            )),
        }
        for name in ("recipe_ids", "generate_instance", "build_corpus"):
            def corrupt(*args, _name=name, **kwargs):
                if _name == "generate_instance":
                    rid = args[0] if args else kwargs["recipe_id"]
                    value = _input(rid)
                else:
                    _need(not args and not kwargs, "generator-public-parameter-kinds")
                    value = pristine[_name]
                observed.append(_name)
                if fault == "wrong-type":
                    return object()
                if _name == "generate_instance":
                    return bytearray(value)
                if _name == "recipe_ids":
                    return list(value)
                first, *rest = value
                return ((first[0], bytearray(first[1])), *rest)
            _patch_public(box, generator, name, corrupt)
        with pytest.raises(RuntimeError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is RuntimeError, "generator-normal-promise-is-runtime-error")
        _need(bool(observed), "actual-public-generator-seam-reached")
        _same(script.calls, [], "bad-generator-before-solve")
        _need(not box.output.exists(), "bad-generator-before-output")


@pytest.mark.parametrize("exception_type", [OSError, MemoryError, RecursionError,
    KeyboardInterrupt])
def test_runner_propagates_generator_exception_identity(tmp_path, exception_type):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        generator = importlib.import_module("exactfrac.corpus_irregular")
        error = exception_type("normal-public-generator-raised-sentinel")
        reached = []
        def fail(*_args, **_kwargs):
            reached.append(True)
            raise error
        for name in ("recipe_ids", "generate_instance", "build_corpus"):
            _patch_public(box, generator, name, fail)
        with pytest.raises(exception_type) as failure:
            _invoke(box, "pilot")
        _need(failure.value is error and bool(reached), "generator-raised-same-object")
        _same(script.calls, [], "generator-exception-before-solve")
        _need(not box.output.exists(), "generator-exception-before-output")


def _change_origin(box, fault):
    """Change only loaded-module provenance; copy existing source, not a stub."""
    module = box.telemetry
    alternate = box.root.parent / "alternate-source" / "telemetry.py"
    alternate.parent.mkdir(exist_ok=True)
    alternate.write_bytes(box.images["exactfrac/telemetry.py"])
    if fault == "file":
        box.patch.setattr(module, "__file__", str(alternate))
    elif fault == "spec":
        changed = copy.copy(module.__spec__)
        changed.origin = str(alternate)
        box.patch.setattr(module, "__spec__", changed)
    else:
        _same(fault, "loaded-module", "declared-origin-fault")
        replacement = types.ModuleType(module.__name__)
        vars(replacement).update(vars(module))
        replacement.__file__ = str(alternate)
        replacement.__spec__ = copy.copy(module.__spec__)
        replacement.__spec__.origin = str(alternate)
        box.patch.setitem(sys.modules, module.__name__, replacement)


@pytest.mark.parametrize("fault", ["file", "spec", "loaded-module"])
def test_initial_conflicting_loaded_source_is_runtime_error(tmp_path, fault):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        _change_origin(box, fault)
        with pytest.raises(RuntimeError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is RuntimeError, "initial-loaded-origin-conflict")
        _same(script.calls, [], "source-conflict-before-schedule")
        _need(not box.output.exists(), "source-conflict-before-output")


@pytest.mark.parametrize("fault", ["file", "spec", "loaded-module"])
def test_end_of_run_loaded_origin_drift_is_runtime_error(tmp_path, fault):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        monitor = _OutputMonitor(box, script)
        reached = []
        def drift(index):
            if index == len(script.positions) - 1:
                _change_origin(box, fault)
                reached.append(index)
        script.after_check = drift
        with pytest.raises(RuntimeError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is RuntimeError, "postvalidation-origin-drift")
        _same(reached, [len(script.positions) - 1], "late-origin-fault-was-reached")
        _need(not monitor.complete_seen, "origin-drift-before-marker")
        _need(box.output.exists(), "origin-drift-preserves-failed-attempt")


def _changed_valid_stats(stats, classes):
    """One changed, internally consistent peak; all H2/native counters unchanged."""
    obj = _projection(stats)
    peak = obj["total"]["peak_integer_bits"] + 1
    obj["nonbranch"]["peak_integer_bits"] = peak
    obj["total"]["peak_integer_bits"] = peak
    result = _algorithm_object(obj, classes)
    _need(result != stats, "valid-record-change-is-real")
    return result


def test_scripted_same_route_valid_stats_change_is_rejected(tmp_path):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "main")
        reached = []
        rid = _selected("main")[0]
        def change(index, response):
            recipe, route, phase, repeat = script.positions[index]
            if (recipe, route, phase, repeat) == (rid, "Standard", "measured", 0):
                result, stats = response
                changed = _changed_valid_stats(stats, box.classes)
                _h2(_projection(changed), _references()[rid]["geometry"])
                reached.append(index)
                return result, changed
            return response
        script.return_fault = change
        with pytest.raises(RuntimeError) as failure:
            _invoke(box, "main")
        _need(type(failure.value) is RuntimeError, "same-route-valid-stats-change")
        _same(len(reached), 1, "intended-valid-repeat-change-reached")
        _need(not (box.output / "COMPLETE.json").exists(), "changed-repeat-no-complete")


def test_output_parent_permissions_are_not_changed(tmp_path):
    with _sandbox(tmp_path) as box:
        box.output.parent.mkdir(parents=True)
        box.output.parent.chmod(0o750)
        before = stat.S_IMODE(box.output.parent.stat().st_mode)
        script = _Script(box, "pilot")
        monitor = _OutputMonitor(box, script)
        # The observer rejects an actual chmod/fchmod attempt, including a later
        # change-and-restore. Final mode equality alone is not the semantic guard.
        _same(_invoke(box, "pilot"), 0, "permission-preservation-pristine-return")
        _completed_scripted_output(box, script, monitor)
        _same(stat.S_IMODE(box.output.parent.stat().st_mode), before,
            "existing-parent-mode-preserved")
        _need(not any(path in monitor.preexisting_ancestors
                      for _kind, path in monitor.permission_calls),
              "no-existing-parent-permission-changing-operation")


def test_output_creation_exception_identity_and_no_cleanup(tmp_path):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        monitor = _OutputMonitor(box, script)
        error = OSError("creation-stage-native-sentinel")
        monitor.creation_failure = error
        with pytest.raises(OSError) as failure:
            _invoke(box, "pilot")
        _need(failure.value is error, "creation-seam-same-native-error")
        _same(monitor.creation_failures, [box.output], "root-creation-seam-actually-reached")
        _same(script.calls, [], "creation-failure-before-solve")
        _need(not box.output.exists(), "failed-creation-does-not-invent-output")


_TIED_RECIPE = "irregular-n12-t064-b00001-frandom-s06"


def _retained_tied_certificates(classes):
    """Use the two already registered attaining witnesses; no optimum search."""
    rid = _TIED_RECIPE
    obj = _parse(_input(rid))
    instance = classes["Instance"].from_dict(obj)
    certificates = []
    module = importlib.import_module("exactfrac.certificate")
    check = importlib.import_module("exactfrac_verify.check").verify_certificate
    for name in ("reference_a", "reference_b"):
        fixed = _references()[rid][name]["optimum"]
        mask, remaining = fixed["mask"], fixed["t"]
        y = [0] * len(obj["edges"])
        for index, (u, v, q) in enumerate(obj["edges"]):
            if bool(mask >> u & 1) != bool(mask >> v & 1):
                y[index] = min(remaining, q)
                remaining -= y[index]
        _same(remaining, 0, "retained-tie-boundary-lift")
        result = classes["SolveResult"](
            classes["ExactValue"](fixed["N"], fixed["D"]),
            classes["Witness"](mask, tuple(y)),
        )
        raw = module.serialize_certificate(instance, module.build_certificate(instance, result))
        _same(check(_input(rid), raw), None, "retained-tie-actual-c0")
        certificates.append(raw)
    left, right = certificates
    _need(left != right, "distinct-retained-tie-certificates")
    _need(_certificate_value(left) != _certificate_value(right), "distinct-retained-raw-pairs")
    _numerical_agreement(_certificate_value(left), _certificate_value(right))
    return tuple(certificates)


def _stats_for_value(stats, result, classes):
    """Adjust only the output/peak carriers of an artificial record."""
    obj = _projection(stats)
    obj["output_numerator_bits"] = max(1, result.value.N.bit_length())
    obj["output_denominator_bits"] = max(1, result.value.D.bit_length())
    for field, output in (("peak_numerator_bits", "output_numerator_bits"),
                          ("peak_denominator_bits", "output_denominator_bits")):
        obj["nonbranch"][field] = max(obj["nonbranch"][field], obj[output])
    obj["nonbranch"]["peak_integer_bits"] = max(
        obj["nonbranch"]["peak_integer_bits"], obj["nonbranch"]["peak_numerator_bits"],
        obj["nonbranch"]["peak_denominator_bits"],
    )
    for field in _schema()["peak_fields"]:
        obj["total"][field] = max(part[field] for part in
                                   [obj["nonbranch"], *(b["work"] for b in obj["branches"])])
    return _algorithm_object(obj, classes)


def test_scripted_cross_route_distinct_attaining_raw_pairs_succeed(tmp_path):
    with _sandbox(tmp_path) as box:
        left, right = _retained_tied_certificates(box.classes)
        script = _Script(box, "main")
        seen = []
        def tied(index, response):
            rid, route, _phase, _repeat = script.positions[index]
            if rid != _TIED_RECIPE:
                return response
            instance = next(value for value in script.instances.values()
                            if value.n == script.objects[rid]["n"]
                            and value.edges == tuple(map(tuple, script.objects[rid]["edges"]))
                            and value.f == tuple(script.objects[rid]["f"]))
            result = _result_from_certificate(instance, left if route == "Standard" else right,
                box.classes)
            stats = _stats_for_value(response[1], result, box.classes)
            _h2(_projection(stats), _references()[rid]["geometry"])
            seen.append(script.positions[index])
            return result, stats
        script.return_fault = tied
        monitor = _OutputMonitor(box, script)
        _same(_invoke(box, "main"), 0, "different-cross-route-raw-pairs-must-succeed")
        script.finished()
        monitor.finished()
        _same(seen, [position for position in script.positions if position[0] == _TIED_RECIPE],
              "complete-tied-recipe-position-observation")
        files = _output_files(box.output)
        _audit_files(files, "main", expected_source=box.source,
                     expected_manifest=(box.inputs / "MANIFEST").read_bytes())
        for route, expected in zip(_ROUTES, (left, right), strict=True):
            _same(files[f"certificates/{_TIED_RECIPE}.{route}.json"], expected,
                  "distinct-route-certificate-retained")


def test_scripted_same_route_changed_attaining_result_is_rejected(tmp_path):
    with _sandbox(tmp_path) as box:
        left, right = _retained_tied_certificates(box.classes)
        script = _Script(box, "main")
        changed = []
        def alter(index, response):
            rid, route, phase, _repeat = script.positions[index]
            if rid != _TIED_RECIPE or route != "Standard":
                return response
            instance = next(value for value in script.instances.values()
                            if value.n == script.objects[rid]["n"]
                            and value.edges == tuple(map(tuple, script.objects[rid]["edges"]))
                            and value.f == tuple(script.objects[rid]["f"]))
            raw = left if phase == "warmup" else right
            result = _result_from_certificate(instance, raw, box.classes)
            stats = _stats_for_value(response[1], result, box.classes)
            _h2(_projection(stats), _references()[rid]["geometry"])
            if phase == "measured":
                changed.append(index)
            return result, stats
        script.return_fault = alter
        with pytest.raises(RuntimeError) as failure:
            _invoke(box, "main")
        _need(type(failure.value) is RuntimeError, "valid-attaining-repeat-result-change")
        _need(bool(changed), "intended-tied-result-change-reached")
        _need(not (box.output / "COMPLETE.json").exists(), "tied-repeat-change-no-complete")


# Controls of the consumer observer itself, not a substitute runner or campaign.
_IO_CONTROL_BACKENDS = (
    "path", "io", "raw-path", "raw-no-b", "raw-fd", "raw-retained",
    "raw-opener", "raw-plus", "buffered-raw", "buffered-open-raw",
    "buffered-retained", "buffered-detach", "low-raw", "low-buffered",
    "descriptor", "descriptor-memoryview", "descriptor-duplicate",
    "descriptor-dup2", "descriptor-closerange", "descriptor-writev",
)


@contextlib.contextmanager
def _io_control_backend(path, backend):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = None
    retained = False
    if backend.startswith("descriptor"):
        descriptor = os.open(path, flags, 0o644)
        if backend in ("descriptor-duplicate", "descriptor-dup2"):
            old = descriptor
            if backend == "descriptor-duplicate":
                descriptor = os.dup(old)
            else:
                descriptor = os.dup(old)
                os.dup2(old, descriptor)
            os.close(old)
        def write(raw):
            if backend == "descriptor-writev":
                split = len(raw) // 2
                return os.writev(descriptor, (raw[:split], memoryview(raw)[split:]))
            return os.write(descriptor,
                memoryview(raw) if backend == "descriptor-memoryview" else raw)
        stream = types.SimpleNamespace(write=write, flush=lambda: None)
    elif backend == "path":
        stream = path.open("xb")
    elif backend == "io":
        # This control must exercise io.open; the shared finally below closes it.
        stream = io.open(path, "xb")  # noqa: SIM115, UP020
    elif backend == "raw-opener":
        stream = io.FileIO(path, "x", opener=lambda name, flags: os.open(name, flags, 0o644))
    elif backend in ("raw-fd", "raw-retained", "buffered-retained"):
        descriptor = os.open(path, flags, 0o644)
        retained = backend != "raw-fd"
        stream = io.FileIO(descriptor, "w", not retained)
        if backend == "buffered-retained":
            stream = io.BufferedWriter(stream)
    elif backend in ("buffered-raw", "buffered-detach"):
        stream = io.BufferedWriter(io.FileIO(path, "xb"))
    elif backend == "buffered-open-raw":
        stream = io.BufferedWriter(path.open("xb", buffering=0))
    elif backend in ("low-raw", "low-buffered"):
        low = importlib.import_module("_io")
        stream = low.FileIO(path, "xb")
        if backend == "low-buffered":
            stream = low.BufferedWriter(stream)
    else:
        mode = {"raw-path": "xb", "raw-no-b": "x", "raw-plus": "x+b"}[backend]
        stream = io.FileIO(path, mode)
    try:
        yield stream
    finally:
        if backend.startswith("descriptor"):
            if backend == "descriptor-closerange":
                os.closerange(descriptor, descriptor + 1)
            else:
                os.close(descriptor)
        elif backend == "buffered-detach":
            stream.detach().close()
        else:
            try:
                stream.close()
            finally:
                if retained:
                    os.close(descriptor)


def _io_control_write_all(stream, raw):
    while raw:
        count = stream.write(raw)
        if type(count) is not int or not 0 < count <= len(raw):
            raise RuntimeError("control-invalid-write-result")
        raw = raw[count:]
    if stream.flush() is not None:
        raise RuntimeError("control-invalid-flush-result")


def _io_observer_control(tmp_path, backend, stage=None, exception_type=OSError,
                         bad_write=(), bad_flush=(), marker=False):
    root = tmp_path / "io-observer-control"
    root.mkdir()
    script = types.SimpleNamespace(checked=[], positions=[], events=[])
    script.event = lambda name, detail=None: script.events.append((name, detail))
    target = root / ("COMPLETE.json" if marker else "payload")
    raw = b'{"consumer_control":true}\n'
    sentinel = exception_type("consumer-observer-native-control")
    with pytest.MonkeyPatch.context() as patch:
        box = types.SimpleNamespace(output=root, patch=patch)
        monitor = _OutputMonitor(box, script)
        monitor.fail_stage, monitor.fail_name, monitor.exception = stage, target.name, sentinel
        monitor.bad_write, monitor.bad_flush = bad_write, bad_flush
        monitor.short_write = not (bad_write or bad_flush)
        caught = None
        try:
            with _io_control_backend(target, backend) as stream:
                _io_control_write_all(stream, raw)
        except (OSError, MemoryError, RecursionError, KeyboardInterrupt, RuntimeError) as error:
            caught = error
        if stage is not None and monitor.failures:
            _need(caught is sentinel, "observer-native-exception-object-identity")
            _same(len(monitor.failures), 1, "observer-one-native-failure")
            _same(monitor.failures[0][:2], (stage, target), "observer-intended-native-seam")
            if stage == "flush" or (stage == "close" and marker):
                _same(monitor.failures[0][2], raw, "observer-late-failure-actual-complete-bytes")
        elif bad_write:
            _need(type(caught) is RuntimeError, "observer-bad-write-control-class")
            _same(str(caught), "control-invalid-write-result", "observer-bad-write-control-guard")
            _need(bool(monitor.bad_write_hits), "observer-bad-write-reached")
        elif bad_flush and monitor.bad_flush_hits:
            _need(type(caught) is RuntimeError, "observer-bad-flush-control-class")
            _same(str(caught), "control-invalid-flush-result", "observer-bad-flush-control-guard")
        else:
            _same(caught, None, "observer-positive-has-no-exception")
            if stage is not None or bad_flush:
                _need(backend.startswith("descriptor"),
                    "unreached-flush-only-raw-descriptor-control")
                _need(stage in (None, "flush"), "other-native-seams-must-be-reached")
                _same(monitor.flush_hits, [], "no-invented-descriptor-flush")
            monitor.fail_stage, monitor.bad_write, monitor.bad_flush = None, (), ()
            if not marker:
                with (root / "COMPLETE.json").open("xb") as marker_stream:
                    _io_control_write_all(marker_stream, b"{}\n")
            monitor.finished()
            expected_paths = [target] if marker else [target, root / "COMPLETE.json"]
            _same(monitor.opened, expected_paths, "each-output-created-once")
            _same(monitor.flushed_bytes[target], raw, "drained-actual-bytes")
        partial = monitor.failures[0][2] if monitor.failures else None
        reached = bool(monitor.failures or monitor.bad_write_hits or monitor.bad_flush_hits)
        # Test-harness teardown only, after the failure observation. This does
        # not assert producer cleanup or change/remove any retained bytes.
        for descriptor in tuple(monitor.descriptors):
            os.close(descriptor)
    if stage == "open":
        _need(not target.exists(), "observer-open-failed-before-creation")
    elif partial is not None:
        _need(target.read_bytes().startswith(partial), "observer-native-error-retained-byte-prefix")
    elif caught is None:
        _same(target.read_bytes(), raw, "actual-control-file-not-synthetic-observer-state")
    return reached


@pytest.mark.parametrize("backend", _IO_CONTROL_BACKENDS)
def test_output_observer_supports_actual_raw_buffered_and_descriptor_backends(tmp_path, backend):
    _same(_io_observer_control(tmp_path, backend), False, "positive-is-not-injected-failure")


@pytest.mark.parametrize("backend", _IO_CONTROL_BACKENDS)
@pytest.mark.parametrize("stage", ["open", "write", "flush", "close"])
@pytest.mark.parametrize("exception_type", [OSError, MemoryError, RecursionError,
    KeyboardInterrupt])
def test_output_observer_preserves_native_failures_at_actual_outer_seams(tmp_path, backend, stage,
                                                                       exception_type):
    # Every negative has its own actual-I/O pristine control on separate files.
    positive = tmp_path / "positive"
    positive.mkdir()
    _io_observer_control(positive, backend)
    changed = tmp_path / "changed"
    changed.mkdir()
    reached = _io_observer_control(changed, backend, stage, exception_type)
    _same(reached, not (backend.startswith("descriptor") and stage == "flush"),
          "native-seam-reachability-not-a-fictional-kill")


@pytest.mark.parametrize("backend", _IO_CONTROL_BACKENDS)
@pytest.mark.parametrize("bad", [None, False, True, 0, -1, 1.0, "1", 10**30])
def test_output_observer_injects_invalid_normal_write_results_at_caller(tmp_path, backend, bad):
    positive = tmp_path / "positive"
    positive.mkdir()
    _io_observer_control(positive, backend)
    changed = tmp_path / "changed"
    changed.mkdir()
    _need(_io_observer_control(changed, backend, bad_write=(bad,)), "normal-write-fault-reached")


@pytest.mark.parametrize("backend", _IO_CONTROL_BACKENDS)
@pytest.mark.parametrize("bad", [False, True, 0, 1, "ok"])
def test_output_observer_distinguishes_flush_promises_from_unbuffered_progress(tmp_path, backend,
    bad):
    positive = tmp_path / "positive"
    positive.mkdir()
    _io_observer_control(positive, backend)
    changed = tmp_path / "changed"
    changed.mkdir()
    reached = _io_observer_control(changed, backend, bad_flush=(bad,))
    _same(reached, not backend.startswith("descriptor"), "normal-flush-fault-reachability")


def _batched_cell_control(tmp_path, backend, partial=False):
    root = tmp_path / "batched-cell"
    (root / "certificates").mkdir(parents=True)
    positions = _schedule("pilot")[:10]
    files = _mode_files("pilot")
    rows = files["pilot.jsonl"].splitlines(keepends=True)[:10]
    script = types.SimpleNamespace(checked=[], positions=positions, events=[])
    script.event = lambda name, detail=None: script.events.append((name, detail))
    with pytest.MonkeyPatch.context() as patch:
        box = types.SimpleNamespace(output=root, patch=patch)
        monitor = _OutputMonitor(box, script)
        for rid, route, _phase, _repeat in positions:
            relative = "certificates/" + rid + "." + route + ".json"
            certificate = files[relative]
            script.checked.append((_input(rid), certificate))
            with _io_control_backend(root / relative, backend) as stream:
                _io_control_write_all(stream, certificate)
        with _io_control_backend(root / "pilot.jsonl", backend) as stream:
            combined = b"".join(rows)
            _io_control_write_all(stream, combined[:-1] if partial else combined)
            if partial:
                with pytest.raises(AssertionError,
                    match=r"^cell-end-after-every-complete-row-flush$"):
                    monitor.cell_end(9)
                _same(monitor.flushed_positions, set(range(9)), "all-complete-prefix-rows-observed")
            else:
                monitor.cell_end(9)
                _same(monitor.flushed_positions, set(range(10)), "batch-covers-every-row")
    _same((root / "pilot.jsonl").read_bytes(), combined[:-1] if partial else combined,
          "actual-batched-file-bytes")


@pytest.mark.parametrize("backend", ["path", "buffered-raw", "descriptor-writev"])
def test_pilot_cell_observer_accepts_a_complete_batched_flush_and_rejects_a_partial_last_row(
    tmp_path,
                                                                                        backend):
    positive = tmp_path / "positive"
    positive.mkdir()
    _batched_cell_control(positive, backend)
    changed = tmp_path / "changed"
    changed.mkdir()
    _batched_cell_control(changed, backend, partial=True)


@pytest.mark.parametrize("backend", _IO_CONTROL_BACKENDS)
@pytest.mark.parametrize("stage", ["flush", "close"])
def test_output_observer_selects_the_late_parseable_marker_failure(tmp_path, backend, stage):
    positive = tmp_path / "positive"
    positive.mkdir()
    _io_observer_control(positive, backend, marker=True)
    changed = tmp_path / "changed"
    changed.mkdir()
    reached = _io_observer_control(changed, backend, stage=stage, marker=True)
    _same(reached, not (backend.startswith("descriptor") and stage == "flush"),
          "late-marker-seam-observed-without-fictional-flush")


def test_output_observer_parses_each_newly_drained_row_once(tmp_path):
    positions = _schedule("pilot")[:10]
    files = _mode_files("pilot")
    rows = files["pilot.jsonl"].splitlines(keepends=True)[:10]
    script = types.SimpleNamespace(positions=positions, checked=[], events=[])
    for rid, route, _phase, _repeat in positions:
        script.checked.append((_input(rid), files["certificates/" + rid + "." + route + ".json"]))
    script.event = lambda name, detail=None: script.events.append((name, detail))
    root = tmp_path / "incremental-output"
    root.mkdir()
    readings, parsed = [], []
    with pytest.MonkeyPatch.context() as patch:
        monitor = _OutputMonitor(types.SimpleNamespace(output=root, patch=patch), script)
        original_open, original_parse = monitor.unobserved_open, _parse
        class Reader:
            def __init__(self, stream):
                self.stream = stream
            def __enter__(self):
                self.stream.__enter__()
                return self
            def __exit__(self, *args):
                return self.stream.__exit__(*args)
            def __getattr__(self, name):
                return getattr(self.stream, name)
            def read(self):
                raw = self.stream.read()
                readings.append(len(raw))
                return raw
        def observed_read(*args, **kwargs):
            return Reader(original_open(*args, **kwargs))
        def observed_parse(raw, canonical=False):
            parsed.append(raw)
            return original_parse(raw, canonical=canonical)
        monitor.unobserved_open = observed_read
        patch.setitem(globals(), "_parse", observed_parse)
        with (root / "pilot.jsonl").open("xb", buffering=0) as stream:
            for row in rows:
                # Multiple raw drains per row, including a partial final token.
                for part in (row[:17], row[17:-1], row[-1:]):
                    _io_control_write_all(stream, part)
        _same(parsed, rows, "one-parse-per-complete-row-not-cumulative-reparse")
        _same(sum(readings), sum(map(len, rows)), "incremental-actual-byte-reads")
        _same(monitor.flushed_positions, set(range(10)), "incremental-complete-row-positions")
    _same((root / "pilot.jsonl").read_bytes(), b"".join(rows), "incremental-control-actual-bytes")


_CONSTRUCTION_FORMS = {
    "from_dict": "Instance.from_dict(data)",
    "direct-positional": "Instance(data['n'], tuple(map(tuple, data['edges'])), tuple(data['f']))",
    "direct-keyword":
        "Instance(f=tuple(data['f']), n=data['n'], edges=tuple(map(tuple, data['edges'])))",
    "from_records":
        "Instance.from_records(data['n'], tuple(map(tuple, data['edges'])), tuple(data['f']))",
    "from_records-keyword":
        (
            "Instance.from_records(f=tuple(data['f']), n=data['n'], records=tuple(map(tuple"
            ", data['edges'])))"
        ),
}


def _construction_control(form, late=False, batch=False, wrong_cell=False, native=False):
    """Actual closed constructors, virtual caller only; not a runner or a solve."""
    cls = _classes()["Instance"]
    selected = _selected("pilot")[:5]
    objects = {rid: _parse(_input(rid)) for rid in selected}
    cell = selected[0].rsplit("-", 1)[0]
    caller = "<unit21b-public-construction-control>"
    trace = []
    native_error = OSError("constructor-native-control")
    with pytest.MonkeyPatch.context() as patch:
        if native:
            def fail(_instance, *_args, **_kwargs):
                raise native_error
            patch.setattr(cls, "__init__", fail)
        script = types.SimpleNamespace(mode="pilot", cell_active=None, objects=objects,
                                       box=types.SimpleNamespace(classes={"Instance": cls},
                                           patch=patch))
        script.event = lambda name, detail=None: trace.append((name, detail))
        watcher = _InstanceStartWatch(script, [caller])
        def start():
            script.cell_active = "different-cell" if wrong_cell else cell
        expression = _CONSTRUCTION_FORMS[form]
        statement = "instances.append(" + expression + ")"
        body = (
            "for data in inputs:\n    " + statement if batch else "data = inputs[0]\n" + statement
        )
        source = (body + "\nstart()\n") if late else ("start()\n" + body + "\n")
        namespace = {"Instance": cls, "inputs": list(objects.values()), "instances": [],
            "start": start}
        caught = None
        try:
            exec(compile(source, caller, "exec"), namespace)
        except (AssertionError, OSError) as error:
            caught = error
        if late:
            _need(type(caught) is AssertionError and str(
                caught) == "pilot-cell-before-construction",
                  "constructor-start-fault-intended-guard")
            _same(watcher.bindings, {}, "late-start-has-no-constructed-object")
        elif wrong_cell:
            _need(type(caught) is AssertionError and str(caught) == "cell-instance-input-binding",
                  "constructor-other-cell-intended-guard")
        elif native:
            _need(caught is native_error, "constructor-native-object-identity")
        else:
            _same(caught, None, "valid-public-constructor")
            _same(len(namespace["instances"]), len(objects) if batch else 1,
                "prepared-instance-count")
            for rid, instance in zip(selected, namespace["instances"], strict=False):
                watcher.require(instance, rid)
                obj = objects[rid]
                _same((instance.n, instance.edges, instance.f),
                      (obj["n"], tuple(map(tuple, obj["edges"])), tuple(obj["f"])),
                      "constructor-values-preserved")
            _same(len(watcher.events), len(namespace["instances"]), "nested-factory-counted-once")
        _same(watcher.depth, 0, "constructor-depth-restored")
        return {"form": form, "late": late, "batch": batch, "wrong_cell": wrong_cell,
                "native": native, "observed_entries": len(watcher.events)}


@pytest.mark.parametrize("form", tuple(_CONSTRUCTION_FORMS))
@pytest.mark.parametrize("batch", [False, True])
def test_pilot_start_observer_accepts_public_constructor_forms_and_cell_preconstruction(form,
    batch):
    _construction_control(form, batch=batch)


@pytest.mark.parametrize("form", tuple(_CONSTRUCTION_FORMS))
def test_pilot_start_observer_rejects_only_late_start_after_pristine_control(form):
    _construction_control(form)
    _construction_control(form, late=True)


@pytest.mark.parametrize("form", tuple(_CONSTRUCTION_FORMS))
def test_pilot_start_observer_rejects_another_cell_and_preserves_native_exception(form):
    _construction_control(form)
    _construction_control(form, wrong_cell=True)
    _construction_control(form, native=True)


_CELL_GEOMETRY_FORMS = {
    "inline": "geometry = sum(data['f']) * data['n']",
    "helper": "geometry = renamed_calculation(data)",
    "five-prepared": "geometries = [sum(item['f']) * item['n'] for item in inputs]",
}


def _cell_source_control(form, late=False, callbacks=False):
    """Source classification is known ONLY for these explicit virtual snippets."""
    path = "<unit21b-raw-geometry-source-control>"
    cell = "explicit-control-cell"
    work = _CELL_GEOMETRY_FORMS[form]
    prelude = "def renamed_calculation(obj):\n    return sum(obj['f']) * obj['n']\n"
    body = (work + "\nstart()\n") if late else ("start()\n" + work + "\n")
    raw = (prelude + "def run():\n    " + body.replace("\n", "\n    ") + "end()\n").encode()
    script = types.SimpleNamespace(cell_active=None)
    watch = _CellSourceTrace(script, {path: raw})
    events = []
    def callback(frame, event, _argument):
        if frame.f_code.co_filename == path:
            events.append((frame.f_code.co_name, event))
        return callback
    def start():
        watch.mark("cell-start", 0)
        script.cell_active = cell
    def end():
        watch.mark("cell-end", 9)
        script.cell_active = None
    old_trace, old_profile = sys.gettrace(), sys.getprofile()
    try:
        if callbacks:
            sys.settrace(callback)
        expected_trace = sys.gettrace()
        data = {"n": 6, "f": [1, 2, 1, 2, 1, 2]}
        scope = {"data": data, "inputs": [data] * 5, "start": start, "end": end}
        exec(compile(raw, path, "exec"), scope)
        with watch.observe():
            scope["run"]()
        _need(sys.gettrace() is expected_trace and sys.getprofile() is old_profile,
              "cell-source-callbacks-restored")
        if callbacks:
            _need(bool(events), "cell-source-existing-tracer-ran")
    finally:
        sys.settrace(old_trace)
        sys.setprofile(old_profile)
    report = watch.report()
    _same(report["files"][0]["sha256"], hashlib.sha256(raw).hexdigest(),
        "actual-snippet-source-hash")
    operations = report["files"][0]["operations"]
    # In these snippets the only multiplication is the visibly specified geometry.
    # This predicate is NEVER applied as a geometry classifier to the real producer.
    multiplication = [row for row in operations if row["opcode"] == "BINARY_OP"
                      and row["argument"] == "*"]
    _need(bool(multiplication), "raw-geometry-operation-actually-observed")
    expected_cell = None if late else cell
    _same({row["cell"] for row in multiplication}, {expected_cell}, "raw-geometry-source-side")
    begin = next(row["order"] for row in report["marks"] if row["kind"] == "cell-start")
    finish = next(row["order"] for row in report["marks"] if row["kind"] == "cell-end")
    _need(all(row["last"] < begin for row in multiplication) if late
          else all(begin < row["first"] <= row["last"] < finish for row in multiplication),
          "raw-geometry-exact-source-order")
    return report


@pytest.mark.parametrize("form", tuple(_CELL_GEOMETRY_FORMS))
@pytest.mark.parametrize("callbacks", [False, True])
def test_cell_source_attribution_distinguishes_raw_geometry_before_and_after_start(form, callbacks):
    _cell_source_control(form, callbacks=callbacks)
    _cell_source_control(form, late=True, callbacks=callbacks)


def test_pilot_retains_actual_source_attribution_for_geometry_review(tmp_path, record_property):
    report = _execute_scripted_case(tmp_path, "pilot", source_attribution=True)
    observed = report["cell_source_observation"]
    starts = [mark for mark in observed["marks"] if mark["kind"] == "cell-start"]
    ends = [mark for mark in observed["marks"] if mark["kind"] == "cell-end"]
    _same(len(starts), 48, "source-observed-cell-starts")
    _same(len(ends), 48, "source-observed-cell-ends")
    _need(any(row["operations"] for row in observed["files"]), "actual-runner-source-observed")
    record_property("pilot_cell_source_attribution", json.dumps(report, sort_keys=True))


# These are independent reader controls. Re-encoding each changed object prevents
# canonical-byte pins from masking the intended schema or semantic rejection.
def _path_at(obj, path):
    for key in path:
        obj = obj[key]
    return obj


def _change_path(obj, path, value):
    target = copy.deepcopy(obj)
    _path_at(target, path[:-1])[path[-1]] = value
    return target


def _assert_reader_fault(read, pristine, changed, guard):
    read(pristine)
    with pytest.raises(AssertionError) as caught:
        read(changed)
    _same(str(caught.value), guard, "single-reader-fault-intended-guard")


def _nested_schema_control(route):
    row = next(row for position, row in _fixed_rows("pilot").items() if position[1] == route)
    pristine = row["record"]["algorithm"]
    _algorithm_object(pristine)
    containers = [((), "exact-algorithm-fields"), (("native",), "exact-native-fields"),
                  (("total",), "all-work-fields"), (("nonbranch",), "all-work-fields")]
    for index in range(4):
        containers.extend([
            (("native", "branch_stats", index), "native-branch-fields"),
            (("native", "branch_stats", index, "oracle_stats"), "oracle-native-fields"),
            (("branches", index), "branch-schema"),
            (("branches", index, "work"), "all-work-fields"),
        ])
    checks = []
    for path, guard in containers:
        obj = _path_at(pristine, path)
        for key in (*obj, "__extra_computed_property__"):
            changed = copy.deepcopy(pristine)
            part = _path_at(changed, path)
            if key in part:
                del part[key]
            else:
                part[key] = 0
            _assert_reader_fault(_algorithm_object, pristine, changed, guard)
            checks.append(("key", path, key, guard))
    numeric = []
    for path, guard in containers:
        if guard in ("all-work-fields", "native-branch-fields", "oracle-native-fields"):
            numeric.extend(((*path, key), "exact-work-count" if guard == "all-work-fields"
                            else "native-branch-count" if guard == "native-branch-fields"
                            else "native-oracle-count")
                           for key in _path_at(pristine, path) if key != "oracle_stats")
    numeric.extend(((name,), "output-bit-count")
                   for name in ("output_numerator_bits", "output_denominator_bits"))
    for path, guard in numeric:
        for value in (True, -1, 0.0, None):
            _assert_reader_fault(_algorithm_object, pristine, _change_path(pristine, path, value),
                guard)
            checks.append(("number", path, type(value).__name__, guard))
    special = [
        (("native", "branch_stats"), (), "native-branch-list"),
        (("branches",), (), "telemetry-branch-list"),
        (("native", "branch_solver"), "Other", "native-selected-route"),
        (("native", "attaining_candidate"), 0, "native-attaining-type"),
        (("native", "attaining_candidate"), "Other", "native-solve-algebra"),
        (("branches", 0, "feasible"), 1, "branch-feasible-bool"),
        (("branches", 0, "branch"), True, "branch-index"),
        (("branches", 0, "branch"), 4, "branch-index"),
        (("native", "branch_stats"), pristine["native"]["branch_stats"][:-1],
            "native-algorithm-algebra"),
        (("branches",), pristine["branches"][:-1], "native-algorithm-algebra"),
    ]
    for path, value, guard in special:
        _assert_reader_fault(_algorithm_object, pristine, _change_path(pristine, path, value),
            guard)
        checks.append(("shape", path, guard))
    _same(_projection(_algorithm_object(pristine)), pristine, "nested-schema-pristine-conserved")
    return {"route": route, "single_fault_controls": len(checks)}


@pytest.mark.parametrize("route", _ROUTES)
def test_independent_nested_schema_single_faults_follow_pristine_controls(route):
    _nested_schema_control(route)


def _metadata_schema_control():
    pristine = next(iter(_fixed_rows("pilot").values()))["record"]["metadata"]
    checks = []
    for key in (*pristine, "private_extra"):
        changed = copy.deepcopy(pristine)
        if key in changed:
            del changed[key]
        else:
            changed[key] = "not-a-declared-field"
        _assert_reader_fault(_metadata_object, pristine, changed, "all-metadata-fields")
        checks.append(key)
    mutations = [("wall_clock_s", value, "metadata-finite-seconds")
                 for value in (False, 0, -0.1, float("nan"), float("inf"))]
    mutations += [(key, value, "metadata-nonempty-text")
                  for key in ("python_version", "platform", "code_version", "instance_sha256")
                  for value in ("", None, 17)]
    mutations += [("cpu", value, "metadata-cpu") for value in ("", 0, False)]
    mutations += [("instance_sha256", value, "metadata-instance-hash")
                  for value in ("A" * 64, "0" * 63, "0" * 65, "g" * 64)]
    for key, value, guard in mutations:
        _assert_reader_fault(_metadata_object, pristine, _change_path(pristine, (key,), value),
            guard)
        checks.append((key, guard))
    for seconds in (None, 0.0, -0.0, 1.25):
        _metadata_object(_change_path(pristine, ("wall_clock_s",), seconds))
    return {"single_fault_controls": len(checks), "valid_seconds_controls": 4}


def test_independent_metadata_types_finiteness_and_exact_fields():
    _metadata_schema_control()


def _source_schema_control():
    pristine = _parse(_mode_files("pilot")["run-info.json"])["source"]
    _validate_source(pristine)
    checks = []
    mutations = [(("entries",), (), "source-entries-list"),
                 (("entries", 0, "path"), None, "source-path-text"),
                 (("entries", 0, "sha256"), "G" * 64, "source-hash"),
                 (("entries", 0), {"path": "x"}, "source-entry-fields")]
    for path, value, guard in mutations:
        _assert_reader_fault(_validate_source, pristine, _change_path(pristine, path, value), guard)
        checks.append((path, guard))
    for index in range(len(pristine["entries"])):
        changed = copy.deepcopy(pristine)
        del changed["entries"][index]
        # Hashes are coherently renewed: a missing fixed source must hit membership,
        # not a stale digest or accidental earlier key dereference.
        prefix = _parse(_bank()["SOURCE_PATHS.json"])["prefix"].encode()
        framing = prefix + b"".join(row["path"].encode() + b"\0" + row["sha256"].encode() + b"\n"
                                   for row in changed["entries"])
        changed["sha256"] = hashlib.sha256(framing).hexdigest()
        changed["code_version"] = "exactfrac-source-sha256:" + changed["sha256"]
        _assert_reader_fault(_validate_source, pristine, changed, "fixed-source-list")
        checks.append((index, "fixed-source-list"))
    for which in ("extra", "reordered", "duplicate"):
        changed = copy.deepcopy(pristine)
        if which == "extra":
            changed["entries"].append({"path": "unlisted.py", "sha256": "0" * 64})
        elif which == "duplicate":
            changed["entries"][1] = copy.deepcopy(changed["entries"][0])
        else:
            changed["entries"][0], changed["entries"][1] = changed["entries"][1], changed[
                "entries"][0]
        _assert_reader_fault(_validate_source, pristine, changed, "fixed-source-list")
        checks.append((which, "fixed-source-list"))
    for path, value, guard in [(("sha256",), "0" * 64, "source-fingerprint-tag-framing"),
                               (("code_version",), "other:" + pristine["sha256"],
                                   "source-version")]:
        _assert_reader_fault(_validate_source, pristine, _change_path(pristine, path, value), guard)
        checks.append((path, guard))
    return {"single_fault_controls": len(checks),
        "individually_omitted_sources": len(pristine["entries"])}


def test_source_entry_shapes_and_coherently_rehashed_fixed_list_faults():
    _source_schema_control()


def _row_binding_control(route):
    files = _mode_files("pilot")
    info = _parse(files["run-info.json"])
    rows = _fixed_rows("pilot")
    position, pristine = next((p, r) for p, r in rows.items() if p[1] == route)
    def read(obj):
        return _row(_encode(obj) + b"\n", "pilot", files, info["source"], info["environment"])
    read(pristine)
    other = "Accelerated" if route == "Standard" else "Standard"
    other_algorithm = rows[position[0], other, "pilot", 0]["record"]["algorithm"]
    mutations = [
        (("record", "algorithm"), other_algorithm, "native-route-binding"),
        (("repeat",), True, "repeat-exact-int"),
        (("elapsed_ns",), True, "exact-integer-elapsed"),
        (("elapsed_ns",), -1, "exact-integer-elapsed"),
        (("record", "metadata", "instance_sha256"), "0" * 64, "metadata-input-binding"),
        (("record", "metadata", "code_version"), "source-other", "metadata-source-binding"),
        (("certificate", "path"), "certificates/another.json", "certificate-path-binding"),
        (("certificate", "sha256"), "0" * 64, "certificate-content-binding"),
        (("certificate", "bytes"), True, "certificate-byte-count"),
        (("input", "n"), True, "input-metadata-and-actual-bits"),
    ]
    for path, value, guard in mutations:
        _assert_reader_fault(read, pristine, _change_path(pristine, path, value), guard)
    return {"route": route, "single_fault_controls": len(mutations)}


@pytest.mark.parametrize("route", _ROUTES)
def test_exact_row_join_faults_are_not_masked_by_canonical_or_native_shape_checks(route):
    _row_binding_control(route)


_NORMAL_NESTED_RETURN_FAULTS = (
    "native-route", "native-branch-list", "native-branch-missing", "native-branch-type",
    "native-count-bool", "native-oracle-count-negative", "telemetry-branch-list",
    "telemetry-branch-missing", "telemetry-feasible-int", "work-type", "work-count-bool",
    "work-inconsistent-total", "output-bits-bool", "result-numerator-bool",
        "result-denominator-zero",
)


def _corrupt_normal_nested_response(response, fault):
    # These are deliberately contradictory *normal* returns at the public seam.
    # Bypass frozen record construction only to test the consumer's validation;
    # no producer class/module or missing-module stub is fabricated.
    result, stats = copy.deepcopy(response)
    native = stats.native
    if fault == "native-route":
        object.__setattr__(native, "branch_solver",
            "Accelerated" if native.branch_solver == "Standard" else "Standard")
    elif fault == "native-branch-list":
        object.__setattr__(native, "branch_stats", list(native.branch_stats))
    elif fault == "native-branch-missing":
        object.__setattr__(native, "branch_stats", native.branch_stats[:-1])
    elif fault == "native-branch-type":
        object.__setattr__(native, "branch_stats", (object(), *native.branch_stats[1:]))
    elif fault == "native-count-bool":
        object.__setattr__(native.branch_stats[0], "oracle_calls", True)
    elif fault == "native-oracle-count-negative":
        object.__setattr__(native.branch_stats[0].oracle_stats, "atomic_families_examined", -1)
    elif fault == "telemetry-branch-list":
        object.__setattr__(stats, "branches", list(stats.branches))
    elif fault == "telemetry-branch-missing":
        object.__setattr__(stats, "branches", stats.branches[:-1])
    elif fault == "telemetry-feasible-int":
        object.__setattr__(stats.branches[0], "feasible", int(stats.branches[0].feasible))
    elif fault == "work-type":
        object.__setattr__(stats, "total", _projection(stats.total))
    elif fault == "work-count-bool":
        object.__setattr__(stats.total, "oracle_calls", True)
    elif fault == "work-inconsistent-total":
        object.__setattr__(stats.total, "oracle_calls", stats.total.oracle_calls + 1)
    elif fault == "output-bits-bool":
        object.__setattr__(stats, "output_numerator_bits", True)
    elif fault == "result-numerator-bool":
        object.__setattr__(result.value, "N", True)
    else:
        _same(fault, "result-denominator-zero", "known-nested-response-control")
        object.__setattr__(result.value, "D", 0)
    return result, stats


@pytest.mark.parametrize("fault", _NORMAL_NESTED_RETURN_FAULTS)
def test_runner_rejects_contradictory_normal_nested_public_response_after_actual_injection(
    tmp_path, fault):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        reached = []
        def corrupt(index, response):
            # Validate the exact supplied pristine objects, then change ONE
            # registered normal-promise aspect at the actual public return seam.
            _same(type(response), tuple, "nested-control-pristine-tuple")
            _same(type(response[0]), box.classes["SolveResult"], "nested-control-pristine-result")
            _same(type(response[1]), box.classes["AlgorithmStats"],
                "nested-control-pristine-algorithm")
            _algorithm_object(_projection(response[1]), box.classes)
            reached.append(index)
            return _corrupt_normal_nested_response(response, fault)
        script.return_fault = corrupt
        with pytest.raises(RuntimeError) as caught:
            _invoke(box, "pilot")
        _same(type(caught.value), RuntimeError, "nested-normal-response-runtime-error")
        _same(reached, [0], "nested-fault-was-actually-returned-before-rejection")
        _same(len(script.calls), 1, "nested-return-rejection-before-next-solve")
        _need(not (box.output / "COMPLETE.json").exists(), "nested-promise-failure-is-not-complete")


def test_normal_nested_fault_injectors_preserve_pristine_objects_and_change_one_field():
    classes = _classes()
    row = next(iter(_fixed_rows("pilot").values()))
    instance = classes["Instance"].from_dict(_parse(_input(row["recipe"])))
    files = _mode_files("pilot")
    result = _result_from_certificate(instance, files[row["certificate"]["path"]], classes)
    stats = _algorithm_object(row["record"]["algorithm"], classes)
    response = (result, stats)
    before = _projection(response)
    for fault in _NORMAL_NESTED_RETURN_FAULTS:
        changed_result, changed_stats = _corrupt_normal_nested_response(response, fault)
        _same(_projection(response), before, "nested-injector-pristine-conservation")
        _same(type(changed_result), classes["SolveResult"], "nested-injector-keeps-result-class")
        _same(type(changed_stats), classes["AlgorithmStats"],
            "nested-injector-keeps-algorithm-class")
        if fault == "result-numerator-bool":
            _need(type(changed_result.value.N) is bool, "actual-bool-numerator-injected")
        elif fault == "result-denominator-zero":
            _same(changed_result.value.D, 0, "actual-zero-denominator-injected")
        elif fault in ("native-branch-list", "telemetry-branch-list"):
            container = (
                changed_stats.native.branch_stats if fault == "native-branch-list" else
                    changed_stats.branches
            )
            _same(type(container), list, "actual-list-instead-of-native-tuple")
        elif fault == "native-branch-type":
            _same(type(changed_stats.native.branch_stats[0]), object,
                "actual-wrong-native-branch-object")
        elif fault == "work-type":
            _same(type(changed_stats.total), dict, "actual-dict-instead-of-native-work-record")
        else:
            # Projection deliberately discards tuple/list and record/dict
            # distinctions; those are handled above, not called wire detections.
            with pytest.raises(AssertionError):
                _algorithm_object(_projection(changed_stats), classes)


@pytest.mark.parametrize("fault", (None, *tuple(_TIMING_EXCLUDED_WORK)))
@pytest.mark.parametrize("side", ("before", "after"))
def test_cell_source_and_solve_interval_observers_compose_without_masking_exclusions(tmp_path,
    fault, side):
    _timing_self_control(tmp_path, form="mapping-lookup", fault=fault, side=side,
                         previous_callbacks=True, outer_source=True)


def _subclass_normal_response(response, selected):
    """Change one outer exact class, preserving all valid native field objects."""
    _need(selected in ("SolveResult", "AlgorithmStats"), "declared-subclass-position")
    index = 0 if selected == "SolveResult" else 1
    record = response[index]
    subclass = type("Consumer" + selected + "Subclass", (type(record),), {"__slots__": ()})
    changed = subclass(**{field.name: getattr(record,
        field.name) for field in dataclasses.fields(record)})
    _need(isinstance(changed, type(record)) and type(changed) is not type(record),
          "otherwise-valid-native-subclass")
    _same(_projection(changed), _projection(record), "subclass-keeps-every-native-field-value")
    for field in dataclasses.fields(record):
        _need(getattr(changed, field.name) is getattr(record, field.name),
              "subclass-keeps-native-field-object-identities")
    return (changed, response[1]) if index == 0 else (response[0], changed)


@pytest.mark.parametrize("selected", ["SolveResult", "AlgorithmStats"])
@pytest.mark.parametrize("route", _ROUTES)
def test_runner_rejects_otherwise_valid_native_subclasses_at_actual_return(tmp_path, selected,
    route):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        reached = []
        def change(index, response):
            if script.positions[index][1] != route:
                return response
            _same(type(response[0]), box.classes["SolveResult"], "subclass-pristine-result")
            _same(type(response[1]), box.classes["AlgorithmStats"], "subclass-pristine-stats")
            _algorithm_object(_projection(response[1]), box.classes)
            changed = _subclass_normal_response(response, selected)
            reached.append(index)
            return changed
        script.return_fault = change
        with pytest.raises(RuntimeError) as caught:
            _invoke(box, "pilot")
        _same(type(caught.value), RuntimeError, "exact-normal-dependency-record-required")
        index = next(i for i, position in enumerate(script.positions) if position[1] == route)
        _same(reached, [index], "otherwise-valid-subclass-was-actually-delivered")
        _same(len(script.calls), index + 1, "subclass-rejected-before-another-solve")
        _need(not (box.output / "COMPLETE.json").exists(), "subclass-failure-not-complete")


_CHECKER_RETURN_LABELS = ("false", "true", "zero", "one", "empty-tuple", "empty-string", "object")


def _non_none_checker_return(label):
    values = {"false": False, "true": True, "zero": 0, "one": 1,
              "empty-tuple": (), "empty-string": "", "object": object()}
    _need(label in values, "declared-checker-return-label")
    return values[label]


@pytest.mark.parametrize("label", _CHECKER_RETURN_LABELS)
def test_runner_rejects_every_non_none_checker_return_after_actual_c0(tmp_path, label):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        value = _non_none_checker_return(label)
        reached = []
        def change(index, response):
            _same(response, None, "checker-positive-control-really-returned-none")
            reached.append(index)
            return value
        script.checker_return_fault = change
        with pytest.raises(RuntimeError) as caught:
            _invoke(box, "pilot")
        _same(type(caught.value), RuntimeError, "checker-must-return-exact-none")
        _same(reached, [0], "non-none-checker-return-actually-delivered")
        _same((len(script.calls), len(script.checked)), (1, 1),
            "one-real-c0-before-return-rejection")
        _same(len(script.checker_returns), 1, "one-observed-checker-return")
        _need(script.checker_returns[0][1] is value, "same-non-none-object-was-returned")
        _need(not (box.output / "COMPLETE.json").exists(), "non-none-checker-failure-not-complete")


class _FifoNoReadStream:
    """A target-FIFO-only read barrier; normal files are never wrapped."""

    def __init__(self, stream, barrier):
        self.stream, self.barrier = stream, barrier

    def __getattr__(self, name):
        if name in ("read", "read1", "readall", "readline", "readlines", "readinto", "readinto1",
            "peek"):
            return lambda *_args, **_kwargs: self.barrier.reject_read(name)
        value = getattr(self.stream, name)
        return _FifoNoReadStream(value, self.barrier) if name in ("raw", "buffer") else value

    def __enter__(self):
        self.stream.__enter__()
        return self

    def __exit__(self, *arguments):
        return self.stream.__exit__(*arguments)

    def __iter__(self):
        self.barrier.reject_read("iter")

    def __next__(self):
        self.barrier.reject_read("next")


class _FifoReadBarrier:
    """Permit safe O_NONBLOCK/fstat rejection; never turn a FIFO read into ValueError.

    Unsafe blocking opens and all target-FIFO reads fail the TEST with a named
    AssertionError. They cannot hang or masquerade as the runner's required
    plain ValueError. Native nonblocking inspection is permitted, not required.
    This is a finite consumer control, not a filesystem-security guarantee.
    """

    def __init__(self, box, leaf):
        info = leaf.lstat()
        _need(stat.S_ISFIFO(info.st_mode), "actual-fifo-required")
        self.identity = info.st_dev, info.st_ino
        self.reads, self.unsafe_opens, self.safe_opens = [], [], []
        original_stat, original_fstat = os.stat, os.fstat
        def targets(value, dir_fd=None):
            try:
                info = (original_fstat(value) if type(value) is int else
                        original_stat(value, dir_fd=dir_fd))
            except (FileNotFoundError, NotADirectoryError, TypeError, ValueError):
                return False
            return (info.st_dev, info.st_ino) == self.identity
        self.targets = targets
        original_open = os.open
        def open_fd(path, flags, mode=0o777, *, dir_fd=None):
            targeted = targets(path, dir_fd)
            if targeted and not flags & os.O_NONBLOCK:
                self.unsafe_opens.append("os.open")
                raise AssertionError("owned-fifo-blocking-open-before-kind-rejection")
            fd = original_open(path, flags, mode, dir_fd=dir_fd)
            if targeted:
                self.safe_opens.append(fd)
            return fd
        _patch_public(box, os, "open", open_fd)
        for name in ("read", "readv", "pread", "preadv"):
            original = getattr(os, name, None)
            if original is None:
                continue
            def read_fd(fd, *args, _name=name, _original=original, **kwargs):
                if targets(fd):
                    self.reject_read(_name)
                return _original(fd, *args, **kwargs)
            _patch_public(box, os, name, read_fd)
        for module, name in ((builtins, "open"), (io, "open"), (io, "FileIO"), (os, "fdopen")):
            original = getattr(module, name)
            def open_stream(file, *args, _name=name, _original=original, **kwargs):
                targeted = targets(file)
                if targeted and type(file) is not int and kwargs.get("opener") is None:
                    self.unsafe_opens.append(_name)
                    raise AssertionError("owned-fifo-blocking-open-before-kind-rejection")
                stream = _original(file, *args, **kwargs)
                return _FifoNoReadStream(stream, self) if targeted else stream
            _patch_public(box, module, name, open_stream)

    def reject_read(self, name):
        self.reads.append(name)
        raise AssertionError("owned-fifo-read-before-kind-rejection")


def test_pilot_rejects_an_actual_unselected_fifo_without_blocking_or_reading(tmp_path):
    with _sandbox(tmp_path) as box:
        rid = _selected("main")[-1]
        leaf = box.inputs / "unit21-v2" / (rid + ".json")
        original = leaf.lstat()
        leaf.unlink()
        os.mkfifo(leaf, 0o600)
        fifo = leaf.lstat()
        _need(stat.S_ISREG(original.st_mode) and stat.S_ISFIFO(fifo.st_mode),
            "one-owned-kind-replaced")
        script = _Script(box, "pilot")
        barrier = _FifoReadBarrier(box, leaf)
        with pytest.raises(ValueError) as caught:
            _invoke(box, "pilot")
        _same(type(caught.value), ValueError, "owned-fifo-is-malformed-external-input")
        _same(barrier.unsafe_opens, [], "no-unsafe-fifo-open-hidden-by-exception-translation")
        _same(barrier.reads, [], "owned-fifo-rejected-before-any-read")
        _same(script.calls, [], "unselected-fifo-validated-before-any-solve")
        _need(not box.output.exists(), "unselected-fifo-validated-before-output")
        current = leaf.lstat()
        _same((current.st_dev, current.st_ino, current.st_mode),
              (fifo.st_dev, fifo.st_ino, fifo.st_mode), "invalid-owned-fifo-not-repaired")


def _fifo_barrier_control(tmp_path):
    leaf, regular = tmp_path / "fifo", tmp_path / "ordinary"
    os.mkfifo(leaf, 0o600)
    regular.write_bytes(b"unchanged ordinary input\n")
    with pytest.MonkeyPatch.context() as patch:
        box = types.SimpleNamespace(patch=patch)
        barrier = _FifoReadBarrier(box, leaf)
        _same(regular.read_bytes(), b"unchanged ordinary input\n", "fifo-barrier-regular-positive")
        # Two safe inspection styles are explicitly accepted. Neither reads.
        fd = os.open(leaf, os.O_RDONLY | os.O_NONBLOCK)
        try:
            _need(stat.S_ISFIFO(os.fstat(fd).st_mode), "fifo-safe-fstat-positive")
            # Exercise the patched io.open descriptor path, not builtins.open.
            with io.open(fd, "rb", closefd=False) as stream:  # noqa: UP020
                _need(stat.S_ISFIFO(os.fstat(stream.fileno()).st_mode),
                    "fifo-safe-stream-fstat-positive")
            with pytest.raises(AssertionError, match=r"^owned-fifo-read-before-kind-rejection$"):
                os.read(fd, 1)
        finally:
            os.close(fd)
        with open(leaf, "rb", opener=lambda path, flags: os.open(path,
            flags | os.O_NONBLOCK)) as stream:
            _need(stat.S_ISFIFO(os.fstat(stream.fileno()).st_mode), "fifo-opener-fstat-positive")
            with pytest.raises(AssertionError, match=r"^owned-fifo-read-before-kind-rejection$"):
                stream.read(1)
        for opener in (lambda: leaf.open("rb"), lambda: io.FileIO(leaf, "rb"),
                       lambda: os.open(leaf, os.O_RDONLY)):
            with pytest.raises(AssertionError,
                match=r"^owned-fifo-blocking-open-before-kind-rejection$"):
                opener()
        _same(len(barrier.reads), 2, "two-target-fifo-read-guards-reached")
        _same(len(barrier.unsafe_opens), 3, "three-target-fifo-open-guards-reached")
        _same(len(barrier.safe_opens), 2, "two-nonblocking-target-fifo-inspections")
        return {"safe_opens": 2, "forbidden_reads": 2, "blocked_unsafe_opens": 3}


def test_fifo_control_allows_safe_inspection_and_never_confuses_its_guard_with_value_error(
    tmp_path):
    _fifo_barrier_control(tmp_path)


_H2_NORMAL_FAULT_GUARDS = {
    "drop-overlap": "h2-enumerated", "deduplicate": "h2-enumerated",
    "fixed-parity": "h2-feasible", "original-n": "h2-reduced-cut-carrier",
    "extra-anchor": "h2-reduced-cut-carrier", "newton-only-cuts": "h2-reduced-cut-carrier",
}


def _h2_coherent_normal_response(response, obj, fault, classes):
    """Native-valid one-rule faults, not malformed records rejected before H2."""
    _need(fault in _H2_NORMAL_FAULT_GUARDS, "declared-h2-normal-fault")
    result, stats = response
    original = _projection(stats)
    geometry, descriptors = _geometry(obj)
    _h2(original, geometry)
    changed = copy.deepcopy(original)
    branch = 1 if fault in ("drop-overlap", "deduplicate", "fixed-parity") else 0
    geo, desc = geometry["branches"][branch], descriptors[branch]
    work = changed["branches"][branch]["work"]
    native = changed["native"]["branch_stats"][branch]
    calls = work["oracle_calls"]
    r, feasible, cut_sum = geo["r"], geo["s"], geo["A"]
    if fault in ("drop-overlap", "deduplicate", "fixed-parity"):
        if fault == "drop-overlap":
            desc = [d for d in desc if not d[2] & d[3]]
        elif fault == "deduplicate":
            desc = list(dict.fromkeys(desc))
        outcomes = []
        flipped = False
        for terminals, parity, inside, outside in desc:
            if (fault == "fixed-parity" and not flipped and not inside & outside
                    and not terminals & ~(inside | outside)):
                # One fixed-terminal descriptor, not two errors that cancel in aggregate.
                parity ^= 1
                flipped = True
            outcomes.append(_descriptor(obj["n"], terminals, parity, inside, outside))
        _need(fault != "fixed-parity" or flipped, "one-fixed-parity-descriptor-was-changed")
        r, feasible = len(desc), sum(ok for ok, _n, _a in outcomes)
        cut_sum = sum(a for _ok, _n, a in outcomes)
    elif fault == "original-n":
        n = obj["n"]
        cut_sum = feasible * (n * n - 3 * n + 3)
    elif fault == "extra-anchor":
        cut_sum = sum(count * ((int(n) + 1) ** 2 - 3 * (int(n) + 1) + 3)
                      for n, count in geo["N_histogram"].items())
    _need(feasible > 0 and geo["s"] > 0, "h2-fault-keeps-native-branch-feasibility")
    cuts = calls * cut_sum
    if fault == "newton-only-cuts":
        queries = native["outer_iterations"] if stats.branch_solver == "Standard" else native[
            "newton_queries"]
        _need(0 < queries < calls, "h2-control-has-excluded-seed-or-initialization-query")
        cuts = queries * cut_sum
    work.update(atomic_families_enumerated=r, atomic_families_examined=calls * r,
                atomic_families_feasible=calls * feasible, parity_cut_calls=calls * feasible,
                ordinary_min_cut_calls=cuts, max_flow_calls=cuts)
    native["oracle_stats"].update(
        atomic_families_examined=work["atomic_families_examined"],
        atomic_families_feasible=work["atomic_families_feasible"],
        parity_cut_calls=work["parity_cut_calls"], ordinary_min_cut_calls=cuts,
    )
    buckets = [changed["nonbranch"], *(row["work"] for row in changed["branches"])]
    changed["total"] = {field: (sum(b[field] for b in buckets) if index < 20 else
                                 max(b[field] for b in buckets))
                        for index, field in enumerate(_schema()["work"])}
    # Construct through the real public validators; no __new__/setattr bypass.
    altered = _algorithm_object(changed, classes)
    _need(type(altered) is classes["AlgorithmStats"], "h2-fault-has-exact-native-class")
    _need(altered != stats, "h2-coherent-normal-fault-changed-a-carrier")
    _same(_projection(stats), original, "h2-normal-fault-keeps-pristine-response")
    with pytest.raises(AssertionError) as caught:
        _h2(_projection(altered), geometry)
    _same(str(caught.value), _H2_NORMAL_FAULT_GUARDS[fault],
        "h2-isolation-not-an-earlier-native-guard")
    return result, altered


@pytest.mark.parametrize("fault", tuple(_H2_NORMAL_FAULT_GUARDS))
@pytest.mark.parametrize("route", _ROUTES)
def test_runner_rejects_native_valid_graph_dependent_h2_fault_at_actual_return(tmp_path, fault,
    route):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        reached = []
        rid = _selected("pilot")[0]
        def change(index, response):
            if script.positions[index][1] != route:
                return response
            _same(script.positions[index][0], rid, "h2-normal-fault-fixed-first-pilot-recipe")
            changed = _h2_coherent_normal_response(response, _parse(_input(rid)), fault,
                box.classes)
            reached.append(index)
            return changed
        script.return_fault = change
        with pytest.raises(RuntimeError) as caught:
            _invoke(box, "pilot")
        _same(type(caught.value), RuntimeError, "graph-dependent-h2-mismatch-is-runtime-error")
        index = next(i for i, position in enumerate(script.positions) if position[1] == route)
        _same(reached, [index], "native-valid-h2-fault-was-actually-returned")
        _same(len(script.calls), index + 1, "h2-fault-rejected-before-next-solve")
        _need(not (box.output / "COMPLETE.json").exists(), "h2-failed-attempt-is-not-complete")


def test_h2_normal_fault_controls_reach_geometry_not_native_shape_or_algebra():
    classes = _classes()
    rid = _selected("pilot")[0]
    obj = _parse(_input(rid))
    instance = classes["Instance"].from_dict(obj)
    files = _mode_files("pilot")
    for route in _ROUTES:
        row = _fixed_rows("pilot")[rid, route, "pilot", 0]
        response = (_result_from_certificate(instance, files[row["certificate"]["path"]], classes),
                    _algorithm_object(row["record"]["algorithm"], classes))
        for fault in _H2_NORMAL_FAULT_GUARDS:
            _h2_coherent_normal_response(response, obj, fault, classes)


_MANIFEST_WIRE_FAULTS = (
    "literal-duplicate", "escaped-duplicate", "float-count", "exponent-count",
    "string-count", "bool-count", "negative-zero", "leading-zero", "plus-count",
    "nan-count", "infinite-count", "bom", "invalid-utf8", "second-root",
)


def _external_manifest_wire_fault(manifest, fault):
    """Only a foreign entry or JSON framing changes; all owned entries are pristine."""
    pristine = _parse(_foreign_and_whitespace(manifest))
    raw = _encode(pristine) + b"\n"
    entry = pristine["entries"][-1]
    _same((entry["suite"], entry["bytes"]), ("unit99-v1", 1), "foreign-control-entry")
    chunk = _encode(entry)
    _same(raw.count(chunk), 1, "single-foreign-entry-target")
    if fault in ("literal-duplicate", "escaped-duplicate"):
        key = b'"recipe":' if fault == "literal-duplicate" else b'"\\u0072ecipe":'
        changed = chunk.replace(b'"recipe":', key + b'"foreign-q01","recipe":', 1)
        return raw, raw.replace(chunk, changed, 1)
    tokens = {
        "float-count": b"1.0", "exponent-count": b"1e0", "string-count": b'"1"',
        "bool-count": b"true", "negative-zero": b"-0", "leading-zero": b"01",
        "plus-count": b"+1", "nan-count": b"NaN", "infinite-count": b"Infinity",
    }
    if fault in tokens:
        needle = b'"bytes":1,'
        _same(chunk.count(needle), 1, "single-foreign-count-target")
        changed = chunk.replace(needle, b'"bytes":' + tokens[fault] + b",", 1)
        return raw, raw.replace(chunk, changed, 1)
    if fault == "bom":
        return raw, b"\xef\xbb\xbf" + raw
    if fault == "invalid-utf8":
        return raw, raw.replace(chunk, chunk.replace(b"foreign-q01", b"foreign-\xff", 1), 1)
    _same(fault, "second-root", "declared-external-wire-fault")
    return raw, raw + b"{}\n"


@pytest.mark.parametrize("fault", _MANIFEST_WIRE_FAULTS)
def test_runner_rejects_hostile_foreign_manifest_wire_before_owned_activity(tmp_path, fault):
    with _sandbox(tmp_path) as box:
        path = box.inputs / "MANIFEST"
        original = _parse(path.read_bytes())
        pristine, altered = _external_manifest_wire_fault(original, fault)
        _need(altered != pristine, "manifest-wire-fault-is-real")
        def owned(obj):
            return [row for row in obj["entries"] if row["suite"] == "unit21-v2"]
        _same(owned(_parse(pristine)), owned(original), "wire-control-owned-projection-unchanged")
        path.write_bytes(altered)
        script = _Script(box, "pilot")
        with pytest.raises(ValueError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is ValueError, "invalid-external-json-is-value-error")
        _same(script.calls, [], "invalid-external-json-before-solve")
        _need(not box.output.exists(), "invalid-external-json-before-output")
        _same(path.read_bytes(), altered, "invalid-external-json-not-repaired")


def test_external_manifest_wire_carriers_preserve_owned_projection_and_isolate_json_rule():
    manifest = _parse(_bank()["OWN_MANIFEST"])
    accepted_by_json_but_not_schema = {
        "float-count": float, "exponent-count": float, "string-count": str,
        "bool-count": bool,
    }
    for fault in _MANIFEST_WIRE_FAULTS:
        pristine, altered = _external_manifest_wire_fault(manifest, fault)
        parsed = _parse(pristine)
        _same([row for row in parsed["entries"] if row["suite"] == "unit21-v2"],
              manifest["entries"], "wire-control-unchanged-owned-entry-values")
        _need(pristine != altered, "one-wire-alteration")
        if fault in accepted_by_json_but_not_schema:
            candidate = _parse(altered)
            _same(type(candidate["entries"][-1]["bytes"]),
                  accepted_by_json_but_not_schema[fault], "wire-fault-intended-non-int-type")
            candidate["entries"][-1]["bytes"] = 1
            _same(candidate, parsed, "wire-fault-only-foreign-count-type")
        else:
            with pytest.raises((ValueError, AssertionError, UnicodeError)):
                _parse(altered)


@pytest.mark.parametrize("mode", ["pilot", "main"])
def test_coherent_output_omissions_reach_mode_inventory_before_lookup(mode):
    files = _mode_files(mode)
    cell_times = {row["cell"]: row["end_ns"] - row["start_ns"] for row in
                  _parse(_bank()["SYNTHETIC_PILOT_CELL_CLOCKS.json"])} if mode == "pilot" else None
    _audit_files(files, mode, cell_times=cell_times)
    complete = _parse(files["COMPLETE.json"])
    # Every absent inventory member is checked. Byte-reencode representative
    # certificates from both routes and every noncertificate artifact separately;
    # serializing the entire unchanged completion ledger per certificate would
    # repeat the same schema obligation quadratically without a new fault family.
    for omitted in sorted(files):
        _require_mode_inventory(files, mode)
        changed_keys = dict.fromkeys(set(files) - {omitted})
        with pytest.raises(AssertionError) as failure:
            _require_mode_inventory(changed_keys, mode)
        _same(str(failure.value), "mode-output-inventory", "every-omitted-member-reaches-inventory")
    representatives = sorted(name for name in files if not name.startswith("certificates/"))
    representatives.extend(f"certificates/{_selected(mode)[0]}.{route}.json" for route in _ROUTES)
    for omitted in representatives:
        _require_mode_inventory(files, mode)
        changed = dict(files)
        del changed[omitted]
        if omitted != "COMPLETE.json":
            marker = copy.deepcopy(complete)
            marker["files"] = [row for row in marker["files"] if row["path"] != omitted]
            changed["COMPLETE.json"] = _encode(marker) + b"\n"
            _same({row["path"] for row in marker["files"]},
                  set(changed) - {"COMPLETE.json"}, "omitted-artifact-ledger-coherent")
        with pytest.raises(AssertionError) as failure:
            _audit_files(changed, mode, cell_times=cell_times)
        _same(str(failure.value), "mode-output-inventory", "omission-not-keyerror-or-stale-hash")
    _same(files, _mode_files(mode), "pristine-output-bank-conserved")


@pytest.mark.parametrize("exception_type", [None, OSError, MemoryError, RecursionError,
    KeyboardInterrupt])
def test_wrapper_restores_import_path_after_same_public_main_return_or_exception(tmp_path,
    exception_type):
    with _sandbox(tmp_path) as box:
        error = None if exception_type is None else exception_type("wrapper-delegation-sentinel")
        reached = []
        def delegated(argv=None):
            actual = sys.argv[1:] if argv is None else argv
            _same(actual, ["--help"], "wrapper-actual-public-main-arguments")
            reached.append(True)
            if error is not None:
                raise error
            return 0
        _patch_public(box, box.module, "main", delegated)
        box.patch.setattr(sys, "argv", ["reproduce_irregular.py", "--help"])
        # The existing public modules are authenticated and loaded; remove the root
        # so a wrapper-managed path insertion is not hidden by a preexisting copy.
        retained = list(sys.path)
        sys.path[:] = [item for item in sys.path if item != str(box.root)]
        before = list(sys.path)
        try:
            execute = importlib.import_module("runpy").run_path
            if error is None:
                with pytest.raises(SystemExit) as failure:
                    execute(str(box.root / "experiments/reproduce_irregular.py"),
                        run_name="__main__")
                _same(failure.value.code, 0, "wrapper-system-exit-same-main-code")
            else:
                with pytest.raises(exception_type) as failure:
                    execute(str(box.root / "experiments/reproduce_irregular.py"),
                        run_name="__main__")
                _need(failure.value is error, "wrapper-propagates-same-native-object")
            _same(reached, [True], "wrapper-exactly-one-public-main-delegation")
            _same(sys.path, before, "wrapper-finally-restores-exact-import-path")
        finally:
            sys.path[:] = retained


_GIANT_PROGRAM = r"""
import json
from pathlib import Path
import runpy
import sys
import tempfile
root = Path(sys.argv[1])
sys.path.insert(0, str(root))
settings = (sys.get_int_max_str_digits(), sys.getrecursionlimit())
initial_path = list(sys.path)
scope = runpy.run_path(str(root / "tests/test_experiments_irregular.py"),
    run_name="consumer_giant_fresh")
with tempfile.TemporaryDirectory(prefix="u21b-giant-scripted.") as temporary:
    observed = scope["_execute_scripted_case"](Path(temporary), "main", giant=True)
assert observed["scripted_calls"] == len(scope["_schedule"]("main"))
assert observed["actual_c0_checks"] == observed["scripted_calls"]
assert observed["real_solver_calls"] == 0
assert settings == (sys.get_int_max_str_digits(), sys.getrecursionlimit())
assert sys.path == initial_path
print(json.dumps({"giant_scripted_main": "PASS", "observed": observed,
                  "int_max_str_digits": settings[0]}, sort_keys=True))
"""


@pytest.mark.parametrize("digits", [640, 4300])
def test_fresh_process_scripted_main_giant_native_records_at_unchanged_digit_limit(tmp_path,
    digits):
    environment = dict(os.environ)
    environment.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    for key in ("PYTHONPATH", "PYTHONHOME", "PYTEST_ADDOPTS", "PYTEST_PLUGINS"):
        environment.pop(key, None)
    child = subprocess.run(
        [sys.executable, "-B", "-X", "int_max_str_digits=" + str(digits), "-c",
         _GIANT_PROGRAM, str(_ROOT)], cwd=tmp_path, env=environment,
        stdin=subprocess.DEVNULL, capture_output=True, check=False,
    )
    _same(child.returncode, 0, "fresh-giant-scripted-main-exit")
    _same(child.stderr, b"", "fresh-giant-no-stderr")
    record = _parse(child.stdout)
    _same(record["giant_scripted_main"], "PASS", "fresh-giant-completed")
    _same(record["int_max_str_digits"], digits, "fresh-giant-observed-limit")
    observed = record["observed"]
    _same(observed["mode"], "main", "fresh-giant-full-mode")
    _same(observed["scripted_calls"], len(_schedule("main")), "fresh-giant-full-scripted-schedule")
    _same(observed["actual_c0_checks"], observed["scripted_calls"],
        "fresh-giant-every-certificate-checked")
    _same(observed["real_solver_calls"], 0, "fresh-giant-not-a-real-campaign")



def _native_accounting_fault(response, fault, classes):
    """Keep every native field well-typed; contradict one cross-record accounting rule."""
    result, original = response
    _algorithm_object(_projection(original), classes)
    changed = copy.deepcopy(original)
    if fault == "infeasible-seed":
        index = next(i for i, branch in enumerate(original.branches) if not branch.feasible)
        work = dataclasses.replace(original.branches[index].work, oracle_calls=0,
                                   atomic_families_examined=0)
        native = original.native.branch_stats[index]
        oracle = dataclasses.replace(native.oracle_stats, atomic_families_examined=0)
        native = dataclasses.replace(native, oracle_calls=0, oracle_stats=oracle)
        native_rows = list(original.native.branch_stats)
        native_rows[index] = native
        branch_rows = list(original.branches)
        branch_rows[index] = dataclasses.replace(branch_rows[index], work=work)
        new_native = dataclasses.replace(original.native, branch_stats=tuple(native_rows))
        buckets = (original.nonbranch, *(branch.work for branch in branch_rows))
        total = classes["WorkStats"](**{
            field: (sum(getattr(bucket, field) for bucket in buckets) if n < 20
                    else max(getattr(bucket, field) for bucket in buckets))
            for n, field in enumerate(_schema()["work"])
        })
        # The deliberately invalid normal promise keeps actual frozen public
        # classes; only their top-level cross-record constructor rule is bypassed.
        object.__setattr__(changed, "native", new_native)
        object.__setattr__(changed, "branches", tuple(branch_rows))
        object.__setattr__(changed, "total", total)
        message = f"infeasible {original.native.branch_solver} branch must stop at its seed"
    else:
        _same(fault, "sum-peaks", "declared-native-accounting-fault")
        peak = sum(bucket.peak_integer_bits for bucket in
                   (original.nonbranch, *(branch.work for branch in original.branches)))
        _need(peak > original.total.peak_integer_bits, "peak-sum-control-distinguishes-max")
        object.__setattr__(changed, "total", dataclasses.replace(original.total,
            peak_integer_bits=peak))
        message = "total must sum events and maximize peaks over every bucket"
    # All nested public records construct successfully. The native complete
    # record itself must reach the precise accounting rule, not a type/shape guard.
    for record in (changed.native, changed.total, changed.nonbranch,
                   *changed.native.branch_stats, *changed.branches,
                   *(branch.work for branch in changed.branches)):
        type(record).__post_init__(record)
    with pytest.raises(ValueError) as failure:
        classes["AlgorithmStats"].__post_init__(changed)
    _same(str(failure.value), message, "native-accounting-fault-exact-intended-rule")
    return result, changed


@pytest.mark.parametrize("fault", ["infeasible-seed", "sum-peaks"])
@pytest.mark.parametrize("route", _ROUTES)
def test_runner_rejects_isolated_native_seed_and_peak_accounting_at_actual_return(tmp_path, fault,
    route):
    with _sandbox(tmp_path) as box:
        script = _Script(box, "pilot")
        reached = []
        def change(index, response):
            if script.positions[index][1] != route:
                return response
            if fault == "infeasible-seed" and all(branch.feasible for branch in response[
                1].branches):
                return response
            before = _projection(response)
            changed = _native_accounting_fault(response, fault, box.classes)
            _same(_projection(response), before, "native-accounting-pristine-conserved")
            reached.append(index)
            return changed
        script.return_fault = change
        with pytest.raises(RuntimeError) as failure:
            _invoke(box, "pilot")
        _need(type(failure.value) is RuntimeError, "native-accounting-normal-promise-runtime-error")
        _same(len(reached), 1, "one-native-accounting-fault-was-returned")
        _same(len(script.calls), reached[0] + 1, "native-accounting-before-next-solve")
        _need(not (box.output / "COMPLETE.json").exists(), "accounting-failure-cannot-complete")


def test_native_accounting_fault_controls_reach_seed_or_peak_rule_after_valid_records():
    classes = _classes()
    files = _mode_files("pilot")
    for route in _ROUTES:
        row = next(row for position, row in _fixed_rows("pilot").items()
                   if position[1] == route and
                   any(not branch["feasible"] for branch in row["record"]["algorithm"]["branches"]))
        instance = classes["Instance"].from_dict(_parse(_input(row["recipe"])))
        result = _result_from_certificate(instance, files[row["certificate"]["path"]], classes)
        response = (result, _algorithm_object(row["record"]["algorithm"], classes))
        before = _projection(response)
        for fault in ("infeasible-seed", "sum-peaks"):
            changed = _native_accounting_fault(response, fault, classes)
            _need(changed[1] != response[1], "native-accounting-control-is-real")
            _same(_projection(response), before, "native-accounting-helper-no-pristine-mutation")


# Explicit R2 checks do not replace or weaken the retained IR1--IR24 cases.
def test_r2_selection_preserves_owned_inputs_and_original_schedules():
    old, new = _bank(), _r2_bank()
    selected = _selected("main")
    excluded = tuple(rid for rid in _REGISTRY if rid.endswith(tuple(
        f"s{i:02d}" for i in range(1, 21))) and rid not in selected)
    _same(len(_REGISTRY), 1200, "r2-complete-owned-registry")
    _same(list(selected), _parse(new["MAIN_SELECTION.json"]), "r2-selected-exact-ids")
    _same(list(excluded), _parse(new["EXCLUDED_MAIN_SELECTION.json"]), "r2-excluded-exact-ids")
    _same((len(selected), len(excluded), len(_selected("pilot"))), (720, 240, 240),
          "r2-owned-versus-selected-counts")
    _same(list(_MAIN_CELLS), _parse(new["MAIN_CELLS.json"]), "r2-complete-main-cells")
    for name in ("WIRE_SCHEMAS.json", "SOURCE_PATHS.json", "PROTOCOLS.json",
                 "H3_ARITHMETIC_CASES.json"):
        _same(new[name], old[name], "r2-unchanged-wire-and-mathematics-" + name)
    old_rows = old["MAIN_SCHEDULE.tsv"].splitlines(keepends=True)
    new_rows = new["MAIN_SCHEDULE.tsv"].splitlines(keepends=True)
    _same(new_rows, old_rows[:5761], "r2-original-index-and-route-order-preserved")
    _same(len(_parse(old["H3_ROUTE_MEDIAN_CASES.json"])["Standard"]["triples"]), 320,
          "r1-h3-reference-not-overwritten")
    _same(len(_parse(old["H5_BOUNDARY_CASES.json"])[0]["pairs"]), 960,
          "r1-h5-reference-not-overwritten")
    original_faults = _parse(old["FAULT_DECLARATIONS.json"])
    revised_faults = _parse(new["FAULT_DECLARATIONS.json"])
    _same([item["id"] for item in revised_faults], [item["id"] for item in original_faults],
          "r2-all-143-original-fault-ids")
    _same(len(revised_faults), 143, "r2-fault-family-count")
    changed = [before["id"] for before, after in zip(original_faults, revised_faults, strict=True)
               if before != after]
    _same(changed, ["U21BF118", "U21BF119", "U21BF121", "U21BF128"],
          "r2-exact-textually-versioned-families")


def test_r2_synthetic_pilot_bytes_and_h3_series_remain_independently_bound():
    with zipfile.ZipFile(io.BytesIO(_bank()["SYNTHETIC_WIRE_BANK.zip"])) as original:
        pilot_names = [name for name in original.namelist() if name.startswith("pilot/")]
        _same(len(pilot_names), 485, "r2-all-original-synthetic-pilot-files")
        for name in pilot_names:
            _same(_wire_bank()[name], original.read(name), "r2-original-pilot-image-" + name)
    triples = _parse(_r2_bank()["H3_SERIES.json"])
    _same(len(triples), 240, "r2-complete-registered-series")
    collected = []
    for triple in triples:
        _same(triple["b"], [1, 8, 64], "r2-matched-bit-axis")
        _same(triple["routes"], list(_ROUTES), "r2-separate-route-series")
        for b, rid in zip(triple["b"], triple["recipes"], strict=True):
            ref = _references()[rid]
            _same((ref["n"], ref["tau"], ref["capacity_mode"], ref["seed"], ref["b"]),
                  (triple["n"], triple["tau"], triple["capacity_mode"], triple["seed"], b),
                  "r2-series-recipe-binding")
            _same(_support_hash(_parse(_input(rid))), triple["support_sha256"],
                  "r2-series-independent-support")
            collected.append(rid)
    _same(tuple(sorted(collected)), _selected("main"), "r2-every-selected-recipe-in-a-triple")


@pytest.mark.parametrize("fault", ["missing", "corrupt", "symlink"])
def test_r2_excluded_n16_input_still_validated_before_main(tmp_path, fault):
    with _sandbox(tmp_path) as box:
        rid = _parse(_r2_bank()["EXCLUDED_MAIN_SELECTION.json"])[-1]
        _need(rid not in _selected("main") and rid in _REGISTRY, "r2-excluded-still-owned")
        leaf = box.inputs / "unit21-v2" / (rid + ".json")
        original = leaf.read_bytes()
        if fault == "missing":
            leaf.unlink()
        elif fault == "corrupt":
            leaf.write_bytes(original + b" ")
        else:
            twin = box.root.parent / "excluded-input-target.json"
            twin.write_bytes(original)
            leaf.unlink()
            leaf.symlink_to(twin)
        script = _Script(box, "main")
        with pytest.raises(ValueError) as failure:
            _invoke(box, "main")
        _same(type(failure.value), ValueError, "r2-excluded-input-reject-not-repair")
        _same(script.calls, [], "r2-excluded-input-before-any-main-solve")
        _need(not box.output.exists(), "r2-excluded-input-before-output")
        if fault == "missing":
            _need(not leaf.exists(), "r2-missing-excluded-input-not-recreated")
        elif fault == "corrupt":
            _same(leaf.read_bytes(), original + b" ", "r2-invalid-excluded-input-not-rewritten")
        else:
            _need(leaf.is_symlink(), "r2-excluded-symlink-not-repaired")
            _same(twin.read_bytes(), original, "r2-excluded-symlink-target-preserved")
