# CONFORMANCE — theorem obligations discharged by tests

Governing source: see SPEC_LOCK.md. One row per obligation; the label is copied from
V2.1's \label{} set. A row is added when its unit lands; a unit is not done until its
row exists and its test is green.

| Obligation (V2.1 label) | What it promises | Discharging test | Status |
|---|---|---|---|
| prop:expanded-equivalence | compact objective equals the expanded-copy objective | tests/test_verify_brute.py::test_compact_expanded_agree | green |
| lem:empty | Q = 1 single edge, f ≡ 1 → ((0,1), Empty) | tests/test_verify_brute.py::test_oracle_001_brute_owned_empty_state | green |
| lem:unit | constructive unit witness is admissible with ratio ≥ 1 | tests/test_verify_brute.py::test_oracle_002_witness_is_admissible_and_preserves_raw_value | green |
| prop:domain-decomp | atomic families cover each branch domain | tests/test_families.py::test_cover | planned |
| lem:ek | reference max-flow: O(NE) augmentations, min cut recovered | tests/test_flow.py | planned |
| prop:branch-invariant | invariant holds after every branch iteration | tests/test_branch.py::test_invariant | planned |
| prop:standard-correct | standard loop terminates with the exact branch optimum | tests/test_branch.py::test_standard | planned |
| prop:branch-correct | accelerated loop terminates with the exact branch optimum | tests/test_branch.py::test_accelerated | planned |
| prop:global-invariant | global invariant holds across branches and the H2 scan | tests/test_global.py::test_invariant | planned |
| thm:main | value equals the brute-force optimum on every catalog instance | tests/test_global.py::test_catalog | planned |

## Stage-1 verifier seam notes

- The `lem:empty` row above discharges the definition-level ORACLE-001 empty-family
  behavior owned by the independent brute verifier: exact value `(0,1)` with no
  manufactured witness. Production input construction and the
  malformed-vs-`UnsupportedInstance` distinction remain deferred to the
  `exactfrac.instance` unit under TEST_PLAN E1/I8.
- B9 multiple-global-maximizer coverage is an engineering verification obligation rather
  than a separate V2.1 theorem-label row. Its independently hand-derived source fixture is
  ORACLE-004, committed before the consuming test in commit `083949f`; its green test is
  `tests/test_verify_brute.py::test_oracle_004_global_tie_and_deterministic_first_witness`.
- The `prop:expanded-equivalence` row records executable conformance/regression evidence
  on the currently committed tiny oracle catalog. The universal compact-to-expanded
  equivalence is a mathematical theorem supplied by the governing source; finite testing
  does not prove that proposition. Broader exhaustive tiny-domain cross-validation may
  strengthen empirical coverage later without changing the theorem's status.
