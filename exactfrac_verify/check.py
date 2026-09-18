"""Independent /1 byte validation and literal witness attainment (DESIGN 4.15).

Only admissibility/attainment or genuine Empty is checked, never optimality.
The instance is completely validated before the certificate is inspected.
"""

from __future__ import annotations

import json

__all__ = ("verify_certificate",)


def _json_integer(token: str) -> int:
    """Accumulate bounded nine-digit groups without full-token int conversion."""
    negative = token.startswith("-")
    start = 1 if negative else 0
    if start == len(token):
        raise ValueError("missing integer digits")
    if token[start] == "0" and (negative or len(token) != 1):
        raise ValueError("noncanonical integer zero")
    result = chunk = width = 0
    for char in token[start:]:
        if not "0" <= char <= "9":
            raise ValueError("noninteger numeric token")
        chunk = 10 * chunk + ord(char) - 48
        width += 1
        if width == 9:
            result = 1_000_000_000 * result + chunk
            chunk = width = 0
    result = result * 10**width + chunk
    return -result if negative else result


def _reject_number(_token: str) -> None:
    raise ValueError("only canonical integer tokens are permitted")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate decoded JSON key")
        value[key] = item
    return value


def _instance_data(raw: bytes) -> tuple[int, list[int], list[list[int]], int]:
    if type(raw) is not bytes:
        raise ValueError("instance must be exact bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("instance BOM is forbidden")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("invalid instance UTF-8") from error
    try:
        data = json.loads(
            text, object_pairs_hook=_unique_object, parse_int=_json_integer,
            parse_float=_reject_number, parse_constant=_reject_number,
        )
    except json.JSONDecodeError as error:
        raise ValueError("invalid instance JSON") from error
    if type(data) is not dict or set(data) not in (
        {"format", "n", "edges", "f"}, {"format", "n", "edges", "f", "labels"},
    ):
        raise ValueError("invalid instance fields")
    if type(data["format"]) is not str or data["format"] != "exactfrac-instance/1":
        raise ValueError("invalid instance format")
    n = data["n"]
    if type(n) is not int or n < 1:
        raise ValueError("invalid vertex count")
    capacities = data["f"]
    if type(capacities) is not list or len(capacities) != n:
        raise ValueError("invalid capacity list")
    for capacity in capacities:
        if type(capacity) is not int or capacity < 1:
            raise ValueError("invalid vertex capacity")
    if "labels" in data:
        labels = data["labels"]
        if type(labels) is not list or len(labels) != n:
            raise ValueError("invalid label list")
        seen: set[str | int] = set()
        for label in labels:
            if type(label) is not str and type(label) is not int:
                raise ValueError("invalid label type")
            if label in seen:
                raise ValueError("duplicate label")
            seen.add(label)
    edges = data["edges"]
    if type(edges) is not list or not edges:
        raise ValueError("invalid support list")
    previous = (-1, -1)
    for record in edges:
        if type(record) is not list or len(record) != 3:
            raise ValueError("invalid edge record")
        if any(type(field) is not int for field in record):
            raise ValueError("invalid edge field type")
        u, v, q = record
        if not 0 <= u < v < n or q < 1:
            raise ValueError("invalid edge endpoints or multiplicity")
        if (u, v) <= previous:
            raise ValueError("noncanonical edge order")
        previous = (u, v)
    # Declared lengths and every edge have been validated before derived storage.
    degrees = [0] * n
    total = 0
    for u, v, q in edges:
        degrees[u] += q
        degrees[v] += q
        total += q
    for capacity, degree in zip(capacities, degrees, strict=True):
        if capacity > degree:
            raise ValueError("instance is not active")
    return n, capacities, edges, total


class _Cursor:
    """One forward scan of the fixed certificate grammar; no JSON round trip."""

    __slots__ = ("data", "position")

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.position = 0

    def take(self, literal: bytes) -> None:
        if not self.data.startswith(literal, self.position):
            raise ValueError("invalid certificate grammar")
        self.position += len(literal)

    def comma(self) -> bool:
        if self.data.startswith(b",", self.position):
            self.position += 1
            return True
        return False

    def integer(self, positive: bool = False) -> int:
        start = self.position
        end = start
        while end < len(self.data) and 48 <= self.data[end] <= 57:
            end += 1
        if start == end or (end - start > 1 and self.data[start] == 48):
            raise ValueError("invalid certificate integer token")
        value = _json_integer(self.data[start:end].decode("ascii"))
        if positive and value == 0:
            raise ValueError("certificate integer must be positive")
        self.position = end
        return value

    def finish(self) -> None:
        self.take(b"}\n")
        if self.position != len(self.data):
            raise ValueError("trailing certificate bytes")


def _certificate_data(raw: bytes) -> tuple[bool, int, int, list[int], list[tuple[int, int]]]:
    if type(raw) is not bytes:
        raise ValueError("certificate must be exact bytes")
    cursor = _Cursor(raw)
    cursor.take(b'{"format":"exactfrac-certificate/1","empty":')
    empty = raw.startswith(b"true", cursor.position)
    cursor.take(b"true" if empty else b"false")
    cursor.take(b',"N":')
    numerator = cursor.integer()
    cursor.take(b',"D":')
    denominator = cursor.integer(positive=True)
    vertices: list[int] = []
    selection: list[tuple[int, int]] = []
    if not empty:
        cursor.take(b',"U":[')
        vertices.append(cursor.integer())
        while cursor.comma():
            vertices.append(cursor.integer())
        cursor.take(b'],"y":[')
        if not raw.startswith(b"]", cursor.position):
            while True:
                cursor.take(b"[")
                reference = cursor.integer()
                cursor.take(b",")
                count = cursor.integer(positive=True)
                cursor.take(b"]")
                selection.append((reference, count))
                if not cursor.comma():
                    break
        cursor.take(b"]")
    cursor.finish()
    return empty, numerator, denominator, vertices, selection


def verify_certificate(instance: bytes, certificate: bytes) -> None:
    """Validate two byte inputs or raise ValueError; operational errors propagate."""
    n, capacities, edges, total = _instance_data(instance)
    empty, numerator, denominator, vertices, selection = _certificate_data(certificate)
    if empty:
        # lem:empty applies only after full active-instance validation.
        if total != 1 or numerator != 0 or denominator != 1:
            raise ValueError("false Empty or incorrect literal Empty pair")
        return None
    membership = [False] * n
    previous = -1
    for vertex in vertices:
        if not previous < vertex < n:
            raise ValueError("noncanonical or out-of-range shore")
        membership[vertex] = True
        previous = vertex
    previous = -1
    selected = 0
    for reference, count in selection:
        if not previous < reference < len(edges):
            raise ValueError("noncanonical or out-of-range sparse reference")
        u, v, q = edges[reference]
        if count > q or membership[u] == membership[v]:
            raise ValueError("invalid selected boundary count")
        selected += count
        previous = reference
    capacity_total = sum(capacities[vertex] for vertex in vertices)
    internal = sum(q for u, v, q in edges if membership[u] and membership[v])
    admissible_total = capacity_total + selected
    # def:parameter: parity and minimum total are separate requirements.
    if admissible_total % 2 != 1 or admissible_total < 3:
        raise ValueError("inadmissible witness total")
    # eq:compact-density: both structural integers must match, not only the ratio.
    if numerator != 2 * (internal + selected) or denominator != admissible_total - 1:
        raise ValueError("incorrect literal raw attainment")
    return None
