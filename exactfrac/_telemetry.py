"""Context-local identity observations; no mathematical layer or runtime I/O.

Disabled taps return their original objects. Active taps retain only fixed-size
peak records; no execution trace or mathematical decision is stored here.
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field


@dataclass(slots=True)
class _Peaks:
    numerator: int = 0
    denominator: int = 0
    integer: int = 0

    def observe(self, value: int) -> int:
        if type(value) is not int:
            raise RuntimeError("an integer observation received a non-integer")
        bits = max(1, abs(value).bit_length())
        self.integer = max(self.integer, bits)
        return bits

    def pair(self, numerator: int, denominator: int) -> None:
        if type(denominator) is not int or denominator <= 0:
            raise RuntimeError("an observed raw pair has an invalid denominator")
        self.numerator = max(self.numerator, self.observe(numerator))
        self.denominator = max(self.denominator, self.observe(denominator))


@dataclass(slots=True)
class _Recorder:
    nonbranch: _Peaks = field(default_factory=_Peaks)
    branches: tuple[_Peaks, ...] = field(default_factory=lambda: tuple(_Peaks() for _ in range(4)))
    active_branch: int | None = None
    prepared: tuple[int, int, int, int] | None = None
    visited: list[int] = field(default_factory=list)

    def bucket(self) -> _Peaks:
        return self.nonbranch if self.active_branch is None else self.branches[self.active_branch]


_ACTIVE: ContextVar[_Recorder | None] = ContextVar("exactfrac_integer_observations", default=None)


@contextmanager
def _measurement():
    """Start one synchronous measurement; nested calls reject before a second solve."""
    if _ACTIVE.get() is not None:
        raise ValueError("nested measured solves are not supported")
    recorder = _Recorder()
    token = _ACTIVE.set(recorder)
    try:
        yield recorder
    finally:
        _ACTIVE.reset(token)


def _tap_int(value: int) -> int:
    recorder = _ACTIVE.get()
    if recorder is not None:
        recorder.bucket().observe(value)
    return value


def _tap_pair(value: tuple[int, int]) -> tuple[int, int]:
    recorder = _ACTIVE.get()
    if recorder is not None:
        if type(value) is not tuple or len(value) != 2:
            raise RuntimeError("a raw-pair tap received an invalid pair")
        recorder.bucket().pair(value[0], value[1])
    return value


def _tap_numerator(value: int, denominator: int) -> int:
    recorder = _ACTIVE.get()
    if recorder is not None:
        recorder.bucket().pair(value, denominator)
    return value


def _observe_ints(*values: int) -> None:
    recorder = _ACTIVE.get()
    if recorder is not None:
        bucket = recorder.bucket()
        for value in values:
            bucket.observe(value)


def _observe_pair_values(numerator: int, denominator: int) -> None:
    recorder = _ACTIVE.get()
    if recorder is not None:
        recorder.bucket().pair(numerator, denominator)


def _record_prepared_sizes(d0: int, d1: int, d2: int, d3: int) -> None:
    recorder = _ACTIVE.get()
    if recorder is not None:
        sizes = (d0, d1, d2, d3)
        if any(type(size) is not int or size < 0 for size in sizes):
            raise RuntimeError("invalid prepared-cover cardinalities")
        if recorder.prepared is not None or recorder.active_branch is not None:
            raise RuntimeError("preparation must be recorded once outside branch work")
        recorder.prepared = sizes


@contextmanager
def _branch_scope(branch: int):
    recorder = _ACTIVE.get()
    if recorder is None:
        yield
        return
    if type(branch) is not int or branch not in (0, 1, 2, 3):
        raise RuntimeError("invalid observed branch index")
    if recorder.active_branch is not None or branch in recorder.visited:
        raise RuntimeError("branch scopes must be separate single visits")
    if branch != len(recorder.visited):
        raise RuntimeError("branch scopes must follow the fixed original order")
    previous = recorder.active_branch
    recorder.active_branch = branch
    recorder.visited.append(branch)
    try:
        recorder.bucket().observe(branch)
        yield
    finally:
        recorder.active_branch = previous
