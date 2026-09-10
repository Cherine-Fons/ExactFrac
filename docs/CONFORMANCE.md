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
| lem:sign-routing | on production Instance inputs, the uncontracted nonnegative cut representation satisfies cut_capacity(X_U) = a*b_q(U) + sum_U gamma + C_minus; no minimization claim | tests/test_sign_routing.py::test_sign_routing_identity | green |
| lem:parity-anchor | on supported SignRoutedNetwork/AtomicFamily inputs, forced contraction and parity anchoring give a cut-value-preserving bijection between family shores and odd reduced source/sink shores | tests/test_parity_cut.py::test_parity_anchor_correspondence | green |
| thm:GR | exact minimum odd-terminal source/sink cut on validated nonnegative directed ParityCutProblem inputs using closed least ordinary cuts; deterministic first retained GR candidate | tests/test_parity_cut.py::test_minimum_parity_cut | green |
| thm:branch-oracle | fixed-parameter exact minimum of B*c_j(U)-A*h_j(U) over the complete original D_j, or infeasible; prepared-cover specialization and work/number-size scope explained below | tests/test_oracle.py::test_exact_branch_min | green |
| prop:branch-invariant | invariant holds after every branch iteration | tests/test_branch.py::test_invariant | planned |
| prop:standard-correct | standard loop terminates with the exact branch optimum | tests/test_branch.py::test_standard | green |
| lem:standard-bits | literal Standard initialization and fresh candidate-ratio resets; source-bound polynomial encoding argument with finite carrier checks, not complete peak telemetry | tests/test_branch.py::test_symbolic_large_families_and_all_112_actual_branch_solves; tests/test_branch.py::test_literal_reset_carriers_and_integer_wyz_change_of_variables; tests/test_branch.py::test_production_source_exact_imports_arithmetic_and_no_graph_rescan | green |
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

## Unit 09 raw rational-pair implementation note

- This is an engineering arithmetic seam under DESIGN sections 4.5--4.5A and TEST_PLAN
  sections 23--24, with source-derived fixtures ORACLE-038--045. It adds no theorem label
  and changes no existing theorem row or status. The historical Unit 08 note's deferred
  numerical comparison/arithmetic now has the Unit 09 evidence below; its other deferred
  responsibilities remain outside this unit.
- `exactfrac.rational` owns the untagged `RawPair = tuple[int, int]` carrier and seven
  scalar operations. `make_pair` preserves exact integer inputs literally and rejects
  nonpositive denominators; every consumer validates exact tuple shape, exact built-in
  integer fields, and denominator positivity before arithmetic. No sign repair, coercion,
  gcd reduction, or normalization of zero to `(0,1)` occurs. An otherwise valid tuple's
  semantic provenance remains a caller responsibility, not a runtime type guarantee.
- `compare_pairs` uses cross products; `pair_sign` validates the complete pair before
  returning its numerator's sign. Both return exact built-in integers in {-1, 0, 1}.
  Literal updates are `(A+B,B)` and `(2*A*D-C*B,B*D)`, with reflection arguments ordered
  as newton then current. Raw common factors and cancellation denominators are retained.
- `residual_numerator((A,B),c,h)` returns the exact integer `B*c-A*h`; scalar c and h may
  be signed or zero. This is not residual minimization or a proof of branch feasibility.
  A branch caller must establish h_j(U) > 0 when using it as a denominator. Raw residuals
  are compared directly only at the same parameter pair; different encodings can scale
  their numerators, so cross-denominator ordering requires explicit rational comparison.
- Unit 08 `ExactValue` records retain their structural equality/hash and raw fields.
  Callers explicitly extract `(N,D)`; no implicit adapter or witness-layer dependency is
  added. Numerical equality, a zero sign, or construction of a value record establishes
  neither Empty, witness admissibility, raw attainment, nor global optimality.
- The frozen 22 tests in `tests/test_rational.py` provide the following principal RP1--RP12
  evidence. These mappings are engineering coverage, not additional theorem-discharge rows.

| Production obligation | Principal tests in `tests/test_rational.py` |
|---|---|
| RP1: scalar surface, signatures, deliberate untagged carrier | `test_rp1_public_surface_alias_and_signatures`; `test_rp1_untagged_tuple_carrier_is_deliberate` |
| RP2--RP3: strict construction, exact types/errors, validation before arithmetic | `test_rp2_make_pair_literal_outputs_and_strict_denominators`; `test_rp2_make_pair_exact_scalar_types_and_validation_order`; `test_rp3_validate_pair_success_and_rejection_matrix`; `test_rp3_residual_scalar_exact_types` |
| RP4--RP5: numerical comparison, scaling, exact sign, complete validation | `test_rp4_comparison_oracle_and_exact_output_type`; `test_rp4_comparison_scale_invariance_and_huge_close_values`; `test_rp5_pair_sign_oracle_and_complete_validation` |
| RP6: literal add-one and denominator preservation | `test_rp6_pair_add_one_literal_oracle`; `test_rp6_pair_add_one_large_cancellation_preserves_denominator` |
| RP7: literal reflection, fixed argument roles, bounded-newton recurrence | `test_rp7_pair_reflect_literal_oracle_and_roles`; `test_rp7_fixed_newton_recurrence_preserves_raw_growth`; `test_rp7_large_symbolic_reflection` |
| RP8: scalar residual, encoding scale, cross-denominator hazard | `test_rp8_residual_oracle_sign_and_scaling_hazard`; `test_rp8_large_symbolic_residual` |
| RP9: explicit ExactValue bridge; closed Unit 08 semantics | `test_rp9_explicit_exactvalue_bridge_preserves_unit08_semantics` |
| RP10: independently expected bounded arithmetic corpus | `test_rp10_finite_independent_arithmetic_corpus` |
| RP11--RP12: source exactness, import isolation, bounded work, large raw values | `test_rp11_source_exactness_and_dependency_isolation`; `test_rp11_no_recursion_dynamic_range_or_set_iteration`; `test_rp11_fresh_process_import_isolation_and_package_root`; `test_rp12_large_integer_outputs_remain_exact_raw_pairs` |

- The separate handoff arithmetic audit does not import the production test module and
  uses independent Fraction comparisons and separately justified literal raw formulas.
  It checks 2,401 bounded core evaluations, 320 supplementary exact-ValueError/hostile-object
  calls, 6,272 scaled comparisons, and 21,952 transitivity triples. It also checks signatures,
  validation-phase order, large integers, raw cancellation, fixed-newton recurrence,
  residual scaling, and fresh-process import isolation. Ten in-memory prohibited-source
  controls are rejected without modifying production files.
- Before this documentation note, the live gate bound unchanged implementation R1, frozen
  test R2, and all 26 prior base files to 22 targeted tests, 410 full repository tests,
  full repository Ruff, and the independent arithmetic audit passing. This append-only
  note deliberately changes CONFORMANCE alone; it does not rewrite those earlier records
  or assert that their pre-note base-file manifest describes the post-note repository.
- Source inspection of this candidate finds no loops or recursive call cycles and only
  the permitted optional future-annotations import. The primitive work is a bounded
  number of integer operations and objects, not constant bit time or constant byte memory.
  The literal reflection recurrence is tested with bounded/fixed newton operands; no
  bound for arbitrary compositions with two growing operands is inferred.
- Historical arithmetic R1--R5 are unchanged. In particular, algorithm-level R5 telemetry
  and Standard/Accelerated bit-growth experiments remain deferred. No lem:standard-bits,
  lem:bitgrowth, branch, or global theorem row is promoted. These finite checks are not
  universal proofs, timing guarantees, or branch-termination certificates.
- Unit 10 sign routing, branch coefficients/residual minimization, actual branch
  initialization/reset/acceptance and tie handling, global solve, certificate assembly,
  serialization, independent certificate checking, and telemetry remain downstream.
  The complete three-file staged tree still requires isolated verification and atomic
  commit/remote closure under TEST_PLAN section 24 before Unit 09 is closed.

## Unit 10 branch-coefficient and sign-routing implementation note

- The new `lem:sign-routing` row is the narrow operational-domain cut-identity row
  authorized by DESIGN 4.7.14 and TEST_PLAN SR16/section 26. It records executable
  evidence for canonical active `Instance` inputs, generic `a >= 0`, and signed gamma.
  It does not extend this API to the lemma's broader graph domain. The governing source
  supplies the universal proof; finite tests do not prove the lemma or certify a minimum.
  Every earlier theorem row and status is preserved unchanged.
- `exactfrac.sign_routing` owns the two frozen/slotted structural records and the functions
  `branch_coefficients`, `build_sign_routed_network`, and `recover_objective`. Constructor
  validity establishes representation, not provenance from a graph or branch. Exact
  built-in types and plain ValueError guard the ruled boundaries; raw tuple order, repeated
  arc records, zero capacities, and signed constants are not normalized or silently repaired.
- The single branch coefficient table is tested against source c_j/h_j expressions with
  s, b, and d independently recomputed from original input records. It obtains d_q once,
  then scans vertices in increasing order. For parameter (A,B), B > 0, the identity is
  `B*c_j(U)-A*h_j(U) = a*b_q(U)+sum_U gamma+constant`. Empty and full masks are included;
  outside D_j this is a polynomial-extension identity, not feasibility or h_j(U) > 0.
- Every support edge and every spoke has two opposite ORIGINAL directed capacity arcs.
  Support pairs follow edge_ref order; spoke pairs follow increasing vertex order.
  Zero gamma retains its two sink spokes; a == 0 retains both zero support arcs. The
  uncontracted builder emits exactly `2*(m+n)` arcs with source=n, sink=n+1, node_count=n+2.
  A directed cut counts only tail-inside/head-outside, not both directions or residual arcs.
- The generic cut identity is `cut_capacity(X_U) = a*b_q(U)+sum_U gamma+C_minus`.
  The nonnegative `negative_shift=C_minus` and signed `constant` stay separate; recovery is
  `cut_value-negative_shift+constant`. A constant-only change does not alter arcs or shift.
  The scalar helper neither validates cut provenance nor chooses a shore or minimum.
  Minimum correspondence requires the SAME nonempty permitted family; the registered
  counterexample rejects substitution of an unrestricted cut for a constrained minimum.
- The frozen R2 test file provides the following 29 principal checks against ORACLE-046--055.
  Except for the explicitly scoped lemma row above, this mapping is engineering evidence.
  Expected literals are transcribed from the committed human-readable catalogue, with
  definition-derived comparison routines; the consuming tests do not read private JSON.

| Production obligation | Principal tests in `tests/test_sign_routing.py` |
|---|---|
| SR1--SR3: exact surface, structural records, raw preservation, terminal properties | `test_public_surface_signatures_and_exact_annotations`; `test_coefficient_record_raw_shape_and_structural_identity`; `test_network_record_preserves_order_repetitions_zeros_and_empty_shape`; `test_record_immutability_no_ordering_or_extra_stored_fields`; `test_keyword_calls_and_wrong_arity_boundary` |
| SR4/SR7/SR13: literal branch coefficients and independent all-shore residual expansion | `test_literal_four_branch_coefficient_rows_and_anchor_shores`; `test_branch_coefficient_identity` |
| SR5--SR6/SR8/SR13: exact original arcs, cut identity, zeros and fixed dimensions | `test_literal_original_arc_tuples_and_all_shore_cut_tables`; `test_sign_routing_identity`; `test_zero_support_zero_spokes_and_all_zero_network_are_not_empty` |
| SR9: separate recovery signs, restricted-family boundary, constant-work scalar helper | `test_scalar_recovery_separate_signs_without_cut_or_provenance_claim`; `test_restricted_family_minimum_is_not_the_unrestricted_minimum`; `test_recovery_does_not_rescan_arcs_or_certify_network` |
| SR10/SR12: zero/negative parameters, active equality, constants, labels and repeatability | `test_zero_negative_parameters_active_equality_and_distinct_constants`; `test_constant_only_variants_preserve_literal_arcs_and_negative_shift`; `test_labels_and_repetition_never_change_raw_results_or_input_records` |
| SR11/SR15: exact errors, hostile objects, validation before graph work, once-only degree access | `test_declared_exact_valueerror_matrix`; `test_supplementary_wrong_scalar_types_at_each_numeric_boundary`; `test_validation_precedes_graph_dependent_work`; `test_closed_pair_validation_occurs_before_degree_access`; `test_degree_tuple_is_obtained_once_per_branch_call` |
| SR14: independent positive scaling and large unreduced integer records | `test_positive_branch_scaling_uses_independent_expected_values`; `test_positive_generic_scaling_from_literal_network_n5`; `test_huge_multiplicities_and_unreduced_parameter_entries`; `test_huge_generic_mixed_zero_signs_and_standalone_records` |
| SR15: static exactness, transitive loop boundaries, source controls and import isolation | `test_source_exactness_dependency_and_structural_loop_controls`; `test_source_recovery_and_terminal_properties_have_no_transitive_loops`; `test_in_memory_prohibited_source_controls`; `test_fresh_process_import_isolation_and_export_free_package_root` |

- The test suite exercises the 81 precommitted exact-ValueError declarations, 120 literal
  branch anchors/2,080 shores, eight literal network tuples/128 shore rows, and the finite
  core: 329 active instances, 2,612 base masks, 13,160 branch/parameter cases, and 104,480
  branch-shore evaluations. Generic forms add 216 cases/1,512 shores. Negative A is checked
  in all four branches; RICH at (-2,1) exercises mixed zero/sign coefficients in 2/3, while
  (-3,1) distinguishes their constants. Under active input, negative A in 0/1 gives
  strictly positive gamma. No parameter sign restriction is imposed by this sanity check.
- The separate handoff implementation audit derives expectations from the definitions,
  without importing the consuming test, verifier, flow, or private fixture JSON. It checks
  the core and anchor/generic cases independently, plus 122 supplementary rejection/hostile-
  object calls and 36 large-integer/raw-scaling cases. Ordered original arcs, zero positions,
  separate shifts/constants, and the restricted-family counterexample pass. The 122 calls
  are separate from, not a replacement for, the test file's 81 rejection declarations.
- Before this documentation change, the live gate pinned implementation R1, frozen test
  R2, and all 28 base files to 29 targeted tests, 439 full-suite tests, live source preflight,
  full repository Ruff, and the independent implementation audit passing. It also checked
  source/import isolation and byte nonmutation. The 28-base-file statement describes that
  PRE-NOTE state; this authorized CONFORMANCE change does not rewrite or reinterpret it.
- Source review checks O(n+m) integer-operation construction including record validation,
  and O(1) integer-operation recovery/terminal properties. Numerical encoding lengths still
  affect bit costs. Positive raw scaling scales coefficients, capacities, shifts, constants,
  and recovered residuals; it preserves positions/signs, not raw magnitudes. No timing,
  constant-byte-memory, unrestricted-composition, or algorithm-level bit-growth claim follows.
- No sign-routing identity test or separate implementation audit calls flow or minimization.
  Full-suite execution still runs the previously closed flow tests. This unit does not
  implement forced contractions, parity anchors or terminal toggles, parity minimization,
  family argmin selection, or the branch oracle's independent raw-residual re-evaluation.
- Historical Unit 09 deferrals of sign routing and branch-coefficient construction receive
  this Unit 10 evidence; residual minimization and every other downstream obligation remain
  deferred. Do not promote prop:branch-transform's ratio theorem, thm:branch-oracle,
  parity/GR, branch/global correctness, certificate work, bit-growth rows, or telemetry.
  A constructed network or recovered scalar certifies neither admissibility, attainment,
  nor global optimality. The complete three-file staged tree still requires isolated
  verification, atomic commit, and remote closure under TEST_PLAN section 26.

## Unit 11 atomic-family parity-cut implementation note

- The new `lem:parity-anchor` and `thm:GR` rows are the narrowly scoped rows authorized by
  DESIGN 4.8.16 and TEST_PLAN PC20/section 28. They record executable conformance for the
  supported forced-family transformation and exact reference parity-cut minimizer. The
  governing source supplies the mathematical proofs; finite tests do not prove the universal
  statements. The GR row covers this cut specialization, not a general submodular optimizer.
  Every previous theorem row and status is unchanged.
- `exactfrac.parity_cut` owns ParityCutProblem, ParityCutResult, ParityCutStats, and the three
  functions reduce_atomic_family, lift_source_shore, and minimum_parity_cut. Frozen/slotted
  structural records, exact built-in types, and plain ValueError enforce their stated shapes.
  Record validity is not provenance from a family or an independent cut/optimality certificate.
  ParityCutResult alone cannot validate its finite upper universe, terminal parity, or value
  attainment without a problem. Normally constructed frozen records are trusted by consumers.
- Original vertices use 0..n-1, original source/sink n/n+1, and optional anchor n+2. Reduced
  source/sink are 0/1. Canonical classes contain their complete original preimages; remaining
  original vertices are increasing singletons. Ordinary pair queries have a THIRD temporary
  coordinate system. Their backend shores are lifted to the base reduced problem BEFORE
  parity filtering; public lifting to original U is a separate later operation.
- Reduction checks exact network/family types and finite T/I/O masks before invoking the
  closed family.is_nonempty predicate or scanning capacities. Well-shaped infeasible families
  return None; malformed inputs raise ValueError. Constructor-bypassing forgeries are outside
  the public contract. Backend exceptions propagate; they are not converted to infeasibility.
- Capacity transport removes mapped loops, sums parallel ORIGINAL directed capacities, and
  emits encountered ordered pairs in increasing order, retaining zero sums. Opposite original
  arcs remain distinct; no division by two, artificial infinity, or anchor edge is introduced.
  pi=0 places one isolated parity-anchor token in the forced source class; pi=1 places none.
  Contracted terminal tokens aggregate by XOR. Odd total terminal cardinality toggles sink
  bit 1 by symmetric difference, including removal of an existing sink token. Both geometric
  lifting and the odd-terminal/original-family parity equivalence preserve cut capacity.
- Lifting accepts either terminal parity of a valid reduced source/sink shore and strips all
  auxiliary bits. It performs no minimization or cut calculation. minimum_parity_cut returns
  an unshifted nonnegative cut value and reduced-coordinate shore, with separate diagnostics.
  A zero terminal mask returns (None, zero stats) without graph access. Empty arcs, all-zero
  capacities, disconnectedness, or an ordinary candidate of wrong parity are not infeasibility.
- For nonzero even terminals, all compatible pairs execute in increasing inside/outside order:
  inside != sink, outside != source, inside != outside. There are N*N-3*N+3 actual ordinary
  calls, including one when N=2. Each query consumes the closed backend's inclusionwise-minimal
  ordinary minimum source shore; an arbitrary tied ordinary minimizer is insufficient. Lifted
  odd candidates update the incumbent only on strict value improvement. No zero early exit,
  pair elimination, or secondary mask/cardinality key is used. The selected parity optimum is
  deterministically first retained, not claimed to be the inclusionwise-minimal parity optimum.
- Stats count actual calls, sum backend augmentations and bfs_scans, and take the maximum
  backend peak_generated_value, or zero for no calls. The peak is FLOW-ONLY: it excludes
  contraction sums, masks, and other non-flow integers. Diagnostics do not influence selection,
  parity, or infeasibility and are not certificate fields or global peak_integer_bits telemetry.
- The frozen R1 file supplies the following 28 principal tests under ORACLE-056--068. Other
  than the two scoped rows above, this is an engineering-obligation mapping. Literal expected
  records come from the committed human-readable catalogue; the consuming tests do not read
  private handoff JSON. Expected parity minima, capacities, and least ordinary shores are
  independently enumerated, never seeded from production results. Diagnostic observation is
  used only for the backend-aggregate checks that PC15 expressly requires.

| Production obligation | Principal tests in `tests/test_parity_cut.py` |
|---|---|
| PC1--PC3: public surface, immutable records, exact shapes and finite universes | `test_public_surface_signatures_and_annotations`; `test_records_are_frozen_slotted_structural_and_not_certificates`; `test_all_fourteen_registered_valid_record_declarations`; `test_all_122_registered_exact_valueerror_cases`; `test_supplementary_hostile_exact_types_and_record_guard_order` |
| PC4: closed validation and logical feasibility before capacity work | `test_reduction_uses_closed_guards_before_predicate_and_capacity_scan` |
| PC5--PC8: literal contractions, zero/parallel transport, anchor/XOR/toggle and full correspondence | `test_fixed_contractions_exact_classes_arcs_and_raw_order_invariance`; `test_anchor_xor_and_sink_toggle_have_literal_distinct_meanings`; `test_parity_anchor_correspondence` |
| PC9: either-parity lifting, closed finite-mask checks and trusted-record boundary | `test_lifting_all_literal_rows_in_both_parities_without_graph_access`; `test_lift_closed_mask_validation_and_constructor_trust` |
| PC10--PC14: literal minima, no-terminal shortcut, full pair order, least shores and coordinate/tie traps | `test_literal_minimum_results_shores_and_separate_stats`; `test_zero_terminal_shortcut_does_not_read_arcs_or_call_flow`; `test_fixed_query_traces_and_least_backend_shores`; `test_all_compatible_pair_orders_including_zero_value_early_exit_trap`; `test_coordinate_trap_filters_only_after_temporary_to_problem_lifting`; `test_arbitrary_tied_minimizers_are_not_an_admissible_backend`; `test_minimum_parity_cut` |
| PC15/PC18: separate exact diagnostics, error propagation and no hidden reconstruction | `test_diagnostic_anchors_and_flow_only_peak`; `test_diagnostics_cannot_select_a_different_tied_candidate`; `test_backend_exceptions_propagate_instead_of_becoming_infeasibility`; `test_consumer_does_not_reconstruct_its_valid_problem` |
| PC14/PC16--PC17: scaling, source-residual seams, retained shifts and label/order independence | `test_fixed_large_capacities_and_raw_positive_scaling`; `test_source_residual_family_seams_and_shift_ownership`; `test_original_labels_and_raw_arc_order_do_not_change_tied_choices` |
| PC18--PC19: exact-source/finite-work guards, negative controls and fresh import isolation | `test_source_exactness_dependencies_and_finite_work_guards`; `test_source_guard_negative_controls_cover_previous_unit_gaps`; `test_fresh_process_import_isolation` |

- The frozen tests exercise all 14 valid-record and 122 rejection declarations, 29 contraction
  fixtures/67 literal lifting rows, 14 problem fixtures/51 shore rows, 40 ordinary-query trace
  rows, and the 21-query arbitrary-tie trap. The family corpus covers 18,720 descriptors,
  15,612 geometric lifting checks, and 9,360 odd-shore images, including 554 sink removals.
  The graph corpus covers 4,164 graphs, 33,032 terminal problems, 131,592 source shores, and
  201,284 actual ordinary calls. None and zero optima remain separate in these finite counts.
- The separate handoff implementation audit does not import the consuming test, verifier,
  or private JSON. It independently enumerates expected minima and least ordinary shores,
  checks the same graph/family corpus and every actual ordinary query's construction/order,
  and additionally performs 134 supplementary exact-ValueError/hostile-object checks, seven
  standalone anchors with 42 calls, one raw-order/shift check, two diagnostic/backend-boundary
  checks, and 11 large-capacity/raw-scaling/130-vertex correspondence cases. Corpus overlap
  between the test and separate audit is not counted as disjoint coverage. The implementation
  package also records rejection of 16 faulty source variants and one nonleast-backend control;
  these finite mutation controls do not establish freedom from every possible defect.
- Before this documentation change, the live gate pinned implementation R1, frozen test R1,
  and all 30 base files to 28 targeted tests, 467 full-suite tests, live source preflight,
  repository Ruff, independent implementation audit, and input/source nonmutation passing.
  The 30-base-file statement describes that PRE-NOTE state. This authorized CONFORMANCE edit
  does not rewrite it or make its old manifest an assertion about the post-note repository.
- Source review retains the ruled integer-operation carriers: O(n+E_in log(E_in+1)) initial
  reduction, O(N) public lifting, and zero-safe O(N^3*(1+E^2)) nonzero-terminal minimization
  including closed flow calls. One temporary graph is processed at a time with O(N+E)
  auxiliary integer records; empty terminals use the constant-operation shortcut. Capacity
  sums are bounded by the supplied total and mask lengths by explicit universes. These are
  operation/record and encoding arguments, not timing guarantees or constant-byte-memory
  claims. No outer branch/global complexity theorem or bit-growth experiment is promoted.
- The original Unit 10 network retains negative_shift and constant; reduction adds no shift.
  The 24 source-residual seam cases recover cut_value-negative_shift+constant and independently
  check B*c_j(U)-A*h_j(U) over the SAME permitted family. This local composition does not
  implement ExactBranchMin, enumerate/select all branch families, or discharge thm:branch-oracle.
  Unit 12 still owns original-shore reconstruction, exactly-once shift recovery, and independent
  source-residual re-evaluation before comparisons in that integrated oracle.
- Unit 10's historical deferrals of forced contraction/parity minimization receive the scoped
  evidence here; all other deferrals remain. lem:ek, lem:sign-routing, and all earlier rows
  retain their existing text/status. No ratio/endpoint, branch/global solver, certificate,
  Standard/Accelerated, telemetry, or outer bit-growth obligation is marked complete. A local
  exact parity minimum is not an independent admissibility, attainment, or global-optimality
  certificate. The three-file staged tree still requires isolated verification, atomic commit,
  and synchronized remote closure under TEST_PLAN section 28 before Unit 11 is closed.

## Unit 12 integrated exact branch residual oracle implementation note

- The new `thm:branch-oracle` row is the fixed-parameter scope authorized by DESIGN 4.9.18
  and TEST_PLAN BO22/section 30. `exactfrac.oracle.exact_branch_min` implements
  `alg:branch-min` with a separately prepared complete cover and one lazy original network
  per nonempty query. It minimizes B*c_j(U)-A*h_j(U) over the entire original D_j for the
  submitted parameter (A,B), B>0. It does not minimize c_j/h_j or solve an outer branch.
  The governing source supplies the mathematical theorem; the tests and separate audit
  supply executable conformance evidence on finite cases, not a universal proof.
- BranchOracleContext retains the exact Instance and the complete four-tuple returned by
  the closed family enumerator, called once during construction. Its families field is
  init=False; no caller-provided partial cover is accepted. Query traversal reuses only
  the selected tuple, in stored order, including overlapping, repeated, and empty
  descriptors. No re-enumeration, sorting, deduplication, or parameter cache is introduced.
- Consumer checks run in order: exact context type, exact branch type/range, then closed
  validate_pair, before family inspection or graph work. Malformed public inputs raise
  exact ValueError; arity and frozen mutation retain Python behavior. Results and stats
  are frozen/slotted structural records, not provenance checks or independent certificates.
  Constructor-bypassing forgeries remain outside this normal-construction contract.
- Empty descriptors are counted and skipped before graph work. If no descriptor is feasible,
  return (None, stats), distinguishing zero descriptors from an all-empty nonzero tuple.
  A feasible zero or negative minimum is not None. The first feasible descriptor triggers
  exactly one closed coefficient calculation and sign-routed network construction. That
  same query-local original network is used for every reduction and recovery; another
  parameter query builds a new network. No network is constructed for an all-empty query.
- Each nonempty descriptor receives one closed reduction and parity minimization. Lift
  its reduced shore to original vertices, check the original finite universe and I/O/parity
  membership, and compute s=shore_f, b=shore_b_q, d=shore_d_q from original Instance records.
  The four source pairs are (s+b-1,d+1-s), (s+b-2,d-s), (b-d,s-1), and (b-d-2,s), under
  their literal DESIGN 4.9.7 domains. Domain failure or h<=0 is an internal RuntimeError,
  never a repaired denominator or silently discarded candidate. Closed dependency errors
  propagate unchanged; unexpected None from a promised nonempty reduction/minimum is also
  RuntimeError, not branch infeasibility.
- Independently re-evaluate raw=B*c-A*h with the closed rational helper. Recover once from
  the ORIGINAL network as cut_value-negative_shift+constant; contraction adds no shift.
  Require raw==recovered before retention and record raw, not the unverified cut value.
  A mismatch raises RuntimeError even if the erroneous value would improve the incumbent.
  This local consistency check is not a stand-alone cut or density-optimality certificate.
- Scan the complete cover after zero/negative residuals and zero cuts. Replace the incumbent
  only on strict raw improvement; equality retains the first encountered minimum without
  a secondary h, c, mask, cardinality, or diagnostic key. The closed least-ORDINARY-cut
  requirement is unchanged. No inclusionwise-least PARITY or BRANCH optimum is claimed;
  legal alternative within-family exact minimizers remain mathematically admissible.
- Query statistics count r_j examined descriptors and k_j feasible descriptors/parity calls,
  sum ordinary calls/augmentations/scans, and take the maximum flow-only peak (zero with no
  calls). max_flow_calls is a derived alias of ordinary_min_cut_calls. Statistics do not
  decide feasibility or selection and do not measure preparation, every generated integer,
  or global peak_integer_bits. Raw parameter scaling by k>0 retains shore,c,h and scales
  residual by k under the shipped policy; it does not assert invariant general diagnostics
  or bit costs. Residual magnitudes from differently encoded denominators are not directly
  comparable across queries without the appropriate rational scaling.
- The following mapping includes all 30 frozen original-R1 tests under ORACLE-069--082.
  Only the row above promotes a theorem-facing obligation. The other entries map engineering
  requirements; BO21 is additionally supported by the separate private implementation audit,
  and BO22 by this source-bound documentation crosswalk. Literal tables were fixed before
  consuming code; no private handoff JSON supplies expected answers at test runtime.

| Production obligation | Principal tests in `tests/test_oracle.py` |
|---|---|
| BO1: fixed public surface and record shapes | `test_public_surface_shapes_annotations_and_signatures`; `test_valid_records_equality_frozen_and_noncertifying_shapes` |
| BO2: complete, immutable, once-prepared cover | `test_context_retains_exact_instance_complete_cover_once` |
| BO3: exact public errors and validation precedence | `test_all_179_registered_rejections_and_python_behaviors`; `test_validation_phases_precede_any_graph_or_empty_family_inspection` |
| BO4--BO5: independent source domains, literal c/h, and exact branch minima | `test_literal_tables_and_independent_source_calculator`; `test_exact_branch_min` |
| BO6--BO8/BO14: complete traversal, genuine emptiness, and one lazy network | `test_all_empty_branches_skip_every_graph_dependency`; `test_complete_selected_sequence_lazy_network_and_seam_calls`; `test_original_networks_match_all_12_literal_rows` |
| BO9--BO10/BO12--BO14: constrained minima, coordinate/shift recovery, and tie/early-exit traps | `test_early_zero_negative_and_secondary_tie_traps`; `test_unrestricted_cut_does_not_replace_family_parity_minimization`; `test_coordinate_recovery_literal_anchors` |
| BO11--BO12/BO17: internal promises fail before candidate retention | `test_internal_none_from_reduction_or_parity_is_runtime_error`; `test_internal_finite_shore_membership_faults_fail_before_source_evaluation`; `test_internal_source_domains_and_h_guard_before_raw_or_recovery`; `test_recovery_and_raw_mismatches_never_become_better_candidates`; `test_closed_dependency_exceptions_propagate_unchanged` |
| BO13/BO16: legal alternative minimizers and nonauthoritative diagnostics | `test_alternative_legal_within_family_minimizer_is_not_rejected`; `test_legal_changed_diagnostics_do_not_change_the_selected_result`; `test_registered_stats_and_146_ordinary_trace_calls` |
| BO15/BO18: fresh query state, labels, raw scaling, and nonmutation | `test_context_reuse_parameter_network_identity_and_nonmutation`; `test_labels_and_normal_reconstruction_do_not_change_query_results`; `test_raw_scaling_20_registered_cases_preserve_unreduced_c_h` |
| BO5--BO6/BO20: tiny-domain corpus, observed calls, number sizes, and preparation separation | `test_60_large_capacity_cases_and_polynomial_number_bounds`; `test_341_descriptor_preparation_is_not_repeated_in_a_d0_query`; `test_exhaustive_corpus_13160_queries_and_138720_actual_ordinary_calls` |
| BO18--BO19: fresh imports, exact-source restrictions, and iteration structure | `test_imports_in_a_fresh_process_resolve_only_closed_project_layers`; `test_production_source_imports_exact_arithmetic_and_no_side_effect_paths`; `test_source_has_no_recursive_or_magnitude_or_all_shore_iteration` |

- The frozen test contains 179 registered rejection/Python-behavior cases (171 exact
  ValueError, five TypeError, three FrozenInstanceError), 360 fixed queries on nine
  instances and ten parameters, 12 literal networks, coordinate/shift/tie traps, and
  146 observed ordinary calls in diagnostic anchors. Its independent tiny-instance
  comparison covers 329 instances and 13,160 queries: 11,370 feasible and 1,790 infeasible,
  with 61,400 descriptor examinations and 34,040 feasible family calls. The previously
  specified 138,720 ordinary calls are also checked against actual backend invocations.
  These nested checks are not additional collected pytest test cases.
- The separate implementation audit fixes expected minima by original vertex-set/domain
  enumeration before production import. It imports no consuming test, global verifier, or
  private expected-data file. On the same 13,160-query corpus it checks 138,720 observed
  least-ordinary calls and 277,160 cut shores; overlap with the consuming corpus is not
  counted as disjoint coverage. It also checks 360 fixed queries, 168 supplementary exact-
  ValueError/hostile cases, two normal Python cases, 23 internal/dependency probes, 60 large-
  capacity cases, 20 raw scalings, five reuse queries, a 341-descriptor preparation anchor,
  and legal alternative-minimizer/diagnostic controls. Backend output is a checked subject,
  never the source of the expected original-domain minimum.
- Before this documentation change, the live GREEN gate recorded 30 collected/30 passing
  targeted tests and 497 collected/497 passing full-suite tests, actual repository Ruff
  0.16.5 source preflight and full checks, and the pinned independent audit passing. All
  32 prior tracked files, the frozen original R1 test, saved RED records, and index bytes
  remained unchanged. That 32-file statement describes the PRE-NOTE state; this authorized
  CONFORMANCE edit does not rewrite its evidence or make the old ledger describe a new
  post-note tree. Source and test remain the exact byte identities that passed GREEN.
- Source-to-code work review is separate from finite test counts. With
  r_j=len(context.families[j]) and R_all=sum_j r_j, preparation pays O(n+m+R_all) integer/
  comparison operations and O(R_all) descriptor records once. It is not charged to a D0
  query or silently repeated. Each query costs O(1+r_j) before graph work; when k_j>0 it
  builds one O(n+m) network and processes each feasible family sequentially through the
  closed zero-safe parity/cut stack, lifting, original sums, and residual checks. DESIGN
  4.9.16 therefore supplies O(1+r_j*(n+3)^3*(m+n)^2) per query, explicitly including r_j=0.
  The exact ordinary-call sum is sum_F(N_F*N_F-3*N_F+3), at most k_j*(n+3)^2. Auxiliary
  integer records beyond input/context are O(n+m); these are not constant-byte or timing
  claims. The many-family D0 anchor checks the preparation/query separation, not asymptotics.
- Source-to-code number-size review follows DESIGN 4.9.17, not flow-only peak telemetry.
  Write Q=sum(q_e). Active original sums satisfy 0<=s<=d<=2Q and 0<=b<=Q, hence
  abs(c)<=3Q+2, abs(h)<=2Q+1 and abs(raw)<=B*(3Q+2)+abs(A)*(2Q+1).
  The closed coefficient table gives abs(gamma[v])<=(2*abs(A)+B)*Q and
  abs(constant)<=abs(A)+2*B. Original total directed capacity is
  S=2*B*Q+2*sum_v abs(gamma[v]), with negative_shift<=sum_v abs(gamma[v]).
  Contractions and temporary contractions discard loops and sum subsets of original
  capacities; capacity/flow/residual-capacity magnitudes are bounded by S. Signed recovery,
  original raw forms, O(n)-bit masks, and structural counters consequently have polynomial
  encoding length in L+bits(A)+bits(B). This composed-query argument is not a finite proof
  from timing, full intermediate-bit instrumentation, or discharge of outer bit-growth
  lemmas. The 60 large-capacity and 20 raw-scale cases are regression evidence only.
- Historical Unit 10/11 deferrals of integrated original-shore evaluation, complete-cover
  selection, and exactly-once residual recovery receive the scoped Unit 12 evidence here;
  those historical notes and every previous theorem row/status remain unchanged. No ratio
  transformation, Standard/Accelerated termination, branch/global invariant or correctness,
  H2/witness reconstruction, certificate verification, telemetry, or experiment obligation
  is promoted. In particular, none of the existing planned outer rows becomes green.
  Unit 12 still requires the complete three-file staged-tree isolation, atomic implementation
  commit, synchronized remote closure, and private closure notes under TEST_PLAN section 30.

## Unit 13 Standard branch solver implementation note

- The existing `prop:standard-correct` row is promoted from planned to green; its
  promise and `tests/test_branch.py::test_standard` mapping are unchanged. The new
  `lem:standard-bits` row records the number-size bridge authorized by DESIGN 4.10.15
  and TEST_PLAN ST20/section 32. Every other pre-existing row, status, and historical
  note is byte-for-byte unchanged. These rows record executable conformance and the
  source-to-code argument below, not universal proofs established by finite tests.
- `exactfrac.branch.solve_branch_standard` implements only `alg:standard-branch` on a
  normally constructed closed `BranchOracleContext` and branch j in (0,1,2,3). It
  returns the transformed minimum rho_j=min c_j(U)/h_j(U) and an original attaining
  shore, or None for branch infeasibility. This is not the original endpoint density,
  global density optimum, witness reconstruction, or a standalone optimality certificate.
  Source-domain membership and literal original c/h remain the closed Unit 12 guarantee.
- `BranchResult(root, shore)` and `StandardBranchStats(oracle_calls, outer_iterations,
  newton_updates, oracle_stats)` are frozen/slotted structural records. The root is
  validated as a RawPair before the positive shore; signed, zero, and unreduced pairs
  are retained literally. Standalone construction cannot check the upper shore bound,
  domain membership, or optimality. Statistics validate three exact nonnegative ints
  in order, then the exact closed nested record; construction does not certify work or
  impose the successful-run counter equations. Wrong arity/frozen mutation retain
  Python behavior; malformed supported public inputs raise exact ValueError.
- The solve validates exact context type, then exact branch type/range, before querying
  or inspecting graph information. It reuses the supplied prepared context without
  re-enumerating/filtering families or inspecting a family tuple to bypass the seed.
  Every optimizer call is the closed exact_branch_min with that context and branch.
  Normal replies must have the exact tuple/result/stat types; an original shore must
  fit the n-bit universe, and residual_numerator(parameter,c,h) must equal the reported
  residual. Explicit violations raise RuntimeError. Arbitrary dependency exceptions
  propagate unchanged rather than becoming infeasibility or partial success.
- Exactly one seed query is made at literal (0,1). A None seed returns counts (1,0,0)
  with its diagnostics included. Feasible seed residuals may have any sign, including
  zero; no seed sign terminates a feasible solve. The next parameter is exactly
  pair_add_one(make_pair(c0,h0))=(c0+h0,h0), not a reduced equivalent or the Accelerated
  seed ratio. The first loop residual at K is strictly negative; after a feasible seed,
  a later None or positive residual is an internal error, not a successful return.
- Each negative loop residual resets to fresh make_pair(c,h), after an explicit exact
  compare_pairs check for strict decrease. The loop stops only on raw residual zero.
  It returns the SUBMITTED terminal parameter and the CURRENT oracle shore separately.
  In the committed EQUALITY-j3 trap, the submitted pair is (-4,4) and the terminal
  shore is 1 with source terms (-2,2); the returned record retains (-4,4), not (-2,2).
  There is no normalization, old-denominator accumulation, reflection, visited-shore
  termination, tolerance, or numerical iteration budget.
- The shipped oracle's fixed-order, strict-improvement retention is unchanged. The
  Standard wrapper introduces no max-h, min-mask, or diagnostic secondary objective.
  Independently legal argmin choices can change raw pair/shore/trajectory and counts
  while preserving the numerical branch optimum. TEST_PLAN A4 receives Standard-only
  evidence here; no Accelerated invariant or correctness obligation is promoted.
- Per-solve diagnostics include seed, K, and terminal query exactly once. The first
  six BranchOracleStats fields are summed and flow_peak_generated_value is maximized.
  The derived max_flow_calls alias retains its ordinary-cut meaning. For a successful
  feasible solve with u updates, u>=1, outer_iterations=u+1, oracle_calls=u+2; infeasible
  counts are (1,0,0). Context preparation is not counted again. The peak remains FLOW-
  ONLY, not a measurement of every generated integer. Mathematical first-loop/sign
  state is separate from counters; diagnostics cannot decide validity or termination.
- The following mapping includes all 31 frozen R2 tests under ORACLE-083--096 and
  ST1--ST18. ST19 additionally uses the separate private source-domain implementation
  audit and executed mutation controls; ST20 is this documentation crosswalk. Expected
  literals are from the committed human catalogue, not runtime private expected JSON.

| Production obligation | Principal tests in `tests/test_branch.py` |
|---|---|
| ST1--ST2: exact public surface, immutable records and noncertifying constructors | `test_public_surface_signatures_annotations_and_package_root`; `test_records_are_frozen_slotted_structural_and_not_certificates`; `test_all_nine_registered_accepted_record_declarations`; `test_all_92_registered_public_rejections_and_python_arity`; `test_result_root_guard_and_statistics_field_validation_order` |
| ST3: public validation before graph access and optimizer use | `test_public_validation_precedes_graph_access_and_seed`; `test_keyword_calls_preserve_the_exact_positional_interface` |
| ST4--ST5: mandatory seed, infeasible branches, literal K and zero-seed continuation | `test_seed_is_mandatory_for_zero_and_all_empty_descriptor_branches`; `test_zero_seed_continues_and_negative_seed_can_give_positive_k`; `test_context_preparation_is_not_repeated_and_seed_is_not_bypassed` |
| ST6--ST8: independent original domains, shipped trajectories and fresh resets | `test_literal_shores_domains_and_complete_optima_are_independent`; `test_all_68_literal_shipped_trajectories_and_complete_accounting`; `test_all_four_branches_execute_multiple_fresh_newton_resets`; `test_independent_core_census_and_both_committed_stream_fingerprints`; `test_standard` |
| ST9: submitted raw root and current terminal shore | `test_terminal_parameter_and_current_shore_are_separately_preserved` |
| ST10/A4: legal argmin alternatives without a secondary objective | `test_all_81_named_legal_argmin_paths_without_secondary_preference`; `test_all_5374_core_legal_paths_are_valid_wrapper_runs` |
| ST11--ST12: explicit shape/universe/binding/sign and progress failures | `test_all_seed_response_shape_type_universe_and_binding_faults`; `test_later_none_nonnegative_k_positive_loop_and_terminal_binding_faults`; `test_comparator_faults_exercise_explicit_strict_progress_guard`; `test_each_successful_reply_is_bound_to_the_submitted_raw_parameter` |
| ST13: exact dependency-exception propagation | `test_all_nine_dependency_exception_instances_propagate` |
| ST14--ST15: six sums/one maximum, diagnostic independence, reuse and labels | `test_all_four_diagnostic_streams_sum_six_max_one_without_control_effect`; `test_six_registered_reuse_steps_and_interleaved_direct_queries`; `test_registered_labels_change_neither_raw_results_traces_nor_diagnostics` |
| ST16: source restrictions, static negative controls and fresh import isolation | `test_production_source_exact_imports_arithmetic_and_no_graph_rescan`; `test_source_guard_negative_controls_reject_prohibited_constructs`; `test_fresh_process_imports_resolve_to_only_permitted_project_layers` |
| ST17--ST18: large actual solves, reset carriers and source-dependent work interpretation | `test_symbolic_large_families_and_all_112_actual_branch_solves`; `test_literal_reset_carriers_and_integer_wyz_change_of_variables` |

- The consuming tests check 9 accepted-record declarations, 92 public rejection/Python-
  behavior declarations, 18 internal-failure declarations, and 9 dependency-exception
  boundaries. They reproduce 68 named branch solves/168 query rows, 81 named legal
  paths, the 329-instance core with 1,316 real solves/3,635 oracle calls, and all 5,374
  core legal paths. The core has 1,137 feasible and 179 infeasible branches; 629 roots
  are negative, 508 positive, and none zero. Zero-root cases are supplied separately.
  Its 116 terminal raw-pair distinctions are an overlapping structural view, not new
  samples. Four constant-support symbolic families give 112 large branch cases through
  exponent 4096. These nested checks are not additional collected pytest cases.
- The separate implementation audit fixes source-domain optima and complete legal-path
  expectations before production import, without importing the consuming tests, global
  verifier, or private expected-data JSON. It checks 1,440 actual solves/3,878 real oracle
  calls across the core, three supplementary inputs, and 112 large branch cases, plus
  6,022 pre-fixed legal paths/17,815 synthetic query replays. Its actual solves contain
  654 negative, 533 positive, and 8 zero roots, with 245 infeasible branches. The audit
  checks membership in the complete legal path set; deterministic shipped trajectories
  are additionally fixed by the consuming tests. Overlap with tests is not disjoint
  coverage. Twenty-two faulty source variants are compiled and executed in isolated
  in-memory modules; all are rejected by mathematical/interface assertions, not lint
  or syntax rejection. This finite mutation set does not prove absence of every defect.
- The pre-note live GREEN gate bound implementation R1 and frozen test R2 to 31 actual
  collected/passing targeted cases, 528 collected/passing full-suite cases (497 earlier
  plus 31 Unit 13), actual repository Ruff 0.16.5 source preflight/full checks, the
  separate implementation audit, and 22 executed mutation rejections. All 34 committed
  base files, the frozen test, index bytes, refs, private notes, and historical evidence
  remained unchanged. That 34-file ledger describes the PRE-NOTE state. This authorized
  CONFORMANCE-only edit does not rewrite it or pretend it describes the post-note tree.
- Correctness is the source's `prop:standard-correct` instantiated by the actual loop.
  On a nonempty finite domain with h>0, F(lambda)=min(c-lambda*h) has unique zero rho.
  K>rho gives a negative first loop residual. At every continuing iterate an exact
  argmin gives rho<=c/h<lambda. Fresh resets belong to the finite candidate-ratio set;
  strict decrease therefore terminates, and the exact-zero shore attains rho. This
  argument does not use WYZ, an empirical iteration count, or a magnitude-based cutoff.
- The `lem:standard-bits` bridge follows DESIGN 4.10.14 and the closed Unit 12/flow
  number-size arguments. With Q=sum(q_e), C=3Q+2, H=2Q+1, every submitted (A,B)
  satisfies abs(A)<=C+H=5Q+3 and 1<=B<=H; after each reset, abs(A)<=C. Original source
  terms bound residual magnitudes by B*C+abs(A)*H<=H*(2C+H)=(2Q+1)*(8Q+5), with
  polynomial-size cross products as well. Every update resets the denominator to h;
  no product of preceding denominators accumulates. Closed oracle sums/products and
  the zero-safe flow carrier give polynomial encoding length for query numbers.
  Masks use O(n) bits. Counter aggregation adds structural logarithmic factors under
  the source iteration bound. Carrier tests are finite regression evidence; no complete
  peak_integer_bits telemetry, universal empirical bit proof, or production cutoff is
  asserted. The full telemetry obligations remain deferred.
- The `cor:standard-strong` operation chain is documented separately, not promoted by
  an empirical theorem row. Let t=oracle_calls and r_j=len(context.families[j]). The
  actual wrapper makes one seed call and one oracle call per loop, keeps O(1) outer
  integer records, and does O(1) wrapper arithmetic/diagnostic operations per call.
  The fixed three-counter constructor loop does not scan the input. Unit 12's uniform
  carrier gives O(t*(1+r_j*(n+3)^3*(m+n)^2)), including empty descriptors and r_j=0.
  Context construction separately pays O(n+m+R_all) once, with R_all=sum_j r_j. The
  frozen `thm:WYZ` invocation supplies t=O(M^2 log M), M=n+m+1; together with
  `lem:standard-bits` this is the source-dependent strongly polynomial composition.
  Finite tests do not prove WYZ, its asymptotic constant, or uniformly flat observed
  counters under arbitrary magnitude changes. Integer-operation/record bounds are
  not constant bit time, constant byte memory, or wall-clock guarantees.
- Historical deferrals of Standard branch iteration receive only this Unit 13 evidence.
  The Accelerated `prop:branch-invariant`, `prop:branch-correct`, `thm:accelerated-bound`,
  and `lem:bitgrowth`, global solver, H2/unit endpoint reconstruction, solver witness reconstruction,
  certificate assembly/independent checking, full telemetry, CLI, and experiments
  remain unpromoted.
  Source/test/CONFORMANCE still require the separate complete-candidate staging,
  index-tree isolation, atomic implementation commit, synchronized remote closure,
  and saved private notes under TEST_PLAN section 32 before Unit 13 is fully closed.
