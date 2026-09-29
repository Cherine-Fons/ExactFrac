"""Construct the finite Unit 21B input family, without I/O or optimization.

DESIGN D21B-I3--I5 fixes the registry, domain-separated SHA-256 messages,
matched magnitude construction, exact payload bytes and own-suite MANIFEST.
The returned MANIFEST is not permission to replace an evolving aggregate.
"""

from __future__ import annotations

import hashlib as _hashlib
import itertools as _itertools
import json as _json

__all__ = ("build_corpus", "generate_instance", "recipe_ids")

_SUITE = "unit21-v2"
_TAG = "exactfrac-u21b-irregular/1"
_SEEDS = tuple(f"p{i:02d}" for i in range(1, 6)) + tuple(
    f"s{i:02d}" for i in range(1, 21)
)
_IDS = tuple(sorted(
    f"irregular-n{n:02d}-t{tau:03d}-b{bits:05d}-f{mode}-{seed}"
    for n, tau, bits, mode, seed in _itertools.product(
        (6, 8, 12, 16), (64, 128), (1, 8, 64), ("alternating", "random"), _SEEDS,
    )
))


def recipe_ids() -> tuple[str, ...]:
    """Return every registered identity in ASCII order, including equal payloads."""
    return _IDS


def _decimal(value: int) -> str:
    """Encode a nonnegative construction integer in at-most-nine-digit chunks."""
    if value == 0:
        return "0"
    chunks = []
    while value:
        value, chunk = divmod(value, 1_000_000_000)
        chunks.append(str(chunk))
    return chunks[-1] + "".join(chunk.zfill(9) for chunk in reversed(chunks[:-1]))


def _digest(*fields: str | int) -> bytes:
    # Integer message fields are n, tau and vertex numbers from the fixed domain.
    text = _TAG + "\n" + "\n".join(str(field) for field in fields) + "\n"
    return _hashlib.sha256(text.encode("ascii")).digest()


def _parts(recipe_id: str) -> tuple[int, tuple[tuple[int, int, int], ...], tuple[int, ...]]:
    # The public boundary has already required an exact registered string.
    fields = recipe_id.split("-")
    n, tau, bits = int(fields[1][1:]), int(fields[2][1:]), int(fields[3][1:])
    mode, seed = fields[4][1:], fields[5]
    support = {(v, v + 1) for v in range(n - 1)} | {(0, n - 1)}
    for u, v in _itertools.combinations(range(n), 2):
        if (u, v) not in support and _digest("support", seed, n, u, v)[0] < tau:
            support.add((u, v))
    degrees = [0] * n
    edges = []
    for u, v in sorted(support):
        digest = _digest("multiplicity", seed, n, tau, mode, u, v)
        q = 1 + int.from_bytes(digest, "big", signed=False) % (1 << bits)
        edges.append((u, v, q))
        degrees[u] += q
        degrees[v] += q
    if mode == "alternating":
        capacities = tuple(1 if v % 2 == 0 else degrees[v] for v in range(n))
    else:
        capacities = tuple(
            1 + int.from_bytes(
                _digest("capacity", seed, n, tau, "random", v), "big", signed=False,
            ) % degrees[v]
            for v in range(n)
        )
    return n, tuple(edges), capacities


def generate_instance(recipe_id: str) -> bytes:
    """Return canonical bytes for one exact registered string; reject, never repair."""
    if type(recipe_id) is not str or recipe_id not in _IDS:
        raise ValueError("recipe_id must be an exact registered Unit 21B string")
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
    """Return this suite's initial MANIFEST and payloads; do not access an aggregate."""
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
    # Metadata counts are bounded. Input q/f integers use _decimal, not json.dumps.
    manifest = (_json.dumps(
        {"format": "exactfrac-corpus-manifest/1", "entries": entries},
        ensure_ascii=True, separators=(",", ":"),
    ) + "\n").encode("ascii")
    return (("MANIFEST", manifest), *records)
