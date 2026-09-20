"""Reproduce the finite, versioned Unit 20 input corpus without filesystem access.

DESIGN D20-C2--C7 fixes the registry, construction formulas and exact bytes.
The initial MANIFEST is a fresh-build product, not a replacement or hash pin
for an evolving aggregate. This module neither solves nor validates optima.
"""

from __future__ import annotations

import hashlib as _hashlib
import itertools as _itertools
import json as _json

__all__ = ("build_corpus", "generate_instance", "recipe_ids")

_FAMILIES = ("path", "cycle", "complete", "bipartite", "matching")
_SUITE = "unit20-v1"


def _make_ids() -> tuple[str, ...]:
    ids = []
    for q in range(1, 6):
        for f0, f1 in _itertools.product(range(1, q + 1), repeat=2):
            ids.append(f"edge-q{q:02d}-f{f0:02d}-{f1:02d}")
    for a, b, c in _itertools.product(range(3), repeat=3):
        for f0, f1, f2 in _itertools.product(
            range(1, a + b + 1), range(1, a + c + 1), range(1, b + c + 1),
        ):
            ids.append(f"tri-q{a}-{b}-{c}-f{f0}-{f1}-{f2}")
    for family, n, bits, fmode in _itertools.product(
        _FAMILIES, (4, 6, 8), (1, 8), ("unit", "half", "near", "degree"),
    ):
        ids.append(f"struct-{family}-n{n:02d}-b{bits:05d}-f{fmode}")
    for family, bits, qmode, fmode in _itertools.product(
        _FAMILIES, (1, 8, 64, 256, 4096, 16384), ("flat", "ramp"), ("unit", "degree"),
    ):
        ids.append(f"bits-{family}-n04-b{bits:05d}-q{qmode}-f{fmode}")
    for n, bits, fmode, seed in _itertools.product(
        (4, 6, 8), (1, 8, 64), ("half", "alternating"), (1, 73),
    ):
        ids.append(f"seeded-n{n:02d}-b{bits:05d}-f{fmode}-s{seed:02d}")
    return tuple(sorted(ids))


_IDS = _make_ids()


def recipe_ids() -> tuple[str, ...]:
    """Return all 655 recipe identities in strict ASCII order, without deduplication."""
    return _IDS


def _support(family: str, n: int, seed: int) -> tuple[tuple[int, int], ...]:
    if family == "complete":
        return tuple(_itertools.combinations(range(n), 2))
    if family == "bipartite":
        return tuple(_itertools.product(range(n // 2), range(n // 2, n)))
    if family == "matching":
        return tuple((u, u + 1) for u in range(0, n, 2))
    pairs = {(u, u + 1) for u in range(n - 1)}
    if family != "path":
        pairs.add((0, n - 1))
    if family == "seeded":
        for u, v in _itertools.combinations(range(n), 2):
            if (u, v) not in pairs:
                message = f"exactfrac-u20-seeded/1\n{seed}\n{n}\n{u}\n{v}\n".encode("ascii")
                if _hashlib.sha256(message).digest()[0] < 64:
                    pairs.add((u, v))
    return tuple(sorted(pairs))


def _capacities(degrees: list[int], mode: str) -> tuple[int, ...]:
    if mode == "unit":
        return (1,) * len(degrees)
    if mode == "half":
        return tuple((degree + 1) // 2 for degree in degrees)
    if mode == "near":
        return tuple(max(1, degree - 1) for degree in degrees)
    if mode == "alternating":
        return tuple(1 if v % 2 == 0 else degree for v, degree in enumerate(degrees))
    return tuple(degrees)


def _parts(recipe_id: str) -> tuple[int, tuple[tuple[int, int, int], ...], tuple[int, ...]]:
    fields = recipe_id.split("-")
    if fields[0] == "edge":
        return 2, ((0, 1, int(fields[1][1:])),), (int(fields[2][1:]), int(fields[3]))
    if fields[0] == "tri":
        a, b, c = int(fields[1][1:]), int(fields[2]), int(fields[3])
        edges = tuple(edge for edge in ((0, 1, a), (0, 2, b), (1, 2, c)) if edge[2] > 0)
        return 3, edges, (int(fields[4][1:]), int(fields[5]), int(fields[6]))
    if fields[0] == "seeded":
        family, n, bits = "seeded", int(fields[1][1:]), int(fields[2][1:])
        qmode, fmode, seed = "ramp", fields[3][1:], int(fields[4][1:])
    else:
        family, n, bits = fields[1], int(fields[2][1:]), int(fields[3][1:])
        qmode = "flat" if fields[0] == "struct" else fields[4][1:]
        fmode, seed = fields[-1][1:], 0
    support = _support(family, n, seed)
    lower = 1 << (bits - 1)
    flat = (1 << bits) - 1
    degrees = [0] * n
    weighted = []
    for j, (u, v) in enumerate(support):
        q = flat if qmode == "flat" else lower + ((j + seed) % lower)
        weighted.append((u, v, q))
        degrees[u] += q
        degrees[v] += q
    return n, tuple(weighted), _capacities(degrees, fmode)


def _decimal(value: int) -> str:
    """Encode a nonnegative construction integer; each conversion has <=9 digits."""
    if value == 0:
        return "0"
    chunks = []
    while value:
        value, chunk = divmod(value, 1_000_000_000)
        chunks.append(str(chunk))
    return chunks[-1] + "".join(chunk.zfill(9) for chunk in reversed(chunks[:-1]))


def generate_instance(recipe_id: str) -> bytes:
    """Return the canonical payload for an exact registered str; reject all others."""
    if type(recipe_id) is not str or recipe_id not in _IDS:
        raise ValueError("recipe_id must be an exact registered Unit 20 string")
    n, edges, capacities = _parts(recipe_id)
    encoded_edges = ",".join(
        "[" + ",".join(_decimal(value) for value in edge) + "]" for edge in edges
    )
    encoded_f = ",".join(_decimal(value) for value in capacities)
    return (
        '{"format":"exactfrac-instance/1","n":' + _decimal(n)
        + ',"edges":[' + encoded_edges + '],"f":[' + encoded_f + "]}\n"
    ).encode("ascii")


def build_corpus() -> tuple[tuple[str, bytes], ...]:
    """Return the initial MANIFEST and owned payloads; propagate failures unchanged."""
    records = []
    entries = []
    for rid in recipe_ids():
        raw = generate_instance(rid)
        path = _SUITE + "/" + rid + ".json"
        records.append((path, raw))
        entries.append({
            "suite": _SUITE, "recipe": rid, "path": path,
            "bytes": len(raw), "sha256": _hashlib.sha256(raw).hexdigest(),
        })
    # Only bounded byte counts occur here; huge input integers use _decimal above.
    manifest = (_json.dumps(
        {"format": "exactfrac-corpus-manifest/1", "entries": entries},
        ensure_ascii=True, separators=(",", ":"),
    ) + "\n").encode("ascii")
    return (("MANIFEST", manifest), *records)
