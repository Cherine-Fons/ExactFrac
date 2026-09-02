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
