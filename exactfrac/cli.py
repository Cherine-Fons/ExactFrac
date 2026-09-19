"""Offline certificate-producing and certificate-checking command entry point.

DESIGN 4.16 owns the grammar, byte streams and composition order. Mathematical
validation remains in the closed Instance, solver, emitter and independent checker.
Verification establishes admissibility and literal attainment, not optimality.
"""

from __future__ import annotations

import json
import sys

__all__ = ("main",)

_SOLVE_USAGE = (
    b"usage: python -m exactfrac.cli solve [--solver Standard|Accelerated] INSTANCE\n"
)
_VERIFY_USAGE = b"usage: python -m exactfrac.cli verify INSTANCE CERTIFICATE\n"
_ROOT_HELP = (
    _SOLVE_USAGE + _VERIFY_USAGE
    + b"INSTANCE or CERTIFICATE may be - for stdin; verify permits at most one -.\n"
)
_SOLVE_HELP = (
    _SOLVE_USAGE
    + b"Writes one exact certificate to stdout; default solver: Accelerated.\n"
)
_VERIFY_HELP = (
    _VERIFY_USAGE
    + b"Success is silent; verifies admissibility and raw attainment, not optimality.\n"
)
_USAGE_ERROR = b"exactfrac: invalid command line; use --help\n"


def _parse(argv: list[str]) -> tuple[str, str, list[str]] | None:
    """Classify the entire token sequence without dependency imports or I/O."""
    if not argv or any(not token or "\0" in token for token in argv):
        return None
    if len(argv) == 1 and argv[0] in ("-h", "--help"):
        return "root-help", "", []
    command = argv[0]
    if command not in ("solve", "verify"):
        return None
    if len(argv) == 2 and argv[1] in ("-h", "--help"):
        return command + "-help", "", []

    operands: list[str] = []
    selection = "Accelerated"
    selected = False
    options = True
    position = 1
    while position < len(argv):
        token = argv[position]
        if options and token == "--":
            options = False
        elif options and token.startswith("-") and token != "-":
            if command != "solve" or token != "--solver" or selected:
                return None
            position += 1
            if position == len(argv) or argv[position] not in ("Standard", "Accelerated"):
                return None
            selection = argv[position]
            selected = True
        else:
            operands.append(token)
        position += 1
    if command == "solve":
        if len(operands) != 1:
            return None
    elif len(operands) != 2 or operands == ["-", "-"]:
        return None
    return command, selection, operands


def _read(operand: str) -> bytes:
    """Acquire one operand, closing only a named-file handle owned here."""
    if operand == "-":
        raw = sys.stdin.buffer.read()
    else:
        with open(operand, "rb") as stream:
            raw = stream.read()
    if type(raw) is not bytes:
        raise RuntimeError("input reader violated its exact bytes promise")
    return raw


def _write(stream: object, raw: bytes) -> None:
    """Complete positive short writes, then flush; never retry an exception."""
    pending = memoryview(raw)
    position = 0
    while position < len(pending):
        count = stream.write(pending[position:])
        if type(count) is not int or not 1 <= count <= len(pending) - position:
            raise RuntimeError("binary writer violated its progress promise")
        position += count
    if stream.flush() is not None:
        raise RuntimeError("binary stream violated its flush return promise")


def _decode_instance(raw: bytes) -> object:
    """Decode only syntax, preserving keys, integer values and graph ordering.

    Integer conversion works in at most nine-digit chunks. Schema and active
    validation are deliberately left to Instance.from_dict, never reproduced here.
    """
    from exactfrac.instance import InvalidInstance

    if raw.startswith(b"\xef\xbb\xbf"):
        raise InvalidInstance("instance UTF-8 BOM is not permitted")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidInstance("instance is not valid UTF-8") from exc

    def integer(token: str) -> int:
        negative = token.startswith("-")
        digits = token[1:] if negative else token
        if (
            not digits
            or any(char not in "0123456789" for char in digits)
            or (len(digits) > 1 and digits[0] == "0")
            or (negative and digits == "0")
        ):
            raise InvalidInstance("instance number is not a canonical integer")
        value = 0
        for start in range(0, len(digits), 9):
            chunk = digits[start:start + 9]
            value = value * (10 ** len(chunk)) + int(chunk)
        return -value if negative else value

    def noninteger(_token: str) -> object:
        raise InvalidInstance("instance numeric tokens must be integers")

    def object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise InvalidInstance("instance contains a duplicate decoded key")
            result[key] = value
        return result

    try:
        return json.loads(
            text,
            parse_int=integer,
            parse_float=noninteger,
            parse_constant=noninteger,
            object_pairs_hook=object_pairs,
        )
    except json.JSONDecodeError as exc:
        raise InvalidInstance("instance is not one valid JSON document") from exc


def _solve_command(operand: str, selection: str) -> None:
    """Compose each closed operation once; self-check before stdout access."""
    from exactfrac.certificate import build_certificate, serialize_certificate
    from exactfrac.instance import Instance
    from exactfrac.solve import SolveResult, SolveStats, solve
    from exactfrac_verify.check import verify_certificate

    raw = _read(operand)
    instance = Instance.from_dict(_decode_instance(raw))
    if type(instance) is not Instance:
        raise RuntimeError("Instance.from_dict violated its exact Instance promise")
    returned = solve(instance, selection)
    if type(returned) is not tuple or len(returned) != 2:
        raise RuntimeError("solve violated its exact two-entry tuple promise")
    result, stats = returned
    if type(result) is not SolveResult or type(stats) is not SolveStats:
        raise RuntimeError("solve violated its exact result/stats promises")
    if type(stats.branch_solver) is not str or stats.branch_solver != selection:
        raise RuntimeError("solve violated its selected-route promise")
    certificate = build_certificate(instance, result)
    if type(certificate) is not dict:
        raise RuntimeError("build_certificate violated its exact dict promise")
    emitted = serialize_certificate(instance, certificate)
    if type(emitted) is not bytes:
        raise RuntimeError("serialize_certificate violated its exact bytes promise")
    if verify_certificate(raw, emitted) is not None:
        raise RuntimeError("independent checker violated its None return promise")
    _write(sys.stdout.buffer, emitted)


def _verify_command(operands: list[str]) -> None:
    """Read in operand order and verify once, without any producer dependency."""
    from exactfrac_verify.check import verify_certificate

    instance = _read(operands[0])
    certificate = _read(operands[1])
    if verify_certificate(instance, certificate) is not None:
        raise RuntimeError("independent checker violated its None return promise")


def main(argv: list[str] | None = None) -> int:
    """Run one command; return 0/2 only after the prescribed completion.

    Invalid Python argv types raise ValueError. Operational and closed dependency
    exceptions propagate unchanged, except the two narrowly translated decoders.
    """
    arguments = sys.argv[1:] if argv is None else argv
    if type(arguments) is not list or any(type(token) is not str for token in arguments):
        raise ValueError("argv must be None or an exact list of exact strings")
    parsed = _parse(arguments)
    if parsed is None:
        _write(sys.stderr.buffer, _USAGE_ERROR)
        return 2
    command, selection, operands = parsed
    if command == "root-help":
        _write(sys.stdout.buffer, _ROOT_HELP)
    elif command == "solve-help":
        _write(sys.stdout.buffer, _SOLVE_HELP)
    elif command == "verify-help":
        _write(sys.stdout.buffer, _VERIFY_HELP)
    elif command == "solve":
        _solve_command(operands[0], selection)
    else:
        _verify_command(operands)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
