# ExactFrac — Design of Record

Governing specification: see `SPEC_LOCK.md` (label-cited; never edited in place).

## 0. What ExactFrac is

An exact, certificate-producing solver for the compact positive-integer-multiplicity
modified set-pair density under the active hypothesis f(v) <= d_q(v) (d_q = the
multiplicity-weighted support degree; V2.1 never writes d_G), implementing `thm:main` of
the governing source. `StrongCompactMSPD` (`alg:global`) = unit-lower-bound baseline
(`lem:unit`) + the four transformed branches D0–D3, each solved by `SolveBranchStandard`
(`alg:standard-branch`) or `SolveBranchAccelerated` (`alg:branch`) with `ExactBranchMin`
(`alg:branch-min`) as the exact residual oracle + the direct H2 endpoint scan + exact
global comparison + compact witness reconstruction. Every nonempty result is a raw exact
quotient (N, D) with a compact witness (U*, y*), independently checkable by a verifier
that shares no code with the solver; the empty admissible family returns ((0,1), Empty).

Regime statement (kept candid, README and paper alike): ExactFrac targets compact-
multiplicity instances whose support graph is small enough for exact parity-family
enumeration, while permitting multiplicities with large binary encodings. Practical
support-size limits are established experimentally, not asserted in advance.
Cost structure per `ExactBranchMin` call, from the governing source (`thm:branch-oracle`,
`thm:GR`): up to R = 1 + 2mn + n + C(n,3) + 2m atomic families; each family is one
parity-cut minimization costing O((n+3)^2) ordinary minimum cuts (Goemans–Ramakrishnan);
each ordinary minimum cut is one exact max-flow. R counts FAMILIES, not flows.
Strong polynomiality bounds operation counts independently of the magnitudes of q and f;
exact-arithmetic wall-clock still grows with bit length. Measure both, separately.

## 1. Scope

Core (complete by the release-candidate gate, Sep 8):
  1. independent reference verifier
  2. shared cut / oracle infrastructure (Edmonds–Karp, sign routing, atomic families)
  3. ExactBranchMin
  4. SolveBranchStandard
  5. SolveBranchAccelerated
  6. StrongCompactMSPD
  7. certificate verifier
  8. CLI
  9. initial benchmarks (first families of the corpus, with counters)

Cut line if the runway shortens: 9 beyond its first family slips first; then 5
(SolveBranchAccelerated) — the standard route is independently strongly polynomial, so a
standard-only solver with certificate verifier and CLI is a theorem-grade v1, not a
consolation; 8 (CLI) and 7 (certificate verifier) are kept because they make the standard
solver usable and inspectable. Never cut 1–4, 6, 7.
Sep 8 is a RELEASE-CANDIDATE GATE, not an automatic release-candidate gate: see §12.

Out of core (Q4, after the core release audit): benchmark corpus design, the MPC
experimental campaign, any second solver (explicit-copy comparator), any max-flow
backend beyond the reference.

## 2. Rulings of record (adopted Aug 26, 2026)

R1  MPC alignment shapes interfaces and discipline only; it does not add deliverables
    to the core.
R2  Positioning: exact certificate engine; scaling axis = encoding length. Regime
    stated per §0; no numeric support-size claim ("tens of vertices" or otherwise)
    before benchmarks earn it.
R3  Dependency policy: the REFERENCE CORE (solver + verifier) is standard library only
    (`fractions`, `itertools`, `dataclasses`, `json`); the reference max-flow is written
    in-repo against `lem:ek`. This is a mandatory reference core, not a permanent
    prohibition: optional future backends are permitted behind the same exact interface
    (R9). Experiments may use extras, declared separately.
R4  Verifier isolation: `exactfrac_verify` imports nothing from `exactfrac`; enforced by
    a test that fails on any such import.
R5  Telemetry contract: every solve returns SolveResult (value, witness, certificate —
    mathematically minimal, independently checkable, carries no counters) and, separately,
    SolveStats (diagnostic counters and timings, §8). Certificates never depend on stats.
R6  File formats: versioned JSON for instance, certificate, run record. The instance
    format expresses the expanded encoding as the special case q_e = 1 for all e.
R7  License: MIT, ratified Aug 26 as the working ruling. Re-confirmed at the release
    gate (§12) with the substance stated explicitly: MIT permits unrestricted commercial
    and noncommercial use, copying, modification, and redistribution subject only to
    preservation of the copyright notice. No LICENSE file is needed while the repo is
    private; it is committed at the release gate.
R8  The governing .tex stays in the private archive, pinned by hash. Never committed.
R9  Max-flow sits behind an interface returning `MinCutResult(value, source_shore,
    stats)`. Backend contract: nonnegative exact integer capacities; directed-network
    semantics; exact minimum value; a deterministic source shore; the inclusionwise-
    minimal minimum source shore when the parity reduction needs it (`thm:GR` uses
    inclusionwise minimal lattice minimizers); augmentation and search counters; no
    backend objects leak upward. First and required backend: the in-repo Edmonds–Karp.
R10 Determinism: no algorithmic path iterates over a Python `set`; all enumeration
    orders are fixed and documented; generators take explicit seeds.
R11 Every commit is one unit; every unit has its test before its code is considered done.
R12 Language rule: outputs are a certified fractional lower bound with a witness;
    never "exact block count".
R13 Toolchain: minimum Python 3.11; pyproject.toml declares requires-python = ">=3.11".
    int.bit_count() is used with NO compatibility fallback. The release gate (§12) tests
    the minimum supported interpreter (3.11) as well as the development interpreter.

## 3. Package layout

    exactfrac/            solver (stdlib only)
      instance.py         canonical instance, aggregation, active check
      families.py         atomic families F(T, pi; I, O); enumeration per branch
      flow.py             Edmonds–Karp reference backend behind the MaxFlow interface
      oracle.py           ExactBranchMin
      branch.py           SolveBranchStandard, SolveBranchAccelerated
      solve.py            StrongCompactMSPD, run records
      certificate.py      certificate construction and serialization
      cli.py
    exactfrac_verify/     independent verifier (stdlib only, imports nothing from above)
      brute.py            exhaustive (U, y) search from the definition
      check.py            certificate verifier: admissibility + attainment
    experiments/          reproduction scripts (Q4)
    instances/            corpus with MANIFEST (paths + sha256)
    tests/
    docs/                 SPEC_LOCK, DESIGN, CONTRACT, CONFORMANCE, ORACLE_CATALOG
    pyproject.toml  README.md  CITATION.cff
    LICENSE               added at the public-release gate (R7)

## 4. Data model  —  RULINGS NEEDED, one per step, in this order

4.1 Graph representation  (RULED — adopted 2026-08-31)
    1. Vertex identity: external labels normalized to dense internal indices 0..n-1;
       external labels preserved only as optional I/O metadata (a label<->index map) and
       never used by the algorithm.
    2. Support-edge identity: IMPLICIT stable identity by position in the canonical
       serialized support-edge list; NO separate explicit id namespace. Construction:
       normalize every edge to u < v; aggregate repeated endpoint pairs; sort the support
       edges lexicographically by (u, v); the resulting position 0..m-1 is edge_ref. The
       serialized instance MUST preserve this canonical order, and the verifier MUST
       validate the order before interpreting any certificate edge reference. Rationale:
       a certificate is always checked together with its instance, so a second explicit
       id namespace adds state and validation obligation without adding mathematical
       information.
    3. Multiplicity: Python int; after aggregation every support edge satisfies q_e >= 1.
    4. f: immutable tuple aligned to dense vertex order; every entry a positive integer.
    5. Repeated unordered endpoint records: aggregated before the canonical instance is
       constructed (this is where q_e becomes the sum of parallel copies).
    6. Loops: rejected at construction, treated as malformed/invalid input -- NOT a failure
       of the active theorem hypothesis. Exact exception taxonomy deferred to the
       API-error definition step.
    7. Active condition: compute d_q from the aggregated support graph; explicitly require
       f(v) <= d_q(v) for every vertex; failure raises UnsupportedInstance.

    Representation invariants (RI) -- hold on every constructed canonical instance;
    asserted at construction, and re-validated by the verifier before use or before any
    certificate reference resolves:
    RI1. n >= 1; the vertex set is exactly {0..n-1}.
    RI2. m >= 1 -- nonempty support (CONTRACT: "finite nonempty loopless support graph").
    RI3. every edge (u, v) has 0 <= u < v <= n-1  (no loops; canonical orientation).
    RI4. the support-edge list is strictly ascending by (u, v) with no duplicate pair;
         edge_ref = position in this list, 0..m-1.
    RI5. q is a tuple aligned to edge_ref order; q[e] is a Python int >= 1.
    RI6. f is a tuple aligned to vertex order; f[v] is a Python int >= 1.
    RI7. d_q(v) = sum of q[e] over edges incident to v (each edge (u,v) contributes q[e]
         to d_q(u) and to d_q(v); loops are excluded by RI3); f[v] <= d_q(v) for all v.
    RI8. serialization preserves RI3-RI6 exactly; deserialization re-checks RI1-RI7 before
         the instance is usable, and canonical edge order is validated before any
         certificate edge_ref is resolved.

4.2 Shore representation  (RULED — adopted 2026-08-31)
    Every shore U (a subset of {0..n-1}) is internally a nonnegative Python int, with
    bit v set iff v is in U. Serialization stays the §9 sorted-index-list form (§9
    unchanged at the schema level; bitmask is strictly the internal representation).
    Invariants and operations of record:
    - full_mask = (1 << n) - 1.
    - every valid shore satisfies 0 <= U <= full_mask; no bit outside the vertex range
      may be set.
    - membership of v: bit v of U.
    - intersection / union: integer bitwise & / |.
    - cardinality: U.bit_count().
    - parity of |U intersect T|: (U & T_mask).bit_count() & 1.
    - complement is ALWAYS relative to the vertex universe: full_mask ^ U; bare Python
      ~U is never treated as a valid shore.
    - internal shore values are immutable and hashable.
    - serialization is exactly the §9 form: U is emitted as the sorted list of member
      vertex indices; deserialization validates indices and reconstructs the bitmask.
    - integer ordering MAY be used where a deterministic enumeration order is needed, but
      the bitmask representation imposes NO new mathematical tie-breaking rule; tie/argmin
      policy remains governed by §4.6.
    Toolchain note: bit_count() requires Python >= 3.10; minimum interpreter is pinned to
    3.11 with no fallback (R13).

4.3 Atomic family  (RULED — adopted 2026-08-31)
    1. Representation: an immutable/frozen AtomicFamily carrying (T, pi, I, O), with
       T, I, O as §4.2 integer bitmasks and pi in {0,1}. Immutable and hashable.
       Mask-range validity (bits within the instance universe) is checked at the
       family-generation boundary.
    2. I & O != 0 means the family is EMPTY, not invalid. Do NOT raise on I & O != 0:
       V2.1 interprets such families as empty, and they arise naturally from the
       branch-family enumeration, so they must be safely representable and skipped as
       infeasible -- never treated as malformed program state.
    3. Nonemptiness is ONE exact predicate owned by the atomic-family layer (not split
       between the object and the oracle). F(T, pi; I, O) is nonempty iff:
         - I & O == 0, and
         - either there is a free terminal in T \ (I ∪ O)   [it can toggle the parity],
         - or the forced terminal parity already holds: |I ∩ T| ≡ pi (mod 2).
       Exposed as one derived property; ExactBranchMin MAY call it and skip an empty
       family before building the sign-routed / parity-cut instance -- an exact
       optimization consistent with the governing family definition, not a new
       restriction. Emptiness is DERIVED deterministically from (T, pi, I, O); there is
       NO separately mutable/authoritative `infeasible` flag that could diverge from the
       descriptor.
    4. Cover, not partition (unchanged): generated atomic families cover each branch
       domain and may overlap; duplicate coverage does not affect correctness because
       ExactBranchMin minimizes over all generated families. Enumeration order is fixed
       and documented (R10); overlap is never deduplicated in a way that changes the
       defined enumeration without an explicit later ruling.
    Conformance: agreement of this predicate with V2.1's family definition is discharged
    by prop:domain-decomp (tests/test_families.py::test_cover) against the brute verifier.

4.4 Witness and certificate representation  (RULED — adopted 2026-08-31)
    1. Witness vs value are SEPARATE. The mathematical Witness is exactly (U, y),
       matching V2.1's compact witness (U*, y*). The exact quotient (N, D) is the
       associated ExactValue, NOT part of Witness. SolveResult may carry both; the
       serialized certificate carries value + witness so an independent checker has
       everything. (N, D) is NOT duplicated as an authoritative field inside Witness.
    2. U: reuse §4.2 unchanged -- internal integer bitmask; serialized as the sorted
       list of member vertex indices; U must be nonempty for a nonempty witness.
    3. y: dense internally, sparse externally.
       Internal y is an immutable tuple of Python ints of length exactly m, aligned to
       canonical edge_ref order. V2.1 defines the boundary-selection vector only on
       delta_H(U), so the dense form is an embedding with a MANDATORY invariant:
         - if edge e does not cross U, then y[e] == 0;
         - if edge e crosses U, then 0 <= y[e] <= q[e].
       Hence Y(y) = sum(y[e] for e crossing U), which equals sum(y) for every valid
       dense witness (noncrossing coords are forced to zero).
       Serialized y stays sparse per §9: [[edge_ref, count], ...], strictly positive
       counts only, and REQUIRE: entries sorted strictly by edge_ref; no duplicate
       edge_ref; every reference in range; every referenced edge crosses U;
       1 <= count <= q[edge_ref]. Missing entries decode to zero.
    4. Raw exact value: production (N, D) is the raw quotient of the chosen witness,
         N = 2 * (e_q(U) + Y(y)),   D = f(U) + Y(y) - 1,
       with N, D Python ints and D > 0. NOT gcd-reduced in v1 (V2.1 permits optional
       Euclidean reduction as separate bit-polynomial postprocessing; unnecessary here,
       and reducing would destroy the canonical raw certificate<->witness relation).
       Cross multiplication remains the required method for comparing two exact quotients
       inside the solver -- distinct from validating that a certificate stores the ruled
       raw (N, D).
    5. Nonempty certificate verification contract (exactfrac_verify.check). After
       independently validating the instance and canonical edge order, a nonempty
       certificate is accepted iff ALL hold (no tolerance, no floating point anywhere):
         - U is a valid, nonempty shore;
         - dense reconstruction of sparse y has length m; every y[e] is an integer;
         - noncrossing edges have y[e] == 0; crossing edges have 0 <= y[e] <= q[e];
         - Y(y) computed from the boundary selection;
         - f(U) + Y(y) is odd;   f(U) + Y(y) >= 3;
         - N == 2 * (e_q(U) + Y(y));   D == f(U) + Y(y) - 1;   D > 0.
       The checker verifies admissibility and exact attainment; it shares no solver code.
    6. Empty result: semantically ((0,1), Empty) -- value (0,1), no (U, y). The serialized
       certificate uses the §9 `empty` field and carries NO fake shore or count vector.
       The verifier VERIFIES emptiness, not the flag: for a validated active instance, by
       V2.1 lem:empty, A_q(H) is empty iff Q == 1. So an empty certificate is valid iff
       the instance is valid and active, Q == 1, value is exactly (0,1), and no witness
       payload is present. No dummy U or y is created for the empty case.
    7. Immutability: Witness is immutable; the ExactValue representation is immutable;
       certificate serialization is derived from those and is not an independent mutable
       source of mathematical truth.
    (§9 external schema is preserved; sparse-y canonicalization is tightened per item 3.)

4.5 Exact arithmetic  (RULED — adopted 2026-08-31)
    1. Production rational representation: raw integer (A, B) pairs throughout -- A a
       Python int, B a Python int with B > 0, NO automatic gcd reduction, denominator
       sign normalized positive. Applies to branch parameters, Newton points, reflected
       look-ahead points, returned values, and any rational residual. A raw pair
       represents a value, not lowest terms, so equality/ordering are mathematical:
       A/B == C/D iff A*D == C*B; A/B < C/D iff A*D < C*B; sign is sign(A) since B>0.
       No float, no tolerance. Standard Newton point is the raw pair (c_j(U), h_j(U));
       the standard init K = c_j(U0)/h_j(U0) + 1 is stored as (c_j(U0)+h_j(U0), h_j(U0)).
       Accelerated look-ahead 2*hat_delta - delta, with hat_delta=A/B and delta=C/D, is
       stored EXACTLY as (2*A*D - C*B, B*D), no gcd reduction -- intentional and matched
       to the bit-growth proof (lengths accumulate only polynomially under successful
       look-ahead).
    2. Oracle residual arithmetic: at lambda = A/B, ExactBranchMin minimizes the raw
       integer residual B*c_j(U) - A*h_j(U), the numerator of F_j(lambda) =
       (B*c_j(U) - A*h_j(U)) / B. Since B>0, sign and zero tests are performed directly
       on the integer numerator (never divide to decide <0, ==0, >0). Aligns with the
       frozen contract Bc_j - Ah_j.
    3. Fraction policy: fractions.Fraction is PROHIBITED from the solver arithmetic path
       (instance, families, flow, oracle, branch, solve, certificate). Fraction is
       permitted only in the independent verifier and tests as an independent correctness
       oracle. CLI may display the raw value as N/D; no normalization needed. This is
       implementation discipline (Fraction's automatic gcd would add arithmetic absent
       from the ruled strong-operation path and obscure the raw bit-growth trajectory),
       not a claim that Fraction is inexact.
    4. Bit-growth is TELEMETRY + TESTS, NOT a production asymptotic assertion. Do NOT
       install a production assert "bit length <= lem:bitgrowth bound": V2.1 proves
       polynomial length asymptotically, without an assertible numeric threshold/constants.
       Production asserts only exact LOCAL invariants: denominators positive; operands and
       results integers; required-nonnegative capacities nonnegative; exact residual
       identities where applicable. Bit growth is measured deterministically (see §8:
       peak_integer_bits).
    5. Executable bit-growth conformance (tests, not a cutoff): cover both source lemmas
       -- lem:standard-bits (SolveBranchStandard) and lem:bitgrowth (SolveBranchAccelerated).
       On the constant-support enormous-multiplicity family, vary multiplicity encoding
       length with the support fixed and record operation/call counters and peak
       numerator/denominator/integer bits. Verify exact arithmetic on hand-derived
       fixtures and the proof-predicted structure: operation counts NOT driven by
       multiplicity magnitude, while integer encoding lengths grow with input bit length.
       A finite sweep is regression/conformance, NOT a proof of polynomial growth; it
       catches accidental multiplicity expansion, magnitude-controlled iteration, or
       arithmetic outside the proof-prescribed recurrence. A later derived closed bound
       could become an asserted obligation separately; not part of this ruling.
    6. Optional reduction stays OUTSIDE the solver: final (N,D) is the raw witness-attaining
       quotient of §4.4. V2.1 cor:gcd permits optional Euclidean reduction only as
       separate polynomial-bit postprocessing, excluded from the strong-operation bound;
       v1 does not perform it in the solver.

4.6 Argmin policy  (RULED — adopted 2026-08-31)
    Separation: theorem = any exact residual argmin; implementation = first-encountered
    under fixed enumeration (equality never replaces); family solver = deterministic cut
    per R9; prohibited = consulting h_j or any secondary objective to resolve a residual tie.
    1. Mathematical contract UNCHANGED: at lambda=A/B, ExactBranchMin may return ANY exact
       minimizer of the raw residual B*c_j(U) - A*h_j(U); no secondary mathematical
       preference; every argmin supplies the valid supergradient -h_j(U). The policy below
       is reproducibility only and does NOT strengthen the oracle spec.
    2. Deterministic global selection = first encountered. Traverse atomic families in the
       fixed documented order (R10); maintain the best candidate by STRICT improvement:
       no incumbent -> accept first feasible; strictly smaller raw residual -> replace;
       EQUAL raw residual -> do NOT replace; larger -> retain. The returned minimizer is
       literally the first exact minimizer under the fixed enumeration. No equality-time
       comparison of h_j, shore size, mask value, numerator/denominator size, witness
       data, or any secondary quantity. Integer-mask order matters only if an enumeration
       routine has separately defined it as that routine's fixed order; §4.2 imposes no
       tie-break.
    3. Within-family determinism uses the R9 cut result (exact min value; deterministic
       source shore; inclusionwise-minimal minimum source shore where the parity reduction
       needs the lattice extremal). No oracle-level tie-break on top of the backend result.
       Distinction: R9 = how ONE family minimization is reproduced; §4.6 = how EQUAL
       residuals from DIFFERENT families are handled.
    4. Max-h_j objective stays REMOVED. On a residual tie the code must NOT inspect h_j to
       prefer larger. This bans the SELECTION RULE, not the incidental properties of the
       selected minimizer: if the first-encountered legal minimizer happens to maximize
       h_j, that output is fully valid and tests must NOT reject it for that. Forbidden is
       code equivalent to "residuals tie -> compare h_j -> choose larger h_j."
    5. Testing separates theorem freedom from shipped determinism (three classes):
       A. Oracle-contract: on fixtures with multiple exact minimizers, independently
          enumerate the full argmin set; verify all share the min raw residual, satisfy
          the branch-domain requirements, and supply -h_j(U); impose NO preferred minimizer.
       B. Deterministic-path: verify fixed enumeration + strict-improvement-only replacement
          returns exactly the first-encountered minimizer; same input -> same result and
          same AlgorithmStats; include a fixture where the first minimizer does NOT maximize
          h_j (so any resurrected max-h_j tie-break is caught). Do NOT require the converse.
       C. Tie-independence / outer loop: on tiny fixtures, inject alternative legal argmins
          and verify each output is legal, branch invariants hold, each branch solve
          terminates at the SAME exact branch optimum, and witnesses are admissible and
          attaining. Different legal choices MAY give different intermediate Newton
          parameters, iteration counts, and attaining witnesses -- permitted; do NOT require
          identical trajectories, intermediate roots, witnesses, or AlgorithmStats across
          different legal tie policies. Default shipped policy stays first-encountered.
    6. No witness-equality requirement: correctness is exact value + admissible attaining
       witness, not witness identity (consistent with the Standard-vs-Accelerated rule).
       Multiple optimal witnesses are legitimate.

## 5. Algorithm map (by label)

    ExactBranchMin          alg:branch-min          per-branch exact residual argmin
    SolveBranchStandard     alg:standard-branch     independently strongly polynomial
    SolveBranchAccelerated  alg:branch              look-ahead; iteration bound via DKNV
    StrongCompactMSPD       alg:global              unit baseline -> four transformed
                                                    branches -> direct H2 scan -> exact
                                                    global comparison -> witness reconstruction
    branch invariant        prop:branch-invariant
    global invariant        prop:global-invariant
    correctness             prop:branch-correct, prop:standard-correct
    domains / families      prop:domain-decomp, prop:endpoints, prop:branch-transform
    compact <-> expanded    prop:expanded-equivalence
    output contract         ((0,1), Empty) when the admissible family is empty
    (Labels above are copied from V2.1's \label{} set; any new citation is checked
    against the source before use.)

Standard is implemented and tested before Accelerated; Accelerated is tested against
Standard on every catalog instance (equal values; witnesses admissible and attaining).

## 6. Oracle layer

`docs/ORACLE_CATALOG.md`: hand-derived instances with expected (N, D) and a witness,
derived BEFORE the code that computes them. Every entry is classified:
  GLOBAL_ORACLE            full instance, proved global optimum and witness
  BRANCH_ORACLE            expected output of one branch on one instance
  LOCAL_CONTRACT_FIXTURE   a lemma's construction (e.g. the unit witness) — a lower
                           bound or candidate, NOT a claimed optimum
  CROSS_MODEL_EQUIVALENCE  compact vs expanded-copy agreement
  NEGATIVE / REJECTION     unsupported instance, infeasible family, empty parity set
Seed cases from the paper, classified: Q = 1 single edge, f ≡ 1 -> ((0,1), Empty) is a
GLOBAL_ORACLE. The constructive unit witness (`lem:unit`) is a LOCAL_CONTRACT_FIXTURE.
The H2 value-2 case is a BRANCH_ORACLE. Promoting either to GLOBAL requires a concrete
instance and a hand proof that no other branch beats the recorded candidate (tiny
instances: cross-checked by the brute verifier after the hand derivation). Then the branch cases, the degenerate cases, and one
instance per pseudocode path (initial delta already the root; early return at delta-hat;
look-ahead accepted; look-ahead rejected; infeasible branch; unit witness stays optimal).

## 7. Verifier

`exactfrac_verify.brute` enumerates all nonempty U and all compact y with
0 <= y_e <= q_e directly from the definition (tiny instances only) and returns the exact
optimum and one witness. It does not know what a branch is.
`exactfrac_verify.check` takes (instance, certificate) and confirms admissibility and
objective equality. It runs on every solver output in every test.

## 8. Telemetry contract (diagnostic; never part of a certificate)

RunRecord = AlgorithmStats (deterministic, derived from the algorithm alone) +
RunMetadata (environmental). Kept in separate structures so determinism tests can
compare AlgorithmStats exactly across machines.

AlgorithmStats, per solve and per branch:
  outer_iterations, oracle_calls, atomic_families_enumerated,
  atomic_families_feasible, parity_cut_calls, ordinary_min_cut_calls,
  max_flow_calls, augmentations, bfs_scans, lookahead_accepted,
  lookahead_rejected, early_returns, peak_numerator_bits,
  peak_denominator_bits, peak_integer_bits, attaining_branch
  # peak_integer_bits (§4.5): max magnitude-bit-length over EVERY theorem-relevant
  # generated integer -- residual numerators, cut/residual capacities, flow values,
  # integer coefficients, branch/output integers. Fixed convention everywhere:
  # bits(x) = max(1, abs(x).bit_length()). Diagnostic only; never part of a certificate.
RunMetadata:
  wall_clock_s, python_version, platform, cpu, code_version, instance_sha256
Both outer loops expose identical AlgorithmStats fields. Certificates carry neither.

## 9. File formats (versioned; `"format": "exactfrac-instance/1"` etc.)

instance:     n, edges in canonical order [[u, v, q_e], ...], f [...], labels (optional)
              — edge identity IMPLICIT: edge_ref = index in this canonical list (§4.1)
certificate:  N, D, U (sorted indices), y (sparse: [[edge_ref, count], ...]), empty flag
              — edge_ref resolves through the §4.1 ruling; no wall-clock or platform data
run record:   §8 (AlgorithmStats + RunMetadata)

## 10. Conformance map

`docs/CONFORMANCE.md`: one row per theorem obligation -> the test that discharges it.
Started on day one, grown with every unit. This is the paper's proof-to-code table.

## 11. Experiments (Q4 placeholder)

`experiments/reproduce.py --all` regenerates every table from `instances/` into
`results/`. Families are declared with generators and seeds. Nothing here is core.

## 12. Release gate (Sep 8 is a release candidate, not a flip)

Before any public release, all of: privacy scan; git-history scan (paths, names, tool
names); license ruling re-confirmed (R7); public status of the theorem source / preprint
noted in the README; README review against §0; benchmark-claim review (no unearned
numbers); secret/path scan; artifact inventory; test reproduction from a clean
environment; a test run on the minimum supported interpreter (Python 3.11, R13) as well as
the development interpreter. If the private history contains anything that should not be exposed, a
clean public release repo is created (the Foundation Portfolio precedent). Target: the
audit runs Sep 7–8 so a passing candidate can still go public at CPF start; a private
week beats a premature public repo.
