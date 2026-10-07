"""Unit 22 release consumer: independently committed C references, then auditor.

D22-R10--R16 and RL10--RL16 govern this module. Fixture/record validation is
independent of the inspected implementation. Real distribution builds, both
interpreter runs and publication decisions remain separately witnessed work.
"""

from __future__ import annotations

import ast
import base64
import binascii
import contextlib
import copy
import functools
import hashlib
import inspect
import io
import json
import os
import re
import socket
import stat
import struct
import subprocess
import sys
import tarfile
import types
import zipfile
import zlib
from collections.abc import Mapping
from pathlib import Path

import pytest

# isort: split
import release_audit as auditor

# Importing the absent owner above must be the first project-dependent operation.
# No stub, importorskip, conditional owner import, metadata installation or writer.
_ROOT = Path(__file__).resolve().parents[1]
_PREFIX_BYTES = 26_761_794
_PREFIX_SHA256 = "74e5ba76c4d3d41b1789abeaf2ac2e8677ad9ffc7ebf12b0ff88d5a82efba4b4"
_APPEND_BYTES = 226_452
_APPEND_SHA256 = "58c2d5813e14d2c2308ad93ed99d37cbd82a0ab02f89d892a4a07070b94f3b23"
_HEADER = "\n## Unit 22 — Phase C setup.cfg reference correction R1, October 4, 2026\n".encode()
_MARKER = re.compile(
    rb"^<!-- U22-C-CORR2 ([^ \n]+) (utf8|base64) (0|[1-9][0-9]*) ([0-9a-f]{64}) -->\n",
    re.MULTILINE,
)
_HEX64 = re.compile(r"[0-9a-f]{64}\Z")
_HEX40 = re.compile(r"[0-9a-f]{40}\Z")
# BEGIN INDEPENDENT PHASE C OBJECT PINS
_OBJECT_PINS = {
    'README.md': (
        18881, "957a98c5c7989a3d38512140df80b6033501d606c60203b4ed06d84ff147d3e9",
        "base64", "base64",
    ),
    'CITATION.cff': (
        882, "6d93ede309e0f854e42e6698778721d5f2f9ee7aaeca5adbde1ce8c3c51ec3a2",
        "utf8", "yaml",
    ),
    'LICENSE': (
        1069, "e8650c7b1066794c9f19e55a0927d7bdee5027fdf120868263edbd6649a2e7d6",
        "utf8", "text",
    ),
    'pyproject.toml': (
        952, "8fed90272a28374a421dd48323a81b41b27ee80790d40e6bfa6f57a0b370d256",
        "utf8", "toml",
    ),
    'tests/test_cli.py': (
        99824, "f2dc6a084030fba3aff1a2de490dc910c01d267db6860844452c338ac8b10c48",
        "utf8", "python",
    ),
    'MANIFEST.in': (
        624, "44e0cc5a4ce73a49d3249ae3dec84d3d053f5b8539fefb0322e534077c987451",
        "utf8", "text",
    ),
    'docs/RELEASE.md.template': (
        3513, "500e9f83e327a1c336e9c344d8b74228b565614800bb5d47dabe9843202ffd6e",
        "utf8", "markdown",
    ),
    'AUDITOR_API.json': (
        2571, "5d94d882ff9011e18f170dc63046ad07d7dcc26389c8ecb31ea7db16b33b48a2",
        "utf8", "json",
    ),
    'LIMITS.json': (
        2942, "84a5c4f79836597575e27d097bbd04e18cc0a71bf515875287864148a416c46c",
        "utf8", "json",
    ),
    'WIRE_SCHEMA.json': (
        2915, "4607d224f25b4bba2271992b1d5f3c391cc4f6a5c499bd7432bf70853569234e",
        "utf8", "json",
    ),
    'SCAN_RULES.json': (
        5154, "1359eeb95c080b568b2e65a424422d01f8d26e8cb9302f0f2985425a75c41e1c",
        "utf8", "json",
    ),
    'SDIST_PROFILE.json': (
        1521, "7c09e57821e084003365e9e5c1bcc9a3c4ba5f7bfc4871aaab6316fb6e87aa55",
        "utf8", "json",
    ),
    'WHEEL_PROFILE.json': (
        918, "f5c85813d75c1fd312710a5e43813737d7ec0fd145c7be4e3aa2e6724b4a2950",
        "utf8", "json",
    ),
    'WHEEL_SMOKE.json': (
        1704, "6cdafb6d12298af0ef10a2edc1a20e17e01084fa0393e7fbdd33c09eeaf86ec1",
        "utf8", "json",
    ),
    'RELEASE_REPORT_SCHEMA.json': (
        924, "ad29cfba15313ee0070285ecd801fc099b29a530fba8073bbeca99439b18ebf7",
        "utf8", "json",
    ),
    'TREE_RUNTIME_FIXTURE_SPEC.json': (
        2140, "f7b7ffca2c8848bd856bb78f65cbb1d79f490dfe3a4da6eef58fe7998c10c293",
        "utf8", "json",
    ),
    'DEPENDENCY_CASES.json': (
        1714, "d523ed4c74ca5d7cdb9c06a125756bfd26d29643124d9717f729b94e87f3a1de",
        "utf8", "json",
    ),
    'ARCHIVE_PRISTINE_RECORD.json': (
        1874, "08adf22986c01a124305b4bb0e3eb001ff9277e6f97ff390d44e7def28ae6151",
        "utf8", "json",
    ),
    'ARCHIVE_TRAVERSAL_RECORD.json': (
        2144, "dcba882f9d5a971eaaae7fd1e4e0fafc57882dcc4212c514b27fa73f94e12155",
        "utf8", "json",
    ),
    'HISTORY_PRISTINE_RECORD.json': (
        2990, "5b391ba7c5ff706703c2ccf3949ed82b0fe7e9ac4f1004860b06b9af7735a65f",
        "utf8", "json",
    ),
    'HISTORY_SENSITIVE_RECORD.json': (
        6879, "0d195c89b7ec0b209a9391e1e85472a8ce378f8da6ac513b7ce67c90bb4d1a7c",
        "utf8", "json",
    ),
    'SOURCE_STATUS_CROSSWALK.json': (
        3150, "2ced195c8e45a2ab566856795e6cbcb2d88b3844678b453b428dd7e06ddae497",
        "utf8", "json",
    ),
    'METADATA_IDENTITIES.json': (
        2588, "d9ddb5e3389a1c15a2fa3ac6de83f7eb11c9db6e90650430d8530a34852d45f8",
        "utf8", "json",
    ),
    'README_CLAIM_CROSSWALK.json': (
        3400, "246ee20c1295aa9a496e5cb90a773e7d8b09d8d215968c438922c577dac793b2",
        "utf8", "json",
    ),
    'GITHUB_MATH_RENDER_REFERENCE.json': (
        2982, "c1973d839e53669df21a618e106a3abb99e2d9b68d1342357948df5dff2da14c",
        "utf8", "json",
    ),
    'GITHUB_DELIMITER_INVENTORY.json': (
        1367, "4e5a02fa5bce6ca6aa4d411471ec536d44e02b3b75f773f10e578b6c4bd954ab",
        "utf8", "json",
    ),
    'README_GITHUB_RENDER_RECORD_TEMPLATE.json': (
        621, "18c620cc8004c470b0eb6edec664afe692ca5db02a0c175e33120b4884cbb6ea",
        "utf8", "json",
    ),
    'REFERENCE_INDEX.json': (
        4925, "a8367483eb0df568ec91e62c7e0a82b1a817294c54b535dd842a1bdbe48e6daa",
        "utf8", "json",
    ),
    'UNIT22_RELEASE_FIXTURE_BANK.zip': (
        20246, "5dc4d492864aeee8bdccf45960132a3e8169ce3691bbed3e78f81192aeaf950c",
        "base64", "base64",
    ),
    'UNIT22_RELEASE_FIXTURE_BANK_MANIFEST.json': (
        5765, "f2143d0111b6428f5bf8651b7d469a77ad480b5b55354400981eebd5d448766d",
        "utf8", "json",
    ),
}
# END INDEPENDENT PHASE C OBJECT PINS


def _need(condition, guard):
    if not condition:
        raise AssertionError(guard)


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _identity(raw):
    return {"bytes": len(raw), "sha256": _digest(raw)}


def _json(raw):
    """Strict independent record reader: decoded duplicate keys never disappear."""
    def pairs(items):
        result = {}
        for key, value in items:
            _need(key not in result, "duplicate-json-key")
            result[key] = value
        return result

    def forbidden(_value):
        raise AssertionError("nonfinite-json-token")

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=forbidden)


def _wire(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()


def _jsonl(rows):
    return b"".join(_wire(row) + b"\n" for row in rows)


def _extract_objects(section):
    """Read counted payloads; fenced material inside a payload is not syntax."""
    _need(type(section) is bytes, "section-bytes")
    result = {}
    cursor = 0
    while (match := _MARKER.search(section, cursor)) is not None:
        label, encoding, count, digest = match.groups()
        label = label.decode("ascii")
        _need(label in _OBJECT_PINS, "unknown-reference-label")
        _need(label not in result, "duplicate-reference-label")
        expected_count, expected_digest, expected_encoding, language = _OBJECT_PINS[label]
        _need((int(count), digest.decode(), encoding.decode()) == (
            expected_count, expected_digest, expected_encoding,
        ), "reference-marker-identity")
        opening = b"```" + language.encode() + b"\n"
        start = match.end()
        _need(section[start:start + len(opening)] == opening, "reference-opening-fence")
        start += len(opening)
        if encoding == b"base64":
            characters = 4 * ((expected_count + 2) // 3)
            breaks = (characters - 1) // 76 if characters else 0
            end = start + characters + breaks
            encoded = section[start:end]
            try:
                raw = base64.b64decode(encoded.replace(b"\n", b""), validate=True)
            except binascii.Error as exc:
                raise AssertionError("reference-base64") from exc
            canonical = base64.b64encode(raw)
            wrapped = b"\n".join(canonical[i:i + 76] for i in range(0, len(canonical), 76))
            _need(encoded == wrapped, "reference-base64-wrapping")
        else:
            end = start + expected_count
            raw = section[start:end]
            raw.decode("utf-8")
        _need(_identity(raw) == {"bytes": expected_count, "sha256": expected_digest},
              "reference-payload-identity")
        suffix = b"\n```\n" if encoding == b"base64" else b"```\n"
        _need(section[end:end + len(suffix)] == suffix, "reference-counted-suffix")
        result[label] = raw
        cursor = end + len(suffix)
    _need(set(result) == set(_OBJECT_PINS), "reference-roster")
    return result


def _read_catalogue(data):
    """Authenticate two immutable spans, not the changing catalogue suffix."""
    _need(type(data) is bytes, "catalogue-bytes")
    stop = _PREFIX_BYTES + _APPEND_BYTES
    _need(len(data) >= stop, "catalogue-truncated")
    _need(_digest(data[:_PREFIX_BYTES]) == _PREFIX_SHA256, "historical-prefix")
    section = data[_PREFIX_BYTES:stop]
    _need(section.startswith(_HEADER), "unit22-located-heading")
    _need(_digest(section) == _APPEND_SHA256, "unit22-owned-span")
    return _extract_objects(section)


@functools.cache
def _refs():
    return _read_catalogue((_ROOT / "docs/ORACLE_CATALOG.md").read_bytes())


def _reference(name):
    return _json(_refs()[name])


def _decode_fixture_bank(raw, manifest):
    """Only decode trusted bank entries; nested adversarial archives stay inert."""
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = archive.namelist()
        _need(len(names) == len(set(names)), "bank-duplicate-member")
        _need(archive.read("MANIFEST.json") == manifest, "bank-manifest-copy")
        declared = _json(manifest)
        entries = declared["members"]
        expected = {row["path"]: row for row in entries}
        _need(len(expected) == len(entries), "bank-manifest-duplicates")
        _need(set(names) == set(expected) | {"MANIFEST.json"}, "bank-roster")
        result = {}
        for name, row in expected.items():
            _safe_parts(name)
            info = archive.getinfo(name)
            _need(not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16),
                  "bank-regular-payload")
            content = archive.read(name)
            _need(_identity(content) == {"bytes": row["bytes"], "sha256": row["sha256"]},
                  "bank-payload-identity")
            result[name] = content
    return result


@functools.cache
def _bank():
    return _decode_fixture_bank(
        _refs()["UNIT22_RELEASE_FIXTURE_BANK.zip"],
        _refs()["UNIT22_RELEASE_FIXTURE_BANK_MANIFEST.json"],
    )


def _safe_parts(name):
    _need(type(name) is str and name and not name.startswith("/"), "fixture-relative-path")
    _need("\\" not in name and "\0" not in name, "fixture-path-spelling")
    parts = name.split("/")
    _need(all(part not in ("", ".", "..") for part in parts), "fixture-path-components")
    return parts


def _materialize(box):
    """Write only authenticated finite fixtures under pytest's new temporary root."""
    box.mkdir(mode=0o755)
    box.chmod(0o755)
    for name, raw in _bank().items():
        if not name.startswith(("trees/", "archives/")):
            continue
        path = box.joinpath(*_safe_parts(name))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        path.chmod(0o644)
    for path in sorted(box.rglob("*")):
        if path.is_dir():
            path.chmod(0o755)
    for name in ("histories/pristine-repo.tar", "histories/historical-sensitive-repo.tar"):
        parent = box / "histories"
        parent.mkdir(exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(_bank()[name]), mode="r:") as archive:
            seen = set()
            for member in archive:
                _need(member.name not in seen, "history-fixture-duplicate")
                seen.add(member.name)
                path = parent.joinpath(*_safe_parts(member.name))
                _need(member.isdir() or member.isfile(), "history-fixture-regular")
                if member.isdir():
                    path.mkdir(parents=True, exist_ok=True)
                    path.chmod(member.mode)
                else:
                    stream = archive.extractfile(member)
                    _need(stream is not None, "history-fixture-stream")
                    with stream:
                        raw = stream.read()
                    _need(len(raw) == member.size, "history-fixture-size")
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(raw)
                    path.chmod(member.mode)
    return box


@pytest.fixture
def box(tmp_path):
    return _materialize(tmp_path.resolve() / "finite-fixtures")


def _snapshot(root):
    """lstat-based conservation; never open a link, FIFO or socket for evidence."""
    records = []
    for path in [root, *sorted(root.rglob("*"))]:
        mode = path.lstat().st_mode
        name = "." if path == root else path.relative_to(root).as_posix()
        if stat.S_ISREG(mode):
            try:
                content = _digest(path.read_bytes())
            except PermissionError:
                content = "unreadable"
        elif stat.S_ISLNK(mode):
            content = os.readlink(path)
        else:
            content = None
        records.append((name, mode, content))
    return records


def _process_state():
    return (
        os.getcwd(), dict(os.environ), sys.getrecursionlimit(),
        sys.get_int_max_str_digits(), sys.dont_write_bytecode,
    )


def _inspect(kind, path, box, limits=None):
    before = _snapshot(box), _process_state()
    result = getattr(auditor, "inspect_" + kind)(str(path))
    _need((_snapshot(box), _process_state()) == before, "inspector-nonmutation")
    _check_record(result, kind, path, limits)
    return result


def _keys(record, names, guard):
    _need(type(record) is dict and set(record) == set(names), guard)


def _integer(value, guard):
    _need(type(value) is int and value >= 0, guard)


def _optional_hash(value, width, guard):
    pattern = _HEX64 if width == 64 else _HEX40
    _need(value is None or (type(value) is str and pattern.fullmatch(value)), guard)


def _check_record(record, kind, path, limits=None):
    """Check complete keys and algebra; exact fixture comparisons supply semantics."""
    schema = _reference("WIRE_SCHEMA.json")
    _keys(record, schema["top_level_key_order"], "record-keys")
    _need(record["format"] == schema["record_format"], "record-format")
    _need(record["kind"] == kind, "record-kind")
    _need(record["coverage"] in schema["coverage_values"], "record-coverage")
    wanted = "incomplete" if record["coverage"] == "incomplete" else (
        "findings" if record["findings"] else "no-findings"
    )
    _need(record["outcome"] == wanted, "record-outcome")
    defaults = _reference("LIMITS.json")["defaults"] if limits is None else limits
    _need(record["limits"] == defaults, "record-limits")
    for value in record["limits"].values():
        _integer(value, "limit-integer")
    subject = record["subject"]
    _keys(subject, schema["subject_key_order"], "subject-keys")
    _need(subject["input_path"] == str(path) and subject["resolved_path"] == str(path),
          "subject-binding")
    _need(type(subject["subject_type"]) is str, "subject-type")
    if subject["bytes"] is not None:
        _integer(subject["bytes"], "subject-byte-count")
    for key in ("sha256", "inventory_sha256", "refs_sha256"):
        _optional_hash(subject[key], 64, "subject-hash")
    _optional_hash(subject["git_head"], 40, "subject-head")
    inventory = record["inventory"]
    findings = record["findings"]
    gaps = record["gaps"]
    _need(type(inventory) is list and type(findings) is list and type(gaps) is list,
          "record-exact-lists")
    for row in inventory:
        _keys(row, schema["inventory_entry_key_order"], "inventory-keys")
        for key in ("path", "object_type", "source"):
            _need(type(row[key]) is str, "inventory-string")
        for key in ("mode", "target"):
            _need(row[key] is None or type(row[key]) is str, "inventory-optional-string")
        if row["bytes"] is not None:
            _integer(row["bytes"], "inventory-byte-count")
        _optional_hash(row["sha256"], 64, "inventory-sha256")
        _optional_hash(row["git_oid"], 40, "inventory-git-oid")
    inv_keys = [(r["path"].encode("utf-8"), r["object_type"], r["git_oid"] or "")
                for r in inventory]
    _need(inv_keys == sorted(set(inv_keys)), "inventory-order-uniqueness")
    _need(subject["inventory_sha256"] == _digest(_jsonl(inventory)), "inventory-digest")
    rules = {r["id"]: r for r in _reference("SCAN_RULES.json")["rules"]}
    for row in findings:
        _keys(row, schema["finding_key_order"], "finding-keys")
        _need(all(type(v) is str for v in row.values()), "finding-string")
        _need(row["rule"] in rules, "finding-rule")
        _need(row["severity"] == rules[row["rule"]]["severity"], "finding-severity")
        _need(row["summary"] == rules[row["rule"]]["summary"], "finding-redaction")
        _optional_hash(row["identity"], 64, "finding-identity")
    finding_keys = [tuple(row[k] for k in schema["sorting"]["findings"]) for row in findings]
    _need(finding_keys == sorted(set(finding_keys)), "finding-order-uniqueness")
    for row in gaps:
        _keys(row, schema["gap_key_order"], "gap-keys")
        _need(all(type(row[k]) is str for k in ("code", "location", "summary")), "gap-string")
        _optional_hash(row["identity"], 64, "gap-identity")
    gap_keys = [(r["code"], r["location"], r["identity"] or "", r["summary"]) for r in gaps]
    _need(gap_keys == sorted(set(gap_keys)), "gap-order-uniqueness")
    _need(record["coverage"] != "complete" or not gaps, "complete-with-gap")
    _need(record["coverage"] != "incomplete" or bool(gaps), "incomplete-without-gap")
    summary = record["summary"]
    _keys(summary, schema["summary_key_order"], "summary-keys")
    for value in summary.values():
        _integer(value, "summary-exact-integer")
    for key, rows in (("inventory_count", inventory), ("finding_count", findings),
                      ("gap_count", gaps)):
        _need(summary[key] == len(rows), "summary-cardinality")
    if record["coverage"] == "complete":
        _need(summary["inspected_bytes"] == sum(r["bytes"] or 0 for r in inventory),
              "summary-byte-count")
    _need(record == _json(_wire(record)), "record-json-roundtrip")


def _expected(label, path, limits=None):
    raw = _bank().get("expected/" + label)
    result = _json(raw if raw is not None else _refs()[label])
    result["subject"]["input_path"] = str(path)
    result["subject"]["resolved_path"] = str(path)
    if limits is not None:
        result["limits"] = dict(limits)
    return result


def _same_record(actual, expected):
    _need(actual == expected, "independent-exact-record")


def _pristine(kind, box):
    cases = {
        "tree": ("trees/pristine", "TREE_PRISTINE_RECORD.json"),
        "archive": ("archives/pristine.zip", "ARCHIVE_PRISTINE_RECORD.json"),
        "history": ("histories/pristine-repo", "HISTORY_PRISTINE_RECORD.json"),
    }
    name, label = cases[kind]
    _same_record(_inspect(kind, box / name, box), _expected(label, box / name))


@contextlib.contextmanager
def _controlled(kind, box):
    """Materialized challenge credit requires an actual pristine on both sides."""
    _pristine(kind, box)
    try:
        yield
    finally:
        _pristine(kind, box)


def _limits(monkeypatch, changes):
    """Use the declared replaceable mapping without inventing its private name."""
    defaults = _reference("LIMITS.json")["defaults"]
    matches = [(name, value) for name, value in vars(auditor).items()
               if name.startswith("_") and isinstance(value, Mapping) and value == defaults]
    _need(bool(matches), "private-default-limits-mapping")
    combined = defaults | changes
    for name, _value in matches:
        monkeypatch.setattr(auditor, name, types.MappingProxyType(combined))
    return combined


def _incomplete(record, rule=None):
    _need(record["coverage"] == "incomplete" and record["outcome"] == "incomplete",
          "incomplete-never-clean")
    _need(bool(record["gaps"]), "incomplete-retains-gap")
    if rule is not None:
        _need(rule in {r["rule"] for r in record["findings"]}, "registered-structural-rule")


def _make_zip(entries, compression=zipfile.ZIP_STORED):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=compression) as archive:
        for name, raw in entries:
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = compression
            archive.writestr(info, raw)
    return buffer.getvalue()


def _make_tar(name, raw=b"safe\n", member_type=tarfile.REGTYPE, linkname=""):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        info = tarfile.TarInfo(name)
        info.type = member_type
        info.mode = 0o644
        info.linkname = linkname
        info.size = len(raw) if member_type == tarfile.REGTYPE else 0
        archive.addfile(info, io.BytesIO(raw) if info.size else None)
    return buffer.getvalue()


def _put(box, name, raw):
    path = box.joinpath(*_safe_parts(name))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    path.chmod(0o644)
    return path


def _content_findings(name, raw):
    """Derive only a fixed object's literal rules, not a replacement tree scanner."""
    result = []
    for rule in _reference("SCAN_RULES.json")["rules"]:
        if rule.get("pattern") == "structural":
            continue
        expression = (bytes.fromhex(rule["pattern_hex"]).decode("ascii")
                      if "pattern_hex" in rule else rule["pattern"])
        pattern = re.compile(expression.encode("ascii"))
        hit = ("content" in rule["target"] and pattern.search(raw)) or (
            "path" in rule["target"] and pattern.search(name.encode("utf-8"))
        )
        if hit:
            result.append({"rule": rule["id"], "severity": rule["severity"],
                           "location": name, "identity": _digest(raw), "summary": rule["summary"]})
    return sorted(result, key=lambda row: (row["rule"], row["location"],
                                          row["identity"], row["summary"]))


# Reference framing, identity and future-append isolation.
def test_committed_reference_roster_and_independent_index():
    refs = _refs()
    _need(len(refs) == 30, "thirty-reference-objects")
    index = _reference("REFERENCE_INDEX.json")["objects"]
    paths = [row["path"] for row in index]
    _need(paths == sorted(set(paths)) and len(paths) == 29, "twenty-nine-indexed-objects")
    for row in index:
        name = row["path"]
        if name.startswith("candidates/"):
            label = name.removeprefix("candidates/")
        elif name == "templates/docs/RELEASE.md":
            label = "docs/RELEASE.md.template"
        else:
            label = name.rsplit("/", 1)[-1]
        _need(label in refs, "indexed-reference-present")
        _need(_identity(refs[label]) == {"bytes": row["bytes"], "sha256": row["sha256"]},
              "indexed-reference-identity")
    _need(len(_bank()) == 35, "thirty-five-fixture-payloads")
    for label in ("ARCHIVE_PRISTINE_RECORD.json", "ARCHIVE_TRAVERSAL_RECORD.json",
                  "HISTORY_PRISTINE_RECORD.json", "HISTORY_SENSITIVE_RECORD.json",
                  "TREE_RUNTIME_FIXTURE_SPEC.json", "DEPENDENCY_CASES.json"):
        _need(refs[label] == _bank()["expected/" + label], "duplicated-reference-bytes")


@pytest.mark.parametrize("suffix", [
    b"\n## Later unit\nNot a Unit 22 payload.\n",
    b"## Later unit without an extra separator\n```json\n{}\n```\n",
    _HEADER + b"<!-- U22-C-CORR2 README.md base64 1 " + b"0" * 64 + b" -->\n",
    b"later suffix with no terminating newline",
], ids=["ordinary", "adjacent-heading", "outside-marker-lookalike", "no-final-lf"])
def test_later_catalogue_appends_cannot_change_owned_references(suffix):
    data = (_ROOT / "docs/ORACLE_CATALOG.md").read_bytes()
    original = _read_catalogue(data)
    _need(_read_catalogue(data + suffix) == original, "later-append-isolation")
    _need(_read_catalogue(data) == original, "pristine-after-append-control")


@pytest.mark.parametrize("fault", ["truncated", "prefix", "heading", "separator", "span"])
def test_catalogue_span_damage_is_not_hidden_by_valid_new_markers(fault):
    data = (_ROOT / "docs/ORACLE_CATALOG.md").read_bytes()
    original = _read_catalogue(data)
    if fault == "truncated":
        changed = data[:_PREFIX_BYTES + _APPEND_BYTES - 1]
    elif fault == "prefix":
        changed = b"!" + data[1:]
    elif fault == "heading":
        changed = data[:_PREFIX_BYTES + 1] + b"!" + data[_PREFIX_BYTES + 2:]
    elif fault == "separator":
        changed = data[:_PREFIX_BYTES] + data[_PREFIX_BYTES + 1:]
    else:
        pos = _PREFIX_BYTES + _APPEND_BYTES - 3
        changed = data[:pos] + b"!" + data[pos + 1:]
    with pytest.raises(AssertionError):
        _read_catalogue(changed)
    _need(_read_catalogue(data) == original, "pristine-after-span-control")


@pytest.mark.parametrize("fault", ["count", "digest", "encoding", "payload", "wrapping",
                                    "suffix", "duplicate", "unknown", "missing"])
def test_counted_reference_parser_challenges_reach_parser_guards(fault):
    data = (_ROOT / "docs/ORACLE_CATALOG.md").read_bytes()
    section = data[_PREFIX_BYTES:_PREFIX_BYTES + _APPEND_BYTES]
    original = _extract_objects(section)
    marker = _MARKER.search(section)
    _need(marker is not None, "first-reference-marker")
    start = marker.end() + len(b"```base64\n")
    characters = 4 * ((18_881 + 2) // 3)
    end = start + characters + (characters - 1) // 76
    block_end = end + 5
    if fault in ("count", "digest", "encoding", "unknown"):
        field, value = {"count": (3, b"18880"), "digest": (4, b"0" * 64),
                        "encoding": (2, b"utf8"), "unknown": (1, b"UNDECLARED.md")}[fault]
        a, b = marker.span(field)
        changed = section[:a] + value + section[b:]
    elif fault == "payload":
        changed = section[:start] + b"A" + section[start + 1:]
    elif fault == "wrapping":
        changed = section[:start + 76] + section[start + 77:]
    elif fault == "suffix":
        changed = section[:end] + b"!" + section[end + 1:]
    elif fault == "duplicate":
        changed = section + b"\n" + section[marker.start():block_end]
    elif fault == "missing":
        changed = section[:marker.start()] + section[block_end:]
    else:
        raise AssertionError("unregistered-parser-control")
    with pytest.raises(AssertionError):
        _extract_objects(changed)
    _need(_extract_objects(section) == original, "pristine-after-parser-control")


def test_base64_readme_and_runtime_only_positive_reference_are_exact():
    refs = _refs()
    raw = refs["README.md"]
    _need(len(raw) == 18_881 and b"```" in raw, "readme-decoded-with-its-own-fences")
    _need(_OBJECT_PINS["README.md"][2] == "base64", "readme-base64")
    _need(_OBJECT_PINS["UNIT22_RELEASE_FIXTURE_BANK.zip"][2] == "base64", "bank-base64")
    runtime = _reference("TREE_RUNTIME_FIXTURE_SPEC.json")
    positive = next(row for row in runtime["cases"] if row["id"] == "provenance-positive-runtime")
    raw = bytes.fromhex(_reference("SCAN_RULES.json")["encoded_provenance_contract"]
                        ["positive_case_hex"])
    _need(_digest(raw) == positive["expected_sha256"], "runtime-positive-digest")
    _need(positive["persistent_fixture_member"] is False, "no-persistent-positive")
    _need("trees/reviewable/PROVENANCE.txt" not in _bank(), "removed-reviewable-fixture")
    _need("trees/findings/provider.txt" not in _bank(), "removed-provider-fixture")
    _need(not any(raw in payload for payload in _bank().values()), "no-plaintext-positive")


# Auditor public contract and independent exact records.
def test_public_exports_and_signatures_are_the_frozen_interface():
    api = _reference("AUDITOR_API.json")
    _need(Path(auditor.__file__).resolve() == (_ROOT / "release_audit.py").resolve(),
          "auditor-import-origin")
    exports = getattr(auditor, "__all__", tuple(
        name for name, value in vars(auditor).items() if not name.startswith("_")
        and inspect.isfunction(value) and value.__module__ == auditor.__name__
    ))
    _need(set(exports) == set(api["exports"]), "public-exports")
    for row, parameter in zip(api["public_api"], ("root", "path", "repository"), strict=True):
        function = getattr(auditor, row["name"])
        _need(inspect.isfunction(function), "public-function")
        params = list(inspect.signature(function).parameters.values())
        _need(len(params) == 1 and params[0].name == parameter, "public-one-parameter")
        _need(params[0].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
              and params[0].default is inspect.Parameter.empty, "public-parameter-contract")


@pytest.mark.parametrize("kind,relative,label", [
    ("tree", "trees/pristine", "TREE_PRISTINE_RECORD.json"),
    ("tree", "trees/findings", "TREE_FINDINGS_RECORD.json"),
    ("archive", "archives/pristine.zip", "ARCHIVE_PRISTINE_RECORD.json"),
    ("archive", "archives/traversal.zip", "ARCHIVE_TRAVERSAL_RECORD.json"),
    ("history", "histories/pristine-repo", "HISTORY_PRISTINE_RECORD.json"),
    ("history", "histories/historical-sensitive-repo", "HISTORY_SENSITIVE_RECORD.json"),
])
def test_exact_frozen_records_and_repeat_determinism(box, kind, relative, label):
    with _controlled(kind, box):
        path = box / relative
        expected = _expected(label, path)
        first = _inspect(kind, path, box)
        second = _inspect(kind, path, box)
        _same_record(first, expected)
        _same_record(second, expected)
        _need(first is not second and first["inventory"] is not second["inventory"],
              "fresh-independent-records")
        first["inventory"].clear()
        _same_record(second, expected)
        _same_record(_inspect(kind, path, box), expected)


@pytest.mark.parametrize("kind", ["tree", "archive", "history"])
@pytest.mark.parametrize("value_kind", ["none", "bool", "int", "path", "str-subclass", "bytes"])
def test_wrong_python_arguments_fail_before_data_or_commands(box, monkeypatch, kind, value_kind):
    class Text(str):
        def __str__(self):
            raise AssertionError("path-coercion-is-not-permitted")

    values = {"none": None, "bool": True, "int": 1, "path": box,
              "str-subclass": Text(str(box)), "bytes": os.fsencode(box)}
    with _controlled(kind, box):
        before = _snapshot(box), _process_state()
        calls = []

        def tripwire(*_args, **_kwargs):
            calls.append("activity")
            raise AssertionError("wrong-argument-activity")

        with monkeypatch.context() as patch:
            for module, name in ((io, "open"), (os, "open"), (subprocess, "Popen")):
                _patch_dependency(patch, module, name, tripwire)
            with pytest.raises(ValueError) as caught:
                getattr(auditor, "inspect_" + kind)(values[value_kind])
            _need(type(caught.value) is ValueError and not calls, "exact-argument-valueerror")
        _need((_snapshot(box), _process_state()) == before, "argument-nonmutation")


@pytest.mark.parametrize("kind", ["tree", "archive", "history"])
@pytest.mark.parametrize("fault", [
    "relative", "missing", "wrong-kind", "root-link", "ancestor-link",
])
def test_invalid_path_domain_is_rejected_without_target_reads(box, monkeypatch, kind, fault):
    paths = {"tree": box / "trees/pristine", "archive": box / "archives/pristine.zip",
             "history": box / "histories/pristine-repo"}
    with _controlled(kind, box):
        path = paths[kind]
        if fault == "relative":
            value = "relative-input"
        elif fault == "missing":
            value = str(box / "missing")
        elif fault == "wrong-kind":
            value = str(box / "trees/pristine" if kind == "archive"
                        else box / "archives/pristine.zip")
        elif fault == "root-link":
            link = box / "root-link"
            link.symlink_to(path)
            value = str(link)
        else:
            link = box / "ancestor-link"
            link.symlink_to(path.parent, target_is_directory=True)
            value = str(link / path.name)
        before = _snapshot(box), _process_state()
        hits = []

        def forbidden(*_args, **_kwargs):
            hits.append("input-activity")
            raise AssertionError("invalid-path-target-read")

        with monkeypatch.context() as patch:
            patch.setattr(io, "open", forbidden)
            patch.setattr(os, "open", forbidden)
            _patch_dependency(patch, subprocess, "Popen", forbidden)
            with pytest.raises(ValueError) as caught:
                getattr(auditor, "inspect_" + kind)(value)
        _need(type(caught.value) is ValueError and not hits, "exact-path-valueerror")
        _need((_snapshot(box), _process_state()) == before, "unsafe-path-nonmutation")


def test_executable_archive_is_wrong_public_input(box):
    with _controlled("archive", box):
        path = _put(box, "executable.zip", _bank()["archives/pristine.zip"])
        path.chmod(0o755)
        before = _snapshot(box)
        with pytest.raises(ValueError) as caught:
            auditor.inspect_archive(str(path))
        _need(type(caught.value) is ValueError, "exact-executable-valueerror")
        _need(_snapshot(box) == before, "no-archive-chmod")


@pytest.mark.parametrize("case", _json(_bank()["expected/STRUCTURAL_CASES.json"])["cases"],
                         ids=lambda row: row["fixture"])
def test_registered_archive_structural_cases(box, case):
    with _controlled("archive", box):
        record = _inspect("archive", box / case["fixture"], box)
        _need(record["coverage"] == case["coverage"], "registered-archive-coverage")
        _need(set(case["rules"]) <= {r["rule"] for r in record["findings"]},
              "registered-archive-rules")
        if case["coverage"] == "incomplete":
            _incomplete(record, case["rules"][0])


@pytest.mark.parametrize("name,member_type,rule", [
    ("../outside.txt", tarfile.REGTYPE, "ARCHIVE001"),
    ("/outside.txt", tarfile.REGTYPE, "ARCHIVE001"),
    ("a\\b.txt", tarfile.REGTYPE, "ARCHIVE001"),
    ("link", tarfile.SYMTYPE, "ARCHIVE002"),
    ("hard", tarfile.LNKTYPE, "ARCHIVE002"),
    ("device", tarfile.CHRTYPE, "ARCHIVE002"),
    ("block", tarfile.BLKTYPE, "ARCHIVE002"),
    ("fifo", tarfile.FIFOTYPE, "ARCHIVE002"),
])
def test_tar_unsafe_names_and_types_are_never_extracted(box, name, member_type, rule):
    with _controlled("archive", box):
        raw = _make_tar(name, member_type=member_type, linkname="../outside.txt")
        path = _put(box, "adversarial.tar", raw)
        record = _inspect("archive", path, box)
        _incomplete(record, rule)
        _need(not (box.parent / "outside.txt").exists(), "no-escaping-extraction")


@pytest.mark.parametrize("compressed", [False, True], ids=["tar", "tar-gzip"])
def test_safe_tar_family_inspection_reads_actual_member_bytes(box, compressed):
    import gzip

    with _controlled("archive", box):
        content = b"synthetic safe data\n"
        raw = _make_tar("folder/member.txt", content)
        path = _put(box, "safe.tar.gz" if compressed else "safe.tar",
                    gzip.compress(raw, mtime=0) if compressed else raw)
        result = _inspect("archive", path, box)
        _need(result["coverage"] == "complete", "supported-tar-complete")
        regular = [r for r in result["inventory"] if r["object_type"] == "regular"]
        _need(len(regular) == 1 and regular[0]["path"] == "folder/member.txt",
              "tar-real-membership")
        _need((regular[0]["bytes"], regular[0]["sha256"]) == (len(content), _digest(content)),
              "tar-decoded-byte-identity")
        _need(result["findings"] == [], "safe-tar-no-findings")


@pytest.mark.parametrize("fault", ["truncated", "unsupported-method", "wrong-crc", "false-size"])
def test_corrupt_zip_metadata_cannot_be_a_clean_scan(box, fault):
    with _controlled("archive", box):
        raw = bytearray(_bank()["archives/pristine.zip"])
        local = raw.index(b"PK\x03\x04")
        central = raw.index(b"PK\x01\x02")
        if fault == "truncated":
            raw = raw[:-30]
        elif fault == "unsupported-method":
            struct.pack_into("<H", raw, local + 8, 99)
            struct.pack_into("<H", raw, central + 10, 99)
        elif fault == "wrong-crc":
            struct.pack_into("<I", raw, local + 14, 0)
            struct.pack_into("<I", raw, central + 16, 0)
        else:
            size = struct.unpack_from("<I", raw, central + 24)[0]
            struct.pack_into("<I", raw, central + 24, size + 17)
            struct.pack_into("<I", raw, local + 22, size + 17)
        path = _put(box, "corrupt.zip", bytes(raw))
        result = _inspect("archive", path, box)
        _incomplete(result)


def test_nested_container_is_read_and_sensitive_inner_bytes_are_detected(box):
    with _controlled("archive", box):
        raw = _bank()["trees/findings/token.txt"]
        inner = _make_zip([("inner.txt", raw)])
        outer = _make_zip([("nested.zip", inner)])
        record = _inspect("archive", _put(box, "nested-positive.zip", outer), box)
        _need(record["coverage"] == "complete", "supported-nested-complete")
        hits = [f for f in record["findings"] if f["rule"] == "SECRET002"]
        _need(len(hits) == 1 and hits[0]["identity"] == _digest(raw), "nested-content-bound-hit")
        _need(record["summary"]["archive_depth"] == 2, "nested-actual-depth")
        _need(raw.strip() not in _wire(record), "nested-secret-not-echoed")


def _inspect_nonutf8_tree(root, box, monkeypatch, record_property):
    """Use a real byte name, or an observed-EILSEQ directory-entry injection."""
    import builtins
    import errno

    raw_name = b"invalid-\xff"
    raw_path = os.fsencode(root) + b"/" + raw_name
    control = _put(root, "readable-control.txt", b"readable-control\n")
    mode = "native-byte-name"
    try:
        descriptor = os.open(raw_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except OSError as exc:
        if exc.errno != errno.EILSEQ:
            raise
        mode = "controlled-scandir-after-EILSEQ"
    else:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(b"nonutf8-name-payload\n")
    record_property("nonutf8_fixture_mode", mode)
    before = _snapshot(box), _process_state()
    identity = root.stat()
    root_key = identity.st_dev, identity.st_ino
    original_scandir, original_stat, original_fstat = os.scandir, os.stat, os.fstat
    enumerated, injected, accesses = [], [], []

    def guarded(original):
        def checked(path, *args, **kwargs):
            try:
                raw = os.fsencode(path)
            except TypeError:
                raw = None
            if raw in (raw_path, raw_name):
                accesses.append(original.__name__)
                raise AssertionError("nonutf8-target-must-not-be-accessed")
            return original(path, *args, **kwargs)
        return checked

    @contextlib.contextmanager
    def directory_entries(path):
        info = original_fstat(path) if type(path) is int else original_stat(path)
        matches_root = (info.st_dev, info.st_ino) == root_key
        with original_scandir(path) as entries:
            if not matches_root:
                yield entries
            else:
                enumerated.append(True)

                def children():
                    for entry in entries:
                        if mode != "native-byte-name":
                            _need(os.fsencode(entry.name) != raw_name,
                                  "controlled-entry-must-not-already-exist")
                        yield entry
                    if mode != "native-byte-name":
                        injected.append(True)
                        yield types.SimpleNamespace(name=os.fsdecode(raw_name))

                yield children()

    with monkeypatch.context() as patch:
        _patch_dependency(patch, os, "scandir", directory_entries)
        for module, name in ((builtins, "open"), (io, "open"), (os, "open"),
                             (os, "stat"), (os, "lstat")):
            _patch_dependency(patch, module, name, guarded(getattr(module, name)))
        result = auditor.inspect_tree(str(root))
    _need((_snapshot(box), _process_state()) == before, "nonutf8-inspector-nonmutation")
    _check_record(result, "tree", root)
    _incomplete(result, "COVERAGE001")
    _need(bool(enumerated) and not accesses, "nonutf8-enumerated-without-target-access")
    _need(bool(injected) == (mode != "native-byte-name"), "nonutf8-injection-observed")
    control_hash = _digest(b"readable-control\n")
    _need(any(row["path"] == control.name and row["sha256"] == control_hash
              for row in result["inventory"]), "nonutf8-readable-control-inspected")
    unsafe = [row for row in result["inventory"] if row["path"] not in (".", control.name)]
    _need(len(unsafe) == 1 and unsafe[0]["bytes"] is None and unsafe[0]["sha256"] is None,
          "nonutf8-unread-entry-retained")
    location = unsafe[0]["path"]
    _need(any(row["location"] == location and row["rule"] == "COVERAGE001"
              for row in result["findings"]), "nonutf8-finding-bound-to-entry")
    _need(any(row["location"] == location for row in result["gaps"]),
          "nonutf8-gap-bound-to-entry")
    return result


@pytest.mark.parametrize("case_id", ["entry-symlink", "fifo", "unix-socket", "non-utf8-name"])
def test_tree_nonregular_entries_retain_coverage_without_reading_targets(
    box, case_id, monkeypatch, record_property,
):
    with _controlled("tree", box):
        root = box / "runtime-tree"
        root.mkdir(mode=0o755)
        resource = None
        if case_id == "entry-symlink":
            target = _put(box, "external-marker.txt", b"external-target-must-not-be-scanned\n")
            (root / "entry").symlink_to(target)
        elif case_id == "fifo":
            _need(hasattr(os, "mkfifo"), "required-posix-fifo-capability")
            os.mkfifo(root / "entry")
        elif case_id == "unix-socket":
            _need(hasattr(socket, "AF_UNIX"), "required-unix-socket-capability")
            resource = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            # tmp_path basename depth must not exceed the platform's AF_UNIX limit.
            previous = os.getcwd()
            try:
                os.chdir(root)
                resource.bind("s")
            finally:
                os.chdir(previous)
        else:
            _need(os.name == "posix", "required-posix-filename-capability")
            result = _inspect_nonutf8_tree(root, box, monkeypatch, record_property)
        try:
            if case_id != "non-utf8-name":
                result = _inspect("tree", root, box)
            _incomplete(result, "COVERAGE001")
            if case_id == "entry-symlink":
                hashes = [row["sha256"] for row in result["inventory"]]
                _need(_digest(target.read_bytes()) not in hashes,
                      "symlink-target-not-inventoried")
        finally:
            if resource is not None:
                resource.close()


def test_provenance_positive_is_created_only_at_test_runtime(box):
    with _controlled("tree", box):
        rule = _reference("SCAN_RULES.json")["encoded_provenance_contract"]
        spec = next(row for row in _reference("TREE_RUNTIME_FIXTURE_SPEC.json")["cases"]
                    if row["id"] == "provenance-positive-runtime")
        raw = bytes.fromhex(rule["positive_case_hex"])
        _need(_digest(raw) == spec["expected_sha256"], "runtime-positive-exact-bytes")
        root = box / "runtime-positive"
        root.mkdir(mode=0o755)
        _put(root, spec["relative_path"], raw)
        record = _inspect("tree", root, box)
        _need(record["coverage"] == "complete" and record["outcome"] == "findings",
              "runtime-positive-complete-findings")
        _need(record["findings"] == _content_findings(spec["relative_path"], raw),
              "runtime-positive-exact-rule")


@pytest.mark.parametrize("repeat,binary", [(1, False), (3, False), (1, True), (3, True)])
def test_one_finding_per_rule_object_and_binary_byte_scanning(box, repeat, binary):
    with _controlled("tree", box):
        content = _bank()["trees/findings/token.txt"]
        raw = (b"\xff\0" if binary else b"") + content * repeat
        root = box / "token-case"
        root.mkdir(mode=0o755)
        _put(root, "content.bin", raw)
        record = _inspect("tree", root, box)
        _need(record["coverage"] == "complete", "binary-scanning-complete")
        _need(record["findings"] == _content_findings("content.bin", raw),
              "one-finding-per-rule-object")
        _need(content.strip() not in _wire(record), "secret-redacted")


def test_inspected_source_is_not_executed(box):
    with _controlled("tree", box):
        root = box / "inert-code"
        root.mkdir(mode=0o755)
        _put(root, "inert.py", b"raise AssertionError('inspected code was executed')\n")
        result = _inspect("tree", root, box)
        _need(result["coverage"] == "complete" and not result["findings"], "source-is-data")


@pytest.mark.parametrize("case", _json(_bank()["expected/LIMIT_CASES.json"])["cases"],
                         ids=lambda row: row["id"])
def test_registered_finite_limit_cases(box, monkeypatch, case):
    name = case["fixture"]
    kind = "archive" if name.startswith("archives/") else (
        "history" if name.startswith("histories/") else "tree"
    )
    path = box / (name.removesuffix(".tar") if kind == "history" else name)
    with _controlled(kind, box), monkeypatch.context() as patch:
        limits = _limits(patch, case["override"])
        result = _inspect(kind, path, box, limits)
        _need(result["coverage"] == case["coverage"], "registered-finite-limit-coverage")
        if case["coverage"] == "incomplete":
            _incomplete(result)


@pytest.mark.parametrize("key,at,above", [
    ("max_regular_file_bytes", 16, 15),
])
def test_remaining_tree_byte_and_path_boundaries(box, monkeypatch, key, at, above):
    with _controlled("tree", box):
        root = box / "small-tree-limit"
        root.mkdir(mode=0o755)
        _put(root, "abcd.txt", b"0123456789abcdef")
        for limit, coverage in ((at, "complete"), (above, "incomplete"), (at, "complete")):
            with monkeypatch.context() as patch:
                limits = _limits(patch, {key: limit})
                result = _inspect("tree", root, box, limits)
                _need(result["coverage"] == coverage, "tree-ceiling-boundary")
                if coverage == "incomplete":
                    _incomplete(result)


def test_declared_total_byte_override_uses_its_own_two_member_fixture(box, monkeypatch):
    """The 32-byte generic override and the 48-byte bank fixture are distinct."""
    with _controlled("archive", box):
        path = _put(box, "two-members.zip", _make_zip([
            ("a", b"0123456789abcdef"), ("b", b"fedcba9876543210"),
        ]))
        for count, coverage in ((32, "complete"), (31, "incomplete"), (32, "complete")):
            with monkeypatch.context() as patch:
                limits = _limits(patch, {"max_archive_uncompressed_bytes": count})
                result = _inspect("archive", path, box, limits)
                _need(result["coverage"] == coverage, "two-member-total-byte-boundary")
                if coverage == "incomplete":
                    _incomplete(result)


def test_declared_compression_ratio_override_has_measured_8_to_7_boundary(box, monkeypatch):
    with _controlled("archive", box):
        # A raw-deflate stream is independently measured, not inferred from a header.
        payload = next(b"x" * n for n in range(16, 256)
                       if 7 * len(zlib.compress(b"x" * n)[2:-4]) < n
                       <= 8 * len(zlib.compress(b"x" * n)[2:-4]))
        raw = _make_zip([("a", payload)], zipfile.ZIP_DEFLATED)
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            info = archive.infolist()[0]
            _need(7 * info.compress_size < len(payload) <= 8 * info.compress_size,
                  "independent-ratio-fixture")
        path = _put(box, "ratio-eight.zip", raw)
        for count, coverage in ((8, "complete"), (7, "incomplete"), (8, "complete")):
            with monkeypatch.context() as patch:
                limits = _limits(patch, {"max_compression_ratio_numerator": count})
                result = _inspect("archive", path, box, limits)
                _need(result["coverage"] == coverage, "generic-ratio-boundary")
                if coverage == "incomplete":
                    _incomplete(result)


def _history_objects_from_fixture(name):
    """Decode the frozen loose objects directly, without the future inspector."""
    result = {}
    with tarfile.open(fileobj=io.BytesIO(_bank()[name]), mode="r:") as archive:
        for member in archive:
            parts = member.name.split("/")
            if len(parts) != 4 or parts[1] != "objects" or len(parts[2]) != 2:
                continue
            stream = archive.extractfile(member)
            _need(stream is not None, "history-object-fixture-stream")
            with stream:
                raw = zlib.decompress(stream.read())
            header, payload = raw.split(b"\0", 1)
            kind, length = header.split(b" ", 1)
            oid = parts[2] + parts[3]
            _need(hashlib.sha1(raw).hexdigest() == oid and int(length) == len(payload),
                  "independent-git-object-identity")
            result[oid] = (kind.decode("ascii"), payload)
    return result


def test_history_frozen_examples_match_independent_loose_objects(box):
    specs = _json(_bank()["expected/HISTORY_EXPECTATIONS.json"])
    for name in ("pristine", "historical_sensitive"):
        row = specs[name]
        objects = _history_objects_from_fixture(row["archive"])
        label = ("HISTORY_PRISTINE_RECORD.json" if name == "pristine"
                 else "HISTORY_SENSITIVE_RECORD.json")
        expected = _reference(label)
        inventory = {r["git_oid"]: r for r in expected["inventory"]
                     if r["object_type"] != "git-ref"}
        _need(set(inventory) == set(objects), "history-reference-object-roster")
        for oid, (kind, payload) in objects.items():
            entry = inventory[oid]
            _need(entry["object_type"] == "git-" + kind, "history-object-type")
            _need((entry["bytes"], entry["sha256"]) == (len(payload), _digest(payload)),
                  "history-payload-identity")
        _need(expected["summary"]["inspected_bytes"] == sum(len(p) for _, p in objects.values()),
              "history-independent-payload-sum")
        _need(expected["subject"]["git_head"] == row["head"], "history-head-reference")
    with _controlled("history", box):
        root = box / "histories/historical-sensitive-repo"
        record = _inspect("history", root, box)
        identities = {r["rule"] for r in record["findings"]}
        _need(set(specs["historical_sensitive"]["required_rules"]) <= identities,
              "deleted-historical-payloads-retained")


def test_generic_history_eight_object_boundary_is_distinct_from_nine_object_bank(box, monkeypatch):
    with _controlled("history", box):
        # Remove only the synthetic annotated-tag ref from a newly materialized copy.
        # The ninth object ceases to be reachable; no real repository is touched.
        source = box / "histories/historical-sensitive-repo"
        duplicate = box / "eight-object-history"
        import shutil
        shutil.copytree(source, duplicate)
        (duplicate / "refs/tags/fixture-v1").unlink()
        known = _history_objects_from_fixture("histories/historical-sensitive-repo.tar")
        _need(len(known) == 9 and sum(k == "tag" for k, _ in known.values()) == 1,
              "one-tag-separates-eight-from-nine")
        for count, coverage in ((8, "complete"), (7, "incomplete"), (8, "complete")):
            with monkeypatch.context() as patch:
                limits = _limits(patch, {"max_history_objects": count})
                result = _inspect("history", duplicate, box, limits)
                _need(result["coverage"] == coverage, "generic-history-object-boundary")
                if coverage == "complete":
                    _need(result["summary"]["history_objects"] == 8, "reachable-eight-objects")
                else:
                    _incomplete(result)


def test_git_output_ceiling_is_explicitly_incomplete(box, monkeypatch):
    with _controlled("history", box), monkeypatch.context() as patch:
        limits = _limits(patch, {"max_git_stdout_bytes": 1})
        result = _inspect("history", box / "histories/pristine-repo", box, limits)
        _incomplete(result)


def _patch_dependency(patch, module, name, replacement):
    """Reach both module access and already-bound direct imports of a dependency."""
    original = getattr(module, name)
    for alias, value in list(vars(auditor).items()):
        if value is original:
            patch.setattr(auditor, alias, replacement)
    patch.setattr(module, name, replacement)


def _guard_history_processes(patch, repository, calls):
    api = _reference("AUDITOR_API.json")
    allowed = [tuple(str(repository) if part == "<repository>" else part for part in argv)
               for argv in api["history_commands"]]
    original = subprocess.Popen

    def guarded(args, *extra, **kwargs):
        _need(type(args) in (tuple, list) and tuple(args) in allowed, "read-only-git-command")
        _need(not kwargs.get("shell", False), "git-no-shell")
        env = kwargs.get("env")
        _need(type(env) is dict, "git-explicit-environment")
        # Only inherited allowlisted data and fixed locale/read-only Git controls.
        controls = {"LC_ALL", "LANG", "GIT_OPTIONAL_LOCKS", "GIT_CONFIG_NOSYSTEM",
                    "GIT_CONFIG_GLOBAL", "GIT_NO_REPLACE_OBJECTS"}
        _need(set(env) <= set(api["history_command_rules"]["environment_allowlist"]) | controls,
              "git-environment-allowlist")
        _need(env.get("LC_ALL") == "C", "git-fixed-locale")
        if "GIT_OPTIONAL_LOCKS" in env:
            _need(env["GIT_OPTIONAL_LOCKS"] == "0", "git-no-optional-locks")
        calls.append(tuple(args))
        return original(args, *extra, **kwargs)

    _patch_dependency(patch, subprocess, "Popen", guarded)


def test_history_uses_only_registered_read_only_git_commands(box, monkeypatch):
    with _controlled("history", box):
        root = box / "histories/historical-sensitive-repo"
        calls = []
        with monkeypatch.context() as patch:
            _guard_history_processes(patch, root, calls)
            result = _inspect("history", root, box)
        _same_record(result, _expected("HISTORY_SENSITIVE_RECORD.json", root))
        _need(bool(calls), "real-git-acquisition-observed")
        _need(any("cat-file" in command for command in calls), "history-object-bytes-acquired")


def _intercept_file_reads(patch, path, exception, hits):
    import builtins

    target = os.fspath(path)
    saved = [(builtins, "open", builtins.open), (io, "open", io.open), (os, "open", os.open)]
    originals = {id(function) for _, _, function in saved}

    def wrap(function):
        def read(candidate, *args, **kwargs):
            try:
                same = os.fsdecode(os.fspath(candidate)) == target
            except TypeError:
                same = False
            if same:
                hits.append(target)
                raise exception
            return function(candidate, *args, **kwargs)
        return read

    for module, name, function in saved:
        patch.setattr(module, name, wrap(function))
    for name, value in list(vars(auditor).items()):
        if id(value) in originals:
            patch.setattr(auditor, name, wrap(value))


@pytest.mark.parametrize("kind", ["tree", "archive"])
def test_native_read_exception_keeps_object_identity(box, monkeypatch, kind):
    with _controlled(kind, box):
        path = box / ("trees/pristine/alpha.txt" if kind == "tree" else "archives/pristine.zip")
        subject = path.parent if kind == "tree" else path
        error = OSError("registered synthetic read failure")
        hits = []
        before = _snapshot(box), _process_state()
        with monkeypatch.context() as patch:
            _intercept_file_reads(patch, path, error, hits)
            with pytest.raises(OSError) as caught:
                getattr(auditor, "inspect_" + kind)(str(subject))
            _need(caught.value is error and bool(hits), "native-read-identity-and-reached")
        _need((_snapshot(box), _process_state()) == before, "failed-read-nonmutation")


def test_unreadable_file_has_explicit_coverage_not_clean_inspection(box):
    """The sole capability skip is the one explicitly allowed by the C fixture."""
    root = box / "permission-case"
    root.mkdir(mode=0o755)
    path = _put(root, "unreadable.txt", b"protected finite fixture\n")
    path.chmod(0)
    readable = False
    try:
        with contextlib.suppress(PermissionError):
            path.read_bytes()
            readable = True
        if readable:
            pytest.skip("registered unreadable-file exception: effective identity can still read")
        with _controlled("tree", box):
            result = _inspect("tree", root, box)
            _incomplete(result)
    finally:
        # Test-fixture teardown only; the inspector itself must not change modes.
        path.chmod(0o644)


def test_native_subprocess_exception_keeps_object_identity(box, monkeypatch):
    with _controlled("history", box):
        error = subprocess.CalledProcessError(71, ["git", "synthetic"], b"", b"synthetic")
        hits = []
        before = _snapshot(box), _process_state()

        def fail(*_args, **_kwargs):
            hits.append("process")
            raise error

        with monkeypatch.context() as patch:
            _patch_dependency(patch, subprocess, "Popen", fail)
            with pytest.raises(subprocess.CalledProcessError) as caught:
                auditor.inspect_history(str(box / "histories/pristine-repo"))
            _need(caught.value is error and hits, "native-git-identity-and-reached")
        _need((_snapshot(box), _process_state()) == before, "failed-git-nonmutation")


def _malform_subprocess_promises(patch, fault, hits):
    """Corrupt observed stdout at run, check_output, or direct pipe boundaries."""
    original_run, original_popen = subprocess.run, subprocess.Popen
    original_check_output = subprocess.check_output
    outer = []

    def invalid():
        hits.append(fault)
        return {"stdout-text": "invalid promised bytes", "stdout-none": None,
                "stdout-list": [b"invalid"]}[fault]

    def run(*args, **kwargs):
        nested = bool(outer)
        outer.append(True)
        try:
            result = original_run(*args, **kwargs)
        finally:
            outer.pop()
        if not nested:
            result.stdout = invalid()
        return result

    def check_output(*args, **kwargs):
        outer.append(True)
        try:
            original_check_output(*args, **kwargs)
        finally:
            outer.pop()
        return invalid()

    class Stream:
        def __init__(self, stream):
            self._stream = stream

        def __getattr__(self, name):
            return getattr(self._stream, name)

        def read(self, *args, **kwargs):
            self._stream.read(*args, **kwargs)
            return invalid()

        def readline(self, *args, **kwargs):
            self._stream.readline(*args, **kwargs)
            return invalid()

        def __iter__(self):
            return self

        def __next__(self):
            next(self._stream)
            return invalid()

    class Process:
        def __init__(self, process):
            self._process = process

        def __getattr__(self, name):
            if name == "stdout" and self._process.stdout is not None:
                return Stream(self._process.stdout)
            return getattr(self._process, name)

        def __enter__(self):
            self._process.__enter__()
            return self

        def __exit__(self, *args):
            return self._process.__exit__(*args)

        def communicate(self, *args, **kwargs):
            _stdout, stderr = self._process.communicate(*args, **kwargs)
            return invalid(), stderr

    def popen(*args, **kwargs):
        result = original_popen(*args, **kwargs)
        return result if outer else Process(result)

    _patch_dependency(patch, subprocess, "Popen", popen)
    _patch_dependency(patch, subprocess, "run", run)
    _patch_dependency(patch, subprocess, "check_output", check_output)


@pytest.mark.parametrize("fault", ["stdout-text", "stdout-none", "stdout-list"])
def test_invalid_subprocess_normal_returns_are_runtime_errors(box, monkeypatch, fault):
    with _controlled("history", box):
        hits = []
        before = _snapshot(box), _process_state()
        with monkeypatch.context() as patch:
            _malform_subprocess_promises(patch, fault, hits)
            with pytest.raises(RuntimeError) as caught:
                auditor.inspect_history(str(box / "histories/pristine-repo"))
            _need(type(caught.value) is RuntimeError and hits, "malformed-promise-reached")
        _need((_snapshot(box), _process_state()) == before, "malformed-return-nonmutation")


_PURITY_PROGRAM = r'''
import ast, builtins, importlib, importlib.util, io, os, socket, subprocess, sys, types
path = sys.argv[1]
source = open(path, "rb").read()
tree = ast.parse(source, filename=path)
roots = set()
modules = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        roots.update(a.name.split(".")[0] for a in node.names)
        modules.update(a.name for a in node.names)
    elif isinstance(node, ast.ImportFrom):
        assert node.level == 0 and node.module, "relative import forbidden"
        roots.add(node.module.split(".")[0])
        modules.add(node.module)
assert roots <= sys.stdlib_module_names, "nonstdlib dependency"
for name in sorted(modules):
    importlib.import_module(name)
module = types.ModuleType("release_audit")
module.__file__ = path
module.__spec__ = importlib.util.spec_from_file_location("release_audit", path)
sys.modules[module.__name__] = module
code = compile(source, path, "exec")
before = os.getcwd(), dict(os.environ), sys.getrecursionlimit(), sys.get_int_max_str_digits()
def forbidden(*a, **k):
    raise AssertionError("import activity forbidden")
original_import = builtins.__import__
def checked_import(name, *args, **kwargs):
    assert name.split(".")[0] in sys.stdlib_module_names, "nonstdlib import"
    return original_import(name, *args, **kwargs)
builtins.__import__ = checked_import
for obj, names in ((builtins, ("open",)), (io, ("open",)),
                   (os, ("open", "listdir", "scandir", "chdir", "putenv", "unsetenv")),
                   (socket, ("socket", "create_connection")),
                   (subprocess, ("Popen", "run", "call", "check_call", "check_output")),
                   (sys, ("setrecursionlimit", "set_int_max_str_digits"))):
    for name in names:
        setattr(obj, name, forbidden)
os._Environ.__setitem__ = forbidden
os._Environ.__delitem__ = forbidden
exec(code, module.__dict__)
assert before == (os.getcwd(), dict(os.environ), sys.getrecursionlimit(),
                  sys.get_int_max_str_digits())
print("IMPORT_PURITY_OK")
'''


def test_fresh_process_import_has_no_io_commands_or_nonstdlib_imports(box):
    source = Path(auditor.__file__).resolve()
    before = _snapshot(box), _process_state()
    completed = subprocess.run(
        [sys.executable, "-I", "-B", "-c", _PURITY_PROGRAM, str(source)],
        cwd=box, capture_output=True, check=False,
    )
    _need(completed.returncode == 0, "fresh-import-purity-exit")
    _need(completed.stdout == b"IMPORT_PURITY_OK\n" and completed.stderr == b"",
          "fresh-import-purity-observation")
    _need((_snapshot(box), _process_state()) == before, "fresh-import-parent-conserved")


def test_provenance_pattern_storage_remains_encoded():
    raw = Path(auditor.__file__).read_bytes()
    rule = next(r for r in _reference("SCAN_RULES.json")["rules"] if r["id"] == "PROVENANCE001")
    _need(rule["pattern_hex"].encode() in raw, "registered-encoded-expression-present")
    expression = bytes.fromhex(rule["pattern_hex"])
    _need(re.search(expression, raw) is None, "no-decoded-provenance-expression")
    _need(bytes.fromhex("617373697374616e74") not in raw.lower(), "no-generic-prohibited-text")


def _derive_tree_record(relative, subject):
    """Reconstruct a fixed finite fixture, using no production inventory."""
    prefix = relative + "/"
    payloads = {name[len(prefix):]: raw for name, raw in _bank().items()
                if name.startswith(prefix)}
    directories = {"."}
    for name in payloads:
        parts = name.split("/")
        directories.update("/".join(parts[:i]) for i in range(1, len(parts)))
    rows = []
    for name in sorted(directories | set(payloads)):
        raw = payloads.get(name)
        rows.append({"path": name, "object_type": "directory" if raw is None else "regular",
                     "mode": "040755" if raw is None else "100644",
                     "bytes": None if raw is None else len(raw),
                     "sha256": None if raw is None else _digest(raw),
                     "git_oid": None, "target": None, "source": "tree"})
    findings = [finding for name, raw in payloads.items()
                for finding in _content_findings(name, raw)]
    findings.sort(key=lambda r: (r["rule"], r["location"], r["identity"], r["summary"]))
    return {
        "format": "exactfrac-release-inspection/1", "kind": "tree",
        "subject": {"input_path": str(subject), "resolved_path": str(subject),
                    "subject_type": "directory", "bytes": None, "sha256": None,
                    "git_head": None, "refs_sha256": None,
                    "inventory_sha256": _digest(_jsonl(rows))},
        "coverage": "complete", "outcome": "findings" if findings else "no-findings",
        "limits": _reference("LIMITS.json")["defaults"], "inventory": rows,
        "findings": findings, "gaps": [],
        "summary": {"inventory_count": len(rows), "finding_count": len(findings), "gap_count": 0,
                    "inspected_bytes": sum(map(len, payloads.values())),
                    "regular_files": len(payloads),
                    "directories": len(directories), "links": 0, "special_files": 0,
                    "archive_depth": 0, "history_refs": 0, "history_objects": 0},
    }


@pytest.mark.parametrize("relative,label", [
    ("trees/pristine", "TREE_PRISTINE_RECORD.json"),
    ("trees/findings", "TREE_FINDINGS_RECORD.json"),
])
def test_tree_records_reconstructed_from_raw_fixture_bytes(box, relative, label):
    with _controlled("tree", box):
        path = box / relative
        expected = _derive_tree_record(relative, path)
        _same_record(expected, _expected(label, path))
        _same_record(_inspect("tree", path, box), expected)


@pytest.mark.parametrize("fault,guard", [
    ("extra", "record-keys"), ("missing", "record-keys"),
    ("format", "record-format"), ("kind", "record-kind"),
    ("bool-count", "summary-exact-integer"), ("subject", "subject-binding"),
    ("false-pass", "record-outcome"), ("false-clean", "record-outcome"),
    ("omitted-gap", "incomplete-without-gap"), ("unsorted", "inventory-order-uniqueness"),
    ("duplicate", "inventory-order-uniqueness"), ("secret-echo", "finding-redaction"),
])
def test_independent_record_reader_rejects_schema_and_accounting_faults(fault, guard):
    path = Path("/synthetic-record-root")
    pristine = _expected("TREE_FINDINGS_RECORD.json", path)
    _check_record(pristine, "tree", path)
    altered = copy.deepcopy(pristine)
    if fault == "extra":
        altered["release_authorized"] = True
    elif fault == "missing":
        del altered["coverage"]
    elif fault == "format":
        altered["format"] = "unknown/1"
    elif fault == "kind":
        altered["kind"] = "archive"
    elif fault == "bool-count":
        altered["summary"]["history_refs"] = False
    elif fault == "subject":
        altered["subject"]["input_path"] = "/different-subject"
    elif fault == "false-pass":
        altered["outcome"] = "PASS"
    elif fault == "false-clean":
        altered["outcome"] = "no-findings"
    elif fault == "omitted-gap":
        altered["coverage"] = altered["outcome"] = "incomplete"
    elif fault == "unsorted":
        altered["inventory"].reverse()
    elif fault == "duplicate":
        altered["inventory"].append(copy.deepcopy(altered["inventory"][-1]))
    else:
        altered["findings"][-1]["summary"] += " forbidden matched content"
    with pytest.raises(AssertionError, match="^" + guard + "$"):
        _check_record(altered, "tree", path)
    _check_record(pristine, "tree", path)


@pytest.mark.parametrize("fault", ["dropped-finding", "dropped-object", "invented-identity"])
def test_coherently_rehashed_false_records_fail_independent_ground_truth(fault):
    path = Path("/synthetic-record-root")
    original = _derive_tree_record("trees/findings", path)
    _check_record(original, "tree", path)
    changed = copy.deepcopy(original)
    if fault == "dropped-finding":
        changed["findings"].pop()
        changed["summary"]["finding_count"] -= 1
    elif fault == "dropped-object":
        row = changed["inventory"].pop()
        changed["findings"] = [r for r in changed["findings"] if r["identity"] != row["sha256"]]
        changed["subject"]["inventory_sha256"] = _digest(_jsonl(changed["inventory"]))
        changed["summary"]["inventory_count"] -= 1
        changed["summary"]["regular_files"] -= 1
        changed["summary"]["inspected_bytes"] -= row["bytes"]
        changed["summary"]["finding_count"] = len(changed["findings"])
    else:
        changed["inventory"][-1]["sha256"] = "a" * 64
        changed["subject"]["inventory_sha256"] = _digest(_jsonl(changed["inventory"]))
    # Prove this reaches the semantic comparison, not an earlier stale-hash guard.
    _check_record(changed, "tree", path)
    with pytest.raises(AssertionError, match=r"^independent-exact-record$"):
        _same_record(changed, original)
    _same_record(_derive_tree_record("trees/findings", path), original)


def test_strict_reference_json_rejects_duplicate_decoded_keys_and_nonfinite_tokens():
    for raw in (b'{"a":1,"a":2}', b'{"a":1,"\\u0061":2}'):
        with pytest.raises(AssertionError, match=r"^duplicate-json-key$"):
            _json(raw)
    for value in (b"NaN", b"Infinity", b"-Infinity"):
        with pytest.raises(AssertionError, match=r"^nonfinite-json-token$"):
            _json(b'{"a":' + value + b"}")
    _need(_json(b'{"a":1}') == {"a": 1}, "pristine-json-after-negative")


def _reconstructed_cli_preimage():
    metadata = _reference("METADATA_IDENTITIES.json")
    result = bytearray(_refs()["tests/test_cli.py"])
    for row in metadata["test_cli_static_pin_intervals"]:
        _need(bytes(result[row["start"]:row["end"]]) == row["postimage"].encode(), "new-static-pin")
        result[row["start"]:row["end"]] = row["preimage"].encode()
    old = bytes(result)
    _need(_identity(old) == metadata["preimages"]["tests/test_cli.py"], "reconstructed-old-cli")
    return old


def _static_pins(source):
    module = ast.parse(source)
    found = [node for node in module.body if isinstance(node, ast.Assign)
             and any(isinstance(target, ast.Name) and target.id == "_FROZEN_SOURCE_HASHES"
                     for target in node.targets)]
    _need(len(found) == 1, "one-static-pin-dictionary")
    try:
        value = ast.literal_eval(found[0].value)
    except (ValueError, TypeError) as exc:
        raise AssertionError("literal-static-pin-dictionary") from exc
    _need(type(value) is dict and len(value) == 41, "forty-one-static-pins")
    return value


def _check_pin_transition(old, new, metadata_files):
    metadata = _reference("METADATA_IDENTITIES.json")
    _need(_identity(old) == metadata["preimages"]["tests/test_cli.py"], "old-cli-identity")
    _need(len(new) == len(old) == 99_824, "cli-byte-length")
    cursor = 0
    for row in metadata["test_cli_static_pin_intervals"]:
        start, end = row["start"], row["end"]
        _need(new[cursor:start] == old[cursor:start], "cli-outside-three-slices")
        _need(new[start:end] == row["postimage"].encode(), "fixed-candidate-pin")
        _need(_identity(metadata_files[row["path"]]) == metadata["candidates"][row["path"]],
              "frozen-metadata-identity")
        _need(_digest(metadata_files[row["path"]]).encode() == new[start:end],
              "metadata-pin-coupling")
        cursor = end
    _need(new[cursor:] == old[cursor:], "cli-outside-three-slices")
    before, after = _static_pins(old), _static_pins(new)
    _need(before.keys() == after.keys(), "pin-key-conservation")
    changed = {row["path"] for row in metadata["test_cli_static_pin_intervals"]}
    _need(all(before[key] == after[key] for key in before if key not in changed), "other-38-pins")
    _need(_identity(new) == metadata["candidates"]["tests/test_cli.py"], "new-cli-identity")


def test_frozen_metadata_pin_transition_and_pyproject_single_literal():
    import tomllib

    refs = _refs()
    files = {name: refs[name] for name in ("README.md", "CITATION.cff", "pyproject.toml")}
    _check_pin_transition(_reconstructed_cli_preimage(), refs["tests/test_cli.py"], files)
    new = refs["pyproject.toml"]
    _need(new.count(b'version = "0.1.0"') == 1, "unique-new-version")
    old = new.replace(b'version = "0.1.0"', b'version = "0.1.0.dev0"', 1)
    _need(_identity(old) == _reference("METADATA_IDENTITIES.json")["preimages"]["pyproject.toml"],
          "pyproject-unique-byte-change")
    parsed_old, parsed_new = tomllib.loads(old.decode()), tomllib.loads(new.decode())
    parsed_old["project"]["version"] = "0.1.0"
    _need(parsed_old == parsed_new, "all-other-toml-values-conserved")


@pytest.mark.parametrize("fault", ["wrong-pin", "changed-assertion", "changed-quote",
                                    "removed-key", "dynamic-value", "extra-byte",
                                    "reordered-line", "extra-substitution",
                                    "wrong-readme", "old-metadata-new-pin"])
def test_metadata_and_static_pin_mismatches_cannot_be_accepted(fault):
    refs = _refs()
    old = _reconstructed_cli_preimage()
    new = refs["tests/test_cli.py"]
    metadata = {name: refs[name] for name in ("README.md", "CITATION.cff", "pyproject.toml")}
    _check_pin_transition(old, new, metadata)
    altered = new
    if fault == "wrong-pin":
        altered = new[:31_512] + b"0" * 64 + new[31_576:]
    elif fault == "changed-assertion":
        _need(b"assert " in new, "assertion-mutation-site")
        altered = new.replace(b"assert ", b"assert not ", 1)
    elif fault == "changed-quote":
        altered = new[:31_511] + b'"' + new[31_512:]
    elif fault == "removed-key":
        altered = new.replace(b"'CITATION.cff'", b"'RENAMED.cff'", 1)
    elif fault == "dynamic-value":
        altered = new[:31_512] + b"x" * 64 + new[31_576:]
    elif fault == "extra-byte":
        altered = new + b"\n"
    elif fault == "reordered-line":
        lines = new.splitlines(keepends=True)
        index = next(i for i, line in enumerate(lines)
                     if line.startswith(b"    'exactfrac/__init__.py': "))
        _need(lines[index + 1].startswith(b"    'exactfrac/_telemetry.py': "),
              "reordered-line-mutation-site")
        lines[index], lines[index + 1] = lines[index + 1], lines[index]
        altered = b"".join(lines)
        _need(_static_pins(altered) == _static_pins(new), "reordered-line-values-conserved")
    elif fault == "extra-substitution":
        value = _static_pins(new)[".gitignore"].encode()
        site = b"    '.gitignore': '" + value + b"'"
        _need(new.count(site) == 1 and value != b"0" * 64, "extra-substitution-mutation-site")
        altered = new.replace(site, b"    '.gitignore': '" + b"0" * 64 + b"'", 1)
    elif fault == "wrong-readme":
        metadata["README.md"] += b"\n"
    else:
        metadata["pyproject.toml"] = metadata["pyproject.toml"].replace(
            b'version = "0.1.0"', b'version = "0.1.0.dev0"', 1,
        )
    with pytest.raises(AssertionError):
        _check_pin_transition(old, altered, metadata)
    clean = {name: refs[name] for name in ("README.md", "CITATION.cff", "pyproject.toml")}
    _check_pin_transition(old, new, clean)


def test_installed_release_metadata_is_the_coupled_frozen_postimage():
    """Executed only after owner import succeeds in E; never installs a file."""
    refs = _refs()
    for name in ("README.md", "CITATION.cff", "LICENSE", "MANIFEST.in",
                 "pyproject.toml", "tests/test_cli.py"):
        _need((_ROOT / name).read_bytes() == refs[name], "live-reviewed-metadata:" + name)
    _check_pin_transition(
        _reconstructed_cli_preimage(), (_ROOT / "tests/test_cli.py").read_bytes(),
        {name: (_ROOT / name).read_bytes()
         for name in ("README.md", "CITATION.cff", "pyproject.toml")},
    )


def _check_source_profile(members, source):
    profile = _reference("SDIST_PROFILE.json")
    root = profile["root"]
    _need(all(name.startswith(root) for name in members), "sdist-single-root")
    relative = {name[len(root):]: raw for name, raw in members.items()}
    for name in relative:
        _safe_parts(name)
        _need(not set(name.split("/")) & set(profile["prohibited_paths_or_segments"]),
              "sdist-prohibited-segment")
        _need(not any(name.endswith(suffix) for suffix in profile["prohibited_suffixes"]),
              "sdist-prohibited-suffix")
    required = {name for name in source if name in profile["required_singletons"]
                or any(name.startswith(prefix) for prefix in profile["required_recursive_roots"])}
    required |= set(profile["required_singletons"])
    _need(required <= set(relative), "sdist-required-membership")
    _need(set(relative) <= required | set(profile["allowed_generated_packaging_metadata"]),
          "sdist-extra-member")
    _need(all(relative[name] == source[name] for name in required), "sdist-source-byte-binding")


def _check_wheel_profile(members, source):
    profile = _reference("WHEEL_PROFILE.json")
    for name in members:
        _safe_parts(name)
        _need(name not in profile["prohibited_names"] and not any(
            name.startswith(prefix) for prefix in profile["prohibited_prefixes"]
        ), "wheel-prohibited-member")
    package_source = {name: raw for name, raw in source.items()
                      if any(name.startswith(package + "/")
                             for package in profile["runtime_packages_only"])}
    metadata = {p for p in profile["required_patterns"] if "*" not in p
                and ".dist-info/" in p}
    _need(set(members) == set(package_source) | metadata, "wheel-exact-membership")
    _need(all(members[name] == raw for name, raw in package_source.items()), "wheel-source-bytes")
    license_path = next(name for name in metadata if name.endswith("/licenses/LICENSE"))
    _need(members[license_path] == _refs()["LICENSE"], "wheel-license-bytes")
    text = members["exactfrac-0.1.0.dist-info/METADATA"]
    _need(b"Name: exactfrac\n" in text and b"Version: 0.1.0\n" in text, "wheel-version-metadata")


def _profile_specimen(kind):
    """In-memory membership specimen only: no build, stub module or wheel exists."""
    source = {name: b"finite membership specimen\n"
              for name in _reference("SDIST_PROFILE.json")["required_singletons"]}
    source |= {"exactfrac/__init__.py": b"", "exactfrac_verify/__init__.py": b"",
               "tests/retained.py": b"finite test member\n",
               "docs/retained.md": b"finite document\n",
               "instances/retained.json": b"{}\n", "results/retained.json": b"{}\n",
               "experiments/retained.py": b"finite source member\n"}
    if kind == "source":
        root = _reference("SDIST_PROFILE.json")["root"]
        members = {root + name: raw for name, raw in source.items()}
    else:
        profile = _reference("WHEEL_PROFILE.json")
        members = {name: source[name]
                   for name in ("exactfrac/__init__.py", "exactfrac_verify/__init__.py")}
        members |= {name: b"finite distribution metadata\n" for name in profile["required_patterns"]
                    if ".dist-info/" in name}
        members["exactfrac-0.1.0.dist-info/licenses/LICENSE"] = _refs()["LICENSE"]
        members["exactfrac-0.1.0.dist-info/METADATA"] = b"Name: exactfrac\nVersion: 0.1.0\n"
    return members, source


@pytest.mark.parametrize("kind", ["source", "wheel"])
@pytest.mark.parametrize("fault", ["missing", "extra", "private", "changed-bytes"])
def test_independent_distribution_profile_checker_rejects_false_inventory(kind, fault):
    checker = _check_source_profile if kind == "source" else _check_wheel_profile
    members, source = _profile_specimen(kind)
    checker(members, source)
    changed = dict(members)
    prefix = _reference("SDIST_PROFILE.json")["root"] if kind == "source" else ""
    if fault == "missing":
        del changed[prefix + "exactfrac/__init__.py"]
    elif fault == "extra":
        changed[prefix + "unexpected.txt"] = b"unexpected\n"
    elif fault == "private":
        changed[prefix + ".git/config"] = b"not-distribution-content\n"
    else:
        changed[prefix + "exactfrac/__init__.py"] = b"changed\n"
    with pytest.raises(AssertionError):
        checker(changed, source)
    checker(members, source)


def _check_installed_origins(environment, checkout, origins):
    base, excluded = Path(environment).resolve(), Path(checkout).resolve()
    _need(base != excluded and not base.is_relative_to(excluded), "environment-outside-checkout")
    _need(set(origins) == {"exactfrac", "exactfrac_verify"}, "two-installed-package-origins")
    for origin in origins.values():
        path = Path(origin).resolve()
        _need(path.is_relative_to(base) and not path.is_relative_to(excluded), "installed-origin")


@pytest.mark.parametrize("fault", ["checkout", "editable", "foreign", "missing-package"])
def test_installed_origin_checker_rejects_shadowing_and_foreign_packages(tmp_path, fault):
    root = tmp_path.resolve()
    environment, checkout = root / "clean-environment", root / "checkout"
    origins = {name: str(environment / "site-packages" / name / "__init__.py")
               for name in ("exactfrac", "exactfrac_verify")}
    _check_installed_origins(environment, checkout, origins)
    changed = dict(origins)
    if fault in ("checkout", "editable"):
        changed["exactfrac"] = str(checkout / "exactfrac/__init__.py")
    elif fault == "foreign":
        changed["exactfrac_verify"] = str(root / "other-install/exactfrac_verify/__init__.py")
    else:
        del changed["exactfrac_verify"]
    with pytest.raises(AssertionError):
        _check_installed_origins(environment, checkout, changed)
    _check_installed_origins(environment, checkout, origins)


def test_fixed_smoke_reference_bytes_are_not_an_installation_verdict():
    smoke = _reference("WHEEL_SMOKE.json")
    _need(len(smoke["cases"]) == 2, "two-registered-tiny-smokes")
    for case in smoke["cases"]:
        instance = _json(case["instance_utf8"].encode())
        _need(instance["format"] == "exactfrac-instance/1", "smoke-instance-format")
        for route in ("standard", "accelerated"):
            raw = case["expected_" + route + "_certificate_utf8"].encode()
            _need(raw.endswith(b"\n") and raw.count(b"\n") == 1, "smoke-canonical-certificate-line")
            certificate = _json(raw)
            _need(certificate["format"] == "exactfrac-certificate/1", "smoke-certificate-format")
            _need(type(certificate["N"]) is int and type(certificate["D"]) is int
                  and certificate["D"] > 0, "smoke-exact-raw-pair")
        _need(case["verify_stdout_utf8"] == "", "smoke-silent-verifier")


def test_review_references_and_report_template_do_not_claim_future_execution():
    refs = _refs()
    schema = _reference("RELEASE_REPORT_SCHEMA.json")
    template = refs["docs/RELEASE.md.template"].decode()
    _need(schema["placeholder_prefix"] in template, "template-still-observation-bound")
    for section in schema["required_sections"]:
        _need(section in template, "required-release-report-section")
    claims = _reference("README_CLAIM_CROSSWALK.json")
    _need(claims["readme_sha256"] == _digest(refs["README.md"]), "claim-crosswalk-readme-binding")
    _need(len(claims["claims"]) > 0, "claim-review-roster")
    _need(_reference("SOURCE_STATUS_CROSSWALK.json")["format"].startswith("exactfrac-"),
          "source-review-reference")
    _need(_reference("GITHUB_DELIMITER_INVENTORY.json")["format"].startswith("exactfrac-"),
          "render-inventory-reference")
    _need(_reference("GITHUB_MATH_RENDER_REFERENCE.json")["selected_inline"] == "$...$",
          "selected-inline-form")
    render = _reference("README_GITHUB_RENDER_RECORD_TEMPLATE.json")
    _need(_digest(refs["README.md"]) in refs["README_GITHUB_RENDER_RECORD_TEMPLATE.json"].decode(),
          "preview-template-byte-binding")
    _need(type(render) is dict, "preview-template-record")
    _need(b"\\(" not in refs["README.md"] and b"\\[" not in refs["README.md"],
          "readme-math-delimiters")


def test_disposition_example_binds_encoded_runtime_case_not_removed_fixture():
    rows = _json(_bank()["expected/DISPOSITIONS_EXAMPLE.json"])["records"]
    policy = _reference("SCAN_RULES.json")["disposition_policy"]
    _need(policy["automatic_suppression"] is False
          and policy["unresolved_blocks_readiness"] is True,
          "manual-disposition-only")
    for row in rows:
        _keys(row, policy["manual_record_fields"], "disposition-fields")
        _need(row["decision"] in policy["allowed_decisions"], "registered-disposition")
        _optional_hash(row["identity"], 64, "disposition-content-identity")
    row = next(r for r in rows if r["rule"] == "PROVENANCE001")
    spec = next(r for r in _reference("TREE_RUNTIME_FIXTURE_SPEC.json")["cases"]
                if r["id"] == "provenance-positive-runtime")
    _need(row["location"] == spec["relative_path"] and row["identity"] == spec["expected_sha256"],
          "runtime-disposition-binding")
    _need(row["decision"] == "retain-truthful-provenance", "truthful-runtime-disposition")
    _need("runtime-only" in row["rationale"], "example-not-actual-release-disposition")


def test_path_resource_limit_cannot_silently_omit_an_entry(box, monkeypatch):
    with _controlled("tree", box):
        root = box / "path-limit"
        root.mkdir(mode=0o755)
        _put(root, "name-exceeding-one-byte", b"safe\n")
        with monkeypatch.context() as patch:
            limits = _limits(patch, {"max_path_utf8_bytes": 1})
            _incomplete(_inspect("tree", root, box, limits))


def test_static_pin_dictionary_rejects_an_actually_computed_value():
    raw = _refs()["tests/test_cli.py"]
    _static_pins(raw)
    tree = ast.parse(raw)
    assignment = next(node for node in tree.body if isinstance(node, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "_FROZEN_SOURCE_HASHES"
                              for t in node.targets))
    assignment.value.values[0] = ast.Call(
        func=ast.Name(id="str", ctx=ast.Load()), args=[ast.Constant(value="computed")], keywords=[],
    )
    changed = ast.unparse(ast.fix_missing_locations(tree))
    with pytest.raises(AssertionError, match=r"^literal-static-pin-dictionary$"):
        _static_pins(changed)
    _static_pins(raw)


@pytest.mark.parametrize("kind", ["tree", "archive", "history"])
def test_no_filesystem_write_network_or_execution_during_inspection(box, monkeypatch, kind):
    import builtins

    path = box / {"tree": "trees/pristine", "archive": "archives/pristine.zip",
                  "history": "histories/pristine-repo"}[kind]
    with _controlled(kind, box):
        before = _snapshot(box), _process_state()
        attempts = []
        open_functions = (builtins.open, io.open, os.open)

        def forbidden(*_args, **_kwargs):
            attempts.append("forbidden-side-effect")
            raise AssertionError("inspector-side-effect")

        def read_open(original):
            def checked(file, mode="r", *args, **kwargs):
                _need(type(mode) is str and not any(c in mode for c in "wax+"), "read-only-open")
                return original(file, mode, *args, **kwargs)
            return checked

        def read_descriptor(file, flags, *args, **kwargs):
            prohibited = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
            allowed_null = kind == "history" and os.fspath(file) == os.devnull
            _need(not flags & prohibited or allowed_null, "read-only-descriptor")
            return open_functions[2](file, flags, *args, **kwargs)

        with monkeypatch.context() as patch:
            _patch_dependency(patch, builtins, "open", read_open(open_functions[0]))
            _patch_dependency(patch, io, "open", read_open(open_functions[1]))
            _patch_dependency(patch, os, "open", read_descriptor)
            for name in ("mkdir", "rmdir", "remove", "unlink", "rename", "replace", "chmod",
                         "link", "symlink", "truncate", "chdir", "putenv", "unsetenv"):
                _patch_dependency(patch, os, name, forbidden)
            _patch_dependency(patch, socket, "socket", forbidden)
            _patch_dependency(patch, socket, "create_connection", forbidden)
            if kind != "history":
                _patch_dependency(patch, subprocess, "Popen", forbidden)
            result = getattr(auditor, "inspect_" + kind)(str(path))
        _check_record(result, kind, path)
        _need(not attempts and (_snapshot(box), _process_state()) == before,
              "no-observed-inspection-side-effects")


def test_history_path_punctuation_is_one_argv_operand(box, monkeypatch):
    import shutil

    with _controlled("history", box):
        path = box / "repository with space; literal"
        shutil.copytree(box / "histories/pristine-repo", path)
        calls = []
        with monkeypatch.context() as patch:
            _guard_history_processes(patch, path, calls)
            result = _inspect("history", path, box)
        _same_record(result, _expected("HISTORY_PRISTINE_RECORD.json", path))
        _need(bool(calls) and all(command[2] == str(path) for command in calls),
              "literal-path-operand")


def test_registered_three_level_archive_is_within_default_depth(box):
    with _controlled("archive", box):
        result = _inspect("archive", box / "archives/nested-depth-3.zip", box)
        _need(result["coverage"] == "complete" and result["summary"]["archive_depth"] == 3,
              "default-depth-three-complete")


def test_reviewable_copyright_is_reported_and_not_silently_removed(box):
    with _controlled("tree", box):
        raw = _bank()["trees/reviewable/LICENSE.txt"]
        result = _inspect("tree", box / "trees/reviewable", box)
        _need(result["coverage"] == "complete", "reviewable-content-complete")
        _need(result["findings"] == _content_findings("LICENSE.txt", raw),
              "no-automatic-suppression")
        _need(any(row["rule"] == "IDENTITY001" for row in result["findings"]),
              "copyright-review-hit")


@pytest.mark.parametrize("kind", ["tree", "archive", "history"])
def test_finding_limit_prevents_clean_status_for_each_interface(box, monkeypatch, kind):
    with _controlled(kind, box):
        if kind == "tree":
            path = box / "trees/findings"
        elif kind == "history":
            path = box / "histories/historical-sensitive-repo"
        else:
            path = _put(box, "multiple-findings.zip", _make_zip([
                ("contact.txt", _bank()["trees/findings/contact.txt"]),
                ("token.txt", _bank()["trees/findings/token.txt"]),
            ]))
        with monkeypatch.context() as patch:
            limits = _limits(patch, {"max_findings": 1})
            _incomplete(_inspect(kind, path, box, limits))


@pytest.mark.parametrize("rule,encoded", [
    ("SECRET001", "2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a"),
    ("SECRET003", "414b4941414141414141414141414141414141410a"),
])
def test_remaining_registered_credential_rules_use_runtime_synthetic_values(box, rule, encoded):
    with _controlled("tree", box):
        raw = bytes.fromhex(encoded)
        expected = _content_findings("synthetic-key.txt", raw)
        _need(any(row["rule"] == rule for row in expected), "independent-runtime-rule-positive")
        root = box / "runtime-credential"
        root.mkdir(mode=0o755)
        _put(root, "synthetic-key.txt", raw)
        result = _inspect("tree", root, box)
        _need(result["findings"] == expected, "runtime-credential-rule-identity")
        _need(raw.strip() not in _wire(result), "runtime-credential-redaction")


def test_counted_text_parser_ignores_fences_and_headings_inside_payload(monkeypatch):
    """Parser-only specimen; the real committed registry is never rewritten."""
    payload = b"literal first line\n```\n## Embedded heading\n```python\npass\n"
    marker = (b"<!-- U22-C-CORR2 counted.txt utf8 " + str(len(payload)).encode()
              + b" " + _digest(payload).encode() + b" -->\n```text\n")
    specimen = marker + payload + b"```\n"
    with monkeypatch.context() as patch:
        patch.setattr(sys.modules[__name__], "_OBJECT_PINS", {
            "counted.txt": (len(payload), _digest(payload), "utf8", "text"),
        })
        _need(_extract_objects(specimen) == {"counted.txt": payload}, "counted-inner-fences")
        bad = marker + payload[:-1] + b"```\n"
        with pytest.raises(AssertionError):
            _extract_objects(bad)
        _need(_extract_objects(specimen) == {"counted.txt": payload}, "counted-pristine-restored")
