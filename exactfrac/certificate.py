"""Detached certificates and exact bytes for admissibility and raw attainment.

DESIGN 4.14 owns this object/encoding boundary, not an optimality proof or a
byte decoder. Closed witness helpers validate original compact coordinates;
the independent checker is a later unit. No solver is invoked here.
"""

from __future__ import annotations

from .instance import Instance
from .shore import shore_from_list, shore_to_list
from .solve import SolveResult
from .witness import ExactValue, Witness, dense_y_to_sparse, sparse_y_to_dense, witness_value

__all__ = ("build_certificate", "serialize_certificate")

_FORMAT = "exactfrac-certificate/1"
_EMPTY_KEYS = ("format", "empty", "N", "D")
_FULL_KEYS = (*_EMPTY_KEYS, "U", "y")


def _require_instance(instance: Instance) -> None:
    if type(instance) is not Instance:
        raise ValueError("instance must be an exact Instance")


def _require_empty(instance: Instance, numerator: int, denominator: int) -> None:
    # The active-instance constructor supplies the hypotheses of lem:empty.
    if instance.Q != 1 or numerator != 0 or denominator != 1:
        raise ValueError("Empty requires Q == 1 and the literal value (0, 1)")


def _require_attainment(value: ExactValue, numerator: int, denominator: int) -> None:
    if type(value) is not ExactValue:
        raise RuntimeError("witness_value violated its exact return-type promise")
    if numerator != value.N or denominator != value.D:
        raise ValueError("the supplied raw pair is not the witness's literal value")


def build_certificate(instance: Instance, result: SolveResult) -> dict[str, object]:
    """Build a fresh certificate from normally constructed closed records.

    Any admissible, literally attaining witness is accepted, including suboptimal
    and zero-valued witnesses. Raised dependency exceptions propagate unchanged.
    """
    _require_instance(instance)
    if type(result) is not SolveResult:
        raise ValueError("result must be an exact SolveResult")

    numerator, denominator = result.value.N, result.value.D
    witness = result.witness
    if witness is None:
        _require_empty(instance, numerator, denominator)
        return {"format": _FORMAT, "empty": True, "N": numerator, "D": denominator}

    value = witness_value(instance, witness)
    _require_attainment(value, numerator, denominator)
    vertices = shore_to_list(instance.n, witness.U)
    if type(vertices) is not list or any(type(vertex) is not int for vertex in vertices):
        raise RuntimeError("shore_to_list violated its exact list/int promise")
    entries = dense_y_to_sparse(instance, witness.U, witness.y)
    if type(entries) is not list or any(
        type(entry) is not list
        or len(entry) != 2
        or any(type(item) is not int for item in entry)
        for entry in entries
    ):
        raise RuntimeError("dense_y_to_sparse violated its exact nested-list promise")

    return {
        "format": _FORMAT,
        "empty": False,
        "N": numerator,
        "D": denominator,
        "U": list(vertices),
        "y": [[edge_ref, count] for edge_ref, count in entries],
    }


def _validate_object(instance: Instance, certificate: dict[str, object]) -> None:
    """Validate headers before payloads, preserving closed-helper precedence."""
    if type(certificate) is not dict:
        raise ValueError("certificate must be an exact dict")
    if any(type(key) is not str for key in certificate):
        raise ValueError("certificate keys must be exact strs")
    if "format" not in certificate or "empty" not in certificate:
        raise ValueError("certificate requires format and empty")
    if type(certificate["format"]) is not str or certificate["format"] != _FORMAT:
        raise ValueError("unsupported certificate format")
    empty = certificate["empty"]
    if type(empty) is not bool:
        raise ValueError("empty must be an exact bool")
    keys = _EMPTY_KEYS if empty else _FULL_KEYS
    if len(certificate) != len(keys) or any(key not in certificate for key in keys):
        raise ValueError("certificate has an invalid case-specific key set")
    numerator, denominator = certificate["N"], certificate["D"]
    if type(numerator) is not int or numerator < 0:
        raise ValueError("N must be a nonnegative built-in int")
    if type(denominator) is not int or denominator <= 0:
        raise ValueError("D must be a positive built-in int")
    if empty:
        _require_empty(instance, numerator, denominator)
        return

    shore = shore_from_list(instance.n, certificate["U"])
    if type(shore) is not int:
        raise RuntimeError("shore_from_list violated its exact int promise")
    if shore == 0:
        raise ValueError("a nonempty certificate requires a nonempty shore")
    counts = sparse_y_to_dense(instance, shore, certificate["y"])
    if type(counts) is not tuple or len(counts) != instance.m:
        raise RuntimeError("sparse_y_to_dense violated its length-m tuple promise")
    witness = Witness(shore, counts)
    value = witness_value(instance, witness)
    _require_attainment(value, numerator, denominator)


def _decimal(value: int) -> bytes:
    """Encode a validated nonnegative integer using bounded nine-digit chunks.

    divmod is confined to representation conversion. Neither an interpreter-wide
    digit-limit change nor full-magnitude decimal conversion is necessary. The
    number of iterations depends on output length, never on expanded unit copies.
    """
    if value == 0:
        return b"0"
    chunks = []
    while value:
        value, remainder = divmod(value, 1_000_000_000)
        chunks.append(remainder)
    # Every converted integer is less than 10**9, including the leading chunk.
    leading = str(chunks.pop()).encode("ascii")
    trailing = b"".join(f"{chunk:09d}".encode("ascii") for chunk in reversed(chunks))
    return leading + trailing


def serialize_certificate(instance: Instance, certificate: dict[str, object]) -> bytes:
    """Revalidate an object and emit the unique /1 bytes, including one final LF.

    Input dict order is irrelevant; U and sparse y must already be canonical.
    This is not a byte decoder. Native resource failures are not translated into
    mathematical rejection or Empty, and no caller-owned object is modified.
    """
    _require_instance(instance)
    _validate_object(instance, certificate)
    empty = certificate["empty"]
    fields = [
        b'"format":"exactfrac-certificate/1"',
        b'"empty":' + (b"true" if empty else b"false"),
        b'"N":' + _decimal(certificate["N"]),
        b'"D":' + _decimal(certificate["D"]),
    ]
    if not empty:
        fields.append(b'"U":[' + b",".join(_decimal(vertex) for vertex in certificate["U"]) + b"]")
        pairs = (
            b"[" + _decimal(edge_ref) + b"," + _decimal(count) + b"]"
            for edge_ref, count in certificate["y"]
        )
        fields.append(b'"y":[' + b",".join(pairs) + b"]")
    return b"{" + b",".join(fields) + b"}\n"
