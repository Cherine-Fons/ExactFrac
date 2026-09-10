"""Unit 13 tests-first Standard contract: DESIGN 4.10 / ST1--ST20.

ORACLE-083--096 tables below were transcribed from the committed human catalogue
at 013e5e5. No private JSON, prior consuming test, or future implementation supplies
expectations. Tiny original-domain enumeration is deliberately test-side only.
These tests do not implement Accelerated or certify global density/optimality.
"""

from __future__ import annotations

import ast
import hashlib
import importlib
import inspect
import json
import os
import subprocess
import sys
from collections import Counter
from dataclasses import MISSING, FrozenInstanceError, fields, is_dataclass
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import get_type_hints

import pytest

from exactfrac import oracle as oracle_module
from exactfrac import rational as rational_module
from exactfrac.instance import Instance
from exactfrac.oracle import BranchOracleContext, BranchOracleResult, BranchOracleStats
from exactfrac.rational import RawPair
from exactfrac.witness import ExactValue

# This unconditional import deliberately causes the intended missing-module RED.
# There is no importorskip, import fallback, placeholder, or dummy production file.
_BRANCH = importlib.import_module("exactfrac.branch")

# U13_INPUTS: name, n, edges, f, d_q, Q
U13_INPUTS = (
    ('Q1', 2, ((0, 1, 1),), (1, 1), (1, 1), 1),
    ('DOUBLE', 2, ((0, 1, 2),), (1, 1), (2, 2), 2),
    ('UNEQUAL', 2, ((0, 1, 2),), (2, 1), (2, 2), 2),
    ('EQUALITY', 3, ((0, 1, 1), (0, 2, 1), (1, 2, 1)), (2, 2, 2), (2, 2, 2), 3),
    ('WTRI', 3, ((0, 1, 1), (0, 2, 1), (1, 2, 1)), (1, 1, 1), (2, 2, 2), 3),
    ('ODDFULL', 3, ((0, 1, 1), (0, 2, 1), (1, 2, 1)), (2, 2, 1), (2, 2, 2), 3),
    ('TIECARD', 3, ((0, 2, 1), (1, 2, 1)), (1, 1, 2), (1, 1, 2), 2),
    ('RICH',
     5,
     ((0, 2, 2), (1, 2, 2), (2, 4, 1), (3, 4, 1)),
     (1, 1, 1, 1, 2),
     (2, 2, 5, 1, 2),
     6),
    ('MIXED',
     4,
     ((0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 4), (1, 3, 2), (2, 3, 5)),
     (2, 3, 4, 5),
     (6, 8, 12, 8),
     17),
    ('ZERO', 2, ((0, 1, 3),), (3, 3), (3, 3), 3),
    ('SHIFT', 2, ((0, 1, 4),), (4, 4), (4, 4), 4),
    ('LOW0', 4, ((0, 1, 9), (0, 2, 1), (1, 3, 1), (2, 3, 8)), (3, 3, 7, 5), (10, 10, 9, 9), 19),
    ('LOW1',
     5,
     ((0, 2, 9), (0, 4, 6), (1, 3, 3), (2, 4, 1), (3, 4, 1)),
     (11, 1, 1, 3, 4),
     (15, 3, 10, 4, 8),
     20),
    ('HIGH2', 3, ((0, 1, 1), (0, 2, 1), (1, 2, 2)), (2, 1, 3), (2, 3, 3), 4),
    ('HIGH3', 3, ((0, 1, 1), (0, 2, 1), (1, 2, 2)), (1, 1, 3), (2, 3, 3), 4),
    ('NONMAX', 3, ((0, 2, 1), (1, 2, 2)), (1, 1, 1), (1, 2, 3), 3),
    ('CHOICE', 3, ((0, 2, 2), (1, 2, 2)), (1, 1, 4), (2, 2, 4), 4),
)

# U13_SHORES: input, U, s, e, b, d, in_D0_D1_D2_D3, domain_pairs
U13_SHORES = (
    ('Q1', 1, 1, 0, 1, 1, (False, False, False, False), (None, None, None, None)),
    ('Q1', 2, 1, 0, 1, 1, (False, False, False, False), (None, None, None, None)),
    ('Q1', 3, 2, 1, 0, 2, (False, False, False, False), (None, None, None, None)),
    ('DOUBLE', 1, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('DOUBLE', 2, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('DOUBLE', 3, 2, 2, 0, 4, (False, False, False, False), (None, None, None, None)),
    ('UNEQUAL', 1, 2, 0, 2, 2, (False, False, False, True), (None, None, None, (-2, 2))),
    ('UNEQUAL', 2, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('UNEQUAL', 3, 3, 2, 0, 4, (True, False, True, False), ((2, 2), None, (-4, 2), None)),
    ('EQUALITY', 1, 2, 0, 2, 2, (False, False, False, True), (None, None, None, (-2, 2))),
    ('EQUALITY', 2, 2, 0, 2, 2, (False, False, False, True), (None, None, None, (-2, 2))),
    ('EQUALITY', 3, 4, 1, 2, 4, (False, False, False, True), (None, None, None, (-4, 4))),
    ('EQUALITY', 4, 2, 0, 2, 2, (False, False, False, True), (None, None, None, (-2, 2))),
    ('EQUALITY', 5, 4, 1, 2, 4, (False, False, False, True), (None, None, None, (-4, 4))),
    ('EQUALITY', 6, 4, 1, 2, 4, (False, False, False, True), (None, None, None, (-4, 4))),
    ('EQUALITY', 7, 6, 3, 0, 6, (False, False, False, False), (None, None, None, None)),
    ('WTRI', 1, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('WTRI', 2, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('WTRI', 3, 2, 1, 2, 4, (False, True, False, True), (None, (2, 2), None, (-4, 2))),
    ('WTRI', 4, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('WTRI', 5, 2, 1, 2, 4, (False, True, False, True), (None, (2, 2), None, (-4, 2))),
    ('WTRI', 6, 2, 1, 2, 4, (False, True, False, True), (None, (2, 2), None, (-4, 2))),
    ('WTRI', 7, 3, 3, 0, 6, (True, False, True, False), ((2, 4), None, (-6, 2), None)),
    ('ODDFULL', 1, 2, 0, 2, 2, (False, False, False, True), (None, None, None, (-2, 2))),
    ('ODDFULL', 2, 2, 0, 2, 2, (False, False, False, True), (None, None, None, (-2, 2))),
    ('ODDFULL', 3, 4, 1, 2, 4, (False, False, False, True), (None, None, None, (-4, 4))),
    ('ODDFULL', 4, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('ODDFULL', 5, 3, 1, 2, 4, (True, False, True, False), ((4, 2), None, (-2, 2), None)),
    ('ODDFULL', 6, 3, 1, 2, 4, (True, False, True, False), ((4, 2), None, (-2, 2), None)),
    ('ODDFULL', 7, 5, 3, 0, 6, (True, False, True, False), ((4, 2), None, (-6, 4), None)),
    ('TIECARD', 1, 1, 0, 1, 1, (False, False, False, False), (None, None, None, None)),
    ('TIECARD', 2, 1, 0, 1, 1, (False, False, False, False), (None, None, None, None)),
    ('TIECARD', 3, 2, 0, 2, 2, (False, False, False, True), (None, None, None, (-2, 2))),
    ('TIECARD', 4, 2, 0, 2, 2, (False, False, False, True), (None, None, None, (-2, 2))),
    ('TIECARD', 5, 3, 1, 1, 3, (False, False, True, False), (None, None, (-2, 2), None)),
    ('TIECARD', 6, 3, 1, 1, 3, (False, False, True, False), (None, None, (-2, 2), None)),
    ('TIECARD', 7, 4, 2, 0, 4, (False, False, False, False), (None, None, None, None)),
    ('RICH', 1, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('RICH', 2, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('RICH', 3, 2, 0, 4, 4, (False, True, False, True), (None, (4, 2), None, (-2, 2))),
    ('RICH', 4, 1, 0, 5, 5, (False, True, False, False), (None, (4, 4), None, None)),
    ('RICH', 5, 2, 2, 3, 7, (True, False, False, True), ((4, 6), None, None, (-6, 2))),
    ('RICH', 6, 2, 2, 3, 7, (True, False, False, True), ((4, 6), None, None, (-6, 2))),
    ('RICH', 7, 3, 4, 1, 9, (False, True, True, False), (None, (2, 6), (-8, 2), None)),
    ('RICH', 8, 1, 0, 1, 1, (False, False, False, False), (None, None, None, None)),
    ('RICH', 9, 2, 0, 3, 3, (True, False, False, True), ((4, 2), None, None, (-2, 2))),
    ('RICH', 10, 2, 0, 3, 3, (True, False, False, True), ((4, 2), None, None, (-2, 2))),
    ('RICH', 11, 3, 0, 5, 5, (False, True, True, False), (None, (6, 2), (0, 2), None)),
    ('RICH', 12, 2, 0, 6, 6, (False, True, False, True), (None, (6, 4), None, (-2, 2))),
    ('RICH', 13, 3, 2, 4, 8, (True, False, True, False), ((6, 6), None, (-4, 2), None)),
    ('RICH', 14, 3, 2, 4, 8, (True, False, True, False), ((6, 6), None, (-4, 2), None)),
    ('RICH', 15, 4, 4, 2, 10, (False, True, False, True), (None, (4, 6), None, (-10, 4))),
    ('RICH', 16, 2, 0, 2, 2, (False, False, False, True), (None, None, None, (-2, 2))),
    ('RICH', 17, 3, 0, 4, 4, (True, False, True, False), ((6, 2), None, (0, 2), None)),
    ('RICH', 18, 3, 0, 4, 4, (True, False, True, False), ((6, 2), None, (0, 2), None)),
    ('RICH', 19, 4, 0, 6, 6, (False, True, False, True), (None, (8, 2), None, (-2, 4))),
    ('RICH', 20, 3, 1, 5, 7, (False, True, True, False), (None, (6, 4), (-2, 2), None)),
    ('RICH', 21, 4, 3, 3, 9, (True, False, False, True), ((6, 6), None, None, (-8, 4))),
    ('RICH', 22, 4, 3, 3, 9, (True, False, False, True), ((6, 6), None, None, (-8, 4))),
    ('RICH', 23, 5, 5, 1, 11, (False, True, True, False), (None, (4, 6), (-10, 4), None)),
    ('RICH', 24, 3, 1, 1, 3, (False, False, True, False), (None, None, (-2, 2), None)),
    ('RICH', 25, 4, 1, 3, 5, (True, False, False, True), ((6, 2), None, None, (-4, 4))),
    ('RICH', 26, 4, 1, 3, 5, (True, False, False, True), ((6, 2), None, None, (-4, 4))),
    ('RICH', 27, 5, 1, 5, 7, (False, True, True, False), (None, (8, 2), (-2, 4), None)),
    ('RICH', 28, 4, 2, 4, 8, (False, True, False, True), (None, (6, 4), None, (-6, 4))),
    ('RICH', 29, 5, 4, 2, 10, (True, False, True, False), ((6, 6), None, (-8, 4), None)),
    ('RICH', 30, 5, 4, 2, 10, (True, False, True, False), ((6, 6), None, (-8, 4), None)),
    ('RICH', 31, 6, 6, 0, 12, (False, False, False, False), (None, None, None, None)),
    ('MIXED', 1, 2, 0, 6, 6, (False, True, False, True), (None, (6, 4), None, (-2, 2))),
    ('MIXED', 2, 3, 0, 8, 8, (True, False, True, False), ((10, 6), None, (0, 2), None)),
    ('MIXED', 3, 5, 2, 10, 14, (True, False, True, False), ((14, 10), None, (-4, 4), None)),
    ('MIXED', 4, 4, 0, 12, 12, (False, True, False, True), (None, (14, 8), None, (-2, 4))),
    ('MIXED', 5, 6, 3, 12, 18, (False, True, False, True), (None, (16, 12), None, (-8, 6))),
    ('MIXED', 6, 7, 4, 12, 20, (True, False, True, False), ((18, 14), None, (-8, 6), None)),
    ('MIXED', 7, 9, 9, 8, 26, (True, False, True, False), ((16, 18), None, (-18, 8), None)),
    ('MIXED', 8, 5, 0, 8, 8, (True, False, True, False), ((12, 4), None, (0, 4), None)),
    ('MIXED', 9, 7, 1, 12, 14, (True, False, True, False), ((18, 8), None, (-2, 6), None)),
    ('MIXED', 10, 8, 2, 12, 16, (False, True, False, True), (None, (18, 8), None, (-6, 8))),
    ('MIXED', 11, 10, 5, 12, 22, (False, True, False, True), (None, (20, 12), None, (-12, 10))),
    ('MIXED', 12, 9, 5, 10, 20, (True, False, True, False), ((18, 12), None, (-10, 8), None)),
    ('MIXED', 13, 11, 9, 8, 26, (True, False, True, False), ((18, 16), None, (-18, 10), None)),
    ('MIXED', 14, 12, 11, 6, 28, (False, True, False, True), (None, (16, 16), None, (-24, 12))),
    ('MIXED', 15, 14, 17, 0, 34, (False, False, False, False), (None, None, None, None)),
    ('ZERO', 1, 3, 0, 3, 3, (False, False, True, False), (None, None, (0, 2), None)),
    ('ZERO', 2, 3, 0, 3, 3, (False, False, True, False), (None, None, (0, 2), None)),
    ('ZERO', 3, 6, 3, 0, 6, (False, False, False, False), (None, None, None, None)),
    ('SHIFT', 1, 4, 0, 4, 4, (False, False, False, True), (None, None, None, (-2, 4))),
    ('SHIFT', 2, 4, 0, 4, 4, (False, False, False, True), (None, None, None, (-2, 4))),
    ('SHIFT', 3, 8, 4, 0, 8, (False, False, False, False), (None, None, None, None)),
    ('LOW0', 1, 3, 0, 10, 10, (True, False, True, False), ((12, 8), None, (0, 2), None)),
    ('LOW0', 2, 3, 0, 10, 10, (True, False, True, False), ((12, 8), None, (0, 2), None)),
    ('LOW0', 3, 6, 9, 2, 20, (False, True, False, True), (None, (6, 14), None, (-20, 6))),
    ('LOW0', 4, 7, 0, 9, 9, (False, True, True, False), (None, (14, 2), (0, 6), None)),
    ('LOW0', 5, 10, 1, 17, 19, (True, False, False, True), ((26, 10), None, None, (-4, 10))),
    ('LOW0', 6, 10, 0, 19, 19, (True, False, False, True), ((28, 10), None, None, (-2, 10))),
    ('LOW0', 7, 13, 10, 9, 29, (False, True, True, False), (None, (20, 16), (-20, 12), None)),
    ('LOW0', 8, 5, 0, 9, 9, (False, True, True, False), (None, (12, 4), (0, 4), None)),
    ('LOW0', 9, 8, 0, 19, 19, (True, False, False, True), ((26, 12), None, None, (-2, 8))),
    ('LOW0', 10, 8, 1, 17, 19, (True, False, False, True), ((24, 12), None, None, (-4, 8))),
    ('LOW0', 11, 11, 10, 9, 29, (False, True, True, False), (None, (18, 18), (-20, 10), None)),
    ('LOW0', 12, 12, 8, 2, 18, (False, True, False, True), (None, (12, 6), None, (-18, 12))),
    ('LOW0', 13, 15, 9, 10, 28, (True, False, True, False), ((24, 14), None, (-18, 14), None)),
    ('LOW0', 14, 15, 9, 10, 28, (True, False, True, False), ((24, 14), None, (-18, 14), None)),
    ('LOW0', 15, 18, 19, 0, 38, (False, False, False, False), (None, None, None, None)),
    ('LOW1', 1, 11, 0, 15, 15, (False, True, True, False), (None, (24, 4), (0, 10), None)),
    ('LOW1', 2, 1, 0, 3, 3, (False, True, False, False), (None, (2, 2), None, None)),
    ('LOW1', 3, 12, 0, 18, 18, (False, True, False, True), (None, (28, 6), None, (-2, 12))),
    ('LOW1', 4, 1, 0, 10, 10, (True, False, False, False), ((10, 10), None, None, None)),
    ('LOW1', 5, 12, 9, 7, 25, (True, False, False, True), ((18, 14), None, None, (-20, 12))),
    ('LOW1', 6, 2, 0, 13, 13, (True, False, False, True), ((14, 12), None, None, (-2, 2))),
    ('LOW1', 7, 13, 9, 10, 28, (True, False, True, False), ((22, 16), None, (-18, 12), None)),
    ('LOW1', 8, 3, 0, 4, 4, (True, False, True, False), ((6, 2), None, (0, 2), None)),
    ('LOW1', 9, 14, 0, 19, 19, (True, False, False, True), ((32, 6), None, None, (-2, 14))),
    ('LOW1', 10, 4, 3, 1, 7, (True, False, False, True), ((4, 4), None, None, (-8, 4))),
    ('LOW1', 11, 15, 3, 16, 22, (True, False, True, False), ((30, 8), None, (-6, 14), None)),
    ('LOW1', 12, 4, 0, 14, 14, (False, True, False, True), (None, (16, 10), None, (-2, 4))),
    ('LOW1', 13, 15, 9, 11, 29, (False, True, True, False), (None, (24, 14), (-18, 14), None)),
    ('LOW1', 14, 5, 3, 11, 17, (False, True, True, False), (None, (14, 12), (-6, 4), None)),
    ('LOW1', 15, 16, 12, 8, 32, (False, True, False, True), (None, (22, 16), None, (-26, 16))),
    ('LOW1', 16, 4, 0, 8, 8, (False, True, False, True), (None, (10, 4), None, (-2, 4))),
    ('LOW1', 17, 15, 6, 11, 23, (False, True, True, False), (None, (24, 8), (-12, 14), None)),
    ('LOW1', 18, 5, 0, 11, 11, (False, True, True, False), (None, (14, 6), (0, 4), None)),
    ('LOW1', 19, 16, 6, 14, 26, (False, True, False, True), (None, (28, 10), None, (-14, 16))),
    ('LOW1', 20, 5, 1, 16, 18, (True, False, True, False), ((20, 14), None, (-2, 4), None)),
    ('LOW1', 21, 16, 16, 1, 33, (True, False, False, True), ((16, 18), None, None, (-34, 16))),
    ('LOW1', 22, 6, 1, 19, 21, (True, False, False, True), ((24, 16), None, None, (-4, 6))),
    ('LOW1', 23, 17, 16, 4, 36, (True, False, True, False), ((20, 20), None, (-32, 16), None)),
    ('LOW1', 24, 7, 1, 10, 12, (True, False, True, False), ((16, 6), None, (-2, 6), None)),
    ('LOW1', 25, 18, 7, 13, 27, (True, False, False, True), ((30, 10), None, None, (-16, 18))),
    ('LOW1', 26, 8, 4, 7, 15, (True, False, False, True), ((14, 8), None, None, (-10, 8))),
    ('LOW1', 27, 19, 10, 10, 30, (True, False, True, False), ((28, 12), None, (-20, 18), None)),
    ('LOW1', 28, 8, 2, 18, 22, (False, True, False, True), (None, (24, 14), None, (-6, 8))),
    ('LOW1', 29, 19, 17, 3, 37, (False, True, True, False), (None, (20, 18), (-34, 18), None)),
    ('LOW1', 30, 9, 5, 15, 25, (False, True, True, False), (None, (22, 16), (-10, 8), None)),
    ('LOW1', 31, 20, 20, 0, 40, (False, False, False, False), (None, None, None, None)),
    ('HIGH2', 1, 2, 0, 2, 2, (False, False, False, True), (None, None, None, (-2, 2))),
    ('HIGH2', 2, 1, 0, 3, 3, (False, True, False, False), (None, (2, 2), None, None)),
    ('HIGH2', 3, 3, 1, 3, 5, (False, True, True, False), (None, (4, 2), (-2, 2), None)),
    ('HIGH2', 4, 3, 0, 3, 3, (False, False, True, False), (None, None, (0, 2), None)),
    ('HIGH2', 5, 5, 1, 3, 5, (False, False, True, False), (None, None, (-2, 4), None)),
    ('HIGH2', 6, 4, 2, 2, 6, (False, True, False, True), (None, (4, 2), None, (-6, 4))),
    ('HIGH2', 7, 6, 4, 0, 8, (False, False, False, False), (None, None, None, None)),
    ('HIGH3', 1, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('HIGH3', 2, 1, 0, 3, 3, (False, True, False, False), (None, (2, 2), None, None)),
    ('HIGH3', 3, 2, 1, 3, 5, (True, False, False, True), ((4, 4), None, None, (-4, 2))),
    ('HIGH3', 4, 3, 0, 3, 3, (False, False, True, False), (None, None, (0, 2), None)),
    ('HIGH3', 5, 4, 1, 3, 5, (True, False, False, True), ((6, 2), None, None, (-4, 4))),
    ('HIGH3', 6, 4, 2, 2, 6, (False, True, False, True), (None, (4, 2), None, (-6, 4))),
    ('HIGH3', 7, 5, 4, 0, 8, (True, False, True, False), ((4, 4), None, (-8, 4), None)),
    ('NONMAX', 1, 1, 0, 1, 1, (False, False, False, False), (None, None, None, None)),
    ('NONMAX', 2, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('NONMAX', 3, 2, 0, 3, 3, (True, False, False, True), ((4, 2), None, None, (-2, 2))),
    ('NONMAX', 4, 1, 0, 3, 3, (False, True, False, False), (None, (2, 2), None, None)),
    ('NONMAX', 5, 2, 1, 2, 4, (False, True, False, True), (None, (2, 2), None, (-4, 2))),
    ('NONMAX', 6, 2, 2, 1, 5, (True, False, False, True), ((2, 4), None, None, (-6, 2))),
    ('NONMAX', 7, 3, 3, 0, 6, (True, False, True, False), ((2, 4), None, (-6, 2), None)),
    ('CHOICE', 1, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('CHOICE', 2, 1, 0, 2, 2, (True, False, False, False), ((2, 2), None, None, None)),
    ('CHOICE', 3, 2, 0, 4, 4, (False, True, False, True), (None, (4, 2), None, (-2, 2))),
    ('CHOICE', 4, 4, 0, 4, 4, (False, False, False, True), (None, None, None, (-2, 4))),
    ('CHOICE', 5, 5, 2, 2, 6, (True, False, True, False), ((6, 2), None, (-4, 4), None)),
    ('CHOICE', 6, 5, 2, 2, 6, (True, False, True, False), ((6, 2), None, (-4, 4), None)),
    ('CHOICE', 7, 6, 4, 0, 8, (False, False, False, False), (None, None, None, None)),
)

# U13_OPTIMA: solve, domain, comparison_pair, complete_argmin
U13_OPTIMA = (
    ('Q1-j0', (), None, ()),
    ('Q1-j1', (), None, ()),
    ('Q1-j2', (), None, ()),
    ('Q1-j3', (), None, ()),
    ('DOUBLE-j0', (1, 2), (2, 2), (1, 2)),
    ('DOUBLE-j1', (), None, ()),
    ('DOUBLE-j2', (), None, ()),
    ('DOUBLE-j3', (), None, ()),
    ('UNEQUAL-j0', (2, 3), (2, 2), (2, 3)),
    ('UNEQUAL-j1', (), None, ()),
    ('UNEQUAL-j2', (3,), (-4, 2), (3,)),
    ('UNEQUAL-j3', (1,), (-2, 2), (1,)),
    ('EQUALITY-j0', (), None, ()),
    ('EQUALITY-j1', (), None, ()),
    ('EQUALITY-j2', (), None, ()),
    ('EQUALITY-j3', (1, 2, 3, 4, 5, 6), (-2, 2), (1, 2, 3, 4, 5, 6)),
    ('WTRI-j0', (1, 2, 4, 7), (2, 4), (7,)),
    ('WTRI-j1', (3, 5, 6), (2, 2), (3, 5, 6)),
    ('WTRI-j2', (7,), (-6, 2), (7,)),
    ('WTRI-j3', (3, 5, 6), (-4, 2), (3, 5, 6)),
    ('ODDFULL-j0', (4, 5, 6, 7), (2, 2), (4,)),
    ('ODDFULL-j1', (), None, ()),
    ('ODDFULL-j2', (5, 6, 7), (-6, 4), (7,)),
    ('ODDFULL-j3', (1, 2, 3), (-2, 2), (1, 2, 3)),
    ('TIECARD-j0', (), None, ()),
    ('TIECARD-j1', (), None, ()),
    ('TIECARD-j2', (5, 6), (-2, 2), (5, 6)),
    ('TIECARD-j3', (3, 4), (-2, 2), (3, 4)),
    ('RICH-j0', (1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, 30), (4, 6), (5, 6)),
    ('RICH-j1', (3, 4, 7, 11, 12, 15, 19, 20, 23, 27, 28), (2, 6), (7,)),
    ('RICH-j2', (7, 11, 13, 14, 17, 18, 20, 23, 24, 27, 29, 30), (-8, 2), (7,)),
    ('RICH-j3', (3, 5, 6, 9, 10, 12, 15, 16, 19, 21, 22, 25, 26, 28), (-6, 2), (5, 6)),
    ('MIXED-j0', (2, 3, 6, 7, 8, 9, 12, 13), (16, 18), (7,)),
    ('MIXED-j1', (1, 4, 5, 10, 11, 14), (16, 16), (14,)),
    ('MIXED-j2', (2, 3, 6, 7, 8, 9, 12, 13), (-18, 8), (7,)),
    ('MIXED-j3', (1, 4, 5, 10, 11, 14), (-24, 12), (14,)),
    ('ZERO-j0', (), None, ()),
    ('ZERO-j1', (), None, ()),
    ('ZERO-j2', (1, 2), (0, 2), (1, 2)),
    ('ZERO-j3', (), None, ()),
    ('SHIFT-j0', (), None, ()),
    ('SHIFT-j1', (), None, ()),
    ('SHIFT-j2', (), None, ()),
    ('SHIFT-j3', (1, 2), (-2, 4), (1, 2)),
    ('LOW0-j0', (1, 2, 5, 6, 9, 10, 13, 14), (12, 8), (1, 2)),
    ('LOW0-j1', (3, 4, 7, 8, 11, 12), (6, 14), (3,)),
    ('LOW0-j2', (1, 2, 4, 7, 8, 11, 13, 14), (-20, 10), (11,)),
    ('LOW0-j3', (3, 5, 6, 9, 10, 12), (-20, 6), (3,)),
    ('LOW1-j0', (4, 5, 6, 7, 8, 9, 10, 11, 20, 21, 22, 23, 24, 25, 26, 27), (16, 18), (21,)),
    ('LOW1-j1', (1, 2, 3, 12, 13, 14, 15, 16, 17, 18, 19, 28, 29, 30), (2, 2), (2,)),
    ('LOW1-j2', (1, 7, 8, 11, 13, 14, 17, 18, 20, 23, 24, 27, 29, 30), (-32, 16), (23,)),
    ('LOW1-j3', (3, 5, 6, 9, 10, 12, 15, 16, 19, 21, 22, 25, 26, 28), (-34, 16), (21,)),
    ('HIGH2-j0', (), None, ()),
    ('HIGH2-j1', (2, 3, 6), (2, 2), (2,)),
    ('HIGH2-j2', (3, 4, 5), (-2, 2), (3,)),
    ('HIGH2-j3', (1, 6), (-6, 4), (6,)),
    ('HIGH3-j0', (1, 3, 5, 7), (2, 2), (1, 3, 7)),
    ('HIGH3-j1', (2, 6), (2, 2), (2,)),
    ('HIGH3-j2', (4, 7), (-8, 4), (7,)),
    ('HIGH3-j3', (3, 5, 6), (-4, 2), (3,)),
    ('NONMAX-j0', (2, 3, 6, 7), (2, 4), (6, 7)),
    ('NONMAX-j1', (4, 5), (2, 2), (4, 5)),
    ('NONMAX-j2', (7,), (-6, 2), (7,)),
    ('NONMAX-j3', (3, 5, 6), (-6, 2), (6,)),
    ('CHOICE-j0', (1, 2, 5, 6), (2, 2), (1, 2)),
    ('CHOICE-j1', (3,), (4, 2), (3,)),
    ('CHOICE-j2', (5, 6), (-4, 4), (5, 6)),
    ('CHOICE-j3', (3, 4), (-2, 2), (3,)),
)

# U13_SOLVES: solve, returned_root, terminal_U, t_outer_updates, query_structural_counts,
# aggregate_structural_counts
U13_SOLVES = (
    ('Q1-j0', None, None, (1, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0)),
    ('Q1-j1', None, None, (1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)),
    ('Q1-j2', None, None, (1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)),
    ('Q1-j3', None, None, (1, 0, 0), (2, 0, 0, 0), (2, 0, 0, 0)),
    ('DOUBLE-j0', (2, 2), 1, (3, 2, 1), (1, 1, 1, 7), (3, 3, 3, 21)),
    ('DOUBLE-j1', None, None, (1, 0, 0), (4, 0, 0, 0), (4, 0, 0, 0)),
    ('DOUBLE-j2', None, None, (1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)),
    ('DOUBLE-j3', None, None, (1, 0, 0), (2, 0, 0, 0), (2, 0, 0, 0)),
    ('UNEQUAL-j0', (2, 2), 3, (3, 2, 1), (1, 1, 1, 7), (3, 3, 3, 21)),
    ('UNEQUAL-j1', None, None, (1, 0, 0), (2, 0, 0, 0), (2, 0, 0, 0)),
    ('UNEQUAL-j2', (-4, 2), 3, (3, 2, 1), (1, 1, 1, 3), (3, 3, 3, 9)),
    ('UNEQUAL-j3', (-2, 2), 1, (3, 2, 1), (2, 1, 1, 1), (6, 3, 3, 3)),
    ('EQUALITY-j0', None, None, (1, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0)),
    ('EQUALITY-j1', None, None, (1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)),
    ('EQUALITY-j2', None, None, (1, 0, 0), (3, 0, 0, 0), (3, 0, 0, 0)),
    ('EQUALITY-j3', (-4, 4), 1, (3, 2, 1), (6, 6, 6, 18), (18, 18, 18, 54)),
    ('WTRI-j0', (2, 4), 7, (3, 2, 1), (1, 1, 1, 13), (3, 3, 3, 39)),
    ('WTRI-j1', (2, 2), 5, (3, 2, 1), (18, 12, 12, 24), (54, 36, 36, 72)),
    ('WTRI-j2', (-6, 2), 7, (3, 2, 1), (1, 1, 1, 1), (3, 3, 3, 3)),
    ('WTRI-j3', (-4, 2), 5, (3, 2, 1), (6, 6, 6, 18), (18, 18, 18, 54)),
    ('ODDFULL-j0', (2, 2), 4, (3, 2, 1), (1, 1, 1, 13), (3, 3, 3, 39)),
    ('ODDFULL-j1', None, None, (1, 0, 0), (6, 0, 0, 0), (6, 0, 0, 0)),
    ('ODDFULL-j2', (-6, 4), 7, (3, 2, 1), (2, 2, 2, 14), (6, 6, 6, 42)),
    ('ODDFULL-j3', (-4, 4), 1, (3, 2, 1), (6, 4, 4, 12), (18, 12, 12, 36)),
    ('TIECARD-j0', None, None, (1, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0)),
    ('TIECARD-j1', None, None, (1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)),
    ('TIECARD-j2', (-2, 2), 6, (3, 2, 1), (1, 1, 1, 7), (3, 3, 3, 21)),
    ('TIECARD-j3', (-2, 2), 3, (3, 2, 1), (4, 4, 4, 12), (12, 12, 12, 36)),
    ('RICH-j0', (4, 6), 5, (3, 2, 1), (1, 1, 1, 31), (3, 3, 3, 93)),
    ('RICH-j1', (2, 6), 7, (3, 2, 1), (24, 17, 17, 149), (72, 51, 51, 447)),
    ('RICH-j2', (-8, 2), 7, (3, 2, 1), (5, 5, 5, 49), (15, 15, 15, 147)),
    ('RICH-j3', (-6, 2), 6, (4, 3, 2), (8, 8, 8, 104), (32, 32, 32, 416)),
    ('MIXED-j0', (16, 18), 7, (3, 2, 1), (1, 1, 1, 21), (3, 3, 3, 63)),
    ('MIXED-j1', (16, 16), 14, (3, 2, 1), (48, 26, 26, 118), (144, 78, 78, 354)),
    ('MIXED-j2', (-18, 8), 7, (3, 2, 1), (4, 4, 4, 52), (12, 12, 12, 156)),
    ('MIXED-j3', (-24, 12), 14, (3, 2, 1), (12, 10, 10, 70), (36, 30, 30, 210)),
    ('ZERO-j0', None, None, (1, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0)),
    ('ZERO-j1', None, None, (1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)),
    ('ZERO-j2', (0, 2), 1, (3, 2, 1), (2, 2, 2, 6), (6, 6, 6, 18)),
    ('ZERO-j3', None, None, (1, 0, 0), (2, 0, 0, 0), (2, 0, 0, 0)),
    ('SHIFT-j0', None, None, (1, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0)),
    ('SHIFT-j1', None, None, (1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)),
    ('SHIFT-j2', None, None, (1, 0, 0), (2, 0, 0, 0), (2, 0, 0, 0)),
    ('SHIFT-j3', (-2, 4), 1, (3, 2, 1), (2, 2, 2, 2), (6, 6, 6, 6)),
    ('LOW0-j0', (12, 8), 1, (4, 3, 2), (1, 1, 1, 21), (4, 4, 4, 84)),
    ('LOW0-j1', (6, 14), 3, (3, 2, 1), (32, 16, 16, 72), (96, 48, 48, 216)),
    ('LOW0-j2', (-20, 10), 11, (3, 2, 1), (4, 4, 4, 52), (12, 12, 12, 156)),
    ('LOW0-j3', (-20, 6), 3, (3, 2, 1), (8, 8, 8, 56), (24, 24, 24, 168)),
    ('LOW1-j0', (16, 18), 21, (3, 2, 1), (1, 1, 1, 31), (3, 3, 3, 93)),
    ('LOW1-j1', (2, 2), 2, (4, 3, 2), (50, 36, 36, 312), (200, 144, 144, 1248)),
    ('LOW1-j2', (-32, 16), 23, (4, 3, 2), (3, 3, 3, 63), (12, 12, 12, 252)),
    ('LOW1-j3', (-34, 16), 21, (3, 2, 1), (10, 10, 10, 130), (30, 30, 30, 390)),
    ('HIGH2-j0', None, None, (1, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0)),
    ('HIGH2-j1', (2, 2), 2, (3, 2, 1), (6, 4, 4, 8), (18, 12, 12, 24)),
    ('HIGH2-j2', (-2, 2), 3, (4, 3, 2), (2, 2, 2, 14), (8, 8, 8, 56)),
    ('HIGH2-j3', (-6, 4), 6, (3, 2, 1), (6, 4, 4, 12), (18, 12, 12, 36)),
    ('HIGH3-j0', (4, 4), 1, (3, 2, 1), (1, 1, 1, 13), (3, 3, 3, 39)),
    ('HIGH3-j1', (2, 2), 2, (3, 2, 1), (12, 3, 3, 7), (36, 9, 9, 21)),
    ('HIGH3-j2', (-8, 4), 7, (3, 2, 1), (1, 1, 1, 7), (3, 3, 3, 21)),
    ('HIGH3-j3', (-4, 2), 3, (4, 3, 2), (6, 6, 6, 18), (24, 24, 24, 72)),
    ('NONMAX-j0', (2, 4), 7, (3, 2, 1), (1, 1, 1, 13), (3, 3, 3, 39)),
    ('NONMAX-j1', (2, 2), 4, (3, 2, 1), (8, 2, 2, 6), (24, 6, 6, 18)),
    ('NONMAX-j2', (-6, 2), 7, (3, 2, 1), (1, 1, 1, 1), (3, 3, 3, 3)),
    ('NONMAX-j3', (-6, 2), 6, (3, 2, 1), (4, 4, 4, 12), (12, 12, 12, 36)),
    ('CHOICE-j0', (2, 2), 1, (3, 2, 1), (1, 1, 1, 13), (3, 3, 3, 39)),
    ('CHOICE-j1', (4, 2), 3, (3, 2, 1), (8, 4, 4, 8), (24, 12, 12, 24)),
    ('CHOICE-j2', (-4, 4), 6, (3, 2, 1), (1, 1, 1, 7), (3, 3, 3, 21)),
    ('CHOICE-j3', (-2, 2), 3, (3, 2, 1), (4, 4, 4, 12), (12, 12, 12, 36)),
)

# U13_TRACES: solve, step, phase, parameter, U, source_pair, raw, all_residual_argmins,
# retained_family, retained_GR_pair
U13_TRACES = (
    ('Q1-j0', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('Q1-j1', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('Q1-j2', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('Q1-j3', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('DOUBLE-j0', 0, 'seed', (0, 1), 1, (2, 2), 2, (1, 2), 0, (2, 3)),
    ('DOUBLE-j0', 1, 'K', (4, 2), 1, (2, 2), -4, (1, 2), 0, (2, 3)),
    ('DOUBLE-j0', 2, 'terminal', (2, 2), 1, (2, 2), 0, (1, 2), 0, (2, 3)),
    ('DOUBLE-j1', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('DOUBLE-j2', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('DOUBLE-j3', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('UNEQUAL-j0', 0, 'seed', (0, 1), 3, (2, 2), 2, (2, 3), 0, (2, 1)),
    ('UNEQUAL-j0', 1, 'K', (4, 2), 3, (2, 2), -4, (2, 3), 0, (2, 1)),
    ('UNEQUAL-j0', 2, 'terminal', (2, 2), 3, (2, 2), 0, (2, 3), 0, (2, 1)),
    ('UNEQUAL-j1', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('UNEQUAL-j2', 0, 'seed', (0, 1), 3, (-4, 2), -4, (3,), 0, (0, 1)),
    ('UNEQUAL-j2', 1, 'K', (-2, 2), 3, (-4, 2), -4, (3,), 0, (0, 1)),
    ('UNEQUAL-j2', 2, 'terminal', (-4, 2), 3, (-4, 2), 0, (3,), 0, (0, 1)),
    ('UNEQUAL-j3', 0, 'seed', (0, 1), 1, (-2, 2), -2, (1,), 0, (0, 1)),
    ('UNEQUAL-j3', 1, 'K', (0, 2), 1, (-2, 2), -4, (1,), 0, (0, 1)),
    ('UNEQUAL-j3', 2, 'terminal', (-2, 2), 1, (-2, 2), 0, (1,), 0, (0, 1)),
    ('EQUALITY-j0', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('EQUALITY-j1', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('EQUALITY-j2', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('EQUALITY-j3', 0, 'seed', (0, 1), 5, (-4, 4), -4, (3, 5, 6), 0, (0, 1)),
    ('EQUALITY-j3', 1, 'K', (0, 4), 5, (-4, 4), -16, (3, 5, 6), 0, (0, 1)),
    ('EQUALITY-j3', 2, 'terminal', (-4, 4), 1, (-2, 2), 0, (1, 2, 3, 4, 5, 6), 0, (0, 1)),
    ('WTRI-j0', 0, 'seed', (0, 1), 1, (2, 2), 2, (1, 2, 4, 7), 0, (2, 1)),
    ('WTRI-j0', 1, 'K', (4, 2), 7, (2, 4), -12, (7,), 0, (0, 1)),
    ('WTRI-j0', 2, 'terminal', (2, 4), 7, (2, 4), 0, (7,), 0, (2, 1)),
    ('WTRI-j1', 0, 'seed', (0, 1), 5, (2, 2), 2, (3, 5, 6), 0, (2, 1)),
    ('WTRI-j1', 1, 'K', (4, 2), 5, (2, 2), -4, (3, 5, 6), 0, (0, 1)),
    ('WTRI-j1', 2, 'terminal', (2, 2), 5, (2, 2), 0, (3, 5, 6), 0, (2, 1)),
    ('WTRI-j2', 0, 'seed', (0, 1), 7, (-6, 2), -6, (7,), 0, (0, 1)),
    ('WTRI-j2', 1, 'K', (-4, 2), 7, (-6, 2), -4, (7,), 0, (0, 1)),
    ('WTRI-j2', 2, 'terminal', (-6, 2), 7, (-6, 2), 0, (7,), 0, (0, 1)),
    ('WTRI-j3', 0, 'seed', (0, 1), 5, (-4, 2), -4, (3, 5, 6), 0, (0, 1)),
    ('WTRI-j3', 1, 'K', (-2, 2), 5, (-4, 2), -4, (3, 5, 6), 0, (0, 1)),
    ('WTRI-j3', 2, 'terminal', (-4, 2), 5, (-4, 2), 0, (3, 5, 6), 0, (2, 1)),
    ('ODDFULL-j0', 0, 'seed', (0, 1), 4, (2, 2), 2, (4,), 0, (4, 1)),
    ('ODDFULL-j0', 1, 'K', (4, 2), 4, (2, 2), -4, (4,), 0, (4, 1)),
    ('ODDFULL-j0', 2, 'terminal', (2, 2), 4, (2, 2), 0, (4,), 0, (4, 1)),
    ('ODDFULL-j1', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('ODDFULL-j2', 0, 'seed', (0, 1), 7, (-6, 4), -6, (7,), 0, (0, 1)),
    ('ODDFULL-j2', 1, 'K', (-2, 4), 7, (-6, 4), -16, (7,), 0, (0, 1)),
    ('ODDFULL-j2', 2, 'terminal', (-6, 4), 7, (-6, 4), 0, (7,), 0, (0, 1)),
    ('ODDFULL-j3', 0, 'seed', (0, 1), 3, (-4, 4), -4, (3,), 2, (0, 1)),
    ('ODDFULL-j3', 1, 'K', (0, 4), 3, (-4, 4), -16, (3,), 2, (0, 1)),
    ('ODDFULL-j3', 2, 'terminal', (-4, 4), 1, (-2, 2), 0, (1, 2, 3), 0, (0, 2)),
    ('TIECARD-j0', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('TIECARD-j1', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('TIECARD-j2', 0, 'seed', (0, 1), 6, (-2, 2), -2, (5, 6), 0, (0, 2)),
    ('TIECARD-j2', 1, 'K', (0, 2), 6, (-2, 2), -4, (5, 6), 0, (0, 2)),
    ('TIECARD-j2', 2, 'terminal', (-2, 2), 6, (-2, 2), 0, (5, 6), 0, (0, 2)),
    ('TIECARD-j3', 0, 'seed', (0, 1), 3, (-2, 2), -2, (3, 4), 0, (2, 1)),
    ('TIECARD-j3', 1, 'K', (0, 2), 3, (-2, 2), -4, (3, 4), 0, (2, 1)),
    ('TIECARD-j3', 2, 'terminal', (-2, 2), 3, (-2, 2), 0, (3, 4), 0, (2, 1)),
    ('RICH-j0', 0, 'seed', (0, 1), 1, (2, 2), 2, (1, 2), 0, (2, 1)),
    ('RICH-j0', 1, 'K', (4, 2), 6, (4, 6), -16, (5, 6), 0, (0, 2)),
    ('RICH-j0', 2, 'terminal', (4, 6), 5, (4, 6), 0, (5, 6), 0, (2, 3)),
    ('RICH-j1', 0, 'seed', (0, 1), 7, (2, 6), 2, (7,), 4, (0, 1)),
    ('RICH-j1', 1, 'K', (8, 6), 7, (2, 6), -36, (7,), 4, (0, 1)),
    ('RICH-j1', 2, 'terminal', (2, 6), 7, (2, 6), 0, (7,), 4, (0, 1)),
    ('RICH-j2', 0, 'seed', (0, 1), 23, (-10, 4), -10, (23,), 0, (0, 5)),
    ('RICH-j2', 1, 'K', (-6, 4), 7, (-8, 2), -20, (7,), 1, (0, 1)),
    ('RICH-j2', 2, 'terminal', (-8, 2), 7, (-8, 2), 0, (7,), 1, (0, 1)),
    ('RICH-j3', 0, 'seed', (0, 1), 15, (-10, 4), -10, (15,), 4, (4, 1)),
    ('RICH-j3', 1, 'K', (-6, 4), 15, (-10, 4), -16, (15,), 4, (4, 1)),
    ('RICH-j3', 2, 'reset-query', (-10, 4), 6, (-6, 2), -4, (5, 6), 1, (0, 1)),
    ('RICH-j3', 3, 'terminal', (-6, 2), 6, (-6, 2), 0, (5, 6), 1, (0, 1)),
    ('MIXED-j0', 0, 'seed', (0, 1), 2, (10, 6), 10, (2,), 0, (3, 1)),
    ('MIXED-j0', 1, 'K', (16, 6), 7, (16, 18), -192, (7,), 0, (0, 5)),
    ('MIXED-j0', 2, 'terminal', (16, 18), 7, (16, 18), 0, (7,), 0, (2, 5)),
    ('MIXED-j1', 0, 'seed', (0, 1), 1, (6, 4), 6, (1,), 0, (0, 1)),
    ('MIXED-j1', 1, 'K', (10, 4), 14, (16, 16), -96, (14,), 13, (0, 1)),
    ('MIXED-j1', 2, 'terminal', (16, 16), 14, (16, 16), 0, (14,), 13, (0, 1)),
    ('MIXED-j2', 0, 'seed', (0, 1), 13, (-18, 10), -18, (7, 13), 0, (0, 2)),
    ('MIXED-j2', 1, 'K', (-8, 10), 7, (-18, 8), -116, (7,), 0, (0, 4)),
    ('MIXED-j2', 2, 'terminal', (-18, 8), 7, (-18, 8), 0, (7,), 0, (0, 4)),
    ('MIXED-j3', 0, 'seed', (0, 1), 14, (-24, 12), -24, (14,), 1, (0, 1)),
    ('MIXED-j3', 1, 'K', (-12, 12), 14, (-24, 12), -144, (14,), 1, (0, 1)),
    ('MIXED-j3', 2, 'terminal', (-24, 12), 14, (-24, 12), 0, (14,), 1, (0, 1)),
    ('ZERO-j0', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('ZERO-j1', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('ZERO-j2', 0, 'seed', (0, 1), 1, (0, 2), 0, (1, 2), 0, (0, 2)),
    ('ZERO-j2', 1, 'K', (2, 2), 1, (0, 2), -4, (1, 2), 0, (0, 2)),
    ('ZERO-j2', 2, 'terminal', (0, 2), 1, (0, 2), 0, (1, 2), 0, (0, 2)),
    ('ZERO-j3', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('SHIFT-j0', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('SHIFT-j1', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('SHIFT-j2', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('SHIFT-j3', 0, 'seed', (0, 1), 1, (-2, 4), -2, (1, 2), 0, (0, 1)),
    ('SHIFT-j3', 1, 'K', (2, 4), 1, (-2, 4), -16, (1, 2), 0, (0, 1)),
    ('SHIFT-j3', 2, 'terminal', (-2, 4), 1, (-2, 4), 0, (1, 2), 0, (0, 1)),
    ('LOW0-j0', 0, 'seed', (0, 1), 1, (12, 8), 12, (1, 2), 0, (2, 3)),
    ('LOW0-j0', 1, 'K', (20, 8), 14, (24, 14), -88, (13, 14), 0, (0, 2)),
    ('LOW0-j0', 2, 'reset-query', (24, 14), 1, (12, 8), -24, (1, 2), 0, (2, 3)),
    ('LOW0-j0', 3, 'terminal', (12, 8), 1, (12, 8), 0, (1, 2), 0, (2, 3)),
    ('LOW0-j1', 0, 'seed', (0, 1), 3, (6, 14), 6, (3,), 2, (0, 1)),
    ('LOW0-j1', 1, 'K', (20, 14), 3, (6, 14), -196, (3,), 2, (0, 1)),
    ('LOW0-j1', 2, 'terminal', (6, 14), 3, (6, 14), 0, (3,), 2, (0, 1)),
    ('LOW0-j2', 0, 'seed', (0, 1), 11, (-20, 10), -20, (7, 11), 0, (0, 3)),
    ('LOW0-j2', 1, 'K', (-10, 10), 11, (-20, 10), -100, (11,), 0, (4, 3)),
    ('LOW0-j2', 2, 'terminal', (-20, 10), 11, (-20, 10), 0, (11,), 0, (4, 3)),
    ('LOW0-j3', 0, 'seed', (0, 1), 3, (-20, 6), -20, (3,), 2, (0, 3)),
    ('LOW0-j3', 1, 'K', (-14, 6), 3, (-20, 6), -36, (3,), 2, (0, 1)),
    ('LOW0-j3', 2, 'terminal', (-20, 6), 3, (-20, 6), 0, (3,), 2, (0, 1)),
    ('LOW1-j0', 0, 'seed', (0, 1), 10, (4, 4), 4, (10,), 0, (5, 1)),
    ('LOW1-j0', 1, 'K', (8, 4), 21, (16, 18), -80, (21, 23), 0, (0, 3)),
    ('LOW1-j0', 2, 'terminal', (16, 18), 21, (16, 18), 0, (21,), 0, (2, 1)),
    ('LOW1-j1', 0, 'seed', (0, 1), 2, (2, 2), 2, (2,), 14, (0, 1)),
    ('LOW1-j1', 1, 'K', (4, 2), 29, (20, 18), -32, (29,), 5, (0, 1)),
    ('LOW1-j1', 2, 'reset-query', (20, 18), 2, (2, 2), -4, (2,), 14, (0, 2)),
    ('LOW1-j1', 3, 'terminal', (2, 2), 2, (2, 2), 0, (2,), 14, (0, 1)),
    ('LOW1-j2', 0, 'seed', (0, 1), 29, (-34, 18), -34, (29,), 0, (0, 2)),
    ('LOW1-j2', 1, 'K', (-16, 18), 29, (-34, 18), -324, (29,), 0, (4, 2)),
    ('LOW1-j2', 2, 'reset-query', (-34, 18), 23, (-32, 16), -32, (23,), 0, (2, 4)),
    ('LOW1-j2', 3, 'terminal', (-32, 16), 23, (-32, 16), 0, (23,), 0, (2, 4)),
    ('LOW1-j3', 0, 'seed', (0, 1), 21, (-34, 16), -34, (21,), 9, (0, 1)),
    ('LOW1-j3', 1, 'K', (-18, 16), 21, (-34, 16), -256, (21,), 9, (0, 1)),
    ('LOW1-j3', 2, 'terminal', (-34, 16), 21, (-34, 16), 0, (21,), 9, (0, 1)),
    ('HIGH2-j0', 0, 'seed', (0, 1), None, None, None, (), None, None),
    ('HIGH2-j1', 0, 'seed', (0, 1), 2, (2, 2), 2, (2,), 1, (0, 1)),
    ('HIGH2-j1', 1, 'K', (4, 2), 2, (2, 2), -4, (2,), 1, (0, 1)),
    ('HIGH2-j1', 2, 'terminal', (2, 2), 2, (2, 2), 0, (2,), 1, (0, 1)),
    ('HIGH2-j2', 0, 'seed', (0, 1), 5, (-2, 4), -2, (3, 5), 0, (0, 2)),
    ('HIGH2-j2', 1, 'K', (2, 4), 5, (-2, 4), -16, (5,), 0, (0, 2)),
    ('HIGH2-j2', 2, 'reset-query', (-2, 4), 3, (-2, 2), -4, (3,), 0, (0, 3)),
    ('HIGH2-j2', 3, 'terminal', (-2, 2), 3, (-2, 2), 0, (3,), 0, (0, 3)),
    ('HIGH2-j3', 0, 'seed', (0, 1), 6, (-6, 4), -6, (6,), 1, (0, 1)),
    ('HIGH2-j3', 1, 'K', (-2, 4), 6, (-6, 4), -16, (6,), 1, (0, 1)),
    ('HIGH2-j3', 2, 'terminal', (-6, 4), 6, (-6, 4), 0, (6,), 1, (2, 1)),
    ('HIGH3-j0', 0, 'seed', (0, 1), 1, (2, 2), 2, (1,), 0, (2, 1)),
    ('HIGH3-j0', 1, 'K', (4, 2), 3, (4, 4), -8, (3, 7), 0, (0, 1)),
    ('HIGH3-j0', 2, 'terminal', (4, 4), 1, (2, 2), 0, (1, 3, 7), 0, (2, 1)),
    ('HIGH3-j1', 0, 'seed', (0, 1), 2, (2, 2), 2, (2,), 7, (0, 1)),
    ('HIGH3-j1', 1, 'K', (4, 2), 2, (2, 2), -4, (2,), 7, (0, 1)),
    ('HIGH3-j1', 2, 'terminal', (2, 2), 2, (2, 2), 0, (2,), 7, (0, 1)),
    ('HIGH3-j2', 0, 'seed', (0, 1), 7, (-8, 4), -8, (7,), 0, (0, 1)),
    ('HIGH3-j2', 1, 'K', (-4, 4), 7, (-8, 4), -16, (7,), 0, (0, 1)),
    ('HIGH3-j2', 2, 'terminal', (-8, 4), 7, (-8, 4), 0, (7,), 0, (0, 1)),
    ('HIGH3-j3', 0, 'seed', (0, 1), 6, (-6, 4), -6, (6,), 1, (0, 1)),
    ('HIGH3-j3', 1, 'K', (-2, 4), 6, (-6, 4), -16, (6,), 1, (0, 1)),
    ('HIGH3-j3', 2, 'reset-query', (-6, 4), 3, (-4, 2), -4, (3,), 2, (0, 1)),
    ('HIGH3-j3', 3, 'terminal', (-4, 2), 3, (-4, 2), 0, (3,), 2, (2, 1)),
    ('NONMAX-j0', 0, 'seed', (0, 1), 2, (2, 2), 2, (2, 6, 7), 0, (3, 1)),
    ('NONMAX-j0', 1, 'K', (4, 2), 6, (2, 4), -12, (6, 7), 0, (0, 1)),
    ('NONMAX-j0', 2, 'terminal', (2, 4), 7, (2, 4), 0, (6, 7), 0, (2, 1)),
    ('NONMAX-j1', 0, 'seed', (0, 1), 4, (2, 2), 2, (4, 5), 5, (0, 2)),
    ('NONMAX-j1', 1, 'K', (4, 2), 4, (2, 2), -4, (4, 5), 5, (0, 2)),
    ('NONMAX-j1', 2, 'terminal', (2, 2), 4, (2, 2), 0, (4, 5), 5, (0, 2)),
    ('NONMAX-j2', 0, 'seed', (0, 1), 7, (-6, 2), -6, (7,), 0, (0, 1)),
    ('NONMAX-j2', 1, 'K', (-4, 2), 7, (-6, 2), -4, (7,), 0, (0, 1)),
    ('NONMAX-j2', 2, 'terminal', (-6, 2), 7, (-6, 2), 0, (7,), 0, (0, 1)),
    ('NONMAX-j3', 0, 'seed', (0, 1), 6, (-6, 2), -6, (6,), 1, (0, 1)),
    ('NONMAX-j3', 1, 'K', (-4, 2), 6, (-6, 2), -4, (6,), 1, (0, 1)),
    ('NONMAX-j3', 2, 'terminal', (-6, 2), 6, (-6, 2), 0, (6,), 1, (0, 1)),
    ('CHOICE-j0', 0, 'seed', (0, 1), 1, (2, 2), 2, (1, 2), 0, (2, 1)),
    ('CHOICE-j0', 1, 'K', (4, 2), 1, (2, 2), -4, (1, 2), 0, (2, 1)),
    ('CHOICE-j0', 2, 'terminal', (2, 2), 1, (2, 2), 0, (1, 2), 0, (2, 1)),
    ('CHOICE-j1', 0, 'seed', (0, 1), 3, (4, 2), 4, (3,), 0, (2, 1)),
    ('CHOICE-j1', 1, 'K', (6, 2), 3, (4, 2), -4, (3,), 0, (2, 1)),
    ('CHOICE-j1', 2, 'terminal', (4, 2), 3, (4, 2), 0, (3,), 0, (2, 1)),
    ('CHOICE-j2', 0, 'seed', (0, 1), 6, (-4, 4), -4, (5, 6), 0, (0, 2)),
    ('CHOICE-j2', 1, 'K', (0, 4), 6, (-4, 4), -16, (5, 6), 0, (0, 2)),
    ('CHOICE-j2', 2, 'terminal', (-4, 4), 6, (-4, 4), 0, (5, 6), 0, (0, 2)),
    ('CHOICE-j3', 0, 'seed', (0, 1), 3, (-2, 2), -2, (3, 4), 0, (2, 1)),
    ('CHOICE-j3', 1, 'K', (0, 2), 3, (-2, 2), -4, (3, 4), 0, (2, 1)),
    ('CHOICE-j3', 2, 'terminal', (-2, 2), 3, (-2, 2), 0, (3,), 0, (2, 1)),
)

# U13_TIE_TRAPS: id, solve, step, submitted_pair, selected_U, selected_pair, purpose
U13_TIE_TRAPS = (
    ('terminal-scale',
     'EQUALITY-j3',
     2,
     (-4, 4),
     1,
     (-2, 2),
     'Return submitted pair and current shore, not terminal c/h or old shore.'),
    ('terminal-shore',
     'RICH-j0',
     2,
     (4, 6),
     5,
     (4, 6),
     'Previous update selected U=6; terminal selects U=5.'),
    ('seed-nonmax-h',
     'NONMAX-j0',
     0,
     (0, 1),
     2,
     (2, 2),
     'Seed argmins (2,6,7); h=(2,4,4); no maximum-h selection.'),
    ('zero-seed',
     'ZERO-j2',
     0,
     (0, 1),
     1,
     (0, 2),
     'Zero seed continues through K=(2,2); returned root stays (0,2).'),
    ('positive-K-from-negative',
     'SHIFT-j3',
     1,
     (2, 4),
     1,
     (-2, 4),
     'Negative seed c=-2 becomes positive initial numerator 2.'),
)

# U13_LEGAL_PATHS: solve, path_id, parameter_and_shore_sequence, returned_root, terminal_U,
# t_outer_updates
U13_LEGAL_PATHS = (
    ('CHOICE-j3', 0, (((0, 1), 3), ((0, 2), 3), ((-2, 2), 3)), (-2, 2), 3, (3, 2, 1)),
    ('CHOICE-j3',
     1,
     (((0, 1), 3), ((0, 2), 4), ((-2, 4), 3), ((-2, 2), 3)),
     (-2, 2),
     3,
     (4, 3, 2)),
    ('CHOICE-j3',
     2,
     (((0, 1), 4), ((2, 4), 4), ((-2, 4), 3), ((-2, 2), 3)),
     (-2, 2),
     3,
     (4, 3, 2)),
    ('EQUALITY-j3', 0, (((0, 1), 3), ((0, 4), 3), ((-4, 4), 1)), (-4, 4), 1, (3, 2, 1)),
    ('EQUALITY-j3', 1, (((0, 1), 3), ((0, 4), 3), ((-4, 4), 2)), (-4, 4), 2, (3, 2, 1)),
    ('EQUALITY-j3', 2, (((0, 1), 3), ((0, 4), 3), ((-4, 4), 3)), (-4, 4), 3, (3, 2, 1)),
    ('EQUALITY-j3', 3, (((0, 1), 3), ((0, 4), 3), ((-4, 4), 4)), (-4, 4), 4, (3, 2, 1)),
    ('EQUALITY-j3', 4, (((0, 1), 3), ((0, 4), 3), ((-4, 4), 5)), (-4, 4), 5, (3, 2, 1)),
    ('EQUALITY-j3', 5, (((0, 1), 3), ((0, 4), 3), ((-4, 4), 6)), (-4, 4), 6, (3, 2, 1)),
    ('EQUALITY-j3', 6, (((0, 1), 3), ((0, 4), 5), ((-4, 4), 1)), (-4, 4), 1, (3, 2, 1)),
    ('EQUALITY-j3', 7, (((0, 1), 3), ((0, 4), 5), ((-4, 4), 2)), (-4, 4), 2, (3, 2, 1)),
    ('EQUALITY-j3', 8, (((0, 1), 3), ((0, 4), 5), ((-4, 4), 3)), (-4, 4), 3, (3, 2, 1)),
    ('EQUALITY-j3', 9, (((0, 1), 3), ((0, 4), 5), ((-4, 4), 4)), (-4, 4), 4, (3, 2, 1)),
    ('EQUALITY-j3', 10, (((0, 1), 3), ((0, 4), 5), ((-4, 4), 5)), (-4, 4), 5, (3, 2, 1)),
    ('EQUALITY-j3', 11, (((0, 1), 3), ((0, 4), 5), ((-4, 4), 6)), (-4, 4), 6, (3, 2, 1)),
    ('EQUALITY-j3', 12, (((0, 1), 3), ((0, 4), 6), ((-4, 4), 1)), (-4, 4), 1, (3, 2, 1)),
    ('EQUALITY-j3', 13, (((0, 1), 3), ((0, 4), 6), ((-4, 4), 2)), (-4, 4), 2, (3, 2, 1)),
    ('EQUALITY-j3', 14, (((0, 1), 3), ((0, 4), 6), ((-4, 4), 3)), (-4, 4), 3, (3, 2, 1)),
    ('EQUALITY-j3', 15, (((0, 1), 3), ((0, 4), 6), ((-4, 4), 4)), (-4, 4), 4, (3, 2, 1)),
    ('EQUALITY-j3', 16, (((0, 1), 3), ((0, 4), 6), ((-4, 4), 5)), (-4, 4), 5, (3, 2, 1)),
    ('EQUALITY-j3', 17, (((0, 1), 3), ((0, 4), 6), ((-4, 4), 6)), (-4, 4), 6, (3, 2, 1)),
    ('EQUALITY-j3', 18, (((0, 1), 5), ((0, 4), 3), ((-4, 4), 1)), (-4, 4), 1, (3, 2, 1)),
    ('EQUALITY-j3', 19, (((0, 1), 5), ((0, 4), 3), ((-4, 4), 2)), (-4, 4), 2, (3, 2, 1)),
    ('EQUALITY-j3', 20, (((0, 1), 5), ((0, 4), 3), ((-4, 4), 3)), (-4, 4), 3, (3, 2, 1)),
    ('EQUALITY-j3', 21, (((0, 1), 5), ((0, 4), 3), ((-4, 4), 4)), (-4, 4), 4, (3, 2, 1)),
    ('EQUALITY-j3', 22, (((0, 1), 5), ((0, 4), 3), ((-4, 4), 5)), (-4, 4), 5, (3, 2, 1)),
    ('EQUALITY-j3', 23, (((0, 1), 5), ((0, 4), 3), ((-4, 4), 6)), (-4, 4), 6, (3, 2, 1)),
    ('EQUALITY-j3', 24, (((0, 1), 5), ((0, 4), 5), ((-4, 4), 1)), (-4, 4), 1, (3, 2, 1)),
    ('EQUALITY-j3', 25, (((0, 1), 5), ((0, 4), 5), ((-4, 4), 2)), (-4, 4), 2, (3, 2, 1)),
    ('EQUALITY-j3', 26, (((0, 1), 5), ((0, 4), 5), ((-4, 4), 3)), (-4, 4), 3, (3, 2, 1)),
    ('EQUALITY-j3', 27, (((0, 1), 5), ((0, 4), 5), ((-4, 4), 4)), (-4, 4), 4, (3, 2, 1)),
    ('EQUALITY-j3', 28, (((0, 1), 5), ((0, 4), 5), ((-4, 4), 5)), (-4, 4), 5, (3, 2, 1)),
    ('EQUALITY-j3', 29, (((0, 1), 5), ((0, 4), 5), ((-4, 4), 6)), (-4, 4), 6, (3, 2, 1)),
    ('EQUALITY-j3', 30, (((0, 1), 5), ((0, 4), 6), ((-4, 4), 1)), (-4, 4), 1, (3, 2, 1)),
    ('EQUALITY-j3', 31, (((0, 1), 5), ((0, 4), 6), ((-4, 4), 2)), (-4, 4), 2, (3, 2, 1)),
    ('EQUALITY-j3', 32, (((0, 1), 5), ((0, 4), 6), ((-4, 4), 3)), (-4, 4), 3, (3, 2, 1)),
    ('EQUALITY-j3', 33, (((0, 1), 5), ((0, 4), 6), ((-4, 4), 4)), (-4, 4), 4, (3, 2, 1)),
    ('EQUALITY-j3', 34, (((0, 1), 5), ((0, 4), 6), ((-4, 4), 5)), (-4, 4), 5, (3, 2, 1)),
    ('EQUALITY-j3', 35, (((0, 1), 5), ((0, 4), 6), ((-4, 4), 6)), (-4, 4), 6, (3, 2, 1)),
    ('EQUALITY-j3', 36, (((0, 1), 6), ((0, 4), 3), ((-4, 4), 1)), (-4, 4), 1, (3, 2, 1)),
    ('EQUALITY-j3', 37, (((0, 1), 6), ((0, 4), 3), ((-4, 4), 2)), (-4, 4), 2, (3, 2, 1)),
    ('EQUALITY-j3', 38, (((0, 1), 6), ((0, 4), 3), ((-4, 4), 3)), (-4, 4), 3, (3, 2, 1)),
    ('EQUALITY-j3', 39, (((0, 1), 6), ((0, 4), 3), ((-4, 4), 4)), (-4, 4), 4, (3, 2, 1)),
    ('EQUALITY-j3', 40, (((0, 1), 6), ((0, 4), 3), ((-4, 4), 5)), (-4, 4), 5, (3, 2, 1)),
    ('EQUALITY-j3', 41, (((0, 1), 6), ((0, 4), 3), ((-4, 4), 6)), (-4, 4), 6, (3, 2, 1)),
    ('EQUALITY-j3', 42, (((0, 1), 6), ((0, 4), 5), ((-4, 4), 1)), (-4, 4), 1, (3, 2, 1)),
    ('EQUALITY-j3', 43, (((0, 1), 6), ((0, 4), 5), ((-4, 4), 2)), (-4, 4), 2, (3, 2, 1)),
    ('EQUALITY-j3', 44, (((0, 1), 6), ((0, 4), 5), ((-4, 4), 3)), (-4, 4), 3, (3, 2, 1)),
    ('EQUALITY-j3', 45, (((0, 1), 6), ((0, 4), 5), ((-4, 4), 4)), (-4, 4), 4, (3, 2, 1)),
    ('EQUALITY-j3', 46, (((0, 1), 6), ((0, 4), 5), ((-4, 4), 5)), (-4, 4), 5, (3, 2, 1)),
    ('EQUALITY-j3', 47, (((0, 1), 6), ((0, 4), 5), ((-4, 4), 6)), (-4, 4), 6, (3, 2, 1)),
    ('EQUALITY-j3', 48, (((0, 1), 6), ((0, 4), 6), ((-4, 4), 1)), (-4, 4), 1, (3, 2, 1)),
    ('EQUALITY-j3', 49, (((0, 1), 6), ((0, 4), 6), ((-4, 4), 2)), (-4, 4), 2, (3, 2, 1)),
    ('EQUALITY-j3', 50, (((0, 1), 6), ((0, 4), 6), ((-4, 4), 3)), (-4, 4), 3, (3, 2, 1)),
    ('EQUALITY-j3', 51, (((0, 1), 6), ((0, 4), 6), ((-4, 4), 4)), (-4, 4), 4, (3, 2, 1)),
    ('EQUALITY-j3', 52, (((0, 1), 6), ((0, 4), 6), ((-4, 4), 5)), (-4, 4), 5, (3, 2, 1)),
    ('EQUALITY-j3', 53, (((0, 1), 6), ((0, 4), 6), ((-4, 4), 6)), (-4, 4), 6, (3, 2, 1)),
    ('NONMAX-j0', 0, (((0, 1), 2), ((4, 2), 6), ((2, 4), 6)), (2, 4), 6, (3, 2, 1)),
    ('NONMAX-j0', 1, (((0, 1), 2), ((4, 2), 6), ((2, 4), 7)), (2, 4), 7, (3, 2, 1)),
    ('NONMAX-j0', 2, (((0, 1), 2), ((4, 2), 7), ((2, 4), 6)), (2, 4), 6, (3, 2, 1)),
    ('NONMAX-j0', 3, (((0, 1), 2), ((4, 2), 7), ((2, 4), 7)), (2, 4), 7, (3, 2, 1)),
    ('NONMAX-j0', 4, (((0, 1), 6), ((6, 4), 6), ((2, 4), 6)), (2, 4), 6, (3, 2, 1)),
    ('NONMAX-j0', 5, (((0, 1), 6), ((6, 4), 6), ((2, 4), 7)), (2, 4), 7, (3, 2, 1)),
    ('NONMAX-j0', 6, (((0, 1), 6), ((6, 4), 7), ((2, 4), 6)), (2, 4), 6, (3, 2, 1)),
    ('NONMAX-j0', 7, (((0, 1), 6), ((6, 4), 7), ((2, 4), 7)), (2, 4), 7, (3, 2, 1)),
    ('NONMAX-j0', 8, (((0, 1), 7), ((6, 4), 6), ((2, 4), 6)), (2, 4), 6, (3, 2, 1)),
    ('NONMAX-j0', 9, (((0, 1), 7), ((6, 4), 6), ((2, 4), 7)), (2, 4), 7, (3, 2, 1)),
    ('NONMAX-j0', 10, (((0, 1), 7), ((6, 4), 7), ((2, 4), 6)), (2, 4), 6, (3, 2, 1)),
    ('NONMAX-j0', 11, (((0, 1), 7), ((6, 4), 7), ((2, 4), 7)), (2, 4), 7, (3, 2, 1)),
    ('RICH-j0', 0, (((0, 1), 1), ((4, 2), 5), ((4, 6), 5)), (4, 6), 5, (3, 2, 1)),
    ('RICH-j0', 1, (((0, 1), 1), ((4, 2), 5), ((4, 6), 6)), (4, 6), 6, (3, 2, 1)),
    ('RICH-j0', 2, (((0, 1), 1), ((4, 2), 6), ((4, 6), 5)), (4, 6), 5, (3, 2, 1)),
    ('RICH-j0', 3, (((0, 1), 1), ((4, 2), 6), ((4, 6), 6)), (4, 6), 6, (3, 2, 1)),
    ('RICH-j0', 4, (((0, 1), 2), ((4, 2), 5), ((4, 6), 5)), (4, 6), 5, (3, 2, 1)),
    ('RICH-j0', 5, (((0, 1), 2), ((4, 2), 5), ((4, 6), 6)), (4, 6), 6, (3, 2, 1)),
    ('RICH-j0', 6, (((0, 1), 2), ((4, 2), 6), ((4, 6), 5)), (4, 6), 5, (3, 2, 1)),
    ('RICH-j0', 7, (((0, 1), 2), ((4, 2), 6), ((4, 6), 6)), (4, 6), 6, (3, 2, 1)),
    ('RICH-j3',
     0,
     (((0, 1), 15), ((-6, 4), 15), ((-10, 4), 5), ((-6, 2), 5)),
     (-6, 2),
     5,
     (4, 3, 2)),
    ('RICH-j3',
     1,
     (((0, 1), 15), ((-6, 4), 15), ((-10, 4), 5), ((-6, 2), 6)),
     (-6, 2),
     6,
     (4, 3, 2)),
    ('RICH-j3',
     2,
     (((0, 1), 15), ((-6, 4), 15), ((-10, 4), 6), ((-6, 2), 5)),
     (-6, 2),
     5,
     (4, 3, 2)),
    ('RICH-j3',
     3,
     (((0, 1), 15), ((-6, 4), 15), ((-10, 4), 6), ((-6, 2), 6)),
     (-6, 2),
     6,
     (4, 3, 2)),
)

# U13_DIAGNOSTIC_ROWS: stream, solve, step, parameter, U, injected_BranchOracleStats
U13_DIAGNOSTIC_ROWS = (
    ('nonzero', 'LOW0-j0', 0, (0, 1), 1, (11, 2, 2, 3, 5, 7, 101)),
    ('nonzero', 'LOW0-j0', 1, (20, 8), 14, (13, 3, 3, 17, 19, 23, 401)),
    ('nonzero', 'LOW0-j0', 2, (24, 14), 1, (29, 5, 5, 31, 37, 41, 211)),
    ('nonzero', 'LOW0-j0', 3, (12, 8), 1, (43, 7, 7, 47, 53, 59, 307)),
    ('zero', 'LOW0-j0', 0, (0, 1), 1, (0, 0, 0, 0, 0, 0, 0)),
    ('zero', 'LOW0-j0', 1, (20, 8), 14, (0, 0, 0, 0, 0, 0, 0)),
    ('zero', 'LOW0-j0', 2, (24, 14), 1, (0, 0, 0, 0, 0, 0, 0)),
    ('zero', 'LOW0-j0', 3, (12, 8), 1, (0, 0, 0, 0, 0, 0, 0)),
    ('infeasible-injected', 'Q1-j0', 0, (0, 1), None, (5, 3, 3, 7, 11, 13, 17)),
    ('infeasible-zero-descriptors', 'Q1-j1', 0, (0, 1), None, (0, 0, 0, 0, 0, 0, 0)),
)

# U13_DIAGNOSTIC_TOTALS: stream, returned_root, terminal_U, t_outer_updates,
# aggregate_BranchOracleStats, max_flow_calls
U13_DIAGNOSTIC_TOTALS = (
    ('nonzero', (12, 8), 1, (4, 3, 2), (96, 17, 17, 98, 114, 130, 401), 98),
    ('zero', (12, 8), 1, (4, 3, 2), (0, 0, 0, 0, 0, 0, 0), 0),
    ('infeasible-injected', None, None, (1, 0, 0), (5, 3, 3, 7, 11, 13, 17), 7),
    ('infeasible-zero-descriptors', None, None, (1, 0, 0), (0, 0, 0, 0, 0, 0, 0), 0),
)

# U13_VALID_RECORDS: target, args_expression, meaning
U13_VALID_RECORDS = (
    ('BranchResult', '((1,1),1)', 'positive root'),
    ('BranchResult', '((-4,4),1)', 'signed unreduced root'),
    ('BranchResult', '((0,7),2)', 'zero keeps denominator'),
    ('BranchResult', '((4,4),1)', 'not equal as record to ((2,2),1)'),
    ('BranchResult', '((2,2),1)', 'equal quotient but distinct raw record'),
    ('BranchResult', '((1,1),1<<130)', 'no instance-aware upper shore bound'),
    ('StandardBranchStats', '(0,0,0,Z)', 'all zero standalone'),
    ('StandardBranchStats', '(9,0,99,Z)', 'no inter-field execution equations in constructor'),
    ('StandardBranchStats', '(3,2,1,S)', 'retain supplied exact immutable oracle stats'),
)

# U13_REJECTIONS: id, target, args_expression, exception, first_guard
U13_REJECTIONS = (
    ('RJ001',
     'BranchResult',
     '(None,1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ002',
     'BranchResult',
     '(True,1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ003', 'BranchResult', '(1,1)', 'ValueError', 'root: closed validate_pair before shore'),
    ('RJ004',
     'BranchResult',
     '(1.0,1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ005',
     'BranchResult',
     "('1',1)",
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ006',
     'BranchResult',
     '([1,1],1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ007',
     'BranchResult',
     '(iter((1,1)),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ008',
     'BranchResult',
     '(TupleSub((1,1)),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ009',
     'BranchResult',
     '(ExactValue(1,1),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ010',
     'BranchResult',
     '(ExactValue(-1,1),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ011',
     'BranchResult',
     '(Fraction(1,1),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ012', 'BranchResult', '((),1)', 'ValueError', 'root: closed validate_pair before shore'),
    ('RJ013',
     'BranchResult',
     '((1,),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ014',
     'BranchResult',
     '((1,1,1),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ015',
     'BranchResult',
     '((True,1),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ016',
     'BranchResult',
     '((IntSub(1),1),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ017',
     'BranchResult',
     '((1.0,1),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ018',
     'BranchResult',
     "(('1',1),1)",
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ019',
     'BranchResult',
     '((1,True),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ020',
     'BranchResult',
     '((1,IntSub(1)),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ021',
     'BranchResult',
     '((1,1.0),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ022',
     'BranchResult',
     "((1,'1'),1)",
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ023',
     'BranchResult',
     '((1,0),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ024',
     'BranchResult',
     '((1,-1),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ025',
     'BranchResult',
     '((0,0),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ026',
     'BranchResult',
     '((-1,-1),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ027',
     'BranchResult',
     '(Hostile(),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ028',
     'BranchResult',
     '((Hostile(),1),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ029',
     'BranchResult',
     '((1,Hostile()),1)',
     'ValueError',
     'root: closed validate_pair before shore'),
    ('RJ030', 'BranchResult', '((1,1),0)', 'ValueError', 'shore: exact built-in int > 0'),
    ('RJ031', 'BranchResult', '((1,1),-1)', 'ValueError', 'shore: exact built-in int > 0'),
    ('RJ032', 'BranchResult', '((1,1),True)', 'ValueError', 'shore: exact built-in int > 0'),
    ('RJ033', 'BranchResult', '((1,1),1.0)', 'ValueError', 'shore: exact built-in int > 0'),
    ('RJ034',
     'BranchResult',
     '((1,1),IntSub(1))',
     'ValueError',
     'shore: exact built-in int > 0'),
    ('RJ035', 'BranchResult', '((1,1),None)', 'ValueError', 'shore: exact built-in int > 0'),
    ('RJ036', 'BranchResult', "((1,1),'1')", 'ValueError', 'shore: exact built-in int > 0'),
    ('RJ037',
     'BranchResult',
     '((1,1),Fraction(1,1))',
     'ValueError',
     'shore: exact built-in int > 0'),
    ('RJ038',
     'BranchResult',
     '((1,1),Hostile())',
     'ValueError',
     'shore: exact built-in int > 0'),
    ('RJ039',
     'StandardBranchStats',
     '(-1,0,0,Z)',
     'ValueError',
     'counter 0: exact built-in nonnegative int'),
    ('RJ040',
     'StandardBranchStats',
     '(True,0,0,Z)',
     'ValueError',
     'counter 0: exact built-in nonnegative int'),
    ('RJ041',
     'StandardBranchStats',
     '(1.0,0,0,Z)',
     'ValueError',
     'counter 0: exact built-in nonnegative int'),
    ('RJ042',
     'StandardBranchStats',
     '(IntSub(1),0,0,Z)',
     'ValueError',
     'counter 0: exact built-in nonnegative int'),
    ('RJ043',
     'StandardBranchStats',
     '(None,0,0,Z)',
     'ValueError',
     'counter 0: exact built-in nonnegative int'),
    ('RJ044',
     'StandardBranchStats',
     "('1',0,0,Z)",
     'ValueError',
     'counter 0: exact built-in nonnegative int'),
    ('RJ045',
     'StandardBranchStats',
     '(Fraction(1,1),0,0,Z)',
     'ValueError',
     'counter 0: exact built-in nonnegative int'),
    ('RJ046',
     'StandardBranchStats',
     '(Hostile(),0,0,Z)',
     'ValueError',
     'counter 0: exact built-in nonnegative int'),
    ('RJ047',
     'StandardBranchStats',
     '(0,-1,0,Z)',
     'ValueError',
     'counter 1: exact built-in nonnegative int'),
    ('RJ048',
     'StandardBranchStats',
     '(0,True,0,Z)',
     'ValueError',
     'counter 1: exact built-in nonnegative int'),
    ('RJ049',
     'StandardBranchStats',
     '(0,1.0,0,Z)',
     'ValueError',
     'counter 1: exact built-in nonnegative int'),
    ('RJ050',
     'StandardBranchStats',
     '(0,IntSub(1),0,Z)',
     'ValueError',
     'counter 1: exact built-in nonnegative int'),
    ('RJ051',
     'StandardBranchStats',
     '(0,None,0,Z)',
     'ValueError',
     'counter 1: exact built-in nonnegative int'),
    ('RJ052',
     'StandardBranchStats',
     "(0,'1',0,Z)",
     'ValueError',
     'counter 1: exact built-in nonnegative int'),
    ('RJ053',
     'StandardBranchStats',
     '(0,Fraction(1,1),0,Z)',
     'ValueError',
     'counter 1: exact built-in nonnegative int'),
    ('RJ054',
     'StandardBranchStats',
     '(0,Hostile(),0,Z)',
     'ValueError',
     'counter 1: exact built-in nonnegative int'),
    ('RJ055',
     'StandardBranchStats',
     '(0,0,-1,Z)',
     'ValueError',
     'counter 2: exact built-in nonnegative int'),
    ('RJ056',
     'StandardBranchStats',
     '(0,0,True,Z)',
     'ValueError',
     'counter 2: exact built-in nonnegative int'),
    ('RJ057',
     'StandardBranchStats',
     '(0,0,1.0,Z)',
     'ValueError',
     'counter 2: exact built-in nonnegative int'),
    ('RJ058',
     'StandardBranchStats',
     '(0,0,IntSub(1),Z)',
     'ValueError',
     'counter 2: exact built-in nonnegative int'),
    ('RJ059',
     'StandardBranchStats',
     '(0,0,None,Z)',
     'ValueError',
     'counter 2: exact built-in nonnegative int'),
    ('RJ060',
     'StandardBranchStats',
     "(0,0,'1',Z)",
     'ValueError',
     'counter 2: exact built-in nonnegative int'),
    ('RJ061',
     'StandardBranchStats',
     '(0,0,Fraction(1,1),Z)',
     'ValueError',
     'counter 2: exact built-in nonnegative int'),
    ('RJ062',
     'StandardBranchStats',
     '(0,0,Hostile(),Z)',
     'ValueError',
     'counter 2: exact built-in nonnegative int'),
    ('RJ063',
     'StandardBranchStats',
     '(0,0,0,None)',
     'ValueError',
     'oracle_stats: exact BranchOracleStats'),
    ('RJ064',
     'StandardBranchStats',
     '(0,0,0,(0,)*7)',
     'ValueError',
     'oracle_stats: exact BranchOracleStats'),
    ('RJ065',
     'StandardBranchStats',
     '(0,0,0,[0]*7)',
     'ValueError',
     'oracle_stats: exact BranchOracleStats'),
    ('RJ066',
     'StandardBranchStats',
     '(0,0,0,{})',
     'ValueError',
     'oracle_stats: exact BranchOracleStats'),
    ('RJ067',
     'StandardBranchStats',
     '(0,0,0,StatsSub(0,0,0,0,0,0,0))',
     'ValueError',
     'oracle_stats: exact BranchOracleStats'),
    ('RJ068',
     'StandardBranchStats',
     '(0,0,0,Hostile())',
     'ValueError',
     'oracle_stats: exact BranchOracleStats'),
    ('RJ069',
     'solve_branch_standard',
     '(None,0)',
     'ValueError',
     'context exact type; no optimizer call'),
    ('RJ070',
     'solve_branch_standard',
     '(0,0)',
     'ValueError',
     'context exact type; no optimizer call'),
    ('RJ071',
     'solve_branch_standard',
     '(True,0)',
     'ValueError',
     'context exact type; no optimizer call'),
    ('RJ072',
     'solve_branch_standard',
     '(Q1_instance,0)',
     'ValueError',
     'context exact type; no optimizer call'),
    ('RJ073',
     'solve_branch_standard',
     '({},0)',
     'ValueError',
     'context exact type; no optimizer call'),
    ('RJ074',
     'solve_branch_standard',
     '(ContextSub(Q1_instance),0)',
     'ValueError',
     'context exact type; no optimizer call'),
    ('RJ075',
     'solve_branch_standard',
     '(Hostile(),0)',
     'ValueError',
     'context exact type; no optimizer call'),
    ('RJ076',
     'solve_branch_standard',
     '(Q1_context,-1)',
     'ValueError',
     'branch exact int in (0,1,2,3); no optimizer call'),
    ('RJ077',
     'solve_branch_standard',
     '(Q1_context,4)',
     'ValueError',
     'branch exact int in (0,1,2,3); no optimizer call'),
    ('RJ078',
     'solve_branch_standard',
     '(Q1_context,True)',
     'ValueError',
     'branch exact int in (0,1,2,3); no optimizer call'),
    ('RJ079',
     'solve_branch_standard',
     '(Q1_context,0.0)',
     'ValueError',
     'branch exact int in (0,1,2,3); no optimizer call'),
    ('RJ080',
     'solve_branch_standard',
     '(Q1_context,IntSub(0))',
     'ValueError',
     'branch exact int in (0,1,2,3); no optimizer call'),
    ('RJ081',
     'solve_branch_standard',
     '(Q1_context,None)',
     'ValueError',
     'branch exact int in (0,1,2,3); no optimizer call'),
    ('RJ082',
     'solve_branch_standard',
     "(Q1_context,'0')",
     'ValueError',
     'branch exact int in (0,1,2,3); no optimizer call'),
    ('RJ083',
     'solve_branch_standard',
     '(Q1_context,Fraction(0,1))',
     'ValueError',
     'branch exact int in (0,1,2,3); no optimizer call'),
    ('RJ084',
     'solve_branch_standard',
     '(Q1_context,Hostile())',
     'ValueError',
     'branch exact int in (0,1,2,3); no optimizer call'),
    ('RJ085',
     'BranchResult',
     '()',
     'TypeError',
     'wrong positional arity retains Python behavior'),
    ('RJ086',
     'BranchResult',
     '((1,1),)',
     'TypeError',
     'wrong positional arity retains Python behavior'),
    ('RJ087',
     'BranchResult',
     '((1,1),1,0)',
     'TypeError',
     'wrong positional arity retains Python behavior'),
    ('RJ088',
     'StandardBranchStats',
     '(0,0,0)',
     'TypeError',
     'wrong positional arity retains Python behavior'),
    ('RJ089',
     'StandardBranchStats',
     '(0,0,0,Z,0)',
     'TypeError',
     'wrong positional arity retains Python behavior'),
    ('RJ090',
     'solve_branch_standard',
     '()',
     'TypeError',
     'wrong positional arity retains Python behavior'),
    ('RJ091',
     'solve_branch_standard',
     '(Q1_context,)',
     'TypeError',
     'wrong positional arity retains Python behavior'),
    ('RJ092',
     'solve_branch_standard',
     '(Q1_context,0,0)',
     'TypeError',
     'wrong positional arity retains Python behavior'),
)

# U13_INTERNAL_FAILURES: id, replace_at, replacement_expression, exception, isolated_violation
U13_INTERNAL_FAILURES = (
    ('F01', 'seed', '[R(1,2,2,2),Z]', 'RuntimeError', 'response is not exact tuple'),
    ('F02', 'seed', '()', 'RuntimeError', 'response tuple arity 0'),
    ('F03', 'seed', '(R(1,2,2,2),)', 'RuntimeError', 'response tuple arity 1'),
    ('F04', 'seed', '(R(1,2,2,2),Z,0)', 'RuntimeError', 'response tuple arity 3'),
    ('F05', 'seed', 'TupleSub((R(1,2,2,2),Z))', 'RuntimeError', 'tuple subclass'),
    ('F06', 'seed', '(0,Z)', 'RuntimeError', 'wrong result exact type'),
    ('F07', 'seed', '(ResultSub(1,2,2,2),Z)', 'RuntimeError', 'result subclass'),
    ('F08', 'seed', '(R(1,2,2,2),None)', 'RuntimeError', 'wrong stats exact type'),
    ('F09', 'seed', '(R(1,2,2,2),StatsSub(0,0,0,0,0,0,0))', 'RuntimeError', 'stats subclass'),
    ('F10', 'seed', '(R(4,2,2,2),Z)', 'RuntimeError', 'positive shore 4 outside n=2 universe'),
    ('F11', 'seed', '(R(1,2,2,3),Z)', 'RuntimeError', 'bound raw should equal 2, not 3'),
    ('F12', 'K', '(None,Z)', 'RuntimeError', 'infeasible result after feasible seed'),
    ('F13',
     'K',
     '(R(1,4,2,0),Z)',
     'RuntimeError',
     'internally bound zero violates strict-negative K'),
    ('F14',
     'K',
     '(R(1,5,2,2),Z)',
     'RuntimeError',
     'internally bound positive violates strict-negative K'),
    ('F15',
     'terminal',
     '(R(1,3,2,2),Z)',
     'RuntimeError',
     'internally bound positive later loop residual'),
    ('F16', 'terminal', '(R(1,2,2,1),Z)', 'RuntimeError', 'terminal raw binding mismatch'),
    ('F17',
     'K',
     'normal reply; compare_pairs substituted to return 0',
     'RuntimeError',
     'explicit nondecreasing-progress guard'),
    ('F18',
     'K',
     'normal reply; compare_pairs substituted to return 1',
     'RuntimeError',
     'explicit nondecreasing-progress guard'),
)

# U13_EXCEPTIONS: id, dependency, boundary
U13_EXCEPTIONS = (
    ('X01', 'exact_branch_min', 'seed'),
    ('X02', 'exact_branch_min', 'K'),
    ('X03', 'exact_branch_min', 'terminal'),
    ('X04', 'residual_numerator', 'seed binding'),
    ('X05', 'make_pair', 'initial seed pair'),
    ('X06', 'pair_add_one', 'initial K'),
    ('X07', 'make_pair', 'first negative reset'),
    ('X08', 'compare_pairs', 'first negative reset'),
    ('X09', 'validate_pair', 'BranchResult construction'),
)

# U13_REUSE: index, operation, expected_reference
U13_REUSE = (
    (0, 'solve RICH branch 0', 'RICH-j0'),
    (1, 'direct RICH branch 1 query at (0,1)', 'first row of RICH-j1'),
    (2, 'solve RICH branch 3', 'RICH-j3'),
    (3, 'solve RICH branch 0', 'RICH-j0'),
    (4, 'solve RICH branch 2', 'RICH-j2'),
    (5, 'solve RICH branch 1', 'RICH-j1'),
)

# U13_LABELS: input, labels
U13_LABELS = (
    ('RICH', ('zeta', 'alpha', 'middle', 'omega', 'beta')),
    ('RICH', (90, -7, 400, 2, 0)),
    ('LOW0', ('v3', 'v2', 'v1', 'v0')),
)

# U13_CORPUS_COUNTS: metric, value
U13_CORPUS_COUNTS = (
    ('all_empty_infeasible', 155),
    ('all_legal_paths', 5374),
    ('domain_memberships', 3354),
    ('family_examinations', 17704),
    ('feasible_family_calls', 10374),
    ('feasible_solves', 1137),
    ('full_shore_returns', 219),
    ('infeasible_solves', 179),
    ('instances', 329),
    ('n2_instances', 5),
    ('n3_instances', 324),
    ('negative_roots', 629),
    ('newton_updates', 1182),
    ('oracle_calls', 3635),
    ('outer_iterations', 2319),
    ('positive_roots', 508),
    ('solves', 1316),
    ('specified_ordinary_calls', 42302),
    ('terminal_pair_distinctions', 116),
    ('updates_1', 1092),
    ('updates_2', 45),
    ('variable_path_length_solves', 54),
    ('zero_descriptor_infeasible', 24),
)

# U13_CORPUS_BY_BRANCH: j, counts
U13_CORPUS_BY_BRANCH = (
    (0,
     {'all_empty_infeasible': 68,
      'all_legal_paths': 2128,
      'domain_memberships': 1038,
      'family_examinations': 851,
      'feasible_family_calls': 783,
      'feasible_solves': 261,
      'full_shore_returns': 67,
      'infeasible_solves': 68,
      'newton_updates': 261,
      'oracle_calls': 851,
      'outer_iterations': 522,
      'positive_roots': 261,
      'solves': 329,
      'specified_ordinary_calls': 10125,
      'terminal_pair_distinctions': 23,
      'updates_1': 261}),
    (1,
     {'all_empty_infeasible': 60,
      'all_legal_paths': 1243,
      'domain_memberships': 567,
      'family_examinations': 9620,
      'feasible_family_calls': 3708,
      'feasible_solves': 247,
      'infeasible_solves': 82,
      'newton_updates': 247,
      'oracle_calls': 823,
      'outer_iterations': 494,
      'positive_roots': 247,
      'solves': 329,
      'specified_ordinary_calls': 8028,
      'terminal_pair_distinctions': 19,
      'updates_1': 247,
      'zero_descriptor_infeasible': 22}),
    (2,
     {'all_empty_infeasible': 25,
      'all_legal_paths': 719,
      'domain_memberships': 839,
      'family_examinations': 1801,
      'feasible_family_calls': 1727,
      'feasible_solves': 302,
      'full_shore_returns': 152,
      'infeasible_solves': 27,
      'negative_roots': 302,
      'newton_updates': 327,
      'oracle_calls': 958,
      'outer_iterations': 629,
      'solves': 329,
      'specified_ordinary_calls': 11705,
      'terminal_pair_distinctions': 14,
      'updates_1': 277,
      'updates_2': 25,
      'variable_path_length_solves': 30,
      'zero_descriptor_infeasible': 2}),
    (3,
     {'all_empty_infeasible': 2,
      'all_legal_paths': 1284,
      'domain_memberships': 910,
      'family_examinations': 5432,
      'feasible_family_calls': 4156,
      'feasible_solves': 327,
      'infeasible_solves': 2,
      'negative_roots': 327,
      'newton_updates': 347,
      'oracle_calls': 1003,
      'outer_iterations': 674,
      'solves': 329,
      'specified_ordinary_calls': 12444,
      'terminal_pair_distinctions': 60,
      'updates_1': 307,
      'updates_2': 20,
      'variable_path_length_solves': 24}),
)

# U13_CORPUS_FINGERPRINTS: stream, encoding, sha256
U13_CORPUS_FINGERPRINTS = (
    ('default',
     'compact JSON '
     '[serial,n,edges,f,j,members,comparison_pair,optimizers,rows,root,U,counts,structural_counts] '
     'plus LF',
     'a3dc3671383fbcc55c463ad5c791325a60ddca3124a741cebbd9dcd738c8abd4'),
    ('any-argmin',
     'compact JSON [serial,j,all_paths] plus LF',
     '22b204da65bf0f8642115b33b49c53ce2f3a078e22bb5d9f8485c530cf7e815b'),
)

# U13_LARGE_SYMBOLS: family, q, n, edges, f, focus_branch, root, terminal_U, parameters, counts
U13_LARGE_SYMBOLS = (
    ('L', '2**k', 2, '((0,1,q),)', '(1,1)', 0, '(q,q)', 1, '((0,1),(2*q,q),(q,q))', (3, 2, 1)),
    ('N', '2**k', 2, '((0,1,q),)', '(q,q)', 3, '(-2,q)', 1, '((0,1),(q-2,q),(-2,q))', (3, 2, 1)),
    ('Z',
     '2**k+1',
     2,
     '((0,1,q),)',
     '(q,q)',
     2,
     '(0,q-1)',
     1,
     '((0,1),(q-1,q-1),(0,q-1))',
     (3, 2, 1)),
    ('NEG',
     '2**k',
     3,
     '((0,1,q),(0,2,q),(1,2,q))',
     '(1,1,1)',
     2,
     '(-6*q,2)',
     7,
     '((0,1),(-6*q+2,2),(-6*q,2))',
     (3, 2, 1)),
)

# U13_LARGE_SWEEP: family, k, four_branch_counts, peak_parameter_entry_bits, block_sha256
U13_LARGE_SWEEP = (
    ('L',
     1,
     ((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0)),
     3,
     '282784ebb7cf3bfb07035ecaa8e1d9c15170fe21f44597090d3f4f20828d3161'),
    ('L',
     2,
     ((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0)),
     4,
     '4f5dd450b1a7a63ef48d3a67538ed2ca68ffe9b8a24f44b1ff6527bb90e8213a'),
    ('L',
     7,
     ((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0)),
     9,
     'c85cfb49ac82381d16aae5c162521b7ec8203a3fa2f8135b373c451b497aa945'),
    ('L',
     31,
     ((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0)),
     33,
     '1e9cabd52acf6b4b3f5957ac405b538988c40803dfffb416241e3b0f0c2ffda6'),
    ('L',
     127,
     ((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0)),
     129,
     'a972293ea791dd247a0f53399a6b1dec86108b4e3dd4ef191cac38870bcb70f8'),
    ('L',
     1024,
     ((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0)),
     1026,
     '38cbaf79fc70728f3de9bae5f5a8437c77b6266f12f08071b8aacbcbeafde644'),
    ('L',
     4096,
     ((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0)),
     4098,
     '009a920679c036da483a2a96472dfcb8c43f58d53f14da399bbfbd3e1a01c401'),
    ('N',
     1,
     ((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1)),
     2,
     '89ebb92a02fe98a6ac30b7e4f7db805d070dc0aba5844f80283024076757c7c4'),
    ('N',
     2,
     ((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1)),
     3,
     '8ad13174640e7841abff45cf928a71fdc221bef33fa28d403025e5e7c31a6763'),
    ('N',
     7,
     ((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1)),
     8,
     '6f7ca6a04f0c998282a359bfc45630edd65d25a74c4a768b523e17ffbaf47c28'),
    ('N',
     31,
     ((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1)),
     32,
     '1ecb6171c543b6b8e460fe67f6e88074739c540130a1d2461e49b0e93c90dda9'),
    ('N',
     127,
     ((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1)),
     128,
     '5889542364c12016b1655a48fe3492a220a9c1f9ec85c84b441d92a1ca51d623'),
    ('N',
     1024,
     ((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1)),
     1025,
     '13961c991941e6f267e4b339977b5e9bf2146b44d466cc5d88c4c43296ffefdd'),
    ('N',
     4096,
     ((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1)),
     4097,
     'd2248dac4b1fc2abf39c0c9524b5283031695664fc4fd9f5fbf9017fc3a72fd4'),
    ('Z',
     1,
     ((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0)),
     2,
     'ec74180ea28187a0da218a92ce6dd8787e398759d3495ec6538567966c6742ae'),
    ('Z',
     2,
     ((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0)),
     3,
     'bc06c4b4afc06ee8e711558f8cfcb75c762458fc33784c844ffece7f91ce7a81'),
    ('Z',
     7,
     ((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0)),
     8,
     '3cf10dbb48cde2e1c237962b53d07fe3729549d08f06f7230f94af072541288a'),
    ('Z',
     31,
     ((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0)),
     32,
     'fb8256e8eaa8446920933d85e44ac9cb7c201c0f4fa732ef0966fd9a299a38dd'),
    ('Z',
     127,
     ((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0)),
     128,
     '7e6f5a81bd489f3ce9101c7b5ab22ca89b7642b4c13f4385a28205ea58130351'),
    ('Z',
     1024,
     ((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0)),
     1025,
     '69a3b1df01ba74ecb9cc8843d168645eccdade2fd80ebf80228590e4dd8c5e0b'),
    ('Z',
     4096,
     ((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0)),
     4097,
     '2cb108b2b829072fac890134655c903430fef8617b4325c8b401d65ff79d2b8b'),
    ('NEG',
     1,
     ((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1)),
     4,
     '54548b453ecd35d0fb09e98e87dc24489f5a49e0dd4ef853f75e9526e1ed14e1'),
    ('NEG',
     2,
     ((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1)),
     5,
     'eea1c56c4e7387927b42249cb6d055f3c213fc3adb9da85b8cb0af6e4c894da1'),
    ('NEG',
     7,
     ((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1)),
     10,
     '226a262c0852065dc84c91516a11ace9dcfcd5f22eb7ae5a7937453ae8cf1ca5'),
    ('NEG',
     31,
     ((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1)),
     34,
     'fd4197d5af27a5cbf779eb5788e4b85ae548f590327a72608ac2c282e6203c6d'),
    ('NEG',
     127,
     ((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1)),
     130,
     'd49a9eb67f7029e4538dcf84b2e162c2aeff943debc5d69f6abe3565f01cef78'),
    ('NEG',
     1024,
     ((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1)),
     1027,
     'd4c203c6ab6aa4400e644dc91384d94c6d18b4941179fa3120477168845a5c20'),
    ('NEG',
     4096,
     ((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1)),
     4099,
     '28af42e213057470abfb0e5ade059a8b7e47ef8d3246c9795062f674addeb9c7'),
)

# U13_LARGE_COUNTS: metric, value
U13_LARGE_COUNTS = (
    ('feasible_solves', 49),
    ('infeasible_solves', 63),
    ('oracle_calls', 210),
    ('solves', 112),
)

# U13_CARRIER_COUNTS: metric, value
U13_CARRIER_COUNTS = (
    ('residual_checks', 11353),
    ('wyz_checks', 7634),
)

# Each table retains its catalogue column order. No external data are read at runtime.
_INPUTS = {row[0]: row[1:4] for row in U13_INPUTS}
_SOLVES = {row[0]: row[1:] for row in U13_SOLVES}
_OPTIMA = {row[0]: row[1:] for row in U13_OPTIMA}
_TRACES = {
    row[0]: tuple(trace[3:] for trace in U13_TRACES if trace[0] == row[0])
    for row in U13_SOLVES
}
_STATS_FIELDS = (
    "atomic_families_examined", "atomic_families_feasible", "parity_cut_calls",
    "ordinary_min_cut_calls", "flow_augmentations", "flow_bfs_scans",
    "flow_peak_generated_value",
)
_ZERO = BranchOracleStats(0, 0, 0, 0, 0, 0, 0)
_DEPENDENCIES = {
    "exact_branch_min": oracle_module.exact_branch_min,
    "validate_pair": rational_module.validate_pair,
    "make_pair": rational_module.make_pair,
    "pair_add_one": rational_module.pair_add_one,
    "compare_pairs": rational_module.compare_pairs,
    "residual_numerator": rational_module.residual_numerator,
}


def _degree(n, edges):
    return tuple(sum(q for a, b, q in edges if v in (a, b)) for v in range(n))


def _quantities(n, edges, f, shore):
    members = tuple(v for v in range(n) if shore & (1 << v))
    s = sum(f[v] for v in members)
    internal = sum(q for a, b, q in edges if a in members and b in members)
    boundary = sum(q for a, b, q in edges if (a in members) != (b in members))
    return s, internal, boundary, 2 * internal + boundary


class _Source:
    """Literal original-shore domains, independent of any production family/cut code."""

    def __init__(self, n, edges, f, branch):
        self.n, self.edges, self.f, self.branch = n, edges, f, branch
        self.quantities = tuple(_quantities(n, edges, f, u) for u in range(1 << n))
        self.pairs = []
        self.members = []
        for u, (s, _e, b, d) in enumerate(self.quantities):
            inside = (
                (s + b) % 2 == 1,
                (s + b) % 2 == 0 and b >= 1 and d > s,
                s % 2 == 1 and s >= 3,
                s % 2 == 0 and b >= 1,
            )[branch]
            pair = ((s + b - 1, d + 1 - s), (s + b - 2, d - s),
                    (b - d, s - 1), (b - d - 2, s))[branch]
            self.pairs.append(pair)
            if u and inside:
                assert pair[1] > 0
                self.members.append(u)
        self.pairs, self.members = tuple(self.pairs), tuple(self.members)
        if self.members:
            first = min(self.members, key=lambda u: Fraction(*self.pairs[u]))
            self.optimum = self.pairs[first]
            self.optimizers = tuple(
                u for u in self.members if Fraction(*self.pairs[u]) == Fraction(*self.optimum)
            )
        else:
            self.optimum, self.optimizers = None, ()

    def raw(self, parameter, shore):
        c, h = self.pairs[shore]
        return parameter[1] * c - parameter[0] * h

    def query(self, parameter):
        if not self.members:
            return None, ()
        value = min(self.raw(parameter, u) for u in self.members)
        return value, tuple(u for u in self.members if self.raw(parameter, u) == value)


def _cover(source):
    """Plain tuple rendition of the separately ruled deterministic family order."""
    n, edges, f, j = source.n, source.edges, source.f, source.branch
    degree = _degree(n, edges)
    tp = sum(1 << v for v in range(n) if (f[v] + degree[v]) % 2)
    tf = sum(1 << v for v in range(n) if f[v] % 2)
    out = []
    if j == 0:
        out.append((tp, 1, 0, 0))
    elif j == 1:
        for p in range(n):
            if degree[p] > f[p]:
                for u, v, _q in edges:
                    out.extend(((tp, 0, (1 << p) | (1 << u), 1 << v),
                                (tp, 0, (1 << p) | (1 << v), 1 << u)))
    elif j == 2:
        out.extend((tf, 1, 1 << v, 0) for v in range(n) if f[v] >= 2)
        unit_vertices = tuple(v for v in range(n) if f[v] == 1)
        out.extend((tf, 1, sum(1 << v for v in tri), 0)
                   for tri in combinations(unit_vertices, 3))
    else:
        for u, v, _q in edges:
            out.extend(((tf, 0, 1 << u, 1 << v), (tf, 0, 1 << v, 1 << u)))
    return tuple(out)


class _Ordered:
    """Exhaustive ordinary-restriction intersections; never a flow implementation."""

    def __init__(self, source):
        self.source = source
        self.cover = _cover(source)
        self.pools = []
        feasible = ordinary = 0
        covered = set()
        for terminals, parity, forced_in, forced_out in self.cover:
            cube = tuple(u for u in range(1 << source.n)
                         if u & forced_in == forced_in and not u & forced_out)
            members = tuple(u for u in cube if (u & terminals).bit_count() % 2 == parity)
            covered.update(members)
            pools = []
            if members:
                feasible += 1
                free = tuple(v for v in range(source.n)
                             if not (forced_in | forced_out) & (1 << v))
                node_count = 2 + len(free)
                for inside in range(node_count):
                    if inside == 1:
                        continue
                    for outside in range(node_count):
                        if outside == 0 or outside == inside:
                            continue
                        restricted = tuple(
                            u for u in cube
                            if (inside == 0 or u & (1 << free[inside - 2]))
                            and (outside == 1 or not u & (1 << free[outside - 2]))
                        )
                        assert restricted
                        pools.append(((inside, outside), restricted))
                assert len(pools) == node_count * node_count - 3 * node_count + 3
                ordinary += len(pools)
            self.pools.append(tuple(pools))
        assert covered == set(source.members)
        self.counts = len(self.cover), feasible, feasible, ordinary

    def row(self, parameter):
        minimum, argmins = self.source.query(parameter)
        winner = None
        for fi, (family, pools) in enumerate(zip(self.cover, self.pools, strict=True)):
            terminals, parity, _i, _o = family
            for pair, masks in pools:
                value = min(self.source.raw(parameter, u) for u in masks)
                tied = tuple(u for u in masks if self.source.raw(parameter, u) == value)
                least = (1 << self.source.n) - 1
                for u in tied:
                    least &= u
                assert least in tied
                if ((least & terminals).bit_count() % 2 == parity
                        and (winner is None or value < winner[0])):
                    winner = value, least, fi, pair
        if winner is None:
            assert not argmins
            return parameter, None, None, None, (), None, None
        value, u, fi, pair = winner
        assert value == minimum and u in argmins
        return parameter, u, self.source.pairs[u], value, argmins, fi, pair


def _reference(source):
    """Freeze the source-only Standard sequence before invoking the tested wrapper."""
    selector = _Ordered(source)
    rows = [selector.row((0, 1))]
    if rows[0][1] is None:
        return tuple(rows), None, None, (1, 0, 0), selector.counts
    c0, h0 = rows[0][2]
    parameter = c0 + h0, h0
    updates = 0
    while True:
        row = selector.row(parameter)
        rows.append(row)
        assert row[1] is not None
        if row[3] == 0:
            assert updates >= 1
            return tuple(rows), parameter, row[1], (len(rows), len(rows) - 1, updates), \
                selector.counts
        assert row[3] < 0
        fresh = row[2]
        assert Fraction(*source.optimum) <= Fraction(*fresh) < Fraction(*parameter)
        parameter = fresh
        updates += 1


def _legal_paths(source):
    """All exact argmin paths, including seed and terminal choices; test-side only."""
    _value, seeds = source.query((0, 1))
    if not seeds:
        return ((((0, 1), None),),)

    def descend(parameter):
        value, argmins = source.query(parameter)
        assert argmins and value <= 0
        if value == 0:
            return tuple(((parameter, u),) for u in argmins)
        paths = []
        for u in argmins:
            fresh = source.pairs[u]
            assert Fraction(*fresh) < Fraction(*parameter)
            for suffix in descend(fresh):
                paths.append(((parameter, u), *suffix))
        return tuple(paths)

    paths = []
    for u in seeds:
        c, h = source.pairs[u]
        for suffix in descend((c + h, h)):
            paths.append((((0, 1), u), *suffix))
    return tuple(paths)


def _rows_for_path(source, path):
    out = []
    for parameter, u in path:
        value, argmins = source.query(parameter)
        if u is None:
            assert not argmins and len(path) == 1
            pair = None
        else:
            assert u in argmins
            pair = source.pairs[u]
        out.append((parameter, u, pair, value, argmins, None, None))
    return tuple(out)


def _assert_plan(source, rows):
    assert rows and rows[0][0] == (0, 1)
    if not source.members:
        assert rows == (((0, 1), None, None, None, (), None, None),)
        return
    for i, (parameter, u, pair, raw, argmins, _fi, _gr) in enumerate(rows):
        assert type(parameter) is tuple and len(parameter) == 2
        assert all(type(v) is int for v in parameter) and parameter[1] > 0
        expected_raw, expected_args = source.query(parameter)
        assert raw == expected_raw and argmins == expected_args and u in argmins
        assert pair == source.pairs[u]
        if i == 0:
            c, h = pair
            assert len(rows) >= 3 and rows[1][0] == (c + h, h)
        elif i == len(rows) - 1:
            assert raw == 0
            assert Fraction(*parameter) == Fraction(*source.optimum)
            assert u in source.optimizers
        else:
            assert raw < 0 and rows[i + 1][0] == pair
            assert Fraction(*source.optimum) <= Fraction(*pair) < Fraction(*parameter)


def _core():
    serial = 0
    for n in (2, 3):
        pairs = tuple(combinations(range(n), 2))
        for values in product(range(3), repeat=len(pairs)):
            edges = tuple((a, b, q) for (a, b), q in zip(pairs, values, strict=True) if q)
            degrees = _degree(n, edges)
            if not all(degrees):
                continue
            for f in product(*(range(1, d + 1) for d in degrees)):
                yield serial, n, edges, f
                serial += 1


def _wire(value):
    return (json.dumps(value, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def _large(family, k):
    q = (1 << k) + (family == "Z")
    if family == "NEG":
        return 3, ((0, 1, q), (0, 2, q), (1, 2, q)), (1, 1, 1)
    return 2, ((0, 1, q),), (1, 1) if family == "L" else (q, q)


def _carriers(source, rows):
    q_total = sum(q for _a, _b, q in source.edges)
    c_bound, h_bound = 3 * q_total + 2, 2 * q_total + 1
    residuals = wyz = 0
    for i, row in enumerate(rows):
        a, b = row[0]
        assert abs(a) <= c_bound + h_bound and 1 <= b <= h_bound
        if i >= 2:
            assert abs(a) <= c_bound
        for u in source.members:
            c, h = source.pairs[u]
            assert abs(c) <= c_bound and 1 <= h <= h_bound
            assert abs(b * c - a * h) <= b * c_bound + abs(a) * h_bound
            assert b * c_bound + abs(a) * h_bound <= h_bound * (2 * c_bound + h_bound)
            residuals += 1
    if source.members:
        c0, h0 = rows[0][2]
        ka, kb = c0 + h0, h0
        assert ka * h0 - kb * c0 == h0 * h0 > 0
        for row in rows[1:]:
            a, b = row[0]
            delta_n, delta_d = ka * b - a * kb, kb * b
            for u in source.members:
                c, h = source.pairs[u]
                aa, bb = ka * h - kb * c, kb * h
                assert bb > 0
                assert aa * delta_d - delta_n * bb == -kb * kb * (b * c - a * h)
                wyz += 1
    return residuals, wyz


def _statistics(record):
    return tuple(getattr(record, name) for name in _STATS_FIELDS)


def _aggregate(records):
    rows = tuple(_statistics(record) for record in records)
    return (*(sum(row[i] for row in rows) for i in range(6)),
            max((row[6] for row in rows), default=0))


def _patch_dependency(patch, name, replacement):
    """Patch the actual imported binding, also accepting an ordinary import alias."""
    original = _DEPENDENCIES[name]
    bindings = [key for key, value in vars(_BRANCH).items() if value is original]
    assert bindings, ("required closed dependency missing", name)
    for key in bindings:
        patch.setattr(_BRANCH, key, replacement)


def _snapshot(context):
    instance = context.instance
    return (
        instance.n, instance.edges, instance.f, instance.labels,
        tuple(tuple((x.T, x.pi, x.I, x.O) for x in group) for group in context.families),
    )


def _assert_result(packet, source, rows, records, counts, structural=None):
    assert type(packet) is tuple and len(packet) == 2
    result, stats = packet
    assert type(stats) is _BRANCH.StandardBranchStats
    actual_counts = stats.oracle_calls, stats.outer_iterations, stats.newton_updates
    assert actual_counts == counts
    assert all(type(x) is int for x in actual_counts)
    assert type(stats.oracle_stats) is BranchOracleStats
    assert _statistics(stats.oracle_stats) == _aggregate(records)
    assert stats.oracle_stats.max_flow_calls == stats.oracle_stats.ordinary_min_cut_calls
    if structural is not None:
        assert _statistics(stats.oracle_stats)[:4] == tuple(counts[0] * x for x in structural)
    if not source.members:
        assert result is None and counts == (1, 0, 0)
    else:
        assert type(result) is _BRANCH.BranchResult
        assert type(result.root) is tuple and all(type(x) is int for x in result.root)
        assert type(result.shore) is int
        assert result.root == rows[-1][0] and result.shore == rows[-1][1]
        assert result.shore in source.optimizers
        c, h = source.pairs[result.shore]
        assert result.root[0] * h == result.root[1] * c
        assert Fraction(*result.root) == Fraction(*source.optimum)
        assert counts[2] >= 1 and counts == (counts[2] + 2, counts[2] + 1, counts[2])
    return result, stats


def _exercise(patch, context, source, rows, counts, structural=None, injected=None):
    """Every expected parameter/reply is fixed before the SUT gets control."""
    _assert_plan(source, rows)
    before = _snapshot(context)
    records, calls = [], []

    def query(given_context, branch, parameter):
        k = len(calls)
        assert given_context is context and type(branch) is int and branch == source.branch
        assert k < len(rows), "unexpected extra optimizer query"
        expected = rows[k]
        assert type(parameter) is tuple and parameter == expected[0]
        assert all(type(x) is int for x in parameter)
        calls.append((parameter, expected[1]))
        if injected is None:
            reply, stats = oracle_module.exact_branch_min(given_context, branch, parameter)
            assert type(stats) is BranchOracleStats
            if structural is not None:
                assert _statistics(stats)[:4] == structural
        else:
            stats = injected[k]
            reply = None if expected[1] is None else BranchOracleResult(
                expected[1], *expected[2], expected[3],
            )
        if expected[1] is None:
            assert reply is None
        else:
            assert type(reply) is BranchOracleResult
            assert (reply.shore, (reply.c, reply.h), reply.residual) == expected[1:4]
        records.append(stats)
        return reply, stats

    _patch_dependency(patch, "exact_branch_min", query)
    packet = _BRANCH.solve_branch_standard(context, source.branch)
    assert tuple(calls) == tuple((row[0], row[1]) for row in rows)
    assert _snapshot(context) == before
    _assert_result(packet, source, rows, records, counts, structural)
    return packet, tuple(calls), tuple(records)


class _IntSub(int):
    pass


class _TupleSub(tuple):
    pass


class _StatsSub(BranchOracleStats):
    pass


class _ResultSub(BranchOracleResult):
    pass


class _ContextSub(BranchOracleContext):
    pass


class _Touched(Exception):
    pass


class _Hostile:
    def _fail(self, *_args, **_kwargs):
        raise _Touched("a rejected object was inspected or coerced")

    __int__ = __index__ = __float__ = __bool__ = _fail
    __eq__ = __lt__ = __le__ = __gt__ = __ge__ = _fail
    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = _fail
    __iter__ = __len__ = __getitem__ = __getattr__ = _fail


def _vocabulary():
    instance = Instance(*_INPUTS["Q1"])
    return {
        "Z": _ZERO, "S": BranchOracleStats(1, 1, 1, 7, 2, 9, 11),
        "Q1_instance": instance, "Q1_context": BranchOracleContext(instance),
        "IntSub": _IntSub, "TupleSub": _TupleSub, "StatsSub": _StatsSub,
        "ResultSub": _ResultSub, "ContextSub": _ContextSub, "Hostile": _Hostile,
        "Fraction": Fraction, "ExactValue": ExactValue, "R": BranchOracleResult,
        "iter": iter,
    }


def _expression(text, names):
    # Only this test's committed literal declarations are evaluated, with no builtins.
    # The AST check below forbids attribute access and unlisted call targets.
    tree = ast.parse(text, mode="eval")
    permitted = (ast.Expression, ast.Constant, ast.Tuple, ast.List, ast.Dict,
                 ast.Name, ast.Load, ast.Call, ast.BinOp, ast.UnaryOp,
                 ast.Add, ast.Sub, ast.Mult, ast.LShift, ast.USub, ast.UAdd)
    assert all(isinstance(node, permitted) for node in ast.walk(tree))
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            assert node.id in names
        if isinstance(node, ast.Call):
            assert isinstance(node.func, ast.Name) and not node.keywords
    return eval(compile(tree, "<committed-test-declaration>", "eval"), {"__builtins__": {}}, names)


def _source_violations(text):
    """Finite AST guard, not a replacement for the later independent code audit."""
    tree = ast.parse(text)
    problems = []
    permitted = {
        "__future__": {"annotations"}, "dataclasses": {"dataclass"},
        "oracle": {"BranchOracleContext", "BranchOracleResult", "BranchOracleStats",
                   "exact_branch_min"},
        "rational": {"RawPair", "validate_pair", "make_pair", "pair_add_one",
                     "compare_pairs", "residual_numerator"},
    }
    forbidden_calls = {
        "float", "Fraction", "int", "gcd", "set", "frozenset", "eval", "exec",
        "compile", "open", "__import__", "getattr", "setattr", "hasattr", "delattr",
        "globals", "locals", "vars", "dir", "print", "input", "pair_reflect",
    }
    forbidden_attributes = {"families", "is_nonempty", "edges", "Q", "q", "f", "d_q"}
    imports = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            problems.append("unapproved direct import")
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            short = module.removeprefix("exactfrac.")
            approved = permitted.get(short)
            level_ok = (
                (node.level == 0 and short in ("dataclasses", "__future__"))
                or (node.level == 1 and module in ("oracle", "rational"))
                or (node.level == 0 and module in ("exactfrac.oracle", "exactfrac.rational"))
            )
            if not level_ok or approved is None or any(x.name not in approved for x in node.names):
                problems.append("unapproved direct import")
            for alias in node.names:
                imports[alias.asname or alias.name] = alias.name
        if isinstance(node, ast.Constant) and type(node.value) is float:
            problems.append("floating literal")
        if isinstance(node, (ast.Div, ast.FloorDiv, ast.Mod)):
            problems.append("division or remainder")
        if isinstance(node, (ast.Set, ast.SetComp)):
            problems.append("set construction")
        if isinstance(node, ast.Attribute) and node.attr in forbidden_attributes:
            problems.append("unapproved graph/family inspection")
        if isinstance(node, ast.Call):
            name = node.func.id if isinstance(node.func, ast.Name) else (
                node.func.attr if isinstance(node.func, ast.Attribute) else ""
            )
            if imports.get(name, name) in forbidden_calls:
                problems.append("forbidden call")
            if name == "range" and any(
                isinstance(x, (ast.LShift, ast.Pow))
                for argument in node.args for x in ast.walk(argument)
            ):
                problems.append("explicit all-shore range")
    functions = {node.name: (node, None) for node in tree.body
                 if isinstance(node, ast.FunctionDef)}
    for cls in tree.body:
        if isinstance(cls, ast.ClassDef):
            for method in cls.body:
                if isinstance(method, ast.FunctionDef):
                    functions[f"{cls.name}.{method.name}"] = method, cls.name
    edges = {name: set() for name in functions}
    optimizer_users = set()
    for name, (body, owner) in functions.items():
        for node in ast.walk(body):
            if not isinstance(node, ast.Call):
                continue
            called = node.func.id if isinstance(node.func, ast.Name) else None
            if (
                isinstance(node.func, ast.Attribute) and owner is not None
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "self"
            ):
                called = f"{owner}.{node.func.attr}"
            if called in functions:
                edges[name].add(called)
            if imports.get(called, called) == "exact_branch_min":
                optimizer_users.add(name)
    for root in edges:
        pending = list(edges[root])
        seen = set()
        while pending:
            nxt = pending.pop()
            if nxt == root:
                problems.append("recursive call cycle")
                break
            if nxt not in seen:
                seen.add(nxt)
                pending.extend(edges[nxt])
    changed = True
    while changed:
        prior = optimizer_users.copy()
        optimizer_users.update(name for name, targets in edges.items()
                               if targets & optimizer_users)
        changed = optimizer_users != prior
    for node in ast.walk(tree):
        if not isinstance(node, (ast.For, ast.While)):
            continue
        has_optimizer = any(
            isinstance(child, ast.Call) and isinstance(child.func, ast.Name)
            and (child.func.id in optimizer_users
                 or imports.get(child.func.id, child.func.id) == "exact_branch_min")
            for child in ast.walk(node)
        )
        if isinstance(node, ast.While) and has_optimizer and any(
            isinstance(x, ast.Constant) and type(x.value) is int and x.value != 0
            for x in ast.walk(node.test)
        ):
            problems.append("numeric optimizer loop budget")
        if (isinstance(node, ast.For) and has_optimizer and isinstance(node.iter, ast.Call)
                and isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range"):
            problems.append("finite range optimizer budget")
    return problems


def test_public_surface_signatures_annotations_and_package_root():
    assert _BRANCH.__all__ == ("BranchResult", "StandardBranchStats", "solve_branch_standard")
    shapes = (
        (_BRANCH.BranchResult, ("root", "shore"), {"root": RawPair, "shore": int}),
        (_BRANCH.StandardBranchStats,
         ("oracle_calls", "outer_iterations", "newton_updates", "oracle_stats"),
         {"oracle_calls": int, "outer_iterations": int, "newton_updates": int,
          "oracle_stats": BranchOracleStats}),
    )
    for cls, names, hints in shapes:
        assert is_dataclass(cls)
        assert tuple(x.name for x in fields(cls)) == names
        assert cls.__slots__ == names
        assert get_type_hints(cls) == hints
        assert get_type_hints(cls.__init__) == {**hints, "return": type(None)}
        assert cls.__dataclass_params__.frozen and not cls.__dataclass_params__.order
        assert cls.__dataclass_params__.eq
        assert all(x.default is MISSING and x.default_factory is MISSING for x in fields(cls))
        parameters = tuple(inspect.signature(cls).parameters.values())
        assert tuple(p.name for p in parameters) == names
        assert all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD for p in parameters)
        assert all(p.default is inspect.Parameter.empty for p in parameters)
    fun = _BRANCH.solve_branch_standard
    signature = inspect.signature(fun)
    assert tuple(signature.parameters) == ("context", "branch")
    assert all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
               and p.default is inspect.Parameter.empty for p in signature.parameters.values())
    assert get_type_hints(fun) == {
        "context": BranchOracleContext, "branch": int,
        "return": tuple[_BRANCH.BranchResult | None, _BRANCH.StandardBranchStats],
    }
    root = importlib.import_module("exactfrac")
    assert not getattr(root, "__all__", ())
    assert all(not hasattr(root, name) for name in _BRANCH.__all__)


def test_records_are_frozen_slotted_structural_and_not_certificates():
    cls, stats_cls = _BRANCH.BranchResult, _BRANCH.StandardBranchStats
    for record in (cls((-4, 4), 1), stats_cls(9, 0, 99, _ZERO)):
        assert not hasattr(record, "__dict__")
        values = tuple(getattr(record, field.name) for field in fields(record))
        twin = type(record)(*values)
        assert twin == record and hash(twin) == hash(record)
        for field in fields(record):
            with pytest.raises(FrozenInstanceError):
                setattr(record, field.name, None)
        assert tuple(getattr(record, field.name) for field in fields(record)) == values
        with pytest.raises(TypeError):
            _ = record < twin
    assert cls((4, 4), 1) != cls((2, 2), 1)
    assert Fraction(4, 4) == Fraction(2, 2)
    assert cls((0, 7), 2).root == (0, 7)
    assert cls((-4, 4), 1).root == (-4, 4)
    assert cls((1, 1), 1 << 130).shore == 1 << 130
    assert stats_cls(9, 0, 99, _ZERO).oracle_stats is _ZERO
    assert cls((1, 1), 1) != cls((1, 1), 2)


def test_all_nine_registered_accepted_record_declarations():
    names = _vocabulary()
    assert len(U13_VALID_RECORDS) == 9
    for target, expression, _meaning in U13_VALID_RECORDS:
        arguments = _expression(expression, names)
        record = getattr(_BRANCH, target)(*arguments)
        assert type(record) is getattr(_BRANCH, target)
        assert tuple(getattr(record, f.name) for f in fields(record)) == arguments
        if target == "StandardBranchStats":
            assert record.oracle_stats is arguments[3]


def test_all_92_registered_public_rejections_and_python_arity(monkeypatch):
    names = _vocabulary()
    assert len(U13_REJECTIONS) == 92

    def forbidden(*_args, **_kwargs):
        raise _Touched("optimizer called for invalid public input")

    with monkeypatch.context() as patch:
        _patch_dependency(patch, "exact_branch_min", forbidden)
        for identifier, target, expression, exception, _guard in U13_REJECTIONS:
            arguments = _expression(expression, names)
            expected = {"ValueError": ValueError, "TypeError": TypeError}[exception]
            with pytest.raises(expected) as caught:
                getattr(_BRANCH, target)(*arguments)
            assert type(caught.value) is expected, identifier


def test_result_root_guard_and_statistics_field_validation_order(monkeypatch):
    sentinel = _Touched("closed root guard")

    def first(pair):
        assert pair is None
        raise sentinel

    with monkeypatch.context() as patch:
        _patch_dependency(patch, "validate_pair", first)
        with pytest.raises(_Touched) as caught:
            _BRANCH.BranchResult(None, _Hostile())
        assert caught.value is sentinel

    for bad_at in range(4):
        values = [17, 19, 23, _ZERO]
        values[bad_at] = _Hostile()
        for later in range(bad_at + 1, 4):
            values[later] = _Hostile()
        observed = []

        def watch_type(value, _values=values, _observed=observed):
            for i, item in enumerate(_values):
                if value is item:
                    _observed.append(i)
            return type(value)

        with monkeypatch.context() as patch:
            patch.setattr(_BRANCH, "type", watch_type, raising=False)
            with pytest.raises(ValueError) as caught:
                _BRANCH.StandardBranchStats(*values)
            assert type(caught.value) is ValueError
        first_occurrences = tuple(dict.fromkeys(observed))
        assert first_occurrences == tuple(range(bad_at + 1)), (bad_at, observed)


def test_public_validation_precedes_graph_access_and_seed(monkeypatch):
    context = BranchOracleContext(Instance(*_INPUTS["Q1"]))
    context_descriptor = BranchOracleContext.__getattribute__

    def deny_graph(self, key):
        if key in ("instance", "families"):
            raise _Touched("graph inspected before public validation")
        return context_descriptor(self, key)

    def forbidden(*_args, **_kwargs):
        raise _Touched("optimizer called before public validation")

    for given, branch in ((None, _Hostile()), (_Hostile(), _Hostile()),
                          (context, _Hostile()), (context, True), (context, -1)):
        checks = []

        def watch_type(value, _given=given, _branch=branch, _checks=checks):
            if value is _given:
                _checks.append("context")
            elif value is _branch:
                _checks.append("branch")
            return type(value)

        with monkeypatch.context() as patch:
            patch.setattr(BranchOracleContext, "__getattribute__", deny_graph)
            patch.setattr(_BRANCH, "type", watch_type, raising=False)
            _patch_dependency(patch, "exact_branch_min", forbidden)
            with pytest.raises(ValueError) as caught:
                _BRANCH.solve_branch_standard(given, branch)
            assert type(caught.value) is ValueError
        assert checks and checks[0] == "context"
        if type(given) is not BranchOracleContext:
            assert "branch" not in checks
        else:
            assert "branch" in checks


def test_literal_shores_domains_and_complete_optima_are_independent():
    assert len(U13_INPUTS) == 17 and len(U13_SHORES) == 163 and len(U13_OPTIMA) == 68
    for name, n, edges, f, degree, q_total in U13_INPUTS:
        assert _degree(n, edges) == degree and sum(q for _a, _b, q in edges) == q_total
        sources = tuple(_Source(n, edges, f, j) for j in range(4))
        for row in U13_SHORES:
            if row[0] == name:
                _name, u, s, e, b, d, flags, pairs = row
                assert _quantities(n, edges, f, u) == (s, e, b, d)
                assert flags == tuple(u in source.members for source in sources)
                assert pairs == tuple(source.pairs[u] if flags[j] else None
                                      for j, source in enumerate(sources))
        for j, source in enumerate(sources):
            assert _OPTIMA[f"{name}-j{j}"] == (
                source.members, source.optimum, source.optimizers,
            )


def test_all_68_literal_shipped_trajectories_and_complete_accounting(monkeypatch):
    assert len(U13_SOLVES) == 68 and len(U13_TRACES) == 168
    for key, root, terminal, counts, structural, aggregate in U13_SOLVES:
        name, j = key.rsplit("-j", 1)
        source = _Source(*_INPUTS[name], int(j))
        rows = _TRACES[key]
        assert _reference(source) == (rows, root, terminal, counts, structural)
        context = BranchOracleContext(Instance(*_INPUTS[name]))
        with monkeypatch.context() as patch:
            packet, _calls, _records = _exercise(
                patch, context, source, rows, counts, structural,
            )
        assert _statistics(packet[1].oracle_stats)[:4] == aggregate


def test_seed_is_mandatory_for_zero_and_all_empty_descriptor_branches(monkeypatch):
    for name in ("Q1", "DOUBLE", "EQUALITY"):
        context = BranchOracleContext(Instance(*_INPUTS[name]))
        for j in range(4):
            source = _Source(*_INPUTS[name], j)
            if source.members:
                continue
            key = f"{name}-j{j}"
            _root, _u, counts, structural, _aggregate_row = _SOLVES[key]
            with monkeypatch.context() as patch:
                result, calls, _records = _exercise(
                    patch, context, source, _TRACES[key], counts, structural,
                )
            assert result[0] is None and calls == (((0, 1), None),)
    assert _SOLVES["Q1-j1"][3][0] == 0
    assert _SOLVES["Q1-j0"][3][0] > 0


def test_zero_seed_continues_and_negative_seed_can_give_positive_k(monkeypatch):
    for key in ("ZERO-j2", "SHIFT-j3"):
        name, branch = key.rsplit("-j", 1)
        source = _Source(*_INPUTS[name], int(branch))
        rows = _TRACES[key]
        with monkeypatch.context() as patch:
            _exercise(patch, BranchOracleContext(Instance(*_INPUTS[name])), source,
                      rows, _SOLVES[key][2], _SOLVES[key][3])
    assert _TRACES["ZERO-j2"][0][3] == 0
    assert _TRACES["ZERO-j2"][1][0] == (2, 2)
    assert _SOLVES["ZERO-j2"][0] == (0, 2)
    assert _TRACES["SHIFT-j3"][0][2][0] < 0 < _TRACES["SHIFT-j3"][1][0][0]


def test_terminal_parameter_and_current_shore_are_separately_preserved(monkeypatch):
    for key in ("EQUALITY-j3", "RICH-j0"):
        name, branch = key.rsplit("-j", 1)
        source = _Source(*_INPUTS[name], int(branch))
        rows = _TRACES[key]
        with monkeypatch.context() as patch:
            packet, _calls, _records = _exercise(
                patch, BranchOracleContext(Instance(*_INPUTS[name])), source,
                rows, _SOLVES[key][2], _SOLVES[key][3],
            )
        assert packet[0].shore == rows[-1][1] != rows[-2][1]
        if key == "EQUALITY-j3":
            assert packet[0].root == (-4, 4) != rows[-1][2] == (-2, 2)


def test_all_four_branches_execute_multiple_fresh_newton_resets(monkeypatch):
    for key in ("LOW0-j0", "LOW1-j1", "HIGH2-j2", "HIGH3-j3"):
        name, branch = key.rsplit("-j", 1)
        source = _Source(*_INPUTS[name], int(branch))
        with monkeypatch.context() as patch:
            packet, _calls, _records = _exercise(
                patch, BranchOracleContext(Instance(*_INPUTS[name])), source,
                _TRACES[key], _SOLVES[key][2], _SOLVES[key][3],
            )
        assert packet[1].newton_updates == 2


def test_all_81_named_legal_argmin_paths_without_secondary_preference(monkeypatch):
    assert len(U13_LEGAL_PATHS) == 81
    for key in dict.fromkeys(row[0] for row in U13_LEGAL_PATHS):
        name, branch = key.rsplit("-j", 1)
        source = _Source(*_INPUTS[name], int(branch))
        declared = tuple(row for row in U13_LEGAL_PATHS if row[0] == key)
        paths = _legal_paths(source)
        assert tuple(row[2] for row in declared) == paths
        context = BranchOracleContext(Instance(*_INPUTS[name]))
        for (_key, index, path, root, terminal, counts), expected_path in zip(
            declared, paths, strict=True,
        ):
            assert path == expected_path and path[-1] == (root, terminal)
            rows = _rows_for_path(source, path)
            with monkeypatch.context() as patch:
                _exercise(patch, context, source, rows, counts,
                          injected=tuple(_ZERO for _ in path))
            assert index >= 0
    # Choice freedom is not identical-trajectory or identical-iteration-count freedom.
    choice = tuple(row for row in U13_LEGAL_PATHS if row[0] == "CHOICE-j3")
    assert tuple(row[5][0] for row in choice) == (3, 4, 4)


def test_all_four_diagnostic_streams_sum_six_max_one_without_control_effect(monkeypatch):
    outputs = {}
    for stream, root, terminal, counts, aggregate, max_flows in U13_DIAGNOSTIC_TOTALS:
        entries = tuple(row for row in U13_DIAGNOSTIC_ROWS if row[0] == stream)
        key = entries[0][1]
        name, branch = key.rsplit("-j", 1)
        source = _Source(*_INPUTS[name], int(branch))
        rows = _TRACES[key]
        assert tuple((row[3], row[4]) for row in entries) == tuple((r[0], r[1]) for r in rows)
        injected = tuple(BranchOracleStats(*row[5]) for row in entries)
        with monkeypatch.context() as patch:
            packet, calls, _records = _exercise(
                patch, BranchOracleContext(Instance(*_INPUTS[name])), source,
                rows, counts, injected=injected,
            )
        assert _statistics(packet[1].oracle_stats) == aggregate
        assert packet[1].oracle_stats.max_flow_calls == max_flows
        outputs[stream] = packet[0], calls
        assert packet[0] is None if root is None else (
            packet[0].root == root and packet[0].shore == terminal
        )
    assert outputs["nonzero"] == outputs["zero"]


def _fault_case(monkeypatch, row):
    identifier, phase, expression, exception, _violation = row
    assert exception == "RuntimeError"
    names = _vocabulary()
    source = _Source(*_INPUTS["DOUBLE"], 0)
    context = BranchOracleContext(Instance(*_INPUTS["DOUBLE"]))
    expected = _TRACES["DOUBLE-j0"]
    at = {"seed": 0, "K": 1, "terminal": 2}[phase]
    calls = []
    comparison_calls = []
    replacement = None if identifier in ("F17", "F18") else _expression(expression, names)

    def query(given_context, j, parameter):
        k = len(calls)
        assert given_context is context and j == 0 and k <= at
        assert parameter == expected[k][0]
        calls.append(parameter)
        if k == at and identifier not in ("F17", "F18"):
            return replacement
        item = expected[k]
        return BranchOracleResult(item[1], *item[2], item[3]), _ZERO

    def failed_comparison(left, right):
        if len(calls) < 2:
            return rational_module.compare_pairs(left, right)
        comparison_calls.append((left, right))
        assert left == (2, 2) and right == (4, 2)
        return 0 if identifier == "F17" else 1

    with monkeypatch.context() as patch:
        _patch_dependency(patch, "exact_branch_min", query)
        if identifier in ("F17", "F18"):
            _patch_dependency(patch, "compare_pairs", failed_comparison)
        with pytest.raises(RuntimeError) as caught:
            _BRANCH.solve_branch_standard(context, source.branch)
        assert type(caught.value) is RuntimeError, identifier
    assert len(calls) == at + 1
    if identifier in ("F17", "F18"):
        assert comparison_calls == [((2, 2), (4, 2))]


def test_all_seed_response_shape_type_universe_and_binding_faults(monkeypatch):
    rows = tuple(row for row in U13_INTERNAL_FAILURES if row[1] == "seed")
    assert len(rows) == 11
    for row in rows:
        _fault_case(monkeypatch, row)


def test_later_none_nonnegative_k_positive_loop_and_terminal_binding_faults(monkeypatch):
    rows = tuple(row for row in U13_INTERNAL_FAILURES if row[0] in (
        "F12", "F13", "F14", "F15", "F16",
    ))
    assert len(rows) == 5
    for row in rows:
        _fault_case(monkeypatch, row)


def test_comparator_faults_exercise_explicit_strict_progress_guard(monkeypatch):
    for row in U13_INTERNAL_FAILURES[-2:]:
        assert row[0] in ("F17", "F18")
        _fault_case(monkeypatch, row)


def test_all_nine_dependency_exception_instances_propagate(monkeypatch):
    assert len(U13_EXCEPTIONS) == 9
    for identifier, dependency, _boundary in U13_EXCEPTIONS:
        context = BranchOracleContext(Instance(*_INPUTS["DOUBLE"]))
        sentinel = _Touched(identifier)
        query_state = [0]
        invocation = []
        boundary = {"X01": 0, "X02": 1, "X03": 2, "X04": 1, "X05": 1,
                    "X06": 1, "X07": 2, "X08": 2, "X09": 0}[identifier]
        original = _DEPENDENCIES[dependency]

        def observe_query(*args, _state=query_state, **kwargs):
            result = oracle_module.exact_branch_min(*args, **kwargs)
            _state[0] += 1
            return result

        def throwing(*args, _calls=invocation, _boundary=boundary, _state=query_state,
                     _sentinel=sentinel, _original=original, _dependency=dependency, **kwargs):
            _calls.append(_state[0])
            if _state[0] == _boundary:
                raise _sentinel
            result = _original(*args, **kwargs)
            if _dependency == "exact_branch_min":
                _state[0] += 1
            return result

        with monkeypatch.context() as patch:
            if dependency not in ("exact_branch_min", "validate_pair"):
                _patch_dependency(patch, "exact_branch_min", observe_query)
            _patch_dependency(patch, dependency, throwing)
            with pytest.raises(_Touched) as caught:
                if identifier == "X09":
                    _BRANCH.BranchResult((2, 2), 1)
                else:
                    _BRANCH.solve_branch_standard(context, 0)
            assert caught.value is sentinel
        assert invocation and invocation[-1] == boundary
        assert query_state[0] == boundary


def test_each_successful_reply_is_bound_to_the_submitted_raw_parameter(monkeypatch):
    source = _Source(*_INPUTS["LOW0"], 0)
    context = BranchOracleContext(Instance(*_INPUTS["LOW0"]))
    rows = _TRACES["LOW0-j0"]
    scalar_calls = []
    original = rational_module.residual_numerator

    def binding(parameter, c, h):
        scalar_calls.append((parameter, c, h))
        return original(parameter, c, h)

    with monkeypatch.context() as patch:
        _patch_dependency(patch, "residual_numerator", binding)
        _exercise(patch, context, source, rows, _SOLVES["LOW0-j0"][2],
                  injected=tuple(_ZERO for _ in rows))
    assert list(dict.fromkeys(scalar_calls)) == [(row[0], *row[2]) for row in rows]


def test_context_preparation_is_not_repeated_and_seed_is_not_bypassed(monkeypatch):
    names = ("Q1", "LOW0")
    contexts = tuple(BranchOracleContext(Instance(*_INPUTS[name])) for name in names)
    original_access = BranchOracleContext.__getattribute__

    def deny_families(self, name):
        if name == "families":
            raise _Touched("Standard wrapper inspected the prepared family list")
        return original_access(self, name)

    def forbidden(*_args, **_kwargs):
        raise _Touched("Standard wrapper repeated preparation or feasibility inspection")

    for name, context in zip(names, contexts, strict=True):
        source = _Source(*_INPUTS[name], 0)
        rows = _TRACES[f"{name}-j0"]
        calls = []

        def query(given_context, branch, parameter,
                  _calls=calls, _context=context, _rows=rows):
            k = len(_calls)
            assert given_context is _context and branch == 0 and k < len(_rows)
            assert parameter == _rows[k][0]
            _calls.append(parameter)
            row = _rows[k]
            reply = None if row[1] is None else BranchOracleResult(row[1], *row[2], row[3])
            return reply, _ZERO

        with monkeypatch.context() as patch:
            patch.setattr(oracle_module, "enumerate_atomic_families", forbidden)
            patch.setattr(BranchOracleContext, "__init__", forbidden)
            patch.setattr(BranchOracleContext, "__getattribute__", deny_families)
            _patch_dependency(patch, "exact_branch_min", query)
            packet = _BRANCH.solve_branch_standard(context, 0)
        assert calls == [row[0] for row in rows]
        _assert_result(packet, source, rows, [_ZERO] * len(rows), _SOLVES[f"{name}-j0"][2])


def test_six_registered_reuse_steps_and_interleaved_direct_queries(monkeypatch):
    context = BranchOracleContext(Instance(*_INPUTS["RICH"]))
    before = _snapshot(context)
    isolated = {}
    for index, operation, _reference_name in U13_REUSE:
        if index == 1:
            assert operation == "direct RICH branch 1 query at (0,1)"
            reply, _stats = oracle_module.exact_branch_min(context, 1, (0, 1))
            row = _TRACES["RICH-j1"][0]
            assert (reply.shore, (reply.c, reply.h), reply.residual) == row[1:4]
        else:
            branch = int(operation.rsplit(" ", 1)[1])
            key = f"RICH-j{branch}"
            with monkeypatch.context() as patch:
                packet, calls, _records = _exercise(
                    patch, context, _Source(*_INPUTS["RICH"], branch), _TRACES[key],
                    _SOLVES[key][2], _SOLVES[key][3],
                )
            if branch in isolated:
                assert (packet, calls) == isolated[branch]
            isolated[branch] = packet, calls
        assert _snapshot(context) == before


def test_registered_labels_change_neither_raw_results_traces_nor_diagnostics(monkeypatch):
    for name, labels in U13_LABELS:
        plain = BranchOracleContext(Instance(*_INPUTS[name]))
        labelled = BranchOracleContext(Instance(*_INPUTS[name], labels=labels))
        for j in range(4):
            key = f"{name}-j{j}"
            source = _Source(*_INPUTS[name], j)
            outputs = []
            for context in (plain, labelled):
                with monkeypatch.context() as patch:
                    outputs.append(_exercise(patch, context, source, _TRACES[key],
                                             _SOLVES[key][2], _SOLVES[key][3]))
            assert outputs[0] == outputs[1]


def test_keyword_calls_preserve_the_exact_positional_interface():
    root = (-4, 4)
    assert _BRANCH.BranchResult(root=root, shore=1) == _BRANCH.BranchResult(root, 1)
    assert _BRANCH.StandardBranchStats(
        oracle_calls=9, outer_iterations=0, newton_updates=99, oracle_stats=_ZERO,
    ) == _BRANCH.StandardBranchStats(9, 0, 99, _ZERO)
    context = BranchOracleContext(Instance(*_INPUTS["DOUBLE"]))
    assert _BRANCH.solve_branch_standard(context=context, branch=0) == \
        _BRANCH.solve_branch_standard(context, 0)


def _census():
    totals = Counter()
    by_branch = [Counter() for _ in range(4)]
    default, any_choice = hashlib.sha256(), hashlib.sha256()
    carriers = Counter()
    for serial, n, edges, f in _core():
        totals["instances"] += 1
        totals[f"n{n}_instances"] += 1
        for j in range(4):
            source = _Source(n, edges, f, j)
            rows, root, u, counts, structural = _reference(source)
            _assert_plan(source, rows)
            paths = _legal_paths(source)
            local = Counter({
                "solves": 1, "oracle_calls": counts[0], "outer_iterations": counts[1],
                "newton_updates": counts[2], "family_examinations": counts[0] * structural[0],
                "feasible_family_calls": counts[0] * structural[1],
                "specified_ordinary_calls": counts[0] * structural[3],
                "domain_memberships": len(source.members), "all_legal_paths": len(paths),
            })
            if root is None:
                local["infeasible_solves"] += 1
                local["zero_descriptor_infeasible" if structural[0] == 0
                      else "all_empty_infeasible"] += 1
            else:
                local["feasible_solves"] += 1
                local["positive_roots" if root[0] > 0 else "negative_roots"
                      if root[0] < 0 else "zero_roots"] += 1
                local[f"updates_{counts[2]}"] += 1
                if u == (1 << n) - 1:
                    local["full_shore_returns"] += 1
                if root != rows[-1][2]:
                    local["terminal_pair_distinctions"] += 1
            if len({len(path) for path in paths}) > 1:
                local["variable_path_length_solves"] += 1
            totals.update(local)
            by_branch[j].update(local)
            default.update(_wire((serial, n, edges, f, j, source.members, source.optimum,
                                  source.optimizers, rows, root, u, counts, structural)))
            any_choice.update(_wire((serial, j, paths)))
            residual, wyz = _carriers(source, rows)
            carriers.update(residual_checks=residual, wyz_checks=wyz)
    return totals, by_branch, (default.hexdigest(), any_choice.hexdigest()), carriers


def test_independent_core_census_and_both_committed_stream_fingerprints():
    totals, by_branch, fingerprints, _carriers_total = _census()
    assert dict(totals) == dict(U13_CORPUS_COUNTS)
    assert tuple(dict(row) for row in by_branch) == tuple(row[1] for row in U13_CORPUS_BY_BRANCH)
    assert fingerprints == tuple(row[2] for row in U13_CORPUS_FINGERPRINTS)


def test_standard(monkeypatch):
    """1,316 real solves versus plans fixed by original-domain enumeration."""
    totals = Counter()
    for _serial, n, edges, f in _core():
        # All four plans are fixed before invoking the subject for this instance.
        sources = tuple(_Source(n, edges, f, j) for j in range(4))
        plans = tuple(_reference(source) for source in sources)
        context = BranchOracleContext(Instance(n, edges, f))
        for source, (rows, _root, _u, counts, structural) in zip(sources, plans, strict=True):
            with monkeypatch.context() as patch:
                packet, _calls, records = _exercise(
                    patch, context, source, rows, counts, structural,
                )
            stats = packet[1]
            totals.update(solves=1, oracle_calls=stats.oracle_calls,
                          outer_iterations=stats.outer_iterations,
                          newton_updates=stats.newton_updates,
                          ordinary_min_cut_calls=sum(x.ordinary_min_cut_calls for x in records))
    assert dict(totals) == {
        "solves": 1316, "oracle_calls": 3635, "outer_iterations": 2319,
        "newton_updates": 1182, "ordinary_min_cut_calls": 42302,
    }


def test_all_5374_core_legal_paths_are_valid_wrapper_runs(monkeypatch):
    count = variable = 0
    for _serial, n, edges, f in _core():
        context = BranchOracleContext(Instance(n, edges, f))
        for j in range(4):
            source = _Source(n, edges, f, j)
            paths = _legal_paths(source)
            if len({len(path) for path in paths}) > 1:
                variable += 1
            for path in paths:
                rows = _rows_for_path(source, path)
                t = len(rows)
                counts = (t, t - 1, t - 2) if source.members else (1, 0, 0)
                with monkeypatch.context() as patch:
                    _exercise(patch, context, source, rows, counts,
                              injected=tuple(_ZERO for _ in rows))
                count += 1
    assert (count, variable) == (5374, 54)


def _large_reference():
    totals = Counter()
    stream = hashlib.sha256()
    plans = []
    for family, k, four_counts, peak_bits, block_hash in U13_LARGE_SWEEP:
        n, edges, f = _large(family, k)
        sources = tuple(_Source(n, edges, f, j) for j in range(4))
        block = []
        peak = 0
        for j, source in enumerate(sources):
            rows, root, u, counts, structural = _reference(source)
            assert counts == four_counts[j]
            _assert_plan(source, rows)
            peak = max(peak, *(abs(x).bit_length() for row in rows for x in row[0]))
            block.append((family, k, j, rows, root, u, counts, structural))
            totals.update(solves=1, oracle_calls=counts[0])
            totals["infeasible_solves" if root is None else "feasible_solves"] += 1
            plans.append((family, k, source, rows, counts, structural))
        assert peak == peak_bits
        encoded = b"".join(_wire(row) for row in block)
        assert hashlib.sha256(encoded).hexdigest() == block_hash
        stream.update(encoded)
    return totals, stream.hexdigest(), plans


def test_symbolic_large_families_and_all_112_actual_branch_solves(monkeypatch):
    totals, stream, plans = _large_reference()
    assert dict(totals) == dict(U13_LARGE_COUNTS)
    assert stream == "739a048182fc518a2125f27416ba16d05aa6535e9183dd9dc19de5ea9f853e3c"
    focus = {row[0]: row for row in U13_LARGE_SYMBOLS}
    for family, k, source, rows, counts, structural in plans:
        symbol = focus[family]
        if source.branch == symbol[5]:
            q = (1 << k) + (family == "Z")
            names = {"q": q}
            assert rows[-1][0] == _expression(symbol[6], names)
            assert rows[-1][1] == symbol[7]
            assert tuple(row[0] for row in rows) == _expression(symbol[8], names)
        context = BranchOracleContext(Instance(source.n, source.edges, source.f))
        with monkeypatch.context() as patch:
            _exercise(patch, context, source, rows, counts, structural)


def test_literal_reset_carriers_and_integer_wyz_change_of_variables():
    _totals, _branches, _fingerprints, carrier_counts = _census()
    for name, n, edges, f, _d, _q in U13_INPUTS:
        for j in range(4):
            residual, wyz = _carriers(_Source(n, edges, f, j), _TRACES[f"{name}-j{j}"])
            carrier_counts.update(residual_checks=residual, wyz_checks=wyz)
    _large_counts, _stream, plans = _large_reference()
    for _family, _k, source, rows, _counts, _structural in plans:
        residual, wyz = _carriers(source, rows)
        carrier_counts.update(residual_checks=residual, wyz_checks=wyz)
    assert dict(carrier_counts) == dict(U13_CARRIER_COUNTS)


def test_production_source_exact_imports_arithmetic_and_no_graph_rescan():
    text = Path(_BRANCH.__file__).read_text(encoding="utf-8")
    assert not _source_violations(text)
    # Static checks are finite controls. They do not prove O(1) retained state or WYZ.
    # The later independent implementation audit inspects all actual call structures.


def test_source_guard_negative_controls_reject_prohibited_constructs():
    snippets = (
        "import math\n", "from .flow import FlowNetwork\n", "from .rational import pair_reflect\n",
        "def f():\n return 1.0\n", "def f(a,b):\n return a/b\n",
        "def f(a,b):\n return a//b\n", "def f(a,b):\n return a%b\n",
        "def f(a):\n return set(a)\n", "def f(a):\n return {x for x in a}\n",
        "def f(a):\n return float(a)\n", "def f(a):\n return int(a)\n",
        "def f(a):\n return getattr(a, 'root')\n", "def f():\n return open('x')\n",
        "def f(c):\n return c.families\n", "def f(c):\n return c.instance.Q\n",
        "def f(n):\n for i in range(1 << n):\n  pass\n",
        "def f():\n return g()\ndef g():\n return f()\n",
        "class A:\n def f(self):\n  return self.f()\n",
        "from .oracle import exact_branch_min\ndef f():\n while i < 1000:\n"
        "  exact_branch_min(c,j,p)\n",
        "from .oracle import exact_branch_min\ndef f():\n for i in range(7):\n"
        "  exact_branch_min(c,j,p)\n",
    )
    for snippet in snippets:
        assert _source_violations(snippet), snippet
    assert not _source_violations(
        '"""float Fraction division in prose is not executable use."""\n'
        "from __future__ import annotations\nfrom .rational import compare_pairs as cp\n"
        "def f(a,b):\n return cp(a,b)\n"
    )


def test_fresh_process_imports_resolve_to_only_permitted_project_layers():
    root = Path(__file__).resolve().parents[1]
    expected = root / "exactfrac/branch.py"
    script = r'''
import importlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
before = set(sys.modules)
module = importlib.import_module("exactfrac.branch")
allowed = {
    "exactfrac", "exactfrac.branch", "exactfrac.instance", "exactfrac.families",
    "exactfrac.flow", "exactfrac.shore", "exactfrac.witness", "exactfrac.rational",
    "exactfrac.sign_routing", "exactfrac.parity_cut", "exactfrac.oracle",
}
origins = {}
for name in set(sys.modules) - before:
    if name.startswith(("exactfrac", "tests")):
        assert name in allowed, name
        origin = pathlib.Path(sys.modules[name].__file__).resolve()
        wanted = root / ("exactfrac/__init__.py" if name == "exactfrac"
                         else name.replace(".", "/") + ".py")
        assert origin == wanted, (name, origin)
        origins[name] = str(origin.relative_to(root))
assert pathlib.Path(module.__file__).resolve() == root / "exactfrac/branch.py"
assert tuple(module.__all__) == ("BranchResult", "StandardBranchStats", "solve_branch_standard")
print(json.dumps(origins, sort_keys=True))
'''
    result = subprocess.run(
        [sys.executable, "-I", "-B", "-c", script, str(root)],
        cwd=root, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["exactfrac.branch"] == "exactfrac/branch.py"
    assert Path(_BRANCH.__file__).resolve() == expected
