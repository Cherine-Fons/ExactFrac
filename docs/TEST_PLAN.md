# ExactFrac Prospectively Specified Test Plan

Status: LIVING PROSPECTIVE ENGINEERING TEST SPECIFICATION

This living document records implementation, regression, adversarial, and isolation
tests. Each obligation is added before the corresponding implementation unit is written;
historical sections remain as evidence after their code lands.

It is not a mathematical authority.

Mathematical authority remains with the current frozen source pinned by `SPEC_LOCK.md`
and the mathematical requirements summarized by `CONTRACT.md`.

`ORACLE_CATALOG.md` contains independently hand-derived expected answers.

`CONFORMANCE.md` maps theorem obligations to the tests that actually discharge them as
those tests land.

This test plan serves a different purpose: it prospectively specifies what correct
implementation behavior must be challenged before implementation choices can influence
the tests.

---

## 1. Testing principles

### TP1 — Oracle before implementation

Expected mathematical answers are derived independently before the implementation that
will later be tested against them.

Implementation output must never be used to create or revise an oracle answer.

### TP2 — Independent verifier

The reference brute verifier lives in `exactfrac_verify`.

It imports nothing from `exactfrac`.

Its exhaustive search is derived directly from the compact definition.

It must not know about:

- transformed branches;
- atomic-family decompositions;
- parity-cut reductions;
- Newton updates;
- `ExactBranchMin`;
- `SolveBranchStandard`;
- `SolveBranchAccelerated`;
- `StrongCompactMSPD`.

### TP3 — Exact arithmetic only

No correctness test may depend on floating-point arithmetic or numerical tolerance.

Rational equality and ordering are exact.

The independent verifier and tests may use `fractions.Fraction`.

The production solver later uses the raw exact arithmetic policy defined in DESIGN §4.5.

### TP4 — Guard isolation

A test intended to exercise guard or condition \(k\) must satisfy all logically earlier
guards.

A test does not count as evidence for a later condition if it is already rejected by an
earlier one.

### TP5 — Value correctness is not enough

Where the API promises a witness or an empty state, tests must verify the complete result
state.

A test must not pass merely because the numerical value is correct while:

- an exception was wrongly raised;
- a fake witness was manufactured;
- an invalid witness was returned;
- an empty flag was trusted incorrectly;
- a witness was silently detached from the claimed value.

### TP6 — Determinism is tested separately from mathematical freedom

Where the mathematics permits multiple correct outputs, tests distinguish:

1. mathematical correctness of every legal output;
2. deterministic behavior of the shipped implementation.

Tests must not convert an implementation-level deterministic convention into a stronger
mathematical claim.

### TP7 — No implementation self-certification

Solver tests may use the independent verifier and hand-derived oracle catalog.

The verifier must not use solver code.

Certificate verification must independently check its declared contract and must not
trust solver-produced metadata merely because the solver produced it.

---

## 2. Seed-oracle test obligations

The following three oracle cases were derived and committed before implementation.

They are the first mandatory known-answer fixtures.

### ORACLE-001 — valid active Q=1 empty family

Classification:

`GLOBAL_ORACLE`

Expected mathematical result:

- value: `(0, 1)`
- witness: `Empty`

The corresponding implementation tests must verify more than the numerical value.

Required behavior:

1. instance construction succeeds;
2. the active condition is satisfied;
3. no `UnsupportedInstance` exception is raised;
4. the exact result value is `(0, 1)`;
5. the witness state is genuinely empty;
6. no shore is manufactured;
7. no `y` vector is manufactured;
8. the result is represented as a valid mathematical empty-family state, not as an error
   or rejection state.

This obligation is intentionally adversarial.

A future implementation that returns value zero while fabricating a dummy witness does
not pass.

A future implementation that rejects the valid instance does not pass.

### ORACLE-002 — constructive unit lower-bound witness

Classification:

`LOCAL_CONTRACT_FIXTURE`

Expected local fixture:

- shore: `[2]`
- dense `y`: `(0, 1, 0)`
- sparse `y`: `[[1, 1]]`
- raw value: `(2, 2)`
- mathematical ratio: `1`

Required behavior:

1. the constructed pair is admissible;
2. the selected positive `y` coordinate lies on the shore boundary;
3. every nonboundary coordinate is zero;
4. the dense and sparse representations encode the same mathematical object;
5. the raw value is `(2, 2)` rather than silently normalized;
6. the mathematical value is exactly \(1\);
7. the fixture is not treated as a global-optimum oracle.

The same instance contains a separately hand-derived admissible competitor of raw value

`(4, 2)`

and mathematical ratio \(2\).

That competitor is used only to prove that the unit witness is not globally optimal.

No test may promote the value \(2\) to a claimed global optimum without an independent
global proof.

### ORACLE-003 — direct H2 endpoint

Classification:

`BRANCH_ORACLE`

Expected H2 fixture:

- shore: `[0]`
- dense `y`: `(2,)`
- sparse `y`: `[[0, 2]]`
- raw value: `(4, 2)`
- mathematical ratio: `2`
- endpoint: `H2`

Required behavior:

1. recognize the H2 condition \(f(v)=1\) and \(d_q(v)\ge2\);
2. distinguish the direct H2 endpoint from the four transformed branch solvers;
3. interpret `q_0 = 2` as two individually selectable copies;
4. permit the compact count `y_0 = 2`;
5. preserve canonical implicit `edge_ref = 0`;
6. reconstruct the exact H2 witness;
7. return raw value `(4, 2)`;
8. preserve the `BRANCH_ORACLE` scope of the claim.

---

## 3. Empty-state adversarial test family

The empty-state contract is tested across several layers.

These cases are pre-registered now so that a future implementation cannot weaken the
tests to match its own behavior.

### E1 — valid active Q=1 instance

Expected:

- construction succeeds;
- no unsupported-instance exception;
- exact value `(0, 1)`;
- no witness;
- no shore;
- no `y`.

### E2 — forged empty certificate carrying witness data

Input state:

- certificate claims empty;
- certificate also carries `U` and/or `y`.

Expected:

- certificate verifier rejects.

An empty mathematical result must not contain a fabricated witness payload.

### E3 — nonempty certificate state with no witness

Input state:

- certificate does not claim empty;
- witness payload is absent.

Expected:

- certificate verifier rejects.

A nonempty result requires an attaining compact witness.

### E4 — false empty claim on a nonempty admissible family

Input state:

- valid active instance;
- \(Q>1\);
- certificate claims the admissible family is empty.

Expected:

- certificate verifier rejects.

For a validated active instance, the verifier must independently establish the empty
condition rather than trusting the certificate's `empty` flag.

This test is deliberately designed to catch a result whose serialized state looks
plausible but whose mathematical claim is false.

---

## 4. Instance-validation test family

The canonical instance representation must be tested independently of later optimization
logic.

Pre-register the following classes.

### I1 — valid canonical instance

Expected:

- construction succeeds;
- dense vertex indexing is established;
- canonical support-edge order is established;
- multiplicities and capacities are immutable exact integers.

### I2 — repeated endpoint records

Input contains repeated records for the same unordered support pair.

Expected:

- normalize endpoints;
- aggregate multiplicities;
- produce one canonical support edge;
- preserve total multiplicity exactly.

### I3 — reversed endpoint orientation

Input includes an edge record with \(u>v\).

Expected:

- normalize to canonical orientation \(u<v\);
- do not create a second distinct support edge merely because endpoint order differs.

### I4 — loop

Input contains \(u=v\).

Expected:

- reject as malformed/invalid input;
- do not classify the failure merely as an active-condition failure.

### I5 — empty support

Expected:

- reject.

The governing problem requires a finite nonempty loopless support graph.

### I6 — nonpositive multiplicity

Input has `q_e <= 0`.

Expected:

- reject.

### I7 — nonpositive f value

Input has `f(v) <= 0`.

Expected:

- reject.

### I8 — active-condition failure

Input is otherwise structurally valid but some vertex satisfies

\[
f(v)>d_q(v).
\]

Expected:

- reject as unsupported by the active ExactFrac regime.

This case must be distinguished from malformed graph input and from a valid instance with
an empty admissible family.

### I9 — deterministic canonical edge order

Provide equivalent input records in different external orders.

Expected:

- both construct the same canonical support-edge list;
- the same implicit `edge_ref` values result.

### I10 — production exception taxonomy and validation precedence

For the production graph-instance layer, malformed input and unsupported active-regime
input are different states.

Expected:

- `InvalidInstance` and `UnsupportedInstance` are distinct sibling subclasses of
  `ValueError`;
- malformed type, shape, format, endpoint, loop, order, multiplicity, `f`, label, and
  empty-support conditions raise exactly `InvalidInstance`;
- only a structurally valid instance with some `f[v] > d_q[v]` raises exactly
  `UnsupportedInstance`;
- malformed validation precedes the active check, so malformed input is never relabeled
  unsupported;
- a structurally valid graph with an isolated vertex and positive `f` is an
  `UnsupportedInstance` seed;
- the sealed flow layer's local `TypeError`/`ValueError` boundary is unchanged.

Tests that distinguish these cases must check the exact exception class (for example,
`type(exc.value) is InvalidInstance`), not merely `pytest.raises(ValueError)`.

### I11 — exact Python domain and compact multiplicity model

For `Instance(...)` and `Instance.from_records(...)`, exercise exact-type and shape
boundaries before normalization or the active check.

Expected:

- numeric instance data has exact built-in type `int`; reject `bool`, integer subclasses,
  floats, `Fraction`, and implicit coercion;
- Python edge/record containers, edge/raw records, and `f` are exact tuples;
- every edge record has exactly three entries `(u, v, q_e)`;
- reject a fourth edge-weight field and every real/rational or other non-integer `q_e`;
- `q_e <= 0` is invalid;
- `f(v) <= 0` is invalid;
- compact multiplicity remains a count of individually selectable unit copies and is never
  expanded into explicit copies.

### I12 — canonical constructor versus raw normalization

Provide one hand-derived mathematical instance in canonical form and in several reversed,
repeated, and permuted raw-record forms.

Expected:

- `Instance(...)` accepts only the canonical edge_ref-ordered form and rejects reversed,
  repeated, or out-of-order edge triples rather than repairing them;
- `Instance.from_records(...)` validates raw records, rejects loops, normalizes endpoint
  orientation, aggregates repeated unordered pairs by exact addition, and sorts the
  resulting support edges lexicographically;
- all equivalent raw orders produce the same canonical `Instance` and edge_ref sequence;
- the hand-derived `m`, `support_edges`, `q`, `Q`, and `d_q` values are exact;
- no independently mutable derived graph state exists.

### I13 — strict versioned instance-object round trip

Expected:

- `to_dict()` emits the `exactfrac-instance/1` object described in DESIGN §9;
- edges, `f`, and optional labels are JSON-ready lists while the canonical Python object
  remains immutable;
- `Instance.from_dict(instance.to_dict()) == instance`;
- `from_dict` validates canonical edge order and rejects rather than repairs reversed,
  repeated, or out-of-order serialized edges;
- unknown keys, missing keys, a wrong format value, a wrong outer type, or wrong serialized
  container types raise exactly `InvalidInstance`;
- JSON text/file I/O is outside this unit.

### I14 — labels are nonalgorithmic metadata

Construct otherwise identical instances with labels absent and present.

Expected:

- labels are absent or an exact tuple of pairwise distinct exact `str` or exact `int`
  values aligned to dense vertex order;
- reject `bool`, duplicates, wrong length, and all other label types;
- labels survive the object-level dictionary round trip;
- labels do not change `edges`, `q`, `f`, `Q`, `d_q`, or any edge_ref;
- raw edge endpoints remain dense integer indices;
- no graph-representation behavior depends on label values.

### I15 — production module surface, immutability, and isolation

Expected:

- `exactfrac.instance.__all__` is exactly `Edge`, `Instance`, `InvalidInstance`, and
  `UnsupportedInstance`;
- `exactfrac.__init__` remains export-free in this unit;
- `Instance` is frozen and slotted;
- its authoritative fields are `n`, `edges`, `f`, and optional `labels`;
- production instance code imports nothing from `exactfrac_verify`;
- no shore, family, witness, arithmetic, argmin, sign-routing, parity-cut, branch, or global
  solver API is introduced by this unit.

---

## 5. Shore-representation test family

The internal shore representation is an integer bitmask.

Pre-register:

### S1 — membership

For selected masks, membership agrees exactly with the represented vertex subset.

### S2 — cardinality

`U.bit_count()` equals the number of represented vertices.

### S3 — intersection parity

For known masks \(U,T\),

\[
(U\mathbin{\&}T).bit_count()\bmod2
\]

matches the hand-derived parity of \(|U\cap T|\).

### S4 — complement

Complement is taken relative to `full_mask`.

Bare Python `~U` is never accepted directly as a valid shore.

### S5 — out-of-range bits

A shore containing any bit outside `0..n-1` is invalid.

### S6 — serialization round trip

Internal bitmask

→ sorted vertex-index list

→ reconstructed bitmask

must return the identical shore.

### S7 — production public surface and plain error boundary

Expected:

- `exactfrac.shore.__all__` is exactly `Shore`, `full_mask`, `validate_shore`,
  `shore_from_list`, `shore_to_list`, and `shore_complement`;
- `Shore` is the alias `int`;
- `exactfrac.__init__` remains export-free in this unit;
- every malformed public input raises the exact built-in class `ValueError`, not
  `TypeError`, `InvalidInstance`, or `UnsupportedInstance`;
- exception messages are not asserted as stable API.

### S8 — exact universe, empty shore, and full shore boundaries

Expected:

- `n` must have exact built-in type `int` and satisfy `n >= 1`;
- `full_mask(n) == (1 << n) - 1`;
- `0` is a valid empty shore;
- `full_mask(n)` is a valid complete shore;
- nonemptiness is not imposed by the generic shore layer;
- negative masks and masks above `full_mask(n)` are rejected;
- `bool`, integer subclasses, floats, `Fraction`, and coercible non-integers are rejected
  as `n` or shore values.

### S9 — strict canonical list decoding and detached encoding

Expected:

- `shore_from_list(n, vertices)` requires an exact built-in list;
- every member is an exact built-in integer in `0..n-1`;
- member indices are strictly increasing;
- the decoder rejects duplicates, descending or unsorted input, tuples, list subclasses,
  `bool`, out-of-range members, and implicit coercion rather than repairing them;
- `[]` decodes to `0`;
- `shore_to_list(n, U)` returns a fresh exact built-in list in increasing order;
- mutating an emitted list cannot alter the integer shore.

### S10 — exhaustive finite-universe identities

For every shore in each exhaustively tested small universe and for selected pairs `U,T`,
verify:

- membership agrees with the represented subset;
- `U.bit_count()` is the exact cardinality;
- `U | T` and `U & T` represent union and intersection;
- `(U & T).bit_count() & 1` is the exact intersection parity;
- `shore_complement(n, U) == full_mask(n) ^ U`;
- complement is an involution;
- `U & shore_complement(n, U) == 0`;
- `U | shore_complement(n, U) == full_mask(n)`;
- validating bare `~U` fails.

### Production shore coverage interpretation

The historical obligations S1--S3 describe the semantics of the chosen integer-bitmask
representation on already validated masks. Their tests are executable documentation and
regression checks of Python integer operations; they do not claim that `exactfrac.shore`
provides separate membership, cardinality, or parity wrapper functions. S4--S6 are the
direct public-helper obligations for relative complement, range validation, and strict
serialization. S7--S12 add the production API, typing, isolation, exactness, and complexity
boundaries around those helpers.

| Obligation group | What the tests discharge |
|---|---|
| S1--S3 | representation-level identities on already validated integer masks |
| S4--S6 | direct `exactfrac.shore` validation, complement, and serialization behavior |
| S7--S12 | production surface, exact typing, isolation, deterministic source discipline, and complexity boundaries |

### S11 — module isolation and responsibility boundary

Expected:

- production shore code is standard-library only;
- importing `exactfrac.shore` imports no `exactfrac_verify` module;
- the module does not import `exactfrac.instance`;
- it exposes no graph-dependent `f(U)`, `e_q(U)`, `b_q(U)`, or `d_q(U)` helper;
- it introduces no family, witness, certificate, rational-pair, argmin, sign-routing,
  parity-cut, branch, or global-solver API.

### S12 — exactness, deterministic source discipline, and large universe

Expected:

- the source contains no `Fraction`, float literal, `float(...)`, true division, or
  tolerance comparison;
- no algorithmic ordering is derived from iteration over a Python `set`;
- for `n = 4096`, the mask with members `0`, `2048`, and `4095` round-trips exactly;
- `full_mask(4096).bit_length() == 4096`;
- the implementation does not enumerate all `2^n` shores or iterate once per numeric mask
  value merely to validate, complement, encode, or decode one shore.

---

## 6. Compact-witness representation test family

The dense internal `y` vector is an embedding of a mathematically boundary-indexed
object.

Pre-register:

### W1 — correct length

Dense `y` has length exactly \(m\).

### W2 — integer counts

Every coordinate is an exact integer.

### W3 — count bounds

For every support edge,

\[
0\le y_e\le q_e.
\]

### W4 — nonboundary forced zero

If support edge \(e\) does not cross \(U\), then

\[
y_e=0.
\]

### W5 — sparse export

Sparse export contains:

- only positive counts;
- strictly increasing `edge_ref` values;
- no duplicate references;
- only in-range references.

### W6 — sparse/dense round trip

Dense witness

→ sparse export

→ dense reconstruction

must preserve the exact mathematical `y`.

### W7 — raw witness-attaining value

For a nonempty admissible witness,

\[
N=2(e_q(U)+Y(y))
\]

and

\[
D=f(U)+Y(y)-1.
\]

The serialized raw pair must satisfy those identities exactly.

An equivalent reduced fraction is not a substitute for the ruled raw production pair.

---

## 7. Independent brute-verifier test family

The first implementation module is the exhaustive compact verifier.

Its tests must prove that it implements the definition directly.

### B1 — no solver imports

`exactfrac_verify` imports nothing from `exactfrac`.

This is an architectural test, not merely a convention.

### B2 — exhaustive nonempty-shore enumeration

For \(n\) vertices, the verifier considers exactly the nonempty shores permitted by the
definition.

### B3 — boundary-only compact enumeration

For a fixed shore \(U\), only boundary-support counts vary.

Nonboundary counts are structurally zero.

### B4 — exact admissibility

The verifier independently checks:

- nonempty shore;
- boundary-supported `y`;
- count bounds;
- odd \(f(U)+Y(y)\);
- lower bound \(f(U)+Y(y)\ge3\).

### B5 — exact objective

For every admissible compact pair,

\[
\rho(U,y)
=
\frac{2(e_q(U)+Y(y))}
     {f(U)+Y(y)-1}.
\]

Verifier arithmetic uses exact rational arithmetic.

No float or tolerance appears.

### B6 — Oracle 001 reproduction

The verifier reproduces the exact empty-family result.

It must satisfy the complete E1 behavior, not only numerical equality.

### B7 — Oracle 002 local cross-check

The verifier confirms that the Oracle 002 witness is admissible and attains mathematical
ratio \(1\) by exact rational-value comparison, not by raw-pair identity.

In particular, the ruled raw witness-attaining value is `(2, 2)`. A test must not expect
the reduced pair `(1, 1)` merely because both represent the same mathematical value.

This requirement is consistent with W7: witness serialization preserves the exact raw
numerator and denominator generated by the witness formulas, while mathematical equality
and ordering are checked by exact rational comparison.

The verifier may discover a better global witness.

Such a discovery must not be treated as a contradiction because Oracle 002 is local.

### B8 — Oracle 003 H2 witness cross-check

The verifier confirms that the Oracle 003 compact witness is admissible and attains
mathematical ratio \(2\).

The verifier is not allowed to know that the witness is called H2.

It sees only the compact definition.

### B9 — deterministic maximizing witness policy

If multiple global maximizing witnesses exist, the brute verifier may return one
deterministically according to its own documented enumeration order.

Tests must compare the exact optimum and admissibility/attainment unless a fixture
independently proves a unique maximizing witness.

Current coverage note: none of the three seed oracles establishes a global optimum with
multiple distinct maximizing witnesses.

Therefore this obligation must not be marked exercised merely because the verifier is
deterministic on the seed catalog.

Before B9 counts as covered, add a hand-derived global-quotient-tie fixture to
`ORACLE_CATALOG.md` that proves:

- the exact global optimum;
- at least two distinct admissible witnesses attain that optimum;
- witness identity is therefore not part of the mathematical correctness contract.

That future fixture should be derived independently before the test that consumes it.

---

## 8. Future atomic-family tests

These are pre-registered now but are not implemented in the brute-verifier unit.

### F1 — I and O overlap

If

\[
I\cap O\ne\varnothing,
\]

the atomic family denotes the empty family.

It is not malformed program state.

### F2 — free terminal toggles parity

If a terminal in

\[
T\setminus(I\cup O)
\]

is free, both parity choices are attainable.

### F3 — no free terminal

If no terminal is free, nonemptiness is determined exactly by the forced parity

\[
|I\cap T|\equiv\pi\pmod2.
\]

### F4 — cover, not partition

Generated atomic families cover the branch domain.

A shore may occur in more than one atomic family.

Overlap must not change the global residual minimum.

### F5 — production public surface and immutable descriptor

Expected:

- `exactfrac.families.__all__` is exactly the Ruff-sorted sequence `AtomicFamily`,
  `enumerate_atomic_families`;
- `exactfrac.__init__` remains export-free in this unit;
- `AtomicFamily` is frozen, slotted, immutable, and hashable;
- its authoritative fields are exactly `T`, `pi`, `I`, and `O`;
- the module introduces no custom exception and malformed public input raises exact
  built-in `ValueError`;
- `I & O != 0` remains valid descriptor state and does not raise.

### F6 — exact descriptor domain and one nonemptiness predicate

Reject `bool`, integer subclasses, floats, `Fraction`, negative masks, invalid parity, and
implicit coercion for direct descriptor fields.

For exhaustive small universes, compare `AtomicFamily.is_nonempty` with independent
enumeration of all valid shores satisfying

\[
I\subseteq U,\qquad U\cap O=\varnothing,\qquad |U\cap T|\equiv\pi\pmod2.
\]

Expected:

- overlap `I & O != 0` always gives `False`;
- any free terminal in `T \ (I \cup O)` makes both parity choices nonempty;
- with no free terminal, nonemptiness is exactly the forced parity of `I & T`;
- no mutable empty/infeasible flag exists.

### F7 — graph-derived masks on the aggregated instance

For hand-derived active compact instances, independently compute

\[
T_+=\{v:f(v)+d_q(v)\text{ odd}\},\qquad
T_f=\{v:f(v)\text{ odd}\},
\]

\[
P=\{v:d_q(v)>f(v)\},\qquad
A=\{v:f(v)\ge2\},\qquad
W=\{v:f(v)=1\}.
\]

Expected:

- generated families carry exactly the corresponding terminal mask;
- D1 forced-in first coordinates traverse exactly the vertices of `P`;
- the D2 singleton block traverses exactly `A`;
- the D2 triple block is generated from exactly the three-subsets of `W`;
- labels do not affect any mask, descriptor, count, or order;
- no raw records are re-aggregated in this unit.

### F8 — exact four-branch return shape and enumeration order

Expected:

- `enumerate_atomic_families(instance)` returns one exact tuple of length four in branch
  order `0,1,2,3`;
- each branch component is an exact tuple;
- D0 contains its one descriptor;
- D1 order is increasing `p`, then canonical `edge_ref`, then the `u-in/v-out` orientation
  before the reverse orientation;
- D2 lists increasing `A` singletons before lexicographic increasing triples from `W`;
- D3 uses canonical `edge_ref` order and the `u-in/v-out` orientation before the reverse;
- identical calls return equal tuples with identical order.

### F9 — exact count, empty-descriptor retention, and no deduplication

For every test instance, verify

\[
R_{\mathrm{actual}}
=
1+2|P|m+|A|+\binom{|W|}{3}+2m
\]

and

\[
R_{\mathrm{actual}}
\le
1+2mn+n+\binom n3+2m.
\]

Expected:

- descriptors with `I & O != 0` remain in their ruled positions;
- duplicate descriptors remain present when the displayed source unions generate them;
- family overlap is not deduplicated through a set or any other order-changing container;
- the source expression with `n` is tested as an upper bound, not as the exact returned
  count for every instance.

### F10 — `prop:domain-decomp` equality against `prop:branch-transform`

Use several tiny active instances, including cases with:

- `P` empty and nonempty;
- `A` empty and nonempty;
- fewer than three and at least three vertices in `W`;
- descriptor overlap;
- naturally generated empty descriptors.

Enumerate nonempty shores through the independent brute-verifier layer. The independent
side of the comparison must implement the branch domains literally from
`prop:branch-transform`; it must not derive a domain from `T_+`, `T_f`, `P`, `A`, `W`, an
atomic-family union, or the production family-membership predicate.

For each nonempty shore `U`, independently compute the fixed-shore quantities

\[
s:=f(U),\qquad e:=e_q(U),\qquad b:=b_q(U),\qquad d:=d_q(U)=2e+b
\]

and then apply exactly the source definitions

\[
D_0:\ s+b\text{ odd},
\]

\[
D_1:\ s+b\text{ even},\ b\ge1,\ d-s>0,
\]

\[
D_2:\ s\text{ odd},\ s\ge3,
\]

\[
D_3:\ s\text{ even},\ b\ge1.
\]

Do not replace `d-s > 0` by membership in `P`, replace `b >= 1` by the existence of a
crossing support edge, replace `s >= 3` by the `A`/`W` decomposition, or add a family-side
prefilter to the comparator. Those equivalences belong to the proof of
`prop:domain-decomp` and are precisely what the equality test is meant to challenge.

For each branch, compare the independently evaluated `prop:branch-transform` domain with
the union of shores satisfying the generated atomic-family descriptors.

Expected:

- equality of the two shore sets for every branch and test instance;
- every source-domain shore is covered;
- no covered shore lies outside the literal source branch domain;
- the tested equality provides finite executable evidence for the proof's automatic
  side-condition claims, including the nonempty-shore convention, the exclusion of the
  impossible `D_0` endpoint `s+b = 1`, the automatic `D_1` lower endpoint, and the `D_2`
  lower bound;
- a shore may satisfy multiple descriptors;
- no preferred descriptor or partition claim is inferred.

### F11 — deterministic repetition and magnitude independence

Use otherwise identical canonical instances whose large exact `q` and `f` values preserve
the same `T_+`, `T_f`, `P`, `A`, and `W` classifications.

Expected:

- the exact descriptor tuples, order, and count remain unchanged;
- construction does not iterate once per multiplicity or capacity unit;
- optional labels do not change results;
- repeated calls are byte-for-byte structurally equal.

This is a support-and-classification-controlled regression, not a claim that arbitrary
changes in numerical magnitudes preserve the derived masks.

### F12 — isolation, exactness, and source discipline

Expected:

- production family code imports only standard-library modules plus
  `exactfrac.instance` and `exactfrac.shore`;
- importing `exactfrac.families` imports no `exactfrac_verify` module;
- the source contains no `Fraction`, float literal, `float(...)`, true division, or
  tolerance comparison;
- no output order or control-flow order is derived from iterating a Python `set`;
- no multiplicity is expanded into explicit copies;
- the module defines no sign-routing, parity-cut, residual-argmin, branch-iteration,
  witness, certificate, or global-solver API.

---

## 9. Future residual-argmin tests

These tests are deferred until the branch oracle exists.

### A1 — multiple exact minimizers

Construct a fixture with multiple exact residual argmins.

Independently enumerate the complete argmin set.

Every member must:

- have the same minimum raw residual;
- satisfy the branch-domain requirements;
- supply the theorem-valid supergradient.

### A2 — deterministic first encountered

The shipped implementation retains the first encountered residual minimizer under the
fixed family enumeration.

Equal residual does not replace the incumbent.

### A3 — forbidden max-h tie-break regression

Include a fixture where the first encountered residual minimizer does not maximize
\(h_j\).

Expected:

- implementation still returns the first encountered residual minimizer.

This test fails if the removed max-\(h_j\) scalarization is accidentally resurrected.

### A4 — tie-policy independence

On tiny fixtures, inject different legal argmin choices.

Expected:

- each oracle choice is mathematically legal;
- branch invariants remain valid;
- completed branch solve reaches the same exact branch optimum.

Intermediate trajectories, iteration counts, and attaining witnesses may differ.

---

## 10. Future exact-arithmetic and bit-growth tests

### R1 — denominator positivity

Every production rational representation maintains positive denominator.

### R2 — cross-multiplication equality

Equivalent raw rational pairs compare equal mathematically even when tuple values differ.

Example:

`(2,2)` and `(1,1)` represent the same mathematical value.

### R3 — no Fraction in solver path

The production solver does not use `fractions.Fraction`.

### R4 — no floating point in correctness path

No correctness decision depends on `float`.

### R5 — magnitude-independent operation-count structure

On constant-support instances with growing binary multiplicity magnitude, record algorithm
operation counters separately from arithmetic bit lengths.

Tests must detect accidental explicit multiplicity expansion or magnitude-controlled
iteration.

A finite experiment is regression evidence, not a proof of strong polynomiality.

---

## 11. Certificate-verifier adversarial tests

These tests are deferred until the certificate verifier is implemented but are
pre-registered now.

### C1 — valid nonempty certificate

Expected:

- accept only when witness is admissible;
- raw `N,D` exactly match the witness formulas.

### C2 — nonboundary sparse y reference

Expected:

- reject.

### C3 — duplicate sparse edge_ref

Expected:

- reject.

### C4 — unsorted sparse edge_ref list

Expected:

- reject.

### C5 — count exceeds multiplicity

Expected:

- reject.

### C6 — forged raw numerator

Expected:

- reject even if the represented rational happens to equal the true value after
  reduction.

The ruled certificate contains the raw witness-attaining numerator.

### C7 — forged raw denominator

Expected:

- reject.

### C8 — fake empty witness payload

Expected:

- reject per E2.

### C9 — missing nonempty witness

Expected:

- reject per E3.

### C10 — false empty claim

Expected:

- reject per E4.

---

## 12. Determinism and reproducibility tests

### D1 — no algorithmic iteration over Python set

Algorithmic enumeration order must be explicit and reproducible.

### D2 — repeated-run determinism

Same instance, same code version, same deterministic backend:

- same returned deterministic result;
- same deterministic algorithm statistics.

Environmental metadata such as wall-clock time is excluded from deterministic equality.

### D3 — generator seeds

Any generated experimental instance family uses an explicit recorded seed.

---

## 13. Test naming and theorem conformance

`TEST_PLAN.md` records intended behavioral coverage.

`CONFORMANCE.md` records theorem obligations and the actual tests that discharge them.

A planned test does not become theorem-discharge evidence merely because it appears in
this document.

When a test lands and passes:

1. verify that it actually tests the intended obligation;
2. add or update the corresponding `CONFORMANCE.md` row under R11;
3. record the test path and test name exactly;
4. do not mark an obligation complete on the basis of a planned or skipped test.

The existing `CONFORMANCE.md` rows remain authoritative for their currently recorded
theorem labels.

This plan may introduce additional adversarial tests without changing the mathematical
meaning of those theorem obligations.

---

## 14. First implementation gate — brute verifier

Before `exactfrac_verify/brute.py` counts as complete, all applicable tests in Sections
2 through 7 must be implemented and green.

At minimum, the first verifier unit must demonstrate:

1. complete independence from `exactfrac`;
2. exact enumeration from the compact definition;
3. exact admissibility;
4. exact rational objective evaluation;
5. correct empty-family behavior from Oracle 001;
6. correct local verification of the Oracle 002 witness;
7. correct local verification of the Oracle 003 witness;
8. deterministic behavior;
9. no floating-point correctness path.

Only after the independent verifier is green may solver-side algorithmic implementation
begin.

---

## 15. Prospective-specification history

The original version of this test plan was committed as `e88861b` after the three seed
mathematical oracles and before implementation of the independent brute verifier.

At that historical version:

- no ExactFrac verifier implementation existed;
- no ExactFrac solver implementation existed;
- no branch oracle implementation existed;
- no production certificate verifier existed.

Those verifier expectations were therefore fixed before the corresponding code was
available to influence them.

The independent brute verifier subsequently landed in commit `ffcb0cf`.

The Stage-2A obligations below are added by the V2.2 repository-authority activation unit
before any flow-specific oracle, `tests/test_flow.py`, or `exactfrac/flow.py` exists.

At the time of this V2.2 revision:

- the independent brute verifier exists and is green;
- no flow-specific oracle has been committed;
- no flow test file exists;
- no flow implementation exists;
- no sign-routing, atomic-family, parity-cut, branch, or global solver implementation
  exists.

Thus Sections 16 and 17 are prospectively specified for the exact directed minimum-cut
primitive. Expected numerical answers and deterministic traces must still be hand-derived
and committed before the tests that consume them.

---

## 16. Stage-2A prospective exact-flow test family

These obligations apply to the required in-repo Edmonds–Karp backend in
`exactfrac/flow.py` and its tests in `tests/test_flow.py`.

Before any flow test body is written, the numerical fixtures and expected answers must be
derived independently and committed to `ORACLE_CATALOG.md`. They are local primitive
fixtures, not `GLOBAL_ORACLE` claims about a complete ExactFrac optimization instance.

### FL1 — exact directed-network input domain

The tested backend accepts a finite directed network with distinct in-range source and
sink vertices and exact nonnegative integer arc capacities.

Expected:

- `E = 0` is valid;
- negative capacities are rejected;
- floating-point, `Fraction`, Boolean, and other non-`int` capacity objects are rejected;
- endpoint indices outside the vertex universe are rejected;
- the backend does not invent a reverse-capacity arc merely because a forward arc exists.

The exact loop and repeated-directed-pair normalization boundary must be ruled and recorded
before the RED tests are written. No flow implementation may precede that ruling.

### FL2 — zero-arc totalization

For `N >= 2`, distinct source and sink, and `E = 0`, expected:

- construction and solve succeed;
- exact minimum value `0`;
- returned source shore is exactly `{s}`;
- the source shore is the inclusionwise-minimal minimum source shore;
- `augmentations == 0`;
- `bfs_scans == 0`;
- no empty-set maximum is evaluated;
- the zero-safe convention gives `u_max = 0` and `l = 0`.

The operation carrier is `O(N)`, which is the `E = 0` specialization of
`O(N + NE^2)`.

### FL3 — positive-arc known-answer network

At least one hand-derived network with `E >= 1` must fix:

- exact maximum-flow/minimum-cut value;
- exact returned inclusionwise-minimal source shore;
- a deterministic shortest-augmenting-path trace under the fixed adjacency order;
- exact `augmentations` and `bfs_scans` values for that fixture.

The returned cut capacity, recomputed from the original directed arcs, must equal the
reported value.

### FL4 — positive arc set with all capacities zero

Use `E >= 1` with every arc capacity equal to zero.

Expected:

- exact value `0`;
- returned source shore `{s}`;
- zero augmentations;
- deterministic search counters;
- the case is not silently treated as `E = 0`, because arcs are present even though no
  positive residual capacity exists.

### FL5 — positive arcs but no residual source-to-sink path

Use a positive-capacity network in which vertices other than `s` are residual-reachable
from the source but `t` is not.

Expected:

- exact flow value `0`;
- returned source shore is the complete residual-reachable set, not automatically `{s}`;
- the cut capacity of that shore is zero;
- the result is deterministic.

### FL6 — inclusionwise-minimal minimum source shore

Use a fixture with multiple distinct minimum source shores.

Independently enumerate all source-containing, sink-avoiding shores and prove the complete
minimum-cut family.

Expected:

- exact minimum value;
- returned source shore is minimum;
- returned source shore is contained in every other minimum source shore;
- the backend does not return an arbitrary larger minimum shore.

### FL7 — directed-cut semantics

A directed cut counts an arc exactly when its tail lies in the source shore and its head
lies outside.

Tests must distinguish an arc `(u,v)` from `(v,u)` and fail any implementation that
silently treats the network as undirected.

### FL8 — reverse-residual cancellation

Include a deterministic positive-capacity fixture whose correct maximum flow requires the
residual reverse arcs created by earlier augmentations.

Expected:

- the final exact value matches independent cut enumeration;
- residual reverse capacity is usable;
- no original reverse-capacity arc is fabricated;
- the deterministic trace reaches the correct maximum rather than getting trapped by an
  earlier augmenting-path choice.

### FL9 — independent tiny-network cut enumeration

For every tiny flow fixture, independently enumerate every shore `S` satisfying
`s in S` and `t not in S` and compute

`sum(u_a for arc a=(u,v) with u in S and v not in S)`.

Expected:

- backend value equals the exact enumerated minimum;
- backend source shore belongs to the enumerated minimizing family;
- backend source shore is the inclusionwise-minimal member of that family.

The comparator must not call the flow implementation or reuse its residual graph.

### FL10 — deterministic counters and result

For a fixed canonical network and fixed backend:

- repeated runs return identical value;
- repeated runs return identical source shore;
- repeated runs return identical `augmentations`;
- repeated runs return identical `bfs_scans`;
- no wall-clock value participates in deterministic equality.

Counter meanings are the DESIGN R9 definitions:

- `augmentations` counts successful residual `s`--`t` path augmentations;
- `bfs_scans` counts residual-adjacency entries inspected by all breadth-first searches,
  including the final no-path/reachability search.

### FL11 — exact arithmetic and zero-safe generated-number bound

No flow correctness decision may use floating point, tolerance, or `Fraction`.

For arc set `A`, define

`u_max = max({0} union {u_a : a in A})`

and

`l = ceil(log2(u_max + 1))`.

The tests independently check, including at `E = 0`,

`1 + sum(u_a) <= (E + 1)(u_max + 1) <= (E + 1)2^l`.

Every instrumented generated flow value or residual capacity `z` must satisfy

`log2(1 + z) <= l + ceil(log2(E + 1))`.

No public backend result is required to expose mutable residual-network objects merely to
perform this test.

### FL12 — support-controlled magnitude regression

Use the hand-proved one-arc family containing only `s -> t` with capacity `2^b` while the
network support remains fixed.

Expected for every tested `b`:

- exact minimum value `2^b`;
- source shore `{s}`;
- exactly one augmentation;
- identical structural search counters under the fixed implementation path;
- integer bit lengths grow with `b`.

This flat counter trace is claimed only for this family-specific invariant path. It is a
regression test against unit-by-unit capacity expansion, not a finite proof of strong
polynomiality and not a claim that all support-controlled families have identical traces.

---

## 17. Stage-2A completion gate — Edmonds–Karp backend

Before `exactfrac/flow.py` counts as complete:

1. the flow input/normalization boundary is ruled before implementation;
2. every required flow fixture is independently derived and committed before its test;
3. `tests/test_flow.py` is written and observed RED before `exactfrac/flow.py` exists;
4. every applicable FL1–FL12 test is implemented and green;
5. the backend returns exact value and the required source shore through the R9 interface;
6. the zero-arc result and uniform `O(N + NE^2)` carrier are represented faithfully;
7. the implementation uses only exact integer arithmetic and standard-library code;
8. deterministic counter semantics are tested;
9. the `lem:ek` CONFORMANCE row is promoted from `planned` to `green` only in the atomic
   code/test/conformance unit;
10. the full repository test suite and Ruff checks pass.

No sign-routing, atomic-family, parity-cut, branch, or global-solver claim is earned merely
because the ordinary directed minimum-cut backend is green.

## 18. Post-Stage-2A production graph-instance completion gate

This unit consumes the still-unimplemented instance obligations I1--I9 and the supplemental
production obligations I10--I15 above. It does not consume or modify the historical
shore-representation obligations S1--S6.

Before `tests/test_instance.py` exists:

1. hand-derived production-instance fixtures are added to `docs/ORACLE_CATALOG.md`;
2. those fixtures cover canonical construction, raw aggregation/orientation/order,
   malformed-versus-unsupported separation, exact derived values, serialization, labels,
   and deterministic edge_ref identity;
3. no `exactfrac/instance.py` implementation output is used to establish any expected
   fixture value.

Then, in order:

4. `tests/test_instance.py` is written against those fixtures and this TEST_PLAN;
5. the intended RED state is observed while `exactfrac.instance` does not yet exist;
6. only then is `exactfrac/instance.py` implemented;
7. I1--I15, targeted tests, the full suite, Ruff with cache disabled, and an independent
   normalization/isolation audit are green;
8. the completed implementation unit adds the appropriate `def:instance` and
   `lem:aggregation` CONFORMANCE evidence; no CONFORMANCE promotion occurs before GREEN;
9. the instance code, its tests, and its CONFORMANCE update land as one atomic
   implementation commit after the earlier oracle-only commit.

The graph-instance unit does not implement shore helpers or any downstream solver layer.

## 19. Production shore-representation completion gate

This unit consumes the historical shore obligations S1--S6 and the supplemental production
obligations S7--S12 above. It does not consume or modify the witness obligations W1--W7 or
any later solver obligation.

Before `tests/test_shore.py` exists:

1. `exactfrac.shore` ownership, public surface, error boundary, and strict list schema are
   ruled and committed;
2. hand-derived shore fixtures are added to `docs/ORACLE_CATALOG.md`, covering empty and
   full shores, mixed masks, membership, cardinality, parity, relative complement, strict
   serialization, malformed inputs, and the large-universe compactness case;
3. no `exactfrac/shore.py` implementation output is used to establish any expected fixture
   value.

Then, in order:

4. `tests/test_shore.py` is written against those fixtures and this TEST_PLAN;
5. the intended RED state is observed while `exactfrac.shore` does not yet exist;
6. only then is `exactfrac/shore.py` implemented;
7. S1--S12, targeted tests, the full suite, Ruff with cache disabled, and an independent
   exhaustive small-universe/isolation audit are green;
8. the completed unit adds a concise shore-representation engineering seam note to
   `docs/CONFORMANCE.md`; no governing-source theorem label is invented merely for this
   software representation layer, and no note is added before GREEN;
9. shore code, its tests, and the CONFORMANCE seam note land as one atomic implementation
   commit after the earlier shore-oracle commit.

The shore unit does not implement graph-dependent shore sums, atomic families, witnesses,
certificates, exact rational-pair helpers, argmin policy, cut reductions, branch logic, or
the global solver.

## 20. Production atomic-family completion gate

This unit consumes the historical obligations F1--F4 and the supplemental production
obligations F5--F12 above. It does not consume or modify the residual-argmin obligations
A1--A5, witness obligations W1--W7, or any cut-reduction or branch-solver obligation.

Before `tests/test_families.py` exists:

1. the canonical V2.2 source statements fixing the nonempty-shore abbreviations
   `s`, `e`, `b`, and `d`, defining the four `prop:branch-transform` domains, defining
   `T_+`, `T_f`, `F(T,pi;I,O)`, `P`, `A`, and `W`, stating `prop:domain-decomp` and its
   proof, giving the bound `R`, and specifying `alg:global` line 1 are authenticated and
   read directly;
2. the production public surface, exact descriptor domain, one nonemptiness predicate,
   derived-mask ownership, exact four-branch return shape, and deterministic enumeration
   order are ruled and committed;
3. hand-derived family fixtures are added to `docs/ORACLE_CATALOG.md`, covering derived
   masks, every branch sequence, exact actual count versus the source upper bound,
   overlapping and empty descriptors, exhaustive nonemptiness, and tiny-instance equality
   against branch domains evaluated independently from `prop:branch-transform`;
4. no `exactfrac/families.py` implementation output is used to establish any expected
   fixture value.

Then, in order:

5. `tests/test_families.py` is written against the committed authority, family oracles, and
   F1--F12;
6. the intended RED state is observed while `exactfrac.families` does not yet exist;
7. only then is `exactfrac/families.py` implemented;
8. F1--F12, targeted tests, the full suite, Ruff with cache disabled, and an independent
   exhaustive nonemptiness/domain-coverage/isolation audit are green;
9. `prop:domain-decomp` is promoted from `planned` to `green` only after the generated
   branch unions agree exactly with the literal `prop:branch-transform` domains computed
   independently on the declared tiny active corpus;
10. family code, its tests, and its CONFORMANCE update land as one atomic implementation
    commit after the earlier family-oracle commit.

The atomic-family unit does not implement sign routing, parity-cut reduction,
`ExactBranchMin`, Standard or Accelerated branch iteration, witness reconstruction,
certificate verification, or the global solver.

## 21. Unit 08 production Witness and ExactValue supplemental obligations

This section is appended after the complete previously committed TEST_PLAN. Sections 1--20,
including the historical compact-witness section 6 (W1--W7) and the brute-verifier gate in
section 14, remain byte-for-byte unchanged. The new obligations below apply to
`exactfrac/witness.py` and `tests/test_witness.py` under DESIGN section 4.4A. They do not
rewrite the evidence used to close `exactfrac_verify.brute`.

Mathematical basis: the V2.2 source's `def:instance`, `eq:degree-identity`, `def:parameter`,
`eq:compact-density`, and exact-output/reduction boundary, together with DESIGN sections
4.4, 4.4A, 4.5, and 9. Module ownership, exact Python classes, public function names,
record equality, validation order, and error classes are software rulings, not new theorems.

### W8 — exact public surface and representation ownership

Require the exact DESIGN 4.4A.2 `__all__` tuple and the named constructors/functions with
their ruled positional/keyword interface. Package root gains no re-exports. `witness.py`
consumes the existing production Instance/shore interfaces; no existing implementation,
verifier, or certificate module is changed merely to supply these records.

Both records are frozen, slotted dataclasses without generated ordering. Witness has only
U and y as fields/slots; ExactValue has only N and D. Require no per-record __dict__, value
inside Witness, attached Instance/n/m, duplicate length, mutable cache, or empty flag.
Assignments to fields and additional attributes must fail without changing state; do not
require frozen-dataclass mutation errors to be the public-data ValueError class.

### W9 — Witness constructor is structural, not instance-aware

Require exact built-in positive-int U, exact tuple y, and exact nonnegative-int coordinates.
Reject U == 0, negative U, list/generator/sequence input, bool, float, Fraction, int/tuple
subclasses, and coercible objects without coercion. Attribute names and positional field
order are exactly U, y. Include valid high-bit U and empty-tuple constructor controls:
they establish only shape and must not be advertised as valid witnesses for an instance.

Distinct records with identical fields compare equal and have equal hashes. Construction
or comparison must not mutate fields or add an associated value. Do not use tuple length
alone as a stored substitute for the instance's canonical m.

### W10 — ExactValue raw-record identity is distinct from rational equality

Require exact built-in integer N and D with D > 0. Accept signed and zero N at this record
boundary; reject bool, subclasses, coercible values, and D <= 0. Do not repair a negative
denominator. Pin exact preservation of nonreduced and zero-numerator pairs.

Compare different raw records that represent the same rational value: their record
inequality must be preserved while an independent test-side Fraction/cross-product check
establishes numerical equality. The production module implements no numerical comparator,
arithmetic operator, generated lexicographic ordering, gcd, or implicit normalization.
Equal raw records must hash equally. Do not assert unequal hashes for unequal records or
persist literal hash integers. Numerical comparison remains Unit 09, not a hidden part of
this representation unit.

### W11 — four graph-shore sums against direct independent definitions

For tiny canonical active instances, enumerate every valid shore including mask 0 and the
full shore. Independently compute f(U), e_q(U), b_q(U), and d_q(U) from canonical records,
without calling any production witness helper on the expected-value side. Check all four
public sums and d_q(U) == 2*e_q(U) + b_q(U).

Include internal, crossing, and external support edges; singleton/full/empty shores; large
multiplicities; and differing vertex capacities. Check zero sums at U == 0 and full-shore
e_q == Q, b_q == 0, d_q == 2*Q. Instance/mask type/range rejection is tested separately.
Do not restrict these generic sum tests to admissible witnesses or only nonempty shores.

### W12 — dense-to-sparse exact export and detached state

Use independently fixed canonical edge_ref positions and hand-derived sparse output, not
only a round trip. Check exact outer/nested list types, two-element records, positive
counts only, strictly increasing refs, and omission of zero coordinates after validation.
Reject wrong tuple length/type, wrong coordinate type, negative or over-capacity counts,
and positive nonboundary counts; no invalid datum is silently omitted.

Empty/full shores accept only the all-zero selection and emit []. All-zero selections on
other shores also emit []; this output is not evidence of an Empty result. Check repeated
exports are detached: changing either the outer or a nested exported list leaves the
Witness/tuple and subsequent exports unchanged. The supplied instance and dense tuple
remain unchanged on both success and failure.

### W13 — sparse-to-dense strict decoding, round trips, and no repair

Accept only an exact list of exact length-two lists [edge_ref, count]. Reject wrong
containers/subclasses/arity, wrong integer types, negative/out-of-range refs, duplicate
refs, descending order, zero/negative/over-capacity counts, and noncrossing references.
All nonzero counts remain individually selectable copy counts, not indivisible weights.

Verify missing refs decode to zeros in an exact length-m tuple. Check both directions:
dense -> canonical sparse -> identical dense and canonical sparse -> dense -> identical
sparse. Also compare each direction with its independent literal expected result. Confirm
inputs remain unmodified even on rejection, and later mutation of source lists does not
change a previously decoded tuple. Do not normalize, aggregate, sort, or coerce malformed
sparse input into an acceptable representation.

### W14 — full admissibility validator and guard isolation

`validate_witness(instance, witness)` returns None exactly for a compact admissible witness
at that canonical active instance. Test the exact instance/Witness boundary, valid nonempty
finite-universe U, exact tuple shape and length m, coordinate types/nonnegativity, count
bounds, nonboundary forced zero, odd total f(U)+Y(y), and total >= 3.

Exercise each guard with preceding conditions satisfied. In particular, a parity seed has
total >= 3 but even; a lower-bound seed has odd total below 3. Include a structurally valid
boundary selection that converts successfully but fails full admissibility. Shape-valid
high-bit U and wrong-length y constructed independently of an instance must fail here.
Validation must not replace invalid input with a repaired witness or infer Empty from a
failure. The evaluator must reject the same inadmissible inputs rather than bypass guards.

### W15 — raw evaluation and separate value/witness records

For each independently catalogued admissible witness, recompute Y(y), internal multiplicity,
and f(U) directly. Require an exact ExactValue with N == 2*(e_q(U)+Y(y)) and
D == f(U)+Y(y)-1, not merely an equal reduced rational number. Validate D > 0 and unchanged
Witness/Instance fields. Evaluation returns a value only; it neither stores N,D inside the
Witness nor returns a new result/certificate object.

Reuse ORACLE-002's local constructive witness and competitor and ORACLE-004's two distinct
maximizers, preserving their existing classifications. Equivalent mathematical values may
come from different raw records or different witnesses; neither record equality nor one
chosen witness is a uniqueness/optimality theorem.

### W16 — zero-valued admissible witness is not an empty-family result

Before the consuming test is written, catalogue the active two-vertex instance with one
edge (0,1,3), f=(3,3), and Witness(U=1, y=(0,)). Independently derive s=3, e=0, b=3, d=3,
Y=0, odd admissibility total 3, and raw value (0,2). Treat this as a local admissible-witness
fixture, not a claimed maximizing witness. The validator must accept it; evaluation must
return ExactValue(0,2), with no reduction to (0,1) and no replacement of the witness by None.
Its sparse representation [] denotes zero selected copies, not absence of a witness.

Reuse ORACLE-001 to distinguish a true empty admissible family. Boundary selections can be
encoded/decoded at that instance, but no admissible witness exists. The new unit creates no
result-level Empty checker. Its records/conversions must not turn a zero numerator, [], or
None into proof of emptiness. DESIGN's later-result convention remains value (0,1) and no
witness for a verified Empty case; no dummy Witness(0,()) or new Empty export is introduced.

### W17 — exact rejection taxonomy and deterministic validation precedence

All malformed-data tests use exact built-in ValueError assertions, not only subclass-
accepting pytest.raises(ValueError). Exercise bool, float, Fraction, exact-type subclasses,
None, strings, and conversion-protocol objects in each applicable public-data position.
Reject production Instance/Witness subclasses and verifier/duck-typed instances as inputs.
Constructors validate only what they know; instance-keyed functions validate the consumed
instance type first. For the full validator, representation errors precede graph-dependent
constraints, which precede parity and the lower bound. Sparse errors are checked in supplied
record order as ruled. Never pin diagnostic message wording as stable API.

The test scope does not convert wrong Python call arity, attempted frozen-field mutation,
or deliberate bypass of the validated Instance constructor into a new data-validation API.

### W18 — static exactness and fresh-process isolation

Source inspection verifies the DESIGN 4.4A.14 import boundary, the explicit section 4.5.3
Fraction prohibition including witness, no float/Fraction/true-division/tolerance/gcd or
normalization correctness path, no numerical comparison operators on ExactValue, and no
algorithmic set iteration. Comments/docstrings naming forbidden techniques are not
executable uses. Approved representation comparisons are not forbidden numerical quotient
comparisons; coordinate and denominator validity checks still require integer comparisons.

In a fresh subprocess, verify import resolves to the candidate production module and does
not load exactfrac_verify or downstream family/flow/oracle/branch/solve/certificate modules
as side effects. Distinguish modules already present at interpreter startup from imports
caused by the candidate. The independent verifier remains unchanged and imports no solver
module; production validation is not reused as its independent correctness path.

### W19 — deterministic compact work, labels, and large integers

Changing only optional labels must not change any sum, converted counts, raw value, or
validation outcome. Repeated operations return identical mathematical/representation
results and do not mutate any input. Canonical edge_ref order, not a set iteration order,
controls exported sparse records.

Independently derive a constant-support fixture with a count of 1 << 4096 and raw outputs
before its test is written. Ensure every operation remains exact and retains the raw
numerator/denominator and count bits. Inspect loops and use an independent support-
controlled sweep to detect unit-copy expansion or iterations bounded by q, f, Q, Y, N, or D.
Do not assert flat wall-clock time, invented asymptotic numeric thresholds, or global strong
polynomiality from a finite sweep. Big-int bit-operation time is not a structural scan count.

### W20 — independent tiny-instance acceptance and evaluation audit

For a declared finite corpus of active tiny instances, independently enumerate nonempty
shores and all legal boundary selections via the brute layer/definition. Build the expected
admissibility decision directly from f(U)+Y(y) and the source bounds, not by calling the
production validator, conversions, or graph-sum helpers. Compare production acceptance in
both directions (no false acceptances or false rejections), and for accepted witnesses
compare the raw formula pair and test-side exact rational value.

Independently enumerate all valid masks including 0 for the generic sums and conversions;
keep that domain distinct from the nonempty witness domain. Add malformed and noncanonical
representations separately so legal-only enumeration does not hide validation defects.
Run exhaustive cases inside a manageable number of test functions with identifying failure
messages, not thousands of collected pytest items. Report actual corpus/count totals and
verify repository nonmutation; finite evidence does not replace the source proof.

### Historical obligation coverage boundary

| Historical obligation | Unit 08 production evidence | Still outside this unit |
|---|---|---|
| W1: length m | W12--W14 and instance-aware validation | Full certificate envelope/checker |
| W2: integer counts | W9, W12--W14, W17 | Independent checker remains separate |
| W3: count bounds | W12--W14 and W20 | Independent checker remains separate |
| W4: nonboundary zero | W11--W14 and W20 | Independent checker remains separate |
| W5: sparse export | W12--W13 strict representation conversion | Certificate-format assembly and JSON I/O |
| W6: sparse/dense round trip | W12--W13 literal output and round-trip checks | Full certificate round trip |
| W7: raw witness-attaining value | W15--W16 raw evaluation and preservation | W7's serialized-certificate raw-pair identity |

This mapping does not alter historical W1--W7 or retroactively change the brute-verifier
gate. No claim that full certificate serialization or independent certificate checking is
green follows from Unit 08 completion.

## 22. Unit 08 completion gate — production Witness and ExactValue

Before tests/test_witness.py or exactfrac/witness.py exists:

1. authenticate and read the pinned V2.2 compact-object/value definitions and the current
   committed DESIGN/CONTRACT/TEST_PLAN representation requirements;
2. commit the documentation-only authority: DESIGN's layout addition, section 4.4A, and
   the explicit witness addition to section 4.5.3; append this section and section 21
   without changing any prior TEST_PLAN byte;
3. derive and commit the new witness/value/conversion/rejection oracle entries, reusing
   prior oracle fixtures without changing their scope. Catalogue the zero-valued witness,
   raw-record comparison controls, strict conversion outputs, isolated guards, and large-
   integer fixture before the corresponding tests. No production output establishes an
   expected answer, and round trips alone do not define a canonical external form.

Then, in order:

4. write tests/test_witness.py against that committed authority/catalogue. Before applying
   its candidate, run the live repository Ruff configuration on its review copy through
   stdin under the target path; syntax/lint must pass. Observe the intended collection
   ModuleNotFoundError for exactfrac.witness while the production module is absent; the
   previously completed suites must remain green;
5. only then implement exactfrac/witness.py. Preflight its review copy with live Ruff before
   application; preserve the recorded test bytes unless a separately authorized repair
   establishes a genuine test defect;
6. require all W8--W20 obligations, mapped production portions of W1--W7, targeted and full
   tests, Ruff with --no-cache, and an independent tiny admissibility/value/conversion/
   isolation audit to pass. Record actual test and audit counts rather than invented totals;
7. add a narrowly scoped engineering CONFORMANCE note and test mapping only after GREEN.
   Preserve existing theorem rows, including lem:empty. Do not invent a theorem label or
   declare certificate serialization, independent checking, reconstruction, or global
   optimality verification complete;
8. stage exactly docs/CONFORMANCE.md, exactfrac/witness.py, and tests/test_witness.py for the
   atomic implementation unit after the earlier authority and oracle commits. Reproduce
   the staged tree in isolation, check candidate byte identities, commit, verify the
   committed payload, push normally, and establish remote/local identity and a clean state;
9. at full Unit 08 closure, supply the private BUILD_NOTES and LEARNING_NOTES append entries
   as two complete self-contained four-backtick Markdown blocks. Neither private note is
   staged or committed.

The Unit 08 authority commit changes only docs/DESIGN.md and docs/TEST_PLAN.md. The locked
mathematical source, SPEC_LOCK, CONTRACT, immutable GOVERNING_SHA256SUMS activation baseline,
existing oracle catalogue, CONFORMANCE, existing implementation/test files, and private
notes remain untouched by that authority commit. This gate creates no Unit 09 arithmetic,
branch/endpoint witness reconstruction, certificate envelope, independent checker, or CLI.

## 23. Unit 09 production raw rational-pair supplemental obligations

This section is appended after the complete previously committed TEST_PLAN. All bytes of
sections 1--22, including historical arithmetic R1--R5 and the Unit 08 obligations/gate,
remain unchanged. These new RP obligations govern `exactfrac/rational.py` and
`tests/test_rational.py` under DESIGN section 4.5A. Source basis: section 4.5's raw formulas;
alg:branch-min and eq:value-supergradient; alg:standard-branch and lem:standard-bits;
alg:branch and lem:bitgrowth; alg:global and cor:gcd. Software names, tuple boundaries,
errors, and ownership are prospective implementation rulings, not new mathematical results.

### RP1 — scalar ownership and exact public interface

Pin RawPair as the tuple[int, int] alias and the exact sorted __all__ from DESIGN 4.5A.2.
Check public argument order, keyword names, positional/keyword behavior, and return types.
No new rational-number class, implicit ExactValue coercion, operator overload, cache,
package-root re-export, or dependency on another production/verifier module is permitted.
Use importlib to load the not-yet-existing module in the RED candidate without suppressing
its ModuleNotFoundError. Prior test names, data, and implementation files stay untouched.
The plain tuple carrier deliberately has no runtime provenance tag: do not require nominal
rejection of an otherwise valid two-int tuple because a caller used it for another role.
Role-specific names and explicit scalar construction/extraction are caller-review obligations.

### RP2 — strict denominator positivity and literal pair preservation

Catalogue exact successful factory outputs for positive denominators with positive,
negative, and zero numerators, common factors, unit denominators, and cancellation controls.
Preserve both entries literally, including (0,B) with B > 1; no gcd or zero normalization.
The factory raises exact built-in ValueError for zero or negative denominators, for every
numerator sign; it must not negate either operand to turn rejected input into a valid pair.
Every pair-consuming function also rejects nonpositive denominators even where its final
formula could avoid reading the denominator. ExactValue's existing strict guard is unchanged.

### RP3 — exact rejection matrix and validation-before-arithmetic

For all applicable arguments, cover exact tuple shape/length, exact int fields, and
positive-denominator requirements. Reject bool, int/tuple subclasses, floats, Fraction,
lists, arbitrary sequences/iterators, None, ExactValue/Witness records, and coercible
objects rather than coercing or iterating them. Exercise invalid c/h scalar types for the
residual helper and zero/negative denominators for make_pair. Assert type(exc.value) is ValueError,
not merely a superclass match, and no input mutation. Objects with raising conversion,
comparison, iteration, or arithmetic methods should be rejected before invoking those
methods. Check the ruled validation order by source inspection and guard-isolated cases;
exception-message wording and arbitrary wrong-call-arity errors are not stable contracts.

### RP4 — mathematical comparison independent of raw-record identity

Use committed fixtures for negative, zero, and positive pairs; unequal field pairs with
equal rational value; same numerators/different denominators; close huge rational values;
and cases in which tuple lexicographic order gives the wrong numerical order. Require
compare_pairs to return exact built-in -1/0/1 matching independent Fraction comparison.
Test reflexivity, antisymmetry, transitivity, and invariance under separately multiplying
both fields of either operand by a positive factor. Tuple/ExactValue record equality is
not changed or used to define expected numerical equality. Do not assert collision-free
hashes or fixed hash integers. A numerical tie returns 0 without choosing a representative.

### RP5 — exact sign without normalization or empty-state inference

Cover negative, zero, and positive numerators with small and huge positive denominators.
Require exact built-in int returns, including for zero. Confirm validation still rejects
malformed/nonpositive denominators. Zero-valued nonempty witnesses from Unit 08 remain
witnesses when their value fields are supplied to this scalar sign/comparison interface;
no Empty result, None replacement, or rewrite of their raw ExactValue pair is allowed.

### RP6 — literal add-one and Newton reset boundary

Catalogue exact (A+B,B) outputs for pair_add_one, including A == -B and unreduced inputs.
Do not accept merely an equivalent Fraction as the expected output: zero must preserve B,
and the denominator must be the supplied denominator rather than a newly accumulated one.
Document the source distinction: Standard begins at (c+h,h); Accelerated begins at (c,h).
On synthetic sequences, a fresh standard point is a fresh (c,h), not the algebraically
expanded delta - r/g representation. This unit tests scalar building blocks only; actual
branch initialization, feasibility, and reset control flow are later integration gates.

### RP7 — literal reflected look-ahead with fixed argument roles

For newton=(A,B) and current=(C,D), require exactly (2*A*D-C*B,B*D). Include an asymmetric
case distinguishing 2*newton-current from 2*current-newton; equal denominators; equivalent
but differently encoded pairs; zero cancellation; negative output; and large signed input.
Independently check the represented value with Fraction, but assert the literal raw tuple
separately. Special-case reduction, zero normalization, swapping arguments, or returning an
existing equivalent operand must fail the test. No acceptance/rejection branch is run here.

### RP8 — exact scalar residual and parameter-dependent scaling

For parameter=(A,B), independently verify residual_numerator == B*c-A*h and
Fraction(result,B) == Fraction(c,1)-Fraction(A,B)*Fraction(h,1). c and h are arbitrary
exact signed ints at this scalar boundary; include h==0 and h<0 controls without claiming
these are feasible branch denominators. Isolate negative/zero/positive residuals with
h>0 too. If (A,B) is replaced by (k*A,k*B), k>0, the raw residual is multiplied by k,
not invariant; its represented rational value and sign are invariant. Include a fixture
showing that comparing raw residual numerators across different denominators is invalid.
Do not label this helper an optimizer, an F_j oracle, or a graph-shift correction routine.

### RP9 — explicit ExactValue bridge with Unit 08 bytes preserved

Use exact existing value records and extract their N,D fields into raw tuples at the test
call site. Numerically equal distinct records compare as 0 without becoming structurally
equal or mutating either record. Supplying an ExactValue directly to a RawPair consumer
raises exact ValueError. Constructing ExactValue from a valid pair preserves its fields
and establishes no attainment. Keep witness_value as the owner of witness-derived raw
quotients. Do not add numerical methods, imports, or API aliases to the closed witness
module. Tests may import both layers; production rational.py imports neither witness.py
nor any other project module, and the independent verifier imports no production helper.

### RP10 — finite independent arithmetic corpus

Before tests exist, define and commit bounded integer/pair domains and the precise
quantifiers for exhaustive unary, binary, residual, and selected composition checks.
Compute expected rational values by independent Fraction arithmetic and expected raw
outputs from separately justified formulas, not production outputs. Add fixed numerical
fixtures that can expose a copied-sign or operand-order error in a test-local formula.
Record actual domain sizes and totals. Execute the finite corpus inside a small number
of ordinary tests with diagnostic inputs on failure, not thousands of pytest parameters.
No finite corpus proves branch termination or the universal complexity theorems.

### RP11 — exactness, dependency isolation, and bounded primitive work

Inspect the production AST for float constants, float/Fraction conversions, division,
floor division, remainder/reduction, tolerance logic, unexpected imports, recursion, and
magnitude-driven iteration. Cover direct, named, comprehended, and derived set iteration
rather than only set literals; fixed-size validation is permitted only with a constant
bound. A fresh process importing exactfrac.rational must load no other exactfrac submodule
and no exactfrac_verify module; distinguish preloaded stdlib modules from dependencies
introduced by the import. Inspect source/import hooks for forbidden direct imports rather
than claiming that sys.modules alone proves absence of every possible runtime technique.
Mutate representative prohibited source constructs in audit-only controls where useful to
show that the static check actually detects them; no production file is altered for that.

### RP12 — large integers, literal recurrence growth, and completion limits

Catalogue very large signed numerators and positive denominators, including distinctions
that a floating-point conversion would lose. Check exact raw formulas and output types
without timing thresholds, resource cutoffs, or implementation-provided expected values.
For reflected recurrence experiments, keep each supplied standard-point operand within a
declared fixed input-size envelope while varying the current iterate as the source does.
Test literal denominator products and cancellation preservation. Do not generalize the
source's linear bit-growth recurrence to two arbitrarily growing operands; do not assert
constant bit time from constant structural work. Local raw-formula conformance does not
complete TEST_PLAN R5's later algorithm-counter experiments or the two source bit lemmas.

### Historical arithmetic coverage boundary

| Existing obligation | Unit 09 evidence | Still outside this unit |
|---|---|---|
| R1: positive denominators | RP2--RP3 validate/produce positive-denominator RawPair | Every later algorithm's maintained-state checks |
| R2: numerical equality | RP4 and RP9 explicit cross-product comparison | Tie handling and candidate selection in callers |
| R3: no Fraction in solver path | RP11 production rational.py checks | Repository-wide enforcement as later modules land |
| R4: no floating correctness decisions | RP4--RP8 and RP11--RP12 | Later cut/oracle/branch/global correctness paths |
| R5: operation counts versus bit lengths | RP11--RP12 primitive work and recurrence fixtures | Full Standard/Accelerated instrumentation and bounds |

No historical section or obligation is rewritten. Existing Witness/ExactValue representation,
raw-attainment, and independent-checker boundaries remain in force.

## 24. Unit 09 completion gate — production raw rational-pair primitives

Before tests/test_rational.py or exactfrac/rational.py exists:

1. authenticate the current Unit 08 commit and read the pinned source's exact residual,
   Standard initialization/update, Accelerated reflection/reset, and bit-growth passages;
2. adopt a documentation-only authority commit: the DESIGN layout addition, section 4.5A,
   explicit rational addition to the Fraction-prohibited module enumeration, and these
   appended TEST_PLAN sections 23--24. Preserve all prior TEST_PLAN bytes and every other
   historical DESIGN byte except the two precisely named layout/policy line amendments;
3. derive and commit the scalar arithmetic, rejection, literal-update, cancellation,
   cross-encoding residual-scaling, ExactValue-bridge, and large-integer oracle fixtures.
   Catalogue the finite audit domains and totals before their consuming tests. Expected
   answers are source/definition-derived, never copied from production execution.

Then, in order:

4. write tests/test_rational.py against the committed authority and oracles. Syntax and
   live Ruff stdin preflight under the intended target path precede applying the candidate;
   establish intended ModuleNotFoundError for exactfrac.rational while it is absent;
   all 388 previously completed tests remain green, and neither private notes file changes;
5. implement only exactfrac/rational.py after RED. Run live Ruff on the full review copy
   before application. Preserve frozen test bytes except for separately adjudicated defects;
6. require RP1--RP12, targeted and full tests, full Ruff, independent exact arithmetic
   corpus, static exactness/import isolation, and unchanged closed-module bytes to pass.
   Bind actual counts, candidate identities, and runnable audit artifacts to the result;
7. append an engineering CONFORMANCE note only after GREEN, preserving every existing
   theorem row/status. Do not promote source bit-growth or algorithm-correctness claims
   merely because the scalar arithmetic functions passed finite checks;
8. stage exactly docs/CONFORMANCE.md, exactfrac/rational.py, and tests/test_rational.py;
   reproduce that exact staged tree in isolation, verify the import origin and byte
   identities, commit atomically after the earlier authority/oracle commits, push normally,
   and establish synchronized remote/local refs and a clean worktree/index;
9. at full closure provide two private append entries in complete self-contained
   four-backtick Markdown blocks: BUILD_NOTES and LEARNING_NOTES. Never stage either file.

This authority changes only docs/DESIGN.md and docs/TEST_PLAN.md. It does not change the
canonical mathematical source, SPEC_LOCK, CONTRACT, immutable GOVERNING_SHA256SUMS baseline,
oracle catalogue, CONFORMANCE, pyproject, existing code/tests, or local private notes. No
Unit 10 reduction, branch coefficient construction, branch solver, global selector,
certificate layer, arbitrary general-purpose fraction API, or telemetry is implemented here.

## 25. Unit 10 production sign-routing supplemental obligations

This section is appended after all previously committed TEST_PLAN bytes, including sections
23--24 for Unit 09. It governs `exactfrac/sign_routing.py` and `tests/test_sign_routing.py`
under DESIGN 4.7. Mathematical sources: prop:branch-transform's c_j/h_j table;
eq:param0--eq:param3; lem:sign-routing and eq:sign-routing; the two-opposite-arcs conversion;
alg:branch-min and thm:branch-oracle. Source identities are distinct from prospective API,
record, emission-order, zero-retention, and error rulings. None of these tests may import or
call the flow backend to establish the expected sign-routing identities.

### SR1 — exact public interface and dependencies

Pin the exact sorted __all__, all signatures and keyword names from DESIGN 4.7.2, and the
two frozen/slotted records. Require the exact two record types and exact built-in scalar/
tuple result types; do not add other constructors, public Arc types, mode flags, or root
exports. Use importlib for the not-yet-existing module without suppressing its intended
ModuleNotFoundError. Allowed production imports are only dataclasses, .instance, .rational,
and optional future annotations. Static and fresh-process checks distinguish those allowed
closed dependencies from forbidden flow, families, witness, oracle, branch, solve,
certificate, exactfrac_verify, fractions, decimal, math, and third-party imports.

### SR2 — coefficient record representation and strictness

Pin fields/slots (a, gamma, constant), structural equality/hash consistency, immutability,
and no generated ordering or __dict__. Cover a==0, a>0, mixed/zero/all-negative gamma,
signed constants, empty gamma as standalone shape, and huge exact integers. Reject negative
a and wrong exact types/containers/entries with exact ValueError, without coercion. A
coefficient record has no attached instance or cached degree/shift. Test independence from
external mutable inputs by rejecting lists rather than copying/repairing them. Matching
vertex count is a builder guard, not a coefficient-constructor claim.

### SR3 — network record representation is not a semantic certificate

Pin fields/slots (vertex_count, arcs, negative_shift, constant), structural equality/hash,
frozen state, and the properties source=vertex_count, sink=vertex_count+1,
node_count=vertex_count+2. Reject malformed exact types, vertex_count<1, invalid arc shape,
noninteger fields, out-of-range endpoints, loops, negative capacities/negative_shift, and
nonscalar constant, with exact ValueError. Zero capacities and an empty arc tuple are valid
record shapes. Retain ordered repeated directed pairs without aggregation or synthesis;
no constructor sort, zero deletion, or mutation is allowed. Do not require the constructor
to certify that arbitrary supplied arcs/shift came from a particular Instance/coefficient
record. Semantic consistency is established for builder outputs by SR5--SR9. The result
record is not the future contracted-network representation.

### SR4 — hand-derived four-branch coefficients

Commit exact a, gamma tuple, and constant for each branch and selected raw parameters before
writing the test. Test the table literally, including distinct constants in branches 0/1
and 2/3, while shared gamma families remain equal. Include negative, zero, positive, unit-
and nonunit-denominator parameters, unreduced equal-value parameters, and huge signed A.
branch is an exact int in 0..3; parameter is the closed strict RawPair. Use MIXED from
ORACLE-031 and the rich five-vertex instance from ORACLE-025, plus an active d_q==f control.
Expected degrees and coefficients are derived from the fixed records, not production
properties/functions. No branch domain is required merely to build its coefficient form.

### SR5 — symmetric support-edge arcs and explicit terminal numbering

For generic a>=0, commit the complete emitted arc tuple on tiny canonical instances. In
edge_ref order, require (u,v,a*q_e) then (v,u,a*q_e); support arcs precede all spoke arcs.
No multiplicity expansion, endpoint relabeling, capacity halving, dictionary-derived order,
or extra source-sink constant edge is allowed. Original indices remain unchanged and the
auxiliary vertices are exactly source=n and sink=n+1. The directed cut evaluator in tests
counts tail-inside/head-outside, never both directions of a crossing pair and never flow
residual entries. Check all returned container, endpoint, and capacity types exactly.

### SR6 — positive, negative, zero, and all-zero spokes

Commit complete spoke tuples in increasing original-vertex order. Positive/zero gamma
uses both v->sink and sink->v arcs of gamma; negative gamma uses both source->v and
v->source arcs of -gamma. Retain zero-gamma sink spokes and a==0 support arcs. Every builder
output has n+2 nodes and exactly 2*(m+n) original directed arc records, including the fully
zero-capacity case. All-zero capacities are not an empty original arc set. Compare exact
negative_shift with the independently derived sum of negative magnitudes; constant never
changes arcs or negative_shift. Test zero, positive, negative, and huge constants.

### SR7 — coefficient identity on every shore, including empty/full

Name the coverage test `test_branch_coefficient_identity`. On the independently fixed tiny
corpus, enumerate every U from 0 through (1<<n)-1. Directly recompute s from f entries, b
from crossing support-edge multiplicities, and d from endpoint incidences in the input
records. Do not import production shore-sum functions, use instance.d_q as the expected
side, or reconstruct branch domains from families. Compute the source pairs independently:
(c0,h0)=(s+b-1,d+1-s); (c1,h1)=(s+b-2,d-s); (c2,h2)=(b-d,s-1);
(c3,h3)=(b-d-2,s). For every branch/parameter/mask, assert
B*c_j-A*h_j == a*b + sum(gamma[v] for v in U) + constant using the actual returned
coefficients on the right. Compute the left directly rather than using the production
rational residual helper as the expected oracle. These all-mask tests concern polynomial
extensions outside D_j; they assert no branch feasibility, nonempty shore, or h_j>0 there.
Do not filter masks or pass off-domain h_j as a RawPair denominator.

### SR8 — generic sign-routing identity without a minimum-cut call

Name the identity test `test_sign_routing_identity`. For every generic coefficient case and
all valid U, build the network and count crossing capacities from its actual arc tuple with
X_U=U|(1<<source), excluding sink. Independently derive Psi(U)=a*b_q(U)+sum gamma over U
from input records and supplied coefficients, and C_minus from supplied gamma. Require
cut_capacity(X_U) == Psi(U)+C_minus, independently of coefficients.constant. Test empty
and full shores explicitly: their cut capacities are respectively C_minus and the sum of
positive gamma entries. Include asymmetric shores and positive support edges so a doubled
undirected cut or omitted/opposite spoke is detected. No max-flow, min-cut, production
cut-evaluation helper, or copied construction routine supplies the expected cut value.

### SR9 — recovery with separate signs and restricted-family boundary

For each branch case and all shores, require recover_objective(network, cut_capacity)
== B*c_j-A*h_j independently. Check negative recovered values, constant==0, nonzero
negative_shift, and branches with opposite constant signs. Direct scalar controls verify
cut_value-negative_shift+constant and validation of nonnegative exact-int cut_value.
The helper establishes neither a cut identity for an arbitrary caller-built record nor
minimality or branch membership. Include a hand-derived tiny nonempty restricted shore
family whose minimum differs from the unrestricted one: test equality of shifted minima
over that SAME family by exhaustive cut counting, not by invoking a flow solver. Empty
family handling, forced contractions, parity, and Infeasible are outside this unit.

### SR10 — zero parameter, negative parameters, and active equality controls

At A=0,B=1, branches 0/1 have gamma=f and C_minus=0; branches 2/3 have gamma=-d_q and
C_minus=2Q. Under the active domain, branches 2/3 have strictly negative gamma for A>=0;
check this conditional assertion without rejecting A<0. Include A<0 cases with gamma of
all three signs and exact zero thresholds; the ORACLE-025 instance at (-2,1) is one such
anchor. Include d_q==f, where gamma for branches 0/1 remains B*f for arbitrary signed A.
Generic a==0 is supported even though branch-derived a=B is strictly positive. Catalogue
all numerical anchor values before their tests and distinguish them from domain membership.

### SR11 — exact rejection matrix and validation before construction

Cover invalid Instance/coefficient/network types, bool and record subclasses, branch values
outside 0..3, every malformed RawPair class already rejected by Unit 09, mismatched gamma
length, malformed arc records, and invalid recovery cut values. Use exact ValueError, not
just a superclass match. Verify specified field/argument validation order by source review
and guard-isolated tests; raising conversion, iterator, comparison, and arithmetic objects
must be rejected before their hooks run. Invalid constructor records are not silently fixed.
Do not test reflective bypass of frozen constructors as an ordinary supported input path.
No public consumer mutates the input Instance, coefficient record, network, or tuples.

### SR12 — deterministic raw emission and label independence

Repeated calls with identical authoritative inputs produce structurally identical records
and exact arc order. Valid relabelings of Instance metadata do not change results. The
builder preserves canonical edge_ref and increasing vertex order rather than relying on
set iteration. A generic constant-only change leaves arcs and negative_shift identical.
Input-order normalization belongs to Instance/flow, not this builder. Do not demand that
permuting a fixed network's input arcs changes its inclusionwise-minimal min-cut shore:
that unique extremal-shore contract is separate from this raw-output ordering contract.

### SR13 — finite independent corpus fixed before tests

Register finite active-instance, parameter, generic-a/gamma/constant, all-shore, and
restricted-family domains and their exact evaluation counts before tests exist. Include
MIXED, ORACLE-025, d_q==f, zero-support-capacity, all-zero network, nonzero shift, and
same-gamma/different-constant cases. Derive expected coefficient/arc/shift/recovery records
without production output; run a separate definition-level audit without production flow
or shared construction logic. Tests must compare actual production outputs with those
independent values, not merely one production operation with another. A corpus count is
finite evidence, not a theorem, resource promise, or reason to skip a source condition.

### SR14 — large integers and classification-controlled scaling

Freeze huge-integer controls including 4097-bit-class multiplicities, signed coefficients,
and raw parameter entries; test exact output fields and types without float/timing cutoffs.
For positive integer k, scaling parameter (A,B) to (k*A,k*B) scales all branch coefficients,
constant, capacities, negative_shift, and recovered raw residuals by k, while vertex/arc
positions and coefficient signs stay fixed. For generic forms the same law holds when
(a,gamma,constant) is scaled componentwise. Derive expected scaled values independently.
Do not claim raw residual magnitude invariance, or fixed source/sink spoke endpoints when
unrelated parameter changes actually change gamma signs. No magnitude or bit-length limit
is added to the API.

### SR15 — source exactness, dependency isolation, and structural operation count

Inspect imports, AST, and call structure for forbidden numerical operations, float constants,
coercion, reduction, synthetic infinity, recursion, explicit copies, all-shore enumeration,
set-valued iteration, flow calls, and magnitude-controlled loops. Allowed loops are over
canonical support edges, vertex indices, gamma entries, or supplied arc records. Obtain
d_q once, outside the per-vertex loop; reject designs that rescan all edges per vertex.
Inspect the O(n+m) construction carrier including output-record validation, and O(1)
recovery/derived-terminal properties; do not install a numeric asymptotic bound or assert
constant wall-clock time/byte memory. Fresh import may load only the allowed closed
instance/rational dependencies. Keep package-root and all closed implementation/test bytes
unchanged. In-memory prohibited-source audit controls may be used without mutating files.

### SR16 — theorem and downstream completion boundaries

The narrowly worded new lem:sign-routing row is authorized only at GREEN, mapped to
test_sign_routing_identity on production-domain inputs. test_branch_coefficient_identity
and the representation/rejection/order checks receive an engineering seam note, not a
new proof of prop:branch-transform's ratio claims. Preserve every existing CONFORMANCE
row/status. Do not mark parity-anchor/GR reduction, branch residual minimization,
argmin policy, Standard/Accelerated control flow, global solve, certificate work, or
algorithm-level bit-growth/telemetry complete. Neither a network nor its shifted scalar
value is an independent certificate of admissibility, attainment, or global optimality.

## 26. Unit 10 completion gate — branch coefficients and sign-routing

Before `tests/test_sign_routing.py` or `exactfrac/sign_routing.py` exists:

1. Authenticate the completed Unit 09 commit/tree/clean remote state and read the pinned
   source table, residual expansions, sign-routing lemma/proof, directed conversion, and
   branch-oracle shift-handling/count passages. Read the closed flow/instance/rational
   contracts without reopening their implementations.
2. Adopt a documentation-only authority commit with the new DESIGN layout line, explicit
   sign_routing addition to the Fraction-prohibited module list, section 4.7, and appended
   TEST_PLAN sections 25--26. Preserve the complete old TEST_PLAN prefix and all historical
   DESIGN bytes except the named layout/policy amendments. No oracle/CONFORMANCE/code/
   pyproject/baseline-manifest/private-note change is part of that authority commit.
3. Derive, audit, and commit the numerical/structural fixtures and finite corpus counts to
   ORACLE_CATALOG before their consuming test file. Keep all earlier oracle bytes intact.

Then, in order:

4. Write only tests/test_sign_routing.py against the adopted authority and oracles; syntax
   and live Ruff stdin checks under the intended path precede application. Observe the
   intended ModuleNotFoundError for exactfrac.sign_routing while production is absent;
   all 410 earlier tests remain green. Do not alter private notes or unrelated files.
5. Implement only exactfrac/sign_routing.py after RED, live-Ruff-preflighting its complete
   review copy before application. Keep the frozen test unchanged except for separately
   adjudicated defects; do not use source normalization to accommodate an erroneous test.
6. Require SR1--SR16, targeted/full tests, full repository Ruff, independent all-shore and
   coefficient/shift audits, source exactness, import isolation, and closed-file nonmutation
   to pass. Bind actual fixture counts, exact file identities, and runnable audit evidence.
7. Add only the narrowly scoped lem:sign-routing CONFORMANCE row and engineering seam note
   authorized above, after GREEN. Preserve every existing row/status and avoid claims of
   min-cut, parity, branch, global, or certificate correctness beyond this unit.
8. Stage exactly docs/CONFORMANCE.md, exactfrac/sign_routing.py, tests/test_sign_routing.py;
   export and test the exact staged tree in isolation, check project import origins and
   byte nonmutation, commit atomically after the authority/oracle commits, push normally,
   and verify synchronized local/remote refs and a clean worktree/index.
9. At unit closure provide exactly two self-contained four-backtick Markdown append blocks
   for private BUILD_NOTES and LEARNING_NOTES; neither notes file is staged.

No flow backend execution is required to verify the Unit 10 identities. Forced memberships,
contraction, parity anchor, terminal parity/toggling, and parity-constrained minimization
remain Unit 11/12 work, with separate authority/oracle/tests-first gates.

## 27. Unit 11 atomic-family parity-cut obligations

This supplement preserves the complete existing TEST_PLAN, including all historical
cut/argmin obligations, Unit 10 SR1--SR16, and all previous gates. It governs only
`exactfrac/parity_cut.py` and `tests/test_parity_cut.py` under DESIGN 4.8. The mathematical
basis is the pinned source's forced-contraction paragraph, lem:parity-anchor, thm:GR, and
lem:ek; the ordinary pair enumeration is made explicit by the cited primary paper's
Theorem 2, Corollary 3, and Section 5. Record source-stated facts separately from new
engineering choices. No source or previous ruling is silently replaced by a different
parity-cut algorithm.

### PC1 — exact public surface and disjoint data/diagnostic records

Pin the exact sorted __all__, constructor/function signatures, keyword names, annotations,
and read-only properties of DESIGN 4.8.2--5. Require frozen, slotted, structurally hashable
records without generated ordering or defaults. Verify separately returned result/stats;
no counter field belongs to ParityCutResult. Package root remains export-free. Instances,
families, network records, inputs, and closed code are not mutated by any new entry point.

### PC2 — original-preimage partition and explicit reduced coordinates

Register and check canonical classes for no forces, only-I, only-O, mixed forces, and all
original vertices forced. Include standalone n=1 as well as production n>=2. Require source
class first, sink class second, then increasing original singleton classes; an optional
anchor belongs only to the source class. Check complete coverage, disjointness, finite
universe, and exact types. Reject missing source/sink, swapped fixed classes, repeated or
omitted original members, a free multi-member class, out-of-order free classes, anchor in
another class, high bits, bool/subclass masks, and wrong outer containers. Constructor
failure rows must satisfy earlier guards to isolate each target failure.

### PC3 — canonical capacity and terminal-mask record guards

Register valid empty, zero, directed-asymmetric, and symmetric arc tuples. Standalone
ParityCutProblem rejects unsorted or duplicate ordered pairs instead of repairing them;
input SignRoutedNetwork may retain such raw pairs and reduction handles them. Require exact
arc tuple/triple/int types before endpoint/capacity arithmetic, valid distinct endpoints,
and nonnegative capacities. Problem terminal mask must be exact, in-range, and even; zero,
source-containing, sink-containing, and source-and-sink-containing masks are legal.
Require exact ValueError for malformed results/stats too. Result shape validation must not
be misrepresented as verification of parity, cut attainment, upper mask bound, or optimality.

### PC4 — reduction validation precedes logical infeasibility and graph access

Use hostile substitutes and controlled monkeypatches to prove network type then family
type then T/I/O range validation happen before the closed family predicate or capacity
scan. Include logically empty, out-of-universe families: range errors take precedence.
A well-shaped overlap I&O or parity-impossible family returns None, without flow or graph
construction. Spy on/use the closed AtomicFamily.is_nonempty contract; inspect the source
against duplicating its emptiness formula. Do not blanket-catch backend exceptions and
reclassify internal errors as None. Include rejection of verifier-instance and duck-typed
substitutes without invoking their iteration/conversion/arithmetic hooks.

### PC5 — literal contraction arcs, order, loops, parallels, and zeros

Hand-derive networks where source/inside and sink/outside contraction removes several
loops and combines distinct original arcs into the same directed pair. Fix the complete
emitted arc tuple, not just a cut value or multiset. Verify increasing (tail,head) order,
exact summation of each surviving pair, preservation of zero-sum encountered pairs, and
absence of invented pairs. Two opposite original arcs remain distinct ordered pairs;
never halve capacities or confuse them with residual reverse entries. Include repeated
and permuted raw input records with the same directed capacity function. Equivalent raw
orders normalize identically under the ruled contraction, without changing input bytes.

### PC6 — zero-cost anchor and XOR contraction of terminal tokens

Fix pi=0 and pi=1 variants of the same raw network/family. pi=0 contributes exactly one
isolated anchor preimage bit to the source class; pi=1 contributes none. No constraint
edge or finite infinity is introduced. Fix examples with zero, one, two, and three base
terminal tokens in a source, sink, or other class. In particular, two terminals in one
class cancel, while three leave one terminal bit. The expected contracted terminal mask
must come from counted preimages, not production output or OR of terminal memberships.

### PC7 — sink symmetric-difference toggle, including removal

Register both initially odd and even contracted terminal counts and both states of sink
membership. Odd cardinality toggles sink bit 1, including removal when already present;
even cardinality changes nothing. Source tokens are retained. Independently check that
sink toggling changes total parity but not |X intersect T| for every source/sink shore X.
Use an all-forced case producing a source token and an existing sink token, and a case
where terminal tokens cancel completely. Do not confuse even terminal-set cardinality
with even source-shore intersection parity: the target intersection is odd.

### PC8 — complete parity/forcing/cut correspondence

Implement `test_parity_anchor_correspondence`. For preregistered tiny networks and all
valid T,pi,I,O descriptors in the chosen bounded domain, enumerate all compatible original
shores independently, and enumerate all reduced source/sink shores independently. Prove
by tests the one-to-one mapping, forced membership, parity equivalence, and exact cut-value
agreement. Include empty and full original U where permitted, infeasible descriptors,
zero-capacity networks, and all-forced domains. Count actual cases and compare to the
precommitted totals. This test must not invoke minimum_parity_cut or flow to establish the
expected mapping or the expected capacities.

### PC9 — strict original-shore lifting without a parity precondition

For every fixed contraction fixture, check every reduced source/sink mask, including both
terminal intersection parities. The expected original U is the independent preimage union
intersected with the original full mask. Verify removal of source/sink/anchor bits and
return of exact int, including 0/full. Reject negative, out-of-universe, bool/subclass,
source-missing, and sink-included masks. Lifting never reads capacities or certifies a
cut value. A returned ParityCutResult still requires this conversion before Unit 12 uses
its shore as an original graph subset.

### PC10 — infeasible parity set versus zero-valued feasible minimum

For a valid problem with terminal_mask=0, require (None, zero stats) and zero backend calls.
Register even nonzero terminal masks with/without free terminals; all have a feasible odd
source/sink shore. Empty arc tuples, nonempty all-zero tuples, disconnected graphs, and
zero minimum values are not infeasibility. Cover N=2 with T=0 and T={0,1}. On all-forced
atomic families the closed predicate still decides feasibility before reduction. Do not
introduce a fake zero mask/result, artificial infinity, NaN, or Empty witness payload.

### PC11 — exact GR pair order and temporary-to-problem lifting

Freeze explicit compatible-pair sequences for N=2,3,4 (and a larger control), and require
increasing a then b, excluding a==sink, b==source, a==b only. Include (source,sink) first.
Record exact temporary contraction maps/arcs in examples where a or b is already fixed,
where both are free, and where temporary and problem vertex numbers differ. Observe one
ordinary call per compatible pair even after a zero-valued or tied incumbent is found.
Check parity only on the lifted BASE-problem shore; never interpret a temporary mask
against problem.terminal_mask. No second anchor/toggle or parity constraint is imposed
inside an ordinary call. Verify Q=N*N-3*N+3 actual calls for every valid nonzero T.

### PC12 — inclusionwise-minimal ordinary minimizers are load-bearing

For small ordinary subqueries independently enumerate all source/sink shores, calculate
all exact directed cut values, and intersect all minimizers. The real closed backend's
returned source shore must equal that intersection. Register a tie-rich zero-capacity
example with at least four free terminals: there are even arbitrary tied minima in every
compatible restriction although odd shores exist. Explain why arbitrary tie selection can
miss the parity optimum; do not use such a backend as an admissible alternative. An
in-memory wrong-backend control should make the consumer/audit fail without changing any
closed source. No epsilon, cardinality perturbation, max-denominator scalarization, or
capacity-gap argument is permitted to supply minimality.

### PC13 — independent exact parity minimum and output contract

Implement `test_minimum_parity_cut`. Over a bounded preregistered graph/terminal corpus,
independently enumerate all base-problem masks, filter source/sink membership and odd
terminal intersection, and sum original directed outgoing capacities. Compare the returned
minimum value, parity, finite mask, and attained capacity with these expected values. For
multiple optima accept exactly the first parity-valid candidate of the separately fixed GR
pair order when testing determinism; value and feasibility comparisons alone must not
invent a global lexicographic or inclusionwise-minimal parity-shore contract. Include an
ordinary minimum of wrong parity where the correct parity minimum costs strictly more.
No test expected value may be seeded from production solver/reducer/flow output.

### PC14 — deterministic ties and no early-exit shortcuts

Fix tied optima reached at multiple pair positions, repeat calls, reorder raw network arcs
before reduction, and change only original labels before Unit 10 construction. Pin the
same result and diagnostic data where the canonical problem is unchanged. Observe every
compatible pair on zero/tied graphs. Neither set iteration, mask sorting, cardinality,
branch denominators, nor stats may decide which equal-valued candidate replaces another:
strict improvement only, first valid candidate wins. A negative control that chooses the
last tie or returns early at zero must be rejected by the deterministic/call-count tests.

### PC15 — stats are exact backend aggregates and remain separate

Independently observe ordinary calls (including zero-arc ones), sum their augmentations
and bfs_scans, and take the maximum of their peak_generated_value values. Compare all
four ParityCutStats fields; no-flow returns all zero fields. Explicitly distinguish the
FLOW-ONLY peak from coefficients, normalized capacities, masks, total-cut sums, and the
later global peak_integer_bits counter. Stats are not result/certificate fields and must
never affect selection. A spying backend forwards to the real closed minimum_cut; it is
not the source of expected parity minima. Do not change closed FlowStats conventions.

### PC16 — directed/symmetric domains, scaling, and zero-safe work

Test asymmetric nonnegative directed problems as well as networks produced by Unit 10's
two-opposite-arcs representation. Hand-fix positive integer scaling cases: capacities and
minimum values scale, the least ordinary shores and chosen parity shore are unchanged,
and compatible-pair counts do not depend on magnitudes. Include very large binary
capacities and a zero-arc problem, with no float conversion, magnitude-driven loop, gcd
normalization, or test time limit. Actual backend diagnostics need not be claimed flat on
arbitrary unrelated families. Freeze the bounded corpus counts before consuming tests.

### PC17 — retained shifts and family restrictions at the integration boundary

Compose the closed Unit 10 construction with reduction, parity minimization, and lifting
on hand-derived tiny instances. Preserve the original SignRoutedNetwork for scalar
recovery; independently recompute c_j,h_j from raw instance records and evaluate B*c_j-A*h_j
on the lifted original shore. Check cut_value-negative_shift+constant equals that raw
residual exactly and minimizes over the SAME specified feasible family. Include a strictly
worse constrained minimum than the unrestricted cut and two networks with identical arcs
but different constants/shifts: parity result/stats are unchanged; recovered scalars differ.
This is a local seam test, not implementation or approval of the full ExactBranchMin loop.

### PC18 — dependency isolation, exact-source checks, and work carriers

Static checks enforce DESIGN 4.8.14's direct imports, exact arithmetic, no recursion,
no all-shore enumeration, no magnitude-driven ranges, and deterministic sorted output.
Detect float Constant nodes, true division, Fraction/gcd/epsilon/big-M shortcuts, direct or
named/comprehended set iteration, downstream/verifier/test/private-file imports, and
modified package roots. Inspect both the constructor and the per-pair path when checking
O(N+E) workspace and O(N^3*(1+E^2)) work: a constant-time recovery claim must not conceal
repeated graph construction or full network validation. Bound actual constructor work by
its input dimensions, not a hard-coded size. Fresh-process import may load the authorized
closed dependency graph, including flow and families, but no verifier/test/oracle/branch/
solve/certificate. Tests may import independent check machinery without making it a
production dependency. Preserve every closed implementation/test byte.

### PC19 — input nonmutation, independent audit, and source-level controls

Hash input tuples, records, all closed base files, and frozen tests before/after all gates.
An independent definition-level audit uses its own enumerations and cut-value evaluator,
not this consuming test module. Exercise controlled source mutations for XOR-to-OR,
sink-toggle removal, anchor omission, coordinate mixing, opposite-arc loss, wrong first
candidate, arbitrary ordinary tie selection, fake infeasibility, early zero return, and
stats misaggregation. These are in-memory/disposable controls, never changes to live source.
Pin real observed counts and limitations. A finite pass is executable conformance evidence,
not a replacement for the source proof or an independent optimality certificate.

### PC20 — narrowly scoped CONFORMANCE and downstream boundaries

After GREEN only, add lem:parity-anchor mapped to test_parity_anchor_correspondence for
atomic-family/cut correspondence on the supported network domain, and thm:GR mapped to
test_minimum_parity_cut for the exact reference parity-cut minimizer using closed least
ordinary cuts. Preserve lem:ek, lem:sign-routing, and every existing row/status. Record the
other PC obligations in an engineering seam note. Do not mark complete thm:branch-oracle,
family enumeration integration, source ratio/endpoint claims, Standard/Accelerated/global
correctness, certificates, or outer bit-growth/experiment obligations. None/zero-result
handling is local parity infeasibility, not the global Empty admissible-family result.

## 28. Unit 11 completion gate — forced contraction and exact parity cuts

Before `tests/test_parity_cut.py` or `exactfrac/parity_cut.py` exists:

1. Authenticate the completed Unit 10 commit/tree, current clean synchronized state, pinned
   source, and closed families/sign-routing/shore/flow contracts. Read the cited primary GR
   construction, including its least-minimizer requirement, and distinguish it from the
   source's no-perturbation cut implementation. Authenticate archives, source bytes, and
   any existing ordinary-cut artifacts used in the intake.
2. Adopt a documentation-only authority commit containing only the parity_cut layout line,
   explicit Fraction-policy enumeration amendment, DESIGN section 4.8, and appended
   TEST_PLAN sections 27--28. Preserve the full previous TEST_PLAN prefix and all other
   DESIGN bytes. No ORACLE_CATALOG, CONFORMANCE, source, test, pyproject, private notes,
   canonical mathematical package, or governing-baseline checksum change is authorized.
3. Derive, independently audit, and commit the Unit 11 numerical/structural oracles with
   explicit contraction/preimage/terminal/arc/result expectations, bounded corpus domains
   and counts, and rejection declarations. Keep all previous catalogue bytes intact.
   Repository consuming tests must not rely on the private handoff directory or JSON there.

Then, in order:

4. Write only tests/test_parity_cut.py from adopted authority and committed oracles. Syntax
   and live repository Ruff stdin checks under that target path precede application.
   Observe intended ModuleNotFoundError for exactfrac.parity_cut while it is absent;
   all 439 earlier tests remain green. A preflight failure is not a successful RED record.
5. Implement only exactfrac/parity_cut.py after RED. Run live Ruff on its entire review
   copy before applying it; preserve frozen tests unless a defect is separately adjudicated.
   Do not repair forbidden behavior by changing closed flow/families/sign-routing code.
6. Require PC1--PC20, targeted/full pytest, full repository Ruff, independent cut/constraint/
   parity/correspondence audits, import isolation, and exact byte nonmutation to pass.
   Audit returned original/reduced/temporary coordinates and actual ordinary-call counters
   explicitly. Bind the real candidate, test, corpus, and all evidence hashes.
7. Only after GREEN add the two narrowly scoped rows and engineering note in PC20.
   Preserve previous CONFORMANCE statuses. Do not reinterpret a saved base-file-nonmutation
   audit as covering a later authorized CONFORMANCE change.
8. Stage exactly docs/CONFORMANCE.md, exactfrac/parity_cut.py, tests/test_parity_cut.py.
   Export the complete staged tree, check real import origins and bytes, run targeted/full
   tests and Ruff in isolation, then commit atomically after the separate authority/oracle
   commits. Push normally and authenticate direct remote/local refs and clean state.
9. At full unit closure provide exactly two self-contained four-backtick Markdown append
   blocks for private BUILD_NOTES and LEARNING_NOTES. Do not stage those notes. Unit 12
   starts only from the closed Unit 11 identity, with its own source/intake gate.

This authority establishes no runtime implementation merely by being committed. Source
intake calculations and private mathematical controls are not the later committed oracle
corpus, a tests-first record, or production completion evidence.

## 29. Unit 12 — integrated exact branch residual oracle

Source authority: `alg:branch-min`, `thm:branch-oracle`, `prop:branch-transform`,
`prop:domain-decomp`, and the composed `lem:sign-routing`, `lem:parity-anchor`,
`thm:GR`, `lem:ek` contracts pinned by SPEC_LOCK. Engineering authority: DESIGN
§4.9 with §§4.3A, 4.5A, 4.6, 4.7, and 4.8. This section is prospective; it creates
no production implementation or executed conformance claim.

The production owner is `exactfrac/oracle.py`; the consuming test is
`tests/test_oracle.py`. A fixture is a FIXED-PARAMETER BRANCH_ORACLE, not a global
modified-density optimum. Existing oracles, source files, tests, and CONFORMANCE
rows stay unchanged until the specific Unit 12 completion steps authorize additions.

### BO1 — public records, function signature, and exact shapes

Freeze the four sorted exports in DESIGN §4.9.2. Test exact field order, annotations,
constructor signatures, slots, frozen mutation behavior, structural equality/hash, and
absence of generated ordering and package-root exports. The context takes only one
Instance; `families` is `init=False`, not an optional caller parameter. Result fields
are `(shore,c,h,residual)`. Stats has seven declared counters plus the derived
`max_flow_calls` property, not a stored duplicate. The query returns an exact two-tuple
of result-or-None and separate stats, never a density witness, raw pair, dictionary,
backend object, or global-empty result. Enumerate malformed field cases before code.

### BO2 — prepared context binds a complete canonical cover

Use independent catalogue rows to fix all four tuples, their order, exact counts,
empty descriptors, overlaps, and repetitions. Observe exactly one closed enumerator
invocation during construction; the resulting tuple and Instance are retained without
copying/reordering/filtering. No parameter, coefficient vector, network, incumbent,
result, or mutable cache is stored. A caller cannot inject a partial/reordered family
tuple through normal construction. Test attempted extra constructor arguments and
frozen mutations with their normal Python exception types. Reconstructed contexts via
normal construction must recompute the complete cover, not retain stale families.
Do not mistake rejection of a caller tuple for a new mathematical restriction.

### BO3 — validation precedence, including empty branches

Test context exact type, then branch exact int/range, then the closed raw-pair guard,
in that order before graph work or family emptiness inspection. Context construction
checks exact Instance first. Public malformed data raises exact built-in ValueError;
wrong arity/frozen mutations retain Python behavior. Cover bool, numeric/record/container
subclasses, lists, generators, Fraction, ExactValue, floats, coercible/hostile objects,
negative and zero denominators, and wrong tuple lengths. Isolate each guard by satisfying
all earlier guards. Repeat invalid parameter cases on branches with no descriptors and
on nonempty tuples of entirely empty descriptors; neither is an invalid-input bypass.

### BO4 — direct source domains and literal c/h

The independent expected calculator reads only canonical original records and applies
DESIGN §4.9.7. Compute s from f, b by crossing support edges, and d by incident weights;
do not use production shore sums, gamma coefficients, family generation, or flow results
to establish expected values. On returned shores check the exact source domain, c,h,
h>0, and raw=B*c-A*h. Include negative c on high-end branches, unreduced positive c/h,
full original shores allowed by the source domains, and exclusion of empty original U.
Do not replace source domains with stronger density-witness or endpoint constraints.

### BO5 — fixed literal branch minima and independent full-domain oracle

Before consuming code, register literal Instance/branch/(A,B) rows with branch-domain
shores, their raw c/h/residuals, exact minimum value or None, and the specified deterministic
winner where tied. Include positive, zero, and negative A in all four branches and at
least one B>1 nonintegral parameter. Build the tiny corpus from explicit domains/counts
fixed in ORACLE_CATALOG. For each valid row independently enumerate original shores
and test membership in D_j directly. Mathematical correctness permits any exact argmin;
assert a particular winner only where the engineering selection is independently fixed.
A global compact-density brute verifier is not the oracle for these transformed residuals.

### BO6 — selected family sequence, counts, and completeness

Register r_j and the feasible-descriptor count k_j for every count anchor. Observe exactly
the selected context tuple in stored order, not all four lists, sorted copies, unique
sets, or a clipped prefix. `atomic_families_examined=r_j` includes skipped/repeated entries.
Test a genuine optimal shore that occurs only in a late family to kill omission/early
exit. Independent source-domain enumeration must detect an incomplete cover even when
all returned candidates are individually legal. Context preparation is checked separately
from query work; calling the enumerator during a query fails the test.

### BO7 — mathematical emptiness versus zero/negative minima

Cover a zero-length D1/D2 tuple, D0's single empty descriptor, D3 nonempty lists with no
feasible shores, overlapping forced masks, and parity-empty descriptors. None iff D_j
is empty. Empty cases have no coefficient/network/reduction/parity calls and zero flow
counters, but preserve the r_j examined count. Include active Q=1,f=(1,1) as an anchor
for all four empty branches. A zero residual, negative residual, zero cut, or no flow
augmentation in a feasible branch is not None. No unit/global Empty fallback is allowed.

### BO8 — exactly one lazy uncontracted network per nonempty query

Observe no coefficient or builder call until the first nonempty descriptor and exactly
one of each when k_j>0, even with repeated/overlapping families. The construction uses
the submitted raw parameter and the sole closed coefficient table. Keep the same original
network identity for all reductions and recoveries in this query. A second parameter query
must construct a fresh network; there is no context or module cache. Do not compare
expected coefficient/shift values with data seeded from the builder under test.

### BO9 — constrained minimization is not unrestricted ordinary cut

Each descriptor passing the closed is_nonempty predicate produces one reduction and
one parity-cut call. Empty descriptors are skipped before either. Register a case where
an unrestricted ordinary minimum has lower value but violates forced membership/parity.
The oracle must use the closed parity minimizer, not direct flow, all-shore production
enumeration, or a substitute family. Validate the observed original network and descriptor
sequence without using the production sequence as the expected mathematical source.

### BO10 — coordinate lifting and candidate membership

Include a reduced shore whose integer mask also happens to fit in the original universe
but denotes a DIFFERENT original set. Require the closed lifting result, then independent
original-universe, I/O, and terminal-parity checks. Kill reusing temporary/reduced masks,
returning auxiliary source/anchor bits, omitting forced vertices, and accepting an original
shore from another feasible family. Public lifting itself is a geometric conversion;
Unit 12, not its constructor, owns the candidate's family and source-domain checks.

### BO11 — independent source re-evaluation and positive h

Observe use of the closed original-record sum helpers (only sums from witness.py) and
source table. Do not compute c/h by rearranging network.gamma, constant, cut_value, or
recovered residual. Inject well-formed but wrong lifted candidates to test original
branch membership; h<=0 or failed source domain is RuntimeError before raw comparison.
No sign flip, clamp, fallback denominator, or construction of a candidate outside D_j.
The expected c/h calculations in the consuming tests stay independent of these helpers.

### BO12 — retain separate shifts and remove them exactly once

Register raw c/h, B*c-A*h, unshifted cut value, C_minus, constant, and recovered value
as distinct quantities. Cover negative and nonzero constants in every branch, positive
C_minus, zero C_minus, negative recovered values, and nonunit B. Assert
`cut_value - C_minus + constant == B*c-A*h` before candidate comparison. Mutations must
kill the wrong sign, double recovery, wrong parameter/network, dividing by B, and using
a shifted residual as input to another recovery. A plausible lower cut paired with a
wrong source raw residual is a seam failure, not a better candidate. RuntimeError,
not None, is required for an explicit mismatch.

### BO13 — exact first retention without a hidden secondary objective

Hand-fix ties across distinct and duplicate families, including tied minima with
different h, c, and original shore cardinality/mask where such cases are present in the
registered corpus. Equality retains the first feasible minimum; neither maximum h nor
smallest mask/cardinality may decide. Inject legal alternative within-family exact
minimizers separately: the branch value and original-domain legality remain correct,
without requiring one universal shore from the mathematics. Do not replace Unit 11's
least ORDINARY requirement with an invented least PARITY/BRANCH requirement.

### BO14 — scan the complete sequence after zero/negative candidates

Use fixed rows where an early feasible residual is zero or negative but a later family
has a strictly smaller value. Also use a zero cut whose later families still must be
processed even if no numerical improvement is possible. Count all r_j examined entries
and k_j parity calls. Neither residual sign nor zero cut is an outer stopping condition
at this fixed-parameter oracle. No branch reflection, Newton update, H2 scan, or unit-
witness call may occur.

### BO15 — raw scale, multiple parameters, and result meaning

For fixed positive integer k, compare independently derived outputs at (A,B) and
(k*A,k*B): deterministic shore,c,h stay identical; residual scales by k. Include zero
numerators with denominators not normalized to one, negative A, and large powers of two
whose c/h cancellation would expose accidental gcd reduction. Repeat parameters in
varying order across all four branches on a shared context; no stale shifts or incumbent
may survive. A result's raw residual divided mathematically by submitted B is F_j(lambda),
and -h is the source supergradient; do not compare residual magnitudes across different
B without cross-scaling or confuse this with a ratio optimum.

### BO16 — diagnostics are separate, exact, and nonauthoritative

For registered count anchors verify r_j,k_j, one parity call per feasible descriptor,
and the exact sum of N_F*N_F-3*N_F+3 ordinary calls. Sum closed augmentation/scan counters
and take the maximum flow-only peak. Observe actual diagnostic outputs for aggregation
checks only; no expected optimum may be derived from them. Changing otherwise legal
stats must leave the selected result unchanged. Standalone stats checks are type/range
checks, not certification of their claimed work. `max_flow_calls` is derived, and
preparation is not charged again as enumeration. Do not claim this flow peak measures
all theorem-relevant generated integers or full SolveStats.

### BO17 — internal failure boundaries and backend exceptions

Inject unexpected None from reduction or parity minimization of a descriptor whose
closed is_nonempty is true; require RuntimeError rather than silent skipping. Inject
finite but wrong original-family/domain candidates and mismatched recovery; require
failure before retention. Exceptions raised by closed dependency calls propagate rather
than being blanket-converted to ValueError/None. Do not require tamper protection for
objects forged by bypassing frozen constructors. Record which failures are deliberate
internal-promise probes versus normal public invalid-data cases.

### BO18 — nonmutation, labels, reuse, and fresh-process import isolation

Hash the context's Instance records and all four tuples before/after calls; verify no
in-place filtering or graph mutation. Repeated calls have equal outputs and diagnostics
under the shipped deterministic backend; labels do not affect algorithmic results.
In a fresh process import exactfrac.oracle from the candidate tree. Require its resolved
project dependencies to be the closed instance/families/rational/shore/sign_routing/
parity_cut/witness/flow layers only, with no verifier, consuming tests, outer branch,
solve, certificate, external graph library, or private artifact loaded by production.
The direct-import whitelist is narrower than those transitive imports.

### BO19 — source exactness and magnitude-independent iteration structure

Parse AST for prohibited float constants (`type(node.value) is float`), float/Fraction/
division/gcd/epsilon/big-M paths, recursive calls, random/I/O imports, and secondary
objectives. Cover direct set literals, SetComp, set calls, and set-typed names used as
algorithmic iterators; membership-only uses do not authorize set-derived order. Audit
all loop bounds and consumers of generators: original n/edge/family counts only, no
q,f,A,B,Q,operand bit length, or all-subset shore range. Context initialization may
assign only its derived families via object.__setattr__; forbid later mutation or
parameter/global caches. Supplement pattern checks with a call-chain/source review.

### BO20 — prep/query work and polynomial-size quantities

Separate O(n+m+R_all) context construction from per-query work and stats. Exercise many
queries on one context and a D0 query on an instance with numerous D2 families; it must
not regenerate the D2 list. Distinguish r_j=0 from a list with k_j=0. Audit the totalized
`O(1+r_j*(n+3)^3*(m+n)^2)` query carrier, including the closed zero-arc vertex work,
shore helper scans, validation, and capacity aggregation. Use bounded-support magnitude
families for arbitrary-size integers; do not turn elapsed time into a formal complexity
test. Check all raw c/h/residual and capacity bounds in DESIGN §4.9.17, including negative
A and retained zeros. Full intermediate bit instrumentation and outer bit-growth theorems
remain separate. Exact equality of observed counters across magnitudes is not asserted
unless justified for the specific family under test.

### BO21 — independent audit and adversarial controls

After consuming tests are frozen and implementation GREEN, a separate audit derives
expected original branch minima from source-domain enumeration. It imports neither the
consuming tests, global density verifier, nor a private expected-data file. Closed
production dependencies may be invoked as subjects of checked composition, never as the
source of expected minima. Freeze independent domains/counts before running candidate
production. Include source-table, shift, coordinate, family-omission, tie, early-exit,
parameter-cache, constructor-precedence, and diagnostic contamination controls. Compare
ordinary/parity/family work only where the registered reference policy fixes it. A
passing tiny corpus is executable evidence, not a complete universal proof.

### BO22 — CONFORMANCE and downstream claim boundary

Only after GREEN and source-to-code audit add a scoped `thm:branch-oracle` row mapped to
`test_exact_branch_min` plus a note mapping every Unit 12 consuming test. Explain complete
cover, original residual recovery, positive h, preparation/query work separation, and the
polynomial generated-integer argument. Preserve all previous rows/statuses. Do not promote
outer branch/global theorems, ratio transformation claims, certificate verification,
maximum-bit telemetry, Standard/Accelerated termination, or witness reconstruction.
No authority change to SPEC_LOCK, CONTRACT, or the immutable governing-checksum baseline
is authorized by this unit.

## 30. Unit 12 completion gate — exact branch residual oracle

The completion order is binding:

1. Authenticate the closed Unit 11 base and live 467-test/Ruff starting evidence.
2. Review/apply only DESIGN §4.9 and this TEST_PLAN addition; stage and close the
   documentation-only authority commit locally and remotely.
3. Derive and register Unit 12 oracles in ORACLE_CATALOG before tests. Keep the private
   machine-readable transcription out of runtime dependencies. Audit and close that
   oracle-only commit before producing consuming tests.
4. Apply only tests/test_oracle.py, after syntax and actual repository-configured Ruff
   preflight. Record the intended missing exactfrac.oracle collection error, unchanged
   pre-existing suite, empty index, and frozen test byte identities.
5. Implement only exactfrac/oracle.py against the ruled context/query/result/stats APIs.
   Do not repair frozen tests to accommodate implementation choices. Authenticate the
   saved RED and all closed bytes; run live source Ruff before applying a candidate.
6. Require targeted/full GREEN, repository Ruff, an independent definition-level audit,
   source-to-code work/bit review, and nonmutation. No CONFORMANCE edit before this gate.
7. Add only the authorized CONFORMANCE row/note; keep source/test bytes unchanged and
   authenticate the pre-note live GREEN evidence without retroactively editing its
   historical base-file claims.
8. Stage exactly docs/CONFORMANCE.md, exactfrac/oracle.py, and tests/test_oracle.py.
   Export the exact staged tree; run targeted/full tests and Ruff in isolation, verify
   project import origins and all staged/live file identities, and bind the audit.
9. Commit that exact candidate once; run postcommit checks; push only the approved
   commit after evidence authentication; require local main, origin/main, and direct
   remote main equal the approved commit with divergence 0 0 and clean worktree/index.
10. Save private BUILD_NOTES and LEARNING_NOTES closure entries. Unit 12 is not complete
    merely because an authority, oracle, RED, or unstaged GREEN checkpoint passed.

No outer-iteration, global-solver, certificate, CLI, or experimental implementation is
part of this Unit 12 gate. Any material interface/authority defect requires a controlled
new revision rather than silent helper/source/test normalization.

## 31. Unit 13 — Standard branch solver obligations

This is a prospective, documentation-only extension. All previous test-plan bytes and
consumed obligations remain unchanged. No Unit 13 oracle fixture, consuming test,
production module, or CONFORMANCE promotion is created by this authority amendment.
DESIGN section 4.10 rules exactfrac/branch.py; the future test is tests/test_branch.py.
Source binding: alg:standard-branch; eq:fj and eq:rhoj; prop:standard-correct;
lem:standard-bits; thm:WYZ and cor:standard-strong; closed thm:branch-oracle.

### ST1 — exact surface and immutable mathematical result

Require exactly BranchResult, StandardBranchStats, solve_branch_standard in __all__;
exact signatures/annotations/field order from DESIGN 4.10.2; frozen, slotted, hashable
records with structural equality and no generated ordering/defaults. Check root before
shore in BranchResult. Accept signed/zero/unreduced valid RawPairs verbatim; reject
ExactValue/Fraction/float/bool and tuple/numeric subclasses, malformed pairs, nonpositive
shore, and implicit coercion. Constructor validation is structural, not optimality.
Package __init__ stays empty; no Accelerated or global API appears in this unit.

### ST2 — local statistics shape and nonauthoritative meaning

Require exact nonnegative ints for oracle_calls, outer_iterations, newton_updates, then
exact BranchOracleStats for oracle_stats, in order. Reject subclasses/duck types; retain
normal Python arity/frozen exceptions. Valid standalone records need not satisfy the
successful-run counter relations; constructors do not certify an observed execution.
No full AlgorithmStats, environment metadata, or global integer-peak claim is introduced.

### ST3 — public validation before graph or optimizer use

Wrong context fails before wrong branch; wrong branch fails before the seed query.
Exercise exact types, bool, int/record subclasses, iterators, hostile coercion/equality
objects, Instance instead of prepared context, and out-of-range branch numbers. Require
exact ValueError for the governed data violations, with no dependency call. Wrong arity
retains Python behavior. Include empty branches so early emptiness cannot hide bad input.

### ST4 — one mandatory seed at literal zero

Record the complete query sequence. The first invocation must use the same context and
branch with literal parameter (0,1). No family enumeration, context construction, Q==1
shortcut, or descriptor-emptiness bypass may replace it. A None seed returns (None,stats)
with counts (1,0,0) and the seed diagnostics; no initialization/loop calls follow. Distinguish
zero descriptors from a nonzero list of all-empty descriptors using closed oracle behavior.

### ST5 — Standard K is not the Accelerated initialization

For a feasible seed (c0,h0), require the exact next parameter (c0+h0,h0), unreduced. Check
both a numerator whose sign changes under +1 and a zero seed residual. Neither sign nor
zero at the seed authorizes termination. At K the true minimum must be negative, so no
normally feasible Standard run finishes at the seed or first loop call. Catch omission
of +1, a fixed (1,1) bound, normalization, user-selected seed, or an extra initialization query.

### ST6 — independent source-domain branch optima

Before consuming tests, enumerate every original nonempty shore for a declared tiny
active corpus. Compute s,b,d directly from original edge/f data; apply the literal D0--D3
conditions and c/h table, not a production family union, source-term private helper, or
future solver output. Find min c/h by independent exact rational comparisons. For every
feasible solve require root numerically equal to that minimum and the returned original
shore in the complete argmin set. Distinguish empty branches, zero roots, and negative
high-branch roots. Test the full original shore when it is a legitimate optimum.

### ST7 — complete prescribed query trajectories

Freeze hand-derived source traces before code, including the zero seed, K, every negative
query/update, and final exact-zero query. Include multiple updates and all four branches.
For deterministic traces, independently identify the closed oracle's first ordered-cover
minimizer using direct finite enumeration with its documented tie policy; keep that trace
reference separate from the independent domain-optimum reference. Compare each queried
raw pair, returned original c/h/residual, and stopping position. No query may be omitted,
reordered, repeated unnecessarily, or replaced with a look-ahead/reflection call.

### ST8 — literal Newton reset, strict progress, and exact zero

At every nonterminal loop query require raw<0 and next_parameter exactly (c,h), not just
an equivalent fraction. Compare rationals by cross multiplication; the new point stays
at least the independent optimum and strictly decreases numerically. Require termination
only on exact integer raw==0. Catch a tolerance, <=0 stop, positive-residual continuation,
stopping on repeated shore/tuple, an arbitrary iteration cap, and unreduced expression
Bc/(Bh) masquerading as the fresh source ratio. No visited collection is necessary.

### ST9 — terminal parameter and terminal shore are separately authoritative

Include a fixture where the last negative query supplies raw pair (c_old,h_old), then the
zero query returns another optimizing shore with a structurally DIFFERENT but numerically
equal (c_new,h_new). Require BranchResult.root to retain the submitted (c_old,h_old) and
BranchResult.shore to be the TERMINAL query's shore. Replacing root with (c_new,h_new),
gcd reduction, returning the previous shore, or returning the seed must fail. Do not
require structural equality across independently legal oracle tie policies.

### ST10 — any exact argmin, shipped first-retention behavior

Historical A4 is discharged for the Standard loop only. For tiny declared instances,
substitute independently checked legal residual minimizers, including non-max-h choices;
require exact optimal root and an attaining shore for each run. Intermediate raw pairs,
iteration counts, and selected shores may differ. Separately require the shipped closed
oracle's deterministic first-retention behavior. Never alter Unit 12's frozen implementation,
tests, or expected deterministic policy; substitutions are test-local and restored.

### ST11 — checked response shape and residual binding

Substitute malformed response tuples, wrong result/stat classes or subclasses, an
out-of-universe positive shore, and a normally constructed BranchOracleResult with an
inconsistent raw residual. Each explicit seam violation must raise RuntimeError before
that response can authorize a root or update. Satisfy earlier shape/type guards to reach
each later check. These probes challenge the consumed contract, not full revalidation of
source-domain membership or exact minimum status already owned by Unit 12. Do not test
constructor-bypassing forgeries as part of the supported public API.

### ST12 — infeasibility and sign failures after a feasible seed

A subsequent None result is RuntimeError, not normal infeasibility. A nonnegative first
K-query residual violates its strict-negative promise; a positive later loop residual is
also RuntimeError. Exercise these separately from residual-binding failures with responses
whose raw arithmetic is internally consistent. No failure returns a partial mathematical
record or misleading completed statistics. The seed is expressly exempt from loop-sign
rules and may have any signed residual.

### ST13 — dependency exceptions propagate without false success

Inject sentinel exceptions from the closed oracle and used arithmetic helpers; require the
same exception to propagate, not None, generic ValueError, or an apparently completed
BranchResult. Distinguish explicitly detected malformed returned data (RuntimeError) from
an exception raised by the dependency itself. No catch-all rollback or fallback algorithm.

### ST14 — exact accounting includes seed, K, and terminal

For every successful trace, independently sum the first six fields of all returned
BranchOracleStats and take max of flow_peak_generated_value, including seed/terminal once
each. Check oracle_calls=outer_iterations+1; on a feasible run with u updates, u>=1,
outer_iterations=u+1 and oracle_calls=u+2; on infeasible run (1,0,0). Use differing nonzero
per-query diagnostics to expose a skipped/double-counted seed/terminal and sum-vs-max
errors. Verify the nested max_flow_calls property keeps its closed meaning. Preparation
is outside this per-solve accounting; no re-enumeration charge or flow-only/full-peak mixup.

### ST15 — diagnostic independence, no state leakage, and labels

Change only valid diagnostics while keeping legal mathematical replies fixed; root,
shore, query sequence, and termination must stay fixed. Reuse one prepared context for
repeated solves, different branches, and interleaved direct oracle queries. Assert no
context/Instance/family mutation or parameter/aggregate survival between solves. Labels
must not alter results, traces, or counters. Do not use a diagnostic counter to control
mathematical initial-state/sign validation or termination.

### ST16 — exactness, direct-import isolation, and compact control flow

AST/source checks enforce the DESIGN 4.10.12 import whitelist and no float, Fraction,
division, gcd/remainder reduction, set construction/iteration, recursion, reflection,
filesystem/I/O, exhaustive shore enumeration, multiplicity expansion, or magnitude-based
iteration budget. Fresh-process imports may include flow/families transitively through
the closed oracle; they must resolve to the expected project tree and import no verifier,
consuming test, private expected-data file, or future solve/certificate implementation.
Inspect the actual call structure; a source-string whitelist alone is not a proof.

### ST17 — input-sized resets and large signed integers

For independently derived constant-support cases, grow q/f encoding lengths and inspect
all submitted parameters and direct residuals. Check literal K=(c0+h0,h0) and each reset
(c,h), including unreduced pairs and signed/zero roots. The source-bound carrier is
abs(A)<=5Q+3, 1<=B<=2Q+1; later abs(A)<=3Q+2; raw magnitude is at most
(2Q+1)*(8Q+5). Test-local checks and derivations must agree. These are NOT production
cutoffs, complete peak_integer_bits instrumentation, or empirical universal proofs.

### ST18 — source-dependent work bound versus observed counters

Record t oracle invocations and its exact seed/loop decomposition. Review the t times
Unit 12 per-query carrier and the separately paid context preparation. M is n+m+1, not Q;
r_j counts descriptors, not flows. No loop bounds may be derived from q,f,Q, the input's
encoding length, or an unproved numerical constant in O(M^2 log M). Magnitude sweeps test
structural envelopes/no copy expansion; assert flat observed counters ONLY when the
chosen fixture family has a proved invariant path. Retain O(1) outer records, not a full
trajectory in production. thm:WYZ remains the frozen source invocation, not a measured fact.

### ST19 — independent implementation audit and mutation controls

After GREEN, independently compare Standard against original-domain exact ratio minima
and source-derived sequences fixed before importing the production branch module. The
auditor must not import consuming tests, the global density verifier, or private expected
JSON to generate its source optima. The closed oracle may run only as a checked dependency,
not as the producer of expected optima. Audit empty/signed/zero cases, any-argmin freedom,
raw terminal-pair distinction, reuse, exact counts, no direct flow calls, bit recurrence,
and all file/evidence nonmutation. Mutation controls must actually reject plausible
wrong implementations; document every tested control and preserve failed-control findings.

### ST20 — scoped conformance and later-unit boundaries

After the independent implementation audit and GREEN only, map actual frozen tests to
prop:standard-correct and lem:standard-bits. Document the source-dependent
cor:standard-strong composition separately from finite evidence. Do not promote the
Accelerated prop:branch-invariant/prop:branch-correct, thm:accelerated-bound,
lem:bitgrowth, global/witness reconstruction, certificate, or full telemetry obligations.
All previous rows/statuses are preserved. Final implementation/tests/CONFORMANCE form
one atomic candidate, tested from the isolated index tree before commit and remote closure.

## 32. Unit 13 completion gate — Standard branch solver

1. Authenticate the closed Unit 12 commit, saved notes, governing V2.2 source/package,
   and recorded Unit 13 starting baseline (497 collected/passed and repository Ruff).
2. Read alg:standard-branch, prop:standard-correct, lem:standard-bits, thm:WYZ,
   cor:standard-strong, residual-root definitions, and the closed oracle/arithmetic API.
   Distinguish source obligations from new Python representation/accounting choices.
3. Apply only the reviewed DESIGN 4.10 / this TEST_PLAN authority amendment; preserve
   all other bytes, frozen tests, CONFORMANCE and historical evidence. Review unstaged,
   then separately stage, commit, postcommit regression/Ruff, push, and verify remote
   closure. No Unit 13 fixtures, consuming tests, or production code exist yet.
4. Independently derive and append Standard fixtures to ORACLE_CATALOG, classifying
   transformed branch optima and local loop traces correctly. Commit/push that catalogue
   change after its independent audit and unchanged baseline/Ruff; do not derive expected
   values from a future branch implementation or promote them to global density results.
5. Create only tests/test_branch.py against committed authority/fixtures and ST1--ST20.
   Run syntax and actual repository-context Ruff preflight before application. Freeze
   exact test bytes and record intended missing-exactfrac.branch RED while production
   remains absent; require all 497 existing tests and repo Ruff still pass.
6. Only after RED, create exactfrac/branch.py implementing the Standard-only surface.
   Apply only its reviewed source after live preflight. Assert actual targeted/full
   collection and passing counts, repository Ruff, and independent implementation audit.
   Do not revise a frozen test based on an unreplicated external lint claim.
7. After GREEN, apply only the narrowly scoped CONFORMANCE amendment, mapping actual
   frozen tests and preserving prior statuses. Do not alter source/test/config bytes.
8. Stage exactly docs/CONFORMANCE.md, exactfrac/branch.py, tests/test_branch.py. Record
   blobs/modes/tree/full-index diff; export the staged tree; rerun targeted/full/Ruff
   with isolated project-import checks and prove live/index/evidence nonmutation.
9. Create the approved implementation commit, check parent/tree/scope/diff, rerun the
   actual targeted/full suite and Ruff, and save the local audit. Push only in a separate
   gate, verifying all four refs equal, 0 0 divergence, clean worktree/index, and unchanged
   historical evidence. Deliver private BUILD_NOTES and LEARNING_NOTES only at full
   unit remote closure; wait for their saved confirmation before Unit 14.

Unit 13 does not implement Accelerated iteration, a global solver, H2/unit witnesses,
endpoint transforms/reconstruction, serialization/checking, CLI, full telemetry, or a
benchmark/release campaign. It does not reopen Unit 12 or the withdrawn import-order R2.

## 33. Unit 14 — Accelerated branch solver obligations

Prospective authority only. All prior TEST_PLAN bytes, including sections 31--32,
remain historical and unchanged. DESIGN section 4.11 prospectively extends branch.py;
the source is pinned V2.2 alg:branch, prop:branch-invariant, prop:branch-correct,
thm:accelerated-bound, lem:bitgrowth, and their eq:fj/eq:rhoj/closed-oracle dependencies.
These obligations are new tests, not claims that Accelerated is already implemented.
The September 10 author rulings make Accelerated core before Unit 15 and exclude
private BUILD/LEARNING notes from ALL machine gates. References in older sections to
checking saved notes or their bytes are superseded; the two-block delivery and
conversational save-confirmation workflow remain unchanged.

### AC1 — exact combined public interface and result reuse

Require DESIGN 4.11.2's exact five-name __all__, signatures, keyword names, annotations,
record order and lack of defaults. BranchResult is the existing class, not a duplicate
or subclass. No package-root re-export, automatic Standard fallback, configurable seed,
trace callback, backend injection, or iteration cap. Preserve signed/zero/unreduced
root pairs, nonempty original shores, and None as infeasibility rather than global Empty.

### AC2 — Accelerated statistics construction and validation order

Exercise all eight fields and frozen/slotted/structural/no-ordering behavior. Validate
seven exact nonnegative-int counters in declaration order, then exact BranchOracleStats.
Reject bool, numeric/record subclasses, coercible objects, and wrong nested shapes with
exact ValueError. Keep Python arity and frozen exceptions. Valid standalone counters
need not obey successful-run identities; construction certifies no actual execution.

### AC3 — preserve the closed Standard implementation and test substance

Authenticate the six closed definitions listed in DESIGN 4.11.14 by exact source text
against their pre-extension contents, not merely functional output. Only module prose,
__all__, pair_reflect import, and appended Accelerated definitions may differ in source.
The tests-only compatibility diff is restricted to the two surface checks, their surface
constants if any, and the old _source_violations import/reflection logic. No changes to
31 names, literal data, mathematical references, behavioral assertions, or 20 existing
source-control snippets. Reject arbitrary/partial export sets. Keep Standard reflection
forbidden directly AND transitively; negative controls must detect that regression.
No skip/xfail, blanket whitelist expansion, or conditional omission of a Standard test.

### AC4 — exact public rejection before dependency or graph use

Require exact context validation before branch validation, then the mandatory query.
Challenge hostile equality/coercion/graph-access objects, bool, subclasses, Instance
instead of prepared context, invalid branch values and empty domains. Wrong supported
data is exact ValueError without calling the optimizer. No family/degree inspection or
context rebuild precedes validation; arbitrary dependency exceptions are not translated.

### AC5 — mandatory seed at literal (0,1), infeasibility and signs

Record the first actual query and same context/branch identity. All feasible seed signs
are legal; None returns (None,stats) and no further calls. Check one seed call, zero other
counters and exact seed diagnostics for both zero descriptors and all-empty descriptors.
A feasible zero seed still requires the subsequent source-ratio query. No Q shortcut,
synthetic reply, extra seed or family-derived bypass; no infeasibility from a zero root.

### AC6 — source-ratio initialization, not Standard's plus one

The second parameter is exactly (seed.c,seed.h) from make_pair. No pair_add_one, fixed
bound, normalized value or reuse of the seed reply. Require initial residual <=0; bind
a zero return to the second query's submitted pair and shore even when they differ from
the seed record. Initial-root counts are (2,0,0,0,0,0,0). Catalogue initial positive,
negative and zero numerical roots, unreduced pairs, and a structural terminal-pair trap.

### AC7 — original-domain independent optimum on every core solve

Use the committed 329-instance core, enumerate original nonempty shores, evaluate s,b,d
from original records and apply literal D0--D3 domains and c/h formulas. Do not derive
expected optima from families, Unit 12 private helpers, Standard or Accelerated output.
Require all 1,316 results, infeasibility, signed/zero roots, and original attaining shores
to match these independent minima. A returned zero at some shore is insufficient without
the independently checked minimum. Include a full original shore when domain-permitted.

### AC8 — full precommitted deterministic Accelerated query streams

Freeze seed, initialization, every Newton and reflected query, reply, disposition and
terminal site before consuming tests. Expected ordered argmins use a separate source/cut
reference under the ruled selector, not production output. Compare literal parameter,
shore, c,h, raw binding and call position. Include initialization termination, Newton
termination, reflected termination, strict-negative acceptance, positive rejection,
multiple continuations and all four branches. Require no omitted, repeated or reordered
query; in particular no query of the retained Newton state after rejection.

### AC9 — fresh Newton reset and explicit monotonicity guard

At each negative current state require make_pair(current_result.c,current_result.h)
literally and compare_pairs(newton,current)<0 before any Newton query. Verify the point
lies at least at the independent optimum and its exact minimum is nonpositive. Terminal
Newton zero returns before reflection arithmetic or a reflected query. Inject a comparator
fault to exercise the guard without claiming that fault is a legal mathematical oracle.
Catch old-denominator accumulation, tuple ordering, normalization and non-strict progress.

### AC10 — closed pair_reflect only and exact role ordering

Spy on the closed arithmetic seam: it receives (newton,current) and returns the exact
formula (2*A*D-C*B,B*D) with fresh Newton operand. Check asymmetric, unreduced, cancellation,
negative-reflection and large-integer cases. Require reflected<newton<current numerically
via closed compare_pairs before querying. Catch reversed operands, local reimplementation,
clipping, reduced equivalence and reusing a growing operand as the supposedly fresh point.
No reflection occurs on initialization-root or Newton-root termination.

### AC11 — negative/zero/positive reflection have distinct legal outcomes

A negative reflected minimum continues with the reflected parameter AND reflected reply.
A zero minimum terminates at that exact pair and current reflected shore. A positive
minimum rejects look-ahead and retains the saved queried Newton pair AND Newton reply.
Check binding first for all three signs; malformed replies must not become legal rejection.
After a positive rejection the next Newton construction uses the retained Newton reply,
not the rejected reflected reply or the previous state's shore. No repeated Newton query.

### AC12 — terminal raw pair and shore preservation at all three sites

Independently catalogue a terminal shore whose own fresh (c,h) differs from the parameter
that was queried, wherever realizable at initialization, Newton and reflection. Distinguish
source-realizable traps from synthetic seam controls. Keep the submitted pair verbatim
and that query's shore. Detect returning a seed/old/rejected shore, normalizing a quotient,
rewriting a reflected root to fresh terminal terms or returning None for zero.

### AC13 — all legal exact argmins, no hidden secondary preference

Enumerate complete legal argmin sets and trajectories on registered tiny fixtures, then
inject those mathematically valid choices. Every completed path must attain the same
numerical optimum with a valid original shore. Verify the retained-state invariant and
strict progress independently; distinct legal choices may change raw pairs and paths.
Include non-max-h choices and deterministic first-retention traps. Never weaken Unit 12's
least ordinary cut contract or add h/mask/cardinality/diagnostic tie-breaking.

### AC14 — malformed response and raw binding at every query kind

At seed, initialization, Newton, and reflected seams independently inject wrong outer
shape, result/stat types or subclasses, out-of-universe shore, and inconsistent raw
residual. Satisfy earlier guards to reach each later boundary. Require RuntimeError before
acceptance, rejection, update or return. Constructor-bypassing forgeries are outside the
normal immutable-record API; the wrapper does not re-solve or rescan source-domain sums.

### AC15 — internal None/sign/progress errors versus normal rejection

After a feasible seed, None at initialization, Newton or reflection is RuntimeError.
Positive initialization/Newton residual is RuntimeError; positive REFLECTED residual is
normal rejection. Exercise arithmetically bound replies to separate sign checks from raw
mismatch. Comparator-fault controls must challenge each ruled strict-decrease comparison,
including final retained-state transfer, without being counted as source-realizable paths.
No counter, arbitrary iteration cap, exception translation or fallback yields false success.

### AC16 — exact accounting and diagnostic independence

Independently count all normally returned queries and aggregate six sums plus the maximum
flow-only peak. Exercise distinct diagnostics at seed, initialization, each Newton and
accepted/rejected/terminal reflection. Assert DESIGN 4.11.12's identities for infeasible,
initial-root, Newton-terminal and reflected-terminal runs. A terminal reflection counts
as neither accepted nor rejected. early_returns means the two explicit in-loop source
returns, not initialization. Alter valid diagnostics alone and require identical roots,
shores, queries and decisions. Preparation and full peak-bit telemetry remain separate.

### AC17 — dependency exception identity and no partial completion

Inject sentinel exceptions from exact_branch_min, make_pair, pair_reflect, compare_pairs,
residual_numerator, and the shared validation/aggregation dependencies at reachable sites.
Require original exception identity to propagate, not None, a relabeled data error or a
partial result/stats tuple. A dependency throwing differs from a normal malformed reply.
Test-local spies are restored; no production exception-catching framework is introduced.

### AC18 — repeated contexts, interleaving, labels and Standard regression

Reuse one prepared context across repeated Accelerated and Standard solves and direct
queries in changing branch order. Require no re-enumeration, parameter/cache leakage or
Instance/family mutation. Labels affect none of the mathematical results or deterministic
counters. Preserve Standard trajectories, diagnostics, validation and exact public record
semantics. All preexisting 528 cases remain required, with only AC3's compatibility edits.

### AC19 — required Standard agreement on all 1,316 core branch solves

Execute both actual solvers for every (instance,j) in the 329-by-four core: no sampling,
feasible-only filtering or counts inflated by duplicates. Require matching infeasibility;
on feasible results compare_pairs(standard.root,accelerated.root)==0. Independently check
EACH shore in the literal branch domain and its own c/h attaining the optimum from AC7.
Do not demand structural pair, witness/shore, trace, stats or iteration-count equality.
Differential agreement is additional evidence, never the source of expected answers.
Do not require Accelerated to have fewer oracle calls on every individual instance.

### AC20 — source-derived encoding recurrence and large integer families

Precommit symbolic trajectories that exercise accepted-reflection accumulation and
rejected-look-ahead reset, including both signs and cancellation, with support fixed and
encoding lengths through at least 4096. Where graph-realizable depth is limited, label
abstract scalar recurrence controls separately instead of claiming real solver coverage.
Check literal pairs, each product/subtraction intermediate, and the test-local carrier
P_new<=(2*C+H)*P, C=3Q+2,H=2Q+1, with fresh reset bounded by C. Inspect attempted
rejected and terminal reflections as well as accepted iterates. Combine raw/capacity
bounds with Unit 12; no production bit cutoff, full-telemetry claim or empirical DKNV proof.

### AC21 — source-dependent work and no numerical loop budget

Review O(M log M) calls under the pinned thm:DKNV/thm:accelerated-bound invocation,
M=n+m+1, and multiplication by the closed uniform per-query carrier. Count r_j as families,
not flows; preparation is once-paid. Inspect O(1) retained outer records and one
residual-controlled solver loop; no q/f/Q/capacity/bit-length-driven range or visited list.
Assert flat observed counters only for a proved invariant fixture family, not general
magnitude changes. Integer-operation bounds are distinct from bit-time and byte-memory.

### AC22 — shared-module exactness and fresh-process isolation

Enforce the combined direct-import whitelist, while keeping pair_add_one Standard-only
and pair_reflect Accelerated-only. Check no prohibited direct graph/cut/verifier import,
local reflection formula, Fraction, float, tolerance, division/gcd, dynamic I/O, sets,
recursion or exhaustive enumeration. Detect reflection leaking into preserved Standard
paths and ensure the 20 prior source controls still fail. Fresh imports resolve to the
chosen candidate tree and introduce no verifier/tests/private data or global solver.

### AC23 — separate implementation audit and executed mutation controls

Derive source-domain optima and legal trajectories independently before importing future
production; do not use consuming tests, global-density verifier or private expected JSON
to generate them. Recheck all core branch agreements as subjects, not answers. Challenge
all terminal sites, rejected-state retention, raw-pair roles/binding, strict progress,
diagnostics, seams, independence, source structure and bit recurrence. Compile and execute
plausible faulty implementations, distinguishing semantic rejection from syntax/lint
failure. Record survivors honestly; preserve frozen candidate/test and evidence bytes.

### AC24 — scoped CONFORMANCE, atomic closure, and Unit 15 dual route

Only after GREEN and AC23, map actual tests to prop:branch-invariant, prop:branch-correct
and scoped lem:bitgrowth; document the source-dependent thm:accelerated-bound chain
separately. Preserve Standard coverage and unrelated rows/statuses. Finite testing does
not prove DKNV or independent global optimality. Stage the complete authorized candidate,
isolate that exact index tree and require both branch suites/full/Ruff before commit.
Unit 15 must rule a Standard | Accelerated selection, execute every global corpus
instance with both, and require equal numerical endpoint/global values with EACH returned
witness independently validated and re-evaluated to that value. Different witnesses/raw
pairs are legal; exact raw witness-formula storage is independently checked. True Empty
remains separate. The Unit 18 certificate checker is not silently assumed to exist.

## 34. Unit 14 completion gate — required Accelerated branch solver

1. Authenticate starting checkpoint R2 at ee4a9b0279424781980d668145c7b3fc5d50f9f7,
   tree 9d22b4c9b1d18f31d49532381a36e82099ba6055, all 36 governed files and the
   pinned source. Baseline: 31 Standard / 528 full and actual repository Ruff. Private
   notes are excluded before dereference from inherited pin/absence/status inventories;
   no note-file predicate is a gate. Their previously confirmed save is conversational.
2. Read the actual Accelerated algorithm, invariant, correctness, external iteration
   invocation and bit proof, together with closed arithmetic/oracle/Standard interfaces.
   Commit documentation-only DESIGN 4.11 and this prospective test plan, explicitly
   superseding deferral and ruling the narrow shared-module compatibility boundary.
   Apply unstaged; separately stage, local commit, postcommit baseline/Ruff, then
   approved-hash push and remote closure. No source/test/catalogue change in authority.
3. Independently derive and commit the Accelerated oracle catalogue before its tests.
   Include all pseudocode paths and output/seam/diagnostic/bit distinctions above.
   Standard numerical answers can be checked after source expectations are fixed; they
   cannot generate Accelerated traces. Audit, baseline, Ruff and remote-close fixtures.
4. Deliver a tests-only candidate: new tests/test_branch_accelerated.py plus EXACTLY
   AC3's constrained edits to tests/test_branch.py. Freeze the compatibility diff and
   both files. Run actual repository-context Ruff stdin preflight on each before apply.
   New tests import solve_branch_accelerated explicitly from exactfrac.branch at
   collection: require the exact missing-name ImportError while that function is absent,
   not ModuleNotFoundError for the already-existing Standard module. No dummy export,
   placeholder, skip or catching of intended RED. Existing 528 tests stay green when
   only the new RED file is excluded. No production change occurs in this tests gate.
5. Only after that RED, extend branch.py under the fixed contract. Preserve the six
   closed definitions exactly; preflight source with live Ruff before applying it.
   Require all new cases' actual collected/passed counts, unchanged 31 Standard cases,
   full suite, repository Ruff, independent AC23 audit and semantic mutations. No
   undocumented change to frozen tests to make code pass. No external reviewer gate.
6. Apply only a narrowly scoped CONFORMANCE amendment after GREEN and audit; identify
   exact test names, proof-dependent bounds and finite limits. No source/test changes.
7. Stage precisely docs/CONFORMANCE.md, exactfrac/branch.py, tests/test_branch.py and
   tests/test_branch_accelerated.py. Verify the full compatibility/source/test/document
   payload, modes, blobs, tree and complete diff. Export the index tree, not working
   copies; rerun both branch suites, full tests and Ruff with import-origin checks.
8. Commit the exact isolated candidate atomically, verify parent/tree/scope/diff and
   rerun tests/Ruff. Push only in a separate approved-hash gate; require four-ref
   agreement, zero divergence and clean governed worktree/index. Preserve historical
   evidence and all unrelated files; no new REVIEW_REQUEST or external-review wait.
9. At full Unit 14 closure deliver exactly two complete four-backtick Markdown note
   blocks, BUILD then LEARNING, with save instructions; wait for the author's save
   confirmation before Unit 15. Never open/stat/hash/locate/check private note files,
   assert their Git-ignore/existence status, stage them, or translate the conversational
   save confirmation into a filesystem condition. Historical evidence is not rewritten.

This unit implements neither the global selection/reconstruction nor the later
experimental campaign. Their required dual-route obligations are prospective, not
reported as completed. No old mathematical/source pin or activation ledger is updated.

## 35. Unit 15 — StrongCompactMSPD global-solver obligations

Authority: proposed DESIGN 4.12, effective only on its controlled authority commit.
Source: def:parameter, lem:empty, lem:unit, prop:endpoints, prop:branch-transform,
sec:global reconstruction table, alg:global, prop:global-invariant and thm:main.
These are prospective obligations, not tests already implemented or passed. No prior
TEST_PLAN obligation, fixture scope, closed test or completion status is changed.

### GL1 — exact interface, raw records and strict selection

Require exactly the DESIGN 4.12 public surface, record fields/signatures, frozen slots,
structural equality/hash, no ordering, and explicit no-default selection. Exercise both
exact strings "Standard" and "Accelerated". Reject wrong types, subclasses, aliases,
case/whitespace changes and callable injection with exact ValueError. Check SolveResult
validation order and literal (0,1) when witness is None. Constructor shape acceptance
must never be described as instance-dependent admissibility or global optimality.

### GL2 — public validation before graph use and dependencies

Require exact Instance first, then selection validation before graph properties/context
construction/optimizer calls, including on a valid Q==1 instance. Separate malformed
public requests from supported-instance construction errors and internal dependency
failures. Wrong call arity and frozen mutation keep Python behavior. No repair, raw-data
adapter, labels-driven path, automatic fallback or constructor-forgery contract.

### GL3 — genuine Empty under both selections

Reproduce ORACLE-001. Require literal ExactValue(0,1), witness None, selected diagnostic
spelling, empty branch_stats and origin "Empty". Instrument context construction, both
branch solvers and Witness construction: none is invoked. Verify emptiness independently
from the valid active input/Q and, on tiny input, brute_force. No fake U/y, rescaled zero,
exception, or zero-valued admissible witness may masquerade as Empty.

### GL4 — complete constructive baseline categories and exact unit guarantee

Independently fix fixtures for all four ordered lem:empty shore-selection categories:
even f; otherwise odd f>=3; otherwise unit-capacity degree>=2; otherwise a matching of
at least two unit edges. Include conflicts between category priority and smaller vertex
indices. Require first-in-category selection, and canonical first-two-edge lower endpoints
for the matching case. Then apply lem:unit's all/all-but-one upgrade, not the preliminary
feasibility proof's possibly zero-valued selection. Independently check admissibility,
raw (N,D), the >=1 inequality, both parity cases and noncrossing zeros.

### GL5 — baseline retention, not a synthetic lower bound

Include an independently proved instance where the baseline remains globally optimal
under strict retention, including omitted L1 d=s value-one shores. Require the original
baseline Witness and its literal raw ExactValue to survive tied/lower later candidates.
Also include a baseline that is improved. Preserve ORACLE-002's LOCAL_CONTRACT_FIXTURE
scope; a local candidate is not promoted to a global optimum without a separate proof.
The result must not be reconstructed from an assumed winning transformed-branch index.

### GL6 — one prepared context and all four selected branch calls

For Q>=2, observe exactly one BranchOracleContext(instance), identity reuse on j=0,1,2,3
in that order, and no call to the unselected branch solver. Require all four calls even
when early candidates tie/dominate or later branches are infeasible. Every normal reply's
diagnostics is retained in branch order. No context.family inspection, direct oracle call,
pre-skipped infeasibility, extra optimizer query, or shortcut at density two.

### GL7 — branch reply shape, universe and source-domain checks

Guard-isolate malformed tuple/result/stats replies, selected-stats-type mismatches,
out-of-universe original shores and each source-domain violation. Require RuntimeError
for explicit broken dependency promises, not ValueError, branch None or global Empty.
A normal (None,stats) reply preserves its stats, creates no witness and continues. Test
feasible zero/signed roots separately. Do not require a second production optimization.

### GL8 — all four original endpoint formulas and compact reconstructions

Fix independent fixtures for L0 all crossing copies, L1 all except one copy on the first
crossing edge, H0 all-zero counts, and H1 one copy on the first crossing edge. Require
original U, exact length-m dense y, every nonboundary zero, correct edge_ref, parity,
lower bound and literal raw formulas from DESIGN 4.12.9. Include q_e=1 decrement-to-zero,
full-shore H0, absent/empty boundary where legal, and candidates with internal edges.
Observe reconstruction/evaluation even for feasible candidates that do not improve.

### GL9 — exact root-to-endpoint binding without scale corruption

Independently verify A*(N-D)==B*D for L0/L1 (N-D>0), and A*D==-B*N for H0/H1. Include
returned terminal pairs numerically equal but structurally different from the returned
shore's c/h; these are accepted. Incorrect root/shore binding is RuntimeError. Correct
endpoint N,D come from the reconstructed witness, never root scale, a reciprocal copied
blindly from the submitted parameter, a signed transformed root or a reduced fraction.

### GL10 — compare endpoints, not transformed roots or stored tuples

Include traps where transformed-root ordering, lexicographic (N,D) ordering, structural
ExactValue equality, negative-root handling or float rounding would select incorrectly.
Require closed compare_pairs on original positive-denominator endpoint pairs. On equality
retain the first encountered candidate in Baseline,L0,L1,H0,H1,H2 order. Reject hidden
max-h, minimum-mask, numerator/denominator, y or provenance secondary keys. Different
legal tied terminal shores may give different final witnesses/raw pairs without error.

### GL11 — direct H2 scan, both two-copy shapes and raw (4,2)

Reproduce ORACLE-003 as a BRANCH_ORACLE, without an unsupported global promotion. Observe
the scan after all four branch calls, first qualifying vertex, canonical greedy two-copy
selection, a count 2 on one support edge and a split 1,1 on two edges. Require independent
admissibility and literal witness_raw_value (4,2), not (2,1). Include absence and later-
index eligibility. H2 must be constructed/evaluated and compared even when it ties/loses;
there is no fifth transformed-branch solver invocation.

### GL12 — honest H2 reachability and global invariant at every candidate

Prove the source-domain redundancy: an H2 singleton is L0 when b is even, useful L1 when
b is odd, and that L endpoint also has value two. Therefore do not demand or manufacture
a valid graph on which correct completed branches are strictly improved by H2. Test its
candidate construction/comparison separately from retained-result provenance. Instrument
existing module-local dependency bindings, not a new production trace API, to check the
baseline and each processed candidate. At every retention, value and witness stay bound,
admissible and dominant over all candidates processed so far. Pure comparator controls
must be labeled abstract controls, not graph-realizable endpoint histories.

### GL13 — every registered instance under both selections

Use at least the existing 329-instance core definition of ORACLE-079/093/100: n=2 then 3;
lexicographic unordered support pairs; multiplicities in {0,1,2} in product order, zero
records omitted; discard isolated-vertex patterns; f(v) ranges from 1 to d_q(v) in product
order. Run each global instance under Standard and Accelerated, including genuine Empty.
This specifies 658 global invocations, not a claimed pytest case count. Also run EVERY
additional valid Unit 15 named/corpus/magnitude instance under both selections. Invalid
requests and abstract fault controls are not mislabeled active graph instances.

### GL14 — independent raw attainment and independent global optimum

For EACH nonempty output of EACH selection construct independent BruteInstance and
brute.Witness from primitive n,edges,f,U,y only. Require witness_is_admissible and
witness_raw_value==(result.value.N,result.value.D) literally. Require the two numerical
values equal by exact arithmetic. For tiny cases compare each to brute_force's exact
global optimum, without requiring the brute enumerator's tied witness or raw scale.
For Empty check its complete state independently. Production witness_value, branch
agreement or a production success flag is not independent verification. Do not import
production helpers into exactfrac_verify or implement the future certificate checker.

### GL15 — independent per-branch endpoint agreement across routes

Capture the actual selected solvers' replies/candidate evaluations while each global
solve runs. For corresponding branches require identical feasible/None decisions and,
when feasible, equal NUMERICAL original endpoint values; independently verify each
reconstructed witness and its own literal raw value. Compare tiny branch values to
independently enumerated original source-domain endpoint optima. Distinct legal roots,
shores, dense y, raw output pairs, traces and stats across the routes are allowed.
For Q==1 the no-branch shortcut is checked instead of inventing missing branch replies.

### GL16 — diagnostic separation, retention and constructor boundaries

Check the exact SolveStats representation and validation order, selected-type tuple
entries, literal branch record retention/order, Empty tuple, and final provenance.
Standalone constructor values do not assert observed history or cross-field identities.
Vary normally constructed legal branch statistics without changing branch results:
mathematical candidates, comparisons and output must be unchanged. Counts, provenance
and root trajectories are not certificates. Do not claim Unit 16 telemetry complete.

### GL17 — unchanged dependency exceptions and no partial result

Inject distinct dependency exceptions at context preparation, each branch position,
source-sum evaluation, reconstruction/evaluation and numerical comparison. They must
propagate unchanged, including identity where applicable; no conversion into Empty,
branch None, a fallback solver or a partial successful result. Independently exercise
explicit consumer-detected promise violations as RuntimeError. Earlier guards must be
satisfied so every intended seam is actually reached.

### GL18 — reuse, deterministic repetition and nonalgorithmic labels

Repeat and interleave both selections on the same immutable Instance, retaining prior
results/stats to test absence of mutation or mutable aliasing. Check same-selection
shipped determinism separately from cross-selection equality. Relabel without changing
the canonical dense indices or edges: choices and mathematical results must not change.
No module-global traces/caches or modifications to instances, contexts, witnesses or
closed branch records. Dense counts must remain original-coordinate/canonical-order.

### GL19 — exactness, direct-import isolation and compact control flow

AST/source and fresh-process controls enforce DESIGN 4.12.12. Distinguish direct forbidden
imports from permitted transitive closed-layer imports. No float, Fraction, true/floor
division, gcd, tolerances, copy expansion, all-shore enumeration, set traversal, mutable
trace cache or magnitude-driven loop bound. The verifier remains solver-blind. The
nonexecuted Phase B interface probe is not a production module or a consuming test.

### GL20 — large integers and separate magnitude/work claims

Before tests, fix independently proved large-q/f active families, raw output formulas,
comparison traps and witness counts. Run both routes; independently evaluate admissibility
and raw attainment without brute_force/copy enumeration at huge magnitudes. Check source-
bounded wrapper scans and the carriers 0<=N<=2Q, 2<=D<=2Q-1 for nonempty returned raw values.
Do not force the returned Accelerated root's intermediate scale into this output bound.
The separate Standard/Accelerated source-dependent iteration carriers are not observed
flatness, a wall-time promise, a complete integer-peak measurement or production cutoffs.

### GL21 — independently fixed oracle coverage before tests/code

Phase C must classify/fix the complete input set, expected global values, admissible
witness choices where deterministic reconstruction is ruled, feasible endpoint values,
legal tie alternatives, baseline categories, all four reconstruction recipes, direct
H2 shapes, rejections, faults and magnitude cases. Derive them from the definition and
source without future solve.py or production-generated expected answers. Cross-check
tiny optima with the closed independent verifier. Preserve historical seed-fixture scopes.
Catalogue counts/fingerprints are independent expectations, not pytest collection counts.

### GL22 — separate implementation audit and executed mutation controls

After implementation, run a separate definition-level audit using the registered corpus
and both real selections. Demonstrate actual rejection/detection of broken mutations:
bare-one/no-witness initialization; feasibility witness used without unit upgrade;
baseline overwritten on a tie; dropped branch; wrong solver selection; independent context
per branch; comparison of transformed roots; rescaled raw output; stale winner witness;
L1 decrement on the wrong edge; nonboundary count; invalid H0/H1 selection; omitted H2
scan or reconstruction; H2 normalization to (2,1); wrong root/shore binding; and diagnostics
controlling mathematical output. Use only mathematically realizable fixtures for graph
claims; label synthetic boundary controls explicitly. External review is not a gate.

### GL23 — narrow CONFORMANCE and later-unit boundaries

Only after GREEN and the implementation audit may CONFORMANCE describe finite tested
coverage of lem:empty, lem:unit, prop:endpoints/reconstruction, prop:global-invariant and
alg:global's composition, mapped to actual frozen tests. Preserve all earlier rows and
statuses. Document thm:main and the Standard alternative as source-dependent algorithm/
operation/bit-growth chains, not universal theorems proved by finite testing. Witness
checking establishes admissibility and attainment; tiny independent exhaustive comparison
establishes optimality only for its enumerated cases. No certificate, CLI, telemetry,
MPC experiment or release completion is implied.

## 36. Unit 15 completion gate — global solve and witness reconstruction

Follow the existing controlled lifecycle without adding a review or approval gate:

1. Remotely close the documentation-only DESIGN/TEST_PLAN authority before Phase C.
2. Independently derive/audit and remotely close ORACLE_CATALOG fixtures before creating
   the consuming test or production source. No future production output supplies answers.
3. Apply only tests/test_solve.py after syntax and repository-context Ruff preflight;
   exactfrac/solve.py and tests/test_global.py remain absent. Require specifically one
   collection error, exit status 2, caused by ModuleNotFoundError for exactfrac.solve.
   A different import/runtime failure is not accepted RED. Keep the pre-existing suite
   green with --ignore=tests/test_solve.py; never create a dummy production module.
4. Under frozen authority/fixtures/test, apply only exactfrac/solve.py after syntax and
   live Ruff preflight. Require targeted GREEN, full regression, repository Ruff, a
   separate independent audit, original-coordinate/raw-value checks and all dual-route
   obligations. Baseline is the authenticated prior checkpoint; new collected/passing
   counts are observed live, not guessed from function counts or corpus cardinalities.
5. Verify source/test/import isolation, immutable closed dependencies, complete-candidate
   nonmutation and the audit's executed adversarial controls before CONFORMANCE.
6. Apply only the narrowly scoped CONFORMANCE amendment unstaged; then stage exactly
   docs/CONFORMANCE.md, exactfrac/solve.py and tests/test_solve.py. Verify full-index
   diff/blobs/modes and isolate the exact staged tree for targeted/full/Ruff checks.
7. Commit only that approved isolated tree; authenticate parent/tree/subject/scope and
   postcommit regression/Ruff. Push only the approved commit in the separate closure
   action; require HEAD/main/origin/main/direct remote equality, divergence 0 0, clean
   worktree/index and unchanged evidence before declaring Unit 15 remotely closed.
8. Deliver the private BUILD and LEARNING text blocks at full unit closure. They remain
   outside every machine gate; accept the author's saved confirmation conversationally
   before Unit 16. No private-note inspection or REVIEW_REQUEST artifact is authorized.

This gate does not reopen closed modules/tests, create a certificate checker early,
require identical witnesses across branch solvers, or replace independent definition-level
verification with agreement between two consumers of the same production oracle.

## 37. Unit 16 — exact telemetry obligations

These obligations implement DESIGN §4.13, not a new mathematical theorem. The
starting authority is the closed Unit 15 tree with 1,178 passing cases. The new
recording layer must preserve that mathematical program while measuring its work.
The Phase B amendment is documentation-only. Its exceptional later instrumentation
and legacy structural-test scopes are explicit in DESIGN §4.13(13), not inferred.

### TE1 — exact public interface and immutable records

Freeze the complete telemetry API and field order from DESIGN §4.13. Reject bool,
subclasses, iterators, ducks, omitted fields, malformed tuples and wrong records;
use exact ValueError for supported public-data rejection. Check slots/frozen fields,
no generated ordering, unchanged legacy signatures/exports/classes, and no root
re-exports. Constructors validate data shape/local equations, not execution history.

### TE2 — no second solver and same mathematical execution

For every registered valid input under each explicit selection, compare the measured
entry point against legacy solve. Require exactly one selected legacy solve call,
the same returned SolveResult object at the seam, the same native SolveStats object,
and exact mathematical records/native diagnostics for repeated equivalent calls.
Independently check each result's admissibility and literal raw value; cross-route
numerical equality does not require equal tied witnesses. Scripted seam tests must
not be confused with real global-solver executions.

### TE3 — complete route and candidate attribution

Nonempty runs prepare once, contain four ordered branch rows, retain infeasible
branch work and all losing/tied endpoint work, and preserve native selection and
attaining-candidate provenance. Baseline and H2 are genuine nonbranch observations.
All 379 Unit 15 oracle inputs run under both selections; supplement with the telemetry
fixtures. A zero-valued H0 endpoint must not be dropped from the observations.

### TE4 — native and common Newton semantics

Independently simulate short exact query streams to establish Standard updates,
Accelerated Newton queries, common Newton-candidate constructions and native outer
iterations. Cover zero iterations, artificial Standard K initialization, early Newton
root, reflection root, accepted reflection and rejected reflection. Compare the full
counter tables, not only oracle totals. Inapplicable native fields are explicit zero;
that is not permission to fill an unmeasured event with zero.

### TE5 — three look-ahead outcomes and return identities

Freeze expected queried/accepted/rejected/terminal counts. Require queried = accepted
+ rejected + terminal; distinguish terminal reflection from terminal Newton using the
native early_returns record. Initialization termination is separately recorded and is
not an early-return increment. Validate each solver's successful-run identities from
DESIGN §4.13(4), with branch infeasibility handled separately. Real larger-input path
coverage is classified by actual outcomes, never by n>3 alone.

### TE6 — one-time preparation versus repeated examinations

Independently compute r_j and k_j from the prescribed ordered family definition.
Prepared descriptor counts include empty and duplicate descriptors, one-time per
branch. Query examinations are accumulated visits, not re-enumerations. Test total
preparation, examined=calls*r_j, feasible=calls*k_j and parity=feasible against observed
native work. Alter descriptors in test-only injected seams to ensure the production
recording is not a hardcoded formula or a second enumeration.

### TE7 — ordinary cuts, flow calls and all queries

For a fixed query independently derive each feasible reduced N_F and sum
N_F^2-3N_F+3. At solve level sum over all queries, including seeds, initialization,
terminal and rejected look-ahead queries. Require agreement to native observed ordinary
cuts and max-flow calls without reconstructing new graphs solely for diagnostics.
Retain native augmentation and residual-adjacency scan definitions, including terminal
reachability work. Zero-arc and zero-terminal cases are distinct fixtures.

### TE8 — sum/max algebra and structural comparability

Use intentionally different branch records to catch sum-versus-max errors. Totals
sum event counts and one-time enumeration counts; maxima combine all magnitude/bit
peaks, including nonbranch work. Derived branch_solver and attaining_branch cannot
disagree with native. WorkStats has the same field layout for both selections. Reject
inconsistent aggregates without claiming they prove an actual execution occurred.

### TE9 — bit convention, zero and absent observations

Verify bits(0)=bits(1)=bits(-1)=1 and sign-symmetric exact integer bit lengths. An empty
observation bucket has peak zero; a bucket observing zero has peak at least one.
flow_peak_generated_value zero with no flow call has flow_peak_bits zero; a real
zero-valued flow call has flow_peak_bits one. Empty output (0,1) has positive output
bit lengths one and no fabricated branch rows.

### TE10 — independently fixed arithmetic-site manifest

Before new tests or code, classify every scalar arithmetic expression on the measured
call graph by qualified function, AST location and numeric role. Fix direct observation
or a written executed-value dominance argument. Cover compound expressions, augmented
assignments, generator/sum intermediates, short circuits and returned expressions.
Publish the manifest in the Phase C human catalogue; a private mirror is not authority.
No missing observation may be relabelled as a complete peak after implementation.

### TE11 — cancellation and transient cross-products

Hand-derive fixtures whose intermediate products exceed both their cancelling result
and every final output field. Cover B*c-A*h, coefficient products, reflection numerator
and denominator, root binding, comparisons of losing/tied candidates, and additive shift
recovery. Check intermediate products before cancellation, not only final expression
results or named locals. Accepted and rejected reflection computations are both counted.
Use exact signed integers and unreduced raw pairs; Fraction is verifier/test-only.

### TE12 — monotone summation and dominance omissions

For allowed sum-prefix omissions, test the supporting nonnegative operand preconditions
and equality of the maximum to the executed final sum. Reject mixed-sign use of that
argument. Separately check branch.py's untouched repeated universe-bound expressions
against the lower-layer observed bound on every successful branch-return path. A bound
not actually generated by the algorithm is not a permissible replacement observation.

### TE13 — flow, contraction and mask completeness

Independently observe capacity aggregation, reverse-residual changes, bottlenecks and
flow totals; exercise parallel/reverse/zero arcs. Include forced contraction, anchor and
sink-terminal toggle, raw and lifted masks, and original-universe validation. Input labels
with enormous integer values must not contaminate the numerical measurement. Algorithmic
epoch/index arithmetic belongs to the defined observation set; recording counters do not.

### TE14 — parameter peaks versus returned output size

Require peak_numerator_bits/peak_denominator_bits to cover actual parameter and residual
pairs, not merely the final optimal pair. Preserve the unreduced scale of accepted
reflection parameters and raw output. Re-evaluate final output bit lengths separately.
Use a trajectory with a large discarded intermediate and a small returned witness.
No implicit gcd, float comparison, tolerance, surrogate upper bound or bit cutoff.

### TE15 — recording noninterference and disabled path

With recording disabled, the primitive is exact identity and legacy behavior remains.
With recording enabled, returned int/tuple object identity is unchanged. Poison/change
recorded maxima/counts in controlled tests and require the same mathematical decisions,
queries, minimizers, tie behavior and raw output. Collector-local branching is permitted;
mathematical reads of diagnostic state are not. No user callback is part of production.

### TE16 — isolation, failures and lifecycle cleanup

Test successive, interleaved and separate-thread measured calls, and reject nested
measured calls before invoking the solver. On every dependency failure restore the
context and propagate the same exception object; no partial AlgorithmStats result.
Inject recorder failure only as a test seam and verify cleanup. Follow it immediately
with an ordinary and a measured solve to detect state leakage. No shared mutable fields
on Instance, prepared context, witnesses/results or native diagnostic records.

### TE17 — exact observational erasure

The stdlib-only source audit helper parses, never executes, immutable reference source
fixtures. Erase only explicitly named leaf imports, scalar/pair identity wrappers and
observation statements/scope wrappers. Compare to the complete original AST, including
validation/exception order and arithmetic operand order. Reject every non-erasable edit,
extra evaluation, regrouped expression, changed comparison, changed loop or tie policy.
Preserve branch.py bytes and all five protected Standard definition hashes exactly.
Execute deliberate mathematical-edit mutants to show the erasure checker rejects them.

### TE18 — existing test-guard adaptations are not a weakening budget

For each permitted existing test edit, preregister the exact structural import whitelist
or historical byte-preservation assertion being adapted. Existing mathematical fixtures,
query traces, expected counters, witness and rejection assertions stay byte-identical.
No deletion/skip/xfail or renamed case. The helper must authenticate legacy source/test
fixtures against the closed hashes and validate only enumerated test-AST changes.
Keep transitive origin checks; add only exactfrac._telemetry to allowed project layers,
not arbitrary exactfrac submodules. Source direct imports add only named leaf primitives.
The old test_branch.py compatibility SHA remains checked against its historical fixture;
its live import-only delta is independently checked, not approved by changing that SHA.

### TE19 — primitive is genuinely a leaf

In a fresh process import _telemetry without any solver/instance/verifier import. Only
approved stdlib dependencies and fixed primitive definitions may appear. There is no
clock/I/O/network/profiling/dynamic source tool in the leaf. Import the instrumented
solver directly from its own file tree without tests, verifier or optional libraries.
No parameter or result flows through a proxy numeric class. Retain minimum Python 3.11
syntax/support obligations; live Ruff is authoritative for actual target paths.

### TE20 — metadata is explicit and external

Reject invalid elapsed values including bool/int substitutes, negative, NaN/infinite
float and numeric subclasses; accept finite nonnegative exact floats and None. Unknown
CPU is None, not a fabricated device string. Validate metadata strings/hash format.
Constructing metadata or RunRecord performs no clock, subprocess, network or file call.
Vary metadata with deterministic AlgorithmStats held equal. These are in-memory records;
no certificate/checker timing, wire-format implementation or benchmark campaign is claimed.

### TE21 — exact source-bound work and storage

Inspect the wrapper and hooks for one solve call, one preparation, no replay/expanded
copies/all-shore enumeration, no unbounded trace storage, no magnitude-based loop bound
and no diagnostic-driven optimizer cutoff. Record actual event counts, not implied total
elementary operations. Test fixed-support large encodings but do not require universally
flat trajectories or infer a theorem from a finite sweep. Preserve both source factors.

### TE22 — independent implementation audit and mutations

Run a separate audit that does not reuse telemetry collectors to derive expected peaks
or event counts. Compare hand-derived site/stream tables, independent raw witness checks,
source erasure, legacy-test preservation and reference-native diagnostics. Execute mutants
for output-only/flow-only peak, missed cancelling product, missed sum prefix where invalid,
max-versus-sum inversion, terminal-look-ahead miscount, doubled preparation, omitted losing
branch/H2/zero-H0, counter feedback, context leakage, metadata mixing, extra optimization,
expanded-copy work and hidden source/test weakening. A detector must pass unmodified code
and fail a real test body against its mutant; import/collection errors are not kills.
The exact finite mutation list is fixed with oracle/test authority before implementation.

### TE23 — exact regression and finite CONFORMANCE

Run every legacy case after the tightly scoped adapters, plus every new collected case.
The new total is 1,178 plus actual new collection, never a forecasted number. Preserve
source/test identity throughout GREEN and later gates. Promote only actual finite scope
in CONFORMANCE; report exceptions to historical source immutability explicitly, rather
than claiming instrumentation changed no source bytes. No theorem, whole-input timing,
optimality certificate or empirical strong-polynomial proof is newly established.

## 38. Unit 16 completion gate — exact telemetry

1. Authenticate the closed Unit 15 commit/tree, all 39 file identities, the fresh
   1,178-case Unit 16 baseline, live Ruff and the pinned V2.2 source.
2. Read the numerical/work source passages and the actual closed counters and static
   preservation tests. Distinguish source requirements from DESIGN §4.13 engineering
   choices. Present the limited source/test reopening explicitly during authority review.
3. Apply only DESIGN/TEST_PLAN, preserving their historical bytes; leave unstaged. Review,
   stage only these documents, record tree/diff, commit, rerun the 1,178-case baseline/Ruff,
   and verify remote closure. No Unit 16 production or consuming-test file exists yet.
4. Derive the independent counter/peak/site/preservation tables and immutable old-source
   fixture digests before code. Append only the oracle catalogue; audit, regression/Ruff,
   then separate stage/commit/postcommit-audit-tests/push/closure. No external-review gate.
5. Phase D creates tests/test_telemetry.py, tests/_telemetry_source_audit.py and the exact
   unexecuted legacy JSON fixture; applies only enumerated import/preservation adapters
   to permitted tests. Run syntax and live per-target Ruff first. Require specific missing-
   exactfrac.telemetry RED; existing 1,178 cases must pass with that new test excluded.
   Neither new production file nor instrumentation edit exists at RED. Freeze all tests.
6. Phase E creates telemetry/_telemetry and only the explicit erasable instrumentation
   source changes. Preserve branch.py and the independent verifier byte-for-byte. Run
   targeted/full regression, live Ruff, import-isolation/nonmutation, independent audit,
   legacy reference checks and executed mutations. Stop on any unruled non-erasable edit.
7. Only after GREEN, amend CONFORMANCE within the actual finite scope. Preserve all
   earlier historical rows/statuses and document rather than conceal observational changes.
   Do not change production/tests in this documentation phase.
8. Stage exactly the reviewed full candidate; record all source/test/doc/fixture identities,
   full-index diff and tree. Test the exact staged export in isolation, including every
   legacy/new case and Ruff, with import origins rooted in that export. Prove nonmutation.
9. Commit that exact isolated tree; check parent/tree/subject/scope/diff and clean index;
   rerun targeted/full/Ruff. Push only in a separate authenticated gate, then verify four
   equal refs and zero divergence. Deliver private BUILD/LEARNING blocks only at full
   Unit 16 closure, then await saved confirmation before Unit 17. Never inspect those notes.

The authority creates no new scientific-review or model gate. The extra source/test
paths arise from an explicitly proposed observational extension to closed code; they
are not a general permission to rewrite dependencies, weaken tests, or alter mathematics.
