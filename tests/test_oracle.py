"""Tests-first Unit 12 branch-oracle contract, BO1--BO22 / ORACLE-069--082.

Literal tables were transcribed from the sealed catalogue. Expected arithmetic,
source domains, and least restricted minimizers below use original records only.
No private handoff JSON, global verifier, or production result seeds expectations.
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
from dataclasses import MISSING, FrozenInstanceError, fields, is_dataclass, replace
from fractions import Fraction
from functools import partial
from itertools import combinations, product
from pathlib import Path
from typing import get_type_hints

import pytest

from exactfrac.families import AtomicFamily, enumerate_atomic_families
from exactfrac.instance import Instance
from exactfrac.parity_cut import (
    ParityCutResult,
    ParityCutStats,
    lift_source_shore,
    minimum_parity_cut,
    reduce_atomic_family,
)
from exactfrac.rational import residual_numerator, validate_pair
from exactfrac.shore import validate_shore
from exactfrac.sign_routing import (
    branch_coefficients,
    build_sign_routed_network,
    recover_objective,
)
from exactfrac.witness import ExactValue, shore_b_q, shore_d_q, shore_f

oracle = importlib.import_module("exactfrac.oracle")
Context = oracle.BranchOracleContext
Result = oracle.BranchOracleResult
Stats = oracle.BranchOracleStats
query = oracle.exact_branch_min
parity_module = importlib.import_module("exactfrac.parity_cut")
BruteInstance = importlib.import_module("exactfrac_verify.brute").BruteInstance

# Literal transcriptions: committed ORACLE-069--082 (all 23 tables).
# No test opens a handoff file or builds expectations from candidate output.

# INPUTS: name, n, edges, f, d_q, Q
INPUTS = (('Q1', 2, ((0, 1, 1),), (1, 1), (1, 1), 1),
 ('DOUBLE', 2, ((0, 1, 2),), (1, 1), (2, 2), 2),
 ('UNEQUAL', 2, ((0, 1, 2),), (2, 1), (2, 2), 2),
 ('EQUALITY', 3, ((0, 1, 1), (0, 2, 1), (1, 2, 1)), (2, 2, 2), (2, 2, 2), 3),
 ('WTRI', 3, ((0, 1, 1), (0, 2, 1), (1, 2, 1)), (1, 1, 1), (2, 2, 2), 3),
 ('ODDFULL', 3, ((0, 1, 1), (0, 2, 1), (1, 2, 1)), (2, 2, 1), (2, 2, 2), 3),
 ('TIECARD', 3, ((0, 2, 1), (1, 2, 1)), (1, 1, 2), (1, 1, 2), 2),
 ('RICH', 5, ((0, 2, 2), (1, 2, 2), (2, 4, 1), (3, 4, 1)), (1, 1, 1, 1, 2), (2, 2, 5, 1, 2), 6),
 ('MIXED',
  4,
  ((0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 4), (1, 3, 2), (2, 3, 5)),
  (2, 3, 4, 5),
  (6, 8, 12, 8),
  17))

# PARAMETERS: index, raw_parameter
PARAMETERS = ((0, (-5, 2)),
 (1, (-2, 1)),
 (2, (-1, 1)),
 (3, (0, 1)),
 (4, (0, 3)),
 (5, (1, 2)),
 (6, (1, 1)),
 (7, (2, 1)),
 (8, (3, 2)),
 (9, (7, 3)))

# COVERS: instance, j, R_all, examined_feasible_parity_ordinary, network_builds_per_query,
# N_F_in_feasible_order
COVERS = (('Q1', 0, 3, (1, 0, 0, 0), 0, ()),
 ('Q1', 1, 3, (0, 0, 0, 0), 0, ()),
 ('Q1', 2, 3, (0, 0, 0, 0), 0, ()),
 ('Q1', 3, 3, (2, 0, 0, 0), 0, ()),
 ('DOUBLE', 0, 7, (1, 1, 1, 7), 1, (4,)),
 ('DOUBLE', 1, 7, (4, 0, 0, 0), 0, ()),
 ('DOUBLE', 2, 7, (0, 0, 0, 0), 0, ()),
 ('DOUBLE', 3, 7, (2, 0, 0, 0), 0, ()),
 ('UNEQUAL', 0, 6, (1, 1, 1, 7), 1, (4,)),
 ('UNEQUAL', 1, 6, (2, 0, 0, 0), 0, ()),
 ('UNEQUAL', 2, 6, (1, 1, 1, 3), 1, (3,)),
 ('UNEQUAL', 3, 6, (2, 1, 1, 1), 1, (2,)),
 ('EQUALITY', 0, 10, (1, 0, 0, 0), 0, ()),
 ('EQUALITY', 1, 10, (0, 0, 0, 0), 0, ()),
 ('EQUALITY', 2, 10, (3, 0, 0, 0), 0, ()),
 ('EQUALITY', 3, 10, (6, 6, 6, 18), 1, (3, 3, 3, 3, 3, 3)),
 ('WTRI', 0, 26, (1, 1, 1, 13), 1, (5,)),
 ('WTRI', 1, 26, (18, 12, 12, 24), 1, (3, 3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 3)),
 ('WTRI', 2, 26, (1, 1, 1, 1), 1, (2,)),
 ('WTRI', 3, 26, (6, 6, 6, 18), 1, (3, 3, 3, 3, 3, 3)),
 ('ODDFULL', 0, 15, (1, 1, 1, 13), 1, (5,)),
 ('ODDFULL', 1, 15, (6, 0, 0, 0), 0, ()),
 ('ODDFULL', 2, 15, (2, 2, 2, 14), 1, (4, 4)),
 ('ODDFULL', 3, 15, (6, 4, 4, 12), 1, (3, 3, 3, 3)),
 ('TIECARD', 0, 6, (1, 0, 0, 0), 0, ()),
 ('TIECARD', 1, 6, (0, 0, 0, 0), 0, ()),
 ('TIECARD', 2, 6, (1, 1, 1, 7), 1, (4,)),
 ('TIECARD', 3, 6, (4, 4, 4, 12), 1, (3, 3, 3, 3)),
 ('RICH', 0, 38, (1, 1, 1, 31), 1, (7,)),
 ('RICH', 1, 38, (24, 17, 17, 149), 1, (5, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 5, 5, 5, 4, 4)),
 ('RICH', 2, 38, (5, 5, 5, 49), 1, (6, 4, 4, 4, 4)),
 ('RICH', 3, 38, (8, 8, 8, 104), 1, (5, 5, 5, 5, 5, 5, 5, 5)),
 ('MIXED', 0, 65, (1, 1, 1, 21), 1, (6,)),
 ('MIXED',
  1,
  65,
  (48, 26, 26, 118),
  1,
  (4, 4, 4, 3, 3, 3, 3, 4, 3, 3, 3, 4, 3, 3, 3, 4, 3, 3, 4, 4, 3, 3, 3, 4, 3, 4)),
 ('MIXED', 2, 65, (4, 4, 4, 52), 1, (5, 5, 5, 5)),
 ('MIXED', 3, 65, (12, 10, 10, 70), 1, (4, 4, 4, 4, 4, 4, 4, 4, 4, 4)))

# FAMILIES: instance, j, index, T_pi_I_O, nonempty, all_original_members
FAMILIES = (('Q1', 0, 0, (0, 1, 0, 0), False, ()),
 ('Q1', 3, 0, (3, 0, 1, 2), False, ()),
 ('Q1', 3, 1, (3, 0, 2, 1), False, ()),
 ('DOUBLE', 0, 0, (3, 1, 0, 0), True, (1, 2)),
 ('DOUBLE', 1, 0, (3, 0, 1, 2), False, ()),
 ('DOUBLE', 1, 1, (3, 0, 3, 1), False, ()),
 ('DOUBLE', 1, 2, (3, 0, 3, 2), False, ()),
 ('DOUBLE', 1, 3, (3, 0, 2, 1), False, ()),
 ('DOUBLE', 3, 0, (3, 0, 1, 2), False, ()),
 ('DOUBLE', 3, 1, (3, 0, 2, 1), False, ()),
 ('UNEQUAL', 0, 0, (2, 1, 0, 0), True, (2, 3)),
 ('UNEQUAL', 1, 0, (2, 0, 3, 2), False, ()),
 ('UNEQUAL', 1, 1, (2, 0, 2, 1), False, ()),
 ('UNEQUAL', 2, 0, (2, 1, 1, 0), True, (3,)),
 ('UNEQUAL', 3, 0, (2, 0, 1, 2), True, (1,)),
 ('UNEQUAL', 3, 1, (2, 0, 2, 1), False, ()),
 ('EQUALITY', 0, 0, (0, 1, 0, 0), False, ()),
 ('EQUALITY', 2, 0, (0, 1, 1, 0), False, ()),
 ('EQUALITY', 2, 1, (0, 1, 2, 0), False, ()),
 ('EQUALITY', 2, 2, (0, 1, 4, 0), False, ()),
 ('EQUALITY', 3, 0, (0, 0, 1, 2), True, (1, 5)),
 ('EQUALITY', 3, 1, (0, 0, 2, 1), True, (2, 6)),
 ('EQUALITY', 3, 2, (0, 0, 1, 4), True, (1, 3)),
 ('EQUALITY', 3, 3, (0, 0, 4, 1), True, (4, 6)),
 ('EQUALITY', 3, 4, (0, 0, 2, 4), True, (2, 3)),
 ('EQUALITY', 3, 5, (0, 0, 4, 2), True, (4, 5)),
 ('WTRI', 0, 0, (7, 1, 0, 0), True, (1, 2, 4, 7)),
 ('WTRI', 1, 0, (7, 0, 1, 2), True, (5,)),
 ('WTRI', 1, 1, (7, 0, 3, 1), False, ()),
 ('WTRI', 1, 2, (7, 0, 1, 4), True, (3,)),
 ('WTRI', 1, 3, (7, 0, 5, 1), False, ()),
 ('WTRI', 1, 4, (7, 0, 3, 4), True, (3,)),
 ('WTRI', 1, 5, (7, 0, 5, 2), True, (5,)),
 ('WTRI', 1, 6, (7, 0, 3, 2), False, ()),
 ('WTRI', 1, 7, (7, 0, 2, 1), True, (6,)),
 ('WTRI', 1, 8, (7, 0, 3, 4), True, (3,)),
 ('WTRI', 1, 9, (7, 0, 6, 1), True, (6,)),
 ('WTRI', 1, 10, (7, 0, 2, 4), True, (3,)),
 ('WTRI', 1, 11, (7, 0, 6, 2), False, ()),
 ('WTRI', 1, 12, (7, 0, 5, 2), True, (5,)),
 ('WTRI', 1, 13, (7, 0, 6, 1), True, (6,)),
 ('WTRI', 1, 14, (7, 0, 5, 4), False, ()),
 ('WTRI', 1, 15, (7, 0, 4, 1), True, (6,)),
 ('WTRI', 1, 16, (7, 0, 6, 4), False, ()),
 ('WTRI', 1, 17, (7, 0, 4, 2), True, (5,)),
 ('WTRI', 2, 0, (7, 1, 7, 0), True, (7,)),
 ('WTRI', 3, 0, (7, 0, 1, 2), True, (5,)),
 ('WTRI', 3, 1, (7, 0, 2, 1), True, (6,)),
 ('WTRI', 3, 2, (7, 0, 1, 4), True, (3,)),
 ('WTRI', 3, 3, (7, 0, 4, 1), True, (6,)),
 ('WTRI', 3, 4, (7, 0, 2, 4), True, (3,)),
 ('WTRI', 3, 5, (7, 0, 4, 2), True, (5,)),
 ('ODDFULL', 0, 0, (4, 1, 0, 0), True, (4, 5, 6, 7)),
 ('ODDFULL', 1, 0, (4, 0, 5, 2), False, ()),
 ('ODDFULL', 1, 1, (4, 0, 6, 1), False, ()),
 ('ODDFULL', 1, 2, (4, 0, 5, 4), False, ()),
 ('ODDFULL', 1, 3, (4, 0, 4, 1), False, ()),
 ('ODDFULL', 1, 4, (4, 0, 6, 4), False, ()),
 ('ODDFULL', 1, 5, (4, 0, 4, 2), False, ()),
 ('ODDFULL', 2, 0, (4, 1, 1, 0), True, (5, 7)),
 ('ODDFULL', 2, 1, (4, 1, 2, 0), True, (6, 7)),
 ('ODDFULL', 3, 0, (4, 0, 1, 2), True, (1,)),
 ('ODDFULL', 3, 1, (4, 0, 2, 1), True, (2,)),
 ('ODDFULL', 3, 2, (4, 0, 1, 4), True, (1, 3)),
 ('ODDFULL', 3, 3, (4, 0, 4, 1), False, ()),
 ('ODDFULL', 3, 4, (4, 0, 2, 4), True, (2, 3)),
 ('ODDFULL', 3, 5, (4, 0, 4, 2), False, ()),
 ('TIECARD', 0, 0, (0, 1, 0, 0), False, ()),
 ('TIECARD', 2, 0, (3, 1, 4, 0), True, (5, 6)),
 ('TIECARD', 3, 0, (3, 0, 1, 4), True, (3,)),
 ('TIECARD', 3, 1, (3, 0, 4, 1), True, (4,)),
 ('TIECARD', 3, 2, (3, 0, 2, 4), True, (3,)),
 ('TIECARD', 3, 3, (3, 0, 4, 2), True, (4,)),
 ('RICH',
  0,
  0,
  (3, 1, 0, 0),
  True,
  (1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, 30)),
 ('RICH', 1, 0, (3, 0, 1, 4), True, (3, 11, 19, 27)),
 ('RICH', 1, 1, (3, 0, 5, 1), False, ()),
 ('RICH', 1, 2, (3, 0, 3, 4), True, (3, 11, 19, 27)),
 ('RICH', 1, 3, (3, 0, 5, 2), False, ()),
 ('RICH', 1, 4, (3, 0, 5, 16), True, (7, 15)),
 ('RICH', 1, 5, (3, 0, 17, 4), True, (19, 27)),
 ('RICH', 1, 6, (3, 0, 9, 16), True, (11, 15)),
 ('RICH', 1, 7, (3, 0, 17, 8), True, (19, 23)),
 ('RICH', 1, 8, (3, 0, 3, 4), True, (3, 11, 19, 27)),
 ('RICH', 1, 9, (3, 0, 6, 1), False, ()),
 ('RICH', 1, 10, (3, 0, 2, 4), True, (3, 11, 19, 27)),
 ('RICH', 1, 11, (3, 0, 6, 2), False, ()),
 ('RICH', 1, 12, (3, 0, 6, 16), True, (7, 15)),
 ('RICH', 1, 13, (3, 0, 18, 4), True, (19, 27)),
 ('RICH', 1, 14, (3, 0, 10, 16), True, (11, 15)),
 ('RICH', 1, 15, (3, 0, 18, 8), True, (19, 23)),
 ('RICH', 1, 16, (3, 0, 5, 4), False, ()),
 ('RICH', 1, 17, (3, 0, 4, 1), True, (4, 12, 20, 28)),
 ('RICH', 1, 18, (3, 0, 6, 4), False, ()),
 ('RICH', 1, 19, (3, 0, 4, 2), True, (4, 12, 20, 28)),
 ('RICH', 1, 20, (3, 0, 4, 16), True, (4, 7, 12, 15)),
 ('RICH', 1, 21, (3, 0, 20, 4), False, ()),
 ('RICH', 1, 22, (3, 0, 12, 16), True, (12, 15)),
 ('RICH', 1, 23, (3, 0, 20, 8), True, (20, 23)),
 ('RICH', 2, 0, (15, 1, 16, 0), True, (17, 18, 20, 23, 24, 27, 29, 30)),
 ('RICH', 2, 1, (15, 1, 7, 0), True, (7, 23)),
 ('RICH', 2, 2, (15, 1, 11, 0), True, (11, 27)),
 ('RICH', 2, 3, (15, 1, 13, 0), True, (13, 29)),
 ('RICH', 2, 4, (15, 1, 14, 0), True, (14, 30)),
 ('RICH', 3, 0, (15, 0, 1, 4), True, (3, 9, 19, 25)),
 ('RICH', 3, 1, (15, 0, 4, 1), True, (6, 12, 22, 28)),
 ('RICH', 3, 2, (15, 0, 2, 4), True, (3, 10, 19, 26)),
 ('RICH', 3, 3, (15, 0, 4, 2), True, (5, 12, 21, 28)),
 ('RICH', 3, 4, (15, 0, 4, 16), True, (5, 6, 12, 15)),
 ('RICH', 3, 5, (15, 0, 16, 4), True, (16, 19, 25, 26)),
 ('RICH', 3, 6, (15, 0, 8, 16), True, (9, 10, 12, 15)),
 ('RICH', 3, 7, (15, 0, 16, 8), True, (16, 19, 21, 22)),
 ('MIXED', 0, 0, (10, 1, 0, 0), True, (2, 3, 6, 7, 8, 9, 12, 13)),
 ('MIXED', 1, 0, (10, 0, 1, 2), True, (1, 5)),
 ('MIXED', 1, 1, (10, 0, 3, 1), False, ()),
 ('MIXED', 1, 2, (10, 0, 1, 4), True, (1, 11)),
 ('MIXED', 1, 3, (10, 0, 5, 1), False, ()),
 ('MIXED', 1, 4, (10, 0, 1, 8), True, (1, 5)),
 ('MIXED', 1, 5, (10, 0, 9, 1), False, ()),
 ('MIXED', 1, 6, (10, 0, 3, 4), True, (11,)),
 ('MIXED', 1, 7, (10, 0, 5, 2), True, (5,)),
 ('MIXED', 1, 8, (10, 0, 3, 8), False, ()),
 ('MIXED', 1, 9, (10, 0, 9, 2), False, ()),
 ('MIXED', 1, 10, (10, 0, 5, 8), True, (5,)),
 ('MIXED', 1, 11, (10, 0, 9, 4), True, (11,)),
 ('MIXED', 1, 12, (10, 0, 3, 2), False, ()),
 ('MIXED', 1, 13, (10, 0, 2, 1), True, (10, 14)),
 ('MIXED', 1, 14, (10, 0, 3, 4), True, (11,)),
 ('MIXED', 1, 15, (10, 0, 6, 1), True, (14,)),
 ('MIXED', 1, 16, (10, 0, 3, 8), False, ()),
 ('MIXED', 1, 17, (10, 0, 10, 1), True, (10, 14)),
 ('MIXED', 1, 18, (10, 0, 2, 4), True, (10, 11)),
 ('MIXED', 1, 19, (10, 0, 6, 2), False, ()),
 ('MIXED', 1, 20, (10, 0, 2, 8), False, ()),
 ('MIXED', 1, 21, (10, 0, 10, 2), False, ()),
 ('MIXED', 1, 22, (10, 0, 6, 8), False, ()),
 ('MIXED', 1, 23, (10, 0, 10, 4), True, (10, 11)),
 ('MIXED', 1, 24, (10, 0, 5, 2), True, (5,)),
 ('MIXED', 1, 25, (10, 0, 6, 1), True, (14,)),
 ('MIXED', 1, 26, (10, 0, 5, 4), False, ()),
 ('MIXED', 1, 27, (10, 0, 4, 1), True, (4, 14)),
 ('MIXED', 1, 28, (10, 0, 5, 8), True, (5,)),
 ('MIXED', 1, 29, (10, 0, 12, 1), True, (14,)),
 ('MIXED', 1, 30, (10, 0, 6, 4), False, ()),
 ('MIXED', 1, 31, (10, 0, 4, 2), True, (4, 5)),
 ('MIXED', 1, 32, (10, 0, 6, 8), False, ()),
 ('MIXED', 1, 33, (10, 0, 12, 2), False, ()),
 ('MIXED', 1, 34, (10, 0, 4, 8), True, (4, 5)),
 ('MIXED', 1, 35, (10, 0, 12, 4), False, ()),
 ('MIXED', 1, 36, (10, 0, 9, 2), False, ()),
 ('MIXED', 1, 37, (10, 0, 10, 1), True, (10, 14)),
 ('MIXED', 1, 38, (10, 0, 9, 4), True, (11,)),
 ('MIXED', 1, 39, (10, 0, 12, 1), True, (14,)),
 ('MIXED', 1, 40, (10, 0, 9, 8), False, ()),
 ('MIXED', 1, 41, (10, 0, 8, 1), True, (10, 14)),
 ('MIXED', 1, 42, (10, 0, 10, 4), True, (10, 11)),
 ('MIXED', 1, 43, (10, 0, 12, 2), False, ()),
 ('MIXED', 1, 44, (10, 0, 10, 8), False, ()),
 ('MIXED', 1, 45, (10, 0, 8, 2), False, ()),
 ('MIXED', 1, 46, (10, 0, 12, 8), False, ()),
 ('MIXED', 1, 47, (10, 0, 8, 4), True, (10, 11)),
 ('MIXED', 2, 0, (10, 1, 1, 0), True, (3, 7, 9, 13)),
 ('MIXED', 2, 1, (10, 1, 2, 0), True, (2, 3, 6, 7)),
 ('MIXED', 2, 2, (10, 1, 4, 0), True, (6, 7, 12, 13)),
 ('MIXED', 2, 3, (10, 1, 8, 0), True, (8, 9, 12, 13)),
 ('MIXED', 3, 0, (10, 0, 1, 2), True, (1, 5)),
 ('MIXED', 3, 1, (10, 0, 2, 1), True, (10, 14)),
 ('MIXED', 3, 2, (10, 0, 1, 4), True, (1, 11)),
 ('MIXED', 3, 3, (10, 0, 4, 1), True, (4, 14)),
 ('MIXED', 3, 4, (10, 0, 1, 8), True, (1, 5)),
 ('MIXED', 3, 5, (10, 0, 8, 1), True, (10, 14)),
 ('MIXED', 3, 6, (10, 0, 2, 4), True, (10, 11)),
 ('MIXED', 3, 7, (10, 0, 4, 2), True, (4, 5)),
 ('MIXED', 3, 8, (10, 0, 2, 8), False, ()),
 ('MIXED', 3, 9, (10, 0, 8, 2), False, ()),
 ('MIXED', 3, 10, (10, 0, 4, 8), True, (4, 5)),
 ('MIXED', 3, 11, (10, 0, 8, 4), True, (10, 11)))

# DOMAINS: instance, j, all_original_U_c_h
DOMAINS = (('Q1', 0, ()),
 ('Q1', 1, ()),
 ('Q1', 2, ()),
 ('Q1', 3, ()),
 ('DOUBLE', 0, ((1, 2, 2), (2, 2, 2))),
 ('DOUBLE', 1, ()),
 ('DOUBLE', 2, ()),
 ('DOUBLE', 3, ()),
 ('UNEQUAL', 0, ((2, 2, 2), (3, 2, 2))),
 ('UNEQUAL', 1, ()),
 ('UNEQUAL', 2, ((3, -4, 2),)),
 ('UNEQUAL', 3, ((1, -2, 2),)),
 ('EQUALITY', 0, ()),
 ('EQUALITY', 1, ()),
 ('EQUALITY', 2, ()),
 ('EQUALITY', 3, ((1, -2, 2), (2, -2, 2), (3, -4, 4), (4, -2, 2), (5, -4, 4), (6, -4, 4))),
 ('WTRI', 0, ((1, 2, 2), (2, 2, 2), (4, 2, 2), (7, 2, 4))),
 ('WTRI', 1, ((3, 2, 2), (5, 2, 2), (6, 2, 2))),
 ('WTRI', 2, ((7, -6, 2),)),
 ('WTRI', 3, ((3, -4, 2), (5, -4, 2), (6, -4, 2))),
 ('ODDFULL', 0, ((4, 2, 2), (5, 4, 2), (6, 4, 2), (7, 4, 2))),
 ('ODDFULL', 1, ()),
 ('ODDFULL', 2, ((5, -2, 2), (6, -2, 2), (7, -6, 4))),
 ('ODDFULL', 3, ((1, -2, 2), (2, -2, 2), (3, -4, 4))),
 ('TIECARD', 0, ()),
 ('TIECARD', 1, ()),
 ('TIECARD', 2, ((5, -2, 2), (6, -2, 2))),
 ('TIECARD', 3, ((3, -2, 2), (4, -2, 2))),
 ('RICH',
  0,
  ((1, 2, 2),
   (2, 2, 2),
   (5, 4, 6),
   (6, 4, 6),
   (9, 4, 2),
   (10, 4, 2),
   (13, 6, 6),
   (14, 6, 6),
   (17, 6, 2),
   (18, 6, 2),
   (21, 6, 6),
   (22, 6, 6),
   (25, 6, 2),
   (26, 6, 2),
   (29, 6, 6),
   (30, 6, 6))),
 ('RICH',
  1,
  ((3, 4, 2),
   (4, 4, 4),
   (7, 2, 6),
   (11, 6, 2),
   (12, 6, 4),
   (15, 4, 6),
   (19, 8, 2),
   (20, 6, 4),
   (23, 4, 6),
   (27, 8, 2),
   (28, 6, 4))),
 ('RICH',
  2,
  ((7, -8, 2),
   (11, 0, 2),
   (13, -4, 2),
   (14, -4, 2),
   (17, 0, 2),
   (18, 0, 2),
   (20, -2, 2),
   (23, -10, 4),
   (24, -2, 2),
   (27, -2, 4),
   (29, -8, 4),
   (30, -8, 4))),
 ('RICH',
  3,
  ((3, -2, 2),
   (5, -6, 2),
   (6, -6, 2),
   (9, -2, 2),
   (10, -2, 2),
   (12, -2, 2),
   (15, -10, 4),
   (16, -2, 2),
   (19, -2, 4),
   (21, -8, 4),
   (22, -8, 4),
   (25, -4, 4),
   (26, -4, 4),
   (28, -6, 4))),
 ('MIXED',
  0,
  ((2, 10, 6),
   (3, 14, 10),
   (6, 18, 14),
   (7, 16, 18),
   (8, 12, 4),
   (9, 18, 8),
   (12, 18, 12),
   (13, 18, 16))),
 ('MIXED', 1, ((1, 6, 4), (4, 14, 8), (5, 16, 12), (10, 18, 8), (11, 20, 12), (14, 16, 16))),
 ('MIXED',
  2,
  ((2, 0, 2),
   (3, -4, 4),
   (6, -8, 6),
   (7, -18, 8),
   (8, 0, 4),
   (9, -2, 6),
   (12, -10, 8),
   (13, -18, 10))),
 ('MIXED', 3, ((1, -2, 2), (4, -2, 4), (5, -8, 6), (10, -6, 8), (11, -12, 10), (14, -24, 12))))

# MINIMA: query, instance, j, A_B, U_c_h_raw_or_None, all_math_argmins, winning_family,
# examined_feasible_parity_ordinary, C_minus_if_built, constant_if_built
MINIMA = (('Q1-j0-p0', 'Q1', 0, (-5, 2), None, (), None, (1, 0, 0, 0), None, None),
 ('Q1-j0-p1', 'Q1', 0, (-2, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('Q1-j0-p2', 'Q1', 0, (-1, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('Q1-j0-p3', 'Q1', 0, (0, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('Q1-j0-p4', 'Q1', 0, (0, 3), None, (), None, (1, 0, 0, 0), None, None),
 ('Q1-j0-p5', 'Q1', 0, (1, 2), None, (), None, (1, 0, 0, 0), None, None),
 ('Q1-j0-p6', 'Q1', 0, (1, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('Q1-j0-p7', 'Q1', 0, (2, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('Q1-j0-p8', 'Q1', 0, (3, 2), None, (), None, (1, 0, 0, 0), None, None),
 ('Q1-j0-p9', 'Q1', 0, (7, 3), None, (), None, (1, 0, 0, 0), None, None),
 ('Q1-j1-p0', 'Q1', 1, (-5, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j1-p1', 'Q1', 1, (-2, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j1-p2', 'Q1', 1, (-1, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j1-p3', 'Q1', 1, (0, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j1-p4', 'Q1', 1, (0, 3), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j1-p5', 'Q1', 1, (1, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j1-p6', 'Q1', 1, (1, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j1-p7', 'Q1', 1, (2, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j1-p8', 'Q1', 1, (3, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j1-p9', 'Q1', 1, (7, 3), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j2-p0', 'Q1', 2, (-5, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j2-p1', 'Q1', 2, (-2, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j2-p2', 'Q1', 2, (-1, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j2-p3', 'Q1', 2, (0, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j2-p4', 'Q1', 2, (0, 3), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j2-p5', 'Q1', 2, (1, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j2-p6', 'Q1', 2, (1, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j2-p7', 'Q1', 2, (2, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j2-p8', 'Q1', 2, (3, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j2-p9', 'Q1', 2, (7, 3), None, (), None, (0, 0, 0, 0), None, None),
 ('Q1-j3-p0', 'Q1', 3, (-5, 2), None, (), None, (2, 0, 0, 0), None, None),
 ('Q1-j3-p1', 'Q1', 3, (-2, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('Q1-j3-p2', 'Q1', 3, (-1, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('Q1-j3-p3', 'Q1', 3, (0, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('Q1-j3-p4', 'Q1', 3, (0, 3), None, (), None, (2, 0, 0, 0), None, None),
 ('Q1-j3-p5', 'Q1', 3, (1, 2), None, (), None, (2, 0, 0, 0), None, None),
 ('Q1-j3-p6', 'Q1', 3, (1, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('Q1-j3-p7', 'Q1', 3, (2, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('Q1-j3-p8', 'Q1', 3, (3, 2), None, (), None, (2, 0, 0, 0), None, None),
 ('Q1-j3-p9', 'Q1', 3, (7, 3), None, (), None, (2, 0, 0, 0), None, None),
 ('DOUBLE-j0-p0', 'DOUBLE', 0, (-5, 2), (1, 2, 2, 14), (1, 2), 0, (1, 1, 1, 7), 0, 3),
 ('DOUBLE-j0-p1', 'DOUBLE', 0, (-2, 1), (1, 2, 2, 6), (1, 2), 0, (1, 1, 1, 7), 0, 1),
 ('DOUBLE-j0-p2', 'DOUBLE', 0, (-1, 1), (1, 2, 2, 4), (1, 2), 0, (1, 1, 1, 7), 0, 0),
 ('DOUBLE-j0-p3', 'DOUBLE', 0, (0, 1), (1, 2, 2, 2), (1, 2), 0, (1, 1, 1, 7), 0, -1),
 ('DOUBLE-j0-p4', 'DOUBLE', 0, (0, 3), (1, 2, 2, 6), (1, 2), 0, (1, 1, 1, 7), 0, -3),
 ('DOUBLE-j0-p5', 'DOUBLE', 0, (1, 2), (1, 2, 2, 2), (1, 2), 0, (1, 1, 1, 7), 0, -3),
 ('DOUBLE-j0-p6', 'DOUBLE', 0, (1, 1), (1, 2, 2, 0), (1, 2), 0, (1, 1, 1, 7), 0, -2),
 ('DOUBLE-j0-p7', 'DOUBLE', 0, (2, 1), (1, 2, 2, -2), (1, 2), 0, (1, 1, 1, 7), 2, -3),
 ('DOUBLE-j0-p8', 'DOUBLE', 0, (3, 2), (1, 2, 2, -2), (1, 2), 0, (1, 1, 1, 7), 2, -5),
 ('DOUBLE-j0-p9', 'DOUBLE', 0, (7, 3), (1, 2, 2, -8), (1, 2), 0, (1, 1, 1, 7), 8, -10),
 ('DOUBLE-j1-p0', 'DOUBLE', 1, (-5, 2), None, (), None, (4, 0, 0, 0), None, None),
 ('DOUBLE-j1-p1', 'DOUBLE', 1, (-2, 1), None, (), None, (4, 0, 0, 0), None, None),
 ('DOUBLE-j1-p2', 'DOUBLE', 1, (-1, 1), None, (), None, (4, 0, 0, 0), None, None),
 ('DOUBLE-j1-p3', 'DOUBLE', 1, (0, 1), None, (), None, (4, 0, 0, 0), None, None),
 ('DOUBLE-j1-p4', 'DOUBLE', 1, (0, 3), None, (), None, (4, 0, 0, 0), None, None),
 ('DOUBLE-j1-p5', 'DOUBLE', 1, (1, 2), None, (), None, (4, 0, 0, 0), None, None),
 ('DOUBLE-j1-p6', 'DOUBLE', 1, (1, 1), None, (), None, (4, 0, 0, 0), None, None),
 ('DOUBLE-j1-p7', 'DOUBLE', 1, (2, 1), None, (), None, (4, 0, 0, 0), None, None),
 ('DOUBLE-j1-p8', 'DOUBLE', 1, (3, 2), None, (), None, (4, 0, 0, 0), None, None),
 ('DOUBLE-j1-p9', 'DOUBLE', 1, (7, 3), None, (), None, (4, 0, 0, 0), None, None),
 ('DOUBLE-j2-p0', 'DOUBLE', 2, (-5, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('DOUBLE-j2-p1', 'DOUBLE', 2, (-2, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('DOUBLE-j2-p2', 'DOUBLE', 2, (-1, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('DOUBLE-j2-p3', 'DOUBLE', 2, (0, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('DOUBLE-j2-p4', 'DOUBLE', 2, (0, 3), None, (), None, (0, 0, 0, 0), None, None),
 ('DOUBLE-j2-p5', 'DOUBLE', 2, (1, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('DOUBLE-j2-p6', 'DOUBLE', 2, (1, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('DOUBLE-j2-p7', 'DOUBLE', 2, (2, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('DOUBLE-j2-p8', 'DOUBLE', 2, (3, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('DOUBLE-j2-p9', 'DOUBLE', 2, (7, 3), None, (), None, (0, 0, 0, 0), None, None),
 ('DOUBLE-j3-p0', 'DOUBLE', 3, (-5, 2), None, (), None, (2, 0, 0, 0), None, None),
 ('DOUBLE-j3-p1', 'DOUBLE', 3, (-2, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('DOUBLE-j3-p2', 'DOUBLE', 3, (-1, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('DOUBLE-j3-p3', 'DOUBLE', 3, (0, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('DOUBLE-j3-p4', 'DOUBLE', 3, (0, 3), None, (), None, (2, 0, 0, 0), None, None),
 ('DOUBLE-j3-p5', 'DOUBLE', 3, (1, 2), None, (), None, (2, 0, 0, 0), None, None),
 ('DOUBLE-j3-p6', 'DOUBLE', 3, (1, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('DOUBLE-j3-p7', 'DOUBLE', 3, (2, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('DOUBLE-j3-p8', 'DOUBLE', 3, (3, 2), None, (), None, (2, 0, 0, 0), None, None),
 ('DOUBLE-j3-p9', 'DOUBLE', 3, (7, 3), None, (), None, (2, 0, 0, 0), None, None),
 ('UNEQUAL-j0-p0', 'UNEQUAL', 0, (-5, 2), (2, 2, 2, 14), (2, 3), 0, (1, 1, 1, 7), 0, 3),
 ('UNEQUAL-j0-p1', 'UNEQUAL', 0, (-2, 1), (2, 2, 2, 6), (2, 3), 0, (1, 1, 1, 7), 0, 1),
 ('UNEQUAL-j0-p2', 'UNEQUAL', 0, (-1, 1), (2, 2, 2, 4), (2, 3), 0, (1, 1, 1, 7), 0, 0),
 ('UNEQUAL-j0-p3', 'UNEQUAL', 0, (0, 1), (3, 2, 2, 2), (2, 3), 0, (1, 1, 1, 7), 0, -1),
 ('UNEQUAL-j0-p4', 'UNEQUAL', 0, (0, 3), (3, 2, 2, 6), (2, 3), 0, (1, 1, 1, 7), 0, -3),
 ('UNEQUAL-j0-p5', 'UNEQUAL', 0, (1, 2), (3, 2, 2, 2), (2, 3), 0, (1, 1, 1, 7), 0, -3),
 ('UNEQUAL-j0-p6', 'UNEQUAL', 0, (1, 1), (3, 2, 2, 0), (2, 3), 0, (1, 1, 1, 7), 0, -2),
 ('UNEQUAL-j0-p7', 'UNEQUAL', 0, (2, 1), (3, 2, 2, -2), (2, 3), 0, (1, 1, 1, 7), 1, -3),
 ('UNEQUAL-j0-p8', 'UNEQUAL', 0, (3, 2), (3, 2, 2, -2), (2, 3), 0, (1, 1, 1, 7), 1, -5),
 ('UNEQUAL-j0-p9', 'UNEQUAL', 0, (7, 3), (3, 2, 2, -8), (2, 3), 0, (1, 1, 1, 7), 4, -10),
 ('UNEQUAL-j1-p0', 'UNEQUAL', 1, (-5, 2), None, (), None, (2, 0, 0, 0), None, None),
 ('UNEQUAL-j1-p1', 'UNEQUAL', 1, (-2, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('UNEQUAL-j1-p2', 'UNEQUAL', 1, (-1, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('UNEQUAL-j1-p3', 'UNEQUAL', 1, (0, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('UNEQUAL-j1-p4', 'UNEQUAL', 1, (0, 3), None, (), None, (2, 0, 0, 0), None, None),
 ('UNEQUAL-j1-p5', 'UNEQUAL', 1, (1, 2), None, (), None, (2, 0, 0, 0), None, None),
 ('UNEQUAL-j1-p6', 'UNEQUAL', 1, (1, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('UNEQUAL-j1-p7', 'UNEQUAL', 1, (2, 1), None, (), None, (2, 0, 0, 0), None, None),
 ('UNEQUAL-j1-p8', 'UNEQUAL', 1, (3, 2), None, (), None, (2, 0, 0, 0), None, None),
 ('UNEQUAL-j1-p9', 'UNEQUAL', 1, (7, 3), None, (), None, (2, 0, 0, 0), None, None),
 ('UNEQUAL-j2-p0', 'UNEQUAL', 2, (-5, 2), (3, -4, 2, 2), (3,), 0, (1, 1, 1, 3), 0, -5),
 ('UNEQUAL-j2-p1', 'UNEQUAL', 2, (-2, 1), (3, -4, 2, 0), (3,), 0, (1, 1, 1, 3), 0, -2),
 ('UNEQUAL-j2-p2', 'UNEQUAL', 2, (-1, 1), (3, -4, 2, -2), (3,), 0, (1, 1, 1, 3), 1, -1),
 ('UNEQUAL-j2-p3', 'UNEQUAL', 2, (0, 1), (3, -4, 2, -4), (3,), 0, (1, 1, 1, 3), 4, 0),
 ('UNEQUAL-j2-p4', 'UNEQUAL', 2, (0, 3), (3, -4, 2, -12), (3,), 0, (1, 1, 1, 3), 12, 0),
 ('UNEQUAL-j2-p5', 'UNEQUAL', 2, (1, 2), (3, -4, 2, -10), (3,), 0, (1, 1, 1, 3), 11, 1),
 ('UNEQUAL-j2-p6', 'UNEQUAL', 2, (1, 1), (3, -4, 2, -6), (3,), 0, (1, 1, 1, 3), 7, 1),
 ('UNEQUAL-j2-p7', 'UNEQUAL', 2, (2, 1), (3, -4, 2, -8), (3,), 0, (1, 1, 1, 3), 10, 2),
 ('UNEQUAL-j2-p8', 'UNEQUAL', 2, (3, 2), (3, -4, 2, -14), (3,), 0, (1, 1, 1, 3), 17, 3),
 ('UNEQUAL-j2-p9', 'UNEQUAL', 2, (7, 3), (3, -4, 2, -26), (3,), 0, (1, 1, 1, 3), 33, 7),
 ('UNEQUAL-j3-p0', 'UNEQUAL', 3, (-5, 2), (1, -2, 2, 6), (1,), 0, (2, 1, 1, 1), 0, -4),
 ('UNEQUAL-j3-p1', 'UNEQUAL', 3, (-2, 1), (1, -2, 2, 2), (1,), 0, (2, 1, 1, 1), 0, -2),
 ('UNEQUAL-j3-p2', 'UNEQUAL', 3, (-1, 1), (1, -2, 2, 0), (1,), 0, (2, 1, 1, 1), 1, -2),
 ('UNEQUAL-j3-p3', 'UNEQUAL', 3, (0, 1), (1, -2, 2, -2), (1,), 0, (2, 1, 1, 1), 4, -2),
 ('UNEQUAL-j3-p4', 'UNEQUAL', 3, (0, 3), (1, -2, 2, -6), (1,), 0, (2, 1, 1, 1), 12, -6),
 ('UNEQUAL-j3-p5', 'UNEQUAL', 3, (1, 2), (1, -2, 2, -6), (1,), 0, (2, 1, 1, 1), 11, -4),
 ('UNEQUAL-j3-p6', 'UNEQUAL', 3, (1, 1), (1, -2, 2, -4), (1,), 0, (2, 1, 1, 1), 7, -2),
 ('UNEQUAL-j3-p7', 'UNEQUAL', 3, (2, 1), (1, -2, 2, -6), (1,), 0, (2, 1, 1, 1), 10, -2),
 ('UNEQUAL-j3-p8', 'UNEQUAL', 3, (3, 2), (1, -2, 2, -10), (1,), 0, (2, 1, 1, 1), 17, -4),
 ('UNEQUAL-j3-p9', 'UNEQUAL', 3, (7, 3), (1, -2, 2, -20), (1,), 0, (2, 1, 1, 1), 33, -6),
 ('EQUALITY-j0-p0', 'EQUALITY', 0, (-5, 2), None, (), None, (1, 0, 0, 0), None, None),
 ('EQUALITY-j0-p1', 'EQUALITY', 0, (-2, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('EQUALITY-j0-p2', 'EQUALITY', 0, (-1, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('EQUALITY-j0-p3', 'EQUALITY', 0, (0, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('EQUALITY-j0-p4', 'EQUALITY', 0, (0, 3), None, (), None, (1, 0, 0, 0), None, None),
 ('EQUALITY-j0-p5', 'EQUALITY', 0, (1, 2), None, (), None, (1, 0, 0, 0), None, None),
 ('EQUALITY-j0-p6', 'EQUALITY', 0, (1, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('EQUALITY-j0-p7', 'EQUALITY', 0, (2, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('EQUALITY-j0-p8', 'EQUALITY', 0, (3, 2), None, (), None, (1, 0, 0, 0), None, None),
 ('EQUALITY-j0-p9', 'EQUALITY', 0, (7, 3), None, (), None, (1, 0, 0, 0), None, None),
 ('EQUALITY-j1-p0', 'EQUALITY', 1, (-5, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('EQUALITY-j1-p1', 'EQUALITY', 1, (-2, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('EQUALITY-j1-p2', 'EQUALITY', 1, (-1, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('EQUALITY-j1-p3', 'EQUALITY', 1, (0, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('EQUALITY-j1-p4', 'EQUALITY', 1, (0, 3), None, (), None, (0, 0, 0, 0), None, None),
 ('EQUALITY-j1-p5', 'EQUALITY', 1, (1, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('EQUALITY-j1-p6', 'EQUALITY', 1, (1, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('EQUALITY-j1-p7', 'EQUALITY', 1, (2, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('EQUALITY-j1-p8', 'EQUALITY', 1, (3, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('EQUALITY-j1-p9', 'EQUALITY', 1, (7, 3), None, (), None, (0, 0, 0, 0), None, None),
 ('EQUALITY-j2-p0', 'EQUALITY', 2, (-5, 2), None, (), None, (3, 0, 0, 0), None, None),
 ('EQUALITY-j2-p1', 'EQUALITY', 2, (-2, 1), None, (), None, (3, 0, 0, 0), None, None),
 ('EQUALITY-j2-p2', 'EQUALITY', 2, (-1, 1), None, (), None, (3, 0, 0, 0), None, None),
 ('EQUALITY-j2-p3', 'EQUALITY', 2, (0, 1), None, (), None, (3, 0, 0, 0), None, None),
 ('EQUALITY-j2-p4', 'EQUALITY', 2, (0, 3), None, (), None, (3, 0, 0, 0), None, None),
 ('EQUALITY-j2-p5', 'EQUALITY', 2, (1, 2), None, (), None, (3, 0, 0, 0), None, None),
 ('EQUALITY-j2-p6', 'EQUALITY', 2, (1, 1), None, (), None, (3, 0, 0, 0), None, None),
 ('EQUALITY-j2-p7', 'EQUALITY', 2, (2, 1), None, (), None, (3, 0, 0, 0), None, None),
 ('EQUALITY-j2-p8', 'EQUALITY', 2, (3, 2), None, (), None, (3, 0, 0, 0), None, None),
 ('EQUALITY-j2-p9', 'EQUALITY', 2, (7, 3), None, (), None, (3, 0, 0, 0), None, None),
 ('EQUALITY-j3-p0', 'EQUALITY', 3, (-5, 2), (1, -2, 2, 6), (1, 2, 4), 0, (6, 6, 6, 18), 0, -4),
 ('EQUALITY-j3-p1', 'EQUALITY', 3, (-2, 1), (1, -2, 2, 2), (1, 2, 4), 0, (6, 6, 6, 18), 0, -2),
 ('EQUALITY-j3-p2',
  'EQUALITY',
  3,
  (-1, 1),
  (1, -2, 2, 0),
  (1, 2, 3, 4, 5, 6),
  0,
  (6, 6, 6, 18),
  0,
  -2),
 ('EQUALITY-j3-p3', 'EQUALITY', 3, (0, 1), (5, -4, 4, -4), (3, 5, 6), 0, (6, 6, 6, 18), 6, -2),
 ('EQUALITY-j3-p4',
  'EQUALITY',
  3,
  (0, 3),
  (5, -4, 4, -12),
  (3, 5, 6),
  0,
  (6, 6, 6, 18),
  18,
  -6),
 ('EQUALITY-j3-p5',
  'EQUALITY',
  3,
  (1, 2),
  (5, -4, 4, -12),
  (3, 5, 6),
  0,
  (6, 6, 6, 18),
  18,
  -4),
 ('EQUALITY-j3-p6', 'EQUALITY', 3, (1, 1), (5, -4, 4, -8), (3, 5, 6), 0, (6, 6, 6, 18), 12, -2),
 ('EQUALITY-j3-p7',
  'EQUALITY',
  3,
  (2, 1),
  (5, -4, 4, -12),
  (3, 5, 6),
  0,
  (6, 6, 6, 18),
  18,
  -2),
 ('EQUALITY-j3-p8',
  'EQUALITY',
  3,
  (3, 2),
  (5, -4, 4, -20),
  (3, 5, 6),
  0,
  (6, 6, 6, 18),
  30,
  -4),
 ('EQUALITY-j3-p9',
  'EQUALITY',
  3,
  (7, 3),
  (5, -4, 4, -40),
  (3, 5, 6),
  0,
  (6, 6, 6, 18),
  60,
  -6),
 ('WTRI-j0-p0', 'WTRI', 0, (-5, 2), (1, 2, 2, 14), (1, 2, 4), 0, (1, 1, 1, 13), 0, 3),
 ('WTRI-j0-p1', 'WTRI', 0, (-2, 1), (1, 2, 2, 6), (1, 2, 4), 0, (1, 1, 1, 13), 0, 1),
 ('WTRI-j0-p2', 'WTRI', 0, (-1, 1), (1, 2, 2, 4), (1, 2, 4), 0, (1, 1, 1, 13), 0, 0),
 ('WTRI-j0-p3', 'WTRI', 0, (0, 1), (1, 2, 2, 2), (1, 2, 4, 7), 0, (1, 1, 1, 13), 0, -1),
 ('WTRI-j0-p4', 'WTRI', 0, (0, 3), (1, 2, 2, 6), (1, 2, 4, 7), 0, (1, 1, 1, 13), 0, -3),
 ('WTRI-j0-p5', 'WTRI', 0, (1, 2), (7, 2, 4, 0), (7,), 0, (1, 1, 1, 13), 0, -3),
 ('WTRI-j0-p6', 'WTRI', 0, (1, 1), (7, 2, 4, -2), (7,), 0, (1, 1, 1, 13), 0, -2),
 ('WTRI-j0-p7', 'WTRI', 0, (2, 1), (7, 2, 4, -6), (7,), 0, (1, 1, 1, 13), 3, -3),
 ('WTRI-j0-p8', 'WTRI', 0, (3, 2), (7, 2, 4, -8), (7,), 0, (1, 1, 1, 13), 3, -5),
 ('WTRI-j0-p9', 'WTRI', 0, (7, 3), (7, 2, 4, -22), (7,), 0, (1, 1, 1, 13), 12, -10),
 ('WTRI-j1-p0', 'WTRI', 1, (-5, 2), (5, 2, 2, 14), (3, 5, 6), 0, (18, 12, 12, 24), 0, -4),
 ('WTRI-j1-p1', 'WTRI', 1, (-2, 1), (5, 2, 2, 6), (3, 5, 6), 0, (18, 12, 12, 24), 0, -2),
 ('WTRI-j1-p2', 'WTRI', 1, (-1, 1), (5, 2, 2, 4), (3, 5, 6), 0, (18, 12, 12, 24), 0, -2),
 ('WTRI-j1-p3', 'WTRI', 1, (0, 1), (5, 2, 2, 2), (3, 5, 6), 0, (18, 12, 12, 24), 0, -2),
 ('WTRI-j1-p4', 'WTRI', 1, (0, 3), (5, 2, 2, 6), (3, 5, 6), 0, (18, 12, 12, 24), 0, -6),
 ('WTRI-j1-p5', 'WTRI', 1, (1, 2), (5, 2, 2, 2), (3, 5, 6), 0, (18, 12, 12, 24), 0, -4),
 ('WTRI-j1-p6', 'WTRI', 1, (1, 1), (5, 2, 2, 0), (3, 5, 6), 0, (18, 12, 12, 24), 0, -2),
 ('WTRI-j1-p7', 'WTRI', 1, (2, 1), (5, 2, 2, -2), (3, 5, 6), 0, (18, 12, 12, 24), 3, -2),
 ('WTRI-j1-p8', 'WTRI', 1, (3, 2), (5, 2, 2, -2), (3, 5, 6), 0, (18, 12, 12, 24), 3, -4),
 ('WTRI-j1-p9', 'WTRI', 1, (7, 3), (5, 2, 2, -8), (3, 5, 6), 0, (18, 12, 12, 24), 12, -6),
 ('WTRI-j2-p0', 'WTRI', 2, (-5, 2), (7, -6, 2, -2), (7,), 0, (1, 1, 1, 1), 0, -5),
 ('WTRI-j2-p1', 'WTRI', 2, (-2, 1), (7, -6, 2, -2), (7,), 0, (1, 1, 1, 1), 0, -2),
 ('WTRI-j2-p2', 'WTRI', 2, (-1, 1), (7, -6, 2, -4), (7,), 0, (1, 1, 1, 1), 3, -1),
 ('WTRI-j2-p3', 'WTRI', 2, (0, 1), (7, -6, 2, -6), (7,), 0, (1, 1, 1, 1), 6, 0),
 ('WTRI-j2-p4', 'WTRI', 2, (0, 3), (7, -6, 2, -18), (7,), 0, (1, 1, 1, 1), 18, 0),
 ('WTRI-j2-p5', 'WTRI', 2, (1, 2), (7, -6, 2, -14), (7,), 0, (1, 1, 1, 1), 15, 1),
 ('WTRI-j2-p6', 'WTRI', 2, (1, 1), (7, -6, 2, -8), (7,), 0, (1, 1, 1, 1), 9, 1),
 ('WTRI-j2-p7', 'WTRI', 2, (2, 1), (7, -6, 2, -10), (7,), 0, (1, 1, 1, 1), 12, 2),
 ('WTRI-j2-p8', 'WTRI', 2, (3, 2), (7, -6, 2, -18), (7,), 0, (1, 1, 1, 1), 21, 3),
 ('WTRI-j2-p9', 'WTRI', 2, (7, 3), (7, -6, 2, -32), (7,), 0, (1, 1, 1, 1), 39, 7),
 ('WTRI-j3-p0', 'WTRI', 3, (-5, 2), (5, -4, 2, 2), (3, 5, 6), 0, (6, 6, 6, 18), 0, -4),
 ('WTRI-j3-p1', 'WTRI', 3, (-2, 1), (5, -4, 2, 0), (3, 5, 6), 0, (6, 6, 6, 18), 0, -2),
 ('WTRI-j3-p2', 'WTRI', 3, (-1, 1), (5, -4, 2, -2), (3, 5, 6), 0, (6, 6, 6, 18), 3, -2),
 ('WTRI-j3-p3', 'WTRI', 3, (0, 1), (5, -4, 2, -4), (3, 5, 6), 0, (6, 6, 6, 18), 6, -2),
 ('WTRI-j3-p4', 'WTRI', 3, (0, 3), (5, -4, 2, -12), (3, 5, 6), 0, (6, 6, 6, 18), 18, -6),
 ('WTRI-j3-p5', 'WTRI', 3, (1, 2), (5, -4, 2, -10), (3, 5, 6), 0, (6, 6, 6, 18), 15, -4),
 ('WTRI-j3-p6', 'WTRI', 3, (1, 1), (5, -4, 2, -6), (3, 5, 6), 0, (6, 6, 6, 18), 9, -2),
 ('WTRI-j3-p7', 'WTRI', 3, (2, 1), (5, -4, 2, -8), (3, 5, 6), 0, (6, 6, 6, 18), 12, -2),
 ('WTRI-j3-p8', 'WTRI', 3, (3, 2), (5, -4, 2, -14), (3, 5, 6), 0, (6, 6, 6, 18), 21, -4),
 ('WTRI-j3-p9', 'WTRI', 3, (7, 3), (5, -4, 2, -26), (3, 5, 6), 0, (6, 6, 6, 18), 39, -6),
 ('ODDFULL-j0-p0', 'ODDFULL', 0, (-5, 2), (4, 2, 2, 14), (4,), 0, (1, 1, 1, 13), 0, 3),
 ('ODDFULL-j0-p1', 'ODDFULL', 0, (-2, 1), (4, 2, 2, 6), (4,), 0, (1, 1, 1, 13), 0, 1),
 ('ODDFULL-j0-p2', 'ODDFULL', 0, (-1, 1), (4, 2, 2, 4), (4,), 0, (1, 1, 1, 13), 0, 0),
 ('ODDFULL-j0-p3', 'ODDFULL', 0, (0, 1), (4, 2, 2, 2), (4,), 0, (1, 1, 1, 13), 0, -1),
 ('ODDFULL-j0-p4', 'ODDFULL', 0, (0, 3), (4, 2, 2, 6), (4,), 0, (1, 1, 1, 13), 0, -3),
 ('ODDFULL-j0-p5', 'ODDFULL', 0, (1, 2), (4, 2, 2, 2), (4,), 0, (1, 1, 1, 13), 0, -3),
 ('ODDFULL-j0-p6', 'ODDFULL', 0, (1, 1), (4, 2, 2, 0), (4,), 0, (1, 1, 1, 13), 0, -2),
 ('ODDFULL-j0-p7', 'ODDFULL', 0, (2, 1), (4, 2, 2, -2), (4,), 0, (1, 1, 1, 13), 1, -3),
 ('ODDFULL-j0-p8', 'ODDFULL', 0, (3, 2), (4, 2, 2, -2), (4,), 0, (1, 1, 1, 13), 1, -5),
 ('ODDFULL-j0-p9', 'ODDFULL', 0, (7, 3), (4, 2, 2, -8), (4,), 0, (1, 1, 1, 13), 4, -10),
 ('ODDFULL-j1-p0', 'ODDFULL', 1, (-5, 2), None, (), None, (6, 0, 0, 0), None, None),
 ('ODDFULL-j1-p1', 'ODDFULL', 1, (-2, 1), None, (), None, (6, 0, 0, 0), None, None),
 ('ODDFULL-j1-p2', 'ODDFULL', 1, (-1, 1), None, (), None, (6, 0, 0, 0), None, None),
 ('ODDFULL-j1-p3', 'ODDFULL', 1, (0, 1), None, (), None, (6, 0, 0, 0), None, None),
 ('ODDFULL-j1-p4', 'ODDFULL', 1, (0, 3), None, (), None, (6, 0, 0, 0), None, None),
 ('ODDFULL-j1-p5', 'ODDFULL', 1, (1, 2), None, (), None, (6, 0, 0, 0), None, None),
 ('ODDFULL-j1-p6', 'ODDFULL', 1, (1, 1), None, (), None, (6, 0, 0, 0), None, None),
 ('ODDFULL-j1-p7', 'ODDFULL', 1, (2, 1), None, (), None, (6, 0, 0, 0), None, None),
 ('ODDFULL-j1-p8', 'ODDFULL', 1, (3, 2), None, (), None, (6, 0, 0, 0), None, None),
 ('ODDFULL-j1-p9', 'ODDFULL', 1, (7, 3), None, (), None, (6, 0, 0, 0), None, None),
 ('ODDFULL-j2-p0', 'ODDFULL', 2, (-5, 2), (5, -2, 2, 6), (5, 6), 0, (2, 2, 2, 14), 0, -5),
 ('ODDFULL-j2-p1', 'ODDFULL', 2, (-2, 1), (7, -6, 4, 2), (5, 6, 7), 0, (2, 2, 2, 14), 0, -2),
 ('ODDFULL-j2-p2', 'ODDFULL', 2, (-1, 1), (7, -6, 4, -2), (7,), 0, (2, 2, 2, 14), 1, -1),
 ('ODDFULL-j2-p3', 'ODDFULL', 2, (0, 1), (7, -6, 4, -6), (7,), 0, (2, 2, 2, 14), 6, 0),
 ('ODDFULL-j2-p4', 'ODDFULL', 2, (0, 3), (7, -6, 4, -18), (7,), 0, (2, 2, 2, 14), 18, 0),
 ('ODDFULL-j2-p5', 'ODDFULL', 2, (1, 2), (7, -6, 4, -16), (7,), 0, (2, 2, 2, 14), 17, 1),
 ('ODDFULL-j2-p6', 'ODDFULL', 2, (1, 1), (7, -6, 4, -10), (7,), 0, (2, 2, 2, 14), 11, 1),
 ('ODDFULL-j2-p7', 'ODDFULL', 2, (2, 1), (7, -6, 4, -14), (7,), 0, (2, 2, 2, 14), 16, 2),
 ('ODDFULL-j2-p8', 'ODDFULL', 2, (3, 2), (7, -6, 4, -24), (7,), 0, (2, 2, 2, 14), 27, 3),
 ('ODDFULL-j2-p9', 'ODDFULL', 2, (7, 3), (7, -6, 4, -46), (7,), 0, (2, 2, 2, 14), 53, 7),
 ('ODDFULL-j3-p0', 'ODDFULL', 3, (-5, 2), (1, -2, 2, 6), (1, 2), 0, (6, 4, 4, 12), 0, -4),
 ('ODDFULL-j3-p1', 'ODDFULL', 3, (-2, 1), (1, -2, 2, 2), (1, 2), 0, (6, 4, 4, 12), 0, -2),
 ('ODDFULL-j3-p2', 'ODDFULL', 3, (-1, 1), (1, -2, 2, 0), (1, 2, 3), 0, (6, 4, 4, 12), 1, -2),
 ('ODDFULL-j3-p3', 'ODDFULL', 3, (0, 1), (3, -4, 4, -4), (3,), 2, (6, 4, 4, 12), 6, -2),
 ('ODDFULL-j3-p4', 'ODDFULL', 3, (0, 3), (3, -4, 4, -12), (3,), 2, (6, 4, 4, 12), 18, -6),
 ('ODDFULL-j3-p5', 'ODDFULL', 3, (1, 2), (3, -4, 4, -12), (3,), 2, (6, 4, 4, 12), 17, -4),
 ('ODDFULL-j3-p6', 'ODDFULL', 3, (1, 1), (3, -4, 4, -8), (3,), 2, (6, 4, 4, 12), 11, -2),
 ('ODDFULL-j3-p7', 'ODDFULL', 3, (2, 1), (3, -4, 4, -12), (3,), 2, (6, 4, 4, 12), 16, -2),
 ('ODDFULL-j3-p8', 'ODDFULL', 3, (3, 2), (3, -4, 4, -20), (3,), 2, (6, 4, 4, 12), 27, -4),
 ('ODDFULL-j3-p9', 'ODDFULL', 3, (7, 3), (3, -4, 4, -40), (3,), 2, (6, 4, 4, 12), 53, -6),
 ('TIECARD-j0-p0', 'TIECARD', 0, (-5, 2), None, (), None, (1, 0, 0, 0), None, None),
 ('TIECARD-j0-p1', 'TIECARD', 0, (-2, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('TIECARD-j0-p2', 'TIECARD', 0, (-1, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('TIECARD-j0-p3', 'TIECARD', 0, (0, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('TIECARD-j0-p4', 'TIECARD', 0, (0, 3), None, (), None, (1, 0, 0, 0), None, None),
 ('TIECARD-j0-p5', 'TIECARD', 0, (1, 2), None, (), None, (1, 0, 0, 0), None, None),
 ('TIECARD-j0-p6', 'TIECARD', 0, (1, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('TIECARD-j0-p7', 'TIECARD', 0, (2, 1), None, (), None, (1, 0, 0, 0), None, None),
 ('TIECARD-j0-p8', 'TIECARD', 0, (3, 2), None, (), None, (1, 0, 0, 0), None, None),
 ('TIECARD-j0-p9', 'TIECARD', 0, (7, 3), None, (), None, (1, 0, 0, 0), None, None),
 ('TIECARD-j1-p0', 'TIECARD', 1, (-5, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('TIECARD-j1-p1', 'TIECARD', 1, (-2, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('TIECARD-j1-p2', 'TIECARD', 1, (-1, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('TIECARD-j1-p3', 'TIECARD', 1, (0, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('TIECARD-j1-p4', 'TIECARD', 1, (0, 3), None, (), None, (0, 0, 0, 0), None, None),
 ('TIECARD-j1-p5', 'TIECARD', 1, (1, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('TIECARD-j1-p6', 'TIECARD', 1, (1, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('TIECARD-j1-p7', 'TIECARD', 1, (2, 1), None, (), None, (0, 0, 0, 0), None, None),
 ('TIECARD-j1-p8', 'TIECARD', 1, (3, 2), None, (), None, (0, 0, 0, 0), None, None),
 ('TIECARD-j1-p9', 'TIECARD', 1, (7, 3), None, (), None, (0, 0, 0, 0), None, None),
 ('TIECARD-j2-p0', 'TIECARD', 2, (-5, 2), (5, -2, 2, 6), (5, 6), 0, (1, 1, 1, 7), 0, -5),
 ('TIECARD-j2-p1', 'TIECARD', 2, (-2, 1), (5, -2, 2, 2), (5, 6), 0, (1, 1, 1, 7), 0, -2),
 ('TIECARD-j2-p2', 'TIECARD', 2, (-1, 1), (6, -2, 2, 0), (5, 6), 0, (1, 1, 1, 7), 0, -1),
 ('TIECARD-j2-p3', 'TIECARD', 2, (0, 1), (6, -2, 2, -2), (5, 6), 0, (1, 1, 1, 7), 4, 0),
 ('TIECARD-j2-p4', 'TIECARD', 2, (0, 3), (6, -2, 2, -6), (5, 6), 0, (1, 1, 1, 7), 12, 0),
 ('TIECARD-j2-p5', 'TIECARD', 2, (1, 2), (6, -2, 2, -6), (5, 6), 0, (1, 1, 1, 7), 12, 1),
 ('TIECARD-j2-p6', 'TIECARD', 2, (1, 1), (6, -2, 2, -4), (5, 6), 0, (1, 1, 1, 7), 8, 1),
 ('TIECARD-j2-p7', 'TIECARD', 2, (2, 1), (6, -2, 2, -6), (5, 6), 0, (1, 1, 1, 7), 12, 2),
 ('TIECARD-j2-p8', 'TIECARD', 2, (3, 2), (6, -2, 2, -10), (5, 6), 0, (1, 1, 1, 7), 20, 3),
 ('TIECARD-j2-p9', 'TIECARD', 2, (7, 3), (6, -2, 2, -20), (5, 6), 0, (1, 1, 1, 7), 40, 7),
 ('TIECARD-j3-p0', 'TIECARD', 3, (-5, 2), (3, -2, 2, 6), (3, 4), 0, (4, 4, 4, 12), 0, -4),
 ('TIECARD-j3-p1', 'TIECARD', 3, (-2, 1), (3, -2, 2, 2), (3, 4), 0, (4, 4, 4, 12), 0, -2),
 ('TIECARD-j3-p2', 'TIECARD', 3, (-1, 1), (3, -2, 2, 0), (3, 4), 0, (4, 4, 4, 12), 0, -2),
 ('TIECARD-j3-p3', 'TIECARD', 3, (0, 1), (3, -2, 2, -2), (3, 4), 0, (4, 4, 4, 12), 4, -2),
 ('TIECARD-j3-p4', 'TIECARD', 3, (0, 3), (3, -2, 2, -6), (3, 4), 0, (4, 4, 4, 12), 12, -6),
 ('TIECARD-j3-p5', 'TIECARD', 3, (1, 2), (3, -2, 2, -6), (3, 4), 0, (4, 4, 4, 12), 12, -4),
 ('TIECARD-j3-p6', 'TIECARD', 3, (1, 1), (3, -2, 2, -4), (3, 4), 0, (4, 4, 4, 12), 8, -2),
 ('TIECARD-j3-p7', 'TIECARD', 3, (2, 1), (3, -2, 2, -6), (3, 4), 0, (4, 4, 4, 12), 12, -2),
 ('TIECARD-j3-p8', 'TIECARD', 3, (3, 2), (3, -2, 2, -10), (3, 4), 0, (4, 4, 4, 12), 20, -4),
 ('TIECARD-j3-p9', 'TIECARD', 3, (7, 3), (3, -2, 2, -20), (3, 4), 0, (4, 4, 4, 12), 40, -6),
 ('RICH-j0-p0', 'RICH', 0, (-5, 2), (1, 2, 2, 14), (1, 2), 0, (1, 1, 1, 31), 0, 3),
 ('RICH-j0-p1', 'RICH', 0, (-2, 1), (1, 2, 2, 6), (1, 2), 0, (1, 1, 1, 31), 0, 1),
 ('RICH-j0-p2', 'RICH', 0, (-1, 1), (1, 2, 2, 4), (1, 2), 0, (1, 1, 1, 31), 0, 0),
 ('RICH-j0-p3', 'RICH', 0, (0, 1), (1, 2, 2, 2), (1, 2), 0, (1, 1, 1, 31), 0, -1),
 ('RICH-j0-p4', 'RICH', 0, (0, 3), (1, 2, 2, 6), (1, 2), 0, (1, 1, 1, 31), 0, -3),
 ('RICH-j0-p5', 'RICH', 0, (1, 2), (1, 2, 2, 2), (1, 2, 5, 6), 0, (1, 1, 1, 31), 2, -3),
 ('RICH-j0-p6', 'RICH', 0, (1, 1), (5, 4, 6, -2), (5, 6), 0, (1, 1, 1, 31), 3, -2),
 ('RICH-j0-p7', 'RICH', 0, (2, 1), (6, 4, 6, -8), (5, 6), 0, (1, 1, 1, 31), 9, -3),
 ('RICH-j0-p8', 'RICH', 0, (3, 2), (6, 4, 6, -10), (5, 6), 0, (1, 1, 1, 31), 12, -5),
 ('RICH-j0-p9', 'RICH', 0, (7, 3), (6, 4, 6, -30), (5, 6), 0, (1, 1, 1, 31), 33, -10),
 ('RICH-j1-p0', 'RICH', 1, (-5, 2), (3, 4, 2, 18), (3,), 0, (24, 17, 17, 149), 0, -4),
 ('RICH-j1-p1', 'RICH', 1, (-2, 1), (3, 4, 2, 8), (3,), 0, (24, 17, 17, 149), 0, -2),
 ('RICH-j1-p2', 'RICH', 1, (-1, 1), (3, 4, 2, 6), (3,), 0, (24, 17, 17, 149), 0, -2),
 ('RICH-j1-p3', 'RICH', 1, (0, 1), (7, 2, 6, 2), (7,), 4, (24, 17, 17, 149), 0, -2),
 ('RICH-j1-p4', 'RICH', 1, (0, 3), (7, 2, 6, 6), (7,), 4, (24, 17, 17, 149), 0, -6),
 ('RICH-j1-p5', 'RICH', 1, (1, 2), (7, 2, 6, -2), (7,), 4, (24, 17, 17, 149), 2, -4),
 ('RICH-j1-p6', 'RICH', 1, (1, 1), (7, 2, 6, -4), (7,), 4, (24, 17, 17, 149), 3, -2),
 ('RICH-j1-p7', 'RICH', 1, (2, 1), (7, 2, 6, -10), (7,), 4, (24, 17, 17, 149), 9, -2),
 ('RICH-j1-p8', 'RICH', 1, (3, 2), (7, 2, 6, -14), (7,), 4, (24, 17, 17, 149), 12, -4),
 ('RICH-j1-p9', 'RICH', 1, (7, 3), (7, 2, 6, -36), (7,), 4, (24, 17, 17, 149), 33, -6),
 ('RICH-j2-p0', 'RICH', 2, (-5, 2), (7, -8, 2, -6), (7,), 1, (5, 5, 5, 49), 5, -5),
 ('RICH-j2-p1', 'RICH', 2, (-2, 1), (7, -8, 2, -4), (7,), 1, (5, 5, 5, 49), 3, -2),
 ('RICH-j2-p2', 'RICH', 2, (-1, 1), (23, -10, 4, -6), (7, 23), 0, (5, 5, 5, 49), 6, -1),
 ('RICH-j2-p3', 'RICH', 2, (0, 1), (23, -10, 4, -10), (23,), 0, (5, 5, 5, 49), 12, 0),
 ('RICH-j2-p4', 'RICH', 2, (0, 3), (23, -10, 4, -30), (23,), 0, (5, 5, 5, 49), 36, 0),
 ('RICH-j2-p5', 'RICH', 2, (1, 2), (23, -10, 4, -24), (23,), 0, (5, 5, 5, 49), 30, 1),
 ('RICH-j2-p6', 'RICH', 2, (1, 1), (23, -10, 4, -14), (23,), 0, (5, 5, 5, 49), 18, 1),
 ('RICH-j2-p7', 'RICH', 2, (2, 1), (23, -10, 4, -18), (23,), 0, (5, 5, 5, 49), 24, 2),
 ('RICH-j2-p8', 'RICH', 2, (3, 2), (23, -10, 4, -32), (23,), 0, (5, 5, 5, 49), 42, 3),
 ('RICH-j2-p9', 'RICH', 2, (7, 3), (23, -10, 4, -58), (23,), 0, (5, 5, 5, 49), 78, 7),
 ('RICH-j3-p0', 'RICH', 3, (-5, 2), (6, -6, 2, -2), (5, 6), 1, (8, 8, 8, 104), 5, -4),
 ('RICH-j3-p1', 'RICH', 3, (-2, 1), (6, -6, 2, -2), (5, 6, 15), 1, (8, 8, 8, 104), 3, -2),
 ('RICH-j3-p2', 'RICH', 3, (-1, 1), (15, -10, 4, -6), (15,), 4, (8, 8, 8, 104), 6, -2),
 ('RICH-j3-p3', 'RICH', 3, (0, 1), (15, -10, 4, -10), (15,), 4, (8, 8, 8, 104), 12, -2),
 ('RICH-j3-p4', 'RICH', 3, (0, 3), (15, -10, 4, -30), (15,), 4, (8, 8, 8, 104), 36, -6),
 ('RICH-j3-p5', 'RICH', 3, (1, 2), (15, -10, 4, -24), (15,), 4, (8, 8, 8, 104), 30, -4),
 ('RICH-j3-p6', 'RICH', 3, (1, 1), (15, -10, 4, -14), (15,), 4, (8, 8, 8, 104), 18, -2),
 ('RICH-j3-p7', 'RICH', 3, (2, 1), (15, -10, 4, -18), (15,), 4, (8, 8, 8, 104), 24, -2),
 ('RICH-j3-p8', 'RICH', 3, (3, 2), (15, -10, 4, -32), (15,), 4, (8, 8, 8, 104), 42, -4),
 ('RICH-j3-p9', 'RICH', 3, (7, 3), (15, -10, 4, -58), (15,), 4, (8, 8, 8, 104), 78, -6),
 ('MIXED-j0-p0', 'MIXED', 0, (-5, 2), (8, 12, 4, 44), (8,), 0, (1, 1, 1, 21), 0, 3),
 ('MIXED-j0-p1', 'MIXED', 0, (-2, 1), (8, 12, 4, 20), (8,), 0, (1, 1, 1, 21), 0, 1),
 ('MIXED-j0-p2', 'MIXED', 0, (-1, 1), (2, 10, 6, 16), (2, 8), 0, (1, 1, 1, 21), 0, 0),
 ('MIXED-j0-p3', 'MIXED', 0, (0, 1), (2, 10, 6, 10), (2,), 0, (1, 1, 1, 21), 0, -1),
 ('MIXED-j0-p4', 'MIXED', 0, (0, 3), (2, 10, 6, 30), (2,), 0, (1, 1, 1, 21), 0, -3),
 ('MIXED-j0-p5', 'MIXED', 0, (1, 2), (2, 10, 6, 14), (2, 7), 0, (1, 1, 1, 21), 0, -3),
 ('MIXED-j0-p6', 'MIXED', 0, (1, 1), (7, 16, 18, -2), (7,), 0, (1, 1, 1, 21), 8, -2),
 ('MIXED-j0-p7', 'MIXED', 0, (2, 1), (7, 16, 18, -20), (7,), 0, (1, 1, 1, 21), 26, -3),
 ('MIXED-j0-p8', 'MIXED', 0, (3, 2), (7, 16, 18, -22), (7,), 0, (1, 1, 1, 21), 33, -5),
 ('MIXED-j0-p9', 'MIXED', 0, (7, 3), (7, 16, 18, -78), (7,), 0, (1, 1, 1, 21), 98, -10),
 ('MIXED-j1-p0', 'MIXED', 1, (-5, 2), (1, 6, 4, 32), (1,), 0, (48, 26, 26, 118), 0, -4),
 ('MIXED-j1-p1', 'MIXED', 1, (-2, 1), (1, 6, 4, 14), (1,), 0, (48, 26, 26, 118), 0, -2),
 ('MIXED-j1-p2', 'MIXED', 1, (-1, 1), (1, 6, 4, 10), (1,), 0, (48, 26, 26, 118), 0, -2),
 ('MIXED-j1-p3', 'MIXED', 1, (0, 1), (1, 6, 4, 6), (1,), 0, (48, 26, 26, 118), 0, -2),
 ('MIXED-j1-p4', 'MIXED', 1, (0, 3), (1, 6, 4, 18), (1,), 0, (48, 26, 26, 118), 0, -6),
 ('MIXED-j1-p5', 'MIXED', 1, (1, 2), (1, 6, 4, 8), (1,), 0, (48, 26, 26, 118), 0, -4),
 ('MIXED-j1-p6', 'MIXED', 1, (1, 1), (14, 16, 16, 0), (14,), 13, (48, 26, 26, 118), 8, -2),
 ('MIXED-j1-p7', 'MIXED', 1, (2, 1), (14, 16, 16, -16), (14,), 13, (48, 26, 26, 118), 26, -2),
 ('MIXED-j1-p8', 'MIXED', 1, (3, 2), (14, 16, 16, -16), (14,), 13, (48, 26, 26, 118), 33, -4),
 ('MIXED-j1-p9', 'MIXED', 1, (7, 3), (14, 16, 16, -64), (14,), 13, (48, 26, 26, 118), 98, -6),
 ('MIXED-j2-p0', 'MIXED', 2, (-5, 2), (7, -18, 8, 4), (7,), 0, (4, 4, 4, 52), 7, -5),
 ('MIXED-j2-p1', 'MIXED', 2, (-2, 1), (7, -18, 8, -2), (7,), 0, (4, 4, 4, 52), 8, -2),
 ('MIXED-j2-p2', 'MIXED', 2, (-1, 1), (7, -18, 8, -10), (7,), 0, (4, 4, 4, 52), 20, -1),
 ('MIXED-j2-p3', 'MIXED', 2, (0, 1), (13, -18, 10, -18), (7, 13), 0, (4, 4, 4, 52), 34, 0),
 ('MIXED-j2-p4', 'MIXED', 2, (0, 3), (13, -18, 10, -54), (7, 13), 0, (4, 4, 4, 52), 102, 0),
 ('MIXED-j2-p5', 'MIXED', 2, (1, 2), (13, -18, 10, -46), (13,), 0, (4, 4, 4, 52), 82, 1),
 ('MIXED-j2-p6', 'MIXED', 2, (1, 1), (13, -18, 10, -28), (13,), 0, (4, 4, 4, 52), 48, 1),
 ('MIXED-j2-p7', 'MIXED', 2, (2, 1), (13, -18, 10, -38), (13,), 0, (4, 4, 4, 52), 62, 2),
 ('MIXED-j2-p8', 'MIXED', 2, (3, 2), (13, -18, 10, -66), (13,), 0, (4, 4, 4, 52), 110, 3),
 ('MIXED-j2-p9', 'MIXED', 2, (7, 3), (13, -18, 10, -124), (13,), 0, (4, 4, 4, 52), 200, 7),
 ('MIXED-j3-p0', 'MIXED', 3, (-5, 2), (1, -2, 2, 6), (1,), 0, (12, 10, 10, 70), 7, -4),
 ('MIXED-j3-p1', 'MIXED', 3, (-2, 1), (14, -24, 12, 0), (14,), 1, (12, 10, 10, 70), 8, -2),
 ('MIXED-j3-p2', 'MIXED', 3, (-1, 1), (14, -24, 12, -12), (14,), 1, (12, 10, 10, 70), 20, -2),
 ('MIXED-j3-p3', 'MIXED', 3, (0, 1), (14, -24, 12, -24), (14,), 1, (12, 10, 10, 70), 34, -2),
 ('MIXED-j3-p4', 'MIXED', 3, (0, 3), (14, -24, 12, -72), (14,), 1, (12, 10, 10, 70), 102, -6),
 ('MIXED-j3-p5', 'MIXED', 3, (1, 2), (14, -24, 12, -60), (14,), 1, (12, 10, 10, 70), 82, -4),
 ('MIXED-j3-p6', 'MIXED', 3, (1, 1), (14, -24, 12, -36), (14,), 1, (12, 10, 10, 70), 48, -2),
 ('MIXED-j3-p7', 'MIXED', 3, (2, 1), (14, -24, 12, -48), (14,), 1, (12, 10, 10, 70), 62, -2),
 ('MIXED-j3-p8', 'MIXED', 3, (3, 2), (14, -24, 12, -84), (14,), 1, (12, 10, 10, 70), 110, -4),
 ('MIXED-j3-p9', 'MIXED', 3, (7, 3), (14, -24, 12, -156), (14,), 1, (12, 10, 10, 70), 200, -6))

# NETWORKS: query, cut_coefficient, gamma, C_minus, constant, ordered_original_arcs
NETWORKS = (('MIXED-j0-p0',
  2,
  (24, 31, 48, 25),
  0,
  3,
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
   (0, 5, 24),
   (5, 0, 24),
   (1, 5, 31),
   (5, 1, 31),
   (2, 5, 48),
   (5, 2, 48),
   (3, 5, 25),
   (5, 3, 25))),
 ('MIXED-j0-p3',
  1,
  (2, 3, 4, 5),
  0,
  -1,
  ((0, 1, 2),
   (1, 0, 2),
   (0, 2, 3),
   (2, 0, 3),
   (0, 3, 1),
   (3, 0, 1),
   (1, 2, 4),
   (2, 1, 4),
   (1, 3, 2),
   (3, 1, 2),
   (2, 3, 5),
   (3, 2, 5),
   (0, 5, 2),
   (5, 0, 2),
   (1, 5, 3),
   (5, 1, 3),
   (2, 5, 4),
   (5, 2, 4),
   (3, 5, 5),
   (5, 3, 5))),
 ('MIXED-j0-p9',
  3,
  (-22, -26, -44, -6),
  98,
  -10,
  ((0, 1, 6),
   (1, 0, 6),
   (0, 2, 9),
   (2, 0, 9),
   (0, 3, 3),
   (3, 0, 3),
   (1, 2, 12),
   (2, 1, 12),
   (1, 3, 6),
   (3, 1, 6),
   (2, 3, 15),
   (3, 2, 15),
   (4, 0, 22),
   (0, 4, 22),
   (4, 1, 26),
   (1, 4, 26),
   (4, 2, 44),
   (2, 4, 44),
   (4, 3, 6),
   (3, 4, 6))),
 ('MIXED-j1-p0',
  2,
  (24, 31, 48, 25),
  0,
  -4,
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
   (0, 5, 24),
   (5, 0, 24),
   (1, 5, 31),
   (5, 1, 31),
   (2, 5, 48),
   (5, 2, 48),
   (3, 5, 25),
   (5, 3, 25))),
 ('MIXED-j1-p3',
  1,
  (2, 3, 4, 5),
  0,
  -2,
  ((0, 1, 2),
   (1, 0, 2),
   (0, 2, 3),
   (2, 0, 3),
   (0, 3, 1),
   (3, 0, 1),
   (1, 2, 4),
   (2, 1, 4),
   (1, 3, 2),
   (3, 1, 2),
   (2, 3, 5),
   (3, 2, 5),
   (0, 5, 2),
   (5, 0, 2),
   (1, 5, 3),
   (5, 1, 3),
   (2, 5, 4),
   (5, 2, 4),
   (3, 5, 5),
   (5, 3, 5))),
 ('MIXED-j1-p9',
  3,
  (-22, -26, -44, -6),
  98,
  -6,
  ((0, 1, 6),
   (1, 0, 6),
   (0, 2, 9),
   (2, 0, 9),
   (0, 3, 3),
   (3, 0, 3),
   (1, 2, 12),
   (2, 1, 12),
   (1, 3, 6),
   (3, 1, 6),
   (2, 3, 15),
   (3, 2, 15),
   (4, 0, 22),
   (0, 4, 22),
   (4, 1, 26),
   (1, 4, 26),
   (4, 2, 44),
   (2, 4, 44),
   (4, 3, 6),
   (3, 4, 6))),
 ('MIXED-j2-p0',
  2,
  (-2, -1, -4, 9),
  7,
  -5,
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
   (4, 0, 2),
   (0, 4, 2),
   (4, 1, 1),
   (1, 4, 1),
   (4, 2, 4),
   (2, 4, 4),
   (3, 5, 9),
   (5, 3, 9))),
 ('MIXED-j2-p3',
  1,
  (-6, -8, -12, -8),
  34,
  0,
  ((0, 1, 2),
   (1, 0, 2),
   (0, 2, 3),
   (2, 0, 3),
   (0, 3, 1),
   (3, 0, 1),
   (1, 2, 4),
   (2, 1, 4),
   (1, 3, 2),
   (3, 1, 2),
   (2, 3, 5),
   (3, 2, 5),
   (4, 0, 6),
   (0, 4, 6),
   (4, 1, 8),
   (1, 4, 8),
   (4, 2, 12),
   (2, 4, 12),
   (4, 3, 8),
   (3, 4, 8))),
 ('MIXED-j2-p9',
  3,
  (-32, -45, -64, -59),
  200,
  7,
  ((0, 1, 6),
   (1, 0, 6),
   (0, 2, 9),
   (2, 0, 9),
   (0, 3, 3),
   (3, 0, 3),
   (1, 2, 12),
   (2, 1, 12),
   (1, 3, 6),
   (3, 1, 6),
   (2, 3, 15),
   (3, 2, 15),
   (4, 0, 32),
   (0, 4, 32),
   (4, 1, 45),
   (1, 4, 45),
   (4, 2, 64),
   (2, 4, 64),
   (4, 3, 59),
   (3, 4, 59))),
 ('MIXED-j3-p0',
  2,
  (-2, -1, -4, 9),
  7,
  -4,
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
   (4, 0, 2),
   (0, 4, 2),
   (4, 1, 1),
   (1, 4, 1),
   (4, 2, 4),
   (2, 4, 4),
   (3, 5, 9),
   (5, 3, 9))),
 ('MIXED-j3-p3',
  1,
  (-6, -8, -12, -8),
  34,
  -2,
  ((0, 1, 2),
   (1, 0, 2),
   (0, 2, 3),
   (2, 0, 3),
   (0, 3, 1),
   (3, 0, 1),
   (1, 2, 4),
   (2, 1, 4),
   (1, 3, 2),
   (3, 1, 2),
   (2, 3, 5),
   (3, 2, 5),
   (4, 0, 6),
   (0, 4, 6),
   (4, 1, 8),
   (1, 4, 8),
   (4, 2, 12),
   (2, 4, 12),
   (4, 3, 8),
   (3, 4, 8))),
 ('MIXED-j3-p9',
  3,
  (-32, -45, -64, -59),
  200,
  -6,
  ((0, 1, 6),
   (1, 0, 6),
   (0, 2, 9),
   (2, 0, 9),
   (0, 3, 3),
   (3, 0, 3),
   (1, 2, 12),
   (2, 1, 12),
   (1, 3, 6),
   (3, 1, 6),
   (2, 3, 15),
   (3, 2, 15),
   (4, 0, 32),
   (0, 4, 32),
   (4, 1, 45),
   (1, 4, 45),
   (4, 2, 64),
   (2, 4, 64),
   (4, 3, 59),
   (3, 4, 59))))

# FAMILY_TRACE: query, family_index, T_pi_I_O,
# classes_rawT_T_reducedU_originalU_c_h_raw_cut_calls_replace_or_None
FAMILY_TRACE = (('Q1-j0-p3', 0, (0, 1, 0, 0), None),
 ('Q1-j3-p3', 0, (3, 0, 1, 2), None),
 ('Q1-j3-p3', 1, (3, 0, 2, 1), None),
 ('DOUBLE-j1-p3', 0, (3, 0, 1, 2), None),
 ('DOUBLE-j1-p3', 1, (3, 0, 3, 1), None),
 ('DOUBLE-j1-p3', 2, (3, 0, 3, 2), None),
 ('DOUBLE-j1-p3', 3, (3, 0, 2, 1), None),
 ('UNEQUAL-j0-p3', 0, (2, 1, 0, 0), ((4, 8, 1, 2), 8, 10, 13, 3, 2, 2, 2, 3, 7, True)),
 ('UNEQUAL-j2-p3', 0, (2, 1, 1, 0), ((5, 8, 2), 4, 6, 5, 3, -4, 2, -4, 0, 3, True)),
 ('EQUALITY-j3-p3', 0, (0, 0, 1, 2), ((41, 18, 4), 1, 3, 5, 5, -4, 4, -4, 4, 3, True)),
 ('EQUALITY-j3-p3', 1, (0, 0, 2, 1), ((42, 17, 4), 1, 3, 5, 6, -4, 4, -4, 4, 3, False)),
 ('EQUALITY-j3-p3', 2, (0, 0, 1, 4), ((41, 20, 2), 1, 3, 5, 3, -4, 4, -4, 4, 3, False)),
 ('EQUALITY-j3-p3', 3, (0, 0, 4, 1), ((44, 17, 2), 1, 3, 5, 6, -4, 4, -4, 4, 3, False)),
 ('EQUALITY-j3-p3', 4, (0, 0, 2, 4), ((42, 20, 1), 1, 3, 5, 3, -4, 4, -4, 4, 3, False)),
 ('EQUALITY-j3-p3', 5, (0, 0, 4, 2), ((44, 18, 1), 1, 3, 5, 5, -4, 4, -4, 4, 3, False)),
 ('RICH-j1-p7', 0, (3, 0, 1, 4), ((161, 68, 2, 8, 16), 4, 6, 5, 3, 4, 2, 0, 11, 13, True)),
 ('RICH-j1-p7', 1, (3, 0, 5, 1), None),
 ('RICH-j1-p7', 2, (3, 0, 3, 4), ((163, 68, 8, 16), 1, 3, 1, 3, 4, 2, 0, 11, 7, False)),
 ('RICH-j1-p7', 3, (3, 0, 5, 2), None),
 ('RICH-j1-p7', 4, (3, 0, 5, 16), ((165, 80, 2, 8), 4, 6, 5, 7, 2, 6, -10, 1, 7, True)),
 ('RICH-j1-p7', 5, (3, 0, 17, 4), ((177, 68, 2, 8), 4, 6, 5, 19, 8, 2, 4, 15, 7, False)),
 ('RICH-j1-p7', 6, (3, 0, 9, 16), ((169, 80, 2, 4), 4, 6, 13, 15, 4, 6, -8, 3, 7, False)),
 ('RICH-j1-p7', 7, (3, 0, 17, 8), ((177, 72, 2, 4), 4, 6, 13, 23, 4, 6, -8, 3, 7, False)),
 ('RICH-j1-p7', 8, (3, 0, 3, 4), ((163, 68, 8, 16), 1, 3, 1, 3, 4, 2, 0, 11, 7, False)),
 ('RICH-j1-p7', 9, (3, 0, 6, 1), None),
 ('RICH-j1-p7', 10, (3, 0, 2, 4), ((162, 68, 1, 8, 16), 4, 6, 5, 3, 4, 2, 0, 11, 13, False)),
 ('RICH-j1-p7', 11, (3, 0, 6, 2), None),
 ('RICH-j1-p7', 12, (3, 0, 6, 16), ((166, 80, 1, 8), 4, 6, 5, 7, 2, 6, -10, 1, 7, False)),
 ('RICH-j1-p7', 13, (3, 0, 18, 4), ((178, 68, 1, 8), 4, 6, 5, 19, 8, 2, 4, 15, 7, False)),
 ('RICH-j1-p7', 14, (3, 0, 10, 16), ((170, 80, 1, 4), 4, 6, 13, 15, 4, 6, -8, 3, 7, False)),
 ('RICH-j1-p7', 15, (3, 0, 18, 8), ((178, 72, 1, 4), 4, 6, 13, 23, 4, 6, -8, 3, 7, False)),
 ('RICH-j1-p7', 16, (3, 0, 5, 4), None),
 ('RICH-j1-p7', 17, (3, 0, 4, 1), ((164, 65, 2, 8, 16), 7, 5, 1, 4, 4, 4, -4, 7, 13, False)),
 ('RICH-j1-p7', 18, (3, 0, 6, 4), None),
 ('RICH-j1-p7', 19, (3, 0, 4, 2), ((164, 66, 1, 8, 16), 7, 5, 1, 4, 4, 4, -4, 7, 13, False)),
 ('RICH-j1-p7',
  20,
  (3, 0, 4, 16),
  ((164, 80, 1, 2, 8), 13, 15, 13, 7, 2, 6, -10, 1, 13, False)),
 ('RICH-j1-p7', 21, (3, 0, 20, 4), None),
 ('RICH-j1-p7', 22, (3, 0, 12, 16), ((172, 80, 1, 2), 13, 15, 13, 15, 4, 6, -8, 3, 7, False)),
 ('RICH-j1-p7', 23, (3, 0, 20, 8), ((180, 72, 1, 2), 13, 15, 13, 23, 4, 6, -8, 3, 7, False)),
 ('RICH-j1-p9', 0, (3, 0, 1, 4), ((161, 68, 2, 8, 16), 4, 6, 5, 3, 4, 2, -2, 37, 13, True)),
 ('RICH-j1-p9', 1, (3, 0, 5, 1), None),
 ('RICH-j1-p9', 2, (3, 0, 3, 4), ((163, 68, 8, 16), 1, 3, 1, 3, 4, 2, -2, 37, 7, False)),
 ('RICH-j1-p9', 3, (3, 0, 5, 2), None),
 ('RICH-j1-p9', 4, (3, 0, 5, 16), ((165, 80, 2, 8), 4, 6, 5, 7, 2, 6, -36, 3, 7, True)),
 ('RICH-j1-p9', 5, (3, 0, 17, 4), ((177, 68, 2, 8), 4, 6, 5, 19, 8, 2, 10, 49, 7, False)),
 ('RICH-j1-p9', 6, (3, 0, 9, 16), ((169, 80, 2, 4), 4, 6, 13, 15, 4, 6, -30, 9, 7, False)),
 ('RICH-j1-p9', 7, (3, 0, 17, 8), ((177, 72, 2, 4), 4, 6, 13, 23, 4, 6, -30, 9, 7, False)),
 ('RICH-j1-p9', 8, (3, 0, 3, 4), ((163, 68, 8, 16), 1, 3, 1, 3, 4, 2, -2, 37, 7, False)),
 ('RICH-j1-p9', 9, (3, 0, 6, 1), None),
 ('RICH-j1-p9', 10, (3, 0, 2, 4), ((162, 68, 1, 8, 16), 4, 6, 5, 3, 4, 2, -2, 37, 13, False)),
 ('RICH-j1-p9', 11, (3, 0, 6, 2), None),
 ('RICH-j1-p9', 12, (3, 0, 6, 16), ((166, 80, 1, 8), 4, 6, 5, 7, 2, 6, -36, 3, 7, False)),
 ('RICH-j1-p9', 13, (3, 0, 18, 4), ((178, 68, 1, 8), 4, 6, 5, 19, 8, 2, 10, 49, 7, False)),
 ('RICH-j1-p9', 14, (3, 0, 10, 16), ((170, 80, 1, 4), 4, 6, 13, 15, 4, 6, -30, 9, 7, False)),
 ('RICH-j1-p9', 15, (3, 0, 18, 8), ((178, 72, 1, 4), 4, 6, 13, 23, 4, 6, -30, 9, 7, False)),
 ('RICH-j1-p9', 16, (3, 0, 5, 4), None),
 ('RICH-j1-p9', 17, (3, 0, 4, 1), ((164, 65, 2, 8, 16), 7, 5, 1, 4, 4, 4, -16, 23, 13, False)),
 ('RICH-j1-p9', 18, (3, 0, 6, 4), None),
 ('RICH-j1-p9', 19, (3, 0, 4, 2), ((164, 66, 1, 8, 16), 7, 5, 1, 4, 4, 4, -16, 23, 13, False)),
 ('RICH-j1-p9',
  20,
  (3, 0, 4, 16),
  ((164, 80, 1, 2, 8), 13, 15, 13, 7, 2, 6, -36, 3, 13, False)),
 ('RICH-j1-p9', 21, (3, 0, 20, 4), None),
 ('RICH-j1-p9', 22, (3, 0, 12, 16), ((172, 80, 1, 2), 13, 15, 13, 15, 4, 6, -30, 9, 7, False)),
 ('RICH-j1-p9', 23, (3, 0, 20, 8), ((180, 72, 1, 2), 13, 15, 13, 23, 4, 6, -30, 9, 7, False)),
 ('RICH-j3-p1', 0, (15, 0, 1, 4), ((161, 68, 2, 8, 16), 14, 12, 5, 3, -2, 2, 2, 7, 13, True)),
 ('RICH-j3-p1', 1, (15, 0, 4, 1), ((164, 65, 2, 8, 16), 14, 12, 5, 6, -6, 2, -2, 3, 13, True)),
 ('RICH-j3-p1', 2, (15, 0, 2, 4), ((162, 68, 1, 8, 16), 14, 12, 5, 3, -2, 2, 2, 7, 13, False)),
 ('RICH-j3-p1', 3, (15, 0, 4, 2), ((164, 66, 1, 8, 16), 14, 12, 5, 5, -6, 2, -2, 3, 13, False)),
 ('RICH-j3-p1', 4, (15, 0, 4, 16), ((164, 80, 1, 2, 8), 28, 30, 9, 6, -6, 2, -2, 3, 13, False)),
 ('RICH-j3-p1', 5, (15, 0, 16, 4), ((176, 68, 1, 2, 8), 31, 29, 1, 16, -2, 2, 2, 7, 13, False)),
 ('RICH-j3-p1',
  6,
  (15, 0, 8, 16),
  ((168, 80, 1, 2, 4), 28, 30, 29, 15, -10, 4, -2, 3, 13, False)),
 ('RICH-j3-p1',
  7,
  (15, 0, 16, 8),
  ((176, 72, 1, 2, 4), 31, 29, 25, 22, -8, 4, 0, 5, 13, False)),
 ('MIXED-j0-p0',
  0,
  (10, 1, 0, 0),
  ((16, 32, 1, 2, 4, 8), 40, 40, 33, 8, 12, 4, 44, 41, 21, True)),
 ('MIXED-j1-p0', 0, (10, 0, 1, 2), ((81, 34, 4, 8), 11, 9, 1, 1, 6, 4, 32, 36, 7, True)),
 ('MIXED-j1-p0', 1, (10, 0, 3, 1), None),
 ('MIXED-j1-p0', 2, (10, 0, 1, 4), ((81, 36, 2, 8), 13, 15, 1, 1, 6, 4, 32, 36, 7, False)),
 ('MIXED-j1-p0', 3, (10, 0, 5, 1), None),
 ('MIXED-j1-p0', 4, (10, 0, 1, 8), ((81, 40, 2, 4), 7, 5, 1, 1, 6, 4, 32, 36, 7, False)),
 ('MIXED-j1-p0', 5, (10, 0, 9, 1), None),
 ('MIXED-j1-p0', 6, (10, 0, 3, 4), ((83, 36, 8), 4, 6, 5, 11, 20, 12, 100, 104, 3, False)),
 ('MIXED-j1-p0', 7, (10, 0, 5, 2), ((85, 34, 8), 7, 5, 1, 5, 16, 12, 92, 96, 3, False)),
 ('MIXED-j1-p0', 8, (10, 0, 3, 8), None),
 ('MIXED-j1-p0', 9, (10, 0, 9, 2), None),
 ('MIXED-j1-p0', 10, (10, 0, 5, 8), ((85, 40, 2), 7, 5, 1, 5, 16, 12, 92, 96, 3, False)),
 ('MIXED-j1-p0', 11, (10, 0, 9, 4), ((89, 36, 2), 4, 6, 5, 11, 20, 12, 100, 104, 3, False)),
 ('MIXED-j1-p0', 12, (10, 0, 3, 2), None),
 ('MIXED-j1-p0', 13, (10, 0, 2, 1), ((82, 33, 4, 8), 8, 10, 9, 10, 18, 8, 76, 80, 7, False)),
 ('MIXED-j1-p0', 14, (10, 0, 3, 4), ((83, 36, 8), 4, 6, 5, 11, 20, 12, 100, 104, 3, False)),
 ('MIXED-j1-p0', 15, (10, 0, 6, 1), ((86, 33, 8), 4, 6, 5, 14, 16, 16, 112, 116, 3, False)),
 ('MIXED-j1-p0', 16, (10, 0, 3, 8), None),
 ('MIXED-j1-p0', 17, (10, 0, 10, 1), ((90, 33, 4), 1, 3, 1, 10, 18, 8, 76, 80, 3, False)),
 ('MIXED-j1-p0', 18, (10, 0, 2, 4), ((82, 36, 1, 8), 8, 10, 9, 10, 18, 8, 76, 80, 7, False)),
 ('MIXED-j1-p0', 19, (10, 0, 6, 2), None),
 ('MIXED-j1-p0', 20, (10, 0, 2, 8), None),
 ('MIXED-j1-p0', 21, (10, 0, 10, 2), None),
 ('MIXED-j1-p0', 22, (10, 0, 6, 8), None),
 ('MIXED-j1-p0', 23, (10, 0, 10, 4), ((90, 36, 1), 1, 3, 1, 10, 18, 8, 76, 80, 3, False)),
 ('MIXED-j1-p0', 24, (10, 0, 5, 2), ((85, 34, 8), 7, 5, 1, 5, 16, 12, 92, 96, 3, False)),
 ('MIXED-j1-p0', 25, (10, 0, 6, 1), ((86, 33, 8), 4, 6, 5, 14, 16, 16, 112, 116, 3, False)),
 ('MIXED-j1-p0', 26, (10, 0, 5, 4), None),
 ('MIXED-j1-p0', 27, (10, 0, 4, 1), ((84, 33, 2, 8), 13, 15, 1, 4, 14, 8, 68, 72, 7, False)),
 ('MIXED-j1-p0', 28, (10, 0, 5, 8), ((85, 40, 2), 7, 5, 1, 5, 16, 12, 92, 96, 3, False)),
 ('MIXED-j1-p0', 29, (10, 0, 12, 1), ((92, 33, 2), 4, 6, 5, 14, 16, 16, 112, 116, 3, False)),
 ('MIXED-j1-p0', 30, (10, 0, 6, 4), None),
 ('MIXED-j1-p0', 31, (10, 0, 4, 2), ((84, 34, 1, 8), 11, 9, 1, 4, 14, 8, 68, 72, 7, False)),
 ('MIXED-j1-p0', 32, (10, 0, 6, 8), None),
 ('MIXED-j1-p0', 33, (10, 0, 12, 2), None),
 ('MIXED-j1-p0', 34, (10, 0, 4, 8), ((84, 40, 1, 2), 11, 9, 1, 4, 14, 8, 68, 72, 7, False)),
 ('MIXED-j1-p0', 35, (10, 0, 12, 4), None),
 ('MIXED-j1-p0', 36, (10, 0, 9, 2), None),
 ('MIXED-j1-p0', 37, (10, 0, 10, 1), ((90, 33, 4), 1, 3, 1, 10, 18, 8, 76, 80, 3, False)),
 ('MIXED-j1-p0', 38, (10, 0, 9, 4), ((89, 36, 2), 4, 6, 5, 11, 20, 12, 100, 104, 3, False)),
 ('MIXED-j1-p0', 39, (10, 0, 12, 1), ((92, 33, 2), 4, 6, 5, 14, 16, 16, 112, 116, 3, False)),
 ('MIXED-j1-p0', 40, (10, 0, 9, 8), None),
 ('MIXED-j1-p0', 41, (10, 0, 8, 1), ((88, 33, 2, 4), 4, 6, 5, 10, 18, 8, 76, 80, 7, False)),
 ('MIXED-j1-p0', 42, (10, 0, 10, 4), ((90, 36, 1), 1, 3, 1, 10, 18, 8, 76, 80, 3, False)),
 ('MIXED-j1-p0', 43, (10, 0, 12, 2), None),
 ('MIXED-j1-p0', 44, (10, 0, 10, 8), None),
 ('MIXED-j1-p0', 45, (10, 0, 8, 2), None),
 ('MIXED-j1-p0', 46, (10, 0, 12, 8), None),
 ('MIXED-j1-p0', 47, (10, 0, 8, 4), ((88, 36, 1, 2), 8, 10, 9, 10, 18, 8, 76, 80, 7, False)),
 ('MIXED-j2-p0', 0, (10, 1, 1, 0), ((17, 32, 2, 4, 8), 20, 20, 13, 7, -18, 8, 4, 16, 13, True)),
 ('MIXED-j2-p0',
  1,
  (10, 1, 2, 0),
  ((18, 32, 1, 4, 8), 17, 17, 13, 7, -18, 8, 4, 16, 13, False)),
 ('MIXED-j2-p0',
  2,
  (10, 1, 4, 0),
  ((20, 32, 1, 2, 8), 24, 24, 13, 7, -18, 8, 4, 16, 13, False)),
 ('MIXED-j2-p0',
  3,
  (10, 1, 8, 0),
  ((24, 32, 1, 2, 4), 9, 9, 21, 13, -18, 10, 14, 26, 13, False)),
 ('MIXED-j3-p0', 0, (10, 0, 1, 2), ((81, 34, 4, 8), 11, 9, 1, 1, -2, 2, 6, 17, 7, True)),
 ('MIXED-j3-p0', 1, (10, 0, 2, 1), ((82, 33, 4, 8), 8, 10, 13, 14, -24, 12, 12, 23, 7, False)),
 ('MIXED-j3-p0', 2, (10, 0, 1, 4), ((81, 36, 2, 8), 13, 15, 1, 1, -2, 2, 6, 17, 7, False)),
 ('MIXED-j3-p0', 3, (10, 0, 4, 1), ((84, 33, 2, 8), 13, 15, 13, 14, -24, 12, 12, 23, 7, False)),
 ('MIXED-j3-p0', 4, (10, 0, 1, 8), ((81, 40, 2, 4), 7, 5, 1, 1, -2, 2, 6, 17, 7, False)),
 ('MIXED-j3-p0', 5, (10, 0, 8, 1), ((88, 33, 2, 4), 4, 6, 13, 14, -24, 12, 12, 23, 7, False)),
 ('MIXED-j3-p0', 6, (10, 0, 2, 4), ((82, 36, 1, 8), 8, 10, 13, 11, -12, 10, 26, 37, 7, False)),
 ('MIXED-j3-p0', 7, (10, 0, 4, 2), ((84, 34, 1, 8), 11, 9, 5, 5, -8, 6, 14, 25, 7, False)),
 ('MIXED-j3-p0', 8, (10, 0, 2, 8), None),
 ('MIXED-j3-p0', 9, (10, 0, 8, 2), None),
 ('MIXED-j3-p0', 10, (10, 0, 4, 8), ((84, 40, 1, 2), 11, 9, 5, 5, -8, 6, 14, 25, 7, False)),
 ('MIXED-j3-p0', 11, (10, 0, 8, 4), ((88, 36, 1, 2), 8, 10, 13, 11, -12, 10, 26, 37, 7, False)),
 ('ODDFULL-j2-p3', 0, (4, 1, 1, 0), ((9, 16, 2, 4), 8, 10, 13, 7, -6, 4, -6, 0, 7, True)),
 ('ODDFULL-j2-p3', 1, (4, 1, 2, 0), ((10, 16, 1, 4), 8, 10, 13, 7, -6, 4, -6, 0, 7, False)),
 ('TIECARD-j3-p0', 0, (3, 0, 1, 4), ((41, 20, 2), 4, 6, 5, 3, -2, 2, 6, 10, 3, True)),
 ('TIECARD-j3-p0', 1, (3, 0, 4, 1), ((44, 17, 2), 7, 5, 1, 4, -2, 2, 6, 10, 3, False)),
 ('TIECARD-j3-p0', 2, (3, 0, 2, 4), ((42, 20, 1), 4, 6, 5, 3, -2, 2, 6, 10, 3, False)),
 ('TIECARD-j3-p0', 3, (3, 0, 4, 2), ((44, 18, 1), 7, 5, 1, 4, -2, 2, 6, 10, 3, False)))

# TRAPS: trap, query, comparison_family, comparison_U_c_h_raw, correct_family, correct_result
TRAPS = (('early-zero', 'RICH-j1-p7', 0, (3, 4, 2, 0), 4, (7, 2, 6, -10)),
 ('early-negative', 'RICH-j1-p9', 0, (3, 4, 2, -2), 4, (7, 2, 6, -36)),
 ('not-max-h', 'RICH-j3-p1', 6, (15, -10, 4, -2), 1, (6, -6, 2, -2)),
 ('not-smallest-mask', 'EQUALITY-j3-p3', 2, (3, -4, 4, -4), 0, (5, -4, 4, -4)),
 ('full-original-shore', 'UNEQUAL-j2-p3', 0, (3, -4, 2, -4), 0, (3, -4, 2, -4)),
 ('not-smallest-cardinality', 'TIECARD-j3-p0', 1, (4, -2, 2, 6), 0, (3, -2, 2, 6)),
 ('zero-cut-complete-scan', 'ODDFULL-j2-p3', 0, (7, -6, 4, -6), 0, (7, -6, 4, -6)))

# COORDINATE_RECOVERY: query, family, classes, reduced_shore, original_shore, cut, C_minus,
# constant, raw
COORDINATE_RECOVERY = (('UNEQUAL-j0-p3', 0, (4, 8, 1, 2), 13, 3, 3, 0, -1, 2),
 ('RICH-j1-p7', 4, (165, 80, 2, 8), 5, 7, 1, 9, -2, -10),
 ('EQUALITY-j3-p3', 0, (41, 18, 4), 5, 5, 4, 6, -2, -4))

# UNRESTRICTED_TRAP: query, unrestricted_original_shore, unrestricted_cut, unrestricted_raw,
# branch_result
UNRESTRICTED_TRAP = (('DOUBLE-j0-p3', 0, 0, -1, (1, 2, 2, 2)),)

# STATS: query, seven_stats_fields, derived_max_flow_calls
STATS = (('Q1-j0-p3', (1, 0, 0, 0, 0, 0, 0), 0),
 ('Q1-j1-p3', (0, 0, 0, 0, 0, 0, 0), 0),
 ('Q1-j2-p3', (0, 0, 0, 0, 0, 0, 0), 0),
 ('Q1-j3-p3', (2, 0, 0, 0, 0, 0, 0), 0),
 ('DOUBLE-j0-p3', (1, 1, 1, 7, 6, 40, 3), 7),
 ('DOUBLE-j0-p7', (1, 1, 1, 7, 6, 52, 3), 7),
 ('UNEQUAL-j0-p3', (1, 1, 1, 7, 6, 36, 4), 7),
 ('UNEQUAL-j2-p3', (1, 1, 1, 3, 1, 7, 4), 3),
 ('EQUALITY-j3-p3', (6, 6, 6, 18, 24, 138, 6), 18),
 ('RICH-j3-p1', (8, 8, 8, 104, 148, 1138, 9), 104))

# FLOW_DIAGNOSTIC_TRACE: query, family, inside, outside, temporary_N, temporary_arcs, value,
# temporary_least_shore, augmentations_scans_peak, BFS_scans_bottleneck_failed_reached_rows
FLOW_DIAGNOSTIC_TRACE = (('DOUBLE-j0-p3',
  0,
  0,
  1,
  4,
  ((1, 2, 1), (1, 3, 1), (2, 1, 1), (2, 3, 2), (3, 1, 1), (3, 2, 2)),
  0,
  1,
  (0, 0, 2),
  ((0, 0, 1),)),
 ('DOUBLE-j0-p3', 0, 0, 2, 3, ((1, 2, 3), (2, 1, 3)), 0, 1, (0, 0, 3), ((0, 0, 1),)),
 ('DOUBLE-j0-p3', 0, 0, 3, 3, ((1, 2, 3), (2, 1, 3)), 0, 1, (0, 0, 3), ((0, 0, 1),)),
 ('DOUBLE-j0-p3',
  0,
  2,
  1,
  3,
  ((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 1), (2, 0, 2), (2, 1, 1)),
  2,
  5,
  (2, 17, 2),
  ((1, 1, None), (8, 1, None), (8, 0, 5))),
 ('DOUBLE-j0-p3',
  0,
  2,
  3,
  2,
  ((0, 1, 3), (1, 0, 3)),
  3,
  1,
  (1, 3, 3),
  ((1, 3, None), (2, 0, 1))),
 ('DOUBLE-j0-p3',
  0,
  3,
  1,
  3,
  ((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 1), (2, 0, 2), (2, 1, 1)),
  2,
  5,
  (2, 17, 2),
  ((1, 1, None), (8, 1, None), (8, 0, 5))),
 ('DOUBLE-j0-p3',
  0,
  3,
  2,
  2,
  ((0, 1, 3), (1, 0, 3)),
  3,
  1,
  (1, 3, 3),
  ((1, 3, None), (2, 0, 1))),
 ('DOUBLE-j0-p7',
  0,
  0,
  1,
  4,
  ((0, 2, 1), (0, 3, 1), (2, 0, 1), (2, 3, 2), (3, 0, 1), (3, 2, 2)),
  0,
  13,
  (0, 12, 2),
  ((12, 0, 13),)),
 ('DOUBLE-j0-p7',
  0,
  0,
  2,
  3,
  ((0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 2, 2), (2, 0, 1), (2, 1, 2)),
  2,
  1,
  (2, 13, 2),
  ((1, 1, None), (8, 1, None), (4, 0, 1))),
 ('DOUBLE-j0-p7',
  0,
  0,
  3,
  3,
  ((0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 2, 2), (2, 0, 1), (2, 1, 2)),
  2,
  1,
  (2, 13, 2),
  ((1, 1, None), (8, 1, None), (4, 0, 1))),
 ('DOUBLE-j0-p7', 0, 2, 1, 3, ((0, 2, 3), (2, 0, 3)), 0, 5, (0, 4, 3), ((4, 0, 5),)),
 ('DOUBLE-j0-p7',
  0,
  2,
  3,
  2,
  ((0, 1, 3), (1, 0, 3)),
  3,
  1,
  (1, 3, 3),
  ((1, 3, None), (2, 0, 1))),
 ('DOUBLE-j0-p7', 0, 3, 1, 3, ((0, 2, 3), (2, 0, 3)), 0, 5, (0, 4, 3), ((4, 0, 5),)),
 ('DOUBLE-j0-p7',
  0,
  3,
  2,
  2,
  ((0, 1, 3), (1, 0, 3)),
  3,
  1,
  (1, 3, 3),
  ((1, 3, None), (2, 0, 1))),
 ('UNEQUAL-j0-p3',
  0,
  0,
  1,
  4,
  ((1, 2, 2), (1, 3, 1), (2, 1, 2), (2, 3, 2), (3, 1, 1), (3, 2, 2)),
  0,
  1,
  (0, 0, 2),
  ((0, 0, 1),)),
 ('UNEQUAL-j0-p3', 0, 0, 2, 3, ((1, 2, 3), (2, 1, 3)), 0, 1, (0, 0, 3), ((0, 0, 1),)),
 ('UNEQUAL-j0-p3', 0, 0, 3, 3, ((1, 2, 4), (2, 1, 4)), 0, 1, (0, 0, 4), ((0, 0, 1),)),
 ('UNEQUAL-j0-p3',
  0,
  2,
  1,
  3,
  ((0, 1, 2), (0, 2, 2), (1, 0, 2), (1, 2, 1), (2, 0, 2), (2, 1, 1)),
  3,
  5,
  (2, 17, 3),
  ((1, 2, None), (8, 1, None), (8, 0, 5))),
 ('UNEQUAL-j0-p3',
  0,
  2,
  3,
  2,
  ((0, 1, 4), (1, 0, 4)),
  4,
  1,
  (1, 3, 4),
  ((1, 4, None), (2, 0, 1))),
 ('UNEQUAL-j0-p3',
  0,
  3,
  1,
  3,
  ((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 2), (2, 0, 2), (2, 1, 2)),
  3,
  1,
  (2, 13, 3),
  ((1, 1, None), (8, 2, None), (4, 0, 1))),
 ('UNEQUAL-j0-p3',
  0,
  3,
  2,
  2,
  ((0, 1, 3), (1, 0, 3)),
  3,
  1,
  (1, 3, 3),
  ((1, 3, None), (2, 0, 1))),
 ('UNEQUAL-j2-p3', 0, 0, 1, 3, ((0, 2, 4), (2, 0, 4)), 0, 5, (0, 4, 4), ((4, 0, 5),)),
 ('UNEQUAL-j2-p3',
  0,
  0,
  2,
  2,
  ((0, 1, 4), (1, 0, 4)),
  4,
  1,
  (1, 3, 4),
  ((1, 4, None), (2, 0, 1))),
 ('UNEQUAL-j2-p3', 0, 2, 1, 2, (), 0, 1, (0, 0, 0), ()),
 ('EQUALITY-j3-p3',
  0,
  0,
  1,
  3,
  ((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1)),
  4,
  5,
  (2, 17, 4),
  ((1, 3, None), (8, 1, None), (8, 0, 5))),
 ('EQUALITY-j3-p3',
  0,
  0,
  2,
  2,
  ((0, 1, 6), (1, 0, 6)),
  6,
  1,
  (1, 3, 6),
  ((1, 6, None), (2, 0, 1))),
 ('EQUALITY-j3-p3',
  0,
  2,
  1,
  2,
  ((0, 1, 4), (1, 0, 4)),
  4,
  1,
  (1, 3, 4),
  ((1, 4, None), (2, 0, 1))),
 ('EQUALITY-j3-p3',
  1,
  0,
  1,
  3,
  ((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1)),
  4,
  5,
  (2, 17, 4),
  ((1, 3, None), (8, 1, None), (8, 0, 5))),
 ('EQUALITY-j3-p3',
  1,
  0,
  2,
  2,
  ((0, 1, 6), (1, 0, 6)),
  6,
  1,
  (1, 3, 6),
  ((1, 6, None), (2, 0, 1))),
 ('EQUALITY-j3-p3',
  1,
  2,
  1,
  2,
  ((0, 1, 4), (1, 0, 4)),
  4,
  1,
  (1, 3, 4),
  ((1, 4, None), (2, 0, 1))),
 ('EQUALITY-j3-p3',
  2,
  0,
  1,
  3,
  ((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1)),
  4,
  5,
  (2, 17, 4),
  ((1, 3, None), (8, 1, None), (8, 0, 5))),
 ('EQUALITY-j3-p3',
  2,
  0,
  2,
  2,
  ((0, 1, 6), (1, 0, 6)),
  6,
  1,
  (1, 3, 6),
  ((1, 6, None), (2, 0, 1))),
 ('EQUALITY-j3-p3',
  2,
  2,
  1,
  2,
  ((0, 1, 4), (1, 0, 4)),
  4,
  1,
  (1, 3, 4),
  ((1, 4, None), (2, 0, 1))),
 ('EQUALITY-j3-p3',
  3,
  0,
  1,
  3,
  ((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1)),
  4,
  5,
  (2, 17, 4),
  ((1, 3, None), (8, 1, None), (8, 0, 5))),
 ('EQUALITY-j3-p3',
  3,
  0,
  2,
  2,
  ((0, 1, 6), (1, 0, 6)),
  6,
  1,
  (1, 3, 6),
  ((1, 6, None), (2, 0, 1))),
 ('EQUALITY-j3-p3',
  3,
  2,
  1,
  2,
  ((0, 1, 4), (1, 0, 4)),
  4,
  1,
  (1, 3, 4),
  ((1, 4, None), (2, 0, 1))),
 ('EQUALITY-j3-p3',
  4,
  0,
  1,
  3,
  ((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1)),
  4,
  5,
  (2, 17, 4),
  ((1, 3, None), (8, 1, None), (8, 0, 5))),
 ('EQUALITY-j3-p3',
  4,
  0,
  2,
  2,
  ((0, 1, 6), (1, 0, 6)),
  6,
  1,
  (1, 3, 6),
  ((1, 6, None), (2, 0, 1))),
 ('EQUALITY-j3-p3',
  4,
  2,
  1,
  2,
  ((0, 1, 4), (1, 0, 4)),
  4,
  1,
  (1, 3, 4),
  ((1, 4, None), (2, 0, 1))),
 ('EQUALITY-j3-p3',
  5,
  0,
  1,
  3,
  ((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1)),
  4,
  5,
  (2, 17, 4),
  ((1, 3, None), (8, 1, None), (8, 0, 5))),
 ('EQUALITY-j3-p3',
  5,
  0,
  2,
  2,
  ((0, 1, 6), (1, 0, 6)),
  6,
  1,
  (1, 3, 6),
  ((1, 6, None), (2, 0, 1))),
 ('EQUALITY-j3-p3',
  5,
  2,
  1,
  2,
  ((0, 1, 4), (1, 0, 4)),
  4,
  1,
  (1, 3, 4),
  ((1, 4, None), (2, 0, 1))),
 ('RICH-j3-p1',
  0,
  0,
  1,
  5,
  ((0, 1, 5),
   (1, 0, 5),
   (1, 2, 2),
   (1, 3, 1),
   (1, 4, 3),
   (2, 1, 2),
   (3, 1, 1),
   (3, 4, 1),
   (4, 1, 3),
   (4, 3, 1)),
  5,
  1,
  (1, 3, 5),
  ((1, 5, None), (2, 0, 1))),
 ('RICH-j3-p1',
  0,
  0,
  2,
  4,
  ((0, 1, 5), (1, 0, 5), (1, 2, 1), (1, 3, 3), (2, 1, 1), (2, 3, 1), (3, 1, 3), (3, 2, 1)),
  5,
  1,
  (1, 3, 5),
  ((1, 5, None), (2, 0, 1))),
 ('RICH-j3-p1',
  0,
  0,
  3,
  4,
  ((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 4), (2, 1, 2), (3, 1, 4)),
  5,
  1,
  (1, 3, 5),
  ((1, 5, None), (2, 0, 1))),
 ('RICH-j3-p1',
  0,
  0,
  4,
  4,
  ((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2)),
  5,
  1,
  (1, 3, 5),
  ((1, 5, None), (2, 0, 1))),
 ('RICH-j3-p1',
  0,
  2,
  1,
  4,
  ((0, 1, 7), (1, 0, 7), (1, 2, 1), (1, 3, 3), (2, 1, 1), (2, 3, 1), (3, 1, 3), (3, 2, 1)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  0,
  2,
  3,
  3,
  ((0, 1, 7), (1, 0, 7), (1, 2, 4), (2, 1, 4)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  0,
  2,
  4,
  3,
  ((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  0,
  3,
  1,
  4,
  ((0, 1, 6), (0, 3, 1), (1, 0, 6), (1, 2, 2), (1, 3, 3), (2, 1, 2), (3, 0, 1), (3, 1, 3)),
  7,
  1,
  (2, 13, 7),
  ((1, 6, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  0,
  3,
  2,
  3,
  ((0, 1, 6), (0, 2, 1), (1, 0, 6), (1, 2, 3), (2, 0, 1), (2, 1, 3)),
  7,
  1,
  (2, 13, 7),
  ((1, 6, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  0,
  3,
  4,
  3,
  ((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  0,
  4,
  1,
  4,
  ((0, 1, 8), (0, 3, 1), (1, 0, 8), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1)),
  9,
  1,
  (2, 13, 9),
  ((1, 8, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  0,
  4,
  2,
  3,
  ((0, 1, 8), (0, 2, 1), (1, 0, 8), (1, 2, 1), (2, 0, 1), (2, 1, 1)),
  9,
  1,
  (2, 13, 9),
  ((1, 8, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  0,
  4,
  3,
  3,
  ((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2)),
  9,
  1,
  (1, 3, 9),
  ((1, 9, None), (2, 0, 1))),
 ('RICH-j3-p1',
  1,
  0,
  1,
  5,
  ((0, 1, 2),
   (0, 2, 2),
   (0, 4, 1),
   (1, 0, 2),
   (1, 2, 0),
   (1, 3, 1),
   (1, 4, 2),
   (2, 0, 2),
   (2, 1, 0),
   (3, 1, 1),
   (3, 4, 1),
   (4, 0, 1),
   (4, 1, 2),
   (4, 3, 1)),
  3,
  5,
  (2, 26, 3),
  ((1, 2, None), (15, 1, None), (10, 0, 5))),
 ('RICH-j3-p1',
  1,
  0,
  2,
  4,
  ((0, 1, 4),
   (0, 3, 1),
   (1, 0, 4),
   (1, 2, 1),
   (1, 3, 2),
   (2, 1, 1),
   (2, 3, 1),
   (3, 0, 1),
   (3, 1, 2),
   (3, 2, 1)),
  5,
  1,
  (2, 14, 5),
  ((1, 4, None), (9, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  1,
  0,
  3,
  4,
  ((0, 1, 2),
   (0, 2, 2),
   (0, 3, 1),
   (1, 0, 2),
   (1, 2, 0),
   (1, 3, 3),
   (2, 0, 2),
   (2, 1, 0),
   (3, 0, 1),
   (3, 1, 3)),
  3,
  5,
  (2, 25, 3),
  ((1, 2, None), (14, 1, None), (10, 0, 5))),
 ('RICH-j3-p1',
  1,
  0,
  4,
  4,
  ((0, 1, 3), (0, 2, 2), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2)),
  3,
  5,
  (1, 9, 3),
  ((1, 3, None), (8, 0, 5))),
 ('RICH-j3-p1',
  1,
  2,
  1,
  4,
  ((0, 1, 2),
   (0, 3, 1),
   (1, 0, 2),
   (1, 2, 1),
   (1, 3, 2),
   (2, 1, 1),
   (2, 3, 1),
   (3, 0, 1),
   (3, 1, 2),
   (3, 2, 1)),
  3,
  1,
  (2, 14, 3),
  ((1, 2, None), (9, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  1,
  2,
  3,
  3,
  ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 3), (2, 0, 1), (2, 1, 3)),
  3,
  1,
  (2, 13, 3),
  ((1, 2, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  1,
  2,
  4,
  3,
  ((0, 1, 3), (1, 0, 3), (1, 2, 2), (2, 1, 2)),
  3,
  1,
  (1, 3, 3),
  ((1, 3, None), (2, 0, 1))),
 ('RICH-j3-p1',
  1,
  3,
  1,
  4,
  ((0, 1, 3),
   (0, 2, 2),
   (0, 3, 2),
   (1, 0, 3),
   (1, 2, 0),
   (1, 3, 2),
   (2, 0, 2),
   (2, 1, 0),
   (3, 0, 2),
   (3, 1, 2)),
  5,
  5,
  (2, 25, 5),
  ((1, 3, None), (14, 2, None), (10, 0, 5))),
 ('RICH-j3-p1',
  1,
  3,
  2,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 2), (2, 0, 2), (2, 1, 2)),
  7,
  1,
  (2, 13, 7),
  ((1, 5, None), (8, 2, None), (4, 0, 1))),
 ('RICH-j3-p1',
  1,
  3,
  4,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  5,
  5,
  (1, 9, 5),
  ((1, 5, None), (8, 0, 5))),
 ('RICH-j3-p1',
  1,
  4,
  1,
  4,
  ((0, 1, 4),
   (0, 2, 2),
   (0, 3, 1),
   (1, 0, 4),
   (1, 2, 0),
   (1, 3, 1),
   (2, 0, 2),
   (2, 1, 0),
   (3, 0, 1),
   (3, 1, 1)),
  5,
  5,
  (2, 25, 5),
  ((1, 4, None), (14, 1, None), (10, 0, 5))),
 ('RICH-j3-p1',
  1,
  4,
  2,
  3,
  ((0, 1, 6), (0, 2, 1), (1, 0, 6), (1, 2, 1), (2, 0, 1), (2, 1, 1)),
  7,
  1,
  (2, 13, 7),
  ((1, 6, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  1,
  4,
  3,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  5,
  5,
  (1, 9, 5),
  ((1, 5, None), (8, 0, 5))),
 ('RICH-j3-p1',
  2,
  0,
  1,
  5,
  ((0, 1, 5),
   (1, 0, 5),
   (1, 2, 2),
   (1, 3, 1),
   (1, 4, 3),
   (2, 1, 2),
   (3, 1, 1),
   (3, 4, 1),
   (4, 1, 3),
   (4, 3, 1)),
  5,
  1,
  (1, 3, 5),
  ((1, 5, None), (2, 0, 1))),
 ('RICH-j3-p1',
  2,
  0,
  2,
  4,
  ((0, 1, 5), (1, 0, 5), (1, 2, 1), (1, 3, 3), (2, 1, 1), (2, 3, 1), (3, 1, 3), (3, 2, 1)),
  5,
  1,
  (1, 3, 5),
  ((1, 5, None), (2, 0, 1))),
 ('RICH-j3-p1',
  2,
  0,
  3,
  4,
  ((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 4), (2, 1, 2), (3, 1, 4)),
  5,
  1,
  (1, 3, 5),
  ((1, 5, None), (2, 0, 1))),
 ('RICH-j3-p1',
  2,
  0,
  4,
  4,
  ((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2)),
  5,
  1,
  (1, 3, 5),
  ((1, 5, None), (2, 0, 1))),
 ('RICH-j3-p1',
  2,
  2,
  1,
  4,
  ((0, 1, 7), (1, 0, 7), (1, 2, 1), (1, 3, 3), (2, 1, 1), (2, 3, 1), (3, 1, 3), (3, 2, 1)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  2,
  2,
  3,
  3,
  ((0, 1, 7), (1, 0, 7), (1, 2, 4), (2, 1, 4)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  2,
  2,
  4,
  3,
  ((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  2,
  3,
  1,
  4,
  ((0, 1, 6), (0, 3, 1), (1, 0, 6), (1, 2, 2), (1, 3, 3), (2, 1, 2), (3, 0, 1), (3, 1, 3)),
  7,
  1,
  (2, 13, 7),
  ((1, 6, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  2,
  3,
  2,
  3,
  ((0, 1, 6), (0, 2, 1), (1, 0, 6), (1, 2, 3), (2, 0, 1), (2, 1, 3)),
  7,
  1,
  (2, 13, 7),
  ((1, 6, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  2,
  3,
  4,
  3,
  ((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  2,
  4,
  1,
  4,
  ((0, 1, 8), (0, 3, 1), (1, 0, 8), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1)),
  9,
  1,
  (2, 13, 9),
  ((1, 8, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  2,
  4,
  2,
  3,
  ((0, 1, 8), (0, 2, 1), (1, 0, 8), (1, 2, 1), (2, 0, 1), (2, 1, 1)),
  9,
  1,
  (2, 13, 9),
  ((1, 8, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  2,
  4,
  3,
  3,
  ((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2)),
  9,
  1,
  (1, 3, 9),
  ((1, 9, None), (2, 0, 1))),
 ('RICH-j3-p1',
  3,
  0,
  1,
  5,
  ((0, 1, 2),
   (0, 2, 2),
   (0, 4, 1),
   (1, 0, 2),
   (1, 2, 0),
   (1, 3, 1),
   (1, 4, 2),
   (2, 0, 2),
   (2, 1, 0),
   (3, 1, 1),
   (3, 4, 1),
   (4, 0, 1),
   (4, 1, 2),
   (4, 3, 1)),
  3,
  5,
  (2, 26, 3),
  ((1, 2, None), (15, 1, None), (10, 0, 5))),
 ('RICH-j3-p1',
  3,
  0,
  2,
  4,
  ((0, 1, 4),
   (0, 3, 1),
   (1, 0, 4),
   (1, 2, 1),
   (1, 3, 2),
   (2, 1, 1),
   (2, 3, 1),
   (3, 0, 1),
   (3, 1, 2),
   (3, 2, 1)),
  5,
  1,
  (2, 14, 5),
  ((1, 4, None), (9, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  3,
  0,
  3,
  4,
  ((0, 1, 2),
   (0, 2, 2),
   (0, 3, 1),
   (1, 0, 2),
   (1, 2, 0),
   (1, 3, 3),
   (2, 0, 2),
   (2, 1, 0),
   (3, 0, 1),
   (3, 1, 3)),
  3,
  5,
  (2, 25, 3),
  ((1, 2, None), (14, 1, None), (10, 0, 5))),
 ('RICH-j3-p1',
  3,
  0,
  4,
  4,
  ((0, 1, 3), (0, 2, 2), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2)),
  3,
  5,
  (1, 9, 3),
  ((1, 3, None), (8, 0, 5))),
 ('RICH-j3-p1',
  3,
  2,
  1,
  4,
  ((0, 1, 2),
   (0, 3, 1),
   (1, 0, 2),
   (1, 2, 1),
   (1, 3, 2),
   (2, 1, 1),
   (2, 3, 1),
   (3, 0, 1),
   (3, 1, 2),
   (3, 2, 1)),
  3,
  1,
  (2, 14, 3),
  ((1, 2, None), (9, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  3,
  2,
  3,
  3,
  ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 3), (2, 0, 1), (2, 1, 3)),
  3,
  1,
  (2, 13, 3),
  ((1, 2, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  3,
  2,
  4,
  3,
  ((0, 1, 3), (1, 0, 3), (1, 2, 2), (2, 1, 2)),
  3,
  1,
  (1, 3, 3),
  ((1, 3, None), (2, 0, 1))),
 ('RICH-j3-p1',
  3,
  3,
  1,
  4,
  ((0, 1, 3),
   (0, 2, 2),
   (0, 3, 2),
   (1, 0, 3),
   (1, 2, 0),
   (1, 3, 2),
   (2, 0, 2),
   (2, 1, 0),
   (3, 0, 2),
   (3, 1, 2)),
  5,
  5,
  (2, 25, 5),
  ((1, 3, None), (14, 2, None), (10, 0, 5))),
 ('RICH-j3-p1',
  3,
  3,
  2,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 2), (2, 0, 2), (2, 1, 2)),
  7,
  1,
  (2, 13, 7),
  ((1, 5, None), (8, 2, None), (4, 0, 1))),
 ('RICH-j3-p1',
  3,
  3,
  4,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  5,
  5,
  (1, 9, 5),
  ((1, 5, None), (8, 0, 5))),
 ('RICH-j3-p1',
  3,
  4,
  1,
  4,
  ((0, 1, 4),
   (0, 2, 2),
   (0, 3, 1),
   (1, 0, 4),
   (1, 2, 0),
   (1, 3, 1),
   (2, 0, 2),
   (2, 1, 0),
   (3, 0, 1),
   (3, 1, 1)),
  5,
  5,
  (2, 25, 5),
  ((1, 4, None), (14, 1, None), (10, 0, 5))),
 ('RICH-j3-p1',
  3,
  4,
  2,
  3,
  ((0, 1, 6), (0, 2, 1), (1, 0, 6), (1, 2, 1), (2, 0, 1), (2, 1, 1)),
  7,
  1,
  (2, 13, 7),
  ((1, 6, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  3,
  4,
  3,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  5,
  5,
  (1, 9, 5),
  ((1, 5, None), (8, 0, 5))),
 ('RICH-j3-p1',
  4,
  0,
  1,
  5,
  ((0, 1, 1),
   (0, 2, 2),
   (0, 3, 2),
   (1, 0, 1),
   (1, 2, 0),
   (1, 3, 0),
   (1, 4, 2),
   (2, 0, 2),
   (2, 1, 0),
   (3, 0, 2),
   (3, 1, 0),
   (4, 1, 2)),
  1,
  13,
  (1, 15, 2),
  ((1, 1, None), (14, 0, 13))),
 ('RICH-j3-p1',
  4,
  0,
  2,
  4,
  ((0, 1, 3), (0, 2, 2), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2)),
  3,
  5,
  (1, 9, 3),
  ((1, 3, None), (8, 0, 5))),
 ('RICH-j3-p1',
  4,
  0,
  3,
  4,
  ((0, 1, 3), (0, 2, 2), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2)),
  3,
  5,
  (1, 9, 3),
  ((1, 3, None), (8, 0, 5))),
 ('RICH-j3-p1',
  4,
  0,
  4,
  4,
  ((0, 1, 1),
   (0, 2, 2),
   (0, 3, 2),
   (1, 0, 1),
   (1, 2, 0),
   (1, 3, 0),
   (2, 0, 2),
   (2, 1, 0),
   (3, 0, 2),
   (3, 1, 0)),
  1,
  13,
  (1, 15, 2),
  ((1, 1, None), (14, 0, 13))),
 ('RICH-j3-p1',
  4,
  2,
  1,
  4,
  ((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2)),
  1,
  5,
  (1, 9, 2),
  ((1, 1, None), (8, 0, 5))),
 ('RICH-j3-p1',
  4,
  2,
  3,
  3,
  ((0, 1, 3), (1, 0, 3), (1, 2, 2), (2, 1, 2)),
  3,
  1,
  (1, 3, 3),
  ((1, 3, None), (2, 0, 1))),
 ('RICH-j3-p1',
  4,
  2,
  4,
  3,
  ((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  1,
  5,
  (1, 9, 2),
  ((1, 1, None), (8, 0, 5))),
 ('RICH-j3-p1',
  4,
  3,
  1,
  4,
  ((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2)),
  1,
  5,
  (1, 9, 2),
  ((1, 1, None), (8, 0, 5))),
 ('RICH-j3-p1',
  4,
  3,
  2,
  3,
  ((0, 1, 3), (1, 0, 3), (1, 2, 2), (2, 1, 2)),
  3,
  1,
  (1, 3, 3),
  ((1, 3, None), (2, 0, 1))),
 ('RICH-j3-p1',
  4,
  3,
  4,
  3,
  ((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  1,
  5,
  (1, 9, 2),
  ((1, 1, None), (8, 0, 5))),
 ('RICH-j3-p1',
  4,
  4,
  1,
  4,
  ((0, 1, 3),
   (0, 2, 2),
   (0, 3, 2),
   (1, 0, 3),
   (1, 2, 0),
   (1, 3, 0),
   (2, 0, 2),
   (2, 1, 0),
   (3, 0, 2),
   (3, 1, 0)),
  3,
  13,
  (1, 15, 3),
  ((1, 3, None), (14, 0, 13))),
 ('RICH-j3-p1',
  4,
  4,
  2,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  5,
  5,
  (1, 9, 5),
  ((1, 5, None), (8, 0, 5))),
 ('RICH-j3-p1',
  4,
  4,
  3,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  5,
  5,
  (1, 9, 5),
  ((1, 5, None), (8, 0, 5))),
 ('RICH-j3-p1',
  5,
  0,
  1,
  5,
  ((0, 1, 6),
   (0, 4, 1),
   (1, 0, 6),
   (1, 2, 2),
   (1, 3, 2),
   (1, 4, 1),
   (2, 1, 2),
   (3, 1, 2),
   (4, 0, 1),
   (4, 1, 1)),
  7,
  1,
  (2, 13, 7),
  ((1, 6, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  5,
  0,
  2,
  4,
  ((0, 1, 6), (0, 3, 1), (1, 0, 6), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1)),
  7,
  1,
  (2, 13, 7),
  ((1, 6, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  5,
  0,
  3,
  4,
  ((0, 1, 6), (0, 3, 1), (1, 0, 6), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1)),
  7,
  1,
  (2, 13, 7),
  ((1, 6, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  5,
  0,
  4,
  4,
  ((0, 1, 7), (1, 0, 7), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  5,
  2,
  1,
  4,
  ((0, 1, 8), (0, 3, 1), (1, 0, 8), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1)),
  9,
  1,
  (2, 13, 9),
  ((1, 8, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  5,
  2,
  3,
  3,
  ((0, 1, 8), (0, 2, 1), (1, 0, 8), (1, 2, 1), (2, 0, 1), (2, 1, 1)),
  9,
  1,
  (2, 13, 9),
  ((1, 8, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  5,
  2,
  4,
  3,
  ((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2)),
  9,
  1,
  (1, 3, 9),
  ((1, 9, None), (2, 0, 1))),
 ('RICH-j3-p1',
  5,
  3,
  1,
  4,
  ((0, 1, 8), (0, 3, 1), (1, 0, 8), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1)),
  9,
  1,
  (2, 13, 9),
  ((1, 8, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  5,
  3,
  2,
  3,
  ((0, 1, 8), (0, 2, 1), (1, 0, 8), (1, 2, 1), (2, 0, 1), (2, 1, 1)),
  9,
  1,
  (2, 13, 9),
  ((1, 8, None), (8, 1, None), (4, 0, 1))),
 ('RICH-j3-p1',
  5,
  3,
  4,
  3,
  ((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2)),
  9,
  1,
  (1, 3, 9),
  ((1, 9, None), (2, 0, 1))),
 ('RICH-j3-p1',
  5,
  4,
  1,
  4,
  ((0, 1, 7), (1, 0, 7), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  5,
  4,
  2,
  3,
  ((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  5,
  4,
  3,
  3,
  ((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  6,
  0,
  1,
  5,
  ((0, 1, 2),
   (0, 4, 3),
   (1, 0, 2),
   (1, 2, 0),
   (1, 3, 0),
   (1, 4, 1),
   (2, 1, 0),
   (2, 4, 2),
   (3, 1, 0),
   (3, 4, 2),
   (4, 0, 3),
   (4, 1, 1),
   (4, 2, 2),
   (4, 3, 2)),
  3,
  29,
  (2, 31, 3),
  ((1, 2, None), (10, 1, None), (20, 0, 29))),
 ('RICH-j3-p1',
  6,
  0,
  2,
  4,
  ((0, 1, 2),
   (0, 3, 3),
   (1, 0, 2),
   (1, 2, 0),
   (1, 3, 3),
   (2, 1, 0),
   (2, 3, 2),
   (3, 0, 3),
   (3, 1, 3),
   (3, 2, 2)),
  5,
  1,
  (2, 14, 5),
  ((1, 2, None), (9, 3, None), (4, 0, 1))),
 ('RICH-j3-p1',
  6,
  0,
  3,
  4,
  ((0, 1, 2),
   (0, 3, 3),
   (1, 0, 2),
   (1, 2, 0),
   (1, 3, 3),
   (2, 1, 0),
   (2, 3, 2),
   (3, 0, 3),
   (3, 1, 3),
   (3, 2, 2)),
  5,
  1,
  (2, 14, 5),
  ((1, 2, None), (9, 3, None), (4, 0, 1))),
 ('RICH-j3-p1',
  6,
  0,
  4,
  4,
  ((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2)),
  5,
  1,
  (1, 3, 5),
  ((1, 5, None), (2, 0, 1))),
 ('RICH-j3-p1',
  6,
  2,
  1,
  4,
  ((0, 1, 2),
   (0, 3, 5),
   (1, 0, 2),
   (1, 2, 0),
   (1, 3, 1),
   (2, 1, 0),
   (2, 3, 2),
   (3, 0, 5),
   (3, 1, 1),
   (3, 2, 2)),
  3,
  13,
  (2, 24, 5),
  ((1, 2, None), (9, 1, None), (14, 0, 13))),
 ('RICH-j3-p1',
  6,
  2,
  3,
  3,
  ((0, 1, 2), (0, 2, 5), (1, 0, 2), (1, 2, 3), (2, 0, 5), (2, 1, 3)),
  5,
  5,
  (2, 17, 5),
  ((1, 2, None), (8, 3, None), (8, 0, 5))),
 ('RICH-j3-p1',
  6,
  2,
  4,
  3,
  ((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  6,
  3,
  1,
  4,
  ((0, 1, 2),
   (0, 3, 5),
   (1, 0, 2),
   (1, 2, 0),
   (1, 3, 1),
   (2, 1, 0),
   (2, 3, 2),
   (3, 0, 5),
   (3, 1, 1),
   (3, 2, 2)),
  3,
  13,
  (2, 24, 5),
  ((1, 2, None), (9, 1, None), (14, 0, 13))),
 ('RICH-j3-p1',
  6,
  3,
  2,
  3,
  ((0, 1, 2), (0, 2, 5), (1, 0, 2), (1, 2, 3), (2, 0, 5), (2, 1, 3)),
  5,
  5,
  (2, 17, 5),
  ((1, 2, None), (8, 3, None), (8, 0, 5))),
 ('RICH-j3-p1',
  6,
  3,
  4,
  3,
  ((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  6,
  4,
  1,
  4,
  ((0, 1, 3),
   (0, 2, 2),
   (0, 3, 2),
   (1, 0, 3),
   (1, 2, 0),
   (1, 3, 0),
   (2, 0, 2),
   (2, 1, 0),
   (3, 0, 2),
   (3, 1, 0)),
  3,
  13,
  (1, 15, 3),
  ((1, 3, None), (14, 0, 13))),
 ('RICH-j3-p1',
  6,
  4,
  2,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  5,
  5,
  (1, 9, 5),
  ((1, 5, None), (8, 0, 5))),
 ('RICH-j3-p1',
  6,
  4,
  3,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  5,
  5,
  (1, 9, 5),
  ((1, 5, None), (8, 0, 5))),
 ('RICH-j3-p1',
  7,
  0,
  1,
  5,
  ((0, 1, 3),
   (0, 4, 4),
   (1, 0, 3),
   (1, 2, 0),
   (1, 3, 0),
   (2, 1, 0),
   (2, 4, 2),
   (3, 1, 0),
   (3, 4, 2),
   (4, 0, 4),
   (4, 2, 2),
   (4, 3, 2)),
  3,
  29,
  (1, 19, 4),
  ((1, 3, None), (18, 0, 29))),
 ('RICH-j3-p1',
  7,
  0,
  2,
  4,
  ((0, 1, 3),
   (0, 3, 4),
   (1, 0, 3),
   (1, 2, 0),
   (1, 3, 2),
   (2, 1, 0),
   (2, 3, 2),
   (3, 0, 4),
   (3, 1, 2),
   (3, 2, 2)),
  5,
  13,
  (2, 24, 5),
  ((1, 3, None), (9, 2, None), (14, 0, 13))),
 ('RICH-j3-p1',
  7,
  0,
  3,
  4,
  ((0, 1, 3),
   (0, 3, 4),
   (1, 0, 3),
   (1, 2, 0),
   (1, 3, 2),
   (2, 1, 0),
   (2, 3, 2),
   (3, 0, 4),
   (3, 1, 2),
   (3, 2, 2)),
  5,
  13,
  (2, 24, 5),
  ((1, 3, None), (9, 2, None), (14, 0, 13))),
 ('RICH-j3-p1',
  7,
  0,
  4,
  4,
  ((0, 1, 7), (1, 0, 7), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2)),
  7,
  1,
  (1, 3, 7),
  ((1, 7, None), (2, 0, 1))),
 ('RICH-j3-p1',
  7,
  2,
  1,
  4,
  ((0, 1, 3), (0, 3, 6), (1, 0, 3), (1, 2, 0), (2, 1, 0), (2, 3, 2), (3, 0, 6), (3, 2, 2)),
  3,
  13,
  (1, 13, 6),
  ((1, 3, None), (12, 0, 13))),
 ('RICH-j3-p1',
  7,
  2,
  3,
  3,
  ((0, 1, 3), (0, 2, 6), (1, 0, 3), (1, 2, 2), (2, 0, 6), (2, 1, 2)),
  5,
  5,
  (2, 17, 6),
  ((1, 3, None), (8, 2, None), (8, 0, 5))),
 ('RICH-j3-p1',
  7,
  2,
  4,
  3,
  ((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2)),
  9,
  1,
  (1, 3, 9),
  ((1, 9, None), (2, 0, 1))),
 ('RICH-j3-p1',
  7,
  3,
  1,
  4,
  ((0, 1, 3), (0, 3, 6), (1, 0, 3), (1, 2, 0), (2, 1, 0), (2, 3, 2), (3, 0, 6), (3, 2, 2)),
  3,
  13,
  (1, 13, 6),
  ((1, 3, None), (12, 0, 13))),
 ('RICH-j3-p1',
  7,
  3,
  2,
  3,
  ((0, 1, 3), (0, 2, 6), (1, 0, 3), (1, 2, 2), (2, 0, 6), (2, 1, 2)),
  5,
  5,
  (2, 17, 6),
  ((1, 3, None), (8, 2, None), (8, 0, 5))),
 ('RICH-j3-p1',
  7,
  3,
  4,
  3,
  ((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2)),
  9,
  1,
  (1, 3, 9),
  ((1, 9, None), (2, 0, 1))),
 ('RICH-j3-p1',
  7,
  4,
  1,
  4,
  ((0, 1, 3),
   (0, 2, 2),
   (0, 3, 2),
   (1, 0, 3),
   (1, 2, 0),
   (1, 3, 0),
   (2, 0, 2),
   (2, 1, 0),
   (3, 0, 2),
   (3, 1, 0)),
  3,
  13,
  (1, 15, 3),
  ((1, 3, None), (14, 0, 13))),
 ('RICH-j3-p1',
  7,
  4,
  2,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  5,
  5,
  (1, 9, 5),
  ((1, 5, None), (8, 0, 5))),
 ('RICH-j3-p1',
  7,
  4,
  3,
  3,
  ((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0)),
  5,
  5,
  (1, 9, 5),
  ((1, 5, None), (8, 0, 5))))

# VALID_RECORDS: type, constructor_arguments
VALID_RECORDS = (('BranchOracleResult', (1, 0, 1, 0)),
 ('BranchOracleResult', (3, -4, 2, -4)),
 ('BranchOracleResult', (1, 6, 4, 2)),
 ('BranchOracleResult', (1361129467683753853853498429727072845824, -2, 2, -2)),
 ('BranchOracleStats', (0, 0, 0, 0, 0, 0, 0)),
 ('BranchOracleStats', (1, 9, 7, 3, 11, 0, 0)),
 ('BranchOracleStats', (2, 0, 0, 0, 0, 0, 0)))

# REJECTIONS: case, target, field, symbolic_substitution, exact_exception, precondition
REJECTIONS = (('V001',
  'BranchOracleContext',
  'instance',
  'None',
  'ValueError',
  'all earlier arguments valid'),
 ('V002',
  'BranchOracleContext',
  'instance',
  'True',
  'ValueError',
  'all earlier arguments valid'),
 ('V003',
  'BranchOracleContext',
  'instance',
  '1.0',
  'ValueError',
  'all earlier arguments valid'),
 ('V004',
  'BranchOracleContext',
  'instance',
  'Fraction(1,1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V005',
  'BranchOracleContext',
  'instance',
  'ExactValue(1,1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V006',
  'BranchOracleContext',
  'instance',
  'INT_SUB(1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V007',
  'BranchOracleContext',
  'instance',
  'HOSTILE',
  'ValueError',
  'all earlier arguments valid'),
 ('V008',
  'BranchOracleContext',
  'instance',
  'BruteInstance',
  'ValueError',
  'all earlier arguments valid'),
 ('V009',
  'BranchOracleContext',
  'instance',
  'INSTANCE_SUB',
  'ValueError',
  'all earlier arguments valid'),
 ('V010', 'BranchOracleResult', 'shore', 'True', 'ValueError', 'all earlier arguments valid'),
 ('V011', 'BranchOracleResult', 'shore', '1.0', 'ValueError', 'all earlier arguments valid'),
 ('V012',
  'BranchOracleResult',
  'shore',
  'Fraction(1,1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V013',
  'BranchOracleResult',
  'shore',
  'INT_SUB(1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V014',
  'BranchOracleResult',
  'shore',
  'HOSTILE',
  'ValueError',
  'all earlier arguments valid'),
 ('V015', 'BranchOracleResult', 'shore', 'None', 'ValueError', 'all earlier arguments valid'),
 ('V016', 'BranchOracleResult', 'shore', '0', 'ValueError', 'all earlier arguments valid'),
 ('V017', 'BranchOracleResult', 'shore', '-1', 'ValueError', 'all earlier arguments valid'),
 ('V018', 'BranchOracleResult', 'c', 'True', 'ValueError', 'all earlier arguments valid'),
 ('V019', 'BranchOracleResult', 'c', '1.0', 'ValueError', 'all earlier arguments valid'),
 ('V020',
  'BranchOracleResult',
  'c',
  'Fraction(1,1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V021', 'BranchOracleResult', 'c', 'INT_SUB(1)', 'ValueError', 'all earlier arguments valid'),
 ('V022', 'BranchOracleResult', 'c', 'HOSTILE', 'ValueError', 'all earlier arguments valid'),
 ('V023', 'BranchOracleResult', 'c', 'None', 'ValueError', 'all earlier arguments valid'),
 ('V024', 'BranchOracleResult', 'h', 'True', 'ValueError', 'all earlier arguments valid'),
 ('V025', 'BranchOracleResult', 'h', '1.0', 'ValueError', 'all earlier arguments valid'),
 ('V026',
  'BranchOracleResult',
  'h',
  'Fraction(1,1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V027', 'BranchOracleResult', 'h', 'INT_SUB(1)', 'ValueError', 'all earlier arguments valid'),
 ('V028', 'BranchOracleResult', 'h', 'HOSTILE', 'ValueError', 'all earlier arguments valid'),
 ('V029', 'BranchOracleResult', 'h', 'None', 'ValueError', 'all earlier arguments valid'),
 ('V030', 'BranchOracleResult', 'h', '0', 'ValueError', 'all earlier arguments valid'),
 ('V031', 'BranchOracleResult', 'h', '-1', 'ValueError', 'all earlier arguments valid'),
 ('V032',
  'BranchOracleResult',
  'residual',
  'True',
  'ValueError',
  'all earlier arguments valid'),
 ('V033', 'BranchOracleResult', 'residual', '1.0', 'ValueError', 'all earlier arguments valid'),
 ('V034',
  'BranchOracleResult',
  'residual',
  'Fraction(1,1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V035',
  'BranchOracleResult',
  'residual',
  'INT_SUB(1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V036',
  'BranchOracleResult',
  'residual',
  'HOSTILE',
  'ValueError',
  'all earlier arguments valid'),
 ('V037',
  'BranchOracleResult',
  'residual',
  'None',
  'ValueError',
  'all earlier arguments valid'),
 ('V038',
  'BranchOracleStats',
  'atomic_families_examined',
  '-1',
  'ValueError',
  'all earlier arguments valid'),
 ('V039',
  'BranchOracleStats',
  'atomic_families_examined',
  'True',
  'ValueError',
  'all earlier arguments valid'),
 ('V040',
  'BranchOracleStats',
  'atomic_families_examined',
  '1.0',
  'ValueError',
  'all earlier arguments valid'),
 ('V041',
  'BranchOracleStats',
  'atomic_families_examined',
  'INT_SUB(1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V042',
  'BranchOracleStats',
  'atomic_families_examined',
  'HOSTILE',
  'ValueError',
  'all earlier arguments valid'),
 ('V043',
  'BranchOracleStats',
  'atomic_families_feasible',
  '-1',
  'ValueError',
  'all earlier arguments valid'),
 ('V044',
  'BranchOracleStats',
  'atomic_families_feasible',
  'True',
  'ValueError',
  'all earlier arguments valid'),
 ('V045',
  'BranchOracleStats',
  'atomic_families_feasible',
  '1.0',
  'ValueError',
  'all earlier arguments valid'),
 ('V046',
  'BranchOracleStats',
  'atomic_families_feasible',
  'INT_SUB(1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V047',
  'BranchOracleStats',
  'atomic_families_feasible',
  'HOSTILE',
  'ValueError',
  'all earlier arguments valid'),
 ('V048',
  'BranchOracleStats',
  'parity_cut_calls',
  '-1',
  'ValueError',
  'all earlier arguments valid'),
 ('V049',
  'BranchOracleStats',
  'parity_cut_calls',
  'True',
  'ValueError',
  'all earlier arguments valid'),
 ('V050',
  'BranchOracleStats',
  'parity_cut_calls',
  '1.0',
  'ValueError',
  'all earlier arguments valid'),
 ('V051',
  'BranchOracleStats',
  'parity_cut_calls',
  'INT_SUB(1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V052',
  'BranchOracleStats',
  'parity_cut_calls',
  'HOSTILE',
  'ValueError',
  'all earlier arguments valid'),
 ('V053',
  'BranchOracleStats',
  'ordinary_min_cut_calls',
  '-1',
  'ValueError',
  'all earlier arguments valid'),
 ('V054',
  'BranchOracleStats',
  'ordinary_min_cut_calls',
  'True',
  'ValueError',
  'all earlier arguments valid'),
 ('V055',
  'BranchOracleStats',
  'ordinary_min_cut_calls',
  '1.0',
  'ValueError',
  'all earlier arguments valid'),
 ('V056',
  'BranchOracleStats',
  'ordinary_min_cut_calls',
  'INT_SUB(1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V057',
  'BranchOracleStats',
  'ordinary_min_cut_calls',
  'HOSTILE',
  'ValueError',
  'all earlier arguments valid'),
 ('V058',
  'BranchOracleStats',
  'flow_augmentations',
  '-1',
  'ValueError',
  'all earlier arguments valid'),
 ('V059',
  'BranchOracleStats',
  'flow_augmentations',
  'True',
  'ValueError',
  'all earlier arguments valid'),
 ('V060',
  'BranchOracleStats',
  'flow_augmentations',
  '1.0',
  'ValueError',
  'all earlier arguments valid'),
 ('V061',
  'BranchOracleStats',
  'flow_augmentations',
  'INT_SUB(1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V062',
  'BranchOracleStats',
  'flow_augmentations',
  'HOSTILE',
  'ValueError',
  'all earlier arguments valid'),
 ('V063',
  'BranchOracleStats',
  'flow_bfs_scans',
  '-1',
  'ValueError',
  'all earlier arguments valid'),
 ('V064',
  'BranchOracleStats',
  'flow_bfs_scans',
  'True',
  'ValueError',
  'all earlier arguments valid'),
 ('V065',
  'BranchOracleStats',
  'flow_bfs_scans',
  '1.0',
  'ValueError',
  'all earlier arguments valid'),
 ('V066',
  'BranchOracleStats',
  'flow_bfs_scans',
  'INT_SUB(1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V067',
  'BranchOracleStats',
  'flow_bfs_scans',
  'HOSTILE',
  'ValueError',
  'all earlier arguments valid'),
 ('V068',
  'BranchOracleStats',
  'flow_peak_generated_value',
  '-1',
  'ValueError',
  'all earlier arguments valid'),
 ('V069',
  'BranchOracleStats',
  'flow_peak_generated_value',
  'True',
  'ValueError',
  'all earlier arguments valid'),
 ('V070',
  'BranchOracleStats',
  'flow_peak_generated_value',
  '1.0',
  'ValueError',
  'all earlier arguments valid'),
 ('V071',
  'BranchOracleStats',
  'flow_peak_generated_value',
  'INT_SUB(1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V072',
  'BranchOracleStats',
  'flow_peak_generated_value',
  'HOSTILE',
  'ValueError',
  'all earlier arguments valid'),
 ('V073', 'exact_branch_min', 'context', 'None', 'ValueError', 'all earlier arguments valid'),
 ('V074',
  'exact_branch_min',
  'context',
  'Instance(Q1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V075',
  'exact_branch_min',
  'context',
  'CONTEXT_SUB(Q1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V076',
  'exact_branch_min',
  'context',
  'HOSTILE',
  'ValueError',
  'all earlier arguments valid'),
 ('V077', 'exact_branch_min', 'context', '()', 'ValueError', 'all earlier arguments valid'),
 ('V078', 'exact_branch_min', 'branch', '-1', 'ValueError', 'all earlier arguments valid'),
 ('V079', 'exact_branch_min', 'branch', '4', 'ValueError', 'all earlier arguments valid'),
 ('V080', 'exact_branch_min', 'branch', 'True', 'ValueError', 'all earlier arguments valid'),
 ('V081', 'exact_branch_min', 'branch', '1.0', 'ValueError', 'all earlier arguments valid'),
 ('V082',
  'exact_branch_min',
  'branch',
  'INT_SUB(1)',
  'ValueError',
  'all earlier arguments valid'),
 ('V083', 'exact_branch_min', 'branch', 'HOSTILE', 'ValueError', 'all earlier arguments valid'),
 ('V084',
  'exact_branch_min',
  'parameter',
  'None',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V085',
  'exact_branch_min',
  'parameter',
  'True',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V086',
  'exact_branch_min',
  'parameter',
  '1.0',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V087',
  'exact_branch_min',
  'parameter',
  'Fraction(1,2)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V088',
  'exact_branch_min',
  'parameter',
  'ExactValue(1,2)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V089',
  'exact_branch_min',
  'parameter',
  '[1,2]',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V090',
  'exact_branch_min',
  'parameter',
  'ITERATOR((1,2))',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V091',
  'exact_branch_min',
  'parameter',
  'TUPLE_SUB((1,2))',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V092',
  'exact_branch_min',
  'parameter',
  '()',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V093',
  'exact_branch_min',
  'parameter',
  '(1,)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V094',
  'exact_branch_min',
  'parameter',
  '(1,2,3)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V095',
  'exact_branch_min',
  'parameter',
  '(True,1)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V096',
  'exact_branch_min',
  'parameter',
  '(1,True)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V097',
  'exact_branch_min',
  'parameter',
  '(INT_SUB(1),1)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V098',
  'exact_branch_min',
  'parameter',
  '(1,INT_SUB(1))',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V099',
  'exact_branch_min',
  'parameter',
  '(1.0,1)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V100',
  'exact_branch_min',
  'parameter',
  '(1,1.0)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V101',
  'exact_branch_min',
  'parameter',
  '(HOSTILE,1)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V102',
  'exact_branch_min',
  'parameter',
  '(1,HOSTILE)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V103',
  'exact_branch_min',
  'parameter',
  '(0,0)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V104',
  'exact_branch_min',
  'parameter',
  '(1,-1)',
  'ValueError',
  'normal Q1 context; branch=0; empty source domain'),
 ('V105',
  'exact_branch_min',
  'parameter',
  'None',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V106',
  'exact_branch_min',
  'parameter',
  'True',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V107',
  'exact_branch_min',
  'parameter',
  '1.0',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V108',
  'exact_branch_min',
  'parameter',
  'Fraction(1,2)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V109',
  'exact_branch_min',
  'parameter',
  'ExactValue(1,2)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V110',
  'exact_branch_min',
  'parameter',
  '[1,2]',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V111',
  'exact_branch_min',
  'parameter',
  'ITERATOR((1,2))',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V112',
  'exact_branch_min',
  'parameter',
  'TUPLE_SUB((1,2))',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V113',
  'exact_branch_min',
  'parameter',
  '()',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V114',
  'exact_branch_min',
  'parameter',
  '(1,)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V115',
  'exact_branch_min',
  'parameter',
  '(1,2,3)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V116',
  'exact_branch_min',
  'parameter',
  '(True,1)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V117',
  'exact_branch_min',
  'parameter',
  '(1,True)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V118',
  'exact_branch_min',
  'parameter',
  '(INT_SUB(1),1)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V119',
  'exact_branch_min',
  'parameter',
  '(1,INT_SUB(1))',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V120',
  'exact_branch_min',
  'parameter',
  '(1.0,1)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V121',
  'exact_branch_min',
  'parameter',
  '(1,1.0)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V122',
  'exact_branch_min',
  'parameter',
  '(HOSTILE,1)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V123',
  'exact_branch_min',
  'parameter',
  '(1,HOSTILE)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V124',
  'exact_branch_min',
  'parameter',
  '(0,0)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V125',
  'exact_branch_min',
  'parameter',
  '(1,-1)',
  'ValueError',
  'normal Q1 context; branch=1; empty source domain'),
 ('V126',
  'exact_branch_min',
  'parameter',
  'None',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V127',
  'exact_branch_min',
  'parameter',
  'True',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V128',
  'exact_branch_min',
  'parameter',
  '1.0',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V129',
  'exact_branch_min',
  'parameter',
  'Fraction(1,2)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V130',
  'exact_branch_min',
  'parameter',
  'ExactValue(1,2)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V131',
  'exact_branch_min',
  'parameter',
  '[1,2]',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V132',
  'exact_branch_min',
  'parameter',
  'ITERATOR((1,2))',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V133',
  'exact_branch_min',
  'parameter',
  'TUPLE_SUB((1,2))',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V134',
  'exact_branch_min',
  'parameter',
  '()',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V135',
  'exact_branch_min',
  'parameter',
  '(1,)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V136',
  'exact_branch_min',
  'parameter',
  '(1,2,3)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V137',
  'exact_branch_min',
  'parameter',
  '(True,1)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V138',
  'exact_branch_min',
  'parameter',
  '(1,True)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V139',
  'exact_branch_min',
  'parameter',
  '(INT_SUB(1),1)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V140',
  'exact_branch_min',
  'parameter',
  '(1,INT_SUB(1))',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V141',
  'exact_branch_min',
  'parameter',
  '(1.0,1)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V142',
  'exact_branch_min',
  'parameter',
  '(1,1.0)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V143',
  'exact_branch_min',
  'parameter',
  '(HOSTILE,1)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V144',
  'exact_branch_min',
  'parameter',
  '(1,HOSTILE)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V145',
  'exact_branch_min',
  'parameter',
  '(0,0)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V146',
  'exact_branch_min',
  'parameter',
  '(1,-1)',
  'ValueError',
  'normal Q1 context; branch=2; empty source domain'),
 ('V147',
  'exact_branch_min',
  'parameter',
  'None',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V148',
  'exact_branch_min',
  'parameter',
  'True',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V149',
  'exact_branch_min',
  'parameter',
  '1.0',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V150',
  'exact_branch_min',
  'parameter',
  'Fraction(1,2)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V151',
  'exact_branch_min',
  'parameter',
  'ExactValue(1,2)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V152',
  'exact_branch_min',
  'parameter',
  '[1,2]',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V153',
  'exact_branch_min',
  'parameter',
  'ITERATOR((1,2))',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V154',
  'exact_branch_min',
  'parameter',
  'TUPLE_SUB((1,2))',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V155',
  'exact_branch_min',
  'parameter',
  '()',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V156',
  'exact_branch_min',
  'parameter',
  '(1,)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V157',
  'exact_branch_min',
  'parameter',
  '(1,2,3)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V158',
  'exact_branch_min',
  'parameter',
  '(True,1)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V159',
  'exact_branch_min',
  'parameter',
  '(1,True)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V160',
  'exact_branch_min',
  'parameter',
  '(INT_SUB(1),1)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V161',
  'exact_branch_min',
  'parameter',
  '(1,INT_SUB(1))',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V162',
  'exact_branch_min',
  'parameter',
  '(1.0,1)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V163',
  'exact_branch_min',
  'parameter',
  '(1,1.0)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V164',
  'exact_branch_min',
  'parameter',
  '(HOSTILE,1)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V165',
  'exact_branch_min',
  'parameter',
  '(1,HOSTILE)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V166',
  'exact_branch_min',
  'parameter',
  '(0,0)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V167',
  'exact_branch_min',
  'parameter',
  '(1,-1)',
  'ValueError',
  'normal Q1 context; branch=3; empty source domain'),
 ('V168',
  'exact_branch_min',
  'parameter',
  '(0,0)',
  'ValueError',
  'normal MIXED context; branch=1; nonempty source domain'),
 ('V169',
  'exact_branch_min',
  'parameter',
  '(1,-1)',
  'ValueError',
  'normal MIXED context; branch=1; nonempty source domain'),
 ('V170',
  'exact_branch_min',
  'parameter',
  '[1,2]',
  'ValueError',
  'normal MIXED context; branch=1; nonempty source domain'),
 ('V171',
  'exact_branch_min',
  'parameter',
  '(True,1)',
  'ValueError',
  'normal MIXED context; branch=1; nonempty source domain'),
 ('V172',
  'BranchOracleContext',
  'call or mutation',
  'extra families=()',
  'TypeError',
  'normal Python behavior; not exact-ValueError data guard'),
 ('V173',
  'BranchOracleContext',
  'call or mutation',
  'missing instance',
  'TypeError',
  'normal Python behavior; not exact-ValueError data guard'),
 ('V174',
  'BranchOracleResult',
  'call or mutation',
  'missing residual',
  'TypeError',
  'normal Python behavior; not exact-ValueError data guard'),
 ('V175',
  'BranchOracleStats',
  'call or mutation',
  'extra max_flow_calls=0',
  'TypeError',
  'normal Python behavior; not exact-ValueError data guard'),
 ('V176',
  'exact_branch_min',
  'call or mutation',
  'missing parameter',
  'TypeError',
  'normal Python behavior; not exact-ValueError data guard'),
 ('V177',
  'normal context',
  'call or mutation',
  'assign families=()',
  'FrozenInstanceError',
  'normal Python behavior; not exact-ValueError data guard'),
 ('V178',
  'normal result',
  'call or mutation',
  'assign h=1',
  'FrozenInstanceError',
  'normal Python behavior; not exact-ValueError data guard'),
 ('V179',
  'normal stats',
  'call or mutation',
  'assign ordinary_min_cut_calls=1',
  'FrozenInstanceError',
  'normal Python behavior; not exact-ValueError data guard'))

# FAILURES: case, substitution, precondition, required_outcome, boundary
FAILURES = (('F01',
  'reduce_atomic_family returns None',
  'known-nonempty descriptor',
  'RuntimeError',
  'do not skip; do not return infeasible'),
 ('F02',
  'minimum_parity_cut returns (None, legal_stats)',
  'known-nonempty reduced problem',
  'RuntimeError',
  'do not skip; no completed stats/result'),
 ('F03',
  'lifting yields finite mask missing forced vertex',
  'candidate I-membership false',
  'RuntimeError',
  'before original residual comparison'),
 ('F04',
  'lifting yields finite mask with forbidden vertex',
  'candidate O-membership false',
  'RuntimeError',
  'before original residual comparison'),
 ('F05',
  'lifting yields finite wrong parity mask',
  'candidate parity false',
  'RuntimeError',
  'before original residual comparison'),
 ('F06',
  'original-sum seam yields failed D_j condition',
  'type-correct closed-sum substitution',
  'RuntimeError',
  'before raw residual/recovery retention'),
 ('F07',
  'original-sum seam yields h<=0',
  'explicit promise failure',
  'RuntimeError',
  'no make_pair repair or sign flip'),
 ('F08',
  'recovered objective differs from B*c-A*h',
  'well-formed candidate and nonnegative cut value',
  'RuntimeError',
  'even if false recovered value looks smaller'),
 ('F09',
  'closed reduction raises backend sentinel',
  'dependency call exception',
  'same exception propagates',
  'no blanket ValueError/None conversion'),
 ('F10',
  'closed minimum raises backend sentinel',
  'dependency call exception',
  'same exception propagates',
  'no false infeasibility'),
 ('F11',
  'lifting/universe validator raises ValueError',
  'out-of-universe mask',
  'same exception propagates',
  'not converted to None/RuntimeError'),
 ('F12',
  'different legal stats from backend',
  'identical legal exact optimum',
  'same result; altered aggregate stats',
  'stats never select candidate'),
 ('F13',
  'legal alternative exact within-family minimizer',
  'matching source/cut identity',
  'exact value and family/domain retained',
  'engineering winner may follow supplied legal candidate; no least-branch claim'),
 ('F14',
  'attempt supplied incomplete cover',
  'ordinary context constructor',
  'TypeError',
  'no accepted families injection API'))

# REUSE: step, query, result, count_prefix, fresh_original_network_if_feasible
REUSE = ((0, 'RICH-j0-p0', (1, 2, 2, 14), (1, 1, 1, 31), True),
 (1, 'RICH-j1-p7', (7, 2, 6, -10), (24, 17, 17, 149), True),
 (2, 'RICH-j2-p3', (23, -10, 4, -10), (5, 5, 5, 49), True),
 (3, 'RICH-j3-p1', (6, -6, 2, -2), (8, 8, 8, 104), True),
 (4, 'RICH-j1-p0', (3, 4, 2, 18), (24, 17, 17, 149), True),
 (5, 'RICH-j0-p4', (1, 2, 2, 6), (1, 1, 1, 31), True),
 (6, 'RICH-j1-p7', (7, 2, 6, -10), (24, 17, 17, 149), True),
 (7, 'RICH-j2-p9', (23, -10, 4, -58), (5, 5, 5, 49), True),
 (8, 'RICH-j3-p0', (6, -6, 2, -2), (8, 8, 8, 104), True))

# CORPUS_COUNTS: metric, value
CORPUS_COUNTS = (('all_empty_descriptor_queries', 1550),
 ('branch_domain_shore_checks', 10448),
 ('domain_memberships', 3354),
 ('empty_descriptors_once', 2736),
 ('family_descriptors_once', 6140),
 ('family_examinations', 61400),
 ('feasible_family_calls', 34040),
 ('feasible_queries', 11370),
 ('full_shore_winners', 1825),
 ('infeasible_queries', 1790),
 ('instances', 329),
 ('multiple_original_argmins', 3271),
 ('n2_instances', 5),
 ('n3_instances', 324),
 ('negative_minima', 6218),
 ('positive_minima', 4357),
 ('queries', 13160),
 ('specified_ordinary_calls', 138720),
 ('zero_descriptor_queries', 240),
 ('zero_minima', 795))

# BRANCH_CORPUS_COUNTS: j, counts
BRANCH_CORPUS_COUNTS = ((0,
  {'all_empty_descriptor_queries': 680,
   'family_examinations': 3290,
   'feasible_family_calls': 2610,
   'feasible_queries': 2610,
   'full_shore_winners': 325,
   'infeasible_queries': 680,
   'multiple_original_argmins': 1047,
   'negative_minima': 694,
   'positive_minima': 1701,
   'queries': 3290,
   'specified_ordinary_calls': 33750,
   'zero_minima': 215}),
 (1,
  {'all_empty_descriptor_queries': 600,
   'family_examinations': 34040,
   'feasible_family_calls': 12360,
   'feasible_queries': 2470,
   'full_shore_winners': 0,
   'infeasible_queries': 820,
   'multiple_original_argmins': 667,
   'negative_minima': 561,
   'positive_minima': 1688,
   'queries': 3290,
   'specified_ordinary_calls': 26760,
   'zero_descriptor_queries': 220,
   'zero_minima': 221}),
 (2,
  {'all_empty_descriptor_queries': 250,
   'family_examinations': 6330,
   'feasible_family_calls': 5590,
   'feasible_queries': 3020,
   'full_shore_winners': 1500,
   'infeasible_queries': 270,
   'multiple_original_argmins': 647,
   'negative_minima': 2399,
   'positive_minima': 430,
   'queries': 3290,
   'specified_ordinary_calls': 37850,
   'zero_descriptor_queries': 20,
   'zero_minima': 191}),
 (3,
  {'all_empty_descriptor_queries': 20,
   'family_examinations': 17740,
   'feasible_family_calls': 13480,
   'feasible_queries': 3270,
   'full_shore_winners': 0,
   'infeasible_queries': 20,
   'multiple_original_argmins': 910,
   'negative_minima': 2564,
   'positive_minima': 538,
   'queries': 3290,
   'specified_ordinary_calls': 40360,
   'zero_minima': 168}))

# CORPUS_FINGERPRINT: encoding, sha256
CORPUS_FINGERPRINT = (('for serial, j, parameter: JSON compact '
  'tuple(serial,j,parameter,result,argmins,winner_family,counts) plus LF',
  '979de1a78b82b55c591d5f25e69e30c13838a88596f82acc15d9589dfc9ccd5e'),)

# LARGE_CASES: q_exponent, j, A_B, original_shore_or_None, c_h_raw_bit_lengths, raw_sign,
# count_prefix, result_tuple_JSON_SHA256
LARGE_CASES = ((1,
  0,
  (-3, 2),
  1,
  (2, 2, 4),
  1,
  (1, 1, 1, 7),
  '87d0cec4a13ef282f70f1e3b5254291a98bc8eb353ee1dd2c3539396d3dc0721'),
 (1,
  0,
  (0, 7),
  1,
  (2, 2, 4),
  1,
  (1, 1, 1, 7),
  '4c7d5c8fe47bb66b9cad0d2feff0afd8ca77aeb6687cdf69e99e47dbfa5a7c45'),
 (1,
  0,
  (5, 3),
  1,
  (2, 2, 3),
  -1,
  (1, 1, 1, 7),
  'dff87bd6dc7a66596e742ea556539917a44a59db87d2389db17b3d2bf7f07d33'),
 (1,
  1,
  (-3, 2),
  None,
  None,
  None,
  (2, 0, 0, 0),
  '74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b'),
 (1,
  1,
  (0, 7),
  None,
  None,
  None,
  (2, 0, 0, 0),
  '74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b'),
 (1,
  1,
  (5, 3),
  None,
  None,
  None,
  (2, 0, 0, 0),
  '74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b'),
 (1,
  2,
  (-3, 2),
  3,
  (3, 2, 2),
  -1,
  (1, 1, 1, 3),
  '83a700c98940b400a70d6dabdbc24c5bcb60d320fd17dfa5285d2cd5dad09760'),
 (1,
  2,
  (0, 7),
  3,
  (3, 2, 5),
  -1,
  (1, 1, 1, 3),
  '169f1255c5621dea8ca0b1565d18c6bdbad6136b367981bcf045883b4c27b7f5'),
 (1,
  2,
  (5, 3),
  3,
  (3, 2, 5),
  -1,
  (1, 1, 1, 3),
  '8c66591343c5e58160108b726cee9b3deb55dee85339d61d6c57a89c543fb206'),
 (1,
  3,
  (-3, 2),
  2,
  (2, 2, 2),
  1,
  (2, 1, 1, 1),
  'fa0c5d32e239af9e641ba72de5edb96c1731fc6ebbd2120d49bd8f7858d9aed3'),
 (1,
  3,
  (0, 7),
  2,
  (2, 2, 4),
  -1,
  (2, 1, 1, 1),
  '5dfaf2a2211fae88fe8a1bac37afcc933351fa06fbc004b96edfaf8e9cf8da93'),
 (1,
  3,
  (5, 3),
  2,
  (2, 2, 5),
  -1,
  (2, 1, 1, 1),
  'fdac2271c941c36158f8167501e847f2ba2509450daab97d2b3005eaf4655186'),
 (2,
  0,
  (-3, 2),
  1,
  (3, 3, 5),
  1,
  (1, 1, 1, 7),
  '0b7ae91fa5bdab0958d3e859867c5dfe602047016013b6a0277d86b64b9f376e'),
 (2,
  0,
  (0, 7),
  3,
  (2, 3, 4),
  1,
  (1, 1, 1, 7),
  '200836be2e822db1637ab6213e143a3b414150f6761746f7e8266585fa259477'),
 (2,
  0,
  (5, 3),
  3,
  (2, 3, 5),
  -1,
  (1, 1, 1, 7),
  '9bb49ed8180327dc6db4a9100e15da1919c7d75f7ce1c57b6fdaadc408af1381'),
 (2,
  1,
  (-3, 2),
  2,
  (3, 2, 4),
  1,
  (4, 1, 1, 1),
  'e09af57b4e51551198dcd6aaae4e5ff12a1f370198676b41764db6bab04ccb4a'),
 (2,
  1,
  (0, 7),
  2,
  (3, 2, 5),
  1,
  (4, 1, 1, 1),
  'a069d1687d9920c3b24d27af3e81506b36d866e1e2df7c6b6cc1131d313a8bc0'),
 (2,
  1,
  (5, 3),
  2,
  (3, 2, 2),
  1,
  (4, 1, 1, 1),
  '35120a11505b4c7667e511de287ee9ab9716f87175fd392479e7e4461bfac11f'),
 (2,
  2,
  (-3, 2),
  3,
  (4, 2, 4),
  -1,
  (1, 1, 1, 3),
  '9733a10b94385cb3d4b99a9f120ebb02fc09261e7b28f32273a7725caf6d114c'),
 (2,
  2,
  (0, 7),
  3,
  (4, 2, 6),
  -1,
  (1, 1, 1, 3),
  '6c9ac9b73f8d0c8f2cc3520cda00654825bb2256926987533c7110910617c612'),
 (2,
  2,
  (5, 3),
  3,
  (4, 2, 6),
  -1,
  (1, 1, 1, 3),
  '8451ad428581b7dbdee45c64db5b14628aa44bf60ed1d4f013d80fad1501a46b'),
 (2,
  3,
  (-3, 2),
  2,
  (2, 2, 2),
  1,
  (2, 1, 1, 1),
  'fa0c5d32e239af9e641ba72de5edb96c1731fc6ebbd2120d49bd8f7858d9aed3'),
 (2,
  3,
  (0, 7),
  2,
  (2, 2, 4),
  -1,
  (2, 1, 1, 1),
  '5dfaf2a2211fae88fe8a1bac37afcc933351fa06fbc004b96edfaf8e9cf8da93'),
 (2,
  3,
  (5, 3),
  2,
  (2, 2, 5),
  -1,
  (2, 1, 1, 1),
  'fdac2271c941c36158f8167501e847f2ba2509450daab97d2b3005eaf4655186'),
 (8,
  0,
  (-3, 2),
  1,
  (9, 9, 11),
  1,
  (1, 1, 1, 7),
  '388fa820295fc17991c5205e0339f3d7c16353a4bdc645a3b63dfce9472e7fe4'),
 (8,
  0,
  (0, 7),
  3,
  (2, 9, 4),
  1,
  (1, 1, 1, 7),
  '8b0ab4d329cfba0b2fb86ecf088d6765206daffef961a701acf3c980c0664af8'),
 (8,
  0,
  (5, 3),
  3,
  (2, 9, 12),
  -1,
  (1, 1, 1, 7),
  'f2fb73e15d5ace84fc85678f6b61816874111bcf272b74316253026a2a54b9b9'),
 (8,
  1,
  (-3, 2),
  2,
  (9, 8, 11),
  1,
  (4, 1, 1, 1),
  '607c9c44512ba6a8015b2e4c67d22e5ca42d3e639f6a381c417f87c73210469a'),
 (8,
  1,
  (0, 7),
  2,
  (9, 8, 11),
  1,
  (4, 1, 1, 1),
  '3862bda2bce1def8b53f6aad8a382865ff24efae219c06b6cc9e80f104daa12f'),
 (8,
  1,
  (5, 3),
  2,
  (9, 8, 9),
  -1,
  (4, 1, 1, 1),
  '2739c4059015bc4160e8a5a07ba72d6a76c81e4e40096b1076d72a6e6524aade'),
 (8,
  2,
  (-3, 2),
  3,
  (10, 2, 10),
  -1,
  (1, 1, 1, 3),
  'f0250bf8adbb211e078bf2814b01ffe880de92421b772378b677c0500f401b9d'),
 (8,
  2,
  (0, 7),
  3,
  (10, 2, 12),
  -1,
  (1, 1, 1, 3),
  '1a267d44587bf8deb255f42755a4b641de09e726e674b4b73de1054fdd40d8dd'),
 (8,
  2,
  (5, 3),
  3,
  (10, 2, 11),
  -1,
  (1, 1, 1, 3),
  'c5a86d78a64f42bb50051ab1e778c8cdb83611c77c762c097fd3f2e99ce51e9f'),
 (8,
  3,
  (-3, 2),
  2,
  (2, 2, 2),
  1,
  (2, 1, 1, 1),
  'fa0c5d32e239af9e641ba72de5edb96c1731fc6ebbd2120d49bd8f7858d9aed3'),
 (8,
  3,
  (0, 7),
  2,
  (2, 2, 4),
  -1,
  (2, 1, 1, 1),
  '5dfaf2a2211fae88fe8a1bac37afcc933351fa06fbc004b96edfaf8e9cf8da93'),
 (8,
  3,
  (5, 3),
  2,
  (2, 2, 5),
  -1,
  (2, 1, 1, 1),
  'fdac2271c941c36158f8167501e847f2ba2509450daab97d2b3005eaf4655186'),
 (64,
  0,
  (-3, 2),
  1,
  (65, 65, 67),
  1,
  (1, 1, 1, 7),
  'b65f08ef0185b3eb93f2d8b265dd52803207bdea91df4a7d77c22e684e3ec68d'),
 (64,
  0,
  (0, 7),
  3,
  (2, 65, 4),
  1,
  (1, 1, 1, 7),
  'fb60f9ab996511489dd43b9da75add6568a70f5fb78ed347e65a5c83728feec4'),
 (64,
  0,
  (5, 3),
  3,
  (2, 65, 68),
  -1,
  (1, 1, 1, 7),
  '1d83e61f38b9c81e536e6c952960ca32f7a2c6dd1788a4a4389cefd0c8571df0'),
 (64,
  1,
  (-3, 2),
  2,
  (65, 64, 67),
  1,
  (4, 1, 1, 1),
  '1ead4a8f8876ed2a412d18928e03d50b471cc420b662ad12e488241cb0c848de'),
 (64,
  1,
  (0, 7),
  2,
  (65, 64, 67),
  1,
  (4, 1, 1, 1),
  'c7290de9ddaed612809abf5146ee1c7a2c67e01fe4db01e41a05464ec2343fd3'),
 (64,
  1,
  (5, 3),
  2,
  (65, 64, 65),
  -1,
  (4, 1, 1, 1),
  '52ad8ec495ce6f1be345934e04f2ee8543999cee627b8f975fe94cb7dd38eef2'),
 (64,
  2,
  (-3, 2),
  3,
  (66, 2, 66),
  -1,
  (1, 1, 1, 3),
  'f8f93a08f0e6a72e8063367412b605e0e0274a09f2e9920be4bc724eef223b44'),
 (64,
  2,
  (0, 7),
  3,
  (66, 2, 68),
  -1,
  (1, 1, 1, 3),
  '7c4f03c28a2f4869258b23327cc2fe7b60b2ec68d9085f977555eff86e27692e'),
 (64,
  2,
  (5, 3),
  3,
  (66, 2, 67),
  -1,
  (1, 1, 1, 3),
  '2b1e98d603a395d2ac3c711137c0b21881cdc5a5d4a75783f30a92724d0de064'),
 (64,
  3,
  (-3, 2),
  2,
  (2, 2, 2),
  1,
  (2, 1, 1, 1),
  'fa0c5d32e239af9e641ba72de5edb96c1731fc6ebbd2120d49bd8f7858d9aed3'),
 (64,
  3,
  (0, 7),
  2,
  (2, 2, 4),
  -1,
  (2, 1, 1, 1),
  '5dfaf2a2211fae88fe8a1bac37afcc933351fa06fbc004b96edfaf8e9cf8da93'),
 (64,
  3,
  (5, 3),
  2,
  (2, 2, 5),
  -1,
  (2, 1, 1, 1),
  'fdac2271c941c36158f8167501e847f2ba2509450daab97d2b3005eaf4655186'),
 (4096,
  0,
  (-3, 2),
  1,
  (4097, 4097, 4099),
  1,
  (1, 1, 1, 7),
  'ccba09c0bb5c17c76de45bf24f3e47d52ca598fc213477ff4044775cdf5860ce'),
 (4096,
  0,
  (0, 7),
  3,
  (2, 4097, 4),
  1,
  (1, 1, 1, 7),
  '9be2c4cbde9fd58578e77cc4282d808ed6864e3dd1291761dd0990343baa66f8'),
 (4096,
  0,
  (5, 3),
  3,
  (2, 4097, 4100),
  -1,
  (1, 1, 1, 7),
  '811b03524ee4edc1160978fb18c7cd3fa8c76ca80dbaa7f9a1b819216d047b07'),
 (4096,
  1,
  (-3, 2),
  2,
  (4097, 4096, 4099),
  1,
  (4, 1, 1, 1),
  '908bf67d74db375a58fc89a8bf7f8fe93dd3b27c49d1d64e49a8beb6b3547128'),
 (4096,
  1,
  (0, 7),
  2,
  (4097, 4096, 4099),
  1,
  (4, 1, 1, 1),
  'a2b4a2f36000be059b7c4694cb8aadb3b21cfb9b05dcd3178313ceb9196c155f'),
 (4096,
  1,
  (5, 3),
  2,
  (4097, 4096, 4097),
  -1,
  (4, 1, 1, 1),
  'd7c80f869152ca7b4544fcea7c563881317e9414e4e9d8177fa7192421d815ca'),
 (4096,
  2,
  (-3, 2),
  3,
  (4098, 2, 4098),
  -1,
  (1, 1, 1, 3),
  '1608fb42bf643413d79f450a6adcf4c75ef421ef88059c357020338a84ba7293'),
 (4096,
  2,
  (0, 7),
  3,
  (4098, 2, 4100),
  -1,
  (1, 1, 1, 3),
  'a38dbe4bf7a1f6a7a7e59194c50016e4d0b5ceb41c17659448fd68560f05ed3c'),
 (4096,
  2,
  (5, 3),
  3,
  (4098, 2, 4099),
  -1,
  (1, 1, 1, 3),
  'd4f20ebda329fce5a93f98b76fbc34278def6507949c8655c31b0cfdcee03cf0'),
 (4096,
  3,
  (-3, 2),
  2,
  (2, 2, 2),
  1,
  (2, 1, 1, 1),
  'fa0c5d32e239af9e641ba72de5edb96c1731fc6ebbd2120d49bd8f7858d9aed3'),
 (4096,
  3,
  (0, 7),
  2,
  (2, 2, 4),
  -1,
  (2, 1, 1, 1),
  '5dfaf2a2211fae88fe8a1bac37afcc933351fa06fbc004b96edfaf8e9cf8da93'),
 (4096,
  3,
  (5, 3),
  2,
  (2, 2, 5),
  -1,
  (2, 1, 1, 1),
  'fdac2271c941c36158f8167501e847f2ba2509450daab97d2b3005eaf4655186'))

# SCALE_COUNTS: raw_parameter_scale_checks, exponents
SCALE_COUNTS = ((20, (1, 2, 8, 64, 4096)),)

# PREPARATION_SEPARATION: n, edges, f, r0_r1_r2_r3, R_all, D0_parameter, D0_result, D0_counts
PREPARATION_SEPARATION = ((10,
  ((0, 1, 1),
   (0, 9, 1),
   (1, 2, 1),
   (2, 3, 1),
   (3, 4, 1),
   (4, 5, 1),
   (5, 6, 1),
   (6, 7, 1),
   (7, 8, 1),
   (8, 9, 1)),
  (1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
  (1, 200, 120, 20),
  341,
  (0, 1),
  (1, 2, 2, 2),
  (1, 1, 1, 111)),)


DATA = {name: (n, edges, f) for name, n, edges, f, _, _ in INPUTS}
PARAMS = tuple(parameter for _, parameter in PARAMETERS)
ROWS = {row[0]: row for row in MINIMA}
RESULT_FIELDS = ("shore", "c", "h", "residual")
STAT_FIELDS = (
    "atomic_families_examined", "atomic_families_feasible", "parity_cut_calls",
    "ordinary_min_cut_calls", "flow_augmentations", "flow_bfs_scans",
    "flow_peak_generated_value",
)
DEPENDENCIES = (
    enumerate_atomic_families, validate_pair, branch_coefficients,
    build_sign_routed_network, reduce_atomic_family, minimum_parity_cut,
    lift_source_shore, validate_shore, shore_f, shore_b_q, shore_d_q,
    residual_numerator, recover_objective,
)


class IntSub(int):
    pass


class TupleSub(tuple):
    pass


class InstanceSub(Instance):
    pass


class ContextSub(Context):
    pass


class Hostile:
    """Any coercion, comparison, iteration, or truth probe is a test failure."""

    def _forbidden(self, *args, **kwargs):
        raise AssertionError("hostile object was inspected before an exact type guard")

    __bool__ = __int__ = __index__ = __float__ = _forbidden
    __eq__ = __lt__ = __le__ = __gt__ = __ge__ = _forbidden
    __iter__ = __len__ = __getitem__ = _forbidden


class BackendSentinel(Exception):
    pass


def _instance(name, labels=None):
    return Instance(*DATA[name], labels=labels)


def _result_tuple(result):
    if result is None:
        return None
    assert type(result) is Result
    return tuple(getattr(result, name) for name in RESULT_FIELDS)


def _stats_tuple(stats):
    assert type(stats) is Stats
    return tuple(getattr(stats, name) for name in STAT_FIELDS)


def _unpack(value):
    assert type(value) is tuple and len(value) == 2
    result, stats = value
    assert result is None or type(result) is Result
    assert type(stats) is Stats
    assert type(stats.max_flow_calls) is int
    assert stats.max_flow_calls == stats.ordinary_min_cut_calls
    return result, stats


def _family_tuple(family):
    assert type(family) is AtomicFamily
    return family.T, family.pi, family.I, family.O


def _degrees(data):
    n, edges, _ = data
    return tuple(sum(q for u, v, q in edges if vertex in (u, v)) for vertex in range(n))


def _source(data, shore, branch):
    """Original-record definition; no production helper or family output."""
    n, edges, capacities = data
    members = tuple(vertex for vertex in range(n) if shore & (1 << vertex))
    s = sum(capacities[vertex] for vertex in members)
    b = 0
    d = 0
    for u, v, multiplicity in edges:
        left, right = bool(shore & (1 << u)), bool(shore & (1 << v))
        b += multiplicity * (left != right)
        d += multiplicity * (int(left) + int(right))
    if branch == 0:
        return bool((s + b) & 1), s + b - 1, d + 1 - s
    if branch == 1:
        return not (s + b) & 1 and b >= 1 and d > s, s + b - 2, d - s
    if branch == 2:
        return bool(s & 1) and s >= 3, b - d, s - 1
    return not s & 1 and b >= 1, b - d - 2, s


def _raw(data, shore, branch, parameter):
    _, c, h = _source(data, shore, branch)
    a, b = parameter
    return b * c - a * h


def _families(data):
    n, edges, capacities = data
    degrees = _degrees(data)
    plus = sum(1 << v for v in range(n) if (capacities[v] + degrees[v]) & 1)
    terminal = sum(1 << v for v in range(n) if capacities[v] & 1)
    d0 = ((plus, 1, 0, 0),)
    d1 = []
    for p in range(n):
        if degrees[p] > capacities[p]:
            for u, v, _ in edges:
                d1.append((plus, 0, (1 << p) | (1 << u), 1 << v))
                d1.append((plus, 0, (1 << p) | (1 << v), 1 << u))
    d2 = [(terminal, 1, 1 << v, 0) for v in range(n) if capacities[v] >= 2]
    ones = tuple(v for v in range(n) if capacities[v] == 1)
    d2.extend((terminal, 1, sum(1 << v for v in triple), 0)
              for triple in combinations(ones, 3))
    d3 = []
    for u, v, _ in edges:
        d3.extend(((terminal, 0, 1 << u, 1 << v), (terminal, 0, 1 << v, 1 << u)))
    return d0, tuple(d1), tuple(d2), tuple(d3)


def _member(family, shore, check_parity=True):
    terminal, parity, inside, outside = family
    return (shore & inside == inside and not shore & outside
            and (not check_parity or (shore & terminal).bit_count() % 2 == parity))


def _geometry(data, family):
    """Independent class geometry, without reading a production reduced graph."""
    n = data[0]
    terminal, parity, inside, outside = family
    groups = [inside | (1 << n), outside | (1 << (n + 1))]
    tokens = terminal
    if parity == 0:
        groups[0] |= 1 << (n + 2)
        tokens |= 1 << (n + 2)
    groups.extend(1 << v for v in range(n) if not (inside | outside) & (1 << v))
    raw_t = sum(1 << i for i, group in enumerate(groups) if (group & tokens).bit_count() % 2)
    terminals = raw_t ^ (2 if raw_t.bit_count() % 2 else 0)
    return tuple(groups), raw_t, terminals


def _least_restricted_candidates(data, branch, parameter, family):
    """Least ordinary cuts via ORIGINAL-shore enumeration, no flow/cut helper.

    The raw source polynomial is valid also off the branch domain. Restrict first
    by forced geometry only, minimize it under each ordered query, intersect all
    tied reduced shores, then impose parity. This is separate from direct D_j minima.
    """
    n = data[0]
    groups, _, terminals = _geometry(data, family)
    size = len(groups)
    geometric = []
    for shore in range(1 << n):
        if _member(family, shore, False):
            reduced_shore = 1
            for i in range(2, size):
                if groups[i] & shore:
                    reduced_shore |= 1 << i
            geometric.append((reduced_shore, _raw(data, shore, branch, parameter)))
    best = None
    calls = 0
    for inside in range(size):
        if inside == 1:
            continue
        for outside in range(1, size):
            if inside == outside:
                continue
            candidates = [(x, value) for x, value in geometric
                          if x & (1 << inside) and not x & (1 << outside)]
            least_value = min(value for _, value in candidates)
            least_shore = (1 << size) - 1
            for x, value in candidates:
                if value == least_value:
                    least_shore &= x
            calls += 1
            if (least_shore & terminals).bit_count() % 2 and (
                best is None or least_value < best[0]
            ):
                original = 0
                for i, group in enumerate(groups):
                    if least_shore & (1 << i):
                        original |= group
                best = least_value, original & ((1 << n) - 1)
    assert best is not None
    return best, calls


def _expected(data, branch, parameter):
    cover = _families(data)[branch]
    domain = tuple((u, c, h) for u in range(1 << data[0])
                   for ok, c, h in (_source(data, u, branch),) if ok)
    values = tuple((u, c, h, parameter[1] * c - parameter[0] * h) for u, c, h in domain)
    minimum = min((row[3] for row in values), default=None)
    argmins = tuple(row[0] for row in values if row[3] == minimum)
    best = None
    winner = None
    feasible = calls = 0
    for index, family in enumerate(cover):
        members = tuple(u for u in range(1 << data[0]) if _member(family, u))
        if not members:
            continue
        (raw, shore), count = _least_restricted_candidates(data, branch, parameter, family)
        feasible += 1
        calls += count
        ok, c, h = _source(data, shore, branch)
        assert ok and h > 0 and shore in members
        assert raw == min(_raw(data, u, branch, parameter) for u in members)
        if best is None or raw < best[3]:
            best = shore, c, h, raw
            winner = index
    assert (best is None) == (minimum is None)
    if best is not None:
        assert best[3] == minimum and best[0] in argmins
    return best, argmins, winner, (len(cover), feasible, feasible, calls)


def _tiny_instances():
    for n in (2, 3):
        pairs = tuple(combinations(range(n), 2))
        for multiplicities in product(range(3), repeat=len(pairs)):
            edges = tuple((u, v, q) for (u, v), q in zip(pairs, multiplicities, strict=True) if q)
            degrees = _degrees((n, edges, ()))
            if all(degrees):
                for capacities in product(*(range(1, degree + 1) for degree in degrees)):
                    yield n, edges, capacities


def _patch(monkeypatch, original, replacement):
    """Patch direct closed imports by identity, permitting ordinary import aliases."""
    names = [name for name, value in vars(oracle).items() if value is original]
    assert names, f"ruled direct dependency is missing: {original.__name__}"
    for name in names:
        monkeypatch.setattr(oracle, name, replacement)


def _forbidden(*args, **kwargs):
    raise AssertionError("forbidden dependency call at this phase")


def _exact_exception(kind, function, *args, **kwargs):
    with pytest.raises(kind) as caught:
        function(*args, **kwargs)
    assert type(caught.value) is kind
    return caught.value


def _check_answer(data, branch, parameter, value, expected=None):
    result, stats = _unpack(value)
    reference = _expected(data, branch, parameter) if expected is None else expected
    correct, argmins, _, counts = reference
    assert _result_tuple(result) == correct
    assert _stats_tuple(stats)[:4] == counts
    if result is not None:
        assert 0 < result.shore < 1 << data[0]
        legal, c, h = _source(data, result.shore, branch)
        assert legal and h > 0 and result.shore in argmins
        assert (result.c, result.h, result.residual) == (
            c, h, parameter[1] * c - parameter[0] * h,
        )
    return result, stats


def _query_row(key):
    _, name, branch, parameter, correct, argmins, winner, counts, _, _ = ROWS[key]
    return name, branch, parameter, (correct, argmins, winner, counts)


def test_public_surface_shapes_annotations_and_signatures():
    """BO1: representation is fixed, not inferred from implementation output."""
    assert type(oracle.__all__) is tuple
    assert oracle.__all__ == (
        "BranchOracleContext", "BranchOracleResult", "BranchOracleStats", "exact_branch_min",
    )
    for name in oracle.__all__:
        assert not hasattr(importlib.import_module("exactfrac"), name)
    specs = ((Context, ("instance", "families")), (Result, RESULT_FIELDS), (Stats, STAT_FIELDS))
    for cls, names in specs:
        assert is_dataclass(cls)
        assert tuple(field.name for field in fields(cls)) == names
        assert cls.__slots__ == names
        assert cls.__dataclass_params__.frozen
        assert cls.__dataclass_params__.eq and not cls.__dataclass_params__.order
        assert all(field.default is MISSING and field.default_factory is MISSING
                   for field in fields(cls))
        signature = inspect.signature(cls)
        required = ("instance",) if cls is Context else names
        assert tuple(signature.parameters) == required
        assert all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
                   and p.default is inspect.Parameter.empty for p in signature.parameters.values())
        assert all(name not in cls.__dict__ for name in ("__lt__", "__le__", "__gt__", "__ge__"))
    assert fields(Context)[1].init is False
    assert get_type_hints(Context) == {
        "instance": Instance, "families": tuple[tuple[AtomicFamily, ...], ...],
    }
    assert get_type_hints(Result) == dict.fromkeys(RESULT_FIELDS, int)
    assert get_type_hints(Stats) == dict.fromkeys(STAT_FIELDS, int)
    assert isinstance(Stats.max_flow_calls, property) and Stats.max_flow_calls.fset is None
    signature = inspect.signature(query)
    assert tuple(signature.parameters) == ("context", "branch", "parameter")
    assert all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
               and p.default is inspect.Parameter.empty for p in signature.parameters.values())
    assert get_type_hints(query) == {
        "context": Context, "branch": int, "parameter": tuple[int, int],
        "return": tuple[Result | None, Stats],
    }
    assert get_type_hints(Context.__init__)["return"] is type(None)
    assert get_type_hints(Result.__init__)["return"] is type(None)
    assert get_type_hints(Stats.__init__)["return"] is type(None)


def test_valid_records_equality_frozen_and_noncertifying_shapes():
    for kind, arguments in VALID_RECORDS:
        cls = Result if kind == "BranchOracleResult" else Stats
        value = cls(*arguments)
        assert value == cls(**dict(zip((RESULT_FIELDS if cls is Result else STAT_FIELDS),
                                      arguments, strict=True)))
        assert hash(value) == hash(cls(*arguments))
        assert not hasattr(value, "__dict__")
        name = "shore" if cls is Result else "atomic_families_examined"
        _exact_exception(FrozenInstanceError, setattr, value, name, 9)
        _exact_exception(FrozenInstanceError, delattr, value, name)
        _exact_exception(
            TypeError,
            lambda left=value, constructor=cls, args=arguments: left < constructor(*args),
        )
    context = Context(_instance("Q1"))
    assert context == Context(_instance("Q1"))
    assert hash(context) == hash(Context(_instance("Q1")))
    assert context == replace(context)
    assert not hasattr(context, "__dict__")
    _exact_exception(FrozenInstanceError, setattr, context, "instance", _instance("DOUBLE"))
    _exact_exception(TypeError, lambda: context < Context(_instance("Q1")))
    assert Stats(1, 9, 7, 3, 11, 0, 0).max_flow_calls == 3


def test_literal_tables_and_independent_source_calculator():
    assert len(INPUTS) == 9 and len(PARAMETERS) == 10
    assert len(MINIMA) == 360 and len(FAMILIES) == 176 and len(DOMAINS) == 36
    assert len(REJECTIONS) == 179 and len(FAILURES) == 14
    for name, _, _, _, degrees, total in INPUTS:
        assert _degrees(DATA[name]) == degrees
        assert sum(edge[2] for edge in DATA[name][1]) == total
    for name, branch, expected in DOMAINS:
        calculated = tuple((u, c, h) for u in range(1 << DATA[name][0])
                           for ok, c, h in (_source(DATA[name], u, branch),) if ok)
        assert calculated == expected
    for name, branch, index, descriptor, feasible, members in FAMILIES:
        assert _families(DATA[name])[branch][index] == descriptor
        assert tuple(u for u in range(1 << DATA[name][0]) if _member(descriptor, u)) == members
        assert bool(members) is feasible
    for row in MINIMA:
        _, name, branch, parameter, result, argmins, winner, counts, _, _ = row
        assert _expected(DATA[name], branch, parameter) == (result, argmins, winner, counts)


def test_context_retains_exact_instance_complete_cover_once(monkeypatch):
    seen = []

    def enumerate_once(instance):
        answer = enumerate_atomic_families(instance)
        seen.append((instance, answer))
        return answer

    _patch(monkeypatch, enumerate_atomic_families, enumerate_once)
    for name in DATA:
        instance = _instance(name)
        old_count = len(seen)
        context = Context(instance)
        assert len(seen) == old_count + 1
        assert seen[-1][0] is instance and context.instance is instance
        assert context.families is seen[-1][1]
        assert tuple(tuple(_family_tuple(f) for f in cover) for cover in context.families) == (
            _families(DATA[name])
        )
        copy = replace(context)
        assert len(seen) == old_count + 2 and copy.families is seen[-1][1]
        assert copy == context
        _exact_exception(TypeError, Context, instance, ())
        _exact_exception(TypeError, Context, instance, families=())
    assert len(seen) == 2 * len(DATA)


def _bad_value(symbol):
    factories = {
        "None": lambda: None, "True": lambda: True, "1.0": lambda: 1.0,
        "Fraction(1,1)": lambda: Fraction(1, 1), "Fraction(1,2)": lambda: Fraction(1, 2),
        "ExactValue(1,1)": lambda: ExactValue(1, 1), "ExactValue(1,2)": lambda: ExactValue(1, 2),
        "INT_SUB(1)": lambda: IntSub(1), "HOSTILE": Hostile,
        "BruteInstance": lambda: BruteInstance(*DATA["Q1"]),
        "INSTANCE_SUB": lambda: InstanceSub(*DATA["Q1"]),
        "Instance(Q1)": lambda: _instance("Q1"),
        "CONTEXT_SUB(Q1)": lambda: ContextSub(_instance("Q1")),
        "[1,2]": lambda: [1, 2], "ITERATOR((1,2))": lambda: iter((1, 2)),
        "TUPLE_SUB((1,2))": lambda: TupleSub((1, 2)),
        "(INT_SUB(1),1)": lambda: (IntSub(1), 1),
        "(1,INT_SUB(1))": lambda: (1, IntSub(1)),
        "(HOSTILE,1)": lambda: (Hostile(), 1), "(1,HOSTILE)": lambda: (1, Hostile()),
    }
    return factories[symbol]() if symbol in factories else ast.literal_eval(symbol)


def test_all_179_registered_rejections_and_python_behaviors():
    counts = Counter()
    for case, target, field, symbol, exception, precondition in REJECTIONS:
        if exception == "ValueError":
            bad = _bad_value(symbol)
            if target == "BranchOracleContext":
                action = partial(Context, bad)
            elif target == "BranchOracleResult":
                args = dict(zip(RESULT_FIELDS, (1, 0, 1, 0), strict=True))
                args[field] = bad
                action = partial(Result, **args)
            elif target == "BranchOracleStats":
                args = dict.fromkeys(STAT_FIELDS, 0)
                args[field] = bad
                action = partial(Stats, **args)
            else:
                args = {"context": Context(_instance("Q1")), "branch": 0, "parameter": (0, 1)}
                if "branch=" in precondition:
                    args["branch"] = int(precondition.split("branch=", 1)[1].split(";", 1)[0])
                if "MIXED" in precondition:
                    args["context"] = Context(_instance("MIXED"))
                args[field] = bad
                action = partial(query, **args)
            _exact_exception(ValueError, action)
        else:
            actions = {
                "extra families=()": lambda: Context(_instance("Q1"), families=()),
                "missing instance": lambda: Context(),
                "missing residual": lambda: Result(1, 0, 1),
                "extra max_flow_calls=0": lambda: Stats(0, 0, 0, 0, 0, 0, 0, max_flow_calls=0),
                "missing parameter": lambda: query(Context(_instance("Q1")), 0),
                "assign families=()": partial(setattr, Context(_instance("Q1")), "families", ()),
                "assign h=1": partial(setattr, Result(1, 0, 1, 0), "h", 1),
                "assign ordinary_min_cut_calls=1": partial(
                    setattr,
                    Stats(0, 0, 0, 0, 0, 0, 0), "ordinary_min_cut_calls", 1,
                ),
            }
            kind = TypeError if exception == "TypeError" else FrozenInstanceError
            _exact_exception(kind, actions[symbol])
        counts[exception] += 1
        assert case.startswith("V")
    assert counts == {"ValueError": 171, "TypeError": 5, "FrozenInstanceError": 3}


def test_validation_phases_precede_any_graph_or_empty_family_inspection(monkeypatch):
    context = Context(_instance("Q1"))
    _patch(monkeypatch, enumerate_atomic_families, _forbidden)
    _exact_exception(ValueError, Context, Hostile())
    with monkeypatch.context() as phase:
        _patch(phase, validate_pair, _forbidden)
        _exact_exception(ValueError, query, Hostile(), Hostile(), Hostile())
        _exact_exception(ValueError, query, context, Hostile(), Hostile())
        for branch in (-1, 4, True, IntSub(1), 1.0):
            _exact_exception(ValueError, query, context, branch, (0, 1))
    monkeypatch.setattr(AtomicFamily, "is_nonempty", property(_forbidden))
    for dependency in DEPENDENCIES[2:]:
        _patch(monkeypatch, dependency, _forbidden)
    for branch in range(4):
        for parameter in ((1, 0), (1, -1), [1, 2], (True, 1)):
            _exact_exception(ValueError, query, context, branch, parameter)
    _exact_exception(ValueError, Result, False, Hostile(), Hostile(), Hostile())
    _exact_exception(ValueError, Result, 1, False, Hostile(), Hostile())
    _exact_exception(ValueError, Result, 1, 0, False, Hostile())
    for index in range(7):
        args = [*[0] * index, -1, *(Hostile() for _ in range(6 - index))]
        _exact_exception(ValueError, Stats, *args)


def test_exact_branch_min():
    """BO4--BO5 / future scoped thm:branch-oracle conformance anchor."""
    contexts = {name: Context(_instance(name)) for name in DATA}
    for row in MINIMA:
        _, name, branch, parameter, correct, argmins, winner, counts, _, _ = row
        _check_answer(DATA[name], branch, parameter, query(contexts[name], branch, parameter),
                      (correct, argmins, winner, counts))


def test_all_empty_branches_skip_every_graph_dependency(monkeypatch):
    cases = [(name, branch, counts) for name, branch, _, counts, _, _ in COVERS if counts[1] == 0]
    contexts = {name: Context(_instance(name)) for name, _, _ in cases}
    for dependency in (enumerate_atomic_families, *DEPENDENCIES[2:]):
        _patch(monkeypatch, dependency, _forbidden)
    zero_lists = empty_lists = 0
    for name, branch, counts in cases:
        for parameter in PARAMS:
            result, stats = _unpack(query(contexts[name], branch, parameter))
            assert result is None
            assert _stats_tuple(stats) == (*counts, 0, 0, 0)
            if counts[0]:
                empty_lists += 1
            else:
                zero_lists += 1
    assert zero_lists and empty_lists


class Trace:
    """Instrument only the integration surface; compute expectations elsewhere."""

    def __init__(self, monkeypatch):
        self.events = []
        self.networks = []
        self.candidates = []
        self.current = None
        self.in_closed_reduce = False
        original_property = AtomicFamily.is_nonempty

        def predicate(family):
            outcome = original_property.fget(family)
            if not self.in_closed_reduce:
                self.events.append(("family", family, outcome))
            return outcome

        monkeypatch.setattr(AtomicFamily, "is_nonempty", property(predicate))
        for function in DEPENDENCIES:
            _patch(monkeypatch, function, self._wrapper(function))

    def _wrapper(self, function):
        def wrapped(*args, **kwargs):
            bound = inspect.signature(function).bind(*args, **kwargs)
            values = tuple(bound.arguments.values())
            self.events.append((function.__name__, *values))
            if function is reduce_atomic_family:
                self.current = {"network": values[0], "family": values[1]}
                self.in_closed_reduce = True
                try:
                    answer = function(*args, **kwargs)
                finally:
                    self.in_closed_reduce = False
                self.current["problem"] = answer
                self.candidates.append(self.current)
                return answer
            answer = function(*args, **kwargs)
            if function is build_sign_routed_network:
                self.networks.append(answer)
            elif function is minimum_parity_cut:
                self.current["parity_result"], self.current["parity_stats"] = answer
            elif function is lift_source_shore:
                self.current["original"] = answer
            elif function is recover_objective:
                self.current["recovered"] = answer
            return answer
        return wrapped


def test_complete_selected_sequence_lazy_network_and_seam_calls(monkeypatch):
    contexts = {name: Context(_instance(name)) for name in DATA}
    keys = tuple(dict.fromkeys(row[0] for row in FAMILY_TRACE))
    for key in keys:
        name, branch, parameter, reference = _query_row(key)
        with monkeypatch.context() as phase:
            trace = Trace(phase)
            value = query(contexts[name], branch, parameter)
        _check_answer(DATA[name], branch, parameter, value, reference)
        events = trace.events
        assert events[0][0] == "validate_pair"
        families = _families(DATA[name])[branch]
        observed = tuple(_family_tuple(event[1]) for event in events if event[0] == "family")
        assert observed == families
        assert not any(event[0] == "enumerate_atomic_families" for event in events)
        expected_rows = tuple(row for row in FAMILY_TRACE if row[0] == key and row[3] is not None)
        assert len(trace.candidates) == len(expected_rows) == reference[3][1]
        assert len(trace.networks) == int(bool(expected_rows))
        assert sum(event[0] == "branch_coefficients" for event in events) == len(trace.networks)
        if expected_rows:
            first_nonempty = next(i for i, event in enumerate(events)
                                  if event[0] == "family" and event[2])
            built = next(i for i, event in enumerate(events) if event[0] == "branch_coefficients")
            assert first_nonempty < built
        for observed_candidate, (_, _, descriptor, expected) in zip(
            trace.candidates, expected_rows, strict=True,
        ):
            candidate = observed_candidate
            problem = candidate["problem"]
            parity = candidate["parity_result"]
            assert candidate["network"] is trace.networks[0]
            assert _family_tuple(candidate["family"]) == descriptor
            classes, _, terminals, reduced, original, c, h, raw, cut, calls, _ = expected
            assert problem.classes == classes and problem.terminal_mask == terminals
            assert parity.source_shore == reduced and parity.cut_value == cut
            assert candidate["original"] == original
            assert candidate["recovered"] == raw == parameter[1] * c - parameter[0] * h
            assert candidate["parity_stats"].mincut_calls == calls
        for dependency in (reduce_atomic_family, minimum_parity_cut, lift_source_shore,
                           validate_shore, shore_f, shore_b_q, shore_d_q,
                           residual_numerator, recover_objective):
            matching = [event for event in events if event[0] == dependency.__name__]
            assert len(matching) == len(expected_rows)
            if dependency is recover_objective:
                assert all(event[1] is trace.networks[0] for event in matching)
            if dependency in (shore_f, shore_b_q, shore_d_q):
                for event, candidate in zip(matching, trace.candidates, strict=True):
                    assert event[1] is contexts[name].instance
                    assert event[2] == candidate["original"]


def test_original_networks_match_all_12_literal_rows(monkeypatch):
    for key, coefficient, gamma, minus, constant, arcs in NETWORKS:
        name, branch, parameter, reference = _query_row(key)
        context = Context(_instance(name))
        seen = []

        expected_network = coefficient, gamma, minus, constant, arcs

        def build(instance, coefficients, expected=expected_network, observations=seen):
            a, g, shift, k, edges = expected
            assert coefficients.a == a and coefficients.gamma == g
            assert coefficients.constant == k
            network = build_sign_routed_network(instance, coefficients)
            assert network.arcs == edges and network.negative_shift == shift
            assert network.constant == k
            assert len(network.arcs) == 2 * (instance.m + instance.n)
            observations.append(network)
            return network

        with monkeypatch.context() as phase:
            _patch(phase, build_sign_routed_network, build)
            _check_answer(
                DATA[name], branch, parameter, query(context, branch, parameter), reference,
            )
        assert len(seen) == 1


def test_early_zero_negative_and_secondary_tie_traps(monkeypatch):
    for _, key, _, _, _, correct in TRAPS:
        name, branch, parameter, reference = _query_row(key)
        context = Context(_instance(name))
        seen = []

        def minimize(problem, observations=seen):
            observations.append(problem)
            return minimum_parity_cut(problem)

        with monkeypatch.context() as phase:
            _patch(phase, minimum_parity_cut, minimize)
            answer = query(context, branch, parameter)
        result, _ = _check_answer(DATA[name], branch, parameter, answer, reference)
        assert _result_tuple(result) == correct
        assert len(seen) == reference[3][1]


def test_unrestricted_cut_does_not_replace_family_parity_minimization():
    key, shore, _, raw, correct = UNRESTRICTED_TRAP[0]
    name, branch, parameter, reference = _query_row(key)
    assert _raw(DATA[name], shore, branch, parameter) == raw
    assert not _source(DATA[name], shore, branch)[0]
    result, _ = _check_answer(DATA[name], branch, parameter,
                              query(Context(_instance(name)), branch, parameter), reference)
    assert _result_tuple(result) == correct and correct[3] > raw


def test_coordinate_recovery_literal_anchors(monkeypatch):
    differences = 0
    for row in COORDINATE_RECOVERY:
        key, family_index, classes, reduced, original, cut, minus, constant, raw = row
        name, branch, parameter, reference = _query_row(key)
        context = Context(_instance(name))
        wanted = context.families[branch][family_index]
        matches = []
        current = [None]

        def reduce(network, family, active=current):
            active[0] = family
            return reduce_atomic_family(network, family)

        def lift(problem, shore, active=current, target=wanted, observations=matches):
            output = lift_source_shore(problem, shore)
            if active[0] is target:
                observations.append((problem.classes, shore, output))
            return output

        with monkeypatch.context() as phase:
            _patch(phase, reduce_atomic_family, reduce)
            _patch(phase, lift_source_shore, lift)
            _check_answer(
                DATA[name], branch, parameter, query(context, branch, parameter), reference,
            )
        assert matches == [(classes, reduced, original)]
        assert cut - minus + constant == raw
        differences += int(reduced != original)
    assert differences == 2


def test_registered_stats_and_146_ordinary_trace_calls(monkeypatch):
    total = 0
    ordinary = parity_module.minimum_cut
    for key, expected_stats, max_calls in STATS:
        name, branch, parameter, reference = _query_row(key)
        context = Context(_instance(name))
        observed = []

        def cut(node_count, source, sink, arcs, observations=observed):
            answer = ordinary(node_count, source, sink, arcs)
            observations.append((node_count, arcs, answer.value, answer.source_shore,
                             (answer.stats.augmentations, answer.stats.bfs_scans,
                              answer.stats.peak_generated_value)))
            assert (source, sink) == (0, 1)
            return answer

        with monkeypatch.context() as phase:
            phase.setattr(parity_module, "minimum_cut", cut)
            _, stats = _check_answer(DATA[name], branch, parameter,
                                     query(context, branch, parameter), reference)
        expected = [(r[4], r[5], r[6], r[7], r[8]) for r in FLOW_DIAGNOSTIC_TRACE if r[0] == key]
        assert observed == expected
        assert _stats_tuple(stats) == expected_stats and stats.max_flow_calls == max_calls
        total += len(observed)
    assert total == 146


def test_internal_none_from_reduction_or_parity_is_runtime_error(monkeypatch):
    context = Context(_instance("DOUBLE"))
    with monkeypatch.context() as phase:
        _patch(phase, reduce_atomic_family, lambda network, family: None)
        _patch(phase, minimum_parity_cut, _forbidden)
        _exact_exception(RuntimeError, query, context, 0, (0, 1))
    with monkeypatch.context() as phase:
        _patch(phase, minimum_parity_cut, lambda problem: (None, ParityCutStats(0, 0, 0, 0)))
        _patch(phase, lift_source_shore, _forbidden)
        _exact_exception(RuntimeError, query, context, 0, (0, 1))


def test_internal_finite_shore_membership_faults_fail_before_source_evaluation(monkeypatch):
    context = Context(_instance("MIXED"))
    descriptor = _families(DATA["MIXED"])[3][0]
    assert descriptor == (10, 0, 1, 2)
    for bad in (0, 3, 9):
        assert not _member(descriptor, bad)
        with monkeypatch.context() as phase:
            _patch(phase, lift_source_shore, lambda problem, shore, output=bad: output)
            for function in (shore_f, shore_b_q, shore_d_q, residual_numerator, recover_objective):
                _patch(phase, function, _forbidden)
            _exact_exception(RuntimeError, query, context, 3, (0, 1))


def test_internal_source_domains_and_h_guard_before_raw_or_recovery(monkeypatch):
    cases = (
        ("DOUBLE", 0, (2, 0, 2)),
        ("RICH", 1, (2, 0, 4)), ("RICH", 1, (2, 2, 2)), ("RICH", 1, (2, 1, 4)),
        ("UNEQUAL", 2, (2, 0, 4)), ("UNEQUAL", 2, (1, 0, 4)),
        ("UNEQUAL", 3, (1, 1, 2)), ("UNEQUAL", 3, (2, 0, 2)),
        # Branch 0's formal domain is odd but h=0 or h<0: explicit seam checks.
        ("DOUBLE", 0, (1, 0, 0)), ("DOUBLE", 0, (3, 0, 0)),
    )
    for name, branch, sums in cases:
        context = Context(_instance(name))
        with monkeypatch.context() as phase:
            for function, value in zip((shore_f, shore_b_q, shore_d_q), sums, strict=True):
                _patch(phase, function, lambda instance, shore, output=value: output)
            _patch(phase, residual_numerator, _forbidden)
            _patch(phase, recover_objective, _forbidden)
            _exact_exception(RuntimeError, query, context, branch, (0, 1))


def test_recovery_and_raw_mismatches_never_become_better_candidates(monkeypatch):
    context = Context(_instance("RICH"))
    for wrong in (-1000000, 1000000):
        with monkeypatch.context() as phase:
            _patch(phase, recover_objective, lambda network, cut, output=wrong: output)
            _exact_exception(RuntimeError, query, context, 1, (2, 1))
    with monkeypatch.context() as phase:
        def incorrect_raw(parameter, c, h):
            return parameter[1] * c - parameter[0] * h + 1
        _patch(phase, residual_numerator, incorrect_raw)
        _exact_exception(RuntimeError, query, context, 1, (2, 1))


def test_closed_dependency_exceptions_propagate_unchanged(monkeypatch):
    context = Context(_instance("DOUBLE"))
    for dependency in DEPENDENCIES:
        sentinel = BackendSentinel(dependency.__name__)

        def fail(*args, error=sentinel, **kwargs):
            raise error

        with monkeypatch.context() as phase:
            _patch(phase, dependency, fail)
            if dependency is enumerate_atomic_families:
                caught = _exact_exception(BackendSentinel, Context, _instance("DOUBLE"))
            else:
                caught = _exact_exception(BackendSentinel, query, context, 0, (0, 1))
            assert caught is sentinel
    for dependency in (lift_source_shore, validate_shore):
        sentinel = ValueError("exact dependency ValueError identity")
        with monkeypatch.context() as phase:
            _patch(phase, dependency, lambda *args, error=sentinel: (_ for _ in ()).throw(error))
            assert _exact_exception(ValueError, query, context, 0, (0, 1)) is sentinel
    with monkeypatch.context() as phase:
        _patch(phase, lift_source_shore, lambda problem, shore: 1 << context.instance.n)
        _exact_exception(ValueError, query, context, 0, (0, 1))


def test_alternative_legal_within_family_minimizer_is_not_rejected(monkeypatch):
    # DOUBLE-j0-p3: both original singletons minimize; no least PARITY rule in Unit 12.
    context = Context(_instance("DOUBLE"))
    assert _expected(DATA["DOUBLE"], 0, (0, 1))[1] == (1, 2)

    def alternative(problem):
        assert problem.classes == (4, 8, 1, 2)
        _, stats = minimum_parity_cut(problem)
        return ParityCutResult(3, 9), stats

    _patch(monkeypatch, minimum_parity_cut, alternative)
    result, stats = _unpack(query(context, 0, (0, 1)))
    assert _result_tuple(result) == (2, 2, 2, 2)
    assert _stats_tuple(stats)[:4] == (1, 1, 1, 7)


def test_legal_changed_diagnostics_do_not_change_the_selected_result(monkeypatch):
    context = Context(_instance("RICH"))
    key = "RICH-j1-p7"
    expected = ROWS[key][4]
    supplied = []

    def diagnostics(problem):
        result, _ = minimum_parity_cut(problem)
        index = len(supplied)
        stats = ParityCutStats(index + 9, index + 20, index + 30, index + 40)
        supplied.append(stats)
        return result, stats

    _patch(monkeypatch, minimum_parity_cut, diagnostics)
    result, stats = _unpack(query(context, 1, (2, 1)))
    assert _result_tuple(result) == expected
    counts = ROWS[key][7]
    assert len(supplied) == counts[1]
    assert _stats_tuple(stats) == (
        *counts[:3],
        sum(value.mincut_calls for value in supplied),
        sum(value.flow_augmentations for value in supplied),
        sum(value.flow_bfs_scans for value in supplied),
        max(value.flow_peak_generated_value for value in supplied),
    )


def test_context_reuse_parameter_network_identity_and_nonmutation(monkeypatch):
    context = Context(_instance("RICH"))
    snapshot = repr(context), hash(context), context.instance, context.families
    before_files = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in Path(oracle.__file__).parent.glob("*.py")}
    networks = []

    def builder(instance, coefficients):
        network = build_sign_routed_network(instance, coefficients)
        networks.append(network)
        return network

    _patch(monkeypatch, enumerate_atomic_families, _forbidden)
    _patch(monkeypatch, build_sign_routed_network, builder)
    first_seen = {}
    for _, key, correct, counts, fresh in REUSE:
        _, branch, parameter, _ = _query_row(key)
        old = len(networks)
        answer = query(context=context, branch=branch, parameter=parameter)
        result, stats = _unpack(answer)
        assert _result_tuple(result) == correct and _stats_tuple(stats)[:4] == counts
        assert len(networks) == old + int(fresh)
        assert len({id(network) for network in networks}) == len(networks)
        assert (repr(context), hash(context), context.instance, context.families) == snapshot
        assert context.instance is snapshot[2] and context.families is snapshot[3]
        if key in first_seen:
            assert answer == first_seen[key]
        first_seen[key] = answer
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in before_files.items())


def test_labels_and_normal_reconstruction_do_not_change_query_results():
    plain = Context(_instance("RICH"))
    labeled = Context(_instance("RICH", labels=("x", 1, "2", 3, "last")))
    for branch in range(4):
        for parameter in ((-5, 2), (0, 3), (7, 3)):
            assert query(plain, branch, parameter) == query(labeled, branch, parameter)
            assert query(plain, branch, parameter) == query(replace(plain), branch, parameter)


def test_raw_scaling_20_registered_cases_preserve_unreduced_c_h():
    checks = 0
    for exponent in (1, 2, 8, 64, 4096):
        scale = 1 << exponent
        for key in ("RICH-j1-p7", "RICH-j3-p1", "MIXED-j0-p0", "MIXED-j2-p3"):
            name, branch, parameter, reference = _query_row(key)
            context = Context(_instance(name))
            correct = reference[0]
            scaled = parameter[0] * scale, parameter[1] * scale
            result, stats = _unpack(query(context, branch, scaled))
            assert _result_tuple(result) == (*correct[:3], correct[3] * scale)
            assert _stats_tuple(stats)[:4] == reference[3]
            # Other diagnostics are not universally invariant under numeric scaling.
            checks += 1
    assert checks == SCALE_COUNTS[0][0] == 20
    result, _ = _unpack(query(Context(_instance("DOUBLE")), 0, (0, 3)))
    assert _result_tuple(result) == (1, 2, 2, 6)


def test_60_large_capacity_cases_and_polynomial_number_bounds():
    for exponent, branch, parameter, shore, bit_lengths, sign, counts, expected_hash in LARGE_CASES:
        magnitude = 1 << exponent
        data = (2, ((0, 1, magnitude),), (1, 2))
        correct, argmins, winner, expected_counts = _expected(data, branch, parameter)
        assert expected_counts == counts
        result, _ = _check_answer(data, branch, parameter,
                                  query(Context(Instance(*data)), branch, parameter),
                                  (correct, argmins, winner, counts))
        raw = _result_tuple(result)
        encoded = json.dumps(raw, separators=(",", ":")).encode()
        assert hashlib.sha256(encoded).hexdigest() == expected_hash
        if result is None:
            assert shore is None and bit_lengths is None and sign is None
        else:
            assert result.shore == shore
            assert tuple(abs(value).bit_length() for value in raw[1:]) == bit_lengths
            assert (result.residual > 0) - (result.residual < 0) == sign
            total = magnitude
            assert abs(result.c) <= 3 * total + 2
            assert 0 < result.h <= 2 * total + 1
            assert abs(result.residual) <= parameter[1] * (3 * total + 2) + (
                abs(parameter[0]) * (2 * total + 1)
            )


def test_341_descriptor_preparation_is_not_repeated_in_a_d0_query(monkeypatch):
    n, edges, capacities, sizes, total, parameter, expected, counts = PREPARATION_SEPARATION[0]
    context = Context(Instance(n, edges, capacities))
    assert tuple(map(len, context.families)) == sizes and sum(sizes) == total == 341
    _patch(monkeypatch, enumerate_atomic_families, _forbidden)
    for raw_parameter, scale in ((parameter, 1), ((0, 7), 7), (parameter, 1)):
        result, stats = _unpack(query(context, 0, raw_parameter))
        assert _result_tuple(result) == (*expected[:3], expected[3] * scale)
        assert _stats_tuple(stats)[:4] == counts == (1, 1, 1, 111)


def test_exhaustive_corpus_13160_queries_and_138720_actual_ordinary_calls(monkeypatch):
    """BO5/BO6/BO20: freeze source expectations before each candidate query."""
    ordinary = parity_module.minimum_cut
    observed_calls = [0]

    def counted(*args, **kwargs):
        observed_calls[0] += 1
        return ordinary(*args, **kwargs)

    monkeypatch.setattr(parity_module, "minimum_cut", counted)
    counts = Counter()
    branches = [Counter() for _ in range(4)]
    fingerprint = hashlib.sha256()
    for serial, data in enumerate(_tiny_instances()):
        n = data[0]
        counts["instances"] += 1
        counts[f"n{n}_instances"] += 1
        covers = _families(data)
        context = Context(Instance(*data))
        assert tuple(tuple(_family_tuple(f) for f in group) for group in context.families) == covers
        for branch in range(4):
            cover = covers[branch]
            counts["family_descriptors_once"] += len(cover)
            counts["empty_descriptors_once"] += sum(
                not any(_member(family, u) for u in range(1 << n)) for family in cover
            )
            for shore in range(1 << n):
                ok, _, h = _source(data, shore, branch)
                assert ok == any(_member(family, shore) for family in cover)
                assert not ok or (shore > 0 and h > 0)
                counts["branch_domain_shore_checks"] += 1
                counts["domain_memberships"] += int(ok)
            for parameter in PARAMS:
                expected = _expected(data, branch, parameter)
                correct, argmins, winner, prefix = expected
                previous = observed_calls[0]
                _check_answer(data, branch, parameter, query(context, branch, parameter), expected)
                assert observed_calls[0] - previous == prefix[3]
                row = serial, branch, parameter, correct, argmins, winner, prefix
                fingerprint.update((json.dumps(row, separators=(",", ":")) + "\n").encode())
                bc = branches[branch]
                counts["queries"] += 1
                bc["queries"] += 1
                bc["family_examinations"] += prefix[0]
                bc["feasible_family_calls"] += prefix[1]
                bc["specified_ordinary_calls"] += prefix[3]
                bc["feasible_queries" if correct is not None else "infeasible_queries"] += 1
                if correct is None:
                    bucket = ("zero_descriptor_queries" if not cover
                              else "all_empty_descriptor_queries")
                    bc[bucket] += 1
                else:
                    bucket = ("positive_minima" if correct[3] > 0 else
                              "negative_minima" if correct[3] < 0 else "zero_minima")
                    bc[bucket] += 1
                    bc["multiple_original_argmins"] += int(len(argmins) > 1)
                    bc["full_shore_winners"] += int(correct[0] == (1 << n) - 1)
    for branch, expected in BRANCH_CORPUS_COUNTS:
        assert dict(branches[branch]) == expected
        for key, value in branches[branch].items():
            if key != "queries":
                counts[key] += value
    assert dict(counts) == dict(CORPUS_COUNTS)
    assert fingerprint.hexdigest() == CORPUS_FINGERPRINT[0][1]
    assert observed_calls[0] == 138720


def test_imports_in_a_fresh_process_resolve_only_closed_project_layers():
    root = Path(oracle.__file__).resolve().parents[1]
    code = r'''
import importlib
import json
from pathlib import Path
import sys
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
module = importlib.import_module("exactfrac.oracle")
allowed = {"exactfrac._telemetry",
           "exactfrac", "exactfrac.oracle", "exactfrac.instance", "exactfrac.families",
           "exactfrac.rational", "exactfrac.shore", "exactfrac.sign_routing",
           "exactfrac.parity_cut", "exactfrac.witness", "exactfrac.flow"}
origins = {}
for name, value in tuple(sys.modules.items()):
    if name == "exactfrac" or name.startswith("exactfrac."):
        if name not in allowed:
            raise SystemExit("unapproved project import: " + name)
        path = Path(value.__file__).resolve()
        if not path.is_relative_to(root):
            raise SystemExit("project import escaped candidate root: " + name)
        origins[name] = str(path.relative_to(root))
    if name.startswith(("exactfrac_verify", "tests.", "networkx", "scipy", "numpy")):
        raise SystemExit("forbidden production import: " + name)
print(json.dumps(origins, sort_keys=True))
'''
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-I", "-S", "-B", "-c", code, str(root)],
        cwd=root, env=env, capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    origins = json.loads(completed.stdout)
    assert origins["exactfrac.oracle"] == "exactfrac/oracle.py"


def test_production_source_imports_exact_arithmetic_and_no_side_effect_paths():
    tree = ast.parse(Path(oracle.__file__).read_text(encoding="utf-8"))
    whitelist = {
        "_telemetry": {"_tap_int", "_tap_pair", "_tap_numerator", "_observe_ints",
                       "_observe_pair_values", "_record_prepared_sizes", "_branch_scope"},
        "__future__": {"annotations"}, "dataclasses": {"dataclass", "field"},
        "instance": {"Instance"}, "families": {"AtomicFamily", "enumerate_atomic_families"},
        "rational": {"RawPair", "validate_pair", "residual_numerator"},
        "shore": {"validate_shore"},
        "sign_routing": {"SignRoutingCoefficients", "SignRoutedNetwork", "branch_coefficients",
                         "build_sign_routed_network", "recover_objective"},
        "parity_cut": {"ParityCutProblem", "ParityCutResult", "ParityCutStats",
                       "reduce_atomic_family", "minimum_parity_cut", "lift_source_shore"},
        "witness": {"shore_f", "shore_b_q", "shore_d_q"},
    }
    prohibited = {"float", "Fraction", "gcd", "round", "open", "eval", "exec", "compile",
                  "__import__", "input", "setattr", "delattr"}
    for node in ast.walk(tree):
        assert not isinstance(node, ast.Import)
        if isinstance(node, ast.ImportFrom):
            name = node.module.removeprefix("exactfrac.") if node.module else ""
            assert name in whitelist and {alias.name for alias in node.names} <= whitelist[name]
        if isinstance(node, ast.Constant):
            assert type(node.value) not in (float, complex)
        assert not isinstance(
            node, (ast.Div, ast.FloorDiv, ast.Mod, ast.AsyncFunctionDef, ast.Await),
        )
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in prohibited
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in ("__import__", "read_text", "read_bytes", "write_text",
                                          "write_bytes", "random", "shuffle", "sort")
    # Only __post_init__ may populate the one declared init=False context field.
    for function in (node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)):
        for node in ast.walk(function):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "__setattr__"):
                assert function.name == "__post_init__"
                assert isinstance(node.func.value, ast.Name) and node.func.value.id == "object"
                assert len(node.args) == 3 and isinstance(node.args[1], ast.Constant)
                assert node.args[1].value == "families"
    for node in tree.body:
        assert isinstance(node, (ast.Expr, ast.ImportFrom, ast.Assign, ast.AnnAssign,
                                 ast.FunctionDef, ast.ClassDef))
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            assert not isinstance(node.value, (ast.List, ast.Set, ast.Dict, ast.Call))


def test_source_has_no_recursive_or_magnitude_or_all_shore_iteration():
    tree = ast.parse(Path(oracle.__file__).read_text(encoding="utf-8"))
    functions = {node.name: node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    edges = {name: set() for name in functions}
    for name, function in functions.items():
        for node in ast.walk(function):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in functions):
                edges[name].add(node.func.id)
    def visit(name, stack):
        assert name not in stack, "recursive production call path"
        for child in edges[name]:
            visit(child, (*stack, name))
    for name in functions:
        visit(name, ())
    set_names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            value = node.value
            if isinstance(value, (ast.Set, ast.SetComp)) or (
                isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
                and value.func.id in ("set", "frozenset")
            ):
                targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
                set_names.update(target.id for target in targets if isinstance(target, ast.Name))
    for node in ast.walk(tree):
        iterator = node.iter if isinstance(node, (ast.For, ast.comprehension)) else None
        if iterator is not None:
            assert not isinstance(iterator, (ast.Set, ast.SetComp))
            assert not (isinstance(iterator, ast.Name) and iterator.id in set_names)
            if isinstance(iterator, ast.Call) and isinstance(iterator.func, ast.Name):
                assert iterator.func.id not in ("set", "frozenset")
                if iterator.func.id == "range":
                    assert not any(isinstance(part, (ast.LShift, ast.Pow))
                                   for arg in iterator.args for part in ast.walk(arg))
                    forbidden = {"A", "B", "Q", "q", "f", "numerator", "denominator",
                                 "multiplicity", "capacity", "residual"}
                    assert not any(isinstance(part, ast.Name) and part.id in forbidden
                                   for arg in iterator.args for part in ast.walk(arg))
                    assert not any(
                        isinstance(part, ast.Call) and isinstance(part.func, ast.Attribute)
                        and part.func.attr == "bit_length"
                        for arg in iterator.args for part in ast.walk(arg)
                    )
