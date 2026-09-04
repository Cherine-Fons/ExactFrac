"""Canonical compact-multiplicity graph instances for ExactFrac."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = (
    "Edge",
    "Instance",
    "InvalidInstance",
    "UnsupportedInstance",
)

Edge = tuple[int, int, int]

_FORMAT = "exactfrac-instance/1"
_REQUIRED_KEYS = ("format", "n", "edges", "f")
_ALLOWED_KEYS = ("format", "n", "edges", "f", "labels")


class InvalidInstance(ValueError):
    """Raised when instance data are malformed or noncanonical."""


class UnsupportedInstance(ValueError):
    """Raised when a valid instance lies outside the active ExactFrac regime."""


def _validate_n(n: object) -> int:
    if type(n) is not int or n < 1:
        raise InvalidInstance("n must be a positive built-in int")
    return n


def _validate_f(n: int, f: object) -> tuple[int, ...]:
    if type(f) is not tuple or len(f) != n:
        raise InvalidInstance("f must be an exact tuple of length n")

    for value in f:
        if type(value) is not int or value < 1:
            raise InvalidInstance("every f value must be a positive built-in int")

    return f


def _validate_labels(
    n: int,
    labels: object,
) -> tuple[str | int, ...] | None:
    if labels is None:
        return None
    if type(labels) is not tuple or len(labels) != n:
        raise InvalidInstance("labels must be None or an exact tuple of length n")

    seen: set[str | int] = set()
    for label in labels:
        if type(label) is not str and type(label) is not int:
            raise InvalidInstance("labels must contain exact str or int values")
        if label in seen:
            raise InvalidInstance("labels must be pairwise distinct")
        seen.add(label)

    return labels


def _validate_record_shape(record: object) -> tuple[object, object, object]:
    if type(record) is not tuple or len(record) != 3:
        raise InvalidInstance("each edge record must be an exact three-entry tuple")
    return record


def _validate_record_values(
    n: int,
    record: object,
) -> Edge:
    raw_u, raw_v, raw_q = _validate_record_shape(record)

    if type(raw_u) is not int or type(raw_v) is not int:
        raise InvalidInstance("edge endpoints must be built-in ints")
    if raw_u < 0 or raw_u >= n or raw_v < 0 or raw_v >= n:
        raise InvalidInstance("edge endpoint is outside the vertex universe")
    if raw_u == raw_v:
        raise InvalidInstance("loops are not valid ExactFrac support edges")
    if type(raw_q) is not int or raw_q < 1:
        raise InvalidInstance("edge multiplicity must be a positive built-in int")

    return raw_u, raw_v, raw_q


def _validate_canonical_edges(n: int, edges: object) -> tuple[Edge, ...]:
    if type(edges) is not tuple:
        raise InvalidInstance("edges must be an exact tuple")
    if not edges:
        raise InvalidInstance("the canonical support must be nonempty")

    previous: tuple[int, int] | None = None
    for record in edges:
        u, v, _ = _validate_record_values(n, record)
        if u >= v:
            raise InvalidInstance("canonical edges require u < v")

        pair = (u, v)
        if previous is not None and pair <= previous:
            raise InvalidInstance("canonical edges must be strictly lexicographically ordered")
        previous = pair

    return edges


def _degree_tuple(n: int, edges: tuple[Edge, ...]) -> tuple[int, ...]:
    degrees = [0] * n
    for u, v, multiplicity in edges:
        degrees[u] += multiplicity
        degrees[v] += multiplicity
    return tuple(degrees)


def _check_active(f: tuple[int, ...], degrees: tuple[int, ...]) -> None:
    for value, degree in zip(f, degrees, strict=True):
        if value > degree:
            raise UnsupportedInstance("instance violates the active condition")


@dataclass(frozen=True, slots=True)
class Instance:
    """Immutable canonical ExactFrac graph instance."""

    n: int
    edges: tuple[Edge, ...]
    f: tuple[int, ...]
    labels: tuple[str | int, ...] | None = None

    def __post_init__(self) -> None:
        n = _validate_n(self.n)
        f = _validate_f(n, self.f)
        _validate_labels(n, self.labels)
        edges = _validate_canonical_edges(n, self.edges)
        _check_active(f, _degree_tuple(n, edges))

    @property
    def m(self) -> int:
        """Number of canonical support edges."""

        return len(self.edges)

    @property
    def support_edges(self) -> tuple[tuple[int, int], ...]:
        """Canonical support endpoints in edge-reference order."""

        return tuple((u, v) for u, v, _ in self.edges)

    @property
    def q(self) -> tuple[int, ...]:
        """Compact multiplicities in edge-reference order."""

        return tuple(multiplicity for _, _, multiplicity in self.edges)

    @property
    def Q(self) -> int:
        """Total compact multiplicity."""

        return sum(multiplicity for _, _, multiplicity in self.edges)

    @property
    def d_q(self) -> tuple[int, ...]:
        """Multiplicity-weighted vertex degrees."""

        return _degree_tuple(self.n, self.edges)

    @classmethod
    def from_records(
        cls,
        n: int,
        records: tuple[Edge, ...],
        f: tuple[int, ...],
        labels: tuple[str | int, ...] | None = None,
    ) -> Instance:
        """Validate and normalize raw compact edge records."""

        checked_n = _validate_n(n)
        checked_f = _validate_f(checked_n, f)
        checked_labels = _validate_labels(checked_n, labels)

        if type(records) is not tuple:
            raise InvalidInstance("records must be an exact tuple")
        if not records:
            raise InvalidInstance("the raw support must be nonempty")

        normalized: list[Edge] = []
        for record in records:
            u, v, multiplicity = _validate_record_values(checked_n, record)
            normalized.append((u, v, multiplicity) if u < v else (v, u, multiplicity))

        normalized.sort(key=lambda edge: (edge[0], edge[1]))
        iterator = iter(normalized)
        first_u, first_v, first_multiplicity = next(iterator)
        canonical: list[Edge] = []

        for u, v, multiplicity in iterator:
            if u == first_u and v == first_v:
                first_multiplicity += multiplicity
                continue

            canonical.append((first_u, first_v, first_multiplicity))
            first_u = u
            first_v = v
            first_multiplicity = multiplicity

        canonical.append((first_u, first_v, first_multiplicity))
        return cls(checked_n, tuple(canonical), checked_f, checked_labels)

    @classmethod
    def from_dict(cls, data: object) -> Instance:
        """Load one strict versioned canonical instance object."""

        if type(data) is not dict:
            raise InvalidInstance("serialized instance must be an exact dict")

        if any(key not in data for key in _REQUIRED_KEYS):
            raise InvalidInstance("serialized instance is missing a required key")
        if any(type(key) is not str or key not in _ALLOWED_KEYS for key in data):
            raise InvalidInstance("serialized instance contains an unknown key")
        if len(data) not in (4, 5):
            raise InvalidInstance("serialized instance has an invalid key set")
        if type(data["format"]) is not str or data["format"] != _FORMAT:
            raise InvalidInstance("unsupported instance format")

        n = _validate_n(data["n"])

        serialized_f = data["f"]
        if type(serialized_f) is not list:
            raise InvalidInstance("serialized f must be an exact list")
        f = _validate_f(n, tuple(serialized_f))

        if "labels" in data:
            serialized_labels = data["labels"]
            if type(serialized_labels) is not list:
                raise InvalidInstance("serialized labels must be an exact list")
            labels = _validate_labels(n, tuple(serialized_labels))
        else:
            labels = None

        serialized_edges = data["edges"]
        if type(serialized_edges) is not list:
            raise InvalidInstance("serialized edges must be an exact list")
        if not serialized_edges:
            raise InvalidInstance("the serialized support must be nonempty")

        converted: list[Edge] = []
        for record in serialized_edges:
            if type(record) is not list:
                raise InvalidInstance("serialized edge records must be exact lists")
            if len(record) != 3:
                raise InvalidInstance("serialized edge records must have three entries")
            converted.append((record[0], record[1], record[2]))

        return cls(n, tuple(converted), f, labels)

    def to_dict(self) -> dict[str, object]:
        """Return a detached JSON-ready canonical instance object."""

        data: dict[str, object] = {
            "format": _FORMAT,
            "n": self.n,
            "edges": [[u, v, multiplicity] for u, v, multiplicity in self.edges],
            "f": list(self.f),
        }
        if self.labels is not None:
            data["labels"] = list(self.labels)
        return data
