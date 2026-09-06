"""Unit 09 tests-first contract for exact raw rational-pair primitives."""

from __future__ import annotations

import ast
import importlib
import inspect
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

rational = importlib.import_module("exactfrac.rational")

EXPECTED_EXPORTS = (
    "RawPair",
    "compare_pairs",
    "make_pair",
    "pair_add_one",
    "pair_reflect",
    "pair_sign",
    "residual_numerator",
    "validate_pair",
)

NUMERATORS = (-3, -2, -1, 0, 1, 2, 3)
DENOMINATORS = (1, 2, 3, 4)
VALID_PAIRS = tuple((a, b) for a in NUMERATORS for b in DENOMINATORS)
SCALARS = (-2, -1, 0, 1, 2)
INVALID_DENOMINATORS = (0, -1, -3)
LARGE_EXPONENTS = (1, 2, 8, 64, 4096)


class IntSubclass(int):
    """Exact-type rejection control."""


class TupleSubclass(tuple):
    """Exact-type rejection control."""


class DuckSequence:
    """Sequence-like object that must not be accepted as a RawPair."""

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index: int) -> int:
        return (1, 2)[index]


class ExplosiveInt(int):
    """Detect positivity testing before exact-type rejection."""

    def __le__(self, other: object) -> bool:
        raise AssertionError("int subclass reached denominator comparison")



def _fraction(pair: tuple[int, int]) -> Fraction:
    return Fraction(pair[0], pair[1])



def _compare_expected(left: tuple[int, int], right: tuple[int, int]) -> int:
    left_cross = left[0] * right[1]
    right_cross = right[0] * left[1]
    return (left_cross > right_cross) - (left_cross < right_cross)



def _exact_value_error(callable_obj: object, *args: object) -> None:
    with pytest.raises(ValueError) as exc_info:
        callable_obj(*args)  # type: ignore[operator]
    assert type(exc_info.value) is ValueError



def _annotation_matches(annotation: object, expected: str) -> bool:
    if expected == "RawPair":
        return annotation == rational.RawPair or annotation == "RawPair"
    if expected == "int":
        return annotation is int or annotation == "int"
    if expected == "None":
        return annotation is None or annotation == "None"
    raise AssertionError(expected)



def _assert_signature(
    function: object,
    names: tuple[str, ...],
    annotations: tuple[str, ...],
    return_annotation: str,
) -> None:
    signature = inspect.signature(function)
    parameters = tuple(signature.parameters.values())
    assert tuple(parameter.name for parameter in parameters) == names
    assert all(
        parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
        for parameter in parameters
    )
    assert all(parameter.default is inspect.Parameter.empty for parameter in parameters)
    assert all(
        _annotation_matches(parameter.annotation, expected)
        for parameter, expected in zip(parameters, annotations, strict=True)
    )
    assert _annotation_matches(signature.return_annotation, return_annotation)



def _module_source() -> str:
    source_path = Path(rational.__file__).resolve()
    assert source_path.name == "rational.py"
    return source_path.read_text(encoding="utf-8")



def _is_set_expression(node: ast.AST, set_names: set[str]) -> bool:
    if isinstance(node, (ast.Set, ast.SetComp)):
        return True
    if isinstance(node, ast.Name):
        return node.id in set_names
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in {"set", "frozenset"}:
            return True
        if isinstance(node.func, ast.Attribute) and node.func.attr in {
            "copy",
            "difference",
            "intersection",
            "symmetric_difference",
            "union",
        }:
            return _is_set_expression(node.func.value, set_names)
    if isinstance(node, ast.BinOp) and isinstance(
        node.op,
        (ast.BitAnd, ast.BitOr, ast.BitXor, ast.Sub),
    ):
        return _is_set_expression(node.left, set_names) or _is_set_expression(
            node.right,
            set_names,
        )
    return False



def _assigned_set_names(tree: ast.AST) -> set[str]:
    set_names: set[str] = set()
    changed = True
    while changed:
        changed = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                value = node.value
                if value is None or not _is_set_expression(value, set_names):
                    continue
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Name) and target.id not in set_names:
                        set_names.add(target.id)
                        changed = True
    return set_names



def _iterators(tree: ast.AST) -> tuple[ast.AST, ...]:
    iterators: list[ast.AST] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.AsyncFor)):
            iterators.append(node.iter)
        elif isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            iterators.extend(generator.iter for generator in node.generators)
        elif isinstance(node, ast.YieldFrom):
            iterators.append(node.value)
    return tuple(iterators)



def test_rp1_public_surface_alias_and_signatures() -> None:
    assert rational.__all__ == EXPECTED_EXPORTS
    assert type(rational.__all__) is tuple
    assert rational.RawPair == tuple[int, int]

    _assert_signature(
        rational.make_pair,
        ("numerator", "denominator"),
        ("int", "int"),
        "RawPair",
    )
    _assert_signature(rational.validate_pair, ("pair",), ("RawPair",), "None")
    _assert_signature(
        rational.compare_pairs,
        ("left", "right"),
        ("RawPair", "RawPair"),
        "int",
    )
    _assert_signature(rational.pair_sign, ("pair",), ("RawPair",), "int")
    _assert_signature(rational.pair_add_one, ("pair",), ("RawPair",), "RawPair")
    _assert_signature(
        rational.pair_reflect,
        ("newton", "current"),
        ("RawPair", "RawPair"),
        "RawPair",
    )
    _assert_signature(
        rational.residual_numerator,
        ("parameter", "c", "h"),
        ("RawPair", "int", "int"),
        "int",
    )

    public_names = {
        name
        for name in vars(rational)
        if not name.startswith("_") and name != "annotations"
    }
    assert public_names == set(EXPECTED_EXPORTS)



def test_rp1_untagged_tuple_carrier_is_deliberate() -> None:
    edge_like_pair = (0, 1)
    assert rational.validate_pair(edge_like_pair) is None
    assert rational.pair_sign(edge_like_pair) == 0
    assert rational.compare_pairs(edge_like_pair, (0, 7)) == 0



def test_rp2_make_pair_literal_outputs_and_strict_denominators() -> None:
    rows = (
        (0, 1, (0, 1)),
        (0, 7, (0, 7)),
        (6, 8, (6, 8)),
        (-6, 8, (-6, 8)),
        (7, 1, (7, 1)),
        (-7, 1, (-7, 1)),
    )
    for numerator, denominator, expected in rows:
        observed = rational.make_pair(numerator, denominator)
        assert type(observed) is tuple
        assert observed == expected
        assert all(type(field) is int for field in observed)

    rejected = 0
    for numerator in NUMERATORS:
        for denominator in INVALID_DENOMINATORS:
            _exact_value_error(rational.make_pair, numerator, denominator)
            rejected += 1
    assert rejected == 21



def test_rp2_make_pair_exact_scalar_types_and_validation_order() -> None:
    invalid_scalars = (True, False, IntSubclass(1), 1.0, Fraction(1, 1), None)
    for value in invalid_scalars:
        _exact_value_error(rational.make_pair, value, 2)
        _exact_value_error(rational.make_pair, 1, value)

    _exact_value_error(rational.make_pair, 1, ExplosiveInt(2))
    _exact_value_error(rational.make_pair, True, ExplosiveInt(2))



def test_rp3_validate_pair_success_and_rejection_matrix() -> None:
    for pair in VALID_PAIRS:
        assert rational.validate_pair(pair) is None

    from exactfrac.witness import ExactValue, Witness

    invalid_pairs: tuple[object, ...] = (
        [1, 2],
        (1,),
        (1, 2, 3),
        TupleSubclass((1, 2)),
        (True, 2),
        (1, True),
        (IntSubclass(1), 2),
        (1, IntSubclass(2)),
        (1.0, 2),
        (1, 2.0),
        (Fraction(1, 1), 2),
        (1, Fraction(2, 1)),
        None,
        iter((1, 2)),
        DuckSequence(),
        (1, 0),
        (1, -1),
        ExactValue(1, 2),
        Witness(1, (0,)),
    )
    for pair in invalid_pairs:
        _exact_value_error(rational.validate_pair, pair)
        _exact_value_error(rational.pair_sign, pair)
        _exact_value_error(rational.pair_add_one, pair)
        _exact_value_error(rational.compare_pairs, pair, (1, 2))
        _exact_value_error(rational.compare_pairs, (1, 2), pair)
        _exact_value_error(rational.pair_reflect, pair, (1, 2))
        _exact_value_error(rational.pair_reflect, (1, 2), pair)
        _exact_value_error(rational.residual_numerator, pair, 1, 2)

    _exact_value_error(rational.validate_pair, (1, ExplosiveInt(2)))



def test_rp3_residual_scalar_exact_types() -> None:
    invalid_scalars = (True, False, IntSubclass(1), 1.0, Fraction(1, 1), None)
    for value in invalid_scalars:
        _exact_value_error(rational.residual_numerator, (1, 2), value, 3)
        _exact_value_error(rational.residual_numerator, (1, 2), 3, value)



def test_rp4_comparison_oracle_and_exact_output_type() -> None:
    rows = (
        ((2, 2), (1, 1), 0),
        ((0, 2), (0, 1), 0),
        ((-2, 2), (-1, 1), 0),
        ((12, 8), (3, 2), 0),
        ((3, 10), (2, 3), -1),
        ((2, 3), (3, 10), 1),
        ((1, 3), (1, 2), -1),
        ((-1, 3), (-1, 2), 1),
        ((5, 7), (4, 5), -1),
        ((-5, 7), (-4, 5), 1),
    )
    for left, right, expected in rows:
        observed = rational.compare_pairs(left, right)
        assert type(observed) is int
        assert observed == expected
        assert observed == _compare_expected(left, right)

    assert (3, 10) > (2, 3)
    assert rational.compare_pairs((3, 10), (2, 3)) == -1



def test_rp4_comparison_scale_invariance_and_huge_close_values() -> None:
    controls = (((2, 3), (5, 7)), ((-2, 3), (-5, 7)), ((2, 2), (1, 1)))
    for left, right in controls:
        expected = _compare_expected(left, right)
        for scale in (1, 2, 7, 4097):
            scaled_left = (scale * left[0], scale * left[1])
            scaled_right = (scale * right[0], scale * right[1])
            assert rational.compare_pairs(scaled_left, right) == expected
            assert rational.compare_pairs(left, scaled_right) == expected

    for exponent in LARGE_EXPONENTS:
        large = 1 << exponent
        left = (large + 1, large)
        right = (large, large - 1)
        assert rational.compare_pairs(left, right) == -1



def test_rp5_pair_sign_oracle_and_complete_validation() -> None:
    rows = (
        ((-9, 1), -1),
        ((-1, 4097), -1),
        ((0, 1), 0),
        ((0, 4097), 0),
        ((1, 4097), 1),
        ((9, 1), 1),
    )
    for pair, expected in rows:
        observed = rational.pair_sign(pair)
        assert type(observed) is int
        assert observed == expected

    _exact_value_error(rational.pair_sign, (1, 0))
    _exact_value_error(rational.pair_sign, (0, -7))



def test_rp6_pair_add_one_literal_oracle() -> None:
    rows = (
        ((-5, 7), (2, 7)),
        ((-7, 7), (0, 7)),
        ((6, 8), (14, 8)),
        ((0, 5), (5, 5)),
        ((11, 6), (17, 6)),
    )
    for pair, expected in rows:
        observed = rational.pair_add_one(pair)
        assert type(observed) is tuple
        assert observed == expected
        assert _fraction(observed) == _fraction(pair) + 1

    assert rational.pair_add_one((11, 6)) == (17, 6)
    accelerated_initialization = (11, 6)
    assert accelerated_initialization != rational.pair_add_one(accelerated_initialization)



def test_rp6_pair_add_one_large_cancellation_preserves_denominator() -> None:
    for exponent in LARGE_EXPONENTS:
        large = 1 << exponent
        assert rational.pair_add_one((-large, large)) == (0, large)



def test_rp7_pair_reflect_literal_oracle_and_roles() -> None:
    rows = (
        ((3, 5), (2, 7), (32, 35)),
        ((2, 7), (3, 5), (-1, 35)),
        ((5, 6), (1, 6), (54, 36)),
        ((2, 4), (3, 6), (12, 24)),
        ((1, 3), (2, 3), (0, 9)),
        ((1, 5), (1, 2), (-1, 10)),
    )
    for newton, current, expected in rows:
        observed = rational.pair_reflect(newton, current)
        assert type(observed) is tuple
        assert observed == expected
        assert _fraction(observed) == 2 * _fraction(newton) - _fraction(current)

    assert rational.pair_reflect((3, 5), (2, 7)) != rational.pair_reflect((2, 7), (3, 5))



def test_rp7_fixed_newton_recurrence_preserves_raw_growth() -> None:
    expected = ((1, 2), (7, 10), (25, 50), (175, 250), (625, 1250))
    current = expected[0]
    observed = [current]
    for next_expected in expected[1:]:
        current = rational.pair_reflect((3, 5), current)
        observed.append(current)
        assert current == next_expected
    assert tuple(observed) == expected



def test_rp7_large_symbolic_reflection() -> None:
    for exponent in LARGE_EXPONENTS:
        large = 1 << exponent
        newton = (large + 1, large)
        current = (large + 2, large + 1)
        expected = (large * large + 2 * large + 2, large * (large + 1))
        assert rational.pair_reflect(newton, current) == expected



def test_rp8_residual_oracle_sign_and_scaling_hazard() -> None:
    rows = (
        ((2, 3), 7, 5, 11, Fraction(11, 3)),
        ((2, 3), 4, 6, 0, Fraction(0, 1)),
        ((2, 3), 3, 5, -1, Fraction(-1, 3)),
        ((2, 3), -4, 0, -12, Fraction(-4, 1)),
        ((2, 3), 2, -3, 12, Fraction(4, 1)),
    )
    for parameter, c_value, h_value, raw_expected, fraction_expected in rows:
        observed = rational.residual_numerator(parameter, c_value, h_value)
        assert type(observed) is int
        assert observed == raw_expected
        assert Fraction(observed, parameter[1]) == fraction_expected

    base = rational.residual_numerator((2, 3), 7, 5)
    scaled = rational.residual_numerator((4, 6), 7, 5)
    assert base == 11
    assert scaled == 22
    assert Fraction(base, 3) == Fraction(scaled, 6)

    raw_first = rational.residual_numerator((1, 3), 1, 1)
    raw_second = rational.residual_numerator((7, 10), 1, 1)
    assert raw_first < raw_second
    assert Fraction(raw_first, 3) > Fraction(raw_second, 10)



def test_rp8_large_symbolic_residual() -> None:
    for exponent in LARGE_EXPONENTS:
        large = 1 << exponent
        parameter = (large + 1, large)
        assert rational.residual_numerator(parameter, large + 2, large + 3) == -2 * large - 3



def test_rp9_explicit_exactvalue_bridge_preserves_unit08_semantics() -> None:
    from exactfrac.witness import ExactValue, Witness

    left_value = ExactValue(2, 2)
    right_value = ExactValue(1, 1)
    zero_nonempty_value = ExactValue(0, 2)

    assert left_value != right_value
    assert rational.compare_pairs((left_value.N, left_value.D), (right_value.N, right_value.D)) == 0
    assert rational.compare_pairs((zero_nonempty_value.N, zero_nonempty_value.D), (0, 1)) == 0
    assert zero_nonempty_value == ExactValue(0, 2)

    _exact_value_error(rational.validate_pair, left_value)
    _exact_value_error(rational.pair_sign, left_value)
    _exact_value_error(rational.pair_add_one, left_value)
    _exact_value_error(rational.compare_pairs, left_value, (1, 1))
    _exact_value_error(rational.pair_reflect, left_value, (1, 1))
    _exact_value_error(rational.residual_numerator, left_value, 1, 1)

    witness = Witness(1, (0,))
    _exact_value_error(rational.validate_pair, witness)

    constructed = ExactValue(*rational.make_pair(12, 8))
    assert constructed == ExactValue(12, 8)



def test_rp10_finite_independent_arithmetic_corpus() -> None:
    sign_counts = {-1: 0, 0: 0, 1: 0}
    add_one_sign_counts = {-1: 0, 0: 0, 1: 0}
    comparison_counts = {-1: 0, 0: 0, 1: 0}
    reflection_counts = {-1: 0, 0: 0, 1: 0}
    residual_counts = {-1: 0, 0: 0, 1: 0}

    factory_success = 0
    validation_success = 0
    sign_evaluations = 0
    add_one_evaluations = 0
    comparison_evaluations = 0
    reflection_evaluations = 0
    residual_evaluations = 0

    for pair in VALID_PAIRS:
        assert rational.make_pair(*pair) == pair
        factory_success += 1

        assert rational.validate_pair(pair) is None
        validation_success += 1

        sign = rational.pair_sign(pair)
        assert sign == (pair[0] > 0) - (pair[0] < 0)
        sign_counts[sign] += 1
        sign_evaluations += 1

        added = rational.pair_add_one(pair)
        assert added == (pair[0] + pair[1], pair[1])
        assert _fraction(added) == _fraction(pair) + 1
        add_sign = (added[0] > 0) - (added[0] < 0)
        add_one_sign_counts[add_sign] += 1
        add_one_evaluations += 1

    factory_rejections = 0
    for numerator in NUMERATORS:
        for denominator in INVALID_DENOMINATORS:
            _exact_value_error(rational.make_pair, numerator, denominator)
            factory_rejections += 1

    for left in VALID_PAIRS:
        for right in VALID_PAIRS:
            compare = rational.compare_pairs(left, right)
            expected_compare = (_fraction(left) > _fraction(right)) - (
                _fraction(left) < _fraction(right)
            )
            assert compare == expected_compare
            comparison_counts[compare] += 1
            comparison_evaluations += 1

            reflected = rational.pair_reflect(left, right)
            assert reflected == (
                2 * left[0] * right[1] - right[0] * left[1],
                left[1] * right[1],
            )
            assert _fraction(reflected) == 2 * _fraction(left) - _fraction(right)
            reflected_sign = (reflected[0] > 0) - (reflected[0] < 0)
            reflection_counts[reflected_sign] += 1
            reflection_evaluations += 1

    for parameter in VALID_PAIRS:
        for c_value in SCALARS:
            for h_value in SCALARS:
                raw = rational.residual_numerator(parameter, c_value, h_value)
                expected_raw = parameter[1] * c_value - parameter[0] * h_value
                assert raw == expected_raw
                assert Fraction(raw, parameter[1]) == Fraction(c_value, 1) - (
                    _fraction(parameter) * Fraction(h_value, 1)
                )
                raw_sign = (raw > 0) - (raw < 0)
                residual_counts[raw_sign] += 1
                residual_evaluations += 1

    assert len(VALID_PAIRS) == 28
    assert len({_fraction(pair) for pair in VALID_PAIRS}) == 19
    assert factory_success == 28
    assert factory_rejections == 21
    assert validation_success == 28
    assert sign_evaluations == 28
    assert add_one_evaluations == 28
    assert comparison_evaluations == 784
    assert reflection_evaluations == 784
    assert residual_evaluations == 700
    assert sign_counts == {-1: 12, 0: 4, 1: 12}
    assert add_one_sign_counts == {-1: 3, 0: 3, 1: 22}
    assert comparison_counts == {-1: 364, 0: 56, 1: 364}
    assert reflection_counts == {-1: 370, 0: 44, 1: 370}
    assert residual_counts == {-1: 310, 0: 80, 1: 310}

    total = (
        factory_success
        + factory_rejections
        + validation_success
        + sign_evaluations
        + add_one_evaluations
        + comparison_evaluations
        + reflection_evaluations
        + residual_evaluations
    )
    assert total == 2401



def test_rp11_source_exactness_and_dependency_isolation() -> None:
    source = _module_source()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest.fail(f"unexpected import: {ast.unparse(node)}")
        if isinstance(node, ast.ImportFrom):
            allowed_future = node.module == "__future__" and [
                alias.name for alias in node.names
            ] == ["annotations"]
            assert allowed_future, ast.unparse(node)
        if isinstance(node, ast.Constant):
            assert type(node.value) is not float
        if isinstance(node, ast.BinOp):
            assert not isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod))
        if isinstance(node, ast.While):
            pytest.fail("magnitude-driven while loop is forbidden")

    forbidden_calls = {
        "Decimal",
        "Fraction",
        "__import__",
        "compile",
        "eval",
        "exec",
        "float",
        "gcd",
        "hash",
        "isclose",
        "round",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_calls
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr != "bit_length"

    identifiers = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    assert not ({"Decimal", "Fraction", "decimal", "fractions", "math"} & identifiers)



def test_rp11_no_recursion_dynamic_range_or_set_iteration() -> None:
    tree = ast.parse(_module_source())
    set_names = _assigned_set_names(tree)

    for iterator in _iterators(tree):
        assert not _is_set_expression(iterator, set_names)
        if (
            isinstance(iterator, ast.Call)
            and isinstance(iterator.func, ast.Name)
            and iterator.func.id == "range"
        ):
            assert iterator.args
            assert all(
                    isinstance(argument, ast.Constant)
                    and type(argument.value) is int
                    for argument in iterator.args
                )

    for function in (
        node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ):
        for node in ast.walk(function):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id != function.name



def test_rp11_fresh_process_import_isolation_and_package_root() -> None:
    import exactfrac

    for name in EXPECTED_EXPORTS:
        assert name not in vars(exactfrac)

    script = """
import sys
before = set(sys.modules)
import exactfrac.rational as module
new = sorted(
    name
    for name in set(sys.modules) - before
    if name == "exactfrac"
    or name.startswith("exactfrac.")
    or name == "exactfrac_verify"
    or name.startswith("exactfrac_verify.")
)
print(module.__file__)
print("|".join(new))
"""
    completed = subprocess.run(
        [sys.executable, "-c", script],
        check=True,
        capture_output=True,
        text=True,
    )
    lines = completed.stdout.strip().splitlines()
    assert len(lines) == 2
    assert Path(lines[0]).resolve() == Path(rational.__file__).resolve()
    assert lines[1].split("|") == ["exactfrac", "exactfrac.rational"]



def test_rp12_large_integer_outputs_remain_exact_raw_pairs() -> None:
    for exponent in LARGE_EXPONENTS:
        large = 1 << exponent

        made = rational.make_pair(large + 1, large)
        assert made == (large + 1, large)
        assert all(type(field) is int for field in made)

        assert rational.compare_pairs((large + 1, large), (large, large - 1)) == -1
        assert rational.pair_add_one((-large, large)) == (0, large)

        reflected = rational.pair_reflect(
            (large + 1, large),
            (large + 2, large + 1),
        )
        assert reflected == (
            large * large + 2 * large + 2,
            large * (large + 1),
        )
        assert all(type(field) is int for field in reflected)

        residual = rational.residual_numerator(
            (large + 1, large),
            large + 2,
            large + 3,
        )
        assert type(residual) is int
        assert residual == -2 * large - 3
