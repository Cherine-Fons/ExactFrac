# ExactFrac Oracle Catalog

Hand-derived mathematical truth cases for ExactFrac.

Every expected result in this catalog is derived independently before implementation
code is allowed to compute it. Implementations may later cross-check these cases, but
implementation output is never used to establish an oracle answer.

## Oracle classifications

- `GLOBAL_ORACLE` — proved exact optimum of the complete compact problem.
- `BRANCH_ORACLE` — proved expected value or output for one specified branch.
- `LOCAL_CONTRACT_FIXTURE` — proved local construction or lower-bound witness; not
  automatically a global optimum.
- `CROSS_MODEL_EQUIVALENCE` — compact and expanded-copy formulations proved to agree.
- `NEGATIVE` — rejected or unsupported input, or an infeasible mathematical object.

---

## ORACLE-001 — Q = 1 single-edge empty family

**Classification:** `GLOBAL_ORACLE`

**Source obligation:** `lem:empty`

### Instance

Let

$$
V=\{0,1\},
\qquad
S=\{\{0,1\}\},
\qquad
q_{01}=1,
\qquad
f=(1,1).
$$

The total multiplicity is

$$
Q=1.
$$

The multiplicity-weighted degrees are

$$
d_q(0)=d_q(1)=1.
$$

Therefore the active hypothesis holds:

$$
f(v)\le d_q(v)
\qquad
\text{for every }v\in V.
$$

Thus this is a valid active ExactFrac instance. The expected `Empty` result below is
not caused by invalid or unsupported input.

### Independent derivation

The nonempty shores are

$$
\{0\},
\qquad
\{1\},
\qquad
\{0,1\}.
$$

#### Shore $U=\{0\}$

The unique support edge crosses the boundary, so the compact boundary count satisfies

$$
y_{01}\in\{0,1\}.
$$

If

$$
y_{01}=0,
$$

then

$$
f(U)+Y(y)=1.
$$

This total is odd, but it fails the admissibility lower bound

$$
f(U)+Y(y)\ge3.
$$

If

$$
y_{01}=1,
$$

then

$$
f(U)+Y(y)=2.
$$

This total is even and also below $3$.

Therefore no admissible compact pair uses

$$
U=\{0\}.
$$

#### Shore $U=\{1\}$

This case is symmetric to $U=\{0\}$.

Again,

$$
y_{01}\in\{0,1\},
$$

and the corresponding totals are $1$ and $2$.

Neither choice satisfies all admissibility conditions.

Therefore no admissible compact pair uses

$$
U=\{1\}.
$$

#### Shore $U=\{0,1\}$

The unique support edge is internal, so the boundary is empty.

Therefore necessarily

$$
Y(y)=0.
$$

Also,

$$
f(U)=f(0)+f(1)=2.
$$

Hence

$$
f(U)+Y(y)=2.
$$

This total is even and below $3$.

Therefore no admissible compact pair uses

$$
U=\{0,1\}.
$$

### Conclusion

Every nonempty shore has been exhausted.

Therefore

$$
\mathcal A_q(H)=\varnothing.
$$

The exact global output is

$$
\boxed{((0,1),\mathrm{Empty})}.
$$

### Machine-facing expected result

- `value = (0, 1)`
- `witness = Empty`

### Interpretation

The instance is valid and satisfies the active hypothesis.

`Empty` therefore represents a legitimate mathematical solution state:

- valid active instance;
- admissible family empty;
- return `((0,1), Empty)`.

This is fundamentally different from an invalid or out-of-regime instance:

- invalid or unsupported instance;
- reject the instance.

The implementation must never conflate these two cases.

### What this oracle protects

This oracle checks that an implementation correctly handles:

1. the active hypothesis;
2. compact boundary multiplicity rather than indivisible edge weight;
3. the parity admissibility condition;
4. the lower bound $f(U)+Y(y)\ge3$;
5. exhaustive treatment of all nonempty shores;
6. the empty-family output contract `((0,1), Empty)`;
7. the distinction between invalid input and a valid instance with an empty admissible
   family;
8. the requirement that no dummy shore or dummy $y$-vector is manufactured when the
   admissible family is empty.

### Oracle status

**Hand-derived before implementation.**

No solver, brute-force verifier, branch oracle, or other implementation output was used
to establish this result.

---

## ORACLE-002 — Constructive unit lower-bound witness

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligation:** `lem:unit`

### Purpose

This fixture checks the constructive unit-lower-bound mechanism of `lem:unit`.

It does not claim that the constructed witness is globally optimal. The instance is
deliberately chosen so that the constructed witness has ratio exactly \(1\), while a
different admissible compact pair has ratio \(2\).

This makes the distinction between a constructive lower-bound witness and a global
optimizer explicit in the fixture itself.

### Instance

Let

$$
V=\{0,1,2\}.
$$

The canonical support-edge order is

$$
e_0=\{0,1\},
\qquad
e_1=\{0,2\},
\qquad
e_2=\{1,2\}.
$$

Every support edge has multiplicity one:

$$
q=(1,1,1).
$$

Let

$$
f=(1,1,2).
$$

Since the support graph is a triangle,

$$
d_q=(2,2,2).
$$

Therefore the active hypothesis holds componentwise:

$$
f(v)\le d_q(v)
\qquad
\text{for every }v\in V.
$$

The total multiplicity is

$$
Q=3>1.
$$

Hence, consistently with `lem:empty`, the admissible compact family is nonempty.

### Construction of the shore

Vertex \(2\) has even capacity:

$$
f(2)=2.
$$

The constructive argument in the proof of `lem:empty` therefore permits the singleton
shore

$$
U=\{2\},
$$

because

$$
d_q(2)=2.
$$

Its support boundary is

$$
\delta_H(U)=\{e_1,e_2\},
$$

and therefore

$$
b_q(U)=2.
$$

### Construction of the unit witness

For this shore,

$$
f(U)+b_q(U)=2+2=4,
$$

which is even.

The even-parity case of `lem:unit` omits one boundary copy.

Fix the deterministic fixture choice by retaining \(e_1=\{0,2\}\) and omitting
\(e_2=\{1,2\}\).

Using canonical edge order \((e_0,e_1,e_2)\), the dense compact count vector is

$$
y=(0,1,0).
$$

Its sparse exported representation is the single pair

$$
[[1,1]],
$$

where edge reference \(1\) denotes \(e_1=\{0,2\}\).

Thus

$$
Y(y)=1.
$$

The selected count is supported only on the boundary of \(U\), and

$$
0\le y_e\le q_e
$$

holds for every support edge.

### Admissibility

Since

$$
f(U)=2
$$

and

$$
Y(y)=1,
$$

we obtain

$$
f(U)+Y(y)=3.
$$

This value is odd and at least \(3\).

Therefore

$$
(U,y)
$$

is an admissible compact pair.

### Exact attained value

Because \(U\) is a singleton,

$$
e_q(U)=0.
$$

The raw numerator is

$$
N=2(e_q(U)+Y(y))
  =2(0+1)
  =2.
$$

The raw denominator is

$$
D=f(U)+Y(y)-1
  =2+1-1
  =2.
$$

Hence the raw ExactFrac value associated with this witness is

$$
(N,D)=(2,2).
$$

Mathematically,

$$
\frac ND=\frac22=1.
$$

The raw pair is intentionally not gcd-reduced. The implementation contract preserves
the witness-attaining numerator and denominator as generated.

### Machine-facing local fixture

- shore: `[2]`
- dense_y: `(0, 1, 0)`
- sparse_y: `[[1, 1]]`
- raw_value: `(2, 2)`
- mathematical_ratio: `1`

### Explicit proof that this is not a global oracle

The purpose of `lem:unit` is to construct a witness of ratio at least \(1\). It does not
state that the constructed witness is optimal.

This instance makes that distinction concrete.

Consider

$$
U'=\{0,1\}.
$$

The edge

$$
e_0=\{0,1\}
$$

is internal, so

$$
e_q(U')=1.
$$

The boundary is

$$
\delta_H(U')=\{e_1,e_2\}.
$$

Select one boundary copy, for example \(e_1\). Then

$$
Y(y')=1.
$$

Also,

$$
f(U')=f(0)+f(1)=2.
$$

Therefore

$$
f(U')+Y(y')=3,
$$

which is odd and at least \(3\). Thus the competitor is admissible.

Its raw numerator is

$$
N'=2(e_q(U')+Y(y'))
   =2(1+1)
   =4.
$$

Its raw denominator is

$$
D'=f(U')+Y(y')-1
   =2+1-1
   =2.
$$

Hence

$$
(N',D')=(4,2)
$$

and

$$
\frac{N'}{D'}=2.
$$

Therefore

$$
2>1.
$$

The constructive `lem:unit` witness is thus provably not globally optimal on this
fixture.

This non-optimality is intentional and is part of the fixture design.

### Source lineage and fixture choice

The source lineage has two distinct steps.

First, the constructive argument in `lem:empty` supplies a suitable nonempty shore \(U\).
For this fixture, that shore is

\[
U=\{2\}.
\]

Second, `lem:unit` takes the shore supplied by that construction and applies its
parity-dependent boundary-copy rule. Because

\[
f(U)+b_q(U)=4
\]

is even, the `lem:unit` construction omits one boundary copy and retains the other,
producing a compact witness with ratio at least \(1\).

Thus the source-faithful dependency is

\[
\texttt{lem:empty}
\longrightarrow
\text{construct the shore }U
\longrightarrow
\texttt{lem:unit}
\longrightarrow
\text{construct the unit witness }(U,y).
\]

The mathematical source does not require a preferred boundary copy when several legal
choices exist.

The choice to retain \(e_1\) and omit \(e_2\) is therefore a deterministic fixture
choice made only so that the expected witness has one reproducible representation.

The correctness claim is the admissibility and attained ratio of the chosen witness, not
that this particular edge copy is mathematically preferred.

Likewise, the ratio-\(2\) competitor is used only to prove that the constructed unit
witness is not globally optimal. This fixture makes **no claim** that \(2\) is the global
optimum of the complete instance. Establishing the existence of one admissible pair with
strictly larger value is already sufficient to prove non-optimality of the unit witness.

### What this fixture protects

This fixture checks that an implementation correctly handles:

1. the constructive unit-lower-bound guarantee of `lem:unit`;
2. the active hypothesis;
3. the distinction between the shore construction and the subsequent unit-witness
   construction;
4. canonical support-edge ordering;
5. implicit edge identity by canonical `edge_ref`;
6. dense internal \(y\) aligned to canonical edge order;
7. sparse exported \(y\);
8. the requirement that nonboundary coordinates of dense \(y\) are zero;
9. exact parity and lower-bound admissibility;
10. raw unreduced exact value `(2, 2)`;
11. mathematical comparison of raw rational pairs by value rather than tuple equality;
12. the distinction between a constructive lower-bound witness and a global optimum;
13. the rule that a `LOCAL_CONTRACT_FIXTURE` must never silently become a
    `GLOBAL_ORACLE`.

### Fixture status

**Hand-derived before implementation.**

No brute-force verifier, solver, branch routine, or other implementation output was used
to construct or validate the expected fixture values.

---

## ORACLE-003 — Direct H2 endpoint with compact multiplicity

**Classification:** `BRANCH_ORACLE`

**Source obligations:** `prop:endpoints`, `alg:global`

### Purpose

This oracle fixes the expected result of the direct H2 endpoint mechanism.

H2 is not solved through the four transformed branch solvers. The global algorithm
checks it directly by finding a vertex \(v\) satisfying

\[
f(v)=1
\]

and

\[
d_q(v)\ge2.
\]

For such a singleton shore, the H2 endpoint uses selected boundary total

\[
x=2
\]

and has exact mathematical value

\[
2.
\]

This fixture is deliberately compact: the two selected copies lie on one support edge
whose multiplicity is \(2\).

### Instance

Let

\[
V=\{0,1\}.
\]

There is one support edge in canonical order,

\[
e_0=\{0,1\},
\]

with compact multiplicity

\[
q_0=2.
\]

Thus

\[
q=(2).
\]

Let

\[
f=(1,2).
\]

The multiplicity-weighted degrees are

\[
d_q(0)=d_q(1)=2.
\]

Therefore the active hypothesis holds componentwise:

\[
f(0)=1\le2=d_q(0)
\]

and

\[
f(1)=2\le2=d_q(1).
\]

The total multiplicity is

\[
Q=2.
\]

### Identification of the H2 shore

Vertex \(0\) satisfies

\[
f(0)=1
\]

and

\[
d_q(0)=2.
\]

Therefore the singleton shore

\[
U=\{0\}
\]

satisfies the H2 condition.

Vertex \(1\) is not an H2 vertex because

\[
f(1)=2.
\]

Thus the H2 vertex is unique in this fixture.

For

\[
U=\{0\},
\]

the unique support edge crosses the shore.

Because its multiplicity is \(2\),

\[
b_q(U)=2.
\]

In the endpoint notation,

\[
s=f(U)=1,
\qquad
b=b_q(U)=2.
\]

Hence the H2 side conditions

\[
s=1,
\qquad
b\ge2
\]

hold.

### H2 endpoint reconstruction

The H2 selected boundary total is

\[
x=2.
\]

Since the only crossing support edge has

\[
q_0=2,
\]

the two incident copies are represented compactly by

\[
y_0=2.
\]

Thus the dense compact vector is

\[
y=(2).
\]

Its sparse exported representation is

\[
[[0,2]].
\]

The selected boundary total is

\[
Y(y)=2.
\]

This reconstruction exercises the H2 case in which two selected copies lie on a single
support edge with multiplicity at least \(2\).

### Admissibility

We have

\[
f(U)+Y(y)=1+2=3.
\]

This total is odd and at least \(3\).

Therefore

\[
(U,y)
\]

is an admissible compact pair.

### Exact H2 value

Because \(U\) is a singleton,

\[
e_q(U)=0.
\]

The raw numerator is

\[
N=2(e_q(U)+Y(y))
  =2(0+2)
  =4.
\]

The raw denominator is

\[
D=f(U)+Y(y)-1
  =1+2-1
  =2.
\]

Therefore the raw exact value is

\[
(N,D)=(4,2).
\]

Its mathematical ratio is

\[
\frac ND=\frac42=2.
\]

This agrees with the H2 endpoint identity

\[
R_{H2}(U)=2.
\]

The raw pair is intentionally not gcd-reduced.

### Machine-facing branch fixture

- shore: `[0]`
- dense_y: `(2,)`
- sparse_y: `[[0, 2]]`
- raw_value: `(4, 2)`
- mathematical_ratio: `2`
- endpoint: `H2`

### Compact-multiplicity significance

The support graph contains only one support edge.

The value

\[
q_0=2
\]

does not represent one indivisible weighted edge. It represents two individually
selectable copies encoded by one compact multiplicity.

Therefore selecting two copies is represented by

\[
y_0=2.
\]

An implementation that incorrectly treats the support edge as one indivisible object
would be unable to reconstruct this H2 witness correctly.

### Scope of the oracle claim

This is a `BRANCH_ORACLE`.

It establishes the exact H2 endpoint witness and value for the specified shore.

It does not use or require a proof that \(2\) is the global optimum of the complete
ExactFrac instance.

Any later global-optimum claim must be established independently by the appropriate
global oracle or verifier.

### What this oracle protects

This oracle checks that an implementation correctly handles:

1. the direct H2 endpoint condition \(f(v)=1\) and \(d_q(v)\ge2\);
2. the distinction between the H2 direct scan and the four transformed branch solvers;
3. compact multiplicity greater than one on a single support edge;
4. selection of two individually selectable copies from one compact multiplicity;
5. canonical implicit `edge_ref`;
6. dense internal \(y=(2)\);
7. sparse exported \(y=[[0,2]]\);
8. boundary-only support of the compact count vector;
9. exact parity and lower-bound admissibility;
10. the exact H2 identity \(R_{H2}=2\);
11. raw unreduced exact value `(4, 2)`;
12. preservation of `BRANCH_ORACLE` scope rather than silently promoting the fixture to
    a global-optimum claim.

### Oracle status

**Hand-derived before implementation.**

No brute-force verifier, solver, global algorithm, or other implementation output was
used to establish the expected H2 witness or value.

---

## ORACLE-004 — Two distinct global maximizers

**Classification:** `GLOBAL_ORACLE`

**Primary obligation:** independent global-tie fixture for brute-verifier B9

### Purpose

This oracle establishes a complete compact instance with more than one distinct global
maximizing witness.

It protects the distinction between:

- the exact global optimum value;
- one deterministic witness returned by an implementation;
- the set of all mathematically valid maximizing witnesses.

Witness identity is not part of the mathematical optimum contract when multiple
maximizers exist.

### Instance

Let

\[
V=\{0,1\}.
\]

There is one support edge in canonical order,

\[
e_0=\{0,1\},
\]

with compact multiplicity

\[
q_0=2.
\]

Thus

\[
q=(2).
\]

Let

\[
f=(1,1).
\]

The multiplicity-weighted degrees are

\[
d_q(0)=d_q(1)=2.
\]

Therefore the active hypothesis holds:

\[
f(0)=1\le2=d_q(0)
\]

and

\[
f(1)=1\le2=d_q(1).
\]

The total multiplicity is

\[
Q=2>1.
\]

### Exhaustion of all nonempty shores

There are exactly three nonempty shores:

\[
\{0\},
\qquad
\{1\},
\qquad
\{0,1\}.
\]

#### Shore \(U=\{0\}\)

The unique support edge crosses the shore.

Therefore

\[
y_0\in\{0,1,2\}.
\]

Since

\[
f(U)=1,
\]

the admissibility total is

\[
f(U)+Y(y)=1+y_0.
\]

For \(y_0=0\),

\[
f(U)+Y(y)=1,
\]

which is odd but below \(3\).

For \(y_0=1\),

\[
f(U)+Y(y)=2,
\]

which is even and below \(3\).

For \(y_0=2\),

\[
f(U)+Y(y)=3,
\]

which is odd and at least \(3\).

Thus the unique admissible compact selection for this shore is

\[
y=(2).
\]

Because the shore is a singleton,

\[
e_q(U)=0.
\]

Hence the raw witness-attaining value is

\[
N=2(e_q(U)+Y(y))
 =2(0+2)
 =4,
\]

and

\[
D=f(U)+Y(y)-1
 =1+2-1
 =2.
\]

Therefore

\[
(N,D)=(4,2)
\]

and the mathematical ratio is

\[
\frac{4}{2}=2.
\]

#### Shore \(U=\{1\}\)

This case is symmetric.

Again the unique admissible boundary selection is

\[
y=(2),
\]

with raw value

\[
(N,D)=(4,2)
\]

and mathematical ratio

\[
2.
\]

#### Shore \(U=\{0,1\}\)

The support edge is internal, so the boundary is empty.

Therefore necessarily

\[
Y(y)=0.
\]

Also,

\[
f(U)=1+1=2.
\]

Hence

\[
f(U)+Y(y)=2.
\]

This is even and below \(3\).

Therefore no admissible compact pair uses the whole-vertex shore.

### Global conclusion

Every nonempty shore and every possible compact boundary count has been exhausted.

The admissible family consists exactly of the two witnesses

\[
(\{0\},(2))
\]

and

\[
(\{1\},(2)).
\]

Both attain mathematical value

\[
2.
\]

Therefore the exact global optimum is

\[
\boxed{2}.
\]

Both witnesses have the raw witness-attaining value

\[
(4,2).
\]

Thus the global optimum has at least two distinct maximizing witnesses.

### Machine-facing expected result

Global mathematical value:

- ratio: `2`

Maximizing witness A:

- shore: `[0]`
- dense_y: `(2,)`
- raw_value: `(4, 2)`

Maximizing witness B:

- shore: `[1]`
- dense_y: `(2,)`
- raw_value: `(4, 2)`

The mathematical contract does not prefer either witness.

A deterministic brute implementation using increasing shore-mask order may return
witness A first, but that is an implementation convention rather than a uniqueness claim.

### What this oracle protects

This oracle checks:

1. complete exhaustion of all nonempty shores;
2. compact multiplicity \(q_0=2\) as two individually selectable copies;
3. exact parity and lower-bound admissibility;
4. exact raw witness-value formulas;
5. exact global value \(2\);
6. existence of at least two distinct global maximizing witnesses;
7. the rule that correct global value does not imply unique witness identity;
8. deterministic implementation choice must not be mistaken for mathematical preference.

### Oracle status

**Hand-derived before the B9 test that consumes it.**

No brute-verifier output, solver output, or other implementation result was used to
establish the expected global value or the existence of the two maximizing witnesses.


---

## Stage-2A exact-flow representation and deterministic-trace ruling

**Governing obligations:** DESIGN R9; TEST_PLAN FL1--FL12; canonical-source
`thm:GR` and `lem:ek`.

This ruling closes the flow-layer representation boundary before either
`tests/test_flow.py` or `exactfrac/flow.py` exists.

### Flow-layer mathematical input

The reference backend consumes:

- a vertex count `N`;
- distinct source and sink indices `s` and `t`;
- a finite ordered tuple of directed arc triples `(u, v, capacity)`.

The vertex universe is exactly

\[
\{0,1,\ldots,N-1\}.
\]

`N`, `s`, `t`, every endpoint, and every capacity must be exact Python `int`
objects. Boolean values are rejected even though `bool` is a Python subclass of `int`.
Capacities must be nonnegative. The flow correctness path uses no `float`, tolerance, or
`Fraction`.

The returned source shore is the internal shore bitmask ruled in DESIGN §4.2: bit `v` is
set exactly when vertex `v` belongs to the shore.

### Validation and canonicalization order

Validation precedes normalization.

1. Validate `N`, `s`, and `t`, requiring `N >= 2`, `0 <= s,t < N`, and `s != t`.
2. Require the outer arc collection and every arc record to be tuples; require each arc
   record to have exactly three entries.
3. Validate the exact integer type and range of both endpoints and the exact integer type
   and nonnegativity of the capacity.
4. Discard a validated loop `(v, v, capacity)`. A loop crosses no directed cut, and the
   canonical source explicitly discards contraction-generated loops.
5. Sort the validated nonloop records lexicographically by `(u, v, capacity)`. This makes
   the normalization path independent of the raw record order without relying on hash-table
   iteration or average-case dictionary behavior.
6. Aggregate consecutive records having the same ordered pair `(u, v)` by exact capacity
   summation.
7. Retain a canonical nonloop arc even when its aggregated capacity is zero. Otherwise
   FL4 would be collapsed incorrectly into the `E = 0` case.

Let `E_in` be the number of supplied arc records before loop deletion and aggregation, and
let `E` be the number of normalized nonloop ordered pairs. The residual-network arc count,
the capacity sum, `u_max`, and all Stage-2A zero-safe number-size accounting refer to the
normalized tuple and therefore use `E`. When raw and normalized counts agree, the catalog
continues to write simply `E`.

Validation and deterministic sort-and-aggregate normalization use

\[
O\!\left(E_{\mathrm{in}}\log(E_{\mathrm{in}}+1)\right)
\]

comparisons and `O(E_in)` exact additions. Edmonds--Karp on the normalized network uses
`O(N + N E^2)` arithmetic and comparison operations. Since `E <= E_in` and `N >= 2`, the
complete flow-layer call, including normalization, uses

\[
O\!\left(
N+E_{\mathrm{in}}\log(E_{\mathrm{in}}+1)+NE^2
\right)
=
O\!\left(N+N E_{\mathrm{in}}^2\right).
\]

Thus parallel-record compression never hides the work required to read and normalize the
supplied input. Because all capacities are nonnegative, every intermediate aggregation sum
is at most its final normalized capacity, so the normalized `u_max` also bounds the
normalization arithmetic. For already-canonical input, `E_in = E`, and the complete carrier
is the governing `O(N + N E^2)` form.

Repeated copies of `(u, v)` are parallel directed arcs and are aggregated. Arcs `(u, v)`
and `(v, u)` are antiparallel, not parallel duplicates; they remain distinct original
arcs with independent capacities. The existence of `(u, v)` never creates original
capacity on `(v, u)`.

Within this flow-layer interface, type violations raise `TypeError`. Structurally or
numerically invalid values with the correct outer type raise `ValueError`. This local split
does not settle the later external `exactfrac.instance` API-error taxonomy deferred by
DESIGN §4.1. In particular, a loop does not hide an invalid capacity: validation occurs
before loop deletion.

### Residual representation and fixed adjacency order

Number the normalized original arcs

\[
a_0,a_1,\ldots,a_{E-1}
\]

in canonical order. For each `a_i = (u, v, c)` in increasing arc-index order:

1. append its forward residual entry to the adjacency list of `u`, initially with
   residual capacity `c`;
2. append its paired reverse residual entry to the adjacency list of `v`, initially with
   residual capacity `0`.

Thus each original arc contributes exactly two directed residual-adjacency entries. An
original antiparallel arc contributes its own distinct forward/reverse pair.

A breadth-first search uses a FIFO queue, marks a vertex when first discovered, and scans
each reached vertex's residual adjacency list in the insertion order above. An adjacency
entry is counted as scanned whether its current residual capacity is positive or zero.

For an augmenting-path search, the search stops immediately when `t` is first discovered.
The parent entry that first discovers each vertex is never replaced. After the final
augmentation, the first breadth-first search that fails to discover `t` runs to
exhaustion; its reached set is returned directly as the inclusionwise-minimal minimum
source shore. No second reachability search is performed. When `E = 0`, the backend uses
the canonical zero-arc branch and invokes no breadth-first search.

The deterministic counters are therefore:

- `augmentations`: successful residual `s`--`t` path augmentations;
- `bfs_scans`: residual-adjacency entries inspected across every breadth-first search,
  including zero-capacity entries and the final failed/reachability search.

### Immutable number-size instrumentation

The flow-local immutable stats record `peak_generated_value`, the largest nonnegative
integer among:

- every initialized or updated residual capacity;
- every augmenting-path bottleneck;
- every running total-flow value.

It is `0` when no positive value occurs. This diagnostic scalar leaks no mutable backend
object, is never certificate data, and does not replace DESIGN's later aggregate
`peak_integer_bits` field. For nonnegative integer `z`, Python's `z.bit_length()` equals

\[
\left\lceil\log_2(1+z)\right\rceil,
\]

including `0.bit_length() = 0`. Therefore FL11 is checked exactly by comparing
`peak_generated_value.bit_length()` with

\[
l+\left\lceil\log_2(E+1)\right\rceil.
\]

A later aggregate `peak_integer_bits` telemetry field uses DESIGN's separate
`max(1, abs(x).bit_length())` convention.

---

## ORACLE-005 — Zero-arc directed minimum cut

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `lem:ek`; TEST_PLAN FL2, FL9, FL10, FL11.

### Instance

Let

\[
N=4,
\qquad
s=1,
\qquad
t=3,
\qquad
A=().
\]

The nonzero source index prevents an implementation from hard-coding vertex `0` as the
source shore.

### Complete directed-cut enumeration

Every source-containing, sink-avoiding shore is obtained by choosing independently whether
vertices `0` and `2` accompany `s=1`:

| Source shore | Bitmask | Directed cut capacity |
|---|---:|---:|
| `\{1\}` | `2` | `0` |
| `\{0,1\}` | `3` | `0` |
| `\{1,2\}` | `6` | `0` |
| `\{0,1,2\}` | `7` | `0` |

Thus every eligible shore is minimum and their inclusionwise-minimal member is exactly

\[
\{1\}.
\]

### Deterministic trace

There are no normalized arcs and hence no residual-adjacency entries. The zero-arc branch
returns without invoking breadth-first search.

### Machine-facing expected result

- normalized arcs: `()`
- `E = 0`
- `value = 0`
- `source_shore = 2`
- source-shore vertices: `[1]`
- `augmentations = 0`
- `bfs_scans = 0`
- `peak_generated_value = 0`

### Zero-safe number accounting

\[
u_{\max}=0,
\qquad
l=\left\lceil\log_2(1)\right\rceil=0.
\]

Also

\[
1+\sum_a u_a=1=(E+1)(u_{\max}+1)=(E+1)2^l.
\]

Every generated flow or residual value is zero.

### Oracle status

**Hand-derived before any Stage-2A test or flow implementation.**

No max-flow or min-cut implementation was used to establish the result.

---

## ORACLE-006 — Positive network with two minimum source shores

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `thm:GR`, `lem:ek`; TEST_PLAN FL3, FL6, FL9--FL11.

### Instance

Let

\[
N=3,
\qquad
s=0,
\qquad
t=2,
\]

with canonical directed arcs

\[
(0,1,2),
\qquad
(0,2,1),
\qquad
(1,2,2).
\]

The canonical arc indices are

\[
a_0=(0,1,2),
\qquad
a_1=(0,2,1),
\qquad
a_2=(1,2,2).
\]

### Complete directed-cut enumeration

There are exactly two source-containing, sink-avoiding shores:

| Source shore | Bitmask | Crossing original arcs | Capacity |
|---|---:|---|---:|
| `\{0\}` | `1` | `a_0,a_1` | `2+1=3` |
| `\{0,1\}` | `3` | `a_1,a_2` | `1+2=3` |

Therefore the exact minimum value is `3`, the complete minimum-cut family is

\[
\bigl\{\{0\},\{0,1\}\bigr\},
\]

and the inclusionwise-minimal minimum source shore is `\{0\}`.

### Residual adjacency order

- vertex `0`: `a_0^+`, `a_1^+`;
- vertex `1`: `a_0^-`, `a_2^+`;
- vertex `2`: `a_1^-`, `a_2^-`.

Here `a_i^+` denotes the original forward residual entry and `a_i^-` its paired reverse
entry.

### Deterministic shortest-augmenting-path trace

#### Search 1

The scanned entries are

\[
a_0^+,
\quad
a_1^+.
\]

Vertex `1` is discovered first; `a_1^+` then discovers `t=2`, so the search stops after
`2` scans. The selected path is

\[
0\to2
\]

with bottleneck `1`. The running flow value becomes `1`.

#### Search 2

The scanned entries are

\[
a_0^+,
\quad
a_1^+,
\quad
a_0^-,
\quad
a_2^+.
\]

The selected path is

\[
0\to1\to2
\]

with bottleneck `2`. The running flow value becomes `3`.

#### Final failed/reachability search

Both original entries leaving `0` now have zero residual capacity. The search scans

\[
a_0^+,
\quad
a_1^+
\]

and reaches only vertex `0`.

Hence

\[
\texttt{bfs\_scans}=2+4+2=8
\]

and there are exactly two successful augmentations.

### Machine-facing expected result

- `value = 3`
- `source_shore = 1`
- source-shore vertices: `[0]`
- `augmentations = 2`
- `bfs_scans = 8`
- `peak_generated_value = 3`
- augmenting paths: `0->2`, then `0->1->2`
- bottlenecks: `1`, then `2`

### Zero-safe number accounting

Here

\[
E=3,
\qquad
u_{\max}=2,
\qquad
l=\left\lceil\log_2(3)\right\rceil=2,
\qquad
\sum_a u_a=5.
\]

Thus

\[
1+5=6
\le4\cdot3=12
\le4\cdot2^2=16.
\]

The largest generated value is the final total flow `3`, and

\[
\operatorname{bitlength}(3)=2
\le
2+\left\lceil\log_2(4)\right\rceil=4.
\]

### Oracle status

**Hand-derived before any Stage-2A test or flow implementation.**

The value follows from the complete cut table, and the counters follow from the fixed
residual-adjacency scan order above.

---

## ORACLE-007 — Positive arc set with every capacity zero

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `lem:ek`; TEST_PLAN FL4, FL9--FL11.

### Instance

Let

\[
N=3,
\qquad
s=0,
\qquad
t=2,
\]

with canonical directed arcs

\[
a_0=(0,1,0),
\qquad
a_1=(1,2,0).
\]

The normalized arc set is nonempty: `E = 2`.

### Complete directed-cut enumeration

| Source shore | Bitmask | Crossing original arcs | Capacity |
|---|---:|---|---:|
| `\{0\}` | `1` | `a_0` | `0` |
| `\{0,1\}` | `3` | `a_1` | `0` |

Both shores are minimum, and the inclusionwise-minimal one is `\{0\}`.

### Deterministic trace

The only residual-adjacency entry at vertex `0` is the zero-capacity forward entry
`a_0^+`. The first search scans that entry, discovers no new vertex, fails, and returns
its reached set `\{0\}`.

This is one genuine breadth-first search over a positive-size residual representation; it
is not the `E = 0` branch.

### Machine-facing expected result

- `E = 2`
- `value = 0`
- `source_shore = 1`
- source-shore vertices: `[0]`
- `augmentations = 0`
- `bfs_scans = 1`
- `peak_generated_value = 0`

### Zero-safe number accounting

\[
u_{\max}=0,
\qquad
l=0,
\qquad
1+\sum_a u_a=1
\le3
=(E+1)(u_{\max}+1)
=(E+1)2^l.
\]

Every generated flow or residual value is zero.

### Oracle status

**Hand-derived before any Stage-2A test or flow implementation.**

No flow output was used to distinguish this case from the zero-arc oracle.

---

## ORACLE-008 — Positive arcs, no source-to-sink path, and directed-cut semantics

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `thm:GR`, `lem:ek`; TEST_PLAN FL1, FL5, FL7, FL9--FL11.

### Instance

Let

\[
N=4,
\qquad
s=0,
\qquad
t=3,
\]

with canonical directed arcs

\[
a_0=(0,1,2),
\qquad
a_1=(1,2,1),
\qquad
a_2=(3,2,7).
\]

The positive-capacity arc `a_2` points from the sink into vertex `2`. It must not be
counted as leaving the eventual source shore and must not create usable original capacity
from `2` to `3`.

### Complete directed-cut enumeration

The eligible shores are:

| Source shore | Bitmask | Crossing original arcs | Capacity |
|---|---:|---|---:|
| `\{0\}` | `1` | `a_0` | `2` |
| `\{0,1\}` | `3` | `a_1` | `1` |
| `\{0,2\}` | `5` | `a_0` | `2` |
| `\{0,1,2\}` | `7` | none | `0` |

The arc `a_2=(3,2,7)` enters `\{0,1,2\}` and therefore contributes zero to its directed
out-cut. The unique minimum source shore is

\[
\{0,1,2\}.
\]

### Residual adjacency order and deterministic trace

The reached vertices and scans are:

1. at vertex `0`, scan `a_0^+` and discover `1`;
2. at vertex `1`, scan `a_0^-` with residual `0`, then scan `a_1^+` and discover `2`;
3. at vertex `2`, scan `a_1^-` with residual `0`, then scan `a_2^-` with residual `0`.

The original positive capacity of `a_2` resides on the separate forward entry at vertex
`3`; its reverse residual entry at vertex `2` begins at zero. Thus `t=3` is not reached.

The sole search fails after `5` scans and returns exactly `\{0,1,2\}`.

### Machine-facing expected result

- `value = 0`
- `source_shore = 7`
- source-shore vertices: `[0, 1, 2]`
- `augmentations = 0`
- `bfs_scans = 5`
- `peak_generated_value = 7`

### Zero-safe number accounting

\[
E=3,
\qquad
u_{\max}=7,
\qquad
l=\left\lceil\log_2(8)\right\rceil=3,
\qquad
\sum_a u_a=10.
\]

Hence

\[
1+10=11
\le4\cdot8=32
=4\cdot2^3.
\]

The largest initialized residual capacity is `7`, and

\[
\operatorname{bitlength}(7)=3
\le3+\left\lceil\log_2(4)\right\rceil=5.
\]

### What this oracle kills

This fixture fails any backend that:

1. treats directed arcs as undirected edges;
2. counts an entering arc in the directed out-cut;
3. assigns original capacity to a reverse residual entry;
4. returns `\{s\}` automatically whenever the flow value is zero.

### Oracle status

**Hand-derived before any Stage-2A test or flow implementation.**

The complete cut table and the one-search residual trace establish the result directly.

---

## ORACLE-009 — Loop deletion and repeated-directed-pair aggregation

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `lem:ek`; TEST_PLAN FL1, FL3, FL9--FL11.

### Raw input

Let

\[
N=3,
\qquad
s=0,
\qquad
t=2,
\]

and supply the deliberately noncanonical raw arc tuple

```text
(
    (1, 2, 4),
    (0, 1, 2),
    (1, 1, 7),
    (0, 2, 1),
    (0, 1, 3),
    (0, 1, 0),
)
```

The supplied record count is `E_in = 6`.

Every record is validated first. The loop `(1,1,7)` is then discarded. The three copies
of `(0,1)` are aggregated exactly:

\[
2+3+0=5.
\]

The normalized canonical arc tuple is therefore

```text
(
    (0, 1, 5),
    (0, 2, 1),
    (1, 2, 4),
)
```

with normalized arc count `E = 3`.

Thus this fixture has `E_in = 6` and `E = 3`; its input-normalization work is charged by
the carrier ruling above rather than being hidden by the smaller normalized support.

### Complete directed-cut enumeration

| Source shore | Bitmask | Crossing normalized arcs | Capacity |
|---|---:|---|---:|
| `\{0\}` | `1` | `(0,1,5)`, `(0,2,1)` | `6` |
| `\{0,1\}` | `3` | `(0,2,1)`, `(1,2,4)` | `5` |

Thus the exact value is `5`, attained uniquely by source shore `\{0,1\}`.

### Deterministic trace

The normalized residual adjacency order is identical to ORACLE-006's three-arc shape.

1. Search 1 scans `2` entries and selects `0->2` with bottleneck `1`.
2. Search 2 scans `4` entries and selects `0->1->2` with bottleneck `4`.
3. The final search scans `4` entries. Residual capacity `1` remains on `0->1`, so vertices
   `0` and `1` are reached; `t=2` is not.

Therefore

\[
\texttt{bfs\_scans}=2+4+4=10.
\]

### Machine-facing expected result

Both the raw tuple above and the already-normalized tuple must return exactly:

- `value = 5`
- `source_shore = 3`
- source-shore vertices: `[0, 1]`
- `augmentations = 2`
- `bfs_scans = 10`
- `peak_generated_value = 5`

Their complete immutable results and stats must be equal. Splitting one directed capacity
among repeated records, changing raw record order, inserting a valid loop, and inserting a
zero-capacity duplicate do not create distinct residual support after normalization.

### Zero-safe number accounting

Accounting uses the normalized nonloop tuple:

\[
E=3,
\qquad
u_{\max}=5,
\qquad
l=\left\lceil\log_2(6)\right\rceil=3,
\qquad
\sum_a u_a=10.
\]

Thus

\[
1+10=11
\le4\cdot6=24
\le4\cdot2^3=32.
\]

The largest generated value is `5`, and

\[
\operatorname{bitlength}(5)=3
\le3+\left\lceil\log_2(4)\right\rceil=5.
\]

### Oracle status

**Hand-derived before any Stage-2A test or flow implementation.**

The expected trace is derived only after applying the representation ruling above; no
implementation output established the normalization result.

---

## ORACLE-010 — Reverse-residual cancellation is necessary

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `lem:ek`; TEST_PLAN FL3, FL8--FL11.

### Instance

Let the vertices be

\[
0=s,
\quad
1=L_1,
\quad
2=L_2,
\quad
3=R_1,
\quad
4=R_2,
\quad
5=t.
\]

Every capacity is `1`, and the canonical directed arcs are

\[
\begin{aligned}
a_0&=(0,1,1), & a_1&=(0,2,1),\\
a_2&=(1,3,1), & a_3&=(1,4,1),\\
a_4&=(2,3,1), & a_5&=(3,5,1),\\
a_6&=(4,5,1). &&
\end{aligned}
\]

This is the unit-capacity flow encoding of a two-left/two-right matching instance. The
first deterministic augmenting path matches `L_1` to `R_1`; obtaining value `2` then
requires cancellation of that middle choice.

### Complete directed-cut enumeration

Every eligible shore is `\{0\}` together with an arbitrary subset of
`\{1,2,3,4\}`. Direct enumeration gives:

| Source shore | Bitmask | Capacity |
|---|---:|---:|
| `\{0\}` | `1` | `2` |
| `\{0,1\}` | `3` | `3` |
| `\{0,2\}` | `5` | `2` |
| `\{0,1,2\}` | `7` | `3` |
| `\{0,3\}` | `9` | `3` |
| `\{0,1,3\}` | `11` | `3` |
| `\{0,2,3\}` | `13` | `2` |
| `\{0,1,2,3\}` | `15` | `2` |
| `\{0,4\}` | `17` | `3` |
| `\{0,1,4\}` | `19` | `3` |
| `\{0,2,4\}` | `21` | `3` |
| `\{0,1,2,4\}` | `23` | `3` |
| `\{0,3,4\}` | `25` | `4` |
| `\{0,1,3,4\}` | `27` | `3` |
| `\{0,2,3,4\}` | `29` | `3` |
| `\{0,1,2,3,4\}` | `31` | `2` |

The exact minimum value is `2`. The complete minimum-cut family is

\[
\bigl\{
\{0\},
\{0,2\},
\{0,2,3\},
\{0,1,2,3\},
\{0,1,2,3,4\}
\bigr\}.
\]

Its inclusionwise-minimal member is `\{0\}`.

### Residual adjacency order

- vertex `0`: `a_0^+`, `a_1^+`;
- vertex `1`: `a_0^-`, `a_2^+`, `a_3^+`;
- vertex `2`: `a_1^-`, `a_4^+`;
- vertex `3`: `a_2^-`, `a_4^-`, `a_5^+`;
- vertex `4`: `a_3^-`, `a_6^+`;
- vertex `5`: `a_5^-`, `a_6^-`.

### Deterministic shortest-augmenting-path trace

#### Search 1: ten scans

The scanned entries, in order, are

\[
\begin{aligned}
&a_0^+,a_1^+,\\
&a_0^-,a_2^+,a_3^+,\\
&a_1^-,a_4^+,\\
&a_2^-,a_4^-,a_5^+.
\end{aligned}
\]

The first selected path is

\[
0\to1\to3\to5
\]

using `a_0^+,a_2^+,a_5^+`, with bottleneck `1`.

#### Search 2: twelve scans

After the first augmentation, `a_2^-` has residual capacity `1`. The second scan order is

\[
\begin{aligned}
&a_0^+,a_1^+,\\
&a_1^-,a_4^+,\\
&a_2^-,a_4^-,a_5^+,\\
&a_0^-,a_2^+,a_3^+,\\
&a_3^-,a_6^+.
\end{aligned}
\]

The selected path is

\[
0\to2\to3\to1\to4\to5.
\]

Its middle step `3->1` is the reverse residual entry `a_2^-`. Augmenting on this path
cancels the earlier unit on original arc `1->3`, then sends that unit through `1->4`.
The running flow value becomes `2`.

Without usable created reverse residual capacity, no second augmenting path would exist
after the deterministic first choice.

#### Final failed/reachability search: two scans

Both original arcs leaving `0` are saturated. The final search scans `a_0^+` and `a_1^+`,
reaches no other vertex, and returns `\{0\}`.

Therefore

\[
\texttt{bfs\_scans}=10+12+2=24
\]

and

\[
\texttt{augmentations}=2.
\]

### Machine-facing expected result

- `value = 2`
- `source_shore = 1`
- source-shore vertices: `[0]`
- `augmentations = 2`
- `bfs_scans = 24`
- `peak_generated_value = 2`
- first path: `0->1->3->5`
- second path: `0->2->3->1->4->5`
- required reverse residual step: `3->1`, paired with original arc `a_2=(1,3,1)`

### Zero-safe number accounting

\[
E=7,
\qquad
u_{\max}=1,
\qquad
l=1,
\qquad
\sum_a u_a=7.
\]

Hence

\[
1+7=8
\le8\cdot2=16
=8\cdot2^1.
\]

The largest generated value is the final total flow `2`, and

\[
\operatorname{bitlength}(2)=2
\le1+\left\lceil\log_2(8)\right\rceil=4.
\]

### Oracle status

**Hand-derived before any Stage-2A test or flow implementation.**

The value is fixed by exhaustive cut enumeration. The reverse step and exact counters
follow from the ruled residual-entry order.

---

## ORACLE-011 — One-arc support-controlled magnitude family

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `lem:ek`; TEST_PLAN FL9--FL12.

### Family

For every integer `b >= 0`, let

\[
N=2,
\qquad
s=0,
\qquad
t=1,
\]

with the single canonical directed arc

\[
a_0=(0,1,2^b).
\]

The support is fixed while only the binary encoding length of the capacity changes.

### Complete directed-cut enumeration

The only source-containing, sink-avoiding shore is `\{0\}`. Its capacity is exactly

\[
2^b.
\]

Therefore the exact minimum-cut and maximum-flow value is `2^b`, and the unique returned
source shore is `\{0\}`.

### Deterministic trace

1. The first search scans the sole forward residual entry, discovers `t`, and augments by
   bottleneck `2^b`.
2. The final search scans the same forward entry at residual capacity zero and fails.

For every `b >= 0`:

- exactly one augmentation occurs;
- exactly two residual-adjacency entries are scanned in total;
- the returned source shore is unchanged;
- no unit-capacity expansion is permitted.

### Machine-facing expected result

For every tested `b >= 0`:

- `value = 1 << b`
- `source_shore = 1`
- source-shore vertices: `[0]`
- `augmentations = 1`
- `bfs_scans = 2`
- `peak_generated_value = 1 << b`
- `(1 << b).bit_length() = b + 1`

The finite regression set may include, for example,

```text
b in (0, 1, 7, 31, 127, 511)
```

without changing the hand proof for the whole family.

### Zero-safe number accounting

Here

\[
E=1,
\qquad
u_{\max}=2^b,
\qquad
l=\left\lceil\log_2(2^b+1)\right\rceil=b+1.
\]

Thus

\[
1+2^b
\le2(2^b+1)
\le2\cdot2^{b+1}.
\]

The largest generated value is `2^b`, whose zero-safe logarithmic size is `b+1`; the
`lem:ek` right-hand side is

\[
(b+1)+\left\lceil\log_2 2\right\rceil=b+2.
\]

### Interpretation

This oracle proves the exact trace only for this one-arc family. Its constant structural
counters are a regression against magnitude-driven iteration or unit-capacity expansion,
not a finite proof of strong polynomiality and not a claim that all fixed-support families
share one trace.

### Oracle status

**Hand-derived before any Stage-2A test or flow implementation.**

No measured runtime or implementation-generated counter was used to establish the family.

---

## ORACLE-012 — Flow-layer rejection matrix

**Classification:** `NEGATIVE`

**Source obligation:** TEST_PLAN FL1.

### Accepted normalization controls

The following are valid and are not rejection cases:

1. `E = 0`;
2. nonloop zero-capacity arcs;
3. validated nonnegative loops, which are discarded;
4. repeated ordered pairs, which are aggregated;
5. antiparallel ordered pairs, which remain distinct.

### Type violations

Each of the following must raise `TypeError` before any flow search begins:

- `N`, `s`, or `t` is not an exact Python `int`;
- an endpoint is not an exact Python `int`;
- a capacity is `True` or `False`;
- a capacity is a `float`;
- a capacity is `Fraction(1, 1)`;
- a capacity is a string or any other non-`int` object;
- the outer arc collection is not a tuple;
- an arc record is not a tuple.

### Value or structural violations

Each of the following must raise `ValueError` before any flow search begins:

- `N < 2`;
- `s == t`;
- `s` or `t` lies outside `0..N-1`;
- an arc endpoint lies outside `0..N-1`;
- an arc record does not contain exactly three entries;
- a capacity is negative.

A loop with a negative or nonintegral capacity is rejected rather than silently deleted,
because validation precedes loop normalization.

### Machine-facing rejection seeds

For `N=2`, `s=0`, `t=1`, representative rejected arc tuples include:

```text
((0, 1, -1),)                 # ValueError
((0, 1, True),)               # TypeError
((0, 1, 1.0),)                # TypeError
((0, 1, Fraction(1, 1)),)     # TypeError
((0, 2, 1),)                  # ValueError
((0, 1),)                     # ValueError
((0, 0, -1),)                 # ValueError before loop deletion
```

### Oracle status

**Ruled before any Stage-2A test or flow implementation.**

These are flow-layer rejection expectations, not outputs inferred from a backend. They
do not settle the deferred external instance-construction exception taxonomy.

---

## Stage-2A flow-oracle coverage matrix

| TEST_PLAN obligation | Pre-implementation oracle evidence |
|---|---|
| FL1 — exact directed-network input domain | representation ruling; ORACLE-008, ORACLE-009, ORACLE-012 |
| FL2 — zero-arc totalization | ORACLE-005 |
| FL3 — positive known-answer network | ORACLE-006 and ORACLE-009 |
| FL4 — positive arc set with all capacities zero | ORACLE-007 |
| FL5 — positive arcs but no residual source-to-sink path | ORACLE-008 |
| FL6 — inclusionwise-minimal minimum source shore | ORACLE-006 complete minimum-cut family |
| FL7 — directed-cut semantics | ORACLE-008 |
| FL8 — reverse-residual cancellation | ORACLE-010 |
| FL9 — independent tiny-network cut enumeration | complete cut tables in ORACLE-005 through ORACLE-011 |
| FL10 — deterministic counters and result | ruled scan semantics and exact traces in ORACLE-005 through ORACLE-011 |
| FL11 — exact arithmetic and zero-safe number bound | exact accounting in ORACLE-005 through ORACLE-011 |
| FL12 — support-controlled magnitude regression | ORACLE-011 |

All Stage-2A entries above are local flow-primitive fixtures. None is a claim about the
global optimum of a complete compact ExactFrac instance.
