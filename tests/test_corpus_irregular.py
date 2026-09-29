"""Unit 21B corpus consumer for the jointly frozen two-test RED candidate.

Consumes DESIGN D21B-I3--I6/I15, inherited D20-C2/C6/C7, and the
committed Phase C byte bank. No solver, producer prototype, pilot, main
campaign, private helper or private Mac evidence is used by this file.
The corpus and runner tests are one candidate and must never be applied separately.
"""

from __future__ import annotations

import ast
import builtins
import collections
import csv
import functools
import hashlib
import inspect
import io
import itertools
import json
import math
import os
import random
import re
import subprocess
import sys
import types
import typing
from pathlib import Path, PurePosixPath

import pytest

import exactfrac.corpus_irregular as corpus

_ROOT = Path(__file__).resolve().parents[1]
_MODULE = "exactfrac.corpus_irregular"
_HEADER = b"## Unit 21B \xe2\x80\x94 Phase C independent irregular oracle, R1\n"
_SUITE = "unit21-v2"
_TAG = "exactfrac-u21b-irregular/1"
_SEEDS = tuple(f"p{i:02d}" for i in range(1, 6)) + tuple(
    f"s{i:02d}" for i in range(1, 21)
)
_REGISTRY = tuple(sorted(
    f"irregular-n{n:02d}-t{tau:03d}-b{b:05d}-f{mode}-{seed}"
    for n, tau, b, mode, seed in itertools.product(
        (6, 8, 12, 16), (64, 128), (1, 8, 64), ("alternating", "random"), _SEEDS,
    )
))
_ID_PATTERN = re.compile(
    r"irregular-n(06|08|12|16)-t(064|128)-b(00001|00008|00064)"
    r"-f(alternating|random)-([ps][0-9]{2})\Z"
)
_FENCE = re.compile(
    rb"^<!-- U21B-FIXTURE ([^ \n]+) (raw|base64) ([0-9]+) ([0-9a-f]{64}) -->\n"
    rb"```[^\n]*\n(.*?)^```\n", re.MULTILINE | re.DOTALL,
)
# Fixed fixture-local identities; NOT a whole-catalogue or aggregate pin.
_FIXTURE_PINS = {
    "CENSUS.json": (1686, "a2be5805d6a7bd15aa5144d4eaa7e1b2a0bac931486025308d9d3bcfc8fa5a17"),
    "DIGEST_INJECTION_CASES.json": (
        9393, "da300b0aa84739652061ccc0a6f3931ff226065aed854c728e06c7299bf64d8f",
    ),
    "ENDPOINT_BOUNDARY_CASES.json": (
        2384, "7a079e89d4c30e3578445310420a85e1cba1b5f28cf9846ded25e857e1d978d6",
    ),
    "EXHAUSTIVE_VECTORS.csv": (
        15062, "aa6dbdfc1a21e7958961993bb51683b62b7df89e54c9b3066d3544762eebb1ec",
    ),
    "INVENTORY.tsv": (
        370655, "1ac23b1a169a6edfb46ec502e2420a71a3d3932007e5d9b70316e948fb430822",
    ),
    "OWN_MANIFEST": (
        271414, "8f34e232966fc5142cc281655f28dfe858ccd610aecb0ecdb5d2b9f61d6510a0",
    ),
    "REFERENCE_ROWS.jsonl": (
        2893425, "f1a2afa6d5adf6185056cccf377c1125a6c12b9a2256538afd5550a4f4991510",
    ),
}


def _identity(raw):
    return len(raw), hashlib.sha256(raw).hexdigest()


def _require(condition, guard):
    if not condition:
        raise AssertionError(guard)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate-decoded-json-key")
        result[key] = value
    return result


def _no_noninteger(token):
    raise AssertionError("noninteger-json-token: " + token)


def _decimal_token(token):
    _require(re.fullmatch(r"(?:0|[1-9][0-9]*)", token) is not None, "integer-token")
    result = 0
    for offset in range(0, len(token), 9):
        part = token[offset:offset + 9]
        result = result * 10 ** len(part) + int(part)
    return result


def _json(raw):
    return json.loads(
        raw, object_pairs_hook=_unique_object, parse_int=_decimal_token,
        parse_float=_no_noninteger, parse_constant=_no_noninteger,
    )


def _read_bank(data):
    """Read only registered corpus fixtures, never execute a catalogue fence."""
    _require(data.count(_HEADER) == 1, "unique-phase-c-appendix")
    appendix = data.split(_HEADER, 1)[1].split(b"\n## ", 1)[0]
    required = set(_FIXTURE_PINS) | {"inputs/" + rid + ".json" for rid in _REGISTRY}
    bank = {}
    for match in _FENCE.finditer(appendix):
        name_raw, encoding, length, digest, raw = match.groups()
        name = name_raw.decode("ascii")
        if name not in required:
            continue
        _require(name not in bank, "duplicate-corpus-fixture: " + name)
        _require(encoding == b"raw", "corpus-fixture-encoding: " + name)
        _require(_identity(raw) == (int(length), digest.decode()), "fence-identity: " + name)
        if name in _FIXTURE_PINS:
            _require(_identity(raw) == _FIXTURE_PINS[name], "fixed-fixture-identity: " + name)
        bank[name] = raw
    _require(set(bank) == required, "complete-corpus-fixture-membership")
    return bank


@functools.cache
def _bank():
    return _read_bank((_ROOT / "docs/ORACLE_CATALOG.md").read_bytes())


@functools.cache
def _inventory():
    rows = tuple(csv.DictReader(io.StringIO(_bank()["INVENTORY.tsv"].decode()), delimiter="\t"))
    _require(tuple(row["recipe"] for row in rows) == _REGISTRY, "fixed-inventory-identity")
    return rows


@functools.cache
def _references():
    rows = tuple(_json(line) for line in _bank()["REFERENCE_ROWS.jsonl"].splitlines())
    _require(tuple(row["recipe"] for row in rows) == _REGISTRY, "fixed-reference-order")
    return {row["recipe"]: row for row in rows}


def _input(rid):
    return _bank()["inputs/" + rid + ".json"]


def _parts(rid):
    match = _ID_PATTERN.fullmatch(rid)
    _require(match is not None, "recipe-grammar")
    n, tau, b, mode, seed = match.groups()
    _require(seed in _SEEDS, "recipe-domain")
    return int(n), int(tau), int(b), mode, seed


def _message(*lines):
    return (_TAG + "\n" + "\n".join(str(line) for line in lines) + "\n").encode("ascii")


def _support_fingerprint(n, edges):
    raw = ("exactfrac-unit21b-support/1\n" + str(n) + "\n"
           + "".join(f"{u},{v}\n" for u, v, _q in edges)).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def _check_payload(raw, rid):
    """Definition-level byte/recipe checks, independent of producer internals."""
    _require(type(raw) is bytes, "exact-payload-bytes")
    obj = _json(raw)
    _require(type(obj) is dict, "instance-object")
    _require(tuple(obj) == ("format", "n", "edges", "f"), "instance-key-order")
    n, tau, b, mode, seed = _parts(rid)
    _require(obj["format"] == "exactfrac-instance/1" and type(obj["n"]) is int,
             "instance-format-and-n-type")
    _require(obj["n"] == n and type(obj["edges"]) is list and type(obj["f"]) is list,
             "instance-shape")
    edges, capacities = obj["edges"], obj["f"]
    _require(all(type(e) is list and len(e) == 3 for e in edges), "edge-record-shape")
    _require(all(type(x) is int for e in edges for x in e), "edge-exact-integers")
    _require(len(capacities) == n and all(type(x) is int for x in capacities),
             "capacity-exact-integers")
    pairs = [(u, v) for u, v, _q in edges]
    _require(pairs == sorted(set(pairs)), "canonical-edge-reference")
    _require(all(0 <= u < v < n for u, v in pairs), "edge-endpoints")
    spine = {(u, u + 1) for u in range(n - 1)} | {(0, n - 1)}
    _require(spine <= set(pairs), "unconditional-spine")
    for u, v in itertools.combinations(range(n), 2):
        included = (u, v) in spine or hashlib.sha256(
            _message("support", seed, n, u, v),
        ).digest()[0] < tau
        _require(((u, v) in pairs) == included, "support-formula")
    degrees = [0] * n
    for u, v, q in edges:
        digest = hashlib.sha256(_message("multiplicity", seed, n, tau, mode, u, v)).digest()
        expected_q = 1 + int.from_bytes(digest, "big", signed=False) % (1 << b)
        _require(q == expected_q and 1 <= q <= 1 << b, "positive-q-formula")
        degrees[u] += q
        degrees[v] += q
    for v, f in enumerate(capacities):
        if mode == "alternating":
            expected_f = 1 if v % 2 == 0 else degrees[v]
        else:
            digest = hashlib.sha256(_message("capacity", seed, n, tau, "random", v)).digest()
            expected_f = 1 + int.from_bytes(digest, "big", signed=False) % degrees[v]
        _require(1 <= f <= degrees[v] and f == expected_f, "active-capacity-formula")
    # These test-only JSON numbers have at most 21 digits; no interpreter change.
    canonical = (json.dumps(obj, ensure_ascii=True, separators=(",", ":")) + "\n").encode()
    _require(raw == canonical, "canonical-instance-wire")
    ref = _references()[rid]
    _require(edges == ref["edges"] and capacities == ref["f"] and degrees == ref["d_q"],
             "registered-construction-vectors")
    _require(len(edges) == ref["m"] and sum(e[2] for e in edges) == ref["Q"],
             "registered-size-and-multiplicity")
    _require(max(e[2].bit_length() for e in edges) == ref["max_q_bits"], "actual-q-bits")
    _require(_support_fingerprint(n, edges) == ref["support_sha256"], "support-fingerprint")
    _require(_identity(raw) == (ref["input_bytes"], ref["input_sha256"]), "input-identity")
    _require(raw == _input(rid), "independent-payload-bytes: " + rid)
    return obj


def _check_registry(actual):
    _require(type(actual) is tuple, "registry-exact-tuple")
    _require(all(type(rid) is str for rid in actual), "registry-exact-str-leaves")
    _require(actual == tuple(row["recipe"] for row in _inventory()), "full-ordered-registry")


def _check_build(actual):
    _require(type(actual) is tuple, "build-exact-tuple")
    _require(all(type(row) is tuple and len(row) == 2 for row in actual), "build-record-types")
    _require(all(type(path) is str and type(raw) is bytes for path, raw in actual),
             "build-immutable-leaves")
    _require(len(actual) == 1201, "own-build-count")
    _require(actual[0] == ("MANIFEST", _bank()["OWN_MANIFEST"]), "independent-own-manifest")
    _require(tuple(path for path, _ in actual[1:]) == tuple(row["path"] for row in _inventory()),
             "own-path-order")
    for (path, raw), expected in zip(actual[1:], _inventory(), strict=True):
        _require(path == expected["path"], "owned-path-equation")
        _require(raw == _input(expected["recipe"]), "own-payload-bytes")
        _require(_identity(raw) == (int(expected["bytes"]), expected["sha256"]),
                 "owned-projection-binding")


def _settings():
    return (
        sys.get_int_max_str_digits(), sys.getrecursionlimit(), sys.gettrace(), sys.getprofile(),
        tuple(sys.path), random.getstate(), dict(os.environ), os.getcwd(),
    )


def _patch_digest_functions(monkeypatch, sha256, new):
    """Instrument stdlib SHA-256, including direct imported aliases, not private APIs."""
    original_sha256, original_new = hashlib.sha256, hashlib.new
    for name, value in tuple(vars(corpus).items()):
        if value is original_sha256:
            monkeypatch.setattr(corpus, name, sha256)
        elif value is original_new:
            monkeypatch.setattr(corpus, name, new)
    monkeypatch.setattr(hashlib, "sha256", sha256)
    monkeypatch.setattr(hashlib, "new", new)


def test_public_surface_signatures_annotations_and_local_origin():
    assert corpus.__all__ == ("build_corpus", "generate_instance", "recipe_ids")
    assert type(corpus.__all__) is tuple
    assert {name for name, value in vars(corpus).items()
            if not name.startswith("_") and callable(value)} == set(corpus.__all__)
    expected_hints = {
        "recipe_ids": {"return": tuple[str, ...]},
        "generate_instance": {"recipe_id": str, "return": bytes},
        "build_corpus": {"return": tuple[tuple[str, bytes], ...]},
    }
    for name in corpus.__all__:
        fn = getattr(corpus, name)
        assert type(fn) is types.FunctionType
        assert fn.__module__ == _MODULE
        params = tuple(inspect.signature(fn).parameters.values())
        assert len(params) == (1 if name == "generate_instance" else 0)
        if params:
            assert params[0].name == "recipe_id"
            assert params[0].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
            assert params[0].default is inspect.Parameter.empty
        assert typing.get_type_hints(fn) == expected_hints[name]
    for name, value in vars(corpus).items():
        if not name.startswith("_"):
            assert not isinstance(value, (dict, list, set, bytearray, memoryview))
    assert Path(corpus.__file__).resolve() == _ROOT / "exactfrac/corpus_irregular.py"


def test_full_registry_matches_independent_inventory_and_measured_payload_diversity():
    actual = corpus.recipe_ids()
    _check_registry(actual)
    assert len(actual) == len(set(actual)) == 1200
    assert len({rid.rsplit("-", 1)[0] for rid in actual}) == 48
    domains = collections.Counter(rid.rsplit("-", 1)[1][0] for rid in actual)
    assert domains == {"p": 240, "s": 960}
    assert all(rid.isascii() and _parts(rid) for rid in actual)
    assert all(left.encode() < right.encode() for left, right in itertools.pairwise(actual))
    payloads = [corpus.generate_instance(rid) for rid in actual]
    observed_distinct = len(set(payloads))
    assert observed_distinct == _json(_bank()["CENSUS.json"])["mathematics"]["distinct_payloads"]
    assert len(actual) == 1200  # Identity retention is separate from observed distinct bytes.
    for rid in actual:
        if rid.endswith("p01"):
            main_rid = rid[:-3] + "s01"
            assert main_rid in actual and rid != main_rid
            assert corpus.generate_instance(rid) == _input(rid)
            assert corpus.generate_instance(main_rid) == _input(main_rid)


@pytest.mark.parametrize("rid", _REGISTRY)
def test_each_exact_payload_recipe_and_registered_input_identity(rid):
    _check_payload(corpus.generate_instance(rid), rid)
    assert corpus.generate_instance(recipe_id=rid) == _input(rid)


def test_all_matched_magnitude_threshold_and_mode_support_relationships():
    observed = {}
    fingerprints = collections.defaultdict(set)
    for rid in _REGISTRY:
        n, tau, b, mode, seed = _parts(rid)
        obj = _json(corpus.generate_instance(rid))
        observed[n, tau, b, mode, seed] = frozenset((e[0], e[1]) for e in obj["edges"])
        fingerprints[n, tau, mode, seed].add(_support_fingerprint(n, obj["edges"]))
    assert len(fingerprints) == 400
    assert all(len(group) == 1 for group in fingerprints.values())
    for n, tau, mode, seed in itertools.product((6, 8, 12, 16), (64, 128),
                                                ("alternating", "random"), _SEEDS):
        assert (observed[n, tau, 1, mode, seed] == observed[n, tau, 8, mode, seed]
                == observed[n, tau, 64, mode, seed])
    for n, b, mode, seed in itertools.product((6, 8, 12, 16), (1, 8, 64),
                                             ("alternating", "random"), _SEEDS):
        assert observed[n, 64, b, mode, seed] <= observed[n, 128, b, mode, seed]
    for n, tau, b, seed in itertools.product((6, 8, 12, 16), (64, 128), (1, 8, 64), _SEEDS):
        assert observed[n, tau, b, "alternating", seed] == observed[n, tau, b, "random", seed]


class _HostileStr(str):
    def __str__(self):
        raise AssertionError("forbidden-str-coercion")

    def __eq__(self, other):
        raise AssertionError("subclass-equality-before-type-rejection")

    def __hash__(self):
        raise AssertionError("subclass-hash-before-type-rejection")


class _HostileObject:
    def __str__(self):
        raise AssertionError("forbidden-object-coercion")

    def __fspath__(self):
        raise AssertionError("forbidden-path-coercion")

    def __iter__(self):
        raise AssertionError("forbidden-object-iteration")

    def __eq__(self, other):
        raise AssertionError("object-equality-before-type-rejection")

    def __hash__(self):
        raise AssertionError("object-hash-before-type-rejection")


_BAD_TYPES = (
    ("none", None), ("false", False), ("true", True), ("int", 1), ("float", 1.0),
    ("bytes", _REGISTRY[0].encode()), ("bytearray", bytearray(_REGISTRY[0].encode())),
    ("memoryview", memoryview(_REGISTRY[0].encode())), ("list", [_REGISTRY[0]]),
    ("tuple", (_REGISTRY[0],)), ("dict", {"recipe": _REGISTRY[0]}),
    ("set", {_REGISTRY[0]}), ("path", Path(_REGISTRY[0])),
    ("pure-path", PurePosixPath(_REGISTRY[0])), ("str-subclass", _HostileStr(_REGISTRY[0])),
    ("hostile-object", _HostileObject()),
)
_BASE_ID = "irregular-n06-t064-b00001-falternating-s01"
_BAD_SPELLINGS = tuple(dict.fromkeys((
    "", " " + _BASE_ID, _BASE_ID + " ", _BASE_ID + "\n", _BASE_ID + "\r\n",
    "\t" + _BASE_ID, _BASE_ID.upper(), _BASE_ID.replace("n06", "n6"),
    _BASE_ID.replace("n06", "n006"), _BASE_ID.replace("n06", "n+6"),
    _BASE_ID.replace("n06", "n-6"), _BASE_ID.replace("n06", "n04"),
    _BASE_ID.replace("n06", "n18"), _BASE_ID.replace("t064", "t64"),
    _BASE_ID.replace("t064", "t065"), _BASE_ID.replace("b00001", "b1"),
    _BASE_ID.replace("b00001", "b00002"), _BASE_ID.replace("b00001", "b16384"),
    _BASE_ID.replace("falternating", "fAlternating"), _BASE_ID.replace("falternating", "funit"),
    _BASE_ID.replace("s01", "s1"), _BASE_ID.replace("s01", "s001"),
    _BASE_ID.replace("s01", "s00"), _BASE_ID.replace("s01", "s21"),
    _BASE_ID.replace("s01", "p00"), _BASE_ID.replace("s01", "p06"),
    _BASE_ID.replace("s01", "p20"), _BASE_ID.replace("s01", "p001"),
    _BASE_ID.replace("s01", "1"), _BASE_ID.replace("s01", "P01"),
    _BASE_ID.replace("s01", "s\uff10\uff11"), _BASE_ID.replace("n06", "n\u0660\u0666"),
    _BASE_ID + "\x00", _BASE_ID + ".json", "unit21-v2/" + _BASE_ID,
    "../" + _BASE_ID, "/" + _BASE_ID, "./" + _BASE_ID, _BASE_ID + "/..",
    _BASE_ID.replace("-", "_"), _BASE_ID.replace("-s01", "\\s01"),
    _BASE_ID.replace("-s01", "%2fs01"), "edge-q01-f01-01",
)))


@pytest.mark.parametrize("_label,bad", _BAD_TYPES, ids=[item[0] for item in _BAD_TYPES])
def test_reject_exact_type_before_hash_comparison_or_coercion(monkeypatch, _label, bad):
    sentinel = AssertionError("digest-before-rejection")

    def forbidden(*args, **kwargs):
        raise sentinel

    before = _settings()
    with monkeypatch.context() as patch:
        _patch_digest_functions(patch, forbidden, forbidden)
        with pytest.raises(ValueError) as caught:
            corpus.generate_instance(bad)
        assert type(caught.value) is ValueError
    assert _settings() == before


@pytest.mark.parametrize("bad", _BAD_SPELLINGS)
def test_reject_unregistered_spelling_without_data_access(monkeypatch, bad):
    assert bad not in _REGISTRY

    def forbidden(*args, **kwargs):
        raise AssertionError("data-access-before-recipe-rejection")

    before = _settings()
    with monkeypatch.context() as patch:
        _patch_digest_functions(patch, forbidden, forbidden)
        patch.setattr(builtins, "open", forbidden)
        patch.setattr(io, "open", forbidden)
        with pytest.raises(ValueError) as caught:
            corpus.generate_instance(bad)
        assert type(caught.value) is ValueError
    assert _settings() == before


def test_complete_build_product_and_repeat_state_conservation():
    before = _settings()
    first = corpus.build_corpus()
    _check_build(first)
    frozen_values = tuple((path, raw) for path, raw in first)
    first_ids = corpus.recipe_ids()
    for rid in reversed(_REGISTRY):
        assert corpus.generate_instance(rid) == _input(rid)
    with pytest.raises(ValueError) as caught:
        corpus.generate_instance(_BASE_ID + " ")
    assert type(caught.value) is ValueError
    second = corpus.build_corpus()
    _check_build(second)
    assert first == frozen_values == second
    assert first_ids == corpus.recipe_ids() == _REGISTRY
    assert _settings() == before


def test_own_manifest_schema_canonical_bytes_and_independent_entry_values():
    manifest = corpus.build_corpus()[0][1]
    assert manifest == _bank()["OWN_MANIFEST"]
    obj = _json(manifest)
    assert tuple(obj) == ("format", "entries")
    assert obj["format"] == "exactfrac-corpus-manifest/1"
    assert type(obj["entries"]) is list and len(obj["entries"]) == 1200
    assert [row["path"] for row in obj["entries"]] == [row["path"] for row in _inventory()]
    for entry, row in zip(obj["entries"], _inventory(), strict=True):
        assert tuple(entry) == ("suite", "recipe", "path", "bytes", "sha256")
        assert entry == {
            "suite": _SUITE, "recipe": row["recipe"], "path": row["path"],
            "bytes": int(row["bytes"]), "sha256": row["sha256"],
        }
        assert type(entry["bytes"]) is int and entry["bytes"] > 0
        assert all(type(entry[k]) is str for k in ("suite", "recipe", "path", "sha256"))
        assert entry["path"] == _SUITE + "/" + entry["recipe"] + ".json"
        assert re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])
    assert manifest == (json.dumps(obj, separators=(",", ":")) + "\n").encode("ascii")


def _check_digest_observation(actual, case, observed, hits):
    """Check actual output/message semantics before the final fixed-byte pins."""
    _require(type(actual) is bytes, "exact-payload-bytes")
    obj = _json(actual)
    _require(type(obj) is dict and tuple(obj) == ("format", "n", "edges", "f"),
             "digest-instance-fields")
    n, tau, b, mode, seed = (case[name] for name in ("n", "tau", "b", "capacity_mode", "seed"))
    _require(type(obj["n"]) is int and obj["n"] == n, "digest-instance-n")
    edges, capacities = obj["edges"], obj["f"]
    _require(type(edges) is list and all(type(row) is list and len(row) == 3 for row in edges),
             "edge-record-shape")
    _require(all(type(value) is int for row in edges for value in row), "edge-exact-integers")
    _require(type(capacities) is list and len(capacities) == n
             and all(type(value) is int for value in capacities), "capacity-exact-integers")
    pairs = [(u, v) for u, v, _q in edges]
    _require(pairs == sorted(set(pairs)), "canonical-edge-reference")
    _require(all(0 <= u < v < n for u, v in pairs), "edge-endpoints")
    spine = {(u, u + 1) for u in range(n - 1)} | {(0, n - 1)}
    _require(spine <= set(pairs), "unconditional-spine")
    _require(not any(_message("support", seed, n, u, v) in observed for u, v in spine),
             "unconditional-spine")
    overrides = {key.encode("ascii"): bytes.fromhex(value) for key,
        value in case["override"].items()}
    def digest(message):
        return overrides[message] if message in overrides else hashlib.sha256(message).digest()
    def messages(kind):
        # Stage labels are observed message bytes, never a presumed helper name.
        return {raw for raw in observed if len(raw.split(b"\n")) > 1
                and raw.split(b"\n")[1] == kind.encode("ascii")}
    support_messages = {_message("support", seed, n, u, v)
                        for u, v in itertools.combinations(range(n), 2) if (u, v) not in spine}
    _require(messages("support") == support_messages, "domain-message-bytes")
    for u, v in itertools.combinations(range(n), 2):
        include = (u, v) in spine or digest(_message("support", seed, n, u, v))[0] < tau
        _require(((u, v) in pairs) == include, "strict-support-threshold")
    multiplicity_messages = {_message("multiplicity", seed, n, tau, mode, u, v) for u, v in pairs}
    _require(messages("multiplicity") == multiplicity_messages, "multiplicity-matched-digest")
    degrees = [0] * n
    for u, v, q in edges:
        expected = 1 + int.from_bytes(digest(_message("multiplicity", seed, n, tau, mode, u, v)),
                                      "big", signed=False) % (1 << b)
        _require(1 <= q <= 1 << b, "positive-q-formula")
        if case["id"].startswith("q-upper-") and (u, v) == pairs[0]:
            _require(q == 1 << b, "q-upper-boundary")
        _require(q == expected, "multiplicity-digest-value")
        degrees[u] += q
        degrees[v] += q
    capacity_messages = {_message("capacity", seed, n, tau, "random", vertex)
                         for vertex in range(n)} if mode == "random" else set()
    _require(messages("capacity") == capacity_messages, "capacity-message-bytes")
    for vertex, f in enumerate(capacities):
        if mode == "alternating":
            expected = 1 if vertex % 2 == 0 else degrees[vertex]
            guard = "alternating-capacity"
        else:
            expected = 1 + int.from_bytes(digest(_message("capacity", seed, n, tau, "random",
                vertex)),
                                          "big", signed=False) % degrees[vertex]
            guard = "random-capacity-modulus"
        _require(f == expected and 1 <= f <= degrees[vertex], guard)
    if case["id"].startswith("q-upper-"):
        _require(max(row[2].bit_length() for row in edges) == b + 1, "observed-max-q-bits")
    _require(set(observed) == support_messages | multiplicity_messages | capacity_messages,
             "domain-message-bytes")
    _require(len(overrides) == case["expected_override_calls"] and set(hits) == set(overrides),
             "registered-override-actually-consumed")
    _require(actual == case["payload_ascii"].encode("ascii"), "registered-digest-payload-bytes")
    _require(_identity(actual) == (case["payload_bytes"], case["payload_sha256"]),
             "registered-digest-payload-identity")


def _exercise_digest_case(monkeypatch, case):
    saved_sha256, saved_new = hashlib.sha256, hashlib.new
    overrides = {key.encode("ascii"): bytes.fromhex(value)
                 for key, value in case["override"].items()}
    observed = []
    hits = []

    class Digest:
        digest_size = 32
        block_size = 64
        name = "sha256"

        def __init__(self, data=b"", **kwargs):
            self.buffer = bytearray(data)

        def update(self, data):
            self.buffer.extend(data)

        def digest(self):
            raw = bytes(self.buffer)
            observed.append(raw)
            if raw in overrides:
                hits.append(raw)
                return overrides[raw]
            return saved_sha256(raw).digest()

        def hexdigest(self):
            return self.digest().hex()

        def copy(self):
            return Digest(bytes(self.buffer))

    def new(name, data=b"", **kwargs):
        if name.lower().replace("-", "") == "sha256":
            return Digest(data, **kwargs)
        return saved_new(name, data, **kwargs)

    rid = (f"irregular-n{case['n']:02d}-t{case['tau']:03d}-b{case['b']:05d}"
           f"-f{case['capacity_mode']}-{case['seed']}")
    before = _settings()
    with monkeypatch.context() as patch:
        _patch_digest_functions(patch, Digest, new)
        actual = corpus.generate_instance(rid)
    assert _settings() == before
    _check_digest_observation(actual, case, observed, hits)


def test_isolated_digest_overrides_consume_registered_boundary_fixtures(monkeypatch):
    cases = _json(_bank()["DIGEST_INJECTION_CASES.json"])
    assert len(cases) == 14
    for case in cases:
        _exercise_digest_case(monkeypatch, case)

def test_build_retains_all_identities_under_synthetic_digest_collisions(monkeypatch):
    """Force recipe-domain digest collisions, without prescribing private composition."""
    saved_sha256, saved_new = hashlib.sha256, hashlib.new
    recipe_hits = []

    class CollidingDigest:
        digest_size = 32
        block_size = 64
        name = "sha256"

        def __init__(self, data=b"", **kwargs):
            self.buffer = bytearray(data)

        def update(self, data):
            self.buffer.extend(data)

        def digest(self):
            raw = bytes(self.buffer)
            if raw.startswith((_TAG + "\n").encode("ascii")):
                recipe_hits.append(raw)
                return bytes(32)
            # MANIFEST identities must hash the actual payload, not the override.
            return saved_sha256(raw).digest()

        def hexdigest(self):
            return self.digest().hex()

        def copy(self):
            return CollidingDigest(bytes(self.buffer))

    def new(name, data=b"", **kwargs):
        if name.lower().replace("-", "") == "sha256":
            return CollidingDigest(data, **kwargs)
        return saved_new(name, data, **kwargs)

    # Zero support bytes include every pair. Zero multiplicity/capacity integers
    # give q=1 and random f=1. Thus many declared identities have identical bytes.
    expected_records = []
    expected_entries = []
    for rid in _REGISTRY:
        n, _tau, _b, mode, _seed = _parts(rid)
        obj = {
            "format": "exactfrac-instance/1", "n": n,
            "edges": [[u, v, 1] for u, v in itertools.combinations(range(n), 2)],
            "f": [1 if mode == "random" or v % 2 == 0 else n - 1 for v in range(n)],
        }
        raw = (json.dumps(obj, separators=(",", ":")) + "\n").encode("ascii")
        path = _SUITE + "/" + rid + ".json"
        expected_records.append((path, raw))
        expected_entries.append({"suite": _SUITE, "recipe": rid, "path": path,
                                 "bytes": len(raw), "sha256": saved_sha256(raw).hexdigest()})
    manifest = (json.dumps({"format": "exactfrac-corpus-manifest/1", "entries": expected_entries},
                           separators=(",", ":")) + "\n").encode("ascii")
    before = _settings()
    with monkeypatch.context() as patch:
        _patch_digest_functions(patch, CollidingDigest, new)
        actual = corpus.build_corpus()
    assert recipe_hits and _settings() == before
    assert type(actual) is tuple and len(actual) == 1201
    assert all(type(item) is tuple and len(item) == 2 for item in actual)
    assert all(type(path) is str and type(raw) is bytes for path, raw in actual)
    assert actual == (("MANIFEST", manifest), *expected_records)
    assert len({raw for _, raw in actual[1:]}) < len(actual) - 1


@pytest.mark.parametrize("failure_type", (OSError, MemoryError, RecursionError, KeyboardInterrupt))
@pytest.mark.parametrize("operation", ("generate_instance", "build_corpus"))
def test_native_digest_exceptions_propagate_unchanged_and_conserve_settings(
    monkeypatch, failure_type, operation,
):
    sentinel = failure_type("unit21b-test-native-sentinel")
    calls = []

    def fail(*args, **kwargs):
        calls.append(True)
        raise sentinel

    before = _settings()
    with monkeypatch.context() as patch:
        _patch_digest_functions(patch, fail, fail)
        with pytest.raises(failure_type) as caught:
            if operation == "generate_instance":
                corpus.generate_instance(_BASE_ID)
            else:
                corpus.build_corpus()
        assert caught.value is sentinel
    assert calls
    assert _settings() == before
    assert corpus.generate_instance(_BASE_ID) == _input(_BASE_ID)


def test_generator_source_has_only_stdlib_imports_and_no_executable_entrypoint():
    tree = ast.parse(Path(corpus.__file__).read_bytes(), filename=corpus.__file__)
    forbidden_modules = {"decimal", "fractions", "random", "secrets"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0 and node.module is not None
            names = [node.module.split(".")[0]]
        else:
            names = []
        assert all(
            name in sys.stdlib_module_names and name not in forbidden_modules for name in names)
        assert not isinstance(node, ast.Div), "no-float-division-in-generator"
        if isinstance(node, ast.Constant):
            assert not isinstance(node.value, float), "no-float-construction"
            assert node.value != "__main__", "no-executable-module-entry"
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in {"eval", "exec", "__import__", "hash"}
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in {"import_module", "set_int_max_str_digits"}


# The child executes the real module by normal import; import-loader reads are
# not producer I/O. All declared stdlib imports are warmed BEFORE observation.
# A source-frame-sensitive audit hook then rejects I/O originating in the source.
_FRESH_PROGRAM = r'''
import ast
import builtins
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import random
import socket
import subprocess
import sys
import time

root = Path(sys.argv[1]).resolve()
expected = json.loads(sys.stdin.buffer.read())
source = root / "exactfrac/corpus_irregular.py"
text = source.read_bytes()
sys.path.insert(0, str(root))
for node in ast.walk(ast.parse(text)):
    if isinstance(node, ast.Import):
        for alias in node.names:
            assert alias.name.split(".")[0] in sys.stdlib_module_names
            importlib.import_module(alias.name)
    elif isinstance(node, ast.ImportFrom):
        assert node.level == 0 and node.module.split(".")[0] in sys.stdlib_module_names
        importlib.import_module(node.module)
assert "exactfrac.corpus_irregular" not in sys.modules
source_name = str(source)

def from_candidate():
    frame = sys._getframe(1)
    while frame:
        if frame.f_code.co_filename == source_name:
            return True
        frame = frame.f_back
    return False

def forbidden_event(event, args):
    dangerous = (event == "open" or event.startswith(("socket.", "subprocess.", "os.")))
    if dangerous and from_candidate():
        raise AssertionError("producer-audit-event:" + event)

sys.addaudithook(forbidden_event)
originals = []

def guard(owner, name):
    original = getattr(owner, name)
    def checked(*args, **kwargs):
        if from_candidate():
            raise AssertionError("producer-forbidden-access:" + name)
        return original(*args, **kwargs)
    originals.append((owner, name, original))
    setattr(owner, name, checked)

for owner, names in (
    (builtins, ("open", "hash")), (io, ("open",)),
    (os, ("getenv", "getcwd", "getcwdb", "stat", "lstat", "access", "readlink", "urandom")),
    (time, ("time", "time_ns", "monotonic", "monotonic_ns", "perf_counter", "perf_counter_ns",
            "process_time", "process_time_ns", "thread_time", "thread_time_ns", "sleep")),
    (random, ("seed", "getstate", "setstate", "random", "randrange", "randint", "getrandbits",
              "choice", "choices", "shuffle", "sample")),
    (socket, ("socket", "create_connection", "getaddrinfo")),
    (subprocess, ("Popen", "run", "call", "check_call", "check_output")),
    (sys, ("set_int_max_str_digits", "setrecursionlimit", "settrace", "setprofile")),
):
    for name in names:
        guard(owner, name)
environ_type = type(os.environ)
for name in ("__getitem__", "__setitem__", "__delitem__", "__iter__", "__len__"):
    guard(environ_type, name)

original_dumps = json.dumps

def guarded_dumps(obj, *args, **kwargs):
    if from_candidate():
        pending = [obj]
        while pending:
            value = pending.pop()
            if type(value) is int:
                assert abs(value) < 1_000_000_000, "producer-unbounded-json-integer"
            elif type(value) in (list, tuple):
                pending.extend(value)
            elif type(value) is dict:
                pending.extend(value.values())
    return original_dumps(obj, *args, **kwargs)

json.dumps = guarded_dumps

def snapshot():
    return (sys.get_int_max_str_digits(), sys.getrecursionlimit(), sys.gettrace(), sys.getprofile(),
            tuple(sys.path), random.getstate(), dict(os.environ), os.getcwd())

before = snapshot()
module = importlib.import_module("exactfrac.corpus_irregular")
assert Path(module.__file__).resolve() == source
assert snapshot() == before
ids = tuple(item[0] for item in expected["payloads"])
assert type(module.recipe_ids()) is tuple and module.recipe_ids() == ids
for rid, length, digest in expected["payloads"]:
    raw = module.generate_instance(rid)
    assert type(raw) is bytes and (len(raw), hashlib.sha256(raw).hexdigest()) == (length, digest)
for bad in (None, False, True, 1, b"bad", " " + ids[0], ids[0] + "\x00"):
    try:
        module.generate_instance(bad)
    except ValueError as error:
        assert type(error) is ValueError
    else:
        raise AssertionError("missing-exact-ValueError")
for _ in range(2):
    records = module.build_corpus()
    assert type(records) is tuple and len(records) == 1201
    assert all(type(row) is tuple and len(row) == 2 for row in records)
    assert records[0][0] == "MANIFEST" and type(records[0][1]) is bytes
    assert [len(records[0][1]), hashlib.sha256(records[0][1]).hexdigest()] == expected["manifest"]
    for (path, raw), (rid, length, digest) in zip(records[1:], expected["payloads"], strict=True):
        assert type(path) is str and path == "unit21-v2/" + rid + ".json"
        assert type(raw) is bytes and (len(raw), hashlib.sha256(raw).hexdigest()) == (length,
            digest)
assert snapshot() == before
native_scenarios = 0
for failure_type in (OSError, MemoryError, RecursionError, KeyboardInterrupt):
    for operation in ("generate_instance", "build_corpus"):
        sentinel = failure_type("unit21b-fresh-native-sentinel")
        digest_calls = []
        def fail(*args, **kwargs):
            digest_calls.append(True)
            raise sentinel
        saved_sha, saved_new = hashlib.sha256, hashlib.new
        aliases = []
        for name, value in tuple(vars(module).items()):
            if value is saved_sha or value is saved_new:
                aliases.append((name, value))
                setattr(module, name, fail)
        hashlib.sha256 = hashlib.new = fail
        try:
            try:
                if operation == "generate_instance":
                    module.generate_instance(ids[0])
                else:
                    module.build_corpus()
            except BaseException as error:
                assert error is sentinel
            else:
                raise AssertionError("missing-native-exception")
        finally:
            hashlib.sha256, hashlib.new = saved_sha, saved_new
            for name, value in aliases:
                setattr(module, name, value)
        assert digest_calls and snapshot() == before
        native_scenarios += 1
assert {name for name in sys.modules if name.startswith("exactfrac.")} == {
    "exactfrac.corpus_irregular"
}
json.dumps = original_dumps
for owner, name, original in reversed(originals):
    setattr(owner, name, original)
print(json.dumps({"result": "PASS", "digit_limit": sys.get_int_max_str_digits(),
                  "direct_payload_checks": len(ids), "builds": 2,
                  "solver_calls": 0, "same_settings": True,
                  "native_exception_scenarios": native_scenarios}, sort_keys=True))
'''


@pytest.mark.parametrize("limit,hash_seed", ((640, "1"), (640, "73"), (4300, "1"), (4300, "73")))
def test_fresh_import_full_generation_purity_and_digit_limit_conservation(limit, hash_seed):
    expected = {"manifest": _FIXTURE_PINS["OWN_MANIFEST"], "payloads": [
        (row["recipe"], int(row["bytes"]), row["sha256"]) for row in _inventory()
    ]}
    environment = dict(os.environ)
    for key in ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONINSPECT"):
        environment.pop(key, None)
    environment.update(PYTHONINTMAXSTRDIGITS=str(limit), PYTHONHASHSEED=hash_seed,
                       PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
    before = _settings()
    result = subprocess.run(
        [sys.executable, "-B", "-s", "-c", _FRESH_PROGRAM, str(_ROOT)], cwd=_ROOT,
        env=environment, input=json.dumps(expected).encode(), capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert result.stderr == b""
    assert _json(result.stdout) == {
        "result": "PASS", "digit_limit": limit, "direct_payload_checks": 1200,
        "builds": 2, "solver_calls": 0, "same_settings": True,
        "native_exception_scenarios": 8,
    }
    assert _settings() == before


def _attainment(obj, result, selected=None):
    n, edges, capacities = obj["n"], obj["edges"], obj["f"]
    mask = result["mask"]
    _require(type(mask) is int and 0 < mask < 1 << n, "attainment-mask")
    s = sum(f for v, f in enumerate(capacities) if mask >> v & 1)
    e = sum(q for u, v, q in edges if mask >> u & 1 and mask >> v & 1)
    boundary = [(j, q) for j, (u, v, q) in enumerate(edges)
                if bool(mask >> u & 1) != bool(mask >> v & 1)]
    total = result["t"]
    _require(type(total) is int and 0 <= total <= sum(q for _j, q in boundary), "attainment-total")
    _require(s + total >= 3 and (s + total) % 2 == 1, "attainment-admissibility")
    _require((result["N"], result["D"]) == (2 * (e + total), s + total - 1),
             "unreduced-attainment-pair")
    if selected is not None:
        limits = dict(boundary)
        refs = [j for j, _count in selected]
        _require(refs == sorted(set(refs)), "selected-boundary-reference-order")
        _require(all(j in limits and type(count) is int and 1 <= count <= limits[j]
                     for j, count in selected), "selected-boundary-coordinate")
        _require(sum(count for _j, count in selected) == total, "selected-boundary-total")


def test_retained_endpoint_attainments_all_recipes_without_optimum_resolve():
    for rid in _REGISTRY:
        obj = _json(_input(rid))
        row = _references()[rid]
        a, b = row["reference_a"], row["reference_b"]
        assert a["method"] == b["method"] == "endpoint-reduction full-shore optimum"
        assert a["shore_order"] == "ascending-nonempty-mask"
        assert b["shore_order"] == "binary-reflected-Gray-nonempty"
        assert a["shores"] == b["shores"] == (1 << obj["n"]) - 1
        assert a["feasible_shores"] + a["infeasible_shores"] == a["shores"]
        assert a["feasible_shores"] == b["feasible_shores"]
        assert a["endpoint_evaluations"] == 2 * a["feasible_shores"] - a["equal_endpoint_shores"]
        assert b["monotone_endpoint_evaluations"] == b["feasible_shores"]
        assert a["empty"] is False and b["empty"] is False
        _attainment(obj, a["optimum"], a["optimum"]["selected_boundary"])
        _attainment(obj, b["optimum"])
        ao, bo = a["optimum"], b["optimum"]
        assert ao["D"] > 0 and bo["D"] > 0
        assert ao["N"] * bo["D"] == bo["N"] * ao["D"]
        # A's fixed greedy allocation is not B's witness-selection obligation.
        remaining = ao["t"]
        greedy = []
        for j, (u, v, q) in enumerate(obj["edges"]):
            if bool(ao["mask"] >> u & 1) != bool(ao["mask"] >> v & 1):
                take = min(remaining, q)
                if take:
                    greedy.append([j, take])
                    remaining -= take
        assert remaining == 0 and greedy == ao["selected_boundary"]


def test_fixed_vector_subset_retained_censuses_and_witnesses_not_reenumeration():
    """Validate saved enumeration evidence; coefficient/product counts are not enumeration."""
    rows = tuple(csv.DictReader(io.StringIO(_bank()["EXHAUSTIVE_VECTORS.csv"].decode())))
    expected_ids = tuple(rid for rid in _REGISTRY if _parts(rid)[0] in (6,
        8) and _parts(rid)[2] == 1)
    assert tuple(row["recipe"] for row in rows) == expected_ids
    assert len(rows) == 200
    assert collections.Counter(rid.rsplit("-", 1)[1][0] for rid in expected_ids) == {"p": 40,
        "s": 160}
    totals = collections.Counter()
    for row in rows:
        obj = _json(_input(row["recipe"]))
        n = obj["n"]
        census = {key: int(row[key]) for key in
                  ("shores", "vectors_visited", "admissible_vectors", "feasible_shores")}
        assert census["shores"] == (1 << n) - 1
        # Independent cardinality identity, INCLUDING inadmissible vectors.
        # This does not revisit the 475,407,622 compact vectors.
        cardinality = 0
        for mask in range(1, 1 << n):
            cardinality += math.prod(q + 1 for u, v, q in obj["edges"]
                                     if bool(mask >> u & 1) != bool(mask >> v & 1))
        assert cardinality == census["vectors_visited"]
        assert 0 < census["admissible_vectors"] <= census["vectors_visited"]
        result = {key: int(row[key]) for key in ("N", "D", "mask", "t")}
        selected = [] if not row["selected_boundary"] else [
            [int(part) for part in token.split(":")] for token in row["selected_boundary"].split(
                ";")
        ]
        _attainment(obj, result, selected)
        reference = _references()[row["recipe"]]["reference_a"]
        assert census["feasible_shores"] == reference["feasible_shores"]
        optimum = reference["optimum"]
        assert result["N"] * optimum["D"] == optimum["N"] * result["D"]
        totals.update(census)
    registered = _json(_bank()["CENSUS.json"])["mathematics"]["exhaustive_compact_vectors"]
    assert dict(totals) == registered


def test_registered_definition_endpoint_boundary_toys_and_strict_first_tie():
    cases = _json(_bank()["ENDPOINT_BOUNDARY_CASES.json"])
    required = {"s1-low", "s1-infeasible", "even-low", "even-infeasible",
                "odd-zero-boundary", "odd-parity", "constant-ratio", "decreasing",
                "increasing", "singleton-endpoints"}
    assert {case["id"] for case in cases} == required
    for case in cases:
        s, e, boundary = case["s"], case["e"], case["B"]
        admissible = [t for t in range(boundary + 1) if s + t >= 3 and (s + t) % 2]
        assert admissible == case["admissible_scalar_totals"]
        assert (admissible[0] if admissible else None) == case["least"]
        assert (admissible[-1] if admissible else None) == case["greatest"]
        retained = None
        for total in admissible:
            candidate = {"N": 2 * (e + total), "D": s + total - 1, "t": total}
            if retained is None or candidate["N"] * retained["D"] > retained["N"] * candidate["D"]:
                retained = candidate
        assert retained == case["strict_first_scalar_optimum"]


def test_registry_guard_has_passing_control_and_isolated_shape_order_membership_faults():
    _check_registry(_REGISTRY)
    mutations = (
        (list(_REGISTRY), "registry-exact-tuple"),
        ((_HostileStr(_REGISTRY[0]), *_REGISTRY[1:]), "registry-exact-str-leaves"),
        (_REGISTRY[:-1], "full-ordered-registry"),
        ((*_REGISTRY, _BASE_ID[:-3] + "s21"), "full-ordered-registry"),
        ((_REGISTRY[1], _REGISTRY[0], *_REGISTRY[2:]), "full-ordered-registry"),
        ((_REGISTRY[0], *_REGISTRY), "full-ordered-registry"),
    )
    for mutant, guard in mutations:
        with pytest.raises(AssertionError, match="^" + re.escape(guard) + "$"):
            _check_registry(mutant)


def test_build_guard_has_passing_control_and_isolated_return_shape_faults():
    pristine = (("MANIFEST", _bank()["OWN_MANIFEST"]), *(
        (row["path"], _input(row["recipe"])) for row in _inventory()
    ))
    _check_build(pristine)
    mutants = (
        (list(pristine), "build-exact-tuple"),
        ((list(pristine[0]), *pristine[1:]), "build-record-types"),
        ((("MANIFEST", bytearray(pristine[0][1])), *pristine[1:]), "build-immutable-leaves"),
        (pristine[:-1], "own-build-count"),
        ((pristine[0], pristine[2], pristine[1], *pristine[3:]), "own-path-order"),
    )
    for mutant, guard in mutants:
        with pytest.raises(AssertionError, match="^" + re.escape(guard) + "$"):
            _check_build(mutant)


def _digest_control_observation(case):
    """Independently fixed message set for helper controls, not producer output."""
    n, tau, _b, mode, seed = (case[key] for key in ("n", "tau", "b", "capacity_mode", "seed"))
    obj = _json(case["payload_ascii"].encode("ascii"))
    spine = {(u, u + 1) for u in range(n - 1)} | {(0, n - 1)}
    observed = [_message("support", seed, n, u, v)
                for u, v in itertools.combinations(range(n), 2) if (u, v) not in spine]
    observed += [_message("multiplicity", seed, n, tau, mode, u, v) for u, v, _q in obj["edges"]]
    if mode == "random":
        observed += [_message("capacity", seed, n, tau, "random", vertex) for vertex in range(n)]
    hits = [message for message in observed if message.decode("ascii") in case["override"]]
    return observed, hits


def test_digest_guard_reads_actual_payload_and_reaches_semantics_before_hash_pins():
    cases = _json(_bank()["DIGEST_INJECTION_CASES.json"])
    for case in cases:
        raw = case["payload_ascii"].encode("ascii")
        observed, hits = _digest_control_observation(case)
        _check_digest_observation(raw, case, observed, hits)
        obj = _json(raw)
        # Each changed specimen starts afresh from its complete valid control.
        altered = list(observed)
        index = next(i for i, message in enumerate(altered) if b"\nsupport\n" in message)
        altered[index] = altered[index][:-1]
        with pytest.raises(AssertionError, match=r"^domain-message-bytes$"):
            _check_digest_observation(raw, case, altered, hits)
        obj["edges"][0][2] = 0
        malformed = (json.dumps(obj, separators=(",", ":")) + "\n").encode("ascii")
        with pytest.raises(AssertionError, match=r"^positive-q-formula$"):
            _check_digest_observation(malformed, case, observed, hits)
        obj = _json(raw)
        obj["edges"].pop(0)
        malformed = (json.dumps(obj, separators=(",", ":")) + "\n").encode("ascii")
        with pytest.raises(AssertionError, match=r"^unconditional-spine$"):
            _check_digest_observation(malformed, case, observed, hits)


def test_payload_semantic_guards_precede_independent_identity_pin():
    rid = _REGISTRY[0]
    raw = _input(rid)
    _check_payload(raw, rid)
    for fault, guard in (("q", "positive-q-formula"), ("spine", "unconditional-spine"),
                         ("order", "canonical-edge-reference"), ("capacity",
                             "active-capacity-formula")):
        obj = _json(raw)
        if fault == "q":
            obj["edges"][0][2] = 0
        elif fault == "spine":
            obj["edges"].pop(0)
        elif fault == "order":
            obj["edges"][:2] = obj["edges"][1::-1]
        else:
            obj["f"][0] = 0
        mutant = (json.dumps(obj, separators=(",", ":")) + "\n").encode("ascii")
        with pytest.raises(AssertionError, match="^" + re.escape(guard) + "$"):
            _check_payload(mutant, rid)
