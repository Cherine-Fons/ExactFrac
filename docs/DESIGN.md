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

Priority amendment (author ruling, September 10, 2026): SolveBranchAccelerated is
required core work for the MPC computational study, built as Unit 14 immediately
after Unit 13 and before Unit 15. It may not be deferred under a shortened runway.
Unit 15 must support a ruled Standard | Accelerated selection and test both routes.
Beyond its first family, item 9 may still slip; CLI and certificate verification
remain core. The former Standard-only deferral permission is superseded.
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

    V2.2 zero-arc totalization: `E = 0` is a valid ordinary-cut instance, not malformed
    input. The backend returns exact value `0` and the inclusionwise-minimal minimum source
    shore `{s}`, with zero augmentations and zero residual-adjacency scans. The uniform
    arithmetic/comparison-operation carrier is `O(N + NE^2)`; for `E >= 1`, the
    Edmonds–Karp augmenting-path work remains `O(NE^2)`, and residual source-shore
    recovery costs `O(N + E)`.

    Reference-counter semantics: `augmentations` counts successful residual `s`--`t`
    path augmentations. `bfs_scans` counts directed residual-adjacency entries inspected
    across all breadth-first searches, including the final no-augmenting-path/reachability
    search. Vertex-record initialization is charged to the `O(N)` carrier and is not an
    arc scan.

    Zero-safe number-size carrier: for arc set `A`, define
    `u_max = max({0} union {u_a : a in A})` and
    `l = ceil(log2(u_max + 1))`. Every generated flow value or residual capacity `z`
    satisfies `log2(1 + z) <= l + ceil(log2(E + 1))`.
R10 Determinism: no algorithmic path iterates over a Python `set`; all enumeration
    orders are fixed and documented; generators take explicit seeds.
R11 Every commit is one unit; every unit has its test before its code is considered done.
R12 Language rule: outputs are a certified fractional lower bound with a witness;
    never "exact block count".
R13 Toolchain: minimum Python 3.11; pyproject.toml declares requires-python = ">=3.11".
    int.bit_count() is used with NO compatibility fallback. The release gate (§12) tests
    the minimum supported interpreter (3.11) as well as the development interpreter.
R14 Governing-checksum baseline (adopted Sep 4, 2026):
    `GOVERNING_SHA256SUMS.txt` authenticates the five governing-document files exactly as
    they existed at V2.2 activation commit `900e15ee93ccfeda42ba36a355f1f1a6c9c43869`.
    It is an immutable baseline inventory, not a rolling manifest. Verify the baseline
    against the activation blobs by hashing each `git show
    900e15ee93ccfeda42ba36a355f1f1a6c9c43869:<path>` stream in manifest order and
    comparing those lines with `GOVERNING_SHA256SUMS.txt`, not against the evolving
    worktree, where later controlled governing-document changes are expected to differ.
    Later controlled changes to DESIGN, TEST_PLAN, or CONFORMANCE are authenticated by
    their Git parent/tree/blob identities, exact diffs, tests, and audit records. Do not
    refresh the baseline checksum file merely because a later unit changes one of those
    documents.

## 3. Package layout

    exactfrac/            solver (stdlib only)
      instance.py         canonical instance, aggregation, active check
      shore.py            finite-universe shore masks and strict list serialization
      rational.py         raw scalar pairs, exact comparisons, prescribed update arithmetic
      witness.py          Witness, ExactValue, shore sums, validation, dense/sparse counts
      families.py         atomic families F(T, pi; I, O); enumeration per branch
      sign_routing.py     branch coefficients, nonnegative cut construction, explicit shifts
      parity_cut.py       forced contraction, parity anchoring, exact parity-cut minimization
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

4.1A Production graph-instance API and error boundary  (RULED — adopted 2026-09-03)
    1. Unit ownership and public surface. `exactfrac.instance` owns only canonical compact-
       instance construction, raw-record normalization, strict canonical object
       deserialization, derived graph data, and the active check. Its module-level `__all__`
       is exactly `Edge`, `Instance`, `InvalidInstance`, and `UnsupportedInstance`; `Edge` is
       the alias `tuple[int, int, int]`. `exactfrac.__init__` remains export-free in this
       unit, and production code imports nothing from `exactfrac_verify`. Shore
       representation and shore helpers remain the separate §4.2 unit and are not
       implemented here.
    2. Canonical object. `Instance` is frozen and slotted. Its authoritative stored fields
       are `n`, `edges`, `f`, and optional `labels`. `edges` is an immutable tuple of
       canonical `(u, v, q_e)` triples in edge_ref order. Read-only derived properties expose
       `m`, `support_edges`, `q`, `Q`, and `d_q`; there is no separately mutable support-edge
       list, multiplicity vector, total multiplicity, or degree vector. Optional `labels` is
       the canonical index-to-label metadata tuple; no second authoritative reverse map is
       stored. Derived data is computed from the authoritative fields and cannot diverge.
    3. Exact Python domain and excluded weight models. Every numeric instance datum (`n`,
       endpoints, multiplicities, and `f` values) has exact built-in type `int`; `bool`,
       integer subclasses, floats, `Fraction`, and implicit `int(...)` coercion are rejected.
       Each edge datum is exactly `(u, v, q_e)`. There is no edge-weight field and no real-
       or rational-weight input mode: `q_e` is a positive integer count of individually
       selectable unit copies, not an indivisible edge weight. The Python constructors
       require exact tuples for the edge/record container, every edge/raw record, and `f`.
       Optional `labels` is `None` or an exact tuple of length `n`; each label has exact
       built-in type `str` or exact built-in type `int`, `bool` is rejected, and labels are
       pairwise distinct. Labels are I/O metadata aligned to dense index order and are never
       algorithmic.
    4. Constructor boundary. `Instance(n, edges, f, labels=None)` is canonical-only: it
       validates RI1--RI7 and rejects reversed, repeated, or out-of-order edge triples rather
       than repairing them. `Instance.from_records(n, records, f, labels=None)` is the sole
       raw normalization entry point: it validates every raw record, rejects loops and
       nonpositive multiplicities, orients endpoints with `u < v`, aggregates repeated
       unordered endpoint pairs by exact addition, and sorts the result lexicographically.
       Raw endpoints are dense indices. Any future label-keyed adapter must translate to
       dense indices before this boundary and requires a separate ruling.
    5. Versioned external object representation. `Instance.to_dict()` emits the JSON-ready
       `exactfrac-instance/1` object of §9 with keys `format`, `n`, `edges`, `f`, and optional
       `labels`; edges are lists `[u, v, q_e]` in canonical edge_ref order, while `f` and
       labels are lists. `Instance.from_dict(data)` accepts only an exact `dict` with exactly
       those required keys plus optional `labels`; its edge container, edge records, `f`, and
       labels are exact lists. It validates the canonical representation and never reorders,
       aggregates, reorients, or silently discards serialized records. Unknown or missing
       keys, a wrong format tag, or a noncanonical edge list are invalid. JSON text/file I/O
       remains outside this unit.
    6. Error taxonomy and validation order. `InvalidInstance` and `UnsupportedInstance` are
       distinct sibling subclasses of `ValueError`; neither subclasses the other. Malformed
       type, container, shape, format, endpoint, loop, ordering, multiplicity, `f`, label, or
       empty-support conditions raise `InvalidInstance`. This production boundary
       intentionally translates its type/shape failures into `InvalidInstance`; it does not
       copy the sealed flow primitive's internal `TypeError`/`ValueError` split. Only a
       structurally valid canonical instance with some `f[v] > d_q[v]` raises
       `UnsupportedInstance`. In particular, a structurally valid graph may contain an
       isolated vertex, but positive `f` then makes the instance unsupported by the active
       hypothesis. Each entry point validates outer representation/format, `n`, `f`, labels,
       edge records, and canonical order or raw normalization before computing `Q` and
       `d_q`; the active check is last. Exception prose is diagnostic, not stable API.
    7. Preprocessing carrier. For `r` raw records, `from_records` follows
       `lem:aggregation`: endpoint normalization, sorting/grouping, and aggregation use
       `O(r log(r+1))` comparisons and `O(r)` additions (or `O(r)` operations when already
       grouped). This optional raw preprocessing is outside the main theorem's canonical-
       instance operation bound. No multiplicity is expanded into unit copies.
    8. Unit boundary. This ruling does not implement §4.2 shores, §4.3 atomic families,
       §4.4 witnesses/certificates, §4.5 arithmetic helpers, §4.6 argmin policy, sign routing,
       parity-cut reduction, branch logic, or the global solver.

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

4.2A Production shore API and error boundary  (RULED — adopted 2026-09-04)
    1. Unit ownership and public surface. `exactfrac.shore` owns only finite-universe shore-
       mask construction, validation, strict sorted-index-list encoding/decoding, and
       universe-relative complement. Its module-level `__all__` is exactly `Shore`,
       `full_mask`, `validate_shore`, `shore_from_list`, `shore_to_list`, and
       `shore_complement`; `Shore` is the alias `int`. `exactfrac.__init__` remains export-
       free in this unit. The module is graph-independent: it imports neither
       `exactfrac.instance` nor `exactfrac_verify`. Membership, union, intersection,
       cardinality, and intersection parity remain the transparent integer operations
       ruled in §4.2 rather than acquiring redundant public wrappers.
    2. Universe and exact Python domain. Every public helper is parameterized by an
       ExactFrac vertex count `n` having exact built-in type `int` and satisfying `n >= 1`;
       `bool`, integer subclasses, floats, `Fraction`, and implicit `int(...)` coercion are
       rejected. `full_mask(n)` returns exactly `(1 << n) - 1`. A shore value has exact
       built-in type `int`. `validate_shore(n, U)` requires `0 <= U <= full_mask(n)` and
       returns the unchanged integer `U`; negative integers and masks with any bit outside
       `0..n-1` are invalid.
    3. Empty and full shores. `0` is the valid representation of the empty shore, and
       `full_mask(n)` is the valid representation of the complete vertex shore. Generic
       shore validity does not impose nonemptiness. Any later witness, family, cut, or
       optimization boundary that requires a nonempty or proper shore owns that additional
       predicate and must not redefine the underlying subset representation.
    4. Strict list serialization. `shore_to_list(n, U)` validates `n` and `U`, then returns
       a fresh exact built-in list of member indices in strictly increasing order.
       `shore_from_list(n, vertices)` accepts only an exact built-in list; every entry has
       exact built-in type `int`, lies in `0..n-1`, and is strictly greater than its
       predecessor. The empty list decodes to `0`. Duplicate, decreasing, unsorted,
       out-of-range, or non-integer entries are rejected rather than sorted, deduplicated,
       or coerced. Serialized shores use dense indices, never optional instance labels.
    5. Complement and inline operations. `shore_complement(n, U)` validates its inputs and
       returns exactly `full_mask(n) ^ U`. Bare Python `~U` is never accepted as a shore.
       On already validated shore values, membership is `bool(U & (1 << v))`, union and
       intersection are `U | W` and `U & W`, cardinality is `U.bit_count()`, and the parity
       of `|U intersect T|` is `(U & T).bit_count() & 1`. Integer mask order is permitted
       only where another unit explicitly fixes an enumeration order; it is not a new
       mathematical tie-break.
    6. Error taxonomy and validation order. Every malformed `n`, shore value, serialized
       container, or serialized member raises the exact built-in class `ValueError`; this
       unit introduces no shore-specific exception and does not reuse `InvalidInstance` or
       `UnsupportedInstance`. Exception prose is diagnostic and not a stable API. Helpers
       validate `n` first; mask-consuming helpers then validate `U`; list decoding then
       validates the exact outer list and its entries in encounter order.
    7. Complexity, exactness, and determinism. `full_mask`, `validate_shore`, and
       `shore_complement` use a fixed number of exact integer/bit operations.
       `shore_from_list` uses `O(k)` operations for a list of length `k`; `shore_to_list`
       uses `O(n)` bit tests. No helper enumerates all `2^n` shores or iterates once per
       numeric mask value. The module uses no `Fraction`, floating point, true division,
       tolerance logic, or algorithmic iteration over a Python `set`.
    8. Unit boundary. This unit does not compute graph-dependent quantities such as
       `f(U)`, `e_q(U)`, `b_q(U)`, or `d_q(U)` and does not import `Instance`. It does not
       implement atomic families, witnesses, certificates, §4.5 rational-pair arithmetic,
       argmin policy, sign routing, parity-cut reduction, branch logic, or the global
       solver. Those responsibilities remain with their separately ruled consumers.

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

4.3A Production atomic-family API and deterministic decomposition
     (RULED — adopted 2026-09-04)
    1. Source binding and ownership. `exactfrac.families` is the first production consumer of
       the graph-dependent sets in `prop:domain-decomp`. It consumes an already validated,
       already aggregated `Instance` and the §4.2 shore representation. It computes the masks
         T_plus = {v : f[v] + d_q[v] is odd},
         T_f    = {v : f[v] is odd},
         P      = {v : d_q[v] > f[v]},
         A      = {v : f[v] >= 2},
         W      = {v : f[v] == 1}
       from dense vertex order and `Instance.f` / `Instance.d_q`; labels are ignored. This is
       the production realization of `alg:global` line 1 on the aggregated support graph.
    2. Public surface. The module-level `__all__` is the Ruff-sorted sequence
       `AtomicFamily`, `enumerate_atomic_families`. `exactfrac.__init__` remains export-free
       in this unit. `AtomicFamily` is a frozen, slotted, immutable and hashable descriptor
       with authoritative fields exactly `T`, `pi`, `I`, and `O`. The function
       `enumerate_atomic_families(instance)` returns all four branch decompositions at once.
    3. Descriptor domain and errors. `T`, `I`, and `O` have exact built-in type `int` and are
       nonnegative; `pi` has exact built-in type `int` and belongs to `{0,1}`. `bool`,
       integer subclasses, floats, `Fraction`, and coercion are rejected. Malformed
       descriptors and a nonexact `Instance` argument raise exact built-in `ValueError`;
       this unit introduces no family-specific exception. Because an `AtomicFamily` stores
       no universe size, its direct constructor checks nonnegativity but cannot check a high
       bit against `n`; `enumerate_atomic_families` constructs and range-validates every
       generated mask against the consumed instance universe.
    4. Overlap and nonemptiness. `I & O != 0` is accepted descriptor state and denotes the
       empty family; it is never raised as malformed. `AtomicFamily.is_nonempty` is the one
       derived Boolean predicate and is true exactly when
         I & O == 0
       and either
         T \ (I union O) is nonempty,
       or
         (I & T).bit_count() & 1 == pi.
       The free-terminal mask is computed by finite mask operations without treating bare
       Python `~` as a shore. No mutable `empty`, `infeasible`, or cached-authority flag is
       stored.
    5. Return shape. `enumerate_atomic_families(instance)` returns an exact built-in
       four-tuple `(D0_families, D1_families, D2_families, D3_families)` in branch order
       `j = 0,1,2,3`. Every component is an exact tuple of `AtomicFamily` values. Returning
       all four tuples in one call permits `alg:global` to compute the derived masks and the
       complete deterministic decomposition once and pass one immutable branch tuple to
       each later branch solve.
    6. D0 order. Branch 0 contains exactly
         AtomicFamily(T_plus, 1, 0, 0).
    7. D1 order. Traverse `p` through `P` in increasing dense vertex order. For each `p`,
       traverse support edges `uv` in canonical `edge_ref` order. For each edge, emit first
         F(T_plus, 0; {p,u}, {v})
       and then
         F(T_plus, 0; {p,v}, {u}).
       Mask unions collapse repeated forced-in vertices naturally. If `p` equals the
       forced-out endpoint, the resulting `I & O != 0` descriptor is retained as an empty
       family.
    8. D2 order. First traverse `a` through `A` in increasing dense vertex order and emit
         F(T_f, 1; {a}, empty).
       Then traverse the three-element subsets `{u,v,w}` of `W` in lexicographic increasing
       vertex-tuple order and emit
         F(T_f, 1; {u,v,w}, empty).
       The singleton block precedes the triple block exactly as displayed in
       `prop:domain-decomp`.
    9. D3 order. Traverse support edges `uv` in canonical `edge_ref` order. For each edge,
       emit first
         F(T_f, 0; {u}, {v})
       and then
         F(T_f, 0; {v}, {u}).
    10. Count, overlap, and no deduplication. The exact number of descriptors returned is
          R_actual = 1 + 2*|P|*m + |A| + binom(|W|,3) + 2*m.
        The source quantity
          R = 1 + 2*m*n + n + binom(n,3) + 2*m
        is an upper bound, not an assertion that every instance returns exactly `R`
        descriptors. Empty descriptors, repeated descriptors, and overlapping family
        coverage are retained in the fixed sequence; no set-based deduplication, emptiness
        filtering, or order-changing normalization occurs in this unit.
    11. Coverage semantics. For a validated shore `U`, membership in a descriptor is the
        mathematical predicate
          (U & I) == I,
          (U & O) == 0,
          (U & T).bit_count() & 1 == pi.
        This predicate is used by independent tests to compare the union of generated
        families with each source branch domain. It is not added as another public wrapper
        in this unit because the production residual oracle consumes descriptors through
        cut reduction rather than enumerating their shores.
    12. Complexity, exactness, and determinism. Derived masks use `O(n)` exact operations.
        Descriptor construction uses `O(R_actual)` fixed-order operations after the
        canonical support scan, for total `O(n + m + R_actual)` operations. The module never
        expands multiplicities, iterates once per copy, or lets `q`/`f` magnitude control an
        iteration count. It uses no `Fraction`, floating point, true division, tolerance
        logic, or output order derived from Python `set` iteration.
    13. Unit boundary. This unit does not evaluate `f(U)`, `e_q(U)`, `b_q(U)`, `d_q(U)`,
        branch residuals, or exact quotients. It does not implement sign routing,
        parity-cut reduction, `ExactBranchMin`, branch iteration, witness reconstruction,
        certificate logic, or the global solver. It prepares the immutable family
        descriptors that those later units consume.

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

4.4A Production Witness and ExactValue interface  (RULED upon controlled adoption, 2026-09-05)
    1. Ownership and dependency direction. `exactfrac.witness` owns the immutable Witness
       and ExactValue records, graph-dependent shore sums, dense/sparse boundary-count
       conversions, production admissibility validation, and raw witness-value evaluation.
       It consumes the already-canonical `Instance` and the existing shore interface; it
       does not repeat aggregation or instance construction. Later solver components and
       `certificate.py` may consume this lower-level module. `certificate.py` retains full
       certificate construction and serialization; `exactfrac_verify.check` remains a
       separately implemented independent checker. No closed implementation is reopened by
       this ruling. The new DESIGN section-3 layout entry and the explicit addition of
       `witness` to section 4.5.3 are the only amendments to pre-existing DESIGN lines.
    2. Exact public surface. Module `__all__` is the following exact tuple, in this order:
         ("ExactValue", "Witness", "dense_y_to_sparse", "shore_b_q", "shore_d_q",
          "shore_e_q", "shore_f", "sparse_y_to_dense", "validate_witness", "witness_value").
       The public signatures, including keyword names and return types, are:
         ExactValue(N: int, D: int)
         Witness(U: int, y: tuple[int, ...])
         shore_f(instance: Instance, U: int) -> int
         shore_e_q(instance: Instance, U: int) -> int
         shore_b_q(instance: Instance, U: int) -> int
         shore_d_q(instance: Instance, U: int) -> int
         dense_y_to_sparse(instance: Instance, U: int, y: tuple[int, ...]) -> list[list[int]]
         sparse_y_to_dense(instance: Instance, U: int, entries: list[list[int]]) -> tuple[int, ...]
         validate_witness(instance: Instance, witness: Witness) -> None
         witness_value(instance: Instance, witness: Witness) -> ExactValue
       These constructors/functions accept positional or the shown keyword arguments; no
       hidden mode flags or alternative public constructors are introduced. Package-root
       `exactfrac.__init__` remains export-free. Internal helpers are not public API.
    3. Witness record. `Witness` is a frozen, slotted, hashable dataclass, with structural
       equality, no generated ordering, and fields/slots exactly `U`, `y` in that order.
       `U` must be an exact built-in int strictly greater than zero. `y` must be an exact
       tuple whose entries are exact built-in nonnegative ints. No coercion or mutable
       container is accepted. The constructor has no instance: it cannot establish the
       finite-universe upper bound, `len(y) == m`, multiplicity bounds, boundary support,
       or admissibility. A high-bit positive U and an empty tuple y are valid constructor
       shapes, not assertions of validity for any particular instance. Store no n, m,
       Instance, N, D, empty flag, or separate length/value/cache field inside Witness.
    4. ExactValue record. `ExactValue` is a frozen, slotted, hashable dataclass with fields/
       slots exactly `N`, `D` in that order and no generated ordering. Both fields must be
       exact built-in ints, and D must be strictly positive. Signed N is allowed at this
       representation boundary; constructing the record is not a claim of attainment.
       Reject D <= 0 rather than repairing its sign. Preserve both supplied integers
       literally: no gcd reduction, rescaling, zero normalization, or conversion to float
       or Fraction. There is no implicit conversion to/from the arithmetic carrier of
       Unit 09 and no arithmetic operator, numerical-comparison method, or empty predicate.
    5. Two equality relations. ExactValue is an immutable record of the exact stored fields
       (N, D). Record equality is structural, and hashing is based on those stored fields
       consistently with structural equality. Neither operation reduces, rescales, or
       normalizes the quotient. Consequently ExactValue(2, 2) and ExactValue(1, 1) are
       unequal records representing equal rational values. DESIGN section 4.5 numerical
       equality and ordering remain the explicit cross-multiplication relations of Unit
       09; solver numerical decisions must not substitute structural equality or
       lexicographic field ordering. This is an explicit Python representation ruling,
       not a change to the source's numerical comparisons. Equal records must have equal
       hashes; unequal records need not have unequal hashes, and hash integers are not
       serialized or treated as cross-process identifiers. Structural equality is chosen
       deliberately, not justified by a claim that every numerical hash requires a gcd.
    6. Instance and shore boundary. Every instance-keyed public function first requires
       `type(instance) is Instance`. It consumes a normally constructed canonical active
       production Instance, not serialized/raw data, an Instance subclass, a verifier
       instance, or a duck-typed object. It neither repairs nor reaggregates that instance.
       All bare-U arguments require exact built-in int masks satisfying
       `0 <= U <= (1 << instance.n) - 1`. The four sums and the two conversion helpers
       accept U == 0 as well as the full shore. They operate on graph subsets/boundary
       selections, not necessarily admissible witnesses. Witness construction and full
       witness validation separately exclude U == 0. Invalid masks are never truncated.
    7. Graph-shore sums. Own the source def:instance quantities here:
         shore_f(instance, U)   = sum(f[v] for v in U);
         shore_e_q(instance, U) = sum(q_e for edges with both endpoints in U);
         shore_b_q(instance, U) = sum(q_e for edges with exactly one endpoint in U);
         shore_d_q(instance, U) = sum(d_q[v] for v in U)
                                = 2*shore_e_q(instance, U) + shore_b_q(instance, U).
       Outputs are exact built-in ints. For U == 0 all four outputs are zero; the full
       shore has e_q(V) == Q, b_q(V) == 0, and d_q(V) == 2*Q. Use increasing dense indices
       and canonical support-edge order. Internal reuse is allowed; no second authoritative
       graph state or mutable cache is introduced. Optional labels have no effect.
    8. Boundary-selection conversion. Both conversion helpers validate the finite-universe
       shore and the exact boundary-count embedding, but do NOT assert the parity/lower-
       bound admissibility conditions or attainment. Their docstrings must say so.
       `dense_y_to_sparse` requires an exact tuple of length m with exact nonnegative int
       counts; every count is at most its q_e and every noncrossing count is zero. It
       returns an exact list of fresh exact two-element lists [edge_ref, count], omitting
       zero coordinates and emitting the positive ones in canonical increasing edge_ref
       order. Zero omission applies only after validation; invalid records are not dropped.
       `sparse_y_to_dense` requires an exact list of exact two-element lists. Every ref and
       count is an exact built-in int; refs are in [0,m), strictly increasing and unique;
       counts satisfy 1 <= count <= q[ref], and every referenced edge crosses U. Missing
       refs decode to zero in an exact length-m tuple. Reject, never sort, merge, repair,
       coerce, or discard malformed input. Do not mutate inputs; each export and its nested
       lists are detached from prior exports and from record state. The empty sparse list
       denotes the all-zero dense selection, not an Empty result. In particular, U == 0
       and U == V each admit only the all-zero boundary selection.
    9. Full production admissibility. `validate_witness` requires an exact Witness and
       checks its field shape, finite-universe nonempty shore, and boundary-count embedding
       against the consumed instance. It then computes Y(y) from that valid selection,
       sets total = f(U) + Y(y), requires total odd, and requires total >= 3. Return None
       on success; return neither a normalized record nor a truth flag. Failure raises
       exact built-in ValueError. The constructor and conversions are not substitutes
       for this full instance-aware check. A structurally valid but inadmissible selection
       may round-trip through conversion and must still fail validate_witness.
    10. Validation precedence. Public functions validate the instance type before their
        other data. The witness validator/evaluator next requires an exact Witness, then
        validates U, the exact tuple and length of y, and every coordinate's exact type
        and nonnegativity; then bound/boundary constraints in canonical edge_ref order;
        then odd total; then total >= 3. Bare-U functions check U before the remaining
        payload. Sparse decoding checks the outer list, then each record in supplied order
        for exact list/arity, exact int fields, in-range/strictly increasing ref, positive
        bounded count, and crossing support, before constructing the dense output. No
        malformed datum is silently coerced or mislabeled as an empty mathematical family.
        Tests isolate guards without depending on exception-message prose.
    11. Raw evaluation. `witness_value` enforces the same complete admissibility conditions
        as validate_witness before evaluating eq:compact-density. For the valid witness:
          Y = sum(y),  N = 2*(e_q(U) + Y),  D = f(U) + Y - 1.
        Return ExactValue(N, D), preserving these raw formula values. Do not reduce the
        result, force N positive, infer optimality, or test whether the witness is an
        endpoint/global maximizer. Value and witness remain separate records. Negative-N
        records may be constructed directly, but cannot be produced by this evaluator on
        admissible witnesses because e_q(U) and Y are nonnegative. No field of either
        input record or the instance is changed by evaluation or validation.
    12. Zero value and absence of a witness. A zero-valued admissible witness is allowed;
        N == 0 never implies an empty admissible family or authorizes dropping the witness.
        Later result carriers use Witness | None: None means no witness payload. A genuine
        Empty result remains ((0,1), Empty), represented at that later boundary by raw
        ExactValue(0, 1) and no witness. No Witness(0, ()), fake count vector, new Empty
        record/singleton, SolveResult, or certificate envelope is implemented in this unit.
        Empty-result certification remains instance-dependent (lem:empty under the active
        hypothesis) and is not inferred from a raw value, sparse [], or None alone.
    13. Errors and independence. Malformed data supplied through the supported signatures
        raises exact built-in ValueError; reject bool and int/container/record subclasses
        wherever the corresponding exact built-in/record type is required. No new exception
        class or blanket conversion of arbitrary Python errors is introduced. Wrong call
        arity and attempted frozen-record mutation retain Python/dataclass behavior. This
        production validator establishes admissibility, not global optimality. The later
        exactfrac_verify.check must independently reimplement admissibility and attainment
        checks and must not import this module or any other production helper.
    14. Exactness and imports. Runtime imports from this module are limited to
        `dataclasses`, `.instance`, `.shore`, and optional future annotations. In particular
        it imports nothing from exactfrac_verify, families, flow, oracle, branch, solve,
        certificate, fractions, decimal, or math. The module's correctness path contains
        no Fraction use, float literal/conversion/arithmetic, true division, tolerance,
        gcd/reduction/normalization routine, or algorithmic iteration over a Python set.
        Existing instance/shore behavior and package-root exports are unchanged.
    15. Compact work and separate arithmetic. Graph sums, witness validation/evaluation,
        and conversions on valid input use O(n+m) structural integer/arithmetic/comparison
        operations and at most O(n+m) auxiliary storage; actual bit-operation time may grow
        with integer encoding length. Constructor work may depend on the supplied tuple
        length, and malformed-container checks may inspect their encoded record counts.
        No loop is controlled by q_e, f[v], Q, Y, N, D, or by their values/bit-lengths in
        place of the structural scans; no explicit-copy or all-shore enumeration occurs.
        Unit 09 owns general rational-pair comparison/arithmetic. Units 15/17/18 own witness
        reconstruction, full certificate assembly/serialization, and independent checking.
        This unit implements none of those algorithms, JSON text/file I/O, result-level
        Empty certification, or telemetry; it invents no new theorem row. Historical
        TEST_PLAN W1--W7 are unchanged: representation and raw evaluation are tested here,
        while W7's full serialized-certificate obligation is not declared complete here.

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
       (instance, families, flow, oracle, branch, solve, certificate, witness, rational, sign_routing, parity_cut). Fraction is
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

4.5A Production raw rational-pair primitives
     (RULED upon controlled adoption, 2026-09-06)
    1. Ownership. `exactfrac.rational` is a graph-independent scalar arithmetic layer for
       the exact operations already prescribed by section 4.5. It owns no Instance,
       Witness, ExactValue, branch, cut, optimizer, certificate, or telemetry object. Its
       only permitted import is optional future annotations; it imports no other production
       module, verifier, fractions, decimal, math, or third-party package. Closed modules
       and package-root exports are unchanged. Consumers explicitly extract scalar fields
       when crossing from a record to arithmetic; no dependency on the witness layer is
       introduced. The section-3 layout addition and the addition of `rational` to section
       4.5.3's enumeration are the only edits to previously existing DESIGN lines.
    2. Exact public surface. `RawPair` is the alias `tuple[int, int]`, not a new class or
       validating constructor. A valid carrier is an exact tuple of length two, containing
       exact built-in ints (A, B), with B > 0. The numerator may be signed or zero. Store
       no reduced form, cached products, bit lengths, graph data, or Empty sentinel.
       Module __all__ is exactly this tuple, in the following sorted order:
         ("RawPair", "compare_pairs", "make_pair", "pair_add_one", "pair_reflect",
          "pair_sign", "residual_numerator", "validate_pair").
       Public signatures, including positional/keyword argument names, are:
         make_pair(numerator: int, denominator: int) -> RawPair
         validate_pair(pair: RawPair) -> None
         compare_pairs(left: RawPair, right: RawPair) -> int
         pair_sign(pair: RawPair) -> int
         pair_add_one(pair: RawPair) -> RawPair
         pair_reflect(newton: RawPair, current: RawPair) -> RawPair
         residual_numerator(parameter: RawPair, c: int, h: int) -> int
       No hidden flags, alternative public constructors, mixed-carrier overloads, or
       package-root re-exports are introduced. Exact tuples may be assembled by a caller,
       but every public consumer validates them; the type alias alone validates nothing.
       The untagged tuple carrier is deliberate: validation checks shape and numeric
       domain, not provenance. Callers use role-specific names such as parameter_pair,
       newton_pair, current_pair, and value_pair, construct/extract their scalar entries
       explicitly, and never infer rational intent merely from a two-int tuple's shape.
       A numerically valid edge/count/shore tuple cannot be distinguished at this boundary;
       preventing that category error remains a caller and integration-review obligation.
    3. Strict pair construction. `make_pair` requires exact built-in ints and
       denominator > 0; otherwise it raises exact built-in ValueError. On success return
       (numerator, denominator) literally. Never flip signs, remove common factors, or
       normalize a zero numerator to denominator one. Section 4.5.1's positive-denominator
       wording is a representation invariant enforced here by rejection, not sign repair.
       Every pair-consuming public function likewise rejects B <= 0 rather than repairing
       it. No int(...) coercion, list/sequence conversion, truncation, Fraction conversion,
       or numerical-size cutoff is permitted.
    4. Validation and errors. `validate_pair` checks, in order, exact tuple type, length
       two, exact int numerator, exact int denominator, then denominator positivity, and
       returns None on success. `make_pair` checks numerator type, denominator type, then
       denominator positivity before constructing the pair. Two-pair functions validate their
       first shown argument completely before their second; `residual_numerator` validates
       parameter completely, then c, then h as exact built-in ints before arithmetic.
       Invalid data supplied through these signatures raises exact built-in ValueError;
       no custom exception and no broad interception of arbitrary Python errors. Reject
       bool, int/tuple subclasses, floats, Fraction, lists, iterators, None, ExactValue,
       Witness, and duck-typed numeric/sequence objects where exact ints/tuples are required.
       Wrong call arity retains Python behavior. Messages are diagnostic, not stable API.
    5. Structural versus numerical equality. RawPair is an ordinary immutable tuple, so
       Python tuple equality and hashing describe stored fields; neither is a numerical
       rational-equivalence operation. ExactValue's existing structural equality/hash and
       rejection of nonpositive denominators remain unchanged. `compare_pairs` is the
       explicit numerical comparison: for left=(A,B), right=(C,D), compare A*D with C*B
       and return the exact built-in int -1, 0, or 1. Numerically equal pairs return 0 even
       when their fields differ. Never compare tuples lexicographically, divide, reduce,
       or use hash identity as a numerical decision. Equal values do not select a preferred
       record, witness, family, or h value; later callers retain their governed tie policy.
    6. Sign. `pair_sign((A,B))` returns the exact built-in int -1, 0, or 1 according to A.
       B must still be validated even though B > 0 makes the sign depend only on A. No
       positive-numerator requirement, negative-value clamp, tolerance, or float conversion
       is introduced. Zero is an ordinary rational value, never an Empty-state decision.
    7. Literal update operations. For pair=(A,B), `pair_add_one` returns exactly (A+B,B).
       For newton=(A,B), current=(C,D), `pair_reflect` returns exactly
       (2*A*D-C*B, B*D), representing 2*newton-current. Do not reverse the argument roles,
       reduce, cancel common factors, replace zero by (0,1), or shortcut equal numerical
       inputs to one operand. Return the exact tuple prescribed by the formula, including
       on cancellation and equal-denominator inputs. Negative reflected points are valid
       arithmetic results and are not clipped or rejected merely for being negative.
    8. Source algorithm boundary. A standard Newton point is freshly formed from (c,h),
       with h > 0 established by its branch-domain owner. Standard initialization is
       pair_add_one((c,h)) == (c+h,h); accelerated initialization is (c,h) WITHOUT the +1.
       At a continuing accelerated step, newton in pair_reflect is a freshly formed
       c_j(U)/h_j(U) point, while current is the stored iterate. A failed look-ahead resets
       the later branch loop to the queried standard point, not to a re-encoded expression
       involving the prior denominator. These are integration requirements inherited from
       alg:standard-branch/alg:branch, not implemented control flow in this scalar unit.
       In particular, make_pair(c,h) rejects h <= 0 and never repairs a violated
       denominator invariant. Positive denominator validation does not establish source
       provenance or replace the branch owner's proof that its h_j(U) is valid.
    9. Residual numerator. For parameter=(A,B), return the exact built-in int B*c-A*h.
       c and h may each be signed or zero at this graph-independent linear-form boundary.
       The scalar function does not establish that they came from a feasible branch shore.
       A branch consumer must separately establish h_j(U) > 0 whenever h_j is used as a
       denominator; accepting an arbitrary scalar h here does not relax prop:branch-transform.
       This function does not return F_j, find a minimizer, subtract graph shifts, or choose
       a shore. The represented rational residual is (B*c-A*h)/B; B > 0 makes its sign and
       zero status exactly those of the returned numerator. Different raw encodings of the
       same parameter can scale this numerator: compare raw residuals directly only for
       the SAME parameter pair; across denominators use explicit rational comparison.
    10. ExactValue bridge. Unit 08's ExactValue remains a distinct record, never an alias
        for RawPair and never implicitly accepted by these functions. A caller comparing
        two value records explicitly supplies (left.N,left.D) and (right.N,right.D) to
        compare_pairs. This copies fields without changing either record or dividing.
        A caller deliberately creating ExactValue from an already valid pair may pass its
        two entries to the existing constructor; that creates only a record, not proof of
        witness admissibility, raw attainment, or optimality. Witness-attaining output is
        still computed by witness_value, not fabricated from an equivalent arithmetic pair.
        No conversion adapter imports or edits witness.py in this unit.
    11. Exactness, work, and number growth. The source of rational.py uses only the above
        exact integer formulas, fixed-size tuple access, type/shape tests, and comparisons.
        No float literal/conversion/arithmetic, Fraction, decimal, math, gcd, floor/true
        division, remainder-based reduction, tolerance, unordered set iteration, explicit
        copies, recursion, or magnitude/bit-length-driven loop is allowed. On valid input
        each public call uses a bounded constant number of integer arithmetic/comparison
        operations and O(1) integer objects; integer bit sizes and actual bit time can grow.
        Do not assert constant byte memory, constant wall-clock time, or a production
        asymptotic bit-length cutoff. `pair_reflect` preserves the exact recurrence to which
        lem:bitgrowth applies when the newton operand has input-bounded encoding length.
        No polynomial bound for arbitrary compositions with two growing operands is claimed.
    12. Completion and conformance boundary. Unit 09 supplies these arithmetic primitives,
        not algorithm-level termination, argmin tie-breaking, residual minimization,
        sign-routing, branch-value reconstruction, certificate verification, or telemetry.
        TEST_PLAN's historical R1--R5 and all previous sections remain unchanged. Add new
        prospective obligations and a gate at its end. After tests, independent arithmetic
        checks, and source inspection pass, append a narrow engineering
        CONFORMANCE note without promoting lem:standard-bits, lem:bitgrowth, branch, or
        global theorem rows. Their algorithm-level obligations remain with later units.
        The complete three-file staged tree must then pass isolated verification before
        the implementation commit, in the order fixed by TEST_PLAN section 24.

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

4.7 Production branch coefficients and sign-routing
    (RULED upon controlled adoption, 2026-09-06)
    1. Ownership. `exactfrac.sign_routing` constructs the uncontracted nonnegative cut
       representation of lem:sign-routing and the four integer coefficient forms prescribed
       by prop:branch-transform and eq:param0--eq:param3. It performs no cut minimization.
       Its only imports are dataclasses, .instance (Instance), .rational (RawPair and
       validate_pair), and optional future annotations. In particular it imports no flow,
       families, witness, oracle, branch, solve, certificate, verifier, math, or fractions.
       No closed module or package-root export changes. The section-3 layout entry and
       explicit addition of sign_routing to section 4.5.3 are the only amendments to
       pre-existing DESIGN lines. The mathematical source and its contract are unchanged.
    2. Exact public surface. The module __all__ is exactly the sorted tuple
         ("SignRoutedNetwork", "SignRoutingCoefficients", "branch_coefficients",
          "build_sign_routed_network", "recover_objective").
       Public signatures, accepting positional or the shown keyword arguments, are:
         SignRoutingCoefficients(a: int, gamma: tuple[int, ...], constant: int)
         SignRoutedNetwork(vertex_count: int, arcs: tuple[tuple[int, int, int], ...],
                           negative_shift: int, constant: int)
         branch_coefficients(instance: Instance, branch: int, parameter: RawPair)
             -> SignRoutingCoefficients
         build_sign_routed_network(instance: Instance, coefficients: SignRoutingCoefficients)
             -> SignRoutedNetwork
         recover_objective(network: SignRoutedNetwork, cut_value: int) -> int
       No hidden mode, backend selection, optional normalization, branch selector alias,
       separate public Arc class, or implicit record conversion is introduced.
    3. Coefficient record. SignRoutingCoefficients is a frozen, slotted, structurally
       hashable dataclass with exactly the stored fields (a, gamma, constant), in that order,
       and no generated ordering. Validate a as an exact built-in int with a >= 0, then
       gamma as an exact tuple whose entries are exact signed built-in ints, then constant
       as an exact signed built-in int. Preserve all values literally; gamma may contain
       zeros or be empty as a standalone shape. The instance-aware builder, not this record,
       requires len(gamma) == instance.n. Store no Instance, branch, parameter, Q, degree
       cache, or independent copy of a derived shift in this record. Valid construction
       asserts scalar representation only, not provenance from a branch or instance.
    4. Network record. SignRoutedNetwork is a frozen, slotted, structurally hashable
       dataclass with exactly the stored fields (vertex_count, arcs, negative_shift,
       constant), in that order, and no generated ordering. vertex_count is the original
       vertex count, an exact built-in int >= 1, not the enlarged network's node count.
       Read-only properties node_count, source, sink return vertex_count+2, vertex_count,
       vertex_count+1 respectively; store no second authoritative terminal/node count.
       Validate vertex_count first, then arcs completely, then negative_shift as an exact
       built-in int >= 0, then constant as an exact signed built-in int. arcs is an exact
       tuple of exact triples (tail, head, capacity). Per triple: check shape, exact integer
       types in that order, endpoint range 0 <= endpoint < node_count, tail != head, then
       capacity >= 0. Retain zero-capacity records, supplied order, and repeated directed
       pairs; do not sort, aggregate, repair, discard, or synthesize arcs in the constructor.
       An empty arc tuple is structurally valid, but the builder below never emits one
       for a production Instance. This record is not an independent certificate that its
       arcs and shifts realize any particular coefficients/Instance. That semantic promise
       belongs to build_sign_routed_network and the two identity tests, not to arbitrary
       caller-constructed records. Direct construction is not a contracted-network adapter.
    5. Consumer validation. Instance-keyed functions first require type(instance) is
       Instance and consume a normally constructed canonical active instance. They neither
       reaggregate it nor repeat its active check. branch_coefficients next checks exact
       int branch in (0,1,2,3), then calls the closed validate_pair on parameter before any
       graph-dependent coefficient arithmetic. build_sign_routed_network next requires
       type(coefficients) is SignRoutingCoefficients and matching gamma length before
       constructing any arcs; it accepts arbitrary valid coefficients, not only branch
       outputs. recover_objective first requires type(network) is SignRoutedNetwork, then
       exact built-in int cut_value >= 0, before shift arithmetic. These consumers rely on
       normally constructed immutable records, not objects forged by bypassing constructors.
       Malformed data through these signatures raises exact built-in ValueError. Reject
       bool, numeric/container/record subclasses, floats, Fraction, coercible objects,
       generators, and duck-typed replacements where exact types are required. Do not
       invoke their coercion/arithmetic methods or blanket-catch arbitrary exceptions.
       Wrong call arity and attempted frozen-record mutation retain Python behavior.
    6. Branch coefficient table. Write parameter=(A,B), with exact A and B > 0, and let
       f_v=instance.f[v], d_v=d_q(v). Obtain the complete degree tuple once before scanning
       vertices in increasing order. The sole production table is:
         branch   a    gamma[v]                       constant (kappa)
         0        B    (A+B)*f_v - A*d_v               -(A+B)
         1        B    (A+B)*f_v - A*d_v               -2*B
         2        B    -B*d_v - A*f_v                  A
         3        B    -B*d_v - A*f_v                  -2*B
       Return the literal coefficient record, without rational reduction or rescaling.
       A may be negative or zero. The shared gamma formulas for 0/1 and 2/3 do not permit
       their different constants to be merged. No U, family, parity, denominator h_j(U),
       witness, or branch-feasibility check occurs at this coefficient-construction step.
    7. Coefficient identity. For s=f(U), b=b_q(U), d=d_q(U), the literal source forms are
         c_0=s+b-1,   h_0=d+1-s;
         c_1=s+b-2,   h_1=d-s;
         c_2=b-d,     h_2=s-1;
         c_3=b-d-2,   h_3=s.
       The returned coefficients satisfy, for every U subset of V,
         B*c_j(U)-A*h_j(U) = a*b_q(U) + sum(gamma[v] for v in U) + constant.
       Outside D_j this is an identity of polynomial extensions of the source expressions,
       not a claim of branch admissibility or positivity of h_j(U). Tests include U=0 and
       U=V without passing their h_j to the positive-denominator RawPair constructor.
    8. Generic construction and terminal identity. The builder supports all a >= 0 and
       signed gamma vectors of the matching size, with any signed constant, on the
       production Instance domain. The broader lemma does not require an active graph;
       this API deliberately consumes the already-closed active Instance rather than
       adding another graph-input/normalization API. Original vertices keep indices
       0..n-1; source=n, sink=n+1, node_count=n+2. The symbols source/sink are not the
       fixed-shore scalar s=f(U). No anchor p, contraction, terminal parity, or forced
       membership is processed in this unit.
    9. Literal arc emission. In canonical edge_ref order, each instance edge (u,v,q_e)
       emits (u,v,a*q_e), immediately followed by (v,u,a*q_e). Then, in increasing vertex
       order, gamma[v] >= 0 emits (v,sink,gamma[v]) followed by (sink,v,gamma[v]); gamma[v]
       < 0 emits (source,v,-gamma[v]) followed by (v,source,-gamma[v]). Every undirected
       support edge AND spoke is represented by two opposite original capacity arcs, per
       the source's undirected-to-directed conversion. Do not divide their capacities by
       two or confuse an opposite original arc with a flow backend's residual reverse arc.
       Retain gamma[v] == 0 as two zero-capacity sink-spoke arcs. When a == 0, retain both
       zero-capacity support arcs too. Thus the uncontracted builder emits exactly
       2*(instance.m+instance.n) original arc records and n+2 vertices, independently of
       the signs/zeros of coefficients. This sharpens the source's upper bound only for
       this explicitly ruled uncontracted representation, not for later contracted graphs.
    10. Separate shift and constant. While constructing spokes compute exactly
          C_minus = sum(-gamma[v] for v with gamma[v] < 0).
        Store it as network.negative_shift and copy coefficients.constant literally into
        network.constant. They remain distinct named integers. The branch constant is not
        an arc capacity, no direct source-sink arc is introduced for it, and the builder
        never folds constant into C_minus or redefines either field as a net offset.
        There is no external mutation of these fields or authoritative duplicate shift.
    11. Cut identity and recovery. A corresponding source shore is X_U={source} union U,
        encoded by U | (1 << source), with sink outside. A directed cut counts only arcs
        whose tail lies in X_U and head lies outside. Each symmetric arc pair contributes
        its capacity exactly once when its underlying edge crosses. Hence
          cut_capacity(X_U) = a*b_q(U) + sum(gamma[v] for v in U) + negative_shift,
        and recover_objective(network, cut_value) returns the exact signed built-in int
          cut_value - network.negative_shift + network.constant.
        Negative recovered values are valid. The routine only removes these known shifts:
        it does not verify that cut_value is a cut of this network or a minimum, determine
        a source shore, evaluate c_j/h_j, or certify feasibility/attainment/optimality.
        For a nonempty permitted family, minimization is equivalent over that SAME family;
        an unrestricted minimum cut is not a substitute for its forced/parity constraints.
        Unit 12 must still reconstruct U and independently re-evaluate the source raw
        residual before global candidate comparison as required by CONTRACT/alg:branch-min.
    12. Determinism and downstream boundary. The emitted raw arc order is fixed for
        reproducible construction/fixtures. The closed flow backend separately sorts and
        aggregates its own input and supplies the unique inclusionwise-minimal minimum
        source shore of the fixed ordinary-cut problem. Do not claim that varying raw arc
        order provides alternative such extremal shores, or add a new within-cut tie rule.
        Section 4.6's first-encountered rule concerns candidates across families. No flow
        call, contraction, loop deletion/parallel aggregation for contractions, parity
        anchor, terminal-set toggle, GR parity minimization, or minimizer selection occurs
        in sign_routing.py. Units 11/12 own those transformations/integration separately.
    13. Exactness and structural work. Constructors preserve raw integer values and use
        exact type/shape/range checks only. Coefficient validation scans O(len(gamma));
        network-record validation scans O(len(arcs)); derived terminal properties and
        recover_objective use O(1) integer operations on valid records. branch_coefficients
        uses O(n+m) integer operations, with d_q obtained once, not once per vertex.
        build_sign_routed_network uses O(n+m) operations and O(n+m) integer records, including
        immutable result validation. Loop bounds are structural vertex/edge/record counts,
        never capacities, coefficient magnitudes, Q, or operand bit lengths. No explicit
        copies, all-shore production enumeration, unbounded recursion, algorithmic Python
        set iteration, float literal/conversion/arithmetic, Fraction, decimal, math, gcd,
        division, remainder reduction, tolerance, or synthetic infinite capacity is used.
        Actual integer bit costs grow with input encoding lengths; no constant byte-memory
        or wall-clock claim, numeric cutoff, or asymptotic assertion is installed in code.
        Telemetry and the full branch-oracle complexity carriers are later obligations.
    14. Independent evidence and completion. Hand-derive and commit coefficient, arc,
        shift, zero/sign, malformed-input, all-shore, label, and huge-integer oracle cases
        before their tests or production code. The coefficient comparator computes s,b,d
        directly from instance records and applies the source c_j,h_j table, not production
        branch_coefficients or a family-derived domain. The cut comparator counts crossings
        in the actual emitted original arcs, without calling flow or sharing construction
        code. Freeze a bounded independent corpus and counts before consuming tests.
        After GREEN and a separate definition-level audit, add a narrowly worded
        lem:sign-routing CONFORMANCE row for the operational-domain cut identity, plus an
        engineering note for coefficient/representation obligations. Preserve every existing
        theorem row/status; do not promote prop:branch-transform's ratio theorem, the
        parity reduction, thm:branch-oracle, branch/global correctness, or bit-growth rows.
        Finite tests are executable evidence, not a universal proof or a min-cut certificate.
        Isolate the complete code/test/CONFORMANCE staged tree before its atomic commit,
        in the order fixed by the appended TEST_PLAN Unit 10 gate.

4.8 Production atomic-family parity-cut reduction
    (RULED by the Unit 11 authority commit; subordinate to the pinned mathematical source)

    1. Ownership and source. exactfrac/parity_cut.py owns forced contraction, parity-anchor
       bookkeeping, lifting between its two explicit vertex universes, and the thm:GR
       ordinary-cut specialization. It consumes the closed AtomicFamily, SignRoutedNetwork,
       finite-shore validator, and exact minimum_cut contracts. Source: the forced-membership
       paragraph following lem:sign-routing, lem:parity-anchor and proof, thm:GR and proof,
       lem:ek including E=0, and alg:branch-min's reconstruction/shift step. The cited primary
       Goemans--Ramakrishnan Theorem 2/Corollary 3 (p.502) and Section 5 (p.511) supply the
       two-element restricted-lattice enumeration; Section 3.1.1 (p.507) supplies its cut
       specialization. The source uses least ordinary lattice minimizers, not arbitrary
       tied ordinary cuts. Its no-perturbation implementation is residual reachability as
       required by the already-closed flow backend. The choices of records, vertex order,
       compatible-pair order, zero handling, and diagnostics below are engineering rulings.
       This unit does not implement ExactBranchMin or change the mathematical specification.

    2. Public surface. The exact sorted tuple __all__ is:
           ("ParityCutProblem", "ParityCutResult", "ParityCutStats",
            "lift_source_shore", "minimum_parity_cut", "reduce_atomic_family")
       Public record constructors and signatures, with these positional/keyword names:
           ParityCutProblem(vertex_count: int, classes: tuple[int, ...],
                            arcs: tuple[tuple[int, int, int], ...], terminal_mask: int)
           ParityCutResult(cut_value: int, source_shore: int)
           ParityCutStats(mincut_calls: int, flow_augmentations: int,
                          flow_bfs_scans: int, flow_peak_generated_value: int)
           reduce_atomic_family(network: SignRoutedNetwork, family: AtomicFamily)
               -> ParityCutProblem | None
           lift_source_shore(problem: ParityCutProblem, source_shore: int) -> int
           minimum_parity_cut(problem: ParityCutProblem)
               -> tuple[ParityCutResult | None, ParityCutStats]
       All three records are frozen/slotted dataclasses, structural equality/hash, no order.
       No fields have default values. The minimum-parity result and diagnostics are separate;
       no counters are put in ParityCutResult. No package-root exports are added.

    3. Two vertex universes, never implicit. ParityCutProblem.vertex_count is the number n
       of ORIGINAL nonterminal vertices. It is an exact built-in int >=1, matching the
       standalone SignRoutedNetwork domain; production Instances happen to have n>=2.
       Original vertices are 0..n-1, original source is n, original sink is n+1, and an
       optional zero-cost anchor is n+2. classes is an exact tuple of at least two exact
       positive int masks over this augmented original universe. Its index is a REDUCED
       vertex; its value is that reduced vertex's original preimage mask. Specifically:
       - classes[0] contains bit n, no bit n+1, and optionally the anchor bit n+2;
       - classes[1] contains bit n+1, no bit n, and never the anchor bit;
       - every later class is one original-vertex singleton, ordered by increasing vertex;
       - classes are pairwise disjoint and cover all bits 0..n+1 exactly once, with only
         the optional bit n+2 additionally permitted, and only in classes[0].
       No other high bit, missing original vertex, repeated class member, or alternate class
       order is valid. Original vertices in classes[0]/classes[1] are the forced sides.
       Derive read-only properties source=0, sink=1, node_count=len(classes). They are not
       redundant stored fields. Do not identify original vertex 0 with reduced source 0.

    4. Problem-record validity. Validate n first, then the complete classes representation,
       then the complete arcs representation, then terminal_mask. arcs is an exact tuple of
       exact triples (tail, head, capacity). Validate all three entries' exact int types
       before their numeric comparisons, require endpoints in 0..node_count-1, tail!=head,
       capacity>=0, and strictly increasing (tail,head) keys. Thus arcs has no parallel
       directed pairs or loops; capacities of encountered zero pairs are retained.
       An empty arcs tuple is valid. No symmetry requirement is imposed: nonnegative directed
       cut functions also meet the invoked submodularity hypothesis, and a normally built
       standalone SignRoutedNetwork may be directed. The builder-generated symmetric case
       remains a special case. terminal_mask is an exact nonnegative int with no bits outside
       node_count and with EVEN bit_count, including zero. Both source and sink may be
       terminals. Constructor inputs are checked, not repaired, reordered, or normalized.
       Shape/partition validity is not proof that a record arose from any particular family.

    5. Result/diagnostic validity. ParityCutResult checks exact int cut_value>=0 first,
       then exact int source_shore>=0 with reduced source bit 0 present and sink bit 1 absent.
       Without a problem it cannot check the upper universe bound, terminal parity, attained
       cut value, or optimality. Those are minimum_parity_cut's output guarantees.
       ParityCutStats checks exact int nonnegativity of its four fields in declaration order.
       It does not infer an audit claim from arbitrary caller-supplied counters.

    6. Errors and validation precedence. Public data violations raise the exact built-in
       ValueError, not a new exception or a subclass. Wrong call arity retains normal Python
       behavior. Do not coerce bool, numeric/container subclasses, generators, or duck-typed
       substitutes. reduce_atomic_family validates exact SignRoutedNetwork type, then exact
       AtomicFamily type, then calls the closed validate_shore on family.T, family.I, family.O
       in that order using network.vertex_count. It does this before deciding family emptiness
       or scanning capacities. Use family.is_nonempty as the closed logical predicate; do not
       duplicate its formula. An out-of-universe mask is invalid, whereas a well-shaped family
       with overlapping I/O or impossible parity is valid but infeasible and returns None.
       lift_source_shore validates exact ParityCutProblem type, then the reduced finite mask,
       then source-present/sink-absent geometry. minimum_parity_cut first validates exact
       ParityCutProblem type. Normally constructed frozen records are trusted after type checks;
       constructor-bypassing forgeries are outside this contract. Do not catch arbitrary backend
       failures and turn them into None or ValueError; they are not family infeasibility.

    7. Forced contraction and canonical original preimages. For a feasible atomic family,
       form classes[0] from I and original source, classes[1] from O and original sink;
       if pi=0, also put the new isolated anchor in classes[0]. The remaining original vertices
       are singleton classes in increasing order. Build one old-to-reduced index map, including
       the optional anchor. This is contraction, never a finite 'infinity' edge, a big-M
       constraint, or a numeric perturbation. No anchor edge is introduced: its only roles are
       a forced-inside preimage bit and one base-terminal token. pi=1 uses no anchor at all.
       Every valid source/sink reduced shore has a unique corresponding original shore meeting
       the forced memberships, and conversely. Original empty/full shores are allowed when
       the family allows them. Family feasibility is not witness admissibility.

    8. Capacity transport. Map each supplied original directed arc through the contraction.
       Discard an arc iff its mapped endpoints coincide. Sum capacities of equal ordered
       endpoint pairs by exact integer addition and emit one triple per encountered nonloop
       pair in increasing (tail,head) order. A pair whose sum is zero is still emitted.
       Sort mapped nonloop records and aggregate equal adjacent keys, or an equivalent method
       with the stated deterministic output and O(E_in log(E_in+1)) comparison carrier.
       Do not invent zero pairs that never occurred, divide symmetric arcs by two, mix an
       original reverse arc with a residual reverse entry, or absorb constants into capacities.
       The same transport rule applies to further two-element contractions in item 12.
       Contraction adds no cut-value shift. The source network's negative_shift and constant
       are neither changed nor stored in ParityCutProblem; the caller retains that network.

    9. Terminal transport and the sink toggle. Start with base_terminal_mask=family.T for
       pi=1; for pi=0, add the anchor bit n+2. A reduced vertex is terminal exactly when its
       class contains an ODD number of these base terminals. This is XOR aggregation, not
       Boolean presence/OR: two terminal tokens in one class cancel modulo two.
       If the resulting reduced terminal mask has odd bit_count, toggle reduced sink bit 1
       by XOR. Toggle even if sink is already a terminal, in which case the toggle removes it.
       Otherwise leave the mask unchanged. Its total cardinality is now even. Sink is outside
       every source shore, so this last toggle does not change source-shore intersection parity.
       For every corresponding pair X,U, odd |X intersect terminal_mask| is equivalent to
       |U intersect family.T| mod 2 == family.pi; cut capacities also agree.
       Feasible family inputs yield a nonzero final terminal mask. None is returned for the
       infeasible families in item 6, not an empty/fake problem or an arbitrary zero shore.

    10. Lifting is a conversion, not an optimization check. lift_source_shore unions the
        preimage masks of the selected reduced vertices, then intersects with (1<<n)-1.
        This strips both fixed terminals and any anchor. Return an exact built-in int, possibly
        0 or the full original mask. The function accepts source/sink reduced shores of EITHER
        terminal parity. It does not check oddness, compute a cut, or certify feasibility under
        a supplied family. Returned minimum_parity_cut shores carry the oddness guarantee;
        generic lifting tests must still cover the even shores without requesting a min-cut.

    11. Exact parity-cut objective. minimum_parity_cut minimizes the sum of ORIGINAL directed
        arc capacities leaving X over all reduced masks X with source in X, sink outside X,
        and odd |X intersect terminal_mask|. The value is unshifted and nonnegative. The result
        shore is in the problem's REDUCED universe, not the original-vertex universe and not
        the temporary vertex universe of a pair-restricted call. Return (None, zero stats)
        immediately for terminal_mask==0; this is infeasible, not malformed. For even nonzero
        terminal_mask this full source/sink lattice contains an odd shore, independently of
        capacities: there is a free terminal whose inclusion can be toggled, or T={source,sink}.
        Do not infer infeasibility from E=0, zero cut value, all-zero capacities, disconnectedness,
        or an ordinary least minimum shore having the wrong parity.

    12. Goemans--Ramakrishnan specialization. For nonzero terminal_mask enumerate every pair
        (a,b) of reduced vertices with a!=sink, b!=source, a!=b. Use increasing a, then increasing
        b; the first pair is (source,sink). For each pair, further contract source with a and
        sink with b. Temporary source and sink are again 0 and 1; other problem vertices remain
        singleton classes in increasing problem-vertex order. Build the temporary-to-problem
        class masks and map arcs by item 8. Invoke the closed minimum_cut exactly once on this
        ordinary nonnegative network. Its inclusionwise-minimal minimum source shore is a
        load-bearing requirement, not merely a deterministic choice. Lift that shore to the
        BASE PROBLEM'S reduced universe, then test oddness using problem.terminal_mask there.
        Retain it iff odd and it improves the incumbent value strictly; the first valid candidate
        initializes the incumbent. Equal values never replace it. Return the chosen cut value
        literally and its base reduced mask. No zero-valued early success return, duplicate-pair
        elimination, or skipped compatible pair is permitted in this reference implementation.
        Incompatible pairs are excluded without invoking flow. No terminal reanchoring is needed
        inside an ordinary pair query; parity is filtered AFTER lifting to problem coordinates.
        The source/sink lattice excludes the full ground set and the empty set, so GR's explicit
        {empty,full} candidates are irrelevant here. Its remaining pair candidates suffice by
        Theorem 2, which is stronger than a mere existence of some tied ordinary minimizer.
        The selected parity minimizer need only be exact and deterministically first encountered;
        do not claim it is the inclusionwise-minimal parity minimizer. No secondary key by
        cardinality, mask, denominator, family, or witness is added to cut-value comparison.

    13. Ordinary backend and diagnostics. Each ordinary query uses minimum_cut and consumes
        its MinCutResult and FlowStats without changing the closed backend or exposing its
        internal residual objects. For N=problem.node_count, a nonzero terminal mask uses
        Q=N*N-3*N+3 compatible-pair calls, including the N=2 case Q=1. The terminal_mask==0
        shortcut uses zero calls. ParityCutStats.mincut_calls counts actual invocations;
        flow_augmentations and flow_bfs_scans are exact sums of those backend counters;
        flow_peak_generated_value is their maximum peak_generated_value, or zero for no calls.
        This peak is FLOW-ONLY, not the largest coefficient, contraction sum, mask, or integer
        generated anywhere in the reduction. Stats never affect candidate selection, acceptance,
        infeasibility, or certificate fields. Do not add clocks, environmental metadata, or
        algorithm-wide bit-growth telemetry here. Later branch/SolveStats integration remains
        separate. Zero-arc calls still count as calls; their closed backend arc-scan and
        augmentation counts are zero, with nonzero vertex-initialization work in the carrier.

    14. Exactness, dependencies, and finite universes. Permitted imports are optional future
        annotations, dataclasses.dataclass, and the specific closed symbols from families,
        sign_routing, shore, and flow used above. Do not import a verifier, test, oracle, branch,
        solve, certificate, external graph library, JSON, or private handoff artifact. Transitive
        closed-module imports do not authorize new direct dependencies. No Fraction, float
        literals/conversions, division, gcd reduction, tolerance, epsilon, capacity-based big-M,
        randomness, recursion, or all-shore/all-subset enumeration is permitted in production.
        Bit masks stay finite; use explicit universes, not bare complement as a shore.
        Iteration ranges depend on n,N,arc records,classes,or compatible vertex pairs, never on
        capacity magnitudes. No algorithmic iteration over sets. Temporary sets/dicts, if used
        for membership/aggregation, must not determine an unsorted output or candidate order.
        Do not change previously closed code, tests, package __init__ files, or toolchain policy.
        Section 4.5.3's prohibited arithmetic-path module list explicitly gains parity_cut.

    15. Structural-work and bit-growth carriers. Let E_in be the number of supplied network
        arc records, and N,E the final reduced problem vertex/arc counts. Constructor/initial
        contraction/lifting work is bounded by O(n+E_in log(E_in+1)) for reduction, O(n+N+E)
        for general problem validation, O(N) integer operations for lifting, and O(1) for
        result/stats validation and derived properties. Sequential pair processing uses
        O(N+E log(E+1)) normalization/lifting work per ordinary call, plus closed flow work
        O(N+NE^2). Thus a nonzero-T solve has a zero-safe O(N^3*(1+E^2)) carrier; empty T
        returns in O(1) after the normally validated problem type check. Do not copy all N^2
        temporary graphs/candidates into memory: process one at a time with O(N+E) auxiliary
        integer records. The original preimage map has O(n+N) integer records. These are
        integer-operation/record bounds, not constant bit-memory or elapsed-time claims.
        Contraction capacities are sums of subsets of original directed records, bounded by
        S=sum(input capacities), with S=0 for no arcs. No multiplying capacity by another
        capacity or artificial feasibility bound occurs. Flow/record/mask quantities therefore
        have polynomial bit length in the input encodings; masks include O(n) vertex bits.
        Graph sizes remain N<=n+3 and E<=E_in; on Unit 10 builder outputs E_in=2(m+n).
        Combining these bounds into thm:branch-oracle is Unit 12 work, not a new Unit 11 claim.

    16. Evidence and completion. Register contraction classes, transported terminal masks,
        retained-zero/aggregated arcs, lifted shores, infeasible cases, and GR exact results/
        pair orders/call counts in ORACLE_CATALOG before consuming tests. Test correspondences
        on all tiny source/sink shores; compare parity minima with an independent literal
        directed-cut enumeration, not the production reducer or the backend's chosen result.
        Separately verify that each ordinary call returns the intersection of all its minimum
        shores on the small fixtures; arbitrary tied ordinary cuts are not a sufficient oracle.
        Freeze corpus domains/counts and hostile-type expectations before production code.
        After GREEN and independent auditing add narrowly scoped lem:parity-anchor and thm:GR
        CONFORMANCE rows, mapped to test_parity_anchor_correspondence and
        test_minimum_parity_cut respectively, plus an engineering note for contracts/stats.
        Preserve every previous row/status; do not promote thm:branch-oracle, branch/global
        correctness, source ratio/witness claims, certificate work, or outer bit-growth theorems.
        Unit 12 still owns retaining the Unit 10 network, lifting to original U, recovering
        shifts once, and independently re-evaluating B*c_j(U)-A*h_j(U) before comparisons.
        No Unit 11 record is an independent admissibility, attainment, or optimality certificate.
        Follow the tests-first and atomic closure order in the appended Unit 11 completion gate.

4.9 Production exact branch residual oracle
    (RULED — Unit 12 authority R1, 2026-09-08)
    1. Source binding and scope. exactfrac/oracle.py implements alg:branch-min and the
       composed fixed-parameter contract of thm:branch-oracle. Its mathematical inputs are
       an active Instance, branch j in {0,1,2,3}, and lambda=A/B with B>0. Its task is an
       exact minimum of B*c_j(U)-A*h_j(U) over the ORIGINAL branch domain D_j, or None iff
       that domain is empty. This is not minimization of c_j/h_j and is not a branch loop.
       The numerical identities and domains are those of prop:branch-transform;
       prop:domain-decomp supplies their complete ordered covers. Sections 4.6--4.8 and
       the closed family, rational, and shore-sum interfaces are dependencies, not replaced
       algorithms. No code, consuming test, oracle fixture, or CONFORMANCE row lands in
       this authority step. This subsection is added without changing preceding rulings.

    2. Public surface and parameter-free preparation. The Ruff-sorted __all__ is exactly
         ("BranchOracleContext", "BranchOracleResult", "BranchOracleStats", "exact_branch_min").
       Public signatures (ordinary positional-or-keyword arguments, no mode/defaults) are
         BranchOracleContext(instance: Instance) -> None
         BranchOracleResult(shore: int, c: int, h: int, residual: int) -> None
         BranchOracleStats(atomic_families_examined: int, atomic_families_feasible: int,
             parity_cut_calls: int, ordinary_min_cut_calls: int, flow_augmentations: int,
             flow_bfs_scans: int, flow_peak_generated_value: int) -> None
         exact_branch_min(context: BranchOracleContext, branch: int, parameter: RawPair)
             -> tuple[BranchOracleResult | None, BranchOracleStats].
       All three classes are frozen, slotted dataclasses with structural equality/hash,
       no generated ordering, and no user-supplied field defaults. Package __init__ stays
       export-free. There is no alternative Instance-only query signature, arbitrary-family
       argument, backend selector, batch query, coefficient adapter, or public evaluator.
       The prepared context is an engineering interface for sharing the already-ruled
       enumeration once; it is not a new mathematical oracle input or an optimization.

    3. Context provenance and construction. BranchOracleContext stores exactly instance
       and families, in that order. instance has annotation Instance; families has annotation
       tuple[tuple[AtomicFamily, ...], ...], declared field(init=False). The constructor first
       requires type(instance) is Instance. It then calls the closed enumerate_atomic_families
       exactly once and stores its complete four-tuple verbatim as families. That dependency
       supplies normally constructed, finite-universe descriptors in the orders of section
       4.3A. No caller may supply, truncate, replace, reorder, filter, or deduplicate a family
       tuple through this constructor. Assigning the derived init=False field during
       __post_init__ is permitted via object.__setattr__ ONLY for families at that point;
       no subsequent mutation, hidden cache, parameter state, or global registry is allowed.
       The Instance itself is retained, not copied, coerced, reaggregated, or revalidated
       for the active condition. Labels play no algorithmic role. Wrong constructor arity
       (including an attempted families argument) retains Python behavior. A context can
       be reused across all four branches and any valid parameters. Context construction
       has its own explicit work charge in item 16; it is never silently repeated inside
       exact_branch_min. A complete, source-bound cover is not established by type-checking
       an arbitrary tuple, so an external tuple-of-families injection API is not provided.

    4. Result validity and meaning. BranchOracleResult stores exactly (shore,c,h,residual).
       In that declaration order, require exact built-in int shore>0, signed exact int c,
       exact int h>0, and signed exact int residual. Reject bool and numeric subclasses.
       No instance, branch, parameter, family index, cut graph, witness, or diagnostic data
       is stored. Without those inputs the constructor cannot verify the shore's upper
       universe bound, branch membership, the c/h formulas, or the residual equality.
       Normally returned results guarantee all of them by items 10--12. The record itself
       is not an independent certificate. A standalone zero/negative c or residual is valid;
       h is not reduced against c, and the raw integers are not normalized or rescaled.
       Infeasible is None, never a fake shore, zero tuple, Empty witness, or exception for
       a normally formed empty branch. All four D_j exclude the empty original shore.

    5. Separate statistics. BranchOracleStats validates its seven declared fields, in
       declaration order, as exact built-in nonnegative ints. Its read-only property
       max_flow_calls returns ordinary_min_cut_calls, because the reference parity layer
       invokes one closed max-flow per ordinary cut; do not store a duplicate counter.
       Arbitrary constructor values do not assert observed work or enforce relationships
       among fields. On a successful query, atomic_families_examined is the length r_j of
       context.families[j], including empty and repeated descriptors; atomic_families_feasible
       counts the k_j descriptors whose closed is_nonempty predicate is true; parity_cut_calls
       equals k_j. ordinary_min_cut_calls is the sum of their ParityCutStats.mincut_calls;
       flow_augmentations and flow_bfs_scans are sums; flow_peak_generated_value is the
       maximum of their flow-only peaks, or zero when there are no calls. No counters
       influence feasibility, shore/value selection, equality handling, or residual checks.
       This record does not count preparation, integer bit growth outside flow, elapsed
       time, outer iterations, or look-ahead. Section 8 SolveStats integration is deferred.
       atomic_families_examined is not renamed atomic_families_enumerated: construction
       occurred earlier in the context and must not be counted again on every query.

    6. Consumer validation and errors. exact_branch_min checks type(context) is
       BranchOracleContext, then type(branch) is int with branch in (0,1,2,3), then calls
       the closed validate_pair(parameter), before inspecting a selected family, testing
       its emptiness, or doing graph-dependent arithmetic. Thus invalid parameters still
       raise on an empty branch. Malformed public data through the ruled signatures raises
       exact built-in ValueError; no custom exception, coercion, or repair is introduced.
       Reject float/Fraction/ExactValue substitutes, bool, integer/tuple/record subclasses,
       iterators, and duck-typed objects where exact types are required. Wrong arity and
       frozen mutation retain Python behavior. Normally constructed immutable records are
       trusted after exact type checks; constructor-bypassing forgeries are outside scope.
       Do not catch arbitrary exceptions from closed dependencies. In particular a backend
       failure is not None or user-input ValueError. Explicit violated internal promises
       identified below raise RuntimeError, not false infeasibility or a silently skipped
       candidate; successful diagnostics/results are not returned after such a failure.

    7. Source domains and raw forms. For an original finite-universe shore U, obtain
       s=shore_f(instance,U), b=shore_b_q(instance,U), d=shore_d_q(instance,U) using the
       closed witness-module SUM HELPERS only. These helpers re-read original Instance
       records, not contraction classes, gamma coefficients, cut values, or residual arcs.
       Do not import/use Witness, ExactValue, witness validation, or witness_value here.
       The domain tests and literal integer pairs are
         j   membership in D_j                          c_j           h_j
         0   (s+b) odd                                  s+b-1         d+1-s
         1   (s+b) even, b>=1, d-s>0                     s+b-2         d-s
         2   s odd, s>=3                                b-d           s-1
         3   s even, b>=1                               b-d-2         s.
       This table is the original-shore evaluator, independent of the sole gamma/constant
       construction in section 4.7.6. Never derive c,h by reversing the recovered cut
       expression. Do not turn these pairs into ExactValue or normalize with gcd/Fraction.
       h_j>0 is an explicit check at the domain-owning seam, not silently repaired by a
       scalar factory. The polynomial extensions outside D_j remain source identities,
       but no result outside D_j is admitted. There is no ratio comparison at this layer.

    8. Fixed family traversal and empty cases. Select context.families[branch] by index;
       do not call the family enumerator again. Traverse every descriptor in its stored
       order. Use family.is_nonempty as the one closed nonemptiness predicate, not a
       locally duplicated formula. Empty descriptors are counted as examined and skipped
       before graph construction/reduction/minimization. Retain overlapping and repeated
       descriptors. If the tuple is empty return (None, all-zero stats) after input
       validation. If it is nonempty but all descriptors are empty, return None with
       examined=r_j and all other fields zero. There is no graph scan or cut call in these
       cases beyond the already-paid context preparation. Do not reinterpret either case
       as the global empty-admissible-family output or invoke the unit-witness baseline.

    9. One network per nonempty query; no graph leakage. Lazily, upon the first nonempty
       descriptor, call branch_coefficients(instance,branch,parameter) exactly once and
       build_sign_routed_network(instance,coefficients) exactly once. Retain THAT original
       network for all descriptors of this query. Its coefficients and arcs do not depend
       on the atomic family; hoisting this pure identical construction is the adopted
       engineering specialization of the source loop. No network survives into another
       parameter query, and the context stores none. Preserve the original separate
       negative_shift and constant. Do not cache a contracted problem across families,
       build the network for all-empty branches, or duplicate the gamma/constant table.
       The original network has n+2 nodes and exactly 2*(m+n) directed arc records.

    10. Per-family constrained minimum and original coordinates. For every descriptor
        passing is_nonempty, call reduce_atomic_family(network,family), then
        minimum_parity_cut(problem), exactly once each. Because this descriptor is
        nonempty, an unexpected None problem or None parity result is RuntimeError,
        not a reason to discard a feasible family. Never substitute ordinary minimum_cut
        for minimum_parity_cut or enumerate all original shores in production. The
        temporary-query/least-ordinary-cut discipline remains owned by the parity layer.
        Lift the returned problem-coordinate source shore with the closed
        lift_source_shore(problem,result.source_shore). This is the only result shore
        used by the branch evaluator. Check it against the original n with validate_shore,
        then check (U & family.I)==family.I, (U & family.O)==0, and
        ((U & family.T).bit_count() & 1)==family.pi. The membership check is an assertion
        about this returned candidate, not another family nonemptiness algorithm.
        A finite but membership-invalid original shore is RuntimeError. An exception
        from the closed lifting/universe validator propagates instead of becoming None.

    11. Evaluate first, recover once, compare only matching residuals. On each lifted
        original U, compute the three original sums and the literal c,h from item 7.
        Require the exact source domain condition and h>0, otherwise RuntimeError.
        Recompute raw= residual_numerator(parameter,c,h), i.e. B*c-A*h, with the closed
        rational helper. Separately call recover_objective(original_network,cut_value)
        exactly once for this candidate. The latter returns
          cut_value - original_network.negative_shift + original_network.constant.
        Require raw==recovered, otherwise RuntimeError. Contraction added no shift;
        do not subtract C_minus from raw, add constant twice, divide by B, fold offsets,
        or recover using another family's/parameter's network. The selected residual is
        raw, not an unverified cut value. This seam check is an internal consistency
        obligation; it is not an independent min-cut or density-optimality certificate.

    12. Incumbent and returned minimizer. Initialize best=None. After all candidate checks,
        accept the first feasible candidate or replace it only when raw<best.residual.
        On equality retain the incumbent without consulting h,c,shore cardinality/mask,
        family index, diagnostics, bit length, or another quantity. No early return on
        negative residual, zero residual, or a zero cut. After the full stored sequence,
        return (best,stats). A returned result has original shore in D_j, its literal
        c_j,h_j, and minimum raw residual over D_j. Mathematical permission for any exact
        argmin is unchanged; first retention only specializes reproducibility. Do not
        claim an inclusionwise-least parity/branch optimum or lexicographically least
        original shore. With closed correct dependencies, best is absent iff k_j=0.

    13. Raw-parameter, supergradient, and downstream handoff. A can be negative, zero,
        or positive; B is strictly positive and the submitted pair need not be reduced.
        For fixed (A,B), raw=B*(c-lambda*h), so minimizing raw is equivalent to minimizing
        the rational residual. For a returned U, F_j(lambda)=raw/B and -h is a valid
        supergradient as in lem:argmin-supergradient; these equalities do not authorize
        division or an outer Newton update here. A downstream caller explicitly retains
        its submitted B and extracts c,h from the result. Across differently encoded
        denominators, raw residual magnitudes are NOT directly comparable. Replacing
        (A,B) by (k*A,k*B), k>0, retains the deterministic shore,c,h and multiplies raw by k;
        it does not imply constant bit cost or a new general diagnostic invariance claim.
        For another parameter, rebuild the uncontracted network; never reuse prior shifts.

    14. Exact dependencies and source discipline. Permitted direct imports are optional
        future annotations; dataclasses.dataclass and field; Instance; AtomicFamily and
        enumerate_atomic_families; RawPair, validate_pair, residual_numerator; validate_shore;
        branch_coefficients, build_sign_routed_network, recover_objective (and their record
        classes for annotations); reduce_atomic_family, minimum_parity_cut, lift_source_shore
        (and their record classes for annotations); shore_f, shore_b_q, shore_d_q. No direct
        flow calls, verifier/test/private-JSON imports, outer branch/solve/certificate modules,
        external optimizer, reflection/Newton helper, filesystem/I/O, randomness, recursion,
        float literal/conversion, Fraction, division, remainder reduction, gcd, epsilon,
        big-M, or scalarized tie objective. Bit-parity tests use finite masks. No algorithmic
        set iteration or unsorted set-derived selection. No loop depends on q,f,A,B,Q,
        their magnitude/bit length, or a denominator search. Closed dependency imports
        remain permitted transitively without expanding this direct-import whitelist.

    15. Correctness chain to be audited. Context preparation fixes the complete source
        cover; empty-descriptor skipping preserves its union. For each remaining family,
        sign routing changes its residual by a fixed known shift, and Unit 11 preserves
        both constrained shores and cut capacities. The least-ordinary-cut GR specialization
        supplies a true minimum over that same family. Original lifting and direct source
        re-evaluation identify its raw residual. A strict minimum across the entire cover
        therefore returns an allowed ExactBranchMin argmin, with positive h from the
        domain theorem. Finite tests challenge each seam separately; a GREEN count is not
        a universal proof, and correct arithmetic alone does not prove completeness of
        a user-supplied partial cover (hence item 3).

    16. Preparation versus per-query work. Write r_j=len(context.families[j]) and
        R_all=sum(r_j for j in (0,1,2,3)); by section 4.3A,
          r_0=1, r_1=2*|P|*m, r_2=|A|+binom(|W|,3), r_3=2*m.
        A BranchOracleContext pays O(n+m+R_all) integer/comparison operations and
        O(R_all) descriptor records ONCE. Shared immutable Instance storage is not copied.
        Do not charge this all-branch preparation to r_0 or hide it in a per-branch bound.
        Per valid query, validation/empty handling costs O(1+r_j); if k_j>0, network
        construction costs O(n+m) once, and each feasible family costs at most
        O((n+3)^3*(1+(m+n)^2)) including reduction, zero-safe parity minimization, lifting,
        direct shore sums, and consistency checks. Since a production Instance has n>=2,
        m>=1, the uniform per-query carrier is
          O(1 + r_j*(n+3)^3*(m+n)^2),
        agreeing with thm:branch-oracle for r_j>=1 and explicitly totalizing the zero-
        descriptor case. Context construction is a separately counted front-end step.
        ordinary_min_cut_calls equals the sum of N_F*N_F-3*N_F+3 over the k_j feasible
        reduced problems; N_F<=n+3. Thus it is at most k_j*(n+3)^2. All query families
        process sequentially, retaining only one original network, one reduced problem,
        one current result and incumbent: O(n+m) auxiliary integer records beyond the
        context and the input. No collection of all candidate shores/graphs is retained.
        These are structural operation/record bounds, not bit-time or constant-byte claims.

    17. Number-size carrier, separate from counters. Let Q=sum(q_e). The active input gives
        0<=s<=d<=2Q and 0<=b<=Q on every original shore. Safe uniform bounds are
          abs(c_j)<=3Q+2, abs(h_j)<=2Q+1,
          abs(B*c_j-A*h_j)<=B*(3Q+2)+abs(A)*(2Q+1).
        With B>0 and d_q(v)<=Q, the coefficient table gives
          abs(gamma[v])<=(2*abs(A)+B)*Q, abs(constant)<=abs(A)+2*B.
        The original directed network's total capacity is
          S=2*B*Q + 2*sum(abs(gamma[v]) for v in V).
        C_minus<=sum(abs(gamma[v])). Contractions only drop loops and sum subsets of
        original capacities; their capacities and the closed flow values/residual
        capacities are bounded by S. Signed recovery, raw c/h/residuals, and O(n)-bit
        masks therefore have polynomial bit length in L+bits(A)+bits(B). Counts and
        flow-only stats add at most structural logarithmic factors. This source-bound
        derivation covers the composed query; it does not instrument every generated
        integer, discharge the outer lem:standard-bits/lem:bitgrowth obligations, or make
        flow_peak_generated_value a complete peak_integer_bits measurement.

    18. Evidence order and CONFORMANCE boundary. Register Unit 12 literal branch-domain
        minima, c/h/raw results, family order/counts, empty cases, signed parameters,
        shift/coordinate failures, and hand-derived diagnostic/call expectations BEFORE
        consuming tests. Expected minima come from original-record source-domain shore
        enumeration, not production family/flow/oracle output or the global density
        verifier. Freeze tiny corpus domains/counts before code. After tests-first GREEN
        and a separate definition-level audit, permit a narrowly scoped thm:branch-oracle
        CONFORMANCE row mapped to test_exact_branch_min, with the preparation/query
        accounting and polynomial-number-size review stated separately from finite tests.
        Preserve all prior rows/statuses. Do not promote prop:branch-transform's ratio
        claims, outer branch correctness/invariants/iteration bounds, global correctness,
        certificates, or peak-bit experiments. Standard/Accelerated outer loops, global
        H2/unit witness/comparison/reconstruction, and certificate construction/verification
        remain later units. Follow the appended Unit 12 completion gate exactly.

4.10 Production Standard branch solver
    (RULED — Unit 13 authority R1; effective on controlled authority commit)
    1. Source and ownership. exactfrac/branch.py implements ONLY SolveBranchStandard,
       alg:standard-branch, in this unit. Its guarantee is Infeasible or the transformed
       minimum rho_j=min_{U in D_j} c_j(U)/h_j(U), together with an original optimizing
       shore. Source obligations are eq:fj, eq:rhoj, prop:standard-correct,
       lem:standard-bits, thm:WYZ, and cor:standard-strong. The last two are the frozen
       source's standard-loop operation-count invocation, not a new empirical theorem.
       Sections 4.5, 4.5A, 4.6, and 4.9 remain unchanged. The returned signed root is
       NOT the original endpoint density, a global optimum, an ExactValue, or a compact
       witness. No reciprocal/sign transform, H2 scan, unit witness, reconstruction,
       certificate, or Accelerated implementation is authorized here. branch.py is the
       previously listed module owner; Unit 14 may later extend its surface by authority.

    2. Exact public interface. The sorted __all__ in this unit is exactly
         ("BranchResult", "StandardBranchStats", "solve_branch_standard").
       Ordinary positional-or-keyword signatures, with no defaults or mode switches:
         BranchResult(root: RawPair, shore: int) -> None
         StandardBranchStats(oracle_calls: int, outer_iterations: int,
             newton_updates: int, oracle_stats: BranchOracleStats) -> None
         solve_branch_standard(context: BranchOracleContext, branch: int)
             -> tuple[BranchResult | None, StandardBranchStats].
       Both new records are frozen, slotted dataclasses with structural equality/hash,
       no generated ordering, and exactly the fields above in declaration order. No
       Instance-only overload, user seed/parameter, iteration cap, tolerance, alternate
       oracle/backend, trace callback, or public residual evaluator is introduced.
       Package __init__ remains export-free. These Python names/records are engineering
       choices; the mathematical source specifies root-and-shore semantics, not Python.

    3. Result validation and meaning. BranchResult first calls closed validate_pair(root),
       then requires type(shore) is int and shore>0. Preserve root verbatim, including a
       negative/zero numerator, an unreduced denominator, and structural pair identity.
       Reject bool, numeric/tuple subclasses, Fraction, ExactValue, and coercion. A record
       without an instance cannot check its upper shore bound, domain membership, or
       optimality. A normally RETURNED record guarantees an original shore in D_j and
       root[0]*h_j(shore)==root[1]*c_j(shore). Constructor acceptance alone certifies
       neither attainment nor a minimum. Infeasible is represented by the first tuple
       component None, never a fake BranchResult, zero root, empty shore, or global Empty.

    4. Statistics validation and scope. StandardBranchStats checks its first three
       fields, in order, as exact built-in nonnegative ints; then requires
       type(oracle_stats) is BranchOracleStats. Retain that immutable nested record, not
       a mutable dictionary or a duplicate set of flow counters. Standalone constructor
       values do not assert observed work or enforce inter-field equations. No clocks,
       environment metadata, final branch label, reflected points, or complete integer-
       peak claim occurs here. Full AlgorithmStats/RunMetadata integration of section 8
       stays deferred to Unit 16; this unit's local aggregate is not its replacement.

    5. Public validation and prepared-context reuse. solve_branch_standard first requires
       type(context) is BranchOracleContext, then type(branch) is int with branch in
       (0,1,2,3), before querying or inspecting graph/domain information. Malformed public
       input through supported signatures raises exact built-in ValueError; wrong arity
       and frozen mutation retain Python behavior. Normally constructed closed immutable
       records are trusted after exact type checks; constructor-bypassing forgeries are
       outside scope. The caller supplies the prepared context. Do not construct another
       context, enumerate/filter/deduplicate families, call is_nonempty, or inspect a
       family list to bypass the seed query. The same context supports repeated solves
       and all four branches; every parameter, incumbent, and aggregate is call-local.

    6. Sole optimizer and checked response boundary. Every optimization call is to the
       closed exact_branch_min(context,branch,parameter), with precisely the submitted
       context and branch. On a normal return require an exact tuple of length two,
       whose components are BranchOracleResult or None, and exact BranchOracleStats.
       An explicit response-shape/type violation is RuntimeError. For a non-None result,
       require its positive original shore to fit the instance's n-bit universe; a shore
       outside that universe is RuntimeError. The closed result constructor supplies
       exact signed c/residual and positive h. Recompute check_raw using the closed
       residual_numerator(parameter,result.c,result.h) and require
       check_raw==result.residual, otherwise RuntimeError. This verifies the parameter-
       binding seam; it is NOT a second optimization or independent optimality proof.
       Source-domain membership and original c/h formulas remain the closed Unit 12
       guarantee. Do not import its private _source_terms or duplicate its four formulas,
       sign-routing coefficients, family traversal, shifts, cuts, or original shore sums.
       Do not catch/translate arbitrary dependency exceptions. An exception raised by a
       closed query or scalar helper propagates unchanged; do not return partial success.

    7. Mandatory zero-parameter seed. After public validation, query exactly once at the
       literal RawPair (0,1). Check its response as above and include its diagnostics.
       If its result is None, return (None,stats) immediately: oracle_calls=1,
       outer_iterations=0, newton_updates=0, with the returned seed oracle_stats included.
       This is source branch infeasibility, not a global empty-family decision. A zero,
       positive, or negative seed residual is allowed for a feasible branch. In particular,
       a zero seed residual does NOT terminate a feasible Standard solve. No Q==1 shortcut,
       all-zero placeholder, or pre-scan of descriptors replaces this seed invocation.

    8. Literal Standard initialization. For a non-None seed result (c0,h0), construct
       seed_pair=make_pair(c0,h0), then parameter=pair_add_one(seed_pair). The initial
       query parameter K is therefore EXACTLY (c0+h0,h0), not (c0,h0), (1,1), a reduced
       equivalent, a rounded bound, or a shared Accelerated initialization. Since h0>0,
       K>c0/h0>=rho_j and F_j(K)<0. No K or denominator is chosen by magnitude search.
       The zero-parameter seed is not counted as an outer-loop iteration or a Newton
       update. Arithmetic at initialization does not create a user-adjustable seed API.

    9. Loop, internal signs, and exact termination. Query at the current parameter,
       validate the response, and aggregate that invocation's diagnostics. After the
       feasible seed, None from any later query is RuntimeError, never a normal empty
       result. The first loop query, at K, must have strictly negative raw residual;
       a nonnegative value there contradicts the initialization guarantee and is
       RuntimeError. At subsequent loop queries a positive raw residual is RuntimeError.
       Such checks use mathematical/initialization state, never diagnostic counters.
       For a zero raw residual at a subsequent query, return
         (BranchResult(parameter, result.shore), stats).
       Test integer equality with zero exactly; no tolerance, sign-of-c shortcut,
       residual decrease threshold, tuple equality to (0,1), or visited-shore test.
       Since submitted B>0, raw==0 iff F_j(A/B)==0. The terminal shore is the current
       oracle shore, not the seed or the preceding update's shore.

    10. Negative-residual update and literal return pair. For every negative loop residual,
        construct next_parameter=make_pair(result.c,result.h). Require
        compare_pairs(next_parameter,parameter)<0, otherwise RuntimeError, then replace
        parameter by that fresh pair. Increment the Newton-update diagnostic once. Never
        form parameter + raw/(B*h), multiply through an old denominator, retain the old
        parameter's scale, normalize, or reflect the point. The source invariant gives
        rho_j<=c/h<parameter numerically. Every loop has one oracle invocation, with no
        extra query at the new point until the next loop iteration. At exact-zero return,
        KEEP the submitted parameter pair even when it differs structurally from the
        current result's (c,h): different optimizing shores can have different raw pairs
        for the same root. Do not overwrite the parameter after detecting zero. A4's
        legal alternative oracle choices may change raw root representation, shore,
        and trajectory, but must preserve the numerical optimum. No new tie objective.

    11. Exact diagnostic accounting. oracle_calls counts all normally returned optimizer
        invocations, including the seed, the K query, and the terminal zero query.
        outer_iterations counts loop invocations at K and later parameters, including
        the terminal one; it excludes the zero seed. newton_updates counts only negative-
        residual assignments to a fresh (c,h), excluding initialization. Aggregate the
        first six fields of each returned BranchOracleStats by exact addition and its
        flow_peak_generated_value by maximum, with initial maximum zero. Include the
        seed and terminal diagnostics exactly once, even when they describe no flow.
        For a successful feasible solve with u=newton_updates, u>=1 and
          outer_iterations=u+1, oracle_calls=u+2.
        For a successful infeasible solve the counts are (1,0,0). Context preparation is
        never included again. Aggregates remain separate from the returned mathematical
        record and cannot affect termination, updates, choice, validation, or feasibility.
        A legal change in diagnostics alone must leave root/shore and query parameters
        unchanged. No result/stats tuple is returned after an internal or backend failure.

    12. Dependency/exactness boundary. Permitted direct imports: optional future
        annotations; dataclasses.dataclass; BranchOracleContext, BranchOracleResult,
        BranchOracleStats, exact_branch_min from oracle; RawPair, validate_pair, make_pair,
        pair_add_one, compare_pairs, residual_numerator from rational. Nothing else is
        required or authorized in the production module. Closed dependencies may import
        their own permitted layers transitively; observing flow in sys.modules is not
        evidence of a prohibited DIRECT flow import here. No direct flow, parity_cut,
        sign_routing, families, witness, instance, verifier, test, private-data, solve,
        certificate, external optimizer, filesystem, randomness, or reflection imports.
        No float literal/conversion, Fraction, true/floor division, remainder/gcd reduction,
        tolerance, big-M, scalarized objective, set construction/iteration, recursion,
        exhaustive shore enumeration, multiplicity expansion, or user iteration budget.
        The loop is controlled by exact residuals, not q,f,Q, bit length, or a numerical
        asymptotic cutoff. No unbounded trace/cache/visited collection is retained.

    13. Correctness and work carrier. On a nonempty finite source domain with h>0, let
        rho=min c/h. F(lambda) is negative above rho and zero exactly at rho. The K
        initialization is strictly above rho; each nonterminal update is a candidate
        ratio at least rho and strictly below its predecessor. The finite candidate
        ratio set proves termination without an external iteration bound; exact zero
        proves the returned shore attains rho. No mathematical max-h tie rule is needed.
        Under the source invocation thm:WYZ, t=oracle_calls is O(M^2 log M), M=n+m+1,
        including the constant seed/init overhead. With r_j=len(context.families[j]),
        Unit 12's uniform per-query carrier yields total solve work
          O(t*(1+r_j*(n+3)^3*(m+n)^2)).
        This counts empty descriptors and totalizes r_j=0. Separate context preparation
        remains O(n+m+R_all) once, as section 4.9.16 rules. Wrapper arithmetic/diagnostic
        work is O(1) per call in the same integer-operation model. Extra retained solver
        state is O(1) integer records beyond the context and the oracle's O(n+m) workspace.
        No support-dimensional bound is replaced by the exponentially large domain size,
        a Q-driven descent count, or an empirical iteration limit.

    14. Number sizes, not a production cutoff. Use Q=sum(q_e), C=3Q+2, H=2Q+1 from
        section 4.9.17. Seed (0,1) and every actual Standard parameter (A,B) satisfy
          abs(A)<=C+H=5Q+3, 1<=B<=H;
        after a Newton assignment the stronger abs(A)<=C holds. Accordingly the raw
        residual magnitude is at most B*C+abs(A)*H <= H*(2C+H), and the exact comparison
        products have the same polynomial-size carrier. Every update resets to original
        source terms; no denominator product accumulates across iterations. Unit 12 and
        the closed zero-safe flow carrier bound the query's remaining integers. Masks
        use O(n) bits; counter aggregation adds only structural logarithmic factors under
        the source iteration bound. These give the lem:standard-bits proof-to-code bridge,
        not a complete measurement of every generated integer and not a wall-time bound.
        Test-local bounds may be checked on specified families. Do not add asymptotic
        production assertions or claim general flat observed counters as magnitudes vary.

    15. Evidence and conformance. Before tests or code, commit independently derived
        fixtures for all four source domains, infeasible/zero/signed roots, complete
        query trajectories including seed/K/terminal, unreduced resets, root-pair ties,
        legal argmin alternatives, exact diagnostic sums/maxima, and failure boundaries.
        The reference route evaluates original instance shores and literal source forms;
        never seed expected optima or traces from the future branch implementation.
        After tests-first GREEN and a separate definition-level implementation audit,
        add narrowly scoped CONFORMANCE coverage for prop:standard-correct and
        lem:standard-bits and document cor:standard-strong's source-dependent operation
        chain. Finite tests do not prove WYZ or universal strong polynomiality. The
        Accelerated prop:branch-invariant, prop:branch-correct, thm:accelerated-bound,
        lem:bitgrowth and all global/certificate obligations remain unpromoted. Preserve
        every prior CONFORMANCE row/status. Follow the appended Unit 13 completion gate.

4.11 Production Accelerated branch solver
    (RULED — Unit 14 authority R1; effective on controlled authority commit)
    1. Source, priority, and scope. Implement alg:branch on the same fixed original
       D_j, c_j, h_j and exact oracle as section 4.10. The mathematical obligations are
       eq:fj, eq:rhoj, eq:value-supergradient, prop:branch-invariant,
       prop:branch-correct, thm:DKNV, thm:accelerated-bound, and lem:bitgrowth in the
       pinned V2.2 source. The exact Python surface and counters below are engineering
       rulings, not additional claims in those theorems. The September 10, 2026 author
       ruling makes Unit 14 required core work immediately after Unit 13 and before
       Unit 15 for the MPC computational study. It supersedes the old permission in
       section 1 to defer Accelerated; the campaign itself is not implemented here.
       This unit extends the previously listed owner exactfrac/branch.py. No global
       solve, endpoint transformation, H2/unit reconstruction, certificate, CLI, or
       complete telemetry is added. Standard remains a frozen independent algorithm.

    2. Exact expanded public surface. After implementation, the sorted __all__ is
         ("AcceleratedBranchStats", "BranchResult", "StandardBranchStats",
          "solve_branch_accelerated", "solve_branch_standard").
       Add the positional-or-keyword signatures, without defaults or mode switches:
         AcceleratedBranchStats(oracle_calls: int, outer_iterations: int,
             newton_queries: int, lookahead_queries: int, lookahead_accepted: int,
             lookahead_rejected: int, early_returns: int,
             oracle_stats: BranchOracleStats) -> None
         solve_branch_accelerated(context: BranchOracleContext, branch: int)
             -> tuple[BranchResult | None, AcceleratedBranchStats].
       Reuse exactly the closed BranchResult. Its signed, zero, unreduced root and
       original positive shore semantics in section 4.10.3 are unchanged. None denotes
       branch infeasibility, not zero root or global Empty. No user seed, callback,
       injected optimizer, iteration limit, normalization, or automatic Standard
       fallback is accepted. Package __init__ remains export-free.

    3. New statistics record. AcceleratedBranchStats is frozen, slotted, structurally
       equal/hashable, with no generated ordering and exactly the eight fields in
       item 2, in that order. Check the first seven as exact built-in nonnegative ints
       in declaration order; then require type(oracle_stats) is BranchOracleStats.
       Reject bool, subclasses, coercible/duck-typed values and malformed supported
       data with exact ValueError. Constructors do not enforce successful-run equations
       or certify that any computation occurred. No trace, mutable cache, Instance,
       branch label, timer, or complete peak_integer_bits field is stored. Unit 16
       remains responsible for the common full AlgorithmStats/RunMetadata interface;
       these local records do not silently enlarge or change StandardBranchStats.

    4. Public validation and checked oracle seam. First require type(context) is
       BranchOracleContext, then exact built-in int branch in (0,1,2,3), before graph
       access or any query. Wrong supported data raises exact ValueError; ordinary
       Python arity and frozen-mutation behavior remain unchanged. Reuse the closed
       _checked_query(context,branch,parameter) and _add_diagnostics without editing
       their definitions. Thus every query checks exact tuple/result/stat types,
       original shore universe, and residual_numerator(parameter,c,h)==result.residual;
       explicit returned-data inconsistencies are RuntimeError. A normally constructed
       BranchOracleResult already guarantees its field types and positive h. Do not
       duplicate original-domain formulas or test a minimum a second time. The sole
       optimizer is the closed exact_branch_min; arbitrary dependency exceptions
       propagate unchanged. No catch-all conversion to infeasibility or partial result.

    5. Mandatory seed and fresh initialization. Query literal (0,1) once and aggregate
       its diagnostics. If the checked result is None, return (None,stats) with
       oracle_calls=1 and all other counters zero. Otherwise construct the initial
       parameter with make_pair(seed.c,seed.h), exactly (c0,h0), WITHOUT pair_add_one.
       Query this parameter even if the seed residual was zero. Any seed residual
       sign is legal; it is not subject to a continuing-state sign test. No context
       construction, descriptor inspection, Q==1 shortcut, or reuse of the seed reply
       as the initialization reply may bypass either required call. After a feasible
       seed every later None is RuntimeError, including at a reflected point: the
       fixed nonempty branch domain cannot become empty when its parameter changes.

    6. Initialization query. Its checked minimum residual must be <=0; a positive
       value is RuntimeError. If zero, immediately return the SUBMITTED initial pair
       and that initialization query's current shore, not the seed shore or its pair.
       For a negative residual retain parameter and its checked result together as
       the current state. The seed and initialization queries are excluded from
       outer_iterations and newton_queries. Even at a numerical zero initial pair,
       do not normalize its denominator or replace the successful result with None.

    7. Newton query from the current negative state. On each execution of the source
       while body, form newton=make_pair(current_result.c,current_result.h) once.
       Require compare_pairs(newton,current)<0 before the query, else RuntimeError.
       Query newton and retain its parameter, minimizing shore, source terms, residual,
       and diagnostics as one already-queried candidate. A positive Newton residual
       is RuntimeError, because the fresh feasible ratio is at least rho_j. A zero
       residual returns BranchResult(newton,newton_result.shore) immediately, before
       calling pair_reflect or performing any reflected query. No division, old-scale
       B*c/(B*h) expression, or re-encoding substitutes for the literal fresh pair.

    8. Reflected query and argument order. Only if the Newton minimum is negative,
       call closed pair_reflect(newton,current), with those roles in that order.
       For newton=(A,B), current=(C,D), this preserves (2*A*D-C*B,B*D) exactly.
       Do not reimplement this arithmetic in branch.py, reduce it, cancel common
       factors, reverse operands, clip a negative value, or shortcut equal denominators.
       Require compare_pairs(reflected,newton)<0 before the query, else RuntimeError;
       combined with item 7 this gives reflected<newton<current. Query reflected once.
       A positive, zero, or negative reflected minimum is a normal mathematical outcome
       AFTER the common response/binding checks, not a reason to repair the parameter.
       A zero residual returns BranchResult(reflected,reflected_result.shore) immediately.

    9. Acceptance, rejection, and exact state transfer. A strictly negative reflected
       residual accepts its queried pair and result as the next current state. A
       strictly positive reflected residual rejects only the look-ahead: retain the
       ALREADY-QUERIED Newton pair and Newton result, whose residual is negative.
       Never retain the rejected shore/raw result, replace the Newton pair by the
       Newton result's own (c,h), or query Newton again on rejection. Keep the parameter
       and its matching oracle result together. Before continuing require
       compare_pairs(next_parameter,current)<0, else RuntimeError; then replace the
       entire current state. Every accepted current state has negative residual.
       Do not apply Standard's blanket no-positive-query rule to reflection.

    10. Terminal binding and arbitrary legal ties. Every successful return keeps the
        exact parameter submitted at the zero query and the shore returned by THAT
        query. Initial, Newton, and reflected termination all obey this rule, even
        when the terminal result's fresh (c,h) differs structurally. Test raw identity
        separately from numerical root equality. The source allows any exact residual
        argmin. Shipped selection remains section 4.6; the wrapper adds no max-h,
        minimum-mask/cardinality, bit-size, or diagnostic secondary objective. Legal
        choices can change queried pairs, attaining shores, and counts without changing
        the numerical root. The closed least-ORDINARY-cut requirement is not relaxed.

    11. Exact local accounting. oracle_calls counts every normally returned optimizer
        invocation, including seed, initialization, all Newton queries, and all
        reflected queries (accepted, rejected, or terminal). outer_iterations counts
        entered negative-state while bodies, including a body that terminates early;
        newton_queries counts their Newton queries, not initialization. lookahead_queries
        counts actual reflected queries; lookahead_accepted counts only strictly negative
        reflected results used for continuation; lookahead_rejected counts only strictly
        positive reflected results that cause Newton retention. A zero reflected result
        is neither accepted nor rejected. early_returns counts the source's explicit
        zero-Newton or zero-reflection returns: one on such a completed run and zero
        on infeasibility or an initialization-root return. Aggregate all six additive
        BranchOracleStats fields and max(flow_peak_generated_value), including discarded
        reflected-query work. No diagnostic determines validation, signs, selection,
        iteration, or an early return. No completed stats tuple is returned after failure.

    12. Successful-run accounting identities (not constructor assertions). Infeasible:
        (oracle_calls,outer_iterations,newton_queries,lookahead_queries,
         lookahead_accepted,lookahead_rejected,early_returns)=(1,0,0,0,0,0,0).
        Initialization root: (2,0,0,0,0,0,0). Otherwise let p=outer_iterations,
        l=lookahead_queries, a=lookahead_accepted, r=lookahead_rejected. Then
          p=newton_queries>=1, oracle_calls=2+p+l, early_returns=1.
        Newton-terminal run: l=p-1 and a+r=l. Reflection-terminal run: l=p and
        a+r=l-1. Equivalently a+r=p-1 for either terminal kind. A positive reflected
        rejection still contributes one oracle call and its full diagnostics. These
        source-order counts are not extra mathematical constraints on valid standalone
        records. Context preparation remains once-paid outside each branch solve.

    13. Dependency and control restrictions. Extend the closed module's direct rational
        import whitelist by pair_reflect only. Keep all other section 4.10.12 imports
        and bans: no direct flow/parity/family/witness/instance/verifier access, external
        optimizer, filesystem/I/O, floating point, Fraction, division/remainder/gcd,
        tolerance, sets, recursive solver, magnitude search or arbitrary iteration cap.
        pair_add_one remains Standard-only; pair_reflect is Accelerated-only. Production
        retains O(1) outer records, not a full trace or a visited collection. The only
        graph access owned by the common query seam is its existing universe check.
        Families are neither rebuilt nor scanned by the outer algorithm. Mathematical
        control depends on query residuals and exact pair comparisons, never counters.

    14. Frozen Standard compatibility boundary. The future implementation may change
        branch.py's module description, __all__, and the addition of pair_reflect to
        its rational imports, and append AcceleratedBranchStats and
        solve_branch_accelerated. Preserve the EXACT source text, signatures, annotations,
        defaults, and behavior of BranchResult, StandardBranchStats, _checked_query,
        _add_diagnostics, and solve_branch_standard from ee4a9b0; no refactoring or
        common algorithm dispatch is authorized. All earlier production modules stay
        byte-identical. The future tests-only compatibility amendment may alter ONLY
        the two exact module-surface assertions in tests/test_branch.py (the main
        surface test and its fresh-process script), their explicitly named surface
        constants if used, and _source_violations' import/reflection permission logic.
        All 31 test names, literal tables, reference calculators, behavioral assertions,
        and the 20 prohibited-source controls are otherwise frozen. No prior test is
        removed, skipped, xfailed, renamed, or made insensitive to Standard regressions.

    15. Compatibility is constrained, not a blanket guard waiver. During tests-first
        RED the existing module still has exactly the legacy three-name surface; after
        GREEN it has exactly item 2's five-name surface. The two old surface checks may
        accept these TWO explicit complete tuples, never an arbitrary superset or a
        partial extension. The new Unit 14 test requires the five-name tuple exactly.
        The shared source guard may permit the pair_reflect import, but its invocation
        is allowed only inside solve_branch_accelerated, never in a Standard-reachable
        function or a generic helper. All other source restrictions remain enforced,
        and a negative control placing reflection in a Standard-reachable function must
        fail. New Unit 14 tests verify the six preserved definitions byte-for-byte and
        exercise the full combined module. Freeze and separately audit the precise
        compatibility diff before production; the authority package itself edits no test.

    16. Source correctness bridge. For rho=min c/h, F is zero only at rho, negative
        above it, and positive below. Initialization delta=c0/h0 is at least rho.
        At negative current residual, rho<=hat_delta<delta. If its query is nonzero,
        delta'=2*hat_delta-delta<hat_delta: a negative reflected minimum proves
        delta'>rho; a positive one proves delta'<rho<=hat_delta and hence requires
        Newton retention. The retained pair/result satisfies the source invariant.
        Concavity makes the selected supergradient -h nondecreasing under decreasing
        parameters; at successive nonterminal retained states it strictly increases,
        by prop:branch-correct's equal-active-slope argument. Finitely many slopes give
        finite termination for any exact argmins. This argument is not the polynomial
        iteration count. That count uses the separate frozen thm:DKNV invocation.
        Strict h descent may be checked test-locally; it is not a secondary selector.

    17. Work carrier and prepared-context separation. With M=n+m+1 and p entered loop
        bodies, t=oracle_calls<=2+2*p on feasible branches. Under thm:accelerated-bound,
        p and t are O(M log M); no numerical O-constant becomes a production limit.
        Unit 12 gives O(t*(1+r_j*(n+3)^3*(m+n)^2)) integer/comparison operations,
        including zero-descriptor and all-empty cases. Once-paid preparation remains
        O(n+m+R_all), not hidden in a branch-0 query. The outer wrapper contributes
        O(1) operations/records per query beyond the oracle's O(n+m) workspace and
        the stored context. Bit-operation time and byte memory are not constant.
        No universal claim that Accelerated uses fewer calls than Standard on every
        instance follows; the two exact algorithms are compared experimentally later.

    18. Bit recurrence as source review and test-local evidence only. Use C=3Q+2,
        H=2Q+1 from section 4.9.17. A fresh (c,h) has abs(c)<=C and 1<=h<=H.
        If P=max(abs(current.A),current.B), reflection with a fresh Newton operand
        has abs(A_new)<=2*C*P+H*P and B_new<=H*P. Thus P_new<=(2*C+H)*P;
        rejection resets the stored point to a fresh source pair, not this product.
        Since C>=H, after s consecutive reflections since a fresh stored point,
        every attempted point, including a rejected/terminal one, has
          max(abs(A),B)<=C*(2*C+H)^s.
        Length therefore increases additively by O(log(C+H)) per reflection, not by
        squaring two growing operands. At every query abs(raw)<=B*C+abs(A)*H;
        comparison products and reflection temporaries have the corresponding
        product/sum length bounds. Combine with section 4.9.17's capacities, signed
        recovery and zero-safe flow bounds. With the source O(M log M) iteration
        invocation this supplies lem:bitgrowth's polynomial encoding argument.
        Large-integer tests may check these derived inequalities and raw preservation;
        production may not enforce them as cutoffs or instrument them as complete
        telemetry. Flow-only peak is not full peak_integer_bits. General magnitude
        changes need not leave observed counters flat; use proved invariant families.

    19. Corpus-wide agreement and Unit 15 handoff. Unit 14 must execute both solvers
        on ALL 1,316 core branch solves (329 instances times four), including empty
        branches. Require matching None decisions; otherwise compare_pairs of their
        roots is zero, and each original shore independently belongs to D_j and attains
        that value under source-term evaluation. Also require each root equal the
        independently enumerated original-domain optimum: agreement alone could hide
        a common dependency defect. Do not require equal raw pairs, shores, counters,
        or trajectories, nor use Standard to generate Accelerated expected traces.
        Unit 15 must make Standard | Accelerated a ruled solver selection and run every
        global corpus instance with both. Require equal numerical endpoint/global
        values and independent verifier re-evaluation of EACH admissible witness to
        that value, preserving each literal witness-derived raw quotient. Different
        witnesses or raw quotient pairs may be equally valid. Verify genuine Empty
        separately. Unit 15 rules exact selection spelling/default/interface before
        its own tests; this authority does not implement solve.py or an unavailable
        certificate checker. The independent definition-level verifier remains isolated.

    20. Evidence sequence and claims. Authority changes only DESIGN and TEST_PLAN;
        commit/push that authority before Phase C fixture derivation. Catalogue complete
        independent initialization/Newton/reflection traces, all three terminal sites,
        accepted/rejected reflections, tied raw terminal pairs, diagnostic accounting,
        negative/zero/infeasible cases, rejection declarations, and large symbolic
        trajectories before tests or Accelerated code. Derive expectations without
        future production, and distinguish abstract algebra controls from graph fixtures.
        Freeze the narrow Standard-compatibility test amendment and new Accelerated
        tests; establish specific missing-symbol RED while Standard stays green. After
        GREEN, a separate source-domain audit and executed mutations precede scoped
        CONFORMANCE: preserve Standard rows and all unrelated rows; map implemented
        prop:branch-invariant, prop:branch-correct and lem:bitgrowth. Document the
        thm:accelerated-bound source-dependent chain separately, not as a finite proof
        of DKNV. Staged-tree isolation, atomic implementation commit, and separate
        approved-hash remote closure remain required. No external review-request
        artifact or external-review wait is part of these gates. Private BUILD/LEARNING
        notes are outside every gate: no existence/path/type/permission/content/hash/
        Git-ignore assertion, and no dereference of inherited note pins. Deliver the
        two complete four-backtick blocks at full closure and await the author's save
        confirmation conversationally; no machine verification of that confirmation.

4.12 Production StrongCompactMSPD global solver
    (Unit 15 authority R1 — effective only on controlled authority commit)
    1. Source and unit boundary. exactfrac/solve.py owns alg:global: the constructive
       lem:unit baseline, four transformed branches in source order, direct H2 scan,
       exact endpoint comparison, and reconstruction of the retained original compact
       witness. Read def:parameter, lem:empty, lem:unit, prop:endpoints,
       prop:branch-transform, sec:global (including its complete reconstruction table),
       prop:global-invariant, and the proof of thm:main in the SPEC_LOCK-pinned V2.2
       source. The main theorem's literal label is thm:main; no thm:B alias is present.
       The September 10 ruling permits exactly Standard | Accelerated, without changing
       the mathematical problem. The source's accelerated operation factor is not
       attributed to Standard. All prior implementation/test files remain closed.

    2. Exact public surface and selection. Module __all__ is exactly the sorted tuple
         ("SolveResult", "SolveStats", "solve").
       The positional-or-keyword signatures, with no defaults or hidden modes, are:
         SolveResult(value: ExactValue, witness: Witness | None) -> None
         SolveStats(branch_solver: str,
             branch_stats: tuple[StandardBranchStats | AcceleratedBranchStats, ...],
             attaining_candidate: str) -> None
         solve(instance: Instance, branch_solver: str) -> tuple[SolveResult, SolveStats].
       branch_solver must be an exact built-in str equal to "Standard" or "Accelerated".
       Reject aliases, alternate capitalization, whitespace, enums, str subclasses,
       callables, bools and coercion. No implicit default, automatic fallback, injected
       optimizer, user seed, budget, callback, backend or externally prepared context.
       The Python name solve implements StrongCompactMSPD; it does not rename its source
       label. The consuming test is tests/test_solve.py, not tests/test_global.py.
       Package-root exports remain unchanged.

    3. Mathematical result record. SolveResult is a frozen, slotted, hashable dataclass
       with structural equality, no generated ordering, and exactly value,witness in
       that order. Validate type(value) is ExactValue first, then witness is None or
       type(witness) is Witness. For None require literally value.N==0 and value.D==1;
       reject a rescaled zero. With a Witness, this constructor checks types only, not
       instance-dependent admissibility, attainment, optimality, or raw-formula equality.
       Normally constructed closed records are trusted; constructor-bypassing forgeries
       are outside scope. Preserve both supplied records; no normalization or duplicate
       U,y,N,D fields. Successful solve returns the exact raw witness-attaining quotient
       required by 4.4 and 4.4A, or ExactValue(0,1) with None for genuine Empty. It never
       returns bare None, a fake witness, a new Empty sentinel, or a zero-valued witness
       reclassified as Empty. There is no certificate field or placeholder object here:
       Unit 17 derives the certificate envelope from value and witness; Unit 18 implements
       independent checking. This is the pre-certificate realization of section 2 R5,
       not permission to claim that certificate serialization/checking is implemented.

    4. Separate local diagnostics. SolveStats is a frozen, slotted, hashable dataclass,
       structural equality/no ordering, fields exactly as in item 2. Validate the solver
       selection first; then an exact tuple whose entries have the exact selected closed
       stats type, StandardBranchStats or AcceleratedBranchStats; then an exact built-in
       str in ("Empty","Baseline","L0","L1","H0","H1","H2"). Keep the original immutable
       branch records without recomputing, merging, replacing, or coercing their fields.
       Construction imposes no cross-field/run-history equations. A successful nonempty
       solve returns four entries aligned to j=0,1,2,3, including infeasible branches;
       a Q==1 solve returns (). attaining_candidate records first-retained provenance,
       not a claim that its witness belongs exclusively to a branch. No counter, origin
       string, or diagnostics field controls mathematical comparison, feasibility, or
       reconstruction. Unit 16 still owns full AlgorithmStats/RunMetadata, timings,
       aggregation and complete peak-integer accounting. This local wrapper does not
       claim those capabilities or put diagnostics in SolveResult or a certificate.

    5. Public validation and Empty. solve first requires type(instance) is Instance,
       then validates branch_solver, before reading graph properties or calling any
       dependency. Accept only a normally constructed canonical active Instance; do
       not repeat normalization, active-regime validation or labels processing. Public
       malformed data/record construction through supported signatures raises exact
       built-in ValueError. Wrong arity and frozen mutation retain Python behavior.
       After validation, read Q. For Q==1, return
         (SolveResult(ExactValue(0,1),None), SolveStats(branch_solver,(),"Empty")).
       This lem:empty shortcut constructs no Witness, no BranchOracleContext, and makes
       no branch/oracle/cut calls. Both selections and selection rejection still apply.
       Q==0 is excluded by the closed canonical Instance, not a new mathematical case.

    6. One preparation and complete traversal. For Q>=2, construct exactly one closed
       BranchOracleContext(instance), retaining the same Instance object. Read d_q into
       one local tuple for wrapper vertex scans; never recompute that property per vertex.
       Construct/evaluate the baseline in item 7. Invoke only the selected closed solver
       once for each j in the literal order (0,1,2,3), passing that same context and j.
       Do not inspect context.families, skip a solver based on descriptor counts, call
       exact_branch_min directly, rebuild contexts, or bypass an infeasible branch's
       required seed. Every normal branch reply contributes its selected-type stats.
       After all four replies, execute the direct H2 scan in item 10. No early return
       based on a current density, a zero/negative transformed root, a known tie, or a
       presumed globally winning branch. The sole global shortcut is the validated Q==1
       case. Mutable working lists are local; no instance cache or cross-run state.

    7. Constructive baseline, including the matching case. Follow lem:empty to choose
       an admissible-capable shore, with these deterministic refinements of its choices:
       (a) first increasing-index vertex with even f(v); otherwise
       (b) first increasing-index vertex with odd f(v)>=3; otherwise
       (c) first increasing-index vertex with f(v)==1 and d_q(v)>=2; otherwise
       (d) all vertices have f(v)==d_q(v)==1, so the graph is a unit matching with at
           least two edges. Choose the smaller endpoint of each of the first two
           canonical support edges, and take their two-vertex shore.
       Category priority precedes vertex-index priority; do not replace it by a single
       differently ordered mixed-condition scan. Guard a violated matching promise with
       RuntimeError, not repair or arbitrary shore enumeration. These choices refine
       source freedom, not a mathematical minimum-mask preference.
       The feasibility proof's preliminary boundary selection is NOT the final baseline.
       Compute s=f(U), b=b_q(U); apply lem:unit: if s+b is odd take Y=b, otherwise Y=b-1.
       Set all crossing counts to q_e, except decrement the first crossing edge_ref by
       one in the latter case. Every noncrossing coordinate is zero. The even case must
       have b>=1 and s+b>=4; the odd case must have s+b>=3. Evaluate this Witness with
       closed witness_value, require its numerical value >=1, and retain its actual raw
       quotient and actual Witness. An explicit violated source prerequisite is an
       internal RuntimeError. Never initialize to a bare value 1, use a feasibility
       witness of value below one, discard the baseline after branch preparation, or
       assume the eventual winner must be a transformed-branch result.

    8. Checked branch reply and original-domain binding. A normal selected-solver reply
       must be an exact two-element tuple containing BranchResult or None, and the exact
       selected closed stats type. Explicit shape/type violations are RuntimeError.
       None is ordinary branch infeasibility and makes no endpoint candidate; keep its
       stats and continue. For a BranchResult require its original shore within the
       nonempty n-bit universe. Use closed shore_f, shore_b_q and shore_d_q to obtain
       s,b,d, and check its source domain before reconstruction:
         j=0: s+b odd (h=d+1-s>0, s+b>=3);
         j=1: s+b even, b>=1, d>s (h=d-s>0, s+b>=4);
         j=2: s odd, s>=3;
         j=3: s even, b>=1 (s>=2).
       Domain/universe failures are RuntimeError, never an infeasible branch. Do not
       import oracle._source_terms or another private closed helper. Domain checks and
       root/shore binding are consumer consistency checks, not a second optimization.
       Trust the closed solver's global branch-minimum promise; do not enumerate shores
       or independently recalculate a branch optimum in production.

    9. Reconstruct each feasible original endpoint and compare the right quantity.
       Work in original vertex coordinates and canonical support-edge order; dense y
       has length instance.m and noncrossing entries zero. Endpoint recipes and literal
       raw quotients (using d=2e_q(U)+b) are:
         j=0 / L0: all crossing copies; Y=b;   (N,D)=(d+b,   s+b-1).
         j=1 / L1: all except one copy from the first crossing edge; Y=b-1;
                                                    (N,D)=(d+b-2, s+b-2).
         j=2 / H0: all counts zero; Y=0;     (N,D)=(d-b,   s-1).
         j=3 / H1: one copy on the first crossing edge only; Y=1;
                                                    (N,D)=(d-b+2, s).
       Build Witness(U,y), call closed witness_value for its authoritative raw ExactValue,
       and require equality of the two literal formula fields above. The evaluator's
       normal return must have exact ExactValue type; an explicit mismatch is RuntimeError.
       Bind the returned root (A,B) NUMERICALLY to this candidate: for j=0,1 require
         N-D>0 and A*(N-D)==B*D;
       for j=2,3 require A*D==-B*N. These are respectively c/h=D/(N-D) and -N/D.
       Never require structural root equality to a fresh c/h pair: terminal root scale
       and terminal shore can legitimately differ. Never compare transformed roots
       across branches, copy a submitted root's scale into the global value, normalize
       (N,D), or treat a zero H0 endpoint as branch infeasibility.
       Reconstruct/evaluate every feasible endpoint before comparison, even if it loses.
       Invoke closed compare_pairs((candidate.N,candidate.D),(best.N,best.D)); update
       value and witness together only when it returns a positive result. Equal values
       preserve the first candidate. No secondary key based on root, h, mask, y,
       numerator/denominator, cardinality, provenance, stats or solver selection.

    10. Direct H2 is a real reconstruction path, not a fifth branch-solver call.
        After the four branches, find the first increasing-index v with f(v)==1 and
        cached d_q(v)>=2. If none, there is no H2 candidate. Otherwise U=1<<v. In
        canonical edge order select two incident copies compactly: start remaining=2,
        assign min(q_e,remaining) on each encountered crossing edge until remaining
        is zero, and zero elsewhere. This uses at most two positive coordinates, either
        a count 2 on one edge or counts 1,1 on two edges, without expanding multiplicity.
        Check that two copies were attained, build its Witness, and call witness_value
        before the same strict-improvement comparison. The literal value is (4,2),
        not (2,1); its mathematical value is two. Do not skip this scan or reconstruction
        merely because previous candidates already dominate it. The source permits any
        such vertex/copies; these are deterministic refinements only.
        For a valid H2 singleton, b=d>=2 and s=1. If b is even its L0 endpoint has value
        2; if b is odd then b>=3 and its useful L1 endpoint has value 2. Therefore, with
        correct complete branch solves and the prescribed order, H2 cannot STRICTLY
        improve the incumbent after the branch loop. This does not authorize deleting
        the source-prescribed direct scan or faking a strict-H2-winner graph fixture.
        Cover its construction and comparison as a candidate, including tie retention.

    11. Retained-result invariant and exception boundary. Initialization and every
        completed candidate preserve: a genuinely admissible BestWitness, BestValue
        literally equal to its raw objective, and numerical dominance over all candidates
        examined so far. The final SolveResult uses those retained records, including
        a retained Baseline; never reconstruct from an assumed branch index afterwards.
        SolveStats provenance is derived from the mathematical retention decision, never
        its authority. Explicit consumer-detected violations of closed promises raise
        RuntimeError. Exceptions RAISED by a dependency (context constructor, selected
        solver, shore helper, witness constructor/evaluator, or rational helper) propagate
        unchanged; no blanket translation, fallback, swallowed error or partial success.
        No returned record is itself an independently verified global-optimality certificate.

    12. Imports, exactness and compact work. Permitted direct runtime imports: optional
        future annotations; dataclasses.dataclass; Instance from instance;
        BranchOracleContext from oracle; BranchResult, StandardBranchStats,
        AcceleratedBranchStats, solve_branch_standard, solve_branch_accelerated from branch;
        compare_pairs from rational; ExactValue, Witness, shore_f, shore_b_q, shore_d_q,
        witness_value from witness. Internal helpers are private, not additional API.
        No direct families/flow/parity_cut/sign_routing imports, private closed imports,
        verifier/test/hand-off imports, certificate/CLI/telemetry implementations, file I/O,
        external optimizers, timing, randomness, Fraction/decimal/float, true/floor division,
        gcd/reduction, tolerances, scalarization, recursion, set construction/iteration,
        all-shore enumeration or copy expansion. Integer parity via &1 or %2 is allowed.
        Do not import forbidden layers merely to add another runtime validity check.
        All wrapper loops are scans over vertices/support edges, the fixed four branches,
        or bounded record fields. No loop bound depends on q,f,Q,Y,N,D or their bit lengths.

    13. Source-dependent operation and number-size carriers. Let M=n+m+1,
        K=(n+3)^3*(m+n)^2, and r_j=len(context.families[j]) for ANALYSIS ONLY. Preparation
        is O(n+m+R_all) once under 4.9; wrapper baseline, at most four branch endpoint
        reconstructions, H2 and their evaluations cost O(n+m) in total. If t_j is the
        selected solver's oracle-call count, the full carrier is
          O(n+m+R_all + sum_j t_j*(1+r_j*K)).
        The source gives t_j=O(M log M) for Accelerated and O(M^2 log M) for Standard.
        Thus the global accelerated bound agrees with thm:main; Standard has its own
        corresponding larger source-dependent factor from cor:standard-strong. Finite
        tests prove neither invocation nor universal strong polynomiality. No observed
        flat-counter assertion or numerical production cutoff follows from these bounds.
        For any admissible compact witness, e_q(U)+Y<=Q and f(U)+Y<=2Q, so
          0<=N<=2Q and 2<=D<=2Q-1.
        Raw endpoint/baseline outputs are input-sized; H2 has literal (4,2). Cross products
        for endpoint comparisons have input-polynomial bit lengths. Root-binding products
        additionally inherit the chosen branch solver's parameter-bit carrier; do not
        falsely bound an unreduced Accelerated terminal pair by the final witness's raw
        scale. Keep only a bounded number of witnesses/branch records plus O(n+m) wrapper
        workspace beyond the prepared context and closed oracle work; no full trace cache.

    14. Independent dual-route obligations and future boundary. On EVERY valid instance
        in the Unit 15 registered corpus, run solve with both exact selections. Check
        genuine Empty separately. Otherwise convert only primitive instance data and
        the returned U,y into independent brute.BruteInstance and brute.Witness records;
        require brute.witness_is_admissible and equality of brute.witness_raw_value to
        that run's literal (N,D). Then compare the two numerical quotients exactly.
        Neither equal witnesses nor equal raw pairs is required across routes under ties.
        On the tiny corpus require equality to brute.brute_force's independent optimum;
        route agreement alone is insufficient. For captured feasible branch endpoints,
        likewise check numerical cross-route agreement and independent admissibility/
        attainment of each reconstructed endpoint. Tests may instrument module-local
        dependency bindings to observe candidates; this is not a production trace API.
        Large-multiplicity fixtures use independent witness evaluation and a prior exact
        mathematical optimum proof, not exhaustive loops to Q. Keep the verifier unchanged
        and solver-blind; the unavailable certificate checker is not an added gate.

    15. Controlled lifecycle. This authority changes only DESIGN and TEST_PLAN and remains
        a proposal until its controlled authority commit; apply unstaged, review, stage,
        commit and remotely close it before Phase C oracle fixtures. Then independently
        derive/cross-check catalogue expectations before tests/test_solve.py exists.
        Establish its specific missing-module RED while exactfrac/solve.py stays absent;
        implement only that new production module under frozen authority/test, perform
        the separate implementation audit, and promote only finite tested CONFORMANCE
        scope after GREEN. Preserve every earlier row and every closed dependency.
        Full telemetry, certificate serialization/checking, CLI, experiments and release
        remain later units. External/second-model review is discretionary, never a gate;
        no REVIEW_REQUEST artifact. Private BUILD/LEARNING notes are outside every gate;
        deliver their two text blocks only at full Unit 15 remote closure and await the
        author's saved confirmation only before Unit 16. No new lifecycle gate is added.

4.13 Unit 16 — exact telemetry and observational instrumentation
    (AUTHORITY R1 PROPOSAL; adopted only by its controlled authority commit)

    1. Basis, boundary, and explicit scope decision.
       This section refines §§4.5 and 8; it does not amend SPEC_LOCK, CONTRACT,
       the V2.2 mathematics, or any prior mathematical result. Relevant source:
       def:complexities, prop:domain-decomp, lem:ek, thm:branch-oracle,
       alg:branch-min, alg:standard-branch, alg:branch, lem:standard-bits,
       lem:bitgrowth, alg:global, prop:global-invariant and thm:main.
       Source statements concern operation counts and number encodings, not
       Python telemetry interfaces. The interfaces below are new engineering
       rulings, not names or definitions purportedly present in the theorem.

       Full peak_integer_bits cannot be recovered from the closed final records.
       It requires observations of intermediate products, sums, masks, parameters,
       capacities and flows. This is NOT a new-file-only unit. Adoption of this
       authority explicitly authorizes the limited recording-only extensions in
       item 13. It does not authorize algorithm redesign or wholesale replacement.
       Prior release/closure identities remain historical truth, not rolling pins.
       The Phase B patch changes only DESIGN and TEST_PLAN; no closed Python file
       or existing test changes in Phase B. All 39 baseline files are authenticated
       against commit aafac4d25bee3992399e8591bd37335b94ce7e9c before application.

    2. Public surface and old-contract preservation.
       New public module: exactfrac/telemetry.py. New private observation primitive
       module: exactfrac/_telemetry.py. No package-root re-exports.
       Entry point, with two required positional-or-keyword arguments:

           solve_with_telemetry(instance: Instance, branch_solver: str)
               -> tuple[SolveResult, AlgorithmStats]

       Validate exact Instance and exact str selection Standard | Accelerated,
       in that order, before graph access. No default, coercion, injected callback,
       alternate solver, automatic route choice, or cached mathematical result.
       Call the existing solve(instance, branch_solver) exactly once. Return its
       exact SolveResult object and retain its exact native SolveStats object.
       Legacy solve and branch public signatures, __all__ sequences, dataclass
       fields, argument-validation order, result/raw-pair meanings, diagnostic
       counters, exception behavior, minimizers, and tie order remain unchanged.
       Legacy solve stays callable without requesting complete measurements.
       No production monkeypatching, int subclass/proxy, tracing, stack inspection,
       dynamic compilation, source rewriting, or cloned mathematical implementation.

    3. Immutable record layout; no implicit adoption by construction.
       All new public records are frozen, slots dataclasses; fields are required
       positional-or-keyword arguments in the order below, with no hidden defaults.
       Exact built-in types are required; bool is not an int. Invalid public data
       raises exact ValueError without coercion or repair. Construction checks
       record shape, local bounds and declared identities, not a historical run.

       WorkStats fields (all exact nonnegative ints), in order:
           outer_iterations, oracle_calls, newton_updates, newton_queries,
           newton_candidates, lookahead_queries, lookahead_accepted,
           lookahead_rejected, lookahead_terminal, newton_terminal,
           initialization_returns, early_returns, atomic_families_enumerated,
           atomic_families_examined, atomic_families_feasible, parity_cut_calls,
           ordinary_min_cut_calls, max_flow_calls, augmentations, bfs_scans,
           flow_peak_generated_value, flow_peak_bits, peak_numerator_bits,
           peak_denominator_bits, peak_integer_bits.
       BranchTelemetry fields:
           branch: int, feasible: bool, work: WorkStats.
       AlgorithmStats fields:
           native: SolveStats, total: WorkStats, nonbranch: WorkStats,
           branches: tuple[BranchTelemetry, ...],
           output_numerator_bits: int, output_denominator_bits: int.
       AlgorithmStats.branch_solver and AlgorithmStats.attaining_branch are read-only
       properties of native.branch_solver and native.attaining_candidate, not second
       independently stored selection/provenance values. The latter property retains
       the labels Empty, Baseline, L0, L1, H0, H1, H2; it never assumes a branch winner.
       BranchTelemetry.branch is exactly 0,1,2,3; feasible is an exact bool.
       AlgorithmStats.native is exact SolveStats; the constituent work/branch records
       are exact declared types; branches is an exact tuple, not a mutable sequence.
       Output bit lengths are exact positive ints, including for the Empty pair (0,1).
       Nonempty-run branches contains four records in order 0,1,2,3 and native has
       four selected-type branch records. Empty has native.attaining_candidate Empty,
       native.branch_stats (), and branches (); absent execution is not four fake runs.
       Record validators must reject mismatched lengths, order, aggregation, and native
       counter mappings. They do not certify that supplied diagnostics were executed.

    4. Common fields do not erase native event definitions.
       Copy the existing returned event counters, never rerun the oracle to count work.
       For Standard, newton_updates is native.newton_updates; newton_queries is zero.
       For Accelerated, newton_queries is native.newton_queries; newton_updates is zero.
       newton_candidates counts formation of the fresh c/h Newton point in a negative-
       residual loop body, excluding the seed, K, initialization, and reflection. It
       equals Standard.newton_updates or Accelerated.newton_queries. This is the common
       event; the native fields are deliberately not renamed to imply identical updates.
       outer_iterations and oracle_calls keep their solver-specific native conventions.
       oracle_calls includes seed, initialization, terminal, and rejected look-ahead calls.
       A Standard feasible branch has calls=1+outer_iterations and
       outer_iterations=newton_updates+1. Standard infeasible has calls=1, all three
       iteration/Newton fields zero. Standard look-ahead/early-return fields are zero.
       Accelerated infeasible has calls=1 and all outer/Newton/look-ahead/return counts
       zero. A feasible Accelerated branch has calls=2+newton_queries+lookahead_queries
       and outer_iterations=newton_queries. Let L=lookahead_queries-accepted-rejected.
       Then L=lookahead_terminal in {0,1}; newton_terminal=early_returns-L in {0,1}.
       early_returns is the sum of these two terminal counts, not initialization returns.
       initialization_returns=1 exactly for a feasible Accelerated branch with zero
       outer_iterations; otherwise zero. Successful nonempty Accelerated branch returns
       once: initialization_returns+early_returns=1. These are recording checks only.
       No event may be inferred from a small-corpus assumption that look-ahead is absent.

    5. Preparation, per-query work, and flow accounting.
       atomic_families_enumerated counts each descriptor actually emitted by the one
       preparation, including empty descriptors and duplicates prescribed by enumeration.
       Attribute the prepared cardinality r_j to branch j once, even if j is infeasible.
       Record it from the existing prepared cover, with no second enumeration and no
       graph-derived formula substituted for observation. Context creation remains once.
       atomic_families_examined is native.oracle_stats.atomic_families_examined, accumulated
       over every query; feasible is its existing nonempty-descriptor visit counter.
       parity_cut_calls and ordinary_min_cut_calls are copied from that same native
       aggregate; max_flow_calls retains the present backend equality to ordinary cuts.
       augmentations and bfs_scans map to flow_augmentations and flow_bfs_scans.
       flow_peak_generated_value is the native flow-only peak; never sum it across calls.
       Nonbranch event counters are zero: prepare cardinalities are attributed once to
       their branch rows. Nonbranch retains preprocessing/baseline/H2/output bit peaks.
       Totals add all event counts and preparation cardinalities, but take maxima of
       flow_peak_generated_value and all bit peaks across nonbranch and all branch rows.
       output_*_bits measure only the final returned raw pair, not a maximum over queries.
       Unit 16 exposes all four branch records, never only the winning branch's work.
       Identity checks in tests: examined_j=calls_j*r_j, feasible_j=calls_j*k_j, and
       parity_j=feasible_j, where k_j is the number of nonempty prepared descriptors.
       Those identities follow the current complete cover; they do not replace counters.
       For each query, ordinary calls sum N_F^2-3N_F+3 over the feasible reduced problems.
       For a whole run sum over queries as well. N_F is the reduced problem's actual
       node count, not automatically n+3. The theorem supplies bounds, not exact counts.

    6. Observation interval and complete integer-peak semantics.
       Measurement begins after the wrapper's public validation and before the sole
       legacy solve call. It includes input mathematical integers consumed by this call,
       Q and degree preparation, baseline, every branch/query/cut/flow, all reconstructed
       candidates, comparisons/root binding and final output. Already-completed Instance
       construction/normalization is outside this interval; labels and metadata are not
       mathematical integers to include merely because a label happens to be an int.
       bits(x)=max(1,abs(x).bit_length()). An empty observation set has peak zero; this is
       different from observing the integer zero, which contributes one bit.
       flow_peak_bits=0 if no ordinary flow call occurred, otherwise bits(flow_peak_generated_value).
       Empty still observes Q and output (0,1); its output numerator/denominator bits are one.

       peak_integer_bits is the EXACT maximum over the following observation set, not
       an upper bound or a subset advertised as complete: consumed q,f,n,m and vertex
       indices; generated degree/shore/selected-copy totals and their scalar subexpressions;
       all numerator/denominator/parameter and c,h/residual terms; coefficient, support
       capacity, spoke, shift and recovery intermediates; contraction/parallel sums;
       normalized flow capacities, bottlenecks, residual updates and total flow; all
       exact comparison/root-binding products; finite-universe masks, anchors, lifted
       coordinates and algorithmic indexing/epoch arithmetic on the measured call path.
       Exclude diagnostic-only counting/aggregation, recorder bookkeeping, Python object
       IDs/runtime internals, wall-clock/metadata/hash/serialization computations, and
       arithmetic in the independent verifier/tests. This is not a CPython memory profiler.
       Include ephemeral products BEFORE cancellation: B*c and A*h as well as their
       difference; all factors/products of 2*A*D-C*B and B*D; root-binding products and
       products from losing/tied global comparisons. Unselected candidate arithmetic and
       rejected look-ahead work still belongs to the run.
       peak_numerator_bits and peak_denominator_bits cover all actual raw rational pairs
       formed or consumed in the measured path (seed/K/Newton/reflection/branch return,
       existing exact comparison operands, residual numerator over submitted B, original
       endpoint pairs and output). A pair need not be reduced or ultimately retained.
       Do not manufacture extra arithmetic solely to enlarge or certify a peak.
       A site may omit individual monotone nonnegative sum prefixes only with an explicit
       dominance proof: the observed final sum is itself an executed value and dominates
       every omitted prefix. Cancellation sums/products may not use that shortcut.

    7. Instrumentation primitive, erasure and noninterference.
       _telemetry.py is a standard-library-only leaf: no imports of any other exactfrac
       layer, verifier, tests, I/O, randomness, or clock. It holds a context-local active
       recorder. Start a fresh recorder for each measured call and restore the previous
       context in finally, including failure. Never install mutable state on an Instance,
       BranchOracleContext, result, witness, or native statistics object.
       A private integer tap returns its original argument object unchanged; a raw-pair
       tap returns its original tuple unchanged. With recording disabled they are identity
       operations. With recording enabled they additionally update peaks, never the value.
       Taps may surround already-validated scalar expressions to expose intermediate
       values without changing Python evaluation order or evaluating an operand twice.
       Statement-only observation events and scope boundaries may return no information
       used by mathematical code. The only recorder reads inside the leaf control whether
       and where to record and whether to update a diagnostic maximum.
       No mathematical condition, parameter, loop bound, result, exception translation,
       minimizer, graph ordering, or tie choice reads a recorded field. No user callbacks.
       Branch scopes include their branch computation and original endpoint comparison;
       preparation outside the branches, baseline and H2 go to nonbranch. Preparation
       counts are distributed to their matching branch IDs without reexecuting preparation.
       Nested measured solves in the same execution context reject before invoking solve;
       independent threads have disjoint recorders. The synchronous wrapper does not spawn
       tasks/threads or suspend into arbitrary user code. Repeated and failed runs leak no
       observations. No complete AlgorithmStats is returned for a failed solve; original
       dependency exceptions propagate as the same exception object. Collector corruption
       or normally returned inconsistent records raise RuntimeError, not partial success.

       The permitted source transformation must admit a deterministic syntax-only
       erasure: remove only named observation imports/events/scope wrappers and replace
       identity taps by their original argument expressions. Original arithmetic ASTs,
       public definitions, validations and control-flow order must then match the closed
       source ASTs. No generalized optimizer, algebraic simplifier, or arbitrary statement
       deletion is permitted in the erasure checker. Any necessary non-erasable edit is
       outside this authority and must be reported, not silently authorized.

    8. Coverage before a whole-peak claim.
       Before production, enumerate a finite observation-site manifest against the exact
       closed source ASTs: module, qualified function, expression/event location, observed
       role, branch/nonbranch scope, and either an explicit tap or a justified dominance
       omission. This is part of the existing Phase C oracle-source derivation, not a new
       workflow gate. Phase D fixes its expected behavior before telemetry code exists.
       Audit every arithmetic expression on the measured call graph, including nested
       temporaries and generator expressions. Fields cannot be zero-filled because an
       observation is missing. Missing coverage is an audit failure, not a complete peak.
       Measurements of final output or the flow-only summary never substitute for item 6.
       No counter/peak may impose a production asymptotic cutoff or a theoretical constant.

    9. Environmental metadata and run records.
       RunMetadata fields: wall_clock_s: float | None, python_version: str,
       platform: str, cpu: str | None, code_version: str, instance_sha256: str.
       wall_clock_s is externally supplied: exact finite nonnegative float or None
       (unmeasured, never represented by fake zero). Text fields are exact nonempty str;
       cpu may be None for unknown. instance_sha256 is exact lower-case 64-digit hex.
       None does not certify an unmeasured resource. No discovery, clock, subprocess,
       Git query, network, or file I/O runs inside telemetry constructors or measured solve.
       RunRecord fields: algorithm: AlgorithmStats, metadata: RunMetadata; exact types.
       These records and measurements are never certificate fields. Their constructors
       assert local data validity, not authenticity of a supplied clock/version/hash.
       Unit 19/21 assembles externally measured metadata and later run serialization.
       Unit 16 rules these in-memory records only; versioned wire-format implementation
       is not smuggled into this phase. §9's versioned run-record requirement remains.
       External timing must disclose whether recording is enabled, interval boundaries,
       warmup, repeats and environment. External timers do not remove instrumentation
       overhead. A timing-only uninstrumented run must not masquerade as the same traced
       execution. Metadata differences must not change deterministic AlgorithmStats.

    10. Tests and independent evidence.
        Test both selections on every registered valid instance, matching legacy results
        exactly for the same selection and independently evaluating each witness's own raw
        pair. Across selections require numerical equality, not tied-witness equality.
        Also compare the underlying native diagnostics exactly to the uninstrumented call.
        Retain all 1,178 previous test case identities and mathematical/rejection assertions.
        Their permitted import/preservation-check adaptations are enumerated in item 13;
        the count is not permission to weaken a case. New collected count is established
        by actual collection, not assumed. Independent audit covers the observation-site
        manifest, erasure, counters, peak completeness, isolation and mutation detection.
        Real and scripted nonzero accepted/rejected/terminal look-ahead cases are required
        for accounting; n>3 by itself is not a sufficient path-coverage predicate.
        Later Unit 20 builds the benchmark corpus; Unit 21 runs experiments. Small tests
        do not prove generic trace invariance or support-size scalability.

    11. Work and encoding statement.
        Forwarding fixed scalar observations adds O(1) tap/record operations per recorded
        scalar expression, O(n+m) initial input observations and a fixed number of bucket
        records. No extra optimization query, family preparation, graph/multiplicity-sized
        replay, or all-shore enumeration is permitted. Streaming maxima retain no execution
        history. Context-local storage is bounded in record count, not byte-size constant.
        Source mathematical operation carriers remain those of the selected algorithm:
        Standard O(M^2 log M) versus Accelerated O(M log M) oracle factors. Monitoring
        costs and Python bit operations are reported separately; no elapsed-time or memory
        bound is inferred merely from the mathematical arithmetic-operation theorem.
        Strong polynomiality does not imply equal observed counters under varying input
        magnitudes. Event counters are measurements, not a count of all elementary operations.

    12. Error, Empty, and zero distinctions.
        New public wrong types/values: exact ValueError. Internal violated closed promises:
        RuntimeError. Dependency exceptions: propagated unchanged. Empty ((0,1),None)
        retains no branch/context; nonempty infeasible branches still have preparation
        rows and seed/oracle diagnostic work. Feasible zero-valued H0 candidates are
        measured, not treated as Empty. Labels, native candidate provenance and raw output
        remain intact. No telemetry record proves global optimality or a universal theorem.

    13. Explicitly bounded reopening and exact future file scope.
        This authority proposes an OBSERVATIONAL extension, not a correction of the proved
        algorithm. After its authority commit/remote closure, only these closed production
        modules may receive the erasable taps/events of items 6–8:
           exactfrac/instance.py, exactfrac/shore.py, exactfrac/families.py,
           exactfrac/witness.py, exactfrac/rational.py, exactfrac/sign_routing.py,
           exactfrac/parity_cut.py, exactfrac/flow.py, exactfrac/oracle.py,
           exactfrac/solve.py.
        Instrument only functions reached by the measured canonical-instance solve, plus
        import plumbing. Normalization/serialization-only functions not reached by it stay
        byte-identical. Public record fields, constructor validation and exports stay
        byte-identical. Arithmetic property bodies may receive only erasable observations.
        branch.py remains entirely byte-identical: its numerical work is in instrumented
        dependencies; its repeated shore-universe bound is dominated by the already
        executed lower-layer validation bound. The site manifest must verify that argument.
        Both branch algorithms and all five protected Standard definitions retain their
        old bytes. Only the transitive-import test envelope gains the new leaf.

        Closed test files permitted ONLY dependency/preservation-guard adaptations:
           tests/test_instance.py, tests/test_shore.py, tests/test_families.py,
           tests/test_witness.py, tests/test_rational.py, tests/test_sign_routing.py,
           tests/test_parity_cut.py, tests/test_oracle.py, tests/test_branch.py,
           tests/test_branch_accelerated.py, tests/test_solve.py.
        Do not touch their fixtures, expected numbers, witnesses, native counter values,
        query traces, exception assertions, case IDs, or prohibitions on inexact arithmetic,
        algorithmic telemetry feedback, verification imports and magnitude-driven loops.
        Whitelists may add only the new leaf dependency and explicitly named observation
        primitives. No wildcard/blanket relative-import permission. Exact old source-byte
        preservation assertions must be retained for their immutable historical fixtures
        and complemented by erasure-equivalence checks for instrumented live definitions,
        not replaced by a freshly blessed hash alone. The Unit 14 test's old Standard-test
        SHA remains a historical reference, not silently overwritten to bypass its purpose.
        New Phase D files: tests/test_telemetry.py, tests/_telemetry_source_audit.py,
        tests/fixtures/unit16_legacy_sources.json (exact unexecuted old source/test bytes).
        The audit helper is stdlib-only and must not import future telemetry/production.
        The JSON is an authenticated immutable comparison fixture, not executed code or a
        second solver. Legacy content identity and allowed test-AST edits are preregistered
        in the oracle catalogue. Hashing it does not change any private evidence record.
        New Phase E files: exactfrac/_telemetry.py and exactfrac/telemetry.py, plus the
        bounded edits above. Existing test adaptations are frozen at RED; do not revise
        them to accommodate unexpected implementation behavior. test_flow.py and
        test_verify_brute.py, exactfrac/branch.py, every exactfrac_verify file, package roots, pyproject.toml,
        instance corpus, SPEC_LOCK, CONTRACT and all other paths remain frozen.
        Actual later patches may omit unnecessary files from this ceiling; no other file
        or edit purpose is implicitly authorized. Export all originals before adaptation.

    14. Existing lifecycle only.
        Phase B changes only DESIGN/TEST_PLAN, unstaged for review, then separately staged,
        committed, tested and remotely closed. No observation primitive or consuming test
        is created here. Phase C fixes independent tables, site manifest and preservation
        references. Phase D applies the declared tests/fixtures/guard adapters, requires
        specific missing-exactfrac.telemetry RED and the same 1,178 legacy cases passing
        with the new telemetry test excluded. No new leaf/telemetry module exists in RED.
        Phase E adds the new modules and ONLY the authorized erasable observation edits,
        requiring GREEN, legacy identity/conservation tests, both routes, live Ruff and
        the separate implementation/mutation audit. Phase G adds only finite CONFORMANCE
        coverage while preserving prior historical rows/statuses. Complete staging must
        include exactly the reviewed new and amended files; isolated staged-tree tests,
        local-postcommit tests and four-reference remote closure follow unchanged.
        No external-model gate, REVIEW_REQUEST, automatic recovery or private-note check.
        BUILD/LEARNING blocks are delivered only at full unit closure; their saved
        confirmation is required only for the transition to Unit 17.

4.14 Unit 17 — certificate construction and exact serialization
    (AUTHORITY R1 PROPOSAL; effective only on its controlled authority commit)

    1. Basis and preserved contracts.
       Source: SPEC_LOCK-pinned V2.2 def:instance, ass:active, def:parameter,
       eq:compact-density, lem:empty, lem:unit, prop:endpoints, sec:global's complete
       reconstruction table, alg:global, prop:global-invariant and their proofs.
       Sections 4.1/4.1A, 4.2, 4.4/4.4A, 4.12, 4.13, 7 and 9 remain in force.
       The mathematical certificate establishes admissibility and LITERAL RAW
       ATTAINMENT, not global optimality. Neither the source nor a SolveResult
       constructor prescribes a JSON codec; the names and wire rules below are
       explicit engineering rulings. They do not amend SPEC_LOCK or CONTRACT.
       Consume the actual Unit 16-closed sources, including their observational
       imports. No earlier snapshot or historical source fixture replaces them.

    2. Ownership and exact public API.
       New production file: exactfrac/certificate.py. Its __all__ is exactly
         ("build_certificate", "serialize_certificate").
       Both arguments are required and positional-or-keyword, with these names:
         build_certificate(instance: Instance, result: SolveResult) -> dict[str, object]
         serialize_certificate(instance: Instance, certificate: dict[str, object]) -> bytes
       Typical composition is serialize_certificate(instance,
       build_certificate(instance, result)). There is no one-argument serializer,
       default, overloaded result/dict input, route flag, file destination or mode.
       The builder derives a detached JSON-ready object from the closed records.
       The serializer consumes an object, revalidates it against the instance, and
       returns bytes. A previous successful build is never a validation token.
       No Certificate dataclass, duplicate mathematical state, added SolveResult
       field, Empty sentinel, package-root re-export or mutable cache is introduced.
       SolveResult remains exactly (value: ExactValue, witness: Witness | None).

    3. Supported inputs and claim boundary.
       Both functions first require type(instance) is Instance and consume a normally
       constructed canonical active instance. They do not normalize, reconstruct or
       reaggregate it. Constructor-bypassing forgeries are outside this closed-record
       contract. The builder next requires type(result) is SolveResult, not the outer
       (SolveResult, SolveStats) pair, telemetry record, subclass or duck-typed object.
       Normal construction of SolveResult guarantees record types, not attainment.
       Validate every supplied nonempty witness against this instance and compare
       its recomputed raw fields literally with the supplied ExactValue fields.
       Any admissible literally attaining pair is accepted, including a suboptimal
       pair, an endpoint that lost the global comparison, or a zero-valued witness.
       Do not rerun a solver or demand source-branch membership, a winning-candidate
       label, a density >=1, or proof that solve actually produced the records.

    4. Versioned object schema, with no added envelope state.
       The format tag is exactly the built-in str "exactfrac-certificate/1".
       A nonempty object has EXACTLY these keys, in emitted order:
         format, empty, N, D, U, y.
       An Empty object has EXACTLY these keys, in emitted order:
         format, empty, N, D.
       All keys are exact built-in strs. empty is an exact bool. N is an exact
       nonnegative built-in int; D is an exact positive built-in int. bool, int/str/
       dict/list subclasses, float, Fraction, coercible objects and null substitutes
       are not accepted where exact types are required. Unknown and missing keys
       are rejected. In particular no digest, embedded instance, instance ID,
       witness wrapper, schema-version number, branch, stats, timing, labels or
       environmental fields are added. The format tag is the existing versioning
       mechanism of sections 2 R6 and 9, not a second version field.
       The input dict's insertion order is immaterial; the emitted field order is
       fixed. This presentation rule never licenses sorting or repairing U or y.

    5. Original coordinates and complete nonempty admissibility.
       For empty == False, U is an exact nonempty list of exact int vertex indices
       in [0,n), strictly increasing, with no duplicates. It is not an internal
       bitmask, label list or auxiliary-cut shore. y is an exact list of exact
       two-element lists [edge_ref, count]. Both entries are exact ints; references
       are in [0,m), strictly increasing and unique; count is strictly positive,
       at most that edge's q_e, and its edge crosses U. Missing coordinates are
       zero. An empty sparse y list is legal and is NOT an Empty result.
       Edge references resolve only by position in the canonical instance edge
       list. The independent checker must validate that list BEFORE resolving refs.
       For the reconstructed boundary selection compute
         Y = sum(y_e), s = sum(f[v] for v in U), e = sum(q_e for edges internal to U).
       Require s+Y odd and s+Y >=3, and then the two literal identities
         N == 2*(e+Y), D == s+Y-1.
       No GCD reduction, rescaling, sign repair, zero normalization, rounding or
       comparison by rational equivalence substitutes for those two equalities.
       Noncrossing coordinates are zero; no explicit parallel-copy list is encoded.

    6. Genuine Empty, not an absent-payload shortcut.
       For empty == True, U and y must be ABSENT, even if their proposed values
       are null, [] or zero. Require Q==1 and the literal pair N==0,D==1.
       For the builder, result.witness is None selects only this validation path;
       None at Q>1 is rejected, notwithstanding the valid SolveResult shape.
       The equivalence is lem:empty under the independently established active
       instance hypotheses. Neither an empty flag nor N==0 proves it by itself.
       With a Witness, empty is False and both payload fields remain present even
       when N==0 or y==[]. The source allows such admissible nonoptimal witnesses.

    7. Construction, validation order and frozen helper reuse.
       Builder order: exact Instance, exact SolveResult, then the None/nonempty
       case. Empty checks Q and the literal pair without constructing Witness.
       Nonempty calls closed witness_value(instance, result.witness), which supplies
       full admissibility and raw evaluation, before literal field comparison.
       Export U with shore_to_list and y with dense_y_to_sparse; allocate a fresh
       outer dict and detached lists, preserving the supplied value integers.
       Do not reconstruct another witness from provenance or a transformed root.

       Serializer order: exact Instance; exact dict; exact-str keys and presence
       of format/empty; exact format tag; exact-bool empty; exact case-specific key
       set; N type/nonnegativity; D type/positivity; then the Empty or nonempty path.
       Empty follows item 6. Nonempty first uses shore_from_list and rejects the
       empty shore, then sparse_y_to_dense, then Witness and witness_value, then
       literal N/D equality. The closed helpers' declared within-payload validation
       precedence is retained. The normal output of a helper is consumed once;
       no independent optimization, shared verifier, or hidden normalization is used.
       Helper return types/shapes that the consumer explicitly checks must satisfy
       their closed promises: evaluator exact ExactValue; decoded shore exact int;
       decoded counts exact length-m tuple; exported U exact list of exact ints;
       exported sparse y exact list of exact two-int lists. An explicitly detected
       normal-return promise violation is RuntimeError. No generalized validator
       of maliciously forged closed objects or second evaluator is required.

    8. Error taxonomy and nonmutation.
       Invalid data through these supported signatures raises exact built-in
       ValueError, including malformed objects, inadmissibility, false Empty and
       raw mismatch. No new certificate exception class. A dependency's raised
       exception propagates unchanged, including identity; do not catch broadly
       and convert it into ValueError, Empty or partial success. Wrong Python call
       arity and frozen-record mutation retain Python/dataclass behavior. Diagnostic
       prose is not stable API and must not require formatting enormous integers.
       Never mutate the instance, result, witness, value, input envelope, nested
       arrays or prior outputs. A caller may mutate an exported object; subsequent
       serialization must validate its current content, not trust its provenance.
       This API is synchronous; concurrent mutation of the same caller-owned dict
       during one call is not a supported snapshot/transaction contract.

    9. Canonical certificate bytes.
       The returned type is exact bytes. Emit one JSON object with the field order
       in item 4, literal unescaped ASCII keys/tag, lowercase true/false, arrays
       bracketed with [,], and commas/colons without spaces. No pretty-printing,
       leading whitespace, internal whitespace, trailing spaces or byte-order mark.
       Append exactly one LF byte (0x0a) after the closing brace, not CRLF. No other
       bytes follow. All certificate characters are ASCII and are encoded as UTF-8.
       Every integer is a JSON NUMBER token, never a quoted string, binary/hex
       spelling, exponent, decimal fraction, leading plus, -0 or leading-zero form.
       Nonnegative tokens have grammar 0 | [1-9][0-9]*; positive tokens exclude 0.
       The format slash is literal, not escaped. No null or nested witness object.
       These rules uniquely determine the bytes of any valid object; repeated
       construction/serialization of identical instance/result fields is byte-equal.
       Bytes intentionally contain no instance identity: verification is always
       with the separately supplied instance, never with a digest alone.

    10. Large integers, resource policy and work accounting.
        No schema-level fixed bound on N,D,q,f,counts, integer bit lengths, digit
        counts or certificate byte length is introduced. In particular no binary64
        interoperability limit and no inherited interpreter decimal-conversion
        cutoff becomes an undocumented input restriction. Decimal encoding must
        work for arbitrarily long finite valid integers, subject to host resources,
        without changing process-global integer-conversion limits or requiring the
        caller to change them. Use private exact bounded-digit conversion (for
        example divmod by 10**9 and formatting only the bounded remainders).
        This is representation conversion, not rescaling the mathematical pair.
        Floor division/modulo/divmod and digit-length loops are permitted ONLY for
        this byte-encoding task, not optimization or multiplicity expansion.
        No public quota/limit argument or silently truncated output is added.
        Native resource failures such as MemoryError are propagated, never reported
        as successful verification, mathematical Empty, or invalid mathematics.
        A deployment accepting untrusted files must enforce its own explicit byte/
        work budget BEFORE this core boundary; this unit is not a denial-of-service
        protection layer and adds no file/network ingestion. Later ingress policy
        must disclose its limits separately and may not silently redefine /1.
        Valid-object construction/admissibility uses O(n+m) structural scans and
        O(n+m) storage, excluding encoded integer sizes. With L output bytes, byte
        serialization also requires output-sized storage/work plus decimal conversion
        bit cost. No magnitude-independent byte-runtime or strong-operation claim
        is made for the codec. It never iterates over all shores or Q unit copies.

    11. Decoding and (instance, certificate) checking ownership.
        Unit 17 has NO raw-byte/text/file decoding API, certificate-from-dict record
        constructor, or public verification function. serialize_certificate takes
        only an object; passing bytes/text is a ValueError, not an attempted decode.
        Unit 18 owns production decoding and independent check.py. Before production,
        Phase C fixes an independent TEST-ONLY parse-and-recompute route, integrated
        into the new test file in Phase D. Its only verification inputs are serialized
        instance bytes and certificate bytes: not Instance, SolveResult, Witness,
        a production-built dict, side-channel expected sums or validation flags.
        It imports no exactfrac module and shares no production parser, serializer,
        validation, shore or witness helpers. Running in a fresh subprocess must
        demonstrate this isolation; importing the certificate module legitimately
        loads closed dependencies through SolveResult and is a DIFFERENT import test.
        Unit 18 must retain that independence, not import the test helper as its
        production checker. Its eventual public callable/error interface belongs
        to Unit 18 authority; it is neither implemented nor an availability gate here.

        Certificate-byte acceptance requires exactly item 9, not merely a JSON
        object with equivalent values. The independent test decoder rejects invalid
        UTF-8, BOM, duplicate keys, wrong order, escaped-key/tag alternatives,
        whitespace/newline variants, extra JSON/trailing data, noninteger tokens,
        unsupported tags and malformed schema before mathematical acceptance.
        Duplicate-key rejection must occur before constructing a last-key-wins dict.
        Python-object serialization cannot observe duplicates already erased by a
        caller's decoder; Unit 17 claims no such raw-text rejection coverage.

        Instance bytes carry the existing exactfrac-instance/1 object of 4.1A.5,
        with required format,n,edges,f and optional labels. This is canonical GRAPH
        data, not a new instance byte-normalization schema: JSON object-key order
        and ordinary JSON whitespace are immaterial at this input boundary. Decode
        UTF-8 only, no BOM, one complete document; reject duplicate decoded keys,
        unknown/missing keys, floats/exponents/nonfinite numeric tokens, -0 and
        non-JSON numeric spellings. Preserve exact integer tokens, including signed
        integer labels, without an accidental digit cap; strings retain their exact
        decoded label values. Validate all 4.1A object/label rules, n, f, orientation,
        strict canonical edge order, positive multiplicities, nonempty support and
        active f<=d_q before ANY certificate reference is interpreted. Do not sort
        or aggregate serialized edges. A certificate requires actual instance data;
        an identifier, omitted instance or envelope-embedded replacement is invalid.
        Unit 17 adds no production instance byte writer or changes to Instance's
        frozen to_dict/from_dict methods. Test input bytes are assembled independently
        from registered primitive instance data, not production Instance.to_dict.
        The test decoder and future checker use the same no-hidden-magnitude-limit
        semantic domain; host-resource failure is not a mathematical verdict. Later
        network/file budget controls are external and explicitly distinct as above.

    12. Dual-route determinism, reconstruction and registry obligation.
        Run every currently registered valid graph entry under both Standard and
        Accelerated, plus every valid Unit 17 addition fixed in Phase C. Preserve
        registry identities even when mathematical inputs repeat. The authenticated
        current inventory is 379 U15_INPUTS plus 10 U16_INPUTS entries (ORACLE-108,
        ORACLE-118/U16_REGISTRY): 389 entries, hence 778 two-route invocations before
        new entries. These are graph/run counts, NOT pytest counts. Phase C must
        fix the cumulative inventory/fingerprints; neither old block is replaced.
        For EACH run, build and serialize its actual SolveResult; independently
        decode/recompute that certificate from the two byte streams and require
        its OWN literal pair, then cross-multiply to compare routes numerically.
        Under ties, different witnesses, raw pairs and bytes are legal between
        selections. Never canonicalize the witness, select another minimizer, add
        a secondary tie rule, or invoke another solve to force equal certificates.
        Repeated identical inputs must produce identical bytes, separately from
        cross-route numerical agreement. Labels and diagnostics do not affect bytes.

        Cover baseline and all endpoint reconstructions including direct H2, using
        source-derived/captured candidate records as LOCAL attainment controls, not
        claiming every endpoint is a final winner. H2's raw pair is (4,2); both one
        count of 2 and two counts of 1 must be covered. By 4.12.10, complete branch
        solves already dominate/tie H2; no strict-H2-winner graph is invented.
        Observing closed candidates through test-local bindings is permitted; no
        production trace API, solver edits or reimplementation of reconstruction.
        A suboptimal zero-valued admissible witness must serialize nonempty.

    13. Direct imports and exactness boundary.
        Permitted direct imports: optional future annotations; Instance from instance;
        SolveResult from solve; shore_from_list/shore_to_list from shore; ExactValue,
        Witness, dense_y_to_sparse, sparse_y_to_dense, witness_value from witness.
        No other runtime imports are needed or authorized for the fixed certificate
        encoder. Transitive Unit 16 observation imports in these closed dependencies
        remain untouched; they do not authorize direct telemetry imports/recording.
        No direct solve function, branch/oracle/cut/flow/context access, private closed
        helper imports, verifier/test/handoff imports, I/O, timing, randomness, hashes,
        subprocess, dynamic evaluation/import, global conversion-setting changes,
        Fraction, decimal, float, true division, tolerance or GCD normalization.
        Do not let set traversal decide emitted order. Iterate fixed field tuples,
        dense indices and canonical edge refs. The independent test parser may use
        standard-library JSON hooks with independent strict validation; they are not
        imported into production. No closed dependency is reopened by this unit.

    14. Prospective tests, scope and lifecycle.
        Authority package scope is ONLY docs/DESIGN.md and docs/TEST_PLAN.md. Insert
        this section and append TEST_PLAN 39/40 without rewriting earlier rulings.
        Apply unstaged for review; stage, commit and remotely close authority before
        Phase C independently derives byte fixtures, acceptance/rejection tables,
        parse/recompute expectations, registry/census and adversarial controls in
        ORACLE_CATALOG. No expected answer comes from future production output.
        Phase D adds ONLY tests/test_certificate.py, including its independent test
        route; require missing-exactfrac.certificate RED while production is absent.
        Phase E adds ONLY exactfrac/certificate.py under the frozen test/authority,
        then GREEN, independent implementation/mutation audit, existing regression
        and live Ruff. check.py remains absent; no Unit 18 availability requirement.
        After GREEN only the scoped CONFORMANCE amendment is allowed, followed by
        complete-candidate staging/isolation, local commit and remote closure.
        Final candidate scope is certificate.py, test_certificate.py and CONFORMANCE;
        authority/oracle amendments were already separately closed. All 44 starting
        files remain frozen except the expressly scoped documentary phases. No new
        gate, external-model requirement, REVIEW_REQUEST or private-note inspection.
        Finite conformance covers assembly, exact bytes, admissibility/raw attainment
        checks and integration, not global optimality or a completed Unit 18 checker.

4.15 Unit 18 — independent certificate-byte checker
    (AUTHORITY R1 PROPOSAL; effective only on its controlled authority commit)

    1. Source basis and affirmative placement ruling.
       Retain exactfrac_verify/check.py, affirmatively reconciling this choice with
       section 3, sections 4.4.5/4.4A.1, 4.14 item 11, and section 7. There is no
       relocation. The earlier starting-gate absence guard authenticated a closed
       state; it did not adopt a path or interface. This section adopts the Unit 18
       interface. New consuming test: tests/test_verify_check.py. Both package-root
       __init__.py files and exactfrac_verify/brute.py remain byte-identical.
       Mathematical authority is SPEC_LOCK-pinned V2.2 def:instance, ass:active,
       def:parameter/eq:compact-density, lem:empty with its complete proof, lem:unit,
       prop:endpoints, and sec:global's reconstruction table, alg:global and proofs.
       The latter passages explain solver outputs; they do not restrict the checker
       to endpoint, globally optimal, or solver-originated witnesses. CONTRACT and
       the closed /1 instance/certificate schemas are preserved, not revised.

    2. Public API, success and ownership.
       The exact module-level __all__ tuple is ("verify_certificate",).
       The only public callable is:
         verify_certificate(instance: bytes, certificate: bytes) -> None
       Both arguments are required positional-or-keyword parameters with exactly
       these names, annotations and no defaults. Success returns exactly None.
       There is no bool verdict, returned quotient, decoded record, new public
       exception class, path/file overload, callback, mode, solver selection, budget
       flag, public decoding helper, certificate constructor, or root re-export.
       Both inputs must have exact built-in type bytes. Reject str, bytearray,
       memoryview, subclasses, Instance/SolveResult/Witness, dicts, streams and paths;
       do not coerce or invoke caller conversion/I/O methods. Public decoding is
       owned by this one verification entry point; any parsers are private.
       Pure validation returns no independently mutable mathematical state. A
       caller needing display data retains its original inputs; later CLI policy
       is separately ruled. No mathematical result is inferred from function names.

    3. Verification claim and instance relationship.
       Return normally iff the supplied canonical active instance and certificate
       byte strings satisfy items 4--8, subject to operational/resource failure.
       The claim is admissibility and LITERAL RAW ATTAINMENT, or genuine Empty.
       It is not a certificate of global optimality, solver provenance, branch
       attribution, telemetry integrity, execution correctness or an exact block
       count. Accept every valid admissible witness with its literal pair, even
       when suboptimal, nonempty zero-valued, or a losing local endpoint candidate.
       No solver/optimizer/reference maximizer is invoked by the checker.
       Verification needs the actual separately supplied instance bytes. A digest,
       identifier, absent instance or certificate-embedded replacement is invalid.
       No digest or envelope field is added. This is semantic checking, not a
       cryptographic unique-instance binding: the same certificate may be valid
       for two instances. Changing only valid metadata need not cause rejection.

    4. Complete instance validation precedes certificate inspection.
       First require exact bytes for instance; then decode and validate the entire
       instance including labels, canonical support order and active condition.
       Only afterward inspect/type-check/parse certificate or resolve its refs.
       Thus invalid instance input does not trigger certificate parsing. Malformed
       instance syntax may fail during decoding; after decoding use this order:
       outer object/key set and tag; n; f; optional labels; edge records and order;
       derived Q/degrees and active condition last. No repair/normalization path.
       Instance bytes use strict UTF-8 with no BOM and exactly one complete JSON
       document. Ordinary JSON whitespace (space, tab, LF, CR), object key order,
       valid string escapes and UTF-8 label spellings do not alter decoded meaning.
       Reject comments, trailing commas, concatenated documents, nonwhitespace
       trailing content, invalid UTF-8, UTF-16/32 encodings and leading BOM.
       Detect duplicate DECODED object keys before last-key-wins collapse, including
       escaped spellings of the same key. Required keys: format,n,edges,f; optional
       labels only. Decoded format is exactly "exactfrac-instance/1". Reject every
       unknown/missing key. No raw-record aggregation or label-keyed adapter.
       Every numeric token in instance data is an integer: 0 or -?[1-9][0-9]*.
       Reject -0, leading plus/zeros, exponents, fractional/nonfinite tokens and
       non-JSON number spellings without first creating float approximations.
       These lexical rules apply throughout the input, including metadata.

    5. Independently implemented instance representation predicates.
       Require exact int n>=1; exact list f of length n with exact positive ints;
       nonempty exact list edges, each an exact length-three list of exact ints
       [u,v,q] with 0<=u<v<n and q>=1. Pairs (u,v) are strictly lexicographically
       increasing and unique. edge_ref is the position in THIS list. Do not sort,
       aggregate, reorient or discard serialized records. Booleans are not ints.
       If labels is present, require an exact length-n list of exact str or int
       values, pairwise distinct under their decoded values; null is not an absent
       labels field. Signed integer labels are allowed; 1 and "1" are distinct.
       Do not normalize strings, case-fold, coerce labels or use labels as indices.
       Valid JSON string escape decoding supplies the label value, including escaped
       control code points and escaped unpaired surrogates supported by the inherited
       str domain; raw invalid UTF-8 remains rejected. No new Unicode scalar-value
       restriction is silently added. Surrogate-pair escapes decode by JSON rules.
       Compute Q=sum(q) and each d_q(v) by adding q to both distinct endpoints;
       require f[v]<=d_q[v] at every vertex. Positive f makes isolates unsupported.
       Check declared lengths before allocating arrays based only on claimed n.
       Malformed and non-active instances both raise exact ValueError here. The
       producer's InvalidInstance/UnsupportedInstance classes are not imported,
       returned, reproduced or added to this independent public API.

    6. Certificate grammar is the exact closed byte grammar, not merely JSON.
       Require exactly one ASCII-encoded object, no BOM/spaces/escapes, exactly one
       terminal LF and no trailing bytes. In the following grammar quoted field
       names/tags/punctuation are literal bytes; NUM=0|[1-9][0-9]* and POS=[1-9][0-9]*:
         empty: {"format":"exactfrac-certificate/1","empty":true,"N":NUM,"D":POS} LF
         full:  {"format":"exactfrac-certificate/1","empty":false,"N":NUM,"D":POS,"U":[NUM(,NUM)*],"y":[PAIR(,PAIR)*]} LF
         PAIR:  [NUM,POS]; the whole contents of y may instead be empty.
       U has at least one entry. The printed grammar's spaces/parentheses/NUM/POS
       are explanatory, not wire bytes. Field order is exactly as shown. No extra
       envelope, nested witness, digest, embedded instance, metadata, quoted integer,
       sign, -0, exponent, decimal point, alternate boolean, duplicate/escaped key,
       escaped tag slash, pretty-printing, CRLF or additional/missing LF is accepted.
       Recognize the grammar directly with an independently written private lexical
       parser, not by importing the producer or by reserializing a decoded object
       and treating its own output as proof of canonical input. A deterministic
       cursor over the fixed grammar is the selected reference strategy. Parsing
       full magnitudes into exact ints uses item 9, never full-token int conversion.
       No third-party parser or production encoding routine is shared.

    7. Nonempty semantic predicates and literal pair.
       Independently validate each U index in [0,n), strict increase, nonemptiness,
       and each y=[edge_ref,count] in strictly increasing ref order with 0<=ref<m.
       Each count is positive and <=q[ref], and exactly one endpoint is in U.
       Omitted coordinates are zero. Reject duplicate/descending refs or vertices;
       never merge, sort or repair them. The sparse positions do not renumber refs.
       Independently compute s=sum(f[v] for v in U), e=sum(q for internal edges),
       and Y=sum(selected counts). Require s+Y odd AND s+Y>=3 before accepting:
         N == 2*(e+Y)
         D == s+Y-1
       Both equalities are literal integers, not cross-products, reduced fractions
       or tolerances. N may be zero; D is positive. Do not infer admissibility solely
       from even D, a positive rational value, or agreement with the producer.
       No boundary copy is expanded, and no extra shore or count vector is selected.
       Membership markers plus scans of original lists suffice; dense y need not be
       allocated because all omitted/noncrossing coordinates are defined to be zero.

    8. Genuine Empty has no witness payload.
       The empty grammar contains no U or y fields, even with null/[] values.
       For the already independently validated active instance require Q==1 and
       literal (N,D)==(0,1), using lem:empty. The flag alone proves nothing.
       Q>1 with empty true is invalid. Nonempty zero and y=[] remain distinct valid
       possibilities under item 7. No unit-lower-bound or endpoint-only filter may
       reject a valid suboptimal witness. The checker does not construct a witness
       for Empty or invoke lem:unit's constructive procedure.

    9. Exact arithmetic, resources, error translation and determinism.
       No schema-level limit on integer magnitude, digit count, n/m, or byte length
       is added. Decode arbitrarily long finite integer tokens subject to available
       resources, without changing or requiring changes to process-global decimal
       conversion/recursion settings. Private digit accumulation or bounded chunks
       are allowed. No float/Fraction/Decimal, GCD, rescaling, sign/zero repair,
       approximate comparison, true division, hashing as mathematical identity,
       Q-copy expansion or all-shore search. Digit-driven work is codec work, not
       magnitude-dependent optimization. Fixed loops/list orders control validation;
       set membership for uniqueness is allowed but set traversal selects no order.
       Invalid byte/type/schema/instance/witness data raises exact built-in ValueError.
       Narrow decoding exception translation is explicitly authorized: a built-in
       UnicodeDecodeError raised by the strict UTF-8 decode, or json.JSONDecodeError
       raised by the standard JSON decoding operation, becomes exact ValueError.
       Limit each catch to that operation; do not blanket-catch ValueError/Exception.
       Other dependency exceptions propagate unchanged, including identity; in
       particular MemoryError, RecursionError and injected operational failures are
       not false/None/Empty or invalid-mathematics verdicts. Private deliberate
       validation ValueErrors may propagate directly. Wrong call arity retains
       Python TypeError. Diagnostic text is not stable API and must not stringify
       arbitrary full-magnitude integers. No partially decoded output is returned.
       Identical bytes give the same success/rejection semantics across repeat calls
       and hash seeds, subject to resources; no clock/randomness/global cache/state.
       Input bytes are immutable; the function retains no caller input or validation
       token across calls. Instance labels cannot influence certificate mathematics.
       Structural verification scans O(n+m+|U|+k) entries for k sparse counts, apart
       from label-uniqueness and byte/numeral-processing costs. Account for L input
       bytes, large-int bit operations, and decoded storage separately. No universal
       strong-polynomial byte-runtime, constant memory or denial-of-service claim.
       Explicit ingress limits belong outside this core, disclosed separately by
       future CLI/service policy; resource exhaustion is not schema rejection.

    10. Independence boundary and standard-library substrate.
        New checker runtime imports are limited to optional future annotations and
        standard-library json. Instance JSON uses independent local object_pairs_hook,
        parse_int, parse_float and parse_constant handlers; float/constant handlers
        reject without constructing approximate numbers. This standard-library syntax
        substrate is not shared project validation. Do not import any exactfrac
        module, exactfrac_verify.brute, test/handoff material or producer helper,
        directly, transitively, dynamically or only under TYPE_CHECKING. No dynamic
        eval/exec/import, file/network/subprocess I/O, optimizer, telemetry or hash
        lookup. The old test-only oracle is not promoted/copied into the checker.
        Fresh-process tests block all exactfrac imports and unexpected project
        imports, check sys.modules and origins, and run with only the independent
        package physically available where practical. The generator/integration
        process may use frozen solvers and serializer; it sends only two byte
        strings to the checker process, never prevalidated objects or expected sums.
        An AST/source audit complements but cannot replace executed import isolation.
        No mandatory external/second-model review is introduced.

    11. Narrowly authorized Unit 17 test transition — no other reopening.
        The author's explicit authorization retains check.py and reopens exactly
        three temporal checks in tests/test_certificate.py, closed original SHA-256
        c70f7120fe10d07668fc37624843cc77a02ef58244fbda432d04591123042724.
        This exception supersedes only those forward-absence/whole-file prohibitions;
        all mathematical assertions, fingerprints, record contracts and frozen
        production bytes remain unchanged. Unit 17 closure/evidence stays historical.
        Phase B changes NO test file. Record this exception in DESIGN/TEST_PLAN and
        complete the ordinary authority adoption before either edit below.

        Phase C replaces exactly the one original line in
        test_closed_fixture_authority_and_registry_identity:
          assert _sha(_CATALOGUE.read_bytes()) == _CATALOGUE_SHA
        with exactly these three lines at the same indentation:
          catalogue_bytes = _CATALOGUE.read_bytes()
          assert len(catalogue_bytes) >= 3_212_040
          assert _sha(catalogue_bytes[:3_212_040]) == _CATALOGUE_SHA
        Keep _CATALOGUE_SHA unchanged at
        04ef6a4b38463aecb0d86731d1873aadb4acb8bc8a8593e0ea82b4325e56e7ac.
        Every other byte in that test file is preserved. The catalogue append keeps
        that entire original prefix byte-identical; a shorter file must fail length,
        any prefix change must fail SHA, and appended Unit 18 bytes get their own
        independently derived identity checks. Retain both checker-absence lines
        during Phase C. Exact C scope: docs/ORACLE_CATALOG.md plus only this guard
        replacement in tests/test_certificate.py. Stage/commit/close these two paths
        together in the existing oracle lifecycle; no additional gate is added.

        Phase D deletes exactly one complete line with its original indentation/LF:
          assert not (_ROOT / "exactfrac_verify/check.py").exists()
        from each of test_exact_public_surface_and_closed_record_ownership and
        test_closed_sources_and_production_import_exactness_boundary. Both enclosing
        functions otherwise remain BYTE-IDENTICAL. No replacement assertion,
        whitespace cleanup, altered import, reformatting or incidental edit is
        permitted. The whole D version must equal the authenticated C version minus
        those TWO precisely located lines, with every other byte conserved. AST
        equivalence is insufficient. Exact D scope: add tests/test_verify_check.py
        and delete only those two lines in tests/test_certificate.py. No checker yet.
        Record successive complete-file SHA/blob identities and byte-exact transforms
        in the corresponding evidence. Never rewrite original Unit 17 hashes or
        authenticated packages/checkpoints. Baseline R1's stale comment is historical,
        not an authority amendment or reason to regenerate a passed helper.

    12. Coverage, independent expectations and two solver selections.
        Retain all 396 closed registry identities and both selections: 792 actual
        final solves before any registered Unit 18 additions. Do not deduplicate
        mathematical inputs. For each actual result emit the frozen /1 bytes, run
        this checker from only serialized inputs, and independently recompute the
        literal pair using a separate test route; compare routes numerically by
        exact cross-products. Do not require equal witnesses/raw pairs/bytes across
        ties and do not invoke extra solvers to force equality. Cover real baseline
        and all endpoint/local reconstructions, both H2 shapes, valid interior and
        suboptimal/zero witnesses, all 31 literal byte fixtures, 140 inherited wire
        rejection rows and seven valid instance-wire variants, plus independently
        fixed Unit 18-specific API/parser/isolation/exception cases. These are
        inherited fixture/run counts, not a prescribed new pytest count.
        Oracle fixtures precede production; expected answers cannot be generated by
        the checker under test or by producer/consumer agreement alone. Source review
        and the independent implementation audit include executed fault variants and
        classify their actual targets instead of claiming every variant is production.
        Stable /1 acceptance is tested, not a new instance byte-canonicalization rule.

    13. Exact lifecycle and final scope.
        Phase B adds this section and TEST_PLAN 41/42 only; all other 44 committed
        files remain frozen. Interface probe stays private and is syntax/lint checked
        without execution; never a production stub. B application leaves docs unstaged,
        followed by existing review/staging/local commit/postcommit tests/remote closure.
        Phase C uses item 11's two-path exception and independently fixed catalogue
        additions; remotely close it before D. Phase D uses its exact two-path scope,
        requires one missing-exactfrac_verify.check collection error, pytest exit 2,
        preserves the 2,445-case existing baseline with only the new test ignored,
        and leaves the old test modified unstaged and new test untracked.
        Phase E adds only exactfrac_verify/check.py under the frozen D tests, then
        targeted/full GREEN, repository Ruff, independent audit and isolation review.
        After GREEN amend only finite scoped CONFORMANCE, preserving previous rows.
        Final H candidate: docs/CONFORMANCE.md, exactfrac_verify/check.py,
        tests/test_verify_check.py and tests/test_certificate.py (two D deletions).
        The C prefix amendment was already committed. Run existing exact staged-tree
        isolation, local commit/postcommit tests and separate approved-commit closure.
        New test counts are measured, not guessed; no generic future-path absence
        assertion becomes a permanent regression constraint in Unit 18 tests.
        No CLI, new producer/instance codec, later corpus campaign, experiments,
        release, additional gate, REVIEW_REQUEST, private-note verification, rollback
        or automatic repair. Unit 17 production remains closed throughout.

4.16 CLI composition of the closed solver, certificate emitter and checker
    (Unit 19 authority R1 — effective only on controlled authority commit)
    1. Source and scope. Retain exactfrac/cli.py from section 3. The new consuming
       test is tests/test_cli.py. This unit supplies a local, offline research CLI,
       not a solver, independent checker, instance normalization tool, benchmark
       driver or public-service security boundary. Read SPEC_LOCK-pinned V2.2
       def:instance, ass:active, def:parameter, eq:compact-density, lem:empty,
       lem:unit, prop:endpoints, sec:global/alg:global, the complete reconstruction
       table and relevant proofs. Read CONTRACT, 4.1/4.1A, 4.4/4.4A, 4.12--4.15,
       sections 3, 7--9, and the actual closed APIs before applying this authority.
       Mathematical semantics come from these sources; command spelling, streams,
       usage status and composition order below are explicit engineering rulings.
       Unit 18's three-check exception does not authorize any new test reopening.

    2. Invocation, exports and lifecycle. Invoke with python -m exactfrac.cli using
       the selected interpreter. Do not add a console-script entry, __main__.py,
       root re-export, executable bit or dependency; pyproject.toml and both package
       __init__.py files stay byte-identical. Module __all__ is exactly ("main",).
       The only public callable defined by this module is
         main(argv: list[str] | None = None) -> int.
       argv is positional-or-keyword. None snapshots sys.argv[1:]; an explicit
       argument must be an exact built-in list of exact built-in str values.
       Reject other containers, subclasses, bytes, booleans or coercion by exact
       built-in ValueError before imports of command dependencies or any stream/I/O
       access. Wrong Python call arity retains native TypeError. Preserve the list
       and its contents; no retained argument/input/output cache. The module guard
       raises SystemExit(main()); import alone runs no command and does no I/O.
       No additional public parser, stream-injection, decoded-record or writer API.
       main is synchronous; concurrent mutation of argv/process streams is not a
       supported contract. Tests may substitute those streams in a controlled call.

    3. Closed command grammar. Exactly two commands, case-sensitive:
         solve [--solver Standard|Accelerated] INSTANCE
         verify INSTANCE CERTIFICATE
       The solve option may precede or follow INSTANCE, but occurs at most once;
       it consumes exactly its next token. Omission selects "Accelerated" explicitly
       in this CLI, not a new default in solve(). Always pass the exact selected
       capitalized string to the closed solver. Reject lower-case aliases, whitespace
       normalization, --solver=VALUE, abbreviations, duplicate options even if equal,
       unknown options/commands, extra or missing operands and options on verify.
       Within command arguments, one standalone -- ends option recognition; later
       tokens are operands literally, including leading hyphens or another --.
       Before --, a token starting with '-' other than the single '-' is an option
       and must be recognized as specified above. Empty tokens and NUL-containing
       tokens are usage errors. There are no environment/config-file defaults,
       response files, interactive prompts, stdin JSON command protocol, seed,
       backend/fallback, quota, output-file or telemetry switches.
       '-' as an operand denotes the process's binary stdin. At most one verify
       operand may be '-'; reject verify - - before opening/reading either input.
       './-' denotes a file named '-'. Other names pass unchanged to the filesystem,
       relative to the invocation directory. No expanduser/expandvars, path repair,
       case folding, symlink resolution policy, globbing or sorting is added here.

    4. Help and usage bytes. The only help forms are the complete token lists
       ["-h"], ["--help"], ["solve","-h"], ["solve","--help"],
       ["verify","-h"] and ["verify","--help"]. They return 0 after writing
       the corresponding fixed ASCII text below to binary stdout and flushing it.
       Extra tokens invalidate a help form; help is not a switch that suppresses
       unrelated argument errors. '-- -h' after a command makes -h an operand.
       Root help is exactly the following three lines, including the terminal LF:
         usage: python -m exactfrac.cli solve [--solver Standard|Accelerated] INSTANCE
         usage: python -m exactfrac.cli verify INSTANCE CERTIFICATE
         INSTANCE or CERTIFICATE may be - for stdin; verify permits at most one -.
       Solve help is exactly the first usage line followed by:
         Writes one exact certificate to stdout; default solver: Accelerated.
       Verify help is exactly the second usage line followed by:
         Success is silent; verifies admissibility and raw attainment, not optimality.
       Help writes nothing to stderr and loads no command dependencies. An empty
       invocation or other invalid grammar returns exact int 2 after writing exactly
         exactfrac: invalid command line; use --help\n
       to binary stderr and flushing it, with stdout untouched. Here and below,
       '\n' denotes one ASCII LF byte, not two printed characters. Help/usage text
       has no leading indentation. Validate the complete token list before input
       I/O or command imports. No parser-library/version-dependent help formatting.

    5. Binary I/O ownership and precedence. After grammar validation, read each
       operand completely into bytes. For files use read-only binary opens and
       context-managed closure; for '-' use sys.stdin.buffer without closing it.
       In verify read INSTANCE first, then CERTIFICATE, then invoke the checker
       once on those exact byte strings. File acquisition is distinct from checker
       validation: a failure acquiring CERTIFICATE can occur before a malformed
       but successfully read instance reaches the checker. This does not alter
       4.15's complete-instance-before-certificate-inspection order inside that
       call. Do not probe instance validity with a fake certificate or reuse private
       checker parsers merely to impose another acquisition precedence.
       A byte-returning reader must return exact bytes, else RuntimeError. No text
       newline conversion, BOM stripping, encoding guessing or certificate rewriting.
       Do not create, overwrite or append any named file. No chdir, Git, subprocess,
       network, environment discovery or temporary files in runtime CLI production.
       Explicitly selected symlinks/FIFOs/devices follow ordinary host open/read
       semantics; this local CLI is not a race-safe path or regular-file sandbox.

    6. Solve input adapter, without reopening Instance. This CLI owns a private
       syntax-only instance-byte adapter, not a public instance byte writer/parser.
       Accept the exact instance-byte domain already stated in 4.14.11 and 4.15:
       strict UTF-8, no BOM, one JSON document, ordinary JSON whitespace/key order
       and valid equivalent string escapes allowed, duplicate DECODED keys rejected
       before last-key-wins collapse. Numeric tokens must be canonical integers;
       reject floats, exponents, nonfinite constants, -0 and non-JSON spellings.
       Signed integer labels remain permitted; strings preserve decoded values,
       including valid escaped surrogates. No Unicode normalization or coercion.
       Use standard-library json with new private syntax hooks and bounded-digit
       exact integer accumulation; never import/call checker-private helpers or
       copy a test reference into production. This syntax substrate is not a second
       implementation of graph/active validation. Send the decoded object once to
       Instance.from_dict, which owns all closed schema, label, edge-order and
       active-instance checks. Never use from_records, sort/reorient/aggregate edges,
       remove vertices or adjust capacities. Normally returned Instance is exact-type
       checked. Preserve the originally read bytes for the independent output check.

    7. Exactly one selected solve and checked emission. After creating Instance,
       call exactfrac.solve.solve(instance, selection) exactly once. Do not call
       solve_with_telemetry or repeat/compare/fallback to another selection. Require
       an exact returned tuple of length two, exact SolveResult and SolveStats,
       and native stats.branch_solver equal to the requested selection. Ordinary
       closed record construction is trusted; constructor-bypassing forgeries and
       exhaustive revalidation of diagnostic histories are not this unit's job.
       Pass the same Instance and the exact returned SolveResult to
       build_certificate exactly once, require an exact dict, and pass that object
       with the same Instance to serialize_certificate exactly once; require exact
       bytes. Call verify_certificate(original_instance_bytes, emitted_bytes)
       exactly once and require normal return to be exactly None. This independent
       composition check precedes any stdout access/write. A failed self-check is
       a failure, never an excuse to change the witness, rescale the pair, retry
       a solver or emit unverified bytes. On normal completion write precisely those
       emitted bytes to binary stdout, flush, and return exact int 0. No prefix,
       progress line, suffix, second newline, wrapper JSON, decimal approximation,
       digest, embedded instance or success banner. stderr is untouched on success.
       Stats are not serialized, measured, repaired or used to choose a witness.
       A successful emitted certificate is a certified fractional lower bound with
       its witness (or genuine Empty); never describe it as an exact block count.

    8. Verify route and import independence. verify reads both inputs and calls
       only exactfrac_verify.check.verify_certificate once with those exact bytes.
       Require normal return exactly None, then return int 0 without any output
       or stdout/stderr buffer access. Do not solve, produce, decode/reencode,
       normalize, hash as a substitute for input, or prevalidate via Instance.
       No alternate certificate format, optimality test, unit-lower-bound filter,
       branch attribution or telemetry is introduced. Valid suboptimal and nonempty
       zero witnesses remain acceptable under the checker; malformed/rescaled pairs
       and false Empty remain rejected by its unchanged rules.
       Import command dependencies lazily after complete grammar validation. A fresh
       verify invocation may load only exactfrac (its empty root), exactfrac.cli,
       exactfrac_verify (its empty root) and exactfrac_verify.check as project modules;
       it must not attempt imports of exactfrac.instance/solve/certificate/telemetry,
       brute, tests or private handoff helpers. This CLI's location under exactfrac
       does not weaken the checker's own no-exactfrac-import contract. Help/usage
       may load only exactfrac and exactfrac.cli. Import/source reviews and actual
       fresh-process blocking/origin checks must establish these route distinctions.
       Production CLI runtime imports are limited to sys, json, optional future
       annotations and the explicitly named closed command dependencies above.
       No dynamic eval/exec/importlib tricks, global monkeypatching or root exports.

    9. Errors, statuses and closed-dependency propagation. main returns only exact
       int 0 for normal command/help completion or int 2 for grammar/usage rejection.
       It does NOT turn input/dependency exceptions into a third mathematical verdict
       or a stable structured error record. Incorrect Python argv types raise exact
       ValueError; wrong arity retains Python TypeError. Private deliberate instance
       syntax rejections raise the closed InvalidInstance class. Translate only a
       UnicodeDecodeError from the strict decode, or json.JSONDecodeError from that
       JSON load, into InvalidInstance, with each catch limited to that operation.
       Instance.from_dict's InvalidInstance and UnsupportedInstance pass unchanged.
       All other exceptions from reads/open/close, json hooks/substrate, solve,
       builder, serializer, verification and stream operations propagate unchanged
       by object identity, including unexpected ValueError, OSError, MemoryError,
       RecursionError and RuntimeError. No blanket ValueError/Exception catch,
       empty fallback, diagnostics swallowing or operational-error-to-invalid-data
       translation. A normally returned value violating a closed return-type or
       selected-route promise raises RuntimeError; it is not malformed user data.
       A checker rejection remains its ValueError, whether on verify input or solve
       self-check. The CLI cannot infer operational versus semantic provenance from
       that exception's class alone, and makes no new classification claim.
       Under module invocation, SystemExit(main()) maps normal 0/2 to exit status;
       uncaught exceptions retain the interpreter's failing process behavior. No
       exact traceback text or numeric status for interpreter-level failures is
       frozen, beyond non-success on the tested interpreter. The CLI adds no custom
       diagnostics for those exceptions. Do not format enormous integers or echo
       untrusted input in deliberate messages. Interrupts retain native behavior.

    10. Write semantics and resources. A help/usage/solve writer consumes only the
        selected binary stream. On a positive short write, continue with the unwritten
        suffix; return 0/2 only after all required bytes and flush succeed. A normal
        write result must be exact int in 1..remaining bytes; None, bool, zero,
        negative or overlarge counts violate the blocking-stream promise and raise
        RuntimeError. A normal flush must return None, else RuntimeError. Never
        close/rebind process streams, silently fall back to text, retry a failed
        operation, clear an exception or exit through os._exit. Short-write progress
        is not a retry of an exception. Missing .buffer or operational stream errors
        propagate. No stream access at all for a silent successful verify.
        All validation/composition failures before emission leave stdout untouched.
        Once a write starts, an I/O failure can leave a partial prefix; stdout cannot
        be rolled back or promised atomic. Shell redirection is outside CLI ownership.
        No schema/input-byte/digit/multiplicity quota or hidden decimal-conversion
        cutoff is added. This local research entry point assumes user-selected inputs
        and available host resources; it is not suitable as an untrusted service
        boundary without separately disclosed outer ingress/work limits. Never alter
        int_max_str_digits, recursion limits, hash seed or other process settings.
        Read-all input and retained output incur input/output-sized storage, JSON
        decoded storage and exact-integer bit costs. Syntax/codec loops are driven by
        bytes/digits, not expansion of Q copies or enumeration of shores. Additional
        checker scans do not confer a new universal strong-polynomial byte-runtime,
        constant-memory or denial-of-service-protection claim.

    11. Determinism and both selections. Identical bytes, argv and the same solver
        selection produce identical certificate bytes, subject to resources and
        unchanged closed code. Neither output nor acceptance depends on input path,
        optional label spelling, clock, environment metadata or telemetry counters
        except insofar as decoded labels must themselves be valid. Different valid
        instance encodings of the same ordered graph give equal mathematical input;
        certificates contain no labels or path identity. Across selections compare
        exact numerical values by cross-multiplication only after independently
        parsing and recomputing EACH run's literal pair. Do not demand equal witness,
        raw pair or certificate bytes across ties; do not normalize or canonicalize
        witnesses to force equality. Both selections must execute every currently
        registered qualified graph identity, including intentional duplicates, not
        just a hand-picked command demonstration. Source baseline/endpoint witnesses,
        including losing direct H2 candidates, also exercise verify independently;
        no assertion that a strict final H2 winner exists is introduced.

    12. Metadata and future ownership. Resolve 4.13.9's "Unit 19/21" allocation
        explicitly: Unit 19 is the certificate/verification entry point specified
        here; Unit 21 owns experiment timing, externally supplied environment data,
        RunMetadata/RunRecord assembly and the later versioned run-record wire schema.
        Section 9's versioned run-record requirement remains OPEN for that later
        authority, not satisfied or cancelled here. No stats JSON, benchmark timing,
        Git/platform discovery, instance hash or release version enters certificate
        bytes or this CLI. This allocation changes no Unit 16 record or solver API.
        Future commands require future authority; do not pre-adopt their syntax.

    13. Independent expectations, frozen scope and phase boundaries. Phase C fixes
        CLI grammar/help/error/stream expectations and independently derived instance/
        certificate cases before any CLI implementation or consuming test exists.
        Append only docs/ORACLE_CATALOG.md. Its existing 3,312,641-byte historical
        prefix (SHA-256 05255f65148c007278a38df664df5e6ff02db868d63fdafe7d9a016861952840)
        and the older 3,212,040-byte prefix remain exact. Both closed tests already
        protect their own prefixes; no test exception/reopening is granted here.
        Phase D adds only tests/test_cli.py and establishes missing exactfrac.cli
        RED before production. Phase E adds only exactfrac/cli.py under the frozen
        test; Phase F import/source/nonmutation and independent audit belong to its
        GREEN checkpoint. Phase G appends only finite-scoped CONFORMANCE, preserving
        earlier rows. Phase H stages only that CONFORMANCE, cli.py and test_cli.py,
        then exact staged-tree isolation, separate local commit and remote closure.
        All 48 existing files are frozen outside these explicitly scheduled document
        additions; no closed test, producer, checker, configuration or root package
        amendment. If a genuine conflict is found, STOP and report it; do not infer
        permission to weaken an old test. No REVIEW_REQUEST, mandatory second model,
        private-note inspection, new gate, automatic repair/rollback or later-unit work.

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

## Unit 20 authority addendum: MANIFEST transition and future-population safeguards

Status: author-authorized conditions for incorporation into the existing documentation-only
Unit 20 Phase B authority. This addendum does not execute Phase D or create a separate
application, approval, commit, or review gate. It does not, by itself, specify the complete
corpus interface or corpus recipe inventory.

### D20-M1. Exact, phase-limited retirement of the empty MANIFEST pin

The sole authorized amendment to the closed Unit 19 CLI test is deletion of one complete
line from the literal `_FROZEN_SOURCE_HASHES` dictionary in `tests/test_cli.py`:

```python
    'instances/MANIFEST': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
```

The line includes four leading ASCII spaces, the trailing comma, and its single LF
terminator. Its exact UTF-8 byte length, including LF, is **94 bytes**. No substitute
assertion, replacement digest, formatting change, or other test amendment is authorized.

| Identity | Frozen Unit 19 R2 preimage | Required Unit 20 Phase D post-retirement image |
|---|---|---|
| SHA-256 | `ad1fa1ec0912f0067135176490c8af962d1655057aeaa9618e67e0e4b43e3112` | `02a63b0f95000aab30405a979034bdb628e37b69c635094f4cd0e7190796f42d` |
| Bytes | 99,918 | 99,824 |
| Lines | 2,000 | 1,999 |

The signed byte-length difference (postimage minus preimage) is **-94**. In the
hash-authenticated preimage, the removed line is line 521 and occupies the zero-based,
half-open byte interval **[33538, 33632)**. Line number and offset locate the deletion;
they do not replace the full-preimage hash, unique-line check, or exact postimage check.

Let `old` denote the complete authenticated R2 bytes. The mandatory comparison is:

```text
new == old[:33538] + old[33632:]
```

The removed slice must equal the exact line above with its LF, must occur exactly once
in `old`, and must be the `instances/MANIFEST` entry in `_FROZEN_SOURCE_HASHES`.
Require both full hashes, both lengths, and exact equality, not merely AST equivalence.
The Phase D postimage must be rejected if any other byte differs. No newline conversion,
whitespace cleanup, reordering, rename, altered quote style, or reserialization is allowed.

Record and close this exception with the ordinary Phase B documentation authority before
its use. Phase B still changes only `docs/DESIGN.md` and `docs/TEST_PLAN.md`; the test
retains its complete original R2 bytes in Phases B and C. The one-line retirement occurs
only in the normal Unit 20 Phase D tests-first transition, together with the consuming
tests adopted by the complete Unit 20 authority. It does not populate the MANIFEST or
introduce corpus implementation in Phase D. Phase C independently registers expectations;
Phase E remains responsible for the separately authorized corpus implementation/data.

### D20-M2. Everything outside that entry is preserved

`instances/MANIFEST` remains in `_CLOSED_PATHS`; that complete assignment is byte-identical.
The hash-checking loop, all **41** remaining `_FROZEN_SOURCE_HASHES` entries, all CLI
behavioral assertions, imports, embedded reference sources, functions, and classes are
untouched. The original dictionary has 42 entries; only the named entry is retired.
The module AST must equal the original AST with only that dictionary key/value pair
removed, disregarding source-location attributes that shift after the deleted line.
AST equivalence supplements, never substitutes for, byte conservation.

The Unit 19 R2 hash remains the valid historical identity in its original packages,
checkpoints, snapshots, and notes. Do not rewrite those records. The Phase D evidence
records the new post-retirement hash and the explicit relation to the original R2 image.
This authorization does not reopen any other existing test pin, including pins on
source, configuration, release documentation, or other files.

### D20-M3. No premature frozen-hash pins on future-populated artifacts

No new enduring executable frozen-hash pin may be placed on a file that a later scheduled
unit is to populate, extend, regenerate, or replace. This applies in particular to
`instances/MANIFEST`, planned corpus files under `instances/`, experiment outputs, and
other scheduled Unit 21-22 artifacts. Do not recreate the same restriction indirectly
with a directory-tree digest, blanket frozen inventory, permanent empty/absence assertion,
or fixed global membership/count that rejects separately authorized future population.
The exact bytes of a placeholder are not a lasting functional requirement.

Before adopting a new pin, classify the path against the remaining unit schedule. Keep
lifecycle-mutable artifacts out of enduring predecessor-test frozen-hash dictionaries.
Use the owning unit's declared schema, exact membership/order rules for its scoped data,
independently established expected content, reproducibility checks, and adversarial
missing/extra/altered-file checks. These must preserve substantive integrity without
forbidding later authorized work. Merely testing existence is insufficient.

This rule does not ban historical byte-identity records or phase-local authentication.
An immutable prior snapshot/package may retain its hashes, and a controlled operation may
pin its complete preimage and expected postimage. Independently preregistered hashes of
finalized, explicitly immutable versioned corpus payloads remain valid within their
owning scope, provided those exact paths are not scheduled for later population or change.
Such checks must not become a freeze of a mutable aggregate MANIFEST, future output file,
or the entire `instances/` or experiment-output directory across later units.

The same classification and source-intake check applies prospectively in Units 21 and 22.
Any already-existing pin that conflicts with their scheduled work must be surfaced and
resolved under explicit, bounded authority, not silently removed or refreshed. This
addendum authorizes no further legacy-pin retirement and grants no release permission.

## 13. Unit 20 corpus authority — versioned, reproducible initial corpus

Status: remaining documentation-only Unit 20 Phase B authority. This section completes
corpus interface and inventory decisions alongside, not instead of, the preceding
D20-M1--D20-M3 addendum. Its adoption does not perform the authorized Phase D deletion.
The complete preceding document, including that addendum, is preserved byte-for-byte.

### D20-C1. Source boundary and ownership

The governing V2.2 labels are `def:instance`, `ass:active`, `def:parameter`,
`def:complexities`, `lem:aggregation`, `lem:interval`, `prop:expanded-equivalence`,
`lem:empty`, `lem:endpoint-difference`, `prop:endpoints`, and `thm:main`.
They fix mathematical semantics, not a software corpus schema or a benchmark grid.
The API, names, finite grids, seeded support recipe, serialization, and scoped manifest
rules below are new Unit 20 engineering rulings. They are not quotations from the
mathematical source or implementations already completed by a predecessor.

Unit 20 delivers an initial reproducible input corpus, its pure generator, owning tests,
and data-integrity evidence. Unit 21 owns experimental execution, run metadata, timings,
operation/bit-growth observations, comparative campaigns, and result tables. Unit 22
owns release, minimum-interpreter reproduction, privacy/licensing and public-export
checks. Existing experiment and release placeholders are not silently implemented here.
Neither a private paper-planning proposal nor the source's historical 11,503-instance
falsification study becomes an extra Unit 20 deliverable by reference.

### D20-C2. Exact production surface; no filesystem interface

Adopt `exactfrac/corpus.py` and `tests/test_corpus.py`. The production module is a
stdlib-only, deterministic input generator; it is not on the solver's correctness path.
Its `__all__` is exactly the following tuple, in this order:

```python
("build_corpus", "generate_instance", "recipe_ids")

def recipe_ids() -> tuple[str, ...]: ...
def generate_instance(recipe_id: str) -> bytes: ...
def build_corpus() -> tuple[tuple[str, bytes], ...]: ...
```

There are no other public callables, public record/error classes, mutable public
registries, default parameters, keyword-only parameters, or variadic parameters.
`generate_instance` has one positional-or-keyword parameter. It accepts only an exact
built-in `str` equal to one of the 655 IDs in D20-C3; nonmembers and all other types,
including subclasses, raise plain `ValueError`. Reject rather than strip, case-fold,
coerce, normalize, or interpret arbitrary paths. This deliberately finite interface is
not an undocumented general-purpose graph generator.

`recipe_ids` returns the exact tuple of qualified IDs, strictly sorted by ASCII bytes.
`generate_instance` returns the exact instance bytes fixed by its recipe.
`build_corpus` returns an exact tuple of `(relative_path, exact_bytes)` tuples: first
`("MANIFEST", initial_manifest_bytes)`, then every owned payload, sorted by ASCII path.
All returned objects are immutable. There is no generator object, delayed I/O, shared
mutable buffer, or optimizer call. Calling any of these functions performs no filesystem
read/write, environment/clock access, subprocess, network operation, or random-state use.
No `main`, module-entry CLI, installation entry point, writer, reader, or merge API is
adopted. A caller materializes a build only into a fresh destination it owns.

The initial MANIFEST returned by `build_corpus` describes only this suite. It is a
reproduction product for a fresh directory, not permission to overwrite a later aggregate
MANIFEST, drop other suites, or assert whole-file identity against that later aggregate.

### D20-C3. Exhaustive finite recipe inventory and identifiers

The owning suite is `unit20-v1`, with 655 distinct recipe IDs. The five rows below are
ordered here for exposition; the public registry and payload enumeration use ASCII ID
order. Integers in IDs use ordinary decimal without signs; only the indicated fields
are zero-padded. Braces describe substitutions, not literal filename characters.

| Stratum | Exact parameter domain | ID recipe | Count |
| --- | --- | --- | --- |
| Two-vertex micro | q in 1..5; f0,f1 each in 1..q | `edge-q{q:02d}-f{f0:02d}-{f1:02d}` | 55 |
| Three-vertex micro | a,b,c in 0..2; all of a+b,a+c,b+c positive; f0 in 1..a+b, f1 in 1..a+c, f2 in 1..b+c | `tri-q{a}-{b}-{c}-f{f0}-{f1}-{f2}` | 324 |
| Structural | family in path,cycle,complete,bipartite,matching; n in 4,6,8; bits in 1,8; fmode in unit,half,near,degree | `struct-{family}-n{n:02d}-b{bits:05d}-f{fmode}` | 120 |
| Fixed-support bit sweep | same five families; n=4; bits in 1,8,64,256,4096,16384; qmode in flat,ramp; fmode in unit,degree | `bits-{family}-n04-b{bits:05d}-q{qmode}-f{fmode}` | 120 |
| Seeded support | n in 4,6,8; bits in 1,8,64; fmode in half,alternating; seed in 1,73 | `seeded-n{n:02d}-b{bits:05d}-f{fmode}-s{seed:02d}` | 36 |

Counts are 55+324+120+120+36=655, including 379 microinstances. For the triangle
stratum, exactly two positive support slots contribute 90 capacity assignments and
three positive slots contribute 234. Zero slots are omitted from the serialized support.
Repeated mathematical inputs across different recipe IDs are intentional. Do not
deduplicate by payload bytes, graph isomorphism, digest, objective value, or witness.
The prior 400-identity solver/checker registry remains an unchanged historical registry;
these 655 IDs neither replace it nor claim 655 previously unseen mathematical graphs.

The micro edge is `(0,1,q)` with f=(f0,f1). Triangle slots a,b,c mean (0,1), (0,2),
(1,2), respectively; retain only positive slots in that order and use f=(f0,f1,f2).
Micro recipes have no pseudorandom choices. Their exact supplied capacities are not
clamped or repaired. Every other parameter combination or alternate ID spelling is
outside this version's generator domain, even if it would describe a valid graph.

### D20-C4. Support recipes and explicit seed semantics

All vertices are dense indices 0..n-1. All supports are sorted lexicographically by
(u,v), with u<v, before edge_ref-dependent multiplicities are assigned.

- `path`: (i,i+1) for 0<=i<n-1.
- `cycle`: that path plus (0,n-1).
- `complete`: every (u,v) with 0<=u<v<n.
- `bipartite`: every (u,v) with 0<=u<n/2<=v<n; all adopted n are even.
- `matching`: (0,1),(2,3),...,(n-2,n-1). Disconnection is intentional; isolation is not.

The seeded family starts with the cycle support. For each remaining pair u<v, compute
SHA-256 of this exact ASCII message, with LF after every line including the last:

```text
exactfrac-u20-seeded/1
{seed}
{n}
{u}
{v}
```

Here the substitutions are unpadded decimal integers. Include that pair iff the first
digest byte, interpreted as an integer 0..255, is less than 64. This is a fixed,
seed-indexed deterministic recipe, not a claim of independent uniform graph sampling.
It has no resampling loop, entropy source, Python `hash`, or unspecified PRNG algorithm.
Visit candidate pairs in lexicographic order. The cycle backbone guarantees no isolated
vertices; q/f generation occurs after the final canonical support is known.
Structural and bit-sweep recipes have seed 0 by definition, not an unrecorded RNG default.
Micro recipes are explicit. Seed 0 is not an accepted seeded-stratum identifier.

### D20-C5. Multiplicity and capacity recipes

For nonmicro recipes write b=bits and j=edge_ref in the final support. Structural
recipes use flat multiplicities. Bit-sweep recipes use their declared qmode. Seeded
recipes use ramp multiplicities. Set:

```text
flat: q_j = 2^b - 1
ramp: q_j = 2^(b-1) + ((j + seed) mod 2^(b-1))
```

Thus all q_j are positive and have exactly b binary digits, including b=1. The seed
in a bit-sweep ramp is 0. Edge count remains the support-edge count, never Q.
Compute d_q(v) by summing incident q_j once at each endpoint. Then:

```text
unit:        f(v) = 1
half:        f(v) = (d_q(v) + 1) // 2
near:        f(v) = max(1, d_q(v) - 1)
degree:      f(v) = d_q(v)
alternating: f(v) = 1 for even v; d_q(v) for odd v
```

These are input-construction formulas, not changes to Instance validation. Since every
support has positive degree, each formula yields 1<=f(v)<=d_q(v). The names `half`,
`near`, and `alternating` describe those formulas only; do not infer balanced capacities,
uniform sampling, a guaranteed parity mix, or an optimizer execution path from a name.
No multiplicity expansion or iteration over 0..q_j, 0..Q, or 0..f(v) is permitted in
production generation. Output encoding necessarily scales with encoded length; this
module has no strong-polynomiality claim. The bit sweep does not require constant
objective values, identical witnesses, or identical operation counts as bits vary.

### D20-C6. Exact instance-byte contract

Each payload is one `exactfrac-instance/1` object with keys, in order, `format`, `n`,
`edges`, `f`; no labels or extra metadata. Use canonical edge order, compact comma/colon
separators, ordinary ASCII integer tokens (no leading zeros or negative zero), and
exactly one trailing LF. There is no BOM, indentation, comment, alternate numeric
notation, quoted integer, platform newline, or trailing whitespace beyond that LF.
No labels are needed for these recipes; their absence does not narrow the Instance API.

Large integer serialization must work under the interpreter's existing decimal-conversion
limit, including 640 and 4300, without changing that setting. Use a bounded-chunk
integer-to-decimal algorithm, not `str(huge_int)`, formatting a full huge integer, or
`json.dumps` on an object containing huge integers. Every direct decimal conversion is
of at most nine digits. JSON metadata with bounded integers may use the stdlib encoder.
No use of floats, Fraction, decimal, eval, exec, dynamic imports, producer codecs, or
private verifier routines is needed. Imports are restricted to stdlib modules; no
`exactfrac.*`, `exactfrac_verify.*`, tests, catalogue, or private handoff dependency.

### D20-C7. Versioned MANIFEST and immutable owned payload namespace

A payload's path relative to `instances/` is `unit20-v1/{recipe_id}.json`.
The aggregate `instances/MANIFEST` has schema:

```json
{"format":"exactfrac-corpus-manifest/1","entries":[{"suite":"unit20-v1","recipe":"...","path":"unit20-v1/....json","bytes":123,"sha256":"..."}]}
```

The example's ellipses, byte count, and digest are illustrative, not oracle values.
The root has exactly `format` and `entries`. Entries have exactly `suite`, `recipe`,
`path`, `bytes`, `sha256`. Required types are exact dict/list/str/int after a strict JSON
parse; bool is not a byte count. `bytes` is positive; `sha256` is exactly 64 lowercase
hex digits. Root and entry duplicate decoded keys are invalid. Numeric byte counts
are nonnegative ordinary integer tokens, not floats, exponent notation, or strings.

A suite matches `unit[1-9][0-9]*-v[1-9][0-9]*`, with no leading-zero component.
A recipe matches `[a-z0-9]+(?:-[a-z0-9]+)*`. A path equals
`suite + "/" + recipe + ".json"` exactly: no absolute path, `..`, backslash,
empty segment, encoded separator, alternate suffix, or nested directory. Entries are
strictly ascending by ASCII path; paths and (suite,recipe) pairs are unique. The owning
suite has exactly the D20-C3 registry. All its payloads are regular nonexecutable files,
not symlinks or paths reached through symlinked parents.

The generator emits the initial root/entry key order displayed above, compact ASCII
JSON and one LF. Phase C fixes its exact expected bytes independently. This initial
encoding is a historical reproduction identity, not a permanent byte pin on the live
aggregate. A consumer of the evolving aggregate accepts JSON whitespace/key order
variation but rejects invalid schema, duplicate keys, invalid ordering, and duplicate
identity. Its Unit 20 projection must match the independently declared 655 entries and
the exact files in `instances/unit20-v1/`, including hashes and lengths.

The versioned Unit 20 payload paths are finalized by this unit and are not scheduled
for mutation by Units 21--22. New suites or changed datasets use a different namespace;
future work may extend the aggregate MANIFEST or add root-level documentation without
invalidating the Unit 20 projection. Do not assert a global directory digest, global
file count, a fixed aggregate digest, or absence of future suites. Missing, extra,
nested, changed, renamed, or redirected files inside the owned namespace must still
fail. A syntactically valid foreign suite is not a claim of authorization or scientific
validity; its owning unit supplies its expected inventory and substantive checks.

`build_corpus` emits only MANIFEST and the 655 payloads: exactly 656 records for this
isolated build product. It neither reads nor merges any live aggregate. The count is
scoped to its own return value and must never be applied to the entire repository or
to an aggregate MANIFEST after other suites are added.

### D20-C8. Independent oracle registration, not checksum self-certification

Before new consuming tests or production, Phase C adds independently derived tables to
ORACLE_CATALOG. Register every recipe ID, path, instance length/digest, support count,
Q, degree/capacity data or bounded summaries sufficient to cross-check the construction,
and independent exact optimum/Empty status. Huge values use compact unambiguous recipes
in human tables; never a full-token decimal conversion that requires changing limits.
Also preregister exact initial MANIFEST bytes/length/digest and the inventory fingerprint.
The production generator and its generated manifest cannot serve as their own oracle.

Derive support/multiplicity/capacity and expected bytes from this prose using a separate
private implementation. Validate all 655 independently against the active input model.
For all 379 microinstances, enumerate admissible compact count vectors and independently
selected expanded unit-copy subsets (Q<=6), compare to scalar totals and endpoint extrema.
For every recipe, an independent nonempty-shore endpoint enumeration is feasible as a
bounded reference (n<=8); it never enumerates all integer totals for huge multiplicities.
Use `lem:interval` and `lem:endpoint-difference`, not production branch logic. Register
numeric quotient expectations by cross multiplication, not equality of tied raw pairs.
These are prospective finite oracle obligations, not executions claimed in Phase B.

Preregister generator, serialization, scoped-manifest, nonmutation and future-extension
fault families. Include guard-isolated missing/extra/wrong-content/wrong-recipe files,
seed/order changes, altered large-digit chunks, a digest recomputed from wrong payload,
foreign-suite extension, and the D20-M1--M3/U20-TR1--TR5 preservation boundary.

### D20-C9. Verification scope and claim boundary

Every materialized payload is checked against the independent Phase C expectations,
not just the self-emitted manifest; independently parse and validate all 655.
During implementation audit run both closed Standard and Accelerated solvers on all
379 microinstances and on each of these five stress recipes:
`bits-{family}-n04-b16384-qramp-fdegree`, for the five families in D20-C3.
This is 384 inputs and 768 actual solves, separately counted from pytest items.
For each output, independently verify the emitted certificate and compare its attained
value with the registered endpoint optimum. Repeat generation in fresh processes under
both hash seeds 1,73 and both decimal limits 640,4300 without changing either setting.
Record actual work; do not claim the larger structural instances were timed or solved
unless those executions actually occurred. Unit 21 retains the full campaign.

The C0 checker proves admissibility and attainment (or the valid Empty case), not
optimality. Optimality comparisons here come from the separate finite reference.
The source theorem supplies the universal mathematical carrier. A finite corpus neither
proves universal correctness/strong polynomiality nor establishes practical support
limits, favorable wall-clock scaling, application validity, or release readiness.
Neither input strata nor their names promise all branch paths/look-ahead outcomes.
Any such claim requires explicit observed or independently proved coverage later.

### D20-C10. Phase scopes, evolution, and preservation

Phase B now changes only DESIGN/TEST_PLAN; all prior bytes including the approved
addenda remain exact prefixes. Keep both documents unstaged for the ordinary review.
The complete authority, including the addenda, follows ordinary staging/local commit/
regression/push closure. No separate addendum subcommit or extra unit gate is introduced.
Phase C changes only ORACLE_CATALOG under append-only historical protections. The empty
MANIFEST and full original Unit 19 R2 test remain unchanged through Phases B and C.

Phase D introduces only `tests/test_corpus.py` and applies exactly the already-authorized
94-byte deletion in `tests/test_cli.py`; no other predecessor edit is permitted.
The intended initial RED is exactly the missing `exactfrac.corpus` import. No stub is
installed to bypass that RED. Phase E may add only `exactfrac/corpus.py`, the 655 owned
payloads, and `instances/README.md`, and populate `instances/MANIFEST`. The README explains
recipes, fresh-directory reproduction, scoped integrity and claim limits; it is later-
mutable documentation, not an enduring byte pin. Phase F's existing conformance step
appends CONFORMANCE only after the appropriate GREEN/audit evidence. Existing isolation,
local commit, remote closure, and final notes follow without collapsing phases.

Closed solver, telemetry, certificate, checker, CLI, configuration, SPEC_LOCK, CONTRACT,
and other predecessor tests remain frozen. `exactfrac.__init__` stays export-free.
No experiment/result file, CLI command, runtime dependency, LICENSE, release version,
public publication, or existing package/evidence rewrite is authorized here.
Prospective corpus/experiment/output paths must be reviewed under D20-M3 rather than
reintroduced into an enduring frozen-placeholder dictionary. Phase-local before/after
hashes and historical snapshots remain mandatory and distinct from those forbidden pins.

## 14. Unit 21 experiments authority — reproducible measured campaigns

Status: prospective documentation-only Unit 21 Phase B authority. This appendix
preserves every preceding byte. It explicitly activates the experiment ownership
reserved by 4.13.9, 4.16.12 and D20-C1. The older Q4/core scheduling descriptions
in §§1, 3 and 11 remain historical; they do not cancel this scheduled Unit 21.
No experiment has been executed by adopting this authority. The contracts below
are new engineering rulings, not quotations from the mathematical source.

### D21-E1. Source, purpose and limits

The V2.2 labels `def:instance`, `ass:active`, `def:parameter`, `def:complexities`,
`lem:empty` and `thm:main` govern the problem, Empty case and distinction between
operation complexity and bit complexity. DESIGN 4.12–4.16 govern the already
closed solver, telemetry, certificate and checker interfaces. D20-C1–D20-C10
supply the fixed input suite. These sources do not specify a repetition policy,
clock interval, run schema, filesystem protocol or statistical estimator; E2–E16
supply those explicitly. No result changes the active-instance input model.

This unit implements a runner, versioned run records, reproducible tables and
one fully recorded initial campaign. Both Standard and Accelerated are required.
The in-repository exact backend is the only backend. There is no explicit-copy
comparator, external optimizer, alternative backend, new input family, solver
optimization, application-domain benchmark or performance promise. Unit 22 still
owns licensing, release, privacy/public export and minimum-interpreter reproduction.

A timed observation is not an operation count. An observed event count is not a
count of all arithmetic/comparison operations. A measured integer peak is not a
memory measurement. No finite campaign proves strong polynomiality, universal
correctness, asymptotic growth, a practical support-size limit or favorable speedup.
Do not convert a source bound on atomic families into an observed max-flow count.

### D21-E2. Entry point, public boundary and dependency direction

Adopt `exactfrac/experiments.py`, the thin direct-script entry point
`experiments/reproduce.py`, and the consuming test `tests/test_experiments.py`.
The experiment module's `__all__` is exactly `("main",)` and its only public
callable is `main(argv: list[str] | None = None) -> int`. There are no new public
record classes, callbacks, solver selectors, serializers, parsers or merger APIs.
The callable parameter is positional-or-keyword. None means sys.argv[1:]; otherwise
require an exact list of exact built-in strings. Other Python types raise plain
ValueError before filesystem, clock, environment discovery or solver activity.

Module import has no experiment, data access, environment discovery, clock read,
file creation or stdout/stderr side effect. The module uses only the standard
library and closed public ExactFrac APIs. Do not import predecessor test helpers,
CLI private codecs, private handoff code, an oracle catalogue or canonical source
at runtime. The checker remains independent and never imports the runner/solver.

The direct script calls this same main and uses SystemExit for its normal result.
It may arrange the repository root for imports inside its guarded invocation;
it must not silently load a different installed ExactFrac. Code/import origins
are bound as in E8. The script does not duplicate the experiment logic or start
work when imported. No setuptools entry point, dependency or configuration edit
is authorized. Private implementation functions may factor validation and execution;
they are not extra user-facing modes or permission to change the fixed schedule.

### D21-E3. Command grammar and paths

Accepted invocations, and no others, are:

```text
python experiments/reproduce.py --help
python experiments/reproduce.py --all [--instances PATH] [--output PATH]
```

The --all token occurs exactly once, first. Each optional flag occurs at most
once, in either order, and has one nonempty operand not beginning with '-'.
NUL, unknown flags, '--flag=value', positional extras, missing operands and
combining help with other tokens are usage errors. A syntactically invalid argv
writes a fixed, non-input-echoing usage message to stderr and returns 2, with no
input/output path access or dependencies invoked. Help writes the grammar and
brief scope to stdout and returns 0 without starting validation or discovery.
Normal successful --all is silent and returns 0 only after completion in E12.
Binary writes must complete positive short writes and flush; normal invalid
write counts/flush returns raise RuntimeError. I/O exceptions propagate unchanged.
Neither process standard stream is closed or rebound.

Default instances is <source-root>/instances. Default output is
<source-root>/results/unit21-v1. Source-root is the root containing the imported
exactfrac source and the direct-script entry point, not the working directory.
Explicit relative operands are interpreted against the caller's working directory.
Resolve relative components lexically, rejecting '..' rather than following it;
reject symlinked existing components, including an existing leaf symlink. Do not
silently replace user paths by realpath targets. The source-root and input root
must be real directories; the output leaf must not exist, even if empty. A fresh
output may be inside the source tree only under its `results/` subtree and never
inside inputs, .git, source or tests. It may also be a disjoint external directory.
Reject overlapping output/input trees and any output ancestor of the source tree.
Missing output parents may be created only after input validation; existing parents
are never chmodded, removed or replaced. See E12 for safe creation and failures.

--all means the exact unit21-v1 campaign below, not arbitrary current/future suites
or every file under instances. There is no single-instance, resume, append, force,
timeout, randomization, seed override, repeat-count or adaptive stopping option.
Do not give a truncated subset the same campaign-complete identity.

### D21-E4. Input ownership, parsing and integrity

Consume all 655 Unit 20 recipe identities, including numerical/byte duplicates,
in the ASCII order of closed recipe_ids(). The closed build_corpus() supplies the
owned initial records and generator identity, not a new mathematical reference.
Before any solve or output creation, strictly validate the evolving aggregate
instances/MANIFEST against D20-C7. Reject duplicate decoded JSON keys, invalid
numeric tokens/types, noncanonical suite/recipe/path identifiers, reordered or
duplicate entries and invalid lengths/hashes. Do not freeze its whole-file hash
or whitespace/key order. Syntactically valid foreign entries are ignored for
this campaign and are not opened, deleted, run or certified by this consumer.

Require exactly the registered Unit 20 projection and exactly its 655 regular,
nonexecutable, nonsymlink payloads in instances/unit20-v1/, with no extra, nested,
missing or redirected owned files. Read each payload, require its length/hash
and exact bytes equal the corresponding closed build record, and bind that same
retained byte buffer to Instance construction and certificate verification.
Do not validate one file then silently solve a subsequently different reread.
Closed generator inventory/return-type inconsistency is RuntimeError; malformed
external aggregate or mismatching owned input bytes are plain ValueError.

Decode input integers by bounded decimal chunks, without changing interpreter
integer-string limits. Reject floats, exponent notation, negative zero and duplicate
keys. Delegate graph/active schema validation to public Instance.from_dict after
syntax decoding; do not aggregate, reorder or repair external input. Its dependency
exceptions retain their classes/objects. Valid Empty input remains a successful
mathematical case, never an input rejection. No copy expansion or shore enumeration
belongs to this runner. Recheck consumed inputs and source identities before the
completion marker; detected drift invalidates the attempt without rollback.
These checks assume a local user-owned filesystem, not hostile concurrent kernel
or interpreter replacement; they do not promise a filesystem snapshot transaction.

### D21-E5. Finite schedule, warmup and repetitions

Campaign name is `unit21-v1`. For each recipe with zero-based index i in the fixed
655-ID list, process round r=-1,0,1,2 in that order. Round -1 is one un-timed,
telemetry-enabled warmup per route; rounds 0,1,2 are three separately timed,
telemetry-enabled samples per route. In a round execute Standard then Accelerated
when (i+r) is even, otherwise Accelerated then Standard. The ordering is deterministic,
not random sampling, and must be retained in the raw records.

A complete campaign has 1,310 warmup solves, 3,930 measured solves and 5,240 total
calls to solve_with_telemetry. Every call produces a separately verified certificate;
there are 5,240 checker invocations for those calls. Extra independent audit solves
must be labeled and counted separately, never incorporated as measured samples.
No repeat may be reused from a cache. Do not deduplicate 599 distinct payloads in
place of 655 design identities, omit Empty cases, stop when values agree, tune the
repetition count from observed speed, or discard a slow/outlying observation.

Execution is synchronous, serial and in one invocation process. There is no worker
pool, CPU affinity change, garbage-collector change, recursion/decimal-limit change
or warm-start state installed on closed objects. This design does not promise
cold-cache timing or equality of machine conditions. Available host resources and
native interruption govern runtime; lack of an internal timeout is disclosed.
A failed or interrupted attempt is incomplete, not a completed censored campaign.
Any later censoring/time-budget policy requires separate prior authority.

### D21-E6. Timing interval and environment

For each measured sample, call time.perf_counter_ns immediately before the one
solve_with_telemetry(instance, route) call and immediately after its normal return.
Require exact integer readings and nonnegative end-start; violated clock promises
are RuntimeError. Dependency/clock exceptions propagate unchanged. Store elapsed_ns
as that exact integer difference. Set RunMetadata.wall_clock_s to
elapsed_ns / 1_000_000_000, a finite nonnegative diagnostic float. This conversion
is explicitly outside solver arithmetic and is never used for rational comparisons,
counters, peak measurements, ordering decisions or completion decisions.

The interval includes wrapper validation, recording, global solve, and construction
of its returned telemetry. It excludes input loading/decoding/Instance construction,
metadata discovery, certificate construction/checking/serialization, output I/O,
source/inventory hashing and report aggregation. Unit 16's integer-observation
interval is narrower at its boundaries and remains unchanged. Do not call this
uninstrumented solver time, whole-command time, verifier time or backend-only time.
Warmups make no clock calls: elapsed_ns and wall_clock_s are null, not fake zero.
A measured zero-nanosecond reading is retained as zero, not silently replaced.

Discover once per invocation: platform.python_version(), platform.platform(), and
platform.processor() or None when empty; require exact nonempty strings where the
closed RunMetadata contract requires them. Record timing clock name, monotonic flag,
adjustable flag and supplied finite positive resolution from time.get_clock_info
for perf_counter. Record sys.get_int_max_str_digits(), sys.getrecursionlimit(),
and the PYTHONHASHSEED environment value or null as observations, not settings to
change. Do not gather username, hostname, home path, credentials, full environment,
Git remotes or private handoff paths. Unknown CPU remains null. No network request.
Code identity is E8's content fingerprint, not an invented Git commit or dirty-tree
claim. The initial campaign may run before its final commit; record this truthfully.

### D21-E7. Exact result, repeated route and dependency checks

Each call is exactly solve_with_telemetry, not solve followed by a second run to
recover counters. Require its normal response to have the exact tuple/record types
and correct route under the closed contract; inconsistent returned promises raise
RuntimeError. Assemble an actual RunRecord(AlgorithmStats, RunMetadata) for the call.
Preserve every total, nonbranch, per-branch and native field without recounting,
renaming native semantics, sum-of-peaks errors, counter zero-filling or extra
arithmetic inserted into the measured solver path.

Build and serialize a certificate using the closed public functions. Require their
normal return types and require verify_certificate(retained_input_bytes, cert_bytes)
to return None. Verify every warmup and measured sample before writing its successful
row. Propagate checker exceptions; do not turn them into skipped rows or a success flag.
For each recipe/route, require exact same-route result, AlgorithmStats and certificate
bytes on all repeats, using its warmup as the reference. Across the two routes require
numerical equality by positive-denominator cross multiplication; do not require tied
witness, raw pair, certificate bytes or AlgorithmStats equality across routes.

Rows record literal N,D through their certificate and native attaining_candidate.
The runner reports checker-accepted attainment and cross-route agreement, not an
independently proved optimum. Its separate Phase E audit compares every recipe's
reported values with independently fixed Phase C expectations. A C0 checker alone
is not an optimality oracle, and a passing pair of solvers is not self-certification.

### D21-E8. Content identity and import origins

At invocation before solving, fingerprint this fixed source set: every .py path
under exactfrac/ or exactfrac_verify/ in the closed Unit 20 708-file tree, plus
exactfrac/experiments.py and experiments/reproduce.py. The exact path list is the following; Phase C independently checks it against
the committed manifest. Do not expand it by runtime filesystem glob, omit a losing
branch module or include future unrelated modules, tests, mutable docs, .venv,
aggregate inputs or result directories.

```text
exactfrac/__init__.py
exactfrac/_telemetry.py
exactfrac/branch.py
exactfrac/certificate.py
exactfrac/cli.py
exactfrac/corpus.py
exactfrac/families.py
exactfrac/flow.py
exactfrac/instance.py
exactfrac/oracle.py
exactfrac/parity_cut.py
exactfrac/rational.py
exactfrac/shore.py
exactfrac/sign_routing.py
exactfrac/solve.py
exactfrac/telemetry.py
exactfrac/witness.py
exactfrac_verify/__init__.py
exactfrac_verify/brute.py
exactfrac_verify/check.py
exactfrac/experiments.py
experiments/reproduce.py
```
Every selected file is regular, nonexecutable and reached without symlinked parents.

For ASCII-sorted relative paths p with lowercase SHA-256 h(p), fingerprint bytes
are ASCII `exactfrac-unit21-source/1\n` followed by `p + "\0" + h(p) + "\n"`
for each path. Let H be their SHA-256. RunMetadata.code_version is exactly
`exactfrac-source-sha256:` followed by H. run-info.json stores the ordered path/hash
entries and this fingerprint, allowing a later audit to associate it with a Git tree.
It must not hash the results into their own source identity or depend on an absolute
machine path. Changing only a permitted output location cannot change this identity.

Every loaded exactfrac/exactfrac_verify module must originate at its expected
source-root path, with bytes matching the recorded entry. Reject conflicting already
loaded modules rather than mixing a local runner and installed solver. Arrange and
restore any runner-controlled sys.path change in finally. In the controlled gate use
isolated Python and disable bytecode writes. No editable install or filesystem search
for private build evidence is part of runtime. Recheck all source files and origins
before completion; runtime/malicious-loader security is outside this local-tool claim.

### D21-E9. Versioned run-record wire contract

Each UTF-8/ASCII JSON line in warmups.jsonl or runs.jsonl has exactly these keys:
`format`, `campaign`, `recipe`, `solver`, `phase`, `repeat`, `input`, `certificate`,
`elapsed_ns`, `record`. format is `exactfrac-run/1`, campaign is `unit21-v1`, solver
is Standard or Accelerated. phase is warmup or measured. repeat is 0 for warmup,
and 0,1,2 for the measured round. Raw row order is the invocation order of E5,
filtered by phase; it is not reordered into the comparison-table order.

input has exactly `suite`, `path`, `bytes`, `sha256`, `n`, `m`, `Q_bits`,
`max_q_bits`, `max_f_bits`, `input_integer_bits_sum`. suite/path/bytes/hash identify
the retained Unit 20 input. Define bits(x)=max(1,abs(x).bit_length()). Q_bits=bits(Q),
max_q_bits=max bits(q), max_f_bits=max bits(f). input_integer_bits_sum is
bits(n)+bits(m)+sum over edges of (bits(u)+bits(v)+bits(q))+sum over vertices bits(f).
This is a disclosed scalar encoding proxy, not exactly the source's binary encoding
length including framing, JSON bytes, memory consumption or number of copies Q.

certificate has exactly `path`, `bytes`, `sha256`, with relative output path
`certificates/{recipe}.{solver}.json`. One certificate file per recipe/route is
written from its verified warmup and every later call must match it. record has
exactly `algorithm`, `metadata`, the structural projection of the actual RunRecord.
metadata has exactly the six RunMetadata dataclass fields; its instance hash and
code_version must bind to input and E8. elapsed_ns is null only for warmup.

algorithm has exactly `native`, `total`, `nonbranch`, `branches`,
`output_numerator_bits`, `output_denominator_bits`. Each work object has all 25
WorkStats fields of 4.13.3, with exact nonnegative integer values and unchanged names.
branches is [] for Empty, otherwise the ordered four objects with exactly `branch`,
`feasible`, `work`; feasible is a JSON boolean. native has exactly branch_solver,
branch_stats, attaining_candidate from SolveStats. Each native branch object has
all fields of its selected StandardBranchStats or AcceleratedBranchStats record;
its oracle_stats has all seven BranchOracleStats dataclass fields. Computed properties
are not additional serialized keys: max_flow_calls already exists in WorkStats;
branch_solver/attaining_branch properties do not duplicate native data. Tuples become
JSON arrays; records become objects without Python type/repr/address strings. The
exact nested field-name registry is fixed independently in Phase C, not inferred from
future runner output. Native route differences are retained, not coerced into fake
uniform branch records.

Generated JSON uses recursively ASCII-sorted object keys, compact separators,
ensure_ascii string escaping, lowercase boolean/null tokens and exactly one LF.
All integers, including enormous native peaks and counts, are ordinary canonical
decimal integer tokens emitted via bounded chunks; never floats or quoted numbers.
Finite environmental floats use the standard JSON finite-number spelling on the
recorded interpreter and are not cross-version byte invariants. Reject NaN/infinity.
No full-token huge-int str/repr/json conversion and no global digit-limit relaxation.
No new public run-record decoder is adopted; test/audit consumers independently
parse and challenge this schema, including duplicate keys and binding mismatches.

### D21-E10. Reports and their exact derivation

The completed output owns run-info.json, warmups.jsonl, runs.jsonl, summary.csv,
branches.csv, comparison.csv, COMPLETE.json and E9's certificate files only.
CSV is ASCII, comma-separated, one header, LF rows, no index column, blank records
or comment preamble. Fields here need no quoting; all integer fields use canonical
bounded-chunk decimal spelling. Timings in tables are integer nanoseconds, not rounded
seconds or a ratio of rounded floats. Let W be the ordered 25 WorkStats names in
4.13.3. Header expansion below is literal, not an extra W column.

summary.csv has 1,310 rows in ASCII recipe order, Standard then Accelerated:
`recipe,solver,n,m,Q_bits,max_q_bits,max_f_bits,input_integer_bits_sum,repeat_count,median_solve_ns,attaining_candidate,`
then W, then `output_numerator_bits,output_denominator_bits`.
repeat_count=3. median_solve_ns is the middle of exactly the three measured elapsed_ns
values for that recipe/route. All diagnostics come from that route's repeated-identical
AlgorithmStats.total, not the sum across trials, just the winner branch, or a theorem
upper bound. Do not pool recipes or multiple machines into a single median.

branches.csv uses `recipe,solver,branch,feasible,` then W, in recipe/route/branch order;
feasible is literal true/false. It has four rows per nonempty recipe/route and zero
for Empty. It reports each actual branch record, including infeasible branches, and
no fictitious nonbranch row. Raw JSON retains nonbranch separately. For the known
654 nonempty recipes this is 5,232 branch rows, to be checked by the independent audit,
not inferred as a substitute for observing which calls returned Empty.

comparison.csv has 655 recipe rows with header:
`recipe,standard_median_solve_ns,accelerated_median_solve_ns,standard_oracle_calls,accelerated_oracle_calls,standard_max_flow_calls,accelerated_max_flow_calls,standard_peak_integer_bits,accelerated_peak_integer_bits`.
Each entry is a direct join of its summary rows. There is no chosen winner, speedup
claim, smoothed trend, significance test, confidence interval or fitted asymptotic
model in this initial table generator. Raw timing scatter remains available.

run-info.json has exactly `format`, `campaign`, `protocol`, `environment`, `source`,
`inputs`. format is `exactfrac-experiment-info/1`. Nested keys are fixed here:

- protocol: routes=["Standard","Accelerated"], recipe_order="ascii", warmups=1,
  measured_repeats=3, route_order="standard-first-iff-(recipe-index+round)-even",
  warmup_round=-1, measured_rounds=[0,1,2], execution="serial-single-process",
  telemetry=true, timeout_ns=null, timing_interval="solve-with-telemetry-return",
  timing_excludes=["input","metadata","certificates","verification","serialization","output"].
- environment: python_version, platform, cpu from E6; clock is an object with
  exactly name="perf_counter_ns", monotonic, adjustable, resolution_s; the last
  three come from E6's clock_info (booleans and finite positive float). Other keys
  are int_max_str_digits (integer), recursion_limit (integer), hash_seed (string
  or null). No extra host identifiers or free-form path-bearing command line.
- source: entries=[{"path":p,"sha256":h(p)},...] in E8 order,
  sha256=H, code_version="exactfrac-source-sha256:"+H.
- inputs: suite="unit20-v1", recipes=655, manifest_sha256 is the hash of the
  actually read aggregate bytes. That hash is observation provenance, not a
  whole-aggregate acceptance pin. Owned byte identities are in each raw row.

All property names are literal. Discovered strings, clock readings and resolution
are actual environmental data. No successful timing values, operating-system names,
or speed estimates may be invented in fixtures; fake-clock examples are labeled
synthetic. Phase C derives concrete expected bytes from these fixed schemas.

### D21-E11. Failure classification and interruption

Reject invalid argv types or malformed caller-controlled data with plain ValueError
at this new public boundary, except exceptions raised by closed Instance/checker
boundaries, which are propagated unchanged. Usage grammar failures alone return 2.
Contradictory normal closed-dependency returns, mismatched repeated/cross-route
results, invalid clock returns, source/input drift and internally inconsistent
report construction raise RuntimeError. No broad catch translating all exceptions,
retrying a failed solve, swallowing interrupts or manufacturing absent stats is allowed.
Missing files/permissions/storage failures retain native OSError subclasses. The
new runner must not turn a failure into an Empty certificate or encode failed work
as a zero-duration successful row. Failed solves have no complete AlgorithmStats.

Positive short writes are completed; a failed write is not retried. MemoryError,
RecursionError and KeyboardInterrupt propagate. A process killed externally may
leave files but cannot legitimately be treated as a completed attempt without E12.
No user-friendly error string may stringify huge mathematical integers or echo
untrusted input bytes. No hidden solver resource quotas, tolerance, Fraction/gcd
normalization or monkeypatching of closed algorithm logic is introduced.

### D21-E12. Output transaction boundary and completion marker

Validate input inventory, source origins, arguments and output disjointness before
creating output. Create the new leaf exclusively; never reuse an existing directory,
follow a symlink, merge, truncate an old report, replace a file, or clean a failed run.
Use exclusive creation for owned files and explicit checked binary writes/flushes.
Create only the output path's missing parents and certificates/ below its new leaf.
Where parent/leaf identities can be checked, detect redirection; do not describe
lstat checks alone as defeating every hostile race. A local writable directory is
a stated prerequisite. Every failure preserves the observable partial attempt.

Write the info and raw rows in their specified order and retain the verified
certificates. The table builder derives all three CSVs from the completed raw
measured records, validating field and binding consistency, not from a second
solver campaign. Flush and close every owned output before completion. Re-read
and validate exact output membership, all row identities/counts, actual hashes,
certificate bindings and table derivations, and recheck inputs and source files.
Only after all checks succeed write COMPLETE.json last via exclusive creation.
Its format is `exactfrac-experiment-complete/1`; its exact fields are format,
campaign, source_sha256, recipes, warmup_solves, measured_solves, checked_certificates,
files. Values are bound to the observed complete E5 execution, not literal success
counters emitted without evidence. files is an ASCII-path-sorted list of objects
with exactly path, bytes, sha256 for every owned output file except COMPLETE.json.
It includes no self-hash, absolute paths or unrelated files.

A parseable, schema-valid marker with an exact matching ledger is necessary, not
proof against deliberate fabrication; Phase E independently audits the run. A missing,
truncated or inconsistent marker is incomplete. Flush/close failure on the marker
still makes the invocation fail; it is not claimed durable against power loss or
atomic publication to concurrent readers. Completion means the successful return
plus validated output, not simply existence of a filename. No automatic rollback.
An alternate fresh --output is the way to rerun; there is no overwrite/resume mode.

### D21-E13. Independent fixture and test obligations

Phase C appends independently derived human tables for the E5 schedule/counts,
E8 source path list, E9 nested field registry, E10 info schemas/constant strings and
small synthetic run records/table bytes. Include deliberately differing valid tied
raw pairs across routes; same-route determinism controls; real Empty and nonempty
known-answer inputs; synthetic nonzero accepted/rejected/terminal look-ahead work;
peaks aggregated by maximum, event counts by sum, and native Standard/Accelerated
differences. Scripted dependency and clock responses are test data, never real runs.
Preregister guard-isolated faults before writing the consumer/producer. Obtain
mathematical expected values independently; reuse the meaning of existing registered
Unit 20 oracle expectations without rerunning a solver to define its own answer.
No future experiment runner output supplies its own schema or reference table.

Tests may exercise private seams using controlled dependencies, filesystem scratch,
synthetic clocks and a finite independently declared small subset. An injected test
schedule is not a public subset mode. Tests that monkeypatch a dependency restore it;
no monkeypatch is installed by production. The inherited regression must not execute
the 5,240-call campaign on every test run. Test full schedule enumeration with scripted
calls and separately execute both closed routes on registered small actual cases.
Report synthetic and real calls distinctly. Live new collected case count is measured.

### D21-E14. Phase E campaign and independent implementation audit

Within the existing implementation GREEN/audit phase, test source and consumer
contracts before the initial real campaign. Run --all once against the authenticated
Unit 20 inputs to a fresh results/unit21-v1 using the exact candidate sources and
pinned development interpreter. Record its actual environment, provenance, all
observations and failure status honestly. Never supply generated container timings
as the user's live results. A partial real attempt cannot satisfy complete GREEN;
preserve it and issue a controlled continuation without rewriting history.

The independent audit is separate from the production writer and reads its outputs.
It must rederive all table rows from raw records, recompute hashes/identities,
verify every stored certificate with the independent checker and match all 655
reported values to independently registered optimum/Empty expectations. Preregister
those expected quotients/compact recipes during Phase C from existing independent
source definitions, not measured producer values. Witnesses across routes may differ.
Check repeat determinism, actual solver/checker invocation accounting, source and
input binding, totals/branch/native relationships and all declared mutation controls.
Do not call a trace scripted inside a unit test an executed campaign observation.

The fixed-schedule campaign can occur on the dirty implementation candidate because
E8 identifies actual source content, not a nonexistent final commit. GREEN records
its exact artifact hashes. Subsequent staged isolation and postcommit tests conserve
those historical output bytes and validate them; they do not rerun real timings to
force byte equality. Repeat campaigns in other fresh destinations may differ in
environment/timing while matching deterministic results/stats/source identities.

### D21-E15. Scope, path classification and non-reopening

Phase B changes only docs/DESIGN.md and docs/TEST_PLAN.md by appending this authority.
Phase C changes only docs/ORACLE_CATALOG.md by independent registration. Phase D adds
only tests/test_experiments.py. Its first import is exactfrac.experiments; before
source exists require ModuleNotFoundError naming that module, exit 2, one collection
error, zero new cases executed. No dummy module, output directory or predecessor-test
retirement is allowed. The inherited 4,512 cases and existing warning remain intact.

Phase E source scope is exactfrac/experiments.py, experiments/reproduce.py and
experiments/README.md. Its observed campaign output scope is the exact E9–E12
results/unit21-v1 tree, captured in a live manifest after successful execution.
Dynamic measured output bytes are evidence, not predictable constants. The phase
may create missing experiments/ and results/ parents but owns neither parent as a
permanently closed aggregate. No other production, test, input, README, packaging,
dependency, CLI, LICENSE, SPEC_LOCK or CONTRACT change is authorized.

Closed code, tests and Unit20 owned inputs remain byte-immutable. Do not repair the
known pytest parametrization warning in this authority or its implementation. The
aggregate input MANIFEST and instances/README.md remain later-extensible under D20-M3
but this unit reads, never modifies them. A completed results/unit21-v1 is a historical
owned run; additional campaigns use new destinations/namespaces. No permanent pin on
the entire results/ tree, experiments/ directory or future release-owned artifacts.
Source fingerprints and phase-local conservation manifests are not blanket future
source/repository freezes. No public release or privacy review is asserted here.

### D21-E16. Completion and claims

Follow the same A–H lifecycle without an extra review service, audit approval gate,
background job or intermediate code commit. Authority and oracle fixtures each
close remotely before tests. GREEN requires finite tests, inherited regression,
live Ruff, full observed initial campaign and independent audit. Phase G preserves
all prior conformance bytes and records exactly the tested/observed engineering
scope, separating schema tests, scientific reference comparisons and actual timings.
No theorem-row promotion follows merely from table generation.

Stage the exact code/test/docs/observed-output candidate, isolate the index tree,
run targeted/full tests and Ruff with authenticated imports, commit that same tree,
rerun postcommit checks, then push and remotely close. Prior measured artifacts
remain unchanged through these transitions; closure does not mean an additional
timing campaign ran. Private BUILD/LEARNING notes are delivered only after full
remote closure and are never created, located or hashed by build helpers.

---

## 15. Unit 21B authority — separately registered irregular-instance follow-up

This section is prospective authority for Unit 21B only. It follows the remotely
closed Unit 21 implementation `df30e1a36d123e1da025097c99f327871f1a97a6` and its
recorded successful Unit 21B Phase A. The author accepted the amendment review
and superseding Part II brief on September 22, 2026, and separately authorized
the single configuration-pin replacement in D21B-I2. Earlier document bytes and
Unit 21's historical authority remain intact. This adoption does not date F7,
claim a pilot ran, or authorize a main campaign before the pilot/author freeze.

### D21B-I1. Purpose, source boundary and affirmative ownership

The canonical V2.2 source remains the archive with SHA-256
`400c4e23a7683571f7181b98bc009954d431f4ac355a247fb22327a609b4f9ce`.
Its `def:instance`, `ass:active`, `def:parameter`, `lem:interval`,
`lem:endpoint-difference`, `prop:endpoints`, `lem:empty`, and `thm:main` govern
mathematics. The active regime, individually selectable positive integer
multiplicities, raw-pair semantics, both closed solvers, and independent C0
checker are unchanged. This section defines a new finite input family and its
experiment, not a solver, theorem, backend, or release.

Affirmatively extend the layout in section 3 with these sibling modules:
`exactfrac/corpus_irregular.py`, `exactfrac/experiments_irregular.py`, and
`experiments/reproduce_irregular.py`; consuming tests are
`tests/test_corpus_irregular.py` and `tests/test_experiments_irregular.py`.
The generator owns suite `unit21-v2` under `instances/unit21-v2/`. Recipe IDs
start `irregular-`. Designated outputs are `results/unit21-v2-pilot/` and
`results/unit21-v2/`. The old proposed `irregular-v1` suite and `irregular-pilot`
output name are not alternate supported namespaces.

`results/unit21-v1/` is historical, byte-frozen evidence, reported first. Never
rerun, retime, edit, replace, or mix it with follow-up samples. Disclose in the
paper: the 21B stratum was designed after observing that `unit21-v1` produced
Accelerated look-ahead events on six seeded recipes and none on the structural
or bit-sweep strata. All follow-up results, including null, unfavorable, and
untestable outcomes, are retained and labeled as follow-up results.

### D21B-I2. Exact predecessor exceptions and phase ownership

Phase B appends this section to DESIGN and the matching obligations/completion
section to TEST_PLAN. Its only other two changes are the author's coupled
configuration/test exception:

1. Append exactly these ASCII bytes to the original `pyproject.toml`:
   `\n[tool.ruff.lint.isort]\nknown-first-party = ["exactfrac", "exactfrac_verify"]\n`.
   The preimage is 879 bytes, SHA-256
   `89977766c002fd79f1c75de93621062b4e7a042debe95ab9d238987fc9469da6`;
   the postimage is 957 bytes, SHA-256
   `13d5e442582c14e278f726cc3e5d9fecdff5a0cba224e53313a3a8cfc1a4812b`.
   There is no dependency, packaging, pytest, rule-selection, line-length,
   version, or other configuration change.
2. In `tests/test_cli.py::_FROZEN_SOURCE_HASHES`, replace only the 64 hexadecimal
   characters of the `pyproject.toml` value, old digest above to new digest above.
   Test preimage SHA-256 is
   `02a63b0f95000aab30405a979034bdb628e37b69c635094f4cd0e7190796f42d`;
   postimage SHA-256 is
   `6edf3930b3a5db998aea9a1e769b14b5af5046edd996a8b3e42022ef4d7545f0`.
   Both are 99,824 bytes. Preserve every other test byte, every other pin and
   all assertions. This is not a pin retirement or a standing amendment budget.

This explicitly supersedes the otherwise blanket closed-test freeze for this
one value only. Ruff first-party declaration is the selected policy; no standing
RED-to-GREEN import-regrouping exception is adopted. Runtime solver code never
reads this development-lint setting. Repository-context preflight and full Ruff
must still pass; no automatic formatter or `--fix` is allowed.

Phase C appends only ORACLE_CATALOG; it may hold independently derived companion
files privately. Phase D adds only the two new tests. Phase E preserves those
exact tests and creates the three sibling modules, all 1,200 owned payloads,
`experiments/README_irregular.md`, and the aggregate MANIFEST extension. It also
appends an explanatory owning-suite paragraph to `instances/README.md`, preserving
its old prefix. The separate new experiment README avoids editing the old one.
Pilot/main output files are subsequently created by their actual invocations,
not shipped as supposedly observed Mac results. Phase G appends only CONFORMANCE.
H stages the complete authorized candidate, isolates, commits, and closes remotely.

Other closed source/tests/configuration, SPEC_LOCK, CONTRACT, existing payloads,
and all historical results remain byte-frozen. Phase-local manifests bind current
bytes without imposing enduring whole-directory or aggregate MANIFEST pins.
Future release paths remain prospective, not asserted absent forever.

### D21B-I3. Pure finite generator surface and inventory

The generator has exactly the D20-C2 surface and parameter kinds:

```python
__all__ = ("build_corpus", "generate_instance", "recipe_ids")
def recipe_ids() -> tuple[str, ...]: ...
def generate_instance(recipe_id: str) -> bytes: ...
def build_corpus() -> tuple[tuple[str, bytes], ...]: ...
```

It has no other public callable/class, no filesystem interface or executable
module entry. `generate_instance` accepts only an exact built-in str in this
version's finite registry; all other values/types raise plain ValueError without
coercion or repair. Immutable return types, import purity and no environment,
clock, random-state, network, subprocess or file access follow D20-C2. Imports
are stdlib-only; no producer, verifier, test, oracle catalogue or private helper
is imported. No deferred generation, mutable public registry, or shared buffer.

The inventory is the Cartesian product of n=(6,8,12,16), tau=(64,128),
b=(1,8,64), mode=(alternating,random), and seed tokens s01 through s20 for main
or p01 through p05 for pilot. Each token includes its letter and two digits;
p01 and s01 are different domains. There are 48 cells, 960 main recipes and
240 pilot recipes, all retained even when payloads coincide.

IDs are exactly `irregular-n{n:02d}-t{tau:03d}-b{b:05d}-f{mode}-{seed_token}`.
For example `irregular-n06-t064-b00001-falternating-p01` is an ID spelling,
not an observed graph or result. A cell ID is that ID without its final seed
suffix. Public registry and payload order are strict ASCII ID order. Pilot and
main schedules filter this same registry by seed letter and reindex separately.
No extra spelling, leading sign, case variant, stripped whitespace or seed is
accepted. No deduplication by bytes, isomorphism, digest, value or witness.

### D21B-I4. Deterministic support, q, f and matched magnitude series

Vertices are 0..n-1. Start with the path edges (i,i+1) and (0,n-1), giving a
cycle spine. Visit all remaining unordered pairs (u,v), u<v, lexicographically.
Let `H(lines)` mean SHA-256 of the ASCII lines joined by LF with one LF after
the last line. Integer substitutions in messages are unpadded decimal. The
first line of every message is `exactfrac-u21b-irregular/1`.

For support the subsequent lines are, in exact order:
`support`, seed_token, n, u, v. Include a nonspine pair iff digest[0] < tau.
Do not hash the spine to decide inclusion. This digest excludes b, tau and
mode: matched magnitude series keep the same support; the two thresholds are
nested and the two modes share support for a fixed n/seed. These dependencies
are intentional, not independent random replicates. The digest recipe is not
a guarantee of uniform graph sampling or look-ahead reachability.

Sort final support pairs lexicographically before assigning edge references.
For each included pair the multiplicity message after the common tag is:
`multiplicity`, seed_token, n, tau, mode, u, v. Let Z be the unsigned big-endian
integer of all 32 digest bytes and set q(u,v)=1+(Z mod 2^b). The message excludes
b, so the series uses the same digest with the stated truncation at each b.
Here 1<=q<=2^b. b is an upper exponent, not exact bit length; an attained 2^b
has b+1 bits. Always retain the actual `max_q_bits` alongside b.

Compute d_q(v) as the incident multiplicity sum. Alternating mode sets f(v)=1
for even v and f(v)=d_q(v) for odd v. Random mode uses a capacity digest whose
lines after the tag are `capacity`, seed_token, n, tau, `random`, v. Let Z_v
be its full unsigned big-endian digest integer and set f(v)=1+(Z_v mod d_q(v)).
It excludes b; its modulus is the degree at that magnitude. Modulo reduction is
the declared deterministic recipe, not a promise of uniform independent f.
The spine implies positive degrees and 1<=f<=d_q. No resampling, clamp, PRNG,
Python hash, iteration over multiplicity magnitudes or copy expansion.

### D21B-I5. Exact input bytes and extensible aggregate

Each payload uses D20-C6's exact `exactfrac-instance/1` object: keys format,n,
edges,f in that order, canonical sorted (u,v,q) edges, no labels or extra
metadata, compact ASCII separators and one trailing LF. Use a separate
bounded-chunk integer codec with direct decimal conversions of at most nine
digits; no change to interpreter limits and no solver arithmetic floats.

`build_corpus()` returns 1,201 records: first ("MANIFEST", own_manifest_bytes),
then the 1,200 ("unit21-v2/"+ID+".json", payload) records in ASCII path order.
Its MANIFEST contains only its own suite using exactly D20-C7 schema and canonical
initial encoding. It never reads or overwrites the shared aggregate.

The Phase E materializer appends the new suite's independently fixed entries
to the valid existing aggregate, keeping every existing entry's values and
relative order and the exact Unit 20 payload bytes. New entries must follow
D20-C7 global order/uniqueness. The resulting initial combined aggregate has
1,855 entries, but no later consumer pins that global count/hash. Reformatting
is not an excuse to mutate existing metadata. A future valid foreign suite is
ignored by this consumer without opening or running its files. The `unit21-v2`
projection must match all 1,200 independent entries and actual owned files;
no extra/missing/nested/renamed/redirected/nonregular/executable owned leaf.
The runner validates all owned inputs before selecting its pilot/main subset.

### D21B-I6. Independent mathematical and geometric expectations

Phase C derives every ID, payload, byte count/hash, construction summary, own
MANIFEST and inventory fingerprint independently from I3-I5 before generator
or runner exists. Two separately implemented derivations must agree on every
payload and exact quotient; neither imports a future producer or its tests.

For every nonempty vertex shore U put s=sum f over U, e=sum internal q, and
B=sum boundary q. Feasible selected totals t have 0<=t<=B, s+t odd, s+t>=3.
The least feasible candidate is 2 if s=1, 0 if s>=3 is odd, and 1 if s is even;
the greatest is B when s+B is odd, otherwise B-1. When least>greatest the shore
is infeasible. Otherwise evaluate the two endpoints of
`2*(e+t)/(s+t-1)`, with positive denominator, or independently select the
monotone extreme from sign(s-e-1). Equal endpoints need only one evaluation
if that convention is reported. Compare raw pairs by exact cross multiplication.
Enumerate every nonempty shore, not a subset, for all 1,200 recipes.

Reference A visits masks 1..(2^n-1), endpoints least then greatest, retaining
strict improvements. It records its exact raw optimum and a compact attainment
whose boundary total is allocated greedily in canonical edge order. Reference B
uses a separately implemented construction and monotonic-extreme route; tied
witnesses may differ, numerical optima must agree. Label both routes
**endpoint-reduction full-shore optimum**, never exhaustive-vector enumeration.
Empty status follows the definition. The planned shore census for one complete
scan is 300*(63+255+4095+65535)=20,984,400, not an already executed observation.

Additionally, for exactly b=1 and n in (6,8), both tau/modes and all 25 seed
tokens, enumerate EVERY compact boundary vector for every nonempty shore,
including inadmissible vectors in the visited census before testing the
admissibility rules. Interior/nonboundary coordinates are zero. Enumeration
is ascending boundary-edge-reference mixed-radix order, last coordinate fastest;
with no boundary there is one empty vector. This is 200 fixed recipes (160 main,
40 pilot), labeled **exhaustive compact-vector enumeration**. Do not replace it
by scalar-total scanning, endpoint checks, convenient workload-selected recipes,
or an unreported partial prefix. Record vector visits and admissible counts.
Finite bounding does not promise this enumeration is fast.

Phase C independently derives the descriptor geometry of I7 for all 1,200
inputs, both schedules, nested field registries and synthetic exact output
examples. Actual visited/feasible shores, endpoint evaluations, enumeration
counts and all derivation work are recorded, distinguished from planned counts.
Reference results are private/committed oracle material as explicitly registered,
not production look-ahead, operation traces or machine timing observations.

### D21B-I7. H2-prime geometry and solve-level identities

Use the fixed source atomic covers, with masks Tplus={v:f(v)+d_q(v) odd},
Tf={v:f(v) odd}, P={v:d_q(v)>f(v)}, A={v:f(v)>=2}, W={v:f(v)=1}.
Descriptors F(T,pi;I,O) in order are: D0=(Tplus,1;0,0); D1 for p in P and
each support edge u<v, (Tplus,0;{p,u},{v}) then (Tplus,0;{p,v},{u}); D2 first
(Tf,1;{a},0) for a in A, then (Tf,1;{u,v,w},0) for ascending W triples;
D3 each edge's (Tf,0;{u},{v}) then (Tf,0;{v},{u}). Vertices/edges are in dense
canonical order. Count even descriptors whose forced-in/out sets intersect.

A descriptor is feasible iff I and O are disjoint and either
T minus (I union O) is nonempty or |I intersect T| mod 2 equals pi. For a
feasible descriptor let N_F=2+n-|I union O|: fixed source/sink are two classes;
a parity anchor, when needed, is contracted into source, not a new free class.
The reference backend makes a_F=N_F^2-3*N_F+3 ordinary cut/flow calls, from its
(N_F-1)^2 ordered pairs minus the N_F-2 equal-free-vertex pairs. This uses the
reduced family size, not original n. Define r_j=number of all descriptors,
s_j=number of feasible descriptors, and A_j=sum a_F over feasible descriptors.
Thus r=(1,2*|P|*m,|A|+binom(|W|,3),2*m); repeated descriptors are counted.

For every pilot, warmup and measured nonempty solve, branch j has observed
C_j=work.oracle_calls and must satisfy, exactly:

- work.atomic_families_enumerated=r_j;
- work.atomic_families_examined=C_j*r_j;
- work.atomic_families_feasible=work.parity_cut_calls=C_j*s_j;
- work.ordinary_min_cut_calls=work.max_flow_calls=C_j*A_j.

All seed, initialization, Newton and look-ahead oracle queries count in C_j.
Infeasible branches stop at their seed (C_j=1), retain r_j examinations, and
have s_j=A_j=0. Empty has no branch records and zero branch event counts;
nonbranch bit observations are not forced to zero. Totals sum the first 20
WorkStats fields and maximize the last five, including nonbranch; never sum
peaks or multiply diagnostic summary counts by repetitions.

The runner may derive the finite descriptor geometry from input by these
support-sized loops outside the measured interval; this is bookkeeping, not
an optimizer or shore/vector enumeration. Validate it against independent
Phase C geometry in the consuming tests and external campaign audit. It must
not derive its expectation by dividing observed cut counts by C_j. Every
identity disagreement is an implementation finding and stops the attempt;
no omitted row, fake zero or best-effort success. Source big-O bounds without
finite constants remain descriptive, never invented numeric thresholds.

### D21B-I8. Runner surface, strict CLI, public dependency direction

The sibling runner has exactly `__all__=("main",)` and
`main(argv: list[str] | None = None) -> int`, positional-or-keyword, with the
same exact-type/None behavior as D21-E2. Imports do not access data, discover
environment, read clocks, run algorithms or write streams. Only stdlib, its
own generator's public surface and closed public ExactFrac APIs are imported.
Record classes may be imported for exact-type validation; solver execution is
only `solve_with_telemetry`. No private predecessor codec/helper, handoff
auditor, catalogue, canonical manuscript or test dependency. No import of
`exactfrac.experiments` to reuse its implementation. The checker stays independent.

Accepted argv is `["--help"]`, or first token exactly one of `--pilot`,`--all`,
followed by optional `--instances PATH` and `--output PATH`, each at most once
in either order. PATH is a nonempty str not beginning with '-' and containing
no NUL. Unknown/repeated/missing tokens, help combinations, `--flag=value` and
positional extras write the fixed usage text to stderr and return 2. Invalid
Python argv types raise plain ValueError before I/O. Exact ASCII usage is:
`usage: reproduce_irregular.py --help | (--pilot | --all) [--instances PATH] [--output PATH]\n`.
Help writes that plus
`ExactFrac irregular follow-up; fresh roots only; pilot precedes the author-frozen campaign.\n`
to stdout and returns 0. Usage/help do not open paths or invoke dependencies.
Successful execution is silent and returns 0 only after valid completion.
Standard streams are not rebound/closed; positive short writes complete and
invalid normal write/flush returns are RuntimeError; I/O exceptions propagate.

The wrapper calls the same main under a guarded executable entry and SystemExit,
not duplicated experiment logic. It can set/restore its import root inside that
entry only. It never installs packages or loads a conflicting installed solver.

### D21B-I9. Input and output path boundaries; no resume

Defaults are source-root/instances and source-root/results/unit21-v2-pilot or
unit21-v2 by selected mode, independent of cwd. Explicit relative paths are
relative to caller cwd. Resolve lexically; reject '..', symlinks at every
existing component, output/input overlap, output ancestors of source, and
output under source except its results subtree. Inputs/source must be real
directories. The output leaf must not exist even if empty. Missing parents
are created only after complete input/source validation. Native missing-file
and access failures are not translated into successful empty results.

An explicit alternate fresh output is a complete new invocation of the same
mode, not resume. Preserve a failed designated attempt and run anew into a
separate fresh root; never rename away, remove, append to, or truncate that
attempt automatically. Retries retain the same inventory/protocol, their
own provenance and all failed-attempt evidence. Only the explicitly identified
successful attempt is used; do not splice or pool attempts. Output location
cannot change source identity or scientific campaign ID. A later controlled
closure binds whichever authorized fresh root contains the retained attempt;
no new input namespace is manufactured for a retry.

Strictly parse the aggregate and validate I5's entire projection before any
solve/output creation. Retain each verified payload buffer for Instance.from_dict
and every checker call; no validation/reread mismatch. Strict duplicate-decoded-key,
integer-token/type, trailing-data, UTF-8/BOM and canonical owned-byte rules follow
D20-C7/D21-E4, implemented locally, not by private import. Malformed external
inputs are plain ValueError; normal generator promise violations are RuntimeError;
exceptions raised by a closed public dependency propagate unchanged.

### D21B-I10. Two fixed schedules and timing boundaries

Main campaign ID is `unit21-v2`. Filter s-tokens, ASCII-sort, index i=0..959.
For each recipe run rounds r=-1,0,1,2; Standard first iff (i+r) is even,
otherwise Accelerated first. r=-1 is one untimed warmup per route, followed
by three measured repeats, numbered 0,1,2. Exactly 1,920 warmups and 5,760
measured calls give 7,680 actual telemetry calls/checker invocations. No
warmup clock read; null elapsed is not zero. No caches, deduplication,
selection of favorable repeats, order/seed/repetition overrides or subsets.

Pilot ID is `unit21-v2-pilot`. Filter p-tokens, ASCII-sort, index i=0..239;
run each once per route at round 0 with Standard first iff i even. These
480 calls are operational diagnostics, not main warmup/measured samples.
Each pilot call is timed around the same telemetry-call boundary, explicitly
labeled pilot. All 48 cells and five seeds per cell must be included.

Execute serially, synchronously in one process per invocation, with no internal
solve/cell/campaign time limit, retry loop, affinity/GC setting, recursion or
decimal-limit change. MemoryError, RecursionError, OSError, KeyboardInterrupt
and native failure still propagate. Unbounded duration is not failure immunity.

For measured main and pilot calls take exact integer `perf_counter_ns` readings
immediately before/after the single normal `solve_with_telemetry` call. Require
nonnegative difference. Include only that call and its telemetry construction;
exclude input, geometry checks, environment, certificates, verification,
serialization, output, hashing and reporting. Retain integer elapsed_ns, plus
finite nonnegative RunMetadata.wall_clock_s=elapsed_ns/1_000_000_000 outside
solver arithmetic. Zero readings are retained; no tolerance or rounding in
integer reports. Pilot time is never pooled with main time.

Additionally the pilot records each cell's total elapsed_ns from immediately
before constructing the first recipe Instance/geometry of that cell to after
the last checked row/certificate of the cell has been written and flushed.
These two extra clock reads include local verification/output overhead and
are separately named `cell_elapsed_ns`, not solve time. Initial global input
validation and final table generation are excluded. Discovery occurs once
per invocation exactly as D21-E6; retain actual platform/python/cpu-or-null,
clock flags/resolution, recursion and integer limits, hash seed. No host/user
identifier, credentials, home path, environment dump, Git remote or private path.

### D21B-I11. Result checks, geometry checks and retained records

Require exact normal response/record types and selected route under closed
contracts. Preserve all native branch fields and every AlgorithmStats field.
No second solve to obtain counters. Build/serialize a certificate, require the
independent checker of the retained input/certificate bytes to return None,
and run the I7 geometry identities outside timing before writing the successful
row. Every warmup, measured sample and pilot call is checked. Native dependency
exceptions retain identity; contradictory normal returns are RuntimeError.

Main repeats must match their route's warmup in exact SolveResult,
AlgorithmStats and certificate bytes. Cross-route quotients agree by exact
positive-denominator cross multiplication; tied witnesses/raw pairs need not
be equal. Pilot has no same-route repeats to compare: no invented determinism
evidence from a single call. Both modes require actual route agreement.
A C0 acceptance is admissibility/attainment, not global optimality. Separate
campaign audit compares reported values to the Phase C exact optima.

Source fingerprint uses the fixed 22 paths of D21-E8 plus the three I1 sibling
modules, exactly 25 paths, ASCII-sorted. Use prefix
`exactfrac-unit21b-source/1\n` followed by each p+'\0'+sha256(p)+'\n'; record
its hash H and `exactfrac-source-sha256:`+H. No glob-discovered extra sources,
results, tests, docs, configuration or data inside the source fingerprint.
Bind loaded project modules to those exact source-root paths and hashes;
reject conflicting loaded modules. Gate-owned test sandbox copies must derive
from authenticated source bytes and cannot escape test teardown. Recheck
all consumed inputs, source images and origins before completion.

Raw main rows retain D21-E9's exact outer field names and nested RunRecord
schema, with campaign/suite now unit21-v2. Pilot uses the same row structure
in `pilot.jsonl`, campaign unit21-v2-pilot, phase `pilot`, repeat 0, integer
elapsed_ns. Main phase warmup/measured retains D21-E9's rules. All phases use
format `exactfrac-run/1`. The input object extends D21-E9 with exactly `cell`,
`tau`, `b`, `capacity_mode`, `seed`, `support_sha256`; seed is its complete token.
Support fingerprint is SHA-256 of ASCII `exactfrac-unit21b-support/1\n`, then
n+'\n', then each canonical u+','+v+'\n', unpadded. It excludes q/f/b and
binds matched topology. Existing n,m,Q_bits,max_q_bits,max_f_bits and
input_integer_bits_sum retain their precise D21-E9 meanings.

Certificates live at `certificates/{recipe}.{solver}.json`, one per recipe/route
from warmup (main) or the single pilot call. The raw certificate reference binds
its actual bytes/hash. JSON uses recursive ASCII key order, compact separators,
ensure_ascii strings, canonical integer tokens and one LF; bounded-chunk huge
integer handling and finite environmental float spelling follow D21-E9.
No public parser or new public result record is added.

### D21B-I12. Exact tables, pilot diagnostics and honest findings

Let W be the exact ordered 25 WorkStats fields in 4.13.3. Every CSV is ASCII,
comma-separated, one header, LF endings, no index/preamble/blank rows or float
formatting for integers. Fields defined here need no quoting. All order ties
below use ASCII recipe/cell order only for presentation, never solver selection.
All main tables derive from retained raw measured records, not another solve.

Main `summary.csv` has 1,920 rows, recipe order then Standard,Accelerated; header
is D21-E10's summary header with `cell,tau,b,capacity_mode,seed,support_sha256,`
inserted immediately after `recipe,solver,`. repeat_count=3; median_solve_ns
is the middle of exactly three integers. Work/peaks are repeated-identical
per-call values, not sums across repeats. `branches.csv` and `comparison.csv`
retain D21-E10's headers and derivation with 960 recipes; actual nonempty branch
counts are verified, not assumed from a planned constant. Main comparison is
one direct join of both summary rows per recipe.

Main `coverage.csv` has 48 cell-order rows and exact header
`cell,n,tau,b,capacity_mode,seeds,active_seeds,coverage_N,coverage_D`.
seeds=20; active means Accelerated total.lookahead_queries>0; fraction is
literal active_seeds/20, unreduced. Count a recipe once, not three repeats.
Never require every seed in an active cell to be active.

Main `findings.json` fields are exactly `format`,`campaign`,`h5`,
`oracle_call_wins`,`time_wins`,`fewer_calls_not_faster`,`more_calls`,
`slowest_ten`,`largest_integer_ten`,`h2_checked_solves`.
format=`exactfrac-irregular-findings/1`. The h5 object has exactly `outcome`,
`active_cells`,`total_cells`,`eligible_recipes`,`paired_difference_median`,
`zero_event_cells`; outcome follows I13, total_cells=48, and median is null
only for empty subset, otherwise {N,D} with D positive and gcd-reduced by
integer arithmetic outside solver records. zero_event_cells is ASCII order.
Each wins object has exactly `accelerated`,`tie`,`standard`, counting all 960
recipe comparisons: smaller count or smaller median time wins its own category.
Lists fewer_calls_not_faster and more_calls contain all matching recipe IDs in
ASCII order; 'not faster' includes a time tie. slowest_ten contains ten
{recipe,standard_median_solve_ns,accelerated_median_solve_ns} objects ranked
by descending max of those two medians. largest_integer_ten has ten
{recipe,standard_peak_integer_bits,accelerated_peak_integer_bits} objects
ranked by descending max peak. Ties break by ASCII recipe. h2_checked_solves
is the observed count of fully checked main calls, not an unevidenced constant.
No H3 slopes, p-values, smoothing, regressions or significance tests in unit
reports; separately preregistered paper analysis reads these retained values.

Pilot owns `pilot.jsonl`, `pilot-solves.csv`, `pilot-cells.csv`, `run-info.json`,
`COMPLETE.json` and 480 certificates, not main tables or an H5 support verdict.
Pilot-solves header:
`cell,recipe,solver,n,m,tau,b,capacity_mode,seed,max_q_bits,solve_elapsed_ns,oracle_calls,lookahead_queries,ordinary_min_cut_calls,peak_integer_bits`.
Rows follow actual pilot call order and retain per-solve diagnostics exactly.
Pilot-cells header: `cell,n,tau,b,capacity_mode,recipes,solver_calls,cell_elapsed_ns`;
48 rows, five recipes and ten successful calls per completed cell. Cell totals
are actual separately measured intervals, never a sum mislabeled as total time.
These observations inform the author's operational review, not an added numeric
time gate, selection rule, or a guarantee about future solve duration.

### D21B-I13. Hypothesis decisions and prespecified paper analysis

H5-prime is primary. Let S be all main recipes with positive Accelerated
lookahead_queries and K the number of cells with at least one such recipe.
If S is empty, report `untestable`. Otherwise report `supported` exactly when
K>=24 and median over S of (Accelerated oracle_calls - Standard oracle_calls)
is strictly negative; all other cases are `not supported`. The median is the
middle value for odd size and the exact mean of two middle values for even
size. Timing never overrides this decision. Report all zero cells and coverage.

H2-prime requires I7's identities on 100% of calls, not approximate agreement.
A valid discrepancy stops the attempt; don't relabel it an unfavorable H5
finding. Passing identities is finite implementation/accounting evidence,
not a proof of all arithmetic-operation bounds or strong polynomiality.

H3-prime series are fixed (n,tau,capacity_mode,seed), main seeds only, per route
separately. There are 320 complete series per route, each using b=1,8,64 and
matching support_sha256. Retain zero/tied responses and every series. For y
=`peak_integer_bits`, slope is exactly
`(3*sum(b*y)-73*sum(y))/7154`. This is the least-squares slope with an intercept,
not a log slope, adjacent-pair median or fit against max_q_bits. The route's
median of its 320 slopes uses the even-size convention above and is supported
iff strictly positive, otherwise not supported. Preserve individual slopes;
no merging the routes into one verdict or dropping series. For wall-clock
characterization replace y by each row's median_solve_ns with the same estimator;
no timing support threshold. Actual max_q_bits remains a reported companion,
not a substituted predictor. These fits belong to separate paper analysis,
which reads files, never calls the solver, and preserves input-record identities.

There is no verification-overhead, compact-versus-explicit, external-solver,
n>16, practical frontier, universal-speedup or isolated causal look-ahead claim.
Support describes this deterministic stratum only. Smaller oracle counts are
not automatically shorter runtime or a causal attribution to one mechanism.

### D21B-I14. Run information, transaction, resource and provenance boundaries

run-info fields are format,campaign,protocol,environment,source,inputs as in
D21-E10; format remains `exactfrac-experiment-info/1`. Environment/source rules
are I10/I11. Inputs has exactly suite=`unit21-v2`, recipes=selected mode count,
owned_recipes=1200, manifest_sha256=hash of actual aggregate bytes. That last
hash is provenance, not a permanent aggregate acceptance condition.

Protocol has exactly D21-E10 protocol keys plus `mode`,`pilot_cell_timing`.
Main values are the D21-E10 values, mode=`campaign`, pilot_cell_timing=null.
Pilot changes warmups=0, measured_repeats=0, warmup_round=null, measured_rounds=[],
mode=`pilot`, route_order=`standard-first-iff-recipe-index-even`,
timing_interval=`pilot-operational-solve-with-telemetry-return`, and
pilot_cell_timing=`first-instance-construction-through-last-row-flush`.
The pilot raw phase supplies its single pass; no fake measured repeats.
All other common values, including timeout_ns=null, are retained.

Create only fresh owned roots and files exclusively; write and flush checked
binary bytes; never overwrite, chmod/rebind predecessor paths or remove partial
attempts. Propagate I/O/native exceptions unchanged. A detected illegal normal
write count/flush result, malformed normal dependency response, clock drift,
source/input drift, inconsistent repeat/join/identity or geometry is RuntimeError.
Usage is distinct from these failures and malformed external data is ValueError.
No broad exception translation, swallowed interrupt, fake Empty, fabricated
zero time or synthetic telemetry for a failed real call.

Main owns exactly run-info.json,warmups.jsonl,runs.jsonl,summary.csv,branches.csv,
comparison.csv,coverage.csv,findings.json,COMPLETE.json and its 1,920 certificates.
Pilot owns exactly I12's files. Flush/close all earlier owned streams, re-read
and validate exact file membership, rows, hashes, source/inputs, certificates
and tables before writing COMPLETE.json last. Its exact keys are
format,campaign,source_sha256,recipes,warmup_solves,measured_solves,pilot_solves,
checked_certificates,files. Format=`exactfrac-irregular-complete/1`;
pilot_solves=480 only for a complete pilot, zero for main; the other counts
are actual mode-specific successful calls. files is the ASCII-sorted
{path,bytes,sha256} ledger of every output except the marker itself.
No self-hash, absolute path or private filename. A main complete directory has
1,929 files; a pilot complete directory has 485. These are scoped inventories,
not blanket pins on results/. Counts are checked against actual successful work.

Successful return and the complete verified ledger are both required. A
parseable marker left after flush/close failure is not successful completion.
No power-loss durability/atomic-reader/hostile-concurrent-filesystem guarantee
is made. A local user-owned writable filesystem is assumed. Never silently
resume an incomplete marker or advance into main after a failed pilot.

### D21B-I15. Phase C/D evidence and pre-freeze solve boundary

Before tests/producers exist, Phase C registers independent input/geometry/optima,
the 240/960 schedules, schemas/source lists, output examples, all decision
boundary cases and individually guard-isolated fault declarations. Include
synthetic no-event, 23-active-cell, 24-active-cell, zero/positive/negative median,
even-median, time-versus-call-disagreement, Empty and tied-raw-pair cases.
Synthetic clocks/work and fake environment strings are explicitly synthetic.
Do not infer any real solver look-ahead coverage from recipe names or schedule.

Phase D adds exactly the two consuming tests, with no dummy production file,
payload or output directory. Targeted combined RED must have precisely two
collection errors naming the two absent sibling modules and no new case
execution. New case counts are observed upon GREEN, never manufactured from
assertion/function counts. Both tests pass live candidate Ruff before applying.

Before F7, new 21B tests exercise the complete main schedule only with scripted
solver/telemetry responses. No real solve of any s-token recipe is allowed in
new tests, benchmarks, helper probes, source-mutant controls or optional reviews.
Independent definition-level optimum/geometry derivation is allowed: it is not
a production performance preview. Bounded real composition uses only the two
fixed preexisting micro inputs edge-q01-f01-01 and tri-q1-1-1-f1-1-1, both routes,
one direct call per route per actual-composition scenario, each labeled/countable;
these are not pilot/main recipes. Other schedule positions are scripted. The
unchanged inherited regressions keep their historical bounded test behavior,
never rerun the saved unit21-v1 timing campaign, and do not gain new 21B solves.

After the production/tests pass under the accepted contracts, run the disjoint
pilot exactly once per route/recipe as its own invocation, normal clocks.
Preserve and independently audit all pilot records/certificates, optima,
geometry, source/input bindings, schedule and operational diagnostics.
Report per-solve and cell observations and STOP before main to obtain the
already-required author review and F7 date. F7 is not dated by this authority,
private receipt, elapsed time, a synthetic fixture or a helper's assumed consent.
No numeric pilot-duration gate is added. Do not use pilot H5 outcomes to select,
drop, reorder or reseed cells. A prospective revision needs consistent dated
planning, authority, oracle and tests under the existing lifecycle.

### D21B-I16. Main invocation, independent audit and closure

Only after the pilot completes and the author explicitly reviews diagnostics,
dates F7 and authorizes main execution may the controlled Phase E continuation
invoke `--all` on main recipes. Private planning/BUILD/LEARNING files are not
read or hashed by execution gates; the author statement is the sequencing record.
The public CLI is not an access-control system enforcing human preregistration;
controlled invocation must respect this boundary. No additional build phase,
external reviewer gate or private-note assertion is introduced.

The campaign is actual execution on the user's authenticated candidate sources,
with normal clocks and retained raw observations, not imported container timing.
Full GREEN additionally requires the separately implemented campaign/source
audits. They independently parse records, reconstruct every table/finding,
verify every stored certificate, compare every value with Phase C optima,
check all geometry identities, inspect full source/wrapper logic and execute
preregistered materialized mutations and integration fault controls. Producer
output, derived tables and a completion marker do not certify themselves.
Mutation detection must be attributable to its intended guard, not syntax/startup
failure. No main telemetry/timing is previewed via mutation work before F7.

Phase G records observed scope and exact tests without promoting finite checks
to a theorem proof. H exports the exact staged Git tree, runs targeted/full/Ruff
with authenticated imports, preserves pilot/main/historical campaign bytes,
commits that tree, verifies postcommit, and pushes/closes separately. Routine
regression, isolation and postcommit validation READ stored run evidence and
never retime either campaign. No license, release, public export/privacy claim
or Unit 22 work begins here. Private unit notes follow full closure only.

## 16. Unit 21B prospective balanced main revision R2 — September 26, 2026

This append implements the author's September 26, 2026 ruling under D21B-I15.
The revision date is not F7. The completed original pilot is historical evidence;
no pilot or historical timing rerun, main execution, or F7 date is authorized by
this append. Earlier bytes of this document remain intact. In the explicit main-
selection and derived-count cases below, this section supersedes the original
48-cell/960-main-recipe settings in section 15. Unaffected mathematics, public
interfaces, schemas, fault families, timing boundaries and lifecycle remain binding.

### D21B-R2-I1. Rationale and original evidence

The author selects the revised main domain on operational-cost grounds: n=16
accounted for approximately 93.26% of recorded original pilot cell time. The
16-fold call-count extrapolation gives conditional workload proxies of about
20.4 days for the original main domain and 32.9 hours for the revised one. These
are planning estimates, not timeouts, bounds, guarantees, or complete workflow
forecasts. Do not claim a numerical F6 failure, general smooth scaling, absence
of future pathological calls, or a performance frontier. Observed pilot outcome
diagnostics have been disclosed; they must not be used to tune cells, seeds,
thresholds, repetition counts or reported findings.

The completed pilot archive is SHA-256
`756c75bfef86ad6858426e431547c171039ff581b640a52c959872969ee75018`.
Its 240 recipes, 480 calls, 48 cells and 485 output files retain the original
pilot interpretation, source identity and observation boundaries. The maximum
observed integer peak was 343 bits; this is neither an arithmetic-growth bound
nor a memory measurement. The archive's completed independent review is not an
unperformed prerequisite. Live transitions still authenticate actual predecessor
files normally; no repeat upload or extra review gate is introduced.

### D21B-R2-I2. Full owned corpus; narrower main selection

Preserve D21B-I3--I6's complete 1,200-recipe registry, exact IDs, payloads,
mathematical/geometry references and manifest projection unchanged. All 240
p-token and all 960 s-token recipes remain owned inputs. The original 200-recipe
exhaustive-reference subset is not reduced or re-enumerated. The original
`corpus_irregular` public behavior is unchanged, including valid n=16 s-tokens.

The revised main execution selection consists exactly of s01..s20 for:

| factor | revised main values |
|---|---|
| n | 6, 8, 12 |
| tau | 64, 128 |
| b | 1, 8, 64 |
| capacity_mode | alternating, random |

There are 36 cells and 720 main recipes. The 240 n=16 s-token inputs are retained
but not scheduled or performance-previewed. The completed pilot retains all 48
original cells, including 60 n=16 p-token recipes and 120 n=16 route calls.
Omission from the main selection is not omission from input validation: validate
all owned 1,200 payloads and the permitted aggregate metadata as before.

### D21B-R2-I3. Revised main schedule and unchanged invocation boundary

The public CLI remains D21B-I8/I9: no subset, seed, repeat, timeout or resume flag.
`--all` denotes the complete revised main selection after this revision is
adopted and validated. Campaign/root names remain `unit21-v2` and
`results/unit21-v2/`; no actual main result existed before this revision.
`--pilot` retains the original full-domain scripted contract; it is not an
instruction to rerun the completed real pilot. No automatic pilot-to-main chain.

Filter the owned registry to the 720 selected s-token recipes, ASCII-sort, and
index i=0..719. Run rounds r=-1,0,1,2 per recipe, with Standard first iff (i+r) is
even. Warmup round -1 is serialized as repeat=0 with null elapsed; measured
rounds 0,1,2 retain their repeat indices. This gives 1,440 untimed warmup calls,
4,320 measured calls and 5,760 total telemetry/checker invocations, when actually
successfully executed. Each route has 720 warmups and 2,160 measured calls.

The selected sequence is also the first 720 recipes of the original main order;
no retained recipe changes its old main index or route order. The separately
registered revised schedule must verify this rather than silently assume it.
D21B-I10's serial execution, normal clocks, no per-solve/cell/invocation deadline,
no retry loop, exact timing exclusions and propagated exceptions are unchanged.
Unbounded execution applies to this revised finite domain; it is not a promise
that future calls or the full invocation will succeed.

### D21B-R2-I4. Revised analysis population and exact decision rules

H5-prime uses only revised-main recipes with positive Accelerated
lookahead_queries. Let S be that eligible set and K the count of revised-main
cells containing at least one eligible recipe. Empty S is `untestable`.
Otherwise the outcome is `supported` exactly when K>=18 and the exact median of
(Accelerated oracle_calls - Standard oracle_calls) over S is strictly negative;
all other nonempty cases are `not supported`. This prospectively replaces 24/48
by 18/36, preserving the author's at-least-half criterion but not pretending the
two experimental populations are identical. The median of an even set is the
exact mean of its two middle entries. One eligible seed suffices for an active
cell; never require ten eligible seeds within each cell. Time never changes the
verdict. Retain every coverage row, zero-event cell and unfavorable observation.

H3-prime retains fixed (n,tau,capacity_mode,s-seed) matched support across
b=(1,8,64), now 240 complete series per route. The slope remains exactly
`(3*sum(b*y)-73*sum(y))/7154`; the two routes are analyzed separately. Preserve
all zero, tied and negative slopes, exact even medians, predictor b and the
companion actual max_q_bits. Peak-integer slope support is strictly positive;
wall-clock slopes remain characterization only. Slopes/fits remain separately
preregistered paper analysis, not new runner output fields or solver calls.

H2-prime identities in I7 apply unchanged to 100% of executed revised-main
warmup and measured calls, with complete branch/native accounting. Finite success
is not a proof of all complexity bounds. Main conclusions are limited to the
revised deterministic stratum, not all graphs with n<=12. Pilot conclusions
retain their original domain. I13's exclusions on universal speedup, practical
frontier, isolated causal look-ahead and other untested claims remain unchanged.

### D21B-R2-I5. Count substitutions; wire shapes and output ownership preserved

No RunRecord, native-record, RunMetadata, source roster, CSV column order, JSON
field set, campaign name or format tag changes merely for this selection.
The run's source fingerprint plus the adopted authority identify the revision;
do not add an undocumented protocol field. `inputs.recipes` becomes 720 in main;
`inputs.owned_recipes` stays 1200. Pilot inputs/counts remain original.

For a successful revised main: warmups.jsonl has 1,440 rows; runs.jsonl has
4,320; summary.csv has 1,440; comparison.csv has 720; coverage.csv has 36 with
20 seeds in every row. `findings.h5.total_cells` is 36. Win/tie/loss objects sum
to 720 comparisons; `h2_checked_solves` is the actual 5,760 checked calls.
Main branches.csv is reconstructed from the actual native branches for each
recipe/route; never substitute a planned branch count for an observed census.
All tables retain their I12 derivation and deterministic presentation order.

Exactly 1,440 distinct recipe/route certificate files are stored, while the
checker must succeed on all 5,760 calls. Preserve their distinction. The nine
noncertificate main files are unchanged, yielding 1,449 output files including
COMPLETE.json and 1,448 entries in its nonself ledger. COMPLETE reports recipes
720, warmup_solves 1440, measured_solves 4320, pilot_solves 0 and
checked_certificates 5760 only after actual success and complete validation.
The original pilot remains exactly 485 files; neither files nor ledger entries
may be inserted into its closed output root. Fresh-root-only, exclusive writes,
complete-last, exact revalidation and exception preservation remain unchanged.

### D21B-R2-I6. Append-only references and controlled consumer revision

Append a separately identified R2 reference bank to ORACLE_CATALOG. Preserve its
entire original prefix, original schedules, optima, payloads, schema and fault
records. Derive the revised schedule, selected/excluded IDs, counts, complete
series and H5 boundary fixtures independently of future producer output.
Use explicit synthetic cases for 17/18 cells, zero/positive/negative medians,
empty sets, exact even medians, time/call disagreement and one-seed-per-cell
activation. Synthetic records never stand in for actual campaign observations.

Retain all U21BF001..U21BF143 family IDs. Version affected quantitative
expectations rather than deleting historical declarations; specifically rebind
118,119,121 and 128 from their 23/24/320 wording to 17/18/240 as appropriate.
Other schedule, table, source and sequencing controls still need revised fixture
bindings and fresh independent coverage; unchanged declaration wording alone is
not proof of new execution. Every source-mutant credit must reach its intended
guard with passing pristine controls, not a syntax/import/count mismatch.
U21BF093 retains the original exception-object and cleanup-isolation obligation.

The smallest complete authorized amendments may change the irregular runner,
its consuming test, irregular experiment README and private independent audits.
Retain the already-authorized `_Script.instances` observation and all unaffected
assertions. Leave the pure generator, corpus consumer, closed solvers/verifier,
configuration and older closed tests unchanged. No blanket literal/count replace,
assertion deletion, fixture weakening or type relaxation is authorized.

### D21B-R2-I7. Historical pilot source lineage

The pilot's executed source fingerprint stays
`01428190bdac17bbde27aba5682503ff93a57bb0925e09fd4ec392a0a517469f`.
Preserve all 25 source images matching that roster in an inert historical source
snapshot at `experiments/provenance/unit21-v2-pilot-r1-source.zip`, outside the
closed 485-file pilot output root. This is archival source material, not an
executable backend, extra source-roster member, public release or access grant.
The archive contains the original relative source paths beneath `sources/` and
an exact source-manifest record. No private handoff paths, host identifiers or
BUILD/LEARNING notes enter it. Its pinned bytes are registered independently.

The amended main source roster still consists of the same 25 live code paths;
it excludes the snapshot, tests, docs, configuration and outputs. Its fingerprint
is recomputed from its own actual source bytes. Audit original pilot bindings
against the historical snapshot and main bindings against the amended live or
staged source. A fingerprint difference caused by the scoped runner amendment
is expected, not permission to relabel the pilot. Do not replace old run-info,
certificates, completion marker, source hashes or original validation evidence.
Preserve the historical snapshot with the complete Phase H candidate and verify
its contents on later audits without executing its old runner or retiming data.

### D21B-R2-I8. Validation and existing author-freeze pause

Authority and independent reference expectations precede consuming amendments
and producer changes. Preparation deliveries are not new gates and never alter
live repository state. Apply only an authenticated complete package for its
stated phase/transition; never replay completed helpers or restart closed units.
Use the existing live-state, candidate Ruff, targeted/full, repository Ruff,
independent-audit and conservation procedures. Observe every new collected-case
count; inherited 2,328/7,027 counts are previous evidence, not guessed new counts.
Private planning and BUILD/LEARNING notes are not execution-gate dependencies.

Retain the documented verification-subprocess-only real TMPDIR spelling needed
by the unchanged Mac positive-path harness; do not relax production symlink
rejection or change a global interpreter/shell setting. Staged-tree/postcommit
verification must carry and record the same scoped environment requirement.

Before F7, new revised-main schedules in tests/audits use scripted telemetry,
not real s-token optimization. Only the already-adopted bounded real micro
composition and unchanged inherited regression behavior remain permitted.
Independently audit all 143 families on the appropriate revision, preserving
old results and actual source bindings. No new pilot, historical timing run,
main preview, CONFORMANCE promotion or Unit 22 work follows from preparation.
After consistent adoption and successful revision validation, STOP for the
author's explicit F7 date and main authorization. Revision date is not F7.
Phase G and H remain the existing later lifecycle, preserving all original pilot,
revised main and unit21-v1 artifacts; routine validation never retimes them.

## 17. Unit 22 — private release preparation and release-gate evidence, September 30, 2026

This section makes section 12's release gate operational under the unchanged
A--H master lifecycle. It introduces release-engineering obligations, not a new
optimization problem, theorem, benchmark stratum or permission to publish.
All preceding DESIGN bytes and all earlier mathematical contracts remain intact.
This authority takes effect only after its normal review, author adoption,
application, documentation commit and remote closure. Drafting it is not adoption.

### D22-R1. Starting state, evidence and scope boundary

The author supplied a successful Unit 22 Phase A R2 transcript from the closed
Unit 21B baseline: commit `939e2c5950b9123fe5165b5232310aa33ebd4080`, parent
`8b9ab9d247efb2bb5500ae8c81e42a79d6059281`, tree
`06f15ebfc22488cf7d4bd312024924fd20a9ab1a`, 5,170 tracked/live files,
clean index/worktree and divergence 0 0. The fresh development baseline observed
7,032 collected/passed cases, repository Ruff PASS and authenticated project
imports; it did not run minimum-interpreter or release-artifact validation.
The single inherited pytest parametrization warning was not suppressed.

Phase A audit SHA-256:
`7c671c2ee33e8db77acf754f147edbe63869a98484061773756c1da7106b7d78`.
Phase A checkpoint SHA-256:
`5346a2ece1b587fe5bda2e2ce8928dc213039c584f181e7faf0bf84f737ff01c`.
These identify actual Mac records for later authentication, not embedded substitutes
for those records. A transcript and a source archive are not a full live-state audit.

No closed source, mathematical test, input, certificate, historical result or
source fingerprint changes in Unit 22. The only proposed exception to an old
consumer is the literal metadata-pin substitution specified in D22-R14; no
behavioral assertion is removed. SPEC_LOCK, CONTRACT and the historical
GOVERNING_SHA256SUMS baseline remain unchanged. H3-prime fits remain paper work.

### D22-R2. Exact unit deliverables and phase-local file scope

Phase B changes only `docs/DESIGN.md` and `docs/TEST_PLAN.md`, by append-only
postimages. No README, citation, configuration, test, license, release artifact
or audit implementation is installed with this authority.

The later unit scope, subject to the tests-first lifecycle, is:

| File | Phase and permitted purpose |
|---|---|
| `docs/ORACLE_CATALOG.md` | C: append independently fixed release fixtures/rules/expected records; retain its entire current prefix. |
| `tests/test_release.py` | D: new owning consumer for release artifact integrity, reports and rejection controls. |
| `release_audit.py` | E: new standard-library-only offline release inventory/scan/report implementation; not a solver module. |
| `LICENSE` | E: create standard MIT license under D22-R3. |
| `README.md` | E: reviewed release-candidate presentation, usage, attribution, evidence and limits under R5--R7. |
| `CITATION.cff` | E: review/update the existing tracked citation under R4, never assume it is absent. |
| `pyproject.toml` | E: only the exact proposed version substitution in R14; no license/dependency/backend change. |
| `tests/test_cli.py` | E: only R14's coupled static digest-value substitutions, atomically with the metadata. |
| `MANIFEST.in` | E: explicit source-distribution membership under R12; no production packaging backend replacement. |
| `docs/RELEASE.md` | E: candidate identity, verified public-source crosswalk, audit scope, interpreter evidence and limitations; no secrets/private paths. |
| `docs/CONFORMANCE.md` | G: append observed Unit 22 engineering scope only; preserve every earlier byte and theorem status. |

New-path absence and all existing preimages are authenticated on the Mac before
application; this proposal does not infer live absence from old archive membership.
An unexpected existing path stops the transition rather than being deleted.
No additional persistent repository files or package directories are authorized.
Private build helpers, raw scan reports, environment locks, candidate wheels,
source distributions and review artifacts stay outside the repository. They are
not private BUILD/LEARNING notes, whose paths/bytes remain outside every gate.

`release_audit.py` and `tests/test_release.py` are retained as committed release
engineering deliverables: readers can reproduce the scoped offline checks rather
than depend solely on private gate helpers. Neither changes
the existing 25-path executed-source roster or either run's fingerprint. The
source distribution includes the release auditor; the runtime wheel continues
to contain the two existing package trees only, with packaging/license metadata.

### D22-R3. MIT decision, notices and nonpublication

R7 is re-confirmed: use the standard unmodified MIT license text with
`Copyright (c) 2026 Cherine Fons`. Preserve applicable third-party notices;
retain both copyright and permission notices. A scholarly citation request is
not an additional condition on MIT reuse. Phase C fixes the exact license bytes
from the identified standard text before consuming tests or artifact production.

The author elects MIT for this release and is not pursuing a patent-protection
path for it. No patent investigation, filing, or attorney-sign-off dependency
is introduced. This is a release decision, not a conclusion about all possible
legal rights, third-party rights or legal clearance. The existing project
metadata already says `license = "MIT"`; do not replace or reserialize it.
A private LICENSE file or a passing audit is not a publication act.

### D22-R4. Existing citation and version-specific attribution

`CITATION.cff` is inherited, not missing: 899 bytes, SHA-256
`8892be71dfb141b10be30b6d0683bfcff9167ac9dff7a8b0d99ea1b47f2fdbae`,
with development version `0.1.0.dev0`. Preserve that preimage and lineage.
Its update must use canonical author identity Cherine Fons, accurate title,
MIT identifier and the same prospective version as packaging. Keep the software
citation distinct from citations for the author's mathematical manuscripts and
inherited algorithmic ingredients. Narrative prose uses "the author"; names
remain where copyright, citation and scholarly attribution require them.

Validate the actual CFF against its declared schema in an isolated validation
environment and record the validator/schema versions. Do not infer validity
from a filename, hand-written YAML parser or a generated badge. Do not invent
DOIs, affiliation, accepted-paper status, publication dates or a public release
URL. A preferred-citation override, if used, must be explicit and must not hide
the direct software citation. Current public-source status and destination
metadata must be checked before final release-candidate content is frozen.
No network lookup occurs inside deterministic tests.

### D22-R5. Mathematical authorship, pre-build implementation, verification design and author-controlled production

Lead with the author's mathematics and the detailed technical work she performed.
The required substance below is the author's controlling contribution account for
this revision. Preserve its distinction between the independently authored
pre-build foundation and the subsequent AI-generated production implementation.
Credit the author's specification, invariant and test design, mathematical
judgment, personal gate execution, corrective rulings, scientific interpretation
and multi-system governance at the specificity given here. The final provenance
paragraph is part of the same account, not a replacement for that technical credit.

**Required contribution account — the author's role in ExactFrac**

<!-- BEGIN REQUIRED CONTRIBUTION ACCOUNT -->

ExactFrac originates in the author’s mathematics. The author proved the underlying
theorem, designed the strongly polynomial algorithm, and authored the mathematical
specification against which the implementation was required to conform. Before the
production build commenced, the author implemented the problem’s fundamental
computational objects within a 214-commit, test-gated codebase containing no AI-written
code. This pre-build foundation included a from-first-principles brute-force checker
implementing the manuscript’s definitions directly, with a hand-proved lemma serving as
its independent oracle, and culminated in a timed mock assessment and exit test. The
resulting codebase established the author's independently authored command of the
problem's computational objects which serves as the basis on which she subsequently
specified, reviewed and judged the ExactFrac implementation.

The author then designed and administered the formal regime under which the production
system was constructed. The mathematical source was frozen as a versioned, hash-pinned
authority containing explicitly identified definitions, lemmas, and theorems, so that
implementation decisions could be traced to fixed mathematical statements rather than to
recollection or informal interpretation of the proof. She translated those statements
into explicit interface contracts: the active hypothesis became a precondition;
witnesses were represented compactly as \((U,y)\); outputs retained raw, unreduced
\((N,D)\) pairs; and the Empty case was assigned a specified value. Representation
choices were made so that the relevant invariants remained externally inspectable, with
exact arithmetic throughout and an explicit prohibition against normalization whenever
such reduction would destroy literal attainment. The implementation architecture was, in
turn, decomposed along the structural joints of the proof itself: branch domains
\(D_0\)–\(D_3\), atomic families, sign routing, parity cuts, the exact residual oracle,
branch solvers, global selection, and witness and certificate construction, so that each
mathematical operation was isolated behind its own contract and could be audited
independently.

Around those invariants, she constructed the project’s verification discipline. Expected
behavior was derived before the corresponding production implementation existed, using
hand-derived cases and independently implemented reference routes that were required to
agree before either could be used to judge production code; production output was never
permitted to serve as its own oracle. Acceptance criteria were preregistered and
adversarial. For each invariant, the relevant failure modes, including parity and
feasibility boundaries, Empty and infeasible families, ties, endpoint monotonicity,
malformed inputs, and dependency failures, were fixed in advance in a preregistered test
plan, and a registered RED state was required before any GREEN implementation could be
accepted. Every nonempty result was required to carry a compact witness checkable
through a two-input certificate contract and by a checker importing nothing from the
solver itself. The certificate establishes admissibility and literal attainment; the
independent reference comparisons and the mathematical argument provide the remaining
basis of validation. She likewise made the algorithm’s complexity structure observable
by defining telemetry whose identities are derived from the geometry of each instance:
\(r_j\), \(s_j\), and \(A_j\) compared against observed oracle calls, so that the
implementation could be examined not only for the value returned, but also for whether
its realized execution structure matched the work prescribed by the proof. That
telemetry was treated expressly as finite evidence about execution structure, not as a
proof of universal complexity bounds.

Across all twenty-two units, she adjudicated each authority before it entered the
repository, correcting architectural defects where necessary and closing each authority
and oracle set in a dedicated commit. She personally executed every RED gate and
inspected the exact collection failure; executed every implementation gate and inspected
the resulting GREEN census; and carried out every conformance, staging, isolated
staged-tree, commit, and push transition. When a gate produced a STOP, whether because
of lint findings invisible to the drafting container, a tracking-reference mismatch, a
preloaded-module collision, or a helper whose logic incorrectly assumed that a file was
absent, she adjudicated the failure, routed the package for independent review,
authorized the corrective revision, and reran only those operations permitted by the
governing rules. Her rulings established the operative discipline of the build: the only
gates are hers; the Accelerated solver is part of the core system; the global solver
must be exercised under both branch solvers; no file intended for population by a later
unit may be prematurely frozen by hash; experimental campaigns must execute from a fresh
root without timeout; and failed attempts are preserved in the record rather than
replayed as though they had not occurred.

As the system became increasingly intricate, she managed it as a controlled multi-system
research project. A drafting model produced implementation packages; a separate
reviewing model recomputed oracles and campaign results through an independent route;
her Mac remained the sole execution environment; and a private evidence tree bound
repository transitions to hashed audits and checkpoints. She established continuation
protocols and state blocks to preserve rulings across sessions, set model-tier routing
and data budgets, maintained upload ledgers so that artifacts could not move between
systems without authentication, and imposed byte-pinned authorities, append-only
governing documents, source fingerprints, and controlled one-value amendments. These
mechanisms made the development history reconstructible from the first commit forward.
She also identified and corrected errors introduced by the surrounding systems
themselves, including a reviewer that inserted an unauthorized step into her protocol, a
reviewer that misstated a commit sequence, and a drafting helper that misread repository
state, preserving the governing lifecycle in each instance.

She retained control of the scientific interpretation of the project. She maintained the
conformance map linking source obligations to implementation, tests, and recorded
status, while enforcing the distinction between computational evidence and mathematical
proof: a passing test was treated as evidence of conformance on the tested instances,
never as a proof of the universal theorem. She fixed the project’s technical language
accordingly: a certified fractional lower bound, never an exact block count; no claim
extending beyond the tested stratum; no pooling of pilot and main-campaign data; and no
removal of unfavorable results from the record. She ruled the experimental designs
before measurement, authorized the pilot, examined its diagnostics, revised the scope of
the main campaign on cost grounds through a dated authority before fixing F7, dated F7,
executed the campaign to completion, and determined both the release terms and the
standards governing the truthfulness of this contribution account.

Within this regime, an AI system generated the production implementation and supporting
infrastructure to the author’s specification and a separate AI system reviewed the
generated packages and independently recomputed oracles and campaign results. Every
resulting artifact was nevertheless admitted only through her acceptance: against her
theorem, under her specification, and at a gate that only she operated.

<!-- END REQUIRED CONTRIBUTION ACCOUNT -->

**Retained test-design and acceptance credit.** The author authored the
preregistered `TEST_PLAN` obligations and the oracle expectations before the
corresponding production code, designed the failure-mode catalogue and the
143 declared fault families, and imposed RED-before-GREEN as a binding gate.
She personally ran every gate, read every RED and GREEN result, and made every
acceptance ruling. The Exit Test was not waived after a clean mock: she held
the required gate even against her own preference. Credit test design,
execution, interpretation and adjudication distinctly; retain the preregistered
scope of the 143 fault families rather than relabeling them as 143 test cases.

**Current-state reading of the contribution account.** The account describes
work across the twenty-two-unit programme; completed-action language refers to
transitions actually achieved by the current checkpoint. At this revision,
Unit 22 Phase A R2 is complete and Phase B is still a reviewer proposal. The
phrase "Across all twenty-two units" does not record completion of pending
Unit 22 authorities, oracles, gates, release checks or closure. In the eventual
README, express the achieved extent at its freeze point using the actual
record. Likewise, "her Mac remained the sole execution environment" identifies
the authoritative build-gate and campaign environment, distinct from assistant
package-preparation checks and separate reviewer recomputation. This preserves
the supplied contribution account without promoting preparation into execution.

**Presentation — Phase E, UNVERIFIED.** Retain the author's open rendering
item for inline `\((U,y)\)` and the corresponding mathematical notation.
Inspect one actual GitHub render of the candidate contribution text at Phase E
before final README acceptance; source inspection or a local Markdown render
is not evidence that the GitHub render passed. Record the candidate identity,
rendering surface and result. This is a presentation review within the existing
README review, not a new lifecycle gate. It neither edits the current README
nor moves the D22-R14/RL15 Phase C exact-byte freeze into Phase E. If the render
requires a delimiter correction after C, use a reviewed, explicit revision of
the affected exact references and the existing coordinated E metadata/pin
process; never silently alter a frozen README or substitute a digest. No public
upload or repository visibility change is authorized by this presentation item.

**Contribution-review basis and scope.** Use the author's current contribution
account and the actual source, authority, test-plan, commit, audit and campaign
records for their respective claims. Keep the 214-commit pre-build foundation
and its independently authored checker distinct from the production repository's
implementation history. The earlier six-module and twelve-module production
handwriting formulations are superseded by this account; preserve prior review
packages as historical records rather than importing their wording as current
requirements. Reviewers identify what each available artifact corroborates and
what is stated in the author's account. Inherited-method citations and accurate
provider provenance remain intact. Use "the author" narratively, with the actual
name retained for copyright, citation and scholarly attribution. This remains
an existing contribution/source review: it adds no authorship gate, historical
replay, private-note inspection or historical-commit rewrite.

### D22-R6. Mathematical, verification and publication-status language

README review against section 0 must distinguish exact computation of the
modified set-pair density under the active hypothesis from its application-level
interpretation as a certified fractional lower bound. Retain compact witnesses,
raw-pair semantics and the Empty case. Never call the output an exact integral
block count, an integral colouring or a deployable schedule.

Keep theorem statements/hypotheses, finite software checks and empirical timing
separate. C0 acceptance is admissibility and literal attainment; global optimality
is not certified by attainment alone. Separate reference comparisons and the
mathematical correctness argument supply different evidence. A test count is
not a proof of universal correctness or strong polynomiality.

Identify the exact public manuscript versions underlying theorem claims, with
verified title/author/identifier/status and a private hash-bound crosswalk to
the governing source where appropriate. The pinned private mathematical source
is not committed or copied into release artifacts. No inferred peer review,
acceptance, publication priority or endorsement. Missing public-source evidence
is reported as unresolved; it cannot be replaced by a plausible citation.

### D22-R7. Experimental reporting and reproduction cost

Present the original `unit21-v1` study before the irregular follow-up. Preserve
the follow-up's design history and the September 26 cost-based scope revision,
separately from F7 of September 27, 2026. Main performance observations concern
the frozen 36-cell deterministic n={6,8,12} stratum; the full 48-cell pilot,
including n=16 and unfavorable observations, remains separately labeled.
Do not reinterpret finite sample size as a restriction on a source theorem.

Any empirical headline retains the observed metric and denominator. H5-prime
support uses the frozen pooled rule, not a cell vote or timing threshold.
The 303/87/119 eligible outcomes, 24/9/3 cell-median signs and the three positive
cells stay visible in the retained conformance/evidence; marketing text may not
turn support into universal acceleration or an isolated causal look-ahead claim.
No new H3-prime slope, route verdict or adjusted benchmark is produced here.

Distinguish small ordinary usage, regression, reading/checking retained results,
and optional fresh experimental re-execution. The full irregular `--all`
workload is 720 recipes, both routes, 1,440 warmups plus 4,320 measured calls,
with the original fresh-root-only/no-timeout behavior. It is optional for users,
not a release acceptance rerun. Do not present 31 or 33 hours as measured total
runtime without a matching elapsed-time record: warmup timings are null, and
summed measured solve intervals exclude other work. Hardware-dependent planning
or author-reported approximations must be labeled and sourced as such.

### D22-R8. Complete inventory and retained-evidence conservation

Inventory the exact candidate source tree and each distribution independently.
Record path, object type, mode, byte length and SHA-256, with canonical path
order and duplicate rejection; bind the report to the artifact hash and source
snapshot identity. Archive and directory inventories are separate claims.
Use exact expected membership, not just file counts or successful extraction.
The 5,170-file baseline is phase-local, not a permanent cap on Unit 22 additions.

Preserve all 1,200 irregular input identities, 1,317 original-study results,
485 pilot results and 1,449 main results in the canonical repository. Preserve
all current source, certificate, reference and run fingerprints. A new release
version identifies distribution metadata, not a rerun or rebinding of the
historical experiments. Historical snapshots are inert files, not imported
alternatives. Packaging omission is not permission to modify canonical bytes.

Baseline SHA-256 identities are maintained in a private phase manifest read from
actual authenticated files at application; no generated example manifest may
substitute for that Mac record. Recursively inspect embedded archives under R10;
for example the original-pilot source ZIP is not cleared by scanning its filename.

### D22-R9. Privacy, history, secrets and disposition records

The section 12 scan covers current candidate paths/content, relevant Git history
and metadata, and candidate archive members. History acquisition is read-only:
record the ref set and inspected commit/tree/blob/tag identities and scan author/
committer metadata, messages and historical paths/content. Record any inaccessible
or omitted history explicitly; a shallow or failed scan is not a complete PASS.
Do not pretend a local scan authenticates unavailable remote-only content.

Flag credential/private-key candidates, private user or handoff paths, contact
information, personal names and tool/provider references for explicit disposition.
A match is a finding, not automatic evidence of a secret and not permission to
delete it. Retain legitimate author attribution, scientific citations and truthful
AI/tool provenance. Dispositions bind rule, location and exact content identity;
no blanket exemption for every occurrence of a name, directory or extension.
Raw findings may contain sensitive context and remain private; publish only
reviewed summaries without echoing credentials or private absolute paths.

A scan failure, unreadable object, unsupported encoding/container or resource
limit leaves affected scope INCOMPLETE. Missing coverage cannot be relabeled
clean. Tests use only unmistakably synthetic credential examples, never live
secrets. Scanner output alone cannot guarantee absence of all sensitive material;
manual review of scope, unclassified findings and content is part of section 12.
No scan opens, locates or hashes the author's private BUILD/LEARNING files.
A prohibited note filename found inside the candidate artifact may be rejected
without making private-note existence elsewhere a gate condition.

### D22-R10. Release auditor interface and nonmutation

The new `release_audit.py` is an offline, stdlib-only engineering auditor outside
`exactfrac` and `exactfrac_verify`. Its import has no I/O, command execution,
project imports, network access, environment change or interpreter-setting change.
Its owning tests import `release_audit`; its absence provides genuine Phase D
missing-module RED. No solver module is deleted to manufacture that state.

The public functions are `inspect_tree(root)`, `inspect_archive(path)` and
`inspect_history(repository)`, each taking an exact `str` naming an absolute
existing path. Tree/repository roots and archive parents must be real directories;
the archive itself must be a regular nonexecutable file. A symlink in the accepted
path or an unsupported root is rejected, not resolved into a different input.
`inspect_history` may invoke only explicitly enumerated read-only Git commands,
without shell interpolation, fetch, index refresh/write, object writes or hooks.
An incorrect public argument raises exact ValueError before activity; violated
validated dependency promises raise RuntimeError; actual dependency exceptions
are propagated unchanged. No repair, chmod, deletion, network or installer call.

Each function returns a fresh JSON-compatible record with format
`exactfrac-release-inspection/1`, kind `tree`, `archive` or `history`, inspected
subject identities, coverage, sorted inventory and sorted findings. Integer
counts are exact, never bool; bytes/hashes and safe relative names are preserved.
`coverage` is `complete` or `incomplete`; inspection outcome is `no-findings`,
`findings` or `incomplete`, never a public-release authorization or unconditional
privacy/legal certification. Actual paths and diagnostic context in raw records
are private. No API returns a final release PASS merely because findings are empty.
The exact closed record keys and wire examples are fixed independently in Phase C
under this interface before tests; they may not remove these fields or meanings.

Tree reads never follow symlink entries or open FIFOs/devices/sockets as ordinary
files. Report such entries and non-UTF-8 paths as unsafe/incomplete as appropriate.
Archive inspection supports ZIP and tar source distributions, including nested
supported archives, without writing extracted content into the candidate tree.
Reject absolute/traversal/backslash/NUL names, duplicate or ambiguous normalized
names, links, device/FIFO entries and escaping paths. Actual decoded membership
and actual bytes, not untrusted length fields alone, determine completeness.
Resource bounds are explicit, recorded inspection parameters fixed in Phase C;
hitting one gives incomplete coverage, never a silently truncated clean result.
No user path can be substituted into a shell command or followed outside scope.

This unit does not require a new installed CLI or daemon. Private orchestration
may call these APIs and save their returned records outside the repository. That
orchestration is itself reviewed and negative-tested before live use; helpers
are not run merely because they are packaged. Artifact creation is separate from
inspection, and inspection never installs or executes inspected source/archive code.

### D22-R11. Independent fixtures, tests and audit independence

Phase C appends versioned release expectations to ORACLE_CATALOG: exact metadata
reference bytes/digests; standard license; source/wheel profiles; scan rules and
finite limits; record examples; positive and negative trees/history/archives;
and scope/publication decision examples. Construct small finite synthetic Git
histories and archives independently of future release-auditor output. No solver,
main/pilot invocation or private-note fixture path is needed to derive expectations.

Test the auditor with materialized faults and passing pristine controls before
and after each fault. Intended semantic, membership, provenance and coverage
errors must reach their registered guard; syntax/import failures are not credited
as their kills. Include coherent metadata/table/report alterations with updated
hashes so a stale hash is not the only protection. Separately implement the
artifact inventory/report cross-check; the release producer must not be the sole
oracle for its own output. Record case count, explicit review types and executed
controls separately; no presumed count or "all cases" claim from a list of IDs.

The completed 21B campaign audit remains closed. Authenticate its retained
records; do not regenerate inputs, reenumerate optima, retime experiments or
replay the 143-family lifecycle simply to perform release inspection.

### D22-R12. Private distribution artifacts and clean-install evidence

Prepare a versioned source distribution and wheel from the exact authorized
candidate in private fresh build directories. `MANIFEST.in` explicitly includes
the source-validation profile: the two package trees, unchanged owning tests and
needed fixtures/docs, all existing instance/result evidence, the release auditor,
README, CITATION, LICENSE and packaging metadata. It does not include .git,
virtual environments, caches, build/dist leftovers, private handoffs/notes or
the private governing manuscript. Preserve legitimate reference files required
by the full suite; do not omit them to make an inventory look cleaner.

The wheel contains only the existing solver/verifier packages and declared build/
license metadata; it is not advertised as containing the full research corpus or
auditor. Independently enumerate both archive profiles, generated metadata and
license notices. Bind builds to source-manifest and interpreter/tool identities.
Byte-for-byte rebuild reproducibility is not assumed from one successful build;
compare content and separately record any nondeterministic archive metadata.
No release tag, external upload or index registration is created by building.

In fresh environments outside the checkout, install the candidate wheel and
exercise the actual public solver/verifier entry points on predeclared tiny
examples. Verify imports originate from that installed artifact, not editable
installs, PYTHONPATH or a repository directory. These are bounded correctness
smokes, not new benchmarks. The source distribution must separately support the
full applicable tests from its exact extracted content under R13. Record any
metadata or membership incompatibility; never silently change closed code/tests.

A candidate containing unresolved sensitive data is not cleared for publication.
If privacy-safe full source/reproduction packaging requires omitting or changing
frozen material, record the conflict and obtain a separately scoped authorization;
do not weaken the source-distribution validation or rewrite historical evidence.
The canonical private repository remains intact regardless of release profile.

### D22-R13. Minimum and development interpreters; genuine reproduction

Run the full applicable suite, including Unit 22 consumers, on an actual Python
3.11.x interpreter and on Python 3.14.6 in separately created clean environments.
Record exact interpreter executable/version, platform, validation/build dependency
versions and acquisition identities, commands, root and import origins, actual
collected/passed/error/skip/xfail counts, warnings and complete failure streams.
The current Phase A 7,032 pass is a development starting result only; it does
not establish minimum-version compatibility or candidate-wheel correctness.

Keep the authenticated existing .venv unchanged. Use available verified base
interpreters; if a required interpreter is absent, report the missing requirement
and obtain any necessary installation authorization. Do not alter global Software
Update settings or install into system/closed environments. Fresh-environment
dependency acquisition is scoped and recorded, not an upgrade of the baseline.
Resolve compatible tooling within the existing declared constraints, then pin
and preserve actual validation versions. An unavailable dependency is not a test
PASS or a reason to silently raise requires-python. Actual failures stop the
transition; source/test/config fixes require separate scoped review.

Run candidate Ruff preflights for every changed Python target before application
with the repository's authoritative Ruff and correct target filename; no detached
lint result substitutes for that gate. Run repository Ruff and the unchanged
applicable regression at the normal B--H checkpoints. Tests and test identities
are preserved except R14. Carry the authenticated resolved TMPDIR spelling only
into verification subprocesses, leaving path guards and global settings intact.
Retain all raw observations; never suppress an inherited warning or skip a
failing test merely to claim cross-version support. Test counts are observed.

### D22-R14. Confirmed release version and adopted metadata-pin exceptions

The selected release-candidate artifact version is `0.1.0`, confirmed for this
R2 authority; it is not an already-published release, publication date or claim
of wider compatibility. The only pyproject edit is
`version = "0.1.0.dev0"` to `version = "0.1.0"`, preserving every other byte.
The existing MIT identifier, >=3.11 requirement, build backend, dependency bounds,
package selection, pytest and Ruff configuration all remain unchanged.

| pyproject image | Bytes | SHA-256 |
|---|---:|---|
| Current | 957 | `13d5e442582c14e278f726cc3e5d9fecdff5a0cba224e53313a3a8cfc1a4812b` |
| Selected candidate | 952 | `8fed90272a28374a421dd48323a81b41b27ee80790d40e6bfa6f57a0b370d256` |

The complete old `tests/test_cli.py` is 99,824 bytes, SHA-256
`6edf3930b3a5db998aea9a1e769b14b5af5046edd996a8b3e42022ef4d7545f0`.
Its `_FROZEN_SOURCE_HASHES` dictionary pins README and CITATION as well as
pyproject. The author has now explicitly adopted all three digest-value
exceptions below, using the D20-M1/D21B-I2 controlled-exception pattern. This is
the recorded permission for the README/CITATION exceptions as well as pyproject;
it is not inferred from the earlier pyproject-only permission:

| Dictionary key | Old digest | Zero-based half-open digest-byte interval |
|---|---|---|
| `CITATION.cff` | `8892be71dfb141b10be30b6d0683bfcff9167ac9dff7a8b0d99ea1b47f2fdbae` | [31512,31576) |
| `README.md` | `05ff99bd562eaed86fe55e7eb2902255dacb4bddcbcb14943b21e2be7b51c09f` | [31697,31761) |
| `pyproject.toml` | `13d5e442582c14e278f726cc3e5d9fecdff5a0cba224e53313a3a8cfc1a4812b` | [33561,33625) |

Each substitute is the static 64-character lowercase SHA-256 of that file's
exact reviewed E postimage, never a dynamic digest read by the test. The pyproject
substitute is the fixed value above. Freeze README/CITATION full postimages and
the resulting full CLI-test postimage in the independently identified Phase C
reference supplement before Phase D; report both lengths, full SHA/blob values
and these three slices. References document expected bytes, not application.
All 41 dictionary keys remain; the other 38 values, quote style, ordering,
whitespace, imports, `_CLOSED_PATHS`, tests and assertions are byte-identical.
Require exact equality outside the three allowed slices, not just AST equivalence.
A reference byte change after freeze needs a reviewed new revision; no arbitrary
replacement hash, ignored key, deleted pin or broader exception is permitted.

Keep the old CLI consumer and all three old metadata files unchanged during
B, C and D. Only the complete E implementation/metadata package substitutes the
three digest tokens atomically with their corresponding reviewed file changes.
This narrowly scoped consumer amendment avoids running a knowingly inconsistent
old metadata/new pin mixture. The new owning release consumer is already frozen
from D, and no other test byte changes at E. The adopted exceptions do not
permit application before normal B closure, independent C freeze and D RED;
missing or changed frozen values stop E rather than bypassing the hash loop.

### D22-R15. Release readiness evidence and noncircular result records

The section 12 conclusion is assembled from separately identified inventory,
scan/disposition, notices, README/theory/benchmark, artifact build/install and
interpreter results. The report binds actual input hashes and outcome scope;
no timestamp, package number, assumed author consent, generated completion marker
or historical test pass supplies missing evidence. Unresolved/failed/incomplete
requirements preclude release-readiness PASS but do not invalidate closed 21B
science. A private-history exclusion can support a separately audited clean
artifact only when its exact profile and exception are expressly authorized.

`docs/RELEASE.md` records evidence already observed at its review point, not
its own future commit hash or self-hash. Later staged/committed artifact identities
and final postcommit audits are private external records bound to that immutable
candidate; do not edit the report after testing to claim it tested itself.
Final release metadata contains no fabricated publication date or DOI. New
metadata does not rewrite pilot/main run-info or old source/version fields.

### D22-R16. Phase sequencing, preservation and controlled failure

A remains closed at the supplied R2 checkpoint. B is review-only until the author
accepts the complete two-document authority; then apply unstaged, validate,
stage, commit and close remotely under the existing lifecycle. C independently
registers expectations before the new owning test or auditor exists. D applies
only `tests/test_release.py` after repository-context candidate Ruff; require
exact ModuleNotFoundError for `release_audit`, with the old suite passing when
that new file is excluded. LICENSE and the future auditor remain absent; the
inherited README/CITATION/pyproject/CLI test remain byte-exact.

E applies the complete authorized auditor, release documents/metadata and
coupled CLI-pin amendment only after D and C evidence authenticate. No partial
metadata/pin installation. Run targeted/full/Ruff, independent release checks,
clean-environment and bounded install validations and required conservation.
F's source/import/nonmutation review remains part of E's checkpoint, not a new
phase. G appends only observed CONFORMANCE scope after genuine GREEN. H stages
the exact candidate, tests its actual index-tree export with authenticated
imports, commits that same tree, validates postcommit and closes the private
remote separately. No step silently creates a public tag or upload.

Every transition authenticates its actual predecessor and all out-of-scope
files before/after. Preserve failures and prior revisions; never reset, clean,
restore, overwrite evidence, auto-retry or replay a completed helper. Slow
validation has no invented timeout. Correct a helper in a separately identified
package without weakening the production/acceptance contracts. Any environment
acquisition or compatibility problem is reported explicitly, not concealed by
an unrelated new test or a different imported installation.

### D22-R17. Publication boundary, private notes and final claim

The canonical repository stays private through Unit 22. No visibility change,
public repository creation, package-index upload, release upload, external deposit,
force-push or history rewrite is authorized here. A passing section 12 audit
establishes only the readiness of its exact reviewed candidate and stated scope.
A separate explicit author act must identify artifact/version/destination before
publication. Reconfirm privacy scope if that act changes the artifact or history.
Preserve section 12's separate clean-public-repository option; do not flip private
research history to public merely because a source ZIP passed a content scan.

Helpers never alter global Software Update settings. The author's existing
settings remain author-controlled. Private BUILD/LEARNING notes are delivered
only after full private remote closure, remain outside the repository and every
gate, and are saved only by the author. Their prior saved confirmation is not
reauthenticated by probing the filesystem. Unit 22 closure is not an H3-prime
paper-analysis verdict, universal software guarantee or a completed public release.

### D22-M1. Post-closure test-path correction and corrected-source artifact selection

This bounded maintenance authority follows private remote closure of candidate
`c11d3063c68265a31ee378982bd181b3107136b9`, tree
`58070430af4fecbc10e41f57437c741948a44582`. That closure and its original
source/distribution evidence remain historical facts, not operations to repeat.
This amendment uses D20-M1's exact-preimage, exact-slice and exact-postimage
control pattern; it does not reuse D20-M1's former CLI-pin permission.

#### D22-M1a. One exact insertion in the closed positive test fixture

The sole test correction is in `tests/test_experiments_irregular.py`, inside
its `_GIANT_PROGRAM` raw string. At the existing line 5378, replace exactly:

```python
    observed = scope["_execute_scripted_case"](Path(temporary), "main", giant=True)
```

with exactly:

```python
    observed = scope["_execute_scripted_case"](Path(temporary).resolve(), "main", giant=True)
```

Preserve the four leading spaces and existing LF. No wrapping, reformatting,
newline conversion, assertion change or second insertion is permitted.

| Complete test identity | Preimage | Required postimage |
|---|---|---|
| SHA-256 | `1112ba023339b857a7ee912843d1c2fc52ed4d973f525c90001d1db0a0c1fe57` | `65ea3e35bdf9e4406c4356a7b5697cd3cd155516becde9ec82dad308efbbc8e9` |
| Git blob | `9aa5a6ecfcf2495a7c45e9841c624a72cd29161e` | `19542148642d22f28989089d5f56e2fa85c125f4` |
| Bytes | 272,656 | 272,666 |
| LF lines | 5,592 | 5,592 |
| Git mode | 100644 | 100644 |

For the complete authenticated old bytes, require:

```text
new == old[:260598] + b".resolve()" + old[260598:]
```

The insertion is ten ASCII bytes at zero-based offset 260598; it occupies
[260598,260608) in the postimage. The offset and line number are locators only.
The exact old line must be unique and belong to `_GIANT_PROGRAM`; authenticate
both complete hashes, lengths and blobs and require byte equality outside the
insertion. AST equality outside that single string value is supplementary,
never a substitute for byte conservation. Reject any additional difference.

The fixture creates the temporary directory before this call. The correction
passes that existing directory's resolved spelling to `_execute_scripted_case`.
It changes neither the test's scheduled work nor its success criteria. The
identified regression consists of the existing parameter values 640 and 4300
of `test_fresh_process_scripted_main_giant_native_records_at_unchanged_digit_limit`;
this authority does not attribute an unidentified third failure to this cause.

#### D22-M1b. Production, consumer and historical boundaries

The production runner `exactfrac/experiments_irregular.py` stays byte-identical
at SHA-256 `61c4c62d95d72c2fb89596f6de09f216064012ea2a526b14fd645fe5b7d71e30`,
including `_parents()` and `_lexical()`. Its symlink rejection remains correct
and unchanged. No production path repair, relaxed guard, digit-limit change,
solver modification or new arithmetic/tie-breaking rule is authorized.

`tests/test_cli.py` stays byte-identical at SHA-256
`f2dc6a084030fba3aff1a2de490dc910c01d267db6860844452c338ac8b10c48`.
Its 41-entry `_FROZEN_SOURCE_HASHES` dictionary does not pin the irregular test;
no CLI-pin exception is needed or granted for this correction. Its README,
CITATION and pyproject pins remain intact. The owning release consumer remains
unchanged. No optional README sentence, metadata/version change, new fixture
bank, scanner change, corpus change or campaign execution is part of this scope.

The only immediate authority application paths are `docs/DESIGN.md` and
`docs/TEST_PLAN.md`, each append-only. The test remains at its old hash during
that documentation-only transition and authority closure. After that authority
has been reviewed, adopted and closed under the ordinary Phase B sequence,
the author performs the exact manual insertion at the controlled correction
application point; a helper authenticates the result rather than silently
substituting another edit. All unrelated source, tests, metadata and recorded
experimental inputs/outputs remain frozen. Any real additional consuming
conflict must be reported and separately ruled, not guessed or bypassed.

#### D22-M1c. Two genuine validation environments

Retain the last recorded development toolchain, Python 3.14.6 / pytest 9.1.1 /
Ruff 0.16.5, unless a separately recorded and adopted environment change is
required. Helpers do not upgrade the development environment or alter global
settings. Use the established real-path TMPDIR condition for documentation-only
authority validation while the old test is still present; do not turn the known
pre-correction default-path failure into an invented authority regression.

After the manual edit, validate the corrected candidate in both the gate
environment (A) and the ordinary-shell default-TMPDIR environment (B), with the
same recorded interpreter and dependencies. A supplies the existing temporary
directory's real-path spelling. B retains the actual default macOS TMPDIR
spelling that crosses `/var` to `/private/var`, including in the fresh child;
neither the launcher nor a test wrapper may normalize TMPDIR for B. The only
new normalization is the reviewed expression at the positive fixture call site.
Record the raw TMPDIR, its resolution and the observed symlink condition;
a B run whose input is already a real path does not demonstrate this regression.

Require actual collection and passing of the same complete 7,220-case roster,
including both named digit-limit cases and the 188 release cases, in both
environments. These counts are expected from the prior census, not fabricated
results. Record actual setup/call/teardown outcomes, errors, skips, deselections,
xfails, warnings, return codes, commands, interpreter and import origins. No
exclusion, xfail credit, warning suppression, environment repair or changed
integer/recursion limit may conceal a failure. Keep the fresh child's substantive
assertions and inherited symlink rejection coverage unchanged. Retain failed
attempts; do not auto-repair or auto-retry.

Repository-context candidate Ruff precedes the manual application point, and
repository Ruff follows validation under the ordinary controls. The standard
source/import/nonmutation review, observed-only CONFORMANCE append, exact
staging, staged-tree isolation, same-tree commit, postcommit verification and
separately authorized non-force remote closure remain applicable. They use the
new candidate's identities; the completed original gates are not replayed.
No missing-module RED, extra numbered unit or new process gate is invented for
this bounded correction of an existing test.

#### D22-M1d. Finalized corrected tree and new artifact pair

The author selects the finalized corrected source tree, not the original
candidate, for publication preparation. Preserve both original distributions,
all original bindings and all stopped/successful evidence unchanged. In
particular, retain the original sdist SHA-256
`43c3cddb411814eb85e47eda1790d102c1d9f68282c40db5f0527e4e61712164`
and wheel SHA-256
`2d209d30da742f5e135ff60f7fe5406ad63c0753f1e57f9a9e60309d8c8a3118`
as historical artifacts of the original source identity. No overwrite, deletion,
retroactive relabeling or rebinding of those bytes is authorized.

After the authorized authority/test/CONFORMANCE work is finalized and the
correction is closed, identify the actual final commit, Git tree and complete
source manifest. Build BOTH a new source distribution and a new wheel from
exports of that same exact tree in fresh separate private build locations.
The documentation-only authority commit is not the final corrected candidate.
Keep the selected version 0.1.0 and all packaging configuration unchanged; any
version or profile change needs a separate exact exception. Even if a rebuilt
wheel has identical bytes, record its new build execution and provenance rather
than carrying forward the old build verdict. Compare instead of assuming
byte-identical rebuilds.

Apply D22-R12/R13 and RL13/RL14 to the new pair: enumerate each complete archive
and generated metadata, verify source membership and clean import origins,
run the complete applicable sdist suite on actual Python 3.11.x and Python 3.14.6
in fresh environments, and perform the predeclared installed-wheel public
solver/checker smokes. The corrected macOS default-TMPDIR obligation remains
explicit and is not replaced by successful controlled-environment validation.
Dependency/interpreter acquisition, if needed, requires its own bounded
permission; no system or closed-environment upgrade is implied.

MANIFEST includes tests and documentation; their changed bytes must occur in
the new sdist. The wheel excludes these test/doc trees, but its content and
metadata still require fresh validation and binding. No optional README edit
is included. Use new external evidence to bind actual final commit/tree/source,
build tools, artifact bytes and validation/inspection results. Do not insert
future artifact hashes or self-hashes into already-tested source documents.
If source changes after building, the old build cannot be described as a build
of the later tree; refresh the affected candidate work before selecting a pair.

#### D22-M1e. Readiness, findings and publication

Refresh the applicable source, distribution and new-commit history inspections
and release-claim reconciliation for the selected corrected candidate. Preserve
the historical disposition ledger; prior dispositions are not automatic approval
of new or changed findings, and previous commit-metadata acceptance does not
approve metadata of future commits. Carry unchanged evidence forward only with
its explicit input identities and scope. Do not rerun scientific campaigns.
The existing release report remains a historical reviewed report; current
readiness is reconciled through new external bindings and review, not a
self-referential rewrite of that report or its old findings.

The author's completed README observation applies to the unchanged README
identity; it is not a claim about future edits or a retroactive change to the
old closure checkpoint. Private notes are outside all helpers and gates. The
lifting of closure-specific operational holds does not permit mutation of
historical evidence or automatic package execution. Every new execution follows
review, explicit adoption and controlled placement/execution; Downloads is the
arrival location, not the permanent execution home.

Readiness remains INCOMPLETE until the corrected-source, artifact and final
readiness obligations are satisfied and reviewed. Publication remains a
separate explicit author act naming exact artifact(s), version and destination.
This authority itself performs no test edit, build, remote action or publication.
