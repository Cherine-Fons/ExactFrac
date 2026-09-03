"""Stage-2A RED tests for the exact directed minimum-cut reference backend.

This module consumes only the preimplementation flow rulings and ORACLE-005 through
ORACLE-012 committed before ``exactfrac.flow`` exists.

Concrete Stage-2A interface frozen by this test unit:

``minimum_cut(n=..., source=..., sink=..., arcs=...)`` returns
``MinCutResult(value, source_shore, stats)``. The flow-local immutable stats expose
``augmentations``, ``bfs_scans``, and ``peak_generated_value``. No residual graph,
mutable backend object, wall-clock value, or certificate data is returned.

The first run of this file is intentionally RED at import time because
``exactfrac/flow.py`` does not yet exist. That missing-module failure is the required
preimplementation checkpoint, not a defect in this test file.
"""

from __future__ import annotations

import ast
import inspect
from collections import deque
from dataclasses import FrozenInstanceError, dataclass, fields
from fractions import Fraction

import pytest

import exactfrac.flow as flow

Arc = tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class _FlowOracle:
    """Machine-facing portion of one committed Stage-2A flow oracle."""

    label: str
    n: int
    source: int
    sink: int
    arcs: tuple[Arc, ...]
    value: int
    source_shore: int
    minimum_shores: tuple[int, ...]
    augmentations: int
    bfs_scans: int
    peak_generated_value: int


ORACLE_005 = _FlowOracle(
    label="ORACLE-005",
    n=4,
    source=1,
    sink=3,
    arcs=(),
    value=0,
    source_shore=0b0010,
    minimum_shores=(0b0010, 0b0011, 0b0110, 0b0111),
    augmentations=0,
    bfs_scans=0,
    peak_generated_value=0,
)

ORACLE_006 = _FlowOracle(
    label="ORACLE-006",
    n=3,
    source=0,
    sink=2,
    arcs=(
        (0, 1, 2),
        (0, 2, 1),
        (1, 2, 2),
    ),
    value=3,
    source_shore=0b001,
    minimum_shores=(0b001, 0b011),
    augmentations=2,
    bfs_scans=8,
    peak_generated_value=3,
)

ORACLE_007 = _FlowOracle(
    label="ORACLE-007",
    n=3,
    source=0,
    sink=2,
    arcs=(
        (0, 1, 0),
        (1, 2, 0),
    ),
    value=0,
    source_shore=0b001,
    minimum_shores=(0b001, 0b011),
    augmentations=0,
    bfs_scans=1,
    peak_generated_value=0,
)

ORACLE_008 = _FlowOracle(
    label="ORACLE-008",
    n=4,
    source=0,
    sink=3,
    arcs=(
        (0, 1, 2),
        (1, 2, 1),
        (3, 2, 7),
    ),
    value=0,
    source_shore=0b0111,
    minimum_shores=(0b0111,),
    augmentations=0,
    bfs_scans=5,
    peak_generated_value=7,
)

ORACLE_009_RAW_ARCS: tuple[Arc, ...] = (
    (1, 2, 4),
    (0, 1, 2),
    (1, 1, 7),
    (0, 2, 1),
    (0, 1, 3),
    (0, 1, 0),
)

ORACLE_009_NORMALIZED_ARCS: tuple[Arc, ...] = (
    (0, 1, 5),
    (0, 2, 1),
    (1, 2, 4),
)

ORACLE_009 = _FlowOracle(
    label="ORACLE-009",
    n=3,
    source=0,
    sink=2,
    arcs=ORACLE_009_RAW_ARCS,
    value=5,
    source_shore=0b011,
    minimum_shores=(0b011,),
    augmentations=2,
    bfs_scans=10,
    peak_generated_value=5,
)

ORACLE_010 = _FlowOracle(
    label="ORACLE-010",
    n=6,
    source=0,
    sink=5,
    arcs=(
        (0, 1, 1),
        (0, 2, 1),
        (1, 3, 1),
        (1, 4, 1),
        (2, 3, 1),
        (3, 5, 1),
        (4, 5, 1),
    ),
    value=2,
    source_shore=0b000001,
    minimum_shores=(0b000001, 0b000101, 0b001101, 0b001111, 0b011111),
    augmentations=2,
    bfs_scans=24,
    peak_generated_value=2,
)

BASE_ORACLES = (
    ORACLE_005,
    ORACLE_006,
    ORACLE_007,
    ORACLE_008,
    ORACLE_009,
    ORACLE_010,
)

MAGNITUDE_BITS = (0, 1, 7, 31, 127, 511)


# ---------------------------------------------------------------------------
# Independent test-side directed-cut machinery; never calls exactfrac.flow
# ---------------------------------------------------------------------------


def _normalize_arcs_independently(arcs: tuple[Arc, ...]) -> tuple[Arc, ...]:
    """Apply the committed loop/parallel policy independently of the backend."""

    records = sorted(arc for arc in arcs if arc[0] != arc[1])
    normalized: list[Arc] = []

    for u, v, capacity in records:
        if normalized and normalized[-1][0:2] == (u, v):
            _, _, previous_capacity = normalized[-1]
            normalized[-1] = (u, v, previous_capacity + capacity)
        else:
            normalized.append((u, v, capacity))

    return tuple(normalized)


def _eligible_source_shores(n: int, source: int, sink: int) -> tuple[int, ...]:
    """Enumerate every source-containing, sink-avoiding shore by bitmask."""

    source_bit = 1 << source
    sink_bit = 1 << sink

    return tuple(
        shore
        for shore in range(1 << n)
        if shore & source_bit and not shore & sink_bit
    )


def _directed_cut_capacity(arcs: tuple[Arc, ...], shore: int) -> int:
    """Compute a directed out-cut directly from the supplied original records."""

    return sum(
        capacity
        for u, v, capacity in arcs
        if shore & (1 << u) and not shore & (1 << v)
    )


def _enumerated_minimum_cuts(
    n: int,
    source: int,
    sink: int,
    arcs: tuple[Arc, ...],
) -> tuple[int, tuple[int, ...]]:
    """Return the exact minimum value and complete minimizing-shore family."""

    capacities = {
        shore: _directed_cut_capacity(arcs, shore)
        for shore in _eligible_source_shores(n, source, sink)
    }
    minimum_value = min(capacities.values())
    minimum_shores = tuple(
        shore for shore, capacity in capacities.items() if capacity == minimum_value
    )

    return minimum_value, minimum_shores


def _least_shore(minimum_shores: tuple[int, ...]) -> int:
    """Return the unique minimizing shore contained in every other minimizer."""

    least = tuple(
        shore
        for shore in minimum_shores
        if all(shore & other == shore for other in minimum_shores)
    )

    assert len(least) == 1
    return least[0]


def _solve(oracle: _FlowOracle) -> flow.MinCutResult:
    """Invoke only the frozen public Stage-2A interface."""

    return flow.minimum_cut(
        n=oracle.n,
        source=oracle.source,
        sink=oracle.sink,
        arcs=oracle.arcs,
    )


def _forward_only_greedy_value(
    n: int,
    source: int,
    sink: int,
    arcs: tuple[Arc, ...],
) -> int:
    """Deliberately omit reverse residual arcs to expose ORACLE-010's trap.

    This is not a competing max-flow implementation. It is an intentionally
    defective test-side process that follows the pinned shortest-path order but
    only decreases original forward capacities. ORACLE-010 proves that this
    process gets stuck at value one, whereas correct residual cancellation
    reaches value two.
    """

    normalized = _normalize_arcs_independently(arcs)
    residual = [capacity for _, _, capacity in normalized]
    outgoing: list[list[int]] = [[] for _ in range(n)]

    for arc_index, (u, _, _) in enumerate(normalized):
        outgoing[u].append(arc_index)

    total = 0

    while True:
        parent_arc = [-1] * n
        reached = [False] * n
        reached[source] = True
        queue = deque([source])

        while queue and not reached[sink]:
            u = queue.popleft()

            for arc_index in outgoing[u]:
                _, v, _ = normalized[arc_index]

                if residual[arc_index] <= 0 or reached[v]:
                    continue

                reached[v] = True
                parent_arc[v] = arc_index
                queue.append(v)

                if v == sink:
                    break

        if not reached[sink]:
            return total

        path: list[int] = []
        vertex = sink

        while vertex != source:
            arc_index = parent_arc[vertex]
            assert arc_index >= 0
            path.append(arc_index)
            vertex = normalized[arc_index][0]

        bottleneck = min(residual[arc_index] for arc_index in path)

        for arc_index in path:
            residual[arc_index] -= bottleneck

        total += bottleneck


# ---------------------------------------------------------------------------
# R9 public result surface and exact integer output
# ---------------------------------------------------------------------------


def test_minimum_cut_result_surface_is_minimal_immutable_and_exact() -> None:
    """R9: return only exact cut data and immutable deterministic flow stats."""

    result = _solve(ORACLE_006)

    assert isinstance(result, flow.MinCutResult)
    assert tuple(field.name for field in fields(result)) == (
        "value",
        "source_shore",
        "stats",
    )
    assert tuple(field.name for field in fields(result.stats)) == (
        "augmentations",
        "bfs_scans",
        "peak_generated_value",
    )

    assert type(result.value) is int
    assert type(result.source_shore) is int
    assert type(result.stats.augmentations) is int
    assert type(result.stats.bfs_scans) is int
    assert type(result.stats.peak_generated_value) is int

    assert not hasattr(result, "residual")
    assert not hasattr(result, "adjacency")
    assert not hasattr(result, "wall_clock_s")
    assert not hasattr(result.stats, "wall_clock_s")

    with pytest.raises((FrozenInstanceError, AttributeError)):
        result.value = 0  # type: ignore[misc]

    with pytest.raises((FrozenInstanceError, AttributeError)):
        result.stats.augmentations = 0  # type: ignore[misc]


# ---------------------------------------------------------------------------
# FL2-FL8 / FL10 — committed exact values, shores, traces, and counters
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("oracle", BASE_ORACLES, ids=lambda oracle: oracle.label.lower())
def test_committed_flow_oracle_results_are_exact(oracle: _FlowOracle) -> None:
    """Consume the machine-facing results of ORACLE-005 through ORACLE-010."""

    result = _solve(oracle)

    assert result.value == oracle.value
    assert result.source_shore == oracle.source_shore
    assert result.stats.augmentations == oracle.augmentations
    assert result.stats.bfs_scans == oracle.bfs_scans
    assert result.stats.peak_generated_value == oracle.peak_generated_value

    assert result.source_shore & (1 << oracle.source)
    assert not result.source_shore & (1 << oracle.sink)
    assert result.source_shore >> oracle.n == 0


@pytest.mark.parametrize("oracle", BASE_ORACLES, ids=lambda oracle: oracle.label.lower())
def test_every_tiny_catalog_network_matches_independent_cut_enumeration(
    oracle: _FlowOracle,
) -> None:
    """FL9: enumerate all eligible shores without consulting the backend."""

    enumerated_value, minimum_shores = _enumerated_minimum_cuts(
        oracle.n,
        oracle.source,
        oracle.sink,
        oracle.arcs,
    )
    result = _solve(oracle)

    assert enumerated_value == oracle.value
    assert minimum_shores == oracle.minimum_shores
    assert result.value == enumerated_value
    assert result.source_shore in minimum_shores
    assert result.source_shore == _least_shore(minimum_shores)
    assert _directed_cut_capacity(oracle.arcs, result.source_shore) == result.value


def test_oracle_005_zero_arc_totalization_is_not_a_search() -> None:
    """FL2: E=0 returns the least zero cut without invoking BFS."""

    result = _solve(ORACLE_005)

    assert result.value == 0
    assert result.source_shore == 1 << ORACLE_005.source
    assert result.stats.augmentations == 0
    assert result.stats.bfs_scans == 0
    assert result.stats.peak_generated_value == 0


def test_oracle_007_zero_capacities_do_not_collapse_to_the_zero_arc_branch() -> None:
    """FL4: positive residual support size still produces one failed search."""

    assert len(ORACLE_007.arcs) == 2
    assert all(capacity == 0 for _, _, capacity in ORACLE_007.arcs)

    result = _solve(ORACLE_007)

    assert result.value == 0
    assert result.source_shore == 0b001
    assert result.stats.augmentations == 0
    assert result.stats.bfs_scans == 1


def test_oracle_008_preserves_directed_cut_and_original_reverse_arc_semantics() -> None:
    """FL5/FL7: the sink-to-2 arc enters the shore and creates no 2-to-sink capacity."""

    result = _solve(ORACLE_008)

    assert result.value == 0
    assert result.source_shore == 0b0111
    assert _directed_cut_capacity(ORACLE_008.arcs, result.source_shore) == 0

    entering_arc = (3, 2, 7)
    assert entering_arc in ORACLE_008.arcs
    assert result.source_shore & (1 << entering_arc[1])
    assert not result.source_shore & (1 << entering_arc[0])

    # The unused forward residual capacity seven is still an initialized
    # generated residual quantity and therefore fixes the peak at seven.
    assert result.stats.peak_generated_value == 7


def test_oracle_009_raw_parallel_records_normalize_to_the_same_exact_result() -> None:
    """FL1/FL3: validate, delete loops, aggregate ordered pairs, then sort."""

    assert _normalize_arcs_independently(ORACLE_009_RAW_ARCS) == (
        ORACLE_009_NORMALIZED_ARCS
    )

    raw_result = flow.minimum_cut(
        n=3,
        source=0,
        sink=2,
        arcs=ORACLE_009_RAW_ARCS,
    )
    normalized_result = flow.minimum_cut(
        n=3,
        source=0,
        sink=2,
        arcs=ORACLE_009_NORMALIZED_ARCS,
    )
    reordered_result = flow.minimum_cut(
        n=3,
        source=0,
        sink=2,
        arcs=tuple(reversed(ORACLE_009_RAW_ARCS)),
    )

    assert raw_result == normalized_result == reordered_result
    assert raw_result.value == 5
    assert raw_result.source_shore == 0b011
    assert raw_result.stats.augmentations == 2
    assert raw_result.stats.bfs_scans == 10
    assert raw_result.stats.peak_generated_value == 5


def test_oracle_010_requires_created_reverse_residual_capacity() -> None:
    """FL8: the pinned first path traps any process that cannot cancel flow."""

    assert _forward_only_greedy_value(
        ORACLE_010.n,
        ORACLE_010.source,
        ORACLE_010.sink,
        ORACLE_010.arcs,
    ) == 1

    result = _solve(ORACLE_010)

    assert result.value == 2
    assert result.source_shore == 0b000001
    assert result.stats.augmentations == 2
    assert result.stats.bfs_scans == 24


@pytest.mark.parametrize("oracle", BASE_ORACLES, ids=lambda oracle: oracle.label.lower())
def test_results_and_counters_are_repeatably_deterministic(oracle: _FlowOracle) -> None:
    """FL10: no environmental or wall-clock quantity affects result equality."""

    first = _solve(oracle)
    second = _solve(oracle)
    third = _solve(oracle)

    assert first == second == third


# ---------------------------------------------------------------------------
# FL1 / ORACLE-012 — flow-local validation and rejection taxonomy
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param(
            {"n": True, "source": 0, "sink": 1, "arcs": ()},
            id="boolean-n",
        ),
        pytest.param(
            {"n": 2.0, "source": 0, "sink": 1, "arcs": ()},
            id="float-n",
        ),
        pytest.param(
            {"n": 2, "source": False, "sink": 1, "arcs": ()},
            id="boolean-source",
        ),
        pytest.param(
            {"n": 2, "source": Fraction(0, 1), "sink": 1, "arcs": ()},
            id="fraction-source",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": True, "arcs": ()},
            id="boolean-sink",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": "1", "arcs": ()},
            id="string-sink",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": []},
            id="outer-list",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ([0, 1, 1],)},
            id="record-list",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((False, 1, 1),)},
            id="boolean-tail",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((0, 1.0, 1),)},
            id="float-head",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((0, 1, True),)},
            id="boolean-capacity",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((0, 1, 1.0),)},
            id="float-capacity",
        ),
        pytest.param(
            {
                "n": 2,
                "source": 0,
                "sink": 1,
                "arcs": ((0, 1, Fraction(1, 1)),),
            },
            id="fraction-capacity",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((0, 1, "1"),)},
            id="string-capacity",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((0, 0, 1.0),)},
            id="invalid-loop-type-before-deletion",
        ),
    ],
)
def test_flow_layer_type_violations_raise_type_error(kwargs: dict[str, object]) -> None:
    """ORACLE-012: exact Python integer and tuple requirements are enforced."""

    with pytest.raises(TypeError):
        flow.minimum_cut(**kwargs)


@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param(
            {"n": 1, "source": 0, "sink": 0, "arcs": ()},
            id="n-below-two",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 0, "arcs": ()},
            id="equal-terminals",
        ),
        pytest.param(
            {"n": 2, "source": -1, "sink": 1, "arcs": ()},
            id="negative-source",
        ),
        pytest.param(
            {"n": 2, "source": 2, "sink": 1, "arcs": ()},
            id="source-out-of-range",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": -1, "arcs": ()},
            id="negative-sink",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 2, "arcs": ()},
            id="sink-out-of-range",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((-1, 1, 1),)},
            id="negative-tail",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((0, 2, 1),)},
            id="head-out-of-range",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((),)},
            id="empty-record",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((0, 1),)},
            id="short-record",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((0, 1, 1, 2),)},
            id="long-record",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((0, 1, -1),)},
            id="negative-capacity",
        ),
        pytest.param(
            {"n": 2, "source": 0, "sink": 1, "arcs": ((0, 0, -1),)},
            id="negative-loop-before-deletion",
        ),
    ],
)
def test_flow_layer_value_and_structure_violations_raise_value_error(
    kwargs: dict[str, object],
) -> None:
    """ORACLE-012: structurally or numerically invalid exact inputs are rejected."""

    with pytest.raises(ValueError):
        flow.minimum_cut(**kwargs)


# ---------------------------------------------------------------------------
# FL11 — exact arithmetic and zero-safe generated-number accounting
# ---------------------------------------------------------------------------


def test_flow_correctness_path_contains_no_float_fraction_or_true_division() -> None:
    """FL11: backend decisions and values remain exact integer operations."""

    source = inspect.getsource(flow)
    tree = ast.parse(source)

    float_literals = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, float)
    ]
    float_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "float"
    ]
    fraction_imports = [
        node
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.Import)
            and any(alias.name == "fractions" for alias in node.names)
        )
        or (isinstance(node, ast.ImportFrom) and node.module == "fractions")
    ]
    fraction_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "Fraction"
    ]
    true_divisions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
    ]
    tolerance_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and (
            (isinstance(node.func, ast.Name) and node.func.id == "isclose")
            or (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "isclose"
            )
        )
    ]

    assert float_literals == []
    assert float_calls == []
    assert fraction_imports == []
    assert fraction_calls == []
    assert true_divisions == []
    assert tolerance_calls == []


@pytest.mark.parametrize("oracle", BASE_ORACLES, ids=lambda oracle: oracle.label.lower())
def test_zero_safe_number_bound_on_every_fixed_catalog_oracle(
    oracle: _FlowOracle,
) -> None:
    """FL11: independently verify both input and generated-value inequalities."""

    normalized = _normalize_arcs_independently(oracle.arcs)
    capacities = tuple(capacity for _, _, capacity in normalized)
    arc_count = len(normalized)
    capacity_sum = sum(capacities)
    maximum_capacity = max((0, *capacities))
    capacity_bits = maximum_capacity.bit_length()
    arc_count_log_ceiling = arc_count.bit_length()

    assert 1 + capacity_sum <= (arc_count + 1) * (maximum_capacity + 1)
    assert (arc_count + 1) * (maximum_capacity + 1) <= (
        (arc_count + 1) * (1 << capacity_bits)
    )

    result = _solve(oracle)
    peak = result.stats.peak_generated_value

    assert 0 <= peak <= capacity_sum
    assert peak.bit_length() <= capacity_bits + arc_count_log_ceiling


# ---------------------------------------------------------------------------
# FL12 / ORACLE-011 — fixed support, varying capacity magnitude
# ---------------------------------------------------------------------------


def test_one_arc_magnitude_family_has_constant_structural_trace() -> None:
    """ORACLE-011: capacity bit length grows without magnitude-driven iteration."""

    structural_trace: tuple[int, int, int] | None = None

    for b in MAGNITUDE_BITS:
        capacity = 1 << b
        arcs = ((0, 1, capacity),)
        result = flow.minimum_cut(n=2, source=0, sink=1, arcs=arcs)

        assert result.value == capacity
        assert result.source_shore == 0b01
        assert result.stats.augmentations == 1
        assert result.stats.bfs_scans == 2
        assert result.stats.peak_generated_value == capacity
        assert result.stats.peak_generated_value.bit_length() == b + 1

        enumerated_value, minimum_shores = _enumerated_minimum_cuts(
            2,
            0,
            1,
            arcs,
        )
        assert enumerated_value == capacity
        assert minimum_shores == (0b01,)

        current_trace = (
            result.source_shore,
            result.stats.augmentations,
            result.stats.bfs_scans,
        )

        if structural_trace is None:
            structural_trace = current_trace
        else:
            assert current_trace == structural_trace

        arc_count = 1
        maximum_capacity = capacity
        capacity_bits = maximum_capacity.bit_length()

        assert 1 + capacity <= (arc_count + 1) * (maximum_capacity + 1)
        assert (arc_count + 1) * (maximum_capacity + 1) <= (
            (arc_count + 1) * (1 << capacity_bits)
        )
        assert result.stats.peak_generated_value.bit_length() <= (
            capacity_bits + arc_count.bit_length()
        )
