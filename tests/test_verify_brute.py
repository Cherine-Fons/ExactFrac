"""Definition-level tests for the independent ExactFrac brute verifier.

This module tests only responsibilities owned by ``exactfrac_verify.brute``.

In particular, production input normalization, aggregation, malformed-input
taxonomy, and the ``UnsupportedInstance`` API belong to the later
``exactfrac.instance`` unit and are deliberately not specified here.

E1 is therefore discharged in two layers:

1. this brute-verifier unit proves the verifier-owned mathematical empty-state
   behavior: exact value (0, 1), no witness, no dummy shore, and no dummy y;
2. the later production instance layer proves that the same valid active input
   is constructed successfully and is not confused with UnsupportedInstance.

The brute verifier is intentionally solver-blind. Nothing here imports or
depends on ``exactfrac``, transformed branches, atomic-family decompositions,
cut reductions, Newton updates, or either production branch solver.
"""

from __future__ import annotations

import ast
import inspect
import subprocess
import sys
from fractions import Fraction

import pytest

from exactfrac_verify import brute

# ---------------------------------------------------------------------------
# Hand-derived seed fixtures
# ---------------------------------------------------------------------------


def _oracle_001_instance() -> brute.BruteInstance:
    """Valid active Q=1 single-edge instance from ORACLE-001."""

    return brute.BruteInstance(
        n=2,
        edges=((0, 1, 1),),
        f=(1, 1),
    )


def _oracle_002_instance() -> brute.BruteInstance:
    """Triangle instance carrying the ORACLE-002 local unit witness."""

    return brute.BruteInstance(
        n=3,
        edges=(
            (0, 1, 1),
            (0, 2, 1),
            (1, 2, 1),
        ),
        f=(1, 1, 2),
    )


def _oracle_003_instance() -> brute.BruteInstance:
    """Compact q=2 instance carrying the ORACLE-003 local witness."""

    return brute.BruteInstance(
        n=2,
        edges=((0, 1, 2),),
        f=(1, 2),
    )



def _oracle_004_instance() -> brute.BruteInstance:
    """Global-tie instance from independently committed ORACLE-004."""

    return brute.BruteInstance(
        n=2,
        edges=((0, 1, 2),),
        f=(1, 1),
    )


# ---------------------------------------------------------------------------
# Independent expanded-copy reference used only by the tests
# ---------------------------------------------------------------------------


def _expanded_copy_optimum(instance: brute.BruteInstance) -> Fraction:
    """Exhaust literal unit copies independently of compact-y enumeration.

    Every compact support edge ``(u, v, q_e)`` is expanded here into ``q_e``
    distinct unit copies.

    The test then enumerates every subset of the distinct crossing copies
    directly. Different subsets with the same cardinality are intentionally
    retained: they are distinct feasible objects in the expanded-copy model,
    even though the objective depends only on their selected total. This
    preserves independence from the compact count-vector representation.

    The comparator does not call ``iter_boundary_y`` or any other
    compact-selection routine from the verifier.

    This comparator is intentionally tiny-instance only.
    """

    copies: list[tuple[int, int]] = []

    for u, v, multiplicity in instance.edges:
        for _ in range(multiplicity):
            copies.append((u, v))

    best: Fraction | None = None

    for shore in range(1, 1 << instance.n):
        internal_copy_count = 0
        crossing_copies: list[int] = []

        for copy_index, (u, v) in enumerate(copies):
            u_inside = bool(shore & (1 << u))
            v_inside = bool(shore & (1 << v))

            if u_inside and v_inside:
                internal_copy_count += 1
            elif u_inside != v_inside:
                crossing_copies.append(copy_index)

        f_shore = sum(
            instance.f[vertex]
            for vertex in range(instance.n)
            if shore & (1 << vertex)
        )

        for selected_mask in range(1 << len(crossing_copies)):
            selected_total = selected_mask.bit_count()
            admissibility_total = f_shore + selected_total

            if admissibility_total < 3:
                continue

            if admissibility_total % 2 == 0:
                continue

            numerator = 2 * (internal_copy_count + selected_total)
            denominator = admissibility_total - 1
            candidate = Fraction(numerator, denominator)

            if best is None or candidate > best:
                best = candidate

    return Fraction(0, 1) if best is None else best


# ---------------------------------------------------------------------------
# TP2 / B1 — verifier isolation
# ---------------------------------------------------------------------------


def test_brute_verifier_does_not_import_solver_package() -> None:
    """The verifier may not acquire a code dependency on ``exactfrac``."""

    source = inspect.getsource(brute)
    tree = ast.parse(source)

    imported_modules: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)

        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported_modules.append(node.module)

    forbidden = [
        name
        for name in imported_modules
        if name == "exactfrac" or name.startswith("exactfrac.")
    ]

    assert forbidden == []

    script = """
import sys
import exactfrac_verify.brute

for name in sys.modules:
    if name == "exactfrac" or name.startswith("exactfrac."):
        raise SystemExit(1)

raise SystemExit(0)
"""

    completed = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


# ---------------------------------------------------------------------------
# TP3 / B5 — no floating-point correctness path
# ---------------------------------------------------------------------------


def test_brute_correctness_path_contains_no_float_arithmetic() -> None:
    """Exact verifier logic must not use float, tolerance, or bare ``/``.

    This is a Stage-1 module-local hardening rule. Integer ``/`` would create a
    float in Python; exact quotients in this verifier must instead be built
    explicitly with ``Fraction(numerator, denominator)``.
    """

    source = inspect.getsource(brute)
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

    true_divisions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
    ]

    assert float_literals == []
    assert float_calls == []
    assert true_divisions == []


# ---------------------------------------------------------------------------
# Minimal canonical verifier-side fixture container
# ---------------------------------------------------------------------------


def test_seed_fixture_metadata_is_exact() -> None:
    """The verifier sees canonical mathematical data, not external raw records."""

    first = _oracle_001_instance()

    assert first.n == 2
    assert first.edges == ((0, 1, 1),)
    assert first.f == (1, 1)
    assert first.degrees == (1, 1)
    assert first.total_multiplicity == 1
    assert first.full_mask == 0b11

    second = _oracle_002_instance()

    assert second.edges == (
        (0, 1, 1),
        (0, 2, 1),
        (1, 2, 1),
    )
    assert second.f == (1, 1, 2)
    assert second.degrees == (2, 2, 2)
    assert second.total_multiplicity == 3


# ---------------------------------------------------------------------------
# Shore representation — S1/S2/S4/S5/S6 and B2
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("instance", "expected"),
    [
        pytest.param(
            _oracle_001_instance(),
            [0b01, 0b10, 0b11],
            id="n2-includes-whole-set",
        ),
        pytest.param(
            _oracle_002_instance(),
            [0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111],
            id="n3-all-seven-nonempty-shores",
        ),
    ],
)
def test_nonempty_shore_enumeration_is_complete_and_deterministic(
    instance: brute.BruteInstance,
    expected: list[int],
) -> None:
    """B2: enumerate every nonempty subset, including the whole vertex set."""

    shores = list(brute.iter_nonempty_shores(instance))

    assert shores == expected
    assert shores == list(range(1, 1 << instance.n))
    assert len(shores) == (1 << instance.n) - 1

    # The whole-vertex-set shore must be enumerated. It is not prefiltered
    # merely because it may later fail admissibility.
    assert shores[-1] == instance.full_mask


def test_shore_round_trip_membership_cardinality_and_complement() -> None:
    instance = _oracle_002_instance()
    shore = brute.shore_from_list(instance, [0, 2])

    assert shore == 0b101
    assert shore.bit_count() == 2

    assert bool(shore & (1 << 0))
    assert not bool(shore & (1 << 1))
    assert bool(shore & (1 << 2))

    assert brute.shore_to_list(instance, shore) == [0, 2]

    complement = brute.shore_complement(instance, shore)

    assert complement == 0b010
    assert brute.shore_to_list(instance, complement) == [1]


def test_out_of_range_shore_bits_are_rejected() -> None:
    instance = _oracle_002_instance()
    out_of_range = 1 << instance.n

    with pytest.raises(ValueError):
        brute.shore_to_list(instance, out_of_range)



def test_bare_python_complement_is_not_a_valid_shore() -> None:
    """S4: complement must be relative to full_mask, never bare ``~U``."""

    instance = _oracle_002_instance()
    shore = brute.shore_from_list(instance, [0, 2])

    bare_complement = ~shore

    assert bare_complement < 0

    with pytest.raises(ValueError):
        brute.shore_to_list(instance, bare_complement)

    with pytest.raises(ValueError):
        brute.shore_complement(instance, bare_complement)


# ---------------------------------------------------------------------------
# B3 — boundary-only compact multiplicity enumeration
# ---------------------------------------------------------------------------


def test_boundary_y_enumeration_varies_only_crossing_edges() -> None:
    """For U={2} in ORACLE-002, e0 is internal to the complement."""

    instance = _oracle_002_instance()
    shore = brute.shore_from_list(instance, [2])

    selections = list(brute.iter_boundary_y(instance, shore))

    assert selections == [
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 1),
    ]

    for y in selections:
        assert y[0] == 0
        assert 0 <= y[1] <= 1
        assert 0 <= y[2] <= 1


def test_whole_vertex_shore_is_enumerated_with_zero_boundary_selection() -> None:
    """Whole-set shores are searched; their boundary simply has no choices."""

    instance = _oracle_001_instance()
    whole_shore = instance.full_mask

    assert whole_shore in list(brute.iter_nonempty_shores(instance))

    assert list(brute.iter_boundary_y(instance, whole_shore)) == [
        (0,),
    ]

    witness = brute.Witness(
        shore=whole_shore,
        y=(0,),
    )

    # ORACLE-001 has f(V)=2, so the whole-set pair is considered and then
    # rejected by admissibility. The shore itself is never skipped.
    assert not brute.witness_is_admissible(instance, witness)


def test_compact_multiplicity_enumerates_individually_selectable_counts() -> None:
    """q=2 means counts 0, 1, and 2 are independently attainable."""

    instance = _oracle_003_instance()
    shore = brute.shore_from_list(instance, [0])

    assert list(brute.iter_boundary_y(instance, shore)) == [
        (0,),
        (1,),
        (2,),
    ]


# ---------------------------------------------------------------------------
# B4 / applicable W1-W4 and W7 — exact witness admissibility
# ---------------------------------------------------------------------------


def test_lower_bound_guard_is_isolated() -> None:
    """TP4/B4: odd total 1 fails only the admissibility lower bound."""

    instance = _oracle_001_instance()

    witness = brute.Witness(
        shore=brute.shore_from_list(instance, [0]),
        y=(0,),
    )

    # Earlier guards all hold:
    # - nonempty in-range shore;
    # - correct dense-y length;
    # - exact integer count;
    # - boundary-supported count;
    # - count within 0..q_e.
    #
    # The total is f(U)+Y = 1, which is odd but below 3.
    assert not brute.witness_is_admissible(instance, witness)


def test_parity_guard_is_isolated() -> None:
    """TP4/B4: total 4 satisfies the lower bound but fails odd parity."""

    instance = _oracle_003_instance()

    witness = brute.Witness(
        shore=brute.shore_from_list(instance, [1]),
        y=(2,),
    )

    # Earlier guards all hold, and f(U)+Y = 2+2 = 4 >= 3.
    # Rejection is therefore specifically due to even parity.
    assert not brute.witness_is_admissible(instance, witness)


def test_noninteger_exact_count_is_not_admissible() -> None:
    """W2: dense compact counts must be Python integers."""

    instance = _oracle_002_instance()

    witness = brute.Witness(
        shore=brute.shore_from_list(instance, [2]),
        y=(0, Fraction(1, 1), 0),  # type: ignore[arg-type]
    )

    assert not brute.witness_is_admissible(instance, witness)


def test_oracle_002_witness_is_admissible_and_preserves_raw_value() -> None:
    """B7: verify the local unit witness without promoting it to a global oracle."""

    instance = _oracle_002_instance()

    witness = brute.Witness(
        shore=brute.shore_from_list(instance, [2]),
        y=(0, 1, 0),
    )

    assert brute.witness_is_admissible(instance, witness)

    # W7: raw witness-attaining value remains unreduced.
    assert brute.witness_raw_value(instance, witness) == (2, 2)

    # Mathematical comparison may use Fraction independently.
    assert brute.witness_ratio(instance, witness) == Fraction(1, 1)


def test_oracle_002_competitor_proves_local_witness_is_not_global() -> None:
    """The catalog competitor disproves optimality without asserting global value 2."""

    instance = _oracle_002_instance()

    unit_witness = brute.Witness(
        shore=brute.shore_from_list(instance, [2]),
        y=(0, 1, 0),
    )

    competitor = brute.Witness(
        shore=brute.shore_from_list(instance, [0, 1]),
        y=(0, 1, 0),
    )

    assert brute.witness_is_admissible(instance, unit_witness)
    assert brute.witness_is_admissible(instance, competitor)

    assert brute.witness_raw_value(instance, unit_witness) == (2, 2)
    assert brute.witness_raw_value(instance, competitor) == (4, 2)

    assert brute.witness_ratio(instance, unit_witness) == Fraction(1, 1)
    assert brute.witness_ratio(instance, competitor) == Fraction(2, 1)

    assert brute.witness_ratio(instance, competitor) > brute.witness_ratio(
        instance,
        unit_witness,
    )


@pytest.mark.parametrize(
    "witness",
    [
        pytest.param(
            brute.Witness(shore=0b100, y=(0, 0, 0)),
            id="fails-parity-lower-bound",
        ),
        pytest.param(
            brute.Witness(shore=0b100, y=(1, 1, 0)),
            id="nonboundary-coordinate-positive",
        ),
        pytest.param(
            brute.Witness(shore=0b100, y=(0, 2, 0)),
            id="count-exceeds-multiplicity",
        ),
        pytest.param(
            brute.Witness(shore=0b100, y=(0, -1, 0)),
            id="negative-count",
        ),
        pytest.param(
            brute.Witness(shore=0b000, y=(0, 1, 0)),
            id="empty-shore",
        ),
        pytest.param(
            brute.Witness(shore=0b100, y=(0, 1)),
            id="wrong-y-length",
        ),
    ],
)
def test_invalid_compact_witnesses_are_not_admissible(
    witness: brute.Witness,
) -> None:
    instance = _oracle_002_instance()

    assert not brute.witness_is_admissible(instance, witness)


# ---------------------------------------------------------------------------
# B6 / verifier-owned portion of E1 — genuine empty mathematical state
# ---------------------------------------------------------------------------


def test_oracle_001_brute_owned_empty_state() -> None:
    """Stage 1 discharges the mathematical part of E1.

    The production ``UnsupportedInstance`` versus malformed-input API distinction
    is intentionally deferred to ``exactfrac.instance``.
    """

    instance = _oracle_001_instance()

    assert instance.degrees == (1, 1)
    assert instance.f == (1, 1)
    assert instance.total_multiplicity == 1

    result = brute.brute_force(instance)

    assert result.value == (0, 1)
    assert result.witness is None


# ---------------------------------------------------------------------------
# B8 — ORACLE-003 compact witness cross-check
# ---------------------------------------------------------------------------


def test_oracle_003_compact_witness_is_admissible_and_attains_two() -> None:
    """The verifier sees a compact witness only; it has no H2 concept."""

    instance = _oracle_003_instance()

    witness = brute.Witness(
        shore=brute.shore_from_list(instance, [0]),
        y=(2,),
    )

    assert brute.witness_is_admissible(instance, witness)
    assert brute.witness_raw_value(instance, witness) == (4, 2)
    assert brute.witness_ratio(instance, witness) == Fraction(2, 1)


# ---------------------------------------------------------------------------
# B9 — independently established multiple global maximizers
# ---------------------------------------------------------------------------


def test_oracle_004_global_tie_and_deterministic_first_witness() -> None:
    """B9: global value is unique as a value, but the maximizing witness is not."""

    instance = _oracle_004_instance()

    witness_a = brute.Witness(
        shore=brute.shore_from_list(instance, [0]),
        y=(2,),
    )

    witness_b = brute.Witness(
        shore=brute.shore_from_list(instance, [1]),
        y=(2,),
    )

    assert witness_a != witness_b

    assert brute.witness_is_admissible(instance, witness_a)
    assert brute.witness_is_admissible(instance, witness_b)

    assert brute.witness_raw_value(instance, witness_a) == (4, 2)
    assert brute.witness_raw_value(instance, witness_b) == (4, 2)

    assert brute.witness_ratio(instance, witness_a) == Fraction(2, 1)
    assert brute.witness_ratio(instance, witness_b) == Fraction(2, 1)

    result = brute.brute_force(instance)

    assert Fraction(*result.value) == Fraction(2, 1)
    assert result.witness == witness_a

    # Increasing shore-mask enumeration sees {0} before {1}; strict
    # improvement only means the equal-valued second maximizer does not
    # replace the first. This is deterministic implementation behavior,
    # not a mathematical preference for witness A.
    assert result.witness != witness_b


# ---------------------------------------------------------------------------
# B5 / prop:expanded-equivalence — independent compact-vs-copy comparison
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "instance",
    [
        pytest.param(
            _oracle_001_instance(),
            id="oracle-001-empty",
        ),
        pytest.param(
            _oracle_002_instance(),
            id="oracle-002-triangle",
        ),
        pytest.param(
            _oracle_003_instance(),
            id="oracle-003-compact-q2",
        ),
        pytest.param(
            _oracle_004_instance(),
            id="oracle-004-global-tie",
        ),
    ],
)
def test_compact_expanded_agree(instance: brute.BruteInstance) -> None:
    """Compact exhaustive search agrees with literal unit-copy enumeration."""

    compact_result = brute.brute_force(instance)
    compact_ratio = Fraction(*compact_result.value)

    expanded_ratio = _expanded_copy_optimum(instance)

    assert compact_ratio == expanded_ratio

    if compact_result.witness is None:
        assert compact_ratio == Fraction(0, 1)
        return

    assert brute.witness_is_admissible(
        instance,
        compact_result.witness,
    )

    assert brute.witness_ratio(
        instance,
        compact_result.witness,
    ) == compact_ratio


# ---------------------------------------------------------------------------
# Minimum Stage-1 determinism obligation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "instance",
    [
        pytest.param(
            _oracle_001_instance(),
            id="empty",
        ),
        pytest.param(
            _oracle_002_instance(),
            id="triangle",
        ),
        pytest.param(
            _oracle_003_instance(),
            id="compact-q2",
        ),
        pytest.param(
            _oracle_004_instance(),
            id="global-tie",
        ),
    ],
)
def test_brute_force_is_repeatably_deterministic(
    instance: brute.BruteInstance,
) -> None:
    first = brute.brute_force(instance)
    second = brute.brute_force(instance)

    assert first == second