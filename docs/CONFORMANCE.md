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
| prop:domain-decomp | each generated atomic-family union equals its literal `prop:branch-transform` domain; overlap is allowed and no partition claim is made | tests/test_families.py::test_cover; tests/test_families.py::test_oracle_026_rich_cover_multiplicities_preserve_overlap | green |
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

## Atomic-family implementation notes

- The `prop:domain-decomp` row records executable conformance for the production
  atomic-family decomposition. `tests/test_families.py::test_cover` enumerates nonempty
  shores through the independent brute-verifier layer, computes the fixed-shore quantities
  `s`, `e`, `b`, and `d = 2e + b` directly, applies the four literal
  `prop:branch-transform` domain conditions, and requires exact branch-by-branch set
  equality with the unions of the generated descriptors.
- The comparator does not reconstruct a source domain from `T_+`, `T_f`, `P`, `A`, `W`,
  an atomic-family union, or the production family-membership predicate. The family-union
  side evaluates every valid shore mask including `0`; mask `0` is excluded by the
  descriptors themselves rather than by an external nonempty-shore prefilter.
- Equality is a cover statement, not a partition statement.
  `tests/test_families.py::test_oracle_026_rich_cover_multiplicities_preserve_overlap`
  verifies that one shore may satisfy several descriptor positions while the union still
  equals the literal branch domain.
- TEST_PLAN F5--F12 additionally exercise the exact public surface, frozen and slotted
  descriptor state, the derived nonemptiness predicate, deterministic D0--D3 order, exact
  descriptor counts, retained empty and duplicate descriptors, exact plain-`ValueError`
  rejection, label independence, classification-controlled magnitude independence,
  source exactness, and verifier isolation. These are cross-cutting engineering
  obligations rather than additional governing-source theorem rows.
- The separate handoff audit checks all 9,360 small-universe descriptor states, the exact
  2,328 / 7,032 nonempty/empty split, 881 independently generated active instances, and
  16,010 literal branch-domain membership decisions. This finite executable evidence does
  not replace the universal proof of `prop:domain-decomp` in the governing source.

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

## Unit 08 witness/value representation implementation note

- This is an engineering/data-representation seam under DESIGN sections 4.4 and 4.4A
  and TEST_PLAN sections 21--22. It adds no governing-source theorem label and changes
  no existing theorem row or status, including the verifier-owned `lem:empty` row.
- `exactfrac.witness` supplies immutable `Witness(U, y)` and raw `ExactValue(N, D)`
  records, exact graph-shore sums, strict boundary-selection conversions, full
  instance-aware admissibility validation, and witness-derived raw value evaluation.
  Structural record equality/hash is not numerical quotient comparison; no reduction
  or normalization of `(N, D)` occurs. Constructor success is not instance validity.
- Generic sums and conversions accept finite-universe mask `0`; a Witness requires a
  nonempty shore. Successful dense/sparse conversion establishes only a legal boundary
  selection, not full admissibility or attainment. The full validator additionally
  requires odd `f(U) + Y(y)` and total at least 3; the evaluator returns the literal
  `N = 2*(e_q(U) + Y(y))`, `D = f(U) + Y(y) - 1` after full validation.
  The admissible zero-valued witness with raw `(0,2)` remains distinct from Empty;
  neither numerator zero, sparse `[]`, nor a standalone value record certifies emptiness.
- The 33 tests in `tests/test_witness.py` cover W8--W20 and the mapped production
  portions of W1--W7. The following groups identify the principal executable evidence;
  they are engineering mappings, not extra theorem-discharge rows.

| Production obligation | Principal tests in `tests/test_witness.py` |
|---|---|
| W8--W10: exact surface, immutable records, structural/raw identity | `test_public_surface_signatures_and_type_hints`; `test_package_root_remains_export_free`; `test_record_immutability_slots_and_structural_witness_equality`; `test_exact_value_structural_equality_hash_and_no_ordering`; `test_exact_value_test_side_numerical_controls` |
| W11: four independent graph-shore sums and degree identity | `test_mixed_graph_shore_sums_all_masks`; `test_degree_identity_all_mixed_masks`; `test_tiny_corpus_sums_and_conversion_outputs` |
| W12--W13: literal dense/sparse outputs, round trips, detachment, strict rejection | `test_dense_to_sparse_literal_rows`; `test_sparse_to_dense_literal_rows_and_round_trips`; `test_conversion_detachment_and_failure_nonmutation`; `test_dense_rejection_matrix`; `test_sparse_rejection_matrix` |
| W14--W16: full admissibility, literal raw attainment, zero versus Empty | `test_conversion_is_not_full_admissibility`; `test_validate_witness_accepts_catalogued_rows`; `test_witness_value_returns_literal_unreduced_rows`; `test_admissibility_guard_isolation`; `test_zero_valued_witness_is_not_empty` |
| W17: exact types, ValueError boundary, instance-aware rejection | `test_witness_constructor_exact_rejections`; `test_exact_value_constructor_exact_rejections`; `test_instance_keyed_functions_require_exact_instance_first`; `test_bare_shore_masks_are_exact_and_finite_universe_bounded`; `test_validator_and_evaluator_require_exact_witness_type`; `test_validator_and_evaluator_reject_graph_invalid_shape_valid_witnesses` |
| W18--W19: static exactness, isolation, compact work, labels, large integers | `test_source_exactness_import_boundary_and_no_numeric_shortcuts`; `test_source_does_not_iterate_over_unordered_sets_or_numeric_magnitudes`; `test_fresh_process_import_isolation`; `test_labels_do_not_change_sums_conversions_or_values`; `test_large_integer_exactness_and_literal_preservation` |
| W20: independent finite-corpus acceptance, raw values, conversion, copy projection | `test_tiny_corpus_independent_counts`; `test_tiny_corpus_production_acceptance_and_raw_values`; `test_tiny_corpus_sums_and_conversion_outputs`; `test_tiny_expanded_copy_projection_matches_compact_counts` |

- The separate handoff definition-level audit imports no production test module and
  obtains expected admissibility, sums, and raw values independently of production
  witness helpers. It checks the actual production candidate on 329 active instances:
  2,612 valid masks, including 2,283 nonempty masks; 12,926 generic boundary selections,
  including 12,597 on nonempty shores; 5,917 admissible witnesses, 6,311 parity rejections,
  369 odd lower-bound rejections, and 249 zero-valued admissible witnesses. It also
  probes validation-phase order, conversion contracts, source/import isolation, and
  candidate/frozen-test nonmutation. The recorded live gate reports 33 targeted tests,
  388 full repository tests, Ruff, and that definition-level audit passing.
- These are finite executable checks, not a universal proof, a timing guarantee, a new
  global-optimality result, or an independent certificate checker. ORACLE-002 remains
  local; ORACLE-004 retains its existing global-tie classification without enlarging
  this unit's claim.
- Historical W1--W7 remain unchanged. W5--W6's representation conversions and W7's raw
  evaluation receive production evidence here; the complete certificate envelope,
  certificate round trip, and W7's serialized raw-pair identity remain later obligations.
  Unit 09 numerical comparison/arithmetic, solver witness reconstruction, full certificate
  assembly/JSON I/O, independent `exactfrac_verify.check`, result-level Empty certification,
  and global optimality verification are not declared complete. The later checker must
  reimplement its checks independently and must not import the production validator.
