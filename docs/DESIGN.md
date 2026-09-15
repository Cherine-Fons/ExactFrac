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
