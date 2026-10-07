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
| prop:branch-correct | Accelerated branch solver returns infeasible or the exact transformed branch root and an original attaining shore; source finite-termination bridge and finite test scope below | tests/test_branch_accelerated.py::test_all_1316_actual_core_branches_agree_with_standard_and_independent_minima; tests/test_branch_accelerated.py::test_source_selected_raw_terminal_pair_traps_at_all_three_sites; tests/test_branch_accelerated.py::test_all_51_named_legal_argmin_paths_and_no_secondary_preference | green |
| thm:accelerated-bound | implemented Accelerated recurrence and constant oracle-call accounting per iteration, composed with the source-dependent O(M log M) bound; finite trace/encoding checks are not a proof of DKNV or a production cutoff | tests/test_branch_accelerated.py::test_all_112_named_actual_trajectories_closed_primitives_and_accounting; tests/test_branch_accelerated.py::test_all_reflections_and_retained_transfers_match_literal_source_records; tests/test_branch_accelerated.py::test_all_168_large_graph_solves_symbolic_traces_and_attempted_bit_bounds | green |
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

## Unit 14 Accelerated branch implementation note

- Scope is DESIGN 4.11, TEST_PLAN AC1--AC24, and the pinned V2.2 `alg:branch`.
  The formerly planned `prop:branch-correct` row now points to actual frozen
  Accelerated tests. The new `thm:accelerated-bound` row records the source-dependent
  work bridge explained below, not an empirical proof of its iteration bound. Every other
  existing row and status, including both Standard rows, is unchanged. All earlier
  note bytes are preserved as historical evidence; later scoped evidence does not
  rewrite their earlier statements of deferred work. A green row records implemented
  conformance with the source, not a universal theorem proved by finite testing.
- `solve_branch_accelerated(context, branch)` returns `(BranchResult | None,
  AcceleratedBranchStats)`. The root is the signed transformed minimum c_j/h_j, NOT
  an endpoint density, global optimum, compact witness, or certificate. BranchResult
  remains the unchanged shared raw-pair/shore carrier. Statistics are frozen/slotted
  structural records: seven nonnegative exact-int counters then exact BranchOracleStats,
  validated in field order. Constructor success is not provenance or successful-run
  accounting. Public malformed inputs raise exact ValueError; wrong arity retains
  Python behavior. No diagnostic participates in a mathematical decision.
- The Unit 14 authority's three references to 'six' preserved Standard definitions (DESIGN §4.11.15, TEST_PLAN AC3, completion-gate item 5) are a clerical miscount; the preserved set is exactly the five definitions named in DESIGN §4.11.14 — BranchResult, StandardBranchStats, _checked_query, _add_diagnostics, solve_branch_standard — with their complete bodies, as ruled on Sep 10, 2026 and recorded in the private handoff erratum. The sealed authority commit is not amended.
  Their decorators, class/function bodies, signatures and annotations remain identical
  to closed Unit 13. The allowed module-description/import/export changes and the two
  appended Accelerated definitions do not refactor Standard. The previously frozen
  compatibility amendment changes only the three ruled Standard test functions;
  all 31 Standard test names, literals, and 20 prior negative controls remain covered.
  This note records the erratum's effect; it edits neither authority document nor
  the authenticated authority archive or private erratum.
- One mandatory seed query uses literal (0,1), including zero/all-empty descriptor
  branches. Only an infeasible seed returns None. A feasible seed's zero residual
  never bypasses initialization: make_pair(seed.c,seed.h), with NO Standard +1, is
  queried once. A zero initialization minimum returns that submitted pair and its
  current shore. A positive minimum, or None after a feasible seed, is RuntimeError.
- At a continuing negative state, Newton is the fresh make_pair(current.c,current.h).
  Require compare_pairs(newton,current_parameter)<0 before its query. Its minimum
  is nonpositive; a positive value is RuntimeError. Exact zero returns immediately,
  before reflection. Otherwise only closed pair_reflect(newton,current_parameter)
  forms (2*A*D-C*B,B*D), with Newton=(A,B), current=(C,D). Require the reflected point
  strictly below Newton before querying. No gcd reduction, rescaling, zero/sign
  repair, local reflection formula, or magnitude-controlled loop is introduced.
- Negative reflected residual accepts its queried pair AND reply; zero returns that
  exact queried pair and shore; positive is normal rejection, retaining the ALREADY
  QUERIED Newton pair AND Newton reply. Rejection adds no repeated Newton query and
  never substitutes the Newton reply's own fresh terms for the submitted pair.
  A separate compare_pairs(next_parameter,current_parameter)<0 guard precedes the
  entire state transfer. A positive REFLECTED residual is not Standard's sign fault.
  The common checked-query seam validates result/stat shape, finite original shore
  and raw B*c-A*h binding before any disposition. Dependency exceptions propagate
  unchanged; malformed replies and internal failures never become infeasibility.
- All three terminal sites preserve the submitted unreduced parameter and that
  query's returned shore, even when the shore's own (c,h) is a different raw pair.
  Legal argmins may produce different raw pairs, shores, counters, and trajectories
  while attaining the same numerical optimum. The wrapper adds no max-h, minimum-mask,
  cardinality, or diagnostic tie preference. The closed least-ORDINARY-cut requirement
  is unchanged; no least parity/branch shore is promised. Standard agreement is
  numerical plus independently checked domain membership and attainment, not raw
  pair/shore identity and not an independent substitute for source-domain minima.
- Accounting includes every normally returned seed, initialization, Newton and
  reflected query, including rejected and terminal look-ahead work. With p entered
  loop bodies and l reflected queries, a noninitial feasible completion has
  newton_queries=p>=1, oracle_calls=2+p+l and early_returns=1. A Newton-terminal run
  has l=p-1; a reflected-terminal run has l=p. Strict-negative acceptances a and
  positive rejections r satisfy a+r=p-1 in either case; reflected zero is neither.
  Infeasible counts are (1,0,0,0,0,0,0); initialization-root counts (2,0,0,0,0,0,0).
  All six additive oracle diagnostics sum, while the flow-only peak takes their
  maximum. These successful-run relations are tested, not constructor restrictions.
  Context preparation is once-paid; flow-only peak is not complete integer telemetry.

The following engineering crosswalk maps all 25 frozen Accelerated tests. AC23 is
additionally supported by the separate source-domain audit and executed mutations;
AC24's remaining staging/isolation/commit/remote-closure obligations are not yet complete.

| Production obligation | Principal tests in `tests/test_branch_accelerated.py` |
|---|---|
| AC1--AC2: exact combined surface; structural statistics, validation order, and Python arity | `test_exact_combined_public_surface_signatures_and_record_reuse`; `test_all_seven_valid_statistics_declarations_are_structural_only`; `test_all_73_registered_public_rejections_and_python_arity`; `test_statistics_validation_field_order_and_no_later_guard` |
| AC3: preservation of five complete Standard definitions and frozen compatibility bytes | `test_five_closed_definitions_and_compatibility_bytes_are_preserved` |
| AC7: independent original domains, shores, and all named optima | `test_original_domains_shores_and_all_named_optima_are_independent` |
| AC4--AC6/AC8--AC11/AC16: literal queries, closed arithmetic, seed and infeasibility, reflection and retained state | `test_all_112_named_actual_trajectories_closed_primitives_and_accounting`; `test_mandatory_seed_zero_and_both_descriptor_infeasibility_kinds`; `test_all_reflections_and_retained_transfers_match_literal_source_records` |
| AC12: submitted raw terminal pair and corresponding shore at all three return sites | `test_source_selected_raw_terminal_pair_traps_at_all_three_sites` |
| AC13: every registered legal argmin path, retained invariant, and no secondary preference | `test_all_51_named_legal_argmin_paths_and_no_secondary_preference`; `test_all_3099_core_legal_argmin_paths_without_shore_identity_constraints` |
| AC19: all 1,316 actual core branches, both solvers, and independent source minima | `test_all_1316_actual_core_branches_agree_with_standard_and_independent_minima` |
| AC7/AC8/AC20: fixed core census and stream fingerprints; explicit zero-reflection coverage boundary | `test_core_census_stream_fingerprints_and_zero_reflection_coverage_boundary` |
| AC14--AC15: guard-isolated malformed/None/sign seams and strict-progress failures | `test_all_45_guard_isolated_malformed_none_and_sign_seams`; `test_all_eight_strict_progress_fault_controls_before_later_queries` |
| AC16: all 12 diagnostic streams; sum-six/max-one aggregation without control effects | `test_all_12_diagnostic_streams_sum_six_max_one_without_control_effect` |
| AC17: original identity of all 16 registered dependency exceptions | `test_all_16_registered_dependency_exceptions_preserve_original_identity` |
| AC18: context preparation, interleaving, six reuse steps, labels, repeatability, and keyword calls | `test_context_preparation_interleaving_six_reuse_steps_and_no_graph_rescan`; `test_registered_labels_repeatability_and_keyword_interface` |
| AC20: 168 large graph solves with attempted-point bit checks; 49 separately classified abstract recurrences | `test_all_168_large_graph_solves_symbolic_traces_and_attempted_bit_bounds`; `test_all_49_abstract_scalar_recurrences_are_not_graph_coverage` |
| AC21--AC22: exact source and arithmetic ownership, preserved negative controls, and fresh-process isolation | `test_combined_source_guard_and_accelerated_only_arithmetic_ownership`; `test_legacy_20_negative_controls_and_standard_reflection_leaks_still_fail`; `test_fresh_process_combined_imports_resolve_only_to_candidate_tree` |

- The consuming file transcribes 31 committed tables / 9,167 literal rows fixed before
  production. It exercises 112 named actual solves, 51 named legal paths, all 3,099
  core legal paths, and all 1,316 actual core branch solves on 329 instances. Each
  feasible root and shore is checked against independently evaluated original domains
  and minima; the same core also executes Standard. This core has ZERO reflected
  queries. It is not advertised as look-ahead coverage. Named and large graph fixtures
  provide reflection coverage, including positive rejection and reflected termination.
- The 168 large graph solves and their symbolic trajectories are actual solver tests;
  the 49 abstract scalar recurrences are separate encoding controls, NOT 49 additional
  graph instances or a proof of DKNV. Public declarations (seven accepted-stat records,
  73 rejection/arity cases), 45 guarded query faults, eight strict-progress controls,
  12 diagnostic streams, and 16 dependency-exception declarations are nested checks,
  not additional collected pytest cases. The exact frozen file collects 25 cases.
- The separate implementation audit fixed source-domain optima and complete legal
  trajectories BEFORE importing production. It used neither consuming tests nor
  production answers to generate expectations. It executed 1,596 actual Accelerated
  solves / 3,376 queries: 1,316 core / 2,603 queries; 112 named / 279 queries; and
  168 large / 494 queries. All 1,316 Standard/core comparisons independently attain
  the source minima or agree on infeasibility. Named runs make 19 reflected queries
  (10 negative acceptances, seven positive rejections, two zero terminal returns);
  large runs make 57 (35 negative acceptances, 22 positive rejections). Core reflection
  count is zero. The audit replays 3,528 legal paths / 7,625 queries and adds 24
  diagnostic variants, 89 query faults, 12 operand-targeted comparator faults,
  16 dependency exceptions and 52 public rejections. These counts overlap consuming
  coverage and are not disjoint samples. All 26 compiled semantic mutants were rejected
  with the unmodified candidate passing; rejection was not based on lint or syntax.
- The live pre-CONFORMANCE GREEN checkpoint binds the frozen source and BOTH frozen
  tests to 25/25 Accelerated, 31/31 Standard and 553/553 full cases (497+31+25), with
  actual repository Ruff 0.16.5 preflight/full checks and the separate audit/mutations
  passing under Python 3.14.6 / pytest 9.1.1. Project-import origins and candidate-file
  nonmutation passed. The 37-file GREEN manifest describes the PRE-NOTE state. This
  documentation-only amendment changes only CONFORMANCE and creates a new manifest;
  it does not reinterpret a historical manifest as the post-amendment state.
- Source correctness bridge: on a nonempty finite domain with h>0, F(delta)=min(c-delta*h)
  is strictly decreasing with unique zero rho=min(c/h). Initialization delta=c0/h0>=rho
  has F<=0. At negative current residual, rho<=Newton<delta. A nonterminal reflected
  point lies below Newton: its negative minimum puts it above rho; its positive
  minimum puts it below rho and requires retention of the still-negative Newton state.
  Exact-zero queries terminate at rho. Thus retained states remain exact negative
  minima with matched parameter/shore and strict decrease (`prop:branch-invariant`).
  In the source's `prop:branch-correct` argument, concavity makes selected -h
  nondecreasing as parameters decrease. Equal active slopes represent the same
  effective affine function: at Newton it would be zero, while at an accepted
  reflection the previous active function is positive and cannot be the new negative
  minimum. Nonterminal retained slopes therefore strictly increase in a finite set,
  giving finite termination for any legal exact argmins. This is NOT a polynomial
  iteration-count argument and installs no slope-based tie selector or cutoff.
- Work bridge, separate from finite correctness tests: the pinned thm:DKNV invocation
  and thm:accelerated-bound supply p,t=O(M log M), M=n+m+1, with t=oracle_calls<=2+2*p
  on feasible branches. Closed Unit 12 gives O(t*(1+r_j*(n+3)^3*(m+n)^2)) integer/
  comparison operations, including empty descriptors and r_j=0; r_j counts families,
  not flows. Preparation separately pays O(n+m+R_all) once. The wrapper retains O(1)
  outer records and does O(1) operations per query beyond the oracle's workspace.
  The scoped thm:accelerated-bound row records this source-dependent composition;
  finite tests do not prove DKNV or the universal iteration bound. No guarantee
  of fewer calls than Standard on EVERY instance, constant bit time, constant byte
  memory, uniformly flat magnitude-sweep counters, or wall-clock speedup is inferred.
- Encoding bridge for lem:bitgrowth follows DESIGN 4.11.18. Let C=3Q+2, H=2Q+1 and
  P=max(abs(current.A),current.B). Fresh Newton terms satisfy abs(c)<=C and 1<=h<=H.
  A reflection's raw numerator is bounded by (2*C+H)*P, and its denominator by H*P;
  thus P_new<=(2*C+H)*P. Rejection resets retained state to the fresh Newton pair.
  After s consecutive reflections from a fresh point, attempted pairs, including
  rejected or terminal ones, satisfy max(abs(A),B)<=C*(2*C+H)^s. Encoding length grows
  additively per reflection, not by squaring two growing operands. At every query
  abs(raw)<=B*C+abs(A)*H. Comparison/reflection temporaries have the corresponding
  product/sum bounds; combine these with the closed oracle's capacities, recovery,
  O(n)-bit masks and zero-safe flow bounds, and the SOURCE iteration invocation above.
  This is the source-dependent polynomial-encoding composition. Test-local carrier
  checks remain finite evidence, not complete peak_integer_bits instrumentation,
  an empirical universal proof, or permitted production bit/iteration cutoffs.
- Historical Accelerated deferrals receive only the scoped evidence above. Unit 15
  still owns endpoint transforms, H2/unit-baseline combination, global selection,
  witness reconstruction, and the ruled Standard | Accelerated dual-route integration.
  Each future global witness must independently validate and attain the equal numerical
  value; different witnesses/raw quotients are permitted, and genuine Empty is separate.
  Global theorem rows, certificate construction/checking, full telemetry, CLI and the
  MPC experimental study remain unpromoted. No authority, catalogue, source, test,
  activation ledger, or historical evidence is changed by this note. Unit 14 still
  requires four-file candidate staging, exact index-tree isolation, atomic implementation
  commit, separate approved-hash remote closure, and the two private note blocks with
  conversational save confirmation. Private notes are never gate inputs.

## Unit 15 global composition and compact-witness implementation note

### Scope and historical-row boundary

This is the finite implementation crosswalk authorized by DESIGN 4.12 and TEST_PLAN
GL1--GL23 / section 36, after production R2 and frozen test R2 passed the live GREEN
and separate implementation audit. Every earlier byte, row and status is preserved.
In particular, the top-table `prop:global-invariant` and `thm:main` rows remain
`planned`, with their historical `tests/test_global.py` reservations unchanged.
Those reservations do not name executable Unit 15 tests: the actual file is
`tests/test_solve.py`; `tests/test_global.py` remains absent. The scoped evidence
below neither promotes those historical rows nor invents a new theorem label.
Earlier notes' deferrals describe their own checkpoints; they are not rewritten.

`exactfrac.solve.solve(instance, branch_solver)` implements `alg:global` under the
explicit exact-string selection `"Standard"` or `"Accelerated"`. It returns the
separate `(SolveResult, SolveStats)` records. Mathematical output is the literal
raw `ExactValue` and original `Witness(U,y)`, or `(0,1)` with None for genuine Empty.
The result is not a serialized certificate or an independent optimality proof.

### Source-referenced finite evidence (not top-table status changes)

| Governing source reference | Implemented and finitely tested scope | Actual frozen tests in `tests/test_solve.py` |
|---|---|---|
| `lem:empty` | The supported active Q=1 case returns literal `(0,1)` and None under both selections without preparing a context, building a witness, or invoking a branch. The earlier verifier-owned row remains unchanged. | `test_gl3_genuine_empty_constructs_no_graph_dependency`; `test_gl4_gl15_every_registered_input_both_real_routes` |
| `lem:unit` | Constructive baseline category priority, matching case, unit upgrade, independent admissibility, raw attainment and retention on ties on the registered inputs; no unattached bare-one incumbent. | `test_gl4_gl15_every_registered_input_both_real_routes`; `test_gl13_gl21_registry_fingerprints_and_core_definition`; `test_gl7_synthetic_source_prerequisite_failures` |
| `prop:endpoints`, `prop:branch-transform`, `sec:global` reconstruction passages | All four original endpoint recipes, zero H0 included, exact root-to-endpoint binding, original coordinates, and compact direct H2 with literal `(4,2)`. Finite reconstruction evidence is not another branch optimization or a proof of the endpoint theorem. | `test_gl4_gl15_every_registered_input_both_real_routes`; `test_gl9_scaled_roots_and_original_shore_binding`; `test_gl7_explicit_broken_dependency_promises` |
| `prop:global-invariant`, `alg:global` | One shared context; four selected branch calls in order; actual H2 construction/comparison; first strict numerical maximum retained with its corresponding witness. Instrumented candidate-by-candidate checks cover the registered trajectories. | `test_gl4_gl15_every_registered_input_both_real_routes`; `test_gl16_diagnostics_do_not_change_mathematical_choices`; `test_gl10_registered_comparison_traps` |

### Implemented composition and representation

For a nonempty original shore, write s=f(U), b=b_q(U), d=d_q(U)=2e_q(U)+b,
and Y=sum(y). Admissibility requires zero nonboundary coordinates, crossing counts
between zero and q_e, and odd s+Y>=3. The raw evaluator returns
N=2*(e_q(U)+Y), D=s+Y-1. Exact structural equality of records is not numerical
quotient equality; normalization and substitution of a branch root's scale are absent.

Public solve validation checks exact Instance type, then exact solver selection,
before graph access. Q=1 is the sole global shortcut. For Q>=2, one closed
BranchOracleContext retains the same Instance; the wrapper caches d_q once for its
vertex scans. The baseline chooses the first even-f vertex, otherwise the first
odd-f>=3 vertex, otherwise the first f=1 vertex of degree>=2. Category priority
precedes vertex index. The remaining case is a checked unit matching with at least
two edges; the smaller endpoints of the first two canonical edges form its shore.
The preliminary feasibility selection is upgraded: use all boundary copies when
s+b is odd, or all except one on the first crossing edge otherwise. The actual
admissible witness and its evaluated quotient, at least one, initialize retention.

The selected closed branch solver is called once for each j=0,1,2,3, including
infeasible branches. Its normally returned exact tuple, result type, selected stats
type, nonempty original-universe shore and source domain are checked. None means
branch infeasibility; it still contributes its original stats record. Production
trusts the closed branch minimum and does not enumerate shores or inspect families.
Each feasible endpoint is reconstructed and evaluated, even if losing or zero:

| Branch | Compact selection in canonical edge order | Literal raw `(N,D)` |
|---|---|---|
| L0 | all crossing copies | `(d+b, s+b-1)` |
| L1 | all crossing copies except one on the first crossing edge | `(d+b-2, s+b-2)` |
| H0 | all zero counts | `(d-b, s-1)` |
| H1 | one copy on the first crossing edge | `(d-b+2, s)` |

The returned branch root (A,B) is checked numerically against that endpoint:
A*(N-D)=B*D with N>D for L0/L1, and A*D=-B*N for H0/H1. The evaluator's literal
fields must first equal the source endpoint formula. Different unreduced terminal
root scales are allowed; unrelated root/shore pairs are rejected. Only the closed
compare_pairs on original raw endpoint values drives strict-improvement retention.
Value and witness update together; ties retain the first examined candidate without
a secondary key. Diagnostics and provenance strings do not control mathematics.

After all four branches, the first f(v)=1, cached d_q(v)>=2 vertex supplies H2.
A canonical support scan takes two copies without expanding multiplicity: either
one count 2 or two counts 1,1. It constructs and evaluates the actual Witness,
requires literal `(4,2)`, and performs the normal comparison even when dominated.
For such a singleton, s=1 and b=d>=2: even b gives an L0 endpoint of value two;
odd b>=3 gives a useful L1 endpoint of value two. Complete correct branch solves
therefore prevent a strict H2 win in this order. H2 construction, tie/losing
comparison and omission detection are tested; no impossible strict-winner graph
is claimed. A retained baseline remains a legitimate final witness.

SolveResult and SolveStats are frozen/slotted structural records, not provenance
certificates. SolveResult checks exact component types and literal `(0,1)` when
witness is None; with a Witness, standalone construction makes no instance-dependent
admissibility/attainment assertion. Successful nonempty solves retain four original
selected-type diagnostics by identity; Empty has (). SolveStats construction does
not impose successful-run equations. Supported malformed public inputs raise exact
ValueError. Consumer-detected broken dependency promises raise RuntimeError; exceptions
raised by dependencies propagate unchanged, without fallback or partial success.
Constructor-bypassing forgeries are outside the adopted contract.

### Complete frozen-test engineering crosswalk

These 16 top-level test functions collect 625 parametrized cases in the authenticated
live run. The following mappings are engineering obligations, not new theorem rows.

| Unit 15 obligations | Principal frozen tests in `tests/test_solve.py` |
|---|---|
| GL1--GL2: exact interface, immutable structural records, public rejection and arity | `test_gl1_public_surface_and_record_contracts`; `test_gl1_gl2_registered_exact_public_rejections` |
| GL3: genuine Empty and dependency-free shortcut | `test_gl3_genuine_empty_constructs_no_graph_dependency` |
| GL4--GL6/GL8/GL10--GL15/GL20: shared context, constructive baseline, complete selected traversal, every original endpoint, retained invariant and dual-route optimum checks | `test_gl4_gl15_every_registered_input_both_real_routes` |
| GL13/GL21: independently fixed registered inputs, table fingerprints, baseline/H2/winner categories | `test_gl13_gl21_registry_fingerprints_and_core_definition` |
| GL9: raw-scale freedom, original shore and numerical root binding | `test_gl9_scaled_roots_and_original_shore_binding` |
| GL7: exact returned shapes/types, source prerequisites and explicit internal faults | `test_gl7_explicit_broken_dependency_promises`; `test_gl7_additional_exact_reply_shapes`; `test_gl7_synthetic_source_prerequisite_failures` |
| GL16: retained diagnostics, noncertifying constructors and mathematical independence | `test_gl16_standalone_diagnostics_have_no_history_equations`; `test_gl16_diagnostics_do_not_change_mathematical_choices` |
| GL17: original dependency-exception identity at the exercised boundaries | `test_gl17_dependency_exceptions_propagate_by_identity` |
| GL18: repetition, interleaving, labels and immutable input state | `test_gl18_repetition_interleaving_labels_and_no_mutable_aliases` |
| GL10: exact numerical comparator traps, separately from actual graph choices | `test_gl10_registered_comparison_traps` |
| GL19: permitted imports, exact arithmetic, compact source structure and fresh-process provenance | `test_gl19_direct_import_exactness_and_compact_source_controls`; `test_gl19_fresh_process_direct_import_isolation` |
| GL22--GL23: separate implementation/mutation audit and narrowly scoped documentation | The private definition-level audit and executed controls described below, plus this source/test/evidence crosswalk; neither is an additional collected pytest case. |

Every one of the 379 registered inputs (329 core, 22 named/labelled, 28 magnitude)
runs through both real selections in the consuming corpus test. Instrumentation
checks intermediate and final witnesses using only primitive data transferred to
the unchanged solver-blind verifier. Raw attainment is checked separately for each
run; numerical endpoint values must agree across selections. Equal witness objects
or equal unreduced pairs across selections are not required. The 351 tiny entries
are compared with independently exhaustive optima. The 28 large entries use the
preimplementation exact symbolic endpoint bounds and attaining constructions, not
multiplicity-sized brute force or route agreement as an optimality proof. Synthetic
fault injections and pure comparator controls are not additional graph instances.

### Separate audit and authenticated live GREEN

The separate audit imports no consuming test to derive its definition-level answers;
it parses the committed preimplementation human tables and checks primitives with
the closed independent verifier. It reports 379 paired inputs / 758 real global
calls: two Empty and 756 nonempty runs. The nonempty runs make 3,024 selected branch
calls, with 2,560 feasible endpoints and 464 infeasible replies. It observes 756
baseline candidates, 510 direct H2 candidates and 3,070 endpoint comparisons, and
performs 4,582 independent raw-witness checks. These categories overlap consuming
coverage; neither audit calls nor nested observations are collected pytest counts.

All 25 preregistered mutations were executed in private exports. Each selected
frozen detector first passed on unmodified R2, then failed in a test body on its
controlled variant with identical collected case identities. Import, collection,
syntax, setup, skip and xfail failures do not qualify as detection. Twenty-four
controls are behavioural; the magnitude-expansion variant is detected by an executed
AST/source-structure test, without attempting a large explicit-copy expansion.
The controls cover omitted branches/H2, wrong selection/preparation, baseline and
tie errors, root/endpoint or lexicographic/float comparison, raw rescaling, stale
witnesses, invalid compact counts, original-coordinate errors, diagnostic influence,
and omitted zero H0 evaluation. Detection of these finite variants is not a proof
of defect absence or a test of every possible incorrect implementation.

The pre-CONFORMANCE live R2 GREEN run reports 625 collected/passing targeted cases
and 1,178 collected/passing full cases: the unchanged 553-case baseline plus the
actual 625 new cases. Live production preflight and repository Ruff 0.16.5 passed
under Python 3.14.6 / pytest 9.1.1, as did import provenance, the separate audit and
all mutation detectors. Its exact production SHA-256 is
`03ade830010ca0aabd69c4fdb961d68dbc2d44108d7217d831e7b1672d2f85bc`;
the frozen test SHA-256 is
`a252300164d727e6e415ae0545583477fb24cea3d81063f2d81df991381d1a5c`.
The 37-file GREEN ledger describes the committed base BEFORE this CONFORMANCE
amendment; source and test were two additional untracked files. This documentation
step does not reinterpret that earlier ledger as the post-amendment state.

### Source-dependent correctness, work and encoding boundary

`prop:endpoints` and `prop:branch-transform` provide the global reduction, not the
agreement of two consumers of a shared oracle. `lem:empty` and `lem:unit` supply
Empty and the constructive unit bound. Each closed solver supplies its own exact
branch minimum; useful-L1 exclusion of value-one endpoints is harmless against that
baseline. Correct reconstruction and strict maximum retention give the source's
`prop:global-invariant`. Adding the direct H2 scan completes `alg:global`.
This is the source-to-code correctness chain for `thm:main`, not a universal theorem
proved by the finite corpus, a second optimization in the wrapper, or an independent
global-optimality certificate obtained by merely checking the returned witness.

Under DESIGN 4.12.13, let M=n+m+1, K=(n+3)^3*(m+n)^2, and r_j be branch-cover sizes
for analysis only. Preparation costs O(n+m+R_all) once. The fixed number of wrapper
vertex/support scans and witness reconstructions contributes O(n+m); the full
integer/comparison-operation carrier is
O(n+m+R_all+sum_j t_j*(1+r_j*K)). The source supplies t_j=O(M log M) for Accelerated
and t_j=O(M^2 log M) for Standard. `thm:main` uses the accelerated chain; the Standard
alternative inherits `cor:standard-strong`, not the accelerated factor. Finite tests
prove neither source invocation nor universal strong polynomiality. No magnitude
cutoff, empirical flat-counter claim or guaranteed per-instance speedup is inferred.

For an admissible compact witness, e_q(U)+Y<=Q and f(U)+Y<=2Q, giving
0<=N<=2Q and 2<=D<=2Q-1. Endpoint comparison products have input-polynomial encoding.
Root-binding products additionally inherit the selected branch solver's parameter
bit-growth bound: an unreduced Accelerated terminal root need not have the witness's
raw scale. Bounded retained candidate/diagnostic records plus O(n+m) wrapper workspace
sit beyond the prepared context and closed oracle workspace. These are source-based
carriers, not constant byte space, constant bit time, complete peak telemetry, or
wall-clock guarantees established by the observed test counts.

Full telemetry, certificate construction/serialization, the independent checker,
CLI, expanded corpus/experiments and release remain later units. This note does not
claim staged-tree isolation, an implementation commit, or Unit 15 remote closure.
Those follow the separate complete-candidate staging, index-tree isolation,
postcommit checks and approved-hash push/closure steps. Source, frozen test, every
other governing document and every earlier CONFORMANCE row/status remain unchanged
by this documentation-only amendment.

## Unit 16 exact telemetry — finite implementation and engineering crosswalk

### Basis, status and preservation boundary

This appendix records the implemented engineering scope of DESIGN 4.13 and
TEST_PLAN TE1--TE23 / section 38, after the live implementation R2 GREEN gate.
Every prior byte, theorem row, status and explanatory note above is preserved.
In particular, the historical `prop:branch-invariant`, `prop:global-invariant`
and `thm:main` planned rows are not promoted or rewritten. No new theorem label
is invented. Earlier telemetry deferrals describe their historical checkpoints;
this separately scoped appendix records the present implementation evidence.

The source remains the V2.2 mathematical specification pinned in SPEC_LOCK.
Its work/encoding claims supply the mathematical context, not the Python record
interfaces. The corrected source-derived manifest traverses `Call.args` and
excludes signature `args` only by callable owner type. The existing 333 scalar
IDs and 25 iterator entries remain historical; the effective inventory has
102 functions, 366 scalar occurrences and 27 iterator sites, including the
33 appended scalar classifications and two coefficient-generator iterators.
The current consumers recognize 237 required direct observations and 25
post-store observations. These are static obligations, not execution counts.

The accepted GREEN candidate adds `exactfrac/_telemetry.py` and
`exactfrac/telemetry.py`. Exactly ten older modules have authorized erasable
recording additions: instance, shore, families, witness, rational, sign_routing,
parity_cut, flow, oracle and solve. Their source bytes DID change; removing only
the ruled observation imports/taps/events/scopes recovers their mathematical ASTs.
`branch.py`, the independent verifier, package roots, and unruled paths retain
their original bytes. The eleven legacy test adapters contain only the 17
registered recipes. Their immutable 27-file JSON reference is parsed comparison
data, never executed. No rolling hash replaces an original historical identity.

### Implemented surface and measurement meaning

`solve_with_telemetry(instance, branch_solver)` validates an exact Instance and
exact selection `Standard` or `Accelerated`, calls the existing global solve once,
and returns its exact SolveResult object with AlgorithmStats retaining the exact
native SolveStats object. Legacy solver signatures, native diagnostics, raw
witness values, first-encountered tie handling and result semantics are preserved.
The new immutable in-memory records are WorkStats, BranchTelemetry, AlgorithmStats,
RunMetadata and RunRecord; there are no package-root re-exports or implicit defaults.
Their validators check shape and local consistency, not that a claimed run occurred.

All four branches, including infeasible/losing ones, retain their own records.
Nonbranch arithmetic includes input values, the constructive baseline, candidate
comparison and direct H2 reconstruction; Empty has no fake branch execution.
Standard newton_updates and Accelerated newton_queries retain distinct native
meanings. The common newton_candidates event is defined explicitly; accepted,
rejected and terminal look-aheads remain separate, and initialization termination
is not an early in-loop return. Prepared-cover cardinality is recorded once;
repeated examinations and cut/flow calls are not recomputed by replaying work.
The first 20 WorkStats fields aggregate by sum; its five magnitude/bit fields
aggregate by maximum, with native field meanings preserved.

Scalar bits use max(1, abs(x).bit_length()); zero has one bit. A zero flow value
is not absent flow. Raw numerator/denominator peaks are distinct from output bit
sizes and from the complete measured integer peak. Cancelling products, rejected
or discarded intermediates, masks, capacities, residuals and executed dominance
carriers are covered in their specified scopes. Display labels and recording
bookkeeping do not enter the mathematical peak. No gcd normalization, float
comparison, tolerance or magnitude-based optimizer cutoff is introduced.

At the two registered D-ITER coefficient-generator sites, the candidate places
`_observe_ints(instance.n)` immediately before the top-level `if branch < 2` in
branch_coefficients, in the same scope. Both generators keep `range(instance.n)`.
The frozen checker accepts the exact preceding statement as well as the original
inline form; exact operand/path/binder, unconditional placement and non-reassignment
requirements remain. Controls reject after-generator and opposite-branch events,
a different operand, intervening reassignment, scope changes and extra evaluation.
The valid statement variant also satisfies the unchanged structural-loop guard.

Recording decisions do not feed mathematical branch/loop/comparison decisions.
Leaf taps preserve object identity, and context-local cleanup is exercised for
normal, rejected-nested, exceptional and separate-thread runs. Metadata values,
including wall_clock_s, are supplied externally and remain separate from AlgorithmStats.
Constructors do not discover clocks, CPUs, files, Git versions or instance hashes.
No wire format, timing campaign or certificate field is implemented here.

### Actual frozen tests and finite scope

Every row below names an existing top-level function in the frozen
`tests/test_telemetry.py`; all 39 functions are represented. Their parametrization
collected 809 live targeted cases. Together with the unchanged identities of
1,178 legacy cases, the full live suite collected and passed 1,987 cases. Case
counts are not counts of solver calls, source sites, or mathematical theorems.
All rows are green only for the executed finite assertions described here.

| Engineering obligations (TEST_PLAN 37) | Actual frozen discharging test | Finite scope | Status |
|---|---|---|---|
| TE2, TE8, TE23 | `tests/test_telemetry.py::test_te02_te08_all_registered_inputs_both_real_routes` | Both routes on the 389-input registry; one legacy call, exact result/native identity, repeats and independent raw-witness checks. | green |
| TE1 | `tests/test_telemetry.py::test_te01_exact_record_layout_required_arguments_and_immutability` | Required record fields and entry signature; frozen/slots, no ordering, and argument-shape rejection. | green |
| TE1, TE8, TE20 | `tests/test_telemetry.py::test_te01_te08_te20_all_registered_rejections` | All catalogue public-data/signature rejection cases with exact exception types. | green |
| TE1 | `tests/test_telemetry.py::test_te01_public_validation_precedes_all_graph_access` | Public argument rejection precedes solver invocation and graph access. | green |
| TE3, TE4, TE5, TE6, TE7 | `tests/test_telemetry.py::test_te03_te07_registered_real_traces_and_all_native_fields` | Registered real query trajectories, native event fields and labelled backend measurements. | green |
| TE9 | `tests/test_telemetry.py::test_te09_integer_tap_bit_convention_and_identity` | Zero-safe scalar bit convention, tap identity and recorded nonbranch maxima. | green |
| TE9, TE14 | `tests/test_telemetry.py::test_te09_te14_raw_pair_streams_and_no_normalization` | Raw-pair streams, separate numerator/denominator peaks and unreduced scale. | green |
| TE11 | `tests/test_telemetry.py::test_te11_real_rational_operations_observe_cancelling_products` | Real residual/reflection/comparison primitives observe cancelling products. | green |
| TE12 | `tests/test_telemetry.py::test_te12_signed_prefixes_and_executed_dominance` | Signed prefix observations and the limited executed nonnegative-sum dominance argument. | green |
| TE7, TE13 | `tests/test_telemetry.py::test_te07_te13_local_flow_definition_and_numeric_measurement` | Local flow fixtures: value, shore, augmentations, scans, generated peaks and injected-call scope. | green |
| TE13 | `tests/test_telemetry.py::test_te13_local_reduced_coordinates_and_masks` | Local reduction coordinates, terminal masks and original/reduced universe observations. | green |
| TE7, TE9 | `tests/test_telemetry.py::test_te09_synthetic_zero_flow_and_aggregate_construction` | Sum-versus-maximum aggregation and zero-valued flow versus absent flow. | green |
| TE13 | `tests/test_telemetry.py::test_te13_huge_labels_do_not_enter_algorithm_statistics` | Huge display labels do not alter the deterministic algorithm statistics. | green |
| TE15 | `tests/test_telemetry.py::test_te15_injected_numeric_maximum_cannot_change_mathematical_decisions` | Injected recorded maxima cannot change the mathematical result or native decisions. | green |
| TE16 | `tests/test_telemetry.py::test_te16_nested_rejection_before_second_call_and_successive_cleanup` | Nested measured calls rejected before a second solve; successive measurements clean up. | green |
| TE16 | `tests/test_telemetry.py::test_te16_dependency_exception_identity_and_recorder_cleanup` | Entry/oracle/recorder failures preserve the exception object and restore the recording context. | green |
| TE16 | `tests/test_telemetry.py::test_te16_separate_thread_measurements_have_disjoint_state` | Independent thread jobs and subsequent reruns produce disjoint, repeatable measurements. | green |
| TE10, TE17, TE18 | `tests/test_telemetry.py::test_te17_te18_complete_source_erasure_and_exact_legacy_adapters` | Complete source erasure, 237 direct/25 post-store sites, 17 recipes, 27 references and frozen branch bytes. | green |
| TE17 | `tests/test_telemetry.py::test_te17_erasure_rejects_controlled_source_faults` | Erasure rejects comparison edits, extra evaluation, omitted scalar taps and arbitrary imports. | green |
| TE18 | `tests/test_telemetry.py::test_te18_test_delta_checker_rejects_changed_math_and_changed_historical_hash` | Exact adapter reconstruction rejects widened dependencies and altered historical-hash guards. | green |
| TE19 | `tests/test_telemetry.py::test_te19_leaf_import_isolation_and_no_runtime_source_tools` | Fresh leaf-only import, allowed dependencies and absence of runtime source/profiling/clock tools. | green |
| TE20 | `tests/test_telemetry.py::test_te20_metadata_is_supplied_not_discovered` | Explicit metadata and record construction; no discovery calls or AlgorithmStats contamination. | green |
| TE10, TE21, TE22 | `tests/test_telemetry.py::test_te10_te21_te22_manifest_registry_and_no_new_math` | Manifest/registry identities, static wrapper restrictions and unchanged branch mathematics. | green |
| TE11 | `tests/test_telemetry.py::test_te11_all_literal_arithmetic_streams_against_leaf` | Every literal arithmetic-stream fixture exercises leaf observations with independently listed results. | green |
| TE4, TE5 | `tests/test_telemetry.py::test_te04_te05_abstract_scalar_streams_drive_actual_mapper` | Abstract scalar oracle streams drive the real branch recurrences and actual event mapping. | green |
| TE3, TE6 | `tests/test_telemetry.py::test_te03_te06_branch_ownership_and_preparation_observation` | Branch ownership, one preparation and actual prepared-cover observations. | green |
| TE3, TE8 | `tests/test_telemetry.py::test_te03_baseline_h2_and_zero_h0_are_really_measured` | Baseline, direct H2 and feasible zero-valued H0 measurements are reached and retained correctly. | green |
| TE15 | `tests/test_telemetry.py::test_te15_disabled_taps_and_record_bookkeeping_do_not_enter_math_peak` | Disabled tap identity and exclusion of recording bookkeeping from mathematical peaks. | green |
| TE16 | `tests/test_telemetry.py::test_te16_normally_returned_invalid_dependency_records_fail_closed` | Normally returned malformed dependency records fail closed rather than produce partial success. | green |
| TE7, TE9 | `tests/test_telemetry.py::test_te07_te09_zero_terminal_performs_no_ordinary_cut` | Zero-terminal execution makes no ordinary cut and preserves zero/absence distinctions. | green |
| TE10 | `tests/test_telemetry.py::test_te10_manifest_rule_manual_syntax_fixtures` | Manual syntax fixtures establish the typed callable-signature exclusion rule. | green |
| TE10 | `tests/test_telemetry.py::test_te10_corrected_inventory_is_complete_from_authenticated_source` | Effective corrected inventory is discovered from authenticated source before manifest comparison. | green |
| TE10 | `tests/test_telemetry.py::test_te10_completeness_rejects_each_added_scalar_omission` | Each of the 33 appended scalar classifications is individually omission-sensitive. | green |
| TE10 | `tests/test_telemetry.py::test_te10_completeness_rejects_each_added_iterator_omission` | Each of the two appended iterator occurrences is individually omission-sensitive. | green |
| TE10 | `tests/test_telemetry.py::test_te10_completeness_rejects_self_consistent_but_incomplete_tables` | Self-consistent incomplete, duplicated and substituted manifest tables are rejected. | green |
| TE10 | `tests/test_telemetry.py::test_te10_rule_fixture_detects_untyped_args_exclusion` | The syntax fixture detects blanket args-field exclusion, including skipped Call.args. | green |
| TE17 | `tests/test_telemetry.py::test_te17_diter_exact_inline_and_preceding_statement_forms` | Inline, exact preceding statement and combined/mixed forms remain accepted at the two D-ITER sites. | green |
| TE17 | `tests/test_telemetry.py::test_te17_diter_statement_rejects_wrong_placement_operand_scope_and_reassignment` | After-use, opposite-branch, different-operand, reassignment, scope and extra-evaluation forms are rejected. | green |
| TE17 | `tests/test_telemetry.py::test_te17_diter_statement_cannot_discharge_another_registered_site` | The statement alternative cannot discharge a different module/function/path/operand/binder obligation. | green |

### Separate independent execution and mutation evidence

The implementation audit runs the 389 registered inputs under both selections:
778 measured global solves, comprising four Empty runs and 774 nonempty runs.
It checks all 3,096 nonempty-run branch records and all 389 cross-route numerical
pairs. Same-route original raw result, witness and native diagnostics agree with
778 uninstrumented original-source calls. Across selections only numerical value
agreement is required; tied witness objects or unreduced pairs need not coincide.
Each of the 774 nonempty witnesses independently passes admissibility and literal
raw-attainment evaluation under the unchanged verifier; direct compact-definition
arithmetic supplies an additional 774 raw checks. These checks are not an
independently checkable global-optimality certificate.

A separate original-source observation transform performs 778 reference calls.
It neither imports production telemetry nor uses candidate outputs/tap placement
as expected peaks. The reference checks scoped integer and raw-pair peaks against
the candidate using its own bin-string bit computation. Manifest cover tables and
native diagnostic comparisons provide separate event-count evidence. Agreement
is finite corroboration, not proof that all possible execution paths were sampled.
The candidate/reference row digest recorded by the audit is:
`9934255109b1304b45f3913f926f261ff716e21a174c1582089e1d594706e323`.

All 30 preregistered fault variants were executed in private copies and detected:
21 behavioural, eight structural, one manifest-static. Each detector first passed
on the unmodified candidate. Import, collection, setup, skip and syntax failures
do not qualify as behavioural kills. Coverage includes output-only/flow-only
peaks, omitted products and arithmetic epochs, invalid dominance, count/peak
aggregation reversal, terminal-event errors, preparation/branch omissions,
normalization, feedback, leakage, nesting, metadata contamination, extra solve,
cover replay, source/guard changes, expanded-copy work and returned-object identity.
These are the implementation audit's 30 executed mutations, not the separate
56 source-rule or 21 bound-recognition controls.

The independent auditor is byte-identical to its R1 version and retains its R1
report label; the authenticated execution here is implementation R2. Both the
full and targeted live runs preserved project import provenance. All twelve
candidate live Ruff preflights and the final repository Ruff passed. Saved
execution evidence is private handoff material, not newly committed source.

### Artifact bindings and limits of this appendix

Accepted implementation package:
`ExactFrac_UNIT16_IMPLEMENTATION_R2_PRO_AUDITED_PACKAGE.zip`
SHA-256: `edddc154209f4ce42252e8db8bfa6fa181535ce112069ae972cd42987559bbed`.
The implementation-only patch has 1,529 lines and SHA-256
`59e1bb6a0ee701c51b7b607cfd4ad0e7ae82c116c9581b3a8f7092a206aa794f`.

| Bound artifact | SHA-256 |
|---|---|
| exactfrac/telemetry.py | aadcbcd00fae3eba9e61a8433b90dae47ab0e67e91fa911cf57d909cef249bd3 |
| exactfrac/_telemetry.py | 3be3cae6757db921aacdde7fbae2cb59cfa1b91b73bd9c16c0695a1f620b9cac |
| exactfrac/branch.py (unchanged) | 584d2f262c94e227f3832563aeceff600c95c6943b0401bd8ef64e3c2a5ef057 |
| tests/test_telemetry.py | a009f6e6052bf386793791a67a7973581c466968465d0d562eb5d4811096f94b |
| tests/_telemetry_source_audit.py | 7d737818adfb193c8335a123b4fdc38735260dd0006c4a0cdb9b5def945e1d77 |
| tests/fixtures/unit16_legacy_sources.json | e81ba1aac48412d7b9e85bb493d1edef1f98e6788d3ef67070b4a9ae21993136 |
| GREEN_CHECKPOINT.txt | 71cb460367618db2af2ee36ec62214271fe2ac88b7abc2402fc08b0a9e841eaf |
| GREEN_AUDIT.json | d5ce342230326713c06672076f03ede78a8dc897387ea7c0c9f7106040f1ca83 |
| Independent implementation report | 77ce145b86c62bc9e93083fcc57a2acc0a32fbf7814d7c596ea1667b8a21de72 |
| Executed mutation record | 9bde75745f78c66df53ad26ff6d8ddd0474fa750cce617b65d2b511f17ff561f |

The governing source's selected-solver work factors remain distinct: Standard
O(M^2 log M), Accelerated O(M log M), within their documented operation carriers.
Finite telemetry tests do not prove those theorems, universally flat trajectories,
end-to-end bit complexity, elapsed-time scalability, or constant byte-space usage.
Instrumentation and Python bit-operation costs require separate reporting.
Full peak claims refer to the ruled measured execution and observation universe,
not arbitrary interpreter internals or unexecuted paths.

Certificate construction/checking, CLI, benchmark corpus, experiments and release
remain later units. No benchmark result, certificate of global optimality, whole-
input timing or public release is promoted here. Unit 16 still requires the
reviewed complete candidate to be staged, tested from its exact Git index tree,
committed and separately remotely closed. This appendix changes only CONFORMANCE;
it does not stage, commit, push, or alter a production/test/fixture identity.


## Unit 17 certificate construction and exact serialization — finite conformance

### Basis, status and historical preservation

This appendix records the finite implementation scope of DESIGN 4.14 and
TEST_PLAN CE1--CE20 / section 40 after the live implementation R2 GREEN gate.
Every preceding byte, theorem row, status and explanatory note is preserved.
In particular `prop:branch-invariant`, `prop:global-invariant` and `thm:main`
remain planned in the historical top table. No new theorem-label row is invented
for the JSON codec, and no earlier historical deferral is retrospectively edited.
Earlier certificate deferrals describe their own checkpoints; this appendix
records the now-tested Unit 17 construction/serialization boundary only.

Authority was remotely closed at
`2cc8bd16287a3ec6a192c4f0b9249ded73484b99`; the independent oracle catalogue was
remotely closed at `e68ea1cd3cf4e47645e90d0f14011290aba4bd4c` before the consuming
test and production implementation. The governing mathematics remains the V2.2
source pinned in SPEC_LOCK, not a reconstructed interface or earlier snapshot.
The current candidate is the 160-line production R2 `exactfrac/certificate.py`
and the byte-frozen R2 `tests/test_certificate.py`.

The live targeted run collected and passed 458 cases. The full run collected
and passed 2,445 cases, equal to the 1,987-case inherited baseline plus those
458 cases. Neither run reported collection errors, deselections or xfails;
all setup, call and teardown reports passed. Candidate production Ruff and
full repository Ruff passed on Python 3.14.6 / pytest 9.1.1 / ruff 0.16.5.
These are authenticated live GREEN results, not detached results substituted
for the Mac gate, and not the 31 top-level test functions counted as cases.

### Implemented object and byte boundary

The exact public surface is `build_certificate(instance, result)` returning a
detached `dict[str, object]` and `serialize_certificate(instance, certificate)`
returning exact `bytes`. Both require a normally constructed exact canonical
active Instance. The builder requires an exact SolveResult, whose only fields
remain value and witness; an outer result/stats pair is not an accepted input.
Constructor-bypassing forgeries and concurrent mutation during one synchronous
call are outside the adopted closed-record/object contract.

For a nonempty certificate, the original-coordinate U is a strictly increasing
vertex-index list; y is a sparse strictly increasing list of [edge_ref, positive
count] pairs, with omitted coordinates zero. References resolve by the canonical
instance edge order, never optional labels, packed sparse positions or auxiliary
cut coordinates. The reused closed helpers establish boundary membership and
capacity, nonempty U, odd s+Y and s+Y >= 3, where s=f(U), Y=sum(y_e), and e=e_q(U).
The certificate then preserves the LITERAL fields N=2*(e+Y) and D=s+Y-1.
Numerical equality after reducing or rescaling N/D is not literal attainment.
This is finite implementation evidence for the def:parameter / eq:compact-density
conditions, not an independently checkable certificate of global optimality.

Genuine Empty requires Q==1 under the active-instance hypotheses of lem:empty,
literal (N,D)=(0,1), and no U/y fields. A Witness selects the nonempty case even
when its numerator is zero or sparse y is empty. Valid suboptimal witnesses,
local candidates that lost a solver comparison, and the nonempty raw (0,2)
fixture remain accepted. No branch membership, provenance label, density >=1,
secondary tie key, alternate witness search or extra optimizer call is required.

The format tag is exactly "exactfrac-certificate/1". Nonempty output order is
format, empty, N, D, U, y; Empty order is format, empty, N, D. Missing/extra fields,
wrong exact types and additional envelopes are rejected. There is no digest,
embedded instance, stats, telemetry, time, environment or branch field. Bytes
use literal ASCII (a UTF-8 subset), unquoted decimal integer tokens, no spaces,
no BOM, and exactly one final LF. Input dict key order is immaterial; this does
not authorize sorting, merging or repairing U/y. Builder outputs and nested
lists are detached, and the serializer revalidates current content on every call.

Public invalid data raises exact ValueError; explicitly checked normal-return
helper-promise violations raise RuntimeError; raised dependency exceptions retain
identity. The nine-digit private decimal codec uses bounded conversions rather
than whole-magnitude str conversion or a process-global cutoff change. Its
4,801-digit fixtures pass under enabled limits 4,300 and 640 and hash seeds 1
and 73. Injected resource exceptions are not converted into Empty or success.
These checks neither exhaust memory nor certify denial-of-service resistance.

### Complete frozen-test engineering crosswalk

Each row identifies an actual top-level function in the frozen consuming file.
"green" means the stated finite test obligations passed; it is not a new
mathematical theorem status or a declaration that Unit 17 is remotely closed.
Parametrizations and loops are distinguished from function counts.

| TEST_PLAN obligations | Frozen test | Finite exercised scope | Status |
|---|---|---|---|
| CE9, CE12, CE18 | `tests/test_certificate.py::test_closed_fixture_authority_and_registry_identity` | Fixed table digests, literal recipes and all 396 registered entry identities; no mathematical-input deduplication. | green |
| CE1, CE20 | `tests/test_certificate.py::test_exact_public_surface_and_closed_record_ownership` | Exactly the two ruled APIs/signatures; unchanged SolveResult fields, empty package roots and absent production checker. | green |
| CE2, CE3, CE5--CE9 | `tests/test_certificate.py::test_literal_bytes_and_detached_record_construction` | All 31 literal fixtures; exact schema/raw fields, detached nested exports, valid Empty/nonempty zero, original coordinates and rejection after mutation. | green |
| CE3, CE9, CE14 | `tests/test_certificate.py::test_repeated_and_reordered_object_serialization` | Repeated inputs and reordered dict keys yield the same fixed bytes without repairing witness coordinates. | green |
| CE8, CE10, CE11 | `tests/test_certificate.py::test_independent_malformed_wire_rejections` | All 140 preregistered raw-byte rejections in the test-only independent route, including equal-ratio raw forgeries. | green |
| CE10, CE11 | `tests/test_certificate.py::test_independent_instance_wire_variants` | Seven accepted instance-wire variants preserve validated canonical graph data; certificate bytes remain exact. | green |
| CE4, CE7, CE8 | `tests/test_certificate.py::test_serializer_rejects_registered_object_corruptions` | Only object-semantic corruptions are assigned to the production serializer, separately from raw lexical rejection. | green |
| CE1--CE5, CE7, CE8 | `tests/test_certificate.py::test_registered_exact_type_and_normal_record_rejections` | The 62 registered object-boundary cases reject unsupported types/records, envelopes and invalid normally constructed claims. | green |
| CE7, CE16 | `tests/test_certificate.py::test_registered_normal_return_promise_faults` | All ten declared normal-return type/shape violations are classified as RuntimeError rather than caller-data rejection. | green |
| CE16 | `tests/test_certificate.py::test_registered_dependency_exception_identity` | All 35 dependency-exception cases preserve the actual raised object, including operational resource failures. | green |
| CE2, CE4, CE16 | `tests/test_certificate.py::test_instance_guard_precedes_every_other_read` | Exact Instance guard precedes other argument or dependency reads. | green |
| CE2, CE16 | `tests/test_certificate.py::test_builder_exact_result_guard_precedes_dependencies` | Exact SolveResult guard precedes evaluator/export dependencies. | green |
| CE5, CE16 | `tests/test_certificate.py::test_empty_paths_invoke_no_witness_helpers` | Genuine/false Empty paths use their ruled validation without manufacturing a witness. | green |
| CE4, CE16 | `tests/test_certificate.py::test_serializer_header_guards_precede_payload_helpers` | Case-specific headers and integer fields are rejected before payload conversion. | green |
| CE4, CE7, CE16 | `tests/test_certificate.py::test_shore_validation_precedes_sparse_decoding` | Invalid U is rejected before sparse-y decoding. | green |
| CE4, CE7, CE16 | `tests/test_certificate.py::test_sparse_validation_precedes_witness_construction` | Sparse-y rejection precedes Witness construction and evaluation. | green |
| CE2, CE4, CE8, CE16 | `tests/test_certificate.py::test_raw_mismatch_does_not_bypass_closed_evaluation` | Closed admissibility/evaluation is not bypassed by a supplied raw-pair mismatch. | green |
| CE2, CE8, CE16 | `tests/test_certificate.py::test_builder_raw_rejection_precedes_exports` | The builder rejects literal mismatch before export helpers. | green |
| CE2, CE4, CE16 | `tests/test_certificate.py::test_declared_helper_call_order_and_single_consumption` | The declared evaluator/conversion sequence and single consumption of normal helper outputs are exercised. | green |
| CE4, CE16 | `tests/test_certificate.py::test_mutation_after_build_is_revalidated` | Later serialization validates current caller-owned content rather than cached/provenance-based approval. | green |
| CE6, CE8, CE14, CE17 | `tests/test_certificate.py::test_tied_raw_scales_remain_distinct_without_optimization` | Legitimate tied witnesses retain different raw scales and bytes; no optimizer is invoked to force equality. | green |
| CE6 | `tests/test_certificate.py::test_suboptimal_local_attainment_is_sufficient` | Admissible suboptimal and zero-valued fixtures need not be global winners or have density at least one. | green |
| CE5--CE10, CE12--CE14, CE17 | `tests/test_certificate.py::test_every_registered_identity_both_routes_and_local_reconstructions` | All 792 actual final solves, own-run raw-pair binding, 396 numerical route comparisons, all endpoint origins and both direct-H2 shapes. | green |
| CE14, CE17 | `tests/test_certificate.py::test_legacy_and_measured_results_serialize_the_same` | Selected legacy/telemetry result pairs emit the same bytes while diagnostic objects remain separate. | green |
| CE7, CE14, CE15, CE17 | `tests/test_certificate.py::test_labels_diagnostics_and_interleaved_calls_do_not_enter_bytes` | Optional labels, huge signed labels, diagnostics and interleaving do not contaminate mathematical certificate bytes. | green |
| CE10, CE11, CE15, CE18 | `tests/test_certificate.py::test_independent_wire_in_fresh_production_blocked_process` | The independent byte route accepts/rejects its fixed inputs with production imports blocked and enabled conversion limits. | green |
| CE9, CE14, CE15, CE18 | `tests/test_certificate.py::test_exact_large_integer_serialization_in_fresh_process` | Literal large-integer bytes across both enabled conversion limits and hash seeds, without process-setting changes. | green |
| CE10, CE18 | `tests/test_certificate.py::test_independent_source_is_fixed_and_has_only_standard_library_imports` | The test-only verifier matches its fixed source identity and has no production parser/validation imports. | green |
| CE1, CE15, CE17, CE18 | `tests/test_certificate.py::test_closed_sources_and_production_import_exactness_boundary` | Frozen dependency bytes, permitted direct imports and isolated production loading; arithmetic/dataflow restrictions distinguish codec work from optimization. | green |
| CE2, CE8 | `tests/test_certificate.py::test_builder_rejects_numerically_equal_nonempty_raw_forgeries` | Numerical equality is established while the forged literal pair is rejected at the builder boundary. | green |
| CE2, CE7, CE8 | `tests/test_certificate.py::test_builder_rejects_instance_dependent_normal_witness_faults` | Normally constructed but instance-dependent invalid witnesses are rejected without reopening the closed-record contract. | green |

CE19 is additionally supported by the separate executed implementation audit below,
not by declaring a mutation name inside a pytest function. CE20 is the scope and
preservation boundary of this appendix; it does not close the historical future
independent-checker obligations in TEST_PLAN section 11 (C1--C10).

### Independent serialized-input route and actual dual-solver evidence

The frozen test-only verifier consumes ONLY serialized instance bytes and
certificate bytes. It validates the canonical active instance, including edge
order and exact labels, before interpreting certificate references. It shares
no production parsing, validation, shore or witness helpers. The isolated audit
reports no exactfrac imports in that verifier. Production imports of normally
closed dependencies through SolveResult are a separate, legitimate loading path;
the source review permits only the adopted direct imports and no optimizer calls.
Import provenance, source restrictions and nonmutation were reviewed as part of
the existing implementation audit, not a newly inserted lifecycle gate.

All 140 registered malformed-wire cases and seven accepted instance-wire variants
are exercised by that independent route. Duplicate keys, noncanonical numeric
spellings, malformed UTF-8 and byte-envelope/newline defects belong to that
TEST-ONLY byte boundary, not a claimed production decoder in this unit.
Instance whitespace/key order may vary under the adopted input schema, but its
edge order is never normalized by verification. Production serialize_certificate
accepts a dictionary, not bytes/text, and cannot detect duplicates erased by a
caller's parser. Unit 18 retains independent production decoder/checker ownership;
`exactfrac_verify/check.py` remains absent and is not a Unit 17 availability gate.

The registry preserves all 389 inherited entry identities and the seven fixed
Unit 17 additions: 396 entries, including intentional duplicate mathematical
inputs. The actual independent implementation audit ran each under Standard
and Accelerated, for 792 final solves and 792 independently verified FINAL
production certificates. Every run preserves its own literal raw pair. All 396
cross-route comparisons are exact numerical comparisons, not demands for equal
witnesses, unreduced pairs or bytes under ties.

The same audit separately emitted and independently verified 3,962 LOCAL
reconstruction certificates: Baseline 788, L0 608, L1 572, H0 712, H1 750 and
H2 532. Both direct-H2 count shapes occurred: 374 one-edge and 158 split cases.
Direct H2 carries raw (4,2); this is local attainment evidence, not an invented
strict final H2 winner. Complete branch solves already dominate/tie direct H2
under the existing DESIGN 4.12.10 / ORACLE-111 ruling. Local counts/stream hashes
are observations of this run and are not additional solver tie rules.

Together with the 31 independently fixed literal fixtures, the audit verified
4,785 instance/certificate byte pairs: 31 + 792 + 3,962. These are executions,
not 4,785 distinct graph inputs or pytest cases. It also records 62 main-process
fixed serializations and 62 production fixed serializations in each of four
fresh-process checks. Each isolated independent route accepts 38 fixed/variant
pairs and rejects 140 corruptions with its production-import barrier intact.
The separate audit records 67 production object-rejection executions; this is
not a replacement for the parametrized consuming test's object-boundary coverage.

### Executed fault controls and what they establish

The independent audit detected all 18 declared fault families through 20 variants
and 23 executions: 17 production-behavior variants / 20 production executions,
one independent-oracle variant, and two integration variants. The extra three
executions are the repeated enabled-cutoff trials. These categories are not
collapsed into a claim that all 20 variants changed production source.

Faults cover literal-vs-numerical equality, delegated admissibility, false Empty,
erased nonempty-zero payload, packed/original-reference confusion, repaired sparse
order/duplicates, dropped envelope fields, byte order/LF, accidental digit cutoff,
hidden re-solving, output aliasing, stale validation, resource-to-Empty conversion,
suboptimal-witness rejection, verifier import contamination, registry deduplication
and an invalid cross-route raw-equality demand. M03 uses an early return accepting
a too-small total; its detection is NOT a claim that deletion of a redundant guard
alone was detected. M13 targets the independent verifier, and M16/M18 target
integration behavior. All observations are finite adversarial evidence, not a
complete mutation score over all possible bugs or an exhaustive correctness proof.

### Artifact bindings, preserved dependencies and remaining work

Accepted production package:
`ExactFrac_UNIT17_CERTIFICATE_IMPLEMENTATION_R2_PACKAGE.zip`
SHA-256: `fcf1eb29fc39436f2b545ac815cefe0d127d0058b95564529fc0581f0c6ec3ae`.
Its source-only patch has 166 lines and SHA-256
`9d3a05465afc54359e92b84bd12601c806b0e05c18dd80d80f6e985ba104ec7e`.
R1 stopped at live Ruff before source application; R2 changes only operand order
in its raw-pair comparison. No test, fixture, authority or closed dependency was
reopened to obtain GREEN. Failed-preflight packages remain historical evidence.

| Bound artifact | SHA-256 |
|---|---|
| exactfrac/certificate.py (production R2) | cffab68bf6c9c6c6ef1d4f9cc177b9718298bf12ec5cc16b4ed3353728b318a4 |
| tests/test_certificate.py (frozen R2) | c70f7120fe10d07668fc37624843cc77a02ef58244fbda432d04591123042724 |
| docs/DESIGN.md (closed authority) | d4494b201e2f19a9c3c30f919a32c7f5bd5f078422ea14dc37775b6db4612b9a |
| docs/TEST_PLAN.md (closed authority) | 42d0e0715392ed898624c329a65763555a01fe064c1ef51640d03513bb530224 |
| docs/ORACLE_CATALOG.md (closed fixtures) | 04ef6a4b38463aecb0d86731d1873aadb4acb8bc8a8593e0ea82b4325e56e7ac |
| IMPLEMENTATION_GREEN_AUDIT.json | 83eedbd48788f02c34d9290068ae25922dd357369df5246a927dfb65edf1a299 |
| IMPLEMENTATION_GREEN_CHECKPOINT.txt | 287e39b669549f7d3f014bbe80b92b2f6944753aa2759ef9ba6844d21da33921 |

The private controlling GREEN directory is
`unit17-certificate-implementation-r2-pro-audited/live-green.3ux80b1v/`.
The audit binds the actual targeted/full/Ruff streams, independent audit report,
source bytes, frozen test and prior evidence. Source Git blob is
`2ce3f2f3ae44177141976f84d15ee0a226b3e281`; test Git blob is
`0cbd94d1dd569c0dea0a434344a7f49a94979b87`. At GREEN all four refs still equal
`e68ea1cd3cf4e47645e90d0f14011290aba4bd4c`, its committed tree remains
`387dd07b05998b3ba0f84e8c4afe1238235b8155`, and the 44 committed files/index are
unchanged. Only the exact production source and frozen test are untracked.
These private evidence records are not added to the public repository.

The O(n+m) structural-scan/storage statement in DESIGN 4.14 excludes encoded
integer size. Serialization requires output-sized storage/work plus decimal
conversion bit cost; finite tests do not establish magnitude-independent codec
runtime, universal bit-complexity bounds, or end-to-end benchmark scalability.
No expanded-copy execution is introduced, but a finite large-integer test is not
a proof of all possible resource trajectories. Deployment quotas remain outside
this synchronous, in-memory object boundary and must not silently redefine /1.

This amendment changes ONLY CONFORMANCE. Source and test remain unchanged and
unstaged pending complete-candidate staging, exact staged-tree isolation,
postcommit checks and separate remote closure. Unit 17 is not yet complete at
this checkpoint. No Unit 18 checker, CLI, corpus-expansion campaign, experiment,
release, universal complexity theorem or independently certified optimum is
claimed complete. Private BUILD/LEARNING notes remain outside every gate and
are not produced as final Unit 17 notes at this intermediate step.


## Unit 18 — independent checker: finite GREEN conformance (implementation R1 / tests R2)

This appendix records the implemented scope of DESIGN 4.15, TEST_PLAN 41
(IQ1–IQ20) and the checker cases C1–C10 from TEST_PLAN 11. It is not a new
mathematical specification, an API revision, or a final unit-closure declaration.
All earlier CONFORMANCE bytes, rows and statuses are preserved as historical
records. In particular, earlier statements that the future checker was absent
remain statements of their earlier checkpoints, not current absence requirements.

Mathematical source remains SPEC_LOCK-pinned canonical V2.2: def:instance,
ass:active, def:parameter/eq:compact-density, lem:empty and its proof. lem:unit,
prop:endpoints and sec:global reconstruction/proofs explain producer candidates;
they do not impose an optimality, endpoint-only or solver-provenance filter here.
The optional normalization in mathematical exposition does not replace the
adopted /1 requirement for the witness's literal structural numerator/denominator.

### Implemented boundary and evidence state

`exactfrac_verify/check.py` exports only
`verify_certificate(instance: bytes, certificate: bytes) -> None`.
Both required positional-or-keyword inputs have exact built-in type bytes.
Success is exactly None. The complete instance is validated before certificate
inspection, including the declared shape, labels, canonical edge order and
active condition. Invalid input raises exact ValueError; the authorized narrow
UTF-8/JSON syntax translations are distinct from operational exceptions, which
propagate unchanged. Diagnostic prose and private parser names are not public API.

The instance substrate is standard-library json with independently written
local numeric/key hooks. Certificate parsing is a forward fixed-grammar cursor,
not re-encoding a decoded object to validate itself. Only json and future
annotations are imported. No producer/test/private reference, brute helper,
solver, I/O, dynamic code, global cache or process-setting change is used.
Nine-digit accumulation preserves finite integer tokens without full-token
int conversion, floating point, quotient reduction or implicit numeric coercion.

For nonempty witnesses, independently validated original indices and sparse
positive counts determine s=f(U), e=e_q(U) and Y=sum(y). Strict order/range,
crossing, count capacity, odd s+Y and s+Y>=3 are required, followed by both literal
identities N=2*(e+Y) and D=s+Y-1. Genuine Empty has no U/y payload and requires
Q==1 and literal (0,1) after active-instance validation. Nonempty zero and y=[]
are not Empty. Every admissible literally attaining witness is eligible, including
suboptimal, interior and losing local endpoint witnesses. No global optimality,
solver provenance or unique cryptographic instance binding is independently certified.

The live R1 implementation gate reports 1,033 targeted cases and 3,478 full-suite
cases, all collected and passed. The full total is the inherited 2,445 plus the
measured 1,033 new cases; it retains all 458 Unit 17 certificate cases. There are
no skipped collection items, collection errors, deselections or xfails. Candidate
source Ruff, repository Ruff and the independent implementation audit passed.
Both R2 tests and all 45 other existing files were conserved. These are executed
checks on the submitted candidate, not a proof of universal correctness.

### Exact consuming-test crosswalk

All rows below refer to the actual frozen R2 file, not planned names. The
19 top-level functions collect 1,033 parametrized cases. Function count, pytest
case count, solver runs, emitted byte pairs and fault executions are distinct.
The `green` status means the stated finite check passed at the implementation gate.

| Obligations | Actual test | Finite scope | Status |
|---|---|---|---|
| IQ10, IQ11, IQ17 | `tests/test_verify_check.py::test_closed_tables_and_qualified_registry_are_preserved` | Closed table fingerprints and 400 qualified registry identities; fault-family names are preregistration, not executed mutation evidence. | green |
| IQ1 | `tests/test_verify_check.py::test_public_api_success_and_root_ownership` | Exact placement/API, required bytes parameters and None success; unchanged package roots and brute helper. | green |
| IQ6–IQ8, IQ10; C1, C6, C7 | `tests/test_verify_check.py::test_literal_fixtures_preserve_raw_fields_and_original_coordinates` | 41 fixed literal byte recipes, original coordinates, exact structural raw pairs and valid nonoptimal/zero witnesses. | green |
| IQ3–IQ10; C1–C10 | `tests/test_verify_check.py::test_all_fixed_wire_verdicts_against_separate_byte_reference` | 519 independently fixed byte verdicts: 64 acceptances and 455 rejections; no producer/consumer self-oracle. | green |
| IQ1, IQ14 | `tests/test_verify_check.py::test_registered_api_type_arity_and_keyword_cases` | 34 declared API type/arity/keyword cases; exact bytes and ValueError rejection without caller coercion. | green |
| IQ2 | `tests/test_verify_check.py::test_instance_rejection_precedes_any_certificate_argument_access` | 12 declared invalid-instance cases never access the certificate argument; opcode instrumentation is test-local. | green |
| IQ2 | `tests/test_verify_check.py::test_certificate_access_trace_has_a_positive_control` | Positive control demonstrates that the certificate-access instrumentation fires on a valid instance. | green |
| IQ14 | `tests/test_verify_check.py::test_registered_dependency_exception_identity_and_narrow_translation` | Eight registered exception cases, narrow decode translations, and identity-preserving operational propagation. | green |
| IQ2, IQ4 | `tests/test_verify_check.py::test_bad_labels_reject_before_edge_degree_processing` | Invalid labels reject before edge/degree processing through finite test-local instrumentation. | green |
| IQ6–IQ8, IQ11, IQ12 | `tests/test_verify_check.py::test_both_real_solver_routes_and_all_local_reconstructions` | Every registry identity under both selections; final and local emitted bytes checked independently with per-run literal pairs. | green |
| IQ12 | `tests/test_verify_check.py::test_actual_local_origin_and_direct_h2_shapes` | Actual Baseline/L0/L1/H0/H1/H2 captures; both direct-H2 count shapes and losing local candidates. | green |
| IQ7, IQ8, IQ11; C6, C7 | `tests/test_verify_check.py::test_distinct_tied_raw_pairs_are_valid_but_rescalings_are_not` | Lawful distinct witnesses with equal ratios accepted; rescaling a fixed witness pair rejected. | green |
| IQ8, IQ16 | `tests/test_verify_check.py::test_no_hidden_solver_invocation_on_suboptimal_witness` | Admissible suboptimal witnesses accepted without hidden solver invocation. | green |
| IQ15, IQ16 | `tests/test_verify_check.py::test_production_source_import_and_forbidden_operation_surface` | Direct imports and forbidden-operation/dataflow surface; source review complements executed isolation. | green |
| IQ10, IQ13 | `tests/test_verify_check.py::test_separate_reference_large_integer_semantics` | Separate fixed byte reference under enabled digit limits and two seeds; not checker-only production evidence by itself. | green |
| IQ13, IQ15 | `tests/test_verify_check.py::test_checker_only_export_large_integer_rejection_and_runtime_isolation` | Checker-only export accepts/rejects fixed pairs with blocked producer/private imports, repeats and unchanged runtime settings. | green |
| IQ11, IQ12, IQ15 | `tests/test_verify_check.py::test_every_real_emission_is_accepted_with_only_checker_files_available` | All final/local emissions verified where only checker package files are available; serialized inputs only. | green |
| IQ18, IQ19 | `tests/test_verify_check.py::test_old_prefix_guard_remains_length_checked_and_append_tolerant` | Actual length-checked historical prefix guard: original/append accepted, truncation/three positional corruptions rejected. | green |
| IQ9 | `tests/test_verify_check.py::test_metadata_changes_can_preserve_attainment_without_digest_binding` | Valid metadata changes may preserve attainment; no cryptographic unique-instance binding is claimed. | green |

IQ16 and IQ17 additionally require the separate executed source/work and fault
audit summarized below. IQ19's exact full-file transition is bound by the RED
package/application evidence; a prefix test alone does not prove the two-line
retirement. IQ20 restricts this appendix to the implemented finite scope.

### C1–C10: independent production-checker scope

| Existing case family | Implemented finite evidence | Status |
|---|---|---|
| C1 | Valid nonempty fixtures and every actual final/local emitted certificate are accepted only after independent admissibility and raw-pair checks. | green |
| C2–C5 | Fixed byte cases reject noncrossing references, duplicates, descending references and counts exceeding original multiplicities. | green |
| C6–C7 | Forged numerator/denominator and equal-ratio reductions/rescalings are rejected for the same fixed witness. | green |
| C8–C9 | Exact byte grammar rejects Empty payloads and missing nonempty witness fields. | green |
| C10 | False Empty is rejected by independent active-instance validation and Q==1, not by trusting the flag. | green |

These rows supplement rather than rewrite the original planned/history rows.
They do not extend C1 into an optimality claim or require all different instance
bytes to invalidate an otherwise valid witness. The checker consumes the actual
supplied instance; optional labels never replace canonical vertex/edge indices.

### Independent bytes, actual producer observations and runtime isolation

The fixed corpus includes 41 literal byte recipes (31 inherited plus ten new)
within 519 wire cases: 64 acceptances and 455 rejections. The private reference
uses separate parsing/validation, receives only two serialized inputs and has no
producer imports. The checker under test is not its own expected-answer source.

All 396 inherited qualified registry identities and four Unit 18 additions are
preserved: 400 identities including intentional mathematical duplicates. The
independent audit ran each under Standard and Accelerated, for 800 actual final
producer solves and 400 exact numerical cross-route comparisons. Each run retains
its own literal raw pair; tied routes need not share witnesses, pairs or bytes.
No deduplication, secondary tie rule or extra solve forces equality.

The audit separately checked 4,006 actual local reconstruction certificates:
Baseline 796, L0 616, L1 578, H0 720, H1 758 and H2 538. Direct H2 includes
378 one-edge selections and 160 split selections. These are local reconstructed
witnesses, not invented strict final H2 winners. The 4,806 final/local pairs
(800+4,006) were both independently recomputed and accepted by the production
checker in a separate checker-only process. They are executions, not 4,806
unique graphs or additional pytest cases. Literal fixtures are a separate corpus;
the count 4,806 does not include an extra addition of those 41 fixtures.

Independent endpoint enumeration supplied 400 numerical references; 369 small
graphs also received full-vector/scalar enumeration. Those exhaustive private
reference routines are audit tools, not algorithms imported or run by the checker.
Producer observations use the frozen Unit 17 builder/serializer in a separate
process and transmit only instance/certificate byte pairs for checking.

Four fresh checker-only runs, with digit limits 4,300 and 640 and seeds 1 and 73,
each accepted 64 fixed pairs and rejected 455. The audit records only
exactfrac_verify and exactfrac_verify.check as loaded project modules, no
producer imports, unchanged settings and no retained caller inputs. Its exported
checker/root files were conserved. Separate source/import review complements
these executed barriers; integration pytest processes may legitimately import
producer modules to emit bytes and are not themselves checker-only processes.
The large-integer corpus includes 4,801-digit magnitudes. This is finite resource
and exactness evidence, not unlimited memory, denial-of-service protection or a
claim that operational failure is malformed mathematics.

### Executed fault controls and actual targets

The independent audit detected all 24 declared families through 24 variants and
27 executions: 21 production-behavior variants, two integration variants and one
test-prefix-guard variant. The accidental digit-cutoff variant accounts for four
executions over the two enabled limits and two seeds, rather than one.

| Fault families | Actual target and intervention | Executed outcome |
|---|---|---|
| Q01–Q06 | Checker source: lose duplicate keys; relax certificate whitespace; erase .0; use full-token int; bypass active or duplicate-label checks. | Detected |
| Q07–Q09 | Checker source: inspect certificate early; sort invalid edge order; confuse sparse positions with original references. | Detected |
| Q10–Q13 | Checker source: sort U/y, omit capacity or parity validation. | Detected |
| Q14 | Checker source: early success at total one, NOT merely deletion of a redundant minimum guard. | Detected |
| Q15–Q17 | Checker source: use numerical instead of literal equality, omit Q for Empty, forbid valid nonempty zero. | Detected |
| Q18–Q20 | Checker source: attempt optimizer/dependency imports or swallow an injected MemoryError into success. | Detected |
| Q21 | Checker source: impose boundary selection and reject a valid losing internal witness. | Detected |
| Q22–Q23 | Integration: require literal pair equality under a legal tie or deduplicate the mathematical registry (391 instead of 400 identities). | Detected |
| Q24 | Test-prefix guard: omit the historical prefix hash assertion. | Detected |

The report's generic accept-invalid/reject-valid labels describe detector outcomes;
its audit source specifies the actual source edits listed above. No variant is
claimed to execute the forbidden optimizer successfully: the import barrier detects
the attempt. Operational-failure tests inject faults; they do not demonstrate
physical memory exhaustion. These are finite adversarial checks, not a universal
mutation score or proof that every possible omission is detectable.

### Frozen transition, source identity and controlling live evidence

The authority and oracle phases are already separately closed. Phase C made only
the length-checked fixed-prefix replacement; Phase D removed exactly the two
checker-absence lines and added the new consuming test. The enclosing old tests
and every other old-test byte remain unchanged by that retirement. Its prefix
still requires at least 3,212,040 bytes hashing to
`04ef6a4b38463aecb0d86731d1873aadb4acb8bc8a8593e0ea82b4325e56e7ac`.
Original/append, empty/short and first/middle/last-corruption controls passed.
Neither transition grants another test edit during production or CONFORMANCE.

Tests-first R1 stopped at live lint before application. R2 changes only the
15 identified formatting/lint sites in the new file, with the module AST and all
embedded string values preserved. Its old-test candidate is unchanged from R1.
The actual R2 missing-module RED preceded the independently written checker.
Historical failed packages, prior source/test hashes and closed evidence are not
rewritten by this appendix. The checker is not a promotion/copy of the embedded
private reference; its independently written cursor and local JSON hooks implement
the adopted contract and retain the prescribed standard-library boundary.

| Bound artifact | SHA-256 |
|---|---|
| exactfrac_verify/check.py | 5beb9850bf7aeb311178a5f35df1357d8d4a3e801fde5341e2108176bd01f1ad |
| tests/test_verify_check.py (R2) | 99a66cef83df1c8c5191349e33966230ac21b8fc73e1e071f2f26bde74796dd3 |
| tests/test_certificate.py (completed two-line retirement) | c94179fdbd3cb106394fd4780f5580664f41068facd65dc15a4f91b5d945a996 |
| docs/DESIGN.md | 45c5b4cb078b8a45d0a724f0beea036557cb7be1d51bcc8aee07cdda68205c5c |
| docs/TEST_PLAN.md | 19fd12fbdcaa59c3b00547030f4dd091d18b69558f40a8b74e93307cdc546470 |
| docs/ORACLE_CATALOG.md | 05255f65148c007278a38df664df5e6ff02db868d63fdafe7d9a016861952840 |
| IMPLEMENTATION_GREEN_AUDIT.json | 8046729e4f00e942b6e938bf97269153e9a2dd9170c8dac6283b083718512609 |
| IMPLEMENTATION_GREEN_CHECKPOINT.txt | fa24ffd8e86043e60090809d82721f5825c0e484589da962367286c131f0ec7d |

The private controlling directory is
`unit18-checker-implementation-r1-pro-audited/live-green.yfmml3yb/`.
The source Git blob is `1c907b4807f7a24d3c062b21b9d58250b2d969fc`.
Accepted implementation ZIP SHA-256 is
`a40f94ac03cde71219ab475f907bf672ff2eeacce42160d7b9be8056a4fddd87`;
its source-only patch has 232 lines and SHA-256
`b8dc7f867730abcd21b0bef908008be41b446a63794b0e47033ebcd979f86392`.
The live toolchain was Python 3.14.6, pytest 9.1.1 and Ruff 0.16.5.
At GREEN all four refs remained `309ce997b4937e0f1a622303e27a01d10088c2ea`,
with committed tree `82442a314cf151848c1f9f8ed256e8f38802dbd3`, 46 unchanged
committed/index entries and divergence 0 0. Checker and new test were untracked;
the old test's exact two-line retirement was unstaged. Private evidence stays
outside the repository; this appendix binds it without embedding its files.

### Work bounds and remaining lifecycle

The source performs compact list scans O(n+m+|U|+k) for k sparse entries, apart
from label uniqueness, input-byte processing, decimal conversion and arbitrary
integer bit-operation costs. No Q-copy expansion or all-shore optimizer is used.
Decoded input storage and numeral work are not constant or magnitude-independent;
this appendix proves no universal strong-polynomial byte-runtime bound.

This step changes only docs/CONFORMANCE.md. It preserves its complete historical
prefix and all other source/test/governing bytes. The saved pre-CONFORMANCE GREEN
audit is authenticated, not rerun against its deliberately changed frozen document
hash. Targeted/full regression and repository Ruff run with this appendix present.
This neither invalidates nor silently rebases the original audit.

The complete four-path candidate still requires staging, exact staged-tree isolation,
a separate local implementation commit/postcommit checks and exact-commit remote
closure under TEST_PLAN 42. Unit 18 is not complete at this documentation checkpoint.
No CLI, later corpus campaign, experiment, release, independent global-optimality
certificate or additional review gate is claimed. Private BUILD/LEARNING notes
remain outside all helper checks and are not final-unit notes at this stage.


## Unit 19 — CLI composition: finite GREEN conformance (implementation R1 / tests R2)

This appendix records DESIGN 4.16 and TEST_PLAN 43 (CL1–CL18), under the
existing completion lifecycle in TEST_PLAN 44. It is a finite engineering
conformance record, not a new API, theorem, test exception or unit-closure claim.
The complete earlier CONFORMANCE prefix, including every prior row/status, is
preserved. Earlier checkpoint statements remain historical, not current bans on
subsequently authorized files. No original theorem row is promoted by this CLI.

### Implemented contract and mathematical boundary

`exactfrac/cli.py` exports only `main(argv: list[str] | None = None) -> int` and
is invoked with `python -m exactfrac.cli`. The implemented commands are
`solve [--solver Standard|Accelerated] INSTANCE` and `verify INSTANCE CERTIFICATE`.
The explicit CLI default is Accelerated; the closed solver default is unchanged.
The adopted grammar, end-marker/literal paths, exact help/usage bytes, binary stdin
operand, and exact built-in argv types are exercised by the frozen consuming test.
No console-script entry, __main__.py, root re-export, dependency, executable bit,
configuration or existing test is added/changed by Unit 19 production.

Solve privately decodes only instance syntax using standard-library json, duplicate
DECODED-key rejection and at-most-nine-digit integer accumulation. It delegates
schema/label/ordered-edge/active validation to Instance.from_dict, once. It calls
one selected solve, then build_certificate and serialize_certificate once on the
same instance/result chain. It checks normal return-type/selected-route promises,
then calls the public independent checker once on the original input and emitted
bytes BEFORE accessing stdout. It writes exactly that certificate and flushes;
there is no stats/banner/envelope, extra LF, retry, fallback or witness rewriting.

Verify acquires instance bytes first and certificate bytes second, then forwards
them once to the public independent checker, requiring exact None and returning
0 silently without stdout/stderr buffer access. A certificate read failure may
precede checking a malformed but acquired instance. This acquisition order does
not change the checker's instance-before-certificate-inspection rule. It does not
parse/re-encode input, construct Instance, invoke a solver or use private checker
helpers. Help/usage load no command dependencies. Route-specific independence is
established by fresh-process barriers, not a producer-populated integration process.

Canonical V2.2 remains the mathematical source: def:instance, ass:active,
def:parameter/eq:compact-density, lem:empty and lem:unit, prop:endpoints, and the
sec:global/alg:global reconstruction table/proofs. For a nonempty admissible witness,
s=f(U), e=e_q(U), Y=sum(y) and original crossing-edge references determine the
literal pair N=2*(e+Y), D=s+Y-1, with s+Y odd and at least 3. The CLI preserves
rather than recomputes/reduces that pair. Genuine Empty uses Q==1 and (0,1) under
the closed active-instance assumptions. Accepted nonempty zero, suboptimal and
losing local witnesses remain valid. The checker certifies admissibility and raw
attainment (a fractional lower bound), NOT global optimality or an exact block count.
Finite optimum comparisons below use separate exhaustive references.

### Actual frozen test crosswalk

The implementation GREEN gate measured 962 CLI cases, all passed, and 4,440 full
cases, all passed: the preserved 3,478-case baseline plus the 962 new CLI cases.
The full run includes 1,033 checker and 458 certificate cases. No collection errors,
collection skips, deselections or xfails were reported. Source/repository Ruff and
the separate implementation audit passed. These are saved executed results, not
new runs performed by this documentation statement. Each green row below means
only the stated finite scope. Top-level functions, parametrized cases, CLI calls,
qualified graph identities and mutation executions are different censuses.

| Obligations | Actual frozen consuming tests | Finite scope | Status |
|---|---|---|---|
| CL1 | `tests/test_cli.py::test_exact_public_surface_and_invocation_contract`<br>`tests/test_cli.py::test_python_call_exact_types_and_native_arity`<br>`tests/test_cli.py::test_argv_is_not_retained_or_cached_between_calls` | Exact main API, built-in argv types/native arity, unchanged roots/configuration and no retained argv. | green |
| CL2, CL3 | `tests/test_cli.py::test_registered_argv_grammar_and_literal_paths`<br>`tests/test_cli.py::test_fresh_cli_dependency_isolation_physically_without_producers` | All 98 registered argv rows, literal paths/end-marker, default and explicit routes, six exact help forms and usage rejection before dependencies/input I/O. | green |
| CL4 | `tests/test_cli.py::test_registered_argv_grammar_and_literal_paths`<br>`tests/test_cli.py::test_verify_operand_acquisition_precedes_checker_validation`<br>`tests/test_cli.py::test_invalid_instance_with_readable_certificate_reaches_only_checker`<br>`tests/test_cli.py::test_verify_checks_each_reader_byte_promise_before_checker` | Binary operand ownership, exact bytes return promises, instance-then-certificate acquisition and no premature checker call. | green |
| CL5 | `tests/test_cli.py::test_registered_instance_syntax_and_graph_boundary`<br>`tests/test_cli.py::test_actual_json_substrate_decode_error_has_the_ruled_translation` | 52 syntax/schema/domain rows; no normalization; syntax-only adapter delegates once to closed Instance.from_dict. | green |
| CL6, CL8 | `tests/test_cli.py::test_fixed_literal_solve_result_seams_preserve_raw_identity`<br>`tests/test_cli.py::test_closed_normal_return_promises_fail_before_downstream_work`<br>`tests/test_cli.py::test_registered_operational_exceptions_preserve_identity` | Same-object composition, one selected solve, exact result/stats/build/serialize/checker promises, original literal bytes and no stdout before self-check. | green |
| CL7, CL12 | `tests/test_cli.py::test_complete_fixed_wire_corpus_through_verify`<br>`tests/test_cli.py::test_verify_command_requires_exact_none_without_stream_access`<br>`tests/test_cli.py::test_all_400_qualified_graphs_both_real_selections_repeats_and_local_candidates` | 519 fixed wire cases and actual local witnesses; silent verification, original reference indices, attainment including valid suboptimal/zero witnesses, not optimality. | green |
| CL9 | `tests/test_cli.py::test_registered_operational_exceptions_preserve_identity`<br>`tests/test_cli.py::test_syntax_exception_classes_are_not_translated_outside_decoders`<br>`tests/test_cli.py::test_actual_json_substrate_decode_error_has_the_ruled_translation` | 81 registered exception rows and additional scoped decoder controls; injected exception identity is preserved outside the two authorized translations. | green |
| CL10 | `tests/test_cli.py::test_registered_short_write_progress_flush_and_partial_failure`<br>`tests/test_cli.py::test_help_and_usage_enforce_all_binary_return_promises`<br>`tests/test_cli.py::test_closed_normal_return_promises_fail_before_downstream_work` | 21 registered write plans and promise controls: suffix progress, flush completion, no exception retry/text fallback and honest retained partial prefix. | green |
| CL11 | `tests/test_cli.py::test_all_400_qualified_graphs_both_real_selections_repeats_and_local_candidates` | All 400 qualified identities under both selections, 800 first plus 800 repeat solves, 400 numerical comparisons and 4,006 local verifies; no deduplication or forced cross-route byte equality. | green |
| CL13 | `tests/test_cli.py::test_fresh_independent_reference_has_no_project_dependencies`<br>`tests/test_cli.py::test_fresh_huge_solve_both_selections_and_literal_pair_observation`<br>`tests/test_cli.py::test_fresh_cli_dependency_isolation_physically_without_producers` | Fresh seed 1/73 and enabled digit-limit 4,300/640 cases, including inherited 4,801-digit numerals and unchanged process settings. | green |
| CL14 | `tests/test_cli.py::test_fresh_cli_dependency_isolation_physically_without_producers` | Physically producer-free export plus import-attempt/origin checks; help/usage and verify have different allowed project-module sets. | green |
| CL15 | `tests/test_cli.py::test_real_module_entry_binary_files_stdin_and_process_status` | Actual python -m entry, binary files/stdin, help/usage, both solve selections, valid and failing verify processes; only normal 0/2 statuses and fixed texts are specified. | green |
| CL16 | `tests/test_cli.py::test_cli_source_dependency_and_process_setting_boundary`<br>`tests/test_cli.py::test_argv_is_not_retained_or_cached_between_calls`<br>`tests/test_cli.py::test_registered_operational_exceptions_preserve_identity` | Executed source/ownership/nonmutation controls supplemented by independent source review; no new parser API, metadata, telemetry, dynamic code or process-setting mutation. | green |
| CL17 | `tests/test_cli.py::test_registered_fixture_tables_and_qualified_censuses` | This test checks preregistration/fingerprints only. Actual detection of all 30 families comes from the separate pinned GREEN implementation audit, not this test alone. | green |
| CL18 | `tests/test_cli.py::test_historical_and_unit19_catalogue_prefixes_are_length_and_hash_guarded`<br>`tests/test_cli.py::test_registered_fixture_tables_and_qualified_censuses` | Historical and Unit 19 length/hash protections, exact table/registry identity, and no closed-test reopening. | green |

Every top-level test in frozen R2 tests/test_cli.py is mapped above; exact source
line ranges are in the private TEST_CROSSWALK.json. CL17's declared fixture rows
alone are NOT evidence that mutations were executed or detected.

### Independently observed corpus, bytes and import boundaries

The registry retains 400 qualified identities, including intentional mathematical
duplicates; no new Unit 19 graphs were added. Its fingerprint remains
`776ed183b5cd778b9e43ce0da08a809149bf233ac1fd9d928c63159d0dde5566`.
Independent endpoint references cover all 400; vector/scalar references cover the
369 declared small graphs. The independent audit executed 800 first CLI solves
and 800 same-route repeats: 1,600 actual solver calls, one per solve invocation,
800 repeat byte checks and 400 exact numerical cross-route comparisons. Tied
routes need not share witness, literal pair or certificate bytes.

The audit additionally exercised 4,006 actual local certificates through CLI verify:
Baseline 796, L0 616, L1 578, H0 720, H1 758 and H2 538. H2 includes 378 one-edge
and 160 split selections. These are local reconstructions, including losers, not
invented strict final H2 winners. The 800 first final plus 4,006 local pairs yield
4,806 independently evaluated pairs; the independent restricted-export verifier
also checked those 4,806 emitted pairs. Repeat solves are not another 800 unique
graphs, and these invocation counts are not additional pytest case counts.

The separate fixed-wire corpus contains 519 cases: 64 acceptances, 455 rejections,
including 41 fixed literal recipes. Four fresh restricted-export processes at
limits 4,300/640 and seeds 1/73 exercised those verdicts and 64 help/usage grammar
cases each. The allowed project files are only the empty exactfrac root, cli.py,
the empty exactfrac_verify root and check.py; producer implementation files are
physically absent. Help/usage load only the first two modules; verify may load all
four. No forbidden import attempts or setting changes were observed. Additional
fresh huge-solve checks and 12 actual module-entry audit cases passed. Test-local
instrumentation is not shipped as production code.

### Executed adversarial controls and errors

All 30 preregistered families CLF01–CLF30 were detected. The independent audit
executed 28 production-source variants with 28 pristine controls, and two
integration variants. The latter target overstrong cross-route raw equality
(CLF25) and registry deduplication (CLF26), not production parser branches.

| Families | Tested intervention | Recorded outcome |
|---|---|---|
| CLF01–CLF06 | Wrong/default selection, duplicate option, help I/O/extra-token acceptance and end-marker handling. | Detected |
| CLF07–CLF11 | Duplicate-key loss, -0/float acceptance, edge normalization and full-token integer cutoff. | Detected |
| CLF12–CLF16 | Second solve, raw rescaling, self-check bypass and stdout/stat/extra-LF leakage. | Detected |
| CLF17–CLF20 | Verify producer import, input rewriting, swallowed operational error and acquisition order. | Detected |
| CLF21–CLF24 | Short-write loss/duplication, closing caller streams and missing flush. | Detected |
| CLF25–CLF26 | Integration-only tied-pair equality and qualified-registry deduplication. | Detected |
| CLF27–CLF30 | Early stdout access, wrong normal return promise, non-silent verify and process-setting change. | Detected |

Wrong Python argv types raise ValueError; native wrong-arity TypeError remains.
Normal command/help completion returns exact int 0 and usage rejection exact int 2.
Only actual strict UTF-8 decode and JSON syntax errors receive the authorized
InvalidInstance translation. Closed semantic and injected operational exceptions
otherwise propagate by identity, including ValueError, OSError, MemoryError,
RecursionError and RuntimeError. Wrong normal-return promises raise RuntimeError,
not a malformed-data verdict. Injected failures do not demonstrate physical memory
exhaustion, and interpreter traceback text/failure status is not a fixed wire API.

The writer completes positive short writes with the unwritten suffix, requires
valid exact-int progress and exact-None flush, and never retries an exception.
Validation/composition failures precede stdout access. Once emission begins, an
I/O failure can retain a partial prefix; output is not atomic and is not rolled
back. Caller process streams remain open/unrebound; no text fallback is provided.

### Frozen identities and preserved archive incident

The R1 tests-only application stopped at live SIM114 before writing any test.
The first R2 preflight then exposed SIM101. The accepted R2 changes only original
lines 1890–1893 to the single isinstance type-tuple branch at 1890–1891. Bytes and
module AST outside that site, and all module constants/embedded reference strings,
were preserved; AST location attributes were excluded because line numbers move.
The accepted R2 live Ruff and precise missing-exactfrac.cli RED preceded production.
Neither this record nor the archive recovery authorizes another source/test edit.

| Bound artifact | SHA-256 |
|---|---|
| exactfrac/cli.py (R1) | 0e41e915bb79e88621df84fe335706a40d0a76f196a5f351ce9d9897863644d8 |
| tests/test_cli.py (R2) | ad1fa1ec0912f0067135176490c8af962d1655057aeaa9618e67e0e4b43e3112 |
| docs/DESIGN.md | 1a088391ace3fbca767ae83e59b644af1699ac880a26183f744837a44f771289 |
| docs/TEST_PLAN.md | 9836b2b70de107b4756e95b94620d12a2e8a7c1d5d87f4ce638fbb478d88db63 |
| docs/ORACLE_CATALOG.md | 523e3025e53fc1676ccd60a8e3e1f1955a8ace545ec34fea0cf4fa5d59dd056b |
| IMPLEMENTATION_GREEN_AUDIT.json | ccaab83b85b9d0f1866354f992a8362094ce3133bd2cb4ecbcb1ef31448ab917 |
| IMPLEMENTATION_GREEN_CHECKPOINT.txt | d212c6ff8e917a6c6e5ee490d5e235021c1041d4ac1fa7198484d72c51dc425f |
| ARCHIVE_RESTORATION_AUDIT.json | b9dbc9cdc6c925954304868fbeff44a02598967ff2f7b279b6feb621007a4161 |
| ARCHIVE_RESTORATION_CHECKPOINT.txt | c123d354228f0552996f71bbfc1b25ffc6f1625d7f6da08b1cc42628ed3a9040 |

The controlling GREEN directory is
`unit19-cli-implementation-r1-pro-audited/live-green.vm1clr6n/`.
The source Git blob is `6a2b0afbae74ffed11715822bfe687559b6744d3`.
The original 874,328-byte implementation ZIP hashes to
`9f41b767b0b7578190fb6d90d93b16e29911e47820168da4ea7c9a394ae991dc`.
After the console-paste incident truncated that ZIP, read-only inspection found
repository GREEN identities, extracted package and saved evidence intact. Recovery
restored those exact published archive bytes without extraction or implementation,
test or audit replay. The zero-byte incident artifact remains TRUNCATED_ORIGINAL.zip
under `unit19-implementation-archive-restoration-r1/live-restoration.gfy6jq1g/`.
The recovery is separate evidence, not a rewritten GREEN record or a new implementation.

The historical catalogue prefixes at 3,212,040 and 3,312,641 bytes remain unchanged;
the Unit 19 catalogue has 3,392,373 bytes. Length-and-hash controls reject truncation
or prefix alteration while permitting later authorized appendices. This step changes
no catalogue byte or test guard. Base commit remains
`25a51a210b117652fecabc0981fbde952675bd3d`, tree
`6f08edc0952cac7571c83f6293133ebee040e6ab`, four-reference agreement and divergence
0 0. CLI and frozen test remain untracked/unstaged; CONFORMANCE alone becomes an
unstaged tracked modification. All other 49 live candidate files are frozen.

### Resource limits and remaining lifecycle

Read-all input/output and decoded JSON incur byte-sized storage and arbitrary
integer bit costs. Syntax accumulation is driven by bytes/digits, not expansion
of Q copies or shore enumeration. No universal strong-polynomial byte-runtime,
constant-memory, unlimited-resource, denial-of-service or regular-file-sandbox
claim is established. Ordinary host-selected file/symlink/device semantics remain.
No benchmark timing, RunRecord wire encoding, telemetry output, environment/Git
metadata discovery, release entry-point packaging, corpus campaign or experiment
is claimed; the later Unit 21 allocation in DESIGN 4.16.12 remains open.

Phase G appends only docs/CONFORMANCE.md. The saved standalone GREEN audit and
archive-recovery evidence are authenticated, not rerun/rebased against the changed
document. Targeted/full regression and repository Ruff must run with this appendix
present. Phase H still requires exact three-path staging (CONFORMANCE, cli.py,
test_cli.py), staged-tree isolation, separate implementation commit/postcommit
checks and separate approved-commit remote closure. Unit 19 is not complete here.
Private BUILD/LEARNING notes are not inspected or gated by this step.

## Unit 20 — reproducible initial corpus: finite engineering conformance

This append-only entry records the Unit 20 Phase E/F audited GREEN candidate under
DESIGN §13 (D20-C1–D20-C10), its D20-M1–D20-M3 addendum, and TEST_PLAN §§45–46
(CP1–CP18). It adds an engineering conformance record, not a new mathematical
source label. Every preceding theorem row, status and historical record remains
unchanged. In particular, this finite corpus does not promote a previously planned
invariant or `thm:main` row or replace the historical 400-identity registry.

The governing mathematical labels `def:instance`, `ass:active`, `def:parameter`,
`lem:aggregation`, `lem:interval`, `prop:expanded-equivalence`, `lem:empty`,
`lem:endpoint-difference` and `prop:endpoints` supply the semantics consumed by
independent references. The versioned recipe grid, seeded support, generator API
and serialization are separately adopted engineering contracts, not source theorems.

### Implemented surface and observed GREEN

| Engineering obligation | Implemented and exercised scope | Status |
|---|---|---|
| D20-C2–C7; CP1–CP12 | Pure deterministic `exactfrac.corpus` generator; exact finite registry, canonical payload bytes, immutable fresh-build result and owning-suite integrity/extension checks. | green |
| D20-C8–C9; CP13–CP16 | Independently registered finite mathematical references, required both-solver subset, certificate attainment/checking and separately counted adversarial controls. | green |
| D20-M1–M3; CP17–CP18 | Witnessed tests-first RED, exact authorized predecessor-test retirement, and scoped rather than aggregate-wide integrity checks. | green |

The production public surface is exactly `recipe_ids() -> tuple[str, ...]`,
`generate_instance(recipe_id: str) -> bytes`, and
`build_corpus() -> tuple[tuple[str, bytes], ...]`; `__all__` is
`("build_corpus", "generate_instance", "recipe_ids")`. The one input parameter is
positional-or-keyword and requires an exact built-in str equal to an adopted ID.
Nonmembers and other types raise plain ValueError without coercion or repair.
No writer, reader, merge API, CLI, public error class or solver call is added.

The live implementation gate observed 72 collected/passed corpus cases from 16
module-level test functions and 4,512 collected/passed full-suite cases, exactly
4,440 inherited plus 72 new. CLI/checker/certificate-file counts remained
962/1,033/458. Setup, call and teardown all passed, with no collection errors,
skips, deselections or xfails. Live source preflight and full-repository Ruff passed;
project import paths and bytes were authenticated. These are case counts, not counts
of graph instances, solves, certificates or fault injections.

The authenticated live toolchain was Python 3.14.6, pytest 9.1.1 and Ruff 0.16.5.
Both targeted and full runs reported one nonfatal PytestRemovedIn10Warning about
`itertools.product` used as parametrization argvalues in
`test_fresh_process_full_generation_purity_and_settings`. The warning was not
suppressed and the frozen R2 consumer was not edited. This record does not claim
warning-free execution, pytest 10 compatibility or minimum-interpreter reproduction.

### Frozen-test crosswalk

All function names below belong to `tests/test_corpus.py` unless a private saved
phase record is explicitly named. CP16 and CP17 require their separately recorded
audit/transition evidence; a declared test name alone is not proof of execution.

| Obligation | Frozen consuming test or authenticated phase evidence | Finite evidence boundary |
|---|---|---|
| CP1 | `test_public_surface`; `test_invalid_recipe_domain` | Exact exports, signatures, types and rejection cases, including hostile coercion and U+FF11. |
| CP2 | `test_complete_inventory_and_immutable_build` | 655 ordered identities retained without deduplicating equal payloads; immutable deterministic results. |
| CP3 | `test_all_payloads_and_closed_instance_boundary` | Independently constructed supports, canonical edge order and edge-index-dependent multiplicities. |
| CP4 | `test_all_payloads_and_closed_instance_boundary`; `test_private_exact_sha_threshold_control` | Exact seed messages/backbone and strict first-byte threshold; injected byte 64 is excluded. |
| CP5 | `test_all_payloads_and_closed_instance_boundary` | Exact q/f formulas, support counts, degrees and active-regime closed Instance construction for every recipe. |
| CP6 | `test_all_payloads_and_closed_instance_boundary`; `test_complete_inventory_and_immutable_build` | Independent payload bytes, lengths/digests and historical initial MANIFEST, not producer self-certification. |
| CP7 | `test_fresh_process_full_generation_purity_and_settings`; `test_operational_sha_failure_is_not_partial_success` | Full generation with existing digit limits 640/4,300; resource-exception injection and no setting changes. |
| CP8 | `test_complete_inventory_and_immutable_build` | Exactly 656 immutable fresh-build records: initial MANIFEST first, then 655 owned payloads. |
| CP9 | `test_manifest_parser_guard_isolation`; `test_live_aggregate_owning_projection` | Strict independent aggregate schema, duplicate/numeric/order rejection and exact Unit 20 projection. |
| CP10 | `test_owned_namespace_guard_isolation`; `test_live_aggregate_owning_projection` | Missing/extra/altered/renamed/nested/redirected/special/executable owned payload checks. |
| CP11 | `test_future_extension_and_formatting_nonmutation`; `test_consumer_mutants_do_not_freeze_or_rewrite_foreign_data` | Temporary foreign-suite/root-document additions and aggregate formatting variation pass; own corruption still fails. |
| CP12 | `test_source_stdlib_exactness_and_dependency_boundary`; `test_fresh_process_full_generation_purity_and_settings`; `test_operational_sha_failure_is_not_partial_success` | Actual standalone production source under blocked I/O/dependencies/state access; failures are not partial successful builds. |
| CP13 | `test_full_endpoint_and_micro_cross_model_references` | All 379 microinstances checked across compact vectors, scalar totals, distinguishable copies and endpoints. |
| CP14 | `test_both_closed_solvers_384_inputs_768_solves`; `test_same_route_repetition_and_numeric_tie_semantics` | Required 384-input subset; independent optimum/attainment/certificate checks, numeric cross-route equality and same-route repetition. |
| CP15 | `test_full_endpoint_and_micro_cross_model_references` | Independent finite shore/endpoint references for all 655 recipes; no huge-copy enumeration. |
| CP16 | Separate authenticated `AUDIT_IMPLEMENTATION.py` execution and GREEN record | 26 actual production-source variants and 27 integration cases with pristine controls; three Phase D preservation families have separate provenance. |
| CP17 | Saved R2 `TESTS_RED_AUDIT.json` and checkpoint; `CHECK_TRANSITION.py` controls | Both test preflights, exact 94-byte retirement, specific missing-module RED and unchanged 4,440-case inherited baseline. |
| CP18 | `test_future_extension_and_formatting_nonmutation`; `test_consumer_mutants_do_not_freeze_or_rewrite_foreign_data`; phase-local pin classification | Own immutable versioned payloads stay checkable without a lasting global MANIFEST/root inventory freeze. |

### Independently fixed bytes and mathematical comparisons

The retained registry contains 55 two-vertex microinstances, 324 triangle-support
microinstances, 120 structural-family recipes, 120 bit-width-sweep recipes and 36
seeded recipes. These total 655 recipe identities and 599 distinct payload byte
strings, not 655 distinct graphs. The 655 owned files contain 794,072 bytes.
The separately preregistered initial MANIFEST contains 126,935 bytes and has SHA-256
`866541ba2ab7a4d5f2a1e6a4cb0a24da769392e8bb8747a8fe1997a8bb8640d8`.
This is the historical initial build-product identity, not a continuing whole-file
pin on the evolving `instances/MANIFEST`.

The consumer reconstructs expected payloads independently and checks committed Phase C
tables fixed at oracle commit `b9c931b4f3d3c1f473e8f1681544286bae3051fe`, before
consuming tests and production existed. Neither producer output nor a producer-derived
MANIFEST establishes the expected answer. Every recipe is independently decoded and
accepted by the closed Instance boundary. The finite endpoint reference examined
21,549 nonempty shores: 20,704 feasible and 845 infeasible, with 39,056 endpoint
evaluations. The 379 microinstances additionally compared 2,433 shores, examining
13,179 compact vectors, 8,787 scalar totals and 21,487 distinguishable-copy subsets;
the respective admissible counts were 6,183, 3,981 and 10,349. The sole global Empty
recipe was `edge-q01-f01-01`; a zero-valued local witness is not global Empty.

For a tested nonempty shore U and boundary total Y, the independent reference checks
`0 <= Y <= b_q(U)`, odd `f(U)+Y >= 3`, and the raw pair
`(N,D) = (2(e_q(U)+Y), f(U)+Y-1)`. Positive-denominator cross multiplication
compares values; raw pairs and tied witnesses need not be equal across solver routes.
The five adopted `bits-{family}-n04-b16384-qramp-fdegree` stress recipes each have
independently registered optimum 1.

Each targeted/full/standalone audit execution ran Standard and Accelerated on the
same required 384 inputs: the 379 microinstances plus those five stress recipes.
Each execution therefore made 768 required solves and checked 768 serialized
certificates, with direct raw witness attainment and independent optimum comparison.
Checker acceptance alone is not an optimality proof. An additional two-recipe,
two-route repetition check made eight separately counted solves and checked four
certificates. These campaigns were repeated in different gate executions; 768 is
not the sum across all executions, and repetitions are not new unique instances.
No solve campaign on the other structural or seeded recipes is credited here.

### Pure generation and separately counted adversarial evidence

The generator uses only stdlib dependencies and exact integers. Its decimal encoder
uses base-1,000,000,000 chunks, with each direct conversion bounded by nine digits;
its output work and storage depend on encoded length. Source review found no
multiplicity-copy expansion, scan through 0..Q or 0..f(v), mutable global state,
optimizer invocation, filesystem/environment/clock access or interpreter-setting
change. Complete generation was exercised in four fresh processes at digit limits
640/4,300 and hash seeds 1/73, with no project imports and 656 output records each.
Four additional fresh scenarios exercised the SHA threshold boundary and injected
MemoryError, RecursionError and OSError; the settings remained unchanged. Injected
exceptions are not evidence of actual physical resource exhaustion.

The standalone audit detected 26 production-source mutation cases across 24 declared
families, with pristine controls. It separately detected 27 owning-integration cases
across 13 families, including manifest/schema/filesystem corruption, forbidden global
freezes, foreign-row loss and overstrong raw-pair equality. These are not 53 production
mutants. The remaining three of the 40 preregistered families, U20F34/U20F35/U20F36,
are Phase D preservation obligations authenticated from the prior RED evidence,
not replayed or counted as production-source mutations. All frozen consumer/source
identities remained unchanged by the audit.

The owning integration validates exactly `instances/unit20-v1/` and its 655 manifest
rows against independent bytes. It rejects corruptions inside that namespace while
accepting a well-formed temporary foreign suite and unrelated root documents. JSON
whitespace/object-key order may vary in the live aggregate; entry order and schema
may not. No production manifest parser or merger is implied. Future suite science
and authorization are responsibilities of the owning future unit.

### Evidence identities and remaining lifecycle

| Bound artifact | SHA-256 |
|---|---|
| `exactfrac/corpus.py` (implementation R1) | `64b04625b219b5de260f08e481e766358bdf39da8280880f563320c05000e369` |
| `tests/test_corpus.py` (RED R2) | `afe19fa4ef4a2fcb1562ecc6012c97b64464832651604d45c34ed0314eeced80` |
| `tests/test_cli.py` (exact D20-M1 postimage) | `02a63b0f95000aab30405a979034bdb628e37b69c635094f4cd0e7190796f42d` |
| `IMPLEMENTATION_GREEN_AUDIT.json` | `c2be2f7b4649b8b7ff4f6f6407e5341d3aad27494736364f043a0b4f2434a21e` |
| `IMPLEMENTATION_GREEN_CHECKPOINT.txt` | `e718f9544ba30ead644cf5cc299248f1144de332b9524417030ffa9595e3b74d` |

The source Git blob is `15af37506690414421989d3bf0ee9e3340491167`.
The controlling private GREEN record is
`unit20-corpus-implementation-r1/live-green.bc8vjkfj/`.
The original Unit 19 CLI-test identity remains valid for its historical snapshot;
D20-M1 authorized only the 94-byte MANIFEST-pin deletion, leaving `_CLOSED_PATHS`,
its MANIFEST membership, the other 41 hashes and every other CLI-test byte intact.
R1's preapplication lint STOP, R2's lint-only correction, and the earlier oracle
symbolic-reference closure recovery remain separate preserved provenance records.
This appendix changes none of those records and authorizes no further test revision.

Phase G changes only `docs/CONFORMANCE.md`, preserving its entire prior prefix.
The original GREEN audit and saved results are authenticated rather than rewritten
against this documentation postimage; targeted/full regression and repository Ruff
run again with the appendix present. All 707 other candidate files and the original
50-entry index remain unchanged. Complete-candidate staging, staged-tree isolation,
local implementation commit/postcommit checks and remote closure are still required.
Unit 20 is not remotely closed by this entry. Final private BUILD/LEARNING notes are
not produced or inspected in this phase.

Finite checks establish only the enumerated byte, schema, arithmetic, composition
and fault-detection behavior. They do not prove universal solver correctness, strong
polynomiality, bit-complexity bounds, performance/scalability, constant memory,
look-ahead coverage, uniform random sampling or application-domain suitability.
Unit 21 experimental execution, timings, comparative/operation/bit-growth results and
Unit 22 minimum-interpreter reproduction, packaging, privacy/licensing and release
remain outside this entry. Mutable aggregates and future-owned artifacts are not
permanently frozen by these phase-local identities.

## Unit 21 — initial measured campaign: finite engineering conformance

This append-only Phase G entry records the Unit 21 Phase E/F audited GREEN
candidate under DESIGN §14 (D21-E1–D21-E16) and TEST_PLAN §§47–48
(EP1–EP20). It adds an engineering record, not a mathematical source label.
Every earlier byte, theorem row and status is preserved. In particular, this
entry does not promote the historical planned invariant or `thm:main` rows.
The mathematical labels named in D21-E1 retain their source-dependent meaning;
the runner protocol, record schemas and timing policy are engineering contracts.

The observed Mac GREEN was reported on September 22, 2026. The predecessor
remains oracle commit `652a1d167a761b30db61192161221b78cf586f95`, tree
`f44b26ceccd0f503e6543b0bbb015e5ce6be56e1`. Production and result additions
are not yet committed by this entry. Authority and oracle documents retain
their historical prospective language; this later record supplies execution
evidence without rewriting those earlier snapshots.

### Implemented surface and actual frozen-test crosswalk

The new runtime surface is `exactfrac.experiments.main(argv: list[str] | None
= None) -> int`, with the guarded direct script `experiments/reproduce.py`
and its `experiments/README.md`. There is no new solver, backend, corpus family,
public parser API, external optimizer, configuration change or release claim.
The existing Standard and Accelerated solvers, telemetry, certificate builder
and independent checker remain closed dependencies.

All test names below are in `tests/test_experiments.py` at the authorized
100,509-byte import-amended identity. Its 37 test functions and 104 assert
statements yielded 187 collected/passing cases on the reported Mac. Function,
assertion, collected-case and solver-call counts are different quantities.
`green (finite)` means the stated finite engineering checks passed, not a
proof of universal mathematical correctness or asymptotic performance.

| Obligation | Implemented and exercised finite scope | Actual tests / other evidence | Status |
|---|---|---|---|
| EP1 | Exact main/argv boundary, pure imports, guarded script, fixed binary help/usage and stream errors. | `test_public_interface_and_runtime_dependency_direction`; `test_exact_argv_types_reject_before_access`; `test_usage_is_fixed_binary_non_echoing_and_help_is_pure`; `test_invalid_standard_binary_write_return`; `test_standard_stream_exception_identity`; `test_invalid_standard_flush_return`; `test_import_wrapper_guard_and_same_main`; `test_direct_script_fresh_process_help_and_usage_do_not_run_campaign` | green (finite) |
| EP2 | All registered inputs and retained buffers; coherent altered input cannot certify itself. | `test_coherent_altered_payload_is_not_its_own_oracle`; `test_retained_bytes_are_not_swapped_after_input_validation`; `test_closed_generator_normal_return_promises`; `test_scripted_schedule_counters_and_exact_tables` | green (finite) |
| EP3 | Strict aggregate/instance decoding; duplicate keys and malformed numeric tokens rejected; foreign rows preserved. | `test_manifest_rejection_precedes_solve_and_output`; `test_manifest_lexical_json_traps`; `test_valid_foreign_aggregate_and_cwd_independence`; `test_closed_instance_exception_identity`; `test_fresh_process_limits_and_hash_seeds` | green (finite) |
| EP4 | Input/source file kinds and ownership; output overlap, redirection and overwrite rejection. | `test_input_filesystem_fail_closed`; `test_output_lexical_and_ownership_rejection`; `test_valid_external_output_and_optional_order`; `test_source_member_filesystem_rejection_before_solve` | green (finite) |
| EP5 | Ordered 5,240-call scripted schedule, both routes and fresh repetitions; not actual timing evidence. | `test_scripted_schedule_counters_and_exact_tables` | green (finite) |
| EP6 | Two measured clock reads, none for warmups; exact interval and diagnostic metadata separation. | `test_scripted_schedule_counters_and_exact_tables`; `test_bad_normal_return_is_runtime_error_not_failed_row`; `test_dependency_exception_object_is_not_translated`; `test_invalid_clock_information_precludes_success` | green (finite) |
| EP7 | Actual record composition, native route fields, counters, nonbranch/infeasible branch retention and peak maxima. | `test_scripted_schedule_counters_and_exact_tables`; `test_giant_native_integer_is_unquoted_and_exact`; `test_independent_consumer_detects_coherent_corruption` | green (finite) |
| EP8 | Per-call checked certificates, exact same-route repeats and numerical cross-route comparison without raw-pair normalization. | `test_repeat_and_cross_route_consistency_is_not_assumed`; `test_same_route_certificate_bytes_must_match_warmup`; `test_bad_normal_return_is_runtime_error_not_failed_row`; `test_bounded_actual_telemetry_integration_not_full_campaign` | green (finite) |
| EP9 | Fixed 22-path source fingerprint, imported origins and input/source drift rejection. | `test_source_input_and_import_identity_drift`; `test_source_member_filesystem_rejection_before_solve`; `test_default_paths_use_source_root_not_cwd`; `test_scoped_fixture_and_source_identities_do_not_freeze_future_roots` | green (finite) |
| EP10 | Versioned raw JSON and unquoted huge integers; bounded conversion without interpreter-limit changes. | `test_giant_native_integer_is_unquoted_and_exact`; `test_fresh_process_limits_and_hash_seeds`; `test_scripted_schedule_counters_and_exact_tables`; `test_independent_consumer_detects_coherent_corruption` | green (finite) |
| EP11 | Exact three-table reconstruction from persisted measured records, correct joins and integer medians. | `test_scripted_schedule_counters_and_exact_tables`; `test_independent_consumer_detects_coherent_corruption` | green (finite) |
| EP12 | Exclusive output and final marker; short writes, invalid returns and distinct I/O failure boundaries. | `test_output_failure_never_publishes_complete`; `test_output_bad_normal_write_return_is_runtime_error`; `test_positive_short_output_writes_are_completed`; `test_marker_io_failure_cannot_be_returned_as_success`; `test_independent_consumer_detects_coherent_corruption` | green (finite) |
| EP13 | Dependency exception identity and invalid-normal-return distinction; no successful partial result. | `test_dependency_exception_object_is_not_translated`; `test_bad_normal_return_is_runtime_error_not_failed_row`; `test_output_failure_never_publishes_complete`; `test_fresh_process_limits_and_hash_seeds` | green (finite) |
| EP14 | Three actual tiny inputs under both telemetry routes; repeated finite composition counted separately. | `test_bounded_actual_telemetry_integration_not_full_campaign` | green (finite) |
| EP15 | Fresh-process synthetic-clock/non-timing checks under hash seeds 1/73 and digit limits 640/4300. | `test_fresh_process_limits_and_hash_seeds` | green (finite) |
| EP16 | Coherent-corruption consumer tests plus materialized production-source and guard-isolated integration audit. | `test_independent_consumer_detects_coherent_corruption`; separate Phase E `SOURCE_AUDIT.result.json`: 35 source/wrapper mutants and seven other family obligations, distinguished below | green (finite) |
| EP17 | Complete actual local initial campaign plus independent stored-output/certificate/reference validation. | `test_completed_historical_output_is_read_only_not_retimed`; explicit local campaign process and independent `CAMPAIGN_AUDIT.result.json`, not a routine test side effect | green (finite) |
| EP18 | Routine regression does not start the full real campaign; historical owned outputs are read-only. | `test_bounded_actual_telemetry_integration_not_full_campaign`; `test_completed_historical_output_is_read_only_not_retimed`; `test_direct_script_fresh_process_help_and_usage_do_not_run_campaign` | green (finite) |
| EP19 | Historical exact missing-module RED; no skeleton production module or campaign existed at that transition. | Historical `TESTS_RED_CHECKPOINT.txt` / `TESTS_RED_AUDIT.json`; the later import-only authorization does not rewrite this record | green (historical RED) |
| EP20 | Scoped identities, extensible aggregates and explicit limits on empirical and theorem claims. | `test_scoped_fixture_and_source_identities_do_not_freeze_future_roots`; `test_valid_foreign_aggregate_and_cwd_independence`; `test_default_paths_use_source_root_not_cwd`; `test_completed_historical_output_is_read_only_not_retimed` | green (finite) |

### Actual campaign, reference comparison and timing boundary

The successful local initial invocation consumed all 655 Unit 20 recipe
identities, preserving numerical/payload duplicates and the known Empty case.
It executed 1,310 untimed warmups and 3,930 measured samples, for 5,240
`solve_with_telemetry` calls. Both routes were executed for every recipe.
Each call built and checked its certificate against the same retained input
bytes before a successful row was written: 5,240 per-call checker invocations.
The deterministic alternating schedule and three measured repetitions per
route follow D21-E5; they are not random sampling or adaptive stopping.

The historical `results/unit21-v1/` contains 1,317 artifacts: `run-info.json`,
`warmups.jsonl`, `runs.jsonl`, `summary.csv`, `branches.csv`, `comparison.csv`,
`COMPLETE.json`, and 1,310 files in `certificates/`. The three CSVs contain
1,310 summary rows, 5,232 branch rows and 655 paired comparison rows. The
Empty recipe produces no fictitious branch records. Each recipe/route
certificate was stored from its verified warmup and matched by subsequent
repetitions. A completion filename alone is not independent validation.

The separate artifact auditor validated the complete raw records, table
reductions, ordered schedule, repeated diagnostics, provenance and output
ledger. It rechecked all 1,310 stored certificates and compared every recipe's
reported value/Empty status with the independently fixed Phase C expectations.
Those 1,310 checker invocations are additional audit work, not timed samples.
The artifact audit made zero production solver calls and did not rerun the
campaign. The expectation source is the earlier independent catalogue, not
the producer, a second agreeing solver or C0 checker acceptance alone.

C0 acceptance establishes admissibility and attainment, or the valid Empty
case, within its existing contract. Independent finite optimum comparisons
are distinct evidence. Same-route result, AlgorithmStats and certificate
bytes agree across repetitions; cross-route numerical equality uses positive-
denominator cross multiplication. Distinct admissible raw pairs/witnesses
with equal values are permitted across routes, including the preregistered
synthetic `2/2` versus `4/4` trap. No tolerance or silent normalization is added.

Measured nanoseconds cover exactly one telemetry-enabled solve call, including
its validation/recording and returned telemetry construction. Input decoding,
Instance creation, source hashing, metadata discovery, certificate construction/
checking/serialization and output/table work are outside that interval.
Warmups contain null timing fields and no clock samples; a measured zero is
retained. Metadata seconds and clock resolution are diagnostic floats, not
solver arithmetic or counter values. This is instrumented-solve time, not
whole-command, uninstrumented, backend-only or verification time.

Run records preserve all route-native fields, four ordered nonempty branch
records, nonbranch work, 25-field WorkStats objects and separate output widths.
Counter summation and peak maximization retain their closed telemetry semantics.
Reports are rederived from persisted measured rows without a second solver
pass. Three-sample time medians are exact integer middle order statistics;
structural counters are not summed over repetitions. Large integer fields
remain canonical unquoted decimal tokens through bounded conversion chunks.

### Synthetic tests, bounded real composition and adversarial scope

The scripted full-schedule test exercises 5,240 call identities with synthetic
dependency returns and clocks; it is not another measured initial campaign.
The bounded real-integration test executes three registered tiny inputs,
including Empty and two nonempty cases, under both routes and all four rounds:
24 actual telemetry calls; the other 5,216 scheduled calls in that test are
scripted. These per-test counts must not be added as unique corpus recipes or
misreported as the initial campaign's measured samples. The giant-record and
fresh-process tests exercise a 4,401-digit token and limit/hash-seed combinations
without changing interpreter settings. Injected resource exceptions do not
establish physical resource exhaustion or a measured support frontier.

The independent source audit materialized and detected 35 production-source/
wrapper mutants at their intended guards, with valid pristine controls and no
surviving mutant. Six additional declared families are tied to actually passed
frozen-test integration cases; a seventh independently rejects a synthetic
three-input subset masquerading as the complete campaign. Together these
account for all 42 preregistered fault families. This is not 42 production
mutants. Variant files, guard reports and failed-attempt provenance remain
private audit evidence. The source audit uses synthetic dependencies and blocks
real optimizer calls; it supplies fault-detection evidence, not runtime data.

Import provenance and candidate-byte conservation were checked throughout.
The historical campaign source fingerprint covers the fixed 22 source paths,
not documentation, tests, outputs or the mutable aggregate MANIFEST. Therefore
this documentation-only append does not reidentify or retime the stored run.
Source-content identity is not represented as an already-created implementation
commit. Output completion is not a power-loss durability or hostile-race claim.

### Observed look-ahead coverage, not a performance acceptance gate

The actual Mac `summary.csv` has 276 recipes with n > 3, hence 552 solver rows.
The independently reported grouping is:

| Stratum | Recipes per route | Standard nonzero / zero rows | Accelerated nonzero / zero rows | Accelerated maximum | Sum over Accelerated summary rows |
|---|---:|---:|---:|---:|---:|
| `struct-*` | 120 | 0 / 120 | 0 / 120 | 0 | 0 |
| `bits-*` | 120 | 0 / 120 | 0 / 120 | 0 | 0 |
| `seeded-*` | 36 | 0 / 36 | 6 / 30 | 2 | 8 |

Structural and bit-sweep recipes did not exercise look-ahead; their names,
larger-than-micro n or Accelerated route label do not establish such coverage.
The six nonzero observations are:

| Recipe | Accelerated lookahead_queries | Standard oracle_calls | Accelerated oracle_calls |
|---|---:|---:|---:|
| `seeded-n06-b00001-falternating-s01` | 1 | 14 | 12 |
| `seeded-n06-b00001-falternating-s73` | 1 | 14 | 12 |
| `seeded-n06-b00008-falternating-s01` | 1 | 16 | 13 |
| `seeded-n06-b00064-falternating-s01` | 1 | 16 | 13 |
| `seeded-n08-b00008-falternating-s73` | 2 | 17 | 14 |
| `seeded-n08-b00064-falternating-s73` | 2 | 17 | 14 |

The eight-query sum is across summary rows, not across all repeated executions.
The paired oracle-call differences on these six observed active recipes have
median -3. This is an observed comparator statistic, not an engineering gate,
a theorem, a timing conclusion or an ablation isolating look-ahead's causal
contribution. Zero-look-ahead rows may also show fewer Accelerated oracle calls.
All zero, unfavorable and mixed observations remain in the historical output.
Paper-level hypothesis interpretation and additional analyses are separate
from this conformance record; private planning material is not made governing
source or a gate dependency. No new experiment or larger-n family is adopted here.

### Exact identities, controlled recovery and remaining lifecycle

| Bound artifact | SHA-256 |
|---|---|
| `exactfrac/experiments.py` | `f01d15aedd917c84245a6562ca26b92e76e518f4e56a860c705572e631ffaf2c` |
| `experiments/reproduce.py` | `ccb404a25f63d34413c4a43a8512056e6195b66f824734a439da0305b03b3577` |
| `experiments/README.md` | `f0373c42b18dcfcd6e08aae345e2f050cf58853da34044a874829c268ec219a2` |
| `tests/test_experiments.py` (authorized import amendment) | `089e68b9f2cea523afc8c85b658ee179c9602572b5fba6c34888d62873e7c0cb` |
| `IMPLEMENTATION_GREEN_AUDIT.json` | `caacc57840ff55326c8c288ec1359f9acba502e6f14c8089995a3e83a7bf0ce6` |
| `IMPLEMENTATION_GREEN_CHECKPOINT.txt` | `b21ac1beff10c1da179c3724f29fc9cd27630891ac0e6b5ffa40eeff145c13cb` |
| `LOOKAHEAD_OBSERVATIONS.json` | `3799d226f0fd56ddeb02778904cb7d62df966d18b9033f7f87c6efc4e7b80a8a` |

The successful private checkpoint is
`unit21-experiments-implementation-r1-recovery-r2/live-green-recovery.9qejw_f3/`.
The amended test Git blob is `2fd2ffa90cad789287bbddbd91b3b6fdaa02c2f8`.
The original R2 test hash
`7c33b6b1080cc87996d614add94da9f9d257f2823ec22eea18e0ce76149e5679`
remains a valid historical RED identity, not the current test identity.

The original production application completed targeted tests but its helper
rejected the recorded pytest argument expansion. Recovery R1 authenticated
that record and stopped before the campaign at an import-grouping Ruff error.
The author then explicitly authorized only moving the pytest import before
the dotted first-party import with one intervening blank line. Recovery R2
recorded the one-byte-size amendment, preserved all other test bytes and both
failed attempts, and required fresh tests under the new identity. No production,
configuration or predecessor change was made. The old targeted run is not
reclassified as verification of the amended test. The deferred first-party
classification policy remains for later authority, not a configuration change here.

Fresh Mac GREEN verification was 187/187 targeted and 4,699/4,699 full cases
(4,512 inherited plus 187 new), using Python 3.14.6, pytest 9.1.1 and Ruff
0.16.5. The inherited corpus parametrization warning was retained, not suppressed
or repaired. It is not evidence of compatibility with a later pytest version.

Phase G changes only `docs/CONFORMANCE.md`, appending after all 189,554 prior
bytes. Its application authenticates the original GREEN records rather than
rewriting them against this later document. Fresh targeted/full tests and
repository Ruff run with the appendix present. They preserve and validate
historical output instead of starting another initial campaign. All other
2,028 candidate files, the 708-entry index, references and prior evidence remain
unchanged. The 2,029-file total is a phase-local snapshot, not a permanent ban
on future authorized additions.

Complete-candidate staging, mandatory staged-tree isolation, local implementation
commit/postcommit checks and remote closure still follow. This entry is not
Unit 21 remote closure. Final private BUILD/LEARNING notes are neither produced
nor inspected in this phase. Unit 22 release/minimum-interpreter/privacy/licensing
work and any separately authorized follow-up campaign remain outside its scope.

Finite tests and this one campaign do not establish universal correctness,
strong polynomiality, a finite wall-clock law, general scalability, constant
memory, a practical tractability threshold or application-domain suitability.
Event counters are not every arithmetic operation; integer peaks are not memory
measurements. No external baseline, explicit-copy speedup, verification-overhead
claim or global theorem promotion is introduced. Historical scoped run artifacts
are preserved without freezing the entire `results/` or `experiments/` aggregate.

## Unit 21B — irregular follow-up and balanced Main R2: finite engineering conformance

This append records completed source/test validation and independently audited
pilot/main execution under DESIGN §15 (D21B-I1–I16), its adopted §16 revision
(D21B-R2-I1–I8), and TEST_PLAN §§49–51 (IR1–IR24 and IRR2-1–IRR2-8).
It preserves every earlier byte, theorem row and status. This is an engineering
conformance record, not a new mathematical source label, theorem promotion,
authority amendment or assertion of Unit 21B remote closure.

### Implemented scope and prospective design history

`exactfrac/corpus_irregular.py` provides the pure finite `recipe_ids`,
`generate_instance` and `build_corpus` interface. The complete owning suite
`instances/unit21-v2/` retains all 1,200 registered inputs: 240 p-token and
960 s-token recipes, including all n=16 inputs. The aggregate MANIFEST extension
preserves the original 655 entries. Earlier independent mathematical references,
including the original 200-recipe exhaustive-vector subset, are preserved;
retained-witness checks are not a new exhaustive enumeration.

`exactfrac/experiments_irregular.py` supplies the separate guarded experiment
runner, with `experiments/reproduce_irregular.py` and
`experiments/README_irregular.md`. The closed Standard and Accelerated solvers,
telemetry, certificate construction and independent checker are consumed, not
replaced. No new solver, backend, arithmetic rule or CLI subset override is added.

The 21B stratum was designed after observing that `unit21-v1` produced Accelerated
look-ahead events on six seeded recipes and none on the structural or bit-sweep
strata. That original study is reported first and its 1,317 result files remain
unchanged. After the complete disjoint pilot, the September 26, 2026 revision
narrowed main execution on operational-cost grounds, not pilot route outcomes.
The author separately dated F7 September 27, 2026 and authorized main execution.
The revision date and the F7 authorization are distinct records.

### Frozen consumers and observed validation

The final Mac implementation R3 validation observed **2,333/2,333 targeted** and
**7,032/7,032 full** cases, with no collection errors, skips, deselections or
xfails. Both changed-Python candidate Ruff preflights and repository Ruff passed
under Python 3.14.6, pytest 9.1.1 and Ruff 0.16.5. The single inherited corpus
parametrization warning was retained, not suppressed or repaired. These are
pre-CONFORMANCE validation results, not claimed post-append test results.

| Frozen consumer | SHA-256 |
|---|---|
| `tests/test_corpus_irregular.py` | `3c083135c8321c676437ab5103ad72bd0e46bb0b2ae7eda2ab1975ae40f0a1c4` |
| `tests/test_experiments_irregular.py` | `1112ba023339b857a7ee912843d1c2fc52ed4d973f525c90001d1db0a0c1fe57` |

The historical two-module collection RED is preserved; it is not a current
failure. Authorized consumer revisions retain their separate identities,
including the `_Script.instances` observation and the later encoding-only
correction. No historical result is relabeled as validation of later bytes.

In the following crosswalk, **C** denotes the corpus consumer above and **R**
the runner consumer. Named functions are evidence locations, not collected-case
counts. Coverage is finite and remains subject to the stated audit distinctions.

| Obligations | Exercised scope and actual evidence locations |
|---|---|
| IR2–IR6; IRR2-1 | Registry, exact payloads, digest boundaries and complete owned inventory: C `test_each_exact_payload_recipe_and_registered_input_identity`, `test_isolated_digest_overrides_consume_registered_boundary_fixtures`; R `test_r2_selection_preserves_owned_inputs_and_original_schedules`, `test_r2_excluded_n16_input_still_validated_before_main`. |
| IR7–IR8; IRR2-5 | Independent retained mathematical references and non-tautological geometry: C `test_retained_endpoint_attainments_all_recipes_without_optimum_resolve`, `test_fixed_vector_subset_retained_censuses_and_witnesses_not_reenumeration`; R `test_all_registered_input_geometries_without_optimization`, `test_runner_rejects_native_valid_graph_dependent_h2_fault_at_actual_return`. |
| IR9–IR11 | Public boundary, imports and path/ownership rejection: R `test_main_python_argument_types_fail_before_activity`, `test_source_import_boundaries_and_wrapper_are_separate_from_observations`, `test_forbidden_output_paths_are_not_repaired_or_overwritten`. |
| IR12–IR13; IRR2-2 | Exact revised schedule, scripted full execution and solve/cell timing boundaries: R `test_registered_schedules_are_independently_reconstructed`, `test_full_runner_schedule_is_scripted_not_a_real_campaign`, `test_timing_observer_detects_one_excluded_operation`, `test_pilot_start_observer_rejects_only_late_start_after_pristine_control`. |
| IR14–IR15 | Native fields, certificate semantics, strict wire records and bounded real composition: R `test_independent_nested_schema_single_faults_follow_pristine_controls`, `test_scripted_cross_route_distinct_attaining_raw_pairs_succeed`, `test_future_bounded_real_micro_composition_only`. |
| IR16, IR19; IRR2-3 | Raw-to-table reconstruction, completion inventory and preserved failures: R `test_coherent_table_and_completion_hash_mutants_fail_independent_derivation`, `test_coherent_output_omissions_reach_mode_inventory_before_lookup`, `test_output_native_failure_preserves_failed_attempt`. |
| IR17–IR18; IRR2-4–IRR2-5 | Revised 17/18-cell boundaries, exact median rules and complete H3 triples: R `test_h5_all_registered_boundaries_and_timing_invariance`, `test_h3_fixed_support_series_and_separate_exact_arithmetic`, `test_r2_synthetic_pilot_bytes_and_h3_series_remain_independently_bound`. |
| IR20; IRR2-6 | All 143 versioned fault families: separate completed implementation audit on source copies, with materialized faults, integration controls and declared source/phase/claim reviews distinguished; U21BF093 evidence described below. |
| IR1, IR21–IR24; IRR2-7–IRR2-8 | Historical prefixes, exact transition scope, full pilot/F7/main sequence and retained source lineages: completed authority/reference/implementation and campaign records; independent pilot/main lineage controls; later closure remains separate. |

The 143-family implementation audit passed with zero optimizer calls. This is
not 143 executable producer-mutant kills. Its credited cases retain intended-
guard attribution and passing pristine controls. U21BF093 reached the intended
timing guard, propagated the same exception object and passed pristine controls
before and afterward; a secondary cleanup failure was not credited instead.
Original and superseded failure evidence remains preserved.

Scripted full schedules and synthetic boundary fixtures are not performance
measurements. The bounded real micro-composition test uses only the two specified
preexisting inputs under both routes, four actual calls per test execution.
Those calls and inherited regression behavior are not additional irregular
pilot/main samples. The campaign launcher authenticated the completed tests,
Ruff and declaration audit; it did not repeat those executions as a campaign.

### Completed pilot, source lineage and actual main execution

The original pilot covered all 48 cells, 240 p-token recipes and 480 actual
route calls, with 480 certificates and 485 output files retained under
`results/unit21-v2-pilot/`. This includes all twelve n=16 cells: 60 pilot
recipes and 120 calls. Its independent certificate, reference-value, geometry
and table checks passed. It remains labeled pilot evidence, including
unfavorable observations, and is never pooled into main results or rerun by
routine validation.
In this retained pilot evidence, Accelerated's solve time exceeded Standard's
on 40 of the 60 n=16 recipes, as recorded in
`results/unit21-v2-pilot/pilot-solves.csv`; these single-pass pilot
observations are never pooled with main results.

The original 25-source pilot snapshot is retained as the inert archive
`experiments/provenance/unit21-v2-pilot-r1-source.zip`, outside the pilot output
root and outside the live source roster. The two actual source fingerprints are:

- Pilot R1: `01428190bdac17bbde27aba5682503ff93a57bb0925e09fd4ec392a0a517469f`.
- Main R2: `9c1fea59193ac3c2772e18004a6d73abdb77c6d3bb7c8430bcde5ee55d815b26`.

The same 25 live source paths identify main; the scoped runner revision changes
its fingerprint, not the historical pilot's identity. Documentation, tests,
outputs and the inert archive are not code-fingerprint members. This append
therefore does not reidentify either run. Source fingerprints are not claims
that the final implementation commit has already been created.

After F7, one actual main invocation completed all 36 cells and 720 original
s-token recipes at n=6,8,12, tau=64,128, b=1,8,64 and both capacity modes, with
20 seeds per cell. It retained both routes, one warmup and three measured
repetitions, the fixed ASCII order and alternating route order. All 1,200 owned
inputs were validated; the 240 n=16 s-token inputs were not executed.

| Main evidence | Observed count |
|---|---:|
| Warmup records / measured records | 1,440 / 4,320 |
| Successful telemetry calls and per-call certificate checks | 5,760 |
| Distinct recipe/route certificate files | 1,440 |
| Summary / branch-summary / comparison / coverage rows | 1,440 / 5,760 / 720 / 36 |
| Output files including `COMPLETE.json` | 1,449 |
| Nonself completion-ledger entries | 1,448 |

The independent result audit additionally checked 5,760 certificates against
retained calls, compared all 5,760 values with each of the two saved Phase C
optimum references, and checked 23,040 branch-accounting records. It verified
4,320 same-route measured repeats against their warmup baselines, 720 cross-
route value comparisons, all source/input bindings and the full output ledger.
It reconstructed `summary.csv`, `branches.csv`, `comparison.csv`, `coverage.csv`
and `findings.json` from retained records. No solver was called by that audit,
and no optimum enumeration or timed campaign was repeated.

C0 acceptance establishes admissibility and literal attainment; independent
optimum-reference agreement is separate evidence. Distinct valid attaining
raw pairs across routes remain permitted. Same-route result/telemetry and
certificate consistency are required, without normalizing raw-pair semantics.

Measured integer nanoseconds cover the single `solve_with_telemetry` call and
its returned telemetry construction. Input/geometry work, metadata, certificates,
verification, hashing, serialization, output and reporting are excluded.
Warmup timing is null, not a zero measurement. Pilot cell intervals are separately
defined operational measurements. Neither the planning proxy nor the sum of
measured solve times is promoted to whole-invocation wall time. No timeout,
retry, resume, favorable-repeat selection or interpreter-limit change was added.

### Finite findings, not new acceptance rules

H2-prime identities held exactly for every retained main call. This checks the
specified descriptor, feasible-family, query-multiplier and sum/max accounting;
it does not prove universal complexity or strong polynomiality.

Under the frozen D21B-R2-I4 rule, H5-prime is **supported**: 509 eligible recipes,
36 of 36 active cells against the threshold 18, and exact eligible paired
oracle-call median **-1**. There are no zero-event cells. The observed outcome
is not inferred from timing, recipe names or pilot data.
On the 509 eligible main recipes, Accelerated used fewer, equal, and more
oracle calls than Standard on 303, 87, and 119 recipes, respectively
(eligible wins/ties/losses, counting each recipe once). Within-cell medians
of (Accelerated minus Standard oracle calls), using only each cell's eligible
recipes, are negative in 24 cells, zero in nine, and positive in three:
`irregular-n12-t064-b00008-falternating` (+2),
`irregular-n12-t064-b00064-frandom` (+1), and
`irregular-n12-t128-b00008-falternating` (+1).
The negative cell medians are concentrated at n=6,8 (21 of the 24);
the remaining three negative-median cells have n=12 and b=1, while all eight
n=12 cells at b=8 or 64 have nonnegative eligible medians. These descriptive
within-cell medians are not an additional support rule; the pooled
D21B-R2-I4 verdict remains unchanged.

| Main comparison over 720 recipes | Accelerated lower | Tie | Standard lower |
|---|---:|---:|---:|
| Oracle calls | 514 | 87 | 119 |
| Median of three measured solve times | 491 | 0 | 229 |

All 59 recipes with fewer Accelerated oracle calls but no faster median time,
all 119 recipes with more Accelerated oracle calls, and both ten-entry slowest/
largest-integer lists remain retained. These are recipe-level comparisons;
repetitions are not additional independent problems or sums of structural work.
Unsupported or unfavorable observations are valid results, not reasons to
repeat or select data.

All 240 matched three-bit H3-prime series per route are present with matching
support. The separately prescribed slopes and route-specific H3-prime decisions
have not been computed by the campaign audit or this entry. Synthetic estimator
checks and recorded integer maxima are not an empirical H3-prime verdict.

### Evidence anchors and remaining lifecycle

| Saved evidence record | SHA-256 |
|---|---|
| Main R2 implementation R3 audit | `7a6eff9a4a9c02729efb53e184b4d0dd81040abf29a207a274c3a13a2ac6aa12` |
| Revised 143-family implementation audit | `7db59c87ff9fc578d42d605188d974ce0777700b6e8066a4f9e14e2ed2b14821` |
| Independent main-result audit | `26f3162e8b1107d9c51df4a92db285eb7c672f404569151926e0c675699fec8b` |
| Main R2 campaign R2 audit | `4a5f54e76bcfb68bb35ea14729e155a12fbaf1e3735db6970a6d15bf37f50503` |
| Main R2 campaign R2 checkpoint | `3065f6726c061cd931e3e4124d10346738feab0a79dff2c6c97a537975096169` |

These anchors identify saved evidence; they do not incorporate private handoff
files into the repository. A review archive is not a complete live-state or
historical-handoff backup. Actual predecessor records remain authenticated at
the applicable Mac transition rather than inferred from these hashes alone.

At campaign completion, HEAD remained oracle commit
`8b9ab9d247efb2bb5500ae8c81e42a79d6059281`; its tree was
`076dfd9589f088c07e9f67107b61a071b338ba77`. The index was unchanged, the complete
5,170-file candidate remained unstaged, and neither a final implementation
commit nor remote closure had occurred. These are recorded phase-local counts,
not permanent limits on authorized future repository contents.

Phase G is limited to appending after all 209,137 prior CONFORMANCE bytes.
Its application must authenticate the successful evidence and conserve every
other file. Fresh targeted/full tests and repository Ruff with this appendix
present are recorded separately; no post-append validation PASS is asserted
here. The documented resolved TMPDIR spelling remains scoped to verification
subprocesses, including later isolation/postcommit checks, without weakening
path guards or changing global settings.

Complete-candidate staging, staged-tree isolation, local commit, postcommit
validation and remote closure still follow under the existing lifecycle.
Routine checks read preserved pilot/main/historical results and never retime
them. No new gate, private-note dependency, source/test/configuration edit,
Unit 22 work or public release is introduced.

Finite results characterize this deterministic stratum, not all graphs at
these orders. No universal correctness or speedup, asymptotic or practical
frontier, isolated causal look-ahead effect, total-memory bound, verification-
overhead result, explicit-copy comparison or external-solver claim is added.
Earlier theorem statuses remain unchanged.

## Unit 22 — observed private release-engineering conformance, October 6, 2026

This append records the implemented and observed engineering scope under DESIGN
D22-R1--R17 and TEST_PLAN RL1--RL16. It adds no mathematical theorem row and
changes no earlier row, status, source hypothesis or empirical conclusion.
Finite tests, release inspections, manual reviews and artifact observations
are separate forms of evidence. None supplies a universal mathematical proof,
legal clearance or permission to publish.

### Implemented scope and fixed source boundaries

The standard-library release auditor supplies the registered read-only tree,
archive and accessible-history inspections. Its owning R6 consumer contains
54 top-level test functions and collected 188 parametrized cases in the
reported native GREEN runs. These 188 cases are additional to the 7,032
inherited cases; each full candidate run therefore collected 7,220 cases.
Repeated executions do not create additional distinct tests or experiments.

The implemented release scope also includes the standard MIT license, reviewed
README and citation, source-distribution manifest and evidence report. The
packaging version is 0.1.0. The pyproject transition changed only its version
literal; the CLI consumer changed only the three adopted static digest slices
for README, CITATION and pyproject. The other 38 values, all 41 dictionary keys
and all other CLI-consumer bytes were preserved. The solver/verifier code,
mathematical contracts, corpus, retained experiment outputs and executed-source
fingerprints are unchanged by this unit's release implementation.

| Exact implemented or adopted object | SHA-256 |
|---|---|
| `release_audit.py` | `d2a6ee5391292aedcdeb36e2d098956dc56aaf62d77faa212719ea269903c9fa` |
| R6 `tests/test_release.py` | `87474f5c91943203cc8ae615d91705dc4da8e8b22b76efa56236c779c99220cc` |
| Current `docs/ORACLE_CATALOG.md` | `f258c45a1b405e89de3e8704dab6bc8d0474126dcad49defe2f2ea0a4df54661` |
| Adopted and applied notice report `docs/RELEASE.md` | `47ba7161c30ab629b86583bfac42e094a57a61523dd0bcf2f720621bda24f178` |
| Private 195-row disposition ledger | `6fd5427f3c7734e098df4795d07f72d37c2ffb129ccf6501cfdc7343557e2924` |

These identities name already-existing objects, not a future commit or this
append's own identity. The private ledger and raw execution records are not
added to the repository. Their complete bytes and the saved predecessor
records remain subject to authentication in each later controlled transition.

### Independent references and the tests-first boundary

The consumer authenticates the 30 objects in the committed U22-C-CORR2 namespace
and its 29-entry reference index. It selects the owned catalogue span, reads
payloads by marker byte count and digest, decodes base64 payloads, and rejects
span damage rather than consuming later appendices. Earlier reference versions
remain preserved as history. The corrected nested-depth constructions, source
profile, manifest and generated setup.cfg allowance are the adopted references;
no archive member was removed and no packaging backend was patched to obtain
acceptance. Provenance-positive test bytes are constructed at run time from
the registered encoded value, not stored as an added plaintext fixture.

The completed R5-to-R6 consumer transition observed the required direct
`import release_audit` failure at line 37: ModuleNotFoundError naming
release_audit, exit 2, one collection error, and zero new cases collected.
The inherited suite passed with that absent-producer consumer excluded.
Only the subsequent implemented candidate provides producer-dependent GREEN.

R6 preserves the real invalid-byte filename construction when it succeeds.
Only an observed EILSEQ construction failure selects a controlled directory
entry on a real directory; the auditor still executes, and unsafe target reads
remain prohibited. The non-UTF-8-name case passed in the native E5 candidate
runs. Their recorded census does not identify which construction route was
taken, so this entry does not infer the route from the host name or platform.

### Engineering obligations and their evidence

All test references below are in the exact R6 `tests/test_release.py` unless
a different path is stated. Named tests identify bounded executable checks;
manual or artifact observations are not replaced by synthetic test fixtures.

| Obligation | Implemented check or separate evidence | Recorded scope |
|---|---|---|
| RL1; D22-R1 | Saved baseline, authority, reference and successive application records authenticated by the controlled transitions | Phase A's 7,032-case result remains starting evidence, not a minimum-interpreter or final-artifact verdict. |
| RL2; D22-R2/R10/R16 | Actual missing-owner RED, followed by the implemented R6 targeted/full runs | Tests-first ordering observed; no conditional import or producer stub supplied the RED. |
| RL3; D22-R3 | `test_reviewable_copyright_is_reported_and_not_silently_removed`; inspected license identities; adopted bounded source/notice review | Existing MIT notice and mathematical citations retained; no additional notice identified within the adopted review scope. |
| RL4; D22-R4 | Recorded isolated CFF validation accepted by the author; metadata identities and version cross-checks | Schema/content review is distinct from the exact-byte consumer checks; no new DOI, publication date or public-release claim. |
| RL5; D22-R5 | Adopted README contribution-account review | Scope and provenance follow the controlling account; the pre-build Exit Test and Unit 21B fault-family scope remain distinguished. |
| RL6; D22-R6 | Adopted source-status and claim crosswalk review, including the author's recorded recheck | Source/theorem wording is traceable to its authority; a consistency review is not a new proof. |
| RL7; D22-R7 | Adopted original-study and Unit 21B reporting review | Pilot and main remain separate; no retiming, pooled claim or new H3-prime result. |
| RL8; D22-R8 | `test_exact_frozen_records_and_repeat_determinism`; `test_tree_records_reconstructed_from_raw_fixture_bytes`; source inventories and conservation | Ordered records and independent reconstruction checked; current-state conservation is separately observed by the application gates. |
| RL9; D22-R9 | `test_history_frozen_examples_match_independent_loose_objects`; `test_history_uses_only_registered_read_only_git_commands`; actual history inspection and manual dispositions | Accessible-history coverage was complete for the inspected predecessor; no history rewrite or blanket scanner exemption. |
| RL10; D22-R10 | `test_registered_archive_structural_cases`; `test_tar_unsafe_names_and_types_are_never_extracted`; `test_tree_nonregular_entries_retain_coverage_without_reading_targets`; `test_registered_finite_limit_cases` | Unsafe paths/types, nonregular entries, nested containers and finite resource ceilings are explicitly represented; incomplete coverage cannot become a clean result. |
| RL11; D22-R10 | `test_fresh_process_import_has_no_io_commands_or_nonstdlib_imports`; `test_native_read_exception_keeps_object_identity`; `test_native_subprocess_exception_keeps_object_identity`; `test_no_filesystem_write_network_or_execution_during_inspection` | Import purity, errors, dependency propagation and nonmutation checked within the registered interface. |
| RL12; D22-R10/R11/R15 | `test_independent_record_reader_rejects_schema_and_accounting_faults`; `test_coherently_rehashed_false_records_fail_independent_ground_truth`; `test_strict_reference_json_rejects_duplicate_decoded_keys_and_nonfinite_tokens` | Record syntax, accounting and independently derived expectations checked; hashes alone are not the reference oracle. |
| RL13; D22-R12 | `test_independent_distribution_profile_checker_rejects_false_inventory`; actual E5 sdist/wheel builds, archive checks and installed-wheel smokes | Observations apply to their exact historical source manifest and artifacts; later report-bearing artifacts require their own binding. |
| RL14; D22-R13 | Actual clean-source runs under Python 3.11.17 and 3.14.6, plus installed-origin observations | Both targeted/full native runs passed at the E5 source identity; relevant later source changes are not silently included in that result. |
| RL15; D22-R14 | `test_frozen_metadata_pin_transition_and_pyproject_single_literal`; `test_metadata_and_static_pin_mismatches_cannot_be_accepted`; `test_installed_release_metadata_is_the_coupled_frozen_postimage`; `test_static_pin_dictionary_rejects_an_actually_computed_value` | Exactly three static pin substitutions and the single version literal; no broader test or metadata rewrite. |
| RL16; D22-R15--R17 | `test_review_references_and_report_template_do_not_claim_future_execution`; adopted report and external execution records | Noncircular evidence and publication boundaries retained; final candidate/artifact, H and committed-render obligations remain incomplete. |

### Observed native validation and bounded install evidence

The successful E5 execution used native arm64/macOS 27.0, actual CPython
3.11.17 and 3.14.6, pytest 9.1.1, and repository Ruff 0.16.5. Locked acquisition
and separately created environments were outside the canonical checkout;
the development .venv was conserved. The dependency probes checked the actual
locked artifacts and installed metadata. The following are execution results,
not predictions from interpreter version declarations or fixture-only tests.

| Execution context | Targeted release cases | Full source cases |
|---|---:|---:|
| E5 external source, Python 3.11.17 | 188 passed | 7,220 passed |
| E5 external source, Python 3.14.6 | 188 passed | 7,220 passed |
| E5 applied development candidate | 188 passed | 7,220 passed |
| E5 populated-report development candidate | 188 passed | 7,220 passed |
| Subsequent applied R3 report | 188 passed | 7,220 passed |
| Subsequent applied notice-report R2 | 188 passed | 7,220 passed |

All eight complete E5 census records report no failures, skips, deselections,
xfails, collection errors or worker-guard errors. The later report gates
recorded the same targeted/full counts with their exact-roster acceptance
checks. Their supplied completion excerpts are not substitutes for reading
the saved full censuses in a subsequent controlled application. Full runs
retain the inherited parametrization deprecation warning from test_corpus.py;
that warning was not suppressed. These are repeated validation runs, not new
benchmark measurements or additional independent problem instances.

E5 built the sdist first and the wheel from a fresh extraction of that exact
sdist. It ran both registered examples, triangle-nonempty and single-edge-empty,
under both Standard and Accelerated in each of the two installed-wheel
interpreter environments, including silent certificate verification and import-
origin checks. These eight case/route/environment combinations are correctness
smokes, not performance experiments or a full wheel-contained research suite.

The historical E5 validation artifacts are:

- Source distribution: `952892bd031e5651cc9d2218d4db54f9f9107eb99bc003f299ec9ad14c3f3bc3`.
- Wheel: `e9853df49bdf0d8d13d2bd92cae2060b9e1744779a619b79c077191bfaca42de`.
- Source manifest: `e3553ad3c63e1d8b6440e50a19c0290154a425b6a6aa44029e0aa6ab303a6ff0`.

That sdist contains the frozen report template, not the later populated,
reviewed notice report or this CONFORMANCE append. Its identities and test
results remain historical and are not relabeled as final report-bearing
artifact evidence. Byte-identical rebuild reproducibility is not asserted.

### Inspection, manual disposition and notice scope

The E5 bundle records complete coverage and 195 review-level findings: 13 in
the candidate tree, 162 in accessible history, 17 in the sdist, and three in
the wheel. The author adopted all 195 full-identity decisions: 93 retained
for author attribution, 74 for approved contact, 11 for truthful provenance,
and 17 false positives. The exact private ledger remains unchanged; raw
sensitive context and named manual-review records are not copied here.

Both subsequent report applications recorded the same 13 complete tree-finding
records and zero new findings. A retained finding is not an uninspected object,
and resolved dispositions do not erase original scan results. No result is
extended automatically to an uninspected new blob, archive or future commit.

The eleven report-entry texts and the bounded distributed-source provenance
and notice conclusion are adopted. The review identified no additional
third-party notice within its stated scope; the author supplied the bounded
known-origin confirmation, with known exceptions requiring identification.
The standard MIT notice and mathematical citations remain. This is not an
exclusive handwritten-origin assertion, an applicable-notice waiver or legal
clearance. The review's stated limits and inherited observations remain intact.
The contribution account, original-study reporting and Unit 21B interpretation
are not rewritten by this release-engineering append.

### Preserved corrections and evidence anchors

The original Phase C reference-application failure remains STOP and its
one-LF separator correction remains a separate accepted transition. The later
reference corrections fixed depth/sdist membership and the allowed generated
setup.cfg member without rewriting original objects. The E2 dependency-probe
STOP and E4 filename-construction STOP remain separately preserved. Their
reviewed helper and consumer corrections precede successful E5; they are not
silently replayed, removed or converted into historical successes.

| Saved evidence record | SHA-256 |
|---|---|
| Successful E5 application audit | `438debddf88fea9c6471c64c495652056dd5b78cec134163fa7b262ba044ab00` |
| Successful E5 application checkpoint | `e9228f318599b0e4d1414689e172694709e3662b28954138d927c4844d32ab6b` |
| Applied R3 report audit | `ab06a3f5a8e5fe39c5a772950df35095d55684c79f7ada93c55772e2d9082960` |
| Applied R3 report checkpoint | `c3fa5db00a0c62dc63d3821552cc6b015bac059732b2c4ac67f2e50f4c27e4f9` |
| Applied notice-report R2 audit | `0d491e088e2e68803c32e2304ca6a966d2b4c85b9abd5f737d8feb1eeef87142` |
| Applied notice-report R2 checkpoint | `3f93902df651e8519edab4ae427c6187d776a3ca6b45af47bb52f99040244a96` |
| Preserved E2 STOP | `8441e1bfa03359157801008966e2ee291c073bf1e9bb9e10be467b79ef333bfa` |
| Preserved E4 STOP | `72df7624bd5c8d0a9daea39578d19352b14f0cc85c329ededac3f3032b1b0065` |

These anchors identify already-recorded evidence. This append does not claim
a new read of the live private records or substitute a displayed digest for
their authentication. At the latest reported completion, HEAD remained
`65e9d6289671e670bc41b37983579fde9a925694`, with committed tree
`db04e8accc701bd53aff74b7ec6fd65d7e0c31a1`, 5,170 tracked files and the
five intended untracked release/test files; the complete 5,175-file candidate
remained unstaged. These are phase-local counts, not permanent file limits.

### Remaining lifecycle and non-promotion

Phase G is limited to appending after all 224,956 existing CONFORMANCE bytes.
Its later application must authenticate the actual completed notice-report
checkpoint and current state, conserve every out-of-scope file, and record
fresh targeted/full/Ruff, import and applicable inspection observations with
this appendix present. No post-append validation result is asserted here.

F's source/import/nonmutation review remains part of E's checkpoint, not a new
phase. H retains separate exact-candidate staging, index-tree export and
isolation, same-tree commit, postcommit validation and private remote closure.
The affected final source-distribution/interpreter evidence must be refreshed
for the exact report-and-conformance-bearing source; a prior hash or successful
run does not cover relevant source changes. Final artifact and commit bindings
are recorded externally under D22-R15, without editing a tested report to
claim its own future identity or endlessly relabeling older archives.

The eventual committed-README front-page observation remains pending; the
October 3 candidate Preview is not substituted for it. Readiness remains
INCOMPLETE until the remaining applicable obligations are actually satisfied.
No stage, commit, push, new tag, visibility change, publication, campaign replay,
H3-prime analysis or private-note inspection is authorized by this entry.
