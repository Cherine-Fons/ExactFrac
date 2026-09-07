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
