"""Exact fixed-parameter branch minima over complete prepared atomic covers.

This is alg:branch-min, with DESIGN section 4.9's parameter-free preparation
and one lazy original network per query. The returned residual is B*c-A*h,
not a ratio optimum or a global density certificate. Diagnostics are separate.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ._telemetry import _tap_int, _tap_pair
from .families import AtomicFamily, enumerate_atomic_families
from .instance import Instance
from .parity_cut import lift_source_shore, minimum_parity_cut, reduce_atomic_family
from .rational import RawPair, residual_numerator, validate_pair
from .shore import validate_shore
from .sign_routing import (
    SignRoutedNetwork,
    branch_coefficients,
    build_sign_routed_network,
    recover_objective,
)
from .witness import shore_b_q, shore_d_q, shore_f

__all__ = (
    "BranchOracleContext",
    "BranchOracleResult",
    "BranchOracleStats",
    "exact_branch_min",
)


@dataclass(frozen=True, slots=True)
class BranchOracleContext:
    """Retain an exact Instance and its complete parameter-independent cover."""

    instance: Instance
    families: tuple[tuple[AtomicFamily, ...], ...] = field(init=False)

    def __post_init__(self) -> None:
        if type(self.instance) is not Instance:
            raise ValueError("instance must be an exact production Instance")
        object.__setattr__(self, "families", enumerate_atomic_families(self.instance))


@dataclass(frozen=True, slots=True)
class BranchOracleResult:
    """Original shore and raw source terms; construction alone certifies no minimum."""

    shore: int
    c: int
    h: int
    residual: int

    def __post_init__(self) -> None:
        if type(self.shore) is not int or self.shore <= 0:
            raise ValueError("shore must be a positive built-in int")
        if type(self.c) is not int:
            raise ValueError("c must be a built-in int")
        if type(self.h) is not int or self.h <= 0:
            raise ValueError("h must be a positive built-in int")
        if type(self.residual) is not int:
            raise ValueError("residual must be a built-in int")


@dataclass(frozen=True, slots=True)
class BranchOracleStats:
    """Query-only counts and flow diagnostics, never selection authority."""

    atomic_families_examined: int
    atomic_families_feasible: int
    parity_cut_calls: int
    ordinary_min_cut_calls: int
    flow_augmentations: int
    flow_bfs_scans: int
    flow_peak_generated_value: int

    def __post_init__(self) -> None:
        for value in (
            self.atomic_families_examined,
            self.atomic_families_feasible,
            self.parity_cut_calls,
            self.ordinary_min_cut_calls,
            self.flow_augmentations,
            self.flow_bfs_scans,
            self.flow_peak_generated_value,
        ):
            if type(value) is not int or value < 0:
                raise ValueError("statistics must be nonnegative built-in ints")

    @property
    def max_flow_calls(self) -> int:
        """The closed parity backend uses one flow for each ordinary cut."""
        return self.ordinary_min_cut_calls


def _source_terms(instance: Instance, shore: int, branch: int) -> tuple[int, int]:
    """Re-evaluate prop:branch-transform from original records, not cut shifts."""
    s = shore_f(instance, shore)
    b = shore_b_q(instance, shore)
    d = shore_d_q(instance, shore)
    if branch == 0:
        in_domain = _tap_int((_tap_int(s + b)) & 1)
        c, h = _tap_int(_tap_int(s + b) - 1), _tap_int(_tap_int(d + 1) - s)
    elif branch == 1:
        in_domain = not (_tap_int((_tap_int(s + b)) & 1)) and b >= 1 and d > s
        c, h = _tap_int(_tap_int(s + b) - 2), _tap_int(d - s)
    elif branch == 2:
        in_domain = (_tap_int(s & 1)) and s >= 3
        c, h = _tap_int(b - d), _tap_int(s - 1)
    else:
        in_domain = not (_tap_int(s & 1)) and b >= 1
        c, h = _tap_int(_tap_int(b - d) - 2), s
    if not in_domain or h <= 0:
        raise RuntimeError("lifted candidate violates the source domain or positive h")
    return _tap_pair((c, h))


def exact_branch_min(
    context: BranchOracleContext,
    branch: int,
    parameter: RawPair,
) -> tuple[BranchOracleResult | None, BranchOracleStats]:
    """Minimize the exact raw residual over one whole source branch domain.

    Empty descriptors are skipped before graph work. Each feasible descriptor
    is reduced, minimized, lifted, checked, and independently re-evaluated from
    original records. Equal residuals retain the incumbent; no sign-based early
    exit is valid here. Closed-dependency exceptions propagate unchanged.
    """
    if type(context) is not BranchOracleContext:
        raise ValueError("context must be an exact BranchOracleContext")
    if type(branch) is not int or branch not in (0, 1, 2, 3):
        raise ValueError("branch must be a built-in int in (0, 1, 2, 3)")
    validate_pair(parameter)

    instance = context.instance
    families = context.families[branch]
    network: SignRoutedNetwork | None = None
    best: BranchOracleResult | None = None
    examined = feasible = ordinary_calls = augmentations = scans = peak = 0

    for family in families:
        examined += 1
        if not family.is_nonempty:
            continue
        feasible += 1
        if network is None:
            coefficients = branch_coefficients(instance, branch, parameter)
            network = build_sign_routed_network(instance, coefficients)

        problem = reduce_atomic_family(network, family)
        if problem is None:
            raise RuntimeError("nonempty atomic family produced no reduced problem")
        cut, diagnostics = minimum_parity_cut(problem)
        if cut is None:
            raise RuntimeError("nonempty atomic family produced no parity minimum")

        shore = lift_source_shore(problem, cut.source_shore)
        validate_shore(instance.n, shore)
        if (
            shore == 0
            or (_tap_int(shore & family.I)) != family.I
            or (_tap_int(shore & family.O)) != 0
            or (_tap_int(_tap_int((_tap_int(shore & family.T)).bit_count()) & 1)) != family.pi
        ):
            raise RuntimeError("lifted original shore violates its atomic family")

        c, h = _source_terms(instance, shore, branch)
        raw = residual_numerator(parameter, c, h)
        recovered = recover_objective(network, cut.cut_value)
        if raw != recovered:
            raise RuntimeError("original raw residual and recovered cut objective differ")

        if best is None or raw < best.residual:
            best = BranchOracleResult(shore, c, h, raw)

        ordinary_calls += diagnostics.mincut_calls
        augmentations += diagnostics.flow_augmentations
        scans += diagnostics.flow_bfs_scans
        peak = max(peak, diagnostics.flow_peak_generated_value)

    return best, BranchOracleStats(
        examined, feasible, feasible, ordinary_calls, augmentations, scans, peak,
    )
