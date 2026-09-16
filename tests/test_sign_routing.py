"""Unit 10 tests-first obligations SR1--SR16; ORACLE-046--055 are the authority.

Literal records below are transcribed from the committed human-readable tables.
This file never reads private fixture JSON and never calls a flow/min-cut backend.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import json
import os
import subprocess
import sys
from collections.abc import Callable, Iterator
from dataclasses import FrozenInstanceError, fields, is_dataclass
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import get_type_hints

import pytest

from exactfrac.instance import Instance
from exactfrac.rational import validate_pair as closed_validate_pair
from exactfrac.witness import ExactValue

BruteInstance = importlib.import_module("exactfrac_verify.brute").BruteInstance
sign_routing = importlib.import_module("exactfrac.sign_routing")
Coeff = sign_routing.SignRoutingCoefficients
Network = sign_routing.SignRoutedNetwork

EXPECTED_EXPORTS = (
    "SignRoutedNetwork",
    "SignRoutingCoefficients",
    "branch_coefficients",
    "build_sign_routed_network",
    "recover_objective",
)
PARAMETERS = ((-3, 1), (-2, 1), (-1, 2), (-2, 4), (0, 1), (0, 3), (1, 1), (2, 1), (3, 2), (6, 4))

# ORACLE-046.
INSTANCES = {'EQUALITY': (2, ((0, 1, 3),), (3, 3)),
 'MIXED': (4,
           ((0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 4), (1, 3, 2), (2, 3, 5)),
           (2, 3, 4, 5)),
 'RICH': (5, ((0, 2, 2), (1, 2, 2), (2, 4, 1), (3, 4, 1)), (1, 1, 1, 1, 2)),
 'TRIANGLE': (3, ((0, 1, 1), (0, 2, 1), (1, 2, 1)), (1, 1, 1))}

# ORACLE-046.
COEFFICIENT_SHAPES = ((0, (), -7), (0, (0, 0), 5), (2, (3, -4, 0, 5), -7))

# ORACLE-046.
NETWORK_SHAPES = ((1, (), 7, -2, (3, 1, 2)),
 (1, ((0, 2, 5), (0, 2, 2), (2, 0, 1), (1, 0, 0)), 11, -4, (3, 1, 2)))

# ORACLE-047: (instance, raw parameter, branch, a, gamma, constant, C_minus).
ANCHOR_ROWS = (
    ('RICH', (-3, 1), 0, 1, (4, 4, 13, 1, 2), 2, 0),
    ('RICH', (-3, 1), 1, 1, (4, 4, 13, 1, 2), -2, 0),
    ('RICH', (-3, 1), 2, 1, (1, 1, -2, 2, 4), -3, 2),
    ('RICH', (-3, 1), 3, 1, (1, 1, -2, 2, 4), -2, 2),
    ('RICH', (-2, 1), 0, 1, (3, 3, 9, 1, 2), 1, 0),
    ('RICH', (-2, 1), 1, 1, (3, 3, 9, 1, 2), -2, 0),
    ('RICH', (-2, 1), 2, 1, (0, 0, -3, 1, 2), -2, 3),
    ('RICH', (-2, 1), 3, 1, (0, 0, -3, 1, 2), -2, 3),
    ('RICH', (-1, 2), 0, 2, (3, 3, 6, 2, 4), -1, 0),
    ('RICH', (-1, 2), 1, 2, (3, 3, 6, 2, 4), -4, 0),
    ('RICH', (-1, 2), 2, 2, (-3, -3, -9, -1, -2), -1, 18),
    ('RICH', (-1, 2), 3, 2, (-3, -3, -9, -1, -2), -4, 18),
    ('RICH', (-2, 4), 0, 4, (6, 6, 12, 4, 8), -2, 0),
    ('RICH', (-2, 4), 1, 4, (6, 6, 12, 4, 8), -8, 0),
    ('RICH', (-2, 4), 2, 4, (-6, -6, -18, -2, -4), -2, 36),
    ('RICH', (-2, 4), 3, 4, (-6, -6, -18, -2, -4), -8, 36),
    ('RICH', (0, 1), 0, 1, (1, 1, 1, 1, 2), -1, 0),
    ('RICH', (0, 1), 1, 1, (1, 1, 1, 1, 2), -2, 0),
    ('RICH', (0, 1), 2, 1, (-2, -2, -5, -1, -2), 0, 12),
    ('RICH', (0, 1), 3, 1, (-2, -2, -5, -1, -2), -2, 12),
    ('RICH', (0, 3), 0, 3, (3, 3, 3, 3, 6), -3, 0),
    ('RICH', (0, 3), 1, 3, (3, 3, 3, 3, 6), -6, 0),
    ('RICH', (0, 3), 2, 3, (-6, -6, -15, -3, -6), 0, 36),
    ('RICH', (0, 3), 3, 3, (-6, -6, -15, -3, -6), -6, 36),
    ('RICH', (1, 1), 0, 1, (0, 0, -3, 1, 2), -2, 3),
    ('RICH', (1, 1), 1, 1, (0, 0, -3, 1, 2), -2, 3),
    ('RICH', (1, 1), 2, 1, (-3, -3, -6, -2, -4), 1, 18),
    ('RICH', (1, 1), 3, 1, (-3, -3, -6, -2, -4), -2, 18),
    ('RICH', (2, 1), 0, 1, (-1, -1, -7, 1, 2), -3, 9),
    ('RICH', (2, 1), 1, 1, (-1, -1, -7, 1, 2), -2, 9),
    ('RICH', (2, 1), 2, 1, (-4, -4, -7, -3, -6), 2, 24),
    ('RICH', (2, 1), 3, 1, (-4, -4, -7, -3, -6), -2, 24),
    ('RICH', (3, 2), 0, 2, (-1, -1, -10, 2, 4), -5, 12),
    ('RICH', (3, 2), 1, 2, (-1, -1, -10, 2, 4), -4, 12),
    ('RICH', (3, 2), 2, 2, (-7, -7, -13, -5, -10), 3, 42),
    ('RICH', (3, 2), 3, 2, (-7, -7, -13, -5, -10), -4, 42),
    ('RICH', (6, 4), 0, 4, (-2, -2, -20, 4, 8), -10, 24),
    ('RICH', (6, 4), 1, 4, (-2, -2, -20, 4, 8), -8, 24),
    ('RICH', (6, 4), 2, 4, (-14, -14, -26, -10, -20), 6, 84),
    ('RICH', (6, 4), 3, 4, (-14, -14, -26, -10, -20), -8, 84),
    ('MIXED', (-3, 1), 0, 1, (14, 18, 28, 14), 2, 0),
    ('MIXED', (-3, 1), 1, 1, (14, 18, 28, 14), -2, 0),
    ('MIXED', (-3, 1), 2, 1, (0, 1, 0, 7), -3, 0),
    ('MIXED', (-3, 1), 3, 1, (0, 1, 0, 7), -2, 0),
    ('MIXED', (-2, 1), 0, 1, (10, 13, 20, 11), 1, 0),
    ('MIXED', (-2, 1), 1, 1, (10, 13, 20, 11), -2, 0),
    ('MIXED', (-2, 1), 2, 1, (-2, -2, -4, 2), -2, 8),
    ('MIXED', (-2, 1), 3, 1, (-2, -2, -4, 2), -2, 8),
    ('MIXED', (-1, 2), 0, 2, (8, 11, 16, 13), -1, 0),
    ('MIXED', (-1, 2), 1, 2, (8, 11, 16, 13), -4, 0),
    ('MIXED', (-1, 2), 2, 2, (-10, -13, -20, -11), -1, 54),
    ('MIXED', (-1, 2), 3, 2, (-10, -13, -20, -11), -4, 54),
    ('MIXED', (-2, 4), 0, 4, (16, 22, 32, 26), -2, 0),
    ('MIXED', (-2, 4), 1, 4, (16, 22, 32, 26), -8, 0),
    ('MIXED', (-2, 4), 2, 4, (-20, -26, -40, -22), -2, 108),
    ('MIXED', (-2, 4), 3, 4, (-20, -26, -40, -22), -8, 108),
    ('MIXED', (0, 1), 0, 1, (2, 3, 4, 5), -1, 0),
    ('MIXED', (0, 1), 1, 1, (2, 3, 4, 5), -2, 0),
    ('MIXED', (0, 1), 2, 1, (-6, -8, -12, -8), 0, 34),
    ('MIXED', (0, 1), 3, 1, (-6, -8, -12, -8), -2, 34),
    ('MIXED', (0, 3), 0, 3, (6, 9, 12, 15), -3, 0),
    ('MIXED', (0, 3), 1, 3, (6, 9, 12, 15), -6, 0),
    ('MIXED', (0, 3), 2, 3, (-18, -24, -36, -24), 0, 102),
    ('MIXED', (0, 3), 3, 3, (-18, -24, -36, -24), -6, 102),
    ('MIXED', (1, 1), 0, 1, (-2, -2, -4, 2), -2, 8),
    ('MIXED', (1, 1), 1, 1, (-2, -2, -4, 2), -2, 8),
    ('MIXED', (1, 1), 2, 1, (-8, -11, -16, -13), 1, 48),
    ('MIXED', (1, 1), 3, 1, (-8, -11, -16, -13), -2, 48),
    ('MIXED', (2, 1), 0, 1, (-6, -7, -12, -1), -3, 26),
    ('MIXED', (2, 1), 1, 1, (-6, -7, -12, -1), -2, 26),
    ('MIXED', (2, 1), 2, 1, (-10, -14, -20, -18), 2, 62),
    ('MIXED', (2, 1), 3, 1, (-10, -14, -20, -18), -2, 62),
    ('MIXED', (3, 2), 0, 2, (-8, -9, -16, 1), -5, 33),
    ('MIXED', (3, 2), 1, 2, (-8, -9, -16, 1), -4, 33),
    ('MIXED', (3, 2), 2, 2, (-18, -25, -36, -31), 3, 110),
    ('MIXED', (3, 2), 3, 2, (-18, -25, -36, -31), -4, 110),
    ('MIXED', (6, 4), 0, 4, (-16, -18, -32, 2), -10, 66),
    ('MIXED', (6, 4), 1, 4, (-16, -18, -32, 2), -8, 66),
    ('MIXED', (6, 4), 2, 4, (-36, -50, -72, -62), 6, 220),
    ('MIXED', (6, 4), 3, 4, (-36, -50, -72, -62), -8, 220),
    ('EQUALITY', (-3, 1), 0, 1, (3, 3), 2, 0),
    ('EQUALITY', (-3, 1), 1, 1, (3, 3), -2, 0),
    ('EQUALITY', (-3, 1), 2, 1, (6, 6), -3, 0),
    ('EQUALITY', (-3, 1), 3, 1, (6, 6), -2, 0),
    ('EQUALITY', (-2, 1), 0, 1, (3, 3), 1, 0),
    ('EQUALITY', (-2, 1), 1, 1, (3, 3), -2, 0),
    ('EQUALITY', (-2, 1), 2, 1, (3, 3), -2, 0),
    ('EQUALITY', (-2, 1), 3, 1, (3, 3), -2, 0),
    ('EQUALITY', (-1, 2), 0, 2, (6, 6), -1, 0),
    ('EQUALITY', (-1, 2), 1, 2, (6, 6), -4, 0),
    ('EQUALITY', (-1, 2), 2, 2, (-3, -3), -1, 6),
    ('EQUALITY', (-1, 2), 3, 2, (-3, -3), -4, 6),
    ('EQUALITY', (-2, 4), 0, 4, (12, 12), -2, 0),
    ('EQUALITY', (-2, 4), 1, 4, (12, 12), -8, 0),
    ('EQUALITY', (-2, 4), 2, 4, (-6, -6), -2, 12),
    ('EQUALITY', (-2, 4), 3, 4, (-6, -6), -8, 12),
    ('EQUALITY', (0, 1), 0, 1, (3, 3), -1, 0),
    ('EQUALITY', (0, 1), 1, 1, (3, 3), -2, 0),
    ('EQUALITY', (0, 1), 2, 1, (-3, -3), 0, 6),
    ('EQUALITY', (0, 1), 3, 1, (-3, -3), -2, 6),
    ('EQUALITY', (0, 3), 0, 3, (9, 9), -3, 0),
    ('EQUALITY', (0, 3), 1, 3, (9, 9), -6, 0),
    ('EQUALITY', (0, 3), 2, 3, (-9, -9), 0, 18),
    ('EQUALITY', (0, 3), 3, 3, (-9, -9), -6, 18),
    ('EQUALITY', (1, 1), 0, 1, (3, 3), -2, 0),
    ('EQUALITY', (1, 1), 1, 1, (3, 3), -2, 0),
    ('EQUALITY', (1, 1), 2, 1, (-6, -6), 1, 12),
    ('EQUALITY', (1, 1), 3, 1, (-6, -6), -2, 12),
    ('EQUALITY', (2, 1), 0, 1, (3, 3), -3, 0),
    ('EQUALITY', (2, 1), 1, 1, (3, 3), -2, 0),
    ('EQUALITY', (2, 1), 2, 1, (-9, -9), 2, 18),
    ('EQUALITY', (2, 1), 3, 1, (-9, -9), -2, 18),
    ('EQUALITY', (3, 2), 0, 2, (6, 6), -5, 0),
    ('EQUALITY', (3, 2), 1, 2, (6, 6), -4, 0),
    ('EQUALITY', (3, 2), 2, 2, (-15, -15), 3, 30),
    ('EQUALITY', (3, 2), 3, 2, (-15, -15), -4, 30),
    ('EQUALITY', (6, 4), 0, 4, (12, 12), -10, 0),
    ('EQUALITY', (6, 4), 1, 4, (12, 12), -8, 0),
    ('EQUALITY', (6, 4), 2, 4, (-30, -30), 6, 60),
    ('EQUALITY', (6, 4), 3, 4, (-30, -30), -8, 60),
)

# ORACLE-048: literal original arcs and (mask, Psi, cut, recovered) rows.
NETWORK_ROWS = (('N1',
  'EQUALITY',
  (2, (-4, 5), -3),
  4,
  ((0, 1, 6), (1, 0, 6), (2, 0, 4), (0, 2, 4), (1, 3, 5), (3, 1, 5)),
  ((0, 0, 4, -3), (1, 2, 6, -1), (2, 11, 15, 8), (3, 1, 5, -2))),
 ('N2',
  'EQUALITY',
  (0, (-4, 5), 7),
  4,
  ((0, 1, 0), (1, 0, 0), (2, 0, 4), (0, 2, 4), (1, 3, 5), (3, 1, 5)),
  ((0, 0, 4, 7), (1, -4, 0, 3), (2, 5, 9, 12), (3, 1, 5, 8))),
 ('N3',
  'EQUALITY',
  (2, (0, 0), -7),
  0,
  ((0, 1, 6), (1, 0, 6), (0, 3, 0), (3, 0, 0), (1, 3, 0), (3, 1, 0)),
  ((0, 0, 0, -7), (1, 6, 6, -1), (2, 6, 6, -1), (3, 0, 0, -7))),
 ('N4',
  'EQUALITY',
  (0, (0, 0), 5),
  0,
  ((0, 1, 0), (1, 0, 0), (0, 3, 0), (3, 0, 0), (1, 3, 0), (3, 1, 0)),
  ((0, 0, 0, 5), (1, 0, 0, 5), (2, 0, 0, 5), (3, 0, 0, 5))),
 ('N5',
  'MIXED',
  (2, (3, -4, 0, 5), -7),
  4,
  ((0, 1, 4),
   (1, 0, 4),
   (0, 2, 6),
   (2, 0, 6),
   (0, 3, 2),
   (3, 0, 2),
   (1, 2, 8),
   (2, 1, 8),
   (1, 3, 4),
   (3, 1, 4),
   (2, 3, 10),
   (3, 2, 10),
   (0, 5, 3),
   (5, 0, 3),
   (4, 1, 4),
   (1, 4, 4),
   (2, 5, 0),
   (5, 2, 0),
   (3, 5, 5),
   (5, 3, 5)),
  ((0, 0, 4, -7),
   (1, 15, 19, 8),
   (2, 12, 16, 5),
   (3, 19, 23, 12),
   (4, 24, 28, 17),
   (5, 27, 31, 20),
   (6, 20, 24, 13),
   (7, 15, 19, 8),
   (8, 21, 25, 14),
   (9, 32, 36, 25),
   (10, 25, 29, 18),
   (11, 28, 32, 21),
   (12, 25, 29, 18),
   (13, 24, 28, 17),
   (14, 13, 17, 6),
   (15, 4, 8, -3))),
 ('N6',
  'RICH',
  (1, (4, 4, 13, 1, 2), 2),
  0,
  ((0, 2, 2),
   (2, 0, 2),
   (1, 2, 2),
   (2, 1, 2),
   (2, 4, 1),
   (4, 2, 1),
   (3, 4, 1),
   (4, 3, 1),
   (0, 6, 4),
   (6, 0, 4),
   (1, 6, 4),
   (6, 1, 4),
   (2, 6, 13),
   (6, 2, 13),
   (3, 6, 1),
   (6, 3, 1),
   (4, 6, 2),
   (6, 4, 2)),
  ((0, 0, 0, 2),
   (1, 6, 6, 8),
   (2, 6, 6, 8),
   (3, 12, 12, 14),
   (4, 18, 18, 20),
   (5, 20, 20, 22),
   (6, 20, 20, 22),
   (7, 22, 22, 24),
   (8, 2, 2, 4),
   (9, 8, 8, 10),
   (10, 8, 8, 10),
   (11, 14, 14, 16),
   (12, 20, 20, 22),
   (13, 22, 22, 24),
   (14, 22, 22, 24),
   (15, 24, 24, 26),
   (16, 4, 4, 6),
   (17, 10, 10, 12),
   (18, 10, 10, 12),
   (19, 16, 16, 18),
   (20, 20, 20, 22),
   (21, 22, 22, 24),
   (22, 22, 22, 24),
   (23, 24, 24, 26),
   (24, 4, 4, 6),
   (25, 10, 10, 12),
   (26, 10, 10, 12),
   (27, 16, 16, 18),
   (28, 20, 20, 22),
   (29, 22, 22, 24),
   (30, 22, 22, 24),
   (31, 24, 24, 26))),
 ('N7',
  'RICH',
  (1, (0, 0, -3, 1, 2), -2),
  3,
  ((0, 2, 2),
   (2, 0, 2),
   (1, 2, 2),
   (2, 1, 2),
   (2, 4, 1),
   (4, 2, 1),
   (3, 4, 1),
   (4, 3, 1),
   (0, 6, 0),
   (6, 0, 0),
   (1, 6, 0),
   (6, 1, 0),
   (5, 2, 3),
   (2, 5, 3),
   (3, 6, 1),
   (6, 3, 1),
   (4, 6, 2),
   (6, 4, 2)),
  ((0, 0, 3, -2),
   (1, 2, 5, 0),
   (2, 2, 5, 0),
   (3, 4, 7, 2),
   (4, 2, 5, 0),
   (5, 0, 3, -2),
   (6, 0, 3, -2),
   (7, -2, 1, -4),
   (8, 2, 5, 0),
   (9, 4, 7, 2),
   (10, 4, 7, 2),
   (11, 6, 9, 4),
   (12, 4, 7, 2),
   (13, 2, 5, 0),
   (14, 2, 5, 0),
   (15, 0, 3, -2),
   (16, 4, 7, 2),
   (17, 6, 9, 4),
   (18, 6, 9, 4),
   (19, 8, 11, 6),
   (20, 4, 7, 2),
   (21, 2, 5, 0),
   (22, 2, 5, 0),
   (23, 0, 3, -2),
   (24, 4, 7, 2),
   (25, 6, 9, 4),
   (26, 6, 9, 4),
   (27, 8, 11, 6),
   (28, 4, 7, 2),
   (29, 2, 5, 0),
   (30, 2, 5, 0),
   (31, 0, 3, -2))),
 ('N8',
  'RICH',
  (1, (-2, -2, -5, -1, -2), 0),
  12,
  ((0, 2, 2),
   (2, 0, 2),
   (1, 2, 2),
   (2, 1, 2),
   (2, 4, 1),
   (4, 2, 1),
   (3, 4, 1),
   (4, 3, 1),
   (5, 0, 2),
   (0, 5, 2),
   (5, 1, 2),
   (1, 5, 2),
   (5, 2, 5),
   (2, 5, 5),
   (5, 3, 1),
   (3, 5, 1),
   (5, 4, 2),
   (4, 5, 2)),
  ((0, 0, 12, 0),
   (1, 0, 12, 0),
   (2, 0, 12, 0),
   (3, 0, 12, 0),
   (4, 0, 12, 0),
   (5, -4, 8, -4),
   (6, -4, 8, -4),
   (7, -8, 4, -8),
   (8, 0, 12, 0),
   (9, 0, 12, 0),
   (10, 0, 12, 0),
   (11, 0, 12, 0),
   (12, 0, 12, 0),
   (13, -4, 8, -4),
   (14, -4, 8, -4),
   (15, -8, 4, -8),
   (16, 0, 12, 0),
   (17, 0, 12, 0),
   (18, 0, 12, 0),
   (19, 0, 12, 0),
   (20, -2, 10, -2),
   (21, -6, 6, -6),
   (22, -6, 6, -6),
   (23, -10, 2, -10),
   (24, -2, 10, -2),
   (25, -2, 10, -2),
   (26, -2, 10, -2),
   (27, -2, 10, -2),
   (28, -4, 8, -4),
   (29, -8, 4, -8),
   (30, -8, 4, -8),
   (31, -12, 0, -12))))

# ORACLE-050: (cut_value, negative_shift, constant, result).
RECOVERY_ROWS = (
    (0, 7, -2, -9), (10, 7, -2, 1), (0, 0, 5, 5),
    (4, 4, -3, -3), (6, 4, -3, -1), (0, 0, 0, 0),
)


def _source_tree() -> ast.Module:
    return ast.parse(Path(sign_routing.__file__).read_text(encoding="utf-8"))


def _targets(node: ast.AST) -> set[str]:
    return {part.id for part in ast.walk(node) if isinstance(part, ast.Name)}


def _set_expression(node: ast.AST, names: set[str]) -> bool:
    if isinstance(node, (ast.Set, ast.SetComp)):
        return True
    if isinstance(node, ast.Name):
        return node.id in names
    if isinstance(node, ast.BinOp) and isinstance(
        node.op, (ast.BitOr, ast.BitAnd, ast.BitXor, ast.Sub)
    ):
        return _set_expression(node.left, names) or _set_expression(node.right, names)
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in ("set", "frozenset"):
            return True
        if isinstance(node.func, ast.Attribute) and node.func.attr in (
            "copy", "union", "intersection", "difference", "symmetric_difference",
        ):
            return _set_expression(node.func.value, names)
    return False


def _assigned_set_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    assignments = [node for node in ast.walk(tree) if isinstance(node, (ast.Assign, ast.AnnAssign))]
    changed = True
    while changed:
        before = len(names)
        for node in assignments:
            targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
            if node.value is not None and _set_expression(node.value, names):
                for target in targets:
                    names.update(_targets(target))
        changed = len(names) != before
    return names


def _iterators(tree: ast.AST) -> Iterator[ast.AST]:
    consumers = {"tuple", "list", "sum", "any", "all", "enumerate", "iter", "sorted"}
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            yield node.iter
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in consumers and node.args:
                yield node.args[0]
            elif node.func.id == "zip":
                yield from node.args
            elif node.func.id in ("map", "filter"):
                yield from node.args[1:]


def _structural_bound(node: ast.AST, names: set[str]) -> bool:
    if isinstance(node, ast.Constant):
        return type(node.value) is int
    if isinstance(node, ast.Name):
        return node.id in names
    if isinstance(node, ast.Attribute):
        return node.attr in ("n", "m", "vertex_count", "node_count")
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return node.func.id == "len" and len(node.args) == 1
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        return _structural_bound(node.operand, names)
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult)):
        return _structural_bound(node.left, names) and _structural_bound(node.right, names)
    return False


def _structural_names(tree: ast.AST) -> set[str]:
    names = {"n", "vertex_count", "node_count"}
    assignments = [node for node in ast.walk(tree) if isinstance(node, (ast.Assign, ast.AnnAssign))]
    changed = True
    while changed:
        before = len(names)
        for node in assignments:
            if node.value is not None and _structural_bound(node.value, names):
                targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
                for target in targets:
                    names.update(_targets(target))
        changed = len(names) != before
    return names


def _source_functions(tree: ast.Module) -> dict[str, ast.FunctionDef]:
    result = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            result[node.name] = node
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    result[f"{node.name}.{child.name}"] = child
    return result


def _call_graph(tree: ast.Module) -> tuple[dict, dict]:
    functions = _source_functions(tree)
    graph = {name: set() for name in functions}
    for name, function in functions.items():
        owner = name.rsplit(".", 1)[0] if "." in name else ""
        for node in ast.walk(function):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in functions:
                graph[name].add(node.func.id)
            elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                receiver = node.func.value.id
                called = f"{owner if receiver == 'self' else receiver}.{node.func.attr}"
                if called in functions:
                    graph[name].add(called)
    return functions, graph


def _assert_acyclic(graph: dict) -> None:
    done: set[str] = set()
    active: set[str] = set()

    def visit(name: str) -> None:
        assert name not in active, f"recursive source call cycle at {name}"
        if name in done:
            return
        active.add(name)
        for called in sorted(graph[name]):
            visit(called)
        active.remove(name)
        done.add(name)

    for name in sorted(graph):
        visit(name)


def _check_source(tree: ast.Module) -> None:
    allowed_from = {
        (1, "_telemetry"): {"_tap_int", "_tap_pair", "_tap_numerator", "_observe_ints",
                       "_observe_pair_values", "_record_prepared_sizes", "_branch_scope"},
        (0, "__future__"): {"annotations"},
        (0, "dataclasses"): {"dataclass"},
        (1, "instance"): {"Instance"},
        (1, "rational"): {"RawPair", "validate_pair"},
    }
    banned_calls = {
        "Decimal", "Fraction", "__import__", "bool", "compile", "complex", "divmod",
        "eval", "exec", "float", "gcd", "int", "isclose", "minimum_cut", "open", "round",
    }
    structural = _structural_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert all(alias.name == "dataclasses" for alias in node.names), ast.unparse(node)
        if isinstance(node, ast.ImportFrom):
            allowed = allowed_from.get((node.level, node.module), set())
            dataclass_import = node.level == 0 and node.module == "dataclasses"
            if not dataclass_import:
                names = {alias.name for alias in node.names}
                assert names <= allowed and allowed, ast.unparse(node)
        if isinstance(node, ast.Constant):
            assert type(node.value) not in (float, complex)
        if isinstance(node, ast.BinOp):
            assert not isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod))
        assert not isinstance(node, (ast.While, ast.AsyncFor, ast.AsyncFunctionDef))
        if isinstance(node, ast.Call):
            target = node.func.id if isinstance(node.func, ast.Name) else None
            if isinstance(node.func, ast.Attribute):
                target = node.func.attr
            assert target not in banned_calls
            assert target != "bit_length"
            if target == "range":
                assert node.args and all(_structural_bound(arg, structural) for arg in node.args)
        if isinstance(node, (ast.For, ast.comprehension)):
            for inner in ast.walk(node):
                assert not (isinstance(inner, ast.Attribute) and inner.attr == "d_q")
    set_names = _assigned_set_names(tree)
    for iterator in _iterators(tree):
        assert not _set_expression(iterator, set_names), ast.unparse(iterator)
    _, graph = _call_graph(tree)
    _assert_acyclic(graph)


def test_source_exactness_dependency_and_structural_loop_controls() -> None:
    _check_source(_source_tree())


def test_source_recovery_and_terminal_properties_have_no_transitive_loops() -> None:
    functions, graph = _call_graph(_source_tree())
    roots = (
        "recover_objective", "SignRoutedNetwork.node_count", "SignRoutedNetwork.source",
        "SignRoutedNetwork.sink",
    )
    for root in roots:
        assert root in functions
        pending = [root]
        visited: set[str] = set()
        while pending:
            name = pending.pop()
            if name in visited:
                continue
            visited.add(name)
            for node in ast.walk(functions[name]):
                assert not isinstance(node, (ast.For, ast.While, ast.comprehension))
            pending.extend(sorted(graph[name]))


def test_in_memory_prohibited_source_controls() -> None:
    bad_sources = (
        "x = 0.5",
        "x = 1 / 2",
        "x = 1 // 2",
        "x = 3 % 2",
        "from fractions import Fraction",
        "from .flow import minimum_cut",
        "x = int(value)",
        "x = float('inf')",
        "x = math.gcd(2, 4)",
        "while True:\n    pass",
        "for i in range(capacity):\n    pass",
        "for i in range(1 << n):\n    pass",
        "for i in range(n):\n    x = instance.d_q[i]",
        "for i in {1, 2}:\n    pass",
        "for i in {v for v in range(n)}:\n    pass",
        "seen = {1, 2}\nother = seen\nfor i in other:\n    pass",
        "seen = set()\nother = seen.copy()\nfor i in other:\n    pass",
        "seen = {1, 2}\nx = sum(seen)",
        "def first():\n    return second()\ndef second():\n    return first()",
    )
    for source in bad_sources:
        with pytest.raises(AssertionError):
            _check_source(ast.parse(source))
    # Permitted structural aliases and lookup-only sets prevent overbroad magnitude/name bans.
    _check_source(ast.parse("count = len(gamma)\nfor i in range(count):\n    pass"))
    _check_source(ast.parse("ok = branch in {0, 1, 2, 3}"))


def test_fresh_process_import_isolation_and_export_free_package_root() -> None:
    import exactfrac

    assert not any(name in vars(exactfrac) for name in EXPECTED_EXPORTS)
    root = Path(sign_routing.__file__).resolve().parents[1]
    script = """
import json
import pathlib
import sys
import exactfrac.sign_routing as module
project = {
    name: str(pathlib.Path(item.__file__).resolve())
    for name, item in sys.modules.copy().items()
    if name == 'exactfrac' or name.startswith('exactfrac.')
    or name == 'exactfrac_verify' or name.startswith('exactfrac_verify.')
}
print(json.dumps(project, sort_keys=True))
print(module.__file__)
"""
    env = dict(os.environ)
    env.pop("PYTHONHOME", None)
    env.update(PYTHONPATH=str(root), PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
    completed = subprocess.run(
        [sys.executable, "-c", script], cwd=root, env=env,
        check=True, capture_output=True, text=True,
    )
    lines = completed.stdout.splitlines()
    assert len(lines) == 2
    origins = json.loads(lines[0])
    assert tuple(sorted(origins)) in (
        ("exactfrac", "exactfrac.instance", "exactfrac.rational", "exactfrac.sign_routing"),
        ("exactfrac", "exactfrac._telemetry", "exactfrac.instance",
         "exactfrac.rational", "exactfrac.sign_routing"),
    )
    for name, path in origins.items():
        relative = name.replace(".", "/") + ("/__init__.py" if name == "exactfrac" else ".py")
        assert Path(path) == root / relative
    assert Path(lines[1]).resolve() == Path(sign_routing.__file__).resolve()


class IntSubclass(int):
    """Otherwise integer-like input that the exact-type boundary must reject."""


class TupleSubclass(tuple):
    """Otherwise tuple-like input that must not be accepted as an exact tuple."""


class Hostile:
    """A wrong-type object whose hooks must never be invoked by validation."""

    def _raise(self, *args: object, **kwargs: object) -> object:
        raise AssertionError("wrong-type object's hook was invoked")

    __int__ = __index__ = __float__ = __bool__ = _raise
    __iter__ = __len__ = __getitem__ = _raise
    __eq__ = __lt__ = __le__ = __gt__ = __ge__ = _raise
    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = _raise
    __neg__ = __abs__ = _raise


class _InstanceSubclass(Instance):
    pass


class _CoeffSubclass(Coeff):
    pass


class _NetworkSubclass(Network):
    pass


def _instance(name: str) -> Instance:
    return Instance(*INSTANCES[name])


def _exact_error(function: Callable[..., object], *args: object) -> None:
    with pytest.raises(ValueError) as caught:
        function(*args)
    assert type(caught.value) is ValueError


def _sums(records: tuple, mask: int) -> tuple[int, int, int]:
    """Independent source s,b,d from the original edge/f records, never Instance.d_q."""
    n, edges, capacities = records
    size = sum(capacities[v] for v in range(n) if (mask >> v) & 1)
    boundary = 0
    degree_sum = 0
    for u, v, multiplicity in edges:
        inside_u = (mask >> u) & 1
        inside_v = (mask >> v) & 1
        degree_sum += multiplicity * (inside_u + inside_v)
        if inside_u != inside_v:
            boundary += multiplicity
    return size, boundary, degree_sum


def _source_residual(records: tuple, branch: int, parameter: tuple[int, int], mask: int) -> int:
    size, boundary, degree_sum = _sums(records, mask)
    numerator, denominator = parameter
    source_pairs = (
        (size + boundary - 1, degree_sum + 1 - size),
        (size + boundary - 2, degree_sum - size),
        (boundary - degree_sum, size - 1),
        (boundary - degree_sum - 2, size),
    )
    cost, divisor = source_pairs[branch]
    return denominator * cost - numerator * divisor


def _coefficient_oracle(records: tuple, branch: int, parameter: tuple[int, int]) -> tuple:
    """Recover coefficients independently from empty/singleton residuals (ORACLE-049)."""
    constant = _source_residual(records, branch, parameter, 0)
    a_value = parameter[1]
    gamma = tuple(
        _source_residual(records, branch, parameter, 1 << vertex)
        - constant - a_value * _sums(records, 1 << vertex)[1]
        for vertex in range(records[0])
    )
    return a_value, gamma, constant


def _cut(arcs: tuple, source: int, mask: int) -> int:
    """Count directed original capacity crossings; no network construction or flow."""
    source_shore = mask | (1 << source)
    return sum(
        capacity
        for tail, head, capacity in arcs
        if ((source_shore >> tail) & 1) and not ((source_shore >> head) & 1)
    )


def _coefficient_fields(record: object) -> tuple:
    assert type(record) is Coeff
    assert type(record.a) is int
    assert type(record.gamma) is tuple
    assert all(type(entry) is int for entry in record.gamma)
    assert type(record.constant) is int
    return record.a, record.gamma, record.constant


def _network_fields(record: object) -> tuple:
    assert type(record) is Network
    assert type(record.vertex_count) is int
    assert type(record.arcs) is tuple
    assert type(record.negative_shift) is int
    assert type(record.constant) is int
    for arc in record.arcs:
        assert type(arc) is tuple and len(arc) == 3
        assert all(type(entry) is int for entry in arc)
    for name in ("node_count", "source", "sink"):
        assert type(getattr(record, name)) is int
    return record.vertex_count, record.arcs, record.negative_shift, record.constant


def _check_emission(records: tuple, raw_coefficients: tuple, network: object) -> None:
    """Check each arc position directly against the ruled edge/spoke record relation."""
    n, edges, _ = records
    a_value, gamma, constant = raw_coefficients
    _network_fields(network)
    assert (network.vertex_count, network.node_count, network.source, network.sink) == (
        n, n + 2, n, n + 1,
    )
    assert len(network.arcs) == 2 * (len(edges) + n)
    assert network.constant == constant
    assert network.negative_shift == sum(-value for value in gamma if value < 0)
    for index, (u, v, multiplicity) in enumerate(edges):
        assert network.arcs[2 * index] == (u, v, a_value * multiplicity)
        assert network.arcs[2 * index + 1] == (v, u, a_value * multiplicity)
    offset = 2 * len(edges)
    for vertex, value in enumerate(gamma):
        tail, head, capacity = (vertex, n + 1, value) if value >= 0 else (n, vertex, -value)
        assert network.arcs[offset + 2 * vertex] == (tail, head, capacity)
        assert network.arcs[offset + 2 * vertex + 1] == (head, tail, capacity)


def _active_records() -> Iterator[tuple]:
    """ORACLE-052 domain; bounded test enumeration, not production construction."""
    for n in (2, 3):
        pairs = tuple(combinations(range(n), 2))
        for multiplicities in product((0, 1, 2), repeat=len(pairs)):
            edges = tuple(
                (u, v, multiplicity)
                for (u, v), multiplicity in zip(pairs, multiplicities, strict=True)
                if multiplicity > 0
            )
            degrees = tuple(
                sum(q for u, v, q in edges if vertex in (u, v))
                for vertex in range(n)
            )
            if not all(degrees):
                continue
            for capacities in product(*(range(1, degree + 1) for degree in degrees)):
                yield n, edges, capacities


def _exercise_branch_shores(records: tuple, branch: int, parameter: tuple, coeff: object) -> int:
    """Compare each production result with an independent definition-side result."""
    raw = _coefficient_oracle(records, branch, parameter)
    assert _coefficient_fields(coeff) == raw
    value = Instance(*records)
    network = sign_routing.build_sign_routed_network(value, coeff)
    _check_emission(records, raw, network)
    n = records[0]
    count = 0
    for mask in range(1 << n):
        expected = _source_residual(records, branch, parameter, mask)
        boundary = _sums(records, mask)[1]
        actual_form = coeff.a * boundary + sum(
            coeff.gamma[v] for v in range(n) if (mask >> v) & 1
        ) + coeff.constant
        assert actual_form == expected, (records, branch, parameter, mask)
        actual_cut = _cut(network.arcs, n, mask)
        expected_shift = sum(-entry for entry in raw[1] if entry < 0)
        assert actual_cut == expected - raw[2] + expected_shift
        recovered = sign_routing.recover_objective(network, actual_cut)
        assert type(recovered) is int
        assert recovered == expected
        count += 1
    return count


def test_public_surface_signatures_and_exact_annotations() -> None:
    assert sign_routing.__all__ == EXPECTED_EXPORTS
    assert type(sign_routing.__all__) is tuple
    expected = {
        "SignRoutingCoefficients": ("a", "gamma", "constant"),
        "SignRoutedNetwork": ("vertex_count", "arcs", "negative_shift", "constant"),
        "branch_coefficients": ("instance", "branch", "parameter"),
        "build_sign_routed_network": ("instance", "coefficients"),
        "recover_objective": ("network", "cut_value"),
    }
    for name, names in expected.items():
        signature = inspect.signature(getattr(sign_routing, name))
        assert tuple(signature.parameters) == names
        for parameter in signature.parameters.values():
            assert parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
            assert parameter.default is inspect.Parameter.empty
    assert get_type_hints(Coeff) == {"a": int, "gamma": tuple[int, ...], "constant": int}
    assert get_type_hints(Network) == {
        "vertex_count": int, "arcs": tuple[tuple[int, int, int], ...],
        "negative_shift": int, "constant": int,
    }
    assert get_type_hints(sign_routing.branch_coefficients) == {
        "instance": Instance, "branch": int, "parameter": tuple[int, int], "return": Coeff,
    }
    assert get_type_hints(sign_routing.build_sign_routed_network) == {
        "instance": Instance, "coefficients": Coeff, "return": Network,
    }
    assert get_type_hints(sign_routing.recover_objective) == {
        "network": Network, "cut_value": int, "return": int,
    }


def test_coefficient_record_raw_shape_and_structural_identity() -> None:
    assert is_dataclass(Coeff)
    assert tuple(field.name for field in fields(Coeff)) == ("a", "gamma", "constant")
    assert Coeff.__slots__ == ("a", "gamma", "constant")
    assert Coeff.__dataclass_params__.frozen and not Coeff.__dataclass_params__.order
    for raw in COEFFICIENT_SHAPES:
        record = Coeff(*raw)
        assert _coefficient_fields(record) == raw
        equal = Coeff(a=raw[0], gamma=raw[1], constant=raw[2])
        assert record == equal and hash(record) == hash(equal)
        assert not hasattr(record, "__dict__")
        assert record != Coeff(raw[0], raw[1], raw[2] + 1)
    assert Coeff(1, (2, 4), 6) != Coeff(2, (4, 8), 12)
    with pytest.raises(TypeError):
        _ = Coeff(0, (), 0) < Coeff(0, (), 1)


def test_network_record_preserves_order_repetitions_zeros_and_empty_shape() -> None:
    assert is_dataclass(Network)
    names = ("vertex_count", "arcs", "negative_shift", "constant")
    assert tuple(field.name for field in fields(Network)) == names
    assert Network.__slots__ == names
    assert Network.__dataclass_params__.frozen and not Network.__dataclass_params__.order
    for name in ("node_count", "source", "sink"):
        assert isinstance(getattr(Network, name), property)
    for vertex_count, arcs, shift, constant, properties in NETWORK_SHAPES:
        record = Network(vertex_count, arcs, shift, constant)
        assert _network_fields(record) == (vertex_count, arcs, shift, constant)
        assert properties == (record.node_count, record.source, record.sink)
        equal = Network(vertex_count=vertex_count, arcs=arcs,
                        negative_shift=shift, constant=constant)
        assert record == equal and hash(record) == hash(equal)
        assert record != Network(vertex_count, arcs, shift, constant + 1)
        assert not hasattr(record, "__dict__")
    with pytest.raises(TypeError):
        _ = Network(1, (), 0, 0) < Network(1, (), 0, 1)


def test_record_immutability_no_ordering_or_extra_stored_fields() -> None:
    records = (Coeff(0, (), -7), Network(1, ((0, 2, 0),), 0, 5))
    for record in records:
        snapshot = tuple(getattr(record, field.name) for field in fields(record))
        for field in fields(record):
            with pytest.raises(FrozenInstanceError):
                setattr(record, field.name, None)
            with pytest.raises(FrozenInstanceError):
                delattr(record, field.name)
        with pytest.raises((AttributeError, TypeError)):
            record.extra = 1
        assert tuple(getattr(record, field.name) for field in fields(record)) == snapshot


def test_keyword_calls_and_wrong_arity_boundary() -> None:
    instance = _instance("RICH")
    expected = (1, (4, 4, 13, 1, 2), 2)
    coeff = sign_routing.branch_coefficients(instance=instance, branch=0, parameter=(-3, 1))
    assert _coefficient_fields(coeff) == expected
    network = sign_routing.build_sign_routed_network(instance=instance, coefficients=coeff)
    _check_emission(INSTANCES["RICH"], expected, network)
    assert sign_routing.recover_objective(network=network, cut_value=0) == 2
    for name in EXPECTED_EXPORTS:
        function = getattr(sign_routing, name)
        with pytest.raises(TypeError):
            function()
        with pytest.raises(TypeError):
            function(unruled_mode=True)


def test_literal_four_branch_coefficient_rows_and_anchor_shores() -> None:
    records = 0
    shores = 0
    for name, parameter, branch, a_value, gamma, constant, shift in ANCHOR_ROWS:
        coeff = sign_routing.branch_coefficients(_instance(name), branch, parameter)
        assert _coefficient_fields(coeff) == (a_value, gamma, constant)
        network = sign_routing.build_sign_routed_network(_instance(name), coeff)
        assert network.negative_shift == shift
        shores += _exercise_branch_shores(INSTANCES[name], branch, parameter, coeff)
        records += 1
    assert records == 120
    assert shores == 2080


def test_literal_original_arc_tuples_and_all_shore_cut_tables() -> None:
    records = 0
    shores = 0
    for row_id, name, raw, shift, arcs, values in NETWORK_ROWS:
        network = sign_routing.build_sign_routed_network(_instance(name), Coeff(*raw))
        assert network.arcs == arcs, row_id
        assert network.negative_shift == shift, row_id
        _check_emission(INSTANCES[name], raw, network)
        assert tuple(row[0] for row in values) == tuple(range(1 << INSTANCES[name][0]))
        for mask, psi, cut_value, recovered in values:
            assert _cut(network.arcs, network.source, mask) == cut_value, (row_id, mask)
            assert cut_value == psi + shift
            result = sign_routing.recover_objective(network, cut_value)
            assert type(result) is int and result == recovered
            shores += 1
        records += 1
    assert records == 8
    assert shores == 128


def test_branch_coefficient_identity() -> None:
    counts = {2: 0, 3: 0}
    base_shores = 0
    cases = 0
    shores = 0
    for records in _active_records():
        n = records[0]
        counts[n] += 1
        base_shores += 1 << n
        value = Instance(*records)
        for parameter in PARAMETERS:
            for branch in range(4):
                coeff = sign_routing.branch_coefficients(value, branch, parameter)
                shores += _exercise_branch_shores(records, branch, parameter, coeff)
                cases += 1
    assert counts == {2: 5, 3: 324}
    assert sum(counts.values()) == 329
    assert base_shores == 2612
    assert cases == 13160
    assert shores == 104480


def test_sign_routing_identity() -> None:
    cases = 0
    shores = 0
    for name in ("EQUALITY", "TRIANGLE"):
        records = INSTANCES[name]
        value = _instance(name)
        n = records[0]
        for a_value in (0, 2):
            for gamma in product((-2, 0, 3), repeat=n):
                for constant in (-3, 0, 5):
                    raw = a_value, gamma, constant
                    coeff = Coeff(*raw)
                    network = sign_routing.build_sign_routed_network(value, coeff)
                    _check_emission(records, raw, network)
                    shift = sum(-entry for entry in gamma if entry < 0)
                    for mask in range(1 << n):
                        psi = a_value * _sums(records, mask)[1] + sum(
                            gamma[v] for v in range(n) if (mask >> v) & 1
                        )
                        cut_value = _cut(network.arcs, n, mask)
                        assert cut_value == psi + shift
                        result = sign_routing.recover_objective(network, cut_value)
                        assert type(result) is int and result == psi + constant
                        shores += 1
                    assert _cut(network.arcs, n, 0) == shift
                    assert _cut(network.arcs, n, (1 << n) - 1) == sum(
                        entry for entry in gamma if entry > 0
                    )
                    cases += 1
    assert cases == 216
    assert shores == 1512


def test_zero_support_zero_spokes_and_all_zero_network_are_not_empty() -> None:
    # N2, N3, N4: fixed dimensions despite zero support/spoke capacities.
    for row in NETWORK_ROWS[1:4]:
        _, name, raw, shift, arcs, _ = row
        network = sign_routing.build_sign_routed_network(_instance(name), Coeff(*raw))
        assert network.arcs == arcs
        assert len(network.arcs) == 6
        assert network.negative_shift == shift
    all_zero = sign_routing.build_sign_routed_network(_instance("EQUALITY"), Coeff(0, (0, 0), 5))
    assert len(all_zero.arcs) == 6 and all(arc[2] == 0 for arc in all_zero.arcs)
    assert all_zero.arcs[-4:] == ((0, 3, 0), (3, 0, 0), (1, 3, 0), (3, 1, 0))


def test_scalar_recovery_separate_signs_without_cut_or_provenance_claim() -> None:
    for cut_value, shift, constant, expected in RECOVERY_ROWS:
        network = Network(1, (), shift, constant)
        result = sign_routing.recover_objective(network, cut_value)
        assert type(result) is int
        assert result == expected


def test_restricted_family_minimum_is_not_the_unrestricted_minimum() -> None:
    raw = (2, (-4, 5), -3)
    network = sign_routing.build_sign_routed_network(_instance("EQUALITY"), Coeff(*raw))
    cuts = tuple(_cut(network.arcs, 2, mask) for mask in range(4))
    assert cuts == (4, 6, 15, 5)
    results = tuple(sign_routing.recover_objective(network, cut) for cut in cuts)
    assert results == (-3, -1, 8, -2)
    family = (1, 2)
    assert min(cuts) == 4
    assert tuple(mask for mask in range(4) if cuts[mask] == min(cuts)) == (0,)
    restricted_cut = min(cuts[mask] for mask in family)
    assert restricted_cut == 6
    assert tuple(mask for mask in family if cuts[mask] == restricted_cut) == (1,)
    assert min(results) == -3
    assert min(results[mask] for mask in family) == -1
    assert sign_routing.recover_objective(network, restricted_cut) == -1


def test_zero_negative_parameters_active_equality_and_distinct_constants() -> None:
    for name in ("RICH", "MIXED", "EQUALITY"):
        n, edges, capacities = INSTANCES[name]
        degrees = tuple(sum(q for u, v, q in edges if x in (u, v)) for x in range(n))
        for parameter in PARAMETERS:
            for branch in range(4):
                coeff = sign_routing.branch_coefficients(_instance(name), branch, parameter)
                network = sign_routing.build_sign_routed_network(_instance(name), coeff)
                if parameter == (0, 1):
                    expected_gamma = capacities if branch < 2 else tuple(-d for d in degrees)
                    assert coeff.gamma == expected_gamma
                    zero_shift = 0 if branch < 2 else 2 * sum(q for _, _, q in edges)
                    assert network.negative_shift == zero_shift
                if branch >= 2 and parameter[0] >= 0:
                    assert all(entry < 0 for entry in coeff.gamma)
                if branch < 2 and parameter[0] < 0:
                    assert all(entry > 0 for entry in coeff.gamma)
                if name == "EQUALITY" and branch < 2:
                    assert coeff.gamma == tuple(parameter[1] * f for f in capacities)
    left = sign_routing.branch_coefficients(_instance("RICH"), 2, (-3, 1))
    right = sign_routing.branch_coefficients(_instance("RICH"), 3, (-3, 1))
    assert left.gamma == right.gamma == (1, 1, -2, 2, 4)
    assert (left.constant, right.constant) == (-3, -2)
    zeros = sign_routing.branch_coefficients(_instance("RICH"), 2, (-2, 1))
    assert zeros.gamma == (0, 0, -3, 1, 2)


def test_constant_only_variants_preserve_literal_arcs_and_negative_shift() -> None:
    _, name, raw, shift, arcs, values = NETWORK_ROWS[4]
    for constant in (-7, 0, 11):
        coeff = Coeff(raw[0], raw[1], constant)
        network = sign_routing.build_sign_routed_network(_instance(name), coeff)
        assert network.arcs == arcs and network.negative_shift == shift == 4
        assert network.constant == constant
        for mask, psi, cut_value, _ in values:
            assert _cut(network.arcs, network.source, mask) == cut_value
            assert sign_routing.recover_objective(network, cut_value) == psi + constant


def test_labels_and_repetition_never_change_raw_results_or_input_records() -> None:
    labels_cases = (None, ("v0", "v1", "v2", "v3", "v4"), (90, "one", -7, "three", 42))
    for name, parameter, branch, a_value, gamma, constant, _ in ANCHOR_ROWS:
        if name != "RICH":
            continue
        raw = a_value, gamma, constant
        for labels in labels_cases:
            value = Instance(*INSTANCES[name], labels=labels)
            original = (value.n, value.edges, value.f, value.labels)
            coeff = sign_routing.branch_coefficients(value, branch, parameter)
            assert _coefficient_fields(coeff) == raw
            network = sign_routing.build_sign_routed_network(value, coeff)
            _check_emission(INSTANCES[name], raw, network)
            assert sign_routing.branch_coefficients(value, branch, parameter) == coeff
            assert sign_routing.build_sign_routed_network(value, coeff) == network
            for mask in range(1 << value.n):
                sign_routing.recover_objective(network, _cut(network.arcs, value.n, mask))
            assert original == (value.n, value.edges, value.f, value.labels)
            assert _coefficient_fields(coeff) == raw
            _check_emission(INSTANCES[name], raw, network)


def test_declared_exact_valueerror_matrix() -> None:
    # ORACLE-051's named placeholders are normally constructed objects, never forged records.
    EQUALITY = _instance("EQUALITY")
    InstanceSubclass = _InstanceSubclass(*INSTANCES["EQUALITY"])
    VerifierInstance = BruteInstance(*INSTANCES["EQUALITY"])
    CoeffSubclass = _CoeffSubclass(1, (0, 0), 0)
    NetworkSubclass = _NetworkSubclass(1, (), 7, -2)
    GOOD_COEFF = Coeff(1, (0, 0), 0)
    EMPTY_RECORD = Network(1, (), 7, -2)
    rows = (
        ('R01', 'SignRoutingCoefficients', (-1, (), 0)),
        ('R02', 'SignRoutingCoefficients', (True, (), 0)),
        ('R03', 'SignRoutingCoefficients', (IntSubclass(1), (), 0)),
        ('R04', 'SignRoutingCoefficients', (0, [1], 0)),
        ('R05', 'SignRoutingCoefficients', (0, TupleSubclass((1,)), 0)),
        ('R06', 'SignRoutingCoefficients', (0, iter((1,)), 0)),
        ('R07', 'SignRoutingCoefficients', (0, (True,), 0)),
        ('R08', 'SignRoutingCoefficients', (0, (IntSubclass(1),), 0)),
        ('R09', 'SignRoutingCoefficients', (0, (1.0,), 0)),
        ('R10', 'SignRoutingCoefficients', (0, (Fraction(1,1),), 0)),
        ('R11', 'SignRoutingCoefficients', (0, (Hostile(),), 0)),
        ('R12', 'SignRoutingCoefficients', (0, (), False)),
        ('R13', 'SignRoutingCoefficients', (0, (), 0.0)),
        ('R14', 'SignRoutingCoefficients', (0, (), Hostile())),
        ('R15', 'SignRoutedNetwork', (0, (), 0, 0)),
        ('R16', 'SignRoutedNetwork', (True, (), 0, 0)),
        ('R17', 'SignRoutedNetwork', (IntSubclass(1), (), 0, 0)),
        ('R18', 'SignRoutedNetwork', (1, [], 0, 0)),
        ('R19', 'SignRoutedNetwork', (1, TupleSubclass(()), 0, 0)),
        ('R20', 'SignRoutedNetwork', (1, iter(()), 0, 0)),
        ('R21', 'SignRoutedNetwork', (1, ([0,1,2],), 0, 0)),
        ('R22', 'SignRoutedNetwork', (1, ((0,1),), 0, 0)),
        ('R23', 'SignRoutedNetwork', (1, ((0,1,2,3),), 0, 0)),
        ('R24', 'SignRoutedNetwork', (1, ((True,1,0),), 0, 0)),
        ('R25', 'SignRoutedNetwork', (1, ((0,False,0),), 0, 0)),
        ('R26', 'SignRoutedNetwork', (1, ((0,1,True),), 0, 0)),
        ('R27', 'SignRoutedNetwork', (1, ((0,1,1.0),), 0, 0)),
        ('R28', 'SignRoutedNetwork', (1, ((0,1,Hostile()),), 0, 0)),
        ('R29', 'SignRoutedNetwork', (1, ((-1,1,0),), 0, 0)),
        ('R30', 'SignRoutedNetwork', (1, ((0,3,0),), 0, 0)),
        ('R31', 'SignRoutedNetwork', (1, ((0,0,0),), 0, 0)),
        ('R32', 'SignRoutedNetwork', (1, ((0,1,-1),), 0, 0)),
        ('R33', 'SignRoutedNetwork', (1, (), -1, 0)),
        ('R34', 'SignRoutedNetwork', (1, (), True, 0)),
        ('R35', 'SignRoutedNetwork', (1, (), Hostile(), 0)),
        ('R36', 'SignRoutedNetwork', (1, (), 0, False)),
        ('R37', 'SignRoutedNetwork', (1, (), 0, Fraction(0,1))),
        ('R38', 'SignRoutedNetwork', (1, (), 0, Hostile())),
        ('R39', 'branch_coefficients', (None, 0, (0,1))),
        ('R40', 'branch_coefficients', (InstanceSubclass, 0, (0,1))),
        ('R41', 'branch_coefficients', (VerifierInstance, 0, (0,1))),
        ('R42', 'branch_coefficients', (Hostile(), 0, (0,1))),
        ('R43', 'build_sign_routed_network', (None, GOOD_COEFF)),
        ('R44', 'build_sign_routed_network', (InstanceSubclass, GOOD_COEFF)),
        ('R45', 'build_sign_routed_network', (VerifierInstance, GOOD_COEFF)),
        ('R46', 'build_sign_routed_network', (Hostile(), GOOD_COEFF)),
        ('R47', 'branch_coefficients', (EQUALITY, -1, (0,1))),
        ('R48', 'branch_coefficients', (EQUALITY, 4, (0,1))),
        ('R49', 'branch_coefficients', (EQUALITY, True, (0,1))),
        ('R50', 'branch_coefficients', (EQUALITY, IntSubclass(0), (0,1))),
        ('R51', 'branch_coefficients', (EQUALITY, "0", (0,1))),
        ('R52', 'branch_coefficients', (EQUALITY, Hostile(), (0,1))),
        ('R53', 'branch_coefficients', (EQUALITY, 0, [0,1])),
        ('R54', 'branch_coefficients', (EQUALITY, 0, (0,))),
        ('R55', 'branch_coefficients', (EQUALITY, 0, (0,1,2))),
        ('R56', 'branch_coefficients', (EQUALITY, 0, TupleSubclass((0,1)))),
        ('R57', 'branch_coefficients', (EQUALITY, 0, (True,1))),
        ('R58', 'branch_coefficients', (EQUALITY, 0, (0,False))),
        ('R59', 'branch_coefficients', (EQUALITY, 0, (IntSubclass(0),1))),
        ('R60', 'branch_coefficients', (EQUALITY, 0, (0,0))),
        ('R61', 'branch_coefficients', (EQUALITY, 0, (0,-1))),
        ('R62', 'branch_coefficients', (EQUALITY, 0, (0,1.0))),
        ('R63', 'branch_coefficients', (EQUALITY, 0, (Fraction(0,1),1))),
        ('R64', 'branch_coefficients', (EQUALITY, 0, iter((0,1)))),
        ('R65', 'branch_coefficients', (EQUALITY, 0, ExactValue(0,1))),
        ('R66', 'branch_coefficients', (EQUALITY, 0, Hostile())),
        ('R67', 'build_sign_routed_network', (EQUALITY, None)),
        ('R68', 'build_sign_routed_network', (EQUALITY, CoeffSubclass)),
        ('R69', 'build_sign_routed_network', (EQUALITY, Hostile())),
        ('R70', 'build_sign_routed_network', (EQUALITY, Coeff(1, (), 0))),
        ('R71', 'build_sign_routed_network', (EQUALITY, Coeff(1, (0,), 0))),
        ('R72', 'build_sign_routed_network', (EQUALITY, Coeff(1, (0,0,0), 0))),
        ('R73', 'recover_objective', (None, 0)),
        ('R74', 'recover_objective', (NetworkSubclass, 0)),
        ('R75', 'recover_objective', (Hostile(), 0)),
        ('R76', 'recover_objective', (EMPTY_RECORD, -1)),
        ('R77', 'recover_objective', (EMPTY_RECORD, True)),
        ('R78', 'recover_objective', (EMPTY_RECORD, IntSubclass(0))),
        ('R79', 'recover_objective', (EMPTY_RECORD, 0.0)),
        ('R80', 'recover_objective', (EMPTY_RECORD, Fraction(0,1))),
        ('R81', 'recover_objective', (EMPTY_RECORD, Hostile())),
    )
    assert tuple(row[0] for row in rows) == tuple(f"R{index:02d}" for index in range(1, 82))
    for row_id, api, args in rows:
        with pytest.raises(ValueError) as caught:
            getattr(sign_routing, api)(*args)
        assert type(caught.value) is ValueError, row_id


def test_supplementary_wrong_scalar_types_at_each_numeric_boundary() -> None:
    for wrong in (None, True, IntSubclass(1), 1.0, Fraction(1, 1), Hostile()):
        _exact_error(Coeff, wrong, (), 0)
        _exact_error(Coeff, 0, (wrong,), 0)
        _exact_error(Coeff, 0, (), wrong)
        _exact_error(Network, wrong, (), 0, 0)
        _exact_error(Network, 1, ((wrong, 1, 0),), 0, 0)
        _exact_error(Network, 1, ((0, wrong, 0),), 0, 0)
        _exact_error(Network, 1, ((0, 1, wrong),), 0, 0)
        _exact_error(Network, 1, (), wrong, 0)
        _exact_error(Network, 1, (), 0, wrong)
        _exact_error(sign_routing.branch_coefficients, _instance("EQUALITY"), wrong, (0, 1))
        _exact_error(sign_routing.branch_coefficients, _instance("EQUALITY"), 0, (wrong, 1))
        _exact_error(sign_routing.branch_coefficients, _instance("EQUALITY"), 0, (0, wrong))
        _exact_error(sign_routing.recover_objective, Network(1, (), 0, 0), wrong)
    _exact_error(Network, 1, (TupleSubclass((0, 1, 0)),), 0, 0)
    _exact_error(Network, 1, ((3, 0, 0),), 0, 0)
    _exact_error(Network, 1, ((0, -1, 0),), 0, 0)


def test_validation_precedes_graph_dependent_work(monkeypatch: pytest.MonkeyPatch) -> None:
    value = _instance("EQUALITY")
    valid_coeff = Coeff(1, (0, 0), 0)
    wrong_length = Coeff(1, (), 0)
    original = Instance.__getattribute__

    def guarded(self: Instance, name: str) -> object:
        if name in ("edges", "f", "d_q"):
            raise AssertionError("graph accessed before all argument validation")
        return original(self, name)

    with monkeypatch.context() as context:
        context.setattr(Instance, "__getattribute__", guarded)
        for parameter in ([0, 1], (0, 0), Hostile()):
            _exact_error(sign_routing.branch_coefficients, value, 0, parameter)
        _exact_error(sign_routing.branch_coefficients, value, True, (0, 1))
        _exact_error(sign_routing.build_sign_routed_network, value, None)
        _exact_error(sign_routing.build_sign_routed_network, value, wrong_length)
    # Normal successful calls are still possible after the observational guard is removed.
    _check_emission(INSTANCES["EQUALITY"], (1, (0, 0), 0),
                    sign_routing.build_sign_routed_network(value, valid_coeff))


def test_closed_pair_validation_occurs_before_degree_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events = []
    validator_names = [
        name for name, value in vars(sign_routing).items() if value is closed_validate_pair
    ]
    assert validator_names
    getter = Instance.d_q.fget
    assert getter is not None

    def tracked_validation(pair: tuple[int, int]) -> None:
        events.append("pair")
        closed_validate_pair(pair)

    def tracked_degree(instance: Instance) -> tuple[int, ...]:
        events.append("degree")
        return getter(instance)

    value = _instance("RICH")
    with monkeypatch.context() as context:
        for name in validator_names:
            context.setattr(sign_routing, name, tracked_validation)
        context.setattr(Instance, "d_q", property(tracked_degree))
        _exact_error(sign_routing.branch_coefficients, None, 0, (0, 1))
        _exact_error(sign_routing.branch_coefficients, value, -1, (0, 1))
        assert events == []
        _exact_error(sign_routing.branch_coefficients, value, 0, (0, 0))
        assert events == ["pair"]
        events.clear()
        coeff = sign_routing.branch_coefficients(value, 2, (-3, 1))
        assert _coefficient_fields(coeff) == (1, (1, 1, -2, 2, 4), -3)
        assert events == ["pair", "degree"]


def test_degree_tuple_is_obtained_once_per_branch_call(monkeypatch: pytest.MonkeyPatch) -> None:
    getter = Instance.d_q.fget
    assert getter is not None
    accesses = []

    def tracked_degree(instance: Instance) -> tuple[int, ...]:
        accesses.append(instance.n)
        return getter(instance)

    values = {name: _instance(name) for name in ("RICH", "MIXED", "EQUALITY")}
    with monkeypatch.context() as context:
        context.setattr(Instance, "d_q", property(tracked_degree))
        for name, parameter, branch, a_value, gamma, constant, _ in ANCHOR_ROWS:
            before = len(accesses)
            coeff = sign_routing.branch_coefficients(values[name], branch, parameter)
            assert len(accesses) == before + 1
            assert _coefficient_fields(coeff) == (a_value, gamma, constant)
    assert len(accesses) == 120


def test_recovery_does_not_rescan_arcs_or_certify_network(monkeypatch: pytest.MonkeyPatch) -> None:
    network = Network(1, (), 7, -2)
    original = Network.__getattribute__

    def guarded(self: object, name: str) -> object:
        if name in ("arcs", "vertex_count", "source", "sink", "node_count"):
            raise AssertionError("recovery inspected fields unrelated to scalar shift")
        return original(self, name)

    with monkeypatch.context() as context:
        context.setattr(Network, "__getattribute__", guarded)
        assert sign_routing.recover_objective(network, 0) == -9
        assert sign_routing.recover_objective(network, 10) == 1
        _exact_error(sign_routing.recover_objective, network, True)


def test_positive_branch_scaling_uses_independent_expected_values() -> None:
    cases = 0
    shores = 0
    for exponent in (0, 1, 8, 64, 4096):
        factor = 1 << exponent
        for branch in range(4):
            raw = _coefficient_oracle(INSTANCES["RICH"], branch, (-3, 1))
            scaled = (raw[0] * factor, tuple(x * factor for x in raw[1]), raw[2] * factor)
            coeff = sign_routing.branch_coefficients(
                _instance("RICH"), branch, (-3 * factor, factor),
            )
            assert _coefficient_fields(coeff) == scaled
            network = sign_routing.build_sign_routed_network(_instance("RICH"), coeff)
            _check_emission(INSTANCES["RICH"], scaled, network)
            for mask in range(32):
                expected = _source_residual(INSTANCES["RICH"], branch, (-3, 1), mask) * factor
                result = sign_routing.recover_objective(network, _cut(network.arcs, 5, mask))
                assert type(result) is int and result == expected
                shores += 1
            cases += 1
    assert (cases, shores) == (20, 640)


def test_positive_generic_scaling_from_literal_network_n5() -> None:
    _, name, raw, shift, arcs, values = NETWORK_ROWS[4]
    cases = 0
    shores = 0
    for exponent in (0, 1, 8, 64, 4096):
        factor = 1 << exponent
        scaled = (raw[0] * factor, tuple(x * factor for x in raw[1]), raw[2] * factor)
        network = sign_routing.build_sign_routed_network(_instance(name), Coeff(*scaled))
        assert network.arcs == tuple((u, v, capacity * factor) for u, v, capacity in arcs)
        assert network.negative_shift == shift * factor
        assert network.constant == raw[2] * factor
        for mask, _, cut_value, expected in values:
            assert _cut(network.arcs, 4, mask) == cut_value * factor
            assert sign_routing.recover_objective(network, cut_value * factor) == expected * factor
            shores += 1
        cases += 1
    assert (cases, shores) == (5, 80)


def test_huge_multiplicities_and_unreduced_parameter_entries() -> None:
    cases = 0
    shores = 0
    for exponent in (1, 8, 64, 4096):
        large = 1 << exponent
        records = (2, ((0, 1, large),), (large, large))
        for branch in range(4):
            coeff = sign_routing.branch_coefficients(
                Instance(*records), branch, (-large, large + 1),
            )
            gamma = (large * (large + 1),) * 2 if branch < 2 else (-large, -large)
            constant = (-1, -2 * (large + 1), -large, -2 * (large + 1))[branch]
            assert _coefficient_fields(coeff) == (large + 1, gamma, constant)
            network = sign_routing.build_sign_routed_network(Instance(*records), coeff)
            _check_emission(records, (large + 1, gamma, constant), network)
            for mask in range(4):
                expected = _source_residual(records, branch, (-large, large + 1), mask)
                recovered = sign_routing.recover_objective(network, _cut(network.arcs, 2, mask))
                assert type(recovered) is int and recovered == expected
                shores += 1
            cases += 1
    assert (cases, shores) == (16, 64)


def test_huge_generic_mixed_zero_signs_and_standalone_records() -> None:
    cases = 0
    shores = 0
    for exponent in (1, 8, 64, 4096):
        large = 1 << exponent
        raw = (large, (-large, 0, large + 3), -(large + 7))
        coeff = Coeff(*raw)
        assert _coefficient_fields(coeff) == raw
        network = sign_routing.build_sign_routed_network(_instance("TRIANGLE"), coeff)
        _check_emission(INSTANCES["TRIANGLE"], raw, network)
        assert network.negative_shift == large
        for mask in range(8):
            psi = large * _sums(INSTANCES["TRIANGLE"], mask)[1] + sum(
                raw[1][v] for v in range(3) if (mask >> v) & 1
            )
            cut_value = _cut(network.arcs, 3, mask)
            assert cut_value == psi + large
            assert sign_routing.recover_objective(network, cut_value) == psi - (large + 7)
            shores += 1
        cases += 1
        record = Network(1, ((0, 2, large), (0, 2, 0)), large + 3, -large)
        assert _network_fields(record) == (1, ((0, 2, large), (0, 2, 0)), large + 3, -large)
    assert (cases, shores) == (4, 32)
