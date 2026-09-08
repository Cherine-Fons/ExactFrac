"""Unit 11 PC1--PC20 consuming tests, from ORACLE-056--068 and DESIGN 4.8.

All literal expectations below are transcribed from the committed human tables.
The test file never reads handoff JSON, imports private audit code, or derives
an expected parity minimum from a production reducer, solver, or flow result.
Ordinary-call spies forward to the closed backend; independent enumerations
supply expected cut values, least shores, and parity optima.
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
from collections.abc import Callable, Iterator
from dataclasses import MISSING, FrozenInstanceError, fields, is_dataclass
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import get_type_hints

import pytest

from exactfrac.families import AtomicFamily
from exactfrac.flow import FlowStats, MinCutResult
from exactfrac.flow import minimum_cut as closed_minimum_cut
from exactfrac.instance import Instance
from exactfrac.shore import validate_shore as closed_validate_shore
from exactfrac.sign_routing import (
    SignRoutedNetwork,
    branch_coefficients,
    build_sign_routed_network,
    recover_objective,
)

BruteInstance = importlib.import_module("exactfrac_verify.brute").BruteInstance
parity_cut = importlib.import_module("exactfrac.parity_cut")
Problem = parity_cut.ParityCutProblem
Result = parity_cut.ParityCutResult
Stats = parity_cut.ParityCutStats

EXPECTED_EXPORTS = (
    "ParityCutProblem",
    "ParityCutResult",
    "ParityCutStats",
    "lift_source_shore",
    "minimum_parity_cut",
    "reduce_atomic_family",
)

# ORACLE-056--068, literal table RAW_NETWORKS.
RAW_NETWORKS = ({'id': 'D1', 'n': 1, 'arcs': (), 'shift': 0, 'constant': 0},
 {'id': 'D2',
  'n': 2,
  'arcs': ((0, 1, 6), (1, 0, 6), (2, 0, 4), (0, 2, 4), (1, 3, 5), (3, 1, 5)),
  'shift': 4,
  'constant': -3},
 {'id': 'D3',
  'n': 3,
  'arcs': ((3, 0, 2), (3, 0, 1), (0, 3, 4), (0, 1, 5), (3, 1, 7), (1, 4, 6), (1, 2, 1),
           (2, 4, 8), (4, 2, 9), (0, 2, 0), (3, 2, 0), (2, 0, 0), (1, 0, 3)),
  'shift': 5,
  'constant': -2},
 {'id': 'D4',
  'n': 4,
  'arcs': ((0, 1, 0), (1, 0, 0), (2, 3, 0), (3, 2, 0), (4, 0, 0), (0, 4, 0), (1, 5, 0),
           (5, 1, 0)),
  'shift': 7,
  'constant': -2},
 {'id': 'D5', 'n': 4, 'arcs': (), 'shift': 0, 'constant': 0},
 {'id': 'D6', 'n': 3, 'arcs': (), 'shift': 0, 'constant': 0})

# ORACLE-056--068, literal table REDUCTIONS.
REDUCTIONS = ({'id': 'C01',
  'network': 'D1',
  'family': (0, 0, 0, 0),
  'classes': (10, 4, 1),
  'arcs': (),
  'before_toggle': 1,
  'terminal_mask': 3,
  'feasible_original': (0, 1)},
 {'id': 'C02',
  'network': 'D1',
  'family': (1, 1, 0, 0),
  'classes': (2, 4, 1),
  'arcs': (),
  'before_toggle': 4,
  'terminal_mask': 6,
  'feasible_original': (1,)},
 {'id': 'C03',
  'network': 'D1',
  'family': (1, 0, 0, 0),
  'classes': (10, 4, 1),
  'arcs': (),
  'before_toggle': 5,
  'terminal_mask': 5,
  'feasible_original': (0,)},
 {'id': 'C04',
  'network': 'D1',
  'family': (1, 1, 1, 0),
  'classes': (3, 4),
  'arcs': (),
  'before_toggle': 1,
  'terminal_mask': 3,
  'feasible_original': (1,)},
 {'id': 'C05',
  'network': 'D1',
  'family': (1, 0, 0, 1),
  'classes': (10, 5),
  'arcs': (),
  'before_toggle': 3,
  'terminal_mask': 3,
  'feasible_original': (0,)},
 {'id': 'C06',
  'network': 'D1',
  'family': (1, 0, 1, 0),
  'classes': None,
  'arcs': None,
  'before_toggle': None,
  'terminal_mask': None,
  'feasible_original': ()},
 {'id': 'C07',
  'network': 'D1',
  'family': (1, 1, 1, 1),
  'classes': None,
  'arcs': None,
  'before_toggle': None,
  'terminal_mask': None,
  'feasible_original': ()},
 {'id': 'C08',
  'network': 'D2',
  'family': (3, 1, 0, 0),
  'classes': (4, 8, 1, 2),
  'arcs': ((0, 2, 4), (1, 3, 5), (2, 0, 4), (2, 3, 6), (3, 1, 5), (3, 2, 6)),
  'before_toggle': 12,
  'terminal_mask': 12,
  'feasible_original': (1, 2)},
 {'id': 'C09',
  'network': 'D2',
  'family': (3, 0, 0, 0),
  'classes': (20, 8, 1, 2),
  'arcs': ((0, 2, 4), (1, 3, 5), (2, 0, 4), (2, 3, 6), (3, 1, 5), (3, 2, 6)),
  'before_toggle': 13,
  'terminal_mask': 15,
  'feasible_original': (0, 3)},
 {'id': 'C10',
  'network': 'D2',
  'family': (1, 1, 1, 0),
  'classes': (5, 8, 2),
  'arcs': ((0, 2, 6), (1, 2, 5), (2, 0, 6), (2, 1, 5)),
  'before_toggle': 1,
  'terminal_mask': 3,
  'feasible_original': (1, 3)},
 {'id': 'C11',
  'network': 'D2',
  'family': (2, 1, 0, 1),
  'classes': (4, 9, 2),
  'arcs': ((0, 1, 4), (1, 0, 4), (1, 2, 11), (2, 1, 11)),
  'before_toggle': 4,
  'terminal_mask': 6,
  'feasible_original': (2,)},
 {'id': 'C12',
  'network': 'D2',
  'family': (3, 0, 1, 2),
  'classes': None,
  'arcs': None,
  'before_toggle': None,
  'terminal_mask': None,
  'feasible_original': ()},
 {'id': 'C13',
  'network': 'D2',
  'family': (3, 1, 1, 2),
  'classes': (5, 10),
  'arcs': ((0, 1, 6), (1, 0, 6)),
  'before_toggle': 3,
  'terminal_mask': 3,
  'feasible_original': (1,)},
 {'id': 'C14',
  'network': 'D3',
  'family': (3, 1, 1, 4),
  'classes': (9, 20, 2),
  'arcs': ((0, 1, 0), (0, 2, 12), (1, 0, 0), (2, 0, 3), (2, 1, 7)),
  'before_toggle': 5,
  'terminal_mask': 5,
  'feasible_original': (1,)},
 {'id': 'C15',
  'network': 'D3',
  'family': (3, 0, 1, 4),
  'classes': (41, 20, 2),
  'arcs': ((0, 1, 0), (0, 2, 12), (1, 0, 0), (2, 0, 3), (2, 1, 7)),
  'before_toggle': 4,
  'terminal_mask': 6,
  'feasible_original': (3,)},
 {'id': 'C16',
  'network': 'D3',
  'family': (7, 1, 3, 4),
  'classes': None,
  'arcs': None,
  'before_toggle': None,
  'terminal_mask': None,
  'feasible_original': ()},
 {'id': 'C17',
  'network': 'D3',
  'family': (3, 0, 3, 4),
  'classes': (43, 20),
  'arcs': ((0, 1, 7), (1, 0, 0)),
  'before_toggle': 1,
  'terminal_mask': 3,
  'feasible_original': (3,)},
 {'id': 'C18',
  'network': 'D3',
  'family': (7, 0, 3, 0),
  'classes': (43, 16, 4),
  'arcs': ((0, 1, 6), (0, 2, 1), (1, 2, 9), (2, 0, 0), (2, 1, 8)),
  'before_toggle': 5,
  'terminal_mask': 5,
  'feasible_original': (3,)},
 {'id': 'C19',
  'network': 'D3',
  'family': (7, 1, 0, 6),
  'classes': (8, 22, 1),
  'arcs': ((0, 1, 7), (0, 2, 3), (1, 2, 3), (2, 0, 4), (2, 1, 5)),
  'before_toggle': 4,
  'terminal_mask': 6,
  'feasible_original': (1,)},
 {'id': 'C20',
  'network': 'D4',
  'family': (15, 0, 3, 8),
  'classes': (83, 40, 4),
  'arcs': ((0, 1, 0), (1, 0, 0), (1, 2, 0), (2, 1, 0)),
  'before_toggle': 7,
  'terminal_mask': 5,
  'feasible_original': (3,)},
 {'id': 'C21',
  'network': 'D4',
  'family': (15, 1, 7, 8),
  'classes': (23, 40),
  'arcs': ((0, 1, 0), (1, 0, 0)),
  'before_toggle': 3,
  'terminal_mask': 3,
  'feasible_original': (7,)},
 {'id': 'C22',
  'network': 'D5',
  'family': (0, 0, 0, 0),
  'classes': (80, 32, 1, 2, 4, 8),
  'arcs': (),
  'before_toggle': 1,
  'terminal_mask': 3,
  'feasible_original': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)},
 {'id': 'C23',
  'network': 'D5',
  'family': (0, 1, 0, 0),
  'classes': None,
  'arcs': None,
  'before_toggle': None,
  'terminal_mask': None,
  'feasible_original': ()},
 {'id': 'C24',
  'network': 'D3',
  'family': (7, 1, 0, 0),
  'classes': (8, 16, 1, 2, 4),
  'arcs': ((0, 2, 3), (0, 3, 7), (0, 4, 0), (1, 4, 9), (2, 0, 4), (2, 3, 5), (2, 4, 0),
           (3, 1, 6), (3, 2, 3), (3, 4, 1), (4, 1, 8), (4, 2, 0)),
  'before_toggle': 28,
  'terminal_mask': 30,
  'feasible_original': (1, 2, 4, 7)},
 {'id': 'C25',
  'network': 'D3',
  'family': (7, 0, 0, 0),
  'classes': (40, 16, 1, 2, 4),
  'arcs': ((0, 2, 3), (0, 3, 7), (0, 4, 0), (1, 4, 9), (2, 0, 4), (2, 3, 5), (2, 4, 0),
           (3, 1, 6), (3, 2, 3), (3, 4, 1), (4, 1, 8), (4, 2, 0)),
  'before_toggle': 29,
  'terminal_mask': 29,
  'feasible_original': (0, 3, 5, 6)},
 {'id': 'C26',
  'network': 'D3',
  'family': (7, 1, 7, 0),
  'classes': (15, 16),
  'arcs': ((0, 1, 14), (1, 0, 9)),
  'before_toggle': 1,
  'terminal_mask': 3,
  'feasible_original': (7,)},
 {'id': 'C27',
  'network': 'D3',
  'family': (7, 0, 7, 0),
  'classes': None,
  'arcs': None,
  'before_toggle': None,
  'terminal_mask': None,
  'feasible_original': ()},
 {'id': 'C28',
  'network': 'D3',
  'family': (7, 0, 0, 7),
  'classes': (40, 23),
  'arcs': ((0, 1, 10), (1, 0, 4)),
  'before_toggle': 3,
  'terminal_mask': 3,
  'feasible_original': (0,)},
 {'id': 'C29',
  'network': 'D3',
  'family': (7, 1, 0, 7),
  'classes': None,
  'arcs': None,
  'before_toggle': None,
  'terminal_mask': None,
  'feasible_original': ()})

# ORACLE-056--068, literal table LIFT_AND_CAPACITY.
LIFT_AND_CAPACITY = ({'id': 'C01-1',
  'reduction': 'C01',
  'reduced': 1,
  'original': 0,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C01-5',
  'reduction': 'C01',
  'reduced': 5,
  'original': 1,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C02-1',
  'reduction': 'C02',
  'reduced': 1,
  'original': 0,
  'cut_value': 0,
  'odd': 0,
  'recovered': 0},
 {'id': 'C02-5',
  'reduction': 'C02',
  'reduced': 5,
  'original': 1,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C03-1',
  'reduction': 'C03',
  'reduced': 1,
  'original': 0,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C03-5',
  'reduction': 'C03',
  'reduced': 5,
  'original': 1,
  'cut_value': 0,
  'odd': 0,
  'recovered': 0},
 {'id': 'C04-1',
  'reduction': 'C04',
  'reduced': 1,
  'original': 1,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C05-1',
  'reduction': 'C05',
  'reduced': 1,
  'original': 0,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C08-1',
  'reduction': 'C08',
  'reduced': 1,
  'original': 0,
  'cut_value': 4,
  'odd': 0,
  'recovered': -3},
 {'id': 'C08-5',
  'reduction': 'C08',
  'reduced': 5,
  'original': 1,
  'cut_value': 6,
  'odd': 1,
  'recovered': -1},
 {'id': 'C08-9',
  'reduction': 'C08',
  'reduced': 9,
  'original': 2,
  'cut_value': 15,
  'odd': 1,
  'recovered': 8},
 {'id': 'C08-13',
  'reduction': 'C08',
  'reduced': 13,
  'original': 3,
  'cut_value': 5,
  'odd': 0,
  'recovered': -2},
 {'id': 'C09-1',
  'reduction': 'C09',
  'reduced': 1,
  'original': 0,
  'cut_value': 4,
  'odd': 1,
  'recovered': -3},
 {'id': 'C09-5',
  'reduction': 'C09',
  'reduced': 5,
  'original': 1,
  'cut_value': 6,
  'odd': 0,
  'recovered': -1},
 {'id': 'C09-9',
  'reduction': 'C09',
  'reduced': 9,
  'original': 2,
  'cut_value': 15,
  'odd': 0,
  'recovered': 8},
 {'id': 'C09-13',
  'reduction': 'C09',
  'reduced': 13,
  'original': 3,
  'cut_value': 5,
  'odd': 1,
  'recovered': -2},
 {'id': 'C10-1',
  'reduction': 'C10',
  'reduced': 1,
  'original': 1,
  'cut_value': 6,
  'odd': 1,
  'recovered': -1},
 {'id': 'C10-5',
  'reduction': 'C10',
  'reduced': 5,
  'original': 3,
  'cut_value': 5,
  'odd': 1,
  'recovered': -2},
 {'id': 'C11-1',
  'reduction': 'C11',
  'reduced': 1,
  'original': 0,
  'cut_value': 4,
  'odd': 0,
  'recovered': -3},
 {'id': 'C11-5',
  'reduction': 'C11',
  'reduced': 5,
  'original': 2,
  'cut_value': 15,
  'odd': 1,
  'recovered': 8},
 {'id': 'C13-1',
  'reduction': 'C13',
  'reduced': 1,
  'original': 1,
  'cut_value': 6,
  'odd': 1,
  'recovered': -1},
 {'id': 'C14-1',
  'reduction': 'C14',
  'reduced': 1,
  'original': 1,
  'cut_value': 12,
  'odd': 1,
  'recovered': 5},
 {'id': 'C14-5',
  'reduction': 'C14',
  'reduced': 5,
  'original': 3,
  'cut_value': 7,
  'odd': 0,
  'recovered': 0},
 {'id': 'C15-1',
  'reduction': 'C15',
  'reduced': 1,
  'original': 1,
  'cut_value': 12,
  'odd': 0,
  'recovered': 5},
 {'id': 'C15-5',
  'reduction': 'C15',
  'reduced': 5,
  'original': 3,
  'cut_value': 7,
  'odd': 1,
  'recovered': 0},
 {'id': 'C17-1',
  'reduction': 'C17',
  'reduced': 1,
  'original': 3,
  'cut_value': 7,
  'odd': 1,
  'recovered': 0},
 {'id': 'C18-1',
  'reduction': 'C18',
  'reduced': 1,
  'original': 3,
  'cut_value': 7,
  'odd': 1,
  'recovered': 0},
 {'id': 'C18-5',
  'reduction': 'C18',
  'reduced': 5,
  'original': 7,
  'cut_value': 14,
  'odd': 0,
  'recovered': 7},
 {'id': 'C19-1',
  'reduction': 'C19',
  'reduced': 1,
  'original': 0,
  'cut_value': 10,
  'odd': 0,
  'recovered': 3},
 {'id': 'C19-5',
  'reduction': 'C19',
  'reduced': 5,
  'original': 1,
  'cut_value': 12,
  'odd': 1,
  'recovered': 5},
 {'id': 'C20-1',
  'reduction': 'C20',
  'reduced': 1,
  'original': 3,
  'cut_value': 0,
  'odd': 1,
  'recovered': -9},
 {'id': 'C20-5',
  'reduction': 'C20',
  'reduced': 5,
  'original': 7,
  'cut_value': 0,
  'odd': 0,
  'recovered': -9},
 {'id': 'C21-1',
  'reduction': 'C21',
  'reduced': 1,
  'original': 7,
  'cut_value': 0,
  'odd': 1,
  'recovered': -9},
 {'id': 'C22-1',
  'reduction': 'C22',
  'reduced': 1,
  'original': 0,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-5',
  'reduction': 'C22',
  'reduced': 5,
  'original': 1,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-9',
  'reduction': 'C22',
  'reduced': 9,
  'original': 2,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-13',
  'reduction': 'C22',
  'reduced': 13,
  'original': 3,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-17',
  'reduction': 'C22',
  'reduced': 17,
  'original': 4,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-21',
  'reduction': 'C22',
  'reduced': 21,
  'original': 5,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-25',
  'reduction': 'C22',
  'reduced': 25,
  'original': 6,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-29',
  'reduction': 'C22',
  'reduced': 29,
  'original': 7,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-33',
  'reduction': 'C22',
  'reduced': 33,
  'original': 8,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-37',
  'reduction': 'C22',
  'reduced': 37,
  'original': 9,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-41',
  'reduction': 'C22',
  'reduced': 41,
  'original': 10,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-45',
  'reduction': 'C22',
  'reduced': 45,
  'original': 11,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-49',
  'reduction': 'C22',
  'reduced': 49,
  'original': 12,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-53',
  'reduction': 'C22',
  'reduced': 53,
  'original': 13,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-57',
  'reduction': 'C22',
  'reduced': 57,
  'original': 14,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C22-61',
  'reduction': 'C22',
  'reduced': 61,
  'original': 15,
  'cut_value': 0,
  'odd': 1,
  'recovered': 0},
 {'id': 'C24-1',
  'reduction': 'C24',
  'reduced': 1,
  'original': 0,
  'cut_value': 10,
  'odd': 0,
  'recovered': 3},
 {'id': 'C24-5',
  'reduction': 'C24',
  'reduced': 5,
  'original': 1,
  'cut_value': 12,
  'odd': 1,
  'recovered': 5},
 {'id': 'C24-9',
  'reduction': 'C24',
  'reduced': 9,
  'original': 2,
  'cut_value': 13,
  'odd': 1,
  'recovered': 6},
 {'id': 'C24-13',
  'reduction': 'C24',
  'reduced': 13,
  'original': 3,
  'cut_value': 7,
  'odd': 0,
  'recovered': 0},
 {'id': 'C24-17',
  'reduction': 'C24',
  'reduced': 17,
  'original': 4,
  'cut_value': 18,
  'odd': 1,
  'recovered': 11},
 {'id': 'C24-21',
  'reduction': 'C24',
  'reduced': 21,
  'original': 5,
  'cut_value': 20,
  'odd': 0,
  'recovered': 13},
 {'id': 'C24-25',
  'reduction': 'C24',
  'reduced': 25,
  'original': 6,
  'cut_value': 20,
  'odd': 0,
  'recovered': 13},
 {'id': 'C24-29',
  'reduction': 'C24',
  'reduced': 29,
  'original': 7,
  'cut_value': 14,
  'odd': 1,
  'recovered': 7},
 {'id': 'C25-1',
  'reduction': 'C25',
  'reduced': 1,
  'original': 0,
  'cut_value': 10,
  'odd': 1,
  'recovered': 3},
 {'id': 'C25-5',
  'reduction': 'C25',
  'reduced': 5,
  'original': 1,
  'cut_value': 12,
  'odd': 0,
  'recovered': 5},
 {'id': 'C25-9',
  'reduction': 'C25',
  'reduced': 9,
  'original': 2,
  'cut_value': 13,
  'odd': 0,
  'recovered': 6},
 {'id': 'C25-13',
  'reduction': 'C25',
  'reduced': 13,
  'original': 3,
  'cut_value': 7,
  'odd': 1,
  'recovered': 0},
 {'id': 'C25-17',
  'reduction': 'C25',
  'reduced': 17,
  'original': 4,
  'cut_value': 18,
  'odd': 0,
  'recovered': 11},
 {'id': 'C25-21',
  'reduction': 'C25',
  'reduced': 21,
  'original': 5,
  'cut_value': 20,
  'odd': 1,
  'recovered': 13},
 {'id': 'C25-25',
  'reduction': 'C25',
  'reduced': 25,
  'original': 6,
  'cut_value': 20,
  'odd': 1,
  'recovered': 13},
 {'id': 'C25-29',
  'reduction': 'C25',
  'reduced': 29,
  'original': 7,
  'cut_value': 14,
  'odd': 0,
  'recovered': 7},
 {'id': 'C26-1',
  'reduction': 'C26',
  'reduced': 1,
  'original': 7,
  'cut_value': 14,
  'odd': 1,
  'recovered': 7},
 {'id': 'C28-1',
  'reduction': 'C28',
  'reduced': 1,
  'original': 0,
  'cut_value': 10,
  'odd': 1,
  'recovered': 3})

# ORACLE-056--068, literal table PROBLEMS.
PROBLEMS = ({'id': 'P01', 'n': 1, 'classes': (3, 4), 'arcs': (), 'terminal_mask': 0},
 {'id': 'P02', 'n': 1, 'classes': (3, 4), 'arcs': (), 'terminal_mask': 3},
 {'id': 'P03', 'n': 1, 'classes': (3, 4), 'arcs': ((0, 1, 5),), 'terminal_mask': 3},
 {'id': 'P04', 'n': 1, 'classes': (3, 4), 'arcs': ((0, 1, 5), (1, 0, 2)), 'terminal_mask': 3},
 {'id': 'P05', 'n': 1, 'classes': (3, 4), 'arcs': ((0, 1, 0), (1, 0, 0)), 'terminal_mask': 3},
 {'id': 'P06',
  'n': 1,
  'classes': (2, 4, 1),
  'arcs': ((0, 2, 2), (2, 1, 3)),
  'terminal_mask': 6},
 {'id': 'P07',
  'n': 1,
  'classes': (2, 4, 1),
  'arcs': ((0, 2, 2), (2, 1, 3)),
  'terminal_mask': 5},
 {'id': 'P08',
  'n': 2,
  'classes': (4, 8, 1, 2),
  'arcs': ((0, 2, 3), (0, 3, 1), (2, 1, 4), (2, 3, 2), (3, 1, 6)),
  'terminal_mask': 12},
 {'id': 'P09', 'n': 2, 'classes': (4, 8, 1, 2), 'arcs': (), 'terminal_mask': 12},
 {'id': 'P10',
  'n': 2,
  'classes': (4, 8, 1, 2),
  'arcs': ((0, 2, 0), (2, 0, 0), (2, 3, 0), (3, 2, 0)),
  'terminal_mask': 9},
 {'id': 'P11',
  'n': 2,
  'classes': (20, 8, 1, 2),
  'arcs': ((0, 2, 1), (1, 3, 2), (2, 0, 1), (2, 3, 3), (3, 1, 2), (3, 2, 3)),
  'terminal_mask': 15},
 {'id': 'P12', 'n': 4, 'classes': (16, 32, 1, 2, 4, 8), 'arcs': (), 'terminal_mask': 60},
 {'id': 'P13',
  'n': 1,
  'classes': (2, 4, 1),
  'arcs': ((0, 1, 7), (1, 0, 9)),
  'terminal_mask': 0},
 {'id': 'P14',
  'n': 3,
  'classes': (8, 16, 1, 2, 4),
  'arcs': ((0, 2, 4), (2, 0, 4), (2, 3, 1), (3, 2, 1), (3, 4, 3), (4, 3, 3)),
  'terminal_mask': 20})

# ORACLE-056--068, literal table MINIMUMS.
MINIMUMS = ({'id': 'P01',
  'minimum': None,
  'all_optimal_shores': (),
  'first_result': None,
  'calls': 0,
  'original_chosen': None},
 {'id': 'P02',
  'minimum': 0,
  'all_optimal_shores': (1,),
  'first_result': 1,
  'calls': 1,
  'original_chosen': 1},
 {'id': 'P03',
  'minimum': 5,
  'all_optimal_shores': (1,),
  'first_result': 1,
  'calls': 1,
  'original_chosen': 1},
 {'id': 'P04',
  'minimum': 5,
  'all_optimal_shores': (1,),
  'first_result': 1,
  'calls': 1,
  'original_chosen': 1},
 {'id': 'P05',
  'minimum': 0,
  'all_optimal_shores': (1,),
  'first_result': 1,
  'calls': 1,
  'original_chosen': 1},
 {'id': 'P06',
  'minimum': 3,
  'all_optimal_shores': (5,),
  'first_result': 5,
  'calls': 3,
  'original_chosen': 1},
 {'id': 'P07',
  'minimum': 2,
  'all_optimal_shores': (1,),
  'first_result': 1,
  'calls': 3,
  'original_chosen': 0},
 {'id': 'P08',
  'minimum': 7,
  'all_optimal_shores': (5,),
  'first_result': 5,
  'calls': 7,
  'original_chosen': 1},
 {'id': 'P09',
  'minimum': 0,
  'all_optimal_shores': (5, 9),
  'first_result': 5,
  'calls': 7,
  'original_chosen': 1},
 {'id': 'P10',
  'minimum': 0,
  'all_optimal_shores': (1, 5),
  'first_result': 1,
  'calls': 7,
  'original_chosen': 0},
 {'id': 'P11',
  'minimum': 1,
  'all_optimal_shores': (1,),
  'first_result': 1,
  'calls': 7,
  'original_chosen': 0},
 {'id': 'P12',
  'minimum': 0,
  'all_optimal_shores': (5, 9, 17, 29, 33, 45, 53, 57),
  'first_result': 5,
  'calls': 21,
  'original_chosen': 1},
 {'id': 'P13',
  'minimum': None,
  'all_optimal_shores': (),
  'first_result': None,
  'calls': 0,
  'original_chosen': None},
 {'id': 'P14',
  'minimum': 1,
  'all_optimal_shores': (5,),
  'first_result': 5,
  'calls': 13,
  'original_chosen': 1})

# ORACLE-056--068, literal table PROBLEM_SHORES.
PROBLEM_SHORES = ({'id': 'P01-1', 'problem': 'P01', 'shore': 1, 'capacity': 0, 'odd': 0},
 {'id': 'P02-1', 'problem': 'P02', 'shore': 1, 'capacity': 0, 'odd': 1},
 {'id': 'P03-1', 'problem': 'P03', 'shore': 1, 'capacity': 5, 'odd': 1},
 {'id': 'P04-1', 'problem': 'P04', 'shore': 1, 'capacity': 5, 'odd': 1},
 {'id': 'P05-1', 'problem': 'P05', 'shore': 1, 'capacity': 0, 'odd': 1},
 {'id': 'P06-1', 'problem': 'P06', 'shore': 1, 'capacity': 2, 'odd': 0},
 {'id': 'P06-5', 'problem': 'P06', 'shore': 5, 'capacity': 3, 'odd': 1},
 {'id': 'P07-1', 'problem': 'P07', 'shore': 1, 'capacity': 2, 'odd': 1},
 {'id': 'P07-5', 'problem': 'P07', 'shore': 5, 'capacity': 3, 'odd': 0},
 {'id': 'P08-1', 'problem': 'P08', 'shore': 1, 'capacity': 4, 'odd': 0},
 {'id': 'P08-5', 'problem': 'P08', 'shore': 5, 'capacity': 7, 'odd': 1},
 {'id': 'P08-9', 'problem': 'P08', 'shore': 9, 'capacity': 9, 'odd': 1},
 {'id': 'P08-13', 'problem': 'P08', 'shore': 13, 'capacity': 10, 'odd': 0},
 {'id': 'P09-1', 'problem': 'P09', 'shore': 1, 'capacity': 0, 'odd': 0},
 {'id': 'P09-5', 'problem': 'P09', 'shore': 5, 'capacity': 0, 'odd': 1},
 {'id': 'P09-9', 'problem': 'P09', 'shore': 9, 'capacity': 0, 'odd': 1},
 {'id': 'P09-13', 'problem': 'P09', 'shore': 13, 'capacity': 0, 'odd': 0},
 {'id': 'P10-1', 'problem': 'P10', 'shore': 1, 'capacity': 0, 'odd': 1},
 {'id': 'P10-5', 'problem': 'P10', 'shore': 5, 'capacity': 0, 'odd': 1},
 {'id': 'P10-9', 'problem': 'P10', 'shore': 9, 'capacity': 0, 'odd': 0},
 {'id': 'P10-13', 'problem': 'P10', 'shore': 13, 'capacity': 0, 'odd': 0},
 {'id': 'P11-1', 'problem': 'P11', 'shore': 1, 'capacity': 1, 'odd': 1},
 {'id': 'P11-5', 'problem': 'P11', 'shore': 5, 'capacity': 3, 'odd': 0},
 {'id': 'P11-9', 'problem': 'P11', 'shore': 9, 'capacity': 6, 'odd': 0},
 {'id': 'P11-13', 'problem': 'P11', 'shore': 13, 'capacity': 2, 'odd': 1},
 {'id': 'P12-1', 'problem': 'P12', 'shore': 1, 'capacity': 0, 'odd': 0},
 {'id': 'P12-5', 'problem': 'P12', 'shore': 5, 'capacity': 0, 'odd': 1},
 {'id': 'P12-9', 'problem': 'P12', 'shore': 9, 'capacity': 0, 'odd': 1},
 {'id': 'P12-13', 'problem': 'P12', 'shore': 13, 'capacity': 0, 'odd': 0},
 {'id': 'P12-17', 'problem': 'P12', 'shore': 17, 'capacity': 0, 'odd': 1},
 {'id': 'P12-21', 'problem': 'P12', 'shore': 21, 'capacity': 0, 'odd': 0},
 {'id': 'P12-25', 'problem': 'P12', 'shore': 25, 'capacity': 0, 'odd': 0},
 {'id': 'P12-29', 'problem': 'P12', 'shore': 29, 'capacity': 0, 'odd': 1},
 {'id': 'P12-33', 'problem': 'P12', 'shore': 33, 'capacity': 0, 'odd': 1},
 {'id': 'P12-37', 'problem': 'P12', 'shore': 37, 'capacity': 0, 'odd': 0},
 {'id': 'P12-41', 'problem': 'P12', 'shore': 41, 'capacity': 0, 'odd': 0},
 {'id': 'P12-45', 'problem': 'P12', 'shore': 45, 'capacity': 0, 'odd': 1},
 {'id': 'P12-49', 'problem': 'P12', 'shore': 49, 'capacity': 0, 'odd': 0},
 {'id': 'P12-53', 'problem': 'P12', 'shore': 53, 'capacity': 0, 'odd': 1},
 {'id': 'P12-57', 'problem': 'P12', 'shore': 57, 'capacity': 0, 'odd': 1},
 {'id': 'P12-61', 'problem': 'P12', 'shore': 61, 'capacity': 0, 'odd': 0},
 {'id': 'P13-1', 'problem': 'P13', 'shore': 1, 'capacity': 7, 'odd': 0},
 {'id': 'P13-5', 'problem': 'P13', 'shore': 5, 'capacity': 7, 'odd': 0},
 {'id': 'P14-1', 'problem': 'P14', 'shore': 1, 'capacity': 4, 'odd': 0},
 {'id': 'P14-5', 'problem': 'P14', 'shore': 5, 'capacity': 1, 'odd': 1},
 {'id': 'P14-9', 'problem': 'P14', 'shore': 9, 'capacity': 8, 'odd': 0},
 {'id': 'P14-13', 'problem': 'P14', 'shore': 13, 'capacity': 3, 'odd': 1},
 {'id': 'P14-17', 'problem': 'P14', 'shore': 17, 'capacity': 7, 'odd': 1},
 {'id': 'P14-21', 'problem': 'P14', 'shore': 21, 'capacity': 4, 'odd': 0},
 {'id': 'P14-25', 'problem': 'P14', 'shore': 25, 'capacity': 5, 'odd': 1},
 {'id': 'P14-29', 'problem': 'P14', 'shore': 29, 'capacity': 0, 'odd': 0})

# ORACLE-056--068, literal table PAIR_ORDERS.
PAIR_ORDERS = ({'N': 2, 'pairs': ((0, 1),), 'calls': 1},
 {'N': 3, 'pairs': ((0, 1), (0, 2), (2, 1)), 'calls': 3},
 {'N': 4, 'pairs': ((0, 1), (0, 2), (0, 3), (2, 1), (2, 3), (3, 1), (3, 2)), 'calls': 7},
 {'N': 5,
  'pairs': ((0, 1), (0, 2), (0, 3), (0, 4), (2, 1), (2, 3), (2, 4), (3, 1), (3, 2), (3, 4),
            (4, 1), (4, 2), (4, 3)),
  'calls': 13},
 {'N': 6,
  'pairs': ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (2, 1), (2, 3), (2, 4), (2, 5), (3, 1),
            (3, 2), (3, 4), (3, 5), (4, 1), (4, 2), (4, 3), (4, 5), (5, 1), (5, 2), (5, 3),
            (5, 4)),
  'calls': 21})

# ORACLE-056--068, literal table PAIR_TRACES.
PAIR_TRACES = ({'id': 'P02-0-1',
  'problem': 'P02',
  'pair': (0, 1),
  'classes': (1, 2),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 1,
  'update': True,
  'incumbent': (0, 1)},
 {'id': 'P04-0-1',
  'problem': 'P04',
  'pair': (0, 1),
  'classes': (1, 2),
  'arcs': ((0, 1, 5), (1, 0, 2)),
  'ordinary_minimum': 5,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 1,
  'update': True,
  'incumbent': (5, 1)},
 {'id': 'P06-0-1',
  'problem': 'P06',
  'pair': (0, 1),
  'classes': (1, 2, 4),
  'arcs': ((0, 2, 2), (2, 1, 3)),
  'ordinary_minimum': 2,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P06-0-2',
  'problem': 'P06',
  'pair': (0, 2),
  'classes': (1, 6),
  'arcs': ((0, 1, 2),),
  'ordinary_minimum': 2,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P06-2-1',
  'problem': 'P06',
  'pair': (2, 1),
  'classes': (5, 2),
  'arcs': ((0, 1, 3),),
  'ordinary_minimum': 3,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 5,
  'odd': 1,
  'update': True,
  'incumbent': (3, 5)},
 {'id': 'P08-0-1',
  'problem': 'P08',
  'pair': (0, 1),
  'classes': (1, 2, 4, 8),
  'arcs': ((0, 2, 3), (0, 3, 1), (2, 1, 4), (2, 3, 2), (3, 1, 6)),
  'ordinary_minimum': 4,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P08-0-2',
  'problem': 'P08',
  'pair': (0, 2),
  'classes': (1, 6, 8),
  'arcs': ((0, 1, 3), (0, 2, 1), (1, 2, 2), (2, 1, 6)),
  'ordinary_minimum': 4,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P08-0-3',
  'problem': 'P08',
  'pair': (0, 3),
  'classes': (1, 10, 4),
  'arcs': ((0, 1, 1), (0, 2, 3), (2, 1, 6)),
  'ordinary_minimum': 4,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P08-2-1',
  'problem': 'P08',
  'pair': (2, 1),
  'classes': (5, 2, 8),
  'arcs': ((0, 1, 4), (0, 2, 3), (2, 1, 6)),
  'ordinary_minimum': 7,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 5,
  'odd': 1,
  'update': True,
  'incumbent': (7, 5)},
 {'id': 'P08-2-3',
  'problem': 'P08',
  'pair': (2, 3),
  'classes': (5, 10),
  'arcs': ((0, 1, 7),),
  'ordinary_minimum': 7,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 5,
  'odd': 1,
  'update': False,
  'incumbent': (7, 5)},
 {'id': 'P08-3-1',
  'problem': 'P08',
  'pair': (3, 1),
  'classes': (9, 2, 4),
  'arcs': ((0, 1, 6), (0, 2, 3), (2, 0, 2), (2, 1, 4)),
  'ordinary_minimum': 9,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 9,
  'odd': 1,
  'update': False,
  'incumbent': (7, 5)},
 {'id': 'P08-3-2',
  'problem': 'P08',
  'pair': (3, 2),
  'classes': (9, 6),
  'arcs': ((0, 1, 9), (1, 0, 2)),
  'ordinary_minimum': 9,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 9,
  'odd': 1,
  'update': False,
  'incumbent': (7, 5)},
 {'id': 'P09-0-1',
  'problem': 'P09',
  'pair': (0, 1),
  'classes': (1, 2, 4, 8),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P09-0-2',
  'problem': 'P09',
  'pair': (0, 2),
  'classes': (1, 6, 8),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P09-0-3',
  'problem': 'P09',
  'pair': (0, 3),
  'classes': (1, 10, 4),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P09-2-1',
  'problem': 'P09',
  'pair': (2, 1),
  'classes': (5, 2, 8),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5),
  'least_temporary': 1,
  'lifted_problem_shore': 5,
  'odd': 1,
  'update': True,
  'incumbent': (0, 5)},
 {'id': 'P09-2-3',
  'problem': 'P09',
  'pair': (2, 3),
  'classes': (5, 10),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 5,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P09-3-1',
  'problem': 'P09',
  'pair': (3, 1),
  'classes': (9, 2, 4),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5),
  'least_temporary': 1,
  'lifted_problem_shore': 9,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P09-3-2',
  'problem': 'P09',
  'pair': (3, 2),
  'classes': (9, 6),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1,),
  'least_temporary': 1,
  'lifted_problem_shore': 9,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-0-1',
  'problem': 'P12',
  'pair': (0, 1),
  'classes': (1, 2, 4, 8, 16, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P12-0-2',
  'problem': 'P12',
  'pair': (0, 2),
  'classes': (1, 6, 8, 16, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13, 17, 21, 25, 29),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P12-0-3',
  'problem': 'P12',
  'pair': (0, 3),
  'classes': (1, 10, 4, 16, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13, 17, 21, 25, 29),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P12-0-4',
  'problem': 'P12',
  'pair': (0, 4),
  'classes': (1, 18, 4, 8, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13, 17, 21, 25, 29),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P12-0-5',
  'problem': 'P12',
  'pair': (0, 5),
  'classes': (1, 34, 4, 8, 16),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13, 17, 21, 25, 29),
  'least_temporary': 1,
  'lifted_problem_shore': 1,
  'odd': 0,
  'update': False,
  'incumbent': None},
 {'id': 'P12-2-1',
  'problem': 'P12',
  'pair': (2, 1),
  'classes': (5, 2, 8, 16, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13, 17, 21, 25, 29),
  'least_temporary': 1,
  'lifted_problem_shore': 5,
  'odd': 1,
  'update': True,
  'incumbent': (0, 5)},
 {'id': 'P12-2-3',
  'problem': 'P12',
  'pair': (2, 3),
  'classes': (5, 10, 16, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 5,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-2-4',
  'problem': 'P12',
  'pair': (2, 4),
  'classes': (5, 18, 8, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 5,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-2-5',
  'problem': 'P12',
  'pair': (2, 5),
  'classes': (5, 34, 8, 16),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 5,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-3-1',
  'problem': 'P12',
  'pair': (3, 1),
  'classes': (9, 2, 4, 16, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13, 17, 21, 25, 29),
  'least_temporary': 1,
  'lifted_problem_shore': 9,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-3-2',
  'problem': 'P12',
  'pair': (3, 2),
  'classes': (9, 6, 16, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 9,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-3-4',
  'problem': 'P12',
  'pair': (3, 4),
  'classes': (9, 18, 4, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 9,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-3-5',
  'problem': 'P12',
  'pair': (3, 5),
  'classes': (9, 34, 4, 16),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 9,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-4-1',
  'problem': 'P12',
  'pair': (4, 1),
  'classes': (17, 2, 4, 8, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13, 17, 21, 25, 29),
  'least_temporary': 1,
  'lifted_problem_shore': 17,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-4-2',
  'problem': 'P12',
  'pair': (4, 2),
  'classes': (17, 6, 8, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 17,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-4-3',
  'problem': 'P12',
  'pair': (4, 3),
  'classes': (17, 10, 4, 32),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 17,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-4-5',
  'problem': 'P12',
  'pair': (4, 5),
  'classes': (17, 34, 4, 8),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 17,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-5-1',
  'problem': 'P12',
  'pair': (5, 1),
  'classes': (33, 2, 4, 8, 16),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13, 17, 21, 25, 29),
  'least_temporary': 1,
  'lifted_problem_shore': 33,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-5-2',
  'problem': 'P12',
  'pair': (5, 2),
  'classes': (33, 6, 8, 16),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 33,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-5-3',
  'problem': 'P12',
  'pair': (5, 3),
  'classes': (33, 10, 4, 16),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 33,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)},
 {'id': 'P12-5-4',
  'problem': 'P12',
  'pair': (5, 4),
  'classes': (33, 18, 4, 8),
  'arcs': (),
  'ordinary_minimum': 0,
  'all_temporary_minimizers': (1, 5, 9, 13),
  'least_temporary': 1,
  'lifted_problem_shore': 33,
  'odd': 1,
  'update': False,
  'incumbent': (0, 5)})

# ORACLE-056--068, literal table ARBITRARY_TIE_TRAP.
ARBITRARY_TIE_TRAP = ({'pair': (0, 1), 'least_shore': 1, 'least_odd': 0, 'wrong_even_minimum': 1},
 {'pair': (0, 2), 'least_shore': 1, 'least_odd': 0, 'wrong_even_minimum': 1},
 {'pair': (0, 3), 'least_shore': 1, 'least_odd': 0, 'wrong_even_minimum': 1},
 {'pair': (0, 4), 'least_shore': 1, 'least_odd': 0, 'wrong_even_minimum': 1},
 {'pair': (0, 5), 'least_shore': 1, 'least_odd': 0, 'wrong_even_minimum': 1},
 {'pair': (2, 1), 'least_shore': 5, 'least_odd': 1, 'wrong_even_minimum': 13},
 {'pair': (2, 3), 'least_shore': 5, 'least_odd': 1, 'wrong_even_minimum': 21},
 {'pair': (2, 4), 'least_shore': 5, 'least_odd': 1, 'wrong_even_minimum': 13},
 {'pair': (2, 5), 'least_shore': 5, 'least_odd': 1, 'wrong_even_minimum': 13},
 {'pair': (3, 1), 'least_shore': 9, 'least_odd': 1, 'wrong_even_minimum': 13},
 {'pair': (3, 2), 'least_shore': 9, 'least_odd': 1, 'wrong_even_minimum': 25},
 {'pair': (3, 4), 'least_shore': 9, 'least_odd': 1, 'wrong_even_minimum': 13},
 {'pair': (3, 5), 'least_shore': 9, 'least_odd': 1, 'wrong_even_minimum': 13},
 {'pair': (4, 1), 'least_shore': 17, 'least_odd': 1, 'wrong_even_minimum': 21},
 {'pair': (4, 2), 'least_shore': 17, 'least_odd': 1, 'wrong_even_minimum': 25},
 {'pair': (4, 3), 'least_shore': 17, 'least_odd': 1, 'wrong_even_minimum': 21},
 {'pair': (4, 5), 'least_shore': 17, 'least_odd': 1, 'wrong_even_minimum': 21},
 {'pair': (5, 1), 'least_shore': 33, 'least_odd': 1, 'wrong_even_minimum': 37},
 {'pair': (5, 2), 'least_shore': 33, 'least_odd': 1, 'wrong_even_minimum': 41},
 {'pair': (5, 3), 'least_shore': 33, 'least_odd': 1, 'wrong_even_minimum': 37},
 {'pair': (5, 4), 'least_shore': 33, 'least_odd': 1, 'wrong_even_minimum': 37})

# ORACLE-056--068, literal table STATS_ANCHORS.
STATS_ANCHORS = (
 {'problem': 'P01', 'calls': 0, 'augmentations': 0, 'bfs_scans': 0, 'peak': 0, 'trace': ()},
 {'problem': 'P02',
  'calls': 1,
  'augmentations': 0,
  'bfs_scans': 0,
  'peak': 0,
  'trace': ((0, 1, 0, 0, 0),)},
 {'problem': 'P03',
  'calls': 1,
  'augmentations': 1,
  'bfs_scans': 2,
  'peak': 5,
  'trace': ((0, 1, 1, 2, 5),)},
 {'problem': 'P04',
  'calls': 1,
  'augmentations': 1,
  'bfs_scans': 3,
  'peak': 5,
  'trace': ((0, 1, 1, 3, 5),)},
 {'problem': 'P05',
  'calls': 1,
  'augmentations': 0,
  'bfs_scans': 2,
  'peak': 0,
  'trace': ((0, 1, 0, 2, 0),)},
 {'problem': 'P06',
  'calls': 3,
  'augmentations': 3,
  'bfs_scans': 8,
  'peak': 3,
  'trace': ((0, 1, 1, 4, 3), (0, 2, 1, 2, 2), (2, 1, 1, 2, 3))},
 {'problem': 'P09',
  'calls': 7,
  'augmentations': 0,
  'bfs_scans': 0,
  'peak': 0,
  'trace': ((0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 0, 0), (2, 1, 0, 0, 0), (2, 3, 0, 0, 0),
            (3, 1, 0, 0, 0), (3, 2, 0, 0, 0))},
 {'problem': 'P12',
  'calls': 21,
  'augmentations': 0,
  'bfs_scans': 0,
  'peak': 0,
  'trace': ((0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 0, 0), (0, 4, 0, 0, 0), (0, 5, 0, 0, 0),
            (2, 1, 0, 0, 0), (2, 3, 0, 0, 0), (2, 4, 0, 0, 0), (2, 5, 0, 0, 0), (3, 1, 0, 0, 0),
            (3, 2, 0, 0, 0), (3, 4, 0, 0, 0), (3, 5, 0, 0, 0), (4, 1, 0, 0, 0), (4, 2, 0, 0, 0),
            (4, 3, 0, 0, 0), (4, 5, 0, 0, 0), (5, 1, 0, 0, 0), (5, 2, 0, 0, 0), (5, 3, 0, 0, 0),
            (5, 4, 0, 0, 0))})

# ORACLE-056--068, literal table INSTANCES.
INSTANCES = ({'id': 'RICH',
  'n': 5,
  'edges': ((0, 2, 2), (1, 2, 2), (2, 4, 1), (3, 4, 1)),
  'f': (1, 1, 1, 1, 2)},
 {'id': 'MIXED',
  'n': 4,
  'edges': ((0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 4), (1, 3, 2), (2, 3, 5)),
  'f': (2, 3, 4, 5)})

# ORACLE-056--068, literal table BRANCH_SEAMS.
BRANCH_SEAMS = ({'id': 'RICH-j0-0-1',
  'instance': 'RICH',
  'branch': 0,
  'parameter': (0, 1),
  'family': (3, 1, 0, 0),
  'gamma': (1, 1, 1, 1, 2),
  'negative_shift': 0,
  'constant': -1,
  'classes': (32, 64, 1, 2, 4, 8, 16),
  'terminal_mask': 12,
  'arcs': ((1, 2, 1), (1, 3, 1), (1, 4, 1), (1, 5, 1), (1, 6, 2), (2, 1, 1), (2, 4, 2),
           (3, 1, 1), (3, 4, 2), (4, 1, 1), (4, 2, 2), (4, 3, 2), (4, 6, 1), (5, 1, 1),
           (5, 6, 1), (6, 1, 2), (6, 4, 1), (6, 5, 1)),
  'minimum_cut': 3,
  'reduced_choice': 5,
  'original_choice': 1,
  'minimum_residual': 2,
  'original_optima': (1, 2),
  'calls': 31,
  'unrestricted_cut': 0},
 {'id': 'RICH-j1-0-1',
  'instance': 'RICH',
  'branch': 1,
  'parameter': (0, 1),
  'family': (3, 0, 1, 4),
  'gamma': (1, 1, 1, 1, 2),
  'negative_shift': 0,
  'constant': -2,
  'classes': (161, 68, 2, 8, 16),
  'terminal_mask': 6,
  'arcs': ((0, 1, 3), (1, 0, 3), (1, 2, 3), (1, 3, 1), (1, 4, 3), (2, 1, 3), (3, 1, 1),
           (3, 4, 1), (4, 1, 3), (4, 3, 1)),
  'minimum_cut': 6,
  'reduced_choice': 5,
  'original_choice': 3,
  'minimum_residual': 4,
  'original_optima': (3,),
  'calls': 13,
  'unrestricted_cut': 0},
 {'id': 'RICH-j2-0-1',
  'instance': 'RICH',
  'branch': 2,
  'parameter': (0, 1),
  'family': (15, 1, 16, 0),
  'gamma': (-2, -2, -5, -1, -2),
  'negative_shift': 12,
  'constant': 0,
  'classes': (48, 64, 1, 2, 4, 8),
  'terminal_mask': 60,
  'arcs': ((0, 2, 2), (0, 3, 2), (0, 4, 6), (0, 5, 2), (2, 0, 2), (2, 4, 2), (3, 0, 2),
           (3, 4, 2), (4, 0, 6), (4, 2, 2), (4, 3, 2), (5, 0, 2)),
  'minimum_cut': 2,
  'reduced_choice': 29,
  'original_choice': 23,
  'minimum_residual': -10,
  'original_optima': (23,),
  'calls': 21,
  'unrestricted_cut': 0},
 {'id': 'RICH-j3-0-1',
  'instance': 'RICH',
  'branch': 3,
  'parameter': (0, 1),
  'family': (15, 0, 1, 4),
  'gamma': (-2, -2, -5, -1, -2),
  'negative_shift': 12,
  'constant': -2,
  'classes': (161, 68, 2, 8, 16),
  'terminal_mask': 12,
  'arcs': ((0, 1, 7), (0, 2, 2), (0, 3, 1), (0, 4, 2), (1, 0, 7), (1, 2, 2), (1, 4, 1),
           (2, 0, 2), (2, 1, 2), (3, 0, 1), (3, 4, 1), (4, 0, 2), (4, 1, 1), (4, 3, 1)),
  'minimum_cut': 10,
  'reduced_choice': 25,
  'original_choice': 25,
  'minimum_residual': -4,
  'original_optima': (25,),
  'calls': 13,
  'unrestricted_cut': 0},
 {'id': 'RICH-j0-2-3',
  'instance': 'RICH',
  'branch': 0,
  'parameter': (2, 3),
  'family': (3, 1, 0, 0),
  'gamma': (1, 1, -5, 3, 6),
  'negative_shift': 5,
  'constant': -5,
  'classes': (32, 64, 1, 2, 4, 8, 16),
  'terminal_mask': 12,
  'arcs': ((0, 4, 5), (1, 2, 1), (1, 3, 1), (1, 5, 3), (1, 6, 6), (2, 1, 1), (2, 4, 6),
           (3, 1, 1), (3, 4, 6), (4, 0, 5), (4, 2, 6), (4, 3, 6), (4, 6, 3), (5, 1, 3),
           (5, 6, 3), (6, 1, 6), (6, 4, 3), (6, 5, 3)),
  'minimum_cut': 10,
  'reduced_choice': 21,
  'original_choice': 5,
  'minimum_residual': 0,
  'original_optima': (5, 6),
  'calls': 31,
  'unrestricted_cut': 5},
 {'id': 'RICH-j1-2-3',
  'instance': 'RICH',
  'branch': 1,
  'parameter': (2, 3),
  'family': (3, 0, 1, 4),
  'gamma': (1, 1, -5, 3, 6),
  'negative_shift': 5,
  'constant': -6,
  'classes': (161, 68, 2, 8, 16),
  'terminal_mask': 6,
  'arcs': ((0, 1, 12), (1, 0, 12), (1, 2, 7), (1, 3, 3), (1, 4, 9), (2, 1, 7), (3, 1, 3),
           (3, 4, 3), (4, 1, 9), (4, 3, 3)),
  'minimum_cut': 19,
  'reduced_choice': 5,
  'original_choice': 3,
  'minimum_residual': 8,
  'original_optima': (3,),
  'calls': 13,
  'unrestricted_cut': 5},
 {'id': 'RICH-j2-2-3',
  'instance': 'RICH',
  'branch': 2,
  'parameter': (2, 3),
  'family': (15, 1, 16, 0),
  'gamma': (-8, -8, -17, -5, -10),
  'negative_shift': 48,
  'constant': 2,
  'classes': (48, 64, 1, 2, 4, 8),
  'terminal_mask': 60,
  'arcs': ((0, 2, 8), (0, 3, 8), (0, 4, 20), (0, 5, 8), (2, 0, 8), (2, 4, 6), (3, 0, 8),
           (3, 4, 6), (4, 0, 20), (4, 2, 6), (4, 3, 6), (5, 0, 8)),
  'minimum_cut': 8,
  'reduced_choice': 29,
  'original_choice': 23,
  'minimum_residual': -38,
  'original_optima': (23,),
  'calls': 21,
  'unrestricted_cut': 0},
 {'id': 'RICH-j3-2-3',
  'instance': 'RICH',
  'branch': 3,
  'parameter': (2, 3),
  'family': (15, 0, 1, 4),
  'gamma': (-8, -8, -17, -5, -10),
  'negative_shift': 48,
  'constant': -6,
  'classes': (161, 68, 2, 8, 16),
  'terminal_mask': 12,
  'arcs': ((0, 1, 23), (0, 2, 8), (0, 3, 5), (0, 4, 10), (1, 0, 23), (1, 2, 6), (1, 4, 3),
           (2, 0, 8), (2, 1, 6), (3, 0, 5), (3, 4, 3), (4, 0, 10), (4, 1, 3), (4, 3, 3)),
  'minimum_cut': 34,
  'reduced_choice': 25,
  'original_choice': 25,
  'minimum_residual': -20,
  'original_optima': (25,),
  'calls': 13,
  'unrestricted_cut': 0},
 {'id': 'RICH-j0--3-1',
  'instance': 'RICH',
  'branch': 0,
  'parameter': (-3, 1),
  'family': (3, 1, 0, 0),
  'gamma': (4, 4, 13, 1, 2),
  'negative_shift': 0,
  'constant': 2,
  'classes': (32, 64, 1, 2, 4, 8, 16),
  'terminal_mask': 12,
  'arcs': ((1, 2, 4), (1, 3, 4), (1, 4, 13), (1, 5, 1), (1, 6, 2), (2, 1, 4), (2, 4, 2),
           (3, 1, 4), (3, 4, 2), (4, 1, 13), (4, 2, 2), (4, 3, 2), (4, 6, 1), (5, 1, 1),
           (5, 6, 1), (6, 1, 2), (6, 4, 1), (6, 5, 1)),
  'minimum_cut': 6,
  'reduced_choice': 5,
  'original_choice': 1,
  'minimum_residual': 8,
  'original_optima': (1, 2),
  'calls': 31,
  'unrestricted_cut': 0},
 {'id': 'RICH-j1--3-1',
  'instance': 'RICH',
  'branch': 1,
  'parameter': (-3, 1),
  'family': (3, 0, 1, 4),
  'gamma': (4, 4, 13, 1, 2),
  'negative_shift': 0,
  'constant': -2,
  'classes': (161, 68, 2, 8, 16),
  'terminal_mask': 6,
  'arcs': ((0, 1, 6), (1, 0, 6), (1, 2, 6), (1, 3, 1), (1, 4, 3), (2, 1, 6), (3, 1, 1),
           (3, 4, 1), (4, 1, 3), (4, 3, 1)),
  'minimum_cut': 12,
  'reduced_choice': 5,
  'original_choice': 3,
  'minimum_residual': 10,
  'original_optima': (3,),
  'calls': 13,
  'unrestricted_cut': 0},
 {'id': 'RICH-j2--3-1',
  'instance': 'RICH',
  'branch': 2,
  'parameter': (-3, 1),
  'family': (15, 1, 16, 0),
  'gamma': (1, 1, -2, 2, 4),
  'negative_shift': 2,
  'constant': -3,
  'classes': (48, 64, 1, 2, 4, 8),
  'terminal_mask': 60,
  'arcs': ((0, 1, 4), (0, 4, 3), (0, 5, 1), (1, 0, 4), (1, 2, 1), (1, 3, 1), (1, 5, 2),
           (2, 1, 1), (2, 4, 2), (3, 1, 1), (3, 4, 2), (4, 0, 3), (4, 2, 2), (4, 3, 2),
           (5, 0, 1), (5, 1, 2)),
  'minimum_cut': 7,
  'reduced_choice': 29,
  'original_choice': 23,
  'minimum_residual': 2,
  'original_optima': (23,),
  'calls': 21,
  'unrestricted_cut': 2},
 {'id': 'RICH-j3--3-1',
  'instance': 'RICH',
  'branch': 3,
  'parameter': (-3, 1),
  'family': (15, 0, 1, 4),
  'gamma': (1, 1, -2, 2, 4),
  'negative_shift': 2,
  'constant': -2,
  'classes': (161, 68, 2, 8, 16),
  'terminal_mask': 12,
  'arcs': ((0, 1, 5), (1, 0, 5), (1, 2, 3), (1, 3, 2), (1, 4, 5), (2, 1, 3), (3, 1, 2),
           (3, 4, 1), (4, 1, 5), (4, 3, 1)),
  'minimum_cut': 8,
  'reduced_choice': 5,
  'original_choice': 3,
  'minimum_residual': 4,
  'original_optima': (3, 9),
  'calls': 13,
  'unrestricted_cut': 2},
 {'id': 'MIXED-j0-0-1',
  'instance': 'MIXED',
  'branch': 0,
  'parameter': (0, 1),
  'family': (10, 1, 0, 0),
  'gamma': (2, 3, 4, 5),
  'negative_shift': 0,
  'constant': -1,
  'classes': (16, 32, 1, 2, 4, 8),
  'terminal_mask': 40,
  'arcs': ((1, 2, 2), (1, 3, 3), (1, 4, 4), (1, 5, 5), (2, 1, 2), (2, 3, 2), (2, 4, 3),
           (2, 5, 1), (3, 1, 3), (3, 2, 2), (3, 4, 4), (3, 5, 2), (4, 1, 4), (4, 2, 3),
           (4, 3, 4), (4, 5, 5), (5, 1, 5), (5, 2, 1), (5, 3, 2), (5, 4, 5)),
  'minimum_cut': 11,
  'reduced_choice': 9,
  'original_choice': 2,
  'minimum_residual': 10,
  'original_optima': (2,),
  'calls': 21,
  'unrestricted_cut': 0},
 {'id': 'MIXED-j1-0-1',
  'instance': 'MIXED',
  'branch': 1,
  'parameter': (0, 1),
  'family': (10, 0, 1, 2),
  'gamma': (2, 3, 4, 5),
  'negative_shift': 0,
  'constant': -2,
  'classes': (81, 34, 4, 8),
  'terminal_mask': 9,
  'arcs': ((0, 1, 4), (0, 2, 3), (0, 3, 1), (1, 0, 4), (1, 2, 8), (1, 3, 7), (2, 0, 3),
           (2, 1, 8), (2, 3, 5), (3, 0, 1), (3, 1, 7), (3, 2, 5)),
  'minimum_cut': 8,
  'reduced_choice': 1,
  'original_choice': 1,
  'minimum_residual': 6,
  'original_optima': (1,),
  'calls': 7,
  'unrestricted_cut': 0},
 {'id': 'MIXED-j2-0-1',
  'instance': 'MIXED',
  'branch': 2,
  'parameter': (0, 1),
  'family': (10, 1, 1, 0),
  'gamma': (-6, -8, -12, -8),
  'negative_shift': 34,
  'constant': 0,
  'classes': (17, 32, 2, 4, 8),
  'terminal_mask': 20,
  'arcs': ((0, 2, 10), (0, 3, 15), (0, 4, 9), (2, 0, 10), (2, 3, 4), (2, 4, 2), (3, 0, 15),
           (3, 2, 4), (3, 4, 5), (4, 0, 9), (4, 2, 2), (4, 3, 5)),
  'minimum_cut': 16,
  'reduced_choice': 25,
  'original_choice': 13,
  'minimum_residual': -18,
  'original_optima': (7, 13),
  'calls': 13,
  'unrestricted_cut': 0},
 {'id': 'MIXED-j3-0-1',
  'instance': 'MIXED',
  'branch': 3,
  'parameter': (0, 1),
  'family': (10, 0, 1, 2),
  'gamma': (-6, -8, -12, -8),
  'negative_shift': 34,
  'constant': -2,
  'classes': (81, 34, 4, 8),
  'terminal_mask': 9,
  'arcs': ((0, 1, 10), (0, 2, 15), (0, 3, 9), (1, 0, 10), (1, 2, 4), (1, 3, 2), (2, 0, 15),
           (2, 1, 4), (2, 3, 5), (3, 0, 9), (3, 1, 2), (3, 2, 5)),
  'minimum_cut': 28,
  'reduced_choice': 5,
  'original_choice': 5,
  'minimum_residual': -8,
  'original_optima': (5,),
  'calls': 7,
  'unrestricted_cut': 0},
 {'id': 'MIXED-j0-2-3',
  'instance': 'MIXED',
  'branch': 0,
  'parameter': (2, 3),
  'family': (10, 1, 0, 0),
  'gamma': (-2, -1, -4, 9),
  'negative_shift': 7,
  'constant': -5,
  'classes': (16, 32, 1, 2, 4, 8),
  'terminal_mask': 40,
  'arcs': ((0, 2, 2), (0, 3, 1), (0, 4, 4), (1, 5, 9), (2, 0, 2), (2, 3, 6), (2, 4, 9),
           (2, 5, 3), (3, 0, 1), (3, 2, 6), (3, 4, 12), (3, 5, 6), (4, 0, 4), (4, 2, 9),
           (4, 3, 12), (4, 5, 15), (5, 1, 9), (5, 2, 3), (5, 3, 6), (5, 4, 15)),
  'minimum_cut': 24,
  'reduced_choice': 29,
  'original_choice': 7,
  'minimum_residual': 12,
  'original_optima': (7,),
  'calls': 21,
  'unrestricted_cut': 7},
 {'id': 'MIXED-j1-2-3',
  'instance': 'MIXED',
  'branch': 1,
  'parameter': (2, 3),
  'family': (10, 0, 1, 2),
  'gamma': (-2, -1, -4, 9),
  'negative_shift': 7,
  'constant': -6,
  'classes': (81, 34, 4, 8),
  'terminal_mask': 9,
  'arcs': ((0, 1, 7), (0, 2, 13), (0, 3, 3), (1, 0, 7), (1, 2, 12), (1, 3, 15), (2, 0, 13),
           (2, 1, 12), (2, 3, 15), (3, 0, 3), (3, 1, 15), (3, 2, 15)),
  'minimum_cut': 23,
  'reduced_choice': 1,
  'original_choice': 1,
  'minimum_residual': 10,
  'original_optima': (1,),
  'calls': 7,
  'unrestricted_cut': 7},
 {'id': 'MIXED-j2-2-3',
  'instance': 'MIXED',
  'branch': 2,
  'parameter': (2, 3),
  'family': (10, 1, 1, 0),
  'gamma': (-22, -30, -44, -34),
  'negative_shift': 130,
  'constant': 2,
  'classes': (17, 32, 2, 4, 8),
  'terminal_mask': 20,
  'arcs': ((0, 2, 36), (0, 3, 53), (0, 4, 37), (2, 0, 36), (2, 3, 12), (2, 4, 6), (3, 0, 53),
           (3, 2, 12), (3, 4, 15), (4, 0, 37), (4, 2, 6), (4, 3, 15)),
  'minimum_cut': 54,
  'reduced_choice': 25,
  'original_choice': 13,
  'minimum_residual': -74,
  'original_optima': (13,),
  'calls': 13,
  'unrestricted_cut': 0},
 {'id': 'MIXED-j3-2-3',
  'instance': 'MIXED',
  'branch': 3,
  'parameter': (2, 3),
  'family': (10, 0, 1, 2),
  'gamma': (-22, -30, -44, -34),
  'negative_shift': 130,
  'constant': -6,
  'classes': (81, 34, 4, 8),
  'terminal_mask': 9,
  'arcs': ((0, 1, 36), (0, 2, 53), (0, 3, 37), (1, 0, 36), (1, 2, 12), (1, 3, 6), (2, 0, 53),
           (2, 1, 12), (2, 3, 15), (3, 0, 37), (3, 1, 6), (3, 2, 15)),
  'minimum_cut': 100,
  'reduced_choice': 5,
  'original_choice': 5,
  'minimum_residual': -36,
  'original_optima': (5,),
  'calls': 7,
  'unrestricted_cut': 0},
 {'id': 'MIXED-j0--3-1',
  'instance': 'MIXED',
  'branch': 0,
  'parameter': (-3, 1),
  'family': (10, 1, 0, 0),
  'gamma': (14, 18, 28, 14),
  'negative_shift': 0,
  'constant': 2,
  'classes': (16, 32, 1, 2, 4, 8),
  'terminal_mask': 40,
  'arcs': ((1, 2, 14), (1, 3, 18), (1, 4, 28), (1, 5, 14), (2, 1, 14), (2, 3, 2), (2, 4, 3),
           (2, 5, 1), (3, 1, 18), (3, 2, 2), (3, 4, 4), (3, 5, 2), (4, 1, 28), (4, 2, 3),
           (4, 3, 4), (4, 5, 5), (5, 1, 14), (5, 2, 1), (5, 3, 2), (5, 4, 5)),
  'minimum_cut': 22,
  'reduced_choice': 33,
  'original_choice': 8,
  'minimum_residual': 24,
  'original_optima': (8,),
  'calls': 21,
  'unrestricted_cut': 0},
 {'id': 'MIXED-j1--3-1',
  'instance': 'MIXED',
  'branch': 1,
  'parameter': (-3, 1),
  'family': (10, 0, 1, 2),
  'gamma': (14, 18, 28, 14),
  'negative_shift': 0,
  'constant': -2,
  'classes': (81, 34, 4, 8),
  'terminal_mask': 9,
  'arcs': ((0, 1, 16), (0, 2, 3), (0, 3, 1), (1, 0, 16), (1, 2, 32), (1, 3, 16), (2, 0, 3),
           (2, 1, 32), (2, 3, 5), (3, 0, 1), (3, 1, 16), (3, 2, 5)),
  'minimum_cut': 20,
  'reduced_choice': 1,
  'original_choice': 1,
  'minimum_residual': 18,
  'original_optima': (1,),
  'calls': 7,
  'unrestricted_cut': 0},
 {'id': 'MIXED-j2--3-1',
  'instance': 'MIXED',
  'branch': 2,
  'parameter': (-3, 1),
  'family': (10, 1, 1, 0),
  'gamma': (0, 1, 0, 7),
  'negative_shift': 0,
  'constant': -3,
  'classes': (17, 32, 2, 4, 8),
  'terminal_mask': 20,
  'arcs': ((0, 1, 0), (0, 2, 2), (0, 3, 3), (0, 4, 1), (1, 0, 0), (1, 2, 1), (1, 3, 0),
           (1, 4, 7), (2, 0, 2), (2, 1, 1), (2, 3, 4), (2, 4, 2), (3, 0, 3), (3, 1, 0),
           (3, 2, 4), (3, 4, 5), (4, 0, 1), (4, 1, 7), (4, 2, 2), (4, 3, 5)),
  'minimum_cut': 9,
  'reduced_choice': 13,
  'original_choice': 7,
  'minimum_residual': 6,
  'original_optima': (7,),
  'calls': 13,
  'unrestricted_cut': 0},
 {'id': 'MIXED-j3--3-1',
  'instance': 'MIXED',
  'branch': 3,
  'parameter': (-3, 1),
  'family': (10, 0, 1, 2),
  'gamma': (0, 1, 0, 7),
  'negative_shift': 0,
  'constant': -2,
  'classes': (81, 34, 4, 8),
  'terminal_mask': 9,
  'arcs': ((0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 0, 2), (1, 2, 4), (1, 3, 9), (2, 0, 3),
           (2, 1, 4), (2, 3, 5), (3, 0, 1), (3, 1, 9), (3, 2, 5)),
  'minimum_cut': 6,
  'reduced_choice': 1,
  'original_choice': 1,
  'minimum_residual': 4,
  'original_optima': (1,),
  'calls': 7,
  'unrestricted_cut': 0})

GRAPH_COUNTS = {'distinct_graph_pair_minimizations': 28868,
 'graphs': 4164,
 'terminal_problems': 33032,
 'all_shore_evaluations': 131592,
 'infeasible': 4164,
 'feasible': 28868,
 'parity_admissible_shores': 65796,
 'specified_backend_calls': 201284,
 'zero_minima': 5018,
 'candidate_parity_acceptances': 115076,
 'positive_minima': 23850,
 'multiple_optima': 11296}

FAMILY_COUNTS = {'descriptors': 18720,
 'disjoint_descriptors': 6216,
 'feasible': 4656,
 'pi0_feasible': 2448,
 'toggle_add': 1894,
 'geometric_lift_checks': 15612,
 'odd_shores': 9360,
 'original_admissible_shores': 9360,
 'overlap_none': 12504,
 'parity_none': 1560,
 'toggle_none': 2208,
 'pi1_feasible': 2208,
 'toggle_remove': 554}

FIXED_COUNTS = {'raw_networks': 6,
 'reduction_fixtures': 29,
 'feasible_reduction_fixtures': 22,
 'literal_lift_rows': 67,
 'problem_fixtures': 14,
 'problem_shore_rows': 51,
 'ordinary_trace_rows': 40,
 'arbitrary_tie_trap_rows': 21,
 'stats_anchors': 8,
 'seam_cases': 24,
 'rejection_declarations': 122,
 'valid_record_declarations': 14}

LARGE_EXPONENTS = (1, 8, 64, 4096)

BASE_PATHS = ('.gitignore',
 'CITATION.cff',
 'GOVERNING_SHA256SUMS.txt',
 'README.md',
 'docs/CONFORMANCE.md',
 'docs/CONTRACT.md',
 'docs/DESIGN.md',
 'docs/ORACLE_CATALOG.md',
 'docs/SPEC_LOCK.md',
 'docs/TEST_PLAN.md',
 'exactfrac/__init__.py',
 'exactfrac/families.py',
 'exactfrac/flow.py',
 'exactfrac/instance.py',
 'exactfrac/rational.py',
 'exactfrac/shore.py',
 'exactfrac/sign_routing.py',
 'exactfrac/witness.py',
 'exactfrac_verify/__init__.py',
 'exactfrac_verify/brute.py',
 'instances/MANIFEST',
 'pyproject.toml',
 'tests/test_families.py',
 'tests/test_flow.py',
 'tests/test_instance.py',
 'tests/test_rational.py',
 'tests/test_shore.py',
 'tests/test_sign_routing.py',
 'tests/test_verify_brute.py',
 'tests/test_witness.py')

class IntSubclass(int):
    pass


class TupleSubclass(tuple):
    pass


class NetworkSubclass(SignRoutedNetwork):
    pass


class FamilySubclass(AtomicFamily):
    pass


class ProblemSubclass(Problem):
    pass


class Hostile:
    """No argument validation may execute an untrusted conversion or protocol hook."""

    def _fail(self, *args: object, **kwargs: object) -> object:
        raise AssertionError("hostile protocol hook executed")

    __int__ = __index__ = __float__ = __bool__ = _fail
    __iter__ = __len__ = __getitem__ = _fail
    __lt__ = __le__ = __gt__ = __ge__ = __eq__ = _fail
    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = _fail
    __and__ = __rand__ = __or__ = __ror__ = __xor__ = __rxor__ = _fail


class ExplosiveInt(int):
    def _fail(self, *args: object) -> object:
        raise AssertionError("numeric subclass was compared or converted")

    __lt__ = __le__ = __gt__ = __ge__ = __eq__ = _fail
    __int__ = __index__ = _fail


class ExplosiveTuple(tuple):
    def _fail(self, *args: object) -> object:
        raise AssertionError("container subclass was traversed")

    __iter__ = __len__ = __getitem__ = _fail


def _row(rows: tuple[dict, ...], name: str) -> dict:
    return next(item for item in rows if item["id"] == name)


def _arcs(rows: tuple) -> tuple[tuple[int, int, int], ...]:
    return tuple(tuple(row) for row in rows)


def _network(name: str) -> SignRoutedNetwork:
    item = _row(RAW_NETWORKS, name)
    return SignRoutedNetwork(item["n"], _arcs(item["arcs"]), item["shift"], item["constant"])


def _problem(name: str) -> object:
    item = _row(PROBLEMS, name)
    return Problem(item["n"], tuple(item["classes"]), _arcs(item["arcs"]), item["terminal_mask"])


def _problem_fields(problem: object) -> tuple:
    assert type(problem) is Problem
    return problem.vertex_count, problem.classes, problem.arcs, problem.terminal_mask


def _stats_fields(stats: object) -> tuple[int, int, int, int]:
    assert type(stats) is Stats
    data = (stats.mincut_calls, stats.flow_augmentations,
            stats.flow_bfs_scans, stats.flow_peak_generated_value)
    assert all(type(value) is int and value >= 0 for value in data)
    return data


def _result_fields(result: object) -> tuple[int, int] | None:
    if result is None:
        return None
    assert type(result) is Result
    assert type(result.cut_value) is int and type(result.source_shore) is int
    return result.cut_value, result.source_shore


def _unpack(observed: object) -> tuple[object, object]:
    assert type(observed) is tuple and len(observed) == 2
    result, stats = observed
    _result_fields(result)
    _stats_fields(stats)
    return result, stats


def _exact_error(function: Callable, *args: object) -> None:
    with pytest.raises(ValueError) as caught:
        function(*args)
    assert type(caught.value) is ValueError


def _members(mask: int) -> frozenset[int]:
    return frozenset(index for index in range(mask.bit_length()) if mask & (1 << index))


def _mask(vertices: frozenset[int] | set[int]) -> int:
    return sum(1 << vertex for vertex in vertices)


def _source_shores(count: int) -> tuple[int, ...]:
    return tuple(mask for mask in range(1 << count) if mask & 1 and not mask & 2)


def _cut(arcs: tuple, shore: int) -> int:
    included = _members(shore)
    return sum(value for tail, head, value in arcs if tail in included and head not in included)


def _lift(classes: tuple[int, ...], shore: int) -> int:
    members: set[int] = set()
    for index in _members(shore):
        members.update(_members(classes[index]))
    return _mask(members)


def _transport(arcs: tuple, classes: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    # Independent class-membership evaluation, deliberately not a production map helper.
    totals: dict[tuple[int, int], int] = {}
    for tail, head, value in arcs:
        left = next(i for i, group in enumerate(classes) if tail in _members(group))
        right = next(i for i, group in enumerate(classes) if head in _members(group))
        if left != right:
            key = left, right
            totals[key] = totals.get(key, 0) + value
    return tuple((a, b, totals[a, b]) for a, b in sorted(totals))


def _original_allowed(n: int, descriptor: tuple[int, int, int, int]) -> tuple[int, ...]:
    terminals, parity, inside, outside = descriptor
    required = _members(inside)
    forbidden = _members(outside)
    return tuple(shore for shore in range(1 << n)
                 if required <= _members(shore) and not (forbidden & _members(shore))
                 and len(_members(shore) & _members(terminals)) % 2 == parity)


def _expected_reduction(n: int, arcs: tuple, descriptor: tuple) -> tuple | None:
    if not _original_allowed(n, descriptor):
        return None
    terminals, parity, inside, outside = descriptor
    groups = [set(_members(inside)) | {n}, set(_members(outside)) | {n + 1}]
    tokens = set(_members(terminals))
    if parity == 0:
        groups[0].add(n + 2)
        tokens.add(n + 2)
    groups.extend({v} for v in range(n) if v not in groups[0] and v not in groups[1])
    classes = tuple(_mask(group) for group in groups)
    before = _mask({i for i, group in enumerate(groups) if len(group & tokens) % 2})
    final = before ^ 2 if len(_members(before)) % 2 else before
    return classes, _transport(arcs, classes), before, final


def _pairs(count: int) -> tuple[tuple[int, int], ...]:
    return tuple((a, b) for a in range(count) for b in range(count)
                 if a != 1 and b != 0 and a != b)


def _pair_classes(count: int, a: int, b: int) -> tuple[int, ...]:
    groups = ({0, a}, {1, b}, *({v} for v in range(count) if v not in (0, 1, a, b)))
    return tuple(_mask(group) for group in groups)


def _least(values: dict[int, int], permitted: tuple[int, ...]) -> tuple[int, int]:
    best = min(values[shore] for shore in permitted)
    optima = [shore for shore in permitted if values[shore] == best]
    intersection = set(_members(optima[0]))
    for shore in optima[1:]:
        intersection.intersection_update(_members(shore))
    return best, _mask(intersection)


def _expected_candidates(count: int, arcs: tuple) -> tuple[tuple[int, int], ...]:
    shores = _source_shores(count)
    values = {shore: _cut(arcs, shore) for shore in shores}
    return tuple(_least(values, tuple(shore for shore in shores
                                     if a in _members(shore) and b not in _members(shore)))
                 for a, b in _pairs(count))


def _expected_minimum(count: int, arcs: tuple, terminals: int) -> tuple[int, int] | None:
    shores = _source_shores(count)
    admissible = tuple(shore for shore in shores if len(_members(shore) & _members(terminals)) % 2)
    if not admissible:
        return None
    optimum = min(_cut(arcs, shore) for shore in admissible)
    first = None
    for value, shore in _expected_candidates(count, arcs):
        if shore in admissible and (first is None or value < first[0]):
            first = value, shore
    assert first is not None and first[0] == optimum
    return first


def _swap_import(monkeypatch: pytest.MonkeyPatch, original: object, substitute: object) -> None:
    names = [name for name, value in vars(parity_cut).items() if value is original]
    assert names, "required closed dependency is not directly consumed"
    for name in names:
        monkeypatch.setattr(parity_cut, name, substitute)


def _backend_args(args: tuple, kwargs: dict) -> tuple[int, int, int, tuple]:
    bound = inspect.signature(closed_minimum_cut).bind(*args, **kwargs)
    return tuple(bound.arguments[key] for key in ("n", "source", "sink", "arcs"))


def _least_backend_result(count: int, arcs: tuple, result: MinCutResult) -> None:
    values = {shore: _cut(arcs, shore) for shore in _source_shores(count)}
    assert _least(values, tuple(values)) == (result.value, result.source_shore)


def _signature(function: Callable, expected: dict[str, object]) -> None:
    signature = inspect.signature(function)
    assert tuple(signature.parameters) == tuple(k for k in expected if k != "return")
    assert all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
               and p.default is inspect.Parameter.empty for p in signature.parameters.values())
    target = function.__init__ if inspect.isclass(function) else function
    hints = get_type_hints(target)
    if inspect.isclass(function):
        hints.pop("return", None)
    assert hints == expected


def _fingerprints(root: Path) -> dict[str, str]:
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in (*BASE_PATHS, "exactfrac/parity_cut.py", "tests/test_parity_cut.py")}


@pytest.fixture(scope="module", autouse=True)
def _no_input_file_mutation() -> Iterator[None]:
    root = Path(__file__).resolve().parents[1]
    before = _fingerprints(root)
    yield
    assert _fingerprints(root) == before


def _rejection_cases() -> tuple[tuple[str, Callable[[], object]], ...]:
    ParityCutProblem = Problem
    ParityCutResult = Result
    ParityCutStats = Stats
    reduce_atomic_family = parity_cut.reduce_atomic_family
    lift_source_shore = parity_cut.lift_source_shore
    minimum_parity_cut = parity_cut.minimum_parity_cut
    F = AtomicFamily(1, 1, 0, 0)
    SN = SignRoutedNetwork(1, (), 0, 0)
    P = Problem(1, (2, 4, 1), (), 6)
    return (
        ('RJ001', lambda: ParityCutProblem(True, (2, 4, 1), (), 0)),
        ('RJ002', lambda: ParityCutProblem(1.0, (2, 4, 1), (), 0)),
        ('RJ003', lambda: ParityCutProblem(Fraction(1, 1), (2, 4, 1), (), 0)),
        ('RJ004', lambda: ParityCutProblem(IntSubclass(1), (2, 4, 1), (), 0)),
        ('RJ005', lambda: ParityCutProblem(0, (2, 4, 1), (), 0)),
        ('RJ006', lambda: ParityCutProblem(-1, (2, 4, 1), (), 0)),
        ('RJ007', lambda: ParityCutProblem(None, (2, 4, 1), (), 0)),
        ('RJ008', lambda: ParityCutProblem(1, [2, 4, 1], (), 0)),
        ('RJ009', lambda: ParityCutProblem(1, TupleSubclass((2, 4, 1)), (), 0)),
        ('RJ010', lambda: ParityCutProblem(1, iter((2, 4, 1)), (), 0)),
        ('RJ011', lambda: ParityCutProblem(1, (), (), 0)),
        ('RJ012', lambda: ParityCutProblem(1, (7,), (), 0)),
        ('RJ013', lambda: ParityCutProblem(1, (True, 4, 1), (), 0)),
        ('RJ014', lambda: ParityCutProblem(1, (2, 4, IntSubclass(1)), (), 0)),
        ('RJ015', lambda: ParityCutProblem(1, (2, 4, 0), (), 0)),
        ('RJ016', lambda: ParityCutProblem(1, (2, 4, -1), (), 0)),
        ('RJ017', lambda: ParityCutProblem(1, (2, 4, 1.0), (), 0)),
        ('RJ018', lambda: ParityCutProblem(1, (2, 4, 16), (), 0)),
        ('RJ019', lambda: ParityCutProblem(1, (1, 4, 2), (), 0)),
        ('RJ020', lambda: ParityCutProblem(1, (6, 1), (), 0)),
        ('RJ021', lambda: ParityCutProblem(1, (2, 5, 1), (), 0)),
        ('RJ022', lambda: ParityCutProblem(1, (2, 4), (), 0)),
        ('RJ023', lambda: ParityCutProblem(1, (4, 2, 1), (), 0)),
        ('RJ024', lambda: ParityCutProblem(1, (2, 12, 1), (), 0)),
        ('RJ025', lambda: ParityCutProblem(1, (2, 4, 9), (), 0)),
        ('RJ026', lambda: ParityCutProblem(1, (10, 4, 9), (), 0)),
        ('RJ027', lambda: ParityCutProblem(2, (4, 8, 3), (), 0)),
        ('RJ028', lambda: ParityCutProblem(2, (4, 8, 2, 1), (), 0)),
        ('RJ029', lambda: ParityCutProblem(2, (5, 8, 1, 2), (), 0)),
        ('RJ030', lambda: ParityCutProblem(2, (4, 8, 1, 1), (), 0)),
        ('RJ031', lambda: ParityCutProblem(2, (4, 8, 1), (), 0)),
        ('RJ032', lambda: ParityCutProblem(1, (2, 4, 1), [], 0)),
        ('RJ033', lambda: ParityCutProblem(1, (2, 4, 1), TupleSubclass(()), 0)),
        ('RJ034', lambda: ParityCutProblem(1, (2, 4, 1), iter(()), 0)),
        ('RJ035', lambda: ParityCutProblem(1, (2, 4, 1), ([0, 1, 0],), 0)),
        ('RJ036', lambda: ParityCutProblem(1, (2, 4, 1), (TupleSubclass((0, 1, 0)),), 0)),
        ('RJ037', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 1),), 0)),
        ('RJ038', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 1, 0, 0),), 0)),
        ('RJ039', lambda: ParityCutProblem(1, (2, 4, 1), ((True, 1, 0),), 0)),
        ('RJ040', lambda: ParityCutProblem(1, (2, 4, 1), ((0, False, 0),), 0)),
        ('RJ041', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 1, False),), 0)),
        ('RJ042', lambda: ParityCutProblem(1, (2, 4, 1), ((IntSubclass(0), 1, 0),), 0)),
        ('RJ043', lambda: ParityCutProblem(1, (2, 4, 1), ((0, IntSubclass(1), 0),), 0)),
        ('RJ044', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 1, IntSubclass(0)),), 0)),
        ('RJ045', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 1, 0.0),), 0)),
        ('RJ046', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 1, Fraction(0, 1)),), 0)),
        ('RJ047', lambda: ParityCutProblem(1, (2, 4, 1), ((-1, 1, 0),), 0)),
        ('RJ048', lambda: ParityCutProblem(1, (2, 4, 1), ((0, -1, 0),), 0)),
        ('RJ049', lambda: ParityCutProblem(1, (2, 4, 1), ((3, 1, 0),), 0)),
        ('RJ050', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 3, 0),), 0)),
        ('RJ051', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 0, 0),), 0)),
        ('RJ052', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 1, -1),), 0)),
        ('RJ053', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 2, 1), (0, 1, 2)), 0)),
        ('RJ054', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 1, 0), (0, 1, 0)), 0)),
        ('RJ055', lambda: ParityCutProblem(1, (2, 4, 1), ((0, 1, 1), (0, 1, 2)), 0)),
        ('RJ056', lambda: ParityCutProblem(1, (2, 4, 1), (), True)),
        ('RJ057', lambda: ParityCutProblem(1, (2, 4, 1), (), -1)),
        ('RJ058', lambda: ParityCutProblem(1, (2, 4, 1), (), 1.0)),
        ('RJ059', lambda: ParityCutProblem(1, (2, 4, 1), (), Fraction(0, 1))),
        ('RJ060', lambda: ParityCutProblem(1, (2, 4, 1), (), IntSubclass(0))),
        ('RJ061', lambda: ParityCutProblem(1, (2, 4, 1), (), 8)),
        ('RJ062', lambda: ParityCutProblem(1, (2, 4, 1), (), 1)),
        ('RJ063', lambda: ParityCutProblem(1, (2, 4, 1), (), None)),
        ('RJ064', lambda: ParityCutResult(True, 1)),
        ('RJ065', lambda: ParityCutResult(-1, 1)),
        ('RJ066', lambda: ParityCutResult(1.0, 1)),
        ('RJ067', lambda: ParityCutResult(Fraction(0, 1), 1)),
        ('RJ068', lambda: ParityCutResult(IntSubclass(0), 1)),
        ('RJ069', lambda: ParityCutResult(None, 1)),
        ('RJ070', lambda: ParityCutResult(0, False)),
        ('RJ071', lambda: ParityCutResult(0, -1)),
        ('RJ072', lambda: ParityCutResult(0, 1.0)),
        ('RJ073', lambda: ParityCutResult(0, IntSubclass(1))),
        ('RJ074', lambda: ParityCutResult(0, 0)),
        ('RJ075', lambda: ParityCutResult(0, 2)),
        ('RJ076', lambda: ParityCutResult(0, 3)),
        ('RJ077', lambda: ParityCutResult(0, 6)),
        ('RJ078', lambda: ParityCutResult(0, None)),
        ('RJ079', lambda: ParityCutStats(False, 0, 0, 0)),
        ('RJ080', lambda: ParityCutStats(-1, 0, 0, 0)),
        ('RJ081', lambda: ParityCutStats(1.0, 0, 0, 0)),
        ('RJ082', lambda: ParityCutStats(IntSubclass(0), 0, 0, 0)),
        ('RJ083', lambda: ParityCutStats(0, False, 0, 0)),
        ('RJ084', lambda: ParityCutStats(0, -1, 0, 0)),
        ('RJ085', lambda: ParityCutStats(0, 1.0, 0, 0)),
        ('RJ086', lambda: ParityCutStats(0, IntSubclass(0), 0, 0)),
        ('RJ087', lambda: ParityCutStats(0, 0, False, 0)),
        ('RJ088', lambda: ParityCutStats(0, 0, -1, 0)),
        ('RJ089', lambda: ParityCutStats(0, 0, 1.0, 0)),
        ('RJ090', lambda: ParityCutStats(0, 0, IntSubclass(0), 0)),
        ('RJ091', lambda: ParityCutStats(0, 0, 0, False)),
        ('RJ092', lambda: ParityCutStats(0, 0, 0, -1)),
        ('RJ093', lambda: ParityCutStats(0, 0, 0, 1.0)),
        ('RJ094', lambda: ParityCutStats(0, 0, 0, IntSubclass(0))),
        ('RJ095', lambda: reduce_atomic_family(None, F)),
        ('RJ096', lambda: reduce_atomic_family(Hostile(), F)),
        ('RJ097', lambda: reduce_atomic_family(NetworkSubclass(1, (), 0, 0), F)),
        ('RJ098', lambda: reduce_atomic_family(SN, None)),
        ('RJ099', lambda: reduce_atomic_family(SN, Hostile())),
        ('RJ100', lambda: reduce_atomic_family(SN, FamilySubclass(1, 1, 0, 0))),
        ('RJ101', lambda: reduce_atomic_family(SN, AtomicFamily(2, 1, 0, 0))),
        ('RJ102', lambda: reduce_atomic_family(SN, AtomicFamily(0, 0, 2, 0))),
        ('RJ103', lambda: reduce_atomic_family(SN, AtomicFamily(0, 0, 0, 2))),
        ('RJ104', lambda: reduce_atomic_family(SN, AtomicFamily(2, 0, 1, 1))),
        ('RJ105', lambda: reduce_atomic_family(SN, AtomicFamily(0, 1, 2, 0))),
        ('RJ106', lambda: reduce_atomic_family(SN, AtomicFamily(0, 1, 0, 2))),
        ('RJ107', lambda: lift_source_shore(None, 1)),
        ('RJ108', lambda: lift_source_shore(Hostile(), 1)),
        ('RJ109', lambda: minimum_parity_cut(None)),
        ('RJ110', lambda: minimum_parity_cut(Hostile())),
        ('RJ111', lambda: minimum_parity_cut(ProblemSubclass(1, (2, 4, 1), (), 6))),
        ('RJ112', lambda: lift_source_shore(P, True)),
        ('RJ113', lambda: lift_source_shore(P, -1)),
        ('RJ114', lambda: lift_source_shore(P, 1.0)),
        ('RJ115', lambda: lift_source_shore(P, IntSubclass(1))),
        ('RJ116', lambda: lift_source_shore(P, 8)),
        ('RJ117', lambda: lift_source_shore(P, 9)),
        ('RJ118', lambda: lift_source_shore(P, 0)),
        ('RJ119', lambda: lift_source_shore(P, 2)),
        ('RJ120', lambda: lift_source_shore(P, 3)),
        ('RJ121', lambda: lift_source_shore(P, 7)),
        ('RJ122', lambda: lift_source_shore(P, Hostile())),
    )

def _valid_cases() -> tuple[tuple[str, Callable[[], object]], ...]:
    ParityCutProblem = Problem
    ParityCutResult = Result
    ParityCutStats = Stats
    lift_source_shore = parity_cut.lift_source_shore
    P = Problem(1, (2, 4, 1), (), 6)
    return (
        ('V01', lambda: ParityCutProblem(1, (2, 4, 1), (), 0)),
        ('V02', lambda: ParityCutProblem(1, (10, 4, 1), (), 3)),
        ('V03', lambda: ParityCutProblem(1, (3, 4), (), 3)),
        ('V04', lambda: ParityCutProblem(1, (2, 5), (), 3)),
        ('V05', lambda: ParityCutProblem(2, (4, 8, 1, 2), ((0, 2, 0), (2, 0, 0)), 12)),
        ('V06', lambda: ParityCutProblem(1, (2, 4, 1), ((1, 0, 9),), 3)),
        ('V07', lambda: ParityCutProblem(1, (2, 4, 1), (), 5)),
        ('V08', lambda: ParityCutProblem(1, (2, 4, 1), (), 6)),
        ('V09', lambda: ParityCutResult(0, 1)),
        ('V10', lambda: ParityCutResult(7, 1048577)),
        ('V11', lambda: ParityCutStats(0, 0, 0, 0)),
        ('V12', lambda: ParityCutStats(0, 7, 9, 10)),
        ('V13', lambda: lift_source_shore(P, 1)),
        ('V14', lambda: lift_source_shore(P, 5)),
    )

def test_public_surface_signatures_and_annotations() -> None:
    assert parity_cut.__all__ == EXPECTED_EXPORTS
    assert type(parity_cut.__all__) is tuple
    _signature(Problem, {"vertex_count": int, "classes": tuple[int, ...],
                         "arcs": tuple[tuple[int, int, int], ...], "terminal_mask": int})
    _signature(Result, {"cut_value": int, "source_shore": int})
    _signature(Stats, {"mincut_calls": int, "flow_augmentations": int,
                       "flow_bfs_scans": int, "flow_peak_generated_value": int})
    _signature(parity_cut.reduce_atomic_family,
               {"network": SignRoutedNetwork, "family": AtomicFamily, "return": Problem | None})
    _signature(parity_cut.lift_source_shore,
               {"problem": Problem, "source_shore": int, "return": int})
    _signature(parity_cut.minimum_parity_cut,
               {"problem": Problem, "return": tuple[Result | None, Stats]})
    problem = Problem(vertex_count=1, classes=(2, 4, 1), arcs=(), terminal_mask=6)
    result, stats = _unpack(parity_cut.minimum_parity_cut(problem=problem))
    assert _result_fields(result) == (0, 5)
    assert _stats_fields(stats) == (3, 0, 0, 0)
    assert parity_cut.lift_source_shore(problem=problem, source_shore=5) == 1
    reduced = parity_cut.reduce_atomic_family(
        network=SignRoutedNetwork(1, (), 0, 0), family=AtomicFamily(1, 1, 0, 0),
    )
    assert _problem_fields(reduced) == (1, (2, 4, 1), (), 6)
    with pytest.raises(TypeError):
        parity_cut.reduce_atomic_family()


def test_records_are_frozen_slotted_structural_and_not_certificates() -> None:
    samples = (Problem(1, (2, 4, 1), (), 6), Result(0, 1), Stats(0, 7, 9, 10))
    names = (("vertex_count", "classes", "arcs", "terminal_mask"),
             ("cut_value", "source_shore"),
             ("mincut_calls", "flow_augmentations", "flow_bfs_scans", "flow_peak_generated_value"))
    for record, expected_names in zip(samples, names, strict=True):
        cls = type(record)
        assert is_dataclass(record)
        assert tuple(field.name for field in fields(record)) == expected_names
        assert tuple(cls.__slots__) == expected_names
        assert not hasattr(record, "__dict__")
        assert cls.__dataclass_params__.frozen and not cls.__dataclass_params__.order
        assert all(field.default is MISSING and field.default_factory is MISSING
                   for field in fields(record))
        twin = cls(*(getattr(record, name) for name in expected_names))
        assert record == twin and hash(record) == hash(twin)
        with pytest.raises(FrozenInstanceError):
            setattr(record, expected_names[0], 9)
        with pytest.raises(TypeError):
            _ = record < twin
    problem = samples[0]
    for name, expected in (("source", 0), ("sink", 1), ("node_count", 3)):
        assert type(getattr(problem, name)) is int and getattr(problem, name) == expected
        assert isinstance(getattr(Problem, name), property)
        assert getattr(Problem, name).fset is None
        with pytest.raises((AttributeError, TypeError)):
            setattr(problem, name, 20)
    # These intentionally valid shapes assert neither parity nor actual solver diagnostics.
    assert Result(7, (1 << 20) | 1).source_shore == 1048577
    assert _stats_fields(samples[2]) == (0, 7, 9, 10)
    assert Result(1, 1) != Result(2, 1)


def test_all_fourteen_registered_valid_record_declarations() -> None:
    cases = _valid_cases()
    assert len(cases) == 14
    values = {name: factory() for name, factory in cases}
    assert _problem_fields(values["V01"]) == (1, (2, 4, 1), (), 0)
    assert values["V02"].classes == (10, 4, 1)
    assert values["V03"].node_count == values["V04"].node_count == 2
    assert values["V05"].arcs == ((0, 2, 0), (2, 0, 0))
    assert values["V06"].arcs == ((1, 0, 9),)
    assert (values["V07"].terminal_mask, values["V08"].terminal_mask) == (5, 6)
    assert _result_fields(values["V09"]) == (0, 1)
    assert _result_fields(values["V10"]) == (7, 1048577)
    assert _stats_fields(values["V11"]) == (0, 0, 0, 0)
    assert _stats_fields(values["V12"]) == (0, 7, 9, 10)
    assert type(values["V13"]) is int and values["V13"] == 0
    assert type(values["V14"]) is int and values["V14"] == 1


def test_all_122_registered_exact_valueerror_cases() -> None:
    cases = _rejection_cases()
    assert len(cases) == 122
    assert tuple(name for name, _ in cases) == tuple(f"RJ{n:03d}" for n in range(1, 123))
    for name, factory in cases:
        with pytest.raises(ValueError) as caught:
            factory()
        assert type(caught.value) is ValueError, name


def test_supplementary_hostile_exact_types_and_record_guard_order() -> None:
    for invalid in (Hostile(), ExplosiveInt(1), True, Fraction(1, 1)):
        _exact_error(Problem, invalid, Hostile(), Hostile(), Hostile())
        _exact_error(Problem, 1, (2, 4, invalid), Hostile(), Hostile())
        _exact_error(Problem, 1, (2, 4, 1), ((invalid, Hostile(), Hostile()),), Hostile())
        _exact_error(Problem, 1, (2, 4, 1), ((0, invalid, Hostile()),), Hostile())
        _exact_error(Problem, 1, (2, 4, 1), ((0, 1, invalid),), Hostile())
        _exact_error(Problem, 1, (2, 4, 1), (), invalid)
        _exact_error(Result, invalid, Hostile())
        _exact_error(Result, 0, invalid)
        for index in range(4):
            args = tuple(0 if i < index else invalid if i == index else Hostile()
                         for i in range(4))
            _exact_error(Stats, *args)
    _exact_error(Problem, 1, ExplosiveTuple((2, 4, 1)), Hostile(), Hostile())
    _exact_error(Problem, 1, (2, 4, 1), ExplosiveTuple(()), Hostile())
    _exact_error(Problem, 1, (2, 4, 1), (ExplosiveTuple((0, 1, 0)),), Hostile())
    # Capacity's exact type must be checked before numerical endpoint comparisons.
    _exact_error(Problem, 1, (2, 4, 1), ((-1, 1, Hostile()),), 0)
    verifier = BruteInstance(2, ((0, 1, 1),), (1, 1))
    for invalid in (None, Hostile(), verifier, NetworkSubclass(1, (), 0, 0)):
        _exact_error(parity_cut.reduce_atomic_family, invalid, Hostile())
        _exact_error(parity_cut.lift_source_shore, invalid, Hostile())
        _exact_error(parity_cut.minimum_parity_cut, invalid)


def test_reduction_uses_closed_guards_before_predicate_and_capacity_scan(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events = []
    network = SignRoutedNetwork(2, (), 0, 0)
    predicate = AtomicFamily.is_nonempty.fget
    getter = SignRoutedNetwork.__getattribute__
    assert predicate is not None

    def validate(n: int, shore: object) -> int:
        events.append(("validate", n, shore))
        return closed_validate_shore(n, shore)

    def nonempty(family: AtomicFamily) -> bool:
        events.append(("predicate",))
        return predicate(family)

    def guarded(record: SignRoutedNetwork, name: str) -> object:
        if name == "arcs":
            raise AssertionError("invalid/infeasible input scanned capacities")
        return getter(record, name)

    with monkeypatch.context() as context:
        _swap_import(context, closed_validate_shore, validate)
        context.setattr(AtomicFamily, "is_nonempty", property(nonempty))
        context.setattr(SignRoutedNetwork, "__getattribute__", guarded)
        _exact_error(parity_cut.reduce_atomic_family, Hostile(), Hostile())
        _exact_error(parity_cut.reduce_atomic_family, network, Hostile())
        assert not events
        cases = ((AtomicFamily(4, 0, 1, 1), (4,)),
                 (AtomicFamily(3, 0, 4, 1), (3, 4)),
                 (AtomicFamily(3, 0, 1, 4), (3, 1, 4)))
        for family, values in cases:
            events.clear()
            _exact_error(parity_cut.reduce_atomic_family, network, family)
            assert events == [("validate", 2, value) for value in values]
        for family in (AtomicFamily(3, 0, 1, 1), AtomicFamily(0, 1, 0, 0)):
            events.clear()
            assert parity_cut.reduce_atomic_family(network, family) is None
            assert events == [("validate", 2, family.T), ("validate", 2, family.I),
                              ("validate", 2, family.O), ("predicate",)]
    # Replacing only the closed logical predicate must control the empty-family decision.
    with monkeypatch.context() as context:
        context.setattr(AtomicFamily, "is_nonempty", property(lambda self: False))
        context.setattr(SignRoutedNetwork, "__getattribute__", guarded)
        assert parity_cut.reduce_atomic_family(network, AtomicFamily(3, 1, 0, 0)) is None


def test_fixed_contractions_exact_classes_arcs_and_raw_order_invariance() -> None:
    checked = 0
    for row in REDUCTIONS:
        network = _network(row["network"])
        family = AtomicFamily(*row["family"])
        before = network, family, hash(network), hash(family)
        reduced = parity_cut.reduce_atomic_family(network, family)
        if row["classes"] is None:
            assert reduced is None, row["id"]
        else:
            expected = (network.vertex_count, tuple(row["classes"]),
                        _arcs(row["arcs"]), row["terminal_mask"])
            assert _problem_fields(reduced) == expected, row["id"]
            assert tuple((a, b) for a, b, _ in reduced.arcs) == tuple(
                sorted({(a, b) for a, b, _ in reduced.arcs}))
            variants = (tuple(reversed(network.arcs)),
                        tuple(part for a, b, c in network.arcs
                              for part in ((a, b, c // 2), (a, b, c - c // 2))))
            for arcs in variants:
                alternate = SignRoutedNetwork(network.vertex_count, arcs,
                                              network.negative_shift, network.constant)
                assert parity_cut.reduce_atomic_family(alternate, family) == reduced
            checked += 1
        assert before == (network, family, hash(network), hash(family))
    assert (len(REDUCTIONS), checked) == (29, 22)


def test_anchor_xor_and_sink_toggle_have_literal_distinct_meanings() -> None:
    removals = 0
    for row in REDUCTIONS:
        if row["classes"] is None:
            continue
        network = _network(row["network"])
        terminals, pi, _, _ = row["family"]
        reduced = parity_cut.reduce_atomic_family(network, AtomicFamily(*row["family"]))
        tokens = set(_members(terminals))
        if pi == 0:
            tokens.add(network.vertex_count + 2)
        counted = _mask({i for i, group in enumerate(row["classes"])
                         if len(_members(group) & tokens) % 2})
        assert counted == row["before_toggle"]
        expected = counted ^ 2 if counted.bit_count() % 2 else counted
        assert reduced.terminal_mask == expected == row["terminal_mask"]
        assert bool(reduced.classes[0] & (1 << (network.vertex_count + 2))) == (pi == 0)
        assert sum(group.bit_count() for group in reduced.classes) == network.node_count + (pi == 0)
        for shore in _source_shores(reduced.node_count):
            assert (shore & counted).bit_count() % 2 == (shore & expected).bit_count() % 2
        removals += int(counted.bit_count() % 2 and bool(counted & 2))
    removal = _row(REDUCTIONS, "C20")
    assert (removal["before_toggle"], removal["terminal_mask"]) == (7, 5)
    assert removals > 0


def test_parity_anchor_correspondence(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> object:
        raise AssertionError("correspondence test must not invoke optimization")

    totals: Counter[str] = Counter()
    with monkeypatch.context() as context:
        _swap_import(context, closed_minimum_cut, forbidden)
        context.setattr(parity_cut, "minimum_parity_cut", forbidden)
        for n in (1, 2, 3, 4):
            for style in (0, 1):
                arcs = () if not style else tuple(
                    (u, v, ((u + 1) * (v + 2)) % 5)
                    for u in range(n + 2) for v in range(n + 2) if u != v)
                network = SignRoutedNetwork(n, arcs, 11, -7)
                for terminal, pi, inside, outside in product(
                    range(1 << n), (0, 1), range(1 << n), range(1 << n),
                ):
                    descriptor = terminal, pi, inside, outside
                    totals["descriptors"] += 1
                    allowed = _original_allowed(n, descriptor)
                    reduced = parity_cut.reduce_atomic_family(network, AtomicFamily(*descriptor))
                    if inside & outside:
                        assert not allowed and reduced is None
                        totals["overlap_none"] += 1
                        continue
                    totals["disjoint_descriptors"] += 1
                    if not allowed:
                        assert reduced is None
                        totals["parity_none"] += 1
                        continue
                    expected = _expected_reduction(n, arcs, descriptor)
                    assert expected is not None
                    classes, normalized, before, final = expected
                    assert _problem_fields(reduced) == (n, classes, normalized, final)
                    totals["feasible"] += 1
                    totals["pi0_feasible" if pi == 0 else "pi1_feasible"] += 1
                    if before.bit_count() % 2:
                        totals["toggle_remove" if before & 2 else "toggle_add"] += 1
                    else:
                        totals["toggle_none"] += 1
                    images = []
                    geometry = []
                    for shore in _source_shores(len(classes)):
                        original = _lift(classes, shore) & ((1 << n) - 1)
                        actual = parity_cut.lift_source_shore(reduced, shore)
                        assert type(actual) is int and actual == original
                        assert _members(inside) <= _members(actual)
                        assert not (_members(actual) & _members(outside))
                        assert _cut(reduced.arcs, shore) == _cut(arcs, original | (1 << n))
                        odd = len(_members(shore) & _members(final)) % 2
                        assert bool(odd) == (original in allowed)
                        totals["geometric_lift_checks"] += 1
                        geometry.append(original)
                        if odd:
                            images.append(original)
                            totals["odd_shores"] += 1
                    assert len(geometry) == len(set(geometry))
                    assert tuple(sorted(images)) == allowed
                    totals["original_admissible_shores"] += len(allowed)
    assert dict(totals) == FAMILY_COUNTS


def test_lifting_all_literal_rows_in_both_parities_without_graph_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_getter = Problem.__getattribute__

    def guarded(record: object, name: str) -> object:
        if name in ("arcs", "terminal_mask"):
            raise AssertionError("lifting inspected capacity or imposed a parity condition")
        return original_getter(record, name)

    problems = {}
    for row in REDUCTIONS:
        if row["classes"] is not None:
            problems[row["id"]] = Problem(_network(row["network"]).vertex_count,
                                          tuple(row["classes"]), _arcs(row["arcs"]),
                                          row["terminal_mask"])
    with monkeypatch.context() as context:
        context.setattr(Problem, "__getattribute__", guarded)
        for row in LIFT_AND_CAPACITY:
            observed = parity_cut.lift_source_shore(problems[row["reduction"]], row["reduced"])
            assert type(observed) is int and observed == row["original"]
    assert len(LIFT_AND_CAPACITY) == 67
    assert {row["odd"] for row in LIFT_AND_CAPACITY} == {0, 1}


def test_lift_closed_mask_validation_and_constructor_trust(monkeypatch: pytest.MonkeyPatch) -> None:
    problem = _problem("P06")
    calls = []

    def validate(n: int, mask: object) -> int:
        calls.append((n, mask))
        return closed_validate_shore(n, mask)

    def forbidden(*args: object, **kwargs: object) -> object:
        raise AssertionError("consumer reconstructed an already-valid immutable problem")

    with monkeypatch.context() as context:
        _swap_import(context, closed_validate_shore, validate)
        context.setattr(Problem, "__post_init__", forbidden)
        assert parity_cut.lift_source_shore(problem, 5) == 1
        assert calls == [(3, 5)]
        _exact_error(parity_cut.lift_source_shore, problem, 9)
        _exact_error(parity_cut.lift_source_shore, problem, 2)
        assert calls == [(3, 5), (3, 9), (3, 2)]


def test_literal_minimum_results_shores_and_separate_stats() -> None:
    for row in MINIMUMS:
        problem = _problem(row["id"])
        before = _problem_fields(problem), hash(problem)
        result, stats = _unpack(parity_cut.minimum_parity_cut(problem))
        expected = None if row["minimum"] is None else (row["minimum"], row["first_result"])
        assert _result_fields(result) == expected, row["id"]
        assert stats.mincut_calls == row["calls"]
        if result is None:
            assert _stats_fields(stats) == (0, 0, 0, 0)
        else:
            assert 0 <= result.source_shore < (1 << problem.node_count)
            assert result.source_shore & 1 and not result.source_shore & 2
            assert (result.source_shore & problem.terminal_mask).bit_count() % 2 == 1
            assert _cut(problem.arcs, result.source_shore) == result.cut_value
            assert result.source_shore in row["all_optimal_shores"]
            assert parity_cut.lift_source_shore(
                problem, result.source_shore,
            ) == row["original_chosen"]
        assert before == (_problem_fields(problem), hash(problem))
    for row in PROBLEM_SHORES:
        problem = _problem(row["problem"])
        assert _cut(problem.arcs, row["shore"]) == row["capacity"]
        assert (row["shore"] & problem.terminal_mask).bit_count() % 2 == row["odd"]
    assert (len(MINIMUMS), len(PROBLEM_SHORES)) == (14, 51)


def test_zero_terminal_shortcut_does_not_read_arcs_or_call_flow(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    problems = (_problem("P01"), _problem("P13"))
    getter = Problem.__getattribute__

    def guarded(record: object, name: str) -> object:
        if name in ("arcs", "classes", "vertex_count", "node_count"):
            raise AssertionError("empty-T shortcut performed graph work")
        return getter(record, name)

    def forbidden(*args: object, **kwargs: object) -> object:
        raise AssertionError("empty-T shortcut invoked flow")

    with monkeypatch.context() as context:
        _swap_import(context, closed_minimum_cut, forbidden)
        context.setattr(Problem, "__getattribute__", guarded)
        for problem in problems:
            result, stats = _unpack(parity_cut.minimum_parity_cut(problem))
            assert result is None and _stats_fields(stats) == (0, 0, 0, 0)


def test_fixed_query_traces_and_least_backend_shores(monkeypatch: pytest.MonkeyPatch) -> None:
    grouped: dict[str, list[dict]] = {}
    for row in PAIR_TRACES:
        grouped.setdefault(row["problem"], []).append(row)
    count = 0
    for name, rows in grouped.items():
        observed = []

        def checked(
            *args: object, _rows: list = rows, _observed: list = observed, **kwargs: object,
        ) -> MinCutResult:
            n, source, sink, arcs = _backend_args(args, kwargs)
            row = _rows[len(_observed)]
            assert (n, source, sink, arcs) == (len(row["classes"]), 0, 1, _arcs(row["arcs"]))
            result = closed_minimum_cut(n, source, sink, arcs)
            _least_backend_result(n, arcs, result)
            assert (result.value, result.source_shore) == (
                row["ordinary_minimum"], row["least_temporary"])
            assert _lift(tuple(row["classes"]), result.source_shore) == row["lifted_problem_shore"]
            _observed.append(result)
            return result

        with monkeypatch.context() as context:
            _swap_import(context, closed_minimum_cut, checked)
            result, stats = _unpack(parity_cut.minimum_parity_cut(_problem(name)))
        expected = _row(MINIMUMS, name)
        assert _result_fields(result) == (expected["minimum"], expected["first_result"])
        assert len(observed) == len(rows) == stats.mincut_calls
        count += len(observed)
    assert count == 40


def test_all_compatible_pair_orders_including_zero_value_early_exit_trap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for row in PAIR_ORDERS:
        count = row["N"]
        # Capacity identifiers make even geometrically duplicate-looking restrictions observable.
        arcs = tuple((u, v, 1 << (u * count + v)) for u in range(count)
                     for v in range(count) if u != v)
        n = max(1, count - 2)
        classes = (3, 4) if count == 2 else (
            1 << n, 1 << (n + 1), *(1 << v for v in range(n)),
        )
        problem = Problem(n, classes, arcs, 3)
        expected_pairs = tuple(tuple(pair) for pair in row["pairs"])
        assert expected_pairs == _pairs(count)
        actual = []

        def checked(
            *args: object, _expected_pairs: tuple = expected_pairs, _actual: list = actual,
            _count: int = count, _base_arcs: tuple = arcs, **kwargs: object,
        ) -> MinCutResult:
            temporary_count, source, sink, query_arcs = _backend_args(args, kwargs)
            a, b = _expected_pairs[len(_actual)]
            query_classes = _pair_classes(_count, a, b)
            assert (temporary_count, source, sink, query_arcs) == (
                len(query_classes), 0, 1, _transport(_base_arcs, query_classes))
            _actual.append((a, b))
            return closed_minimum_cut(temporary_count, source, sink, query_arcs)

        with monkeypatch.context() as context:
            _swap_import(context, closed_minimum_cut, checked)
            result, stats = _unpack(parity_cut.minimum_parity_cut(problem))
        assert tuple(actual) == expected_pairs
        assert stats.mincut_calls == row["calls"] == count * count - 3 * count + 3
        assert _result_fields(result) == _expected_minimum(count, arcs, 3)
        # Empty arcs yield a zero incumbent immediately, but every pair must still execute.
        empty = Problem(n, classes, (), 3)
        observed = []

        def zeros(
            *args: object, _observed: list = observed, **kwargs: object,
        ) -> MinCutResult:
            values = _backend_args(args, kwargs)
            _observed.append(values[:3])
            return closed_minimum_cut(*values)

        with monkeypatch.context() as context:
            _swap_import(context, closed_minimum_cut, zeros)
            result, stats = _unpack(parity_cut.minimum_parity_cut(empty))
        assert _result_fields(result) == (0, 1)
        assert len(observed) == stats.mincut_calls == row["calls"]


def test_coordinate_trap_filters_only_after_temporary_to_problem_lifting() -> None:
    problem = _problem("P06")
    assert _least({shore: _cut(problem.arcs, shore) for shore in (1, 5)}, (1, 5)) == (2, 1)
    row = next(row for row in PAIR_TRACES if row["id"] == "P06-2-1")
    assert (row["least_temporary"], row["lifted_problem_shore"]) == (1, 5)
    assert (1 & problem.terminal_mask).bit_count() % 2 == 0
    assert (5 & problem.terminal_mask).bit_count() % 2 == 1
    result, stats = _unpack(parity_cut.minimum_parity_cut(problem))
    assert _result_fields(result) == (3, 5)
    assert stats.mincut_calls == 3
    assert parity_cut.lift_source_shore(problem, result.source_shore) == 1


def test_arbitrary_tied_minimizers_are_not_an_admissible_backend() -> None:
    problem = _problem("P12")
    assert problem.arcs == () and problem.terminal_mask == 60
    least_accepted = []
    for row in ARBITRARY_TIE_TRAP:
        a, b = row["pair"]
        allowed = tuple(shore for shore in _source_shores(problem.node_count)
                        if a in _members(shore) and b not in _members(shore))
        best, least = _least(dict.fromkeys(allowed, 0), allowed)
        assert (best, least) == (0, row["least_shore"])
        assert row["wrong_even_minimum"] in allowed
        assert _cut(problem.arcs, row["wrong_even_minimum"]) == best
        assert (row["wrong_even_minimum"] & 60).bit_count() % 2 == 0
        if (least & 60).bit_count() % 2:
            least_accepted.append(least)
    assert least_accepted and len(ARBITRARY_TIE_TRAP) == 21
    result, stats = _unpack(parity_cut.minimum_parity_cut(problem))
    assert _result_fields(result) == (0, least_accepted[0])
    assert stats.mincut_calls == 21
    # A controlled wrong ordinary result is rejected by the test-side least-shore check.
    with pytest.raises(AssertionError):
        _least_backend_result(4, (), MinCutResult(0, 13, FlowStats(0, 0, 0)))


def test_minimum_parity_cut(monkeypatch: pytest.MonkeyPatch) -> None:
    totals: Counter[str] = Counter()
    call_log = []
    observed_calls = 0

    def tracked(n: int, source: int, sink: int, arcs: tuple) -> MinCutResult:
        result = closed_minimum_cut(n, source, sink, arcs)
        call_log.append(result.stats)
        return result

    with monkeypatch.context() as context:
        _swap_import(context, closed_minimum_cut, tracked)
        for count in (2, 3, 4):
            n = max(1, count - 2)
            classes = (3, 4) if count == 2 else (
                1 << n, 1 << (n + 1), *(1 << v for v in range(n)),
            )
            positions = tuple((u, v) for u in range(count) for v in range(count) if u != v)
            shores = _source_shores(count)
            even_terminals = tuple(mask for mask in range(1 << count) if mask.bit_count() % 2 == 0)
            for capacities in product((0, 1), repeat=len(positions)):
                arcs = tuple((u, v, capacity) for (u, v), capacity
                             in zip(positions, capacities, strict=True))
                values = {shore: _cut(arcs, shore) for shore in shores}
                candidates = tuple(_least(values, tuple(shore for shore in shores
                                                       if a in _members(shore)
                                                       and b not in _members(shore)))
                                   for a, b in _pairs(count))
                totals["graphs"] += 1
                totals["distinct_graph_pair_minimizations"] += len(candidates)
                for terminal in even_terminals:
                    totals["terminal_problems"] += 1
                    totals["all_shore_evaluations"] += len(shores)
                    allowed = tuple(shore for shore in shores if (shore & terminal).bit_count() % 2)
                    problem = Problem(n, classes, arcs, terminal)
                    call_log.clear()
                    result, stats = _unpack(parity_cut.minimum_parity_cut(problem))
                    observed_calls += len(call_log)
                    aggregates = (len(call_log), sum(item.augmentations for item in call_log),
                                  sum(item.bfs_scans for item in call_log),
                                  max((item.peak_generated_value for item in call_log), default=0))
                    assert _stats_fields(stats) == aggregates
                    if not allowed:
                        assert result is None and aggregates == (0, 0, 0, 0)
                        totals["infeasible"] += 1
                        continue
                    totals["feasible"] += 1
                    totals["parity_admissible_shores"] += len(allowed)
                    optimum = min(values[shore] for shore in allowed)
                    optima = tuple(shore for shore in allowed if values[shore] == optimum)
                    expected = None
                    for value, shore in candidates:
                        if (shore & terminal).bit_count() % 2:
                            totals["candidate_parity_acceptances"] += 1
                            if expected is None or value < expected[0]:
                                expected = value, shore
                    assert expected is not None and expected[0] == optimum
                    assert _result_fields(result) == expected
                    assert result.source_shore in optima
                    assert values[result.source_shore] == result.cut_value
                    assert len(call_log) == len(candidates) == count * count - 3 * count + 3
                    totals["specified_backend_calls"] += len(candidates)
                    totals["zero_minima" if optimum == 0 else "positive_minima"] += 1
                    totals["multiple_optima"] += int(len(optima) > 1)
    assert dict(totals) == GRAPH_COUNTS
    assert observed_calls == GRAPH_COUNTS["specified_backend_calls"] == 201284


def test_diagnostic_anchors_and_flow_only_peak(monkeypatch: pytest.MonkeyPatch) -> None:
    for row in STATS_ANCHORS:
        observed = []

        def spy(
            *args: object, _observed: list = observed, **kwargs: object,
        ) -> MinCutResult:
            result = closed_minimum_cut(*args, **kwargs)
            _observed.append(result.stats)
            return result

        with monkeypatch.context() as context:
            _swap_import(context, closed_minimum_cut, spy)
            result, stats = _unpack(parity_cut.minimum_parity_cut(_problem(row["problem"])))
        expected = _row(MINIMUMS, row["problem"])
        assert _result_fields(result) == (None if expected["minimum"] is None else
                                          (expected["minimum"], expected["first_result"]))
        assert _stats_fields(stats) == (
            row["calls"], row["augmentations"], row["bfs_scans"], row["peak"],
        )
        actual_rows = tuple((item.augmentations, item.bfs_scans, item.peak_generated_value)
                            for item in observed)
        assert actual_rows == tuple(tuple(part[2:]) for part in row["trace"])
    # Source/preimage masks in P12 are nonzero, but its actual flow-only peak is zero.
    result, stats = _unpack(parity_cut.minimum_parity_cut(_problem("P12")))
    assert result.source_shore > 0 and stats.flow_peak_generated_value == 0


def test_diagnostics_cannot_select_a_different_tied_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    problem = _problem("P09")
    injected = []

    def diagnostics_only(*args: object, **kwargs: object) -> MinCutResult:
        actual = closed_minimum_cut(*args, **kwargs)
        ordinal = len(injected) + 1
        counters = FlowStats(ordinal, ordinal * 3, 1000 - ordinal)
        injected.append(counters)
        return MinCutResult(actual.value, actual.source_shore, counters)

    with monkeypatch.context() as context:
        _swap_import(context, closed_minimum_cut, diagnostics_only)
        result, stats = _unpack(parity_cut.minimum_parity_cut(problem))
    assert _result_fields(result) == (0, 5)
    assert _stats_fields(stats) == (7, 28, 84, 999)
    assert len(injected) == 7


def test_backend_exceptions_propagate_instead_of_becoming_infeasibility(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    problem = _problem("P06")
    error = RuntimeError("ordinary backend sentinel")

    def failing(*args: object, **kwargs: object) -> MinCutResult:
        raise error

    with monkeypatch.context() as context:
        _swap_import(context, closed_minimum_cut, failing)
        with pytest.raises(RuntimeError) as caught:
            parity_cut.minimum_parity_cut(problem)
        assert caught.value is error


def test_consumer_does_not_reconstruct_its_valid_problem(monkeypatch: pytest.MonkeyPatch) -> None:
    problem = _problem("P06")

    def forbidden(*args: object, **kwargs: object) -> object:
        raise AssertionError("normally constructed problem was validated or rebuilt again")

    with monkeypatch.context() as context:
        context.setattr(Problem, "__post_init__", forbidden)
        result, stats = _unpack(parity_cut.minimum_parity_cut(problem))
    assert _result_fields(result) == (3, 5)
    assert stats.mincut_calls == 3


def test_fixed_large_capacities_and_raw_positive_scaling() -> None:
    problem = _problem("P06")
    cases = 0
    for exponent in LARGE_EXPONENTS:
        factor = 1 << exponent
        scaled = Problem(problem.vertex_count, problem.classes,
                         tuple((a, b, c * factor) for a, b, c in problem.arcs), 6)
        result, stats = _unpack(parity_cut.minimum_parity_cut(scaled))
        assert _result_fields(result) == (3 * factor, 5)
        assert stats.mincut_calls == 3
        assert parity_cut.lift_source_shore(scaled, result.source_shore) == 1
        raw = ((2, 0, factor), (2, 0, factor + 1), (0, 1, factor),
               (0, 1, 0), (1, 3, factor + 2))
        network = SignRoutedNetwork(2, raw, factor + 7, -factor)
        reduced = parity_cut.reduce_atomic_family(network, AtomicFamily(3, 1, 1, 0))
        assert _problem_fields(reduced) == (2, (5, 8, 2),
                                            ((0, 2, factor), (2, 1, factor + 2)), 5)
        for shore in (1, 5):
            original = _lift((5, 8, 2), shore) & 3
            assert _cut(reduced.arcs, shore) == _cut(raw, original | 4)
        cases += 2
    assert cases == 8


def _source_residual(instance: dict, branch: int, parameter: tuple, shore: int) -> int:
    included = _members(shore)
    edges = instance["edges"]
    f_values = instance["f"]
    vertex_sum = sum(f_values[v] for v in included)
    degree_sum = sum(q * (int(u in included) + int(v in included)) for u, v, q in edges)
    boundary_sum = sum(q for u, v, q in edges if (u in included) != (v in included))
    costs = ((vertex_sum + boundary_sum - 1, degree_sum + 1 - vertex_sum),
             (vertex_sum + boundary_sum - 2, degree_sum - vertex_sum),
             (boundary_sum - degree_sum, vertex_sum - 1),
             (boundary_sum - degree_sum - 2, vertex_sum))
    cost, denominator = costs[branch]
    numerator, raw_denominator = parameter
    return raw_denominator * cost - numerator * denominator


def test_source_residual_family_seams_and_shift_ownership() -> None:
    constrained_strictly_worse = 0
    for row in BRANCH_SEAMS:
        data = _row(INSTANCES, row["instance"])
        instance = Instance(data["n"], _arcs(data["edges"]), tuple(data["f"]))
        family = AtomicFamily(*row["family"])
        coeff = branch_coefficients(instance, row["branch"], tuple(row["parameter"]))
        network = build_sign_routed_network(instance, coeff)
        assert coeff.gamma == tuple(row["gamma"])
        assert (network.negative_shift, network.constant) == (
            row["negative_shift"], row["constant"],
        )
        problem = parity_cut.reduce_atomic_family(network, family)
        assert _problem_fields(problem) == (data["n"], tuple(row["classes"]),
                                             _arcs(row["arcs"]), row["terminal_mask"])
        result, stats = _unpack(parity_cut.minimum_parity_cut(problem))
        assert _result_fields(result) == (row["minimum_cut"], row["reduced_choice"])
        assert stats.mincut_calls == row["calls"]
        original = parity_cut.lift_source_shore(problem, result.source_shore)
        assert original == row["original_choice"]
        allowed = _original_allowed(data["n"], tuple(row["family"]))
        expected = {mask: _source_residual(data, row["branch"], tuple(row["parameter"]), mask)
                    for mask in allowed}
        optimum = min(expected.values())
        assert recover_objective(network, result.cut_value) == expected[original] == optimum
        assert optimum == row["minimum_residual"]
        assert tuple(mask for mask, value in expected.items() if value == optimum) == tuple(
            row["original_optima"])
        unrestricted = min(_cut(network.arcs, mask | (1 << data["n"]))
                           for mask in range(1 << data["n"]))
        assert unrestricted == row["unrestricted_cut"]
        constrained_strictly_worse += int(row["minimum_cut"] > unrestricted)
        shifted = SignRoutedNetwork(network.vertex_count, network.arcs,
                                    network.negative_shift + 17, network.constant - 9)
        alternate = parity_cut.reduce_atomic_family(shifted, family)
        assert alternate == problem
        again, again_stats = _unpack(parity_cut.minimum_parity_cut(alternate))
        assert again == result and again_stats == stats
        assert recover_objective(shifted, again.cut_value) == optimum - 26
    assert len(BRANCH_SEAMS) == 24 and constrained_strictly_worse > 0


def test_original_labels_and_raw_arc_order_do_not_change_tied_choices() -> None:
    for data in INSTANCES:
        n = data["n"]
        instance = Instance(n, _arcs(data["edges"]), tuple(data["f"]))
        labeled = Instance(n, instance.edges, instance.f,
                           labels=tuple(f"label-{n - v}" for v in range(n)))
        for branch in range(4):
            network = build_sign_routed_network(
                instance, branch_coefficients(instance, branch, (-2, 1)),
            )
            label_network = build_sign_routed_network(
                labeled, branch_coefficients(labeled, branch, (-2, 1)),
            )
            assert network == label_network
            family = AtomicFamily(3, 1, 0, 0)
            permuted = SignRoutedNetwork(n, tuple(reversed(network.arcs)),
                                        network.negative_shift, network.constant)
            problem = parity_cut.reduce_atomic_family(network, family)
            assert parity_cut.reduce_atomic_family(permuted, family) == problem
            reference = _expected_minimum(problem.node_count, problem.arcs, problem.terminal_mask)
            first, first_stats = _unpack(parity_cut.minimum_parity_cut(problem))
            assert _result_fields(first) == reference
            for _ in range(2):
                result, stats = _unpack(parity_cut.minimum_parity_cut(problem))
                assert _result_fields(result) == reference and stats == first_stats


def _is_set_expression(node: ast.AST, known: set[str]) -> bool:
    if isinstance(node, (ast.Set, ast.SetComp)):
        return True
    if isinstance(node, ast.Name):
        return node.id in known
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in ("set", "frozenset"):
            return True
        if isinstance(node.func, ast.Attribute) and node.func.attr in (
            "union", "intersection", "difference", "symmetric_difference", "copy",
        ):
            return _is_set_expression(node.func.value, known)
    if isinstance(node, ast.BinOp) and isinstance(
        node.op, (ast.BitOr, ast.BitAnd, ast.BitXor, ast.Sub),
    ):
        return _is_set_expression(node.left, known) or _is_set_expression(node.right, known)
    return False


def _iterators(tree: ast.AST) -> Iterator[ast.AST]:
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            yield node.iter


def _source_violations(source: str) -> set[str]:
    tree = ast.parse(source)
    failures: set[str] = set()
    allowed = {"__future__": {"annotations"}, "dataclasses": {"dataclass"},
               "families": {"AtomicFamily"}, "sign_routing": {"SignRoutedNetwork"},
               "shore": {"validate_shore"}, "flow": {"minimum_cut", "MinCutResult", "FlowStats"}}
    known_sets: set[str] = set()
    assignments = [node for node in ast.walk(tree) if isinstance(node, (ast.Assign, ast.AnnAssign))]
    changed = True
    while changed:
        changed = False
        for node in assignments:
            if node.value is not None and _is_set_expression(node.value, known_sets):
                targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
                for target in targets:
                    if isinstance(target, ast.Name) and target.id not in known_sets:
                        known_sets.add(target.id)
                        changed = True
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    graph = {name: {child.func.id for child in ast.walk(node)
                    if isinstance(child, ast.Call) and isinstance(child.func, ast.Name)
                    and child.func.id in functions}
             for name, node in functions.items()}
    for start in graph:
        pending = list(graph[start])
        visited: set[str] = set()
        while pending:
            child = pending.pop()
            if child == start:
                failures.add("recursion")
            if child not in visited:
                visited.add(child)
                pending.extend(graph[child])
    for iterator in _iterators(tree):
        probe = iterator
        if isinstance(probe, ast.Call) and isinstance(probe.func, ast.Name) and probe.func.id in (
            "iter", "enumerate", "reversed",
        ) and probe.args:
            probe = probe.args[0]
        if _is_set_expression(probe, known_sets):
            failures.add("set iteration")
    forbidden = {"float", "Fraction", "gcd", "isclose", "epsilon", "eps", "tolerance",
                 "big_m", "infinity", "random", "eval", "exec", "open", "__import__"}
    magnitude = {"capacity", "capacities", "q", "Q", "weight", "weights", "cut_value",
                 "negative_shift", "constant", "peak_generated_value"}
    range_taints: dict[str, set[str]] = {name: {"magnitude range"} for name in magnitude}

    def taints(node: ast.AST) -> set[str]:
        found: set[str] = set()
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "len":
            return found
        if isinstance(node, ast.Name):
            found.update(range_taints.get(node.id, set()))
        if isinstance(node, ast.Attribute) and node.attr in magnitude:
            found.add("magnitude range")
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.LShift, ast.Pow)):
            found.add("subset range")
        for child in ast.iter_child_nodes(node):
            found.update(taints(child))
        return found

    changed = True
    while changed:
        changed = False
        for assignment in assignments:
            if assignment.value is None:
                continue
            labels = taints(assignment.value)
            targets = (assignment.targets if isinstance(assignment, ast.Assign)
                       else (assignment.target,))
            for target in targets:
                if isinstance(target, ast.Name):
                    previous = range_taints.setdefault(target.id, set())
                    if not labels <= previous:
                        previous.update(labels)
                        changed = True
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            failures.add("import")
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.startswith("exactfrac."):
                module = module.removeprefix("exactfrac.")
            if module not in allowed or any(
                alias.name not in allowed[module] for alias in node.names
            ):
                failures.add("import")
            if node.level > 1:
                failures.add("import")
        if isinstance(node, ast.Constant) and type(node.value) is float:
            failures.add("float literal")
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.FloorDiv)):
            failures.add("division")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Invert):
            failures.add("bare complement")
        if isinstance(node, ast.Name) and node.id in forbidden:
            failures.add("prohibited arithmetic or dynamic access")
        if isinstance(node, ast.Attribute) and node.attr in forbidden:
            failures.add("prohibited arithmetic or dynamic access")
        if (
            isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "range"
        ):
            for arg in node.args:
                failures.update(taints(arg))
    return failures


def test_source_exactness_dependencies_and_finite_work_guards() -> None:
    source = inspect.getsource(parity_cut)
    assert _source_violations(source) == set()
    tree = ast.parse(source)
    attributes = [node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)]
    assert "is_nonempty" in attributes
    assert any(value is closed_validate_shore for value in vars(parity_cut).values())
    assert any(value is closed_minimum_cut for value in vars(parity_cut).values())
    # An explicit source audit is still needed for asymptotic workspace and indirect aliases.
    # These tests do not purport to prove a semantic complexity theorem from an AST.
    root = Path(__file__).resolve().parents[1]
    for package in ("exactfrac", "exactfrac_verify"):
        assert (root / package / "__init__.py").read_bytes() == b""


def test_source_guard_negative_controls_cover_previous_unit_gaps() -> None:
    bad = (
        "x = 0.0", "x = float(1)", "from fractions import Fraction",
        "x = a / b", "x = a // b", "from math import gcd", "x = ~mask",
        "for x in {v for v in items}:\n    pass", "for x in {1, 2}:\n    pass",
        "s = {1, 2}\nt = s\nfor x in t:\n    pass",
        "s = set()\nfor x in enumerate(s):\n    pass",
        "for x in range(capacity):\n    pass", "for x in range(1 << N):\n    pass",
        "for x in range(2 ** N):\n    pass", "import exactfrac_verify.brute",
        "from exactfrac.oracle import foo", "def f():\n    return g()\ndef g():\n    return f()",
        "x = eval('1')", "x = epsilon * q",
        "bound = capacity\nlimit = bound\nfor x in range(limit):\n    pass",
        "bound = 1 << N\nlimit = bound\nfor x in range(limit):\n    pass",
        "s = {1}\nt = s.copy()\nfor x in t:\n    pass",
    )
    for snippet in bad:
        assert _source_violations(snippet), snippet
    good = "s = {1, 2}\nfor x in sorted(s):\n    pass"
    assert _source_violations(good) == set()
    assert len(bad) == 22


def test_fresh_process_import_isolation() -> None:
    root = Path(__file__).resolve().parents[1]
    script = '''import importlib, json, pathlib, sys
root = pathlib.Path.cwd().resolve()
module = importlib.import_module("exactfrac.parity_cut")
modules = {}
for name, value in sorted(sys.modules.items()):
    if name.split(".")[0] not in ("exactfrac", "exactfrac_verify"):
        continue
    path = pathlib.Path(value.__file__).resolve()
    if not path.is_relative_to(root):
        raise RuntimeError("nonlocal project import: " + name)
    modules[name] = path.relative_to(root).as_posix()
print(json.dumps(modules, sort_keys=True))
'''
    environment = dict(os.environ)
    for key in ("PYTHONHOME", "PYTHONSTARTUP", "PYTEST_ADDOPTS", "PYTEST_PLUGINS"):
        environment.pop(key, None)
    environment.update({"PYTHONPATH": str(root), "PYTHONDONTWRITEBYTECODE": "1",
                        "PYTHONNOUSERSITE": "1"})
    completed = subprocess.run([sys.executable, "-c", script], cwd=root, env=environment,
                               capture_output=True, text=True, check=False)
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout)
    allowed = {"exactfrac", "exactfrac.parity_cut", "exactfrac.families", "exactfrac.flow",
               "exactfrac.shore", "exactfrac.instance", "exactfrac.sign_routing",
               "exactfrac.rational"}
    assert set(observed) <= allowed
    assert observed["exactfrac.parity_cut"] == "exactfrac/parity_cut.py"
    assert "exactfrac_verify" not in observed
