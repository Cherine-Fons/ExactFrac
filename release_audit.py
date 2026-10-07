"""Read-only, bounded inspection of trees, archives and reachable Git history.

D22-R10--R16 define the inspection contract. Records are observations, not
publication authorization. No inspected code is imported or executed. Default
limits and rule literals are fixed from the independently registered references;
no catalogue, configuration file or user path is read during module import.
"""

from __future__ import annotations

import bz2 as _bz2
import hashlib as _hashlib
import io as _io
import json as _json
import lzma as _lzma
import os as _os
import re as _re
import stat as _stat
import struct as _struct
import subprocess as _subprocess
import tarfile as _tarfile
import threading as _threading
import types as _types
import zipfile as _zipfile
import zlib as _zlib

__all__ = ("inspect_archive", "inspect_history", "inspect_tree")

# A single replaceable immutable mapping, copied at each public invocation.
_DEFAULT_LIMITS = _types.MappingProxyType({'max_archive_depth': 3,
 'max_archive_members': 8192,
 'max_archive_uncompressed_bytes': 536870912,
 'max_compression_ratio_numerator': 1000,
 'max_findings': 100000,
 'max_git_stdout_bytes': 536870912,
 'max_history_objects': 250000,
 'max_history_payload_bytes': 4294967296,
 'max_member_uncompressed_bytes': 67108864,
 'max_path_utf8_bytes': 1024,
 'max_regular_file_bytes': 536870912,
 'max_tree_objects': 100000})

_RULES = (
    (
        'PATH001',
        'review',
        'absolute user-home path candidate',
        ('path', 'content'),
        '(?i)(?:/Users/|/home/|[A-Z]:\\\\Users\\\\)',
        None,
    ),
    (
        'PATH002',
        'review',
        'private research or handoff path candidate',
        ('path', 'content'),
        '(?i)(?:research-private|/handoffs/|\\\\handoffs\\\\)',
        None,
    ),
    (
        'PATH003',
        'block',
        'private build or learning note',
        ('path',),
        '(?i)(?:^|/)(?:BUILD_NOTES|LEARNING_NOTES)(?:\\.[^/]*)?$',
        None,
    ),
    (
        'SECRET001',
        'block',
        'private-key material candidate',
        ('content',),
        '-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        None,
    ),
    (
        'SECRET002',
        'block',
        'GitHub token candidate',
        ('content',),
        '\\bgh[pousr]_[A-Za-z0-9_]{20,}\\b',
        None,
    ),
    (
        'SECRET003',
        'block',
        'AWS access-key candidate',
        ('content',),
        '\\bAKIA[0-9A-Z]{16}\\b',
        None,
    ),
    (
        'CONTACT001',
        'review',
        'email-address candidate',
        ('content', 'history-metadata'),
        '(?i)\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}\\b',
        None,
    ),
    (
        'IDENTITY001',
        'review',
        'author-name occurrence',
        ('content', 'history-metadata'),
        '\\bCherine Fons\\b',
        None,
    ),
    (
        'PROVENANCE001',
        'review',
        'encoded development-provenance occurrence',
        ('content', 'history-metadata'),
        None,
        '283f69295c62283f3a4f70656e41497c436861744750547c416e7468726f7069637c436c617564657c414920617373697374616e747c41492073797374656d295c62',
    ),
    (
        'ARCHIVE001',
        'block',
        'absolute, traversal, NUL, backslash, empty component or duplicate normalized archive name',
        ('archive-name',),
        'structural',
        None,
    ),
    (
        'ARCHIVE002',
        'block',
        'archive link or special member',
        ('archive-member',),
        'structural',
        None,
    ),
    (
        'COVERAGE001',
        'block',
        'unsupported encoding, unsupported object or finite resource ceiling',
        ('decoder', 'resource'),
        'structural',
        None,
    ),
)


def _sha(raw):
    return _hashlib.sha256(raw).hexdigest()


def _wire(value):
    return _json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()


def _jsonl(rows):
    return b"".join(_wire(row) + b"\n" for row in rows)


def _text(raw):
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("invalid UTF-8 in validated Git response") from exc


def _promise(ok, message):
    if not ok:
        raise RuntimeError(message)


def _mode(mode):
    return format(_stat.S_IFMT(mode) | _stat.S_IMODE(mode), "06o")


def _entry(path, kind, mode=None, raw=None, oid=None, target=None, source="tree"):
    return {"path": path, "object_type": kind, "mode": mode,
            "bytes": None if raw is None else len(raw),
            "sha256": None if raw is None else _sha(raw),
            "git_oid": oid, "target": target, "source": source}


def _safe_name(name, directory=False):
    if type(name) is not str or not name or "\0" in name or "\\" in name:
        return False
    if name.startswith("/") or _re.match(r"^[A-Za-z]:", name):
        return False
    bare = name[:-1] if directory and name.endswith("/") else name
    return bool(bare) and all(part not in ("", ".", "..") for part in bare.split("/"))


def _display_name(name):
    """Lossless diagnostic spelling for a name that cannot be emitted as UTF-8."""
    try:
        name.encode("utf-8")
        return name, True
    except UnicodeEncodeError:
        return "bytes:" + _os.fsencode(name).hex(), False


def _validate_path(value, archive=False):
    if type(value) is not str or not value or "\0" in value or not _os.path.isabs(value):
        raise ValueError("expected exact str containing an absolute existing path")
    if value != _os.path.normpath(value) or value.startswith("//"):
        raise ValueError("path must use its canonical absolute spelling")
    current = _os.path.sep
    parts = value.split(_os.path.sep)[1:]
    parts = [part for part in parts if part]
    try:
        root_stat = _os.lstat(current)
        final_stat = root_stat
        for index, part in enumerate(parts):
            current = _os.path.join(current, part)
            final_stat = _os.lstat(current)
            if _stat.S_ISLNK(final_stat.st_mode):
                raise ValueError("symlink in input path")
            if index + 1 < len(parts) and not _stat.S_ISDIR(final_stat.st_mode):
                raise ValueError("input ancestor is not a directory")
    except (FileNotFoundError, NotADirectoryError) as exc:
        raise ValueError("input does not exist in the accepted path domain") from exc
    if archive:
        if not _stat.S_ISREG(final_stat.st_mode) or final_stat.st_mode & 0o111:
            raise ValueError("archive must be a regular nonexecutable file")
    elif not _stat.S_ISDIR(final_stat.st_mode):
        raise ValueError("root must be a real directory")
    return final_stat


class _Ceiling(Exception):
    """Internal bounded-acquisition signal, converted into explicit coverage."""


def _read_regular(path, expected, maximum):
    """Open no final symlink or special stream; verify the inode before reading."""
    if expected.st_size > maximum:
        raise _Ceiling("regular-file-bytes")
    flags = _os.O_RDONLY | getattr(_os, "O_NOFOLLOW", 0) | getattr(_os, "O_NONBLOCK", 0)
    descriptor = _os.open(path, flags)
    with _os.fdopen(descriptor, "rb") as stream:
        actual = _os.fstat(stream.fileno())
        _promise(_stat.S_ISREG(actual.st_mode), "opened object is not regular")
        _promise((actual.st_dev, actual.st_ino) == (expected.st_dev, expected.st_ino),
                 "file identity changed before read")
        raw = stream.read(maximum + 1)
        _promise(type(raw) is bytes, "file reader did not return bytes")
        if len(raw) > maximum:
            raise _Ceiling("regular-file-bytes")
        after = _os.fstat(stream.fileno())
        _promise((actual.st_size, actual.st_mtime_ns, actual.st_ctime_ns)
                 == (after.st_size, after.st_mtime_ns, after.st_ctime_ns)
                 and len(raw) == after.st_size, "file changed during inspection")
    return raw


class _Inspection:
    def __init__(self, kind, path, subject_type):
        self.kind = kind
        self.limits = dict(_DEFAULT_LIMITS)
        _promise(all(type(v) is int and v >= 0 for v in self.limits.values()),
                 "invalid private limit mapping")
        self.subject = {"input_path": path, "resolved_path": path,
                        "subject_type": subject_type, "bytes": None, "sha256": None,
                        "git_head": None, "refs_sha256": None, "inventory_sha256": None}
        self.rows = []
        self.row_keys = set()
        self.findings = {}
        self.gaps = {}
        self.depth = 0
        self.archive_members = 0
        self.archive_bytes = 0
        self.rules = {row[0]: row for row in _RULES}
        self.patterns = []
        for rule, severity, summary, targets, pattern, pattern_hex in _RULES:
            if pattern == "structural":
                continue
            if pattern_hex is not None:
                pattern = bytes.fromhex(pattern_hex).decode("ascii")
            compiled = _re.compile(pattern.encode("ascii"))
            self.patterns.append((rule, severity, summary, targets, compiled))

    def gap(self, code, location, identity, summary):
        key = code, location, identity or "", summary
        self.gaps[key] = {"code": code, "location": location,
                          "identity": identity, "summary": summary}

    def finding(self, rule, location, identity):
        _, severity, summary, _, _, _ = self.rules[rule]
        key = rule, location, identity, summary
        if key in self.findings:
            return
        if len(self.findings) >= self.limits["max_findings"]:
            self.gap("finding-limit", location, identity, "finding ceiling exceeded")
            return
        self.findings[key] = {"rule": rule, "severity": severity, "location": location,
                              "identity": identity, "summary": summary}

    def problem(self, code, location, identity=None, summary="inspection coverage incomplete",
                rule="COVERAGE001"):
        self.gap(code, location, identity, summary)
        self.finding(rule, location, identity or _sha(location.encode("utf-8")))

    def add(self, row):
        key = row["path"].encode("utf-8"), row["object_type"], row["git_oid"] or ""
        if key in self.row_keys:
            self.problem("duplicate-inventory-entry", row["path"], row["sha256"])
            return False
        self.row_keys.add(key)
        self.rows.append(row)
        return True

    def scan(self, location, raw, target="content", path_text=None):
        identity = _sha(raw)
        path_bytes = (location if path_text is None else path_text).encode("utf-8")
        for rule, _severity, _summary, targets, pattern in self.patterns:
            content_target = (target in targets or
                              (target == "history-metadata" and "content" in targets))
            if (content_target and pattern.search(raw)) or (
                    "path" in targets and pattern.search(path_bytes)):
                self.finding(rule, location, identity)

    def finish(self):
        inventory = sorted(self.rows, key=lambda r: (
            r["path"].encode("utf-8"), r["object_type"], r["git_oid"] or ""))
        findings = [self.findings[key] for key in sorted(self.findings)]
        gaps = [self.gaps[key] for key in sorted(self.gaps)]
        self.subject["inventory_sha256"] = _sha(_jsonl(inventory))
        types = [r["object_type"] for r in inventory]
        regular = sum(t in ("regular", "git-blob") for t in types)
        directories = sum(t in ("directory", "git-tree") for t in types)
        links = sum(t in ("symlink", "hardlink") for t in types)
        special = sum(t not in ("regular", "git-blob", "directory", "git-tree",
                               "symlink", "hardlink", "git-ref") for t in types)
        summary = {"inventory_count": len(inventory), "finding_count": len(findings),
                   "gap_count": len(gaps),
                   "inspected_bytes": sum(r["bytes"] or 0 for r in inventory),
                   "regular_files": regular, "directories": directories, "links": links,
                   "special_files": special, "archive_depth": self.depth,
                   "history_refs": types.count("git-ref"),
                   "history_objects": sum(t.startswith("git-") and t != "git-ref" for t in types)}
        return {"format": "exactfrac-release-inspection/1", "kind": self.kind,
                "subject": self.subject, "coverage": "incomplete" if gaps else "complete",
                "outcome": "incomplete" if gaps else ("findings" if findings else "no-findings"),
                "limits": dict(self.limits), "inventory": inventory, "findings": findings,
                "gaps": gaps, "summary": summary}


def _archive_kind(name, raw):
    lower = name.lower()
    if (raw.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"))
            or lower.endswith((".zip", ".whl"))):
        return "zip"
    if (lower.endswith((".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tar.xz", ".txz"))
            or raw.startswith((b"\x1f\x8b", b"BZh", b"\xfd7zXZ\x00"))
            or (len(raw) >= 262 and raw[257:262] == b"ustar")):
        return "tar"
    return None


def _tree(state, root):
    pending = [(root, ".")]
    visited = set()
    count = 0
    while pending:
        path, relative = pending.pop()
        count += 1
        if count > state.limits["max_tree_objects"]:
            state.problem("tree-object-limit", relative)
            break
        shown, utf8 = _display_name(relative)
        if not utf8:
            state.add(_entry(shown, "unsupported"))
            state.problem("non-utf8-path", shown)
            continue
        if len(relative.encode("utf-8")) > state.limits["max_path_utf8_bytes"]:
            state.problem("path-byte-limit", shown)
            continue
        info = _os.lstat(path)
        mode = info.st_mode
        if _stat.S_ISDIR(mode):
            key = info.st_dev, info.st_ino
            state.add(_entry(shown, "directory", _mode(mode)))
            if key in visited:
                state.problem("directory-cycle", shown)
                continue
            visited.add(key)
            flags = _os.O_RDONLY | getattr(_os, "O_DIRECTORY", 0) | getattr(_os, "O_NOFOLLOW", 0)
            descriptor = _os.open(path, flags)
            try:
                opened = _os.fstat(descriptor)
                _promise((opened.st_dev, opened.st_ino) == key, "directory changed before read")
                available = state.limits["max_tree_objects"] - count - len(pending)
                children = []
                with _os.scandir(descriptor) as entries:
                    for entry in entries:
                        if len(children) >= available:
                            children.clear()
                            state.problem("tree-object-limit", shown)
                            break
                        children.append(entry.name)
            except PermissionError:
                state.problem("unreadable-directory", shown)
                continue
            finally:
                _os.close(descriptor)
            children.sort(key=_os.fsencode, reverse=True)
            for name in children:
                child = name if relative == "." else relative + "/" + name
                pending.append((_os.path.join(path, name), child))
        elif _stat.S_ISREG(mode):
            try:
                raw = _read_regular(path, info, state.limits["max_regular_file_bytes"])
            except PermissionError:
                state.add(_entry(shown, "regular", _mode(mode)))
                state.problem("unreadable-file", shown)
                continue
            except _Ceiling:
                state.add(_entry(shown, "regular", _mode(mode)))
                state.problem("regular-file-byte-limit", shown)
                continue
            state.add(_entry(shown, "regular", _mode(mode), raw))
            kind = _archive_kind(shown, raw)
            state.scan(shown, raw, target="content" if kind is None else None)
            if kind is not None:
                _archive(state, raw, kind, shown + "!", 1)
        elif _stat.S_ISLNK(mode):
            target = _os.readlink(path)
            text, valid = _display_name(target)
            raw = target.encode("utf-8") if valid else _os.fsencode(target)
            state.add(_entry(shown, "symlink", _mode(mode), raw, target=text))
            state.problem("unsupported-link", shown, _sha(raw))
        else:
            state.add(_entry(shown, "special", _mode(mode)))
            state.problem("unsupported-object", shown)


def inspect_tree(root: str) -> dict[str, object]:
    """Inspect an existing real directory without following link entries."""
    _validate_path(root)
    state = _Inspection("tree", root, "directory")
    _tree(state, root)
    return state.finish()


def _member_name(state, name, directory, prefix, seen):
    shown, valid_utf8 = _display_name(name)
    location = prefix + shown
    normalized = shown[:-1] if directory and shown.endswith("/") else shown
    accepted = _safe_name(shown, directory) and normalized not in seen
    if not valid_utf8:
        state.problem("non-utf8-member", location)
    if len(location.encode("utf-8")) > state.limits["max_path_utf8_bytes"]:
        state.problem("path-byte-limit", location)
        accepted = False
    if not accepted:
        state.gap("unsafe-archive-name", location, _sha(_os.fsencode(name)),
                  "member cannot enter the accepted normalized namespace")
    duplicate = normalized in seen
    seen.add(normalized)
    return location, accepted and valid_utf8, duplicate


def _archive_row(state, location, kind, mode, raw, source, safe=True, duplicate=False,
                 target=None):
    identity = _sha(raw) if raw is not None else _sha(location.encode())
    if not safe:
        state.finding("ARCHIVE001", location, identity)
    if duplicate:
        return
    state.add(_entry(location, kind, mode, raw, target=target, source=source))


def _archive_payload(state, location, raw, depth):
    state.archive_bytes += len(raw)
    if state.archive_bytes > state.limits["max_archive_uncompressed_bytes"]:
        state.problem("archive-total-byte-limit", location, _sha(raw))
        return
    nested = _archive_kind(location, raw)
    if nested is None:
        state.scan(location, raw)
    else:
        # Scan decoded members, not a second copy of their compressed container.
        state.scan(location, raw, target=None)
        _archive(state, raw, nested, location + "!", depth + 1)


def _next_member(state, location):
    state.archive_members += 1
    if state.archive_members > state.limits["max_archive_members"]:
        state.problem("archive-member-limit", location)
        return False
    return True


def _zip_decoded(raw, info, maximum):
    """Check actual decoder output independently of ZipExtFile's declared size."""
    start = info.header_offset
    _promise(type(start) is int and start >= 0, "invalid ZIP offset promise")
    if start + 30 > len(raw) or raw[start:start + 4] != b"PK\x03\x04":
        raise _zipfile.BadZipFile("invalid local header")
    name_bytes, extra_bytes = _struct.unpack_from("<HH", raw, start + 26)
    start += 30 + name_bytes + extra_bytes
    end = start + info.compress_size
    if end > len(raw):
        raise _zipfile.BadZipFile("truncated compressed member")
    compressed = raw[start:end]
    if info.compress_type == _zipfile.ZIP_STORED:
        content = compressed
    elif info.compress_type == _zipfile.ZIP_DEFLATED:
        decoder = _zlib.decompressobj(-15)
        content = decoder.decompress(compressed, maximum + 1)
        if len(content) > maximum:
            raise _Ceiling("archive-member-byte-limit")
        if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
            raise _zipfile.BadZipFile("incomplete or trailing deflate stream")
    elif info.compress_type == _zipfile.ZIP_BZIP2:
        decoder = _bz2.BZ2Decompressor()
        content = decoder.decompress(compressed, max_length=maximum + 1)
        if len(content) > maximum:
            raise _Ceiling("archive-member-byte-limit")
        if not decoder.eof or decoder.unused_data:
            raise _zipfile.BadZipFile("incomplete or trailing bzip2 stream")
    else:
        raise NotImplementedError("unsupported ZIP compression")
    if len(content) > maximum:
        raise _Ceiling("archive-member-byte-limit")
    if len(content) != info.file_size or _zlib.crc32(content) != info.CRC:
        raise _zipfile.BadZipFile("actual decoded length or CRC differs")
    return content


def _zip_directory_bound(state, raw, prefix):
    """Bound the central-directory entry count before ZipFile allocates entries."""
    end = raw.rfind(b"PK\x05\x06", max(0, len(raw) - 65557))
    if end < 0 or end + 22 > len(raw):
        return True  # The normal decoder records the malformed-container gap.
    fields = _struct.unpack_from("<4H2LH", raw, end + 4)
    disk, central_disk, here, total, size, offset, comment = fields
    if disk or central_disk or here != total or total == 65535 or offset == 4294967295:
        state.problem("unsupported-zip-layout", prefix or ".", _sha(raw))
        return False
    if end + 22 + comment != len(raw) or offset + size != end:
        state.problem("ambiguous-zip-layout", prefix or ".", _sha(raw))
        return False
    cursor, count = offset, 0
    while cursor < end:
        if cursor + 46 > end or raw[cursor:cursor + 4] != b"PK\x01\x02":
            return True
        name, extra, note = _struct.unpack_from("<HHH", raw, cursor + 28)
        cursor += 46 + name + extra + note
        count += 1
        if count + state.archive_members > state.limits["max_archive_members"]:
            state.problem("archive-member-limit", prefix or ".")
            return False
    if cursor != end or count != total:
        state.problem("inconsistent-zip-directory", prefix or ".", _sha(raw))
        return False
    return True


def _zip(state, raw, prefix, depth):
    source = f"archive:zip:depth={depth}"
    if not _zip_directory_bound(state, raw, prefix):
        return
    seen = set()
    try:
        with _zipfile.ZipFile(_io.BytesIO(raw), "r") as archive:
            for info in archive.infolist():
                name = info.orig_filename
                if not _next_member(state, prefix or "."):
                    break
                directory = info.is_dir()
                location, safe, duplicate = _member_name(state, name, directory, prefix, seen)
                mode = info.external_attr >> 16
                category = _stat.S_IFMT(mode)
                if not category:
                    mode = (0o040000 if directory else 0o100000) | (_stat.S_IMODE(mode) or 0o644)
                if not (_stat.S_ISREG(mode) or _stat.S_ISDIR(mode)):
                    link = _stat.S_ISLNK(mode)
                    _archive_row(state, location, "symlink" if link else "special",
                                 _mode(mode), None, source, safe, duplicate)
                    state.problem("unsafe-archive-object", location,
                                  summary="member is not regular", rule="ARCHIVE002")
                    continue
                if info.flag_bits & 1 or info.compress_type not in (
                        _zipfile.ZIP_STORED, _zipfile.ZIP_DEFLATED,
                        _zipfile.ZIP_BZIP2):
                    state.problem("unsupported-archive-compression", location)
                    continue
                if info.file_size > state.limits["max_member_uncompressed_bytes"]:
                    state.problem("archive-member-byte-limit", location)
                    continue
                if info.file_size > max(1, info.compress_size) * state.limits[
                        "max_compression_ratio_numerator"]:
                    state.problem("archive-compression-ratio", location)
                    continue
                try:
                    with archive.open(info, "r") as stream:
                        content = stream.read(state.limits["max_member_uncompressed_bytes"] + 1)
                    _promise(type(content) is bytes, "archive reader did not return bytes")
                    actual = _zip_decoded(raw, info, state.limits["max_member_uncompressed_bytes"])
                    _promise(content == actual,
                             "ZIP dependency returned inconsistent decoded bytes")
                    if info.compress_size and len(content) > info.compress_size * state.limits[
                            "max_compression_ratio_numerator"]:
                        raise _Ceiling("archive-compression-ratio")
                except _Ceiling as exc:
                    state.problem(str(exc), location)
                    continue
                except (_zipfile.BadZipFile, EOFError, _zlib.error, NotImplementedError) as exc:
                    state.problem("archive-decoder", location, summary=type(exc).__name__)
                    continue
                if directory:
                    if content:
                        state.problem("archive-directory-payload", location, _sha(content))
                    _archive_row(state, location.rstrip("/"), "directory", _mode(mode),
                                 None, source, safe, duplicate)
                else:
                    _archive_row(state, location, "regular", _mode(mode), content,
                                 source, safe, duplicate)
                    if not duplicate:
                        _archive_payload(state, location, content, depth)
    except (UnicodeDecodeError, _zipfile.BadZipFile, EOFError, _zlib.error) as exc:
        state.problem("archive-decoder", prefix or ".", _sha(raw), type(exc).__name__)


def _tar_decoded(state, raw):
    # A physical TAR member needs at most a 512-byte header and 511-byte padding,
    # plus a final 10240-byte record. The payload ceiling remains independently checked.
    maximum = (state.limits["max_archive_uncompressed_bytes"]
               + 1024 * state.limits["max_archive_members"] + 10240)
    if raw.startswith(b"\x1f\x8b"):
        decoder = _zlib.decompressobj(31)
        content = decoder.decompress(raw, maximum + 1)
    elif raw.startswith(b"BZh"):
        decoder = _bz2.BZ2Decompressor()
        content = decoder.decompress(raw, max_length=maximum + 1)
    elif raw.startswith(b"\xfd7zXZ\x00"):
        decoder = _lzma.LZMADecompressor(memlimit=maximum)
        content = decoder.decompress(raw, max_length=maximum + 1)
    else:
        if len(raw) > maximum:
            raise _Ceiling("archive-physical-byte-limit")
        return raw
    if len(content) > maximum:
        raise _Ceiling("archive-physical-byte-limit")
    if not decoder.eof or decoder.unused_data:
        raise _tarfile.ReadError("incomplete or concatenated compressed stream")
    if len(content) > max(1, len(raw)) * state.limits["max_compression_ratio_numerator"]:
        raise _Ceiling("archive-compression-ratio")
    return content


def _tar(state, raw, prefix, depth):
    source = f"archive:tar:depth={depth}"
    seen = set()
    try:
        decoded = _tar_decoded(state, raw)
        with _tarfile.open(fileobj=_io.BytesIO(decoded), mode="r:") as archive:
            for info in archive:
                if not _next_member(state, prefix or "."):
                    break
                location, safe, duplicate = _member_name(
                    state, info.name, info.isdir(), prefix, seen,
                )
                if not info.isfile() and not info.isdir():
                    kind = ("symlink" if info.issym()
                            else ("hardlink" if info.islnk() else "special"))
                    target, valid = _display_name(info.linkname)
                    _archive_row(state, location, kind, format(info.mode, "06o"), None,
                                 source, safe, duplicate, target=target if valid else None)
                    state.problem("unsafe-archive-object", location,
                                  summary="member is not regular", rule="ARCHIVE002")
                    continue
                if info.isdir():
                    _archive_row(state, location.rstrip("/"), "directory",
                                 _mode(_stat.S_IFDIR | info.mode), None, source, safe, duplicate)
                    continue
                if info.size > state.limits["max_member_uncompressed_bytes"]:
                    state.problem("archive-member-byte-limit", location)
                    continue
                stream = archive.extractfile(info)
                _promise(stream is not None, "regular tar member has no byte stream")
                with stream:
                    content = stream.read(state.limits["max_member_uncompressed_bytes"] + 1)
                _promise(type(content) is bytes, "tar reader did not return bytes")
                if len(content) != info.size:
                    state.problem("archive-decoded-size", location)
                    continue
                _archive_row(state, location, "regular", _mode(_stat.S_IFREG | info.mode),
                             content, source, safe, duplicate)
                if not duplicate:
                    _archive_payload(state, location, content, depth)
    except _Ceiling as exc:
        state.problem(str(exc), prefix or ".", _sha(raw))
    except (_tarfile.TarError, EOFError, UnicodeDecodeError, _zlib.error, _lzma.LZMAError) as exc:
        state.problem("archive-decoder", prefix or ".", _sha(raw), type(exc).__name__)


def _archive(state, raw, kind, prefix, depth):
    if depth > state.limits["max_archive_depth"]:
        state.problem("archive-depth-limit", prefix or ".", _sha(raw))
        return
    state.depth = max(state.depth, depth)
    if kind == "zip":
        _zip(state, raw, prefix, depth)
    else:
        _tar(state, raw, prefix, depth)


def inspect_archive(path: str) -> dict[str, object]:
    """Inspect ZIP or tar-family bytes in memory; never extract into a filesystem."""
    info = _validate_path(path, archive=True)
    kind = "zip" if path.lower().endswith((".zip", ".whl")) else "tar"
    state = _Inspection("archive", path, kind)
    try:
        raw = _read_regular(path, info, state.limits["max_regular_file_bytes"])
    except PermissionError:
        state.problem("unreadable-file", ".")
        return state.finish()
    except _Ceiling:
        state.problem("regular-file-byte-limit", ".")
        return state.finish()
    state.subject["bytes"], state.subject["sha256"] = len(raw), _sha(raw)
    kind = _archive_kind(path, raw)
    if kind is None:
        state.subject["subject_type"] = "unsupported"
        state.problem("unsupported-container", ".", _sha(raw))
    else:
        state.subject["subject_type"] = kind
        _archive(state, raw, kind, "", 1)
    return state.finish()


def _git(repository, arguments, maximum, input_bytes=b""):
    """Acquire registered read-only Git output with bounded stdout/stderr buffers."""
    env = {key: _os.environ[key] for key in ("PATH", "SYSTEMROOT") if key in _os.environ}
    env.update({"LC_ALL": "C", "LANG": "C", "GIT_OPTIONAL_LOCKS": "0",
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": _os.devnull,
                "GIT_NO_REPLACE_OBJECTS": "1"})
    argv = ["git", "-C", repository, *arguments]
    read_end, write_end = _os.pipe()
    try:
        process = _subprocess.Popen(argv, stdin=read_end, stdout=_subprocess.PIPE,
                                    stderr=_subprocess.PIPE, env=env, shell=False)
    except BaseException:
        _os.close(write_end)
        raise
    finally:
        _os.close(read_end)
    errors = []
    exceeded = []
    stderr = bytearray()

    def drain(stream, buffer):
        try:
            while True:
                chunk = stream.read(65536)
                _promise(type(chunk) is bytes, "Git output did not return exact bytes")
                if not chunk:
                    break
                if len(buffer) + len(chunk) > maximum:
                    exceeded.append(True)
                    process.kill()
                    break
                buffer.extend(chunk)
        except BaseException as exc:
            errors.append(exc)
            if process.poll() is None:
                process.kill()
        finally:
            stream.close()

    def feed():
        try:
            offset = 0
            while offset < len(input_bytes):
                sent = _os.write(write_end, input_bytes[offset:offset + 65536])
                _promise(type(sent) is int and 0 < sent <= min(65536, len(input_bytes) - offset),
                         "Git stdin violated write promise")
                offset += sent
        except BrokenPipeError as exc:
            if not exceeded and not errors:
                errors.append(exc)
        except BaseException as exc:
            errors.append(exc)
            if process.poll() is None:
                process.kill()
        finally:
            _os.close(write_end)

    output = bytearray()
    reader = _threading.Thread(target=drain, args=(process.stderr, stderr))
    writer = _threading.Thread(target=feed)
    reader.start()
    writer.start()
    try:
        drain(process.stdout, output)
    finally:
        writer.join()
        reader.join()
        code = process.wait()
    if errors:
        raise errors[0]
    if exceeded:
        raise _Ceiling("git-output-limit")
    _promise(type(code) is int and code == 0, "read-only Git command returned nonzero status")
    return bytes(output)


def _oid(raw):
    return bool(_re.fullmatch(rb"[0-9a-f]{40}", raw))


def _metadata_directory(path, prefix):
    info = _os.lstat(path)
    if not _stat.S_ISREG(info.st_mode):
        raise ValueError("Git indirection is not a regular file")
    raw = _read_regular(path, info, _DEFAULT_LIMITS["max_regular_file_bytes"])
    if prefix and not raw.startswith(prefix):
        raise ValueError("invalid Git directory indirection")
    value = raw[len(prefix):].rstrip(b"\n")
    if not value or b"\n" in value or b"\r" in value or b"\0" in value:
        raise ValueError("invalid Git directory indirection")
    try:
        named = value.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Git directory path is not UTF-8") from exc
    if not _os.path.isabs(named):
        named = _os.path.join(_os.path.dirname(path), named)
    named = _os.path.normpath(named)
    _validate_path(named)
    return named


def _repository_storage(repository):
    git_path = _os.path.join(repository, ".git")
    if _os.path.lexists(git_path):
        mode = _os.lstat(git_path).st_mode
        if _stat.S_ISDIR(mode):
            _validate_path(git_path)
            return git_path
        if _stat.S_ISREG(mode):
            return _metadata_directory(git_path, b"gitdir: ")
        raise ValueError("unsafe Git control path")
    if not all(_os.path.lexists(_os.path.join(repository, part))
               for part in ("HEAD", "objects", "refs")):
        raise ValueError("input is not a Git repository")
    for part in ("objects", "refs"):
        _validate_path(_os.path.join(repository, part))
    if not _stat.S_ISREG(_os.lstat(_os.path.join(repository, "HEAD")).st_mode):
        raise ValueError("unsafe Git HEAD")
    return repository


def _local_history_storage(state, directory):
    """Refuse external, shallow or lazy-fetch sources before starting Git."""
    roots = [directory]
    common = _os.path.join(directory, "commondir")
    if _os.path.lexists(common):
        roots.append(_metadata_directory(common, b""))
    for root in sorted(set(roots)):
        for marker in ("shallow", "info/grafts", "objects/info/alternates",
                       "objects/info/http-alternates"):
            if _os.path.lexists(_os.path.join(root, marker)):
                state.problem("external-or-incomplete-history", marker)
                return False
        config = _os.path.join(root, "config")
        if _os.path.lexists(config):
            info = _os.lstat(config)
            if not _stat.S_ISREG(info.st_mode):
                state.problem("unsafe-history-control", "config")
                return False
            try:
                raw = _read_regular(config, info, state.limits["max_regular_file_bytes"])
            except _Ceiling:
                state.problem("history-config-limit", "config")
                return False
            if _re.search(rb"(?im)^\s*\[\s*include|^\s*(?:promisor|partialclone)\s*=", raw):
                state.problem("external-history-configuration", "config", _sha(raw))
                return False
        # Git must not follow internal links or trigger lazy object acquisition.
        names = ("objects", "refs", "HEAD", "packed-refs")
        pending = [(_os.path.join(root, name), name) for name in names
                   if _os.path.lexists(_os.path.join(root, name))]
        visited = 0
        while pending:
            path, relative = pending.pop()
            visited += 1
            if visited > state.limits["max_tree_objects"]:
                state.problem("history-storage-entry-limit", ".")
                return False
            info = _os.lstat(path)
            if not (_stat.S_ISREG(info.st_mode) or _stat.S_ISDIR(info.st_mode)):
                state.problem("unsafe-history-storage", _display_name(relative)[0])
                return False
            if relative.endswith(".promisor"):
                state.problem("lazy-history-storage", relative)
                return False
            if _stat.S_ISDIR(info.st_mode):
                with _os.scandir(path) as entries:
                    for entry in entries:
                        pending.append((entry.path, relative + "/" + entry.name))
                        if len(pending) + visited > state.limits["max_tree_objects"]:
                            state.problem("history-storage-entry-limit", ".")
                            return False
    return True


def _tree_items(raw):
    result, offset = [], 0
    while offset < len(raw):
        stop = raw.find(b"\0", offset)
        _promise(stop >= 0 and stop + 21 <= len(raw), "malformed Git tree payload")
        mode, space, name = raw[offset:stop].partition(b" ")
        accepted_modes = (b"40000", b"100644", b"100755", b"120000", b"160000")
        _promise(space == b" " and mode in accepted_modes
                 and bool(name) and b"/" not in name, "invalid Git tree entry")
        result.append((mode, name, raw[stop + 1:stop + 21].hex()))
        offset = stop + 21
    return result


def _historical_paths(state, paths, trees, roots):
    """Retain all committed names, including renamed copies of the same blob."""
    todo = [(oid, "", frozenset()) for oid in roots]
    visited = set()
    while todo:
        oid, prefix, ancestors = todo.pop()
        key = oid, prefix
        if key in visited:
            continue
        if len(visited) >= state.limits["max_tree_objects"]:
            state.problem("history-path-expansion-limit", ".")
            return
        visited.add(key)
        if oid in ancestors or oid not in trees:
            state.problem("missing-or-cyclic-history-tree", "trees/" + oid)
            continue
        for mode, name_raw, child in trees[oid]:
            try:
                name = name_raw.decode("utf-8")
            except UnicodeDecodeError:
                state.problem("non-utf8-history-path", "trees/" + oid, _sha(name_raw))
                continue
            full = prefix + name
            if not _safe_name(full) or len(full.encode()) > state.limits["max_path_utf8_bytes"]:
                state.problem("unsafe-history-path", "trees/" + oid, _sha(name_raw))
                continue
            if mode == b"160000":
                state.problem("external-submodule-history", full)
                continue
            if child not in paths:
                state.problem("missing-history-tree-object", full)
                continue
            paths[child].add(full)
            if mode == b"40000":
                todo.append((child, full + "/", ancestors | {oid}))


def _history(state, repository):
    maximum = state.limits["max_git_stdout_bytes"]
    inside = _git(repository, ["rev-parse", "--is-inside-work-tree"], maximum)
    _promise(inside in (b"true\n", b"false\n"), "invalid repository-kind response")
    git_dir = _text(_git(repository, ["rev-parse", "--git-dir"], maximum)).rstrip("\n")
    _promise(bool(git_dir) and "\n" not in git_dir, "invalid Git directory response")
    directory = git_dir if _os.path.isabs(git_dir) else _os.path.join(repository, git_dir)
    directory = _os.path.normpath(directory)
    _validate_path(directory)
    # Incomplete local histories cannot receive a complete-coverage verdict.
    for marker in ("shallow", "info/grafts", "objects/info/alternates",
                   "objects/info/http-alternates"):
        if _os.path.lexists(_os.path.join(directory, marker)):
            state.problem("external-or-incomplete-history", marker)
            return
    head = _git(repository, ["rev-parse", "HEAD"], maximum)
    _promise(head.endswith(b"\n") and _oid(head[:-1]), "invalid HEAD response")
    state.subject["git_head"] = head[:-1].decode()
    refs_command = ["for-each-ref", "--format=%(refname)%00%(objectname)%00%(objecttype)"]
    refs_raw = _git(repository, refs_command, maximum)
    _promise(not refs_raw or refs_raw.endswith(b"\n"), "unterminated ref response")
    refs = []
    for line in refs_raw.splitlines():
        pieces = line.split(b"\0")
        _promise(len(pieces) == 3 and _oid(pieces[1]), "malformed ref response")
        name, target, kind = map(_text, pieces)
        _promise(name.startswith("refs/") and _safe_name(name), "invalid ref name")
        _promise(kind in ("commit", "tree", "blob", "tag"), "invalid ref type")
        refs.append({"ref": name, "oid": target, "type": kind})
        state.add(_entry(name, "git-ref", oid=target, target=target, source="history-ref"))
    _promise(len({row["ref"] for row in refs}) == len(refs), "duplicate ref response")
    refs.sort(key=lambda r: r["ref"].encode())
    state.subject["refs_sha256"] = _sha(_jsonl(refs))
    listing = _git(repository, ["rev-list", "--objects", "--all"], maximum)
    _promise(not listing or listing.endswith(b"\n"), "unterminated object response")
    paths = {}
    for line in listing.splitlines():
        oid, _, name = line.partition(b" ")
        _promise(_oid(oid), "invalid reachable object id")
        key = oid.decode()
        names = paths.setdefault(key, set())
        if name:
            try:
                names.add(name.decode("utf-8"))
            except UnicodeDecodeError:
                state.problem("non-utf8-history-path", "objects/" + key, _sha(name))
    if len(paths) > state.limits["max_history_objects"]:
        state.problem("history-object-limit", ".")
        return
    payload_input = b"".join(name.encode() + b"\n" for name in sorted(paths))
    sizes_command = ["cat-file", "--batch-check=%(objectname)%00%(objecttype)%00%(objectsize)"]
    sizes_raw = _git(repository, sizes_command, maximum, payload_input)
    sizes = {}
    for line in sizes_raw.splitlines():
        fields = line.split(b"%00")
        _promise(len(fields) == 3 and _oid(fields[0]), "invalid batch-check response")
        oid = fields[0].decode()
        _promise(oid in paths and oid not in sizes, "unexpected batch-check object")
        _promise(fields[1] in (b"blob", b"tree", b"commit", b"tag")
                 and _re.fullmatch(rb"0|[1-9][0-9]*", fields[2]) is not None,
                 "invalid object type or size")
        sizes[oid] = fields[1].decode(), int(fields[2])
    _promise(set(sizes) == set(paths), "batch-check object roster differs")
    if sum(size for _, size in sizes.values()) > state.limits["max_history_payload_bytes"]:
        state.problem("history-payload-limit", ".")
        return
    objects, trees, roots = set(), {}, set()
    roots.update(row["oid"] for row in refs if row["type"] == "tree")
    paths_expanded = False
    # Trees and commits first, then blob payloads. No full payload history is retained.
    for oid in sorted(sizes, key=lambda value: (sizes[value][0] == "blob", value)):
        kind, size = sizes[oid]
        data = _git(repository, ["cat-file", "--batch"], maximum, oid.encode() + b"\n")
        header, newline, tail = data.partition(b"\n")
        _promise(newline == b"\n", "missing batch object header")
        _promise(header == f"{oid} {kind} {size}".encode(), "batch object header mismatch")
        _promise(len(tail) == size + 1 and tail[-1:] == b"\n", "batch object length mismatch")
        raw = tail[:-1]
        git_payload = f"{kind} {size}\0".encode() + raw
        _promise(_hashlib.sha1(git_payload).hexdigest() == oid, "Git object identity mismatch")
        objects.add(oid)
        if kind == "tree":
            trees[oid] = _tree_items(raw)
        elif kind == "commit":
            first = raw.split(b"\n", 1)[0]
            _promise(first.startswith(b"tree ") and _oid(first[5:]), "invalid commit tree")
            roots.add(first[5:].decode())
        elif kind == "tag":
            lines = raw.split(b"\n\n", 1)[0].splitlines()
            if b"type tree" in lines:
                first = lines[0]
                _promise(first.startswith(b"object ") and _oid(first[7:]), "invalid tag object")
                roots.add(first[7:].decode())
        if kind == "blob" and not paths_expanded:
            _historical_paths(state, paths, trees, roots)
            paths_expanded = True
        names = sorted(paths[oid], key=lambda n: n.encode())
        source = "history-paths:" + "|".join(names) if names else "history-object"
        state.add(_entry("objects/" + oid, "git-" + kind, raw=raw, oid=oid, source=source))
        if kind == "blob":
            for name in names or [""]:
                location = "blobs/" + oid + ("/" + name if name else "")
                state.scan(location, raw, path_text=name)
        elif kind in ("commit", "tag"):
            state.scan(("commits/" if kind == "commit" else "tags/") + oid,
                       raw, target="history-metadata")
    # The registered rev-list view covers reachable objects, not just HEAD files.
    # Retain every object in the inventory even when it has no printed path.
    if not paths_expanded:
        _historical_paths(state, paths, trees, roots)
    _promise(set(objects) == set(paths), "incomplete acquired-object roster")


def inspect_history(repository: str) -> dict[str, object]:
    """Inspect all refs and their reachable Git objects using only read-only argv."""
    _validate_path(repository)
    directory = _repository_storage(repository)
    state = _Inspection("history", repository, "git-repository")
    if not _local_history_storage(state, directory):
        return state.finish()
    try:
        _history(state, repository)
    except _Ceiling:
        state.problem("git-output-limit", ".")
    return state.finish()
