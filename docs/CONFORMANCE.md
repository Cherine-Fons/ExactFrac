# CONFORMANCE — theorem obligations discharged by tests

Governing source: see SPEC_LOCK.md. One row per obligation; the label is copied from
the governing source's \label{} set. A row is added when its unit lands; a unit is not
done until its row exists and its test is green.

| Obligation (governing source label) | What it promises | Discharging test | Status |
|---|---|---|---|
| prop:expanded-equivalence | compact objective equals the expanded-copy objective | tests/test_verify_brute.py::test_compact_expanded_agree | green |
| lem:empty | Q = 1 single edge, f ≡ 1 → ((0,1), Empty) | tests/test_verify_brute.py::test_oracle_001_brute_owned_empty_state | green |
| lem:unit | constructive unit witness is admissible with ratio ≥ 1 | tests/test_verify_brute.py::test_oracle_002_witness_is_admissible_and_preserves_raw_value | green |
| def:instance | finite nonempty loopless compact support; positive integer multiplicities and f; exact n, m, Q, and d_q data | tests/test_instance.py::test_oracle_013_canonical_active_instance_and_exact_derived_data; tests/test_instance.py::test_canonical_constructor_rejects_exact_oracle_016_cases | green |
| lem:aggregation | repeated unordered raw records are oriented, grouped, and summed exactly into one canonical support edge without explicit-copy expansion | tests/test_instance.py::test_oracle_014_raw_forms_normalize_to_oracle_013; tests/test_instance.py::test_every_permutation_of_raw_a_has_the_same_canonical_result; tests/test_instance.py::test_reversed_and_repeated_raw_pairs_aggregate_by_exact_addition; tests/test_instance.py::test_enormous_multiplicity_remains_one_compact_support_record | green |
| prop:domain-decomp | atomic families cover each branch domain | tests/test_families.py::test_cover | planned |
| lem:ek | zero-arc totalization; exact minimum and inclusionwise-minimal source shore; O(NE) augmentations and uniform O(N+NE^2) operations | tests/test_flow.py (TEST_PLAN FL1-FL12) | green |
| prop:branch-invariant | invariant holds after every branch iteration | tests/test_branch.py::test_invariant | planned |
| prop:standard-correct | standard loop terminates with the exact branch optimum | tests/test_branch.py::test_standard | planned |
| prop:branch-correct | accelerated loop terminates with the exact branch optimum | tests/test_branch.py::test_accelerated | planned |
| prop:global-invariant | global invariant holds across branches and the H2 scan | tests/test_global.py::test_invariant | planned |
| thm:main | value equals the brute-force optimum on every catalog instance | tests/test_global.py::test_catalog | planned |

## Stage-1 verifier seam notes

- The `lem:empty` row above discharges the definition-level ORACLE-001 empty-family
  behavior owned by the independent brute verifier: exact value `(0,1)` with no
  manufactured witness. Production input construction and the
  malformed-vs-`UnsupportedInstance` distinction are now discharged separately by the
  `def:instance` row and `tests/test_instance.py`; this does not enlarge the
  `lem:empty` claim.
- B9 multiple-global-maximizer coverage is an engineering verification obligation rather
  than a separate governing-source theorem-label row. Its independently hand-derived source fixture is
  ORACLE-004, committed before the consuming test in commit `083949f`; its green test is
  `tests/test_verify_brute.py::test_oracle_004_global_tie_and_deterministic_first_witness`.
- The `prop:expanded-equivalence` row records executable conformance/regression evidence
  on the currently committed tiny oracle catalog. The universal compact-to-expanded
  equivalence is a mathematical theorem supplied by the governing source; finite testing
  does not prove that proposition. Broader exhaustive tiny-domain cross-validation may
  strengthen empirical coverage later without changing the theorem's status.

## Graph-instance implementation notes

- The `def:instance` row records executable evidence for the production representation of
  finite nonempty loopless compact support with positive integer multiplicities and `f`,
  together with exact canonical and derived data. The active-regime behavior under
  `ass:active` is exercised by
  `tests/test_instance.py::test_oracle_017_structurally_valid_active_failures_are_exact_unsupported`
  and
  `tests/test_instance.py::test_oracle_017_malformed_validation_precedes_active_check`; no
  separate theorem-discharge row is created for an assumption.
- The `lem:aggregation` row records deterministic endpoint orientation, grouping, exact
  multiplicity summation, canonical order, and compact non-expansion in the production
  preprocessor. The governing lemma supplies the universal preservation of `e_q(U)`,
  `b_q(U)`, `d_q(v)`, compact admissible totals, and objective value; finite tests provide
  executable implementation evidence rather than a proof of the lemma.
- TEST_PLAN R3, R4, D1, and verifier isolation are cross-cutting engineering obligations,
  not separate governing-source theorem labels. Their green tests are
  `tests/test_instance.py::test_instance_correctness_path_contains_no_fraction_float_or_true_division`,
  `tests/test_instance.py::test_instance_source_does_not_derive_algorithmic_order_from_set_iteration`,
  and `tests/test_instance.py::test_instance_source_and_fresh_import_are_verifier_isolated`.

## Shore-representation implementation note

- Shore representation is an engineering/data-representation seam rather than a separately
  labeled governing-source theorem. No new theorem-label row is created solely for this
  unit. `tests/test_shore.py` supplies executable evidence for TEST_PLAN S1--S12.
- Historical S1--S3 document the semantics of validated integer masks. S4--S12 exercise the
  actual `exactfrac.shore` validation, strict sorted-list serialization, universe-relative
  complement, exact plain-`ValueError` boundary, public surface, compact large-universe
  behavior, and graph-independent responsibility boundary.
- TEST_PLAN R3, R4, D1, and import isolation remain cross-cutting engineering obligations,
  not separate theorem rows. Their direct checks are
  `tests/test_shore.py::test_oracle_022_correctness_path_contains_no_fraction_float_or_true_division`,
  `tests/test_shore.py::test_oracle_022_source_does_not_derive_order_from_set_iteration`,
  and `tests/test_shore.py::test_oracle_022_fresh_process_import_isolation`.
- The separate handoff audit supplies reproducible implementation evidence over 510 valid
  masks, 87,380 ordered mask pairs, and 20,000 random large-universe cases. This finite
  audit does not prove a universal theorem and is not a production solver dependency.

## V2.2 authority-activation note

- V2.2 changes only the zero-arc totalization and zero-safe complexity carrier attached to
  `thm:GR`, `lem:ek`, and the proof of `thm:branch-oracle`. The four algorithm
  environments, `thm:main`, both invariants, domains, endpoint formulas, exact-arithmetic
  policy, argmin policy, and output contract remain unchanged.
- This authority activation does not promote `lem:ek` to `green`. No flow-specific oracle,
  `tests/test_flow.py`, or `exactfrac/flow.py` exists at activation time.
- The prospective flow obligations are recorded in TEST_PLAN FL1–FL12. The `lem:ek` row
  becomes green only when the later atomic flow code/test/conformance unit lands and the
  complete flow gate passes.
