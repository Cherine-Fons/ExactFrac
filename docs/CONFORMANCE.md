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
