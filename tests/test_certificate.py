"""Unit 17 consuming tests under DESIGN 4.14 / TEST_PLAN 39-40.

The committed ORACLE-126+ human tables are the only fixture authority.  The
embedded byte-pair oracle is the exact independently fixed Phase C source;
its namespace and fresh-process runs cannot import production.  No test
implements an optimizer or a production certificate codec.  RED must be
missing exactfrac.certificate, not a substitute implementation.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import inspect
import json
import os
import subprocess
import sys
from collections import Counter
from dataclasses import fields, is_dataclass
from fractions import Fraction
from pathlib import Path
from typing import get_type_hints

import pytest

# Keep the deliberately missing import in its own sortable block across RED/GREEN.
# isort: split
import exactfrac.certificate as certificate

# isort: split
import exactfrac.solve as solver
import exactfrac.telemetry as telemetry
from exactfrac.instance import Instance
from exactfrac.solve import SolveResult, SolveStats
from exactfrac.witness import ExactValue, Witness

_ROOT = Path(__file__).resolve().parents[1]
_CATALOGUE = _ROOT / "docs/ORACLE_CATALOG.md"
_CATALOGUE_SHA = "04ef6a4b38463aecb0d86731d1873aadb4acb8bc8a8593e0ea82b4325e56e7ac"
_ROUTES = ("Standard", "Accelerated")
_FORMAT = "exactfrac-certificate/1"
_BASE_KEYS = ("format", "empty", "N", "D")
_FULL_KEYS = (*_BASE_KEYS, "U", "y")
_SYMBOLS = {
    "T": 10**4800, "Tm1": 10**4800 - 1, "Tp1": 10**4800 + 1,
    "twoT": 2 * 10**4800, "twoTm2": 2 * 10**4800 - 2, "minusT": -(10**4800),
}

# Exact Phase C test-only source.  Embedding preserves one-file Phase D scope and
# allows isolation without importing this consuming module or a handoff helper.
_INDEPENDENT_SOURCE = (
    '"""Phase C test-only byte-pair oracle; not Unit 18 production code.\n'
    '\n'
    'No ExactFrac imports, no production helpers, no file I/O and no expected answers.\n'
    'The public-to-this-private-module verification function accepts only two bytes objects.\n'
    'A lexical certificate grammar is checked without re-encoding the decoded object.\n'
    '"""\n'
    'import json\n'
    'import re\n'
    '\n'
    "_NUM = rb'(?:0|[1-9][0-9]*)'\n"
    "_POS = rb'(?:[1-9][0-9]*)'\n"
    "_U = rb'\\[' + _NUM + rb'(?:,' + _NUM + rb')*\\]'\n"
    "_PAIR = rb'\\[' + _NUM + rb',' + _POS + rb'\\]'\n"
    "_Y = rb'\\[(?:' + _PAIR + rb'(?:,' + _PAIR + rb')*)?\\]'\n"
    '_EMPTY = rb\'\\{"format":"exactfrac-certificate/1","empty":true,"N":\' + _NUM + rb\',"D":'
    "' + _POS + rb'\\}\\n'\n"
    '_NONEMPTY = (rb\'\\{"format":"exactfrac-certificate/1","empty":false,"N":\' + _NUM\n'
    '            + rb\',"D":\' + _POS + rb\',"U":\' + _U + rb\',"y":\' + _Y + rb\'\\}\\n\')\n'
    "_CERTIFICATE = re.compile(rb'(?:' + _EMPTY + rb'|' + _NONEMPTY + rb')')\n"
    "_INTEGER = re.compile(r'(?:0|-?[1-9][0-9]*)')\n"
    '\n'
    '\n'
    'def _require(condition, reason):\n'
    '    if not condition:\n'
    '        raise ValueError(reason)\n'
    '\n'
    '\n'
    'def _decimal(token):\n'
    "    _require(_INTEGER.fullmatch(token) is not None, 'noncanonical integer token')\n"
    "    negative = token.startswith('-')\n"
    '    digits = token[1:] if negative else token\n'
    '    value = 0\n'
    '    # No full-token int conversion; each conversion is at most seven digits.\n'
    '    for position in range(0, len(digits), 7):\n'
    '        chunk = digits[position:position + 7]\n'
    '        value = value * (10 ** len(chunk)) + int(chunk)\n'
    '    return -value if negative else value\n'
    '\n'
    '\n'
    'def _no_noninteger(_token):\n'
    "    raise ValueError('noninteger number token')\n"
    '\n'
    '\n'
    'def _object(pairs):\n'
    '    result = {}\n'
    '    for key, value in pairs:\n'
    "        _require(key not in result, 'duplicate decoded key')\n"
    '        result[key] = value\n'
    '    return result\n'
    '\n'
    '\n'
    'def _parse(raw):\n'
    "    _require(type(raw) is bytes, 'serialized input must be exact bytes')\n"
    "    _require(not raw.startswith(b'\\xef\\xbb\\xbf'), 'UTF-8 BOM forbidden')\n"
    '    try:\n'
    "        text = raw.decode('utf-8')\n"
    '    except UnicodeDecodeError as exc:\n'
    "        raise ValueError('invalid UTF-8') from exc\n"
    '    try:\n'
    '        return json.loads(text, object_pairs_hook=_object, parse_int=_decimal,\n'
    '                          parse_float=_no_noninteger, parse_constant=_no_noninteger)\n'
    '    except json.JSONDecodeError as exc:\n'
    "        raise ValueError('invalid JSON document') from exc\n"
    '\n'
    '\n'
    'def parse_instance(raw):\n'
    '    """Decode and validate canonical graph data; do not sort or aggregate."""\n'
    '    data = _parse(raw)\n'
    "    _require(type(data) is dict, 'instance must be object')\n"
    '    keys = set(data)\n'
    "    _require(keys in ({'format', 'n', 'edges', 'f'},\n"
    "                      {'format', 'n', 'edges', 'f', 'labels'}), 'instance fields')\n"
    "    _require(type(data['format']) is str and data['format'] == 'exactfrac-instance/1',\n"
    "             'instance format')\n"
    "    n = data['n']\n"
    "    _require(type(n) is int and n >= 1, 'positive integer n')\n"
    "    f = data['f']\n"
    "    _require(type(f) is list and len(f) == n, 'f length/type')\n"
    "    _require(all(type(x) is int and x >= 1 for x in f), 'positive integer f')\n"
    "    if 'labels' in data:\n"
    "        labels = data['labels']\n"
    "        _require(type(labels) is list and len(labels) == n, 'labels length/type')\n"
    "        _require(all(type(x) in (int, str) for x in labels), 'label exact types')\n"
    "        _require(len(set(labels)) == len(labels), 'duplicate labels')\n"
    "    edges = data['edges']\n"
    "    _require(type(edges) is list and len(edges) > 0, 'nonempty support')\n"
    '    degrees = [0] * n\n'
    '    previous = None\n'
    '    for edge in edges:\n'
    "        _require(type(edge) is list and len(edge) == 3, 'edge shape')\n"
    '        u, v, q = edge\n'
    "        _require(all(type(x) is int for x in edge), 'integer edge fields')\n"
    "        _require(0 <= u < v < n and q >= 1, 'edge range/orientation/multiplicity')\n"
    "        _require(previous is None or previous < (u, v), 'strict canonical edge order')\n"
    '        previous = (u, v)\n'
    '        degrees[u] += q\n'
    '        degrees[v] += q\n'
    "    _require(all(cap <= degree for cap, degree in zip(f, degrees)), 'active condition')\n"
    '    return data\n'
    '\n'
    '\n'
    'def verify(instance_bytes, certificate_bytes):\n'
    '    """Independently return a decoded certificate iff admissible/raw-attaining or Empty.'
    '\n'
    '\n'
    '    Validation of the complete instance precedes parsing the certificate and hence\n'
    '    precedes every interpretation of an edge reference. No optimality is asserted.\n'
    '    """\n'
    '    instance = parse_instance(instance_bytes)\n'
    "    _require(type(certificate_bytes) is bytes, 'certificate must be exact bytes')\n"
    "    _require(_CERTIFICATE.fullmatch(certificate_bytes) is not None, 'certificate wire gra"
    "mmar')\n"
    '    cert = _parse(certificate_bytes)\n'
    '    # Grammar checks precede object creation; duplicate/escaped/reordered keys cannot mat'
    'ch.\n'
    "    _require(type(cert) is dict, 'certificate object')\n"
    "    _require(type(cert['empty']) is bool and type(cert['N']) is int and type(cert['D']) i"
    's int,\n'
    "             'certificate field types')\n"
    "    _require(cert['N'] >= 0 and cert['D'] > 0, 'certificate signs')\n"
    "    if cert['empty']:\n"
    "        _require(sum(edge[2] for edge in instance['edges']) == 1, 'false Empty')\n"
    "        _require((cert['N'], cert['D']) == (0, 1), 'literal Empty pair')\n"
    '        return cert\n'
    "    U = cert['U']\n"
    "    _require(type(U) is list and bool(U), 'nonempty U')\n"
    "    _require(all(type(v) is int and 0 <= v < instance['n'] for v in U), 'vertex range/typ"
    "e')\n"
    "    _require(all(a < b for a, b in zip(U, U[1:])), 'strict U order')\n"
    '    shore = set(U)\n'
    "    y = cert['y']\n"
    "    _require(type(y) is list, 'sparse list')\n"
    '    previous = -1\n'
    '    selected = 0\n'
    '    for entry in y:\n'
    "        _require(type(entry) is list and len(entry) == 2, 'sparse pair shape')\n"
    '        ref, count = entry\n'
    "        _require(type(ref) is int and type(count) is int, 'sparse exact integers')\n"
    "        _require(previous < ref < len(instance['edges']), 'sparse reference order/range')"
    '\n'
    '        previous = ref\n'
    "        u, v, q = instance['edges'][ref]\n"
    "        _require(0 < count <= q, 'sparse positive bounded count')\n"
    "        _require((u in shore) != (v in shore), 'sparse crossing constraint')\n"
    '        selected += count\n'
    "    s = sum(instance['f'][v] for v in U)\n"
    "    e = sum(q for u, v, q in instance['edges'] if u in shore and v in shore)\n"
    "    _require((s + selected) % 2 == 1, 'odd admissibility')\n"
    "    _require(s + selected >= 3, 'minimum admissibility')\n"
    "    _require(cert['N'] == 2 * (e + selected), 'literal numerator')\n"
    "    _require(cert['D'] == s + selected - 1, 'literal denominator')\n"
    '    return cert\n'
)
_INDEPENDENT_SHA = '95c1031fc387b765569fc381062384b8919a79f12128883becfc11ad7236bff6'

_FROZEN_PRODUCTION = {
    'exactfrac/__init__.py':
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    'exactfrac/_telemetry.py':
        '3be3cae6757db921aacdde7fbae2cb59cfa1b91b73bd9c16c0695a1f620b9cac',
    'exactfrac/branch.py':
        '584d2f262c94e227f3832563aeceff600c95c6943b0401bd8ef64e3c2a5ef057',
    'exactfrac/families.py':
        '92830c7cac7a6f39df5f16f316295352dee9e65bc31fe1220a85305cacd9872b',
    'exactfrac/flow.py':
        'ee318ccbdfc59cadccd055dd1b57e016a1288387afb124792b52ce39c2b76fcc',
    'exactfrac/instance.py':
        '32695ee226d3636451d2964ee99bca0ed4cd9cc4a71542ffd435504a3918558e',
    'exactfrac/oracle.py':
        'fa8885689608cc216e131cdc63573f698f628b1a9e313bde521e1f3feff88913',
    'exactfrac/parity_cut.py':
        'f0cb4bbb38f80f05459c89662d3ee7fc3e09b63e1ca985ea37ccbfc9e0f85ec1',
    'exactfrac/rational.py':
        '933a1b79187bd8c93dddb8a93e9e92708775d980d2161f971a597a5f61a27a4b',
    'exactfrac/shore.py':
        '323fa6f5074a83dcedd16acadf8bc99905396298c7609cacab871f4dccab0415',
    'exactfrac/sign_routing.py':
        'e0bd497b5034cee544332901d937f1973a6f37fbffb281337e4b091dabdb2beb',
    'exactfrac/solve.py':
        '46773d6f2247025220712e967315a33ff36bea60328bcc2b9b149d824f4d6e51',
    'exactfrac/telemetry.py':
        'aadcbcd00fae3eba9e61a8433b90dae47ab0e67e91fa911cf57d909cef249bd3',
    'exactfrac/witness.py':
        '1225387644890efe4d70e9ede64d07b612b599f70c73b7de5378781fd17ceb6a',
    'exactfrac_verify/__init__.py':
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    'exactfrac_verify/brute.py':
        'b31e53a8b16a37ef8827141a78169ffe9b0a84762843a3ad45c89d9344f98bf6',
}


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def _number(value):
    if type(value) is tuple and len(value) == 2 and value[0] == "sym":
        return _SYMBOLS[value[1]]
    _require(type(value) is int, "fixture requires an exact integer or named symbol")
    return value


def _digits(value):
    """Independent test transport; never used to derive expected certificate bytes."""
    negative = value < 0
    value = abs(value)
    if value == 0:
        return b"0"
    chunks = []
    while value:
        value, remainder = divmod(value, 100000)
        chunks.append(remainder)
    raw = str(chunks.pop()).encode("ascii")
    raw += b"".join(f"{chunk:05d}".encode("ascii") for chunk in reversed(chunks))
    return (b"-" if negative else b"") + raw


def _transport(value):
    """Encode primitive test data, not a production Instance.to_dict result."""
    if value is None:
        return b"null"
    if type(value) is bool:
        return b"true" if value else b"false"
    if type(value) is int:
        return _digits(value)
    if type(value) is str:
        return json.dumps(value, ensure_ascii=True).encode("ascii")
    if type(value) in (list, tuple):
        return b"[" + b",".join(_transport(item) for item in value) + b"]"
    if type(value) is dict:
        return b"{" + b",".join(
            _transport(key) + b":" + _transport(item) for key, item in value.items()
        ) + b"}"
    raise AssertionError("unsupported test transport type")


def _fingerprint(rows):
    return _sha(b"".join(_transport(row) + b"\n" for row in rows))


def _tables():
    result = {}
    current = None
    header = False
    for line in _CATALOGUE.read_text(encoding="utf-8").splitlines():
        if line.startswith("### Fixture table: "):
            name = line.split(": ", 1)[1]
            current = name if name.startswith(("U15_INPUTS", "U16_INPUTS", "U17_")) else None
            if current:
                _require(name not in result, "duplicate fixture table")
                result[name] = []
                header = True
        elif current and line.startswith("| "):
            cells = [value.strip() for value in line[1:-1].split("|")]
            if header:
                header = False
            elif not all(value == "---" for value in cells):
                _require(all(value.startswith("`") and value.endswith("`") for value in cells),
                         "nonliteral fixture cell")
                result[current].append(tuple(ast.literal_eval(value[1:-1]) for value in cells))
        elif current and line.strip():
            current = None
    return result


def _registry(tables):
    records = []
    for key, _kind, n, edges, f, labels in tables["U15_INPUTS"]:
        records.append(("U15_INPUTS/" + key, n, edges, f, labels))
    for key, n, edges, f, labels in tables["U16_INPUTS"]:
        records.append(("U16_INPUTS/" + key, n, edges, f, labels))
    for key, n, edges, f, labels in tables["U17_INPUTS"]:
        records.append(("U17_INPUTS/" + key, n, edges, f, labels))
    graphs = []
    for key, n, edges, f, labels in records:
        graph = {
            "format": "exactfrac-instance/1", "n": n,
            "edges": [[u, v, _number(q)] for u, v, q in edges],
            "f": [_number(value) for value in f],
        }
        if labels is not None:
            graph["labels"] = [
                _number(value) if type(value) is tuple else value for value in labels
            ]
        graphs.append((key, graph))
    _require(len({key for key, _ in graphs}) == len(graphs), "duplicate qualified registry ID")
    return graphs


def _recipe(parts):
    """Only literal bytes and the catalogue's literal repetition recipes."""
    pieces = []
    for part in parts:
        if type(part) is str:
            pieces.append(part.encode("ascii"))
        else:
            _require(type(part) is tuple and len(part) == 3 and part[0] == "repeat",
                     "bad literal byte recipe")
            char, count = part[1:]
            _require(type(char) is str and len(char) == 1 and type(count) is int and count >= 0,
                     "bad literal byte repetition")
            pieces.append(char.encode("ascii") * count)
    return b"".join(pieces)


def _new_wire():
    # No production object or function enters this namespace.  The sole inputs to
    # verify are independently serialized instance bytes and certificate bytes.
    namespace = {"__name__": "_unit17_independent_wire"}
    exec(compile(_INDEPENDENT_SOURCE, "<unit17-independent-wire>", "exec"), namespace)
    return namespace


_TABLES = _tables()
_REGISTRY = _registry(_TABLES)
_GRAPHS = dict(_REGISTRY)
_FIXTURES = {row[0]: row for row in _TABLES["U17_BYTES"]}
_GLOBALS = {row[0]: row for row in _TABLES["U17_GLOBALS"]}
_OBJECT_WIRE_CASES = [
    row for row in _TABLES["U17_WIRE_REJECT"]
    if row[2] == "certificate" and all(op[0] in ("set", "delete", "quote_field") for op in row[3])
]


def _fixture_object(row):
    _, _, _, vertices, sparse, numerator, denominator, *_ = row
    obj = {"format": _FORMAT, "empty": vertices is None,
           "N": _number(numerator), "D": _number(denominator)}
    if vertices is not None:
        obj["U"] = list(vertices)
        obj["y"] = [[ref, _number(count)] for ref, count in sparse]
    return obj


def _instance(graph):
    return Instance(graph["n"], tuple(tuple(edge) for edge in graph["edges"]),
                    tuple(graph["f"]), None if "labels" not in graph else tuple(graph["labels"]))


def _result(row):
    obj = _fixture_object(row)
    if obj["empty"]:
        return SolveResult(ExactValue(obj["N"], obj["D"]), None)
    dense = [0] * len(_GRAPHS[row[1]]["edges"])
    for ref, count in obj["y"]:
        dense[ref] = count
    mask = sum(1 << vertex for vertex in obj["U"])
    return SolveResult(ExactValue(obj["N"], obj["D"]), Witness(mask, tuple(dense)))


def _snapshot(value):
    """Check exact types, values, order and mutable identities without coercion."""
    kind = type(value)
    if kind in (str, int, bool, float, type(None), bytes, Fraction):
        return kind, value
    if isinstance(value, dict):
        return kind, id(value), tuple((_snapshot(k), _snapshot(v)) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return kind, id(value), tuple(_snapshot(item) for item in value)
    if is_dataclass(value):
        return kind, id(value), tuple((item.name, _snapshot(getattr(value, item.name)))
                                     for item in fields(value))
    return kind, id(value)


def _exact_error(error_type, function, *args, **kwargs):
    before = _snapshot((args, kwargs))
    # args/kwargs wrappers are not retained; inspect their children instead.
    before = before[2]
    with pytest.raises(error_type) as caught:
        function(*args, **kwargs)
    assert type(caught.value) is error_type
    assert _snapshot((args, kwargs))[2] == before
    return caught.value


def _bindings():
    result = {}
    for node in ast.walk(ast.parse(Path(certificate.__file__).read_bytes())):
        if isinstance(node, ast.ImportFrom):
            for item in node.names:
                result[item.name] = item.asname or item.name
    return result


def _patch_dependency(monkeypatch, name, replacement):
    bindings = _bindings()
    assert name in bindings, "the ruled closed dependency must be imported"
    monkeypatch.setattr(certificate, bindings[name], replacement)


def _certificate_call(api, instance, argument):
    function = getattr(certificate, api)
    before = (_snapshot(instance), _snapshot(argument))
    answer = function(instance, argument)
    assert (_snapshot(instance), _snapshot(argument)) == before
    return answer


def _check_object(actual, expected):
    assert type(actual) is dict
    assert tuple(actual) == (_BASE_KEYS if expected["empty"] else _FULL_KEYS)
    assert all(type(key) is str for key in actual)
    assert type(actual["format"]) is str and actual["format"] == _FORMAT
    assert type(actual["empty"]) is bool
    assert type(actual["N"]) is int and type(actual["D"]) is int
    if not actual["empty"]:
        assert type(actual["U"]) is list and all(type(v) is int for v in actual["U"])
        assert type(actual["y"]) is list
        assert all(type(pair) is list and len(pair) == 2
                   and all(type(v) is int for v in pair) for pair in actual["y"])
    assert actual == expected


def _emit(instance, result, instance_bytes, wire):
    obj = _certificate_call("build_certificate", instance, result)
    expected = {"format": _FORMAT, "empty": result.witness is None,
                "N": result.value.N, "D": result.value.D}
    if result.witness is not None:
        expected["U"] = [v for v in range(instance.n) if result.witness.U & (1 << v)]
        expected["y"] = [[ref, count] for ref, count in enumerate(result.witness.y) if count]
    _check_object(obj, expected)
    raw = _certificate_call("serialize_certificate", instance, obj)
    assert type(raw) is bytes
    assert wire["verify"](instance_bytes, raw) == expected
    return raw


def _mutate(raw, operations, wire):
    for operation in operations:
        op = operation[0]
        if op in ("set", "delete"):
            document = wire["_parse"](raw)
            target = document
            for part in operation[1][:-1]:
                target = target[part]
            if op == "set":
                target[operation[1][-1]] = copy.deepcopy(operation[2])
            else:
                del target[operation[1][-1]]
            raw = _transport(document) + (b"\n" if raw.endswith(b"\n") else b"")
        elif op == "replace":
            old, new = operation[1].encode("utf-8"), operation[2].encode("utf-8")
            assert raw.count(old) == 1
            raw = raw.replace(old, new)
        elif op == "prefix":
            raw = operation[1].encode("utf-8") + raw
        elif op == "prefix_hex":
            raw = bytes.fromhex(operation[1]) + raw
        elif op == "suffix":
            raw += operation[1].encode("utf-8")
        elif op == "strip_final_lf":
            assert raw.endswith(b"\n")
            raw = raw[:-1]
        elif op == "reverse_keys":
            raw = _transport(dict(reversed(list(wire["_parse"](raw).items())))) + (
                b"\n" if raw.endswith(b"\n") else b""
            )
        elif op == "pretty":
            raw = json.dumps(wire["_parse"](raw), ensure_ascii=True, indent=2).encode() + b"\n"
        elif op == "utf8_strings":
            raw = json.dumps(wire["_parse"](raw), ensure_ascii=False,
                             separators=(",", ":")).encode("utf-8")
        elif op == "quote_field":
            token = b'"' + operation[1].encode() + b'":'
            start = raw.index(token) + len(token)
            end = start
            while end < len(raw) and 48 <= raw[end] <= 57:
                end += 1
            raw = raw[:start] + b'"' + raw[start:end] + b'"' + raw[end:]
        else:
            raise AssertionError("unknown registered wire operation")
    return raw


def _wire_pair(row, wire):
    _, fixture_id, stream, operations, *_ = row
    fixture = _FIXTURES[fixture_id]
    instance_bytes = _transport(_GRAPHS[fixture[1]])
    certificate_bytes = _recipe(fixture[7])
    mutated = _mutate(instance_bytes if stream == "instance" else certificate_bytes,
                      operations, wire)
    assert len(mutated) == row[-2] and _sha(mutated) == row[-1]
    return ((mutated, certificate_bytes) if stream == "instance"
            else (instance_bytes, mutated))


@pytest.fixture
def wire():
    return _new_wire()


def test_closed_fixture_authority_and_registry_identity():
    catalogue_bytes = _CATALOGUE.read_bytes()
    assert len(catalogue_bytes) >= 3_212_040
    assert _sha(catalogue_bytes[:3_212_040]) == _CATALOGUE_SHA
    assert _sha(_INDEPENDENT_SOURCE.encode()) == _INDEPENDENT_SHA
    assert len(_TABLES["U15_INPUTS"]) == 379
    assert _fingerprint(_TABLES["U15_INPUTS"]) == (
        "98d3f32c3dde19670e36900525b8bd6623ca4fd932c804d47725d305fd45b90c"
    )
    assert len(_TABLES["U16_INPUTS"]) == 10
    assert _fingerprint(_TABLES["U16_INPUTS"]) == (
        "231d5dc3d91429aed5c78e890c25ccfb2456dbe1551e59ef566359bfa5a91df9"
    )
    names = {name for name in _TABLES if name.startswith("U17_")}
    assert {row[0] for row in _TABLES["U17_FINGERPRINTS"]} == names - {"U17_FINGERPRINTS"}
    for name, count, digest in _TABLES["U17_FINGERPRINTS"]:
        assert len(_TABLES[name]) == count and _fingerprint(_TABLES[name]) == digest
    assert _TABLES["U17_REGISTRY"] == [
        (name, len(_TABLES[name]), _fingerprint(_TABLES[name]))
        for name in ("U15_INPUTS", "U16_INPUTS", "U17_INPUTS")
    ]
    census = dict(_TABLES["U17_CENSUS"])
    assert len(_REGISTRY) == census["cumulative_registry_identities"] == 396
    assert len(_REGISTRY) * len(_ROUTES) == 792
    assert census["required_real_solves_per_cumulative_pass"] == 792
    assert _fingerprint(_REGISTRY) == census["cumulative_graph_stream_sha256"]
    assert list(_GLOBALS) == [key for key, _ in _REGISTRY]
    for expected, (key, graph) in zip(_TABLES["U17_INSTANCE_BYTES"], _REGISTRY, strict=True):
        raw = _transport(graph)
        assert expected == (key, len(raw), _sha(raw))
    for name, parts, _description in _TABLES["U17_SYMBOLS"]:
        assert _new_wire()["_decimal"](_recipe(parts).decode()) == _SYMBOLS[name]


def test_exact_public_surface_and_closed_record_ownership():
    assert certificate.__all__ == ("build_certificate", "serialize_certificate")
    assert type(certificate.__all__) is tuple
    for name, second, annotation, output in (
        ("build_certificate", "result", SolveResult, dict[str, object]),
        ("serialize_certificate", "certificate", dict[str, object], bytes),
    ):
        function = getattr(certificate, name)
        parameters = inspect.signature(function).parameters
        assert tuple(parameters) == ("instance", second)
        assert all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
                   and p.default is inspect.Parameter.empty for p in parameters.values())
        assert get_type_hints(function) == {
            "instance": Instance, second: annotation, "return": output,
        }
    assert tuple(item.name for item in fields(SolveResult)) == ("value", "witness")
    assert (_ROOT / "exactfrac/__init__.py").read_bytes() == b""
    assert (_ROOT / "exactfrac_verify/__init__.py").read_bytes() == b""


@pytest.mark.parametrize("fixture_id", tuple(_FIXTURES))
def test_literal_bytes_and_detached_record_construction(fixture_id, wire):
    row = _FIXTURES[fixture_id]
    instance = _instance(_GRAPHS[row[1]])
    result = _result(row)
    expected = _fixture_object(row)
    raw = _recipe(row[7])
    assert len(raw) == row[8] and _sha(raw) == row[9]
    assert wire["verify"](_transport(_GRAPHS[row[1]]), raw) == expected
    # No builder call is needed to serialize an independently specified object.
    assert _certificate_call("serialize_certificate", instance, expected) == raw
    first = _certificate_call("build_certificate", instance, result)
    _check_object(first, expected)
    assert _certificate_call("serialize_certificate", instance, first) == raw
    second = certificate.build_certificate(instance=instance, result=result)
    assert second is not first
    _check_object(second, expected)
    assert certificate.serialize_certificate(instance=instance, certificate=second) == raw
    if not expected["empty"]:
        assert first["U"] is not second["U"] and first["y"] is not second["y"]
        for left, right in zip(first["y"], second["y"], strict=True):
            assert left is not right
        first["U"].append(instance.n)
        if first["y"]:
            first["y"][0][1] += 1
        else:
            first["y"].append([0, 1])
    first["N"] = -1
    _check_object(second, expected)
    _check_object(certificate.build_certificate(instance, result), expected)
    _exact_error(ValueError, certificate.serialize_certificate, instance, first)


@pytest.mark.parametrize("fixture_id", tuple(_FIXTURES))
def test_repeated_and_reordered_object_serialization(fixture_id):
    row = _FIXTURES[fixture_id]
    instance, result = _instance(_GRAPHS[row[1]]), _result(row)
    expected = _recipe(row[7])
    obj = _fixture_object(row)
    reverse = dict(reversed(list(obj.items())))
    for _ in range(3):
        assert _certificate_call("serialize_certificate", instance, reverse) == expected
        assert _certificate_call("serialize_certificate", instance, obj) == expected
        built = certificate.build_certificate(instance, result)
        assert certificate.serialize_certificate(instance, built) == expected


@pytest.mark.parametrize("row", _TABLES["U17_WIRE_REJECT"], ids=lambda row: row[0])
def test_independent_malformed_wire_rejections(row, wire):
    instance_bytes, certificate_bytes = _wire_pair(row, wire)
    if row[5]:
        before = wire["_parse"](_recipe(_FIXTURES[row[1]][7]))
        after = wire["_parse"](certificate_bytes)
        assert before["N"] * after["D"] == after["N"] * before["D"]
    _exact_error(ValueError, wire["verify"], instance_bytes, certificate_bytes)


@pytest.mark.parametrize("row", _TABLES["U17_WIRE_ACCEPT"], ids=lambda row: row[0])
def test_independent_instance_wire_variants(row, wire):
    pair = _wire_pair(row, wire)
    assert wire["verify"](*pair) == _fixture_object(_FIXTURES[row[1]])


@pytest.mark.parametrize("row", _OBJECT_WIRE_CASES, ids=lambda row: row[0])
def test_serializer_rejects_registered_object_corruptions(row, wire):
    # Only object-semantic mutations are asserted at the serializer boundary.
    # Reordered keys/JSON whitespace/duplicate spellings belong to the byte route.
    instance_bytes, raw = _wire_pair(row, wire)
    obj = wire["_parse"](raw)
    instance = _instance(_GRAPHS[_FIXTURES[row[1]][1]])
    _exact_error(ValueError, certificate.serialize_certificate, instance, obj)
    _exact_error(ValueError, wire["verify"], instance_bytes, raw)


class _IntSubclass(int):
    pass


class _StrSubclass(str):
    pass


class _ListSubclass(list):
    pass


class _DictSubclass(dict):
    pass


class _InstanceSubclass(Instance):
    __slots__ = ()


class _ResultSubclass(SolveResult):
    __slots__ = ()


class _CoercibleInt:
    def __init__(self, value):
        self.value = value

    def __int__(self):
        raise AssertionError("the boundary must not coerce")

    def __index__(self):
        raise AssertionError("the boundary must not coerce")


class _Duck:
    def __getattr__(self, name):
        raise AssertionError("the boundary must check exact type before attribute reads: " + name)


class _DependencyError(Exception):
    pass


def _retype(value, tag):
    conversions = {
        "bool": bool, "int": int, "int-subclass": _IntSubclass, "float": float,
        "Fraction": Fraction, "coercible-int": _CoercibleInt, "list-subclass": _ListSubclass,
        "dict-subclass": _DictSubclass, "tuple": tuple, "str-subclass": _StrSubclass,
    }
    return conversions[tag](value)


def _object_case(row):
    _case, api, fixture_id, operation, *_ = row
    fixture = _FIXTURES[fixture_id]
    graph = _GRAPHS[fixture[1]]
    instance, result, obj = _instance(graph), _result(fixture), _fixture_object(fixture)
    if operation[0] == "normal-result":
        value, U, y = operation[1:]
        result = SolveResult(ExactValue(*value), None if U is None else Witness(U, y))
    elif operation[0] == "argument":
        name, tag = operation[1:]
        replacements = {
            "None": lambda: None, "dict-from-primitive": lambda: copy.deepcopy(graph),
            "Instance-subclass": lambda: _InstanceSubclass(instance.n, instance.edges, instance.f,
                                                          instance.labels),
            "duck-instance": _Duck, "duck-result": _Duck,
            "outer-(SolveResult,SolveStats)": lambda: (
                result, SolveStats("Standard", (), "Baseline"),
            ),
            "SolveResult-subclass": lambda: _ResultSubclass(result.value, result.witness),
            "certificate-dict": lambda: obj, "bytes-of-fixture": lambda: _recipe(fixture[7]),
            "str-of-fixture": lambda: _recipe(fixture[7]).decode("ascii"),
            "dict-subclass": lambda: _DictSubclass(obj), "list-of-items": lambda: list(obj.items()),
            "SolveResult": lambda: result,
        }
        replacement = replacements[tag]()
        if name == "instance":
            instance = replacement
        elif name == "result":
            result = replacement
        else:
            assert name == "certificate"
            obj = replacement
    else:
        assert operation[0] == "retype"
        path, tag = operation[1:]
        if path == ("format-key",):
            obj = {(_StrSubclass(key) if key == "format" else key): value
                   for key, value in obj.items()}
        elif not path:
            obj = _retype(obj, tag)
        else:
            parent = obj
            for key in path[:-1]:
                parent = parent[key]
            parent[path[-1]] = _retype(parent[path[-1]], tag)
    return api, instance, result if api == "build_certificate" else obj


@pytest.mark.parametrize("row", _TABLES["U17_OBJECT_CASES"], ids=lambda row: row[0])
def test_registered_exact_type_and_normal_record_rejections(row):
    api, instance, argument = _object_case(row)
    assert row[4] == "ValueError"
    _exact_error(ValueError, getattr(certificate, api), instance, argument)


@pytest.mark.parametrize("row", _TABLES["U17_PROMISE_FAULTS"], ids=lambda row: row[0])
def test_registered_normal_return_promise_faults(row, monkeypatch):
    _, api, fixture_id, dependency, specification, exception = row
    instance, result, obj = (_instance(_GRAPHS[_FIXTURES[fixture_id][1]]),
                             _result(_FIXTURES[fixture_id]), _fixture_object(_FIXTURES[fixture_id]))
    tag, *values = specification
    wrong = bool(values[0]) if tag == "bool" else tuple(values) if tag == "tuple" else list(values)
    calls = []

    def normal_fault(*args):
        calls.append(args)
        return copy.deepcopy(wrong)

    _patch_dependency(monkeypatch, dependency, normal_fault)
    assert exception == "RuntimeError"
    _exact_error(RuntimeError, getattr(certificate, api), instance,
                 result if api == "build_certificate" else obj)
    assert len(calls) == 1


@pytest.mark.parametrize("row", _TABLES["U17_EXCEPTIONS"],
                         ids=lambda row: "-".join(row[:4]))
def test_registered_dependency_exception_identity(row, monkeypatch):
    api, dependency, fixture_id, kind, _ = row
    error_type = {"ValueError": ValueError, "RuntimeError": RuntimeError, "TypeError": TypeError,
                  "MemoryError": MemoryError, "CustomDependencyError": _DependencyError}[kind]
    sentinel = error_type("injected closed-dependency failure")
    calls = []

    def fail(*args):
        calls.append(args)
        raise sentinel

    _patch_dependency(monkeypatch, dependency, fail)
    fixture = _FIXTURES[fixture_id]
    instance = _instance(_GRAPHS[fixture[1]])
    argument = _result(fixture) if api == "build_certificate" else _fixture_object(fixture)
    assert _exact_error(error_type, getattr(certificate, api), instance, argument) is sentinel
    assert len(calls) == 1


def _forbidden(*_args, **_kwargs):
    raise AssertionError("an unowned or premature dependency was invoked")


def _optimizer_barrier(monkeypatch):
    names = {
        "solve", "solve_with_telemetry", "solve_branch_standard", "solve_branch_accelerated",
        "exact_branch_min", "reduce_atomic_family", "minimum_parity_cut", "minimum_cut",
    }
    # Replace test-local runtime bindings, never files or persisted module state.
    for module_name, module in tuple(sys.modules.items()):
        if module_name == "exactfrac" or module_name.startswith("exactfrac."):
            for name in names:
                if hasattr(module, name):
                    monkeypatch.setattr(module, name, _forbidden)


@pytest.mark.parametrize("api", ("build_certificate", "serialize_certificate"))
def test_instance_guard_precedes_every_other_read(api, monkeypatch):
    for name in ("witness_value", "shore_to_list", "dense_y_to_sparse", "shore_from_list",
                 "sparse_y_to_dense", "Witness"):
        _patch_dependency(monkeypatch, name, _forbidden)
    _exact_error(ValueError, getattr(certificate, api), _Duck(), _Duck())


def test_builder_exact_result_guard_precedes_dependencies(monkeypatch):
    for name in ("witness_value", "shore_to_list", "dense_y_to_sparse"):
        _patch_dependency(monkeypatch, name, _forbidden)
    _exact_error(ValueError, certificate.build_certificate,
                 _instance(_GRAPHS[_FIXTURES["H2-ONE"][1]]), _Duck())


@pytest.mark.parametrize("fixture_id", ("EMPTY", "H2-ONE"))
def test_empty_paths_invoke_no_witness_helpers(fixture_id, monkeypatch):
    row = _FIXTURES[fixture_id]
    instance = _instance(_GRAPHS[row[1]])
    result = SolveResult(ExactValue(0, 1), None)
    obj = _fixture_object(_FIXTURES["EMPTY"])
    for name in ("witness_value", "shore_to_list", "dense_y_to_sparse", "shore_from_list",
                 "sparse_y_to_dense", "Witness"):
        _patch_dependency(monkeypatch, name, _forbidden)
    if fixture_id == "EMPTY":
        _check_object(certificate.build_certificate(instance, result), obj)
        assert certificate.serialize_certificate(instance, obj) == _recipe(_FIXTURES["EMPTY"][7])
    else:
        _exact_error(ValueError, certificate.build_certificate, instance, result)
        _exact_error(ValueError, certificate.serialize_certificate, instance, obj)


@pytest.mark.parametrize("key,value", (("N", -1), ("D", 0), ("format", None),
                                      ("empty", 0), ("digest", None)))
def test_serializer_header_guards_precede_payload_helpers(key, value, monkeypatch):
    row = _FIXTURES["H2-ONE"]
    instance, obj = _instance(_GRAPHS[row[1]]), _fixture_object(row)
    obj[key] = value
    obj["U"] = _Duck()
    obj["y"] = _Duck()
    _patch_dependency(monkeypatch, "shore_from_list", _forbidden)
    _patch_dependency(monkeypatch, "sparse_y_to_dense", _forbidden)
    _exact_error(ValueError, certificate.serialize_certificate, instance, obj)


@pytest.mark.parametrize("vertices", ([], [-1], [2], [0, 0], [True], (0,)))
def test_shore_validation_precedes_sparse_decoding(vertices, monkeypatch):
    row = _FIXTURES["H2-ONE"]
    instance, obj = _instance(_GRAPHS[row[1]]), _fixture_object(row)
    obj["U"] = vertices
    _patch_dependency(monkeypatch, "sparse_y_to_dense", _forbidden)
    _exact_error(ValueError, certificate.serialize_certificate, instance, obj)


@pytest.mark.parametrize("entries", (None, [[0]], [[0, 0]], [[1, 2]], [[0, 3]], ((0, 2),)))
def test_sparse_validation_precedes_witness_construction(entries, monkeypatch):
    row = _FIXTURES["H2-ONE"]
    instance, obj = _instance(_GRAPHS[row[1]]), _fixture_object(row)
    obj["y"] = entries
    _patch_dependency(monkeypatch, "Witness", _forbidden)
    _exact_error(ValueError, certificate.serialize_certificate, instance, obj)


@pytest.mark.parametrize("api", ("build_certificate", "serialize_certificate"))
def test_raw_mismatch_does_not_bypass_closed_evaluation(api, monkeypatch):
    row = _FIXTURES["H2-ONE"]
    instance, result, obj = _instance(_GRAPHS[row[1]]), _result(row), _fixture_object(row)
    obj["N"], obj["D"] = 8, 4
    result = SolveResult(ExactValue(8, 4), result.witness)
    sentinel = _DependencyError("evaluation must happen before raw comparison")

    def fail(*_args):
        raise sentinel

    _patch_dependency(monkeypatch, "witness_value", fail)
    assert _exact_error(_DependencyError, getattr(certificate, api), instance,
                        result if api == "build_certificate" else obj) is sentinel


def test_builder_raw_rejection_precedes_exports(monkeypatch):
    row = _FIXTURES["H2-ONE"]
    instance, result = _instance(_GRAPHS[row[1]]), _result(row)
    result = SolveResult(ExactValue(8, 4), result.witness)
    _patch_dependency(monkeypatch, "shore_to_list", _forbidden)
    _patch_dependency(monkeypatch, "dense_y_to_sparse", _forbidden)
    _exact_error(ValueError, certificate.build_certificate, instance, result)


@pytest.mark.parametrize("api,expected", (
    ("build_certificate", ("witness_value", "shore_to_list", "dense_y_to_sparse")),
    ("serialize_certificate", ("shore_from_list", "sparse_y_to_dense", "Witness", "witness_value")),
))
def test_declared_helper_call_order_and_single_consumption(api, expected):
    row = _FIXTURES["H2-ONE"]
    instance = _instance(_GRAPHS[row[1]])
    argument = _result(row) if api == "build_certificate" else _fixture_object(row)
    codes = {}
    for module_name, names in (
        ("exactfrac.shore", ("shore_from_list", "shore_to_list")),
        ("exactfrac.witness", (
            "Witness", "witness_value", "sparse_y_to_dense", "dense_y_to_sparse",
        )),
    ):
        module = sys.modules[module_name]
        for name in names:
            target = getattr(module, name)
            codes[(target.__init__ if name == "Witness" else target).__code__] = name
    calls = []

    def observe(frame, event, _argument):
        if event == "call" and frame.f_code in codes:
            calls.append(codes[frame.f_code])

    old_profile = sys.getprofile()
    try:
        sys.setprofile(observe)
        _certificate_call(api, instance, argument)
    finally:
        sys.setprofile(old_profile)
    assert tuple(calls) == expected


def test_mutation_after_build_is_revalidated():
    row = _FIXTURES["H2-ONE"]
    instance, result = _instance(_GRAPHS[row[1]]), _result(row)
    obj = certificate.build_certificate(instance, result)
    assert certificate.serialize_certificate(instance, obj) == _recipe(row[7])
    obj["D"] = 4
    _exact_error(ValueError, certificate.serialize_certificate, instance, obj)
    obj["D"] = 2
    assert certificate.serialize_certificate(instance, obj) == _recipe(row[7])


def test_tied_raw_scales_remain_distinct_without_optimization(monkeypatch, wire):
    small, large = _FIXTURES["TIE-SMALL"], _FIXTURES["TIE-LARGE"]
    assert small[1] == large[1]
    a, b = _result(small), _result(large)
    assert (a.value.N, a.value.D) != (b.value.N, b.value.D)
    assert a.value.N * b.value.D == b.value.N * a.value.D
    instance = _instance(_GRAPHS[small[1]])
    instance_bytes = _transport(_GRAPHS[small[1]])
    _optimizer_barrier(monkeypatch)
    for row, result in ((small, a), (large, b), (small, a), (large, b)):
        assert _emit(instance, result, instance_bytes, wire) == _recipe(row[7])


@pytest.mark.parametrize("fixture_id", ("ZERO", "INTERIOR", "H2-LOSER", "BIG-ZERO"))
def test_suboptimal_local_attainment_is_sufficient(fixture_id, monkeypatch, wire):
    row = _FIXTURES[fixture_id]
    instance, result = _instance(_GRAPHS[row[1]]), _result(row)
    reference = _GLOBALS[row[1]]
    assert result.value.N * _number(reference[2]) < _number(reference[1]) * result.value.D
    _optimizer_barrier(monkeypatch)
    assert _emit(instance, result, _transport(_GRAPHS[row[1]]), wire) == _recipe(row[7])


def _observe_solve(instance, route, monkeypatch):
    candidates = []
    original_base = solver._baseline
    original_endpoint = solver._endpoint
    original_evaluate = solver._evaluate

    def baseline(*args):
        value, witness = original_base(*args)
        candidates.append(("Baseline", value, witness))
        return value, witness

    def endpoint(inst, branch, result):
        value, witness = original_endpoint(inst, branch, result)
        candidates.append((("L0", "L1", "H0", "H1")[branch], value, witness))
        return value, witness

    def evaluate(inst, witness):
        value = original_evaluate(inst, witness)
        if sys._getframe(1).f_code is solver.solve.__code__:
            candidates.append(("H2", value, witness))
        return value

    with monkeypatch.context() as local:
        local.setattr(solver, "_baseline", baseline)
        local.setattr(solver, "_endpoint", endpoint)
        local.setattr(solver, "_evaluate", evaluate)
        result, stats = solver.solve(instance, route)
    return result, stats, candidates


def test_every_registered_identity_both_routes_and_local_reconstructions(monkeypatch, wire):
    executed = []
    origins = Counter()
    h2_shapes = set()
    baseline_matches = 0
    h2_matches = 0
    baseline_retention = {
        "N-EVEN-ALL", "N-ODD-ALL", "N-H2-ONE-EDGE", "N-MATCH2",
        "N-EVEN-UPGRADE", "N-ODD-UPGRADE-ZERO",
    }
    for key, graph in _REGISTRY:
        instance, instance_bytes = _instance(graph), _transport(graph)
        own_pairs = []
        for route in _ROUTES:
            before = _snapshot(instance)
            result, stats, candidates = _observe_solve(instance, route, monkeypatch)
            assert _snapshot(instance) == before
            executed.append((key, route))
            own_pairs.append((result.value.N, result.value.D))
            reference = _GLOBALS[key]
            assert result.value.N * _number(reference[2]) == _number(reference[1]) * result.value.D
            if key.removeprefix("U15_INPUTS/") in baseline_retention:
                assert stats.attaining_candidate == "Baseline"
            with monkeypatch.context() as guard:
                _optimizer_barrier(guard)
                raw = _emit(instance, result, instance_bytes, wire)
                assert _emit(instance, result, instance_bytes, wire) == raw
                local_bytes = []
                for origin, value, witness in candidates:
                    local_result = SolveResult(value, witness)
                    candidate_bytes = _emit(instance, local_result, instance_bytes, wire)
                    local_bytes.append((origin, candidate_bytes))
                    origins[origin] += 1
                    if origin == "H2":
                        assert (value.N, value.D) == (4, 2)
                        counts = tuple(count for count in witness.y if count)
                        assert counts in ((2,), (1, 1))
                        h2_shapes.add(counts)
            for row in _FIXTURES.values():
                if row[1] != key:
                    continue
                origin = "Baseline" if row[2].startswith("Baseline-") else (
                    "H2" if row[2] == "H2" else None
                )
                if origin:
                    matches = [
                        blob for observed_origin, blob in local_bytes if observed_origin == origin
                    ]
                    assert matches == [_recipe(row[7])]
                    baseline_matches += int(origin == "Baseline")
                    h2_matches += int(origin == "H2")
        # Numerical agreement only.  Do not compare witnesses, raw scales or bytes.
        (n1, d1), (n2, d2) = own_pairs
        assert n1 * d2 == n2 * d1
    assert executed == [(key, route) for key, _ in _REGISTRY for route in _ROUTES]
    assert len(executed) == 792
    assert set(origins) == {"Baseline", "L0", "L1", "H0", "H1", "H2"}
    assert h2_shapes == {(2,), (1, 1)}
    assert baseline_matches == 22 and h2_matches == 8
    # These are execution observations, not a demanded cross-route raw stream.
    print("UNIT17_CERTIFICATE_CORPUS " + json.dumps({
        "registry_identities": len(_REGISTRY), "actual_final_solves": len(executed),
        "numerical_cross_route_comparisons": len(_REGISTRY),
        "local_candidates": sum(origins.values()), "local_origins": dict(sorted(origins.items())),
        "fixed_baseline_matches": baseline_matches, "fixed_H2_matches": h2_matches,
    }, sort_keys=True))


@pytest.mark.parametrize("route", _ROUTES)
@pytest.mark.parametrize("fixture_id", ("EMPTY", "BASE-EVEN", "L0", "L1", "H0", "H1", "H2-SPLIT"))
def test_legacy_and_measured_results_serialize_the_same(fixture_id, route, monkeypatch, wire):
    row = _FIXTURES[fixture_id]
    graph = _GRAPHS[row[1]]
    instance = _instance(graph)
    legacy, legacy_stats = solver.solve(instance, route)
    measured, measured_stats = telemetry.solve_with_telemetry(instance, route)
    assert measured == legacy
    assert measured_stats.native == legacy_stats
    snapshots = _snapshot((legacy_stats, measured_stats))
    _optimizer_barrier(monkeypatch)
    a = _emit(instance, legacy, _transport(graph), wire)
    b = _emit(instance, measured, _transport(graph), wire)
    assert a == b
    # Diagnostic objects are never certificate arguments or envelope fields.
    assert _snapshot((legacy_stats, measured_stats))[2] == snapshots[2]


@pytest.mark.parametrize("fixture_id", ("H2-ONE", "FULL", "SPARSE-GAP", "BIG-COUNTS", "BIG-LABEL"))
def test_labels_diagnostics_and_interleaved_calls_do_not_enter_bytes(fixture_id, monkeypatch, wire):
    row = _FIXTURES[fixture_id]
    graph, result = _GRAPHS[row[1]], _result(row)
    expected = _recipe(row[7])
    _optimizer_barrier(monkeypatch)
    for labels in (None, tuple("label-" + str(v) for v in range(graph["n"])),
                   tuple(-(10**4800) - v for v in range(graph["n"]))):
        changed = copy.deepcopy(graph)
        changed.pop("labels", None)
        if labels is not None:
            changed["labels"] = list(labels)
        assert _emit(_instance(changed), result, _transport(changed), wire) == expected
        other = _FIXTURES["ZERO"]
        assert _emit(_instance(_GRAPHS[other[1]]), _result(other),
                     _transport(_GRAPHS[other[1]]), wire) == _recipe(other[7])


# The independent worker never imports the consuming test or production.  The
# production worker imports the proposed module only to exercise its public API.
_FRESH_WORKER = r'''
import hashlib
import json
import sys

payload = json.loads(sys.stdin.buffer.read())
source = payload["source"]
mode = payload["mode"]
if mode == "independent":
    class BlockProduction:
        def find_spec(self, fullname, path=None, target=None):
            if fullname.split(".")[0] in ("exactfrac", "exactfrac_verify"):
                raise AssertionError("independent route attempted production import")
    sys.meta_path.insert(0, BlockProduction())
space = {"__name__": "_unit17_isolated_wire"}
exec(compile(source, "<unit17-isolated-wire>", "exec"), space)
initial_limit = sys.get_int_max_str_digits()
assert initial_limit == payload["limit"]
if mode == "independent":
    accepted = rejected = 0
    for instance_hex, certificate_hex, expected in payload["pairs"]:
        try:
            space["verify"](bytes.fromhex(instance_hex), bytes.fromhex(certificate_hex))
        except ValueError as error:
            assert type(error) is ValueError and not expected
            rejected += 1
        else:
            assert expected
            accepted += 1
    # Instance validation must precede even attempting certificate parsing.
    original_parse = space["_parse"]
    seen = []
    def traced(raw):
        seen.append(raw)
        return original_parse(raw)
    space["_parse"] = traced
    try:
        space["verify"](b"{}", b"not a certificate")
    except ValueError as error:
        assert type(error) is ValueError and seen == [b"{}"]
    else:
        raise AssertionError("invalid instance accepted")
    marker = MemoryError("injected independent resource failure")
    def fail(raw):
        raise marker
    space["_parse"] = fail
    try:
        space["verify"](b"{}", b"{}")
    except MemoryError as error:
        assert error is marker
    else:
        raise AssertionError("resource failure swallowed")
    loaded = sorted(name for name in sys.modules
                    if name.split(".")[0] in ("exactfrac", "exactfrac_verify"))
    assert not loaded
    answer = {"accepted": accepted, "rejected": rejected, "production_imports": loaded,
              "instance_before_certificate": True, "resource_exception_identity": True}
else:
    assert mode == "production"
    import exactfrac.certificate as api
    from exactfrac.instance import Instance
    from exactfrac.solve import SolveResult
    from exactfrac.witness import ExactValue, Witness
    def forbidden(*args, **kwargs):
        raise AssertionError("certificate path invoked optimization")
    for name, module in tuple(sys.modules.items()):
        if name == "exactfrac" or name.startswith("exactfrac."):
            for function in ("solve", "solve_with_telemetry", "solve_branch_standard",
                             "solve_branch_accelerated", "exact_branch_min", "minimum_cut",
                             "minimum_parity_cut", "reduce_atomic_family"):
                if hasattr(module, function):
                    setattr(module, function, forbidden)
    outputs = []
    rows = payload["fixtures"]
    for row in rows + list(reversed(rows)):
        key, instance_hex, certificate_hex = row
        ib, expected = bytes.fromhex(instance_hex), bytes.fromhex(certificate_hex)
        graph = space["parse_instance"](ib)
        obj = space["verify"](ib, expected)
        instance = Instance(graph["n"], tuple(tuple(edge) for edge in graph["edges"]),
                            tuple(graph["f"]),
                            None if "labels" not in graph else tuple(graph["labels"]))
        if obj["empty"]:
            witness = None
        else:
            counts = [0] * len(graph["edges"])
            for ref, count in obj["y"]:
                counts[ref] = count
            witness = Witness(sum(1 << v for v in obj["U"]), tuple(counts))
        result = SolveResult(ExactValue(obj["N"], obj["D"]), witness)
        for repeat in range(3):
            built = api.build_certificate(instance, result)
            assert built == obj and list(built) == list(obj)
            raw = api.serialize_certificate(instance, built)
            assert type(raw) is bytes and raw == expected
            reordered = dict(reversed(list(obj.items())))
            assert api.serialize_certificate(instance, reordered) == expected
            assert space["verify"](ib, raw) == obj
            assert sys.get_int_max_str_digits() == initial_limit
        outputs.append([key, len(raw), hashlib.sha256(raw).hexdigest()])
    assert not any(name.split(".")[0] == "exactfrac_verify" for name in sys.modules)
    answer = {"outputs": outputs, "loaded_production": sorted(
        name for name in sys.modules if name == "exactfrac" or name.startswith("exactfrac."))}
assert sys.get_int_max_str_digits() == initial_limit
answer["limit"] = initial_limit
answer["conversion_setting_unchanged"] = True
print(json.dumps(answer, sort_keys=True))
'''


def _fresh(mode, seed, limit):
    payload = {"mode": mode, "source": _INDEPENDENT_SOURCE, "limit": limit}
    if mode == "independent":
        pairs = [(_transport(_GRAPHS[row[1]]).hex(), _recipe(row[7]).hex(), True)
                 for row in _FIXTURES.values()]
        namespace = _new_wire()
        for row in _TABLES["U17_WIRE_REJECT"]:
            a, b = _wire_pair(row, namespace)
            pairs.append((a.hex(), b.hex(), False))
        for row in _TABLES["U17_WIRE_ACCEPT"]:
            a, b = _wire_pair(row, namespace)
            pairs.append((a.hex(), b.hex(), True))
        payload["pairs"] = pairs
    else:
        payload["fixtures"] = [(row[0], _transport(_GRAPHS[row[1]]).hex(), _recipe(row[7]).hex())
                               for row in _FIXTURES.values()]
    env = dict(os.environ)
    for name in ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONINSPECT"):
        env.pop(name, None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = seed
    answer = subprocess.run(
        [sys.executable, "-B", "-s", "-X", "int_max_str_digits=" + str(limit), "-c", _FRESH_WORKER],
        input=json.dumps(payload).encode(), capture_output=True,
        cwd=_ROOT, env=env, check=False, timeout=180,
    )
    assert answer.returncode == 0, answer.stderr.decode("utf-8", "replace")
    return json.loads(answer.stdout)


@pytest.mark.parametrize("seed", ("1", "73"))
@pytest.mark.parametrize("limit", (4300, 640))
def test_independent_wire_in_fresh_production_blocked_process(seed, limit):
    assert _fresh("independent", seed, limit) == {
        "accepted": 38, "rejected": 140, "production_imports": [],
        "instance_before_certificate": True, "resource_exception_identity": True,
        "limit": limit, "conversion_setting_unchanged": True,
    }


@pytest.mark.parametrize("seed", ("1", "73"))
@pytest.mark.parametrize("limit", (4300, 640))
def test_exact_large_integer_serialization_in_fresh_process(seed, limit):
    result = _fresh("production", seed, limit)
    rows = list(_FIXTURES.values())
    assert result["outputs"] == [[row[0], row[8], row[9]] for row in rows + list(reversed(rows))]
    assert result["limit"] == limit and result["conversion_setting_unchanged"] is True
    assert "exactfrac.certificate" in result["loaded_production"]
    assert all(not name.startswith("exactfrac_verify") for name in result["loaded_production"])


def test_independent_source_is_fixed_and_has_only_standard_library_imports(wire):
    assert _sha(_INDEPENDENT_SOURCE.encode()) == _INDEPENDENT_SHA
    tree = ast.parse(_INDEPENDENT_SOURCE)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    assert imports == ["json", "re"]
    assert tuple(inspect.signature(wire["verify"]).parameters) == (
        "instance_bytes", "certificate_bytes",
    )
    assert all(not key.startswith("exactfrac") for key in wire)
    assert not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                   and node.func.id in {"open", "eval", "exec", "__import__"}
                   for node in ast.walk(tree))


def test_closed_sources_and_production_import_exactness_boundary():
    for path, digest in _FROZEN_PRODUCTION.items():
        assert _sha((_ROOT / path).read_bytes()) == digest
    raw = Path(certificate.__file__).read_bytes()
    tree = ast.parse(raw)
    allowed = {
        "__future__": {"annotations"}, "instance": {"Instance"}, "solve": {"SolveResult"},
        "shore": {"shore_from_list", "shore_to_list"},
        "witness": {
            "ExactValue", "Witness", "dense_y_to_sparse", "sparse_y_to_dense", "witness_value",
        },
    }
    imported_names = {}
    forbidden_calls = {
        "eval", "exec", "compile", "__import__", "open", "input", "print", "float", "complex",
        "Fraction", "gcd", "round", "set_int_max_str_digits",
    }
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {name for name in functions if not name.startswith("_")} == {
        "build_certificate", "serialize_certificate",
    }
    for node in ast.walk(tree):
        assert not isinstance(node, (ast.Import, ast.Div))
        if isinstance(node, ast.ClassDef):
            assert node.name != "Certificate"
        if isinstance(node, ast.Constant):
            assert type(node.value) not in (float, complex)
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.startswith("exactfrac."):
                assert node.level == 0
                module = module.removeprefix("exactfrac.")
            else:
                assert node.level == (0 if module == "__future__" else 1)
            assert module in allowed
            assert {item.name for item in node.names} <= allowed[module]
            imported_names.update({item.asname or item.name: item.name for item in node.names})
        if isinstance(node, ast.Call):
            name = (node.func.id if isinstance(node.func, ast.Name)
                    else node.func.attr if isinstance(node.func, ast.Attribute) else None)
            assert name not in forbidden_calls
        if isinstance(node, ast.Attribute):
            assert node.attr not in {"__globals__", "__builtins__", "__dict__", "__class__",
                                     "__subclasses__", "__getattribute__", "__import__"}
    calls = {
        name: {node.func.id for node in ast.walk(body) if isinstance(node, ast.Call)
               and isinstance(node.func, ast.Name) and node.func.id in functions}
        for name, body in functions.items()
    }

    def reachable(start):
        seen = set()
        pending = [start]
        while pending:
            name = pending.pop()
            if name not in seen:
                seen.add(name)
                pending.extend(calls[name])
        return seen

    builder_reachable = reachable("build_certificate")
    serializer_reachable = reachable("serialize_certificate")
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if not ((isinstance(node, ast.BinOp) and isinstance(node.op, (ast.FloorDiv, ast.Mod)))
                or (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == "divmod")):
            continue
        owners = []
        cursor = node
        while cursor in parents:
            cursor = parents[cursor]
            if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                owners.append(cursor.name)
        # A private decimal helper may be module-level or nested.  Do not make
        # helper placement or use of a local generator into an unadopted API rule.
        # Complete codec dataflow/work review remains in the Phase E audit.
        assert owners and owners[0].startswith("_")
        assert owners[-1] in serializer_reachable
        assert owners[-1] not in builder_reachable


@pytest.mark.parametrize("row", [row for row in _TABLES["U17_WIRE_REJECT"]
                                 if row[5] and row[1] != "EMPTY"], ids=lambda row: row[0])
def test_builder_rejects_numerically_equal_nonempty_raw_forgeries(row, wire):
    fixture = _FIXTURES[row[1]]
    instance, original = _instance(_GRAPHS[fixture[1]]), _result(fixture)
    _, bad_bytes = _wire_pair(row, wire)
    bad = wire["_parse"](bad_bytes)
    assert bad["N"] * original.value.D == original.value.N * bad["D"]
    forged = SolveResult(ExactValue(bad["N"], bad["D"]), original.witness)
    _exact_error(ValueError, certificate.build_certificate, instance, forged)


@pytest.mark.parametrize("case_id", (
    "C-Y-EXTERNAL", "C-Y-INTERNAL", "C-AUX-REF", "C-Y-OVER-GUARD",
))
def test_builder_rejects_instance_dependent_normal_witness_faults(case_id, wire):
    row = next(row for row in _TABLES["U17_WIRE_REJECT"] if row[0] == case_id)
    fixture = _FIXTURES[row[1]]
    instance = _instance(_GRAPHS[fixture[1]])
    _, bad_bytes = _wire_pair(row, wire)
    obj = wire["_parse"](bad_bytes)
    counts = [0] * instance.m
    for ref, count in obj["y"]:
        counts[ref] = count
    # These are valid record shapes.  Their graph-dependent promises are false.
    witness = Witness(sum(1 << v for v in obj["U"]), tuple(counts))
    forged = SolveResult(ExactValue(obj["N"], obj["D"]), witness)
    _exact_error(ValueError, certificate.build_certificate, instance, forged)
