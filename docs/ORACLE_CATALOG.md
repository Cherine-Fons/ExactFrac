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

---

## Post-Stage-2A production graph-instance oracle ruling

**Governing obligations:** DESIGN §4.1 and §4.1A; TEST_PLAN I1--I15 and §18;
canonical-source `def:instance`, `ass:active`, and `lem:aggregation`.

These fixtures are fixed after the production graph-instance authority commit
`61a96d12299f14e857b28d9a1e1be4078fba3aa4` and before either
`tests/test_instance.py` or `exactfrac/instance.py` exists.

They govern only production graph representation, normalization, strict object-level
serialization, error classification, immutability, compactness, and module isolation. They
make no claim about the modified set-pair-density optimum, any branch value, any shore
operation, or any downstream solver component.

The machine-facing exception expectations below use exact classes:

- malformed or noncanonical graph-instance data: exact `InvalidInstance`;
- structurally valid data outside the active regime: exact `UnsupportedInstance`.

Because both classes are sibling subclasses of `ValueError`, a test that merely catches
`ValueError` does not discharge the class distinction.

---

## ORACLE-013 — Canonical active graph instance and exact derived data

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `def:instance`; `ass:active`; DESIGN §4.1 and §4.1A;
TEST_PLAN I1, I10--I12, I15.

### Canonical instance

Let

```text
n = 4
edges = (
    (0, 1, 5),
    (0, 3, 2),
    (1, 2, 4),
    (2, 3, 3),
)
f = (2, 4, 6, 5)
labels = None
```

The vertex set is exactly `0,1,2,3`. Every edge has canonical orientation `u < v`, the
support pairs are strictly lexicographically increasing, every multiplicity is positive,
and the support is nonempty and loopless.

### Exact edge references and derived values

Canonical tuple position gives:

| `edge_ref` | Canonical edge |
|---:|---|
| `0` | `(0, 1, 5)` |
| `1` | `(0, 3, 2)` |
| `2` | `(1, 2, 4)` |
| `3` | `(2, 3, 3)` |

Therefore

```text
m = 4
support_edges = ((0, 1), (0, 3), (1, 2), (2, 3))
q = (5, 2, 4, 3)
Q = 14
```

The multiplicity degree at each vertex is obtained by adding the multiplicity of every
incident support edge:

\[
d_q(0)=5+2=7,
\]

\[
d_q(1)=5+4=9,
\]

\[
d_q(2)=4+3=7,
\]

\[
d_q(3)=2+3=5.
\]

Hence

```text
d_q = (7, 9, 7, 5)
```

and the active inequalities are

\[
2\le7,
\qquad
4\le9,
\qquad
6\le7,
\qquad
5\le5.
\]

The instance is therefore structurally valid and active.

### Machine-facing expected object

```text
n = 4
edges = ((0, 1, 5), (0, 3, 2), (1, 2, 4), (2, 3, 3))
f = (2, 4, 6, 5)
labels = None
m = 4
support_edges = ((0, 1), (0, 3), (1, 2), (2, 3))
q = (5, 2, 4, 3)
Q = 14
d_q = (7, 9, 7, 5)
```

The authoritative stored fields remain `n`, `edges`, `f`, and `labels`; the remaining
values are derived and cannot be independently mutated.

### Oracle status

**Hand-derived before any production graph-instance test or implementation.**

No `exactfrac.instance` output was used to establish the canonical order, edge references,
total multiplicity, degree tuple, or active status.

---

## ORACLE-014 — Raw aggregation, endpoint orientation, and deterministic edge references

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `lem:aggregation`; DESIGN §4.1A.4 and §4.1A.7;
TEST_PLAN I2, I3, I9, I11, I12.

### Target canonical instance

The target is the ORACLE-013 instance:

```text
((0, 1, 5), (0, 3, 2), (1, 2, 4), (2, 3, 3))
```

with `n = 4`, `f = (2, 4, 6, 5)`, and total multiplicity `Q = 14`.

### Raw form A

```text
raw_a = (
    (3, 2, 1),
    (1, 0, 2),
    (2, 1, 4),
    (0, 3, 2),
    (0, 1, 3),
    (2, 3, 2),
)
```

Endpoint orientation produces:

```text
(2, 3, 1)
(0, 1, 2)
(1, 2, 4)
(0, 3, 2)
(0, 1, 3)
(2, 3, 2)
```

The repeated unordered pairs aggregate as

\[
q_{01}=2+3=5,
\qquad
q_{23}=1+2=3.
\]

The other group totals are

\[
q_{03}=2,
\qquad
q_{12}=4.
\]

Sorting the four resulting support pairs gives exactly the target canonical tuple.

The raw total is

\[
1+2+4+2+3+2=14,
\]

so aggregation preserves `Q`.

### Raw form B

```text
raw_b = (
    (1, 2, 1),
    (3, 0, 2),
    (0, 1, 3),
    (3, 2, 2),
    (2, 1, 3),
    (1, 0, 2),
    (2, 3, 1),
)
```

Here

\[
q_{12}=1+3=4,
\qquad
q_{01}=3+2=5,
\qquad
q_{23}=2+1=3,
\qquad
q_{03}=2.
\]

Again the total multiplicity is

\[
1+2+3+2+3+2+1=14.
\]

After orientation, aggregation, and sorting, `raw_b` yields the same target canonical
instance.

### Deterministic normalization result

Each of the following must produce the complete ORACLE-013 canonical object:

```text
Instance.from_records(4, raw_a, (2, 4, 6, 5))
Instance.from_records(4, tuple(reversed(raw_a)), (2, 4, 6, 5))
Instance.from_records(4, raw_b, (2, 4, 6, 5))
```

In every case:

```text
edge_ref 0 = (0, 1, 5)
edge_ref 1 = (0, 3, 2)
edge_ref 2 = (1, 2, 4)
edge_ref 3 = (2, 3, 3)
```

and

```text
m = 4
q = (5, 2, 4, 3)
Q = 14
d_q = (7, 9, 7, 5)
```

The canonical constructor does not perform this repair. Supplying any reversed, repeated,
or out-of-order raw form directly to `Instance(...)` is an exact `InvalidInstance` case.

### Compactness requirement

Normalization sums multiplicities by group. It does not materialize five separate copies
of `(0,1)`, four separate copies of `(1,2)`, or any other unit-copy expansion.

### Oracle status

**Hand-derived before any production graph-instance test or implementation.**

The group sums, canonical order, and derived values were established from the raw records
and `lem:aggregation`, not from an instance normalizer.

---

## ORACLE-015 — Strict versioned serialization and nonalgorithmic labels

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN §4.1A.2, §4.1A.3, §4.1A.5, and §9;
TEST_PLAN I13--I15.

### Unlabeled canonical object

Use ORACLE-013 with `labels = None`.

Its exact JSON-ready object representation is:

```python
{
    "format": "exactfrac-instance/1",
    "n": 4,
    "edges": [
        [0, 1, 5],
        [0, 3, 2],
        [1, 2, 4],
        [2, 3, 3],
    ],
    "f": [2, 4, 6, 5],
}
```

The optional `labels` key is absent.

Strict object-level deserialization of this dictionary must reconstruct the exact
ORACLE-013 canonical instance.

### Labeled canonical object

Let

```text
labels = ("north", 17, "south", 23)
```

Every label is an exact built-in `str` or exact built-in `int`, the labels are pairwise
distinct, and the tuple is aligned with dense vertex order `0,1,2,3`.

The exact JSON-ready object is:

```python
{
    "format": "exactfrac-instance/1",
    "n": 4,
    "edges": [
        [0, 1, 5],
        [0, 3, 2],
        [1, 2, 4],
        [2, 3, 3],
    ],
    "f": [2, 4, 6, 5],
    "labels": ["north", 17, "south", 23],
}
```

Strict deserialization must reconstruct:

```text
labels = ("north", 17, "south", 23)
```

while preserving all mathematical graph data.

### Label-independence comparison

The labeled and unlabeled instances have the same:

```text
n
edges
f
m
support_edges
q
Q
d_q
edge_ref sequence
```

Their only governed difference is the `labels` field and the corresponding optional
serialized key.

No constructor, normalization result, edge reference, degree, or active-condition result
may depend on the label values.

### Strict deserialization boundary

`Instance.from_dict(...)` validates a canonical external object. It does not:

- reorient reversed serialized edges;
- aggregate repeated serialized edges;
- sort out-of-order serialized edges;
- ignore unknown keys;
- supply missing keys;
- accept a wrong format tag;
- accept tuple containers where the schema requires exact lists.

Those cases belong to ORACLE-016 and raise exact `InvalidInstance`.

### Oracle status

**Hand-derived before any production graph-instance test or implementation.**

The serialized forms were written directly from the ruled schema and the ORACLE-013
canonical data. No serializer or deserializer output established them.

---

## ORACLE-016 — Malformed production graph-instance rejection matrix

**Classification:** `NEGATIVE`

**Source obligations:** `def:instance`; DESIGN §4.1 and §4.1A.3--§4.1A.6;
TEST_PLAN I4--I7, I10, I11, I13, I14.

### Exact exception contract

Every case in this oracle raises an exception whose exact type is:

```text
InvalidInstance
```

The expected result is not merely “some `ValueError`.”

For type-adversarial tests, define a representative subclass:

```python
class IntSubclass(int):
    pass
```

### Canonical-constructor rejection seeds

Unless a different value is shown, use the valid control data:

```text
n = 2
edges = ((0, 1, 2),)
f = (1, 1)
labels = None
```

The following are exact `InvalidInstance` cases:

| Category | Representative input |
|---|---|
| nonexact `n` | `n=True`, `n=2.0`, `n=IntSubclass(2)` |
| invalid `n` value | `n=0`, `n=-1` |
| wrong edge container | `edges=[(0, 1, 2)]` |
| wrong edge-record container | `edges=([0, 1, 2],)` |
| short edge record | `edges=((0, 1),)` |
| fourth weight field | `edges=((0, 1, 2, 99),)` |
| negative endpoint | `edges=((-1, 1, 2),)` |
| out-of-range endpoint | `edges=((0, 2, 2),)` with `n=2` |
| nonexact endpoint | endpoint `True`, `1.0`, `Fraction(1, 1)`, or `IntSubclass(1)` |
| loop | `edges=((0, 0, 2),)` |
| reversed canonical edge | `edges=((1, 0, 2),)` |
| repeated canonical pair | `edges=((0, 1, 1), (0, 1, 1))` |
| out-of-order canonical tuple | `edges=((1, 2, 1), (0, 1, 1))`, `n=3`, `f=(1, 1, 1)` |
| zero multiplicity | `edges=((0, 1, 0),)` |
| negative multiplicity | `edges=((0, 1, -1),)` |
| nonexact multiplicity | `True`, `1.0`, `Fraction(1, 1)`, `IntSubclass(1)`, or a string |
| empty support | `edges=()` |
| wrong `f` container | `f=[1, 1]` |
| wrong `f` length | `f=(1,)` or `f=(1, 1, 1)` when `n=2` |
| nonpositive `f` | `f=(0, 1)` or `f=(-1, 1)` |
| nonexact `f` entry | `True`, `1.0`, `Fraction(1, 1)`, `IntSubclass(1)`, or a string |
| wrong label container | `labels=["a", "b"]` |
| wrong label length | `labels=("a",)` |
| duplicate labels | `labels=("a", "a")` |
| invalid label type | label `True`, `1.0`, `Fraction(1, 1)`, tuple, or other object |

The out-of-order three-vertex seed is structurally active if its edges are sorted:

```text
sorted edges = ((0, 1, 1), (1, 2, 1))
d_q = (1, 2, 1)
f = (1, 1, 1)
```

Therefore its canonical-constructor rejection isolates ordering rather than active failure.

### Raw-normalization rejection seeds

`Instance.from_records(...)` also raises exact `InvalidInstance` for:

- a non-tuple outer record container;
- a non-tuple individual record;
- wrong record arity;
- a loop;
- an out-of-range or nonexact endpoint;
- zero, negative, or nonexact multiplicity;
- malformed `n`, `f`, or labels.

Unlike reversed endpoints, loops are rejected and are not silently discarded.

### Strict-deserialization rejection seeds

Starting from the valid ORACLE-015 serialized object, each of the following raises exact
`InvalidInstance`:

- outer object is not an exact `dict`;
- a `dict` subclass is supplied;
- `format` is missing;
- `n`, `edges`, or `f` is missing;
- an unknown key is present;
- `format` is not exactly `exactfrac-instance/1`;
- `edges` is a tuple rather than an exact list;
- a serialized edge record is a tuple rather than an exact list;
- `f` is a tuple rather than an exact list;
- present `labels` is `None` or a tuple rather than an exact list;
- a serialized edge is reversed;
- serialized support pairs repeat;
- serialized edges are out of canonical order;
- any serialized numeric or label value violates the exact domain.

Strict deserialization does not repair any of these conditions.

### Oracle status

**Ruled before any production graph-instance test or implementation.**

The rejection matrix is derived from the production API boundary. It does not report
behavior observed from `exactfrac.instance`.

---

## ORACLE-017 — Unsupported active regime and malformed-before-active precedence

**Classification:** `NEGATIVE`

**Source obligations:** `ass:active`; DESIGN §4.1.7 and §4.1A.6;
TEST_PLAN I8 and I10.

### Unsupported seed A — nonisolated degree-capacity failure

```text
n = 2
edges = ((0, 1, 2),)
f = (3, 1)
labels = None
```

The support is nonempty, loopless, simple, canonically ordered, and has positive
multiplicity.

The exact degrees are:

```text
d_q = (2, 2)
```

Vertex `0` violates the active condition:

\[
f(0)=3>2=d_q(0).
\]

Expected exact exception:

```text
UnsupportedInstance
```

### Unsupported seed B — isolated vertex

```text
n = 3
edges = ((0, 1, 2),)
f = (1, 1, 1)
labels = None
```

The graph representation is structurally valid. Vertex `2` is isolated, so

```text
d_q = (2, 2, 0)
```

and

\[
f(2)=1>0=d_q(2).
\]

Expected exact exception:

```text
UnsupportedInstance
```

The isolated vertex is not itself malformed. The instance is rejected only because it is
outside the active theorem regime.

### Valid active empty-family control

The existing ORACLE-001 graph data are:

```text
n = 2
edges = ((0, 1, 1),)
f = (1, 1)
```

Here

```text
d_q = (1, 1)
```

so construction succeeds and raises neither production exception. The fact that the later
admissible optimization family is empty is not an instance-construction error.

### Malformed-before-active precedence seeds

Each following case has data that would also lead to an active-regime problem after a
hypothetical repair, but malformed validation must win first:

| Entry point and seed | Exact expected class |
|---|---|
| `Instance(3, ((1, 0, 2),), (1, 1, 1))` — reversed canonical edge plus isolated vertex | `InvalidInstance` |
| `Instance.from_records(3, ((0, 0, 2),), (1, 1, 1))` — loop plus isolated vertices | `InvalidInstance` |
| `Instance(2, ((0, 1, 0),), (3, 1))` — zero multiplicity plus apparent active failure | `InvalidInstance` |
| `Instance.from_dict(...)` with a wrong format tag and the data of unsupported seed A | `InvalidInstance` |

No malformed case may be relabeled `UnsupportedInstance` merely because an active check
would also fail.

### Oracle status

**Hand-derived and ruled before any production graph-instance test or implementation.**

The degree vectors and active violations were calculated directly from the canonical edge
data. No constructor output established the exception classes.

---

## ORACLE-018 — Module surface, immutability, isolation, and compact magnitude

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `def:instance`; DESIGN R10, §4.1A.1--§4.1A.3, §4.1A.8,
and §4.5.3; TEST_PLAN I11, I15, R3, R4, and D1.

### Exact public surface

The production module-level export sequence is exactly:

```text
Edge
Instance
InvalidInstance
UnsupportedInstance
```

Equivalently, tests may compare:

```python
tuple(exactfrac.instance.__all__) == (
    "Edge",
    "Instance",
    "InvalidInstance",
    "UnsupportedInstance",
)
```

The package root does not re-export those names in this unit.

The graph-instance module exposes no shore-helper or downstream solver API. In particular,
this unit does not introduce public names for:

```text
validate_shore
shore_from_list
shore_to_list
shore_complement
AtomicFamily
Witness
ExactBranchMin
SolveBranchStandard
SolveBranchAccelerated
StrongCompactMSPD
```

The absence list is a scope guard, not a complete forecast of every future symbol.

### Frozen and slotted canonical object

The authoritative stored-state names are exactly:

```text
n
edges
f
labels
```

The authority requires a frozen and slotted object but does not require one particular
Python implementation technique for achieving that contract. Assignments to the stored
fields after construction are rejected, and the tuple-backed `edges`, `f`, and optional
`labels` values are not list-mutable.

Derived properties do not create independently mutable graph state.

The graph-instance object has no graph-owned `full_mask` field or property in this unit;
shore-universe operations remain deferred to the separate shore layer.

### Compact enormous-multiplicity fixture

Let

```text
B = 1 << 4096
n = 2
edges = ((0, 1, B),)
f = (1, 1)
labels = None
```

Then

```text
m = 1
support_edges = ((0, 1),)
q = (B,)
Q = B
d_q = (B, B)
```

The active condition holds because `1 <= B` at both vertices.

The object contains exactly one support-edge record and one multiplicity integer. It does
not contain `B` unit-copy records and performs no iteration once per represented copy.

The multiplicity bit length is

```text
B.bit_length() = 4097
```

while the structural support size remains `m = 1`.

### Isolation boundary

Static and fresh-process checks must establish that importing `exactfrac.instance` does not
import any `exactfrac_verify` module.

Source inspection must also show that this unit does not import or implement shore,
family, witness, §4.5 raw-pair rational arithmetic, argmin, sign-routing, parity-cut,
branch, or global-solver machinery.

The cross-cutting production obligations TEST_PLAN R3--R4 and D1 apply to this module.
Consistently with DESIGN §4.5.3, which expressly names `instance` in the production
`Fraction` prohibition, static source checks must find no import of or from `fractions`,
no reference or call to `Fraction`, no float literal, no call to `float`, no true-division
operator, and no tolerance-based comparison. Static inspection must also establish that
no algorithmic enumeration derives its order from iteration over a Python `set`. Set
construction and membership tests are permitted; no output order or control-flow order may
be derived from iterating a set. These are source-level checks in the manner of the sealed
flow exactness test, not conclusions drawn from observed outputs.

### Oracle status

**Ruled before any production graph-instance test or implementation.**

The public surface, immutable field model, compact large-multiplicity result, and isolation
expectations come from the committed graph-instance authority rather than implementation
inspection.

---

## Production graph-instance oracle coverage matrix

| TEST_PLAN obligation | Pre-implementation oracle evidence |
|---|---|
| I1 — valid canonical instance | ORACLE-013 |
| I2 — repeated endpoint records | ORACLE-014 |
| I3 — reversed endpoint orientation | ORACLE-014 |
| I4 — loop | ORACLE-016 |
| I5 — empty support | ORACLE-016 |
| I6 — nonpositive multiplicity | ORACLE-016 |
| I7 — nonpositive `f` value | ORACLE-016 |
| I8 — active-condition failure | ORACLE-017 |
| I9 — deterministic canonical edge order | ORACLE-014 |
| I10 — exception taxonomy and validation precedence | ORACLE-016 and ORACLE-017 |
| I11 — exact Python domain and compact multiplicity | ORACLE-016 and ORACLE-018 |
| I12 — canonical constructor versus raw normalization | ORACLE-013 and ORACLE-014 |
| I13 — strict versioned object round trip | ORACLE-015 and ORACLE-016 |
| I14 — labels are nonalgorithmic metadata | ORACLE-015 and ORACLE-016 |
| I15 — module surface, immutability, and isolation | ORACLE-018 |
| R3 — no `Fraction` in solver path | ORACLE-018 isolation boundary |
| R4 — no floating point in correctness path | ORACLE-018 isolation boundary |
| D1 — no algorithmic iteration over Python `set` | ORACLE-018 isolation boundary |

These fixtures establish only graph-instance behavior. They do not implement or discharge
the later shore, witness, family, §4.5 raw-pair rational-arithmetic helper, cut-reduction,
branch, certificate, or global-optimization layers.

---

## Post-graph-instance production shore oracle ruling

**Governing obligations:** DESIGN §4.2 and §4.2A; TEST_PLAN S1--S12 and §19;
cross-cutting TEST_PLAN R3, R4, and D1.

These fixtures are fixed after the production shore-interface authority commit
`9d71ff1f0d433281142441695edffcffc29aa9a2` and before either
`tests/test_shore.py` or `exactfrac/shore.py` exists.

They govern only finite-universe shore-mask representation, exact validation, strict
sorted-index-list serialization, universe-relative complement, compactness, deterministic
source discipline, and module isolation. They do not compute graph-dependent quantities
such as `f(U)`, `e_q(U)`, `b_q(U)`, or `d_q(U)` and make no claim about any ExactFrac branch
or global optimum.

No governing-source theorem label is invented for this software representation seam.
S1--S3 are representation-level identities for already validated Python integer masks;
they do not require redundant public wrapper functions. S4--S6 and S7--S12 govern the
actual `exactfrac.shore` helper boundary.

Every malformed public input below has the exact expected exception class:

```text
ValueError
```

The expected class is the built-in `ValueError` itself, not `TypeError`, `InvalidInstance`,
`UnsupportedInstance`, or a shore-specific subclass. Exception prose is not part of the
oracle.

---

## ORACLE-019 — Empty, full, and mixed shores in a five-vertex universe

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN §4.2 and §4.2A.2--§4.2A.6; TEST_PLAN S1--S9.

### Five-vertex universe

Let

```text
n = 5
full = (1 << 5) - 1 = 31 = 0b11111
```

The dense vertex universe is exactly

```text
0, 1, 2, 3, 4
```

Define the mixed shore

```text
U = 21 = 0b10101
```

so that

```text
members(U) = [0, 2, 4]
```

and define

```text
T = 14 = 0b01110
```

so that

```text
members(T) = [1, 2, 3]
```

### Exact membership and cardinality

For `U`, the membership values in vertex order are

```text
v = 0: True
v = 1: False
v = 2: True
v = 3: False
v = 4: True
```

Equivalently,

```text
(bool(U & (1 << v)) for v in range(5))
= (True, False, True, False, True)
```

The exact cardinalities are

```text
U.bit_count() = 3
T.bit_count() = 3
```

### Exact union, intersection, and parity

The intersection is

```text
U & T = 4 = 0b00100
members(U & T) = [2]
```

Hence

```text
(U & T).bit_count() = 1
(U & T).bit_count() & 1 = 1
```

which agrees with the hand-derived odd parity of

\[
|U\cap T|=1.
\]

The union is

```text
U | T = 31 = full
members(U | T) = [0, 1, 2, 3, 4]
```

### Exact universe-relative complement

The complement of `U` relative to the five-vertex universe is

```text
C = full ^ U
  = 31 ^ 21
  = 10
  = 0b01010
```

Therefore

```text
members(C) = [1, 3]
C.bit_count() = 2
```

and the complement identities are

```text
U & C = 0
U | C = 31
full ^ C = U
```

The intersection parity with the complement is even:

```text
(U & C).bit_count() & 1 = 0
```

Bare Python complement is not a valid finite-universe shore:

```text
~U = -22
```

so passing `~U` to a mask-consuming shore helper must raise exact built-in `ValueError`.

### Empty and full shore boundaries

The empty shore is

```text
E = 0 = 0b00000
members(E) = []
E.bit_count() = 0
shore_complement(5, E) = 31
```

The complete shore is

```text
F = 31 = 0b11111
members(F) = [0, 1, 2, 3, 4]
F.bit_count() = 5
shore_complement(5, F) = 0
```

Both `E` and `F` are valid generic shore representations. Nonemptiness and properness are
consumer-owned predicates and are not imposed by `validate_shore`.

### Strict sorted-list serialization

The exact encoding and decoding results are

| Shore | Integer mask | Encoded list | Decoded mask |
|---|---:|---|---:|
| empty | `0` | `[]` | `0` |
| mixed `U` | `21` | `[0, 2, 4]` | `21` |
| complement `C` | `10` | `[1, 3]` | `10` |
| full | `31` | `[0, 1, 2, 3, 4]` | `31` |

Every emitted list is a fresh exact built-in `list`. Mutating that list cannot change the
integer shore from which it was derived.

### One-vertex edge universe

For the smallest valid universe,

```text
n = 1
full_mask(1) = 1
```

and the complete shore table is

| Shore | Mask | Encoded list | Complement |
|---|---:|---|---:|
| empty | `0` | `[]` | `1` |
| full | `1` | `[0]` | `0` |

This confirms that `n = 1` is valid and that the generic shore layer permits both shores.

### Machine-facing expected results

```text
full_mask(5) = 31
validate_shore(5, 0) = 0
validate_shore(5, 21) = 21
validate_shore(5, 31) = 31
shore_to_list(5, 0) = []
shore_to_list(5, 21) = [0, 2, 4]
shore_to_list(5, 10) = [1, 3]
shore_to_list(5, 31) = [0, 1, 2, 3, 4]
shore_from_list(5, []) = 0
shore_from_list(5, [0, 2, 4]) = 21
shore_from_list(5, [1, 3]) = 10
shore_from_list(5, [0, 1, 2, 3, 4]) = 31
shore_complement(5, 0) = 31
shore_complement(5, 21) = 10
shore_complement(5, 10) = 21
shore_complement(5, 31) = 0
```

### Oracle status

**Hand-derived before any production shore test or implementation.**

All masks, membership values, cardinalities, parity values, complements, and serialized
lists above follow directly from the five-bit and one-bit representations.

---

## ORACLE-020 — Exhaustive small-universe shore identity family

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN §4.2 and §4.2A.3--§4.2A.5; TEST_PLAN S1--S6 and S10.

### Exhaustive family

For every

```text
n in (1, 2, 3, 4, 5, 6, 7)
```

let

\[
M_n=(1\ll n)-1.
\]

For every valid mask

\[
0\le U\le M_n,
\]

define its independently specified sorted member list by

```text
members_n(U) = [v for v in range(n) if U & (1 << v)]
```

and for every ordered pair of valid masks `U,T`, use the exact integer expressions below.

The family contains

\[
\sum_{n=1}^{7}2^n=254
\]

valid single-shore cases and

\[
\sum_{n=1}^{7}4^n=21844
\]

ordered two-shore cases.

### Single-shore identities

For every one of the 254 valid masks:

```text
full_mask(n) = M_n
validate_shore(n, U) = U
shore_to_list(n, U) = members_n(U)
shore_from_list(n, members_n(U)) = U
U.bit_count() = len(members_n(U))
shore_complement(n, U) = M_n ^ U
shore_complement(n, shore_complement(n, U)) = U
U & shore_complement(n, U) = 0
U | shore_complement(n, U) = M_n
```

The encoded member list is strictly increasing because `range(n)` is traversed in increasing
vertex order.

Calling `shore_to_list(n, U)` twice must produce equal built-in lists that are distinct
mutable output objects. Mutating one emitted list does not alter `U` and does not alter the
next encoding of `U`.

For every valid `U`, Python's bare complement satisfies

\[
\mathord{\sim}U=-U-1<0,
\]

so `validate_shore(n, ~U)`, `shore_to_list(n, ~U)`, and
`shore_complement(n, ~U)` each raise exact built-in `ValueError`.

### Two-shore identities

For every one of the 21,844 ordered pairs `(U,T)`:

```text
members_n(U | T)
= sorted union of members_n(U) and members_n(T)

members_n(U & T)
= sorted intersection of members_n(U) and members_n(T)

(U & T).bit_count()
= len(set(members_n(U)) intersect set(members_n(T)))

(U & T).bit_count() & 1
= len(set(members_n(U)) intersect set(members_n(T))) & 1
```

The sets in the mathematical comparator above describe unordered membership only. They do
not authorize the production module to derive output order from Python set iteration.

For every vertex `v` in `0..n-1`:

```text
bool(U & (1 << v)) == (v in members_n(U))
bool(T & (1 << v)) == (v in members_n(T))
```

### Boundary coverage inside the family

For each tested `n`, the family includes:

```text
U = 0
U = M_n
T = 0
T = M_n
```

Therefore empty/full membership, cardinality, union, intersection, parity, complement, and
serialization are not separate assumptions; they are exhaustively included.

### Interpretation

S1--S3 are validated here as representation-level identities for Python integer masks.
They are not evidence for nonexistent `contains`, `cardinality`, or `intersection_parity`
wrapper functions.

S4--S6 are exercised through the actual public helpers:

```text
validate_shore
shore_complement
shore_to_list
shore_from_list
```

### Oracle status

**The family and exact expected formulas were fixed before any shore test or implementation.**

The values are determined by finite binary-set semantics, not by observing a future
`exactfrac.shore` module.

---

## ORACLE-021 — Shore-layer exact rejection matrix

**Classification:** `NEGATIVE`

**Source obligations:** DESIGN §4.2A.2, §4.2A.4, and §4.2A.6; TEST_PLAN S5 and S7--S9.

### Exact exception class

Every rejection in this oracle must raise

```text
ValueError
```

with

```python
type(exc) is ValueError
```

The following do not discharge the oracle:

```text
TypeError
InvalidInstance
UnsupportedInstance
any ValueError subclass
```

Exception messages are diagnostic and are not compared.

### Adversarial helper types

Tests may define the exact subclasses

```python
class IntSubclass(int):
    pass


class ListSubclass(list):
    pass
```

The subclasses remain invalid even when their contained numerical or list values otherwise
match a valid built-in object.

### Invalid universe sizes

For every public helper, `n` is invalid when it is any of:

```text
0
-1
True
False
1.0
Fraction(1, 1)
IntSubclass(1)
"1"
None
```

Representative calls are:

```text
full_mask(bad_n)
validate_shore(bad_n, 0)
shore_to_list(bad_n, 0)
shore_from_list(bad_n, [])
shore_complement(bad_n, 0)
```

Each raises exact built-in `ValueError` before a result is produced.

### Invalid shore masks

Fix

```text
n = 5
full_mask(5) = 31
```

Each of the following is invalid as a shore value for every mask-consuming helper:

| Seed | Reason |
|---|---|
| `-1` | negative mask |
| `32` | bit outside `0..4` |
| `1 << 100` | high out-of-universe bit |
| `True` | exact type is `bool`, not `int` |
| `False` | exact type is `bool`, not `int` |
| `21.0` | float |
| `Fraction(21, 1)` | non-`int` exact rational object |
| `IntSubclass(21)` | integer subclass |
| `"21"` | string |
| `None` | unrelated object |

Representative calls are:

```text
validate_shore(5, bad_U)
shore_to_list(5, bad_U)
shore_complement(5, bad_U)
```

Each raises exact built-in `ValueError`.

### Bare-complement rejection

For the valid masks

```text
0, 1, 10, 21, 31
```

bare Python complement gives

```text
~0  = -1
~1  = -2
~10 = -11
~21 = -22
~31 = -32
```

Every one is invalid when supplied to a mask-consuming helper.

### Invalid serialized outer containers

For `n = 5`, `shore_from_list` rejects each nonexact-list outer object:

```text
()
(0, 2, 4)
range(3)
"024"
None
ListSubclass([0, 2, 4])
iter([0, 2, 4])
```

It does not coerce any of them into a built-in list.

### Invalid serialized members

Each of the following exact-list inputs is rejected:

| Input | Reason |
|---|---|
| `[True]` | Boolean member |
| `[1.0]` | float member |
| `[Fraction(1, 1)]` | non-`int` exact rational member |
| `[IntSubclass(1)]` | integer-subclass member |
| `["1"]` | string member |
| `[None]` | unrelated member |
| `[-1]` | negative member |
| `[5]` | member outside `0..4` |
| `[0, 0]` | duplicate |
| `[0, 2, 2]` | later duplicate |
| `[2, 1]` | decreasing order |
| `[0, 3, 2]` | unsorted order |

No invalid sequence is sorted, deduplicated, truncated, or coerced.

### Valid strict-decoding controls

The following remain valid controls:

```text
shore_from_list(5, []) = 0
shore_from_list(5, [0]) = 1
shore_from_list(5, [0, 2, 4]) = 21
shore_from_list(5, [0, 1, 2, 3, 4]) = 31
```

These controls distinguish strict validation from a decoder that rejects every list.

### Validation order boundary

Every helper validates `n` first. Mask-consuming helpers then validate `U`.
`shore_from_list` then validates the exact outer list and visits entries in encounter order.

Tests may use noncoercible or protocol-hostile objects to ensure malformed data is rejected
rather than converted or consumed through an unintended protocol. They must not assert
exception prose to infer order.

### Oracle status

**Ruled before any production shore test or implementation.**

The rejection classes and seeds come from the committed shore API boundary, not from a
future implementation's observed exceptions.

---

## ORACLE-022 — Shore module surface, isolation, and 4096-vertex compactness

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN R10, §4.2A.1, §4.2A.7, and §4.2A.8;
TEST_PLAN S7, S11, S12, R3, R4, and D1.

### Exact public surface

The module-level export sequence is exactly:

```text
Shore
full_mask
validate_shore
shore_from_list
shore_to_list
shore_complement
```

Equivalently:

```python
tuple(exactfrac.shore.__all__) == (
    "Shore",
    "full_mask",
    "validate_shore",
    "shore_from_list",
    "shore_to_list",
    "shore_complement",
)
```

The alias is exactly:

```python
Shore is int
```

The package root does not re-export these names in this unit.

Membership, union, intersection, cardinality, and intersection parity remain direct integer
operations and do not appear as additional public wrappers.

### Graph-independent isolation boundary

Static and fresh-process checks must establish that importing `exactfrac.shore` imports no:

```text
exactfrac.instance
exactfrac_verify
exactfrac_verify.*
```

The module exposes no graph-dependent helper for:

```text
f(U)
e_q(U)
b_q(U)
d_q(U)
```

and no public or private definition implementing:

```text
AtomicFamily
Witness
ExactValue
ExactBranchMin
SolveBranchStandard
SolveBranchAccelerated
StrongCompactMSPD
```

The absence list is a scope guard, not a complete forecast of every future symbol.

### Exactness and deterministic source discipline

Static source checks must find no:

- import of or from `fractions`;
- reference or call to `Fraction`;
- float literal;
- call to `float`;
- true-division operator;
- tolerance-based comparison such as `isclose`;
- algorithmic ordering derived from iteration over a Python `set`.

Set construction and membership checks are not needed by this minimal module, but the
cross-cutting rule remains that no output order or control-flow order may be derived from
set iteration.

### Large-universe fixture

Let

```text
n = 4096
M = (1 << 4096) - 1
U = (1 << 0) | (1 << 2048) | (1 << 4095)
vertices = [0, 2048, 4095]
C = M ^ U
```

Then the exact properties are:

```text
full_mask(4096) = M
M.bit_length() = 4096
U.bit_count() = 3
U.bit_length() = 4096
shore_to_list(4096, U) = [0, 2048, 4095]
shore_from_list(4096, [0, 2048, 4095]) = U
shore_complement(4096, U) = C
C.bit_count() = 4093
C.bit_length() = 4095
U & C = 0
U | C = M
shore_complement(4096, C) = U
```

The full-shore encoding is specified compactly as

```text
shore_to_list(4096, M) = list(range(4096))
```

and has length `4096`.

The complement encoding is

```text
[v for v in range(4096) if v not in (0, 2048, 4095)]
```

and has length `4093`.

### Structural complexity interpretation

For this fixture:

- `full_mask` constructs one integer mask from `n`;
- `validate_shore` validates one integer mask;
- `shore_complement` performs universe-relative integer complement;
- `shore_from_list` visits the three supplied member indices;
- `shore_to_list` may test the 4096 vertex positions.

No operation enumerates the

\[
2^{4096}
\]

possible shore values or loops once per numeric mask value.

The finite fixture is a regression against magnitude-domain enumeration. It is not a
wall-clock benchmark and does not by itself prove an asymptotic complexity theorem.

### Oracle status

**Hand-derived and ruled before any production shore test or implementation.**

The large mask, member list, bit lengths, complement cardinality, public surface, and
isolation expectations follow from the committed authority rather than source inspection of
`exactfrac.shore`.

---

## Production shore oracle coverage matrix

| TEST_PLAN obligation | Pre-implementation oracle evidence |
|---|---|
| S1 — membership | ORACLE-019 and exhaustive ORACLE-020 representation identities |
| S2 — cardinality | ORACLE-019 and exhaustive ORACLE-020 representation identities |
| S3 — intersection parity | ORACLE-019 and exhaustive ORACLE-020 representation identities |
| S4 — relative complement | ORACLE-019 and ORACLE-020 |
| S5 — out-of-range bits | ORACLE-021 |
| S6 — serialization round trip | ORACLE-019 and ORACLE-020 |
| S7 — public surface and plain error boundary | ORACLE-021 and ORACLE-022 |
| S8 — exact universe, empty shore, and full shore | ORACLE-019, ORACLE-020, and ORACLE-021 |
| S9 — strict canonical list decoding and detached encoding | ORACLE-019, ORACLE-020, and ORACLE-021 |
| S10 — exhaustive finite-universe identities | ORACLE-020 |
| S11 — module isolation and responsibility boundary | ORACLE-022 |
| S12 — exactness, deterministic source discipline, and large universe | ORACLE-022 |
| R3 — no `Fraction` in solver path | ORACLE-022 exactness boundary |
| R4 — no floating point in correctness path | ORACLE-022 exactness boundary |
| D1 — no algorithmic iteration over Python `set` | ORACLE-022 deterministic-source boundary |

The S1--S3 rows record executable representation identities for already validated masks;
they do not claim that `exactfrac.shore` exposes membership, cardinality, or parity wrappers.

These fixtures establish only finite-universe shore representation and strict list
serialization. They do not implement or discharge graph-dependent shore sums, atomic
families, witnesses, certificates, rational-pair helpers, argmin policy, cut reductions,
branch algorithms, or global optimization.

---

## Atomic-family oracle unit — source and scope

The following fixtures govern the production atomic-family unit before
`tests/test_families.py` or `exactfrac/families.py` exists.

Repository authority at derivation time:

```text
4b0e13fb95b3fdff9ff50b503fce8dcbde947f9a
docs: rule production atomic-family interface
```

Canonical mathematical authority:

```text
ExactFrac_Mathematical_Specification_v2_2_CANONICAL_2026-09-02.zip
SHA-256: 400c4e23a7683571f7181b98bc009954d431f4ac355a247fb22327a609b4f9ce

Theorem_B_Strongly_Polynomial_Proof_ExactFrac_Spec_v2_2.tex
SHA-256: 4cceb9984bc6d24b78f0eeff1f9014650fc490de2210e748f0fcae85d1ffcaa6
```

The expected masks, descriptor sequences, nonemptiness values, branch-domain values, and
counts below are derived from:

- the literal atomic-family definition;
- the literal `prop:branch-transform` domains;
- `prop:domain-decomp`;
- the active compact-instance data;
- the deterministic implementation order fixed in DESIGN §4.3A.

No output from a production `exactfrac.families` implementation was used.

For compact machine-facing notation, write

```text
AF(T, pi, I, O)
```

for the descriptor with fields `(T, pi, I, O)`. Decimal integers are shore masks. Set
columns show the represented dense vertex subsets.

These fixtures establish local representation, decomposition, and finite equality facts.
They do not assert a branch optimum or a global ExactFrac optimum unless an oracle is
separately classified at that strength.

---

## ORACLE-023 — Atomic-family nonemptiness and exact descriptor semantics

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN §4.3 and §4.3A.2--§4.3A.4; TEST_PLAN F1--F6.

### Mathematical family

For an ambient finite vertex universe and a descriptor

```text
AF(T, pi, I, O)
```

the represented family is

$$
\mathcal F(T,\pi;I,O)
=
\left\{
U:
I\subseteq U,\;
U\cap O=\varnothing,\;
|U\cap T|\equiv\pi\pmod 2
\right\}.
$$

The descriptor is nonempty exactly when

$$
I\cap O=\varnothing
$$

and either

$$
T\setminus(I\cup O)\ne\varnothing
$$

or

$$
|I\cap T|\equiv\pi\pmod 2.
$$

`I & O != 0` is therefore an accepted descriptor state whose represented family is empty.
It is not malformed input.

### Direct hand cases

| Case | Descriptor | T | I | O | Free terminals | Forced parity | `is_nonempty` |
|---|---|---|---|---|---|---:|---|
| free terminal, pi=0 | `AF(5, 0, 1, 2)` | `{0, 2}` | `{0}` | `{1}` | `{2}` | 1 | `True` |
| free terminal, pi=1 | `AF(5, 1, 1, 2)` | `{0, 2}` | `{0}` | `{1}` | `{2}` | 1 | `True` |
| forced odd parity accepted | `AF(5, 1, 1, 4)` | `{0, 2}` | `{0}` | `{2}` | `∅` | 1 | `True` |
| forced odd parity rejected | `AF(5, 0, 1, 4)` | `{0, 2}` | `{0}` | `{2}` | `∅` | 1 | `False` |
| overlap, pi=0 | `AF(5, 0, 3, 2)` | `{0, 2}` | `{0, 1}` | `{1}` | `{2}` | 1 | `False` |
| overlap, pi=1 | `AF(5, 1, 3, 2)` | `{0, 2}` | `{0, 1}` | `{1}` | `{2}` | 1 | `False` |
| no terminal, pi=0 | `AF(0, 0, 2, 1)` | `∅` | `{1}` | `{0}` | `∅` | 0 | `True` |
| no terminal, pi=1 | `AF(0, 1, 2, 1)` | `∅` | `{1}` | `{0}` | `∅` | 0 | `False` |
| high terminal bit, pi=0 | `AF(1 << 100, 0, 0, 0)` | `{100}` | `∅` | `∅` | `{100}` | 0 | `True` |
| high terminal bit, pi=1 | `AF(1 << 100, 1, 0, 0)` | `{100}` | `∅` | `∅` | `{100}` | 0 | `True` |

The high-bit cases are valid direct descriptors because `AtomicFamily` stores no ambient
`n`. Direct construction therefore validates exact nonnegative mask type, not
universe-relative high bits. Universe-relative range validation belongs to
`enumerate_atomic_families(instance)`.

### Exhaustive finite family

For each

```text
n in (1, 2, 3, 4)
```

exhaust every exact mask triple

```text
0 <= T, I, O < 1 << n
```

and both

```text
pi in (0, 1).
```

For each descriptor, independently enumerate every

```text
0 <= U < 1 << n
```

and determine whether at least one `U` satisfies the three family conditions.

The number of descriptors for one `n` is

$$
2\cdot 8^n.
$$

Among descriptors with disjoint `I` and `O`, there are `6^n` triples `(T,I,O)`. There are
`5^n` such triples with no free terminal. Hence the exact nonempty count is

$$
2\cdot 6^n-5^n.
$$

The overlap-empty count is

$$
2(8^n-6^n),
$$

and the disjoint wrong-forced-parity empty count is

$$
5^n.
$$

The exact totals are:

| n | All descriptors | Nonempty | Empty | Overlap-empty | Disjoint parity-empty |
|:---:|---:|---:|---:|---:|---:|
| 1 | 16 | 7 | 9 | 4 | 5 |
| 2 | 128 | 47 | 81 | 56 | 25 |
| 3 | 1024 | 307 | 717 | 592 | 125 |
| 4 | 8192 | 1967 | 6225 | 5600 | 625 |

Across `n = 1,2,3,4`:

```text
all descriptors:                     9360
nonempty descriptors:                2328
empty descriptors:                   7032
empty because I & O != 0:            6252
disjoint/no-free wrong-parity empty:  780
```

For every one of the 9,360 descriptors, the source-definition existence result and the
closed nonemptiness predicate must agree exactly.

### Object-state expectations

`AtomicFamily` has authoritative fields exactly:

```text
T
pi
I
O
```

`is_nonempty` is derived from those fields. There is no separately mutable or authoritative:

```text
empty
infeasible
feasible
free_terminal
```

field.

### Oracle status

**Derived before any production atomic-family test or implementation.**

The exhaustive family checks the logical equivalence defining nonemptiness; it does not
claim that any branch decomposition or optimizer has been implemented.

---

## ORACLE-024 — Sparse active instance with empty transformed branch domains

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `prop:branch-transform`; `prop:domain-decomp`; DESIGN §4.3A.1 and
§4.3A.5--§4.3A.11; TEST_PLAN F3--F10.

### Instance

Reuse the valid active ORACLE-001 instance:

```text
n = 2
edges = ((0, 1, 1),)
f = (1, 1)
labels = None
```

The canonical support data are:

```text
m = 1
q = (1,)
Q = 1
d_q = (1, 1)
```

The graph-derived sets and masks are:

| Object | Vertex set | Mask |
|---|---|---:|
| `T_plus` | `{}` | 0 |
| `T_f` | `{0, 1}` | 3 |
| `P` | `{}` | 0 |
| `A` | `{}` | 0 |
| `W` | `{0, 1}` | 3 |

Indeed, `f(v)+d_q(v)=2` is even at both vertices, while both `f` values are odd.

### Exact four-branch descriptor result

The exact returned four-tuple is:

```text
D0_families = (
    AF(0, 1, 0, 0),
)

D1_families = ()

D2_families = ()

D3_families = (
    AF(3, 0, 1, 2),
    AF(3, 0, 2, 1),
)
```

All three generated descriptors are empty:

- `AF(0,1,0,0)` has no free terminal and forced parity 0 rather than 1;
- `AF(3,0,1,2)` forces one odd terminal in and the other out;
- `AF(3,0,2,1)` is symmetric.

They remain present in their ruled positions.

### Exact count

The exact descriptor count is

$$
R_{\mathrm{actual}}
=
1+2|P|m+|A|+\binom{|W|}{3}+2m
=
1+0+0+0+2
=
3.
$$

The source upper bound is

$$
R
=
1+2mn+n+\binom n3+2m
=
1+4+2+0+2
=
9.
$$

Therefore:

```text
R_actual = 3
R = 9
R_actual < R
```

This fixture prevents the source upper bound from being mistaken for an exact per-instance
return count.

### Literal `prop:branch-transform` domains

| Mask | Shore | s | e | b | d | d-s | D0 | D1 | D2 | D3 |
|---:|---|---:|---:|---:|---:|---:|:---:|:---:|:---:|:---:|
| 1 | `{0}` | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | `{1}` | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | `{0, 1}` | 2 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |

Thus:

```text
D0 domain masks = []
D1 domain masks = []
D2 domain masks = []
D3 domain masks = []
```

The union of the generated atomic families is also empty in each branch. Therefore the
literal source domain and generated family union are exactly equal for all four branches.

### Oracle status

**Derived from ORACLE-001 and the source equations before production family code existed.**

This fixture covers `P` empty, `A` empty, fewer than three vertices in `W`, naturally empty
descriptors, and strict retention of those descriptors.

---

## ORACLE-025 — Rich deterministic atomic-family enumeration

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `prop:domain-decomp`; `eq:Rcount`; `alg:global` line 1; DESIGN
§4.3A.1 and §4.3A.5--§4.3A.10; TEST_PLAN F7--F9.

### Canonical active instance

```text
n = 5

edges = (
    (0, 2, 2),
    (1, 2, 2),
    (2, 4, 1),
    (3, 4, 1),
)

f = (1, 1, 1, 1, 2)
labels = None
```

Canonical `edge_ref` order is:

```text
edge_ref 0 -> (0, 2, 2)
edge_ref 1 -> (1, 2, 2)
edge_ref 2 -> (2, 4, 1)
edge_ref 3 -> (3, 4, 1)
```

The exact derived graph values are:

```text
m = 4
q = (2, 2, 1, 1)
Q = 6
d_q = (2, 2, 5, 1, 2)
```

The active inequalities are:

```text
1 <= 2
1 <= 2
1 <= 5
1 <= 1
2 <= 2
```

### Exact derived sets and masks

| Object | Definition | Vertex set | Mask |
|---|---|---|---:|
| `T_plus` | `f[v] + d_q[v]` odd | `{0, 1}` | 3 |
| `T_f` | `f[v]` odd | `{0, 1, 2, 3}` | 15 |
| `P` | `d_q[v] > f[v]` | `{0, 1, 2}` | 7 |
| `A` | `f[v] >= 2` | `{4}` | 16 |
| `W` | `f[v] == 1` | `{0, 1, 2, 3}` | 15 |

The masks are derived from dense vertex order and the already aggregated canonical
instance.

### D0 sequence

| Index | Descriptor | I set | O set | Status |
|---|---|---|---|---|
| 0 | `AF(3, 1, 0, 0)` | `∅` | `∅` | nonempty: free terminal |

Thus:

```text
D0_families = (
    AF(3, 1, 0, 0),
)
```

### D1 sequence

The outer order is `p = 0,1,2`. The middle order is canonical `edge_ref = 0,1,2,3`.
Within each edge, the source-displayed orientation is emitted before its reverse.

| Index | Source | Descriptor | I set | O set | Status |
|---:|---|---|---|---|---|
| 0 | `p=0`, `edge_ref=0`, 0-in/2-out | `AF(3, 0, 1, 4)` | `{0}` | `{2}` | nonempty: free terminal |
| 1 | `p=0`, `edge_ref=0`, 2-in/0-out | `AF(3, 0, 5, 1)` | `{0, 2}` | `{0}` | empty: `I & O != 0` |
| 2 | `p=0`, `edge_ref=1`, 1-in/2-out | `AF(3, 0, 3, 4)` | `{0, 1}` | `{2}` | nonempty: forced parity `0` |
| 3 | `p=0`, `edge_ref=1`, 2-in/1-out | `AF(3, 0, 5, 2)` | `{0, 2}` | `{1}` | empty: forced parity `1` |
| 4 | `p=0`, `edge_ref=2`, 2-in/4-out | `AF(3, 0, 5, 16)` | `{0, 2}` | `{4}` | nonempty: free terminal |
| 5 | `p=0`, `edge_ref=2`, 4-in/2-out | `AF(3, 0, 17, 4)` | `{0, 4}` | `{2}` | nonempty: free terminal |
| 6 | `p=0`, `edge_ref=3`, 3-in/4-out | `AF(3, 0, 9, 16)` | `{0, 3}` | `{4}` | nonempty: free terminal |
| 7 | `p=0`, `edge_ref=3`, 4-in/3-out | `AF(3, 0, 17, 8)` | `{0, 4}` | `{3}` | nonempty: free terminal |
| 8 | `p=1`, `edge_ref=0`, 0-in/2-out | `AF(3, 0, 3, 4)` | `{0, 1}` | `{2}` | nonempty: forced parity `0`; duplicate retained (same as index 2) |
| 9 | `p=1`, `edge_ref=0`, 2-in/0-out | `AF(3, 0, 6, 1)` | `{1, 2}` | `{0}` | empty: forced parity `1` |
| 10 | `p=1`, `edge_ref=1`, 1-in/2-out | `AF(3, 0, 2, 4)` | `{1}` | `{2}` | nonempty: free terminal |
| 11 | `p=1`, `edge_ref=1`, 2-in/1-out | `AF(3, 0, 6, 2)` | `{1, 2}` | `{1}` | empty: `I & O != 0` |
| 12 | `p=1`, `edge_ref=2`, 2-in/4-out | `AF(3, 0, 6, 16)` | `{1, 2}` | `{4}` | nonempty: free terminal |
| 13 | `p=1`, `edge_ref=2`, 4-in/2-out | `AF(3, 0, 18, 4)` | `{1, 4}` | `{2}` | nonempty: free terminal |
| 14 | `p=1`, `edge_ref=3`, 3-in/4-out | `AF(3, 0, 10, 16)` | `{1, 3}` | `{4}` | nonempty: free terminal |
| 15 | `p=1`, `edge_ref=3`, 4-in/3-out | `AF(3, 0, 18, 8)` | `{1, 4}` | `{3}` | nonempty: free terminal |
| 16 | `p=2`, `edge_ref=0`, 0-in/2-out | `AF(3, 0, 5, 4)` | `{0, 2}` | `{2}` | empty: `I & O != 0` |
| 17 | `p=2`, `edge_ref=0`, 2-in/0-out | `AF(3, 0, 4, 1)` | `{2}` | `{0}` | nonempty: free terminal |
| 18 | `p=2`, `edge_ref=1`, 1-in/2-out | `AF(3, 0, 6, 4)` | `{1, 2}` | `{2}` | empty: `I & O != 0` |
| 19 | `p=2`, `edge_ref=1`, 2-in/1-out | `AF(3, 0, 4, 2)` | `{2}` | `{1}` | nonempty: free terminal |
| 20 | `p=2`, `edge_ref=2`, 2-in/4-out | `AF(3, 0, 4, 16)` | `{2}` | `{4}` | nonempty: free terminal |
| 21 | `p=2`, `edge_ref=2`, 4-in/2-out | `AF(3, 0, 20, 4)` | `{2, 4}` | `{2}` | empty: `I & O != 0` |
| 22 | `p=2`, `edge_ref=3`, 3-in/4-out | `AF(3, 0, 12, 16)` | `{2, 3}` | `{4}` | nonempty: free terminal |
| 23 | `p=2`, `edge_ref=3`, 4-in/3-out | `AF(3, 0, 20, 8)` | `{2, 4}` | `{3}` | nonempty: free terminal |

The exact D1 empty indices are:

```text
1, 3, 9, 11, 16, 18, 21
```

Their causes are:

```text
I & O overlap:       1, 11, 16, 18, 21
forced parity empty: 3, 9
```

The exact duplicate is:

```text
D1[2] == D1[8] == AF(3, 0, 3, 4)
```

Both occurrences remain in the tuple.

### D2 sequence

The `A` singleton block precedes the lexicographic `W` triple block.

| Index | Source | Descriptor | I set | O set | Status |
|---:|---|---|---|---|---|
| 0 | `A singleton a=4` | `AF(15, 1, 16, 0)` | `{4}` | `∅` | nonempty: free terminal |
| 1 | `W triple (0, 1, 2)` | `AF(15, 1, 7, 0)` | `{0, 1, 2}` | `∅` | nonempty: free terminal |
| 2 | `W triple (0, 1, 3)` | `AF(15, 1, 11, 0)` | `{0, 1, 3}` | `∅` | nonempty: free terminal |
| 3 | `W triple (0, 2, 3)` | `AF(15, 1, 13, 0)` | `{0, 2, 3}` | `∅` | nonempty: free terminal |
| 4 | `W triple (1, 2, 3)` | `AF(15, 1, 14, 0)` | `{1, 2, 3}` | `∅` | nonempty: free terminal |

Thus:

```text
D2_families = (
    AF(15, 1, 16, 0),
    AF(15, 1, 7, 0),
    AF(15, 1, 11, 0),
    AF(15, 1, 13, 0),
    AF(15, 1, 14, 0),
)
```

### D3 sequence

Canonical `edge_ref` order and displayed orientation order are retained.

| Index | Source | Descriptor | I set | O set | Status |
|---:|---|---|---|---|---|
| 0 | `edge_ref=0`, 0-in/2-out | `AF(15, 0, 1, 4)` | `{0}` | `{2}` | nonempty: free terminal |
| 1 | `edge_ref=0`, 2-in/0-out | `AF(15, 0, 4, 1)` | `{2}` | `{0}` | nonempty: free terminal |
| 2 | `edge_ref=1`, 1-in/2-out | `AF(15, 0, 2, 4)` | `{1}` | `{2}` | nonempty: free terminal |
| 3 | `edge_ref=1`, 2-in/1-out | `AF(15, 0, 4, 2)` | `{2}` | `{1}` | nonempty: free terminal |
| 4 | `edge_ref=2`, 2-in/4-out | `AF(15, 0, 4, 16)` | `{2}` | `{4}` | nonempty: free terminal |
| 5 | `edge_ref=2`, 4-in/2-out | `AF(15, 0, 16, 4)` | `{4}` | `{2}` | nonempty: free terminal |
| 6 | `edge_ref=3`, 3-in/4-out | `AF(15, 0, 8, 16)` | `{3}` | `{4}` | nonempty: free terminal |
| 7 | `edge_ref=3`, 4-in/3-out | `AF(15, 0, 16, 8)` | `{4}` | `{3}` | nonempty: free terminal |

Thus:

```text
D3_families = (
    AF(15, 0, 1, 4),
    AF(15, 0, 4, 1),
    AF(15, 0, 2, 4),
    AF(15, 0, 4, 2),
    AF(15, 0, 4, 16),
    AF(15, 0, 16, 4),
    AF(15, 0, 8, 16),
    AF(15, 0, 16, 8),
)
```

### Exact tuple sizes and count

```text
len(D0_families) = 1
len(D1_families) = 24
len(D2_families) = 5
len(D3_families) = 8
```

Hence:

$$
R_{\mathrm{actual}}
=
1+24+5+8
=
38.
$$

The formula gives:

$$
1+2|P|m+|A|+\binom{|W|}{3}+2m
=
1+2(3)(4)+1+4+8
=
38.
$$

The source upper bound is:

$$
R
=
1+2mn+n+\binom n3+2m
=
1+40+5+10+8
=
64.
$$

Therefore:

```text
R_actual = 38
R = 64
R_actual < R
```

### Retention requirements

The exact sequence retains:

- all seven empty D1 descriptors;
- both copies of the duplicate descriptor;
- all overlapping mathematical family coverage;
- the displayed branch, vertex, edge, orientation, singleton, and triple order.

No descriptor is deleted because it is empty, repeated, or overlaps another family.

### Oracle status

**Hand-derived from the canonical instance and deterministic ruling before family tests or
implementation.**

---

## ORACLE-026 — Literal branch-domain equality for the rich fixture

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `prop:branch-transform`; `prop:domain-decomp`; TEST_PLAN F4 and F10.

### Independent quantities

For every nonempty shore `U`, compute directly:

$$
s=f(U),\qquad
e=e_q(U),\qquad
b=b_q(U),\qquad
d=2e+b.
$$

Then apply only the literal source conditions:

```text
D0: s+b is odd
D1: s+b is even, b >= 1, d-s > 0
D2: s is odd, s >= 3
D3: s is even, b >= 1
```

The comparator does not use `T_plus`, `T_f`, `P`, `A`, `W`, or a family union to decide
source-domain membership.

### Complete nonempty-shore table

| Mask | Shore | `s` | `e` | `b` | `d=2e+b` | `d-s` | D0 | D1 | D2 | D3 |
|---:|---|---:|---:|---:|---:|---:|:---:|:---:|:---:|:---:|
| 1 | `{0}` | 1 | 0 | 2 | 2 | 1 | 1 | 0 | 0 | 0 |
| 2 | `{1}` | 1 | 0 | 2 | 2 | 1 | 1 | 0 | 0 | 0 |
| 3 | `{0, 1}` | 2 | 0 | 4 | 4 | 2 | 0 | 1 | 0 | 1 |
| 4 | `{2}` | 1 | 0 | 5 | 5 | 4 | 0 | 1 | 0 | 0 |
| 5 | `{0, 2}` | 2 | 2 | 3 | 7 | 5 | 1 | 0 | 0 | 1 |
| 6 | `{1, 2}` | 2 | 2 | 3 | 7 | 5 | 1 | 0 | 0 | 1 |
| 7 | `{0, 1, 2}` | 3 | 4 | 1 | 9 | 6 | 0 | 1 | 1 | 0 |
| 8 | `{3}` | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 9 | `{0, 3}` | 2 | 0 | 3 | 3 | 1 | 1 | 0 | 0 | 1 |
| 10 | `{1, 3}` | 2 | 0 | 3 | 3 | 1 | 1 | 0 | 0 | 1 |
| 11 | `{0, 1, 3}` | 3 | 0 | 5 | 5 | 2 | 0 | 1 | 1 | 0 |
| 12 | `{2, 3}` | 2 | 0 | 6 | 6 | 4 | 0 | 1 | 0 | 1 |
| 13 | `{0, 2, 3}` | 3 | 2 | 4 | 8 | 5 | 1 | 0 | 1 | 0 |
| 14 | `{1, 2, 3}` | 3 | 2 | 4 | 8 | 5 | 1 | 0 | 1 | 0 |
| 15 | `{0, 1, 2, 3}` | 4 | 4 | 2 | 10 | 6 | 0 | 1 | 0 | 1 |
| 16 | `{4}` | 2 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 1 |
| 17 | `{0, 4}` | 3 | 0 | 4 | 4 | 1 | 1 | 0 | 1 | 0 |
| 18 | `{1, 4}` | 3 | 0 | 4 | 4 | 1 | 1 | 0 | 1 | 0 |
| 19 | `{0, 1, 4}` | 4 | 0 | 6 | 6 | 2 | 0 | 1 | 0 | 1 |
| 20 | `{2, 4}` | 3 | 1 | 5 | 7 | 4 | 0 | 1 | 1 | 0 |
| 21 | `{0, 2, 4}` | 4 | 3 | 3 | 9 | 5 | 1 | 0 | 0 | 1 |
| 22 | `{1, 2, 4}` | 4 | 3 | 3 | 9 | 5 | 1 | 0 | 0 | 1 |
| 23 | `{0, 1, 2, 4}` | 5 | 5 | 1 | 11 | 6 | 0 | 1 | 1 | 0 |
| 24 | `{3, 4}` | 3 | 1 | 1 | 3 | 0 | 0 | 0 | 1 | 0 |
| 25 | `{0, 3, 4}` | 4 | 1 | 3 | 5 | 1 | 1 | 0 | 0 | 1 |
| 26 | `{1, 3, 4}` | 4 | 1 | 3 | 5 | 1 | 1 | 0 | 0 | 1 |
| 27 | `{0, 1, 3, 4}` | 5 | 1 | 5 | 7 | 2 | 0 | 1 | 1 | 0 |
| 28 | `{2, 3, 4}` | 4 | 2 | 4 | 8 | 4 | 0 | 1 | 0 | 1 |
| 29 | `{0, 2, 3, 4}` | 5 | 4 | 2 | 10 | 5 | 1 | 0 | 1 | 0 |
| 30 | `{1, 2, 3, 4}` | 5 | 4 | 2 | 10 | 5 | 1 | 0 | 1 | 0 |
| 31 | `{0, 1, 2, 3, 4}` | 6 | 6 | 0 | 12 | 6 | 0 | 0 | 0 | 0 |

### Exact literal domain sets

```text
D0 = [1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, 30]

D1 = [3, 4, 7, 11, 12, 15, 19, 20, 23, 27, 28]

D2 = [7, 11, 13, 14, 17, 18, 20, 23, 24, 27, 29, 30]

D3 = [3, 5, 6, 9, 10, 12, 15, 16, 19, 21, 22, 25, 26, 28]
```

Their exact sizes are:

```text
|D0| = 16
|D1| = 11
|D2| = 12
|D3| = 14
```

### Generated-family union sets

Evaluating the descriptors fixed in ORACLE-025 gives:

```text
union(D0_families) = [1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, 30]

union(D1_families) = [3, 4, 7, 11, 12, 15, 19, 20, 23, 27, 28]

union(D2_families) = [7, 11, 13, 14, 17, 18, 20, 23, 24, 27, 29, 30]

union(D3_families) = [3, 5, 6, 9, 10, 12, 15, 16, 19, 21, 22, 25, 26, 28]
```

Therefore, branch by branch:

$$
D_j
=
\bigcup_{F\in\mathscr F_j}F
\qquad
(j=0,1,2,3).
$$

For this fixture, the empty-shore mask `0` satisfies no descriptor in any generated branch
tuple, so the family-union side excludes `0` through the descriptors themselves rather than
through an external nonempty-shore prefilter.

### Cover multiplicities

The number after each mask is the number of distinct tuple positions whose descriptor
contains that shore.

```text
D0:
1:1, 2:1, 5:1, 6:1, 9:1, 10:1, 13:1, 14:1,
17:1, 18:1, 21:1, 22:1, 25:1, 26:1, 29:1, 30:1

D1:
3:4, 4:3, 7:3, 11:6, 12:4, 15:6,
19:8, 20:3, 23:3, 27:6, 28:2

D2:
7:1, 11:1, 13:1, 14:1, 17:1, 18:1,
20:1, 23:2, 24:1, 27:2, 29:2, 30:2

D3:
3:2, 5:2, 6:2, 9:2, 10:2, 12:4, 15:2,
16:2, 19:4, 21:2, 22:2, 25:2, 26:2, 28:2
```

Thus equality of the union with the source domain does not imply a partition. D1, D2, and
D3 have substantial overlap.

### Automatic-side-condition evidence

On this complete finite fixture:

```text
minimum s+b on D0 = 3
minimum s+b on D1 = 4
minimum s on D2   = 3
```

Therefore the literal equality also exercises the proof’s automatic endpoint and
lower-bound claims. This finite table is executable oracle evidence; the universal claim
remains supplied by the mathematical proof.

### Oracle status

**Derived by complete nonempty-shore enumeration from `prop:branch-transform` before family
implementation.**

No branch-domain condition was reconstructed from the family decomposition.

---

## ORACLE-027 — Classification-controlled magnitude and label invariance

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN §4.3A.1, §4.3A.5--§4.3A.12; TEST_PLAN F7--F11.

### Instance family

For an exact positive even integer `L`, define:

```text
n = 3

edges = (
    (0, 1, L),
    (0, 2, L),
    (1, 2, L),
)

f = (1, L, L)
```

Use the two values:

```text
L_small = 2
L_large = 1 << 4096
```

and test each with labels absent and with:

```text
labels = ("v0", "v1", "v2")
```

For either `L`:

```text
m = 3
Q = 3L
d_q = (2L, 2L, 2L)
```

Since `L` is even:

| Object | Vertex set | Mask |
|---|---|---:|
| `T_plus` | `{0}` | 1 |
| `T_f` | `{0}` | 1 |
| `P` | `{0, 1, 2}` | 7 |
| `A` | `{1, 2}` | 6 |
| `W` | `{0}` | 1 |

### Exact descriptor result

All four instance variants produce the same descriptor tuples.

```text
D0_families = (
    AF(1, 1, 0, 0),
)
```

D1 is the exact nested-order sequence:

```text
for p in (0, 1, 2):
    for (u, v) in ((0, 1), (0, 2), (1, 2)):
        emit AF(1, 0, (1 << p) | (1 << u), 1 << v)
        emit AF(1, 0, (1 << p) | (1 << v), 1 << u)
```

D2 is:

```text
D2_families = (
    AF(1, 1, 2, 0),
    AF(1, 1, 4, 0),
)
```

D3 is:

```text
D3_families = (
    AF(1, 0, 1, 2),
    AF(1, 0, 2, 1),
    AF(1, 0, 1, 4),
    AF(1, 0, 4, 1),
    AF(1, 0, 2, 4),
    AF(1, 0, 4, 2),
)
```

The exact tuple lengths are:

```text
1, 18, 2, 6
```

and:

$$
R_{\mathrm{actual}}
=
1+18+2+6
=
27.
$$

The source upper bound is:

$$
R=1+18+3+1+6=29.
$$

### Magnitude and labels

```text
L_large.bit_length() = 4097
```

Despite the large exact multiplicities and capacities:

- the derived classification masks are unchanged;
- the exact descriptor values, order, and count are unchanged;
- labels do not affect any result;
- no loop count depends on `L`;
- no multiplicity is expanded into copies.

This is a support-and-classification-controlled regression. It does not claim that
arbitrary magnitude changes preserve the five derived masks.

### Oracle status

**Derived from parity and comparison of the displayed formulas before implementation.**

---

## ORACLE-028 — Atomic-family exact rejection matrix

**Classification:** `NEGATIVE`

**Source obligations:** DESIGN §4.3A.2--§4.3A.4; TEST_PLAN F5--F6.

### Exact exception class

Every malformed public input in this oracle raises:

```text
ValueError
```

with:

```python
type(exc) is ValueError
```

The following do not discharge the oracle:

```text
TypeError
InvalidInstance
UnsupportedInstance
any ValueError subclass
```

Exception prose is diagnostic and is not compared.

### Adversarial helper types

Tests may define:

```python
class IntSubclass(int):
    pass


class InstanceSubclass(Instance):
    pass


class CoercibleInteger:
    def __int__(self) -> int:
        return 1

    def __index__(self) -> int:
        return 1
```

No value is accepted through implicit coercion.

### Invalid mask fields

For each field in:

```text
T
I
O
```

the following values are invalid:

```text
-1
True
False
1.0
Fraction(1, 1)
IntSubclass(1)
"1"
None
CoercibleInteger()
```

The other descriptor fields are held at valid controls while one target field is varied.

### Invalid parity field

The following `pi` values are invalid:

```text
-1
2
True
False
0.0
1.0
Fraction(0, 1)
Fraction(1, 1)
IntSubclass(0)
IntSubclass(1)
"0"
None
CoercibleInteger()
```

Valid controls are exact built-in integers:

```text
0
1
```

### Valid overlap and high-bit controls

The following are valid direct descriptor constructions:

```text
AF(1, 0, 1, 1)
AF(1 << 100, 0, 0, 0)
AF(0, 0, 1 << 100, 0)
AF(0, 0, 0, 1 << 100)
```

The first has `I & O != 0` and constructs successfully with `is_nonempty == False`.

The high-bit cases construct successfully because a direct descriptor stores no universe
size. They do not authorize `enumerate_atomic_families(instance)` to generate
out-of-range masks.

### Invalid enumerator arguments

`enumerate_atomic_families(value)` raises exact built-in `ValueError` for:

```text
None
object()
{}
a valid serialized instance dict
a valid InstanceSubclass object
a verifier-side BruteInstance object
```

The enumerator requires an exact production `Instance`; it does not deserialize, coerce,
or accept subclasses.

### Oracle status

**Ruled before production family tests or implementation.**

---

## ORACLE-029 — Atomic-family module surface, isolation, and complexity boundary

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN §4.3A.2, §4.3A.12--§4.3A.13; TEST_PLAN F5 and F12; R3, R4,
and D1.

### Public surface

The module-level export sequence is exactly the Ruff-sorted tuple:

```python
(
    "AtomicFamily",
    "enumerate_atomic_families",
)
```

The package root does not re-export either name.

`AtomicFamily` is:

- frozen;
- slotted;
- immutable;
- hashable;
- defined by fields exactly `T`, `pi`, `I`, `O`.

The module exposes no public family-membership wrapper and no downstream solver API.

### Import boundary

Production family source may import only standard-library modules plus:

```text
exactfrac.instance
exactfrac.shore
```

A fresh-process import of `exactfrac.families` must not import:

```text
exactfrac_verify
exactfrac_verify.*
```

The module consumes `Instance`; the verifier never consumes production family code.

### Exactness and deterministic source discipline

Static checks must find no:

- import of or from `fractions`;
- reference or call to `Fraction`;
- float literal;
- call to `float`;
- true-division operator;
- tolerance comparison such as `isclose`;
- output or control-flow order derived from iteration over a Python `set`;
- loop over a multiplicity or capacity value;
- expansion of compact multiplicities into explicit copy objects.

The source may use deterministic:

- dense `range(instance.n)` order;
- canonical `instance.edges` order;
- lexicographic `itertools.combinations` order;
- list accumulation followed by tuple conversion.

### Responsibility boundary

The module defines no implementation of:

```text
f(U)
e_q(U)
b_q(U)
d_q(U)
sign routing
parity-cut reduction
ExactBranchMin
SolveBranchStandard
SolveBranchAccelerated
Witness
ExactValue
certificate verification
StrongCompactMSPD
```

It prepares family descriptors only.

### Structural operation carrier

For one valid canonical instance, the expected structural carrier is:

```text
O(n)     derived-mask work
O(m)     canonical support traversal overhead
O(R_actual) descriptor construction
```

for total:

```text
O(n + m + R_actual)
```

where:

$$
R_{\mathrm{actual}}
=
1+2|P|m+|A|+\binom{|W|}{3}+2m.
$$

ORACLE-027 fixes a case in which the numerical bit lengths grow to 4097 while the
descriptor count remains 27.

### Oracle status

**Architecture and source-boundary fixture established before implementation.**

---

## Production atomic-family oracle coverage matrix

| TEST_PLAN obligation | Pre-implementation oracle evidence |
|---|---|
| F1 — overlap means empty | ORACLE-023 and ORACLE-028 |
| F2 — free terminal | ORACLE-023 exhaustive nonemptiness family |
| F3 — forced parity | ORACLE-023 exhaustive nonemptiness family |
| F4 — cover, not partition | ORACLE-024 and ORACLE-026 |
| F5 — public surface and immutable descriptor | ORACLE-023, ORACLE-028, ORACLE-029 |
| F6 — exact descriptor domain and one nonemptiness predicate | ORACLE-023 and ORACLE-028 |
| F7 — graph-derived masks | ORACLE-024, ORACLE-025, ORACLE-027 |
| F8 — four-branch shape and order | ORACLE-024, ORACLE-025, ORACLE-027 |
| F9 — count, empty retention, no deduplication | ORACLE-024, ORACLE-025, ORACLE-027 |
| F10 — independent literal branch-domain equality | ORACLE-024 and ORACLE-026 |
| F11 — deterministic repetition and magnitude independence | ORACLE-027 |
| F12 — isolation, exactness, source discipline | ORACLE-029 |
| `prop:domain-decomp` | ORACLE-024 sparse equality and ORACLE-026 complete rich equality |
| R3 — no `Fraction` in solver path | ORACLE-029 |
| R4 — no floating point in correctness path | ORACLE-029 |
| D1 — no algorithmic iteration over Python `set` | ORACLE-029 |

These fixtures do not implement sign routing, parity-cut reduction, `ExactBranchMin`,
branch iteration, witnesses, certificates, or global optimization.


---

## Unit 08 oracle authority and chronology

ORACLE-030 through ORACLE-037 are prospective fixtures for the production Witness and
ExactValue unit. They are governed by DESIGN section 4.4A and TEST_PLAN W8--W20 at commit
`4ad6eaa14d1ae1dd2881416769fa5e88d984a8f6`, together with the canonical V2.2 definitions
`def:instance`, `eq:degree-identity`, `def:parameter`, `eq:compact-density`, and the exact
output contract. This addition changes no pre-existing catalogue byte or classification.

All numerical expectations below follow from the written input data and displayed
mathematical formulas. A separate AI-authored, definition-level handoff audit recomputes
the arithmetic and the finite corpus without importing any production module. That audit
is supporting executable evidence, not a human external review or the future witness
implementation. The production module `exactfrac/witness.py` and its consuming test module
`tests/test_witness.py` remain absent at oracle adoption.

Unless otherwise stated, numerical fixture tables use `(s,e,b,d)` to mean
`(f(U),e_q(U),b_q(U),d_q(U))`, and the dense vector has one entry for each canonical support
edge, including zero entries off the boundary. A listed raw pair is unreduced.

No new fixture below asserts a global optimum. ORACLE-001 and ORACLE-004 retain their
existing global claims; ORACLE-002 remains local and its competitor is not newly promoted
to a global optimum. No new theorem or production comparison interface is introduced.

---

## ORACLE-030 — Raw records, structural equality, and constructor-only controls

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN 4.4A.2--4.4A.5 and 4.4A.12--4.4A.13; TEST_PLAN W8--W10.
These are representation rulings, not claims that arbitrary records are attained values.

### Exact records and literal preservation

`ExactValue` has dataclass fields/slots exactly `N`, `D`, in that order. Both fields have
exact built-in type int; `D > 0`. The following are accepted constructor records, stored
literally: `(2,2)`, `(1,1)`, `(0,2)`, `(0,1)`, `(-2,2)`, `(-1,1)`, `(12,8)`, `(3,2)`,
`(3,10)`, and `(2,3)`. The signed numerator records do not claim an attaining witness.

| Left raw pair | Right raw pair | Structural equality | Numerical equality, test side only |
|---|---|---|---|
| `(2,2)` | `(1,1)` | false | true: `2*1 == 1*2` |
| `(0,2)` | `(0,1)` | false | true: `0*1 == 0*2` |
| `(-2,2)` | `(-1,1)` | false | true: `-2*1 == -1*2` |
| `(12,8)` | `(3,2)` | false | true: `12*2 == 3*8` |
| `(2,2)` | `(2,2)` | true | true |
| `(3,10)` | `(2,3)` | false | false: `3*3 != 2*10` |

The last row also exposes lexicographic ordering as wrong for rational comparison:
`3 > 2`, but `3*3 < 2*10`. No production ordering/comparison operation is added in Unit 08.
Tests may use exact test-side Fraction or cross-products to establish these numerical
facts; they must not infer a missing production comparator from them.

Independently constructed equal raw records must compare equal and hash equally. Unequal
records remain distinct dictionary/set keys even if hashes collide. Do not require unequal
hash integers, store literal hash values, or claim cross-process hash stability. Testing
record hashability may use a test-side set; this is not permission for production
algorithmic set iteration.

`Witness` has fields/slots exactly `U`, `y`, in that order, with exact positive int U and
an exact tuple of nonnegative exact ints. Accepted constructor-only controls are
`Witness(1, ())`, `Witness(1 << 100, ())`, and `Witness(3, (0,2,0,1,1,0))`.
The first two demonstrate absence of an instance from the constructor, not validity for
any chosen instance. Repeated construction with identical fields gives equal records and
equal hashes. Distinct U or y values produce structurally unequal records.

Both classes are frozen and slotted with no instance __dict__, attached Instance, n, m,
value/cache, or empty flag. No generated ordering exists. Mutating a field or adding an
attribute must fail without changing state; the error type follows dataclass/Python
behavior, not the malformed-data ValueError contract. Positional calls and the exact
ruled keywords (`N`, `D`, `U`, `y`) have the same meaning. No new constructor or method is
implied by this fixture. Adversarial constructor inputs are fixed in ORACLE-034.

---

## ORACLE-031 — Mixed graph-shore sums for every mask of a four-vertex universe

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `def:instance`, `eq:degree-identity`; DESIGN 4.4A.6--4.4A.7;
TEST_PLAN W11 and W19.

### Canonical active instance MIXED

```text
n = 4
edges = ((0,1,2), (0,2,3), (0,3,1), (1,2,4), (1,3,2), (2,3,5))
f = (2,3,4,5)
q = (2,3,1,4,2,5)
Q = 17
d_q = (6,8,12,8)
```

The degree sums are `2+3+1=6`, `2+4+2=8`, `3+4+5=12`, `1+2+5=8`.
Thus the active inequalities are `2<=6`, `3<=8`, `4<=12`, `5<=8`.
Canonical edge_ref values are 0 through 5 in the displayed order.

For each mask, sum f over its member vertices, sum multiplicity separately over internal
and crossing support edges, and independently sum vertex degrees over its member vertices.
Each table row is the direct evaluation of those definitions, not a production output.

| U mask | s | e | b | d |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 2 | 0 | 6 | 6 |
| 2 | 3 | 0 | 8 | 8 |
| 3 | 5 | 2 | 10 | 14 |
| 4 | 4 | 0 | 12 | 12 |
| 5 | 6 | 3 | 12 | 18 |
| 6 | 7 | 4 | 12 | 20 |
| 7 | 9 | 9 | 8 | 26 |
| 8 | 5 | 0 | 8 | 8 |
| 9 | 7 | 1 | 12 | 14 |
| 10 | 8 | 2 | 12 | 16 |
| 11 | 10 | 5 | 12 | 22 |
| 12 | 9 | 5 | 10 | 20 |
| 13 | 11 | 9 | 8 | 26 |
| 14 | 12 | 11 | 6 | 28 |
| 15 | 14 | 17 | 0 | 34 |

For example, U=3 means `{0,1}`. Edge 0 is internal, edge 5 is external, and edges
1,2,3,4 cross. Therefore `s=2+3=5`, `e=2`, `b=3+1+4+2=10`, and `d=6+8=14=2*2+10`.
This single mask exercises all three support-edge roles.

For U=0 the four sums are zero. For U=15, `s=14`, `e=Q=17`, `b=0`, and `d=2Q=34`.
Every row must satisfy `d=2e+b`. Generic sum helpers accept all sixteen masks, without a
witness-admissibility filter. They return exact ints. Applying any valid distinct labels
must not change these values; label-specific controls appear in ORACLE-035.

---

## ORACLE-032 — Strict literal dense/sparse conversion and detached representations

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN 4.4.3 and 4.4A.6--4.4A.8; TEST_PLAN W12--W13 and the
representation portions of historical W1--W6.

Use MIXED from ORACLE-031, with U=3 unless a different mask is shown.
The allowable nonzero dense positions are exactly 1,2,3,4.

| U | Exact dense tuple | Exact canonical sparse list |
|---|---|---|
| 3 | `(0,2,0,1,1,0)` | `[[1,2],[3,1],[4,1]]` |
| 3 | `(0,2,0,0,0,0)` | `[[1,2]]` |
| 3 | `(0,3,1,4,2,0)` | `[[1,3],[2,1],[3,4],[4,2]]` |
| 3 | `(0,0,0,0,0,0)` | `[]` |
| 0 | `(0,0,0,0,0,0)` | `[]` |
| 15 | `(0,0,0,0,0,0)` | `[]` |

Each coordinate is an individually selectable number of copies; for example, count 2 at
edge_ref 1 is legal although q[1]=3. Requiring zero-or-all q would reject a legal partial
selection. Sparse decoding inserts zero at every missing ref and returns an exact tuple
of length six. Exports are exact lists of fresh exact two-element lists, in increasing
edge_ref order. Check every direction against the literal table, not just against another
converter. Then check both round trips without changing their prescribed normal form.

For U=0 or U=15 the boundary is empty; only the all-zero selection is legal. Nonempty
sparse input or any positive dense count is rejected there. `[]` on U=3 denotes no selected
boundary copies, not absence of a shore or an Empty result.

### Conversion is not full admissibility

Still at MIXED U=3, the dense vector `(0,1,0,0,0,0)` and sparse `[[1,1]]` convert
successfully. Its total is `s+Y=5+1=6`, which is even although it is at least three.
Both `validate_witness` and `witness_value` reject that witness. Conversion must not use
the validator's parity/lower-bound guard as a hidden prefilter.

MIXED U=15 with all-zero y also converts successfully but has even total 14. The two
converter docstrings must accurately state that conversion checks representation only.

### Detachment and failure nonmutation

Starting from dense `(0,2,0,1,1,0)`, produce two exports and require that each is literally
`[[1,2],[3,1],[4,1]]`, with distinct outer objects and corresponding nested list objects.
Change the first export's first count to 99 and remove its last entry. The dense tuple,
any existing Witness containing it, the second export, and a subsequent export remain
unchanged. Decode a fresh canonical sparse list, then mutate that source list: the decoded
tuple remains the original six counts. The mutation value 99 is only a detachment probe,
not an accepted input to a conversion. Failed conversions leave the instance and supplied
containers byte/value-equivalent to their pre-call state. Rejection fixtures are ORACLE-034.

---

## ORACLE-033 — Admissibility, unreduced attainment, and zero versus Empty

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `def:parameter`, `eq:compact-density`; DESIGN 4.4A.9--4.4A.12;
TEST_PLAN W14--W16. Prior oracle classifications are preserved.

### Exact reuse of already catalogued witnesses

O002 means the unchanged ORACLE-002 instance: n=3, edges
`((0,1,1),(0,2,1),(1,2,1))`, f=(1,1,2).
Its constructive witness uses mask 4, not the integer index 2; its competitor uses mask 3.
O004 means the unchanged ORACLE-004 instance: n=2, edge `(0,1,2)`, f=(1,1).
Both catalogued singleton maximizers use dense y=(2,). The present unit evaluates these
fixed witnesses; it does not implement their construction or prove the optimization again.

### New local ZERO instance

```text
n = 2
edges = ((0,1,3),)
f = (3,3)
d_q = (3,3)
Q = 3
U = 1  (the subset {0})
y = (0,)
sparse_y = []
```

The active condition holds with equality at both vertices. The unique edge crosses U, but
selecting zero copies is legal. Thus `s=3`, `e=0`, `b=3`, `d=3`, `Y=0`, and total=3.
The pair is admissible, and its literal raw value is `(0,2)` from `2*(0+0)` and `3+0-1`.
This is a local zero-valued attaining witness, not a maximizing-witness claim.

The validator returns None; that is its success return value, not a missing witness.
The evaluator returns `ExactValue(0,2)`. The Witness object remains present and unchanged.
Never infer Empty from N==0, zero rational value, or sparse []. Never normalize (0,2) to (0,1).

### Exact accepted-witness table

The sums column is `(s,e,b,d)`. Every listed total is odd and at least three, every dense
coordinate is in bounds, and nonboundary coordinates are zero. Each raw value is derived
by `N=2*(e+Y)` and `D=s+Y-1`.

| ID | Instance | U | Dense y | Sparse y | Sums | Y | Total | Raw (N,D) |
|---|---|---|---|---|---|---|---|---|
| unit-witness | O002 | 4 | (0, 1, 0) | [[1, 1]] | (2, 0, 2, 2) | 1 | 3 | (2, 2) |
| unit-competitor | O002 | 3 | (0, 1, 0) | [[1, 1]] | (2, 1, 2, 4) | 1 | 3 | (4, 2) |
| tie-left | O004 | 1 | (2,) | [[0, 2]] | (1, 0, 2, 2) | 2 | 3 | (4, 2) |
| tie-right | O004 | 2 | (2,) | [[0, 2]] | (1, 0, 2, 2) | 2 | 3 | (4, 2) |
| zero-not-empty | ZERO | 1 | (0,) | [] | (3, 0, 3, 3) | 0 | 3 | (0, 2) |
| mixed-partial | MIXED | 3 | (0, 2, 0, 1, 1, 0) | [[1, 2], [3, 1], [4, 1]] | (5, 2, 10, 14) | 4 | 9 | (12, 8) |
| mixed-no-selected-copies | MIXED | 3 | (0, 0, 0, 0, 0, 0) | [] | (5, 2, 10, 14) | 0 | 5 | (4, 4) |
| mixed-all-boundary-copies | MIXED | 3 | (0, 3, 1, 4, 2, 0) | [[1, 3], [2, 1], [3, 4], [4, 2]] | (5, 2, 10, 14) | 10 | 15 | (24, 14) |

In MIXED's partial case, `Y=2+1+1=4`, so `N=2*(2+4)=12` and `D=5+4-1=8`.
Selecting none gives `(4,4)`, not `(1,1)`. Selecting all boundary copies gives Y=10 and
raw `(24,14)`. This unit accepts all three admissible selections regardless of which has
the largest ratio. The validator's success is exactly None, never True or a replacement
record; the evaluator returns only the separate ExactValue, not a new Witness/result.

O002's two rows remain local witness/competitor evaluations. O004's two distinct Witness
records have equal ExactValue records `(4,2)`; equal output records do not imply a unique
witness. No global claim is attached to the new MIXED or ZERO rows.

### Independently isolated last guards

| Guard | Fixture | U | y | Y | s+Y | Conversion | Validator/evaluator |
|---|---|---|---|---|---|---|---|
| parity only | MIXED | 3 | `(0,1,0,0,0,0)` | 1 | 6 | succeeds | exact ValueError |
| lower bound only | O004 | 1 | `(0,)` | 0 | 1 | succeeds | exact ValueError |
| whole-shore parity | MIXED | 15 | `(0,0,0,0,0,0)` | 0 | 14 | succeeds | exact ValueError |

The lower-bound seed is odd and satisfies every earlier guard. The parity-only seed
already satisfies total>=3. A failure on one cannot be credited to the other guard.

### Genuine empty-family control from ORACLE-001

O001 is the existing n=2, edge `(0,1,1)`, f=(1,1) instance. At either singleton, legal
counts 0 and 1 give totals 1 and 2. The full shore has only count 0 and total 2.
No nonempty shore admits a valid witness. U=0 and the full shore still permit generic
all-zero conversions. The future empty-result convention is `(0,1)` and no witness;
this oracle introduces no Empty checker, result class, or certificate envelope in Unit 08.
Passing None to validate_witness/witness_value is malformed input, not successful empty
certification. Witness(0,()) is rejected by the constructor.

---

## ORACLE-034 — Exact rejection matrix and validation-order controls

**Classification:** `NEGATIVE`

**Source obligations:** DESIGN 4.4A.3--4.4A.4, 4.4A.6, 4.4A.8--4.4A.10, 4.4A.13;
TEST_PLAN W9--W10, W12--W14, and W17.

Every malformed-data case below raises exact built-in ValueError through the supported
public signature. Future tests assert `type(exc.value) is ValueError`; accepting subclasses
alone is insufficient. Wrong Python call arity and frozen-record mutation are excluded
from this ValueError matrix. No exception-message wording is fixed.

### Adversarial type vocabulary

For each applicable integer position, substitute each of: True, False, 1.0,
Fraction(1,1), a direct int subclass instance with value 1, "1", None, and an object
with __int__/__index__ that would produce 1 if called. Test a poison conversion variant
whose __int__/__index__ raises AssertionError: rejection must occur without conversion.
Use a numerically in-range value in the malformed type to isolate exact-type validation.

For exact tuple positions use list, tuple subclass, range, iterator/generator, string,
and None controls. For exact list positions use tuple, list subclass, iterator/generator,
string, and None controls. Record subclasses and duck-typed objects are nonexact records,
even if their attributes appear valid. No consumption/coercion of rejected iterators is
required or permitted merely to make their shape acceptable.

### Constructor matrix

| Boundary | Invalid variation | Valid constructor-only control |
|---|---|---|
| Witness U | 0, -1, or every malformed int type | 1; 1<<100 |
| Witness y outer | every nonexact tuple container | (); (0,); (0,2,0,1,1,0) |
| Witness y coordinate | -1 or every malformed int type, in each tested coordinate | 0 and positive exact counts |
| ExactValue N | every malformed int type | negative, zero, positive exact int |
| ExactValue D | 0, -1, or every malformed int type | 1 and larger exact ints |

Constructing Witness(1,()) or Witness(1<<100,()) is allowed as shape. Validating either
against MIXED rejects it (wrong length or outside-universe shore). A constructor cannot
silently impose an unseen instance or fix its m. No InvalidInstance/UnsupportedInstance
exception is substituted for Unit 08 malformed-data ValueError.

### Instance-keyed and record boundaries

Each of the four sums, the two converters, validate_witness, and witness_value rejects a
nonexact Instance: None, a serialized dictionary, an Instance subclass, a verifier-side
instance, or a duck-typed object. This check precedes U or payload work. No normally
validated Instance is deliberately corrupted by bypassing its constructor for these tests.
The full validator/evaluator likewise rejects None, a tuple, a dictionary, a Witness
subclass, or a duck-typed witness where an exact Witness is required.

For the four sums and two converters, use MIXED and bare U values -1 and 16, plus every
malformed int type. Masks 0 and 15 are accepted. No high bits are truncated.

### Dense embedding matrix (MIXED, U=3)

| Invalid dense input | Isolated reason |
|---|---|
| exact tuples of length 5 and 7 | length must be m=6 |
| nonexact tuple container | container type |
| `(0,-1,0,0,0,0)` | negative coordinate |
| `(0,4,0,0,0,0)` | edge 1 exceeds q[1]=3 |
| `(1,0,0,1,0,0)` | internal edge 0 has positive count, within q[0] |
| `(0,1,0,0,0,1)` | external edge 5 has positive count, within q[5] |
| any coordinate replaced by malformed integer type | exact coordinate type |

For bound/boundary cases all coordinates have correct built-in types and nonnegativity.
The first overbound example has odd total 9; both nonboundary examples have odd total 7.
They cannot be explained away as parity or lower-bound failures. The converter rejects
before zero omission. The validator and evaluator reject the same graph-invalid
shape-valid Witness objects; they must not allow evaluation to bypass validation.

At U=0 and U=15, any positive coordinate (for example `(1,0,0,0,0,0)`) is a nonboundary
violation; all-zero input is valid for conversion. A full-shore Witness can be constructed,
but MIXED's full-shore admissibility fails parity as in ORACLE-033.

### Sparse decoding matrix (MIXED, U=3)

| Invalid sparse input | Isolated reason |
|---|---|
| nonexact outer list | outer type |
| `[()]`, `[(1,1)]`, record list subclass | record must be exact list |
| `[[]]`, `[[1]]`, `[[1,1,1]]` | record arity must be two |
| `[[bad,1]]` or `[[1,bad]]` for each malformed int type | exact ref/count types |
| `[[-1,1]]`, `[[6,1]]` | ref outside [0,6) |
| `[[1,1],[1,1]]` | duplicate ref; no merging |
| `[[3,1],[1,1]]` | descending refs; no sorting |
| `[[1,0]]`, `[[1,-1]]` | count must be positive; no dropping zeros |
| `[[1,4]]` | count exceeds q[1]=3 |
| `[[0,1]]`, `[[5,1]]` | internal/external ref is not crossing |

Every ref mentioned as an accepted counterpart refers to the fixed canonical instance,
not a reaggregated or reordered interpretation. On rejection the source list is unchanged.
Duplicate positive records may not be silently summed; even a resulting in-range sum would
not repair the invalid representation.

### Guard order is not inferred merely from an exception class

The single-defect cases establish each guard's rejection when its predecessors pass.
Since all ordinary data failures share ValueError, two-invalid-input examples alone do
not prove which guard ran first. Future static inspection must compare the actual order
with DESIGN 4.4A.10. Hostile rejected objects with attribute/iteration/conversion hooks
that raise AssertionError can additionally expose premature payload inspection: with a
nonexact instance the production function must reject the instance before touching the
other data; similarly it must reject a nonexact Witness before reading its fields.
Do not add message-string assertions or fabricate a bypass-construction API to infer order.

These are prospective rejection expectations; no Unit 08 production errors have been
executed or verified at catalogue adoption because the module does not yet exist.

---

## ORACLE-035 — Exact 4097-bit counts, large f, labels, and support-controlled work

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** compact-copy meaning in `def:instance`, `eq:compact-density`;
DESIGN 4.4A.7--4.4A.8, 4.4A.11, 4.4A.15; TEST_PLAN W19.

Let `k` be one of the fixed test parameters `(1,2,8,64,4096)` and set `L=1<<k`.
For every k here L is even. Use n=2 and one canonical edge `(0,1,L+1)`.
Both degrees equal L+1, Q=L+1, and the support size remains m=1.

### Small f and a partial boundary count

Choose f=(1,1), U=1, y=(L,), and sparse_y=[[0,L]]. The selected count is strictly less
than q=L+1, so it is a legal partial count. The four sums are `(1,0,L+1,L+1)`.
Total is L+1, odd and at least three. The unreduced raw output is `(2*L,L)`.
No output may become `(2,1)` by reduction.

At k=1 the literal small control is edge `(0,1,3)`, f=(1,1), y=(2,), raw `(4,2)`.
At k=4096, y[0], D, and q each have 4097 bits; N has 4098 bits.

### Large f on the same support

Instead choose f=(L+1,L+1), still active with equality at each endpoint.
At U=1 and y=(L,), the four sums are `(L+1,0,L+1,L+1)`, total=2*L+1,
and raw output `(2*L,2*L)`. Preserve both fields; do not reduce to `(1,1)`.
At the same U with y=(0,), total=L+1 and raw output `(0,L)`; the zero-valued witness
still exists, with sparse []. At k=1 this zero row is exactly the ZERO fixture of
ORACLE-033. The full-shore sums in either f regime are `(sum(f),L+1,0,2*(L+1))`.

At k=4096, the large-f accepted-count row has N and D of bit length 4098; the zero row
has N==0 and D of bit length 4097. These are algebraic consequences of L=2^k, not a
runtime asymptotic cutoff or a numeric bound imposed on production.

### Labels and scans

For every fixed instance compare labels=None, the tuple of strings `("left","right")`,
and the exact-int tuple `(10,20)`. For MIXED additionally compare labels=None,
`("a","b","c","d")`, and `(10,20,30,40)` against the complete sum table and conversion
rows. Labels do not change any output or validation decision.

The production loops must remain bounded by n, m, or encoded malformed-payload length as
ruled, never by q, f, Q, Y, N, D, or a count's bit length in place of structural scans.
The test-side parameter sweep and tiny exhaustive enumeration are not production loops.
No wall-clock flatness, exact machine-time ratio, universal strong-polynomial proof, or
invented telemetry counter is asserted. Huge counts are never expanded in this fixture.

---

## ORACLE-036 — Declared tiny admissibility corpus with independently counted decisions

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** `def:instance`, `ass:active`, `def:parameter`, `eq:compact-density`;
DESIGN 4.4A.7--4.4A.11; TEST_PLAN W20. This is a finite definition-level corpus, not a
new theorem or a global optimum claim.

### Corpus definition

For n in (2,3), list every unordered pair of dense vertices in lexicographic order.
Assign each pair a number in {0,1,2}; omit records assigned 0, retain 1 or 2 as the
positive multiplicity. Discard choices with an isolated vertex. For each remaining
canonical support/multiplicity instance enumerate every f with 1 <= f[v] <= d_q[v].
Each (n,edges,f) tuple occurs once. No labels are attached for the count calculation.

For each instance, enumerate every mask U in [0,2^n), including zero for generic sums and
conversions. Legal dense selections have zero off the boundary and coordinates in
[0,q_e] on it. The nonempty-mask subcorpus alone is the domain of Witness admissibility.

### Counts derived without production witness code

For a fixed U, let

$$
B_U(t)=\prod_{e\in\delta(U)}(1+t+\cdots+t^{q_e}),\qquad
L_U=B_U(1)=\prod_{e\in\delta(U)}(q_e+1).
$$

The empty product equals one, so empty boundaries still have one legal selection.
Let Delta_U=B_U(-1). It equals one if every crossing q_e is even and zero otherwise.
The number of selections with s+Y odd is

$$
P_U=\frac{L_U+(-1)^{s+1}\,\Delta_U}{2}.
$$

For nonempty U we have s>=1. Among the odd totals, the only one below three is total=1,
which happens exactly when s=1 and all counts are zero. Therefore

$$
A_U=P_U-\mathbf 1_{s=1},\qquad
E_U=L_U-P_U,\qquad
H_U=\mathbf 1_{s=1}.
$$

Here A_U counts admissible selections, E_U parity failures, and H_U odd lower-bound
failures after parity passes. No class overlaps these latter two rejection counts.
An admissible zero-valued selection has e=0, Y=0, and odd s>=3; there is one such zero
selection for each shore meeting those conditions.

Sum these products over the explicitly bounded supports, capacities, and shores above:

| Corpus | Instances | All shores | Nonempty shores | Generic selections including U=0 | Nonempty selections | Admissible | Parity rejected | Odd lower-bound rejected | Zero-valued admissible |
|---|---|---|---|---|---|---|---|---|---|
| n=2 | 5 | 20 | 15 | 38 | 33 | 10 | 17 | 6 | 0 |
| n=3 | 324 | 2592 | 2268 | 12888 | 12564 | 5907 | 6294 | 363 | 249 |
| total | 329 | 2612 | 2283 | 12926 | 12597 | 5917 | 6311 | 369 | 249 |

In particular `12597 = 5917 + 6311 + 369` and `12926 = 12597 + 329`.
U=0 contributes exactly one all-zero generic selection per instance and is never counted
as a candidate Witness. This corpus contains 249 zero-valued admissible witnesses; their
presence is expected from the same source definition, not inferred Empty behavior.

### Independent future comparison and current oracle audit

The handoff oracle audit recomputes these totals both by the displayed parity-product
identities and by literal subset/count enumeration. For the latter it builds each small
shore as a Python set and inspects internal and crossing edges directly. It independently
enumerates subsets of the tiny individual boundary copies and projects them to dense
counts, checking that this set equals the compact count product. Distinct expanded subsets
may project to the same count vector; they must be deduplicated only in this independent
cross-model comparison, not incorrectly counted as distinct compact witnesses.

No production module is imported or used to establish the expected answers. For later
W20 tests, compare production acceptance and rejection in both directions, literal raw
pairs on every accepted witness, direct graph sums on every mask, and both conversion
outputs on each legal embedding. The independently implemented expected side must not call
production validators, conversion functions, or shore-sum helpers. Add ORACLE-034 malformed
inputs separately, since legal-only enumeration cannot expose malformed-input acceptance.
Report these finite corpus totals separately from pytest's collected-test count. Run loops
inside a manageable set of tests with identifying failure messages; no future pytest test
count is claimed here. The corpus supplies regression evidence, not a universal proof.

---

## ORACLE-037 — Witness module surface, exactness, isolation, and deferred boundaries

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN 4.4A.1--4.4A.2 and 4.4A.13--4.4A.15; the explicit witness
addition in DESIGN 4.5.3; TEST_PLAN W8 and W18--W20.

The exact module-level export tuple is:

```text
("ExactValue", "Witness", "dense_y_to_sparse", "shore_b_q", "shore_d_q",
 "shore_e_q", "shore_f", "sparse_y_to_dense", "validate_witness", "witness_value")
```

The signature/keyword contract is exactly DESIGN 4.4A.2. Imports are limited to dataclasses,
.instance, .shore, and optional future annotations. Direct source inspection must establish
no executable use/import of Fraction, float, true division, tolerances, gcd, reduction,
normalization, algorithmic set iteration, or downstream/verifier machinery. Naming a
forbidden technique in a comment/docstring is not an executable use. Structural record
comparisons and integer bounds are allowed; a ban on rational ordering is not a ban on
ordinary integer validation comparisons.

A fresh-process check must verify the imported module path and compare loaded modules
before and after importing exactfrac.witness. It must not newly import exactfrac_verify,
exactfrac.families, exactfrac.flow, exactfrac.oracle, exactfrac.branch, exactfrac.solve, or
exactfrac.certificate. Attribute transitive imports accurately: dependencies required by
an allowed standard-library module are not falsely reported as direct imports written by
witness.py. Direct forbidden imports remain forbidden regardless of startup state. The
production package root gains no exports, and the verifier's no-production-import boundary
is independently preserved.

No new Empty singleton, SolveResult, certificate envelope, numerical comparison operator,
Unit 09 arithmetic API, branch/endpoint reconstruction, JSON I/O, certificate verifier,
telemetry, or global-optimization routine is introduced. A later CONFORMANCE engineering
note may cite representation/raw-evaluation coverage only after implementation GREEN;
it may not promote theorem rows or close historical W7's complete serialized-certificate
obligation. Full Unit 08 closure still follows TEST_PLAN section 22.

---

## Production Unit 08 witness oracle coverage matrix

| TEST_PLAN obligation | Prospective oracle evidence |
|---|---|
| W8 — public surface, frozen/slotted records, ownership | ORACLE-030, ORACLE-037 |
| W9 — structural Witness constructor | ORACLE-030, ORACLE-034 |
| W10 — ExactValue structural versus rational equality | ORACLE-030, ORACLE-034 |
| W11 — graph-shore sums for all masks | ORACLE-031, ORACLE-035, ORACLE-036 |
| W12 — literal dense-to-sparse output and detachment | ORACLE-032, ORACLE-034 |
| W13 — strict sparse decoding and both round trips | ORACLE-032, ORACLE-034 |
| W14 — full admissibility and isolated guards | ORACLE-033, ORACLE-034, ORACLE-036 |
| W15 — unreduced raw evaluation, separate records | ORACLE-033, ORACLE-035, ORACLE-036 |
| W16 — zero-valued witness distinct from Empty | ORACLE-033 with unchanged ORACLE-001 |
| W17 — exact ValueError and precedence | ORACLE-034; constructor controls ORACLE-030 |
| W18 — source exactness and fresh-process isolation | ORACLE-037 |
| W19 — labels, compact scans, large integer exactness | ORACLE-031, ORACLE-032, ORACLE-035 |
| W20 — independent finite acceptance/evaluation audit | ORACLE-036 plus ORACLE-034 malformed cases |
| Historical W1--W4 production representation portions | ORACLE-032--ORACLE-034, ORACLE-036 |
| Historical W5--W6 production representation conversions | ORACLE-032 and ORACLE-034 |
| Historical W7 raw-evaluation portion only | ORACLE-033 and ORACLE-035; full serialization deferred |
| R3/R4 exact arithmetic path; no production set iteration | ORACLE-037, with explicit witness policy basis |

## Unit 08 numerical fixture payload for independent audit

The following JSON is an exact private audit-data mirror of the numeric fixtures and
corpus totals above. JSON arrays representing dense vectors are converted to exact tuples
by future test setup, not accepted as constructor inputs by implication. This is NOT a
new production file format, certificate schema, or source of mathematical truth independent
of the definitions/derivations above. Its separate handoff copy must agree byte-for-byte
with this block; the audit checks that agreement before arithmetic. Huge values use the
symbolic parameter k fixed in ORACLE-035 rather than thousand-digit decimal literals.

<!-- BEGIN_UNIT08_NUMERIC_FIXTURES -->
```json
{
  "format": "exactfrac-unit08-oracle-audit-fixtures/1",
  "scope": "Private oracle-audit input; not an instance/certificate/result production schema.",
  "authority_commit": "4ad6eaa14d1ae1dd2881416769fa5e88d984a8f6",
  "instances": {
    "O001": {
      "n": 2,
      "edges": [
        [
          0,
          1,
          1
        ]
      ],
      "f": [
        1,
        1
      ]
    },
    "O002": {
      "n": 3,
      "edges": [
        [
          0,
          1,
          1
        ],
        [
          0,
          2,
          1
        ],
        [
          1,
          2,
          1
        ]
      ],
      "f": [
        1,
        1,
        2
      ]
    },
    "O004": {
      "n": 2,
      "edges": [
        [
          0,
          1,
          2
        ]
      ],
      "f": [
        1,
        1
      ]
    },
    "ZERO": {
      "n": 2,
      "edges": [
        [
          0,
          1,
          3
        ]
      ],
      "f": [
        3,
        3
      ]
    },
    "MIXED": {
      "n": 4,
      "edges": [
        [
          0,
          1,
          2
        ],
        [
          0,
          2,
          3
        ],
        [
          0,
          3,
          1
        ],
        [
          1,
          2,
          4
        ],
        [
          1,
          3,
          2
        ],
        [
          2,
          3,
          5
        ]
      ],
      "f": [
        2,
        3,
        4,
        5
      ]
    }
  },
  "mixed_degrees": [
    6,
    8,
    12,
    8
  ],
  "mixed_Q": 17,
  "mixed_sum_columns": [
    "U",
    "s",
    "e",
    "b",
    "d"
  ],
  "mixed_sum_rows": [
    [
      0,
      0,
      0,
      0,
      0
    ],
    [
      1,
      2,
      0,
      6,
      6
    ],
    [
      2,
      3,
      0,
      8,
      8
    ],
    [
      3,
      5,
      2,
      10,
      14
    ],
    [
      4,
      4,
      0,
      12,
      12
    ],
    [
      5,
      6,
      3,
      12,
      18
    ],
    [
      6,
      7,
      4,
      12,
      20
    ],
    [
      7,
      9,
      9,
      8,
      26
    ],
    [
      8,
      5,
      0,
      8,
      8
    ],
    [
      9,
      7,
      1,
      12,
      14
    ],
    [
      10,
      8,
      2,
      12,
      16
    ],
    [
      11,
      10,
      5,
      12,
      22
    ],
    [
      12,
      9,
      5,
      10,
      20
    ],
    [
      13,
      11,
      9,
      8,
      26
    ],
    [
      14,
      12,
      11,
      6,
      28
    ],
    [
      15,
      14,
      17,
      0,
      34
    ]
  ],
  "accepted_witnesses": [
    {
      "id": "unit-witness",
      "instance": "O002",
      "U": 4,
      "y": [
        0,
        1,
        0
      ],
      "sparse": [
        [
          1,
          1
        ]
      ],
      "sums": [
        2,
        0,
        2,
        2
      ],
      "Y": 1,
      "total": 3,
      "raw": [
        2,
        2
      ]
    },
    {
      "id": "unit-competitor",
      "instance": "O002",
      "U": 3,
      "y": [
        0,
        1,
        0
      ],
      "sparse": [
        [
          1,
          1
        ]
      ],
      "sums": [
        2,
        1,
        2,
        4
      ],
      "Y": 1,
      "total": 3,
      "raw": [
        4,
        2
      ]
    },
    {
      "id": "tie-left",
      "instance": "O004",
      "U": 1,
      "y": [
        2
      ],
      "sparse": [
        [
          0,
          2
        ]
      ],
      "sums": [
        1,
        0,
        2,
        2
      ],
      "Y": 2,
      "total": 3,
      "raw": [
        4,
        2
      ]
    },
    {
      "id": "tie-right",
      "instance": "O004",
      "U": 2,
      "y": [
        2
      ],
      "sparse": [
        [
          0,
          2
        ]
      ],
      "sums": [
        1,
        0,
        2,
        2
      ],
      "Y": 2,
      "total": 3,
      "raw": [
        4,
        2
      ]
    },
    {
      "id": "zero-not-empty",
      "instance": "ZERO",
      "U": 1,
      "y": [
        0
      ],
      "sparse": [],
      "sums": [
        3,
        0,
        3,
        3
      ],
      "Y": 0,
      "total": 3,
      "raw": [
        0,
        2
      ]
    },
    {
      "id": "mixed-partial",
      "instance": "MIXED",
      "U": 3,
      "y": [
        0,
        2,
        0,
        1,
        1,
        0
      ],
      "sparse": [
        [
          1,
          2
        ],
        [
          3,
          1
        ],
        [
          4,
          1
        ]
      ],
      "sums": [
        5,
        2,
        10,
        14
      ],
      "Y": 4,
      "total": 9,
      "raw": [
        12,
        8
      ]
    },
    {
      "id": "mixed-no-selected-copies",
      "instance": "MIXED",
      "U": 3,
      "y": [
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "sparse": [],
      "sums": [
        5,
        2,
        10,
        14
      ],
      "Y": 0,
      "total": 5,
      "raw": [
        4,
        4
      ]
    },
    {
      "id": "mixed-all-boundary-copies",
      "instance": "MIXED",
      "U": 3,
      "y": [
        0,
        3,
        1,
        4,
        2,
        0
      ],
      "sparse": [
        [
          1,
          3
        ],
        [
          2,
          1
        ],
        [
          3,
          4
        ],
        [
          4,
          2
        ]
      ],
      "sums": [
        5,
        2,
        10,
        14
      ],
      "Y": 10,
      "total": 15,
      "raw": [
        24,
        14
      ]
    }
  ],
  "inadmissible_boundary_selections": [
    {
      "id": "parity-only",
      "instance": "MIXED",
      "U": 3,
      "y": [
        0,
        1,
        0,
        0,
        0,
        0
      ],
      "sparse": [
        [
          1,
          1
        ]
      ],
      "s": 5,
      "Y": 1,
      "total": 6,
      "reason": "even total; lower bound satisfied"
    },
    {
      "id": "lower-only",
      "instance": "O004",
      "U": 1,
      "y": [
        0
      ],
      "sparse": [],
      "s": 1,
      "Y": 0,
      "total": 1,
      "reason": "odd total below three"
    },
    {
      "id": "whole-shore-parity",
      "instance": "MIXED",
      "U": 15,
      "y": [
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "sparse": [],
      "s": 14,
      "Y": 0,
      "total": 14,
      "reason": "even total; empty boundary is representable"
    }
  ],
  "generic_conversion_controls": [
    {
      "id": "empty-subset",
      "instance": "MIXED",
      "U": 0,
      "y": [
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "sparse": []
    },
    {
      "id": "full-subset",
      "instance": "MIXED",
      "U": 15,
      "y": [
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "sparse": []
    },
    {
      "id": "one-partial-copy-count",
      "instance": "MIXED",
      "U": 3,
      "y": [
        0,
        2,
        0,
        0,
        0,
        0
      ],
      "sparse": [
        [
          1,
          2
        ]
      ]
    }
  ],
  "raw_record_pairs": [
    {
      "left": [
        2,
        2
      ],
      "right": [
        1,
        1
      ],
      "structurally_equal": false,
      "numerically_equal": true
    },
    {
      "left": [
        0,
        2
      ],
      "right": [
        0,
        1
      ],
      "structurally_equal": false,
      "numerically_equal": true
    },
    {
      "left": [
        -2,
        2
      ],
      "right": [
        -1,
        1
      ],
      "structurally_equal": false,
      "numerically_equal": true
    },
    {
      "left": [
        12,
        8
      ],
      "right": [
        3,
        2
      ],
      "structurally_equal": false,
      "numerically_equal": true
    },
    {
      "left": [
        2,
        2
      ],
      "right": [
        2,
        2
      ],
      "structurally_equal": true,
      "numerically_equal": true
    },
    {
      "left": [
        3,
        10
      ],
      "right": [
        2,
        3
      ],
      "structurally_equal": false,
      "numerically_equal": false
    }
  ],
  "large_exponents": [
    1,
    2,
    8,
    64,
    4096
  ],
  "corpus": {
    "by_n": {
      "2": {
        "instances": 5,
        "all_shores": 20,
        "nonempty_shores": 15,
        "generic_selections": 38,
        "nonempty_selections": 33,
        "admissible": 10,
        "parity_rejected": 17,
        "lower_rejected": 6,
        "zero_value_admissible": 0
      },
      "3": {
        "instances": 324,
        "all_shores": 2592,
        "nonempty_shores": 2268,
        "generic_selections": 12888,
        "nonempty_selections": 12564,
        "admissible": 5907,
        "parity_rejected": 6294,
        "lower_rejected": 363,
        "zero_value_admissible": 249
      }
    },
    "total": {
      "instances": 329,
      "all_shores": 2612,
      "nonempty_shores": 2283,
      "generic_selections": 12926,
      "nonempty_selections": 12597,
      "admissible": 5917,
      "parity_rejected": 6311,
      "lower_rejected": 369,
      "zero_value_admissible": 249
    }
  }
}
```
<!-- END_UNIT08_NUMERIC_FIXTURES -->

**Unit 08 oracle status:** definition/authority-derived, independently recomputed before
production implementation. Existing catalogue bytes and oracle classifications unchanged.
No Unit 08 production or consuming test module exists at this oracle-only checkpoint.
---

## ORACLE-038 — RawPair carrier, strict factory, and exact rejection boundary

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN 4.5A.1--4.5A.4; TEST_PLAN RP1--RP3.

This fixture governs the scalar carrier before `exactfrac.rational` exists. `RawPair` is the
plain type alias `tuple[int, int]`; it is deliberately not a runtime-tagged rational-number
class. A valid pair is an exact built-in tuple of length two, with exact built-in integer
entries `(A,B)` and `B > 0`.

### Literal successful factory outputs

`make_pair` must return the two supplied integer fields literally for every valid row:

| numerator | denominator | exact output |
|---|---|---|
| `0` | `1` | `(0,1)` |
| `0` | `7` | `(0,7)` |
| `6` | `8` | `(6,8)` |
| `-6` | `8` | `(-6,8)` |
| `7` | `1` | `(7,1)` |
| `-7` | `1` | `(-7,1)` |

Common factors are retained. Zero is not rewritten to `(0,1)`. There is no sign-repair path.

For each numerator in `{-3,-2,-1,0,1,2,3}`, denominators `0`, `-1`, and `-3` are rejected
with exact built-in `ValueError`; neither operand is negated. Thus the bounded denominator
rejection subcorpus contains exactly `7*3 = 21` cases.

### Representation/type rejection controls

Each applicable public pair consumer rejects, before arithmetic:

- list `[1,2]`, one-tuple `(1,)`, three-tuple `(1,2,3)`;
- a tuple subclass containing otherwise valid fields;
- `True` or `False` in either field;
- an int subclass in either field;
- float and `fractions.Fraction` fields;
- `None`, iterators/generators, and duck-typed sequence/numeric objects;
- a Unit 08 `ExactValue` or `Witness` object supplied directly instead of an exact tuple;
- any exact tuple whose denominator is zero or negative.

`make_pair` separately rejects non-exact integer numerator/denominator arguments and every
nonpositive denominator. The exact exception type is built-in `ValueError`.

The deliberate carrier limitation is also fixed here: a different program role may happen
to use a two-int tuple with positive second entry, and this scalar boundary cannot infer
that provenance. Future callers must use role-specific names and explicit extraction/
construction discipline; no nominal provenance check is expected from Unit 09.

---

## ORACLE-039 — Mathematical comparison and exact sign without record normalization

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN 4.5A.5--4.5A.6; TEST_PLAN RP4--RP5.

Every comparison below is derived from cross multiplication. The raw tuples remain unchanged.

| left | right | `A*D` | `C*B` | exact compare |
|---|---|---:|---:|---:|
| `(2,2)` | `(1,1)` | 2 | 2 | `0` |
| `(0,2)` | `(0,1)` | 0 | 0 | `0` |
| `(-2,2)` | `(-1,1)` | -2 | -2 | `0` |
| `(12,8)` | `(3,2)` | 24 | 24 | `0` |
| `(3,10)` | `(2,3)` | 9 | 20 | `-1` |
| `(2,3)` | `(3,10)` | 20 | 9 | `1` |
| `(1,3)` | `(1,2)` | 2 | 3 | `-1` |
| `(-1,3)` | `(-1,2)` | -2 | -3 | `1` |
| `(5,7)` | `(4,5)` | 25 | 28 | `-1` |
| `(-5,7)` | `(-4,5)` | -25 | -28 | `1` |

The `(3,10)` versus `(2,3)` row explicitly catches lexicographic tuple comparison:
`3 > 2` as first fields, while `3/10 < 2/3`.

For every positive integer scale `k`, replacing either operand `(A,B)` by `(k*A,k*B)`
must preserve the comparison result. This is a numerical invariance, not permission to
normalize the stored pair.

### Huge close-value fixture

For `L = 2^k`, with `k in {1,2,8,64,4096}` and therefore `L > 1`, compare

```text
left  = (L+1, L)
right = (L,   L-1)
```

because

```text
(L+1)*(L-1) = L^2 - 1
L*L         = L^2
```

so the exact comparison is always `-1`. This exposes any float conversion at large `k`.

### Exact sign table

`pair_sign((A,B))` depends on the numerator only after validating the complete pair:

| pair | exact sign |
|---|---:|
| `(-9,1)` | `-1` |
| `(-1,4097)` | `-1` |
| `(0,1)` | `0` |
| `(0,4097)` | `0` |
| `(1,4097)` | `1` |
| `(9,1)` | `1` |

Zero is an ordinary rational value. No Empty state, `None`, or `(0,1)` rewrite follows from
a zero sign.

---

## ORACLE-040 — Literal add-one arithmetic and initialization boundary

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN 4.5A.7--4.5A.8; TEST_PLAN RP6.

For pair `(A,B)`, the output is literally `(A+B,B)`:

| input pair | exact output |
|---|---|
| `(-5,7)` | `(2,7)` |
| `(-7,7)` | `(0,7)` |
| `(6,8)` | `(14,8)` |
| `(0,5)` | `(5,5)` |
| `(11,6)` | `(17,6)` |

The cancellation row `(-7,7) -> (0,7)` must not become `(0,1)`. The unreduced row
`(6,8) -> (14,8)` must not become `(7,4)`.

For the source-level branch initialization control with fresh scalar point `(c,h)=(11,6)`:

```text
standard initialization    = pair_add_one((11,6)) = (17,6)
accelerated initialization = (11,6)
```

The present oracle fixes only these scalar values. It does not implement branch feasibility,
query order, early return, look-ahead acceptance, or reset control flow.

For `L=2^k`, `k in {1,2,8,64,4096}`, the literal cancellation control

```text
pair_add_one((-L,L)) = (0,L)
```

preserves the supplied denominator exactly.

---

## ORACLE-041 — Literal reflected look-ahead and bounded-operand recurrence

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN 4.5A.7--4.5A.8 and 4.5A.11--4.5A.12; TEST_PLAN RP7 and RP12.

For `newton=(A,B)` and `current=(C,D)`, derive the exact raw output

```text
(2*A*D - C*B, B*D)
```

without reduction or argument reversal.

| newton | current | exact raw output | represented value |
|---|---|---|---|
| `(3,5)` | `(2,7)` | `(32,35)` | `32/35` |
| `(2,7)` | `(3,5)` | `(-1,35)` | `-1/35` |
| `(5,6)` | `(1,6)` | `(54,36)` | `3/2` |
| `(2,4)` | `(3,6)` | `(12,24)` | `1/2` |
| `(1,3)` | `(2,3)` | `(0,9)` | `0` |
| `(1,5)` | `(1,2)` | `(-1,10)` | `-1/10` |

The first two rows distinguish `2*newton-current` from `2*current-newton`.
The equivalent-input row `(2,4),(3,6)` must return `(12,24)`, not either operand.
The zero row must retain denominator 9.

### Fixed-newton recurrence fixture

Keep the newton operand fixed at `(3,5)` and start current at `(1,2)`. Repeated literal
reflection gives:

| step | current raw pair | mathematical value |
|---:|---|---|
| 0 | `(1,2)` | `1/2` |
| 1 | `(7,10)` | `7/10` |
| 2 | `(25,50)` | `1/2` |
| 3 | `(175,250)` | `7/10` |
| 4 | `(625,1250)` | `1/2` |

Each denominator is the previous denominator multiplied by 5. The raw fields therefore
grow even though the represented values alternate. This is a literal arithmetic recurrence,
not a claim that these are successful source-algorithm look-aheads or that arbitrary
two-growing-operand compositions satisfy a particular bit bound.

### Large symbolic row

For `L=2^k`, `k in {1,2,8,64,4096}`:

```text
newton  = (L+1, L)
current = (L+2, L+1)
output  = (L^2 + 2*L + 2, L*(L+1))
```

obtained by direct expansion of the ruled formula.

---

## ORACLE-042 — Residual numerator, sign preservation, and denominator-scaling hazard

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN 4.5A.9; TEST_PLAN RP8.

For parameter `(A,B)`, the exact scalar residual numerator is

```text
B*c - A*h
```

and represents residual `(B*c-A*h)/B`.

| parameter | c | h | raw numerator | represented residual |
|---|---:|---:|---:|---|
| `(2,3)` | 7 | 5 | 11 | `11/3` |
| `(2,3)` | 4 | 6 | 0 | `0` |
| `(2,3)` | 3 | 5 | -1 | `-1/3` |
| `(2,3)` | -4 | 0 | -12 | `-4` |
| `(2,3)` | 2 | -3 | 12 | `4` |

The `h==0` and `h<0` rows exercise only this graph-independent linear form; they do not
claim branch feasibility.

### Same rational parameter, scaled raw numerator

Using the same `c=7,h=5`:

```text
parameter (2,3) -> raw residual 11
parameter (4,6) -> raw residual 22
```

The second parameter is exactly twice the raw encoding of the first, so the raw numerator
also doubles. Both represented residuals are `11/3`, and their signs agree.

### Raw cross-denominator comparison is invalid

Consider two different parameter encodings and scalar inputs:

```text
P1=(1,3), c1=1, h1=1 -> raw numerator 2, residual 2/3
P2=(7,10), c2=1, h2=1 -> raw numerator 3, residual 3/10
```

Raw integers satisfy `2 < 3`, while exact rational residuals satisfy `2/3 > 3/10`.
Therefore raw residual numerators from different denominators may not be globally ordered
as integers. Direct raw comparison is valid only under the same parameter pair.

For `L=2^k`, parameter `(L+1,L)`, `c=L+2`, `h=L+3` gives exactly

```text
L*(L+2) - (L+1)*(L+3) = -2*L - 3.
```

---

## ORACLE-043 — Explicit ExactValue bridge and layer separation

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN 4.5A.1--4.5A.2 and 4.5A.10; TEST_PLAN RP9.

Reuse the closed Unit 08 structural records from ORACLE-030. The arithmetic layer does not
import them and does not accept them implicitly.

At a test/integration call site:

```text
ExactValue(2,2) -> explicit raw tuple (2,2)
ExactValue(1,1) -> explicit raw tuple (1,1)
```

and `compare_pairs((2,2),(1,1))` has numerical result 0, while the two `ExactValue`
records remain structurally unequal and byte/state unchanged.

Similarly, `ExactValue(0,2)` from the zero-valued nonempty witness remains a distinct
record. Explicit extraction `(0,2)` has sign 0 and compares numerically equal to `(0,1)`,
but neither operation turns the original witness into Empty.

Supplying an `ExactValue` object itself to any RawPair consumer is malformed at this layer
and raises exact built-in `ValueError`.

Conversely, starting from an already valid arithmetic pair such as `(12,8)`, a caller may
deliberately construct `ExactValue(12,8)`. That creates a structural record only; it does
not prove witness admissibility, attainment, or optimality. `witness_value` remains the
owner of witness-derived values.

---

## ORACLE-044 — Finite independent scalar arithmetic corpus

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN 4.5A.2--4.5A.11; TEST_PLAN RP10.

The bounded corpus is declared before any production rational module or consuming test exists.

### Domains

```text
NUMERATORS = (-3,-2,-1,0,1,2,3)
DENOMINATORS = (1,2,3,4)
VALID_PAIRS = {(A,B): A in NUMERATORS, B in DENOMINATORS}
SCALARS = (-2,-1,0,1,2)
INVALID_DENOMINATORS = (0,-1,-3)
```

Therefore:

```text
valid raw pairs                         = 7*4       = 28
distinct mathematical Fraction values  = 19
factory nonpositive-denominator rows   = 7*3       = 21
ordered pair comparisons               = 28^2      = 784
ordered pair reflections               = 28^2      = 784
residual evaluations                    = 28*5*5    = 700
```

The independent expected side uses exact `Fraction` only in the verifier/test layer and
separately checks literal raw formulas for update operations.

### Exact aggregate counts

Over every valid pair:

| unary statistic | negative | zero | positive |
|---|---:|---:|---:|
| `pair_sign` | 12 | 4 | 12 |
| numerator of literal `pair_add_one` output | 3 | 3 | 22 |

Over all 784 ordered comparisons:

| compare result | count |
|---:|---:|
| `-1` | 364 |
| `0` | 56 |
| `1` | 364 |

Over all 784 literal reflections, classified by raw output numerator:

| reflected sign | count |
|---:|---:|
| negative | 370 |
| zero | 44 |
| positive | 370 |

Over all 700 residual evaluations:

| residual-numerator sign | count |
|---:|---:|
| negative | 310 |
| zero | 80 |
| positive | 310 |

The core corpus therefore contains 28 successful factory rows, 21 denominator-rejection
factory rows, 28 validation rows, 28 sign rows, 28 add-one rows, 784 comparisons,
784 reflections, and 700 residual rows: `2401` explicitly bounded evaluations before
additional exact-type rejection controls.

For each comparison, independently check `Fraction(left) ? Fraction(right)`. For each
add-one row, check the exact tuple `(A+B,B)` separately from `Fraction(A,B)+1`. For every
reflection, check the literal tuple separately from `2*Fraction(newton)-Fraction(current)`.
For every residual, check both the raw integer `B*c-A*h` and `Fraction(result,B)`.
The aggregate counts above are independently recomputed by the handoff audit and are not
learned from production outputs.

No finite corpus proves algorithm termination or the universal strong-polynomiality claims.

---

## ORACLE-045 — Rational module surface, exactness, isolation, and deferred boundaries

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Source obligations:** DESIGN 4.5A.1--4.5A.2 and 4.5A.11--4.5A.12; TEST_PLAN RP1,
RP11--RP12.

The exact module export tuple is:

```text
("RawPair", "compare_pairs", "make_pair", "pair_add_one", "pair_reflect",
 "pair_sign", "residual_numerator", "validate_pair")
```

The public signatures and argument-role names are exactly those ruled in DESIGN 4.5A.2.

The production module has no project imports and no verifier imports. Direct source/AST
inspection must reject executable use of:

- float constants or float conversion/arithmetic;
- `fractions.Fraction`, decimal, math, gcd/reduction helpers;
- true or floor division, remainder-based reduction, tolerance logic;
- recursion;
- magnitude/bit-length-driven iteration;
- direct, named, comprehended, or derived algorithmic set iteration;
- downstream graph, branch, solve, certificate, telemetry, or verifier machinery.

Each valid public operation has a bounded constant number of structural checks and exact
integer arithmetic/comparison operations. This is a structural-operation statement only:
integer bit sizes and actual bit-operation time may grow with the operands.

A fresh process importing `exactfrac.rational` must not newly import any other
`exactfrac.*` submodule or any `exactfrac_verify` module. The package root gains no exports.

The huge fixtures in ORACLE-039--ORACLE-042 are exactness/recurrence controls, not timing
thresholds or asserted production bit-length ceilings. Unit 09 does not close the
algorithm-level `lem:standard-bits`, `lem:bitgrowth`, branch termination, sign-routing,
argmin, global-solve, certificate, or telemetry obligations.

---

## Production Unit 09 raw rational-pair oracle coverage matrix

| TEST_PLAN obligation | Prospective oracle evidence |
|---|---|
| RP1 — scalar ownership and exact public interface | ORACLE-038, ORACLE-045 |
| RP2 — strict denominator positivity and literal preservation | ORACLE-038, ORACLE-040 |
| RP3 — exact rejection matrix and validation-before-arithmetic | ORACLE-038 |
| RP4 — mathematical comparison independent of raw identity | ORACLE-039, ORACLE-044 |
| RP5 — exact sign without normalization/Empty inference | ORACLE-039, ORACLE-043 |
| RP6 — literal add-one and initialization boundary | ORACLE-040, ORACLE-044 |
| RP7 — literal reflected look-ahead and fixed roles | ORACLE-041, ORACLE-044 |
| RP8 — exact residual and parameter-dependent scaling | ORACLE-042, ORACLE-044 |
| RP9 — explicit ExactValue bridge | ORACLE-043 |
| RP10 — finite independent arithmetic corpus | ORACLE-044 |
| RP11 — exactness, isolation, bounded primitive work | ORACLE-045 |
| RP12 — large integers and literal recurrence growth | ORACLE-039--ORACLE-042, ORACLE-045 |

**Unit 09 oracle status:** authority-derived and independently recomputed before
`tests/test_rational.py` or `exactfrac/rational.py` exists. No Unit 09 production output is
used to establish these expected values.

---

## ORACLE-046 — Sign-routing records, exact shape, and fixed active instances

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Authority:** DESIGN 4.7.1--4.7.5, 4.7.8; TEST_PLAN SR1--SR3, SR11.
Authority commit: `4af674e70155c632b6ddf3e9ee36109854f227af`.

The Unit 10 fixtures are registered before any `tests/test_sign_routing.py` or
`exactfrac/sign_routing.py` exists. They do not call max-flow or optimize a branch.
The source is the V2.2 sign-routing lemma, its proof and directed conversion, and the
literal c_j/h_j table in prop:branch-transform. Prospective Python representation choices
are those of the adopted DESIGN 4.7, not new requirements invented by an implementation.

### Accepted standalone coefficient record shapes

For `SignRoutingCoefficients(a, gamma, constant)`, exact built-in integers and an exact tuple
are required. The following records are valid even when their gamma length does not fit a
particular instance. Empty gamma is accepted here and rejected only by a builder whose
instance dimension does not match.

<!-- UNIT10:COEFFICIENT_SHAPES:BEGIN -->
| a | gamma | constant |
|---:|---|---:|
| 0 | `()` | -7 |
| 0 | `(0, 0)` | 5 |
| 2 | `(3, -4, 0, 5)` | -7 |
<!-- UNIT10:COEFFICIENT_SHAPES:END -->

The stored fields/slots are exactly `(a, gamma, constant)`. Equal records hash equally;
unequal records are not required to have different hashes. Do not pin cross-process hash
integers. Frozen/slotted state has no __dict__ or generated ordering and no extra cached
Instance, degree, parameter, branch, or negative-shift field. Valid shape is not branch
provenance. Numeric magnitude has no upper cutoff.

### Accepted standalone network record shapes

`SignRoutedNetwork(vertex_count, arcs, negative_shift, constant)` stores those four fields,
not redundant terminal fields. Properties are exactly
`(node_count, source, sink) = (vertex_count+2, vertex_count, vertex_count+1)`.

<!-- UNIT10:NETWORK_SHAPES:BEGIN -->
| vertex_count | arcs (exact tuple notation) | negative_shift | constant | node_count, source, sink |
|---:|---|---:|---:|---|
| 1 | `()` | 7 | -2 | `(3, 1, 2)` |
| 1 | `((0, 2, 5), (0, 2, 2), (2, 0, 1), (1, 0, 0))` | 11 | -4 | `(3, 1, 2)` |
<!-- UNIT10:NETWORK_SHAPES:END -->

The second record deliberately retains repeated directed pairs, their supplied order,
asymmetric capacities, and a zero-capacity arc. It is a valid scalar/network representation,
not a claim that it came from sign routing. The constructor must not sort, aggregate,
create opposite arcs, delete zeros, or infer coefficients. The empty-arc record is valid,
whereas the actual builder on an active Instance always emits 2(m+n)>0 original arcs.
Mutation/frozen-assignment and wrong-arity behavior are ordinary Python behavior, not part
of the malformed-data exact-ValueError matrix below.

### Fixed canonical active instances

RICH is exactly ORACLE-025; MIXED is exactly ORACLE-031. EQUALITY and TRIANGLE are new tiny
local fixtures, not a new input model. All records below have labels=None initially.

<!-- UNIT10:INSTANCES:BEGIN -->
| Name | n | Canonical `(u,v,q)` records | f |
|---|---:|---|---|
| EQUALITY | 2 | `((0, 1, 3),)` | `(3, 3)` |
| MIXED | 4 | `((0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 4), (1, 3, 2), (2, 3, 5))` | `(2, 3, 4, 5)` |
| RICH | 5 | `((0, 2, 2), (1, 2, 2), (2, 4, 1), (3, 4, 1))` | `(1, 1, 1, 1, 2)` |
| TRIANGLE | 3 | `((0, 1, 1), (0, 2, 1), (1, 2, 1))` | `(1, 1, 1)` |
<!-- UNIT10:INSTANCES:END -->

Derive degrees from endpoint incidences, not from a production property:

```text
RICH:     m=4, Q=6,  d_q=(2,2,5,1,2)
MIXED:    m=6, Q=17, d_q=(6,8,12,8)
EQUALITY: m=1, Q=3,  d_q=(3,3)=f
TRIANGLE: m=3, Q=3,  d_q=(2,2,2)
```

Thus each f_v is positive and at most its degree. The support tuples are in canonical
edge_ref order; these fixtures do not authorize raw-instance repair or new normalization.

---

## ORACLE-047 — Four-branch coefficient rows, including negative parameters in every branch

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Authority:** DESIGN 4.7.6--4.7.7; TEST_PLAN SR4, SR7, SR10.

The ten literal raw parameter encodings, in the prescribed fixture order, are:

```text
(-3,1), (-2,1), (-1,2), (-2,4), (0,1), (0,3), (1,1), (2,1), (3,2), (6,4)
```

Equal-value encodings remain separate rows; no reduction is performed. For s=f(U), b=b_q(U),
d=d_q(U), the independent source expressions are

```text
(c0,h0) = (s+b-1, d+1-s)
(c1,h1) = (s+b-2, d-s)
(c2,h2) = (b-d,   s-1)
(c3,h3) = (b-d-2, s)
```

With parameter (A,B), the coefficient table is derived by expansion of B*c_j-A*h_j:

```text
j=0: a=B; gamma_v=(A+B)*f_v-A*d_v; constant=-(A+B)
j=1: a=B; gamma_v=(A+B)*f_v-A*d_v; constant=-2*B
j=2: a=B; gamma_v=-B*d_v-A*f_v;    constant=A
j=3: a=B; gamma_v=-B*d_v-A*f_v;    constant=-2*B
```

Every following gamma tuple is indexed by increasing original vertex index. C_minus is a
separate expected builder output, not an extra stored coefficient-record field. The 120
rows specify all four branches on all ten parameters for RICH, MIXED, and EQUALITY.

<!-- UNIT10:BRANCHES:BEGIN -->
| Instance | Parameter `(A,B)` | j | a | gamma | constant | C_minus |
|---|---|---:|---:|---|---:|---:|
| RICH | `(-3, 1)` | 0 | 1 | `(4, 4, 13, 1, 2)` | 2 | 0 |
| RICH | `(-3, 1)` | 1 | 1 | `(4, 4, 13, 1, 2)` | -2 | 0 |
| RICH | `(-3, 1)` | 2 | 1 | `(1, 1, -2, 2, 4)` | -3 | 2 |
| RICH | `(-3, 1)` | 3 | 1 | `(1, 1, -2, 2, 4)` | -2 | 2 |
| RICH | `(-2, 1)` | 0 | 1 | `(3, 3, 9, 1, 2)` | 1 | 0 |
| RICH | `(-2, 1)` | 1 | 1 | `(3, 3, 9, 1, 2)` | -2 | 0 |
| RICH | `(-2, 1)` | 2 | 1 | `(0, 0, -3, 1, 2)` | -2 | 3 |
| RICH | `(-2, 1)` | 3 | 1 | `(0, 0, -3, 1, 2)` | -2 | 3 |
| RICH | `(-1, 2)` | 0 | 2 | `(3, 3, 6, 2, 4)` | -1 | 0 |
| RICH | `(-1, 2)` | 1 | 2 | `(3, 3, 6, 2, 4)` | -4 | 0 |
| RICH | `(-1, 2)` | 2 | 2 | `(-3, -3, -9, -1, -2)` | -1 | 18 |
| RICH | `(-1, 2)` | 3 | 2 | `(-3, -3, -9, -1, -2)` | -4 | 18 |
| RICH | `(-2, 4)` | 0 | 4 | `(6, 6, 12, 4, 8)` | -2 | 0 |
| RICH | `(-2, 4)` | 1 | 4 | `(6, 6, 12, 4, 8)` | -8 | 0 |
| RICH | `(-2, 4)` | 2 | 4 | `(-6, -6, -18, -2, -4)` | -2 | 36 |
| RICH | `(-2, 4)` | 3 | 4 | `(-6, -6, -18, -2, -4)` | -8 | 36 |
| RICH | `(0, 1)` | 0 | 1 | `(1, 1, 1, 1, 2)` | -1 | 0 |
| RICH | `(0, 1)` | 1 | 1 | `(1, 1, 1, 1, 2)` | -2 | 0 |
| RICH | `(0, 1)` | 2 | 1 | `(-2, -2, -5, -1, -2)` | 0 | 12 |
| RICH | `(0, 1)` | 3 | 1 | `(-2, -2, -5, -1, -2)` | -2 | 12 |
| RICH | `(0, 3)` | 0 | 3 | `(3, 3, 3, 3, 6)` | -3 | 0 |
| RICH | `(0, 3)` | 1 | 3 | `(3, 3, 3, 3, 6)` | -6 | 0 |
| RICH | `(0, 3)` | 2 | 3 | `(-6, -6, -15, -3, -6)` | 0 | 36 |
| RICH | `(0, 3)` | 3 | 3 | `(-6, -6, -15, -3, -6)` | -6 | 36 |
| RICH | `(1, 1)` | 0 | 1 | `(0, 0, -3, 1, 2)` | -2 | 3 |
| RICH | `(1, 1)` | 1 | 1 | `(0, 0, -3, 1, 2)` | -2 | 3 |
| RICH | `(1, 1)` | 2 | 1 | `(-3, -3, -6, -2, -4)` | 1 | 18 |
| RICH | `(1, 1)` | 3 | 1 | `(-3, -3, -6, -2, -4)` | -2 | 18 |
| RICH | `(2, 1)` | 0 | 1 | `(-1, -1, -7, 1, 2)` | -3 | 9 |
| RICH | `(2, 1)` | 1 | 1 | `(-1, -1, -7, 1, 2)` | -2 | 9 |
| RICH | `(2, 1)` | 2 | 1 | `(-4, -4, -7, -3, -6)` | 2 | 24 |
| RICH | `(2, 1)` | 3 | 1 | `(-4, -4, -7, -3, -6)` | -2 | 24 |
| RICH | `(3, 2)` | 0 | 2 | `(-1, -1, -10, 2, 4)` | -5 | 12 |
| RICH | `(3, 2)` | 1 | 2 | `(-1, -1, -10, 2, 4)` | -4 | 12 |
| RICH | `(3, 2)` | 2 | 2 | `(-7, -7, -13, -5, -10)` | 3 | 42 |
| RICH | `(3, 2)` | 3 | 2 | `(-7, -7, -13, -5, -10)` | -4 | 42 |
| RICH | `(6, 4)` | 0 | 4 | `(-2, -2, -20, 4, 8)` | -10 | 24 |
| RICH | `(6, 4)` | 1 | 4 | `(-2, -2, -20, 4, 8)` | -8 | 24 |
| RICH | `(6, 4)` | 2 | 4 | `(-14, -14, -26, -10, -20)` | 6 | 84 |
| RICH | `(6, 4)` | 3 | 4 | `(-14, -14, -26, -10, -20)` | -8 | 84 |
| MIXED | `(-3, 1)` | 0 | 1 | `(14, 18, 28, 14)` | 2 | 0 |
| MIXED | `(-3, 1)` | 1 | 1 | `(14, 18, 28, 14)` | -2 | 0 |
| MIXED | `(-3, 1)` | 2 | 1 | `(0, 1, 0, 7)` | -3 | 0 |
| MIXED | `(-3, 1)` | 3 | 1 | `(0, 1, 0, 7)` | -2 | 0 |
| MIXED | `(-2, 1)` | 0 | 1 | `(10, 13, 20, 11)` | 1 | 0 |
| MIXED | `(-2, 1)` | 1 | 1 | `(10, 13, 20, 11)` | -2 | 0 |
| MIXED | `(-2, 1)` | 2 | 1 | `(-2, -2, -4, 2)` | -2 | 8 |
| MIXED | `(-2, 1)` | 3 | 1 | `(-2, -2, -4, 2)` | -2 | 8 |
| MIXED | `(-1, 2)` | 0 | 2 | `(8, 11, 16, 13)` | -1 | 0 |
| MIXED | `(-1, 2)` | 1 | 2 | `(8, 11, 16, 13)` | -4 | 0 |
| MIXED | `(-1, 2)` | 2 | 2 | `(-10, -13, -20, -11)` | -1 | 54 |
| MIXED | `(-1, 2)` | 3 | 2 | `(-10, -13, -20, -11)` | -4 | 54 |
| MIXED | `(-2, 4)` | 0 | 4 | `(16, 22, 32, 26)` | -2 | 0 |
| MIXED | `(-2, 4)` | 1 | 4 | `(16, 22, 32, 26)` | -8 | 0 |
| MIXED | `(-2, 4)` | 2 | 4 | `(-20, -26, -40, -22)` | -2 | 108 |
| MIXED | `(-2, 4)` | 3 | 4 | `(-20, -26, -40, -22)` | -8 | 108 |
| MIXED | `(0, 1)` | 0 | 1 | `(2, 3, 4, 5)` | -1 | 0 |
| MIXED | `(0, 1)` | 1 | 1 | `(2, 3, 4, 5)` | -2 | 0 |
| MIXED | `(0, 1)` | 2 | 1 | `(-6, -8, -12, -8)` | 0 | 34 |
| MIXED | `(0, 1)` | 3 | 1 | `(-6, -8, -12, -8)` | -2 | 34 |
| MIXED | `(0, 3)` | 0 | 3 | `(6, 9, 12, 15)` | -3 | 0 |
| MIXED | `(0, 3)` | 1 | 3 | `(6, 9, 12, 15)` | -6 | 0 |
| MIXED | `(0, 3)` | 2 | 3 | `(-18, -24, -36, -24)` | 0 | 102 |
| MIXED | `(0, 3)` | 3 | 3 | `(-18, -24, -36, -24)` | -6 | 102 |
| MIXED | `(1, 1)` | 0 | 1 | `(-2, -2, -4, 2)` | -2 | 8 |
| MIXED | `(1, 1)` | 1 | 1 | `(-2, -2, -4, 2)` | -2 | 8 |
| MIXED | `(1, 1)` | 2 | 1 | `(-8, -11, -16, -13)` | 1 | 48 |
| MIXED | `(1, 1)` | 3 | 1 | `(-8, -11, -16, -13)` | -2 | 48 |
| MIXED | `(2, 1)` | 0 | 1 | `(-6, -7, -12, -1)` | -3 | 26 |
| MIXED | `(2, 1)` | 1 | 1 | `(-6, -7, -12, -1)` | -2 | 26 |
| MIXED | `(2, 1)` | 2 | 1 | `(-10, -14, -20, -18)` | 2 | 62 |
| MIXED | `(2, 1)` | 3 | 1 | `(-10, -14, -20, -18)` | -2 | 62 |
| MIXED | `(3, 2)` | 0 | 2 | `(-8, -9, -16, 1)` | -5 | 33 |
| MIXED | `(3, 2)` | 1 | 2 | `(-8, -9, -16, 1)` | -4 | 33 |
| MIXED | `(3, 2)` | 2 | 2 | `(-18, -25, -36, -31)` | 3 | 110 |
| MIXED | `(3, 2)` | 3 | 2 | `(-18, -25, -36, -31)` | -4 | 110 |
| MIXED | `(6, 4)` | 0 | 4 | `(-16, -18, -32, 2)` | -10 | 66 |
| MIXED | `(6, 4)` | 1 | 4 | `(-16, -18, -32, 2)` | -8 | 66 |
| MIXED | `(6, 4)` | 2 | 4 | `(-36, -50, -72, -62)` | 6 | 220 |
| MIXED | `(6, 4)` | 3 | 4 | `(-36, -50, -72, -62)` | -8 | 220 |
| EQUALITY | `(-3, 1)` | 0 | 1 | `(3, 3)` | 2 | 0 |
| EQUALITY | `(-3, 1)` | 1 | 1 | `(3, 3)` | -2 | 0 |
| EQUALITY | `(-3, 1)` | 2 | 1 | `(6, 6)` | -3 | 0 |
| EQUALITY | `(-3, 1)` | 3 | 1 | `(6, 6)` | -2 | 0 |
| EQUALITY | `(-2, 1)` | 0 | 1 | `(3, 3)` | 1 | 0 |
| EQUALITY | `(-2, 1)` | 1 | 1 | `(3, 3)` | -2 | 0 |
| EQUALITY | `(-2, 1)` | 2 | 1 | `(3, 3)` | -2 | 0 |
| EQUALITY | `(-2, 1)` | 3 | 1 | `(3, 3)` | -2 | 0 |
| EQUALITY | `(-1, 2)` | 0 | 2 | `(6, 6)` | -1 | 0 |
| EQUALITY | `(-1, 2)` | 1 | 2 | `(6, 6)` | -4 | 0 |
| EQUALITY | `(-1, 2)` | 2 | 2 | `(-3, -3)` | -1 | 6 |
| EQUALITY | `(-1, 2)` | 3 | 2 | `(-3, -3)` | -4 | 6 |
| EQUALITY | `(-2, 4)` | 0 | 4 | `(12, 12)` | -2 | 0 |
| EQUALITY | `(-2, 4)` | 1 | 4 | `(12, 12)` | -8 | 0 |
| EQUALITY | `(-2, 4)` | 2 | 4 | `(-6, -6)` | -2 | 12 |
| EQUALITY | `(-2, 4)` | 3 | 4 | `(-6, -6)` | -8 | 12 |
| EQUALITY | `(0, 1)` | 0 | 1 | `(3, 3)` | -1 | 0 |
| EQUALITY | `(0, 1)` | 1 | 1 | `(3, 3)` | -2 | 0 |
| EQUALITY | `(0, 1)` | 2 | 1 | `(-3, -3)` | 0 | 6 |
| EQUALITY | `(0, 1)` | 3 | 1 | `(-3, -3)` | -2 | 6 |
| EQUALITY | `(0, 3)` | 0 | 3 | `(9, 9)` | -3 | 0 |
| EQUALITY | `(0, 3)` | 1 | 3 | `(9, 9)` | -6 | 0 |
| EQUALITY | `(0, 3)` | 2 | 3 | `(-9, -9)` | 0 | 18 |
| EQUALITY | `(0, 3)` | 3 | 3 | `(-9, -9)` | -6 | 18 |
| EQUALITY | `(1, 1)` | 0 | 1 | `(3, 3)` | -2 | 0 |
| EQUALITY | `(1, 1)` | 1 | 1 | `(3, 3)` | -2 | 0 |
| EQUALITY | `(1, 1)` | 2 | 1 | `(-6, -6)` | 1 | 12 |
| EQUALITY | `(1, 1)` | 3 | 1 | `(-6, -6)` | -2 | 12 |
| EQUALITY | `(2, 1)` | 0 | 1 | `(3, 3)` | -3 | 0 |
| EQUALITY | `(2, 1)` | 1 | 1 | `(3, 3)` | -2 | 0 |
| EQUALITY | `(2, 1)` | 2 | 1 | `(-9, -9)` | 2 | 18 |
| EQUALITY | `(2, 1)` | 3 | 1 | `(-9, -9)` | -2 | 18 |
| EQUALITY | `(3, 2)` | 0 | 2 | `(6, 6)` | -5 | 0 |
| EQUALITY | `(3, 2)` | 1 | 2 | `(6, 6)` | -4 | 0 |
| EQUALITY | `(3, 2)` | 2 | 2 | `(-15, -15)` | 3 | 30 |
| EQUALITY | `(3, 2)` | 3 | 2 | `(-15, -15)` | -4 | 30 |
| EQUALITY | `(6, 4)` | 0 | 4 | `(12, 12)` | -10 | 0 |
| EQUALITY | `(6, 4)` | 1 | 4 | `(12, 12)` | -8 | 0 |
| EQUALITY | `(6, 4)` | 2 | 4 | `(-30, -30)` | 6 | 60 |
| EQUALITY | `(6, 4)` | 3 | 4 | `(-30, -30)` | -8 | 60 |
<!-- UNIT10:BRANCHES:END -->

### Sign anchors that must not be weakened

At (0,1), branches 0/1 have gamma=f and C_minus=0; branches 2/3 have gamma=-d_q and
C_minus=2Q. Thus RICH has C_minus=12 and MIXED has C_minus=34 in branches 2/3.

For A<0 and active input, gamma in branches 0/1 can be rewritten as
`B*f_v+(-A)*(d_v-f_v)>0`; these branches have only positive sink spokes. They are not
permitted to skip negative-A tests merely because this algebra guarantees positivity.

At RICH (-2,1), branches 0/1 have `(3,3,9,1,2)` and C_minus=0, while branches 2/3 have
`(0,0,-3,1,2)` and C_minus=3. This tests all three coefficient signs in the latter family.
At RICH (-3,1), branches 2/3 share `(1,1,-2,2,4)` and shift 2 but have distinct constants
-3 and -2. The (-2,1) coincidence of those constants must not hide a branch error.

For EQUALITY, branches 0/1 have gamma=B*f for every signed A. The coefficient routine must
obtain the degree tuple once before the increasing-vertex scan; a correct numerical row
alone does not establish that structural-work requirement. It is also inspected in SR15.

---

## ORACLE-048 — Complete original arc tuples and directly derived cut tables

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Authority:** DESIGN 4.7.8--4.7.11; TEST_PLAN SR5--SR6, SR8, SR12.

Each support edge emits both original directions before any spokes, in edge_ref order.
Spokes follow increasing original vertex order. Nonnegative gamma, including zero, emits
v->sink then sink->v. Negative gamma emits source->v then v->source. The two directions
have equal capacity. They are original capacity arcs, not residual reverse entries.
All eight lists below are exact tuple fixtures, including zeros and order.

```text
EQUALITY: source=2, sink=3, node_count=4,  original arc records=6
MIXED:    source=4, sink=5, node_count=6,  original arc records=20
RICH:     source=5, sink=6, node_count=7,  original arc records=18
```

For each U, X_U={source} union U. A directed arc contributes only if its tail lies in X_U
and its head lies outside. Opposite directions of a crossing pair are not both counted.
The following scalar tables are independently derived from input edges and coefficients:
`Psi=a*b_q(U)+sum_U gamma`; `cut=Psi+C_minus`; `recovered=Psi+constant`.
A separate direct crossing count over each literal arc list must give the same cut column.
The eight fixtures contain 128 explicit all-shore rows.

<!-- UNIT10:NETWORKS:BEGIN -->
### N1 — EQUALITY

`(a, gamma, constant) = (2, (-4, 5), -3)`
`negative_shift = 4`

Exact original arc tuple:

```text
(
    (0, 1, 6),
    (1, 0, 6),
    (2, 0, 4),
    (0, 2, 4),
    (1, 3, 5),
    (3, 1, 5),
)
```

| U mask | Psi(U) | Directed cut | Recovered objective |
|---:|---:|---:|---:|
| 0 | 0 | 4 | -3 |
| 1 | 2 | 6 | -1 |
| 2 | 11 | 15 | 8 |
| 3 | 1 | 5 | -2 |

### N2 — EQUALITY

`(a, gamma, constant) = (0, (-4, 5), 7)`
`negative_shift = 4`

Exact original arc tuple:

```text
(
    (0, 1, 0),
    (1, 0, 0),
    (2, 0, 4),
    (0, 2, 4),
    (1, 3, 5),
    (3, 1, 5),
)
```

| U mask | Psi(U) | Directed cut | Recovered objective |
|---:|---:|---:|---:|
| 0 | 0 | 4 | 7 |
| 1 | -4 | 0 | 3 |
| 2 | 5 | 9 | 12 |
| 3 | 1 | 5 | 8 |

### N3 — EQUALITY

`(a, gamma, constant) = (2, (0, 0), -7)`
`negative_shift = 0`

Exact original arc tuple:

```text
(
    (0, 1, 6),
    (1, 0, 6),
    (0, 3, 0),
    (3, 0, 0),
    (1, 3, 0),
    (3, 1, 0),
)
```

| U mask | Psi(U) | Directed cut | Recovered objective |
|---:|---:|---:|---:|
| 0 | 0 | 0 | -7 |
| 1 | 6 | 6 | -1 |
| 2 | 6 | 6 | -1 |
| 3 | 0 | 0 | -7 |

### N4 — EQUALITY

`(a, gamma, constant) = (0, (0, 0), 5)`
`negative_shift = 0`

Exact original arc tuple:

```text
(
    (0, 1, 0),
    (1, 0, 0),
    (0, 3, 0),
    (3, 0, 0),
    (1, 3, 0),
    (3, 1, 0),
)
```

| U mask | Psi(U) | Directed cut | Recovered objective |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 5 |
| 1 | 0 | 0 | 5 |
| 2 | 0 | 0 | 5 |
| 3 | 0 | 0 | 5 |

### N5 — MIXED

`(a, gamma, constant) = (2, (3, -4, 0, 5), -7)`
`negative_shift = 4`

Exact original arc tuple:

```text
(
    (0, 1, 4),
    (1, 0, 4),
    (0, 2, 6),
    (2, 0, 6),
    (0, 3, 2),
    (3, 0, 2),
    (1, 2, 8),
    (2, 1, 8),
    (1, 3, 4),
    (3, 1, 4),
    (2, 3, 10),
    (3, 2, 10),
    (0, 5, 3),
    (5, 0, 3),
    (4, 1, 4),
    (1, 4, 4),
    (2, 5, 0),
    (5, 2, 0),
    (3, 5, 5),
    (5, 3, 5),
)
```

| U mask | Psi(U) | Directed cut | Recovered objective |
|---:|---:|---:|---:|
| 0 | 0 | 4 | -7 |
| 1 | 15 | 19 | 8 |
| 2 | 12 | 16 | 5 |
| 3 | 19 | 23 | 12 |
| 4 | 24 | 28 | 17 |
| 5 | 27 | 31 | 20 |
| 6 | 20 | 24 | 13 |
| 7 | 15 | 19 | 8 |
| 8 | 21 | 25 | 14 |
| 9 | 32 | 36 | 25 |
| 10 | 25 | 29 | 18 |
| 11 | 28 | 32 | 21 |
| 12 | 25 | 29 | 18 |
| 13 | 24 | 28 | 17 |
| 14 | 13 | 17 | 6 |
| 15 | 4 | 8 | -3 |

### N6 — RICH

`(a, gamma, constant) = (1, (4, 4, 13, 1, 2), 2)`
`negative_shift = 0`

Exact original arc tuple:

```text
(
    (0, 2, 2),
    (2, 0, 2),
    (1, 2, 2),
    (2, 1, 2),
    (2, 4, 1),
    (4, 2, 1),
    (3, 4, 1),
    (4, 3, 1),
    (0, 6, 4),
    (6, 0, 4),
    (1, 6, 4),
    (6, 1, 4),
    (2, 6, 13),
    (6, 2, 13),
    (3, 6, 1),
    (6, 3, 1),
    (4, 6, 2),
    (6, 4, 2),
)
```

| U mask | Psi(U) | Directed cut | Recovered objective |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 2 |
| 1 | 6 | 6 | 8 |
| 2 | 6 | 6 | 8 |
| 3 | 12 | 12 | 14 |
| 4 | 18 | 18 | 20 |
| 5 | 20 | 20 | 22 |
| 6 | 20 | 20 | 22 |
| 7 | 22 | 22 | 24 |
| 8 | 2 | 2 | 4 |
| 9 | 8 | 8 | 10 |
| 10 | 8 | 8 | 10 |
| 11 | 14 | 14 | 16 |
| 12 | 20 | 20 | 22 |
| 13 | 22 | 22 | 24 |
| 14 | 22 | 22 | 24 |
| 15 | 24 | 24 | 26 |
| 16 | 4 | 4 | 6 |
| 17 | 10 | 10 | 12 |
| 18 | 10 | 10 | 12 |
| 19 | 16 | 16 | 18 |
| 20 | 20 | 20 | 22 |
| 21 | 22 | 22 | 24 |
| 22 | 22 | 22 | 24 |
| 23 | 24 | 24 | 26 |
| 24 | 4 | 4 | 6 |
| 25 | 10 | 10 | 12 |
| 26 | 10 | 10 | 12 |
| 27 | 16 | 16 | 18 |
| 28 | 20 | 20 | 22 |
| 29 | 22 | 22 | 24 |
| 30 | 22 | 22 | 24 |
| 31 | 24 | 24 | 26 |

### N7 — RICH

`(a, gamma, constant) = (1, (0, 0, -3, 1, 2), -2)`
`negative_shift = 3`

Exact original arc tuple:

```text
(
    (0, 2, 2),
    (2, 0, 2),
    (1, 2, 2),
    (2, 1, 2),
    (2, 4, 1),
    (4, 2, 1),
    (3, 4, 1),
    (4, 3, 1),
    (0, 6, 0),
    (6, 0, 0),
    (1, 6, 0),
    (6, 1, 0),
    (5, 2, 3),
    (2, 5, 3),
    (3, 6, 1),
    (6, 3, 1),
    (4, 6, 2),
    (6, 4, 2),
)
```

| U mask | Psi(U) | Directed cut | Recovered objective |
|---:|---:|---:|---:|
| 0 | 0 | 3 | -2 |
| 1 | 2 | 5 | 0 |
| 2 | 2 | 5 | 0 |
| 3 | 4 | 7 | 2 |
| 4 | 2 | 5 | 0 |
| 5 | 0 | 3 | -2 |
| 6 | 0 | 3 | -2 |
| 7 | -2 | 1 | -4 |
| 8 | 2 | 5 | 0 |
| 9 | 4 | 7 | 2 |
| 10 | 4 | 7 | 2 |
| 11 | 6 | 9 | 4 |
| 12 | 4 | 7 | 2 |
| 13 | 2 | 5 | 0 |
| 14 | 2 | 5 | 0 |
| 15 | 0 | 3 | -2 |
| 16 | 4 | 7 | 2 |
| 17 | 6 | 9 | 4 |
| 18 | 6 | 9 | 4 |
| 19 | 8 | 11 | 6 |
| 20 | 4 | 7 | 2 |
| 21 | 2 | 5 | 0 |
| 22 | 2 | 5 | 0 |
| 23 | 0 | 3 | -2 |
| 24 | 4 | 7 | 2 |
| 25 | 6 | 9 | 4 |
| 26 | 6 | 9 | 4 |
| 27 | 8 | 11 | 6 |
| 28 | 4 | 7 | 2 |
| 29 | 2 | 5 | 0 |
| 30 | 2 | 5 | 0 |
| 31 | 0 | 3 | -2 |

### N8 — RICH

`(a, gamma, constant) = (1, (-2, -2, -5, -1, -2), 0)`
`negative_shift = 12`

Exact original arc tuple:

```text
(
    (0, 2, 2),
    (2, 0, 2),
    (1, 2, 2),
    (2, 1, 2),
    (2, 4, 1),
    (4, 2, 1),
    (3, 4, 1),
    (4, 3, 1),
    (5, 0, 2),
    (0, 5, 2),
    (5, 1, 2),
    (1, 5, 2),
    (5, 2, 5),
    (2, 5, 5),
    (5, 3, 1),
    (3, 5, 1),
    (5, 4, 2),
    (4, 5, 2),
)
```

| U mask | Psi(U) | Directed cut | Recovered objective |
|---:|---:|---:|---:|
| 0 | 0 | 12 | 0 |
| 1 | 0 | 12 | 0 |
| 2 | 0 | 12 | 0 |
| 3 | 0 | 12 | 0 |
| 4 | 0 | 12 | 0 |
| 5 | -4 | 8 | -4 |
| 6 | -4 | 8 | -4 |
| 7 | -8 | 4 | -8 |
| 8 | 0 | 12 | 0 |
| 9 | 0 | 12 | 0 |
| 10 | 0 | 12 | 0 |
| 11 | 0 | 12 | 0 |
| 12 | 0 | 12 | 0 |
| 13 | -4 | 8 | -4 |
| 14 | -4 | 8 | -4 |
| 15 | -8 | 4 | -8 |
| 16 | 0 | 12 | 0 |
| 17 | 0 | 12 | 0 |
| 18 | 0 | 12 | 0 |
| 19 | 0 | 12 | 0 |
| 20 | -2 | 10 | -2 |
| 21 | -6 | 6 | -6 |
| 22 | -6 | 6 | -6 |
| 23 | -10 | 2 | -10 |
| 24 | -2 | 10 | -2 |
| 25 | -2 | 10 | -2 |
| 26 | -2 | 10 | -2 |
| 27 | -2 | 10 | -2 |
| 28 | -4 | 8 | -4 |
| 29 | -8 | 4 | -8 |
| 30 | -8 | 4 | -8 |
| 31 | -12 | 0 | -12 |

<!-- UNIT10:NETWORKS:END -->

N2 retains its zero support arcs; N3 retains zero sink-spoke pairs; N4 retains all six arcs
although every capacity is zero. No case becomes an empty original arc list. For N5, keep
gamma and a fixed and separately use constants -7, 0, and 11. Its arcs and C_minus=4 must
remain identical; only the copied constant and recovered objectives change. These two
additional constant variants do not count as extra rows in the eight-list fixture total.

For label independence, construct RICH with metadata `('v0','v1','v2','v3','v4')` and with
`(90,'one',-7,'three',42)`, each alongside its labels=None control. All are distinct valid
labels. Every branch coefficient and network result must be identical to its unlabeled
control. Labels never alter canonical indices, gamma order, or arc endpoints.

---

## ORACLE-049 — All-shore coefficient and routing identities without domain filters

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Authority:** DESIGN 4.7.7, 4.7.11; TEST_PLAN SR7--SR9, SR13.

For every fixed branch row in ORACLE-047, enumerate U=0 through (1<<n)-1. There are
40*(32+16+4)=2080 anchor branch/parameter/shore evaluations. Test the named functions
`test_branch_coefficient_identity` and `test_sign_routing_identity` against definitions,
not against one another's production results.

Independent coefficient side:

1. sum f_v over member vertices for s;
2. count crossing input-edge multiplicity for b;
3. sum input-edge incidences in U for d (an internal edge contributes twice);
4. substitute the source (c_j,h_j) expressions in ORACLE-047;
5. compute B*c_j-A*h_j directly, with no production residual helper.

The production side supplies a,gamma,constant. Require the independent residual to equal
`a*b+sum_U gamma+constant`. Do not use a production degree property or production shore-sum
helper in the expected side. As a second derivation of each fixed coefficient, the constant
is the polynomial residual at U=0, and

`gamma_v = residual({v}) - residual(empty) - B*b_q({v})`.

Independent routing side: derive Psi and C_minus from supplied generic coefficients and
input-edge crossings; count directed crossings in the actual emitted original arc tuple.
Require `cut=Psi+C_minus` and `recover_objective(network,cut)=Psi+constant`.
For branch coefficients the final value must equal the independently computed source
residual. No max-flow/min-cut invocation or shared construction code supplies an expected
answer. The private audit's reference graph is a mathematical verification object, not an
implementation being approved or a fixture learned from production.

U=0 and U=V are included. Cut(empty-source shore)=C_minus;
cut(full-original shore)=sum of positive gamma. Outside D_j, all these residual expressions
are polynomial extensions only. No branch membership, positive h_j, witness, quotient, or
Empty result is asserted. Never send off-domain h_j to a positive-denominator factory.

---

## ORACLE-050 — Separate shift recovery and a restricted-family counterexample

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Authority:** DESIGN 4.7.10--4.7.11; TEST_PLAN SR9.

For a normally constructed network record, recovery subtracts negative_shift and then adds
constant. Scalar control rows (no claim that cut_value is attained by those arbitrary arcs):

<!-- UNIT10:RECOVERY:BEGIN -->
| cut_value | negative_shift | constant | recovered integer |
|---:|---:|---:|---:|
| 0 | 7 | -2 | -9 |
| 10 | 7 | -2 | 1 |
| 0 | 0 | 5 | 5 |
| 4 | 4 | -3 | -3 |
| 6 | 4 | -3 | -1 |
| 0 | 0 | 0 | 0 |
<!-- UNIT10:RECOVERY:END -->

In particular, the valid empty-arc network record of ORACLE-046 with shift 7 and constant -2
returns -9 when cut_value=0. Constructor validity is not a sign-routing certificate, and
recovery does not attempt a provenance/minimality check. Negative recovered values are valid.

For N1 from ORACLE-048, its complete cuts are `[4,6,15,5]` at masks `[0,1,2,3]`.
Its recovered objectives are `[-3,-1,8,-2]`. Fix the nonempty allowed family `{1,2}`:

```text
All masks:       cut minimum=4, unique argmin={0}, objective minimum=-3
Family {1,2}:    cut minimum=6, unique argmin={1}, objective minimum=-1
Shift recovery: 6 - 4 + (-3) = -1
```

This is an arbitrary explicit family allowed by the lemma, not an assertion that it is a
particular generated branch family. It proves why an unrestricted cut minimum cannot replace
a constrained one. Both sides of the minimization identity must use the SAME allowed
family. The cut minima here are obtained by exhaustive table inspection, never a backend.
No Infeasible carrier, empty-family decision, contraction, or parity anchor is introduced.

---

## ORACLE-051 — Exact malformed-input matrix and validation-order boundaries

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Authority:** DESIGN 4.7.3--4.7.5; TEST_PLAN SR2--SR3, SR11.

Every row below expects the exact built-in ValueError class when the prospective public
implementation exists. These are DECLARED pre-code oracle obligations, not executed
production rejection tests. Exception messages are not pinned.

Notation: Coeff means SignRoutingCoefficients; GOOD_COEFF is Coeff(1,(0,0),0), suitable for
EQUALITY. EMPTY_RECORD is SignRoutedNetwork(1,(),7,-2). IntSubclass and TupleSubclass mean
proper subclasses with otherwise valid values. InstanceSubclass, CoeffSubclass, and
NetworkSubclass mean normally initialized proper subclass instances; VerifierInstance is
an object from the independent verifier, not production Instance. Hostile() denotes an
object whose numeric/coercion/iteration/comparison hooks raise if called. Reject its exact
type without invoking those hooks. Do not forge frozen records to bypass constructors.

<!-- UNIT10:REJECTIONS:BEGIN -->
| ID | API | Positional arguments (Python notation) | First failing guard | Exception |
|---|---|---|---|---|
| R01 | `SignRoutingCoefficients` | `(-1, (), 0)` | a: exact int and nonnegative | `ValueError` |
| R02 | `SignRoutingCoefficients` | `(True, (), 0)` | a: exact int and nonnegative | `ValueError` |
| R03 | `SignRoutingCoefficients` | `(IntSubclass(1), (), 0)` | a: exact int and nonnegative | `ValueError` |
| R04 | `SignRoutingCoefficients` | `(0, [1], 0)` | gamma: exact tuple | `ValueError` |
| R05 | `SignRoutingCoefficients` | `(0, TupleSubclass((1,)), 0)` | gamma: exact tuple | `ValueError` |
| R06 | `SignRoutingCoefficients` | `(0, iter((1,)), 0)` | gamma: exact tuple | `ValueError` |
| R07 | `SignRoutingCoefficients` | `(0, (True,), 0)` | gamma entry: exact int | `ValueError` |
| R08 | `SignRoutingCoefficients` | `(0, (IntSubclass(1),), 0)` | gamma entry: exact int | `ValueError` |
| R09 | `SignRoutingCoefficients` | `(0, (1.0,), 0)` | gamma entry: exact int | `ValueError` |
| R10 | `SignRoutingCoefficients` | `(0, (Fraction(1,1),), 0)` | gamma entry: exact int | `ValueError` |
| R11 | `SignRoutingCoefficients` | `(0, (Hostile(),), 0)` | gamma entry: exact int | `ValueError` |
| R12 | `SignRoutingCoefficients` | `(0, (), False)` | constant: exact int | `ValueError` |
| R13 | `SignRoutingCoefficients` | `(0, (), 0.0)` | constant: exact int | `ValueError` |
| R14 | `SignRoutingCoefficients` | `(0, (), Hostile())` | constant: exact int | `ValueError` |
| R15 | `SignRoutedNetwork` | `(0, (), 0, 0)` | vertex_count: exact int >=1 | `ValueError` |
| R16 | `SignRoutedNetwork` | `(True, (), 0, 0)` | vertex_count: exact int >=1 | `ValueError` |
| R17 | `SignRoutedNetwork` | `(IntSubclass(1), (), 0, 0)` | vertex_count: exact int >=1 | `ValueError` |
| R18 | `SignRoutedNetwork` | `(1, [], 0, 0)` | arcs / arc: exact tuple and triple shape | `ValueError` |
| R19 | `SignRoutedNetwork` | `(1, TupleSubclass(()), 0, 0)` | arcs / arc: exact tuple and triple shape | `ValueError` |
| R20 | `SignRoutedNetwork` | `(1, iter(()), 0, 0)` | arcs / arc: exact tuple and triple shape | `ValueError` |
| R21 | `SignRoutedNetwork` | `(1, ([0,1,2],), 0, 0)` | arcs / arc: exact tuple and triple shape | `ValueError` |
| R22 | `SignRoutedNetwork` | `(1, ((0,1),), 0, 0)` | arcs / arc: exact tuple and triple shape | `ValueError` |
| R23 | `SignRoutedNetwork` | `(1, ((0,1,2,3),), 0, 0)` | arcs / arc: exact tuple and triple shape | `ValueError` |
| R24 | `SignRoutedNetwork` | `(1, ((True,1,0),), 0, 0)` | arc fields: exact ints tail then head then capacity | `ValueError` |
| R25 | `SignRoutedNetwork` | `(1, ((0,False,0),), 0, 0)` | arc fields: exact ints tail then head then capacity | `ValueError` |
| R26 | `SignRoutedNetwork` | `(1, ((0,1,True),), 0, 0)` | arc fields: exact ints tail then head then capacity | `ValueError` |
| R27 | `SignRoutedNetwork` | `(1, ((0,1,1.0),), 0, 0)` | arc fields: exact ints tail then head then capacity | `ValueError` |
| R28 | `SignRoutedNetwork` | `(1, ((0,1,Hostile()),), 0, 0)` | arc fields: exact ints tail then head then capacity | `ValueError` |
| R29 | `SignRoutedNetwork` | `(1, ((-1,1,0),), 0, 0)` | endpoint range, loop exclusion, then nonnegative capacity | `ValueError` |
| R30 | `SignRoutedNetwork` | `(1, ((0,3,0),), 0, 0)` | endpoint range, loop exclusion, then nonnegative capacity | `ValueError` |
| R31 | `SignRoutedNetwork` | `(1, ((0,0,0),), 0, 0)` | endpoint range, loop exclusion, then nonnegative capacity | `ValueError` |
| R32 | `SignRoutedNetwork` | `(1, ((0,1,-1),), 0, 0)` | endpoint range, loop exclusion, then nonnegative capacity | `ValueError` |
| R33 | `SignRoutedNetwork` | `(1, (), -1, 0)` | negative_shift: exact int >=0 | `ValueError` |
| R34 | `SignRoutedNetwork` | `(1, (), True, 0)` | negative_shift: exact int >=0 | `ValueError` |
| R35 | `SignRoutedNetwork` | `(1, (), Hostile(), 0)` | negative_shift: exact int >=0 | `ValueError` |
| R36 | `SignRoutedNetwork` | `(1, (), 0, False)` | constant: exact int | `ValueError` |
| R37 | `SignRoutedNetwork` | `(1, (), 0, Fraction(0,1))` | constant: exact int | `ValueError` |
| R38 | `SignRoutedNetwork` | `(1, (), 0, Hostile())` | constant: exact int | `ValueError` |
| R39 | `branch_coefficients` | `(None, 0, (0,1))` | instance: exact production Instance | `ValueError` |
| R40 | `branch_coefficients` | `(InstanceSubclass, 0, (0,1))` | instance: exact production Instance | `ValueError` |
| R41 | `branch_coefficients` | `(VerifierInstance, 0, (0,1))` | instance: exact production Instance | `ValueError` |
| R42 | `branch_coefficients` | `(Hostile(), 0, (0,1))` | instance: exact production Instance | `ValueError` |
| R43 | `build_sign_routed_network` | `(None, GOOD_COEFF)` | instance: exact production Instance | `ValueError` |
| R44 | `build_sign_routed_network` | `(InstanceSubclass, GOOD_COEFF)` | instance: exact production Instance | `ValueError` |
| R45 | `build_sign_routed_network` | `(VerifierInstance, GOOD_COEFF)` | instance: exact production Instance | `ValueError` |
| R46 | `build_sign_routed_network` | `(Hostile(), GOOD_COEFF)` | instance: exact production Instance | `ValueError` |
| R47 | `branch_coefficients` | `(EQUALITY, -1, (0,1))` | branch: exact int in 0..3 | `ValueError` |
| R48 | `branch_coefficients` | `(EQUALITY, 4, (0,1))` | branch: exact int in 0..3 | `ValueError` |
| R49 | `branch_coefficients` | `(EQUALITY, True, (0,1))` | branch: exact int in 0..3 | `ValueError` |
| R50 | `branch_coefficients` | `(EQUALITY, IntSubclass(0), (0,1))` | branch: exact int in 0..3 | `ValueError` |
| R51 | `branch_coefficients` | `(EQUALITY, "0", (0,1))` | branch: exact int in 0..3 | `ValueError` |
| R52 | `branch_coefficients` | `(EQUALITY, Hostile(), (0,1))` | branch: exact int in 0..3 | `ValueError` |
| R53 | `branch_coefficients` | `(EQUALITY, 0, [0,1])` | parameter: closed validate_pair | `ValueError` |
| R54 | `branch_coefficients` | `(EQUALITY, 0, (0,))` | parameter: closed validate_pair | `ValueError` |
| R55 | `branch_coefficients` | `(EQUALITY, 0, (0,1,2))` | parameter: closed validate_pair | `ValueError` |
| R56 | `branch_coefficients` | `(EQUALITY, 0, TupleSubclass((0,1)))` | parameter: closed validate_pair | `ValueError` |
| R57 | `branch_coefficients` | `(EQUALITY, 0, (True,1))` | parameter: closed validate_pair | `ValueError` |
| R58 | `branch_coefficients` | `(EQUALITY, 0, (0,False))` | parameter: closed validate_pair | `ValueError` |
| R59 | `branch_coefficients` | `(EQUALITY, 0, (IntSubclass(0),1))` | parameter: closed validate_pair | `ValueError` |
| R60 | `branch_coefficients` | `(EQUALITY, 0, (0,0))` | parameter: closed validate_pair | `ValueError` |
| R61 | `branch_coefficients` | `(EQUALITY, 0, (0,-1))` | parameter: closed validate_pair | `ValueError` |
| R62 | `branch_coefficients` | `(EQUALITY, 0, (0,1.0))` | parameter: closed validate_pair | `ValueError` |
| R63 | `branch_coefficients` | `(EQUALITY, 0, (Fraction(0,1),1))` | parameter: closed validate_pair | `ValueError` |
| R64 | `branch_coefficients` | `(EQUALITY, 0, iter((0,1)))` | parameter: closed validate_pair | `ValueError` |
| R65 | `branch_coefficients` | `(EQUALITY, 0, ExactValue(0,1))` | parameter: closed validate_pair | `ValueError` |
| R66 | `branch_coefficients` | `(EQUALITY, 0, Hostile())` | parameter: closed validate_pair | `ValueError` |
| R67 | `build_sign_routed_network` | `(EQUALITY, None)` | coefficients: exact SignRoutingCoefficients | `ValueError` |
| R68 | `build_sign_routed_network` | `(EQUALITY, CoeffSubclass)` | coefficients: exact SignRoutingCoefficients | `ValueError` |
| R69 | `build_sign_routed_network` | `(EQUALITY, Hostile())` | coefficients: exact SignRoutingCoefficients | `ValueError` |
| R70 | `build_sign_routed_network` | `(EQUALITY, Coeff(1, (), 0))` | len(gamma) == instance.n | `ValueError` |
| R71 | `build_sign_routed_network` | `(EQUALITY, Coeff(1, (0,), 0))` | len(gamma) == instance.n | `ValueError` |
| R72 | `build_sign_routed_network` | `(EQUALITY, Coeff(1, (0,0,0), 0))` | len(gamma) == instance.n | `ValueError` |
| R73 | `recover_objective` | `(None, 0)` | network: exact SignRoutedNetwork | `ValueError` |
| R74 | `recover_objective` | `(NetworkSubclass, 0)` | network: exact SignRoutedNetwork | `ValueError` |
| R75 | `recover_objective` | `(Hostile(), 0)` | network: exact SignRoutedNetwork | `ValueError` |
| R76 | `recover_objective` | `(EMPTY_RECORD, -1)` | cut_value: exact int >=0 | `ValueError` |
| R77 | `recover_objective` | `(EMPTY_RECORD, True)` | cut_value: exact int >=0 | `ValueError` |
| R78 | `recover_objective` | `(EMPTY_RECORD, IntSubclass(0))` | cut_value: exact int >=0 | `ValueError` |
| R79 | `recover_objective` | `(EMPTY_RECORD, 0.0)` | cut_value: exact int >=0 | `ValueError` |
| R80 | `recover_objective` | `(EMPTY_RECORD, Fraction(0,1))` | cut_value: exact int >=0 | `ValueError` |
| R81 | `recover_objective` | `(EMPTY_RECORD, Hostile())` | cut_value: exact int >=0 | `ValueError` |
<!-- UNIT10:REJECTIONS:END -->

The 81 listed rows are a minimum explicit matrix, not an exhaustive inventory of malformed
Python objects. Applicable scalar/container subclasses and hostile objects should also be
placed at each corresponding boundary in tests. No `isinstance(...,int)` shortcut may accept
bool. Wrong call arity and attempted frozen mutation are deliberately outside this matrix.

Guard order is independently fixed by the authority: coefficient a -> gamma tuple and entries
-> constant; network vertex_count -> entire arcs -> negative_shift -> constant. Inside each
arc: shape -> exact tail/head/capacity types -> endpoint ranges -> no loop -> nonnegative
capacity. branch_coefficients: exact Instance -> branch -> closed validate_pair -> graph
arithmetic. Builder: exact Instance -> exact coefficient record -> gamma length -> arcs.
Recovery: exact network record -> exact nonnegative cut_value -> shift arithmetic.

Guard-isolated rows pass all earlier guards. Source review and hostile-object probes verify
order; it cannot be inferred solely from catching ValueError. Invalid input is never
normalized, sorted, aggregated, coerced, silently discarded, or converted to a feasible one.

---

## ORACLE-052 — Precommitted finite identity corpus and exact counts

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Authority:** DESIGN 4.7.14; TEST_PLAN SR7--SR9, SR13.

### Active-instance corpus

Enumerate n in (2,3). List all unordered vertex pairs in lexicographic order. For each pair,
choose q in (0,1,2), with 0 meaning absent support. Omit graphs with a degree-zero vertex.
For every remaining support, independently choose each f_v from 1 through d_q(v), inclusive.
Store positive edges in pair order. This fixes 5 n=2 instances and 324 n=3 instances, for 329
distinct canonical active instances. Iterate parameter pairs in the ten-row order of
ORACLE-047 and branch j=0,1,2,3. For every combination enumerate all 2^n shores.

There are 2612 base instance/shores, 13160 branch coefficient/network cases, and 104480
branch/parameter/shore evaluations. Each evaluation verifies both the coefficient and cut
identities and shift recovery. It is not reported as three independent corpus members.

### Generic-coefficient corpus

Use EQUALITY (n=2) and TRIANGLE (n=3) from ORACLE-046. Independently choose
`a in (0,2)`, every gamma entry in `(-2,0,3)`, and `constant in (-3,0,5)`.
Thus 2*3*(3^2+3^3)=216 networks and 2*3*(3^2*2^2+3^3*2^3)=1512 all-shore evaluations
cover arbitrary signs, zero-support capacity, all-zero gamma, and constant independence.
These are in addition to, not replacements for, the named branch anchors and literal lists.

<!-- UNIT10:COUNTS:BEGIN -->
| Fixed audit domain/count | Expected |
|---|---:|
| `anchor_branch_records` | 120 |
| `anchor_branch_shore_evaluations` | 2080 |
| `base_shores` | 2612 |
| `branch_records` | 13160 |
| `branch_shore_evaluations` | 104480 |
| `generic_records` | 216 |
| `generic_shore_evaluations` | 1512 |
| `instances` | 329 |
| `literal_network_records` | 8 |
| `literal_network_shores` | 128 |
| `n2_instances` | 5 |
| `n3_instances` | 324 |
| `rejection_declarations` | 81 |
<!-- UNIT10:COUNTS:END -->

Counts bind these finite domains only. They are not a proof of asymptotic performance or a
reason to skip a source hypothesis. Label variants, scalar-shape/recovery checks, constant
twins, and the symbolic/scaling controls below are supplemental and not folded into the
listed branch/generic all-shore totals. The handoff audit recomputes both domains and counts;
future tests must independently check production outputs against these fixed expectations.

---

## ORACLE-053 — Positive scaling and huge signed exact integers

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Authority:** DESIGN 4.7.6, 4.7.9--4.7.13; TEST_PLAN SR10, SR14--SR15.

### Classification-controlled scaling

Use k=2^r for r in (0,1,8,64,4096). On RICH, for EVERY branch compare the fixed
parameter (-3,1) with (-3*k,k). All a,gamma,constant, arc capacities, C_minus, and raw
recovered residuals scale by k. Original endpoints, direction, order, signs and zero
classification remain unchanged. Expected values come from the independent unscaled
oracle row times k, never from an unscaled production result. This gives 20 scaled
branch networks and 640 all-shore evaluations.

Apply componentwise scaling to generic N5 as well: scale a, every gamma entry, and constant.
The same identity gives five scaled generic networks and 80 all-shore evaluations. For all
cases keep source/sink/node count and raw arc length unchanged. This says nothing about
endpoint invariance for arbitrary unrelated parameter changes, which may change signs.

### Huge multiplicities AND raw parameter entries

For L=2^r, r in (1,8,64,4096), use n=2, edge (0,1,L), f=(L,L) and
parameter `(A,B)=(-L,L+1)`. This is an active equality instance. Derive:

```text
All branches: a=L+1; support capacities=L*(L+1); six original arcs.
j=0: gamma=(L*(L+1), L*(L+1)), C_minus=0,  constant=-1
j=1: gamma=(L*(L+1), L*(L+1)), C_minus=0,  constant=-2*(L+1)
j=2: gamma=(-L,-L),           C_minus=2L, constant=-L
j=3: gamma=(-L,-L),           C_minus=2L, constant=-2*(L+1)
```

At r=4096, L and both raw parameter entries have 4097-bit-class magnitude; capacities can
have longer encodings. This tests exact arithmetic and literal preservation, not a maximum
permitted bit length. All four shore masks and all four branches are checked at each L,
for 16 huge branch networks and 64 all-shore evaluations.

For a generic mixed/zero-sign control on TRIANGLE, take
`a=L, gamma=(-L,0,L+3), constant=-(L+7)`. C_minus=L, original arc count=12;
empty-source cut=L and full-original cut=L+3. Every mask is checked for each L, adding
four huge generic networks and 32 evaluations. The zero spoke must remain present.

No float conversion, reduction, numeric cutoff, timing threshold, capacity-sized loop,
explicit unit-copy expansion, or synthetic infinity is introduced by these fixtures.

---

## ORACLE-054 — Determinism, field ownership, and source-inspection controls

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Authority:** DESIGN 4.7.1--4.7.5, 4.7.12--4.7.14; TEST_PLAN SR1--SR3, SR11--SR12, SR15.

Require exact field/slot sequences and properties from ORACLE-046. Repeated identical inputs
produce structurally equal records and identical arc sequences. Hash equality follows record
equality; no cross-process hash identity is promised. Inputs and output tuples are immutable;
no external mutable alias or authoritative duplicated shift/terminal/degree field is added.

Import/export contract is the exact sorted tuple:

```text
("SignRoutedNetwork", "SignRoutingCoefficients", "branch_coefficients",
 "build_sign_routed_network", "recover_objective")
```

Both constructors and the three functions accept the positional and exact keyword names
from DESIGN 4.7.2. No public Arc class, backend flag, coercing adapter, serialization layer,
cut evaluator, or minimizer exists here. The fresh import may load only dataclasses,
Instance, RawPair/validate_pair, their allowed closed dependencies, and optional future
annotations; it must not newly import flow, families, witness, oracle, branch, solve,
certificate, or exactfrac_verify. Package-root exports remain unchanged.

Static/source obligations are not established merely by the numeric tables: reject float
constants/conversion, Fraction/decimal/math/reduction, true/floor division, remainder,
coercion, tolerance, recursion, synthetic infinity, algorithmic set iteration, flow calls,
all-shore production enumeration, and magnitude/bit-length loop bounds. Obtain d_q once
before scanning vertices, not once for each vertex. Constructor validation scans record
lengths; branch coefficients and builder have O(n+m) structural work including record
validation. Recovery and terminal properties are O(1) integer operations on valid records.
None of these claims asserts constant bit cost or wall-clock time.

The closed backend sorts/aggregates its own directed input. Its inclusionwise-minimal
minimum source shore is unique for a fixed ordinary-cut problem. Raw emission order is
specified for reproducible construction, not to create new tie-breaking freedoms. Tests
must not call flow here or assert that input permutations change that extremal source shore.

---

## ORACLE-055 — Coverage ledger and deferred minimization/certificate boundaries

**Classification:** `LOCAL_CONTRACT_FIXTURE`

**Authority:** DESIGN 4.7.14; TEST_PLAN SR16 and Unit 10 completion gate, section 26.

| Prospective TEST_PLAN obligation | Oracle evidence |
|---|---|
| SR1 interface/dependencies | ORACLE-046, ORACLE-054 |
| SR2 coefficient record | ORACLE-046, ORACLE-051 |
| SR3 network record/properties | ORACLE-046, ORACLE-051 |
| SR4 branch coefficients | ORACLE-047 |
| SR5 support arcs/terminals | ORACLE-048 |
| SR6 signed/zero/all-zero spokes | ORACLE-048, ORACLE-052 |
| SR7 coefficient identity | ORACLE-047, ORACLE-049, ORACLE-052 |
| SR8 generic routing identity | ORACLE-048--ORACLE-049, ORACLE-052 |
| SR9 recovery/restricted families | ORACLE-050 |
| SR10 zero/negative/equality | ORACLE-047, ORACLE-053 |
| SR11 rejection/validation order | ORACLE-051, ORACLE-054 |
| SR12 deterministic order/labels | ORACLE-048, ORACLE-054 |
| SR13 precommitted corpus | ORACLE-052 |
| SR14 huge/scaled integers | ORACLE-053 |
| SR15 source and work boundaries | ORACLE-054 |
| SR16 conformance boundary | ORACLE-055 |

The identities hold on every tested shore of the chosen production-domain inputs. No
cut/minimizer, active-set membership, admissible witness, attaining quotient, or optimality
certificate follows merely from constructing a coefficient/network record or shifting an
integer. The same-family minimum correspondence is demonstrated only by explicit finite
shore enumeration; the operational optimizer is deferred.

Unit 10 may promote only the narrowly worded operational-domain lem:sign-routing cut-identity
row at its later implementation GREEN checkpoint, plus a coefficient/representation seam
note. This oracle-only commit does not change any CONFORMANCE row. prop:branch-transform's
ratio claims, parity anchoring/contraction/GR reduction, thm:branch-oracle, branch/global
correctness, telemetry, and algorithm-level bit-growth remain later obligations.

**Unit 10 oracle status:** source/authority-derived and independently audited before the
consuming test or production sign-routing module exists. No production sign-routing output,
minimum-cut solver, or flow result established these expected values.


---

## ORACLE-056 — Unit 11 record boundaries and rejection declarations

**Classification:** `LOCAL_CONTRACT_FIXTURE`; invalid-input rows: `NEGATIVE / REJECTION`.

**Source/authority:** DESIGN 4.8.2--6; TEST_PLAN PC1--PC4, PC9, PC10, PC18--PC19.
The interface and strict Python shapes are engineering rulings. They do not enlarge the
pinned compact-instance mathematical domain or constitute an independent certificate.

All tables below are the committed expected-data authority. The companion JSON is a
private transcription used for independent auditing; it is not embedded here and is not
a dependency permitted in repository tests. The package ledger authenticates identities;
the separate audit compares every literal table with the companion and independently
recomputes numerical expectations. Later tests must carry their own versioned literal
expectations or read these committed tables without accessing private handoff paths.

### Notation and pre-code status

`n` is original nonterminal vertex count, original source is `n`, original sink is `n+1`,
and the optional parity anchor is `n+2`. Problem source and sink are reduced vertices
0 and 1. `classes[v]` is the original preimage of reduced vertex v. A pair query introduces
its own temporary vertices; its returned mask must be lifted back to problem coordinates
before parity is tested. Numeric masks in distinct columns have distinct universes.

An atomic descriptor is `(T, pi, I, O)`. Raw-network `shift` means the existing Unit 10
`negative_shift`, not a new offset. All cut values here sum ORIGINAL directed arcs leaving
a source shore; two opposite original arcs are not two charges for the same crossing.

Record boundaries are expressed as future constructor/function calls. Symbols:

```python
SN = SignRoutedNetwork(1, (), 0, 0)
F = AtomicFamily(1, 1, 0, 0)
P = ParityCutProblem(1, (2, 4, 1), (), 6)
```

`IntSubclass`, `TupleSubclass`, `NetworkSubclass`, `FamilySubclass`, and `ProblemSubclass`
mean proper subclasses of the corresponding closed/new type, constructed with otherwise
valid fields. `Hostile()` is a non-domain object whose conversion, iteration, attribute,
comparison, and arithmetic hooks raise if called. `Fraction` appears only in rejection
inputs on the test side. All `RJ` rows require **type(error) is ValueError** from the new
public boundary. Wrong call arity is not included; normal Python TypeError remains normal.
No Unit 11 public implementation exists at the oracle stage. These rows declare expected
behavior; they are not assertions that the absent production constructors were executed.

All logically earlier constructor guards are satisfied unless the row explicitly tests
precedence. Classes are validated before arcs; arcs before terminal mask. Reduction must
reject out-of-range family masks before interpreting overlap or parity infeasibility.

### Fixture table: VALID_RECORDS

| id | call | assertion |
| --- | --- | --- |
| `'V01'` | `'ParityCutProblem(1,(2,4,1),(),0)'` | `'valid: source=0, sink=1, node_count=3; empty T is not malformed'` |
| `'V02'` | `'ParityCutProblem(1,(10,4,1),(),3)'` | `'valid: anchored source class; no anchor capacity required'` |
| `'V03'` | `'ParityCutProblem(1,(3,4),(),3)'` | `'valid: N=2, original vertex forced inside'` |
| `'V04'` | `'ParityCutProblem(1,(2,5),(),3)'` | `'valid: N=2, original vertex forced outside'` |
| `'V05'` | `'ParityCutProblem(2,(4,8,1,2),((0,2,0),(2,0,0)),12)'` | `'valid: zero capacities remain original records'` |
| `'V06'` | `'ParityCutProblem(1,(2,4,1),((1,0,9),),3)'` | `'valid: asymmetric directed arc'` |
| `'V07'` | `'ParityCutProblem(1,(2,4,1),(),5)'` | `'valid: even T includes source without sink'` |
| `'V08'` | `'ParityCutProblem(1,(2,4,1),(),6)'` | `'valid: even T includes sink without source'` |
| `'V09'` | `'ParityCutResult(0,1)'` | `'valid shape; not an optimality certificate'` |
| `'V10'` | `'ParityCutResult(7,1048577)'` | `'valid shape; without problem no upper-universe check'` |
| `'V11'` | `'ParityCutStats(0,0,0,0)'` | `'valid shape'` |
| `'V12'` | `'ParityCutStats(0,7,9,10)'` | `'valid shape only; arbitrary counters do not certify execution'` |
| `'V13'` | `'lift_source_shore(P,1)'` | `'returns 0 even though reduced T-intersection is even'` |
| `'V14'` | `'lift_source_shore(P,5)'` | `'returns 1; strips reduced source original preimage'` |

### Fixture table: REJECTIONS

| id | phase | call | expected | reason |
| --- | --- | --- | --- | --- |
| `'RJ001'` | `'problem.n'` | `'ParityCutProblem(True, (2,4,1), (), 0)'` | `'ValueError'` | `'n must be exact int >= 1'` |
| `'RJ002'` | `'problem.n'` | `'ParityCutProblem(1.0, (2,4,1), (), 0)'` | `'ValueError'` | `'n must be exact int >= 1'` |
| `'RJ003'` | `'problem.n'` | `'ParityCutProblem(Fraction(1,1), (2,4,1), (), 0)'` | `'ValueError'` | `'n must be exact int >= 1'` |
| `'RJ004'` | `'problem.n'` | `'ParityCutProblem(IntSubclass(1), (2,4,1), (), 0)'` | `'ValueError'` | `'n must be exact int >= 1'` |
| `'RJ005'` | `'problem.n'` | `'ParityCutProblem(0, (2,4,1), (), 0)'` | `'ValueError'` | `'n must be exact int >= 1'` |
| `'RJ006'` | `'problem.n'` | `'ParityCutProblem(-1, (2,4,1), (), 0)'` | `'ValueError'` | `'n must be exact int >= 1'` |
| `'RJ007'` | `'problem.n'` | `'ParityCutProblem(None, (2,4,1), (), 0)'` | `'ValueError'` | `'n must be exact int >= 1'` |
| `'RJ008'` | `'problem.classes'` | `'ParityCutProblem(1, [2,4,1], (), 0)'` | `'ValueError'` | `'outer list'` |
| `'RJ009'` | `'problem.classes'` | `'ParityCutProblem(1, TupleSubclass((2,4,1)), (), 0)'` | `'ValueError'` | `'tuple subclass'` |
| `'RJ010'` | `'problem.classes'` | `'ParityCutProblem(1, iter((2,4,1)), (), 0)'` | `'ValueError'` | `'iterator'` |
| `'RJ011'` | `'problem.classes'` | `'ParityCutProblem(1, (), (), 0)'` | `'ValueError'` | `'too few classes'` |
| `'RJ012'` | `'problem.classes'` | `'ParityCutProblem(1, (7,), (), 0)'` | `'ValueError'` | `'too few classes'` |
| `'RJ013'` | `'problem.classes'` | `'ParityCutProblem(1, (True,4,1), (), 0)'` | `'ValueError'` | `'bool class'` |
| `'RJ014'` | `'problem.classes'` | `'ParityCutProblem(1, (2,4,IntSubclass(1)), (), 0)'` | `'ValueError'` | `'int subclass'` |
| `'RJ015'` | `'problem.classes'` | `'ParityCutProblem(1, (2,4,0), (), 0)'` | `'ValueError'` | `'zero class'` |
| `'RJ016'` | `'problem.classes'` | `'ParityCutProblem(1, (2,4,-1), (), 0)'` | `'ValueError'` | `'negative class'` |
| `'RJ017'` | `'problem.classes'` | `'ParityCutProblem(1, (2,4,1.0), (), 0)'` | `'ValueError'` | `'float class'` |
| `'RJ018'` | `'problem.classes'` | `'ParityCutProblem(1, (2,4,16), (), 0)'` | `'ValueError'` | `'high bit'` |
| `'RJ019'` | `'problem.classes'` | `'ParityCutProblem(1, (1,4,2), (), 0)'` | `'ValueError'` | `'missing source from first class'` |
| `'RJ020'` | `'problem.classes'` | `'ParityCutProblem(1, (6,1), (), 0)'` | `'ValueError'` | `'source class includes sink'` |
| `'RJ021'` | `'problem.classes'` | `'ParityCutProblem(1, (2,5,1), (), 0)'` | `'ValueError'` | `'repeated original member'` |
| `'RJ022'` | `'problem.classes'` | `'ParityCutProblem(1, (2,4), (), 0)'` | `'ValueError'` | `'missing original'` |
| `'RJ023'` | `'problem.classes'` | `'ParityCutProblem(1, (4,2,1), (), 0)'` | `'ValueError'` | `'fixed classes swapped'` |
| `'RJ024'` | `'problem.classes'` | `'ParityCutProblem(1, (2,12,1), (), 0)'` | `'ValueError'` | `'anchor in sink'` |
| `'RJ025'` | `'problem.classes'` | `'ParityCutProblem(1, (2,4,9), (), 0)'` | `'ValueError'` | `'anchor in free class'` |
| `'RJ026'` | `'problem.classes'` | `'ParityCutProblem(1, (10,4,9), (), 0)'` | `'ValueError'` | `'repeated anchor'` |
| `'RJ027'` | `'problem.classes'` | `'ParityCutProblem(2, (4,8,3), (), 0)'` | `'ValueError'` | `'free multi-member class'` |
| `'RJ028'` | `'problem.classes'` | `'ParityCutProblem(2, (4,8,2,1), (), 0)'` | `'ValueError'` | `'free singleton order'` |
| `'RJ029'` | `'problem.classes'` | `'ParityCutProblem(2, (5,8,1,2), (), 0)'` | `'ValueError'` | `'repeated forced original'` |
| `'RJ030'` | `'problem.classes'` | `'ParityCutProblem(2, (4,8,1,1), (), 0)'` | `'ValueError'` | `'duplicate singleton'` |
| `'RJ031'` | `'problem.classes'` | `'ParityCutProblem(2, (4,8,1), (), 0)'` | `'ValueError'` | `'missing second original'` |
| `'RJ032'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), [], 0)'` | `'ValueError'` | `'outer list'` |
| `'RJ033'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), TupleSubclass(()), 0)'` | `'ValueError'` | `'outer tuple subclass'` |
| `'RJ034'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), iter(()), 0)'` | `'ValueError'` | `'outer iterator'` |
| `'RJ035'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ([0,1,0],), 0)'` | `'ValueError'` | `'list arc'` |
| `'RJ036'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), (TupleSubclass((0,1,0)),), 0)'` | `'ValueError'` | `'arc subclass'` |
| `'RJ037'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,1),), 0)'` | `'ValueError'` | `'short arc'` |
| `'RJ038'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,1,0,0),), 0)'` | `'ValueError'` | `'long arc'` |
| `'RJ039'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((True,1,0),), 0)'` | `'ValueError'` | `'bool tail'` |
| `'RJ040'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,False,0),), 0)'` | `'ValueError'` | `'bool head'` |
| `'RJ041'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,1,False),), 0)'` | `'ValueError'` | `'bool capacity'` |
| `'RJ042'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((IntSubclass(0),1,0),), 0)'` | `'ValueError'` | `'tail subclass'` |
| `'RJ043'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,IntSubclass(1),0),), 0)'` | `'ValueError'` | `'head subclass'` |
| `'RJ044'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,1,IntSubclass(0)),), 0)'` | `'ValueError'` | `'capacity subclass'` |
| `'RJ045'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,1,0.0),), 0)'` | `'ValueError'` | `'float capacity'` |
| `'RJ046'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,1,Fraction(0,1)),), 0)'` | `'ValueError'` | `'Fraction capacity'` |
| `'RJ047'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((-1,1,0),), 0)'` | `'ValueError'` | `'negative tail'` |
| `'RJ048'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,-1,0),), 0)'` | `'ValueError'` | `'negative head'` |
| `'RJ049'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((3,1,0),), 0)'` | `'ValueError'` | `'high tail'` |
| `'RJ050'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,3,0),), 0)'` | `'ValueError'` | `'high head'` |
| `'RJ051'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,0,0),), 0)'` | `'ValueError'` | `'loop even if zero'` |
| `'RJ052'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,1,-1),), 0)'` | `'ValueError'` | `'negative capacity'` |
| `'RJ053'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,2,1),(0,1,2)), 0)'` | `'ValueError'` | `'unsorted'` |
| `'RJ054'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,1,0),(0,1,0)), 0)'` | `'ValueError'` | `'duplicate zero pair'` |
| `'RJ055'` | `'problem.arcs'` | `'ParityCutProblem(1, (2,4,1), ((0,1,1),(0,1,2)), 0)'` | `'ValueError'` | `'parallel records'` |
| `'RJ056'` | `'problem.terminal_mask'` | `'ParityCutProblem(1, (2,4,1), (), True)'` | `'ValueError'` | `'terminal must be exact finite mask with even cardinality'` |
| `'RJ057'` | `'problem.terminal_mask'` | `'ParityCutProblem(1, (2,4,1), (), -1)'` | `'ValueError'` | `'terminal must be exact finite mask with even cardinality'` |
| `'RJ058'` | `'problem.terminal_mask'` | `'ParityCutProblem(1, (2,4,1), (), 1.0)'` | `'ValueError'` | `'terminal must be exact finite mask with even cardinality'` |
| `'RJ059'` | `'problem.terminal_mask'` | `'ParityCutProblem(1, (2,4,1), (), Fraction(0,1))'` | `'ValueError'` | `'terminal must be exact finite mask with even cardinality'` |
| `'RJ060'` | `'problem.terminal_mask'` | `'ParityCutProblem(1, (2,4,1), (), IntSubclass(0))'` | `'ValueError'` | `'terminal must be exact finite mask with even cardinality'` |
| `'RJ061'` | `'problem.terminal_mask'` | `'ParityCutProblem(1, (2,4,1), (), 8)'` | `'ValueError'` | `'terminal must be exact finite mask with even cardinality'` |
| `'RJ062'` | `'problem.terminal_mask'` | `'ParityCutProblem(1, (2,4,1), (), 1)'` | `'ValueError'` | `'terminal must be exact finite mask with even cardinality'` |
| `'RJ063'` | `'problem.terminal_mask'` | `'ParityCutProblem(1, (2,4,1), (), None)'` | `'ValueError'` | `'terminal must be exact finite mask with even cardinality'` |
| `'RJ064'` | `'result.cut_value'` | `'ParityCutResult(True,1)'` | `'ValueError'` | `'cut value exact int >= 0'` |
| `'RJ065'` | `'result.cut_value'` | `'ParityCutResult(-1,1)'` | `'ValueError'` | `'cut value exact int >= 0'` |
| `'RJ066'` | `'result.cut_value'` | `'ParityCutResult(1.0,1)'` | `'ValueError'` | `'cut value exact int >= 0'` |
| `'RJ067'` | `'result.cut_value'` | `'ParityCutResult(Fraction(0,1),1)'` | `'ValueError'` | `'cut value exact int >= 0'` |
| `'RJ068'` | `'result.cut_value'` | `'ParityCutResult(IntSubclass(0),1)'` | `'ValueError'` | `'cut value exact int >= 0'` |
| `'RJ069'` | `'result.cut_value'` | `'ParityCutResult(None,1)'` | `'ValueError'` | `'cut value exact int >= 0'` |
| `'RJ070'` | `'result.source_shore'` | `'ParityCutResult(0,False)'` | `'ValueError'` | `'exact nonnegative mask, source present and sink absent'` |
| `'RJ071'` | `'result.source_shore'` | `'ParityCutResult(0,-1)'` | `'ValueError'` | `'exact nonnegative mask, source present and sink absent'` |
| `'RJ072'` | `'result.source_shore'` | `'ParityCutResult(0,1.0)'` | `'ValueError'` | `'exact nonnegative mask, source present and sink absent'` |
| `'RJ073'` | `'result.source_shore'` | `'ParityCutResult(0,IntSubclass(1))'` | `'ValueError'` | `'exact nonnegative mask, source present and sink absent'` |
| `'RJ074'` | `'result.source_shore'` | `'ParityCutResult(0,0)'` | `'ValueError'` | `'exact nonnegative mask, source present and sink absent'` |
| `'RJ075'` | `'result.source_shore'` | `'ParityCutResult(0,2)'` | `'ValueError'` | `'exact nonnegative mask, source present and sink absent'` |
| `'RJ076'` | `'result.source_shore'` | `'ParityCutResult(0,3)'` | `'ValueError'` | `'exact nonnegative mask, source present and sink absent'` |
| `'RJ077'` | `'result.source_shore'` | `'ParityCutResult(0,6)'` | `'ValueError'` | `'exact nonnegative mask, source present and sink absent'` |
| `'RJ078'` | `'result.source_shore'` | `'ParityCutResult(0,None)'` | `'ValueError'` | `'exact nonnegative mask, source present and sink absent'` |
| `'RJ079'` | `'stats.mincut_calls'` | `'ParityCutStats(False,0,0,0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ080'` | `'stats.mincut_calls'` | `'ParityCutStats(-1,0,0,0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ081'` | `'stats.mincut_calls'` | `'ParityCutStats(1.0,0,0,0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ082'` | `'stats.mincut_calls'` | `'ParityCutStats(IntSubclass(0),0,0,0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ083'` | `'stats.flow_augmentations'` | `'ParityCutStats(0,False,0,0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ084'` | `'stats.flow_augmentations'` | `'ParityCutStats(0,-1,0,0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ085'` | `'stats.flow_augmentations'` | `'ParityCutStats(0,1.0,0,0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ086'` | `'stats.flow_augmentations'` | `'ParityCutStats(0,IntSubclass(0),0,0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ087'` | `'stats.flow_bfs_scans'` | `'ParityCutStats(0,0,False,0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ088'` | `'stats.flow_bfs_scans'` | `'ParityCutStats(0,0,-1,0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ089'` | `'stats.flow_bfs_scans'` | `'ParityCutStats(0,0,1.0,0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ090'` | `'stats.flow_bfs_scans'` | `'ParityCutStats(0,0,IntSubclass(0),0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ091'` | `'stats.flow_peak_generated_value'` | `'ParityCutStats(0,0,0,False)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ092'` | `'stats.flow_peak_generated_value'` | `'ParityCutStats(0,0,0,-1)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ093'` | `'stats.flow_peak_generated_value'` | `'ParityCutStats(0,0,0,1.0)'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ094'` | `'stats.flow_peak_generated_value'` | `'ParityCutStats(0,0,0,IntSubclass(0))'` | `'ValueError'` | `'field exact int >= 0 in declaration order'` |
| `'RJ095'` | `'reduce.boundary'` | `'reduce_atomic_family(None,F)'` | `'ValueError'` | `'wrong network'` |
| `'RJ096'` | `'reduce.boundary'` | `'reduce_atomic_family(Hostile(),F)'` | `'ValueError'` | `'hostile network'` |
| `'RJ097'` | `'reduce.boundary'` | `'reduce_atomic_family(NetworkSubclass(1,(),0,0),F)'` | `'ValueError'` | `'network subclass'` |
| `'RJ098'` | `'reduce.boundary'` | `'reduce_atomic_family(SN,None)'` | `'ValueError'` | `'wrong family'` |
| `'RJ099'` | `'reduce.boundary'` | `'reduce_atomic_family(SN,Hostile())'` | `'ValueError'` | `'hostile family'` |
| `'RJ100'` | `'reduce.boundary'` | `'reduce_atomic_family(SN,FamilySubclass(1,1,0,0))'` | `'ValueError'` | `'family subclass'` |
| `'RJ101'` | `'reduce.boundary'` | `'reduce_atomic_family(SN,AtomicFamily(2,1,0,0))'` | `'ValueError'` | `'T high bit'` |
| `'RJ102'` | `'reduce.boundary'` | `'reduce_atomic_family(SN,AtomicFamily(0,0,2,0))'` | `'ValueError'` | `'I high bit'` |
| `'RJ103'` | `'reduce.boundary'` | `'reduce_atomic_family(SN,AtomicFamily(0,0,0,2))'` | `'ValueError'` | `'O high bit'` |
| `'RJ104'` | `'reduce.boundary'` | `'reduce_atomic_family(SN,AtomicFamily(2,0,1,1))'` | `'ValueError'` | `'T range before overlap infeasibility'` |
| `'RJ105'` | `'reduce.boundary'` | `'reduce_atomic_family(SN,AtomicFamily(0,1,2,0))'` | `'ValueError'` | `'I range before parity infeasibility'` |
| `'RJ106'` | `'reduce.boundary'` | `'reduce_atomic_family(SN,AtomicFamily(0,1,0,2))'` | `'ValueError'` | `'O range before parity infeasibility'` |
| `'RJ107'` | `'consumer.problem_type'` | `'lift_source_shore(None,1)'` | `'ValueError'` | `'wrong problem'` |
| `'RJ108'` | `'consumer.problem_type'` | `'lift_source_shore(Hostile(),1)'` | `'ValueError'` | `'hostile problem'` |
| `'RJ109'` | `'consumer.problem_type'` | `'minimum_parity_cut(None)'` | `'ValueError'` | `'wrong problem'` |
| `'RJ110'` | `'consumer.problem_type'` | `'minimum_parity_cut(Hostile())'` | `'ValueError'` | `'hostile problem'` |
| `'RJ111'` | `'consumer.problem_type'` | `'minimum_parity_cut(ProblemSubclass(1,(2,4,1),(),6))'` | `'ValueError'` | `'problem subclass'` |
| `'RJ112'` | `'lift.mask'` | `'lift_source_shore(P,True)'` | `'ValueError'` | `'strict finite reduced source/sink shore'` |
| `'RJ113'` | `'lift.mask'` | `'lift_source_shore(P,-1)'` | `'ValueError'` | `'strict finite reduced source/sink shore'` |
| `'RJ114'` | `'lift.mask'` | `'lift_source_shore(P,1.0)'` | `'ValueError'` | `'strict finite reduced source/sink shore'` |
| `'RJ115'` | `'lift.mask'` | `'lift_source_shore(P,IntSubclass(1))'` | `'ValueError'` | `'strict finite reduced source/sink shore'` |
| `'RJ116'` | `'lift.mask'` | `'lift_source_shore(P,8)'` | `'ValueError'` | `'strict finite reduced source/sink shore'` |
| `'RJ117'` | `'lift.mask'` | `'lift_source_shore(P,9)'` | `'ValueError'` | `'strict finite reduced source/sink shore'` |
| `'RJ118'` | `'lift.mask'` | `'lift_source_shore(P,0)'` | `'ValueError'` | `'strict finite reduced source/sink shore'` |
| `'RJ119'` | `'lift.mask'` | `'lift_source_shore(P,2)'` | `'ValueError'` | `'strict finite reduced source/sink shore'` |
| `'RJ120'` | `'lift.mask'` | `'lift_source_shore(P,3)'` | `'ValueError'` | `'strict finite reduced source/sink shore'` |
| `'RJ121'` | `'lift.mask'` | `'lift_source_shore(P,7)'` | `'ValueError'` | `'strict finite reduced source/sink shore'` |
| `'RJ122'` | `'lift.mask'` | `'lift_source_shore(P,Hostile())'` | `'ValueError'` | `'strict finite reduced source/sink shore'` |


## ORACLE-057 — Fixed forced contractions, loops, parallel arcs, and retained zeros

**Classification:** `LOCAL_CONTRACT_FIXTURE`; well-formed impossible families:
`NEGATIVE / REJECTION` with returned None rather than an exception.

**Source:** forced-contraction paragraph following `lem:sign-routing`; `lem:parity-anchor`.
**Engineering authority:** DESIGN 4.8.6--9; TEST_PLAN PC2--PC8.

The raw networks are valid standalone SignRoutedNetwork records. They need not arise from
an active Instance: n=1, empty arcs, arbitrary nonnegative directed arcs, repeated ordered
pairs, unsorted records, and zero capacities are legitimate standalone inputs. No density
or global-solver conclusion is attached to them. D2 reuses the six-arc shape of Unit 10's
N1 fixture. D3 intentionally contains repeated arcs, arcs becoming loops, and zero pairs.
D4 retains explicit zero positions; D5 and D6 have no arcs.

### Fixture table: RAW_NETWORKS

| id | n | arcs | shift | constant |
| --- | --- | --- | --- | --- |
| `'D1'` | `1` | `()` | `0` | `0` |
| `'D2'` | `2` | `((0, 1, 6), (1, 0, 6), (2, 0, 4), (0, 2, 4), (1, 3, 5), (3, 1, 5))` | `4` | `-3` |
| `'D3'` | `3` | `((3, 0, 2), (3, 0, 1), (0, 3, 4), (0, 1, 5), (3, 1, 7), (1, 4, 6), (1, 2, 1), (2, 4, 8), (4, 2, 9), (0, 2, 0), (3, 2, 0), (2, 0, 0), (1, 0, 3))` | `5` | `-2` |
| `'D4'` | `4` | `((0, 1, 0), (1, 0, 0), (2, 3, 0), (3, 2, 0), (4, 0, 0), (0, 4, 0), (1, 5, 0), (5, 1, 0))` | `7` | `-2` |
| `'D5'` | `4` | `()` | `0` | `0` |
| `'D6'` | `3` | `()` | `0` | `0` |


For every feasible row, source class is I plus original source and, exactly when pi=0,
the anchor. Sink class is O plus original sink. Free originals are singleton classes in
increasing order. Each raw arc is mapped; mapped loops disappear; equal ordered pairs
are summed. Encountered zero-sum pairs remain. No other pair is invented.

`before_toggle` is recorded for independent verification of token transport, not a
proposed new production field. `terminal_mask` is the final even mask. Infeasible rows
have None in every constructed-problem field and an empty feasible_original tuple.
The constructor is never used to disguise logical infeasibility as an empty valid graph.

### Fixture table: REDUCTIONS

| id | network | family | classes | arcs | before_toggle | terminal_mask | feasible_original |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `'C01'` | `'D1'` | `(0, 0, 0, 0)` | `(10, 4, 1)` | `()` | `1` | `3` | `(0, 1)` |
| `'C02'` | `'D1'` | `(1, 1, 0, 0)` | `(2, 4, 1)` | `()` | `4` | `6` | `(1,)` |
| `'C03'` | `'D1'` | `(1, 0, 0, 0)` | `(10, 4, 1)` | `()` | `5` | `5` | `(0,)` |
| `'C04'` | `'D1'` | `(1, 1, 1, 0)` | `(3, 4)` | `()` | `1` | `3` | `(1,)` |
| `'C05'` | `'D1'` | `(1, 0, 0, 1)` | `(10, 5)` | `()` | `3` | `3` | `(0,)` |
| `'C06'` | `'D1'` | `(1, 0, 1, 0)` | `None` | `None` | `None` | `None` | `()` |
| `'C07'` | `'D1'` | `(1, 1, 1, 1)` | `None` | `None` | `None` | `None` | `()` |
| `'C08'` | `'D2'` | `(3, 1, 0, 0)` | `(4, 8, 1, 2)` | `((0, 2, 4), (1, 3, 5), (2, 0, 4), (2, 3, 6), (3, 1, 5), (3, 2, 6))` | `12` | `12` | `(1, 2)` |
| `'C09'` | `'D2'` | `(3, 0, 0, 0)` | `(20, 8, 1, 2)` | `((0, 2, 4), (1, 3, 5), (2, 0, 4), (2, 3, 6), (3, 1, 5), (3, 2, 6))` | `13` | `15` | `(0, 3)` |
| `'C10'` | `'D2'` | `(1, 1, 1, 0)` | `(5, 8, 2)` | `((0, 2, 6), (1, 2, 5), (2, 0, 6), (2, 1, 5))` | `1` | `3` | `(1, 3)` |
| `'C11'` | `'D2'` | `(2, 1, 0, 1)` | `(4, 9, 2)` | `((0, 1, 4), (1, 0, 4), (1, 2, 11), (2, 1, 11))` | `4` | `6` | `(2,)` |
| `'C12'` | `'D2'` | `(3, 0, 1, 2)` | `None` | `None` | `None` | `None` | `()` |
| `'C13'` | `'D2'` | `(3, 1, 1, 2)` | `(5, 10)` | `((0, 1, 6), (1, 0, 6))` | `3` | `3` | `(1,)` |
| `'C14'` | `'D3'` | `(3, 1, 1, 4)` | `(9, 20, 2)` | `((0, 1, 0), (0, 2, 12), (1, 0, 0), (2, 0, 3), (2, 1, 7))` | `5` | `5` | `(1,)` |
| `'C15'` | `'D3'` | `(3, 0, 1, 4)` | `(41, 20, 2)` | `((0, 1, 0), (0, 2, 12), (1, 0, 0), (2, 0, 3), (2, 1, 7))` | `4` | `6` | `(3,)` |
| `'C16'` | `'D3'` | `(7, 1, 3, 4)` | `None` | `None` | `None` | `None` | `()` |
| `'C17'` | `'D3'` | `(3, 0, 3, 4)` | `(43, 20)` | `((0, 1, 7), (1, 0, 0))` | `1` | `3` | `(3,)` |
| `'C18'` | `'D3'` | `(7, 0, 3, 0)` | `(43, 16, 4)` | `((0, 1, 6), (0, 2, 1), (1, 2, 9), (2, 0, 0), (2, 1, 8))` | `5` | `5` | `(3,)` |
| `'C19'` | `'D3'` | `(7, 1, 0, 6)` | `(8, 22, 1)` | `((0, 1, 7), (0, 2, 3), (1, 2, 3), (2, 0, 4), (2, 1, 5))` | `4` | `6` | `(1,)` |
| `'C20'` | `'D4'` | `(15, 0, 3, 8)` | `(83, 40, 4)` | `((0, 1, 0), (1, 0, 0), (1, 2, 0), (2, 1, 0))` | `7` | `5` | `(3,)` |
| `'C21'` | `'D4'` | `(15, 1, 7, 8)` | `(23, 40)` | `((0, 1, 0), (1, 0, 0))` | `3` | `3` | `(7,)` |
| `'C22'` | `'D5'` | `(0, 0, 0, 0)` | `(80, 32, 1, 2, 4, 8)` | `()` | `1` | `3` | `(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)` |
| `'C23'` | `'D5'` | `(0, 1, 0, 0)` | `None` | `None` | `None` | `None` | `()` |
| `'C24'` | `'D3'` | `(7, 1, 0, 0)` | `(8, 16, 1, 2, 4)` | `((0, 2, 3), (0, 3, 7), (0, 4, 0), (1, 4, 9), (2, 0, 4), (2, 3, 5), (2, 4, 0), (3, 1, 6), (3, 2, 3), (3, 4, 1), (4, 1, 8), (4, 2, 0))` | `28` | `30` | `(1, 2, 4, 7)` |
| `'C25'` | `'D3'` | `(7, 0, 0, 0)` | `(40, 16, 1, 2, 4)` | `((0, 2, 3), (0, 3, 7), (0, 4, 0), (1, 4, 9), (2, 0, 4), (2, 3, 5), (2, 4, 0), (3, 1, 6), (3, 2, 3), (3, 4, 1), (4, 1, 8), (4, 2, 0))` | `29` | `29` | `(0, 3, 5, 6)` |
| `'C26'` | `'D3'` | `(7, 1, 7, 0)` | `(15, 16)` | `((0, 1, 14), (1, 0, 9))` | `1` | `3` | `(7,)` |
| `'C27'` | `'D3'` | `(7, 0, 7, 0)` | `None` | `None` | `None` | `None` | `()` |
| `'C28'` | `'D3'` | `(7, 0, 0, 7)` | `(40, 23)` | `((0, 1, 10), (1, 0, 4))` | `3` | `3` | `(0,)` |
| `'C29'` | `'D3'` | `(7, 1, 0, 7)` | `None` | `None` | `None` | `None` | `()` |


### Hand derivation: C14 and C15

D3 has original source 3 and sink 4. C14 forces original 0 inside and 2 outside, so its
classes are `(9,20,2)`, representing `{3,0}`, `{4,2}`, and `{1}`. The raw arcs 3->0,
0->3, 2->4, and 4->2 become loops. Raw 0->1 of capacity 5 and 3->1 of capacity 7 aggregate
to reduced 0->2 of capacity 12. Raw 1->4 of capacity 6 and 1->2 of capacity 1 aggregate
to reduced 2->1 of capacity 7. Reduced 2->0 retains capacity 3; encountered 0->1 and
1->0 remain at capacity zero. Thus the exact reduced tuple is:

```text
((0,1,0), (0,2,12), (1,0,0), (2,0,3), (2,1,7))
```

C15 differs only by even required parity: anchor bit 5 is added to the source preimage,
changing classes[0] from 9 to 41. No edge is added. Capacities are identical. The source's
original terminal token and anchor cancel, leaving raw reduced T=4; the sink toggle adds
bit 1 and yields final T=6. For C14, raw and final T are both 5.

Reversing raw arc order or splitting every capacity c into two same-pair records
`c//2` and `c-c//2` must produce the same canonical contracted tuple. Such division is
only a test-data decomposition here, not a production arithmetic requirement.

## ORACLE-058 — Anchor tokens, XOR cancellation, and sink-toggle removal

**Classification:** `LOCAL_CONTRACT_FIXTURE`.
**Source/authority:** `lem:parity-anchor`; DESIGN 4.8.7--9; TEST_PLAN PC6--PC7.

The exact masks are fixed in the REDUCTIONS table; this entry states why selected rows
protect the essential signs and parities.

C01 has no original terminals and pi=0. Its anchor creates a source token, raw T=1, and
toggling sink makes final T=3. Both original shores are allowed. C23 has no terminals
and pi=1 and is infeasible; capacity zero does not change this distinction.

C17 has two original terminal tokens forced inside. They cancel; its extra anchor leaves
one source token. C19 has two terminal tokens forced outside; they cancel in the sink
class. C21 and C26 force three original terminal tokens inside, leaving one source token.
C28 has three terminal tokens in the sink class and one anchor in source, raw T=3;
its total is already even and neither token changes.

C20 is the removal case. Its source preimage `(83)` contains original tokens 0 and 1 plus
the anchor, hence one reduced token. Sink preimage `(40)` contains original token 3,
and free vertex 2 is a token. Raw reduced T=7 is odd; toggling the existing sink token
REMOVES bit 1, producing T=5. Replacing XOR with OR incorrectly leaves 7.

For any reduced source/sink shore X the sink is absent. Therefore toggling sink changes
`bit_count(T) mod 2` but never changes `bit_count(X & T) mod 2`. Source tokens are retained,
not discarded as if they were sink tokens. Two tokens in a class cancel; three do not.

## ORACLE-059 — Complete lifting, parity, and cut-value correspondence

**Classification:** `LOCAL_CONTRACT_FIXTURE`.
**Source/authority:** `lem:parity-anchor`; DESIGN 4.8.7--10; TEST_PLAN PC8--PC9.

Every geometrically valid reduced source shore is listed for each of the 22 feasible
fixed contractions, including shores with EVEN terminal intersection. `odd` is 0 or 1,
not a demand that generic lifting reject even shores. `original` is the preimage union
intersected with `(1<<n)-1`; all source/sink/anchor bits are removed.

`cut_value` equals the original raw-network cut of `{original source} union original`.
`recovered` uses the original raw network's shift and constant. Contraction itself adds
no shift. Odd rows correspond bijectively to feasible_original in the REDUCTIONS table.

### Fixture table: LIFT_AND_CAPACITY

| id | reduction | reduced | original | cut_value | odd | recovered |
| --- | --- | --- | --- | --- | --- | --- |
| `'C01-1'` | `'C01'` | `1` | `0` | `0` | `1` | `0` |
| `'C01-5'` | `'C01'` | `5` | `1` | `0` | `1` | `0` |
| `'C02-1'` | `'C02'` | `1` | `0` | `0` | `0` | `0` |
| `'C02-5'` | `'C02'` | `5` | `1` | `0` | `1` | `0` |
| `'C03-1'` | `'C03'` | `1` | `0` | `0` | `1` | `0` |
| `'C03-5'` | `'C03'` | `5` | `1` | `0` | `0` | `0` |
| `'C04-1'` | `'C04'` | `1` | `1` | `0` | `1` | `0` |
| `'C05-1'` | `'C05'` | `1` | `0` | `0` | `1` | `0` |
| `'C08-1'` | `'C08'` | `1` | `0` | `4` | `0` | `-3` |
| `'C08-5'` | `'C08'` | `5` | `1` | `6` | `1` | `-1` |
| `'C08-9'` | `'C08'` | `9` | `2` | `15` | `1` | `8` |
| `'C08-13'` | `'C08'` | `13` | `3` | `5` | `0` | `-2` |
| `'C09-1'` | `'C09'` | `1` | `0` | `4` | `1` | `-3` |
| `'C09-5'` | `'C09'` | `5` | `1` | `6` | `0` | `-1` |
| `'C09-9'` | `'C09'` | `9` | `2` | `15` | `0` | `8` |
| `'C09-13'` | `'C09'` | `13` | `3` | `5` | `1` | `-2` |
| `'C10-1'` | `'C10'` | `1` | `1` | `6` | `1` | `-1` |
| `'C10-5'` | `'C10'` | `5` | `3` | `5` | `1` | `-2` |
| `'C11-1'` | `'C11'` | `1` | `0` | `4` | `0` | `-3` |
| `'C11-5'` | `'C11'` | `5` | `2` | `15` | `1` | `8` |
| `'C13-1'` | `'C13'` | `1` | `1` | `6` | `1` | `-1` |
| `'C14-1'` | `'C14'` | `1` | `1` | `12` | `1` | `5` |
| `'C14-5'` | `'C14'` | `5` | `3` | `7` | `0` | `0` |
| `'C15-1'` | `'C15'` | `1` | `1` | `12` | `0` | `5` |
| `'C15-5'` | `'C15'` | `5` | `3` | `7` | `1` | `0` |
| `'C17-1'` | `'C17'` | `1` | `3` | `7` | `1` | `0` |
| `'C18-1'` | `'C18'` | `1` | `3` | `7` | `1` | `0` |
| `'C18-5'` | `'C18'` | `5` | `7` | `14` | `0` | `7` |
| `'C19-1'` | `'C19'` | `1` | `0` | `10` | `0` | `3` |
| `'C19-5'` | `'C19'` | `5` | `1` | `12` | `1` | `5` |
| `'C20-1'` | `'C20'` | `1` | `3` | `0` | `1` | `-9` |
| `'C20-5'` | `'C20'` | `5` | `7` | `0` | `0` | `-9` |
| `'C21-1'` | `'C21'` | `1` | `7` | `0` | `1` | `-9` |
| `'C22-1'` | `'C22'` | `1` | `0` | `0` | `1` | `0` |
| `'C22-5'` | `'C22'` | `5` | `1` | `0` | `1` | `0` |
| `'C22-9'` | `'C22'` | `9` | `2` | `0` | `1` | `0` |
| `'C22-13'` | `'C22'` | `13` | `3` | `0` | `1` | `0` |
| `'C22-17'` | `'C22'` | `17` | `4` | `0` | `1` | `0` |
| `'C22-21'` | `'C22'` | `21` | `5` | `0` | `1` | `0` |
| `'C22-25'` | `'C22'` | `25` | `6` | `0` | `1` | `0` |
| `'C22-29'` | `'C22'` | `29` | `7` | `0` | `1` | `0` |
| `'C22-33'` | `'C22'` | `33` | `8` | `0` | `1` | `0` |
| `'C22-37'` | `'C22'` | `37` | `9` | `0` | `1` | `0` |
| `'C22-41'` | `'C22'` | `41` | `10` | `0` | `1` | `0` |
| `'C22-45'` | `'C22'` | `45` | `11` | `0` | `1` | `0` |
| `'C22-49'` | `'C22'` | `49` | `12` | `0` | `1` | `0` |
| `'C22-53'` | `'C22'` | `53` | `13` | `0` | `1` | `0` |
| `'C22-57'` | `'C22'` | `57` | `14` | `0` | `1` | `0` |
| `'C22-61'` | `'C22'` | `61` | `15` | `0` | `1` | `0` |
| `'C24-1'` | `'C24'` | `1` | `0` | `10` | `0` | `3` |
| `'C24-5'` | `'C24'` | `5` | `1` | `12` | `1` | `5` |
| `'C24-9'` | `'C24'` | `9` | `2` | `13` | `1` | `6` |
| `'C24-13'` | `'C24'` | `13` | `3` | `7` | `0` | `0` |
| `'C24-17'` | `'C24'` | `17` | `4` | `18` | `1` | `11` |
| `'C24-21'` | `'C24'` | `21` | `5` | `20` | `0` | `13` |
| `'C24-25'` | `'C24'` | `25` | `6` | `20` | `0` | `13` |
| `'C24-29'` | `'C24'` | `29` | `7` | `14` | `1` | `7` |
| `'C25-1'` | `'C25'` | `1` | `0` | `10` | `1` | `3` |
| `'C25-5'` | `'C25'` | `5` | `1` | `12` | `0` | `5` |
| `'C25-9'` | `'C25'` | `9` | `2` | `13` | `0` | `6` |
| `'C25-13'` | `'C25'` | `13` | `3` | `7` | `1` | `0` |
| `'C25-17'` | `'C25'` | `17` | `4` | `18` | `0` | `11` |
| `'C25-21'` | `'C25'` | `21` | `5` | `20` | `1` | `13` |
| `'C25-25'` | `'C25'` | `25` | `6` | `20` | `1` | `13` |
| `'C25-29'` | `'C25'` | `29` | `7` | `14` | `0` | `7` |
| `'C26-1'` | `'C26'` | `1` | `7` | `14` | `1` | `7` |
| `'C28-1'` | `'C28'` | `1` | `0` | `10` | `1` | `3` |


## ORACLE-060 — Standalone parity problems and exact minimum shores

**Classification:** `LOCAL_CONTRACT_FIXTURE`; T=0 cases: `NEGATIVE / REJECTION` (None).
**Source/authority:** `thm:GR`; DESIGN 4.8.3--5, 4.8.11--13; TEST_PLAN PC3, PC10, PC13--PC16.

These are canonical, possibly asymmetric directed problem records. All arcs are sorted
by ordered endpoints; all terminal masks have even cardinality, including zero. `n` is
not N: N is len(classes). In P02--P05 all original vertices have already been forced,
so n=1 and N=2. P11 explicitly retains an anchor in the source preimage.

### Fixture table: PROBLEMS

| id | n | classes | arcs | terminal_mask |
| --- | --- | --- | --- | --- |
| `'P01'` | `1` | `(3, 4)` | `()` | `0` |
| `'P02'` | `1` | `(3, 4)` | `()` | `3` |
| `'P03'` | `1` | `(3, 4)` | `((0, 1, 5),)` | `3` |
| `'P04'` | `1` | `(3, 4)` | `((0, 1, 5), (1, 0, 2))` | `3` |
| `'P05'` | `1` | `(3, 4)` | `((0, 1, 0), (1, 0, 0))` | `3` |
| `'P06'` | `1` | `(2, 4, 1)` | `((0, 2, 2), (2, 1, 3))` | `6` |
| `'P07'` | `1` | `(2, 4, 1)` | `((0, 2, 2), (2, 1, 3))` | `5` |
| `'P08'` | `2` | `(4, 8, 1, 2)` | `((0, 2, 3), (0, 3, 1), (2, 1, 4), (2, 3, 2), (3, 1, 6))` | `12` |
| `'P09'` | `2` | `(4, 8, 1, 2)` | `()` | `12` |
| `'P10'` | `2` | `(4, 8, 1, 2)` | `((0, 2, 0), (2, 0, 0), (2, 3, 0), (3, 2, 0))` | `9` |
| `'P11'` | `2` | `(20, 8, 1, 2)` | `((0, 2, 1), (1, 3, 2), (2, 0, 1), (2, 3, 3), (3, 1, 2), (3, 2, 3))` | `15` |
| `'P12'` | `4` | `(16, 32, 1, 2, 4, 8)` | `()` | `60` |
| `'P13'` | `1` | `(2, 4, 1)` | `((0, 1, 7), (1, 0, 9))` | `0` |
| `'P14'` | `3` | `(8, 16, 1, 2, 4)` | `((0, 2, 4), (2, 0, 4), (2, 3, 1), (3, 2, 1), (3, 4, 3), (4, 3, 3))` | `20` |


Every geometrically valid problem source shore is enumerated below. Rows with odd=1
are the feasible parity cuts; no production minimum-cut output establishes these values.

### Fixture table: PROBLEM_SHORES

| id | problem | shore | capacity | odd |
| --- | --- | --- | --- | --- |
| `'P01-1'` | `'P01'` | `1` | `0` | `0` |
| `'P02-1'` | `'P02'` | `1` | `0` | `1` |
| `'P03-1'` | `'P03'` | `1` | `5` | `1` |
| `'P04-1'` | `'P04'` | `1` | `5` | `1` |
| `'P05-1'` | `'P05'` | `1` | `0` | `1` |
| `'P06-1'` | `'P06'` | `1` | `2` | `0` |
| `'P06-5'` | `'P06'` | `5` | `3` | `1` |
| `'P07-1'` | `'P07'` | `1` | `2` | `1` |
| `'P07-5'` | `'P07'` | `5` | `3` | `0` |
| `'P08-1'` | `'P08'` | `1` | `4` | `0` |
| `'P08-5'` | `'P08'` | `5` | `7` | `1` |
| `'P08-9'` | `'P08'` | `9` | `9` | `1` |
| `'P08-13'` | `'P08'` | `13` | `10` | `0` |
| `'P09-1'` | `'P09'` | `1` | `0` | `0` |
| `'P09-5'` | `'P09'` | `5` | `0` | `1` |
| `'P09-9'` | `'P09'` | `9` | `0` | `1` |
| `'P09-13'` | `'P09'` | `13` | `0` | `0` |
| `'P10-1'` | `'P10'` | `1` | `0` | `1` |
| `'P10-5'` | `'P10'` | `5` | `0` | `1` |
| `'P10-9'` | `'P10'` | `9` | `0` | `0` |
| `'P10-13'` | `'P10'` | `13` | `0` | `0` |
| `'P11-1'` | `'P11'` | `1` | `1` | `1` |
| `'P11-5'` | `'P11'` | `5` | `3` | `0` |
| `'P11-9'` | `'P11'` | `9` | `6` | `0` |
| `'P11-13'` | `'P11'` | `13` | `2` | `1` |
| `'P12-1'` | `'P12'` | `1` | `0` | `0` |
| `'P12-5'` | `'P12'` | `5` | `0` | `1` |
| `'P12-9'` | `'P12'` | `9` | `0` | `1` |
| `'P12-13'` | `'P12'` | `13` | `0` | `0` |
| `'P12-17'` | `'P12'` | `17` | `0` | `1` |
| `'P12-21'` | `'P12'` | `21` | `0` | `0` |
| `'P12-25'` | `'P12'` | `25` | `0` | `0` |
| `'P12-29'` | `'P12'` | `29` | `0` | `1` |
| `'P12-33'` | `'P12'` | `33` | `0` | `1` |
| `'P12-37'` | `'P12'` | `37` | `0` | `0` |
| `'P12-41'` | `'P12'` | `41` | `0` | `0` |
| `'P12-45'` | `'P12'` | `45` | `0` | `1` |
| `'P12-49'` | `'P12'` | `49` | `0` | `0` |
| `'P12-53'` | `'P12'` | `53` | `0` | `1` |
| `'P12-57'` | `'P12'` | `57` | `0` | `1` |
| `'P12-61'` | `'P12'` | `61` | `0` | `0` |
| `'P13-1'` | `'P13'` | `1` | `7` | `0` |
| `'P13-5'` | `'P13'` | `5` | `7` | `0` |
| `'P14-1'` | `'P14'` | `1` | `4` | `0` |
| `'P14-5'` | `'P14'` | `5` | `1` | `1` |
| `'P14-9'` | `'P14'` | `9` | `8` | `0` |
| `'P14-13'` | `'P14'` | `13` | `3` | `1` |
| `'P14-17'` | `'P14'` | `17` | `7` | `1` |
| `'P14-21'` | `'P14'` | `21` | `4` | `0` |
| `'P14-25'` | `'P14'` | `25` | `5` | `1` |
| `'P14-29'` | `'P14'` | `29` | `0` | `0` |


`all_optimal_shores` lists all mathematical parity optima in increasing numeric order for
inspection only. This listing order is NOT the result tie-break. `first_result` is derived
from the separately fixed GR pair order and each ordinary query's least minimizer.
`original_chosen` is the separate original-universe lifting. None signifies infeasible.
`calls` is the prescribed future count, not a measurement of absent parity code.

### Fixture table: MINIMUMS

| id | minimum | all_optimal_shores | first_result | calls | original_chosen |
| --- | --- | --- | --- | --- | --- |
| `'P01'` | `None` | `()` | `None` | `0` | `None` |
| `'P02'` | `0` | `(1,)` | `1` | `1` | `1` |
| `'P03'` | `5` | `(1,)` | `1` | `1` | `1` |
| `'P04'` | `5` | `(1,)` | `1` | `1` | `1` |
| `'P05'` | `0` | `(1,)` | `1` | `1` | `1` |
| `'P06'` | `3` | `(5,)` | `5` | `3` | `1` |
| `'P07'` | `2` | `(1,)` | `1` | `3` | `0` |
| `'P08'` | `7` | `(5,)` | `5` | `7` | `1` |
| `'P09'` | `0` | `(5, 9)` | `5` | `7` | `1` |
| `'P10'` | `0` | `(1, 5)` | `1` | `7` | `0` |
| `'P11'` | `1` | `(1,)` | `1` | `7` | `0` |
| `'P12'` | `0` | `(5, 9, 17, 29, 33, 45, 53, 57)` | `5` | `21` | `1` |
| `'P13'` | `None` | `()` | `None` | `0` | `None` |
| `'P14'` | `1` | `(5,)` | `5` | `13` | `1` |


### Strictly worse parity minimum and coordinate hazard: P06

The two admissible geometric shores are 1={0}, of cut capacity 2, and 5={0,2}, of cut
capacity 3. Terminal T=6 means only shore 5 is odd. Thus the ordinary minimum 2 is wrong
for the constrained problem; the parity minimum is exactly 3 at shore 5.

The query (2,1) contracts problem source 0 with problem vertex 2. Its temporary least
minimum is mask 1, which lifts to problem mask 5. Checking mask 1 directly against
problem T=6 would wrongly reject the only correct candidate. Original lifting then
returns original mask 1; this equality to the earlier temporary integer is accidental,
not permission to mix the universes.

P09 fixes tied parity optima 5 and 9 and requires the first encountered 5, not the last.
P10 accepts a source-containing terminal set and an all-zero-capacity nonempty arc tuple.
P01/P13 return None without any flow calls despite different capacities; P02/P12 are
zero-valued feasible problems even though their arc tuples are empty.

## ORACLE-061 — Exact ordered pair sequence and ordinary-query traces

**Classification:** `LOCAL_CONTRACT_FIXTURE`.
**Source:** original Goemans--Ramakrishnan Theorem 2, Corollary 3, Section 5; pinned thm:GR.
**Engineering authority:** DESIGN 4.8.12--13; TEST_PLAN PC11--PC14.

Pairs are increasing a then b with a!=sink, b!=source, a!=b. This reference enumeration
makes exactly `(N-1)^2-(N-2) = N*N-3*N+3` calls for nonzero T, without early exit at zero
and without deduplicating restrictions. The fixed source/sink lattice excludes the empty
and entire ground set, so those exceptional GR candidates are not added as feasible cuts.

### Fixture table: PAIR_ORDERS

| N | pairs | calls |
| --- | --- | --- |
| `2` | `((0, 1),)` | `1` |
| `3` | `((0, 1), (0, 2), (2, 1))` | `3` |
| `4` | `((0, 1), (0, 2), (0, 3), (2, 1), (2, 3), (3, 1), (3, 2))` | `7` |
| `5` | `((0, 1), (0, 2), (0, 3), (0, 4), (2, 1), (2, 3), (2, 4), (3, 1), (3, 2), (3, 4), (4, 1), (4, 2), (4, 3))` | `13` |
| `6` | `((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (2, 1), (2, 3), (2, 4), (2, 5), (3, 1), (3, 2), (3, 4), (3, 5), (4, 1), (4, 2), (4, 3), (4, 5), (5, 1), (5, 2), (5, 3), (5, 4))` | `21` |


For the selected problems all query partitions, canonical arcs, and ordinary minimizers
are literal below. `classes` now maps temporary vertices to PROBLEM-vertex masks.
`all_temporary_minimizers` is obtained by complete ordinary-cut enumeration; their
intersection is `least_temporary`. `lifted_problem_shore` must precede the oddness test.
`update` uses strict value improvement only; `incumbent` is (cut value, problem shore).
These are private exhaustive expected-data calculations, not a Unit 11 implementation.

### Fixture table: PAIR_TRACES

| id | problem | pair | classes | arcs | ordinary_minimum | all_temporary_minimizers | least_temporary | lifted_problem_shore | odd | update | incumbent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `'P02-0-1'` | `'P02'` | `(0, 1)` | `(1, 2)` | `()` | `0` | `(1,)` | `1` | `1` | `1` | `True` | `(0, 1)` |
| `'P04-0-1'` | `'P04'` | `(0, 1)` | `(1, 2)` | `((0, 1, 5), (1, 0, 2))` | `5` | `(1,)` | `1` | `1` | `1` | `True` | `(5, 1)` |
| `'P06-0-1'` | `'P06'` | `(0, 1)` | `(1, 2, 4)` | `((0, 2, 2), (2, 1, 3))` | `2` | `(1,)` | `1` | `1` | `0` | `False` | `None` |
| `'P06-0-2'` | `'P06'` | `(0, 2)` | `(1, 6)` | `((0, 1, 2),)` | `2` | `(1,)` | `1` | `1` | `0` | `False` | `None` |
| `'P06-2-1'` | `'P06'` | `(2, 1)` | `(5, 2)` | `((0, 1, 3),)` | `3` | `(1,)` | `1` | `5` | `1` | `True` | `(3, 5)` |
| `'P08-0-1'` | `'P08'` | `(0, 1)` | `(1, 2, 4, 8)` | `((0, 2, 3), (0, 3, 1), (2, 1, 4), (2, 3, 2), (3, 1, 6))` | `4` | `(1,)` | `1` | `1` | `0` | `False` | `None` |
| `'P08-0-2'` | `'P08'` | `(0, 2)` | `(1, 6, 8)` | `((0, 1, 3), (0, 2, 1), (1, 2, 2), (2, 1, 6))` | `4` | `(1,)` | `1` | `1` | `0` | `False` | `None` |
| `'P08-0-3'` | `'P08'` | `(0, 3)` | `(1, 10, 4)` | `((0, 1, 1), (0, 2, 3), (2, 1, 6))` | `4` | `(1,)` | `1` | `1` | `0` | `False` | `None` |
| `'P08-2-1'` | `'P08'` | `(2, 1)` | `(5, 2, 8)` | `((0, 1, 4), (0, 2, 3), (2, 1, 6))` | `7` | `(1,)` | `1` | `5` | `1` | `True` | `(7, 5)` |
| `'P08-2-3'` | `'P08'` | `(2, 3)` | `(5, 10)` | `((0, 1, 7),)` | `7` | `(1,)` | `1` | `5` | `1` | `False` | `(7, 5)` |
| `'P08-3-1'` | `'P08'` | `(3, 1)` | `(9, 2, 4)` | `((0, 1, 6), (0, 2, 3), (2, 0, 2), (2, 1, 4))` | `9` | `(1,)` | `1` | `9` | `1` | `False` | `(7, 5)` |
| `'P08-3-2'` | `'P08'` | `(3, 2)` | `(9, 6)` | `((0, 1, 9), (1, 0, 2))` | `9` | `(1,)` | `1` | `9` | `1` | `False` | `(7, 5)` |
| `'P09-0-1'` | `'P09'` | `(0, 1)` | `(1, 2, 4, 8)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `1` | `0` | `False` | `None` |
| `'P09-0-2'` | `'P09'` | `(0, 2)` | `(1, 6, 8)` | `()` | `0` | `(1, 5)` | `1` | `1` | `0` | `False` | `None` |
| `'P09-0-3'` | `'P09'` | `(0, 3)` | `(1, 10, 4)` | `()` | `0` | `(1, 5)` | `1` | `1` | `0` | `False` | `None` |
| `'P09-2-1'` | `'P09'` | `(2, 1)` | `(5, 2, 8)` | `()` | `0` | `(1, 5)` | `1` | `5` | `1` | `True` | `(0, 5)` |
| `'P09-2-3'` | `'P09'` | `(2, 3)` | `(5, 10)` | `()` | `0` | `(1,)` | `1` | `5` | `1` | `False` | `(0, 5)` |
| `'P09-3-1'` | `'P09'` | `(3, 1)` | `(9, 2, 4)` | `()` | `0` | `(1, 5)` | `1` | `9` | `1` | `False` | `(0, 5)` |
| `'P09-3-2'` | `'P09'` | `(3, 2)` | `(9, 6)` | `()` | `0` | `(1,)` | `1` | `9` | `1` | `False` | `(0, 5)` |
| `'P12-0-1'` | `'P12'` | `(0, 1)` | `(1, 2, 4, 8, 16, 32)` | `()` | `0` | `(1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61)` | `1` | `1` | `0` | `False` | `None` |
| `'P12-0-2'` | `'P12'` | `(0, 2)` | `(1, 6, 8, 16, 32)` | `()` | `0` | `(1, 5, 9, 13, 17, 21, 25, 29)` | `1` | `1` | `0` | `False` | `None` |
| `'P12-0-3'` | `'P12'` | `(0, 3)` | `(1, 10, 4, 16, 32)` | `()` | `0` | `(1, 5, 9, 13, 17, 21, 25, 29)` | `1` | `1` | `0` | `False` | `None` |
| `'P12-0-4'` | `'P12'` | `(0, 4)` | `(1, 18, 4, 8, 32)` | `()` | `0` | `(1, 5, 9, 13, 17, 21, 25, 29)` | `1` | `1` | `0` | `False` | `None` |
| `'P12-0-5'` | `'P12'` | `(0, 5)` | `(1, 34, 4, 8, 16)` | `()` | `0` | `(1, 5, 9, 13, 17, 21, 25, 29)` | `1` | `1` | `0` | `False` | `None` |
| `'P12-2-1'` | `'P12'` | `(2, 1)` | `(5, 2, 8, 16, 32)` | `()` | `0` | `(1, 5, 9, 13, 17, 21, 25, 29)` | `1` | `5` | `1` | `True` | `(0, 5)` |
| `'P12-2-3'` | `'P12'` | `(2, 3)` | `(5, 10, 16, 32)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `5` | `1` | `False` | `(0, 5)` |
| `'P12-2-4'` | `'P12'` | `(2, 4)` | `(5, 18, 8, 32)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `5` | `1` | `False` | `(0, 5)` |
| `'P12-2-5'` | `'P12'` | `(2, 5)` | `(5, 34, 8, 16)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `5` | `1` | `False` | `(0, 5)` |
| `'P12-3-1'` | `'P12'` | `(3, 1)` | `(9, 2, 4, 16, 32)` | `()` | `0` | `(1, 5, 9, 13, 17, 21, 25, 29)` | `1` | `9` | `1` | `False` | `(0, 5)` |
| `'P12-3-2'` | `'P12'` | `(3, 2)` | `(9, 6, 16, 32)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `9` | `1` | `False` | `(0, 5)` |
| `'P12-3-4'` | `'P12'` | `(3, 4)` | `(9, 18, 4, 32)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `9` | `1` | `False` | `(0, 5)` |
| `'P12-3-5'` | `'P12'` | `(3, 5)` | `(9, 34, 4, 16)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `9` | `1` | `False` | `(0, 5)` |
| `'P12-4-1'` | `'P12'` | `(4, 1)` | `(17, 2, 4, 8, 32)` | `()` | `0` | `(1, 5, 9, 13, 17, 21, 25, 29)` | `1` | `17` | `1` | `False` | `(0, 5)` |
| `'P12-4-2'` | `'P12'` | `(4, 2)` | `(17, 6, 8, 32)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `17` | `1` | `False` | `(0, 5)` |
| `'P12-4-3'` | `'P12'` | `(4, 3)` | `(17, 10, 4, 32)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `17` | `1` | `False` | `(0, 5)` |
| `'P12-4-5'` | `'P12'` | `(4, 5)` | `(17, 34, 4, 8)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `17` | `1` | `False` | `(0, 5)` |
| `'P12-5-1'` | `'P12'` | `(5, 1)` | `(33, 2, 4, 8, 16)` | `()` | `0` | `(1, 5, 9, 13, 17, 21, 25, 29)` | `1` | `33` | `1` | `False` | `(0, 5)` |
| `'P12-5-2'` | `'P12'` | `(5, 2)` | `(33, 6, 8, 16)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `33` | `1` | `False` | `(0, 5)` |
| `'P12-5-3'` | `'P12'` | `(5, 3)` | `(33, 10, 4, 16)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `33` | `1` | `False` | `(0, 5)` |
| `'P12-5-4'` | `'P12'` | `(5, 4)` | `(33, 18, 4, 8)` | `()` | `0` | `(1, 5, 9, 13)` | `1` | `33` | `1` | `False` | `(0, 5)` |


## ORACLE-062 — Why arbitrary tied ordinary minimizers are insufficient

**Classification:** `LOCAL_CONTRACT_FIXTURE` with a deliberately inadmissible backend control.
**Source/authority:** GR Theorem 2 minimal-minimizer requirement; DESIGN 4.8.12; PC12.

P12 has N=6, no arcs, and all four free vertices terminal: T=60. Every geometric shore
has capacity zero. In each ordered-pair restriction, the least ordinary minimizer is
exactly its forced source class `{0,a}`. For a free terminal a it is odd. The first such
candidate is pair (2,1), after all five a=0 pairs, so the ruled result is mask 5.

Every restriction also has an EVEN tied minimizer, explicitly listed below. Thus a
backend that chooses that even minimizer in every restriction would cause the parity
filter to discard every candidate although parity-optimal shores exist. Such a backend
violates the adopted contract. This is not an alternative admissible tie-breaking policy.
The least ordinary shore is the intersection of all ordinary minimizers, not the first
shore visited by a brute enumerator unless that equality is independently established.

### Fixture table: ARBITRARY_TIE_TRAP

| pair | least_shore | least_odd | wrong_even_minimum |
| --- | --- | --- | --- |
| `(0, 1)` | `1` | `0` | `1` |
| `(0, 2)` | `1` | `0` | `1` |
| `(0, 3)` | `1` | `0` | `1` |
| `(0, 4)` | `1` | `0` | `1` |
| `(0, 5)` | `1` | `0` | `1` |
| `(2, 1)` | `5` | `1` | `13` |
| `(2, 3)` | `5` | `1` | `21` |
| `(2, 4)` | `5` | `1` | `13` |
| `(2, 5)` | `5` | `1` | `13` |
| `(3, 1)` | `9` | `1` | `13` |
| `(3, 2)` | `9` | `1` | `25` |
| `(3, 4)` | `9` | `1` | `13` |
| `(3, 5)` | `9` | `1` | `13` |
| `(4, 1)` | `17` | `1` | `21` |
| `(4, 2)` | `17` | `1` | `25` |
| `(4, 3)` | `17` | `1` | `21` |
| `(4, 5)` | `17` | `1` | `21` |
| `(5, 1)` | `33` | `1` | `37` |
| `(5, 2)` | `33` | `1` | `41` |
| `(5, 3)` | `33` | `1` | `37` |
| `(5, 4)` | `33` | `1` | `37` |


## ORACLE-063 — Flow-only diagnostic anchors, kept separate from minima

**Classification:** `LOCAL_CONTRACT_FIXTURE` of the closed flow-interface accounting.
**Authority:** closed minimum_cut/FlowStats; DESIGN 4.8.13; TEST_PLAN PC15--PC16.

Each trace tuple is `(a,b,augmentations,bfs_scans,peak_generated_value)`. The four totals
become ParityCutStats fields in declaration order. Counters never decide which parity
candidate is kept. These anchors were hand-traced before comparison with the closed flow
backend. Expected parity minima were derived solely by cut enumeration.

P03 has one source->sink residual forward entry of capacity 5: one successful scan,
one augmentation, one failed scan, peak 5. P04 has the same first successful scan but two
source-adjacency entries on the failed search because both original orientations exist:
three total scans, peak 5. P05 has zero capacities and only a failed scan of those two
entries. Empty arc lists do not initiate a BFS, but each actual query still counts.

P06's uncontracted path query scans three entries in its successful BFS and one in the
failed BFS: `(1,4,3)`. Its two contracted single-edge queries have `(1,2,2)` and `(1,2,3)`.
Thus aggregate diagnostics are `(3,3,8,3)`. The peak is FLOW-ONLY; it is not the largest
mask, original coefficient, retained shift, or arbitrary integer in the entire reduction.

### Fixture table: STATS_ANCHORS

| problem | calls | augmentations | bfs_scans | peak | trace |
| --- | --- | --- | --- | --- | --- |
| `'P01'` | `0` | `0` | `0` | `0` | `()` |
| `'P02'` | `1` | `0` | `0` | `0` | `((0, 1, 0, 0, 0),)` |
| `'P03'` | `1` | `1` | `2` | `5` | `((0, 1, 1, 2, 5),)` |
| `'P04'` | `1` | `1` | `3` | `5` | `((0, 1, 1, 3, 5),)` |
| `'P05'` | `1` | `0` | `2` | `0` | `((0, 1, 0, 2, 0),)` |
| `'P06'` | `3` | `3` | `8` | `3` | `((0, 1, 1, 4, 3), (0, 2, 1, 2, 2), (2, 1, 1, 2, 3))` |
| `'P09'` | `7` | `0` | `0` | `0` | `((0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 0, 0), (2, 1, 0, 0, 0), (2, 3, 0, 0, 0), (3, 1, 0, 0, 0), (3, 2, 0, 0, 0))` |
| `'P12'` | `21` | `0` | `0` | `0` | `((0, 1, 0, 0, 0), (0, 2, 0, 0, 0), (0, 3, 0, 0, 0), (0, 4, 0, 0, 0), (0, 5, 0, 0, 0), (2, 1, 0, 0, 0), (2, 3, 0, 0, 0), (2, 4, 0, 0, 0), (2, 5, 0, 0, 0), (3, 1, 0, 0, 0), (3, 2, 0, 0, 0), (3, 4, 0, 0, 0), (3, 5, 0, 0, 0), (4, 1, 0, 0, 0), (4, 2, 0, 0, 0), (4, 3, 0, 0, 0), (4, 5, 0, 0, 0), (5, 1, 0, 0, 0), (5, 2, 0, 0, 0), (5, 3, 0, 0, 0), (5, 4, 0, 0, 0))` |


The independent oracle audit verifies the trace sums and hand-fixed anchors without
executing flow. A separate closed-backend compatibility record may compare these
pre-existing anchors with actual ordinary minimum_cut calls. It must not use returned
flow values to seed the expected parity minimum or rewrite a discrepant oracle silently.

## ORACLE-064 — Registered exhaustive directed-graph and terminal corpus

**Classification:** `LOCAL_CONTRACT_FIXTURE` / finite independent optimality oracle.
**Authority:** TEST_PLAN PC11--PC16, PC18--PC19.

For N in {2,3,4}, include every ordered pair (u,v) with u!=v, sorted by endpoints. Assign
each capacity independently from {0,1}; retain even the zero-capacity positions. For each
graph include every even-cardinality terminal mask, including zero. Thus there are
4 + 64 + 4096 graphs, and 4*2 + 64*4 + 4096*8 graph/terminal problems. For N=2 use
n=1, classes=(3,4); for N>=3 use n=N-2, source/sink singleton preimages first and free
original singletons thereafter. These are standalone problem fixtures, not active Instances.

For every graph, list all source-containing/sink-excluding masks and their directed cut
values. For each parity mask compute its true optimum by independent all-shore filtering.
For every compatible pair separately intersect all ordinary minimizing shores, then apply
the ruled parity filter and strict-improvement selection. Compare the two optimum values.

Query minimizer enumeration may be reused per graph in the private oracle audit because
it is independent of T. `distinct_graph_pair_minimizations` counts that private work;
`specified_backend_calls` instead sums the contractual future calls for all nonempty-T
problems. **The latter is an expected call count, not a measurement of production code.**
No flow backend or Unit 11 implementation is used to establish these counts or optima.

### Fixture table: GRAPH_COUNTS

| metric | value |
| --- | --- |
| `'distinct_graph_pair_minimizations'` | `28868` |
| `'graphs'` | `4164` |
| `'terminal_problems'` | `33032` |
| `'all_shore_evaluations'` | `131592` |
| `'infeasible'` | `4164` |
| `'feasible'` | `28868` |
| `'parity_admissible_shores'` | `65796` |
| `'specified_backend_calls'` | `201284` |
| `'zero_minima'` | `5018` |
| `'candidate_parity_acceptances'` | `115076` |
| `'positive_minima'` | `23850` |
| `'multiple_optima'` | `11296` |


T=0 accounts for every infeasible problem. A nonzero even T always allows an odd shore
in this complete source/sink lattice, regardless of capacities. `all_shore_evaluations`
counts every geometric shore once per terminal problem, whether parity admissible or not.
`multiple_optima` counts feasible problems with at least two minimizing parity shores.
No global least or lexicographically minimal parity-shore guarantee is invented.

## ORACLE-065 — Registered exhaustive forced-family correspondence corpus

**Classification:** `LOCAL_CONTRACT_FIXTURE`; valid but impossible descriptors return None.
**Authority:** TEST_PLAN PC4--PC9, PC19.

For n in {1,2,3,4}, use two standalone raw networks on n+2 vertices:

1. no arcs;
2. every ordered nonloop pair, capacity `((u+1)*(v+2)) % 5`, in increasing pair order,
   including zero capacities.

For each network, take every T,I,O in `range(1<<n)` and pi in {0,1}. In particular overlaps
are included and return None; every mask is in range. The descriptor count is
`sum(2 * 2 * 8**n for n in (1,2,3,4)) = 18720`. Independently enumerate original subsets
to establish logical feasibility, rather than calling the production family predicate.
Production, unlike this audit, must use the closed predicate after finite-universe checks.

For each feasible descriptor, enumerate all geometric reduced shores, lift them, and
check forced membership, parity correspondence, exact directed-cut equality, and
one-to-one coverage of the original parity-feasible family. Include even reduced-parity
shores when checking generic lifting. No min-cut or parity minimizer is invoked here.

### Fixture table: FAMILY_COUNTS

| metric | value |
| --- | --- |
| `'descriptors'` | `18720` |
| `'disjoint_descriptors'` | `6216` |
| `'feasible'` | `4656` |
| `'pi0_feasible'` | `2448` |
| `'toggle_add'` | `1894` |
| `'geometric_lift_checks'` | `15612` |
| `'odd_shores'` | `9360` |
| `'original_admissible_shores'` | `9360` |
| `'overlap_none'` | `12504` |
| `'parity_none'` | `1560` |
| `'toggle_none'` | `2208` |
| `'pi1_feasible'` | `2208` |
| `'toggle_remove'` | `554` |


The 15612 geometric lift checks concern feasible descriptors only. The 9360 odd-image
count equals the independent original admissible-shore count. The 554 sink-removal cases
must not be conflated with the 1894 sink-add cases. None cases are neither malformed
input exceptions nor global Empty admissible-family results.

## ORACLE-066 — Local source-residual integration without the full branch oracle

**Classification:** `LOCAL_CONTRACT_FIXTURE`; expected minima are over the stated family only.
**Source:** eq:param0--3, prop:domain-decomp, lem:sign-routing, lem:parity-anchor, thm:GR.
**Authority:** DESIGN 4.8.16; TEST_PLAN PC17.

The exact RICH and MIXED instances are already fixed by ORACLE-025 and ORACLE-031.
They are repeated here for self-contained arithmetic:

### Fixture table: INSTANCES

| id | n | edges | f |
| --- | --- | --- | --- |
| `'RICH'` | `5` | `((0, 2, 2), (1, 2, 2), (2, 4, 1), (3, 4, 1))` | `(1, 1, 1, 1, 2)` |
| `'MIXED'` | `4` | `((0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 4), (1, 3, 2), (2, 3, 5))` | `(2, 3, 4, 5)` |


The selected families use the source T_plus or T_f as appropriate. For branch 1, take
p=0 and the first support edge orientation; branch 2 uses the first f>=2 vertex; branch 3
uses the first support orientation. These are explicit local families, not a loop over
all atomic families. For every branch use parameters (0,1), (2,3), and (-3,1).

Independently construct source coefficients, fix the corresponding contracted classes,
terminal mask and arcs, enumerate parity cuts, lift the chosen shore, and evaluate the
source's literal B*c_j(U)-A*h_j(U) from raw instance records. It must equal
`minimum_cut - negative_shift + constant` and be minimal over precisely the stated family.
No use of the eventual ExactBranchMin, production family enumeration, or witness reconstruction
establishes these values. The original graph and original source/sink are preserved for
independent raw-cut evaluation.

### Fixture table: BRANCH_SEAMS

| id | instance | branch | parameter | family | gamma | negative_shift | constant | classes | terminal_mask | arcs | minimum_cut | reduced_choice | original_choice | minimum_residual | original_optima | calls | unrestricted_cut |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `'RICH-j0-0-1'` | `'RICH'` | `0` | `(0, 1)` | `(3, 1, 0, 0)` | `(1, 1, 1, 1, 2)` | `0` | `-1` | `(32, 64, 1, 2, 4, 8, 16)` | `12` | `((1, 2, 1), (1, 3, 1), (1, 4, 1), (1, 5, 1), (1, 6, 2), (2, 1, 1), (2, 4, 2), (3, 1, 1), (3, 4, 2), (4, 1, 1), (4, 2, 2), (4, 3, 2), (4, 6, 1), (5, 1, 1), (5, 6, 1), (6, 1, 2), (6, 4, 1), (6, 5, 1))` | `3` | `5` | `1` | `2` | `(1, 2)` | `31` | `0` |
| `'RICH-j1-0-1'` | `'RICH'` | `1` | `(0, 1)` | `(3, 0, 1, 4)` | `(1, 1, 1, 1, 2)` | `0` | `-2` | `(161, 68, 2, 8, 16)` | `6` | `((0, 1, 3), (1, 0, 3), (1, 2, 3), (1, 3, 1), (1, 4, 3), (2, 1, 3), (3, 1, 1), (3, 4, 1), (4, 1, 3), (4, 3, 1))` | `6` | `5` | `3` | `4` | `(3,)` | `13` | `0` |
| `'RICH-j2-0-1'` | `'RICH'` | `2` | `(0, 1)` | `(15, 1, 16, 0)` | `(-2, -2, -5, -1, -2)` | `12` | `0` | `(48, 64, 1, 2, 4, 8)` | `60` | `((0, 2, 2), (0, 3, 2), (0, 4, 6), (0, 5, 2), (2, 0, 2), (2, 4, 2), (3, 0, 2), (3, 4, 2), (4, 0, 6), (4, 2, 2), (4, 3, 2), (5, 0, 2))` | `2` | `29` | `23` | `-10` | `(23,)` | `21` | `0` |
| `'RICH-j3-0-1'` | `'RICH'` | `3` | `(0, 1)` | `(15, 0, 1, 4)` | `(-2, -2, -5, -1, -2)` | `12` | `-2` | `(161, 68, 2, 8, 16)` | `12` | `((0, 1, 7), (0, 2, 2), (0, 3, 1), (0, 4, 2), (1, 0, 7), (1, 2, 2), (1, 4, 1), (2, 0, 2), (2, 1, 2), (3, 0, 1), (3, 4, 1), (4, 0, 2), (4, 1, 1), (4, 3, 1))` | `10` | `25` | `25` | `-4` | `(25,)` | `13` | `0` |
| `'RICH-j0-2-3'` | `'RICH'` | `0` | `(2, 3)` | `(3, 1, 0, 0)` | `(1, 1, -5, 3, 6)` | `5` | `-5` | `(32, 64, 1, 2, 4, 8, 16)` | `12` | `((0, 4, 5), (1, 2, 1), (1, 3, 1), (1, 5, 3), (1, 6, 6), (2, 1, 1), (2, 4, 6), (3, 1, 1), (3, 4, 6), (4, 0, 5), (4, 2, 6), (4, 3, 6), (4, 6, 3), (5, 1, 3), (5, 6, 3), (6, 1, 6), (6, 4, 3), (6, 5, 3))` | `10` | `21` | `5` | `0` | `(5, 6)` | `31` | `5` |
| `'RICH-j1-2-3'` | `'RICH'` | `1` | `(2, 3)` | `(3, 0, 1, 4)` | `(1, 1, -5, 3, 6)` | `5` | `-6` | `(161, 68, 2, 8, 16)` | `6` | `((0, 1, 12), (1, 0, 12), (1, 2, 7), (1, 3, 3), (1, 4, 9), (2, 1, 7), (3, 1, 3), (3, 4, 3), (4, 1, 9), (4, 3, 3))` | `19` | `5` | `3` | `8` | `(3,)` | `13` | `5` |
| `'RICH-j2-2-3'` | `'RICH'` | `2` | `(2, 3)` | `(15, 1, 16, 0)` | `(-8, -8, -17, -5, -10)` | `48` | `2` | `(48, 64, 1, 2, 4, 8)` | `60` | `((0, 2, 8), (0, 3, 8), (0, 4, 20), (0, 5, 8), (2, 0, 8), (2, 4, 6), (3, 0, 8), (3, 4, 6), (4, 0, 20), (4, 2, 6), (4, 3, 6), (5, 0, 8))` | `8` | `29` | `23` | `-38` | `(23,)` | `21` | `0` |
| `'RICH-j3-2-3'` | `'RICH'` | `3` | `(2, 3)` | `(15, 0, 1, 4)` | `(-8, -8, -17, -5, -10)` | `48` | `-6` | `(161, 68, 2, 8, 16)` | `12` | `((0, 1, 23), (0, 2, 8), (0, 3, 5), (0, 4, 10), (1, 0, 23), (1, 2, 6), (1, 4, 3), (2, 0, 8), (2, 1, 6), (3, 0, 5), (3, 4, 3), (4, 0, 10), (4, 1, 3), (4, 3, 3))` | `34` | `25` | `25` | `-20` | `(25,)` | `13` | `0` |
| `'RICH-j0--3-1'` | `'RICH'` | `0` | `(-3, 1)` | `(3, 1, 0, 0)` | `(4, 4, 13, 1, 2)` | `0` | `2` | `(32, 64, 1, 2, 4, 8, 16)` | `12` | `((1, 2, 4), (1, 3, 4), (1, 4, 13), (1, 5, 1), (1, 6, 2), (2, 1, 4), (2, 4, 2), (3, 1, 4), (3, 4, 2), (4, 1, 13), (4, 2, 2), (4, 3, 2), (4, 6, 1), (5, 1, 1), (5, 6, 1), (6, 1, 2), (6, 4, 1), (6, 5, 1))` | `6` | `5` | `1` | `8` | `(1, 2)` | `31` | `0` |
| `'RICH-j1--3-1'` | `'RICH'` | `1` | `(-3, 1)` | `(3, 0, 1, 4)` | `(4, 4, 13, 1, 2)` | `0` | `-2` | `(161, 68, 2, 8, 16)` | `6` | `((0, 1, 6), (1, 0, 6), (1, 2, 6), (1, 3, 1), (1, 4, 3), (2, 1, 6), (3, 1, 1), (3, 4, 1), (4, 1, 3), (4, 3, 1))` | `12` | `5` | `3` | `10` | `(3,)` | `13` | `0` |
| `'RICH-j2--3-1'` | `'RICH'` | `2` | `(-3, 1)` | `(15, 1, 16, 0)` | `(1, 1, -2, 2, 4)` | `2` | `-3` | `(48, 64, 1, 2, 4, 8)` | `60` | `((0, 1, 4), (0, 4, 3), (0, 5, 1), (1, 0, 4), (1, 2, 1), (1, 3, 1), (1, 5, 2), (2, 1, 1), (2, 4, 2), (3, 1, 1), (3, 4, 2), (4, 0, 3), (4, 2, 2), (4, 3, 2), (5, 0, 1), (5, 1, 2))` | `7` | `29` | `23` | `2` | `(23,)` | `21` | `2` |
| `'RICH-j3--3-1'` | `'RICH'` | `3` | `(-3, 1)` | `(15, 0, 1, 4)` | `(1, 1, -2, 2, 4)` | `2` | `-2` | `(161, 68, 2, 8, 16)` | `12` | `((0, 1, 5), (1, 0, 5), (1, 2, 3), (1, 3, 2), (1, 4, 5), (2, 1, 3), (3, 1, 2), (3, 4, 1), (4, 1, 5), (4, 3, 1))` | `8` | `5` | `3` | `4` | `(3, 9)` | `13` | `2` |
| `'MIXED-j0-0-1'` | `'MIXED'` | `0` | `(0, 1)` | `(10, 1, 0, 0)` | `(2, 3, 4, 5)` | `0` | `-1` | `(16, 32, 1, 2, 4, 8)` | `40` | `((1, 2, 2), (1, 3, 3), (1, 4, 4), (1, 5, 5), (2, 1, 2), (2, 3, 2), (2, 4, 3), (2, 5, 1), (3, 1, 3), (3, 2, 2), (3, 4, 4), (3, 5, 2), (4, 1, 4), (4, 2, 3), (4, 3, 4), (4, 5, 5), (5, 1, 5), (5, 2, 1), (5, 3, 2), (5, 4, 5))` | `11` | `9` | `2` | `10` | `(2,)` | `21` | `0` |
| `'MIXED-j1-0-1'` | `'MIXED'` | `1` | `(0, 1)` | `(10, 0, 1, 2)` | `(2, 3, 4, 5)` | `0` | `-2` | `(81, 34, 4, 8)` | `9` | `((0, 1, 4), (0, 2, 3), (0, 3, 1), (1, 0, 4), (1, 2, 8), (1, 3, 7), (2, 0, 3), (2, 1, 8), (2, 3, 5), (3, 0, 1), (3, 1, 7), (3, 2, 5))` | `8` | `1` | `1` | `6` | `(1,)` | `7` | `0` |
| `'MIXED-j2-0-1'` | `'MIXED'` | `2` | `(0, 1)` | `(10, 1, 1, 0)` | `(-6, -8, -12, -8)` | `34` | `0` | `(17, 32, 2, 4, 8)` | `20` | `((0, 2, 10), (0, 3, 15), (0, 4, 9), (2, 0, 10), (2, 3, 4), (2, 4, 2), (3, 0, 15), (3, 2, 4), (3, 4, 5), (4, 0, 9), (4, 2, 2), (4, 3, 5))` | `16` | `25` | `13` | `-18` | `(7, 13)` | `13` | `0` |
| `'MIXED-j3-0-1'` | `'MIXED'` | `3` | `(0, 1)` | `(10, 0, 1, 2)` | `(-6, -8, -12, -8)` | `34` | `-2` | `(81, 34, 4, 8)` | `9` | `((0, 1, 10), (0, 2, 15), (0, 3, 9), (1, 0, 10), (1, 2, 4), (1, 3, 2), (2, 0, 15), (2, 1, 4), (2, 3, 5), (3, 0, 9), (3, 1, 2), (3, 2, 5))` | `28` | `5` | `5` | `-8` | `(5,)` | `7` | `0` |
| `'MIXED-j0-2-3'` | `'MIXED'` | `0` | `(2, 3)` | `(10, 1, 0, 0)` | `(-2, -1, -4, 9)` | `7` | `-5` | `(16, 32, 1, 2, 4, 8)` | `40` | `((0, 2, 2), (0, 3, 1), (0, 4, 4), (1, 5, 9), (2, 0, 2), (2, 3, 6), (2, 4, 9), (2, 5, 3), (3, 0, 1), (3, 2, 6), (3, 4, 12), (3, 5, 6), (4, 0, 4), (4, 2, 9), (4, 3, 12), (4, 5, 15), (5, 1, 9), (5, 2, 3), (5, 3, 6), (5, 4, 15))` | `24` | `29` | `7` | `12` | `(7,)` | `21` | `7` |
| `'MIXED-j1-2-3'` | `'MIXED'` | `1` | `(2, 3)` | `(10, 0, 1, 2)` | `(-2, -1, -4, 9)` | `7` | `-6` | `(81, 34, 4, 8)` | `9` | `((0, 1, 7), (0, 2, 13), (0, 3, 3), (1, 0, 7), (1, 2, 12), (1, 3, 15), (2, 0, 13), (2, 1, 12), (2, 3, 15), (3, 0, 3), (3, 1, 15), (3, 2, 15))` | `23` | `1` | `1` | `10` | `(1,)` | `7` | `7` |
| `'MIXED-j2-2-3'` | `'MIXED'` | `2` | `(2, 3)` | `(10, 1, 1, 0)` | `(-22, -30, -44, -34)` | `130` | `2` | `(17, 32, 2, 4, 8)` | `20` | `((0, 2, 36), (0, 3, 53), (0, 4, 37), (2, 0, 36), (2, 3, 12), (2, 4, 6), (3, 0, 53), (3, 2, 12), (3, 4, 15), (4, 0, 37), (4, 2, 6), (4, 3, 15))` | `54` | `25` | `13` | `-74` | `(13,)` | `13` | `0` |
| `'MIXED-j3-2-3'` | `'MIXED'` | `3` | `(2, 3)` | `(10, 0, 1, 2)` | `(-22, -30, -44, -34)` | `130` | `-6` | `(81, 34, 4, 8)` | `9` | `((0, 1, 36), (0, 2, 53), (0, 3, 37), (1, 0, 36), (1, 2, 12), (1, 3, 6), (2, 0, 53), (2, 1, 12), (2, 3, 15), (3, 0, 37), (3, 1, 6), (3, 2, 15))` | `100` | `5` | `5` | `-36` | `(5,)` | `7` | `0` |
| `'MIXED-j0--3-1'` | `'MIXED'` | `0` | `(-3, 1)` | `(10, 1, 0, 0)` | `(14, 18, 28, 14)` | `0` | `2` | `(16, 32, 1, 2, 4, 8)` | `40` | `((1, 2, 14), (1, 3, 18), (1, 4, 28), (1, 5, 14), (2, 1, 14), (2, 3, 2), (2, 4, 3), (2, 5, 1), (3, 1, 18), (3, 2, 2), (3, 4, 4), (3, 5, 2), (4, 1, 28), (4, 2, 3), (4, 3, 4), (4, 5, 5), (5, 1, 14), (5, 2, 1), (5, 3, 2), (5, 4, 5))` | `22` | `33` | `8` | `24` | `(8,)` | `21` | `0` |
| `'MIXED-j1--3-1'` | `'MIXED'` | `1` | `(-3, 1)` | `(10, 0, 1, 2)` | `(14, 18, 28, 14)` | `0` | `-2` | `(81, 34, 4, 8)` | `9` | `((0, 1, 16), (0, 2, 3), (0, 3, 1), (1, 0, 16), (1, 2, 32), (1, 3, 16), (2, 0, 3), (2, 1, 32), (2, 3, 5), (3, 0, 1), (3, 1, 16), (3, 2, 5))` | `20` | `1` | `1` | `18` | `(1,)` | `7` | `0` |
| `'MIXED-j2--3-1'` | `'MIXED'` | `2` | `(-3, 1)` | `(10, 1, 1, 0)` | `(0, 1, 0, 7)` | `0` | `-3` | `(17, 32, 2, 4, 8)` | `20` | `((0, 1, 0), (0, 2, 2), (0, 3, 3), (0, 4, 1), (1, 0, 0), (1, 2, 1), (1, 3, 0), (1, 4, 7), (2, 0, 2), (2, 1, 1), (2, 3, 4), (2, 4, 2), (3, 0, 3), (3, 1, 0), (3, 2, 4), (3, 4, 5), (4, 0, 1), (4, 1, 7), (4, 2, 2), (4, 3, 5))` | `9` | `13` | `7` | `6` | `(7,)` | `13` | `0` |
| `'MIXED-j3--3-1'` | `'MIXED'` | `3` | `(-3, 1)` | `(10, 0, 1, 2)` | `(0, 1, 0, 7)` | `0` | `-2` | `(81, 34, 4, 8)` | `9` | `((0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 0, 2), (1, 2, 4), (1, 3, 9), (2, 0, 3), (2, 1, 4), (2, 3, 5), (3, 0, 1), (3, 1, 9), (3, 2, 5))` | `6` | `1` | `1` | `4` | `(1,)` | `7` | `0` |


For example, RICH-j1-0-1 has required family (3,0,1,4). Its constrained minimum cut is 6,
whereas unrestricted minimum cut is 0. Its residual minimum is 6-0-2=4, at original U=3.
A zero-valued unrestricted candidate would violate the family and cannot replace that value.

For every seam, changing only the retained network shift from C to C+17 and constant
from kappa to kappa-9 leaves the parity problem and mathematical result unchanged, and
changes recovered scalar by exactly -26. A future implementation must also preserve its
diagnostic output because query graphs and pair order are unchanged. This control does
not assert that the altered retained offsets arise from the same branch source expression.

## ORACLE-067 — Large integers, positive scaling, and zero-safe boundaries

**Classification:** `LOCAL_CONTRACT_FIXTURE`.
**Authority:** TEST_PLAN PC15--PC16, PC18.

For each listed k set L=2**k; arithmetic is exact. No decimal-to-float conversion, test
runtime threshold, or assertion of magnitude-independent bit cost is permitted.

### Fixture table: LARGE_EXPONENTS

| k |
| --- |
| `1` |
| `8` |
| `64` |
| `4096` |


**Fixed path scaling:** scale P06's capacities to 2L and 3L. Its constrained minimum is
3L, chosen problem shore 5, original shore 1, and required query count 3. The least
ordinary shores do not change. On this particular path and pair family the hand-traced
backend aggregates are `(3,3,8,3L)`; the fixed path makes those flat structural counters
justified. No flatness claim is made for arbitrary unrelated input families.

**Large contraction:** original n=2, family `(3,1,1,0)`, raw arcs:

```text
((2,0,L), (2,0,L+1), (0,1,L), (0,1,0), (1,3,L+2))
```

The first two records become loops, not capacity constraints. Canonical classes are
`(5,8,2)`, final terminal mask is 5, and reduced arcs are exactly
`((0,2,L),(2,1,L+2))`. Both geometric source shores preserve their raw cut value.
In particular the zero duplicate remains part of an encountered ordered pair before
aggregation, but is not materialized as a second problem arc.

The generic record validation admits high original-preimage bits only within its explicit
universe. Large numerical capacities never authorize enlarging that universe or expanding
multiplicities into copies. Empty arc inputs use the zero-safe flow carrier; no capacity
maximum is needed to manufacture an infinity bound.

## ORACLE-068 — Coverage, independent checking, and the completion boundary

**Classification:** `LOCAL_CONTRACT_FIXTURE` / audit ledger, not a global solver claim.

### Fixture table: FIXED_COUNTS

| metric | value |
| --- | --- |
| `'raw_networks'` | `6` |
| `'reduction_fixtures'` | `29` |
| `'feasible_reduction_fixtures'` | `22` |
| `'literal_lift_rows'` | `67` |
| `'problem_fixtures'` | `14` |
| `'problem_shore_rows'` | `51` |
| `'ordinary_trace_rows'` | `40` |
| `'arbitrary_tie_trap_rows'` | `21` |
| `'stats_anchors'` | `8` |
| `'seam_cases'` | `24` |
| `'rejection_declarations'` | `122` |
| `'valid_record_declarations'` | `14` |


| Prospective obligations | Catalogue evidence |
|---|---|
| PC1--PC4 record shapes and validation order | ORACLE-056--058 |
| PC5--PC9 contraction, XOR, toggle, lifting, correspondence | ORACLE-057--059, ORACLE-065 |
| PC10 zero/infeasible and standalone boundary | ORACLE-060, ORACLE-063--065 |
| PC11--PC14 pair coordinates, least minimizers, exact deterministic optimum | ORACLE-060--062, ORACLE-064 |
| PC15--PC16 separate stats, zero-safe and scaled cases | ORACLE-063--064, ORACLE-067 |
| PC17 source-residual seam and preserved offsets | ORACLE-066 |
| PC18--PC19 isolation, structure, nonmutation and negative controls | This entry plus all audit bindings |
| PC20 narrow conformance, future branch/certificate boundaries | This entry |

The package's independent definition-level audit imports no production, verifier, flow,
consuming tests, or external graph library. It verifies the historical catalogue prefix,
every fixed human table against its JSON transcription, direct finite objective minima,
GR least-query candidate equivalence, terminal/forcing bijections, and input nonmutation.
Counter declarations and shape rejection declarations are distinct from production execution.
A separate optional compatibility check of the already-closed flow backend is reported
separately and never supplies expected parity values.

Future tests must verify validation phase order, actual minimum_cut invocation counts,
actual FlowStats sums, input nonmutation, immutable record behavior, and source/import/work
restrictions. No production all-shore enumeration is authorized by using it in these oracles.
In-memory audit mutations must reject changed classes, terminal XOR/toggle mistakes, lost
zero pairs/opposite arcs, wrong temporary/base lifting, wrong least minimizers, wrong ties,
wrong None handling, incorrect fixed counts, and shift mistakes without editing live source.

Only after implementation GREEN, full independent auditing, and frozen-test satisfaction
may PC20 add the narrowly scoped lem:parity-anchor and thm:GR rows plus an engineering note.
Existing lem:ek, lem:sign-routing, and all previous conformance statuses remain unchanged at
this oracle step. Complete thm:branch-oracle, outer solvers, witness and certificate claims,
and global bit-growth/experiments are not discharged by these finite fixtures.

**Unit 11 oracle status:** expected values derived from pinned mathematical definitions
and the adopted DESIGN/TEST_PLAN, independently checked before `tests/test_parity_cut.py`
or `exactfrac/parity_cut.py` exists. No Unit 11 production or consuming-test code is
created, staged, committed, or treated as an authority by this catalogue addition.

## ORACLE-069 — Unit 12 canonical inputs and unreduced query parameters

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

Governing mathematics: `prop:branch-transform`, `prop:domain-decomp`, `alg:branch-min`,
`thm:branch-oracle`. Engineering authority: DESIGN §4.9 and TEST_PLAN BO1--BO22.
The authority commit is `bc98c0cd73669ccddb0c2b30cb934ebc02403a58`.
These fixtures precede `tests/test_oracle.py` and `exactfrac/oracle.py`.

Every INPUTS row is a canonical active Instance; labels=None. RICH is the existing
ORACLE-025 instance and MIXED is the existing ORACLE-031 instance. No historical input
is changed. EQUALITY means f equals d_q at every vertex. TIECARD also has this equality
but different shore cardinalities can share the same f-sum. ODDFULL has odd total f
and more than one high-end forced-vertex family.

All parameters are raw exact integer pairs. Do not normalize (0,3) to (0,1), reject
negative numerators, or compare raw residuals at different B without cross-scaling.
A query id `NAME-jJ-pP` uses the INPUTS name, branch J, and PARAMETERS index P.

### Fixture table: INPUTS

| name | n | edges | f | d_q | Q |
| --- | --- | --- | --- | --- | --- |
| `'Q1'` | `2` | `((0, 1, 1),)` | `(1, 1)` | `(1, 1)` | `1` |
| `'DOUBLE'` | `2` | `((0, 1, 2),)` | `(1, 1)` | `(2, 2)` | `2` |
| `'UNEQUAL'` | `2` | `((0, 1, 2),)` | `(2, 1)` | `(2, 2)` | `2` |
| `'EQUALITY'` | `3` | `((0, 1, 1), (0, 2, 1), (1, 2, 1))` | `(2, 2, 2)` | `(2, 2, 2)` | `3` |
| `'WTRI'` | `3` | `((0, 1, 1), (0, 2, 1), (1, 2, 1))` | `(1, 1, 1)` | `(2, 2, 2)` | `3` |
| `'ODDFULL'` | `3` | `((0, 1, 1), (0, 2, 1), (1, 2, 1))` | `(2, 2, 1)` | `(2, 2, 2)` | `3` |
| `'TIECARD'` | `3` | `((0, 2, 1), (1, 2, 1))` | `(1, 1, 2)` | `(1, 1, 2)` | `2` |
| `'RICH'` | `5` | `((0, 2, 2), (1, 2, 2), (2, 4, 1), (3, 4, 1))` | `(1, 1, 1, 1, 2)` | `(2, 2, 5, 1, 2)` | `6` |
| `'MIXED'` | `4` | `((0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 4), (1, 3, 2), (2, 3, 5))` | `(2, 3, 4, 5)` | `(6, 8, 12, 8)` | `17` |

### Fixture table: PARAMETERS

| index | raw_parameter |
| --- | --- |
| `0` | `(-5, 2)` |
| `1` | `(-2, 1)` |
| `2` | `(-1, 1)` |
| `3` | `(0, 1)` |
| `4` | `(0, 3)` |
| `5` | `(1, 2)` |
| `6` | `(1, 1)` |
| `7` | `(2, 1)` |
| `8` | `(3, 2)` |
| `9` | `(7, 3)` |



## ORACLE-070 — Complete ordered covers, preparation, and empty descriptors

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO2, BO6--BO8, BO16, BO20. Family tuples are (T,pi,I,O) in original-vertex masks.
Their order is the previously ruled source order: D0 singleton; D1 increasing p then
edge_ref then forward/reverse orientation; D2 increasing f>=2 vertex then increasing
triples from f=1; D3 edge_ref then orientation. Retain duplicates and empty descriptors.
The FAMILIES table lists EVERY descriptor and all its original members, in increasing
mask order. Geometric overlap and even/odd impossibility are both genuine empty cases.

The four count-prefix entries are examined, feasible, parity calls, ordinary cut calls.
They are not four flow-stat fields. For feasible F the reduced N_F has one source,
one sink, and one class for each free original vertex; the anchor merges into source.
The ordinary count is the sum of N_F^2-3*N_F+3. These are prescribed reference-policy
counts, not observed production Unit 12 calls. R_all is paid once in context preparation.
A context constructor accepts only Instance and retains its complete generated cover;
an externally supplied clipped, sorted, or deduplicated cover is not a permitted API.

### Fixture table: COVERS

| instance | j | R_all | examined_feasible_parity_ordinary | network_builds_per_query | N_F_in_feasible_order |
| --- | --- | --- | --- | --- | --- |
| `'Q1'` | `0` | `3` | `(1, 0, 0, 0)` | `0` | `()` |
| `'Q1'` | `1` | `3` | `(0, 0, 0, 0)` | `0` | `()` |
| `'Q1'` | `2` | `3` | `(0, 0, 0, 0)` | `0` | `()` |
| `'Q1'` | `3` | `3` | `(2, 0, 0, 0)` | `0` | `()` |
| `'DOUBLE'` | `0` | `7` | `(1, 1, 1, 7)` | `1` | `(4,)` |
| `'DOUBLE'` | `1` | `7` | `(4, 0, 0, 0)` | `0` | `()` |
| `'DOUBLE'` | `2` | `7` | `(0, 0, 0, 0)` | `0` | `()` |
| `'DOUBLE'` | `3` | `7` | `(2, 0, 0, 0)` | `0` | `()` |
| `'UNEQUAL'` | `0` | `6` | `(1, 1, 1, 7)` | `1` | `(4,)` |
| `'UNEQUAL'` | `1` | `6` | `(2, 0, 0, 0)` | `0` | `()` |
| `'UNEQUAL'` | `2` | `6` | `(1, 1, 1, 3)` | `1` | `(3,)` |
| `'UNEQUAL'` | `3` | `6` | `(2, 1, 1, 1)` | `1` | `(2,)` |
| `'EQUALITY'` | `0` | `10` | `(1, 0, 0, 0)` | `0` | `()` |
| `'EQUALITY'` | `1` | `10` | `(0, 0, 0, 0)` | `0` | `()` |
| `'EQUALITY'` | `2` | `10` | `(3, 0, 0, 0)` | `0` | `()` |
| `'EQUALITY'` | `3` | `10` | `(6, 6, 6, 18)` | `1` | `(3, 3, 3, 3, 3, 3)` |
| `'WTRI'` | `0` | `26` | `(1, 1, 1, 13)` | `1` | `(5,)` |
| `'WTRI'` | `1` | `26` | `(18, 12, 12, 24)` | `1` | `(3, 3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 3)` |
| `'WTRI'` | `2` | `26` | `(1, 1, 1, 1)` | `1` | `(2,)` |
| `'WTRI'` | `3` | `26` | `(6, 6, 6, 18)` | `1` | `(3, 3, 3, 3, 3, 3)` |
| `'ODDFULL'` | `0` | `15` | `(1, 1, 1, 13)` | `1` | `(5,)` |
| `'ODDFULL'` | `1` | `15` | `(6, 0, 0, 0)` | `0` | `()` |
| `'ODDFULL'` | `2` | `15` | `(2, 2, 2, 14)` | `1` | `(4, 4)` |
| `'ODDFULL'` | `3` | `15` | `(6, 4, 4, 12)` | `1` | `(3, 3, 3, 3)` |
| `'TIECARD'` | `0` | `6` | `(1, 0, 0, 0)` | `0` | `()` |
| `'TIECARD'` | `1` | `6` | `(0, 0, 0, 0)` | `0` | `()` |
| `'TIECARD'` | `2` | `6` | `(1, 1, 1, 7)` | `1` | `(4,)` |
| `'TIECARD'` | `3` | `6` | `(4, 4, 4, 12)` | `1` | `(3, 3, 3, 3)` |
| `'RICH'` | `0` | `38` | `(1, 1, 1, 31)` | `1` | `(7,)` |
| `'RICH'` | `1` | `38` | `(24, 17, 17, 149)` | `1` | `(5, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 5, 5, 5, 4, 4)` |
| `'RICH'` | `2` | `38` | `(5, 5, 5, 49)` | `1` | `(6, 4, 4, 4, 4)` |
| `'RICH'` | `3` | `38` | `(8, 8, 8, 104)` | `1` | `(5, 5, 5, 5, 5, 5, 5, 5)` |
| `'MIXED'` | `0` | `65` | `(1, 1, 1, 21)` | `1` | `(6,)` |
| `'MIXED'` | `1` | `65` | `(48, 26, 26, 118)` | `1` | `(4, 4, 4, 3, 3, 3, 3, 4, 3, 3, 3, 4, 3, 3, 3, 4, 3, 3, 4, 4, 3, 3, 3, 4, 3, 4)` |
| `'MIXED'` | `2` | `65` | `(4, 4, 4, 52)` | `1` | `(5, 5, 5, 5)` |
| `'MIXED'` | `3` | `65` | `(12, 10, 10, 70)` | `1` | `(4, 4, 4, 4, 4, 4, 4, 4, 4, 4)` |

### Fixture table: FAMILIES

| instance | j | index | T_pi_I_O | nonempty | all_original_members |
| --- | --- | --- | --- | --- | --- |
| `'Q1'` | `0` | `0` | `(0, 1, 0, 0)` | `False` | `()` |
| `'Q1'` | `3` | `0` | `(3, 0, 1, 2)` | `False` | `()` |
| `'Q1'` | `3` | `1` | `(3, 0, 2, 1)` | `False` | `()` |
| `'DOUBLE'` | `0` | `0` | `(3, 1, 0, 0)` | `True` | `(1, 2)` |
| `'DOUBLE'` | `1` | `0` | `(3, 0, 1, 2)` | `False` | `()` |
| `'DOUBLE'` | `1` | `1` | `(3, 0, 3, 1)` | `False` | `()` |
| `'DOUBLE'` | `1` | `2` | `(3, 0, 3, 2)` | `False` | `()` |
| `'DOUBLE'` | `1` | `3` | `(3, 0, 2, 1)` | `False` | `()` |
| `'DOUBLE'` | `3` | `0` | `(3, 0, 1, 2)` | `False` | `()` |
| `'DOUBLE'` | `3` | `1` | `(3, 0, 2, 1)` | `False` | `()` |
| `'UNEQUAL'` | `0` | `0` | `(2, 1, 0, 0)` | `True` | `(2, 3)` |
| `'UNEQUAL'` | `1` | `0` | `(2, 0, 3, 2)` | `False` | `()` |
| `'UNEQUAL'` | `1` | `1` | `(2, 0, 2, 1)` | `False` | `()` |
| `'UNEQUAL'` | `2` | `0` | `(2, 1, 1, 0)` | `True` | `(3,)` |
| `'UNEQUAL'` | `3` | `0` | `(2, 0, 1, 2)` | `True` | `(1,)` |
| `'UNEQUAL'` | `3` | `1` | `(2, 0, 2, 1)` | `False` | `()` |
| `'EQUALITY'` | `0` | `0` | `(0, 1, 0, 0)` | `False` | `()` |
| `'EQUALITY'` | `2` | `0` | `(0, 1, 1, 0)` | `False` | `()` |
| `'EQUALITY'` | `2` | `1` | `(0, 1, 2, 0)` | `False` | `()` |
| `'EQUALITY'` | `2` | `2` | `(0, 1, 4, 0)` | `False` | `()` |
| `'EQUALITY'` | `3` | `0` | `(0, 0, 1, 2)` | `True` | `(1, 5)` |
| `'EQUALITY'` | `3` | `1` | `(0, 0, 2, 1)` | `True` | `(2, 6)` |
| `'EQUALITY'` | `3` | `2` | `(0, 0, 1, 4)` | `True` | `(1, 3)` |
| `'EQUALITY'` | `3` | `3` | `(0, 0, 4, 1)` | `True` | `(4, 6)` |
| `'EQUALITY'` | `3` | `4` | `(0, 0, 2, 4)` | `True` | `(2, 3)` |
| `'EQUALITY'` | `3` | `5` | `(0, 0, 4, 2)` | `True` | `(4, 5)` |
| `'WTRI'` | `0` | `0` | `(7, 1, 0, 0)` | `True` | `(1, 2, 4, 7)` |
| `'WTRI'` | `1` | `0` | `(7, 0, 1, 2)` | `True` | `(5,)` |
| `'WTRI'` | `1` | `1` | `(7, 0, 3, 1)` | `False` | `()` |
| `'WTRI'` | `1` | `2` | `(7, 0, 1, 4)` | `True` | `(3,)` |
| `'WTRI'` | `1` | `3` | `(7, 0, 5, 1)` | `False` | `()` |
| `'WTRI'` | `1` | `4` | `(7, 0, 3, 4)` | `True` | `(3,)` |
| `'WTRI'` | `1` | `5` | `(7, 0, 5, 2)` | `True` | `(5,)` |
| `'WTRI'` | `1` | `6` | `(7, 0, 3, 2)` | `False` | `()` |
| `'WTRI'` | `1` | `7` | `(7, 0, 2, 1)` | `True` | `(6,)` |
| `'WTRI'` | `1` | `8` | `(7, 0, 3, 4)` | `True` | `(3,)` |
| `'WTRI'` | `1` | `9` | `(7, 0, 6, 1)` | `True` | `(6,)` |
| `'WTRI'` | `1` | `10` | `(7, 0, 2, 4)` | `True` | `(3,)` |
| `'WTRI'` | `1` | `11` | `(7, 0, 6, 2)` | `False` | `()` |
| `'WTRI'` | `1` | `12` | `(7, 0, 5, 2)` | `True` | `(5,)` |
| `'WTRI'` | `1` | `13` | `(7, 0, 6, 1)` | `True` | `(6,)` |
| `'WTRI'` | `1` | `14` | `(7, 0, 5, 4)` | `False` | `()` |
| `'WTRI'` | `1` | `15` | `(7, 0, 4, 1)` | `True` | `(6,)` |
| `'WTRI'` | `1` | `16` | `(7, 0, 6, 4)` | `False` | `()` |
| `'WTRI'` | `1` | `17` | `(7, 0, 4, 2)` | `True` | `(5,)` |
| `'WTRI'` | `2` | `0` | `(7, 1, 7, 0)` | `True` | `(7,)` |
| `'WTRI'` | `3` | `0` | `(7, 0, 1, 2)` | `True` | `(5,)` |
| `'WTRI'` | `3` | `1` | `(7, 0, 2, 1)` | `True` | `(6,)` |
| `'WTRI'` | `3` | `2` | `(7, 0, 1, 4)` | `True` | `(3,)` |
| `'WTRI'` | `3` | `3` | `(7, 0, 4, 1)` | `True` | `(6,)` |
| `'WTRI'` | `3` | `4` | `(7, 0, 2, 4)` | `True` | `(3,)` |
| `'WTRI'` | `3` | `5` | `(7, 0, 4, 2)` | `True` | `(5,)` |
| `'ODDFULL'` | `0` | `0` | `(4, 1, 0, 0)` | `True` | `(4, 5, 6, 7)` |
| `'ODDFULL'` | `1` | `0` | `(4, 0, 5, 2)` | `False` | `()` |
| `'ODDFULL'` | `1` | `1` | `(4, 0, 6, 1)` | `False` | `()` |
| `'ODDFULL'` | `1` | `2` | `(4, 0, 5, 4)` | `False` | `()` |
| `'ODDFULL'` | `1` | `3` | `(4, 0, 4, 1)` | `False` | `()` |
| `'ODDFULL'` | `1` | `4` | `(4, 0, 6, 4)` | `False` | `()` |
| `'ODDFULL'` | `1` | `5` | `(4, 0, 4, 2)` | `False` | `()` |
| `'ODDFULL'` | `2` | `0` | `(4, 1, 1, 0)` | `True` | `(5, 7)` |
| `'ODDFULL'` | `2` | `1` | `(4, 1, 2, 0)` | `True` | `(6, 7)` |
| `'ODDFULL'` | `3` | `0` | `(4, 0, 1, 2)` | `True` | `(1,)` |
| `'ODDFULL'` | `3` | `1` | `(4, 0, 2, 1)` | `True` | `(2,)` |
| `'ODDFULL'` | `3` | `2` | `(4, 0, 1, 4)` | `True` | `(1, 3)` |
| `'ODDFULL'` | `3` | `3` | `(4, 0, 4, 1)` | `False` | `()` |
| `'ODDFULL'` | `3` | `4` | `(4, 0, 2, 4)` | `True` | `(2, 3)` |
| `'ODDFULL'` | `3` | `5` | `(4, 0, 4, 2)` | `False` | `()` |
| `'TIECARD'` | `0` | `0` | `(0, 1, 0, 0)` | `False` | `()` |
| `'TIECARD'` | `2` | `0` | `(3, 1, 4, 0)` | `True` | `(5, 6)` |
| `'TIECARD'` | `3` | `0` | `(3, 0, 1, 4)` | `True` | `(3,)` |
| `'TIECARD'` | `3` | `1` | `(3, 0, 4, 1)` | `True` | `(4,)` |
| `'TIECARD'` | `3` | `2` | `(3, 0, 2, 4)` | `True` | `(3,)` |
| `'TIECARD'` | `3` | `3` | `(3, 0, 4, 2)` | `True` | `(4,)` |
| `'RICH'` | `0` | `0` | `(3, 1, 0, 0)` | `True` | `(1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, 30)` |
| `'RICH'` | `1` | `0` | `(3, 0, 1, 4)` | `True` | `(3, 11, 19, 27)` |
| `'RICH'` | `1` | `1` | `(3, 0, 5, 1)` | `False` | `()` |
| `'RICH'` | `1` | `2` | `(3, 0, 3, 4)` | `True` | `(3, 11, 19, 27)` |
| `'RICH'` | `1` | `3` | `(3, 0, 5, 2)` | `False` | `()` |
| `'RICH'` | `1` | `4` | `(3, 0, 5, 16)` | `True` | `(7, 15)` |
| `'RICH'` | `1` | `5` | `(3, 0, 17, 4)` | `True` | `(19, 27)` |
| `'RICH'` | `1` | `6` | `(3, 0, 9, 16)` | `True` | `(11, 15)` |
| `'RICH'` | `1` | `7` | `(3, 0, 17, 8)` | `True` | `(19, 23)` |
| `'RICH'` | `1` | `8` | `(3, 0, 3, 4)` | `True` | `(3, 11, 19, 27)` |
| `'RICH'` | `1` | `9` | `(3, 0, 6, 1)` | `False` | `()` |
| `'RICH'` | `1` | `10` | `(3, 0, 2, 4)` | `True` | `(3, 11, 19, 27)` |
| `'RICH'` | `1` | `11` | `(3, 0, 6, 2)` | `False` | `()` |
| `'RICH'` | `1` | `12` | `(3, 0, 6, 16)` | `True` | `(7, 15)` |
| `'RICH'` | `1` | `13` | `(3, 0, 18, 4)` | `True` | `(19, 27)` |
| `'RICH'` | `1` | `14` | `(3, 0, 10, 16)` | `True` | `(11, 15)` |
| `'RICH'` | `1` | `15` | `(3, 0, 18, 8)` | `True` | `(19, 23)` |
| `'RICH'` | `1` | `16` | `(3, 0, 5, 4)` | `False` | `()` |
| `'RICH'` | `1` | `17` | `(3, 0, 4, 1)` | `True` | `(4, 12, 20, 28)` |
| `'RICH'` | `1` | `18` | `(3, 0, 6, 4)` | `False` | `()` |
| `'RICH'` | `1` | `19` | `(3, 0, 4, 2)` | `True` | `(4, 12, 20, 28)` |
| `'RICH'` | `1` | `20` | `(3, 0, 4, 16)` | `True` | `(4, 7, 12, 15)` |
| `'RICH'` | `1` | `21` | `(3, 0, 20, 4)` | `False` | `()` |
| `'RICH'` | `1` | `22` | `(3, 0, 12, 16)` | `True` | `(12, 15)` |
| `'RICH'` | `1` | `23` | `(3, 0, 20, 8)` | `True` | `(20, 23)` |
| `'RICH'` | `2` | `0` | `(15, 1, 16, 0)` | `True` | `(17, 18, 20, 23, 24, 27, 29, 30)` |
| `'RICH'` | `2` | `1` | `(15, 1, 7, 0)` | `True` | `(7, 23)` |
| `'RICH'` | `2` | `2` | `(15, 1, 11, 0)` | `True` | `(11, 27)` |
| `'RICH'` | `2` | `3` | `(15, 1, 13, 0)` | `True` | `(13, 29)` |
| `'RICH'` | `2` | `4` | `(15, 1, 14, 0)` | `True` | `(14, 30)` |
| `'RICH'` | `3` | `0` | `(15, 0, 1, 4)` | `True` | `(3, 9, 19, 25)` |
| `'RICH'` | `3` | `1` | `(15, 0, 4, 1)` | `True` | `(6, 12, 22, 28)` |
| `'RICH'` | `3` | `2` | `(15, 0, 2, 4)` | `True` | `(3, 10, 19, 26)` |
| `'RICH'` | `3` | `3` | `(15, 0, 4, 2)` | `True` | `(5, 12, 21, 28)` |
| `'RICH'` | `3` | `4` | `(15, 0, 4, 16)` | `True` | `(5, 6, 12, 15)` |
| `'RICH'` | `3` | `5` | `(15, 0, 16, 4)` | `True` | `(16, 19, 25, 26)` |
| `'RICH'` | `3` | `6` | `(15, 0, 8, 16)` | `True` | `(9, 10, 12, 15)` |
| `'RICH'` | `3` | `7` | `(15, 0, 16, 8)` | `True` | `(16, 19, 21, 22)` |
| `'MIXED'` | `0` | `0` | `(10, 1, 0, 0)` | `True` | `(2, 3, 6, 7, 8, 9, 12, 13)` |
| `'MIXED'` | `1` | `0` | `(10, 0, 1, 2)` | `True` | `(1, 5)` |
| `'MIXED'` | `1` | `1` | `(10, 0, 3, 1)` | `False` | `()` |
| `'MIXED'` | `1` | `2` | `(10, 0, 1, 4)` | `True` | `(1, 11)` |
| `'MIXED'` | `1` | `3` | `(10, 0, 5, 1)` | `False` | `()` |
| `'MIXED'` | `1` | `4` | `(10, 0, 1, 8)` | `True` | `(1, 5)` |
| `'MIXED'` | `1` | `5` | `(10, 0, 9, 1)` | `False` | `()` |
| `'MIXED'` | `1` | `6` | `(10, 0, 3, 4)` | `True` | `(11,)` |
| `'MIXED'` | `1` | `7` | `(10, 0, 5, 2)` | `True` | `(5,)` |
| `'MIXED'` | `1` | `8` | `(10, 0, 3, 8)` | `False` | `()` |
| `'MIXED'` | `1` | `9` | `(10, 0, 9, 2)` | `False` | `()` |
| `'MIXED'` | `1` | `10` | `(10, 0, 5, 8)` | `True` | `(5,)` |
| `'MIXED'` | `1` | `11` | `(10, 0, 9, 4)` | `True` | `(11,)` |
| `'MIXED'` | `1` | `12` | `(10, 0, 3, 2)` | `False` | `()` |
| `'MIXED'` | `1` | `13` | `(10, 0, 2, 1)` | `True` | `(10, 14)` |
| `'MIXED'` | `1` | `14` | `(10, 0, 3, 4)` | `True` | `(11,)` |
| `'MIXED'` | `1` | `15` | `(10, 0, 6, 1)` | `True` | `(14,)` |
| `'MIXED'` | `1` | `16` | `(10, 0, 3, 8)` | `False` | `()` |
| `'MIXED'` | `1` | `17` | `(10, 0, 10, 1)` | `True` | `(10, 14)` |
| `'MIXED'` | `1` | `18` | `(10, 0, 2, 4)` | `True` | `(10, 11)` |
| `'MIXED'` | `1` | `19` | `(10, 0, 6, 2)` | `False` | `()` |
| `'MIXED'` | `1` | `20` | `(10, 0, 2, 8)` | `False` | `()` |
| `'MIXED'` | `1` | `21` | `(10, 0, 10, 2)` | `False` | `()` |
| `'MIXED'` | `1` | `22` | `(10, 0, 6, 8)` | `False` | `()` |
| `'MIXED'` | `1` | `23` | `(10, 0, 10, 4)` | `True` | `(10, 11)` |
| `'MIXED'` | `1` | `24` | `(10, 0, 5, 2)` | `True` | `(5,)` |
| `'MIXED'` | `1` | `25` | `(10, 0, 6, 1)` | `True` | `(14,)` |
| `'MIXED'` | `1` | `26` | `(10, 0, 5, 4)` | `False` | `()` |
| `'MIXED'` | `1` | `27` | `(10, 0, 4, 1)` | `True` | `(4, 14)` |
| `'MIXED'` | `1` | `28` | `(10, 0, 5, 8)` | `True` | `(5,)` |
| `'MIXED'` | `1` | `29` | `(10, 0, 12, 1)` | `True` | `(14,)` |
| `'MIXED'` | `1` | `30` | `(10, 0, 6, 4)` | `False` | `()` |
| `'MIXED'` | `1` | `31` | `(10, 0, 4, 2)` | `True` | `(4, 5)` |
| `'MIXED'` | `1` | `32` | `(10, 0, 6, 8)` | `False` | `()` |
| `'MIXED'` | `1` | `33` | `(10, 0, 12, 2)` | `False` | `()` |
| `'MIXED'` | `1` | `34` | `(10, 0, 4, 8)` | `True` | `(4, 5)` |
| `'MIXED'` | `1` | `35` | `(10, 0, 12, 4)` | `False` | `()` |
| `'MIXED'` | `1` | `36` | `(10, 0, 9, 2)` | `False` | `()` |
| `'MIXED'` | `1` | `37` | `(10, 0, 10, 1)` | `True` | `(10, 14)` |
| `'MIXED'` | `1` | `38` | `(10, 0, 9, 4)` | `True` | `(11,)` |
| `'MIXED'` | `1` | `39` | `(10, 0, 12, 1)` | `True` | `(14,)` |
| `'MIXED'` | `1` | `40` | `(10, 0, 9, 8)` | `False` | `()` |
| `'MIXED'` | `1` | `41` | `(10, 0, 8, 1)` | `True` | `(10, 14)` |
| `'MIXED'` | `1` | `42` | `(10, 0, 10, 4)` | `True` | `(10, 11)` |
| `'MIXED'` | `1` | `43` | `(10, 0, 12, 2)` | `False` | `()` |
| `'MIXED'` | `1` | `44` | `(10, 0, 10, 8)` | `False` | `()` |
| `'MIXED'` | `1` | `45` | `(10, 0, 8, 2)` | `False` | `()` |
| `'MIXED'` | `1` | `46` | `(10, 0, 12, 8)` | `False` | `()` |
| `'MIXED'` | `1` | `47` | `(10, 0, 8, 4)` | `True` | `(10, 11)` |
| `'MIXED'` | `2` | `0` | `(10, 1, 1, 0)` | `True` | `(3, 7, 9, 13)` |
| `'MIXED'` | `2` | `1` | `(10, 1, 2, 0)` | `True` | `(2, 3, 6, 7)` |
| `'MIXED'` | `2` | `2` | `(10, 1, 4, 0)` | `True` | `(6, 7, 12, 13)` |
| `'MIXED'` | `2` | `3` | `(10, 1, 8, 0)` | `True` | `(8, 9, 12, 13)` |
| `'MIXED'` | `3` | `0` | `(10, 0, 1, 2)` | `True` | `(1, 5)` |
| `'MIXED'` | `3` | `1` | `(10, 0, 2, 1)` | `True` | `(10, 14)` |
| `'MIXED'` | `3` | `2` | `(10, 0, 1, 4)` | `True` | `(1, 11)` |
| `'MIXED'` | `3` | `3` | `(10, 0, 4, 1)` | `True` | `(4, 14)` |
| `'MIXED'` | `3` | `4` | `(10, 0, 1, 8)` | `True` | `(1, 5)` |
| `'MIXED'` | `3` | `5` | `(10, 0, 8, 1)` | `True` | `(10, 14)` |
| `'MIXED'` | `3` | `6` | `(10, 0, 2, 4)` | `True` | `(10, 11)` |
| `'MIXED'` | `3` | `7` | `(10, 0, 4, 2)` | `True` | `(4, 5)` |
| `'MIXED'` | `3` | `8` | `(10, 0, 2, 8)` | `False` | `()` |
| `'MIXED'` | `3` | `9` | `(10, 0, 8, 2)` | `False` | `()` |
| `'MIXED'` | `3` | `10` | `(10, 0, 4, 8)` | `True` | `(4, 5)` |
| `'MIXED'` | `3` | `11` | `(10, 0, 8, 4)` | `True` | `(10, 11)` |



## ORACLE-071 — Original branch domains and raw c/h before minimization

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO4--BO5, BO11. For every original shore let s=sum(f on U), b=sum(q across U),
and d=sum(d_q on U). The literal domains/forms are:

| j | original domain | c | h |
| --- | --- | --- | --- |
| 0 | s+b odd | s+b-1 | d+1-s |
| 1 | s+b even, b>=1, d>s | s+b-2 | d-s |
| 2 | s odd and s>=3 | b-d | s-1 |
| 3 | s even and b>=1 | b-d-2 | s |

Each DOMAINS cell lists every (U,c,h) in its branch. Empty U is absent from all four;
full U remains allowed whenever its domain condition holds. All listed h are positive.
No witness-admissibility or stronger endpoint filter is inserted. c/h is not reduced,
and this stage does not minimize that ratio. Expected sums are derived from original
records, never from production helpers, family output, network gamma, or cut results.

### Fixture table: DOMAINS

| instance | j | all_original_U_c_h |
| --- | --- | --- |
| `'Q1'` | `0` | `()` |
| `'Q1'` | `1` | `()` |
| `'Q1'` | `2` | `()` |
| `'Q1'` | `3` | `()` |
| `'DOUBLE'` | `0` | `((1, 2, 2), (2, 2, 2))` |
| `'DOUBLE'` | `1` | `()` |
| `'DOUBLE'` | `2` | `()` |
| `'DOUBLE'` | `3` | `()` |
| `'UNEQUAL'` | `0` | `((2, 2, 2), (3, 2, 2))` |
| `'UNEQUAL'` | `1` | `()` |
| `'UNEQUAL'` | `2` | `((3, -4, 2),)` |
| `'UNEQUAL'` | `3` | `((1, -2, 2),)` |
| `'EQUALITY'` | `0` | `()` |
| `'EQUALITY'` | `1` | `()` |
| `'EQUALITY'` | `2` | `()` |
| `'EQUALITY'` | `3` | `((1, -2, 2), (2, -2, 2), (3, -4, 4), (4, -2, 2), (5, -4, 4), (6, -4, 4))` |
| `'WTRI'` | `0` | `((1, 2, 2), (2, 2, 2), (4, 2, 2), (7, 2, 4))` |
| `'WTRI'` | `1` | `((3, 2, 2), (5, 2, 2), (6, 2, 2))` |
| `'WTRI'` | `2` | `((7, -6, 2),)` |
| `'WTRI'` | `3` | `((3, -4, 2), (5, -4, 2), (6, -4, 2))` |
| `'ODDFULL'` | `0` | `((4, 2, 2), (5, 4, 2), (6, 4, 2), (7, 4, 2))` |
| `'ODDFULL'` | `1` | `()` |
| `'ODDFULL'` | `2` | `((5, -2, 2), (6, -2, 2), (7, -6, 4))` |
| `'ODDFULL'` | `3` | `((1, -2, 2), (2, -2, 2), (3, -4, 4))` |
| `'TIECARD'` | `0` | `()` |
| `'TIECARD'` | `1` | `()` |
| `'TIECARD'` | `2` | `((5, -2, 2), (6, -2, 2))` |
| `'TIECARD'` | `3` | `((3, -2, 2), (4, -2, 2))` |
| `'RICH'` | `0` | `((1, 2, 2), (2, 2, 2), (5, 4, 6), (6, 4, 6), (9, 4, 2), (10, 4, 2), (13, 6, 6), (14, 6, 6), (17, 6, 2), (18, 6, 2), (21, 6, 6), (22, 6, 6), (25, 6, 2), (26, 6, 2), (29, 6, 6), (30, 6, 6))` |
| `'RICH'` | `1` | `((3, 4, 2), (4, 4, 4), (7, 2, 6), (11, 6, 2), (12, 6, 4), (15, 4, 6), (19, 8, 2), (20, 6, 4), (23, 4, 6), (27, 8, 2), (28, 6, 4))` |
| `'RICH'` | `2` | `((7, -8, 2), (11, 0, 2), (13, -4, 2), (14, -4, 2), (17, 0, 2), (18, 0, 2), (20, -2, 2), (23, -10, 4), (24, -2, 2), (27, -2, 4), (29, -8, 4), (30, -8, 4))` |
| `'RICH'` | `3` | `((3, -2, 2), (5, -6, 2), (6, -6, 2), (9, -2, 2), (10, -2, 2), (12, -2, 2), (15, -10, 4), (16, -2, 2), (19, -2, 4), (21, -8, 4), (22, -8, 4), (25, -4, 4), (26, -4, 4), (28, -6, 4))` |
| `'MIXED'` | `0` | `((2, 10, 6), (3, 14, 10), (6, 18, 14), (7, 16, 18), (8, 12, 4), (9, 18, 8), (12, 18, 12), (13, 18, 16))` |
| `'MIXED'` | `1` | `((1, 6, 4), (4, 14, 8), (5, 16, 12), (10, 18, 8), (11, 20, 12), (14, 16, 16))` |
| `'MIXED'` | `2` | `((2, 0, 2), (3, -4, 4), (6, -8, 6), (7, -18, 8), (8, 0, 4), (9, -2, 6), (12, -10, 8), (13, -18, 10))` |
| `'MIXED'` | `3` | `((1, -2, 2), (4, -2, 4), (5, -8, 6), (10, -6, 8), (11, -12, 10), (14, -24, 12))` |



## ORACLE-072 — Fixed-parameter exact minima and deterministic winners

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO5--BO7, BO13--BO15. MINIMA fixes 360 queries: nine inputs, four branches, ten
parameters. The result is (original U,c,h,raw) with raw=B*c-A*h. None means the source
domain is empty. The mathematical argmin masks are listed separately from the selected
engineering winner and its first-retained family index. Mathematics permits any exact
argmin; the specific winner here follows the shipped least-ORDINARY-cut GR policy and
strict family-level improvement. It is not a least-parity or least-branch claim.

C_minus_if_built and constant_if_built are None for all-empty queries: no coefficient
or original network is built there. A zero residual, negative residual, or zero cut is
not an infeasible result. Q1 at every parameter has four empty branches despite active
input; D0 and D3 retain examined descriptors while D1 and D2 have zero descriptors.

### Fixture table: MINIMA

| query | instance | j | A_B | U_c_h_raw_or_None | all_math_argmins | winning_family | examined_feasible_parity_ordinary | C_minus_if_built | constant_if_built |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `'Q1-j0-p0'` | `'Q1'` | `0` | `(-5, 2)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'Q1-j0-p1'` | `'Q1'` | `0` | `(-2, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'Q1-j0-p2'` | `'Q1'` | `0` | `(-1, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'Q1-j0-p3'` | `'Q1'` | `0` | `(0, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'Q1-j0-p4'` | `'Q1'` | `0` | `(0, 3)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'Q1-j0-p5'` | `'Q1'` | `0` | `(1, 2)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'Q1-j0-p6'` | `'Q1'` | `0` | `(1, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'Q1-j0-p7'` | `'Q1'` | `0` | `(2, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'Q1-j0-p8'` | `'Q1'` | `0` | `(3, 2)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'Q1-j0-p9'` | `'Q1'` | `0` | `(7, 3)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'Q1-j1-p0'` | `'Q1'` | `1` | `(-5, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j1-p1'` | `'Q1'` | `1` | `(-2, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j1-p2'` | `'Q1'` | `1` | `(-1, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j1-p3'` | `'Q1'` | `1` | `(0, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j1-p4'` | `'Q1'` | `1` | `(0, 3)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j1-p5'` | `'Q1'` | `1` | `(1, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j1-p6'` | `'Q1'` | `1` | `(1, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j1-p7'` | `'Q1'` | `1` | `(2, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j1-p8'` | `'Q1'` | `1` | `(3, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j1-p9'` | `'Q1'` | `1` | `(7, 3)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j2-p0'` | `'Q1'` | `2` | `(-5, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j2-p1'` | `'Q1'` | `2` | `(-2, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j2-p2'` | `'Q1'` | `2` | `(-1, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j2-p3'` | `'Q1'` | `2` | `(0, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j2-p4'` | `'Q1'` | `2` | `(0, 3)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j2-p5'` | `'Q1'` | `2` | `(1, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j2-p6'` | `'Q1'` | `2` | `(1, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j2-p7'` | `'Q1'` | `2` | `(2, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j2-p8'` | `'Q1'` | `2` | `(3, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j2-p9'` | `'Q1'` | `2` | `(7, 3)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'Q1-j3-p0'` | `'Q1'` | `3` | `(-5, 2)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'Q1-j3-p1'` | `'Q1'` | `3` | `(-2, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'Q1-j3-p2'` | `'Q1'` | `3` | `(-1, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'Q1-j3-p3'` | `'Q1'` | `3` | `(0, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'Q1-j3-p4'` | `'Q1'` | `3` | `(0, 3)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'Q1-j3-p5'` | `'Q1'` | `3` | `(1, 2)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'Q1-j3-p6'` | `'Q1'` | `3` | `(1, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'Q1-j3-p7'` | `'Q1'` | `3` | `(2, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'Q1-j3-p8'` | `'Q1'` | `3` | `(3, 2)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'Q1-j3-p9'` | `'Q1'` | `3` | `(7, 3)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j0-p0'` | `'DOUBLE'` | `0` | `(-5, 2)` | `(1, 2, 2, 14)` | `(1, 2)` | `0` | `(1, 1, 1, 7)` | `0` | `3` |
| `'DOUBLE-j0-p1'` | `'DOUBLE'` | `0` | `(-2, 1)` | `(1, 2, 2, 6)` | `(1, 2)` | `0` | `(1, 1, 1, 7)` | `0` | `1` |
| `'DOUBLE-j0-p2'` | `'DOUBLE'` | `0` | `(-1, 1)` | `(1, 2, 2, 4)` | `(1, 2)` | `0` | `(1, 1, 1, 7)` | `0` | `0` |
| `'DOUBLE-j0-p3'` | `'DOUBLE'` | `0` | `(0, 1)` | `(1, 2, 2, 2)` | `(1, 2)` | `0` | `(1, 1, 1, 7)` | `0` | `-1` |
| `'DOUBLE-j0-p4'` | `'DOUBLE'` | `0` | `(0, 3)` | `(1, 2, 2, 6)` | `(1, 2)` | `0` | `(1, 1, 1, 7)` | `0` | `-3` |
| `'DOUBLE-j0-p5'` | `'DOUBLE'` | `0` | `(1, 2)` | `(1, 2, 2, 2)` | `(1, 2)` | `0` | `(1, 1, 1, 7)` | `0` | `-3` |
| `'DOUBLE-j0-p6'` | `'DOUBLE'` | `0` | `(1, 1)` | `(1, 2, 2, 0)` | `(1, 2)` | `0` | `(1, 1, 1, 7)` | `0` | `-2` |
| `'DOUBLE-j0-p7'` | `'DOUBLE'` | `0` | `(2, 1)` | `(1, 2, 2, -2)` | `(1, 2)` | `0` | `(1, 1, 1, 7)` | `2` | `-3` |
| `'DOUBLE-j0-p8'` | `'DOUBLE'` | `0` | `(3, 2)` | `(1, 2, 2, -2)` | `(1, 2)` | `0` | `(1, 1, 1, 7)` | `2` | `-5` |
| `'DOUBLE-j0-p9'` | `'DOUBLE'` | `0` | `(7, 3)` | `(1, 2, 2, -8)` | `(1, 2)` | `0` | `(1, 1, 1, 7)` | `8` | `-10` |
| `'DOUBLE-j1-p0'` | `'DOUBLE'` | `1` | `(-5, 2)` | `None` | `()` | `None` | `(4, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j1-p1'` | `'DOUBLE'` | `1` | `(-2, 1)` | `None` | `()` | `None` | `(4, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j1-p2'` | `'DOUBLE'` | `1` | `(-1, 1)` | `None` | `()` | `None` | `(4, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j1-p3'` | `'DOUBLE'` | `1` | `(0, 1)` | `None` | `()` | `None` | `(4, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j1-p4'` | `'DOUBLE'` | `1` | `(0, 3)` | `None` | `()` | `None` | `(4, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j1-p5'` | `'DOUBLE'` | `1` | `(1, 2)` | `None` | `()` | `None` | `(4, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j1-p6'` | `'DOUBLE'` | `1` | `(1, 1)` | `None` | `()` | `None` | `(4, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j1-p7'` | `'DOUBLE'` | `1` | `(2, 1)` | `None` | `()` | `None` | `(4, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j1-p8'` | `'DOUBLE'` | `1` | `(3, 2)` | `None` | `()` | `None` | `(4, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j1-p9'` | `'DOUBLE'` | `1` | `(7, 3)` | `None` | `()` | `None` | `(4, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j2-p0'` | `'DOUBLE'` | `2` | `(-5, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j2-p1'` | `'DOUBLE'` | `2` | `(-2, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j2-p2'` | `'DOUBLE'` | `2` | `(-1, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j2-p3'` | `'DOUBLE'` | `2` | `(0, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j2-p4'` | `'DOUBLE'` | `2` | `(0, 3)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j2-p5'` | `'DOUBLE'` | `2` | `(1, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j2-p6'` | `'DOUBLE'` | `2` | `(1, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j2-p7'` | `'DOUBLE'` | `2` | `(2, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j2-p8'` | `'DOUBLE'` | `2` | `(3, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j2-p9'` | `'DOUBLE'` | `2` | `(7, 3)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j3-p0'` | `'DOUBLE'` | `3` | `(-5, 2)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j3-p1'` | `'DOUBLE'` | `3` | `(-2, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j3-p2'` | `'DOUBLE'` | `3` | `(-1, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j3-p3'` | `'DOUBLE'` | `3` | `(0, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j3-p4'` | `'DOUBLE'` | `3` | `(0, 3)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j3-p5'` | `'DOUBLE'` | `3` | `(1, 2)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j3-p6'` | `'DOUBLE'` | `3` | `(1, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j3-p7'` | `'DOUBLE'` | `3` | `(2, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j3-p8'` | `'DOUBLE'` | `3` | `(3, 2)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'DOUBLE-j3-p9'` | `'DOUBLE'` | `3` | `(7, 3)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'UNEQUAL-j0-p0'` | `'UNEQUAL'` | `0` | `(-5, 2)` | `(2, 2, 2, 14)` | `(2, 3)` | `0` | `(1, 1, 1, 7)` | `0` | `3` |
| `'UNEQUAL-j0-p1'` | `'UNEQUAL'` | `0` | `(-2, 1)` | `(2, 2, 2, 6)` | `(2, 3)` | `0` | `(1, 1, 1, 7)` | `0` | `1` |
| `'UNEQUAL-j0-p2'` | `'UNEQUAL'` | `0` | `(-1, 1)` | `(2, 2, 2, 4)` | `(2, 3)` | `0` | `(1, 1, 1, 7)` | `0` | `0` |
| `'UNEQUAL-j0-p3'` | `'UNEQUAL'` | `0` | `(0, 1)` | `(3, 2, 2, 2)` | `(2, 3)` | `0` | `(1, 1, 1, 7)` | `0` | `-1` |
| `'UNEQUAL-j0-p4'` | `'UNEQUAL'` | `0` | `(0, 3)` | `(3, 2, 2, 6)` | `(2, 3)` | `0` | `(1, 1, 1, 7)` | `0` | `-3` |
| `'UNEQUAL-j0-p5'` | `'UNEQUAL'` | `0` | `(1, 2)` | `(3, 2, 2, 2)` | `(2, 3)` | `0` | `(1, 1, 1, 7)` | `0` | `-3` |
| `'UNEQUAL-j0-p6'` | `'UNEQUAL'` | `0` | `(1, 1)` | `(3, 2, 2, 0)` | `(2, 3)` | `0` | `(1, 1, 1, 7)` | `0` | `-2` |
| `'UNEQUAL-j0-p7'` | `'UNEQUAL'` | `0` | `(2, 1)` | `(3, 2, 2, -2)` | `(2, 3)` | `0` | `(1, 1, 1, 7)` | `1` | `-3` |
| `'UNEQUAL-j0-p8'` | `'UNEQUAL'` | `0` | `(3, 2)` | `(3, 2, 2, -2)` | `(2, 3)` | `0` | `(1, 1, 1, 7)` | `1` | `-5` |
| `'UNEQUAL-j0-p9'` | `'UNEQUAL'` | `0` | `(7, 3)` | `(3, 2, 2, -8)` | `(2, 3)` | `0` | `(1, 1, 1, 7)` | `4` | `-10` |
| `'UNEQUAL-j1-p0'` | `'UNEQUAL'` | `1` | `(-5, 2)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'UNEQUAL-j1-p1'` | `'UNEQUAL'` | `1` | `(-2, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'UNEQUAL-j1-p2'` | `'UNEQUAL'` | `1` | `(-1, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'UNEQUAL-j1-p3'` | `'UNEQUAL'` | `1` | `(0, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'UNEQUAL-j1-p4'` | `'UNEQUAL'` | `1` | `(0, 3)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'UNEQUAL-j1-p5'` | `'UNEQUAL'` | `1` | `(1, 2)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'UNEQUAL-j1-p6'` | `'UNEQUAL'` | `1` | `(1, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'UNEQUAL-j1-p7'` | `'UNEQUAL'` | `1` | `(2, 1)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'UNEQUAL-j1-p8'` | `'UNEQUAL'` | `1` | `(3, 2)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'UNEQUAL-j1-p9'` | `'UNEQUAL'` | `1` | `(7, 3)` | `None` | `()` | `None` | `(2, 0, 0, 0)` | `None` | `None` |
| `'UNEQUAL-j2-p0'` | `'UNEQUAL'` | `2` | `(-5, 2)` | `(3, -4, 2, 2)` | `(3,)` | `0` | `(1, 1, 1, 3)` | `0` | `-5` |
| `'UNEQUAL-j2-p1'` | `'UNEQUAL'` | `2` | `(-2, 1)` | `(3, -4, 2, 0)` | `(3,)` | `0` | `(1, 1, 1, 3)` | `0` | `-2` |
| `'UNEQUAL-j2-p2'` | `'UNEQUAL'` | `2` | `(-1, 1)` | `(3, -4, 2, -2)` | `(3,)` | `0` | `(1, 1, 1, 3)` | `1` | `-1` |
| `'UNEQUAL-j2-p3'` | `'UNEQUAL'` | `2` | `(0, 1)` | `(3, -4, 2, -4)` | `(3,)` | `0` | `(1, 1, 1, 3)` | `4` | `0` |
| `'UNEQUAL-j2-p4'` | `'UNEQUAL'` | `2` | `(0, 3)` | `(3, -4, 2, -12)` | `(3,)` | `0` | `(1, 1, 1, 3)` | `12` | `0` |
| `'UNEQUAL-j2-p5'` | `'UNEQUAL'` | `2` | `(1, 2)` | `(3, -4, 2, -10)` | `(3,)` | `0` | `(1, 1, 1, 3)` | `11` | `1` |
| `'UNEQUAL-j2-p6'` | `'UNEQUAL'` | `2` | `(1, 1)` | `(3, -4, 2, -6)` | `(3,)` | `0` | `(1, 1, 1, 3)` | `7` | `1` |
| `'UNEQUAL-j2-p7'` | `'UNEQUAL'` | `2` | `(2, 1)` | `(3, -4, 2, -8)` | `(3,)` | `0` | `(1, 1, 1, 3)` | `10` | `2` |
| `'UNEQUAL-j2-p8'` | `'UNEQUAL'` | `2` | `(3, 2)` | `(3, -4, 2, -14)` | `(3,)` | `0` | `(1, 1, 1, 3)` | `17` | `3` |
| `'UNEQUAL-j2-p9'` | `'UNEQUAL'` | `2` | `(7, 3)` | `(3, -4, 2, -26)` | `(3,)` | `0` | `(1, 1, 1, 3)` | `33` | `7` |
| `'UNEQUAL-j3-p0'` | `'UNEQUAL'` | `3` | `(-5, 2)` | `(1, -2, 2, 6)` | `(1,)` | `0` | `(2, 1, 1, 1)` | `0` | `-4` |
| `'UNEQUAL-j3-p1'` | `'UNEQUAL'` | `3` | `(-2, 1)` | `(1, -2, 2, 2)` | `(1,)` | `0` | `(2, 1, 1, 1)` | `0` | `-2` |
| `'UNEQUAL-j3-p2'` | `'UNEQUAL'` | `3` | `(-1, 1)` | `(1, -2, 2, 0)` | `(1,)` | `0` | `(2, 1, 1, 1)` | `1` | `-2` |
| `'UNEQUAL-j3-p3'` | `'UNEQUAL'` | `3` | `(0, 1)` | `(1, -2, 2, -2)` | `(1,)` | `0` | `(2, 1, 1, 1)` | `4` | `-2` |
| `'UNEQUAL-j3-p4'` | `'UNEQUAL'` | `3` | `(0, 3)` | `(1, -2, 2, -6)` | `(1,)` | `0` | `(2, 1, 1, 1)` | `12` | `-6` |
| `'UNEQUAL-j3-p5'` | `'UNEQUAL'` | `3` | `(1, 2)` | `(1, -2, 2, -6)` | `(1,)` | `0` | `(2, 1, 1, 1)` | `11` | `-4` |
| `'UNEQUAL-j3-p6'` | `'UNEQUAL'` | `3` | `(1, 1)` | `(1, -2, 2, -4)` | `(1,)` | `0` | `(2, 1, 1, 1)` | `7` | `-2` |
| `'UNEQUAL-j3-p7'` | `'UNEQUAL'` | `3` | `(2, 1)` | `(1, -2, 2, -6)` | `(1,)` | `0` | `(2, 1, 1, 1)` | `10` | `-2` |
| `'UNEQUAL-j3-p8'` | `'UNEQUAL'` | `3` | `(3, 2)` | `(1, -2, 2, -10)` | `(1,)` | `0` | `(2, 1, 1, 1)` | `17` | `-4` |
| `'UNEQUAL-j3-p9'` | `'UNEQUAL'` | `3` | `(7, 3)` | `(1, -2, 2, -20)` | `(1,)` | `0` | `(2, 1, 1, 1)` | `33` | `-6` |
| `'EQUALITY-j0-p0'` | `'EQUALITY'` | `0` | `(-5, 2)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j0-p1'` | `'EQUALITY'` | `0` | `(-2, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j0-p2'` | `'EQUALITY'` | `0` | `(-1, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j0-p3'` | `'EQUALITY'` | `0` | `(0, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j0-p4'` | `'EQUALITY'` | `0` | `(0, 3)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j0-p5'` | `'EQUALITY'` | `0` | `(1, 2)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j0-p6'` | `'EQUALITY'` | `0` | `(1, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j0-p7'` | `'EQUALITY'` | `0` | `(2, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j0-p8'` | `'EQUALITY'` | `0` | `(3, 2)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j0-p9'` | `'EQUALITY'` | `0` | `(7, 3)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j1-p0'` | `'EQUALITY'` | `1` | `(-5, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j1-p1'` | `'EQUALITY'` | `1` | `(-2, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j1-p2'` | `'EQUALITY'` | `1` | `(-1, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j1-p3'` | `'EQUALITY'` | `1` | `(0, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j1-p4'` | `'EQUALITY'` | `1` | `(0, 3)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j1-p5'` | `'EQUALITY'` | `1` | `(1, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j1-p6'` | `'EQUALITY'` | `1` | `(1, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j1-p7'` | `'EQUALITY'` | `1` | `(2, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j1-p8'` | `'EQUALITY'` | `1` | `(3, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j1-p9'` | `'EQUALITY'` | `1` | `(7, 3)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j2-p0'` | `'EQUALITY'` | `2` | `(-5, 2)` | `None` | `()` | `None` | `(3, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j2-p1'` | `'EQUALITY'` | `2` | `(-2, 1)` | `None` | `()` | `None` | `(3, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j2-p2'` | `'EQUALITY'` | `2` | `(-1, 1)` | `None` | `()` | `None` | `(3, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j2-p3'` | `'EQUALITY'` | `2` | `(0, 1)` | `None` | `()` | `None` | `(3, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j2-p4'` | `'EQUALITY'` | `2` | `(0, 3)` | `None` | `()` | `None` | `(3, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j2-p5'` | `'EQUALITY'` | `2` | `(1, 2)` | `None` | `()` | `None` | `(3, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j2-p6'` | `'EQUALITY'` | `2` | `(1, 1)` | `None` | `()` | `None` | `(3, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j2-p7'` | `'EQUALITY'` | `2` | `(2, 1)` | `None` | `()` | `None` | `(3, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j2-p8'` | `'EQUALITY'` | `2` | `(3, 2)` | `None` | `()` | `None` | `(3, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j2-p9'` | `'EQUALITY'` | `2` | `(7, 3)` | `None` | `()` | `None` | `(3, 0, 0, 0)` | `None` | `None` |
| `'EQUALITY-j3-p0'` | `'EQUALITY'` | `3` | `(-5, 2)` | `(1, -2, 2, 6)` | `(1, 2, 4)` | `0` | `(6, 6, 6, 18)` | `0` | `-4` |
| `'EQUALITY-j3-p1'` | `'EQUALITY'` | `3` | `(-2, 1)` | `(1, -2, 2, 2)` | `(1, 2, 4)` | `0` | `(6, 6, 6, 18)` | `0` | `-2` |
| `'EQUALITY-j3-p2'` | `'EQUALITY'` | `3` | `(-1, 1)` | `(1, -2, 2, 0)` | `(1, 2, 3, 4, 5, 6)` | `0` | `(6, 6, 6, 18)` | `0` | `-2` |
| `'EQUALITY-j3-p3'` | `'EQUALITY'` | `3` | `(0, 1)` | `(5, -4, 4, -4)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `6` | `-2` |
| `'EQUALITY-j3-p4'` | `'EQUALITY'` | `3` | `(0, 3)` | `(5, -4, 4, -12)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `18` | `-6` |
| `'EQUALITY-j3-p5'` | `'EQUALITY'` | `3` | `(1, 2)` | `(5, -4, 4, -12)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `18` | `-4` |
| `'EQUALITY-j3-p6'` | `'EQUALITY'` | `3` | `(1, 1)` | `(5, -4, 4, -8)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `12` | `-2` |
| `'EQUALITY-j3-p7'` | `'EQUALITY'` | `3` | `(2, 1)` | `(5, -4, 4, -12)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `18` | `-2` |
| `'EQUALITY-j3-p8'` | `'EQUALITY'` | `3` | `(3, 2)` | `(5, -4, 4, -20)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `30` | `-4` |
| `'EQUALITY-j3-p9'` | `'EQUALITY'` | `3` | `(7, 3)` | `(5, -4, 4, -40)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `60` | `-6` |
| `'WTRI-j0-p0'` | `'WTRI'` | `0` | `(-5, 2)` | `(1, 2, 2, 14)` | `(1, 2, 4)` | `0` | `(1, 1, 1, 13)` | `0` | `3` |
| `'WTRI-j0-p1'` | `'WTRI'` | `0` | `(-2, 1)` | `(1, 2, 2, 6)` | `(1, 2, 4)` | `0` | `(1, 1, 1, 13)` | `0` | `1` |
| `'WTRI-j0-p2'` | `'WTRI'` | `0` | `(-1, 1)` | `(1, 2, 2, 4)` | `(1, 2, 4)` | `0` | `(1, 1, 1, 13)` | `0` | `0` |
| `'WTRI-j0-p3'` | `'WTRI'` | `0` | `(0, 1)` | `(1, 2, 2, 2)` | `(1, 2, 4, 7)` | `0` | `(1, 1, 1, 13)` | `0` | `-1` |
| `'WTRI-j0-p4'` | `'WTRI'` | `0` | `(0, 3)` | `(1, 2, 2, 6)` | `(1, 2, 4, 7)` | `0` | `(1, 1, 1, 13)` | `0` | `-3` |
| `'WTRI-j0-p5'` | `'WTRI'` | `0` | `(1, 2)` | `(7, 2, 4, 0)` | `(7,)` | `0` | `(1, 1, 1, 13)` | `0` | `-3` |
| `'WTRI-j0-p6'` | `'WTRI'` | `0` | `(1, 1)` | `(7, 2, 4, -2)` | `(7,)` | `0` | `(1, 1, 1, 13)` | `0` | `-2` |
| `'WTRI-j0-p7'` | `'WTRI'` | `0` | `(2, 1)` | `(7, 2, 4, -6)` | `(7,)` | `0` | `(1, 1, 1, 13)` | `3` | `-3` |
| `'WTRI-j0-p8'` | `'WTRI'` | `0` | `(3, 2)` | `(7, 2, 4, -8)` | `(7,)` | `0` | `(1, 1, 1, 13)` | `3` | `-5` |
| `'WTRI-j0-p9'` | `'WTRI'` | `0` | `(7, 3)` | `(7, 2, 4, -22)` | `(7,)` | `0` | `(1, 1, 1, 13)` | `12` | `-10` |
| `'WTRI-j1-p0'` | `'WTRI'` | `1` | `(-5, 2)` | `(5, 2, 2, 14)` | `(3, 5, 6)` | `0` | `(18, 12, 12, 24)` | `0` | `-4` |
| `'WTRI-j1-p1'` | `'WTRI'` | `1` | `(-2, 1)` | `(5, 2, 2, 6)` | `(3, 5, 6)` | `0` | `(18, 12, 12, 24)` | `0` | `-2` |
| `'WTRI-j1-p2'` | `'WTRI'` | `1` | `(-1, 1)` | `(5, 2, 2, 4)` | `(3, 5, 6)` | `0` | `(18, 12, 12, 24)` | `0` | `-2` |
| `'WTRI-j1-p3'` | `'WTRI'` | `1` | `(0, 1)` | `(5, 2, 2, 2)` | `(3, 5, 6)` | `0` | `(18, 12, 12, 24)` | `0` | `-2` |
| `'WTRI-j1-p4'` | `'WTRI'` | `1` | `(0, 3)` | `(5, 2, 2, 6)` | `(3, 5, 6)` | `0` | `(18, 12, 12, 24)` | `0` | `-6` |
| `'WTRI-j1-p5'` | `'WTRI'` | `1` | `(1, 2)` | `(5, 2, 2, 2)` | `(3, 5, 6)` | `0` | `(18, 12, 12, 24)` | `0` | `-4` |
| `'WTRI-j1-p6'` | `'WTRI'` | `1` | `(1, 1)` | `(5, 2, 2, 0)` | `(3, 5, 6)` | `0` | `(18, 12, 12, 24)` | `0` | `-2` |
| `'WTRI-j1-p7'` | `'WTRI'` | `1` | `(2, 1)` | `(5, 2, 2, -2)` | `(3, 5, 6)` | `0` | `(18, 12, 12, 24)` | `3` | `-2` |
| `'WTRI-j1-p8'` | `'WTRI'` | `1` | `(3, 2)` | `(5, 2, 2, -2)` | `(3, 5, 6)` | `0` | `(18, 12, 12, 24)` | `3` | `-4` |
| `'WTRI-j1-p9'` | `'WTRI'` | `1` | `(7, 3)` | `(5, 2, 2, -8)` | `(3, 5, 6)` | `0` | `(18, 12, 12, 24)` | `12` | `-6` |
| `'WTRI-j2-p0'` | `'WTRI'` | `2` | `(-5, 2)` | `(7, -6, 2, -2)` | `(7,)` | `0` | `(1, 1, 1, 1)` | `0` | `-5` |
| `'WTRI-j2-p1'` | `'WTRI'` | `2` | `(-2, 1)` | `(7, -6, 2, -2)` | `(7,)` | `0` | `(1, 1, 1, 1)` | `0` | `-2` |
| `'WTRI-j2-p2'` | `'WTRI'` | `2` | `(-1, 1)` | `(7, -6, 2, -4)` | `(7,)` | `0` | `(1, 1, 1, 1)` | `3` | `-1` |
| `'WTRI-j2-p3'` | `'WTRI'` | `2` | `(0, 1)` | `(7, -6, 2, -6)` | `(7,)` | `0` | `(1, 1, 1, 1)` | `6` | `0` |
| `'WTRI-j2-p4'` | `'WTRI'` | `2` | `(0, 3)` | `(7, -6, 2, -18)` | `(7,)` | `0` | `(1, 1, 1, 1)` | `18` | `0` |
| `'WTRI-j2-p5'` | `'WTRI'` | `2` | `(1, 2)` | `(7, -6, 2, -14)` | `(7,)` | `0` | `(1, 1, 1, 1)` | `15` | `1` |
| `'WTRI-j2-p6'` | `'WTRI'` | `2` | `(1, 1)` | `(7, -6, 2, -8)` | `(7,)` | `0` | `(1, 1, 1, 1)` | `9` | `1` |
| `'WTRI-j2-p7'` | `'WTRI'` | `2` | `(2, 1)` | `(7, -6, 2, -10)` | `(7,)` | `0` | `(1, 1, 1, 1)` | `12` | `2` |
| `'WTRI-j2-p8'` | `'WTRI'` | `2` | `(3, 2)` | `(7, -6, 2, -18)` | `(7,)` | `0` | `(1, 1, 1, 1)` | `21` | `3` |
| `'WTRI-j2-p9'` | `'WTRI'` | `2` | `(7, 3)` | `(7, -6, 2, -32)` | `(7,)` | `0` | `(1, 1, 1, 1)` | `39` | `7` |
| `'WTRI-j3-p0'` | `'WTRI'` | `3` | `(-5, 2)` | `(5, -4, 2, 2)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `0` | `-4` |
| `'WTRI-j3-p1'` | `'WTRI'` | `3` | `(-2, 1)` | `(5, -4, 2, 0)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `0` | `-2` |
| `'WTRI-j3-p2'` | `'WTRI'` | `3` | `(-1, 1)` | `(5, -4, 2, -2)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `3` | `-2` |
| `'WTRI-j3-p3'` | `'WTRI'` | `3` | `(0, 1)` | `(5, -4, 2, -4)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `6` | `-2` |
| `'WTRI-j3-p4'` | `'WTRI'` | `3` | `(0, 3)` | `(5, -4, 2, -12)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `18` | `-6` |
| `'WTRI-j3-p5'` | `'WTRI'` | `3` | `(1, 2)` | `(5, -4, 2, -10)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `15` | `-4` |
| `'WTRI-j3-p6'` | `'WTRI'` | `3` | `(1, 1)` | `(5, -4, 2, -6)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `9` | `-2` |
| `'WTRI-j3-p7'` | `'WTRI'` | `3` | `(2, 1)` | `(5, -4, 2, -8)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `12` | `-2` |
| `'WTRI-j3-p8'` | `'WTRI'` | `3` | `(3, 2)` | `(5, -4, 2, -14)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `21` | `-4` |
| `'WTRI-j3-p9'` | `'WTRI'` | `3` | `(7, 3)` | `(5, -4, 2, -26)` | `(3, 5, 6)` | `0` | `(6, 6, 6, 18)` | `39` | `-6` |
| `'ODDFULL-j0-p0'` | `'ODDFULL'` | `0` | `(-5, 2)` | `(4, 2, 2, 14)` | `(4,)` | `0` | `(1, 1, 1, 13)` | `0` | `3` |
| `'ODDFULL-j0-p1'` | `'ODDFULL'` | `0` | `(-2, 1)` | `(4, 2, 2, 6)` | `(4,)` | `0` | `(1, 1, 1, 13)` | `0` | `1` |
| `'ODDFULL-j0-p2'` | `'ODDFULL'` | `0` | `(-1, 1)` | `(4, 2, 2, 4)` | `(4,)` | `0` | `(1, 1, 1, 13)` | `0` | `0` |
| `'ODDFULL-j0-p3'` | `'ODDFULL'` | `0` | `(0, 1)` | `(4, 2, 2, 2)` | `(4,)` | `0` | `(1, 1, 1, 13)` | `0` | `-1` |
| `'ODDFULL-j0-p4'` | `'ODDFULL'` | `0` | `(0, 3)` | `(4, 2, 2, 6)` | `(4,)` | `0` | `(1, 1, 1, 13)` | `0` | `-3` |
| `'ODDFULL-j0-p5'` | `'ODDFULL'` | `0` | `(1, 2)` | `(4, 2, 2, 2)` | `(4,)` | `0` | `(1, 1, 1, 13)` | `0` | `-3` |
| `'ODDFULL-j0-p6'` | `'ODDFULL'` | `0` | `(1, 1)` | `(4, 2, 2, 0)` | `(4,)` | `0` | `(1, 1, 1, 13)` | `0` | `-2` |
| `'ODDFULL-j0-p7'` | `'ODDFULL'` | `0` | `(2, 1)` | `(4, 2, 2, -2)` | `(4,)` | `0` | `(1, 1, 1, 13)` | `1` | `-3` |
| `'ODDFULL-j0-p8'` | `'ODDFULL'` | `0` | `(3, 2)` | `(4, 2, 2, -2)` | `(4,)` | `0` | `(1, 1, 1, 13)` | `1` | `-5` |
| `'ODDFULL-j0-p9'` | `'ODDFULL'` | `0` | `(7, 3)` | `(4, 2, 2, -8)` | `(4,)` | `0` | `(1, 1, 1, 13)` | `4` | `-10` |
| `'ODDFULL-j1-p0'` | `'ODDFULL'` | `1` | `(-5, 2)` | `None` | `()` | `None` | `(6, 0, 0, 0)` | `None` | `None` |
| `'ODDFULL-j1-p1'` | `'ODDFULL'` | `1` | `(-2, 1)` | `None` | `()` | `None` | `(6, 0, 0, 0)` | `None` | `None` |
| `'ODDFULL-j1-p2'` | `'ODDFULL'` | `1` | `(-1, 1)` | `None` | `()` | `None` | `(6, 0, 0, 0)` | `None` | `None` |
| `'ODDFULL-j1-p3'` | `'ODDFULL'` | `1` | `(0, 1)` | `None` | `()` | `None` | `(6, 0, 0, 0)` | `None` | `None` |
| `'ODDFULL-j1-p4'` | `'ODDFULL'` | `1` | `(0, 3)` | `None` | `()` | `None` | `(6, 0, 0, 0)` | `None` | `None` |
| `'ODDFULL-j1-p5'` | `'ODDFULL'` | `1` | `(1, 2)` | `None` | `()` | `None` | `(6, 0, 0, 0)` | `None` | `None` |
| `'ODDFULL-j1-p6'` | `'ODDFULL'` | `1` | `(1, 1)` | `None` | `()` | `None` | `(6, 0, 0, 0)` | `None` | `None` |
| `'ODDFULL-j1-p7'` | `'ODDFULL'` | `1` | `(2, 1)` | `None` | `()` | `None` | `(6, 0, 0, 0)` | `None` | `None` |
| `'ODDFULL-j1-p8'` | `'ODDFULL'` | `1` | `(3, 2)` | `None` | `()` | `None` | `(6, 0, 0, 0)` | `None` | `None` |
| `'ODDFULL-j1-p9'` | `'ODDFULL'` | `1` | `(7, 3)` | `None` | `()` | `None` | `(6, 0, 0, 0)` | `None` | `None` |
| `'ODDFULL-j2-p0'` | `'ODDFULL'` | `2` | `(-5, 2)` | `(5, -2, 2, 6)` | `(5, 6)` | `0` | `(2, 2, 2, 14)` | `0` | `-5` |
| `'ODDFULL-j2-p1'` | `'ODDFULL'` | `2` | `(-2, 1)` | `(7, -6, 4, 2)` | `(5, 6, 7)` | `0` | `(2, 2, 2, 14)` | `0` | `-2` |
| `'ODDFULL-j2-p2'` | `'ODDFULL'` | `2` | `(-1, 1)` | `(7, -6, 4, -2)` | `(7,)` | `0` | `(2, 2, 2, 14)` | `1` | `-1` |
| `'ODDFULL-j2-p3'` | `'ODDFULL'` | `2` | `(0, 1)` | `(7, -6, 4, -6)` | `(7,)` | `0` | `(2, 2, 2, 14)` | `6` | `0` |
| `'ODDFULL-j2-p4'` | `'ODDFULL'` | `2` | `(0, 3)` | `(7, -6, 4, -18)` | `(7,)` | `0` | `(2, 2, 2, 14)` | `18` | `0` |
| `'ODDFULL-j2-p5'` | `'ODDFULL'` | `2` | `(1, 2)` | `(7, -6, 4, -16)` | `(7,)` | `0` | `(2, 2, 2, 14)` | `17` | `1` |
| `'ODDFULL-j2-p6'` | `'ODDFULL'` | `2` | `(1, 1)` | `(7, -6, 4, -10)` | `(7,)` | `0` | `(2, 2, 2, 14)` | `11` | `1` |
| `'ODDFULL-j2-p7'` | `'ODDFULL'` | `2` | `(2, 1)` | `(7, -6, 4, -14)` | `(7,)` | `0` | `(2, 2, 2, 14)` | `16` | `2` |
| `'ODDFULL-j2-p8'` | `'ODDFULL'` | `2` | `(3, 2)` | `(7, -6, 4, -24)` | `(7,)` | `0` | `(2, 2, 2, 14)` | `27` | `3` |
| `'ODDFULL-j2-p9'` | `'ODDFULL'` | `2` | `(7, 3)` | `(7, -6, 4, -46)` | `(7,)` | `0` | `(2, 2, 2, 14)` | `53` | `7` |
| `'ODDFULL-j3-p0'` | `'ODDFULL'` | `3` | `(-5, 2)` | `(1, -2, 2, 6)` | `(1, 2)` | `0` | `(6, 4, 4, 12)` | `0` | `-4` |
| `'ODDFULL-j3-p1'` | `'ODDFULL'` | `3` | `(-2, 1)` | `(1, -2, 2, 2)` | `(1, 2)` | `0` | `(6, 4, 4, 12)` | `0` | `-2` |
| `'ODDFULL-j3-p2'` | `'ODDFULL'` | `3` | `(-1, 1)` | `(1, -2, 2, 0)` | `(1, 2, 3)` | `0` | `(6, 4, 4, 12)` | `1` | `-2` |
| `'ODDFULL-j3-p3'` | `'ODDFULL'` | `3` | `(0, 1)` | `(3, -4, 4, -4)` | `(3,)` | `2` | `(6, 4, 4, 12)` | `6` | `-2` |
| `'ODDFULL-j3-p4'` | `'ODDFULL'` | `3` | `(0, 3)` | `(3, -4, 4, -12)` | `(3,)` | `2` | `(6, 4, 4, 12)` | `18` | `-6` |
| `'ODDFULL-j3-p5'` | `'ODDFULL'` | `3` | `(1, 2)` | `(3, -4, 4, -12)` | `(3,)` | `2` | `(6, 4, 4, 12)` | `17` | `-4` |
| `'ODDFULL-j3-p6'` | `'ODDFULL'` | `3` | `(1, 1)` | `(3, -4, 4, -8)` | `(3,)` | `2` | `(6, 4, 4, 12)` | `11` | `-2` |
| `'ODDFULL-j3-p7'` | `'ODDFULL'` | `3` | `(2, 1)` | `(3, -4, 4, -12)` | `(3,)` | `2` | `(6, 4, 4, 12)` | `16` | `-2` |
| `'ODDFULL-j3-p8'` | `'ODDFULL'` | `3` | `(3, 2)` | `(3, -4, 4, -20)` | `(3,)` | `2` | `(6, 4, 4, 12)` | `27` | `-4` |
| `'ODDFULL-j3-p9'` | `'ODDFULL'` | `3` | `(7, 3)` | `(3, -4, 4, -40)` | `(3,)` | `2` | `(6, 4, 4, 12)` | `53` | `-6` |
| `'TIECARD-j0-p0'` | `'TIECARD'` | `0` | `(-5, 2)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j0-p1'` | `'TIECARD'` | `0` | `(-2, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j0-p2'` | `'TIECARD'` | `0` | `(-1, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j0-p3'` | `'TIECARD'` | `0` | `(0, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j0-p4'` | `'TIECARD'` | `0` | `(0, 3)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j0-p5'` | `'TIECARD'` | `0` | `(1, 2)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j0-p6'` | `'TIECARD'` | `0` | `(1, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j0-p7'` | `'TIECARD'` | `0` | `(2, 1)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j0-p8'` | `'TIECARD'` | `0` | `(3, 2)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j0-p9'` | `'TIECARD'` | `0` | `(7, 3)` | `None` | `()` | `None` | `(1, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j1-p0'` | `'TIECARD'` | `1` | `(-5, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j1-p1'` | `'TIECARD'` | `1` | `(-2, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j1-p2'` | `'TIECARD'` | `1` | `(-1, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j1-p3'` | `'TIECARD'` | `1` | `(0, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j1-p4'` | `'TIECARD'` | `1` | `(0, 3)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j1-p5'` | `'TIECARD'` | `1` | `(1, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j1-p6'` | `'TIECARD'` | `1` | `(1, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j1-p7'` | `'TIECARD'` | `1` | `(2, 1)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j1-p8'` | `'TIECARD'` | `1` | `(3, 2)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j1-p9'` | `'TIECARD'` | `1` | `(7, 3)` | `None` | `()` | `None` | `(0, 0, 0, 0)` | `None` | `None` |
| `'TIECARD-j2-p0'` | `'TIECARD'` | `2` | `(-5, 2)` | `(5, -2, 2, 6)` | `(5, 6)` | `0` | `(1, 1, 1, 7)` | `0` | `-5` |
| `'TIECARD-j2-p1'` | `'TIECARD'` | `2` | `(-2, 1)` | `(5, -2, 2, 2)` | `(5, 6)` | `0` | `(1, 1, 1, 7)` | `0` | `-2` |
| `'TIECARD-j2-p2'` | `'TIECARD'` | `2` | `(-1, 1)` | `(6, -2, 2, 0)` | `(5, 6)` | `0` | `(1, 1, 1, 7)` | `0` | `-1` |
| `'TIECARD-j2-p3'` | `'TIECARD'` | `2` | `(0, 1)` | `(6, -2, 2, -2)` | `(5, 6)` | `0` | `(1, 1, 1, 7)` | `4` | `0` |
| `'TIECARD-j2-p4'` | `'TIECARD'` | `2` | `(0, 3)` | `(6, -2, 2, -6)` | `(5, 6)` | `0` | `(1, 1, 1, 7)` | `12` | `0` |
| `'TIECARD-j2-p5'` | `'TIECARD'` | `2` | `(1, 2)` | `(6, -2, 2, -6)` | `(5, 6)` | `0` | `(1, 1, 1, 7)` | `12` | `1` |
| `'TIECARD-j2-p6'` | `'TIECARD'` | `2` | `(1, 1)` | `(6, -2, 2, -4)` | `(5, 6)` | `0` | `(1, 1, 1, 7)` | `8` | `1` |
| `'TIECARD-j2-p7'` | `'TIECARD'` | `2` | `(2, 1)` | `(6, -2, 2, -6)` | `(5, 6)` | `0` | `(1, 1, 1, 7)` | `12` | `2` |
| `'TIECARD-j2-p8'` | `'TIECARD'` | `2` | `(3, 2)` | `(6, -2, 2, -10)` | `(5, 6)` | `0` | `(1, 1, 1, 7)` | `20` | `3` |
| `'TIECARD-j2-p9'` | `'TIECARD'` | `2` | `(7, 3)` | `(6, -2, 2, -20)` | `(5, 6)` | `0` | `(1, 1, 1, 7)` | `40` | `7` |
| `'TIECARD-j3-p0'` | `'TIECARD'` | `3` | `(-5, 2)` | `(3, -2, 2, 6)` | `(3, 4)` | `0` | `(4, 4, 4, 12)` | `0` | `-4` |
| `'TIECARD-j3-p1'` | `'TIECARD'` | `3` | `(-2, 1)` | `(3, -2, 2, 2)` | `(3, 4)` | `0` | `(4, 4, 4, 12)` | `0` | `-2` |
| `'TIECARD-j3-p2'` | `'TIECARD'` | `3` | `(-1, 1)` | `(3, -2, 2, 0)` | `(3, 4)` | `0` | `(4, 4, 4, 12)` | `0` | `-2` |
| `'TIECARD-j3-p3'` | `'TIECARD'` | `3` | `(0, 1)` | `(3, -2, 2, -2)` | `(3, 4)` | `0` | `(4, 4, 4, 12)` | `4` | `-2` |
| `'TIECARD-j3-p4'` | `'TIECARD'` | `3` | `(0, 3)` | `(3, -2, 2, -6)` | `(3, 4)` | `0` | `(4, 4, 4, 12)` | `12` | `-6` |
| `'TIECARD-j3-p5'` | `'TIECARD'` | `3` | `(1, 2)` | `(3, -2, 2, -6)` | `(3, 4)` | `0` | `(4, 4, 4, 12)` | `12` | `-4` |
| `'TIECARD-j3-p6'` | `'TIECARD'` | `3` | `(1, 1)` | `(3, -2, 2, -4)` | `(3, 4)` | `0` | `(4, 4, 4, 12)` | `8` | `-2` |
| `'TIECARD-j3-p7'` | `'TIECARD'` | `3` | `(2, 1)` | `(3, -2, 2, -6)` | `(3, 4)` | `0` | `(4, 4, 4, 12)` | `12` | `-2` |
| `'TIECARD-j3-p8'` | `'TIECARD'` | `3` | `(3, 2)` | `(3, -2, 2, -10)` | `(3, 4)` | `0` | `(4, 4, 4, 12)` | `20` | `-4` |
| `'TIECARD-j3-p9'` | `'TIECARD'` | `3` | `(7, 3)` | `(3, -2, 2, -20)` | `(3, 4)` | `0` | `(4, 4, 4, 12)` | `40` | `-6` |
| `'RICH-j0-p0'` | `'RICH'` | `0` | `(-5, 2)` | `(1, 2, 2, 14)` | `(1, 2)` | `0` | `(1, 1, 1, 31)` | `0` | `3` |
| `'RICH-j0-p1'` | `'RICH'` | `0` | `(-2, 1)` | `(1, 2, 2, 6)` | `(1, 2)` | `0` | `(1, 1, 1, 31)` | `0` | `1` |
| `'RICH-j0-p2'` | `'RICH'` | `0` | `(-1, 1)` | `(1, 2, 2, 4)` | `(1, 2)` | `0` | `(1, 1, 1, 31)` | `0` | `0` |
| `'RICH-j0-p3'` | `'RICH'` | `0` | `(0, 1)` | `(1, 2, 2, 2)` | `(1, 2)` | `0` | `(1, 1, 1, 31)` | `0` | `-1` |
| `'RICH-j0-p4'` | `'RICH'` | `0` | `(0, 3)` | `(1, 2, 2, 6)` | `(1, 2)` | `0` | `(1, 1, 1, 31)` | `0` | `-3` |
| `'RICH-j0-p5'` | `'RICH'` | `0` | `(1, 2)` | `(1, 2, 2, 2)` | `(1, 2, 5, 6)` | `0` | `(1, 1, 1, 31)` | `2` | `-3` |
| `'RICH-j0-p6'` | `'RICH'` | `0` | `(1, 1)` | `(5, 4, 6, -2)` | `(5, 6)` | `0` | `(1, 1, 1, 31)` | `3` | `-2` |
| `'RICH-j0-p7'` | `'RICH'` | `0` | `(2, 1)` | `(6, 4, 6, -8)` | `(5, 6)` | `0` | `(1, 1, 1, 31)` | `9` | `-3` |
| `'RICH-j0-p8'` | `'RICH'` | `0` | `(3, 2)` | `(6, 4, 6, -10)` | `(5, 6)` | `0` | `(1, 1, 1, 31)` | `12` | `-5` |
| `'RICH-j0-p9'` | `'RICH'` | `0` | `(7, 3)` | `(6, 4, 6, -30)` | `(5, 6)` | `0` | `(1, 1, 1, 31)` | `33` | `-10` |
| `'RICH-j1-p0'` | `'RICH'` | `1` | `(-5, 2)` | `(3, 4, 2, 18)` | `(3,)` | `0` | `(24, 17, 17, 149)` | `0` | `-4` |
| `'RICH-j1-p1'` | `'RICH'` | `1` | `(-2, 1)` | `(3, 4, 2, 8)` | `(3,)` | `0` | `(24, 17, 17, 149)` | `0` | `-2` |
| `'RICH-j1-p2'` | `'RICH'` | `1` | `(-1, 1)` | `(3, 4, 2, 6)` | `(3,)` | `0` | `(24, 17, 17, 149)` | `0` | `-2` |
| `'RICH-j1-p3'` | `'RICH'` | `1` | `(0, 1)` | `(7, 2, 6, 2)` | `(7,)` | `4` | `(24, 17, 17, 149)` | `0` | `-2` |
| `'RICH-j1-p4'` | `'RICH'` | `1` | `(0, 3)` | `(7, 2, 6, 6)` | `(7,)` | `4` | `(24, 17, 17, 149)` | `0` | `-6` |
| `'RICH-j1-p5'` | `'RICH'` | `1` | `(1, 2)` | `(7, 2, 6, -2)` | `(7,)` | `4` | `(24, 17, 17, 149)` | `2` | `-4` |
| `'RICH-j1-p6'` | `'RICH'` | `1` | `(1, 1)` | `(7, 2, 6, -4)` | `(7,)` | `4` | `(24, 17, 17, 149)` | `3` | `-2` |
| `'RICH-j1-p7'` | `'RICH'` | `1` | `(2, 1)` | `(7, 2, 6, -10)` | `(7,)` | `4` | `(24, 17, 17, 149)` | `9` | `-2` |
| `'RICH-j1-p8'` | `'RICH'` | `1` | `(3, 2)` | `(7, 2, 6, -14)` | `(7,)` | `4` | `(24, 17, 17, 149)` | `12` | `-4` |
| `'RICH-j1-p9'` | `'RICH'` | `1` | `(7, 3)` | `(7, 2, 6, -36)` | `(7,)` | `4` | `(24, 17, 17, 149)` | `33` | `-6` |
| `'RICH-j2-p0'` | `'RICH'` | `2` | `(-5, 2)` | `(7, -8, 2, -6)` | `(7,)` | `1` | `(5, 5, 5, 49)` | `5` | `-5` |
| `'RICH-j2-p1'` | `'RICH'` | `2` | `(-2, 1)` | `(7, -8, 2, -4)` | `(7,)` | `1` | `(5, 5, 5, 49)` | `3` | `-2` |
| `'RICH-j2-p2'` | `'RICH'` | `2` | `(-1, 1)` | `(23, -10, 4, -6)` | `(7, 23)` | `0` | `(5, 5, 5, 49)` | `6` | `-1` |
| `'RICH-j2-p3'` | `'RICH'` | `2` | `(0, 1)` | `(23, -10, 4, -10)` | `(23,)` | `0` | `(5, 5, 5, 49)` | `12` | `0` |
| `'RICH-j2-p4'` | `'RICH'` | `2` | `(0, 3)` | `(23, -10, 4, -30)` | `(23,)` | `0` | `(5, 5, 5, 49)` | `36` | `0` |
| `'RICH-j2-p5'` | `'RICH'` | `2` | `(1, 2)` | `(23, -10, 4, -24)` | `(23,)` | `0` | `(5, 5, 5, 49)` | `30` | `1` |
| `'RICH-j2-p6'` | `'RICH'` | `2` | `(1, 1)` | `(23, -10, 4, -14)` | `(23,)` | `0` | `(5, 5, 5, 49)` | `18` | `1` |
| `'RICH-j2-p7'` | `'RICH'` | `2` | `(2, 1)` | `(23, -10, 4, -18)` | `(23,)` | `0` | `(5, 5, 5, 49)` | `24` | `2` |
| `'RICH-j2-p8'` | `'RICH'` | `2` | `(3, 2)` | `(23, -10, 4, -32)` | `(23,)` | `0` | `(5, 5, 5, 49)` | `42` | `3` |
| `'RICH-j2-p9'` | `'RICH'` | `2` | `(7, 3)` | `(23, -10, 4, -58)` | `(23,)` | `0` | `(5, 5, 5, 49)` | `78` | `7` |
| `'RICH-j3-p0'` | `'RICH'` | `3` | `(-5, 2)` | `(6, -6, 2, -2)` | `(5, 6)` | `1` | `(8, 8, 8, 104)` | `5` | `-4` |
| `'RICH-j3-p1'` | `'RICH'` | `3` | `(-2, 1)` | `(6, -6, 2, -2)` | `(5, 6, 15)` | `1` | `(8, 8, 8, 104)` | `3` | `-2` |
| `'RICH-j3-p2'` | `'RICH'` | `3` | `(-1, 1)` | `(15, -10, 4, -6)` | `(15,)` | `4` | `(8, 8, 8, 104)` | `6` | `-2` |
| `'RICH-j3-p3'` | `'RICH'` | `3` | `(0, 1)` | `(15, -10, 4, -10)` | `(15,)` | `4` | `(8, 8, 8, 104)` | `12` | `-2` |
| `'RICH-j3-p4'` | `'RICH'` | `3` | `(0, 3)` | `(15, -10, 4, -30)` | `(15,)` | `4` | `(8, 8, 8, 104)` | `36` | `-6` |
| `'RICH-j3-p5'` | `'RICH'` | `3` | `(1, 2)` | `(15, -10, 4, -24)` | `(15,)` | `4` | `(8, 8, 8, 104)` | `30` | `-4` |
| `'RICH-j3-p6'` | `'RICH'` | `3` | `(1, 1)` | `(15, -10, 4, -14)` | `(15,)` | `4` | `(8, 8, 8, 104)` | `18` | `-2` |
| `'RICH-j3-p7'` | `'RICH'` | `3` | `(2, 1)` | `(15, -10, 4, -18)` | `(15,)` | `4` | `(8, 8, 8, 104)` | `24` | `-2` |
| `'RICH-j3-p8'` | `'RICH'` | `3` | `(3, 2)` | `(15, -10, 4, -32)` | `(15,)` | `4` | `(8, 8, 8, 104)` | `42` | `-4` |
| `'RICH-j3-p9'` | `'RICH'` | `3` | `(7, 3)` | `(15, -10, 4, -58)` | `(15,)` | `4` | `(8, 8, 8, 104)` | `78` | `-6` |
| `'MIXED-j0-p0'` | `'MIXED'` | `0` | `(-5, 2)` | `(8, 12, 4, 44)` | `(8,)` | `0` | `(1, 1, 1, 21)` | `0` | `3` |
| `'MIXED-j0-p1'` | `'MIXED'` | `0` | `(-2, 1)` | `(8, 12, 4, 20)` | `(8,)` | `0` | `(1, 1, 1, 21)` | `0` | `1` |
| `'MIXED-j0-p2'` | `'MIXED'` | `0` | `(-1, 1)` | `(2, 10, 6, 16)` | `(2, 8)` | `0` | `(1, 1, 1, 21)` | `0` | `0` |
| `'MIXED-j0-p3'` | `'MIXED'` | `0` | `(0, 1)` | `(2, 10, 6, 10)` | `(2,)` | `0` | `(1, 1, 1, 21)` | `0` | `-1` |
| `'MIXED-j0-p4'` | `'MIXED'` | `0` | `(0, 3)` | `(2, 10, 6, 30)` | `(2,)` | `0` | `(1, 1, 1, 21)` | `0` | `-3` |
| `'MIXED-j0-p5'` | `'MIXED'` | `0` | `(1, 2)` | `(2, 10, 6, 14)` | `(2, 7)` | `0` | `(1, 1, 1, 21)` | `0` | `-3` |
| `'MIXED-j0-p6'` | `'MIXED'` | `0` | `(1, 1)` | `(7, 16, 18, -2)` | `(7,)` | `0` | `(1, 1, 1, 21)` | `8` | `-2` |
| `'MIXED-j0-p7'` | `'MIXED'` | `0` | `(2, 1)` | `(7, 16, 18, -20)` | `(7,)` | `0` | `(1, 1, 1, 21)` | `26` | `-3` |
| `'MIXED-j0-p8'` | `'MIXED'` | `0` | `(3, 2)` | `(7, 16, 18, -22)` | `(7,)` | `0` | `(1, 1, 1, 21)` | `33` | `-5` |
| `'MIXED-j0-p9'` | `'MIXED'` | `0` | `(7, 3)` | `(7, 16, 18, -78)` | `(7,)` | `0` | `(1, 1, 1, 21)` | `98` | `-10` |
| `'MIXED-j1-p0'` | `'MIXED'` | `1` | `(-5, 2)` | `(1, 6, 4, 32)` | `(1,)` | `0` | `(48, 26, 26, 118)` | `0` | `-4` |
| `'MIXED-j1-p1'` | `'MIXED'` | `1` | `(-2, 1)` | `(1, 6, 4, 14)` | `(1,)` | `0` | `(48, 26, 26, 118)` | `0` | `-2` |
| `'MIXED-j1-p2'` | `'MIXED'` | `1` | `(-1, 1)` | `(1, 6, 4, 10)` | `(1,)` | `0` | `(48, 26, 26, 118)` | `0` | `-2` |
| `'MIXED-j1-p3'` | `'MIXED'` | `1` | `(0, 1)` | `(1, 6, 4, 6)` | `(1,)` | `0` | `(48, 26, 26, 118)` | `0` | `-2` |
| `'MIXED-j1-p4'` | `'MIXED'` | `1` | `(0, 3)` | `(1, 6, 4, 18)` | `(1,)` | `0` | `(48, 26, 26, 118)` | `0` | `-6` |
| `'MIXED-j1-p5'` | `'MIXED'` | `1` | `(1, 2)` | `(1, 6, 4, 8)` | `(1,)` | `0` | `(48, 26, 26, 118)` | `0` | `-4` |
| `'MIXED-j1-p6'` | `'MIXED'` | `1` | `(1, 1)` | `(14, 16, 16, 0)` | `(14,)` | `13` | `(48, 26, 26, 118)` | `8` | `-2` |
| `'MIXED-j1-p7'` | `'MIXED'` | `1` | `(2, 1)` | `(14, 16, 16, -16)` | `(14,)` | `13` | `(48, 26, 26, 118)` | `26` | `-2` |
| `'MIXED-j1-p8'` | `'MIXED'` | `1` | `(3, 2)` | `(14, 16, 16, -16)` | `(14,)` | `13` | `(48, 26, 26, 118)` | `33` | `-4` |
| `'MIXED-j1-p9'` | `'MIXED'` | `1` | `(7, 3)` | `(14, 16, 16, -64)` | `(14,)` | `13` | `(48, 26, 26, 118)` | `98` | `-6` |
| `'MIXED-j2-p0'` | `'MIXED'` | `2` | `(-5, 2)` | `(7, -18, 8, 4)` | `(7,)` | `0` | `(4, 4, 4, 52)` | `7` | `-5` |
| `'MIXED-j2-p1'` | `'MIXED'` | `2` | `(-2, 1)` | `(7, -18, 8, -2)` | `(7,)` | `0` | `(4, 4, 4, 52)` | `8` | `-2` |
| `'MIXED-j2-p2'` | `'MIXED'` | `2` | `(-1, 1)` | `(7, -18, 8, -10)` | `(7,)` | `0` | `(4, 4, 4, 52)` | `20` | `-1` |
| `'MIXED-j2-p3'` | `'MIXED'` | `2` | `(0, 1)` | `(13, -18, 10, -18)` | `(7, 13)` | `0` | `(4, 4, 4, 52)` | `34` | `0` |
| `'MIXED-j2-p4'` | `'MIXED'` | `2` | `(0, 3)` | `(13, -18, 10, -54)` | `(7, 13)` | `0` | `(4, 4, 4, 52)` | `102` | `0` |
| `'MIXED-j2-p5'` | `'MIXED'` | `2` | `(1, 2)` | `(13, -18, 10, -46)` | `(13,)` | `0` | `(4, 4, 4, 52)` | `82` | `1` |
| `'MIXED-j2-p6'` | `'MIXED'` | `2` | `(1, 1)` | `(13, -18, 10, -28)` | `(13,)` | `0` | `(4, 4, 4, 52)` | `48` | `1` |
| `'MIXED-j2-p7'` | `'MIXED'` | `2` | `(2, 1)` | `(13, -18, 10, -38)` | `(13,)` | `0` | `(4, 4, 4, 52)` | `62` | `2` |
| `'MIXED-j2-p8'` | `'MIXED'` | `2` | `(3, 2)` | `(13, -18, 10, -66)` | `(13,)` | `0` | `(4, 4, 4, 52)` | `110` | `3` |
| `'MIXED-j2-p9'` | `'MIXED'` | `2` | `(7, 3)` | `(13, -18, 10, -124)` | `(13,)` | `0` | `(4, 4, 4, 52)` | `200` | `7` |
| `'MIXED-j3-p0'` | `'MIXED'` | `3` | `(-5, 2)` | `(1, -2, 2, 6)` | `(1,)` | `0` | `(12, 10, 10, 70)` | `7` | `-4` |
| `'MIXED-j3-p1'` | `'MIXED'` | `3` | `(-2, 1)` | `(14, -24, 12, 0)` | `(14,)` | `1` | `(12, 10, 10, 70)` | `8` | `-2` |
| `'MIXED-j3-p2'` | `'MIXED'` | `3` | `(-1, 1)` | `(14, -24, 12, -12)` | `(14,)` | `1` | `(12, 10, 10, 70)` | `20` | `-2` |
| `'MIXED-j3-p3'` | `'MIXED'` | `3` | `(0, 1)` | `(14, -24, 12, -24)` | `(14,)` | `1` | `(12, 10, 10, 70)` | `34` | `-2` |
| `'MIXED-j3-p4'` | `'MIXED'` | `3` | `(0, 3)` | `(14, -24, 12, -72)` | `(14,)` | `1` | `(12, 10, 10, 70)` | `102` | `-6` |
| `'MIXED-j3-p5'` | `'MIXED'` | `3` | `(1, 2)` | `(14, -24, 12, -60)` | `(14,)` | `1` | `(12, 10, 10, 70)` | `82` | `-4` |
| `'MIXED-j3-p6'` | `'MIXED'` | `3` | `(1, 1)` | `(14, -24, 12, -36)` | `(14,)` | `1` | `(12, 10, 10, 70)` | `48` | `-2` |
| `'MIXED-j3-p7'` | `'MIXED'` | `3` | `(2, 1)` | `(14, -24, 12, -48)` | `(14,)` | `1` | `(12, 10, 10, 70)` | `62` | `-2` |
| `'MIXED-j3-p8'` | `'MIXED'` | `3` | `(3, 2)` | `(14, -24, 12, -84)` | `(14,)` | `1` | `(12, 10, 10, 70)` | `110` | `-4` |
| `'MIXED-j3-p9'` | `'MIXED'` | `3` | `(7, 3)` | `(14, -24, 12, -156)` | `(14,)` | `1` | `(12, 10, 10, 70)` | `200` | `-6` |



## ORACLE-073 — Sole coefficient table, retained original arcs, and separate offsets

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO8, BO12, BO15. For lambda=A/B all branches have cut coefficient B.
Branches 0/1 use gamma=(A+B)f-A*d_q with constants -(A+B),-2B respectively;
branches 2/3 use gamma=-B*d_q-Af with constants A,-2B.
The following twelve MIXED networks include a negative parameter in EVERY branch,
zero, and a positive nonintegral parameter. Support arcs appear in edge_ref order,
two opposite arcs each; spoke pairs follow in vertex order, including zero pairs.

The original network has exactly 2(m+n) records and is the same object for every
nonempty family of ONE query. Repeated parameter calls build fresh original networks.
The total original capacity is 2*B*Q+2*sum(abs(gamma)). No family contraction owns or
alters C_minus or the constant. A result must be checked using original sums before
recovering cut-C_minus+constant exactly once and requiring equality with raw.

### Fixture table: NETWORKS

| query | cut_coefficient | gamma | C_minus | constant | ordered_original_arcs |
| --- | --- | --- | --- | --- | --- |
| `'MIXED-j0-p0'` | `2` | `(24, 31, 48, 25)` | `0` | `3` | `((0, 1, 4), (1, 0, 4), (0, 2, 6), (2, 0, 6), (0, 3, 2), (3, 0, 2), (1, 2, 8), (2, 1, 8), (1, 3, 4), (3, 1, 4), (2, 3, 10), (3, 2, 10), (0, 5, 24), (5, 0, 24), (1, 5, 31), (5, 1, 31), (2, 5, 48), (5, 2, 48), (3, 5, 25), (5, 3, 25))` |
| `'MIXED-j0-p3'` | `1` | `(2, 3, 4, 5)` | `0` | `-1` | `((0, 1, 2), (1, 0, 2), (0, 2, 3), (2, 0, 3), (0, 3, 1), (3, 0, 1), (1, 2, 4), (2, 1, 4), (1, 3, 2), (3, 1, 2), (2, 3, 5), (3, 2, 5), (0, 5, 2), (5, 0, 2), (1, 5, 3), (5, 1, 3), (2, 5, 4), (5, 2, 4), (3, 5, 5), (5, 3, 5))` |
| `'MIXED-j0-p9'` | `3` | `(-22, -26, -44, -6)` | `98` | `-10` | `((0, 1, 6), (1, 0, 6), (0, 2, 9), (2, 0, 9), (0, 3, 3), (3, 0, 3), (1, 2, 12), (2, 1, 12), (1, 3, 6), (3, 1, 6), (2, 3, 15), (3, 2, 15), (4, 0, 22), (0, 4, 22), (4, 1, 26), (1, 4, 26), (4, 2, 44), (2, 4, 44), (4, 3, 6), (3, 4, 6))` |
| `'MIXED-j1-p0'` | `2` | `(24, 31, 48, 25)` | `0` | `-4` | `((0, 1, 4), (1, 0, 4), (0, 2, 6), (2, 0, 6), (0, 3, 2), (3, 0, 2), (1, 2, 8), (2, 1, 8), (1, 3, 4), (3, 1, 4), (2, 3, 10), (3, 2, 10), (0, 5, 24), (5, 0, 24), (1, 5, 31), (5, 1, 31), (2, 5, 48), (5, 2, 48), (3, 5, 25), (5, 3, 25))` |
| `'MIXED-j1-p3'` | `1` | `(2, 3, 4, 5)` | `0` | `-2` | `((0, 1, 2), (1, 0, 2), (0, 2, 3), (2, 0, 3), (0, 3, 1), (3, 0, 1), (1, 2, 4), (2, 1, 4), (1, 3, 2), (3, 1, 2), (2, 3, 5), (3, 2, 5), (0, 5, 2), (5, 0, 2), (1, 5, 3), (5, 1, 3), (2, 5, 4), (5, 2, 4), (3, 5, 5), (5, 3, 5))` |
| `'MIXED-j1-p9'` | `3` | `(-22, -26, -44, -6)` | `98` | `-6` | `((0, 1, 6), (1, 0, 6), (0, 2, 9), (2, 0, 9), (0, 3, 3), (3, 0, 3), (1, 2, 12), (2, 1, 12), (1, 3, 6), (3, 1, 6), (2, 3, 15), (3, 2, 15), (4, 0, 22), (0, 4, 22), (4, 1, 26), (1, 4, 26), (4, 2, 44), (2, 4, 44), (4, 3, 6), (3, 4, 6))` |
| `'MIXED-j2-p0'` | `2` | `(-2, -1, -4, 9)` | `7` | `-5` | `((0, 1, 4), (1, 0, 4), (0, 2, 6), (2, 0, 6), (0, 3, 2), (3, 0, 2), (1, 2, 8), (2, 1, 8), (1, 3, 4), (3, 1, 4), (2, 3, 10), (3, 2, 10), (4, 0, 2), (0, 4, 2), (4, 1, 1), (1, 4, 1), (4, 2, 4), (2, 4, 4), (3, 5, 9), (5, 3, 9))` |
| `'MIXED-j2-p3'` | `1` | `(-6, -8, -12, -8)` | `34` | `0` | `((0, 1, 2), (1, 0, 2), (0, 2, 3), (2, 0, 3), (0, 3, 1), (3, 0, 1), (1, 2, 4), (2, 1, 4), (1, 3, 2), (3, 1, 2), (2, 3, 5), (3, 2, 5), (4, 0, 6), (0, 4, 6), (4, 1, 8), (1, 4, 8), (4, 2, 12), (2, 4, 12), (4, 3, 8), (3, 4, 8))` |
| `'MIXED-j2-p9'` | `3` | `(-32, -45, -64, -59)` | `200` | `7` | `((0, 1, 6), (1, 0, 6), (0, 2, 9), (2, 0, 9), (0, 3, 3), (3, 0, 3), (1, 2, 12), (2, 1, 12), (1, 3, 6), (3, 1, 6), (2, 3, 15), (3, 2, 15), (4, 0, 32), (0, 4, 32), (4, 1, 45), (1, 4, 45), (4, 2, 64), (2, 4, 64), (4, 3, 59), (3, 4, 59))` |
| `'MIXED-j3-p0'` | `2` | `(-2, -1, -4, 9)` | `7` | `-4` | `((0, 1, 4), (1, 0, 4), (0, 2, 6), (2, 0, 6), (0, 3, 2), (3, 0, 2), (1, 2, 8), (2, 1, 8), (1, 3, 4), (3, 1, 4), (2, 3, 10), (3, 2, 10), (4, 0, 2), (0, 4, 2), (4, 1, 1), (1, 4, 1), (4, 2, 4), (2, 4, 4), (3, 5, 9), (5, 3, 9))` |
| `'MIXED-j3-p3'` | `1` | `(-6, -8, -12, -8)` | `34` | `-2` | `((0, 1, 2), (1, 0, 2), (0, 2, 3), (2, 0, 3), (0, 3, 1), (3, 0, 1), (1, 2, 4), (2, 1, 4), (1, 3, 2), (3, 1, 2), (2, 3, 5), (3, 2, 5), (4, 0, 6), (0, 4, 6), (4, 1, 8), (1, 4, 8), (4, 2, 12), (2, 4, 12), (4, 3, 8), (3, 4, 8))` |
| `'MIXED-j3-p9'` | `3` | `(-32, -45, -64, -59)` | `200` | `-6` | `((0, 1, 6), (1, 0, 6), (0, 2, 9), (2, 0, 9), (0, 3, 3), (3, 0, 3), (1, 2, 12), (2, 1, 12), (1, 3, 6), (3, 1, 6), (2, 3, 15), (3, 2, 15), (4, 0, 32), (0, 4, 32), (4, 1, 45), (1, 4, 45), (4, 2, 64), (2, 4, 64), (4, 3, 59), (3, 4, 59))` |



## ORACLE-074 — Complete selected-query family traces and coordinate recovery

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO6, BO9--BO12, BO14. FAMILY_TRACE contains every descriptor of the 17 named trace
queries, including skipped ones; a None payload means no reduction/parity/recovery call.
A non-None payload has this EXACT order:

`(classes, raw_terminal_mask, final_terminal_mask, reduced_shore, original_shore,
  c, h, raw, unshifted_cut, ordinary_calls, replace_incumbent)`.

The class masks live in the original augmented universe; reduced_shore lives in class
coordinates; original_shore has auxiliary source/sink/anchor bits stripped. The raw
terminal mask is shown before the symmetric-difference sink toggle. For each candidate,
raw equals cut-C_minus+constant using the MINIMA row's offsets.

RICH-j1-p7 exhibits reduced mask 5 lifting to original mask 7; both fit within the
original bit universe, so a mere upper-bound check cannot detect confusing them.
UNEQUAL-j0-p3 also records full-original lifting from reduced mask 13 to original mask 3.

### Fixture table: FAMILY_TRACE

| query | family_index | T_pi_I_O | classes_rawT_T_reducedU_originalU_c_h_raw_cut_calls_replace_or_None |
| --- | --- | --- | --- |
| `'Q1-j0-p3'` | `0` | `(0, 1, 0, 0)` | `None` |
| `'Q1-j3-p3'` | `0` | `(3, 0, 1, 2)` | `None` |
| `'Q1-j3-p3'` | `1` | `(3, 0, 2, 1)` | `None` |
| `'DOUBLE-j1-p3'` | `0` | `(3, 0, 1, 2)` | `None` |
| `'DOUBLE-j1-p3'` | `1` | `(3, 0, 3, 1)` | `None` |
| `'DOUBLE-j1-p3'` | `2` | `(3, 0, 3, 2)` | `None` |
| `'DOUBLE-j1-p3'` | `3` | `(3, 0, 2, 1)` | `None` |
| `'UNEQUAL-j0-p3'` | `0` | `(2, 1, 0, 0)` | `((4, 8, 1, 2), 8, 10, 13, 3, 2, 2, 2, 3, 7, True)` |
| `'UNEQUAL-j2-p3'` | `0` | `(2, 1, 1, 0)` | `((5, 8, 2), 4, 6, 5, 3, -4, 2, -4, 0, 3, True)` |
| `'EQUALITY-j3-p3'` | `0` | `(0, 0, 1, 2)` | `((41, 18, 4), 1, 3, 5, 5, -4, 4, -4, 4, 3, True)` |
| `'EQUALITY-j3-p3'` | `1` | `(0, 0, 2, 1)` | `((42, 17, 4), 1, 3, 5, 6, -4, 4, -4, 4, 3, False)` |
| `'EQUALITY-j3-p3'` | `2` | `(0, 0, 1, 4)` | `((41, 20, 2), 1, 3, 5, 3, -4, 4, -4, 4, 3, False)` |
| `'EQUALITY-j3-p3'` | `3` | `(0, 0, 4, 1)` | `((44, 17, 2), 1, 3, 5, 6, -4, 4, -4, 4, 3, False)` |
| `'EQUALITY-j3-p3'` | `4` | `(0, 0, 2, 4)` | `((42, 20, 1), 1, 3, 5, 3, -4, 4, -4, 4, 3, False)` |
| `'EQUALITY-j3-p3'` | `5` | `(0, 0, 4, 2)` | `((44, 18, 1), 1, 3, 5, 5, -4, 4, -4, 4, 3, False)` |
| `'RICH-j1-p7'` | `0` | `(3, 0, 1, 4)` | `((161, 68, 2, 8, 16), 4, 6, 5, 3, 4, 2, 0, 11, 13, True)` |
| `'RICH-j1-p7'` | `1` | `(3, 0, 5, 1)` | `None` |
| `'RICH-j1-p7'` | `2` | `(3, 0, 3, 4)` | `((163, 68, 8, 16), 1, 3, 1, 3, 4, 2, 0, 11, 7, False)` |
| `'RICH-j1-p7'` | `3` | `(3, 0, 5, 2)` | `None` |
| `'RICH-j1-p7'` | `4` | `(3, 0, 5, 16)` | `((165, 80, 2, 8), 4, 6, 5, 7, 2, 6, -10, 1, 7, True)` |
| `'RICH-j1-p7'` | `5` | `(3, 0, 17, 4)` | `((177, 68, 2, 8), 4, 6, 5, 19, 8, 2, 4, 15, 7, False)` |
| `'RICH-j1-p7'` | `6` | `(3, 0, 9, 16)` | `((169, 80, 2, 4), 4, 6, 13, 15, 4, 6, -8, 3, 7, False)` |
| `'RICH-j1-p7'` | `7` | `(3, 0, 17, 8)` | `((177, 72, 2, 4), 4, 6, 13, 23, 4, 6, -8, 3, 7, False)` |
| `'RICH-j1-p7'` | `8` | `(3, 0, 3, 4)` | `((163, 68, 8, 16), 1, 3, 1, 3, 4, 2, 0, 11, 7, False)` |
| `'RICH-j1-p7'` | `9` | `(3, 0, 6, 1)` | `None` |
| `'RICH-j1-p7'` | `10` | `(3, 0, 2, 4)` | `((162, 68, 1, 8, 16), 4, 6, 5, 3, 4, 2, 0, 11, 13, False)` |
| `'RICH-j1-p7'` | `11` | `(3, 0, 6, 2)` | `None` |
| `'RICH-j1-p7'` | `12` | `(3, 0, 6, 16)` | `((166, 80, 1, 8), 4, 6, 5, 7, 2, 6, -10, 1, 7, False)` |
| `'RICH-j1-p7'` | `13` | `(3, 0, 18, 4)` | `((178, 68, 1, 8), 4, 6, 5, 19, 8, 2, 4, 15, 7, False)` |
| `'RICH-j1-p7'` | `14` | `(3, 0, 10, 16)` | `((170, 80, 1, 4), 4, 6, 13, 15, 4, 6, -8, 3, 7, False)` |
| `'RICH-j1-p7'` | `15` | `(3, 0, 18, 8)` | `((178, 72, 1, 4), 4, 6, 13, 23, 4, 6, -8, 3, 7, False)` |
| `'RICH-j1-p7'` | `16` | `(3, 0, 5, 4)` | `None` |
| `'RICH-j1-p7'` | `17` | `(3, 0, 4, 1)` | `((164, 65, 2, 8, 16), 7, 5, 1, 4, 4, 4, -4, 7, 13, False)` |
| `'RICH-j1-p7'` | `18` | `(3, 0, 6, 4)` | `None` |
| `'RICH-j1-p7'` | `19` | `(3, 0, 4, 2)` | `((164, 66, 1, 8, 16), 7, 5, 1, 4, 4, 4, -4, 7, 13, False)` |
| `'RICH-j1-p7'` | `20` | `(3, 0, 4, 16)` | `((164, 80, 1, 2, 8), 13, 15, 13, 7, 2, 6, -10, 1, 13, False)` |
| `'RICH-j1-p7'` | `21` | `(3, 0, 20, 4)` | `None` |
| `'RICH-j1-p7'` | `22` | `(3, 0, 12, 16)` | `((172, 80, 1, 2), 13, 15, 13, 15, 4, 6, -8, 3, 7, False)` |
| `'RICH-j1-p7'` | `23` | `(3, 0, 20, 8)` | `((180, 72, 1, 2), 13, 15, 13, 23, 4, 6, -8, 3, 7, False)` |
| `'RICH-j1-p9'` | `0` | `(3, 0, 1, 4)` | `((161, 68, 2, 8, 16), 4, 6, 5, 3, 4, 2, -2, 37, 13, True)` |
| `'RICH-j1-p9'` | `1` | `(3, 0, 5, 1)` | `None` |
| `'RICH-j1-p9'` | `2` | `(3, 0, 3, 4)` | `((163, 68, 8, 16), 1, 3, 1, 3, 4, 2, -2, 37, 7, False)` |
| `'RICH-j1-p9'` | `3` | `(3, 0, 5, 2)` | `None` |
| `'RICH-j1-p9'` | `4` | `(3, 0, 5, 16)` | `((165, 80, 2, 8), 4, 6, 5, 7, 2, 6, -36, 3, 7, True)` |
| `'RICH-j1-p9'` | `5` | `(3, 0, 17, 4)` | `((177, 68, 2, 8), 4, 6, 5, 19, 8, 2, 10, 49, 7, False)` |
| `'RICH-j1-p9'` | `6` | `(3, 0, 9, 16)` | `((169, 80, 2, 4), 4, 6, 13, 15, 4, 6, -30, 9, 7, False)` |
| `'RICH-j1-p9'` | `7` | `(3, 0, 17, 8)` | `((177, 72, 2, 4), 4, 6, 13, 23, 4, 6, -30, 9, 7, False)` |
| `'RICH-j1-p9'` | `8` | `(3, 0, 3, 4)` | `((163, 68, 8, 16), 1, 3, 1, 3, 4, 2, -2, 37, 7, False)` |
| `'RICH-j1-p9'` | `9` | `(3, 0, 6, 1)` | `None` |
| `'RICH-j1-p9'` | `10` | `(3, 0, 2, 4)` | `((162, 68, 1, 8, 16), 4, 6, 5, 3, 4, 2, -2, 37, 13, False)` |
| `'RICH-j1-p9'` | `11` | `(3, 0, 6, 2)` | `None` |
| `'RICH-j1-p9'` | `12` | `(3, 0, 6, 16)` | `((166, 80, 1, 8), 4, 6, 5, 7, 2, 6, -36, 3, 7, False)` |
| `'RICH-j1-p9'` | `13` | `(3, 0, 18, 4)` | `((178, 68, 1, 8), 4, 6, 5, 19, 8, 2, 10, 49, 7, False)` |
| `'RICH-j1-p9'` | `14` | `(3, 0, 10, 16)` | `((170, 80, 1, 4), 4, 6, 13, 15, 4, 6, -30, 9, 7, False)` |
| `'RICH-j1-p9'` | `15` | `(3, 0, 18, 8)` | `((178, 72, 1, 4), 4, 6, 13, 23, 4, 6, -30, 9, 7, False)` |
| `'RICH-j1-p9'` | `16` | `(3, 0, 5, 4)` | `None` |
| `'RICH-j1-p9'` | `17` | `(3, 0, 4, 1)` | `((164, 65, 2, 8, 16), 7, 5, 1, 4, 4, 4, -16, 23, 13, False)` |
| `'RICH-j1-p9'` | `18` | `(3, 0, 6, 4)` | `None` |
| `'RICH-j1-p9'` | `19` | `(3, 0, 4, 2)` | `((164, 66, 1, 8, 16), 7, 5, 1, 4, 4, 4, -16, 23, 13, False)` |
| `'RICH-j1-p9'` | `20` | `(3, 0, 4, 16)` | `((164, 80, 1, 2, 8), 13, 15, 13, 7, 2, 6, -36, 3, 13, False)` |
| `'RICH-j1-p9'` | `21` | `(3, 0, 20, 4)` | `None` |
| `'RICH-j1-p9'` | `22` | `(3, 0, 12, 16)` | `((172, 80, 1, 2), 13, 15, 13, 15, 4, 6, -30, 9, 7, False)` |
| `'RICH-j1-p9'` | `23` | `(3, 0, 20, 8)` | `((180, 72, 1, 2), 13, 15, 13, 23, 4, 6, -30, 9, 7, False)` |
| `'RICH-j3-p1'` | `0` | `(15, 0, 1, 4)` | `((161, 68, 2, 8, 16), 14, 12, 5, 3, -2, 2, 2, 7, 13, True)` |
| `'RICH-j3-p1'` | `1` | `(15, 0, 4, 1)` | `((164, 65, 2, 8, 16), 14, 12, 5, 6, -6, 2, -2, 3, 13, True)` |
| `'RICH-j3-p1'` | `2` | `(15, 0, 2, 4)` | `((162, 68, 1, 8, 16), 14, 12, 5, 3, -2, 2, 2, 7, 13, False)` |
| `'RICH-j3-p1'` | `3` | `(15, 0, 4, 2)` | `((164, 66, 1, 8, 16), 14, 12, 5, 5, -6, 2, -2, 3, 13, False)` |
| `'RICH-j3-p1'` | `4` | `(15, 0, 4, 16)` | `((164, 80, 1, 2, 8), 28, 30, 9, 6, -6, 2, -2, 3, 13, False)` |
| `'RICH-j3-p1'` | `5` | `(15, 0, 16, 4)` | `((176, 68, 1, 2, 8), 31, 29, 1, 16, -2, 2, 2, 7, 13, False)` |
| `'RICH-j3-p1'` | `6` | `(15, 0, 8, 16)` | `((168, 80, 1, 2, 4), 28, 30, 29, 15, -10, 4, -2, 3, 13, False)` |
| `'RICH-j3-p1'` | `7` | `(15, 0, 16, 8)` | `((176, 72, 1, 2, 4), 31, 29, 25, 22, -8, 4, 0, 5, 13, False)` |
| `'MIXED-j0-p0'` | `0` | `(10, 1, 0, 0)` | `((16, 32, 1, 2, 4, 8), 40, 40, 33, 8, 12, 4, 44, 41, 21, True)` |
| `'MIXED-j1-p0'` | `0` | `(10, 0, 1, 2)` | `((81, 34, 4, 8), 11, 9, 1, 1, 6, 4, 32, 36, 7, True)` |
| `'MIXED-j1-p0'` | `1` | `(10, 0, 3, 1)` | `None` |
| `'MIXED-j1-p0'` | `2` | `(10, 0, 1, 4)` | `((81, 36, 2, 8), 13, 15, 1, 1, 6, 4, 32, 36, 7, False)` |
| `'MIXED-j1-p0'` | `3` | `(10, 0, 5, 1)` | `None` |
| `'MIXED-j1-p0'` | `4` | `(10, 0, 1, 8)` | `((81, 40, 2, 4), 7, 5, 1, 1, 6, 4, 32, 36, 7, False)` |
| `'MIXED-j1-p0'` | `5` | `(10, 0, 9, 1)` | `None` |
| `'MIXED-j1-p0'` | `6` | `(10, 0, 3, 4)` | `((83, 36, 8), 4, 6, 5, 11, 20, 12, 100, 104, 3, False)` |
| `'MIXED-j1-p0'` | `7` | `(10, 0, 5, 2)` | `((85, 34, 8), 7, 5, 1, 5, 16, 12, 92, 96, 3, False)` |
| `'MIXED-j1-p0'` | `8` | `(10, 0, 3, 8)` | `None` |
| `'MIXED-j1-p0'` | `9` | `(10, 0, 9, 2)` | `None` |
| `'MIXED-j1-p0'` | `10` | `(10, 0, 5, 8)` | `((85, 40, 2), 7, 5, 1, 5, 16, 12, 92, 96, 3, False)` |
| `'MIXED-j1-p0'` | `11` | `(10, 0, 9, 4)` | `((89, 36, 2), 4, 6, 5, 11, 20, 12, 100, 104, 3, False)` |
| `'MIXED-j1-p0'` | `12` | `(10, 0, 3, 2)` | `None` |
| `'MIXED-j1-p0'` | `13` | `(10, 0, 2, 1)` | `((82, 33, 4, 8), 8, 10, 9, 10, 18, 8, 76, 80, 7, False)` |
| `'MIXED-j1-p0'` | `14` | `(10, 0, 3, 4)` | `((83, 36, 8), 4, 6, 5, 11, 20, 12, 100, 104, 3, False)` |
| `'MIXED-j1-p0'` | `15` | `(10, 0, 6, 1)` | `((86, 33, 8), 4, 6, 5, 14, 16, 16, 112, 116, 3, False)` |
| `'MIXED-j1-p0'` | `16` | `(10, 0, 3, 8)` | `None` |
| `'MIXED-j1-p0'` | `17` | `(10, 0, 10, 1)` | `((90, 33, 4), 1, 3, 1, 10, 18, 8, 76, 80, 3, False)` |
| `'MIXED-j1-p0'` | `18` | `(10, 0, 2, 4)` | `((82, 36, 1, 8), 8, 10, 9, 10, 18, 8, 76, 80, 7, False)` |
| `'MIXED-j1-p0'` | `19` | `(10, 0, 6, 2)` | `None` |
| `'MIXED-j1-p0'` | `20` | `(10, 0, 2, 8)` | `None` |
| `'MIXED-j1-p0'` | `21` | `(10, 0, 10, 2)` | `None` |
| `'MIXED-j1-p0'` | `22` | `(10, 0, 6, 8)` | `None` |
| `'MIXED-j1-p0'` | `23` | `(10, 0, 10, 4)` | `((90, 36, 1), 1, 3, 1, 10, 18, 8, 76, 80, 3, False)` |
| `'MIXED-j1-p0'` | `24` | `(10, 0, 5, 2)` | `((85, 34, 8), 7, 5, 1, 5, 16, 12, 92, 96, 3, False)` |
| `'MIXED-j1-p0'` | `25` | `(10, 0, 6, 1)` | `((86, 33, 8), 4, 6, 5, 14, 16, 16, 112, 116, 3, False)` |
| `'MIXED-j1-p0'` | `26` | `(10, 0, 5, 4)` | `None` |
| `'MIXED-j1-p0'` | `27` | `(10, 0, 4, 1)` | `((84, 33, 2, 8), 13, 15, 1, 4, 14, 8, 68, 72, 7, False)` |
| `'MIXED-j1-p0'` | `28` | `(10, 0, 5, 8)` | `((85, 40, 2), 7, 5, 1, 5, 16, 12, 92, 96, 3, False)` |
| `'MIXED-j1-p0'` | `29` | `(10, 0, 12, 1)` | `((92, 33, 2), 4, 6, 5, 14, 16, 16, 112, 116, 3, False)` |
| `'MIXED-j1-p0'` | `30` | `(10, 0, 6, 4)` | `None` |
| `'MIXED-j1-p0'` | `31` | `(10, 0, 4, 2)` | `((84, 34, 1, 8), 11, 9, 1, 4, 14, 8, 68, 72, 7, False)` |
| `'MIXED-j1-p0'` | `32` | `(10, 0, 6, 8)` | `None` |
| `'MIXED-j1-p0'` | `33` | `(10, 0, 12, 2)` | `None` |
| `'MIXED-j1-p0'` | `34` | `(10, 0, 4, 8)` | `((84, 40, 1, 2), 11, 9, 1, 4, 14, 8, 68, 72, 7, False)` |
| `'MIXED-j1-p0'` | `35` | `(10, 0, 12, 4)` | `None` |
| `'MIXED-j1-p0'` | `36` | `(10, 0, 9, 2)` | `None` |
| `'MIXED-j1-p0'` | `37` | `(10, 0, 10, 1)` | `((90, 33, 4), 1, 3, 1, 10, 18, 8, 76, 80, 3, False)` |
| `'MIXED-j1-p0'` | `38` | `(10, 0, 9, 4)` | `((89, 36, 2), 4, 6, 5, 11, 20, 12, 100, 104, 3, False)` |
| `'MIXED-j1-p0'` | `39` | `(10, 0, 12, 1)` | `((92, 33, 2), 4, 6, 5, 14, 16, 16, 112, 116, 3, False)` |
| `'MIXED-j1-p0'` | `40` | `(10, 0, 9, 8)` | `None` |
| `'MIXED-j1-p0'` | `41` | `(10, 0, 8, 1)` | `((88, 33, 2, 4), 4, 6, 5, 10, 18, 8, 76, 80, 7, False)` |
| `'MIXED-j1-p0'` | `42` | `(10, 0, 10, 4)` | `((90, 36, 1), 1, 3, 1, 10, 18, 8, 76, 80, 3, False)` |
| `'MIXED-j1-p0'` | `43` | `(10, 0, 12, 2)` | `None` |
| `'MIXED-j1-p0'` | `44` | `(10, 0, 10, 8)` | `None` |
| `'MIXED-j1-p0'` | `45` | `(10, 0, 8, 2)` | `None` |
| `'MIXED-j1-p0'` | `46` | `(10, 0, 12, 8)` | `None` |
| `'MIXED-j1-p0'` | `47` | `(10, 0, 8, 4)` | `((88, 36, 1, 2), 8, 10, 9, 10, 18, 8, 76, 80, 7, False)` |
| `'MIXED-j2-p0'` | `0` | `(10, 1, 1, 0)` | `((17, 32, 2, 4, 8), 20, 20, 13, 7, -18, 8, 4, 16, 13, True)` |
| `'MIXED-j2-p0'` | `1` | `(10, 1, 2, 0)` | `((18, 32, 1, 4, 8), 17, 17, 13, 7, -18, 8, 4, 16, 13, False)` |
| `'MIXED-j2-p0'` | `2` | `(10, 1, 4, 0)` | `((20, 32, 1, 2, 8), 24, 24, 13, 7, -18, 8, 4, 16, 13, False)` |
| `'MIXED-j2-p0'` | `3` | `(10, 1, 8, 0)` | `((24, 32, 1, 2, 4), 9, 9, 21, 13, -18, 10, 14, 26, 13, False)` |
| `'MIXED-j3-p0'` | `0` | `(10, 0, 1, 2)` | `((81, 34, 4, 8), 11, 9, 1, 1, -2, 2, 6, 17, 7, True)` |
| `'MIXED-j3-p0'` | `1` | `(10, 0, 2, 1)` | `((82, 33, 4, 8), 8, 10, 13, 14, -24, 12, 12, 23, 7, False)` |
| `'MIXED-j3-p0'` | `2` | `(10, 0, 1, 4)` | `((81, 36, 2, 8), 13, 15, 1, 1, -2, 2, 6, 17, 7, False)` |
| `'MIXED-j3-p0'` | `3` | `(10, 0, 4, 1)` | `((84, 33, 2, 8), 13, 15, 13, 14, -24, 12, 12, 23, 7, False)` |
| `'MIXED-j3-p0'` | `4` | `(10, 0, 1, 8)` | `((81, 40, 2, 4), 7, 5, 1, 1, -2, 2, 6, 17, 7, False)` |
| `'MIXED-j3-p0'` | `5` | `(10, 0, 8, 1)` | `((88, 33, 2, 4), 4, 6, 13, 14, -24, 12, 12, 23, 7, False)` |
| `'MIXED-j3-p0'` | `6` | `(10, 0, 2, 4)` | `((82, 36, 1, 8), 8, 10, 13, 11, -12, 10, 26, 37, 7, False)` |
| `'MIXED-j3-p0'` | `7` | `(10, 0, 4, 2)` | `((84, 34, 1, 8), 11, 9, 5, 5, -8, 6, 14, 25, 7, False)` |
| `'MIXED-j3-p0'` | `8` | `(10, 0, 2, 8)` | `None` |
| `'MIXED-j3-p0'` | `9` | `(10, 0, 8, 2)` | `None` |
| `'MIXED-j3-p0'` | `10` | `(10, 0, 4, 8)` | `((84, 40, 1, 2), 11, 9, 5, 5, -8, 6, 14, 25, 7, False)` |
| `'MIXED-j3-p0'` | `11` | `(10, 0, 8, 4)` | `((88, 36, 1, 2), 8, 10, 13, 11, -12, 10, 26, 37, 7, False)` |
| `'ODDFULL-j2-p3'` | `0` | `(4, 1, 1, 0)` | `((9, 16, 2, 4), 8, 10, 13, 7, -6, 4, -6, 0, 7, True)` |
| `'ODDFULL-j2-p3'` | `1` | `(4, 1, 2, 0)` | `((10, 16, 1, 4), 8, 10, 13, 7, -6, 4, -6, 0, 7, False)` |
| `'TIECARD-j3-p0'` | `0` | `(3, 0, 1, 4)` | `((41, 20, 2), 4, 6, 5, 3, -2, 2, 6, 10, 3, True)` |
| `'TIECARD-j3-p0'` | `1` | `(3, 0, 4, 1)` | `((44, 17, 2), 7, 5, 1, 4, -2, 2, 6, 10, 3, False)` |
| `'TIECARD-j3-p0'` | `2` | `(3, 0, 2, 4)` | `((42, 20, 1), 4, 6, 5, 3, -2, 2, 6, 10, 3, False)` |
| `'TIECARD-j3-p0'` | `3` | `(3, 0, 4, 2)` | `((44, 18, 1), 7, 5, 1, 4, -2, 2, 6, 10, 3, False)` |

### Fixture table: COORDINATE_RECOVERY

| query | family | classes | reduced_shore | original_shore | cut | C_minus | constant | raw |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `'UNEQUAL-j0-p3'` | `0` | `(4, 8, 1, 2)` | `13` | `3` | `3` | `0` | `-1` | `2` |
| `'RICH-j1-p7'` | `4` | `(165, 80, 2, 8)` | `5` | `7` | `1` | `9` | `-2` | `-10` |
| `'EQUALITY-j3-p3'` | `0` | `(41, 18, 4)` | `5` | `5` | `4` | `6` | `-2` | `-4` |



## ORACLE-075 — Counterexamples to shortcut minimization and hidden tie rules

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO6, BO9, BO13--BO14. RICH-j1-p7 starts with (U,c,h,raw)=(3,4,2,0)
and first attains its true minimum at family 4: (7,2,6,-10). At p9 the corresponding
early candidate is -2 and the true minimum is -36. Neither zero nor negativity licenses
an early return or truncated cover.

At RICH-j3-p1 the first selected minimum (6,-6,2,-2) ties a later
(15,-10,4,-2); preferring maximum h changes the ruled winner. At EQUALITY-j3-p3,
mask 5 is retained before mask 3. At TIECARD-j3-p0, the retained two-vertex mask 3
ties the later singleton mask 4, killing a minimum-cardinality secondary rule.
ODDFULL-j2-p3 has two feasible high-end families with zero cuts; both must execute.

The unrestricted ordinary trap has cut 0 and raw -1 on empty original U, below the
legal DOUBLE branch-0 residual 2. Ignoring parity/membership solves the wrong problem.

### Fixture table: TRAPS

| trap | query | comparison_family | comparison_U_c_h_raw | correct_family | correct_result |
| --- | --- | --- | --- | --- | --- |
| `'early-zero'` | `'RICH-j1-p7'` | `0` | `(3, 4, 2, 0)` | `4` | `(7, 2, 6, -10)` |
| `'early-negative'` | `'RICH-j1-p9'` | `0` | `(3, 4, 2, -2)` | `4` | `(7, 2, 6, -36)` |
| `'not-max-h'` | `'RICH-j3-p1'` | `6` | `(15, -10, 4, -2)` | `1` | `(6, -6, 2, -2)` |
| `'not-smallest-mask'` | `'EQUALITY-j3-p3'` | `2` | `(3, -4, 4, -4)` | `0` | `(5, -4, 4, -4)` |
| `'full-original-shore'` | `'UNEQUAL-j2-p3'` | `0` | `(3, -4, 2, -4)` | `0` | `(3, -4, 2, -4)` |
| `'not-smallest-cardinality'` | `'TIECARD-j3-p0'` | `1` | `(4, -2, 2, 6)` | `0` | `(3, -2, 2, 6)` |
| `'zero-cut-complete-scan'` | `'ODDFULL-j2-p3'` | `0` | `(7, -6, 4, -6)` | `0` | `(7, -6, 4, -6)` |

### Fixture table: UNRESTRICTED_TRAP

| query | unrestricted_original_shore | unrestricted_cut | unrestricted_raw | branch_result |
| --- | --- | --- | --- | --- |
| `'DOUBLE-j0-p3'` | `0` | `0` | `-1` | `(1, 2, 2, 2)` |



## ORACLE-076 — Diagnostic anchors and explicit temporary-query bookkeeping

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO16. STATS uses the exact declared order:
`(atomic_families_examined, atomic_families_feasible, parity_cut_calls,
ordinary_min_cut_calls, flow_augmentations, flow_bfs_scans, flow_peak_generated_value)`.
max_flow_calls is the fourth field as a DERIVED property, not a stored duplicate.

The ten anchors have 146 prescribed ordinary queries. Each FLOW_DIAGNOSTIC_TRACE
row includes its temporary arcs and least ordinary shore. The final cell lists every
BFS as (entries_scanned, bottleneck, failed_search_reached_mask): reached mask is None
on augmenting searches, bottleneck is zero only for the final failed search. The closed
policy scans adjacency entries in original canonical order and stops at first sink
discovery. Reverse entries are paired and count as scans. The failed search's reachability
is reused; no extra final BFS is counted. Flow peak is the maximum initial/generated
capacity, bottleneck, and accumulated value, not every integer in the composed solver.

These diagnostic expectations are obtained by an independent edge-index bookkeeping
replay, with every value/least shore separately checked against exhaustive cuts. The
standalone oracle audit imports NO production or flow module. A separate compatibility
run against the already-closed backend may confirm the replay, but does not establish
expected branch minima. Diagnostics never determine those minima.

### Fixture table: STATS

| query | seven_stats_fields | derived_max_flow_calls |
| --- | --- | --- |
| `'Q1-j0-p3'` | `(1, 0, 0, 0, 0, 0, 0)` | `0` |
| `'Q1-j1-p3'` | `(0, 0, 0, 0, 0, 0, 0)` | `0` |
| `'Q1-j2-p3'` | `(0, 0, 0, 0, 0, 0, 0)` | `0` |
| `'Q1-j3-p3'` | `(2, 0, 0, 0, 0, 0, 0)` | `0` |
| `'DOUBLE-j0-p3'` | `(1, 1, 1, 7, 6, 40, 3)` | `7` |
| `'DOUBLE-j0-p7'` | `(1, 1, 1, 7, 6, 52, 3)` | `7` |
| `'UNEQUAL-j0-p3'` | `(1, 1, 1, 7, 6, 36, 4)` | `7` |
| `'UNEQUAL-j2-p3'` | `(1, 1, 1, 3, 1, 7, 4)` | `3` |
| `'EQUALITY-j3-p3'` | `(6, 6, 6, 18, 24, 138, 6)` | `18` |
| `'RICH-j3-p1'` | `(8, 8, 8, 104, 148, 1138, 9)` | `104` |

### Fixture table: FLOW_DIAGNOSTIC_TRACE

| query | family | inside | outside | temporary_N | temporary_arcs | value | temporary_least_shore | augmentations_scans_peak | BFS_scans_bottleneck_failed_reached_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `'DOUBLE-j0-p3'` | `0` | `0` | `1` | `4` | `((1, 2, 1), (1, 3, 1), (2, 1, 1), (2, 3, 2), (3, 1, 1), (3, 2, 2))` | `0` | `1` | `(0, 0, 2)` | `((0, 0, 1),)` |
| `'DOUBLE-j0-p3'` | `0` | `0` | `2` | `3` | `((1, 2, 3), (2, 1, 3))` | `0` | `1` | `(0, 0, 3)` | `((0, 0, 1),)` |
| `'DOUBLE-j0-p3'` | `0` | `0` | `3` | `3` | `((1, 2, 3), (2, 1, 3))` | `0` | `1` | `(0, 0, 3)` | `((0, 0, 1),)` |
| `'DOUBLE-j0-p3'` | `0` | `2` | `1` | `3` | `((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 1), (2, 0, 2), (2, 1, 1))` | `2` | `5` | `(2, 17, 2)` | `((1, 1, None), (8, 1, None), (8, 0, 5))` |
| `'DOUBLE-j0-p3'` | `0` | `2` | `3` | `2` | `((0, 1, 3), (1, 0, 3))` | `3` | `1` | `(1, 3, 3)` | `((1, 3, None), (2, 0, 1))` |
| `'DOUBLE-j0-p3'` | `0` | `3` | `1` | `3` | `((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 1), (2, 0, 2), (2, 1, 1))` | `2` | `5` | `(2, 17, 2)` | `((1, 1, None), (8, 1, None), (8, 0, 5))` |
| `'DOUBLE-j0-p3'` | `0` | `3` | `2` | `2` | `((0, 1, 3), (1, 0, 3))` | `3` | `1` | `(1, 3, 3)` | `((1, 3, None), (2, 0, 1))` |
| `'DOUBLE-j0-p7'` | `0` | `0` | `1` | `4` | `((0, 2, 1), (0, 3, 1), (2, 0, 1), (2, 3, 2), (3, 0, 1), (3, 2, 2))` | `0` | `13` | `(0, 12, 2)` | `((12, 0, 13),)` |
| `'DOUBLE-j0-p7'` | `0` | `0` | `2` | `3` | `((0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 2, 2), (2, 0, 1), (2, 1, 2))` | `2` | `1` | `(2, 13, 2)` | `((1, 1, None), (8, 1, None), (4, 0, 1))` |
| `'DOUBLE-j0-p7'` | `0` | `0` | `3` | `3` | `((0, 1, 1), (0, 2, 1), (1, 0, 1), (1, 2, 2), (2, 0, 1), (2, 1, 2))` | `2` | `1` | `(2, 13, 2)` | `((1, 1, None), (8, 1, None), (4, 0, 1))` |
| `'DOUBLE-j0-p7'` | `0` | `2` | `1` | `3` | `((0, 2, 3), (2, 0, 3))` | `0` | `5` | `(0, 4, 3)` | `((4, 0, 5),)` |
| `'DOUBLE-j0-p7'` | `0` | `2` | `3` | `2` | `((0, 1, 3), (1, 0, 3))` | `3` | `1` | `(1, 3, 3)` | `((1, 3, None), (2, 0, 1))` |
| `'DOUBLE-j0-p7'` | `0` | `3` | `1` | `3` | `((0, 2, 3), (2, 0, 3))` | `0` | `5` | `(0, 4, 3)` | `((4, 0, 5),)` |
| `'DOUBLE-j0-p7'` | `0` | `3` | `2` | `2` | `((0, 1, 3), (1, 0, 3))` | `3` | `1` | `(1, 3, 3)` | `((1, 3, None), (2, 0, 1))` |
| `'UNEQUAL-j0-p3'` | `0` | `0` | `1` | `4` | `((1, 2, 2), (1, 3, 1), (2, 1, 2), (2, 3, 2), (3, 1, 1), (3, 2, 2))` | `0` | `1` | `(0, 0, 2)` | `((0, 0, 1),)` |
| `'UNEQUAL-j0-p3'` | `0` | `0` | `2` | `3` | `((1, 2, 3), (2, 1, 3))` | `0` | `1` | `(0, 0, 3)` | `((0, 0, 1),)` |
| `'UNEQUAL-j0-p3'` | `0` | `0` | `3` | `3` | `((1, 2, 4), (2, 1, 4))` | `0` | `1` | `(0, 0, 4)` | `((0, 0, 1),)` |
| `'UNEQUAL-j0-p3'` | `0` | `2` | `1` | `3` | `((0, 1, 2), (0, 2, 2), (1, 0, 2), (1, 2, 1), (2, 0, 2), (2, 1, 1))` | `3` | `5` | `(2, 17, 3)` | `((1, 2, None), (8, 1, None), (8, 0, 5))` |
| `'UNEQUAL-j0-p3'` | `0` | `2` | `3` | `2` | `((0, 1, 4), (1, 0, 4))` | `4` | `1` | `(1, 3, 4)` | `((1, 4, None), (2, 0, 1))` |
| `'UNEQUAL-j0-p3'` | `0` | `3` | `1` | `3` | `((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 2), (2, 0, 2), (2, 1, 2))` | `3` | `1` | `(2, 13, 3)` | `((1, 1, None), (8, 2, None), (4, 0, 1))` |
| `'UNEQUAL-j0-p3'` | `0` | `3` | `2` | `2` | `((0, 1, 3), (1, 0, 3))` | `3` | `1` | `(1, 3, 3)` | `((1, 3, None), (2, 0, 1))` |
| `'UNEQUAL-j2-p3'` | `0` | `0` | `1` | `3` | `((0, 2, 4), (2, 0, 4))` | `0` | `5` | `(0, 4, 4)` | `((4, 0, 5),)` |
| `'UNEQUAL-j2-p3'` | `0` | `0` | `2` | `2` | `((0, 1, 4), (1, 0, 4))` | `4` | `1` | `(1, 3, 4)` | `((1, 4, None), (2, 0, 1))` |
| `'UNEQUAL-j2-p3'` | `0` | `2` | `1` | `2` | `()` | `0` | `1` | `(0, 0, 0)` | `()` |
| `'EQUALITY-j3-p3'` | `0` | `0` | `1` | `3` | `((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1))` | `4` | `5` | `(2, 17, 4)` | `((1, 3, None), (8, 1, None), (8, 0, 5))` |
| `'EQUALITY-j3-p3'` | `0` | `0` | `2` | `2` | `((0, 1, 6), (1, 0, 6))` | `6` | `1` | `(1, 3, 6)` | `((1, 6, None), (2, 0, 1))` |
| `'EQUALITY-j3-p3'` | `0` | `2` | `1` | `2` | `((0, 1, 4), (1, 0, 4))` | `4` | `1` | `(1, 3, 4)` | `((1, 4, None), (2, 0, 1))` |
| `'EQUALITY-j3-p3'` | `1` | `0` | `1` | `3` | `((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1))` | `4` | `5` | `(2, 17, 4)` | `((1, 3, None), (8, 1, None), (8, 0, 5))` |
| `'EQUALITY-j3-p3'` | `1` | `0` | `2` | `2` | `((0, 1, 6), (1, 0, 6))` | `6` | `1` | `(1, 3, 6)` | `((1, 6, None), (2, 0, 1))` |
| `'EQUALITY-j3-p3'` | `1` | `2` | `1` | `2` | `((0, 1, 4), (1, 0, 4))` | `4` | `1` | `(1, 3, 4)` | `((1, 4, None), (2, 0, 1))` |
| `'EQUALITY-j3-p3'` | `2` | `0` | `1` | `3` | `((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1))` | `4` | `5` | `(2, 17, 4)` | `((1, 3, None), (8, 1, None), (8, 0, 5))` |
| `'EQUALITY-j3-p3'` | `2` | `0` | `2` | `2` | `((0, 1, 6), (1, 0, 6))` | `6` | `1` | `(1, 3, 6)` | `((1, 6, None), (2, 0, 1))` |
| `'EQUALITY-j3-p3'` | `2` | `2` | `1` | `2` | `((0, 1, 4), (1, 0, 4))` | `4` | `1` | `(1, 3, 4)` | `((1, 4, None), (2, 0, 1))` |
| `'EQUALITY-j3-p3'` | `3` | `0` | `1` | `3` | `((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1))` | `4` | `5` | `(2, 17, 4)` | `((1, 3, None), (8, 1, None), (8, 0, 5))` |
| `'EQUALITY-j3-p3'` | `3` | `0` | `2` | `2` | `((0, 1, 6), (1, 0, 6))` | `6` | `1` | `(1, 3, 6)` | `((1, 6, None), (2, 0, 1))` |
| `'EQUALITY-j3-p3'` | `3` | `2` | `1` | `2` | `((0, 1, 4), (1, 0, 4))` | `4` | `1` | `(1, 3, 4)` | `((1, 4, None), (2, 0, 1))` |
| `'EQUALITY-j3-p3'` | `4` | `0` | `1` | `3` | `((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1))` | `4` | `5` | `(2, 17, 4)` | `((1, 3, None), (8, 1, None), (8, 0, 5))` |
| `'EQUALITY-j3-p3'` | `4` | `0` | `2` | `2` | `((0, 1, 6), (1, 0, 6))` | `6` | `1` | `(1, 3, 6)` | `((1, 6, None), (2, 0, 1))` |
| `'EQUALITY-j3-p3'` | `4` | `2` | `1` | `2` | `((0, 1, 4), (1, 0, 4))` | `4` | `1` | `(1, 3, 4)` | `((1, 4, None), (2, 0, 1))` |
| `'EQUALITY-j3-p3'` | `5` | `0` | `1` | `3` | `((0, 1, 3), (0, 2, 3), (1, 0, 3), (1, 2, 1), (2, 0, 3), (2, 1, 1))` | `4` | `5` | `(2, 17, 4)` | `((1, 3, None), (8, 1, None), (8, 0, 5))` |
| `'EQUALITY-j3-p3'` | `5` | `0` | `2` | `2` | `((0, 1, 6), (1, 0, 6))` | `6` | `1` | `(1, 3, 6)` | `((1, 6, None), (2, 0, 1))` |
| `'EQUALITY-j3-p3'` | `5` | `2` | `1` | `2` | `((0, 1, 4), (1, 0, 4))` | `4` | `1` | `(1, 3, 4)` | `((1, 4, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `0` | `1` | `5` | `((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 1), (1, 4, 3), (2, 1, 2), (3, 1, 1), (3, 4, 1), (4, 1, 3), (4, 3, 1))` | `5` | `1` | `(1, 3, 5)` | `((1, 5, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `0` | `2` | `4` | `((0, 1, 5), (1, 0, 5), (1, 2, 1), (1, 3, 3), (2, 1, 1), (2, 3, 1), (3, 1, 3), (3, 2, 1))` | `5` | `1` | `(1, 3, 5)` | `((1, 5, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `0` | `3` | `4` | `((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 4), (2, 1, 2), (3, 1, 4))` | `5` | `1` | `(1, 3, 5)` | `((1, 5, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `0` | `4` | `4` | `((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2))` | `5` | `1` | `(1, 3, 5)` | `((1, 5, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `2` | `1` | `4` | `((0, 1, 7), (1, 0, 7), (1, 2, 1), (1, 3, 3), (2, 1, 1), (2, 3, 1), (3, 1, 3), (3, 2, 1))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `2` | `3` | `3` | `((0, 1, 7), (1, 0, 7), (1, 2, 4), (2, 1, 4))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `2` | `4` | `3` | `((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `3` | `1` | `4` | `((0, 1, 6), (0, 3, 1), (1, 0, 6), (1, 2, 2), (1, 3, 3), (2, 1, 2), (3, 0, 1), (3, 1, 3))` | `7` | `1` | `(2, 13, 7)` | `((1, 6, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `3` | `2` | `3` | `((0, 1, 6), (0, 2, 1), (1, 0, 6), (1, 2, 3), (2, 0, 1), (2, 1, 3))` | `7` | `1` | `(2, 13, 7)` | `((1, 6, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `3` | `4` | `3` | `((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `4` | `1` | `4` | `((0, 1, 8), (0, 3, 1), (1, 0, 8), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1))` | `9` | `1` | `(2, 13, 9)` | `((1, 8, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `4` | `2` | `3` | `((0, 1, 8), (0, 2, 1), (1, 0, 8), (1, 2, 1), (2, 0, 1), (2, 1, 1))` | `9` | `1` | `(2, 13, 9)` | `((1, 8, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `0` | `4` | `3` | `3` | `((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2))` | `9` | `1` | `(1, 3, 9)` | `((1, 9, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `1` | `0` | `1` | `5` | `((0, 1, 2), (0, 2, 2), (0, 4, 1), (1, 0, 2), (1, 2, 0), (1, 3, 1), (1, 4, 2), (2, 0, 2), (2, 1, 0), (3, 1, 1), (3, 4, 1), (4, 0, 1), (4, 1, 2), (4, 3, 1))` | `3` | `5` | `(2, 26, 3)` | `((1, 2, None), (15, 1, None), (10, 0, 5))` |
| `'RICH-j3-p1'` | `1` | `0` | `2` | `4` | `((0, 1, 4), (0, 3, 1), (1, 0, 4), (1, 2, 1), (1, 3, 2), (2, 1, 1), (2, 3, 1), (3, 0, 1), (3, 1, 2), (3, 2, 1))` | `5` | `1` | `(2, 14, 5)` | `((1, 4, None), (9, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `1` | `0` | `3` | `4` | `((0, 1, 2), (0, 2, 2), (0, 3, 1), (1, 0, 2), (1, 2, 0), (1, 3, 3), (2, 0, 2), (2, 1, 0), (3, 0, 1), (3, 1, 3))` | `3` | `5` | `(2, 25, 3)` | `((1, 2, None), (14, 1, None), (10, 0, 5))` |
| `'RICH-j3-p1'` | `1` | `0` | `4` | `4` | `((0, 1, 3), (0, 2, 2), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2))` | `3` | `5` | `(1, 9, 3)` | `((1, 3, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `1` | `2` | `1` | `4` | `((0, 1, 2), (0, 3, 1), (1, 0, 2), (1, 2, 1), (1, 3, 2), (2, 1, 1), (2, 3, 1), (3, 0, 1), (3, 1, 2), (3, 2, 1))` | `3` | `1` | `(2, 14, 3)` | `((1, 2, None), (9, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `1` | `2` | `3` | `3` | `((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 3), (2, 0, 1), (2, 1, 3))` | `3` | `1` | `(2, 13, 3)` | `((1, 2, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `1` | `2` | `4` | `3` | `((0, 1, 3), (1, 0, 3), (1, 2, 2), (2, 1, 2))` | `3` | `1` | `(1, 3, 3)` | `((1, 3, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `1` | `3` | `1` | `4` | `((0, 1, 3), (0, 2, 2), (0, 3, 2), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 0, 2), (3, 1, 2))` | `5` | `5` | `(2, 25, 5)` | `((1, 3, None), (14, 2, None), (10, 0, 5))` |
| `'RICH-j3-p1'` | `1` | `3` | `2` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 2), (2, 0, 2), (2, 1, 2))` | `7` | `1` | `(2, 13, 7)` | `((1, 5, None), (8, 2, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `1` | `3` | `4` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `5` | `5` | `(1, 9, 5)` | `((1, 5, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `1` | `4` | `1` | `4` | `((0, 1, 4), (0, 2, 2), (0, 3, 1), (1, 0, 4), (1, 2, 0), (1, 3, 1), (2, 0, 2), (2, 1, 0), (3, 0, 1), (3, 1, 1))` | `5` | `5` | `(2, 25, 5)` | `((1, 4, None), (14, 1, None), (10, 0, 5))` |
| `'RICH-j3-p1'` | `1` | `4` | `2` | `3` | `((0, 1, 6), (0, 2, 1), (1, 0, 6), (1, 2, 1), (2, 0, 1), (2, 1, 1))` | `7` | `1` | `(2, 13, 7)` | `((1, 6, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `1` | `4` | `3` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `5` | `5` | `(1, 9, 5)` | `((1, 5, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `2` | `0` | `1` | `5` | `((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 1), (1, 4, 3), (2, 1, 2), (3, 1, 1), (3, 4, 1), (4, 1, 3), (4, 3, 1))` | `5` | `1` | `(1, 3, 5)` | `((1, 5, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `0` | `2` | `4` | `((0, 1, 5), (1, 0, 5), (1, 2, 1), (1, 3, 3), (2, 1, 1), (2, 3, 1), (3, 1, 3), (3, 2, 1))` | `5` | `1` | `(1, 3, 5)` | `((1, 5, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `0` | `3` | `4` | `((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 4), (2, 1, 2), (3, 1, 4))` | `5` | `1` | `(1, 3, 5)` | `((1, 5, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `0` | `4` | `4` | `((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2))` | `5` | `1` | `(1, 3, 5)` | `((1, 5, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `2` | `1` | `4` | `((0, 1, 7), (1, 0, 7), (1, 2, 1), (1, 3, 3), (2, 1, 1), (2, 3, 1), (3, 1, 3), (3, 2, 1))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `2` | `3` | `3` | `((0, 1, 7), (1, 0, 7), (1, 2, 4), (2, 1, 4))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `2` | `4` | `3` | `((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `3` | `1` | `4` | `((0, 1, 6), (0, 3, 1), (1, 0, 6), (1, 2, 2), (1, 3, 3), (2, 1, 2), (3, 0, 1), (3, 1, 3))` | `7` | `1` | `(2, 13, 7)` | `((1, 6, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `3` | `2` | `3` | `((0, 1, 6), (0, 2, 1), (1, 0, 6), (1, 2, 3), (2, 0, 1), (2, 1, 3))` | `7` | `1` | `(2, 13, 7)` | `((1, 6, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `3` | `4` | `3` | `((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `4` | `1` | `4` | `((0, 1, 8), (0, 3, 1), (1, 0, 8), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1))` | `9` | `1` | `(2, 13, 9)` | `((1, 8, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `4` | `2` | `3` | `((0, 1, 8), (0, 2, 1), (1, 0, 8), (1, 2, 1), (2, 0, 1), (2, 1, 1))` | `9` | `1` | `(2, 13, 9)` | `((1, 8, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `2` | `4` | `3` | `3` | `((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2))` | `9` | `1` | `(1, 3, 9)` | `((1, 9, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `3` | `0` | `1` | `5` | `((0, 1, 2), (0, 2, 2), (0, 4, 1), (1, 0, 2), (1, 2, 0), (1, 3, 1), (1, 4, 2), (2, 0, 2), (2, 1, 0), (3, 1, 1), (3, 4, 1), (4, 0, 1), (4, 1, 2), (4, 3, 1))` | `3` | `5` | `(2, 26, 3)` | `((1, 2, None), (15, 1, None), (10, 0, 5))` |
| `'RICH-j3-p1'` | `3` | `0` | `2` | `4` | `((0, 1, 4), (0, 3, 1), (1, 0, 4), (1, 2, 1), (1, 3, 2), (2, 1, 1), (2, 3, 1), (3, 0, 1), (3, 1, 2), (3, 2, 1))` | `5` | `1` | `(2, 14, 5)` | `((1, 4, None), (9, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `3` | `0` | `3` | `4` | `((0, 1, 2), (0, 2, 2), (0, 3, 1), (1, 0, 2), (1, 2, 0), (1, 3, 3), (2, 0, 2), (2, 1, 0), (3, 0, 1), (3, 1, 3))` | `3` | `5` | `(2, 25, 3)` | `((1, 2, None), (14, 1, None), (10, 0, 5))` |
| `'RICH-j3-p1'` | `3` | `0` | `4` | `4` | `((0, 1, 3), (0, 2, 2), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2))` | `3` | `5` | `(1, 9, 3)` | `((1, 3, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `3` | `2` | `1` | `4` | `((0, 1, 2), (0, 3, 1), (1, 0, 2), (1, 2, 1), (1, 3, 2), (2, 1, 1), (2, 3, 1), (3, 0, 1), (3, 1, 2), (3, 2, 1))` | `3` | `1` | `(2, 14, 3)` | `((1, 2, None), (9, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `3` | `2` | `3` | `3` | `((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 3), (2, 0, 1), (2, 1, 3))` | `3` | `1` | `(2, 13, 3)` | `((1, 2, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `3` | `2` | `4` | `3` | `((0, 1, 3), (1, 0, 3), (1, 2, 2), (2, 1, 2))` | `3` | `1` | `(1, 3, 3)` | `((1, 3, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `3` | `3` | `1` | `4` | `((0, 1, 3), (0, 2, 2), (0, 3, 2), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 0, 2), (3, 1, 2))` | `5` | `5` | `(2, 25, 5)` | `((1, 3, None), (14, 2, None), (10, 0, 5))` |
| `'RICH-j3-p1'` | `3` | `3` | `2` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 2), (2, 0, 2), (2, 1, 2))` | `7` | `1` | `(2, 13, 7)` | `((1, 5, None), (8, 2, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `3` | `3` | `4` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `5` | `5` | `(1, 9, 5)` | `((1, 5, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `3` | `4` | `1` | `4` | `((0, 1, 4), (0, 2, 2), (0, 3, 1), (1, 0, 4), (1, 2, 0), (1, 3, 1), (2, 0, 2), (2, 1, 0), (3, 0, 1), (3, 1, 1))` | `5` | `5` | `(2, 25, 5)` | `((1, 4, None), (14, 1, None), (10, 0, 5))` |
| `'RICH-j3-p1'` | `3` | `4` | `2` | `3` | `((0, 1, 6), (0, 2, 1), (1, 0, 6), (1, 2, 1), (2, 0, 1), (2, 1, 1))` | `7` | `1` | `(2, 13, 7)` | `((1, 6, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `3` | `4` | `3` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `5` | `5` | `(1, 9, 5)` | `((1, 5, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `4` | `0` | `1` | `5` | `((0, 1, 1), (0, 2, 2), (0, 3, 2), (1, 0, 1), (1, 2, 0), (1, 3, 0), (1, 4, 2), (2, 0, 2), (2, 1, 0), (3, 0, 2), (3, 1, 0), (4, 1, 2))` | `1` | `13` | `(1, 15, 2)` | `((1, 1, None), (14, 0, 13))` |
| `'RICH-j3-p1'` | `4` | `0` | `2` | `4` | `((0, 1, 3), (0, 2, 2), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2))` | `3` | `5` | `(1, 9, 3)` | `((1, 3, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `4` | `0` | `3` | `4` | `((0, 1, 3), (0, 2, 2), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2))` | `3` | `5` | `(1, 9, 3)` | `((1, 3, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `4` | `0` | `4` | `4` | `((0, 1, 1), (0, 2, 2), (0, 3, 2), (1, 0, 1), (1, 2, 0), (1, 3, 0), (2, 0, 2), (2, 1, 0), (3, 0, 2), (3, 1, 0))` | `1` | `13` | `(1, 15, 2)` | `((1, 1, None), (14, 0, 13))` |
| `'RICH-j3-p1'` | `4` | `2` | `1` | `4` | `((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2))` | `1` | `5` | `(1, 9, 2)` | `((1, 1, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `4` | `2` | `3` | `3` | `((0, 1, 3), (1, 0, 3), (1, 2, 2), (2, 1, 2))` | `3` | `1` | `(1, 3, 3)` | `((1, 3, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `4` | `2` | `4` | `3` | `((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `1` | `5` | `(1, 9, 2)` | `((1, 1, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `4` | `3` | `1` | `4` | `((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 0), (1, 3, 2), (2, 0, 2), (2, 1, 0), (3, 1, 2))` | `1` | `5` | `(1, 9, 2)` | `((1, 1, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `4` | `3` | `2` | `3` | `((0, 1, 3), (1, 0, 3), (1, 2, 2), (2, 1, 2))` | `3` | `1` | `(1, 3, 3)` | `((1, 3, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `4` | `3` | `4` | `3` | `((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `1` | `5` | `(1, 9, 2)` | `((1, 1, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `4` | `4` | `1` | `4` | `((0, 1, 3), (0, 2, 2), (0, 3, 2), (1, 0, 3), (1, 2, 0), (1, 3, 0), (2, 0, 2), (2, 1, 0), (3, 0, 2), (3, 1, 0))` | `3` | `13` | `(1, 15, 3)` | `((1, 3, None), (14, 0, 13))` |
| `'RICH-j3-p1'` | `4` | `4` | `2` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `5` | `5` | `(1, 9, 5)` | `((1, 5, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `4` | `4` | `3` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `5` | `5` | `(1, 9, 5)` | `((1, 5, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `5` | `0` | `1` | `5` | `((0, 1, 6), (0, 4, 1), (1, 0, 6), (1, 2, 2), (1, 3, 2), (1, 4, 1), (2, 1, 2), (3, 1, 2), (4, 0, 1), (4, 1, 1))` | `7` | `1` | `(2, 13, 7)` | `((1, 6, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `0` | `2` | `4` | `((0, 1, 6), (0, 3, 1), (1, 0, 6), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1))` | `7` | `1` | `(2, 13, 7)` | `((1, 6, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `0` | `3` | `4` | `((0, 1, 6), (0, 3, 1), (1, 0, 6), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1))` | `7` | `1` | `(2, 13, 7)` | `((1, 6, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `0` | `4` | `4` | `((0, 1, 7), (1, 0, 7), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `2` | `1` | `4` | `((0, 1, 8), (0, 3, 1), (1, 0, 8), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1))` | `9` | `1` | `(2, 13, 9)` | `((1, 8, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `2` | `3` | `3` | `((0, 1, 8), (0, 2, 1), (1, 0, 8), (1, 2, 1), (2, 0, 1), (2, 1, 1))` | `9` | `1` | `(2, 13, 9)` | `((1, 8, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `2` | `4` | `3` | `((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2))` | `9` | `1` | `(1, 3, 9)` | `((1, 9, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `3` | `1` | `4` | `((0, 1, 8), (0, 3, 1), (1, 0, 8), (1, 2, 2), (1, 3, 1), (2, 1, 2), (3, 0, 1), (3, 1, 1))` | `9` | `1` | `(2, 13, 9)` | `((1, 8, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `3` | `2` | `3` | `((0, 1, 8), (0, 2, 1), (1, 0, 8), (1, 2, 1), (2, 0, 1), (2, 1, 1))` | `9` | `1` | `(2, 13, 9)` | `((1, 8, None), (8, 1, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `3` | `4` | `3` | `((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2))` | `9` | `1` | `(1, 3, 9)` | `((1, 9, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `4` | `1` | `4` | `((0, 1, 7), (1, 0, 7), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `4` | `2` | `3` | `((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `5` | `4` | `3` | `3` | `((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `6` | `0` | `1` | `5` | `((0, 1, 2), (0, 4, 3), (1, 0, 2), (1, 2, 0), (1, 3, 0), (1, 4, 1), (2, 1, 0), (2, 4, 2), (3, 1, 0), (3, 4, 2), (4, 0, 3), (4, 1, 1), (4, 2, 2), (4, 3, 2))` | `3` | `29` | `(2, 31, 3)` | `((1, 2, None), (10, 1, None), (20, 0, 29))` |
| `'RICH-j3-p1'` | `6` | `0` | `2` | `4` | `((0, 1, 2), (0, 3, 3), (1, 0, 2), (1, 2, 0), (1, 3, 3), (2, 1, 0), (2, 3, 2), (3, 0, 3), (3, 1, 3), (3, 2, 2))` | `5` | `1` | `(2, 14, 5)` | `((1, 2, None), (9, 3, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `6` | `0` | `3` | `4` | `((0, 1, 2), (0, 3, 3), (1, 0, 2), (1, 2, 0), (1, 3, 3), (2, 1, 0), (2, 3, 2), (3, 0, 3), (3, 1, 3), (3, 2, 2))` | `5` | `1` | `(2, 14, 5)` | `((1, 2, None), (9, 3, None), (4, 0, 1))` |
| `'RICH-j3-p1'` | `6` | `0` | `4` | `4` | `((0, 1, 5), (1, 0, 5), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2))` | `5` | `1` | `(1, 3, 5)` | `((1, 5, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `6` | `2` | `1` | `4` | `((0, 1, 2), (0, 3, 5), (1, 0, 2), (1, 2, 0), (1, 3, 1), (2, 1, 0), (2, 3, 2), (3, 0, 5), (3, 1, 1), (3, 2, 2))` | `3` | `13` | `(2, 24, 5)` | `((1, 2, None), (9, 1, None), (14, 0, 13))` |
| `'RICH-j3-p1'` | `6` | `2` | `3` | `3` | `((0, 1, 2), (0, 2, 5), (1, 0, 2), (1, 2, 3), (2, 0, 5), (2, 1, 3))` | `5` | `5` | `(2, 17, 5)` | `((1, 2, None), (8, 3, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `6` | `2` | `4` | `3` | `((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `6` | `3` | `1` | `4` | `((0, 1, 2), (0, 3, 5), (1, 0, 2), (1, 2, 0), (1, 3, 1), (2, 1, 0), (2, 3, 2), (3, 0, 5), (3, 1, 1), (3, 2, 2))` | `3` | `13` | `(2, 24, 5)` | `((1, 2, None), (9, 1, None), (14, 0, 13))` |
| `'RICH-j3-p1'` | `6` | `3` | `2` | `3` | `((0, 1, 2), (0, 2, 5), (1, 0, 2), (1, 2, 3), (2, 0, 5), (2, 1, 3))` | `5` | `5` | `(2, 17, 5)` | `((1, 2, None), (8, 3, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `6` | `3` | `4` | `3` | `((0, 1, 7), (1, 0, 7), (1, 2, 2), (2, 1, 2))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `6` | `4` | `1` | `4` | `((0, 1, 3), (0, 2, 2), (0, 3, 2), (1, 0, 3), (1, 2, 0), (1, 3, 0), (2, 0, 2), (2, 1, 0), (3, 0, 2), (3, 1, 0))` | `3` | `13` | `(1, 15, 3)` | `((1, 3, None), (14, 0, 13))` |
| `'RICH-j3-p1'` | `6` | `4` | `2` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `5` | `5` | `(1, 9, 5)` | `((1, 5, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `6` | `4` | `3` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `5` | `5` | `(1, 9, 5)` | `((1, 5, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `7` | `0` | `1` | `5` | `((0, 1, 3), (0, 4, 4), (1, 0, 3), (1, 2, 0), (1, 3, 0), (2, 1, 0), (2, 4, 2), (3, 1, 0), (3, 4, 2), (4, 0, 4), (4, 2, 2), (4, 3, 2))` | `3` | `29` | `(1, 19, 4)` | `((1, 3, None), (18, 0, 29))` |
| `'RICH-j3-p1'` | `7` | `0` | `2` | `4` | `((0, 1, 3), (0, 3, 4), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 1, 0), (2, 3, 2), (3, 0, 4), (3, 1, 2), (3, 2, 2))` | `5` | `13` | `(2, 24, 5)` | `((1, 3, None), (9, 2, None), (14, 0, 13))` |
| `'RICH-j3-p1'` | `7` | `0` | `3` | `4` | `((0, 1, 3), (0, 3, 4), (1, 0, 3), (1, 2, 0), (1, 3, 2), (2, 1, 0), (2, 3, 2), (3, 0, 4), (3, 1, 2), (3, 2, 2))` | `5` | `13` | `(2, 24, 5)` | `((1, 3, None), (9, 2, None), (14, 0, 13))` |
| `'RICH-j3-p1'` | `7` | `0` | `4` | `4` | `((0, 1, 7), (1, 0, 7), (1, 2, 2), (1, 3, 2), (2, 1, 2), (3, 1, 2))` | `7` | `1` | `(1, 3, 7)` | `((1, 7, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `7` | `2` | `1` | `4` | `((0, 1, 3), (0, 3, 6), (1, 0, 3), (1, 2, 0), (2, 1, 0), (2, 3, 2), (3, 0, 6), (3, 2, 2))` | `3` | `13` | `(1, 13, 6)` | `((1, 3, None), (12, 0, 13))` |
| `'RICH-j3-p1'` | `7` | `2` | `3` | `3` | `((0, 1, 3), (0, 2, 6), (1, 0, 3), (1, 2, 2), (2, 0, 6), (2, 1, 2))` | `5` | `5` | `(2, 17, 6)` | `((1, 3, None), (8, 2, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `7` | `2` | `4` | `3` | `((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2))` | `9` | `1` | `(1, 3, 9)` | `((1, 9, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `7` | `3` | `1` | `4` | `((0, 1, 3), (0, 3, 6), (1, 0, 3), (1, 2, 0), (2, 1, 0), (2, 3, 2), (3, 0, 6), (3, 2, 2))` | `3` | `13` | `(1, 13, 6)` | `((1, 3, None), (12, 0, 13))` |
| `'RICH-j3-p1'` | `7` | `3` | `2` | `3` | `((0, 1, 3), (0, 2, 6), (1, 0, 3), (1, 2, 2), (2, 0, 6), (2, 1, 2))` | `5` | `5` | `(2, 17, 6)` | `((1, 3, None), (8, 2, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `7` | `3` | `4` | `3` | `((0, 1, 9), (1, 0, 9), (1, 2, 2), (2, 1, 2))` | `9` | `1` | `(1, 3, 9)` | `((1, 9, None), (2, 0, 1))` |
| `'RICH-j3-p1'` | `7` | `4` | `1` | `4` | `((0, 1, 3), (0, 2, 2), (0, 3, 2), (1, 0, 3), (1, 2, 0), (1, 3, 0), (2, 0, 2), (2, 1, 0), (3, 0, 2), (3, 1, 0))` | `3` | `13` | `(1, 15, 3)` | `((1, 3, None), (14, 0, 13))` |
| `'RICH-j3-p1'` | `7` | `4` | `2` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `5` | `5` | `(1, 9, 5)` | `((1, 5, None), (8, 0, 5))` |
| `'RICH-j3-p1'` | `7` | `4` | `3` | `3` | `((0, 1, 5), (0, 2, 2), (1, 0, 5), (1, 2, 0), (2, 0, 2), (2, 1, 0))` | `5` | `5` | `(1, 9, 5)` | `((1, 5, None), (8, 0, 5))` |



## ORACLE-077 — Valid record declarations and exact public rejection matrix

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO1--BO3. The three records are frozen/slotted, structural equality/hash, no ordering.
BranchOracleContext takes only a normally constructed exact Instance; its families field
is init=False and derived once. BranchOracleResult fields are (shore,c,h,residual), with
shore>0,h>0, signed c and residual, all exact built-in ints. A standalone result cannot
check an upper universe bound or attest domain membership/value attainment. Stats requires
only seven nonnegative exact ints, not cross-field relationships. All nine INPUTS rows
are valid normal context inputs; the additional seven valid result/stats rows are below.

Symbolic substitutions: INT_SUB and TUPLE_SUB are ordinary subclasses of their built-ins;
INSTANCE_SUB and CONTEXT_SUB are normally initialized subclasses, not constructor-bypassing
forgeries; BruteInstance is a valid closed-verifier instance; ExactValue is a valid closed
record; ITERATOR is a one-pass iterator; HOSTILE is a distinct object whose conversion,
comparison, truthiness and iteration hooks raise a sentinel. These substitutions must be
rejected by exact type checks without invoking those hooks. They are descriptions for
future test construction, not string arguments to the production API.

The 179 rows comprise 171 exact built-in ValueError declarations and eight ordinary
Python arity/frozen-mutation declarations. They are NOT executed against absent Unit 12
production. Query validation order is context, branch, validate_pair BEFORE any emptiness
inspection. Q1 covers zero-descriptor and nonempty-but-entirely-empty tuples for invalid
parameters; MIXED covers nonempty domains. All prior arguments must satisfy their guards
when isolating a later phase. Frozen-record and signature tests belong to consuming RED.

### Fixture table: VALID_RECORDS

| type | constructor_arguments |
| --- | --- |
| `'BranchOracleResult'` | `(1, 0, 1, 0)` |
| `'BranchOracleResult'` | `(3, -4, 2, -4)` |
| `'BranchOracleResult'` | `(1, 6, 4, 2)` |
| `'BranchOracleResult'` | `(1361129467683753853853498429727072845824, -2, 2, -2)` |
| `'BranchOracleStats'` | `(0, 0, 0, 0, 0, 0, 0)` |
| `'BranchOracleStats'` | `(1, 9, 7, 3, 11, 0, 0)` |
| `'BranchOracleStats'` | `(2, 0, 0, 0, 0, 0, 0)` |

### Fixture table: REJECTIONS

| case | target | field | symbolic_substitution | exact_exception | precondition |
| --- | --- | --- | --- | --- | --- |
| `'V001'` | `'BranchOracleContext'` | `'instance'` | `'None'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V002'` | `'BranchOracleContext'` | `'instance'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V003'` | `'BranchOracleContext'` | `'instance'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V004'` | `'BranchOracleContext'` | `'instance'` | `'Fraction(1,1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V005'` | `'BranchOracleContext'` | `'instance'` | `'ExactValue(1,1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V006'` | `'BranchOracleContext'` | `'instance'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V007'` | `'BranchOracleContext'` | `'instance'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V008'` | `'BranchOracleContext'` | `'instance'` | `'BruteInstance'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V009'` | `'BranchOracleContext'` | `'instance'` | `'INSTANCE_SUB'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V010'` | `'BranchOracleResult'` | `'shore'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V011'` | `'BranchOracleResult'` | `'shore'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V012'` | `'BranchOracleResult'` | `'shore'` | `'Fraction(1,1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V013'` | `'BranchOracleResult'` | `'shore'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V014'` | `'BranchOracleResult'` | `'shore'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V015'` | `'BranchOracleResult'` | `'shore'` | `'None'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V016'` | `'BranchOracleResult'` | `'shore'` | `'0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V017'` | `'BranchOracleResult'` | `'shore'` | `'-1'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V018'` | `'BranchOracleResult'` | `'c'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V019'` | `'BranchOracleResult'` | `'c'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V020'` | `'BranchOracleResult'` | `'c'` | `'Fraction(1,1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V021'` | `'BranchOracleResult'` | `'c'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V022'` | `'BranchOracleResult'` | `'c'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V023'` | `'BranchOracleResult'` | `'c'` | `'None'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V024'` | `'BranchOracleResult'` | `'h'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V025'` | `'BranchOracleResult'` | `'h'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V026'` | `'BranchOracleResult'` | `'h'` | `'Fraction(1,1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V027'` | `'BranchOracleResult'` | `'h'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V028'` | `'BranchOracleResult'` | `'h'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V029'` | `'BranchOracleResult'` | `'h'` | `'None'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V030'` | `'BranchOracleResult'` | `'h'` | `'0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V031'` | `'BranchOracleResult'` | `'h'` | `'-1'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V032'` | `'BranchOracleResult'` | `'residual'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V033'` | `'BranchOracleResult'` | `'residual'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V034'` | `'BranchOracleResult'` | `'residual'` | `'Fraction(1,1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V035'` | `'BranchOracleResult'` | `'residual'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V036'` | `'BranchOracleResult'` | `'residual'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V037'` | `'BranchOracleResult'` | `'residual'` | `'None'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V038'` | `'BranchOracleStats'` | `'atomic_families_examined'` | `'-1'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V039'` | `'BranchOracleStats'` | `'atomic_families_examined'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V040'` | `'BranchOracleStats'` | `'atomic_families_examined'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V041'` | `'BranchOracleStats'` | `'atomic_families_examined'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V042'` | `'BranchOracleStats'` | `'atomic_families_examined'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V043'` | `'BranchOracleStats'` | `'atomic_families_feasible'` | `'-1'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V044'` | `'BranchOracleStats'` | `'atomic_families_feasible'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V045'` | `'BranchOracleStats'` | `'atomic_families_feasible'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V046'` | `'BranchOracleStats'` | `'atomic_families_feasible'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V047'` | `'BranchOracleStats'` | `'atomic_families_feasible'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V048'` | `'BranchOracleStats'` | `'parity_cut_calls'` | `'-1'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V049'` | `'BranchOracleStats'` | `'parity_cut_calls'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V050'` | `'BranchOracleStats'` | `'parity_cut_calls'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V051'` | `'BranchOracleStats'` | `'parity_cut_calls'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V052'` | `'BranchOracleStats'` | `'parity_cut_calls'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V053'` | `'BranchOracleStats'` | `'ordinary_min_cut_calls'` | `'-1'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V054'` | `'BranchOracleStats'` | `'ordinary_min_cut_calls'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V055'` | `'BranchOracleStats'` | `'ordinary_min_cut_calls'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V056'` | `'BranchOracleStats'` | `'ordinary_min_cut_calls'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V057'` | `'BranchOracleStats'` | `'ordinary_min_cut_calls'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V058'` | `'BranchOracleStats'` | `'flow_augmentations'` | `'-1'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V059'` | `'BranchOracleStats'` | `'flow_augmentations'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V060'` | `'BranchOracleStats'` | `'flow_augmentations'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V061'` | `'BranchOracleStats'` | `'flow_augmentations'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V062'` | `'BranchOracleStats'` | `'flow_augmentations'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V063'` | `'BranchOracleStats'` | `'flow_bfs_scans'` | `'-1'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V064'` | `'BranchOracleStats'` | `'flow_bfs_scans'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V065'` | `'BranchOracleStats'` | `'flow_bfs_scans'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V066'` | `'BranchOracleStats'` | `'flow_bfs_scans'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V067'` | `'BranchOracleStats'` | `'flow_bfs_scans'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V068'` | `'BranchOracleStats'` | `'flow_peak_generated_value'` | `'-1'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V069'` | `'BranchOracleStats'` | `'flow_peak_generated_value'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V070'` | `'BranchOracleStats'` | `'flow_peak_generated_value'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V071'` | `'BranchOracleStats'` | `'flow_peak_generated_value'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V072'` | `'BranchOracleStats'` | `'flow_peak_generated_value'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V073'` | `'exact_branch_min'` | `'context'` | `'None'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V074'` | `'exact_branch_min'` | `'context'` | `'Instance(Q1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V075'` | `'exact_branch_min'` | `'context'` | `'CONTEXT_SUB(Q1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V076'` | `'exact_branch_min'` | `'context'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V077'` | `'exact_branch_min'` | `'context'` | `'()'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V078'` | `'exact_branch_min'` | `'branch'` | `'-1'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V079'` | `'exact_branch_min'` | `'branch'` | `'4'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V080'` | `'exact_branch_min'` | `'branch'` | `'True'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V081'` | `'exact_branch_min'` | `'branch'` | `'1.0'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V082'` | `'exact_branch_min'` | `'branch'` | `'INT_SUB(1)'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V083'` | `'exact_branch_min'` | `'branch'` | `'HOSTILE'` | `'ValueError'` | `'all earlier arguments valid'` |
| `'V084'` | `'exact_branch_min'` | `'parameter'` | `'None'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V085'` | `'exact_branch_min'` | `'parameter'` | `'True'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V086'` | `'exact_branch_min'` | `'parameter'` | `'1.0'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V087'` | `'exact_branch_min'` | `'parameter'` | `'Fraction(1,2)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V088'` | `'exact_branch_min'` | `'parameter'` | `'ExactValue(1,2)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V089'` | `'exact_branch_min'` | `'parameter'` | `'[1,2]'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V090'` | `'exact_branch_min'` | `'parameter'` | `'ITERATOR((1,2))'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V091'` | `'exact_branch_min'` | `'parameter'` | `'TUPLE_SUB((1,2))'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V092'` | `'exact_branch_min'` | `'parameter'` | `'()'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V093'` | `'exact_branch_min'` | `'parameter'` | `'(1,)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V094'` | `'exact_branch_min'` | `'parameter'` | `'(1,2,3)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V095'` | `'exact_branch_min'` | `'parameter'` | `'(True,1)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V096'` | `'exact_branch_min'` | `'parameter'` | `'(1,True)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V097'` | `'exact_branch_min'` | `'parameter'` | `'(INT_SUB(1),1)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V098'` | `'exact_branch_min'` | `'parameter'` | `'(1,INT_SUB(1))'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V099'` | `'exact_branch_min'` | `'parameter'` | `'(1.0,1)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V100'` | `'exact_branch_min'` | `'parameter'` | `'(1,1.0)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V101'` | `'exact_branch_min'` | `'parameter'` | `'(HOSTILE,1)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V102'` | `'exact_branch_min'` | `'parameter'` | `'(1,HOSTILE)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V103'` | `'exact_branch_min'` | `'parameter'` | `'(0,0)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V104'` | `'exact_branch_min'` | `'parameter'` | `'(1,-1)'` | `'ValueError'` | `'normal Q1 context; branch=0; empty source domain'` |
| `'V105'` | `'exact_branch_min'` | `'parameter'` | `'None'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V106'` | `'exact_branch_min'` | `'parameter'` | `'True'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V107'` | `'exact_branch_min'` | `'parameter'` | `'1.0'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V108'` | `'exact_branch_min'` | `'parameter'` | `'Fraction(1,2)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V109'` | `'exact_branch_min'` | `'parameter'` | `'ExactValue(1,2)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V110'` | `'exact_branch_min'` | `'parameter'` | `'[1,2]'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V111'` | `'exact_branch_min'` | `'parameter'` | `'ITERATOR((1,2))'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V112'` | `'exact_branch_min'` | `'parameter'` | `'TUPLE_SUB((1,2))'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V113'` | `'exact_branch_min'` | `'parameter'` | `'()'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V114'` | `'exact_branch_min'` | `'parameter'` | `'(1,)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V115'` | `'exact_branch_min'` | `'parameter'` | `'(1,2,3)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V116'` | `'exact_branch_min'` | `'parameter'` | `'(True,1)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V117'` | `'exact_branch_min'` | `'parameter'` | `'(1,True)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V118'` | `'exact_branch_min'` | `'parameter'` | `'(INT_SUB(1),1)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V119'` | `'exact_branch_min'` | `'parameter'` | `'(1,INT_SUB(1))'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V120'` | `'exact_branch_min'` | `'parameter'` | `'(1.0,1)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V121'` | `'exact_branch_min'` | `'parameter'` | `'(1,1.0)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V122'` | `'exact_branch_min'` | `'parameter'` | `'(HOSTILE,1)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V123'` | `'exact_branch_min'` | `'parameter'` | `'(1,HOSTILE)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V124'` | `'exact_branch_min'` | `'parameter'` | `'(0,0)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V125'` | `'exact_branch_min'` | `'parameter'` | `'(1,-1)'` | `'ValueError'` | `'normal Q1 context; branch=1; empty source domain'` |
| `'V126'` | `'exact_branch_min'` | `'parameter'` | `'None'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V127'` | `'exact_branch_min'` | `'parameter'` | `'True'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V128'` | `'exact_branch_min'` | `'parameter'` | `'1.0'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V129'` | `'exact_branch_min'` | `'parameter'` | `'Fraction(1,2)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V130'` | `'exact_branch_min'` | `'parameter'` | `'ExactValue(1,2)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V131'` | `'exact_branch_min'` | `'parameter'` | `'[1,2]'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V132'` | `'exact_branch_min'` | `'parameter'` | `'ITERATOR((1,2))'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V133'` | `'exact_branch_min'` | `'parameter'` | `'TUPLE_SUB((1,2))'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V134'` | `'exact_branch_min'` | `'parameter'` | `'()'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V135'` | `'exact_branch_min'` | `'parameter'` | `'(1,)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V136'` | `'exact_branch_min'` | `'parameter'` | `'(1,2,3)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V137'` | `'exact_branch_min'` | `'parameter'` | `'(True,1)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V138'` | `'exact_branch_min'` | `'parameter'` | `'(1,True)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V139'` | `'exact_branch_min'` | `'parameter'` | `'(INT_SUB(1),1)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V140'` | `'exact_branch_min'` | `'parameter'` | `'(1,INT_SUB(1))'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V141'` | `'exact_branch_min'` | `'parameter'` | `'(1.0,1)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V142'` | `'exact_branch_min'` | `'parameter'` | `'(1,1.0)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V143'` | `'exact_branch_min'` | `'parameter'` | `'(HOSTILE,1)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V144'` | `'exact_branch_min'` | `'parameter'` | `'(1,HOSTILE)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V145'` | `'exact_branch_min'` | `'parameter'` | `'(0,0)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V146'` | `'exact_branch_min'` | `'parameter'` | `'(1,-1)'` | `'ValueError'` | `'normal Q1 context; branch=2; empty source domain'` |
| `'V147'` | `'exact_branch_min'` | `'parameter'` | `'None'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V148'` | `'exact_branch_min'` | `'parameter'` | `'True'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V149'` | `'exact_branch_min'` | `'parameter'` | `'1.0'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V150'` | `'exact_branch_min'` | `'parameter'` | `'Fraction(1,2)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V151'` | `'exact_branch_min'` | `'parameter'` | `'ExactValue(1,2)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V152'` | `'exact_branch_min'` | `'parameter'` | `'[1,2]'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V153'` | `'exact_branch_min'` | `'parameter'` | `'ITERATOR((1,2))'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V154'` | `'exact_branch_min'` | `'parameter'` | `'TUPLE_SUB((1,2))'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V155'` | `'exact_branch_min'` | `'parameter'` | `'()'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V156'` | `'exact_branch_min'` | `'parameter'` | `'(1,)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V157'` | `'exact_branch_min'` | `'parameter'` | `'(1,2,3)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V158'` | `'exact_branch_min'` | `'parameter'` | `'(True,1)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V159'` | `'exact_branch_min'` | `'parameter'` | `'(1,True)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V160'` | `'exact_branch_min'` | `'parameter'` | `'(INT_SUB(1),1)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V161'` | `'exact_branch_min'` | `'parameter'` | `'(1,INT_SUB(1))'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V162'` | `'exact_branch_min'` | `'parameter'` | `'(1.0,1)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V163'` | `'exact_branch_min'` | `'parameter'` | `'(1,1.0)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V164'` | `'exact_branch_min'` | `'parameter'` | `'(HOSTILE,1)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V165'` | `'exact_branch_min'` | `'parameter'` | `'(1,HOSTILE)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V166'` | `'exact_branch_min'` | `'parameter'` | `'(0,0)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V167'` | `'exact_branch_min'` | `'parameter'` | `'(1,-1)'` | `'ValueError'` | `'normal Q1 context; branch=3; empty source domain'` |
| `'V168'` | `'exact_branch_min'` | `'parameter'` | `'(0,0)'` | `'ValueError'` | `'normal MIXED context; branch=1; nonempty source domain'` |
| `'V169'` | `'exact_branch_min'` | `'parameter'` | `'(1,-1)'` | `'ValueError'` | `'normal MIXED context; branch=1; nonempty source domain'` |
| `'V170'` | `'exact_branch_min'` | `'parameter'` | `'[1,2]'` | `'ValueError'` | `'normal MIXED context; branch=1; nonempty source domain'` |
| `'V171'` | `'exact_branch_min'` | `'parameter'` | `'(True,1)'` | `'ValueError'` | `'normal MIXED context; branch=1; nonempty source domain'` |
| `'V172'` | `'BranchOracleContext'` | `'call or mutation'` | `'extra families=()'` | `'TypeError'` | `'normal Python behavior; not exact-ValueError data guard'` |
| `'V173'` | `'BranchOracleContext'` | `'call or mutation'` | `'missing instance'` | `'TypeError'` | `'normal Python behavior; not exact-ValueError data guard'` |
| `'V174'` | `'BranchOracleResult'` | `'call or mutation'` | `'missing residual'` | `'TypeError'` | `'normal Python behavior; not exact-ValueError data guard'` |
| `'V175'` | `'BranchOracleStats'` | `'call or mutation'` | `'extra max_flow_calls=0'` | `'TypeError'` | `'normal Python behavior; not exact-ValueError data guard'` |
| `'V176'` | `'exact_branch_min'` | `'call or mutation'` | `'missing parameter'` | `'TypeError'` | `'normal Python behavior; not exact-ValueError data guard'` |
| `'V177'` | `'normal context'` | `'call or mutation'` | `'assign families=()'` | `'FrozenInstanceError'` | `'normal Python behavior; not exact-ValueError data guard'` |
| `'V178'` | `'normal result'` | `'call or mutation'` | `'assign h=1'` | `'FrozenInstanceError'` | `'normal Python behavior; not exact-ValueError data guard'` |
| `'V179'` | `'normal stats'` | `'call or mutation'` | `'assign ordinary_min_cut_calls=1'` | `'FrozenInstanceError'` | `'normal Python behavior; not exact-ValueError data guard'` |



## ORACLE-078 — Explicit internal failures, exception propagation, and context reuse

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO8, BO10--BO11, BO17--BO18. FAILURE rows distinguish violated closed-dependency
promises from malformed public input and from mathematical infeasibility. Injected
sum/domain failures are deliberate private seam probes, not normally possible outputs
of correct closed sums on active source-domain members. Do not silently repair any
invalid denominator, mask, or residual. No successful aggregate diagnostics are returned
on failure. Forging frozen objects by bypassing constructors is outside this contract.

REUSE fixes a sequence on one RICH context. Its instance/families and order do not change.
Only preparation calls the enumerator, exactly once. Each feasible query has its own
original network, even when a raw parameter is repeated; no incumbent or offsets survive
between queries. Labels may change external names but not these algorithmic results.

### Fixture table: FAILURES

| case | substitution | precondition | required_outcome | boundary |
| --- | --- | --- | --- | --- |
| `'F01'` | `'reduce_atomic_family returns None'` | `'known-nonempty descriptor'` | `'RuntimeError'` | `'do not skip; do not return infeasible'` |
| `'F02'` | `'minimum_parity_cut returns (None, legal_stats)'` | `'known-nonempty reduced problem'` | `'RuntimeError'` | `'do not skip; no completed stats/result'` |
| `'F03'` | `'lifting yields finite mask missing forced vertex'` | `'candidate I-membership false'` | `'RuntimeError'` | `'before original residual comparison'` |
| `'F04'` | `'lifting yields finite mask with forbidden vertex'` | `'candidate O-membership false'` | `'RuntimeError'` | `'before original residual comparison'` |
| `'F05'` | `'lifting yields finite wrong parity mask'` | `'candidate parity false'` | `'RuntimeError'` | `'before original residual comparison'` |
| `'F06'` | `'original-sum seam yields failed D_j condition'` | `'type-correct closed-sum substitution'` | `'RuntimeError'` | `'before raw residual/recovery retention'` |
| `'F07'` | `'original-sum seam yields h<=0'` | `'explicit promise failure'` | `'RuntimeError'` | `'no make_pair repair or sign flip'` |
| `'F08'` | `'recovered objective differs from B*c-A*h'` | `'well-formed candidate and nonnegative cut value'` | `'RuntimeError'` | `'even if false recovered value looks smaller'` |
| `'F09'` | `'closed reduction raises backend sentinel'` | `'dependency call exception'` | `'same exception propagates'` | `'no blanket ValueError/None conversion'` |
| `'F10'` | `'closed minimum raises backend sentinel'` | `'dependency call exception'` | `'same exception propagates'` | `'no false infeasibility'` |
| `'F11'` | `'lifting/universe validator raises ValueError'` | `'out-of-universe mask'` | `'same exception propagates'` | `'not converted to None/RuntimeError'` |
| `'F12'` | `'different legal stats from backend'` | `'identical legal exact optimum'` | `'same result; altered aggregate stats'` | `'stats never select candidate'` |
| `'F13'` | `'legal alternative exact within-family minimizer'` | `'matching source/cut identity'` | `'exact value and family/domain retained'` | `'engineering winner may follow supplied legal candidate; no least-branch claim'` |
| `'F14'` | `'attempt supplied incomplete cover'` | `'ordinary context constructor'` | `'TypeError'` | `'no accepted families injection API'` |

### Fixture table: REUSE

| step | query | result | count_prefix | fresh_original_network_if_feasible |
| --- | --- | --- | --- | --- |
| `0` | `'RICH-j0-p0'` | `(1, 2, 2, 14)` | `(1, 1, 1, 31)` | `True` |
| `1` | `'RICH-j1-p7'` | `(7, 2, 6, -10)` | `(24, 17, 17, 149)` | `True` |
| `2` | `'RICH-j2-p3'` | `(23, -10, 4, -10)` | `(5, 5, 5, 49)` | `True` |
| `3` | `'RICH-j3-p1'` | `(6, -6, 2, -2)` | `(8, 8, 8, 104)` | `True` |
| `4` | `'RICH-j1-p0'` | `(3, 4, 2, 18)` | `(24, 17, 17, 149)` | `True` |
| `5` | `'RICH-j0-p4'` | `(1, 2, 2, 6)` | `(1, 1, 1, 31)` | `True` |
| `6` | `'RICH-j1-p7'` | `(7, 2, 6, -10)` | `(24, 17, 17, 149)` | `True` |
| `7` | `'RICH-j2-p9'` | `(23, -10, 4, -58)` | `(5, 5, 5, 49)` | `True` |
| `8` | `'RICH-j3-p0'` | `(6, -6, 2, -2)` | `(8, 8, 8, 104)` | `True` |



## ORACLE-079 — Frozen exhaustive original-domain branch corpus

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO4--BO7, BO13--BO16, BO21. Enumerate n=2 then n=3. List unordered vertex pairs
lexicographically. Enumerate their multiplicities in {0,1,2} in product order; omit zero
records. Discard isolated-vertex patterns. Enumerate each f(v) in 1..d_q(v), product order,
so every input is active. This gives 5 two-vertex and 324 three-vertex instances.
For each instance visit branches 0,1,2,3 and all ten PARAMETERS in listed order.
Enumerate original shores as masks 0..2^n-1 and test the source domain DIRECTLY.

There are 13,160 fixed-parameter queries. The family source cover is independently
compared to original domains before minimization. The graph-side recalculation checks
sign routing on all original shores, contraction on all geometric shores of each
feasible family, and the least ordinary restrictions by exhaustive cut enumeration.
The second direct-source derivation never uses those cut values to compute expected raw
minima. Their deterministic result/count streams agree with the pinned fingerprint.

`specified_ordinary_calls=138720` is an EXPECTED future Unit 12 backend-call count,
not an observed production invocation count in this pre-code audit. Overlapping source
and cut cross-checks share domains; their totals must not be added as disjoint coverage.

### Fixture table: CORPUS_COUNTS

| metric | value |
| --- | --- |
| `'all_empty_descriptor_queries'` | `1550` |
| `'branch_domain_shore_checks'` | `10448` |
| `'domain_memberships'` | `3354` |
| `'empty_descriptors_once'` | `2736` |
| `'family_descriptors_once'` | `6140` |
| `'family_examinations'` | `61400` |
| `'feasible_family_calls'` | `34040` |
| `'feasible_queries'` | `11370` |
| `'full_shore_winners'` | `1825` |
| `'infeasible_queries'` | `1790` |
| `'instances'` | `329` |
| `'multiple_original_argmins'` | `3271` |
| `'n2_instances'` | `5` |
| `'n3_instances'` | `324` |
| `'negative_minima'` | `6218` |
| `'positive_minima'` | `4357` |
| `'queries'` | `13160` |
| `'specified_ordinary_calls'` | `138720` |
| `'zero_descriptor_queries'` | `240` |
| `'zero_minima'` | `795` |

### Fixture table: BRANCH_CORPUS_COUNTS

| j | counts |
| --- | --- |
| `0` | `{'all_empty_descriptor_queries': 680, 'family_examinations': 3290, 'feasible_family_calls': 2610, 'feasible_queries': 2610, 'full_shore_winners': 325, 'infeasible_queries': 680, 'multiple_original_argmins': 1047, 'negative_minima': 694, 'positive_minima': 1701, 'queries': 3290, 'specified_ordinary_calls': 33750, 'zero_minima': 215}` |
| `1` | `{'all_empty_descriptor_queries': 600, 'family_examinations': 34040, 'feasible_family_calls': 12360, 'feasible_queries': 2470, 'full_shore_winners': 0, 'infeasible_queries': 820, 'multiple_original_argmins': 667, 'negative_minima': 561, 'positive_minima': 1688, 'queries': 3290, 'specified_ordinary_calls': 26760, 'zero_descriptor_queries': 220, 'zero_minima': 221}` |
| `2` | `{'all_empty_descriptor_queries': 250, 'family_examinations': 6330, 'feasible_family_calls': 5590, 'feasible_queries': 3020, 'full_shore_winners': 1500, 'infeasible_queries': 270, 'multiple_original_argmins': 647, 'negative_minima': 2399, 'positive_minima': 430, 'queries': 3290, 'specified_ordinary_calls': 37850, 'zero_descriptor_queries': 20, 'zero_minima': 191}` |
| `3` | `{'all_empty_descriptor_queries': 20, 'family_examinations': 17740, 'feasible_family_calls': 13480, 'feasible_queries': 3270, 'full_shore_winners': 0, 'infeasible_queries': 20, 'multiple_original_argmins': 910, 'negative_minima': 2564, 'positive_minima': 538, 'queries': 3290, 'specified_ordinary_calls': 40360, 'zero_minima': 168}` |

### Fixture table: CORPUS_FINGERPRINT

| encoding | sha256 |
| --- | --- |
| `'for serial, j, parameter: JSON compact tuple(serial,j,parameter,result,argmins,winner_family,counts) plus LF'` | `'979de1a78b82b55c591d5f25e69e30c13838a88596f82acc15d9589dfc9ccd5e'` |



## ORACLE-080 — Raw scaling, large integers, and no ratio normalization

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO15, BO19--BO20. LARGE_CASES uses n=2, edges=((0,1,q),), f=(1,2), q=2^e
for e in (1,2,8,64,4096), all four branches, and parameters (-3,2),(0,7),(5,3).
These 60 rows preserve exact types and never expand q into copies. Independent formulas:
D0 has candidates U=1 with (c,h)=(q,q), and U=3 with (2,2q-2).
D1 has U=2 with (q,q-2) only when q>2. D2 has U=3 with (-2q,2).
D3 has U=2 with (-2,2). Every raw value is B*c-A*h; D0 ties follow the fixed least
ordinary / first-retained rules, not reduced-fraction ordering.

The table records signs, bit lengths, counts, and SHA-256 of the compact JSON result
array (or literal JSON null), without LF. It does not replace those explicit formulas
with a hash-only oracle. Large f/c/h or residual magnitudes do not change vertex universes.

For raw parameter scaling, multiply both submitted A and B by 2^e for each listed e
on RICH-j1-p7, RICH-j3-p1, MIXED-j0-p0, MIXED-j2-p3. These 20 checks retain U,c,h,
scale raw by 2^e, and preserve the prescribed family/ordinary count prefix. No general
claim of equal augmentation/scan/bit-cost counters across magnitudes is made.

### Fixture table: LARGE_CASES

| q_exponent | j | A_B | original_shore_or_None | c_h_raw_bit_lengths | raw_sign | count_prefix | result_tuple_JSON_SHA256 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `1` | `0` | `(-3, 2)` | `1` | `(2, 2, 4)` | `1` | `(1, 1, 1, 7)` | `'87d0cec4a13ef282f70f1e3b5254291a98bc8eb353ee1dd2c3539396d3dc0721'` |
| `1` | `0` | `(0, 7)` | `1` | `(2, 2, 4)` | `1` | `(1, 1, 1, 7)` | `'4c7d5c8fe47bb66b9cad0d2feff0afd8ca77aeb6687cdf69e99e47dbfa5a7c45'` |
| `1` | `0` | `(5, 3)` | `1` | `(2, 2, 3)` | `-1` | `(1, 1, 1, 7)` | `'dff87bd6dc7a66596e742ea556539917a44a59db87d2389db17b3d2bf7f07d33'` |
| `1` | `1` | `(-3, 2)` | `None` | `None` | `None` | `(2, 0, 0, 0)` | `'74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b'` |
| `1` | `1` | `(0, 7)` | `None` | `None` | `None` | `(2, 0, 0, 0)` | `'74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b'` |
| `1` | `1` | `(5, 3)` | `None` | `None` | `None` | `(2, 0, 0, 0)` | `'74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b'` |
| `1` | `2` | `(-3, 2)` | `3` | `(3, 2, 2)` | `-1` | `(1, 1, 1, 3)` | `'83a700c98940b400a70d6dabdbc24c5bcb60d320fd17dfa5285d2cd5dad09760'` |
| `1` | `2` | `(0, 7)` | `3` | `(3, 2, 5)` | `-1` | `(1, 1, 1, 3)` | `'169f1255c5621dea8ca0b1565d18c6bdbad6136b367981bcf045883b4c27b7f5'` |
| `1` | `2` | `(5, 3)` | `3` | `(3, 2, 5)` | `-1` | `(1, 1, 1, 3)` | `'8c66591343c5e58160108b726cee9b3deb55dee85339d61d6c57a89c543fb206'` |
| `1` | `3` | `(-3, 2)` | `2` | `(2, 2, 2)` | `1` | `(2, 1, 1, 1)` | `'fa0c5d32e239af9e641ba72de5edb96c1731fc6ebbd2120d49bd8f7858d9aed3'` |
| `1` | `3` | `(0, 7)` | `2` | `(2, 2, 4)` | `-1` | `(2, 1, 1, 1)` | `'5dfaf2a2211fae88fe8a1bac37afcc933351fa06fbc004b96edfaf8e9cf8da93'` |
| `1` | `3` | `(5, 3)` | `2` | `(2, 2, 5)` | `-1` | `(2, 1, 1, 1)` | `'fdac2271c941c36158f8167501e847f2ba2509450daab97d2b3005eaf4655186'` |
| `2` | `0` | `(-3, 2)` | `1` | `(3, 3, 5)` | `1` | `(1, 1, 1, 7)` | `'0b7ae91fa5bdab0958d3e859867c5dfe602047016013b6a0277d86b64b9f376e'` |
| `2` | `0` | `(0, 7)` | `3` | `(2, 3, 4)` | `1` | `(1, 1, 1, 7)` | `'200836be2e822db1637ab6213e143a3b414150f6761746f7e8266585fa259477'` |
| `2` | `0` | `(5, 3)` | `3` | `(2, 3, 5)` | `-1` | `(1, 1, 1, 7)` | `'9bb49ed8180327dc6db4a9100e15da1919c7d75f7ce1c57b6fdaadc408af1381'` |
| `2` | `1` | `(-3, 2)` | `2` | `(3, 2, 4)` | `1` | `(4, 1, 1, 1)` | `'e09af57b4e51551198dcd6aaae4e5ff12a1f370198676b41764db6bab04ccb4a'` |
| `2` | `1` | `(0, 7)` | `2` | `(3, 2, 5)` | `1` | `(4, 1, 1, 1)` | `'a069d1687d9920c3b24d27af3e81506b36d866e1e2df7c6b6cc1131d313a8bc0'` |
| `2` | `1` | `(5, 3)` | `2` | `(3, 2, 2)` | `1` | `(4, 1, 1, 1)` | `'35120a11505b4c7667e511de287ee9ab9716f87175fd392479e7e4461bfac11f'` |
| `2` | `2` | `(-3, 2)` | `3` | `(4, 2, 4)` | `-1` | `(1, 1, 1, 3)` | `'9733a10b94385cb3d4b99a9f120ebb02fc09261e7b28f32273a7725caf6d114c'` |
| `2` | `2` | `(0, 7)` | `3` | `(4, 2, 6)` | `-1` | `(1, 1, 1, 3)` | `'6c9ac9b73f8d0c8f2cc3520cda00654825bb2256926987533c7110910617c612'` |
| `2` | `2` | `(5, 3)` | `3` | `(4, 2, 6)` | `-1` | `(1, 1, 1, 3)` | `'8451ad428581b7dbdee45c64db5b14628aa44bf60ed1d4f013d80fad1501a46b'` |
| `2` | `3` | `(-3, 2)` | `2` | `(2, 2, 2)` | `1` | `(2, 1, 1, 1)` | `'fa0c5d32e239af9e641ba72de5edb96c1731fc6ebbd2120d49bd8f7858d9aed3'` |
| `2` | `3` | `(0, 7)` | `2` | `(2, 2, 4)` | `-1` | `(2, 1, 1, 1)` | `'5dfaf2a2211fae88fe8a1bac37afcc933351fa06fbc004b96edfaf8e9cf8da93'` |
| `2` | `3` | `(5, 3)` | `2` | `(2, 2, 5)` | `-1` | `(2, 1, 1, 1)` | `'fdac2271c941c36158f8167501e847f2ba2509450daab97d2b3005eaf4655186'` |
| `8` | `0` | `(-3, 2)` | `1` | `(9, 9, 11)` | `1` | `(1, 1, 1, 7)` | `'388fa820295fc17991c5205e0339f3d7c16353a4bdc645a3b63dfce9472e7fe4'` |
| `8` | `0` | `(0, 7)` | `3` | `(2, 9, 4)` | `1` | `(1, 1, 1, 7)` | `'8b0ab4d329cfba0b2fb86ecf088d6765206daffef961a701acf3c980c0664af8'` |
| `8` | `0` | `(5, 3)` | `3` | `(2, 9, 12)` | `-1` | `(1, 1, 1, 7)` | `'f2fb73e15d5ace84fc85678f6b61816874111bcf272b74316253026a2a54b9b9'` |
| `8` | `1` | `(-3, 2)` | `2` | `(9, 8, 11)` | `1` | `(4, 1, 1, 1)` | `'607c9c44512ba6a8015b2e4c67d22e5ca42d3e639f6a381c417f87c73210469a'` |
| `8` | `1` | `(0, 7)` | `2` | `(9, 8, 11)` | `1` | `(4, 1, 1, 1)` | `'3862bda2bce1def8b53f6aad8a382865ff24efae219c06b6cc9e80f104daa12f'` |
| `8` | `1` | `(5, 3)` | `2` | `(9, 8, 9)` | `-1` | `(4, 1, 1, 1)` | `'2739c4059015bc4160e8a5a07ba72d6a76c81e4e40096b1076d72a6e6524aade'` |
| `8` | `2` | `(-3, 2)` | `3` | `(10, 2, 10)` | `-1` | `(1, 1, 1, 3)` | `'f0250bf8adbb211e078bf2814b01ffe880de92421b772378b677c0500f401b9d'` |
| `8` | `2` | `(0, 7)` | `3` | `(10, 2, 12)` | `-1` | `(1, 1, 1, 3)` | `'1a267d44587bf8deb255f42755a4b641de09e726e674b4b73de1054fdd40d8dd'` |
| `8` | `2` | `(5, 3)` | `3` | `(10, 2, 11)` | `-1` | `(1, 1, 1, 3)` | `'c5a86d78a64f42bb50051ab1e778c8cdb83611c77c762c097fd3f2e99ce51e9f'` |
| `8` | `3` | `(-3, 2)` | `2` | `(2, 2, 2)` | `1` | `(2, 1, 1, 1)` | `'fa0c5d32e239af9e641ba72de5edb96c1731fc6ebbd2120d49bd8f7858d9aed3'` |
| `8` | `3` | `(0, 7)` | `2` | `(2, 2, 4)` | `-1` | `(2, 1, 1, 1)` | `'5dfaf2a2211fae88fe8a1bac37afcc933351fa06fbc004b96edfaf8e9cf8da93'` |
| `8` | `3` | `(5, 3)` | `2` | `(2, 2, 5)` | `-1` | `(2, 1, 1, 1)` | `'fdac2271c941c36158f8167501e847f2ba2509450daab97d2b3005eaf4655186'` |
| `64` | `0` | `(-3, 2)` | `1` | `(65, 65, 67)` | `1` | `(1, 1, 1, 7)` | `'b65f08ef0185b3eb93f2d8b265dd52803207bdea91df4a7d77c22e684e3ec68d'` |
| `64` | `0` | `(0, 7)` | `3` | `(2, 65, 4)` | `1` | `(1, 1, 1, 7)` | `'fb60f9ab996511489dd43b9da75add6568a70f5fb78ed347e65a5c83728feec4'` |
| `64` | `0` | `(5, 3)` | `3` | `(2, 65, 68)` | `-1` | `(1, 1, 1, 7)` | `'1d83e61f38b9c81e536e6c952960ca32f7a2c6dd1788a4a4389cefd0c8571df0'` |
| `64` | `1` | `(-3, 2)` | `2` | `(65, 64, 67)` | `1` | `(4, 1, 1, 1)` | `'1ead4a8f8876ed2a412d18928e03d50b471cc420b662ad12e488241cb0c848de'` |
| `64` | `1` | `(0, 7)` | `2` | `(65, 64, 67)` | `1` | `(4, 1, 1, 1)` | `'c7290de9ddaed612809abf5146ee1c7a2c67e01fe4db01e41a05464ec2343fd3'` |
| `64` | `1` | `(5, 3)` | `2` | `(65, 64, 65)` | `-1` | `(4, 1, 1, 1)` | `'52ad8ec495ce6f1be345934e04f2ee8543999cee627b8f975fe94cb7dd38eef2'` |
| `64` | `2` | `(-3, 2)` | `3` | `(66, 2, 66)` | `-1` | `(1, 1, 1, 3)` | `'f8f93a08f0e6a72e8063367412b605e0e0274a09f2e9920be4bc724eef223b44'` |
| `64` | `2` | `(0, 7)` | `3` | `(66, 2, 68)` | `-1` | `(1, 1, 1, 3)` | `'7c4f03c28a2f4869258b23327cc2fe7b60b2ec68d9085f977555eff86e27692e'` |
| `64` | `2` | `(5, 3)` | `3` | `(66, 2, 67)` | `-1` | `(1, 1, 1, 3)` | `'2b1e98d603a395d2ac3c711137c0b21881cdc5a5d4a75783f30a92724d0de064'` |
| `64` | `3` | `(-3, 2)` | `2` | `(2, 2, 2)` | `1` | `(2, 1, 1, 1)` | `'fa0c5d32e239af9e641ba72de5edb96c1731fc6ebbd2120d49bd8f7858d9aed3'` |
| `64` | `3` | `(0, 7)` | `2` | `(2, 2, 4)` | `-1` | `(2, 1, 1, 1)` | `'5dfaf2a2211fae88fe8a1bac37afcc933351fa06fbc004b96edfaf8e9cf8da93'` |
| `64` | `3` | `(5, 3)` | `2` | `(2, 2, 5)` | `-1` | `(2, 1, 1, 1)` | `'fdac2271c941c36158f8167501e847f2ba2509450daab97d2b3005eaf4655186'` |
| `4096` | `0` | `(-3, 2)` | `1` | `(4097, 4097, 4099)` | `1` | `(1, 1, 1, 7)` | `'ccba09c0bb5c17c76de45bf24f3e47d52ca598fc213477ff4044775cdf5860ce'` |
| `4096` | `0` | `(0, 7)` | `3` | `(2, 4097, 4)` | `1` | `(1, 1, 1, 7)` | `'9be2c4cbde9fd58578e77cc4282d808ed6864e3dd1291761dd0990343baa66f8'` |
| `4096` | `0` | `(5, 3)` | `3` | `(2, 4097, 4100)` | `-1` | `(1, 1, 1, 7)` | `'811b03524ee4edc1160978fb18c7cd3fa8c76ca80dbaa7f9a1b819216d047b07'` |
| `4096` | `1` | `(-3, 2)` | `2` | `(4097, 4096, 4099)` | `1` | `(4, 1, 1, 1)` | `'908bf67d74db375a58fc89a8bf7f8fe93dd3b27c49d1d64e49a8beb6b3547128'` |
| `4096` | `1` | `(0, 7)` | `2` | `(4097, 4096, 4099)` | `1` | `(4, 1, 1, 1)` | `'a2b4a2f36000be059b7c4694cb8aadb3b21cfb9b05dcd3178313ceb9196c155f'` |
| `4096` | `1` | `(5, 3)` | `2` | `(4097, 4096, 4097)` | `-1` | `(4, 1, 1, 1)` | `'d7c80f869152ca7b4544fcea7c563881317e9414e4e9d8177fa7192421d815ca'` |
| `4096` | `2` | `(-3, 2)` | `3` | `(4098, 2, 4098)` | `-1` | `(1, 1, 1, 3)` | `'1608fb42bf643413d79f450a6adcf4c75ef421ef88059c357020338a84ba7293'` |
| `4096` | `2` | `(0, 7)` | `3` | `(4098, 2, 4100)` | `-1` | `(1, 1, 1, 3)` | `'a38dbe4bf7a1f6a7a7e59194c50016e4d0b5ceb41c17659448fd68560f05ed3c'` |
| `4096` | `2` | `(5, 3)` | `3` | `(4098, 2, 4099)` | `-1` | `(1, 1, 1, 3)` | `'d4f20ebda329fce5a93f98b76fbc34278def6507949c8655c31b0cfdcee03cf0'` |
| `4096` | `3` | `(-3, 2)` | `2` | `(2, 2, 2)` | `1` | `(2, 1, 1, 1)` | `'fa0c5d32e239af9e641ba72de5edb96c1731fc6ebbd2120d49bd8f7858d9aed3'` |
| `4096` | `3` | `(0, 7)` | `2` | `(2, 2, 4)` | `-1` | `(2, 1, 1, 1)` | `'5dfaf2a2211fae88fe8a1bac37afcc933351fa06fbc004b96edfaf8e9cf8da93'` |
| `4096` | `3` | `(5, 3)` | `2` | `(2, 2, 5)` | `-1` | `(2, 1, 1, 1)` | `'fdac2271c941c36158f8167501e847f2ba2509450daab97d2b3005eaf4655186'` |

### Fixture table: SCALE_COUNTS

| raw_parameter_scale_checks | exponents |
| --- | --- |
| `20` | `(1, 2, 8, 64, 4096)` |



## ORACLE-081 — Preparation/query separation and numerical carriers

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

BO2, BO6, BO8, BO20. The ten-cycle has r=(1,200,120,20), so context preparation
materializes 341 descriptors once. A D0 query examines exactly one descriptor and
performs 111 prescribed ordinary cuts; it must not invoke the all-branch enumerator
or scan D2's 120 descriptors again. This is a fixed functional/call-trace assertion,
not a wall-clock performance benchmark.

The separately charged preparation is O(n+m+R_all). The per-query carrier remains
O(1+r_j*(n+3)^3*(m+n)^2), including r_j=0 and closed zero-arc vertex work. Families
are processed sequentially with one original network and at most one reduced problem.
The input's active condition gives 0<=s<=d<=2Q and 0<=b<=Q. Check the ruled bounds
abs(c)<=3Q+2, abs(h)<=2Q+1, abs(raw)<=B*(3Q+2)+abs(A)*(2Q+1),
abs(gamma[v])<=(2*abs(A)+B)*Q and abs(constant)<=abs(A)+2B.
Contractions sum subsets of the original total capacity S=2BQ+2*sum(abs(gamma)),
and introduce no infinity, capacity products, or numeric iteration bound.
Finite checks of these inequalities do not replace their source-bound derivation.

### Fixture table: PREPARATION_SEPARATION

| n | edges | f | r0_r1_r2_r3 | R_all | D0_parameter | D0_result | D0_counts |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `10` | `((0, 1, 1), (0, 9, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1), (6, 7, 1), (7, 8, 1), (8, 9, 1))` | `(1, 1, 1, 1, 1, 1, 1, 1, 1, 1)` | `(1, 200, 120, 20)` | `341` | `(0, 1)` | `(1, 2, 2, 2)` | `(1, 1, 1, 111)` |



## ORACLE-082 — Coverage and oracle-only completion boundary

**Classification:** `FIXED_PARAMETER_BRANCH_ORACLE` / local contract fixture.

The private JSON is a transcription, not a runtime input. All literal tables above
are committed expected-data authority; future consuming tests must be self-contained.
The companion standalone audit imports no production, verifier, consuming test, or
external graph library. It rechecks the complete historical catalogue prefix, exact
human-table/JSON agreement, source-domain minima, graph-cut identities, deterministic
family selection, declared work counts, diagnostic replay, and raw scaling.

| Prospective test obligations | Registered expected evidence |
| --- | --- |
| BO1--BO3 public shapes, context provenance, validation order | ORACLE-069--070, ORACLE-077--078 |
| BO4--BO7 complete domains, minima, cover, and emptiness | ORACLE-070--072, ORACLE-075, ORACLE-079 |
| BO8--BO12 network lifetime, constrained cuts, coordinates and shifts | ORACLE-073--076, ORACLE-078 |
| BO13--BO15 first retention, no early exit, raw scale | ORACLE-072, ORACLE-075, ORACLE-078--080 |
| BO16 diagnostics | ORACLE-070, ORACLE-076, ORACLE-079 |
| BO17--BO18 internal failures, nonmutation, isolation/reuse | ORACLE-078 plus future source/import probes |
| BO19--BO20 exactness and structural/number-size review | ORACLE-080--081 plus future AST/call-chain review |
| BO21 independent audit and faulty-implementation controls | All entries plus later frozen-test/production audit |
| BO22 narrow conformance and downstream scope | This entry |

Rejection and internal-failure rows are pre-code declarations, not executed constructor
or seam tests. No Unit 12 source or consuming test is created here. The independent
graph corpus and source corpus are finite checks, not an optimality certificate for a
future returned density witness and not a universal correctness proof.

Only after the oracle-only commit is audited and closed does tests-first RED begin.
After frozen tests, implementation GREEN, and independent source-to-code verification,
a narrowly scoped thm:branch-oracle CONFORMANCE row may be proposed. No existing row
or status is promoted here. Outer branch/global loops, ratio transformations, witness
reconstruction, certificates, and peak-bit experiments remain outside this oracle stage.

**Unit 12 oracle status:** source- and authority-derived expected data independently
checked before `tests/test_oracle.py` or `exactfrac/oracle.py` exists.


## Unit 13 Standard branch oracle fixtures — source and scope

Authority commit: `2446aa59356f25ff446a9db85d992a424637348a`.
Authority tree: `9513e0f34c9eafeb7361756920fd0d8367689351`.
Governing V2.2 source SHA-256:
`4cceb9984bc6d24b78f0eeff1f9014650fc490de2210e748f0fcae85d1ffcaa6`.
Governing canonical archive SHA-256:
`400c4e23a7683571f7181b98bc009954d431f4ac355a247fb22327a609b4f9ce`.
Received Phase C transfer SHA-256:
`d9d6554a273c3a1304f593316912249a94ecde60be902d20c75bbb06ff334501`.

These prospective fixtures precede `tests/test_branch.py` and `exactfrac/branch.py`.
They extend ORACLE-001--082 without changing any previous byte, fixture, classification,
source ruling, or test. Mathematical source: `prop:branch-transform`, `eq:fj`, `eq:rhoj`,
`alg:standard-branch`, `prop:standard-correct`, `lem:standard-bits`, and the source-bound
`thm:WYZ` / `cor:standard-strong` invocation. Engineering authority is DESIGN 4.10 and
TEST_PLAN ST1--ST20. No Standard implementation or CONFORMANCE promotion exists yet.

`BRANCH_ORACLE` below means the transformed minimum rho_j=min c_j/h_j over its stated
original source domain, not the original endpoint density, a global density optimum,
a compact witness, or a certificate. A returned `BranchResult.root` is a literal RawPair;
its numerical value is compared by cross multiplication. None is source-branch infeasibility.
Neither None, a zero branch root, nor an accepted standalone record settles global Empty.

Human tables below are the committed expected-data authority. Private JSON is a convenience
copy, never a consuming-test dependency. Private executable enumerations provide checkable
finite derivations; they are deliberately exponential tiny references, not production solvers.
No expected optimum, parameter, residual, or shore is generated by production output.

### Independent expected-value routes

Route A first enumerates every nonempty original shore U and computes s=f(U),
e=e_q(U), b=b_q(U), d=2e+b directly from input records. It applies the four literal domains:
D0: s+b odd; D1: s+b even, b>=1, d-s>0; D2: s odd and s>=3; D3: s even and b>=1.
The pairs are respectively (s+b-1,d+1-s), (s+b-2,d-s), (b-d,s-1), (b-d-2,s).
It finds min c/h and every attaining shore without consulting any family or cut optimizer.
Empty U is excluded from this ratio comparison. Empty U remains available to the polynomial
extension of the residual when ordinary-cut comparisons require the whole geometric lattice.

The shipped-selection reference is separate: enumerate the complete source-ordered family
cover; within each feasible family's forced-membership cube, enumerate each compatible
GR pair in increasing reduced (a,b) order. Reduced source and sink are 0 and 1; each free
original vertex is a subsequent singleton class in increasing original order. The optional
anchor belongs to source and creates no extra reduced class. Minimize the extended raw
residual over the pair restriction. Intersect ALL ordinary minimizing shores to obtain the
inclusionwise-least ordinary minimizer, verify it is minimizing, and apply family parity.
Keep the first strictly improving odd candidate, then the first strictly improving family.
An intersection of minimizers is not a minimum-mask, maximum-h, or cardinality tie rule.

Route B independently computes original-domain optima using vertex subsets and Fraction.
For shipped selection it builds the source's nonnegative directed network, transports
capacities by canonical contraction, transports terminal tokens by XOR and sink toggle,
and enumerates cut capacities in the reduced universe. It intersects all least ordinary
cut ties and filters parity only in that universe. Neither route imports ExactFrac,
its verifier, a consuming test, the other route, or a future branch implementation.

For one query, structural counts are (r_j,k_j,k_j,o_j): descriptors examined, feasible
descriptors, parity calls, and specified ordinary calls. With N_F=2+n-|I|-|O| for a
feasible descriptor, o_j=sum_F(N_F*N_F-3*N_F+3). These are EXPECTED reference-policy
call counts, not observed production execution. Context preparation is not counted again.
Actual flow augmentations, scans, and flow-only peaks are not inferred from these four fields.

## ORACLE-083 — Canonical Standard inputs and complete original-shore data

**Classification:** `BRANCH_ORACLE`; input/shape facts are `LOCAL_CONTRACT_FIXTURE`.
**Coverage:** ST4--ST10, ST14--ST18.

The first nine inputs reuse ORACLE-069 exactly. ZERO reuses the active q=3, f=(3,3)
zero-witness instance but makes a NEW transformed-branch claim derived below; it does
not promote the earlier local witness to a global optimum. SHIFT has q=4, f=(4,4).
LOW0 and LOW1 were selected by a private seeded search (seed 1302446, trials 14 and 5),
then all source-domain values were rederived exactly. HIGH2, HIGH3, NONMAX and CHOICE
are explicit tiny inputs; their role is fully determined by the tables, not a random search.
Every label is None unless a later label-only control expressly changes it.

The SHORE table covers every nonempty original shore of every named input. domain_pairs
has four positions: the literal (c_j,h_j) when U belongs to D_j, otherwise None.
None there means the ratio is outside that domain; it does not deny the residual's
polynomial extension on all subsets. The four membership flags and every pair are
computed from s,e,b,d, not inferred from a produced cover.

### Fixture table: U13_INPUTS

| name | n | edges | f | d_q | Q |
| --- | --- | --- | --- | --- | --- |
| `'Q1'` | `2` | `((0, 1, 1),)` | `(1, 1)` | `(1, 1)` | `1` |
| `'DOUBLE'` | `2` | `((0, 1, 2),)` | `(1, 1)` | `(2, 2)` | `2` |
| `'UNEQUAL'` | `2` | `((0, 1, 2),)` | `(2, 1)` | `(2, 2)` | `2` |
| `'EQUALITY'` | `3` | `((0, 1, 1), (0, 2, 1), (1, 2, 1))` | `(2, 2, 2)` | `(2, 2, 2)` | `3` |
| `'WTRI'` | `3` | `((0, 1, 1), (0, 2, 1), (1, 2, 1))` | `(1, 1, 1)` | `(2, 2, 2)` | `3` |
| `'ODDFULL'` | `3` | `((0, 1, 1), (0, 2, 1), (1, 2, 1))` | `(2, 2, 1)` | `(2, 2, 2)` | `3` |
| `'TIECARD'` | `3` | `((0, 2, 1), (1, 2, 1))` | `(1, 1, 2)` | `(1, 1, 2)` | `2` |
| `'RICH'` | `5` | `((0, 2, 2), (1, 2, 2), (2, 4, 1), (3, 4, 1))` | `(1, 1, 1, 1, 2)` | `(2, 2, 5, 1, 2)` | `6` |
| `'MIXED'` | `4` | `((0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 4), (1, 3, 2), (2, 3, 5))` | `(2, 3, 4, 5)` | `(6, 8, 12, 8)` | `17` |
| `'ZERO'` | `2` | `((0, 1, 3),)` | `(3, 3)` | `(3, 3)` | `3` |
| `'SHIFT'` | `2` | `((0, 1, 4),)` | `(4, 4)` | `(4, 4)` | `4` |
| `'LOW0'` | `4` | `((0, 1, 9), (0, 2, 1), (1, 3, 1), (2, 3, 8))` | `(3, 3, 7, 5)` | `(10, 10, 9, 9)` | `19` |
| `'LOW1'` | `5` | `((0, 2, 9), (0, 4, 6), (1, 3, 3), (2, 4, 1), (3, 4, 1))` | `(11, 1, 1, 3, 4)` | `(15, 3, 10, 4, 8)` | `20` |
| `'HIGH2'` | `3` | `((0, 1, 1), (0, 2, 1), (1, 2, 2))` | `(2, 1, 3)` | `(2, 3, 3)` | `4` |
| `'HIGH3'` | `3` | `((0, 1, 1), (0, 2, 1), (1, 2, 2))` | `(1, 1, 3)` | `(2, 3, 3)` | `4` |
| `'NONMAX'` | `3` | `((0, 2, 1), (1, 2, 2))` | `(1, 1, 1)` | `(1, 2, 3)` | `3` |
| `'CHOICE'` | `3` | `((0, 2, 2), (1, 2, 2))` | `(1, 1, 4)` | `(2, 2, 4)` | `4` |


### Fixture table: U13_SHORES

| input | U | s | e | b | d | in_D0_D1_D2_D3 | domain_pairs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `'Q1'` | `1` | `1` | `0` | `1` | `1` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'Q1'` | `2` | `1` | `0` | `1` | `1` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'Q1'` | `3` | `2` | `1` | `0` | `2` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'DOUBLE'` | `1` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'DOUBLE'` | `2` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'DOUBLE'` | `3` | `2` | `2` | `0` | `4` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'UNEQUAL'` | `1` | `2` | `0` | `2` | `2` | `(False, False, False, True)` | `(None, None, None, (-2, 2))` |
| `'UNEQUAL'` | `2` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'UNEQUAL'` | `3` | `3` | `2` | `0` | `4` | `(True, False, True, False)` | `((2, 2), None, (-4, 2), None)` |
| `'EQUALITY'` | `1` | `2` | `0` | `2` | `2` | `(False, False, False, True)` | `(None, None, None, (-2, 2))` |
| `'EQUALITY'` | `2` | `2` | `0` | `2` | `2` | `(False, False, False, True)` | `(None, None, None, (-2, 2))` |
| `'EQUALITY'` | `3` | `4` | `1` | `2` | `4` | `(False, False, False, True)` | `(None, None, None, (-4, 4))` |
| `'EQUALITY'` | `4` | `2` | `0` | `2` | `2` | `(False, False, False, True)` | `(None, None, None, (-2, 2))` |
| `'EQUALITY'` | `5` | `4` | `1` | `2` | `4` | `(False, False, False, True)` | `(None, None, None, (-4, 4))` |
| `'EQUALITY'` | `6` | `4` | `1` | `2` | `4` | `(False, False, False, True)` | `(None, None, None, (-4, 4))` |
| `'EQUALITY'` | `7` | `6` | `3` | `0` | `6` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'WTRI'` | `1` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'WTRI'` | `2` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'WTRI'` | `3` | `2` | `1` | `2` | `4` | `(False, True, False, True)` | `(None, (2, 2), None, (-4, 2))` |
| `'WTRI'` | `4` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'WTRI'` | `5` | `2` | `1` | `2` | `4` | `(False, True, False, True)` | `(None, (2, 2), None, (-4, 2))` |
| `'WTRI'` | `6` | `2` | `1` | `2` | `4` | `(False, True, False, True)` | `(None, (2, 2), None, (-4, 2))` |
| `'WTRI'` | `7` | `3` | `3` | `0` | `6` | `(True, False, True, False)` | `((2, 4), None, (-6, 2), None)` |
| `'ODDFULL'` | `1` | `2` | `0` | `2` | `2` | `(False, False, False, True)` | `(None, None, None, (-2, 2))` |
| `'ODDFULL'` | `2` | `2` | `0` | `2` | `2` | `(False, False, False, True)` | `(None, None, None, (-2, 2))` |
| `'ODDFULL'` | `3` | `4` | `1` | `2` | `4` | `(False, False, False, True)` | `(None, None, None, (-4, 4))` |
| `'ODDFULL'` | `4` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'ODDFULL'` | `5` | `3` | `1` | `2` | `4` | `(True, False, True, False)` | `((4, 2), None, (-2, 2), None)` |
| `'ODDFULL'` | `6` | `3` | `1` | `2` | `4` | `(True, False, True, False)` | `((4, 2), None, (-2, 2), None)` |
| `'ODDFULL'` | `7` | `5` | `3` | `0` | `6` | `(True, False, True, False)` | `((4, 2), None, (-6, 4), None)` |
| `'TIECARD'` | `1` | `1` | `0` | `1` | `1` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'TIECARD'` | `2` | `1` | `0` | `1` | `1` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'TIECARD'` | `3` | `2` | `0` | `2` | `2` | `(False, False, False, True)` | `(None, None, None, (-2, 2))` |
| `'TIECARD'` | `4` | `2` | `0` | `2` | `2` | `(False, False, False, True)` | `(None, None, None, (-2, 2))` |
| `'TIECARD'` | `5` | `3` | `1` | `1` | `3` | `(False, False, True, False)` | `(None, None, (-2, 2), None)` |
| `'TIECARD'` | `6` | `3` | `1` | `1` | `3` | `(False, False, True, False)` | `(None, None, (-2, 2), None)` |
| `'TIECARD'` | `7` | `4` | `2` | `0` | `4` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'RICH'` | `1` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'RICH'` | `2` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'RICH'` | `3` | `2` | `0` | `4` | `4` | `(False, True, False, True)` | `(None, (4, 2), None, (-2, 2))` |
| `'RICH'` | `4` | `1` | `0` | `5` | `5` | `(False, True, False, False)` | `(None, (4, 4), None, None)` |
| `'RICH'` | `5` | `2` | `2` | `3` | `7` | `(True, False, False, True)` | `((4, 6), None, None, (-6, 2))` |
| `'RICH'` | `6` | `2` | `2` | `3` | `7` | `(True, False, False, True)` | `((4, 6), None, None, (-6, 2))` |
| `'RICH'` | `7` | `3` | `4` | `1` | `9` | `(False, True, True, False)` | `(None, (2, 6), (-8, 2), None)` |
| `'RICH'` | `8` | `1` | `0` | `1` | `1` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'RICH'` | `9` | `2` | `0` | `3` | `3` | `(True, False, False, True)` | `((4, 2), None, None, (-2, 2))` |
| `'RICH'` | `10` | `2` | `0` | `3` | `3` | `(True, False, False, True)` | `((4, 2), None, None, (-2, 2))` |
| `'RICH'` | `11` | `3` | `0` | `5` | `5` | `(False, True, True, False)` | `(None, (6, 2), (0, 2), None)` |
| `'RICH'` | `12` | `2` | `0` | `6` | `6` | `(False, True, False, True)` | `(None, (6, 4), None, (-2, 2))` |
| `'RICH'` | `13` | `3` | `2` | `4` | `8` | `(True, False, True, False)` | `((6, 6), None, (-4, 2), None)` |
| `'RICH'` | `14` | `3` | `2` | `4` | `8` | `(True, False, True, False)` | `((6, 6), None, (-4, 2), None)` |
| `'RICH'` | `15` | `4` | `4` | `2` | `10` | `(False, True, False, True)` | `(None, (4, 6), None, (-10, 4))` |
| `'RICH'` | `16` | `2` | `0` | `2` | `2` | `(False, False, False, True)` | `(None, None, None, (-2, 2))` |
| `'RICH'` | `17` | `3` | `0` | `4` | `4` | `(True, False, True, False)` | `((6, 2), None, (0, 2), None)` |
| `'RICH'` | `18` | `3` | `0` | `4` | `4` | `(True, False, True, False)` | `((6, 2), None, (0, 2), None)` |
| `'RICH'` | `19` | `4` | `0` | `6` | `6` | `(False, True, False, True)` | `(None, (8, 2), None, (-2, 4))` |
| `'RICH'` | `20` | `3` | `1` | `5` | `7` | `(False, True, True, False)` | `(None, (6, 4), (-2, 2), None)` |
| `'RICH'` | `21` | `4` | `3` | `3` | `9` | `(True, False, False, True)` | `((6, 6), None, None, (-8, 4))` |
| `'RICH'` | `22` | `4` | `3` | `3` | `9` | `(True, False, False, True)` | `((6, 6), None, None, (-8, 4))` |
| `'RICH'` | `23` | `5` | `5` | `1` | `11` | `(False, True, True, False)` | `(None, (4, 6), (-10, 4), None)` |
| `'RICH'` | `24` | `3` | `1` | `1` | `3` | `(False, False, True, False)` | `(None, None, (-2, 2), None)` |
| `'RICH'` | `25` | `4` | `1` | `3` | `5` | `(True, False, False, True)` | `((6, 2), None, None, (-4, 4))` |
| `'RICH'` | `26` | `4` | `1` | `3` | `5` | `(True, False, False, True)` | `((6, 2), None, None, (-4, 4))` |
| `'RICH'` | `27` | `5` | `1` | `5` | `7` | `(False, True, True, False)` | `(None, (8, 2), (-2, 4), None)` |
| `'RICH'` | `28` | `4` | `2` | `4` | `8` | `(False, True, False, True)` | `(None, (6, 4), None, (-6, 4))` |
| `'RICH'` | `29` | `5` | `4` | `2` | `10` | `(True, False, True, False)` | `((6, 6), None, (-8, 4), None)` |
| `'RICH'` | `30` | `5` | `4` | `2` | `10` | `(True, False, True, False)` | `((6, 6), None, (-8, 4), None)` |
| `'RICH'` | `31` | `6` | `6` | `0` | `12` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'MIXED'` | `1` | `2` | `0` | `6` | `6` | `(False, True, False, True)` | `(None, (6, 4), None, (-2, 2))` |
| `'MIXED'` | `2` | `3` | `0` | `8` | `8` | `(True, False, True, False)` | `((10, 6), None, (0, 2), None)` |
| `'MIXED'` | `3` | `5` | `2` | `10` | `14` | `(True, False, True, False)` | `((14, 10), None, (-4, 4), None)` |
| `'MIXED'` | `4` | `4` | `0` | `12` | `12` | `(False, True, False, True)` | `(None, (14, 8), None, (-2, 4))` |
| `'MIXED'` | `5` | `6` | `3` | `12` | `18` | `(False, True, False, True)` | `(None, (16, 12), None, (-8, 6))` |
| `'MIXED'` | `6` | `7` | `4` | `12` | `20` | `(True, False, True, False)` | `((18, 14), None, (-8, 6), None)` |
| `'MIXED'` | `7` | `9` | `9` | `8` | `26` | `(True, False, True, False)` | `((16, 18), None, (-18, 8), None)` |
| `'MIXED'` | `8` | `5` | `0` | `8` | `8` | `(True, False, True, False)` | `((12, 4), None, (0, 4), None)` |
| `'MIXED'` | `9` | `7` | `1` | `12` | `14` | `(True, False, True, False)` | `((18, 8), None, (-2, 6), None)` |
| `'MIXED'` | `10` | `8` | `2` | `12` | `16` | `(False, True, False, True)` | `(None, (18, 8), None, (-6, 8))` |
| `'MIXED'` | `11` | `10` | `5` | `12` | `22` | `(False, True, False, True)` | `(None, (20, 12), None, (-12, 10))` |
| `'MIXED'` | `12` | `9` | `5` | `10` | `20` | `(True, False, True, False)` | `((18, 12), None, (-10, 8), None)` |
| `'MIXED'` | `13` | `11` | `9` | `8` | `26` | `(True, False, True, False)` | `((18, 16), None, (-18, 10), None)` |
| `'MIXED'` | `14` | `12` | `11` | `6` | `28` | `(False, True, False, True)` | `(None, (16, 16), None, (-24, 12))` |
| `'MIXED'` | `15` | `14` | `17` | `0` | `34` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'ZERO'` | `1` | `3` | `0` | `3` | `3` | `(False, False, True, False)` | `(None, None, (0, 2), None)` |
| `'ZERO'` | `2` | `3` | `0` | `3` | `3` | `(False, False, True, False)` | `(None, None, (0, 2), None)` |
| `'ZERO'` | `3` | `6` | `3` | `0` | `6` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'SHIFT'` | `1` | `4` | `0` | `4` | `4` | `(False, False, False, True)` | `(None, None, None, (-2, 4))` |
| `'SHIFT'` | `2` | `4` | `0` | `4` | `4` | `(False, False, False, True)` | `(None, None, None, (-2, 4))` |
| `'SHIFT'` | `3` | `8` | `4` | `0` | `8` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'LOW0'` | `1` | `3` | `0` | `10` | `10` | `(True, False, True, False)` | `((12, 8), None, (0, 2), None)` |
| `'LOW0'` | `2` | `3` | `0` | `10` | `10` | `(True, False, True, False)` | `((12, 8), None, (0, 2), None)` |
| `'LOW0'` | `3` | `6` | `9` | `2` | `20` | `(False, True, False, True)` | `(None, (6, 14), None, (-20, 6))` |
| `'LOW0'` | `4` | `7` | `0` | `9` | `9` | `(False, True, True, False)` | `(None, (14, 2), (0, 6), None)` |
| `'LOW0'` | `5` | `10` | `1` | `17` | `19` | `(True, False, False, True)` | `((26, 10), None, None, (-4, 10))` |
| `'LOW0'` | `6` | `10` | `0` | `19` | `19` | `(True, False, False, True)` | `((28, 10), None, None, (-2, 10))` |
| `'LOW0'` | `7` | `13` | `10` | `9` | `29` | `(False, True, True, False)` | `(None, (20, 16), (-20, 12), None)` |
| `'LOW0'` | `8` | `5` | `0` | `9` | `9` | `(False, True, True, False)` | `(None, (12, 4), (0, 4), None)` |
| `'LOW0'` | `9` | `8` | `0` | `19` | `19` | `(True, False, False, True)` | `((26, 12), None, None, (-2, 8))` |
| `'LOW0'` | `10` | `8` | `1` | `17` | `19` | `(True, False, False, True)` | `((24, 12), None, None, (-4, 8))` |
| `'LOW0'` | `11` | `11` | `10` | `9` | `29` | `(False, True, True, False)` | `(None, (18, 18), (-20, 10), None)` |
| `'LOW0'` | `12` | `12` | `8` | `2` | `18` | `(False, True, False, True)` | `(None, (12, 6), None, (-18, 12))` |
| `'LOW0'` | `13` | `15` | `9` | `10` | `28` | `(True, False, True, False)` | `((24, 14), None, (-18, 14), None)` |
| `'LOW0'` | `14` | `15` | `9` | `10` | `28` | `(True, False, True, False)` | `((24, 14), None, (-18, 14), None)` |
| `'LOW0'` | `15` | `18` | `19` | `0` | `38` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'LOW1'` | `1` | `11` | `0` | `15` | `15` | `(False, True, True, False)` | `(None, (24, 4), (0, 10), None)` |
| `'LOW1'` | `2` | `1` | `0` | `3` | `3` | `(False, True, False, False)` | `(None, (2, 2), None, None)` |
| `'LOW1'` | `3` | `12` | `0` | `18` | `18` | `(False, True, False, True)` | `(None, (28, 6), None, (-2, 12))` |
| `'LOW1'` | `4` | `1` | `0` | `10` | `10` | `(True, False, False, False)` | `((10, 10), None, None, None)` |
| `'LOW1'` | `5` | `12` | `9` | `7` | `25` | `(True, False, False, True)` | `((18, 14), None, None, (-20, 12))` |
| `'LOW1'` | `6` | `2` | `0` | `13` | `13` | `(True, False, False, True)` | `((14, 12), None, None, (-2, 2))` |
| `'LOW1'` | `7` | `13` | `9` | `10` | `28` | `(True, False, True, False)` | `((22, 16), None, (-18, 12), None)` |
| `'LOW1'` | `8` | `3` | `0` | `4` | `4` | `(True, False, True, False)` | `((6, 2), None, (0, 2), None)` |
| `'LOW1'` | `9` | `14` | `0` | `19` | `19` | `(True, False, False, True)` | `((32, 6), None, None, (-2, 14))` |
| `'LOW1'` | `10` | `4` | `3` | `1` | `7` | `(True, False, False, True)` | `((4, 4), None, None, (-8, 4))` |
| `'LOW1'` | `11` | `15` | `3` | `16` | `22` | `(True, False, True, False)` | `((30, 8), None, (-6, 14), None)` |
| `'LOW1'` | `12` | `4` | `0` | `14` | `14` | `(False, True, False, True)` | `(None, (16, 10), None, (-2, 4))` |
| `'LOW1'` | `13` | `15` | `9` | `11` | `29` | `(False, True, True, False)` | `(None, (24, 14), (-18, 14), None)` |
| `'LOW1'` | `14` | `5` | `3` | `11` | `17` | `(False, True, True, False)` | `(None, (14, 12), (-6, 4), None)` |
| `'LOW1'` | `15` | `16` | `12` | `8` | `32` | `(False, True, False, True)` | `(None, (22, 16), None, (-26, 16))` |
| `'LOW1'` | `16` | `4` | `0` | `8` | `8` | `(False, True, False, True)` | `(None, (10, 4), None, (-2, 4))` |
| `'LOW1'` | `17` | `15` | `6` | `11` | `23` | `(False, True, True, False)` | `(None, (24, 8), (-12, 14), None)` |
| `'LOW1'` | `18` | `5` | `0` | `11` | `11` | `(False, True, True, False)` | `(None, (14, 6), (0, 4), None)` |
| `'LOW1'` | `19` | `16` | `6` | `14` | `26` | `(False, True, False, True)` | `(None, (28, 10), None, (-14, 16))` |
| `'LOW1'` | `20` | `5` | `1` | `16` | `18` | `(True, False, True, False)` | `((20, 14), None, (-2, 4), None)` |
| `'LOW1'` | `21` | `16` | `16` | `1` | `33` | `(True, False, False, True)` | `((16, 18), None, None, (-34, 16))` |
| `'LOW1'` | `22` | `6` | `1` | `19` | `21` | `(True, False, False, True)` | `((24, 16), None, None, (-4, 6))` |
| `'LOW1'` | `23` | `17` | `16` | `4` | `36` | `(True, False, True, False)` | `((20, 20), None, (-32, 16), None)` |
| `'LOW1'` | `24` | `7` | `1` | `10` | `12` | `(True, False, True, False)` | `((16, 6), None, (-2, 6), None)` |
| `'LOW1'` | `25` | `18` | `7` | `13` | `27` | `(True, False, False, True)` | `((30, 10), None, None, (-16, 18))` |
| `'LOW1'` | `26` | `8` | `4` | `7` | `15` | `(True, False, False, True)` | `((14, 8), None, None, (-10, 8))` |
| `'LOW1'` | `27` | `19` | `10` | `10` | `30` | `(True, False, True, False)` | `((28, 12), None, (-20, 18), None)` |
| `'LOW1'` | `28` | `8` | `2` | `18` | `22` | `(False, True, False, True)` | `(None, (24, 14), None, (-6, 8))` |
| `'LOW1'` | `29` | `19` | `17` | `3` | `37` | `(False, True, True, False)` | `(None, (20, 18), (-34, 18), None)` |
| `'LOW1'` | `30` | `9` | `5` | `15` | `25` | `(False, True, True, False)` | `(None, (22, 16), (-10, 8), None)` |
| `'LOW1'` | `31` | `20` | `20` | `0` | `40` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'HIGH2'` | `1` | `2` | `0` | `2` | `2` | `(False, False, False, True)` | `(None, None, None, (-2, 2))` |
| `'HIGH2'` | `2` | `1` | `0` | `3` | `3` | `(False, True, False, False)` | `(None, (2, 2), None, None)` |
| `'HIGH2'` | `3` | `3` | `1` | `3` | `5` | `(False, True, True, False)` | `(None, (4, 2), (-2, 2), None)` |
| `'HIGH2'` | `4` | `3` | `0` | `3` | `3` | `(False, False, True, False)` | `(None, None, (0, 2), None)` |
| `'HIGH2'` | `5` | `5` | `1` | `3` | `5` | `(False, False, True, False)` | `(None, None, (-2, 4), None)` |
| `'HIGH2'` | `6` | `4` | `2` | `2` | `6` | `(False, True, False, True)` | `(None, (4, 2), None, (-6, 4))` |
| `'HIGH2'` | `7` | `6` | `4` | `0` | `8` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'HIGH3'` | `1` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'HIGH3'` | `2` | `1` | `0` | `3` | `3` | `(False, True, False, False)` | `(None, (2, 2), None, None)` |
| `'HIGH3'` | `3` | `2` | `1` | `3` | `5` | `(True, False, False, True)` | `((4, 4), None, None, (-4, 2))` |
| `'HIGH3'` | `4` | `3` | `0` | `3` | `3` | `(False, False, True, False)` | `(None, None, (0, 2), None)` |
| `'HIGH3'` | `5` | `4` | `1` | `3` | `5` | `(True, False, False, True)` | `((6, 2), None, None, (-4, 4))` |
| `'HIGH3'` | `6` | `4` | `2` | `2` | `6` | `(False, True, False, True)` | `(None, (4, 2), None, (-6, 4))` |
| `'HIGH3'` | `7` | `5` | `4` | `0` | `8` | `(True, False, True, False)` | `((4, 4), None, (-8, 4), None)` |
| `'NONMAX'` | `1` | `1` | `0` | `1` | `1` | `(False, False, False, False)` | `(None, None, None, None)` |
| `'NONMAX'` | `2` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'NONMAX'` | `3` | `2` | `0` | `3` | `3` | `(True, False, False, True)` | `((4, 2), None, None, (-2, 2))` |
| `'NONMAX'` | `4` | `1` | `0` | `3` | `3` | `(False, True, False, False)` | `(None, (2, 2), None, None)` |
| `'NONMAX'` | `5` | `2` | `1` | `2` | `4` | `(False, True, False, True)` | `(None, (2, 2), None, (-4, 2))` |
| `'NONMAX'` | `6` | `2` | `2` | `1` | `5` | `(True, False, False, True)` | `((2, 4), None, None, (-6, 2))` |
| `'NONMAX'` | `7` | `3` | `3` | `0` | `6` | `(True, False, True, False)` | `((2, 4), None, (-6, 2), None)` |
| `'CHOICE'` | `1` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'CHOICE'` | `2` | `1` | `0` | `2` | `2` | `(True, False, False, False)` | `((2, 2), None, None, None)` |
| `'CHOICE'` | `3` | `2` | `0` | `4` | `4` | `(False, True, False, True)` | `(None, (4, 2), None, (-2, 2))` |
| `'CHOICE'` | `4` | `4` | `0` | `4` | `4` | `(False, False, False, True)` | `(None, None, None, (-2, 4))` |
| `'CHOICE'` | `5` | `5` | `2` | `2` | `6` | `(True, False, True, False)` | `((6, 2), None, (-4, 4), None)` |
| `'CHOICE'` | `6` | `5` | `2` | `2` | `6` | `(True, False, True, False)` | `((6, 2), None, (-4, 4), None)` |
| `'CHOICE'` | `7` | `6` | `4` | `0` | `8` | `(False, False, False, False)` | `(None, None, None, None)` |


## ORACLE-084 — Exact transformed branch optima and complete attaining sets

**Classification:** `BRANCH_ORACLE`; infeasible rows are `NEGATIVE` mathematical domains,
not malformed input. **Coverage:** ST4, ST6, ST10.

comparison_pair is the literal source pair at the first NUMERIC-MASK enumerated ratio
minimizer and is used only to compare the numerical optimum. It is NOT the expected
raw return representation and does not impose a solver tie rule. complete_argmin lists
ALL original shores attaining that minimum, in increasing mask order. Empty domains
have comparison_pair=None and complete_argmin=(). Q1 is a valid active instance and
all four branch seeds return None without a fake shore or root.

### Fixture table: U13_OPTIMA

| solve | domain | comparison_pair | complete_argmin |
| --- | --- | --- | --- |
| `'Q1-j0'` | `()` | `None` | `()` |
| `'Q1-j1'` | `()` | `None` | `()` |
| `'Q1-j2'` | `()` | `None` | `()` |
| `'Q1-j3'` | `()` | `None` | `()` |
| `'DOUBLE-j0'` | `(1, 2)` | `(2, 2)` | `(1, 2)` |
| `'DOUBLE-j1'` | `()` | `None` | `()` |
| `'DOUBLE-j2'` | `()` | `None` | `()` |
| `'DOUBLE-j3'` | `()` | `None` | `()` |
| `'UNEQUAL-j0'` | `(2, 3)` | `(2, 2)` | `(2, 3)` |
| `'UNEQUAL-j1'` | `()` | `None` | `()` |
| `'UNEQUAL-j2'` | `(3,)` | `(-4, 2)` | `(3,)` |
| `'UNEQUAL-j3'` | `(1,)` | `(-2, 2)` | `(1,)` |
| `'EQUALITY-j0'` | `()` | `None` | `()` |
| `'EQUALITY-j1'` | `()` | `None` | `()` |
| `'EQUALITY-j2'` | `()` | `None` | `()` |
| `'EQUALITY-j3'` | `(1, 2, 3, 4, 5, 6)` | `(-2, 2)` | `(1, 2, 3, 4, 5, 6)` |
| `'WTRI-j0'` | `(1, 2, 4, 7)` | `(2, 4)` | `(7,)` |
| `'WTRI-j1'` | `(3, 5, 6)` | `(2, 2)` | `(3, 5, 6)` |
| `'WTRI-j2'` | `(7,)` | `(-6, 2)` | `(7,)` |
| `'WTRI-j3'` | `(3, 5, 6)` | `(-4, 2)` | `(3, 5, 6)` |
| `'ODDFULL-j0'` | `(4, 5, 6, 7)` | `(2, 2)` | `(4,)` |
| `'ODDFULL-j1'` | `()` | `None` | `()` |
| `'ODDFULL-j2'` | `(5, 6, 7)` | `(-6, 4)` | `(7,)` |
| `'ODDFULL-j3'` | `(1, 2, 3)` | `(-2, 2)` | `(1, 2, 3)` |
| `'TIECARD-j0'` | `()` | `None` | `()` |
| `'TIECARD-j1'` | `()` | `None` | `()` |
| `'TIECARD-j2'` | `(5, 6)` | `(-2, 2)` | `(5, 6)` |
| `'TIECARD-j3'` | `(3, 4)` | `(-2, 2)` | `(3, 4)` |
| `'RICH-j0'` | `(1, 2, 5, 6, 9, 10, 13, 14, 17, 18, 21, 22, 25, 26, 29, 30)` | `(4, 6)` | `(5, 6)` |
| `'RICH-j1'` | `(3, 4, 7, 11, 12, 15, 19, 20, 23, 27, 28)` | `(2, 6)` | `(7,)` |
| `'RICH-j2'` | `(7, 11, 13, 14, 17, 18, 20, 23, 24, 27, 29, 30)` | `(-8, 2)` | `(7,)` |
| `'RICH-j3'` | `(3, 5, 6, 9, 10, 12, 15, 16, 19, 21, 22, 25, 26, 28)` | `(-6, 2)` | `(5, 6)` |
| `'MIXED-j0'` | `(2, 3, 6, 7, 8, 9, 12, 13)` | `(16, 18)` | `(7,)` |
| `'MIXED-j1'` | `(1, 4, 5, 10, 11, 14)` | `(16, 16)` | `(14,)` |
| `'MIXED-j2'` | `(2, 3, 6, 7, 8, 9, 12, 13)` | `(-18, 8)` | `(7,)` |
| `'MIXED-j3'` | `(1, 4, 5, 10, 11, 14)` | `(-24, 12)` | `(14,)` |
| `'ZERO-j0'` | `()` | `None` | `()` |
| `'ZERO-j1'` | `()` | `None` | `()` |
| `'ZERO-j2'` | `(1, 2)` | `(0, 2)` | `(1, 2)` |
| `'ZERO-j3'` | `()` | `None` | `()` |
| `'SHIFT-j0'` | `()` | `None` | `()` |
| `'SHIFT-j1'` | `()` | `None` | `()` |
| `'SHIFT-j2'` | `()` | `None` | `()` |
| `'SHIFT-j3'` | `(1, 2)` | `(-2, 4)` | `(1, 2)` |
| `'LOW0-j0'` | `(1, 2, 5, 6, 9, 10, 13, 14)` | `(12, 8)` | `(1, 2)` |
| `'LOW0-j1'` | `(3, 4, 7, 8, 11, 12)` | `(6, 14)` | `(3,)` |
| `'LOW0-j2'` | `(1, 2, 4, 7, 8, 11, 13, 14)` | `(-20, 10)` | `(11,)` |
| `'LOW0-j3'` | `(3, 5, 6, 9, 10, 12)` | `(-20, 6)` | `(3,)` |
| `'LOW1-j0'` | `(4, 5, 6, 7, 8, 9, 10, 11, 20, 21, 22, 23, 24, 25, 26, 27)` | `(16, 18)` | `(21,)` |
| `'LOW1-j1'` | `(1, 2, 3, 12, 13, 14, 15, 16, 17, 18, 19, 28, 29, 30)` | `(2, 2)` | `(2,)` |
| `'LOW1-j2'` | `(1, 7, 8, 11, 13, 14, 17, 18, 20, 23, 24, 27, 29, 30)` | `(-32, 16)` | `(23,)` |
| `'LOW1-j3'` | `(3, 5, 6, 9, 10, 12, 15, 16, 19, 21, 22, 25, 26, 28)` | `(-34, 16)` | `(21,)` |
| `'HIGH2-j0'` | `()` | `None` | `()` |
| `'HIGH2-j1'` | `(2, 3, 6)` | `(2, 2)` | `(2,)` |
| `'HIGH2-j2'` | `(3, 4, 5)` | `(-2, 2)` | `(3,)` |
| `'HIGH2-j3'` | `(1, 6)` | `(-6, 4)` | `(6,)` |
| `'HIGH3-j0'` | `(1, 3, 5, 7)` | `(2, 2)` | `(1, 3, 7)` |
| `'HIGH3-j1'` | `(2, 6)` | `(2, 2)` | `(2,)` |
| `'HIGH3-j2'` | `(4, 7)` | `(-8, 4)` | `(7,)` |
| `'HIGH3-j3'` | `(3, 5, 6)` | `(-4, 2)` | `(3,)` |
| `'NONMAX-j0'` | `(2, 3, 6, 7)` | `(2, 4)` | `(6, 7)` |
| `'NONMAX-j1'` | `(4, 5)` | `(2, 2)` | `(4, 5)` |
| `'NONMAX-j2'` | `(7,)` | `(-6, 2)` | `(7,)` |
| `'NONMAX-j3'` | `(3, 5, 6)` | `(-6, 2)` | `(6,)` |
| `'CHOICE-j0'` | `(1, 2, 5, 6)` | `(2, 2)` | `(1, 2)` |
| `'CHOICE-j1'` | `(3,)` | `(4, 2)` | `(3,)` |
| `'CHOICE-j2'` | `(5, 6)` | `(-4, 4)` | `(5, 6)` |
| `'CHOICE-j3'` | `(3, 4)` | `(-2, 2)` | `(3,)` |


## ORACLE-085 — Full shipped Standard query trajectories and literal results

**Classification:** `BRANCH_ORACLE`; accounting fields are `LOCAL_CONTRACT_FIXTURE`.
**Coverage:** ST4--ST9, ST14--ST15, ST17--ST18.

Each solve id NAME-jJ uses the INPUTS row NAME and branch J. Steps start at zero.
Seed is exactly (0,1). For a feasible seed pair (c0,h0), the next parameter is the
literal K=(c0+h0,h0). Every negative-residual loop query is followed by the fresh
source pair (c,h); every displayed residual is B*c-A*h for the SAME displayed (A,B).
At exact zero, return the SUBMITTED parameter and the CURRENT oracle shore, without
normalizing or replacing the submitted pair by the terminal shore's source terms.
all_residual_argmins is the complete source-domain minimum set, independent of the
shipped chosen U. retained_family and retained_GR_pair explain the shipped first-retention
selection; they are reference explanations, not new BranchResult fields.

SOLVES records (t,outer,updates). On feasible rows these are (u+2,u+1,u), u>=1;
on infeasible rows (1,0,0). Every loop invocation, including terminal, counts once.
aggregate_structural_counts is t times the per-query four-count prefix; preparation
is separate. No flow augmentation, BFS scan, or full-integer-peak value is invented.
LOW0-j0, LOW1-j1, HIGH2-j2 and HIGH3-j3 each require two negative-residual resets;
thus every branch has a registered multi-update trajectory. RICH-j3 also has two.

### Fixture table: U13_SOLVES

| solve | returned_root | terminal_U | t_outer_updates | query_structural_counts | aggregate_structural_counts |
| --- | --- | --- | --- | --- | --- |
| `'Q1-j0'` | `None` | `None` | `(1, 0, 0)` | `(1, 0, 0, 0)` | `(1, 0, 0, 0)` |
| `'Q1-j1'` | `None` | `None` | `(1, 0, 0)` | `(0, 0, 0, 0)` | `(0, 0, 0, 0)` |
| `'Q1-j2'` | `None` | `None` | `(1, 0, 0)` | `(0, 0, 0, 0)` | `(0, 0, 0, 0)` |
| `'Q1-j3'` | `None` | `None` | `(1, 0, 0)` | `(2, 0, 0, 0)` | `(2, 0, 0, 0)` |
| `'DOUBLE-j0'` | `(2, 2)` | `1` | `(3, 2, 1)` | `(1, 1, 1, 7)` | `(3, 3, 3, 21)` |
| `'DOUBLE-j1'` | `None` | `None` | `(1, 0, 0)` | `(4, 0, 0, 0)` | `(4, 0, 0, 0)` |
| `'DOUBLE-j2'` | `None` | `None` | `(1, 0, 0)` | `(0, 0, 0, 0)` | `(0, 0, 0, 0)` |
| `'DOUBLE-j3'` | `None` | `None` | `(1, 0, 0)` | `(2, 0, 0, 0)` | `(2, 0, 0, 0)` |
| `'UNEQUAL-j0'` | `(2, 2)` | `3` | `(3, 2, 1)` | `(1, 1, 1, 7)` | `(3, 3, 3, 21)` |
| `'UNEQUAL-j1'` | `None` | `None` | `(1, 0, 0)` | `(2, 0, 0, 0)` | `(2, 0, 0, 0)` |
| `'UNEQUAL-j2'` | `(-4, 2)` | `3` | `(3, 2, 1)` | `(1, 1, 1, 3)` | `(3, 3, 3, 9)` |
| `'UNEQUAL-j3'` | `(-2, 2)` | `1` | `(3, 2, 1)` | `(2, 1, 1, 1)` | `(6, 3, 3, 3)` |
| `'EQUALITY-j0'` | `None` | `None` | `(1, 0, 0)` | `(1, 0, 0, 0)` | `(1, 0, 0, 0)` |
| `'EQUALITY-j1'` | `None` | `None` | `(1, 0, 0)` | `(0, 0, 0, 0)` | `(0, 0, 0, 0)` |
| `'EQUALITY-j2'` | `None` | `None` | `(1, 0, 0)` | `(3, 0, 0, 0)` | `(3, 0, 0, 0)` |
| `'EQUALITY-j3'` | `(-4, 4)` | `1` | `(3, 2, 1)` | `(6, 6, 6, 18)` | `(18, 18, 18, 54)` |
| `'WTRI-j0'` | `(2, 4)` | `7` | `(3, 2, 1)` | `(1, 1, 1, 13)` | `(3, 3, 3, 39)` |
| `'WTRI-j1'` | `(2, 2)` | `5` | `(3, 2, 1)` | `(18, 12, 12, 24)` | `(54, 36, 36, 72)` |
| `'WTRI-j2'` | `(-6, 2)` | `7` | `(3, 2, 1)` | `(1, 1, 1, 1)` | `(3, 3, 3, 3)` |
| `'WTRI-j3'` | `(-4, 2)` | `5` | `(3, 2, 1)` | `(6, 6, 6, 18)` | `(18, 18, 18, 54)` |
| `'ODDFULL-j0'` | `(2, 2)` | `4` | `(3, 2, 1)` | `(1, 1, 1, 13)` | `(3, 3, 3, 39)` |
| `'ODDFULL-j1'` | `None` | `None` | `(1, 0, 0)` | `(6, 0, 0, 0)` | `(6, 0, 0, 0)` |
| `'ODDFULL-j2'` | `(-6, 4)` | `7` | `(3, 2, 1)` | `(2, 2, 2, 14)` | `(6, 6, 6, 42)` |
| `'ODDFULL-j3'` | `(-4, 4)` | `1` | `(3, 2, 1)` | `(6, 4, 4, 12)` | `(18, 12, 12, 36)` |
| `'TIECARD-j0'` | `None` | `None` | `(1, 0, 0)` | `(1, 0, 0, 0)` | `(1, 0, 0, 0)` |
| `'TIECARD-j1'` | `None` | `None` | `(1, 0, 0)` | `(0, 0, 0, 0)` | `(0, 0, 0, 0)` |
| `'TIECARD-j2'` | `(-2, 2)` | `6` | `(3, 2, 1)` | `(1, 1, 1, 7)` | `(3, 3, 3, 21)` |
| `'TIECARD-j3'` | `(-2, 2)` | `3` | `(3, 2, 1)` | `(4, 4, 4, 12)` | `(12, 12, 12, 36)` |
| `'RICH-j0'` | `(4, 6)` | `5` | `(3, 2, 1)` | `(1, 1, 1, 31)` | `(3, 3, 3, 93)` |
| `'RICH-j1'` | `(2, 6)` | `7` | `(3, 2, 1)` | `(24, 17, 17, 149)` | `(72, 51, 51, 447)` |
| `'RICH-j2'` | `(-8, 2)` | `7` | `(3, 2, 1)` | `(5, 5, 5, 49)` | `(15, 15, 15, 147)` |
| `'RICH-j3'` | `(-6, 2)` | `6` | `(4, 3, 2)` | `(8, 8, 8, 104)` | `(32, 32, 32, 416)` |
| `'MIXED-j0'` | `(16, 18)` | `7` | `(3, 2, 1)` | `(1, 1, 1, 21)` | `(3, 3, 3, 63)` |
| `'MIXED-j1'` | `(16, 16)` | `14` | `(3, 2, 1)` | `(48, 26, 26, 118)` | `(144, 78, 78, 354)` |
| `'MIXED-j2'` | `(-18, 8)` | `7` | `(3, 2, 1)` | `(4, 4, 4, 52)` | `(12, 12, 12, 156)` |
| `'MIXED-j3'` | `(-24, 12)` | `14` | `(3, 2, 1)` | `(12, 10, 10, 70)` | `(36, 30, 30, 210)` |
| `'ZERO-j0'` | `None` | `None` | `(1, 0, 0)` | `(1, 0, 0, 0)` | `(1, 0, 0, 0)` |
| `'ZERO-j1'` | `None` | `None` | `(1, 0, 0)` | `(0, 0, 0, 0)` | `(0, 0, 0, 0)` |
| `'ZERO-j2'` | `(0, 2)` | `1` | `(3, 2, 1)` | `(2, 2, 2, 6)` | `(6, 6, 6, 18)` |
| `'ZERO-j3'` | `None` | `None` | `(1, 0, 0)` | `(2, 0, 0, 0)` | `(2, 0, 0, 0)` |
| `'SHIFT-j0'` | `None` | `None` | `(1, 0, 0)` | `(1, 0, 0, 0)` | `(1, 0, 0, 0)` |
| `'SHIFT-j1'` | `None` | `None` | `(1, 0, 0)` | `(0, 0, 0, 0)` | `(0, 0, 0, 0)` |
| `'SHIFT-j2'` | `None` | `None` | `(1, 0, 0)` | `(2, 0, 0, 0)` | `(2, 0, 0, 0)` |
| `'SHIFT-j3'` | `(-2, 4)` | `1` | `(3, 2, 1)` | `(2, 2, 2, 2)` | `(6, 6, 6, 6)` |
| `'LOW0-j0'` | `(12, 8)` | `1` | `(4, 3, 2)` | `(1, 1, 1, 21)` | `(4, 4, 4, 84)` |
| `'LOW0-j1'` | `(6, 14)` | `3` | `(3, 2, 1)` | `(32, 16, 16, 72)` | `(96, 48, 48, 216)` |
| `'LOW0-j2'` | `(-20, 10)` | `11` | `(3, 2, 1)` | `(4, 4, 4, 52)` | `(12, 12, 12, 156)` |
| `'LOW0-j3'` | `(-20, 6)` | `3` | `(3, 2, 1)` | `(8, 8, 8, 56)` | `(24, 24, 24, 168)` |
| `'LOW1-j0'` | `(16, 18)` | `21` | `(3, 2, 1)` | `(1, 1, 1, 31)` | `(3, 3, 3, 93)` |
| `'LOW1-j1'` | `(2, 2)` | `2` | `(4, 3, 2)` | `(50, 36, 36, 312)` | `(200, 144, 144, 1248)` |
| `'LOW1-j2'` | `(-32, 16)` | `23` | `(4, 3, 2)` | `(3, 3, 3, 63)` | `(12, 12, 12, 252)` |
| `'LOW1-j3'` | `(-34, 16)` | `21` | `(3, 2, 1)` | `(10, 10, 10, 130)` | `(30, 30, 30, 390)` |
| `'HIGH2-j0'` | `None` | `None` | `(1, 0, 0)` | `(1, 0, 0, 0)` | `(1, 0, 0, 0)` |
| `'HIGH2-j1'` | `(2, 2)` | `2` | `(3, 2, 1)` | `(6, 4, 4, 8)` | `(18, 12, 12, 24)` |
| `'HIGH2-j2'` | `(-2, 2)` | `3` | `(4, 3, 2)` | `(2, 2, 2, 14)` | `(8, 8, 8, 56)` |
| `'HIGH2-j3'` | `(-6, 4)` | `6` | `(3, 2, 1)` | `(6, 4, 4, 12)` | `(18, 12, 12, 36)` |
| `'HIGH3-j0'` | `(4, 4)` | `1` | `(3, 2, 1)` | `(1, 1, 1, 13)` | `(3, 3, 3, 39)` |
| `'HIGH3-j1'` | `(2, 2)` | `2` | `(3, 2, 1)` | `(12, 3, 3, 7)` | `(36, 9, 9, 21)` |
| `'HIGH3-j2'` | `(-8, 4)` | `7` | `(3, 2, 1)` | `(1, 1, 1, 7)` | `(3, 3, 3, 21)` |
| `'HIGH3-j3'` | `(-4, 2)` | `3` | `(4, 3, 2)` | `(6, 6, 6, 18)` | `(24, 24, 24, 72)` |
| `'NONMAX-j0'` | `(2, 4)` | `7` | `(3, 2, 1)` | `(1, 1, 1, 13)` | `(3, 3, 3, 39)` |
| `'NONMAX-j1'` | `(2, 2)` | `4` | `(3, 2, 1)` | `(8, 2, 2, 6)` | `(24, 6, 6, 18)` |
| `'NONMAX-j2'` | `(-6, 2)` | `7` | `(3, 2, 1)` | `(1, 1, 1, 1)` | `(3, 3, 3, 3)` |
| `'NONMAX-j3'` | `(-6, 2)` | `6` | `(3, 2, 1)` | `(4, 4, 4, 12)` | `(12, 12, 12, 36)` |
| `'CHOICE-j0'` | `(2, 2)` | `1` | `(3, 2, 1)` | `(1, 1, 1, 13)` | `(3, 3, 3, 39)` |
| `'CHOICE-j1'` | `(4, 2)` | `3` | `(3, 2, 1)` | `(8, 4, 4, 8)` | `(24, 12, 12, 24)` |
| `'CHOICE-j2'` | `(-4, 4)` | `6` | `(3, 2, 1)` | `(1, 1, 1, 7)` | `(3, 3, 3, 21)` |
| `'CHOICE-j3'` | `(-2, 2)` | `3` | `(3, 2, 1)` | `(4, 4, 4, 12)` | `(12, 12, 12, 36)` |


### Fixture table: U13_TRACES

| solve | step | phase | parameter | U | source_pair | raw | all_residual_argmins | retained_family | retained_GR_pair |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `'Q1-j0'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'Q1-j1'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'Q1-j2'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'Q1-j3'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'DOUBLE-j0'` | `0` | `'seed'` | `(0, 1)` | `1` | `(2, 2)` | `2` | `(1, 2)` | `0` | `(2, 3)` |
| `'DOUBLE-j0'` | `1` | `'K'` | `(4, 2)` | `1` | `(2, 2)` | `-4` | `(1, 2)` | `0` | `(2, 3)` |
| `'DOUBLE-j0'` | `2` | `'terminal'` | `(2, 2)` | `1` | `(2, 2)` | `0` | `(1, 2)` | `0` | `(2, 3)` |
| `'DOUBLE-j1'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'DOUBLE-j2'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'DOUBLE-j3'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'UNEQUAL-j0'` | `0` | `'seed'` | `(0, 1)` | `3` | `(2, 2)` | `2` | `(2, 3)` | `0` | `(2, 1)` |
| `'UNEQUAL-j0'` | `1` | `'K'` | `(4, 2)` | `3` | `(2, 2)` | `-4` | `(2, 3)` | `0` | `(2, 1)` |
| `'UNEQUAL-j0'` | `2` | `'terminal'` | `(2, 2)` | `3` | `(2, 2)` | `0` | `(2, 3)` | `0` | `(2, 1)` |
| `'UNEQUAL-j1'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'UNEQUAL-j2'` | `0` | `'seed'` | `(0, 1)` | `3` | `(-4, 2)` | `-4` | `(3,)` | `0` | `(0, 1)` |
| `'UNEQUAL-j2'` | `1` | `'K'` | `(-2, 2)` | `3` | `(-4, 2)` | `-4` | `(3,)` | `0` | `(0, 1)` |
| `'UNEQUAL-j2'` | `2` | `'terminal'` | `(-4, 2)` | `3` | `(-4, 2)` | `0` | `(3,)` | `0` | `(0, 1)` |
| `'UNEQUAL-j3'` | `0` | `'seed'` | `(0, 1)` | `1` | `(-2, 2)` | `-2` | `(1,)` | `0` | `(0, 1)` |
| `'UNEQUAL-j3'` | `1` | `'K'` | `(0, 2)` | `1` | `(-2, 2)` | `-4` | `(1,)` | `0` | `(0, 1)` |
| `'UNEQUAL-j3'` | `2` | `'terminal'` | `(-2, 2)` | `1` | `(-2, 2)` | `0` | `(1,)` | `0` | `(0, 1)` |
| `'EQUALITY-j0'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'EQUALITY-j1'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'EQUALITY-j2'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'EQUALITY-j3'` | `0` | `'seed'` | `(0, 1)` | `5` | `(-4, 4)` | `-4` | `(3, 5, 6)` | `0` | `(0, 1)` |
| `'EQUALITY-j3'` | `1` | `'K'` | `(0, 4)` | `5` | `(-4, 4)` | `-16` | `(3, 5, 6)` | `0` | `(0, 1)` |
| `'EQUALITY-j3'` | `2` | `'terminal'` | `(-4, 4)` | `1` | `(-2, 2)` | `0` | `(1, 2, 3, 4, 5, 6)` | `0` | `(0, 1)` |
| `'WTRI-j0'` | `0` | `'seed'` | `(0, 1)` | `1` | `(2, 2)` | `2` | `(1, 2, 4, 7)` | `0` | `(2, 1)` |
| `'WTRI-j0'` | `1` | `'K'` | `(4, 2)` | `7` | `(2, 4)` | `-12` | `(7,)` | `0` | `(0, 1)` |
| `'WTRI-j0'` | `2` | `'terminal'` | `(2, 4)` | `7` | `(2, 4)` | `0` | `(7,)` | `0` | `(2, 1)` |
| `'WTRI-j1'` | `0` | `'seed'` | `(0, 1)` | `5` | `(2, 2)` | `2` | `(3, 5, 6)` | `0` | `(2, 1)` |
| `'WTRI-j1'` | `1` | `'K'` | `(4, 2)` | `5` | `(2, 2)` | `-4` | `(3, 5, 6)` | `0` | `(0, 1)` |
| `'WTRI-j1'` | `2` | `'terminal'` | `(2, 2)` | `5` | `(2, 2)` | `0` | `(3, 5, 6)` | `0` | `(2, 1)` |
| `'WTRI-j2'` | `0` | `'seed'` | `(0, 1)` | `7` | `(-6, 2)` | `-6` | `(7,)` | `0` | `(0, 1)` |
| `'WTRI-j2'` | `1` | `'K'` | `(-4, 2)` | `7` | `(-6, 2)` | `-4` | `(7,)` | `0` | `(0, 1)` |
| `'WTRI-j2'` | `2` | `'terminal'` | `(-6, 2)` | `7` | `(-6, 2)` | `0` | `(7,)` | `0` | `(0, 1)` |
| `'WTRI-j3'` | `0` | `'seed'` | `(0, 1)` | `5` | `(-4, 2)` | `-4` | `(3, 5, 6)` | `0` | `(0, 1)` |
| `'WTRI-j3'` | `1` | `'K'` | `(-2, 2)` | `5` | `(-4, 2)` | `-4` | `(3, 5, 6)` | `0` | `(0, 1)` |
| `'WTRI-j3'` | `2` | `'terminal'` | `(-4, 2)` | `5` | `(-4, 2)` | `0` | `(3, 5, 6)` | `0` | `(2, 1)` |
| `'ODDFULL-j0'` | `0` | `'seed'` | `(0, 1)` | `4` | `(2, 2)` | `2` | `(4,)` | `0` | `(4, 1)` |
| `'ODDFULL-j0'` | `1` | `'K'` | `(4, 2)` | `4` | `(2, 2)` | `-4` | `(4,)` | `0` | `(4, 1)` |
| `'ODDFULL-j0'` | `2` | `'terminal'` | `(2, 2)` | `4` | `(2, 2)` | `0` | `(4,)` | `0` | `(4, 1)` |
| `'ODDFULL-j1'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'ODDFULL-j2'` | `0` | `'seed'` | `(0, 1)` | `7` | `(-6, 4)` | `-6` | `(7,)` | `0` | `(0, 1)` |
| `'ODDFULL-j2'` | `1` | `'K'` | `(-2, 4)` | `7` | `(-6, 4)` | `-16` | `(7,)` | `0` | `(0, 1)` |
| `'ODDFULL-j2'` | `2` | `'terminal'` | `(-6, 4)` | `7` | `(-6, 4)` | `0` | `(7,)` | `0` | `(0, 1)` |
| `'ODDFULL-j3'` | `0` | `'seed'` | `(0, 1)` | `3` | `(-4, 4)` | `-4` | `(3,)` | `2` | `(0, 1)` |
| `'ODDFULL-j3'` | `1` | `'K'` | `(0, 4)` | `3` | `(-4, 4)` | `-16` | `(3,)` | `2` | `(0, 1)` |
| `'ODDFULL-j3'` | `2` | `'terminal'` | `(-4, 4)` | `1` | `(-2, 2)` | `0` | `(1, 2, 3)` | `0` | `(0, 2)` |
| `'TIECARD-j0'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'TIECARD-j1'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'TIECARD-j2'` | `0` | `'seed'` | `(0, 1)` | `6` | `(-2, 2)` | `-2` | `(5, 6)` | `0` | `(0, 2)` |
| `'TIECARD-j2'` | `1` | `'K'` | `(0, 2)` | `6` | `(-2, 2)` | `-4` | `(5, 6)` | `0` | `(0, 2)` |
| `'TIECARD-j2'` | `2` | `'terminal'` | `(-2, 2)` | `6` | `(-2, 2)` | `0` | `(5, 6)` | `0` | `(0, 2)` |
| `'TIECARD-j3'` | `0` | `'seed'` | `(0, 1)` | `3` | `(-2, 2)` | `-2` | `(3, 4)` | `0` | `(2, 1)` |
| `'TIECARD-j3'` | `1` | `'K'` | `(0, 2)` | `3` | `(-2, 2)` | `-4` | `(3, 4)` | `0` | `(2, 1)` |
| `'TIECARD-j3'` | `2` | `'terminal'` | `(-2, 2)` | `3` | `(-2, 2)` | `0` | `(3, 4)` | `0` | `(2, 1)` |
| `'RICH-j0'` | `0` | `'seed'` | `(0, 1)` | `1` | `(2, 2)` | `2` | `(1, 2)` | `0` | `(2, 1)` |
| `'RICH-j0'` | `1` | `'K'` | `(4, 2)` | `6` | `(4, 6)` | `-16` | `(5, 6)` | `0` | `(0, 2)` |
| `'RICH-j0'` | `2` | `'terminal'` | `(4, 6)` | `5` | `(4, 6)` | `0` | `(5, 6)` | `0` | `(2, 3)` |
| `'RICH-j1'` | `0` | `'seed'` | `(0, 1)` | `7` | `(2, 6)` | `2` | `(7,)` | `4` | `(0, 1)` |
| `'RICH-j1'` | `1` | `'K'` | `(8, 6)` | `7` | `(2, 6)` | `-36` | `(7,)` | `4` | `(0, 1)` |
| `'RICH-j1'` | `2` | `'terminal'` | `(2, 6)` | `7` | `(2, 6)` | `0` | `(7,)` | `4` | `(0, 1)` |
| `'RICH-j2'` | `0` | `'seed'` | `(0, 1)` | `23` | `(-10, 4)` | `-10` | `(23,)` | `0` | `(0, 5)` |
| `'RICH-j2'` | `1` | `'K'` | `(-6, 4)` | `7` | `(-8, 2)` | `-20` | `(7,)` | `1` | `(0, 1)` |
| `'RICH-j2'` | `2` | `'terminal'` | `(-8, 2)` | `7` | `(-8, 2)` | `0` | `(7,)` | `1` | `(0, 1)` |
| `'RICH-j3'` | `0` | `'seed'` | `(0, 1)` | `15` | `(-10, 4)` | `-10` | `(15,)` | `4` | `(4, 1)` |
| `'RICH-j3'` | `1` | `'K'` | `(-6, 4)` | `15` | `(-10, 4)` | `-16` | `(15,)` | `4` | `(4, 1)` |
| `'RICH-j3'` | `2` | `'reset-query'` | `(-10, 4)` | `6` | `(-6, 2)` | `-4` | `(5, 6)` | `1` | `(0, 1)` |
| `'RICH-j3'` | `3` | `'terminal'` | `(-6, 2)` | `6` | `(-6, 2)` | `0` | `(5, 6)` | `1` | `(0, 1)` |
| `'MIXED-j0'` | `0` | `'seed'` | `(0, 1)` | `2` | `(10, 6)` | `10` | `(2,)` | `0` | `(3, 1)` |
| `'MIXED-j0'` | `1` | `'K'` | `(16, 6)` | `7` | `(16, 18)` | `-192` | `(7,)` | `0` | `(0, 5)` |
| `'MIXED-j0'` | `2` | `'terminal'` | `(16, 18)` | `7` | `(16, 18)` | `0` | `(7,)` | `0` | `(2, 5)` |
| `'MIXED-j1'` | `0` | `'seed'` | `(0, 1)` | `1` | `(6, 4)` | `6` | `(1,)` | `0` | `(0, 1)` |
| `'MIXED-j1'` | `1` | `'K'` | `(10, 4)` | `14` | `(16, 16)` | `-96` | `(14,)` | `13` | `(0, 1)` |
| `'MIXED-j1'` | `2` | `'terminal'` | `(16, 16)` | `14` | `(16, 16)` | `0` | `(14,)` | `13` | `(0, 1)` |
| `'MIXED-j2'` | `0` | `'seed'` | `(0, 1)` | `13` | `(-18, 10)` | `-18` | `(7, 13)` | `0` | `(0, 2)` |
| `'MIXED-j2'` | `1` | `'K'` | `(-8, 10)` | `7` | `(-18, 8)` | `-116` | `(7,)` | `0` | `(0, 4)` |
| `'MIXED-j2'` | `2` | `'terminal'` | `(-18, 8)` | `7` | `(-18, 8)` | `0` | `(7,)` | `0` | `(0, 4)` |
| `'MIXED-j3'` | `0` | `'seed'` | `(0, 1)` | `14` | `(-24, 12)` | `-24` | `(14,)` | `1` | `(0, 1)` |
| `'MIXED-j3'` | `1` | `'K'` | `(-12, 12)` | `14` | `(-24, 12)` | `-144` | `(14,)` | `1` | `(0, 1)` |
| `'MIXED-j3'` | `2` | `'terminal'` | `(-24, 12)` | `14` | `(-24, 12)` | `0` | `(14,)` | `1` | `(0, 1)` |
| `'ZERO-j0'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'ZERO-j1'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'ZERO-j2'` | `0` | `'seed'` | `(0, 1)` | `1` | `(0, 2)` | `0` | `(1, 2)` | `0` | `(0, 2)` |
| `'ZERO-j2'` | `1` | `'K'` | `(2, 2)` | `1` | `(0, 2)` | `-4` | `(1, 2)` | `0` | `(0, 2)` |
| `'ZERO-j2'` | `2` | `'terminal'` | `(0, 2)` | `1` | `(0, 2)` | `0` | `(1, 2)` | `0` | `(0, 2)` |
| `'ZERO-j3'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'SHIFT-j0'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'SHIFT-j1'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'SHIFT-j2'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'SHIFT-j3'` | `0` | `'seed'` | `(0, 1)` | `1` | `(-2, 4)` | `-2` | `(1, 2)` | `0` | `(0, 1)` |
| `'SHIFT-j3'` | `1` | `'K'` | `(2, 4)` | `1` | `(-2, 4)` | `-16` | `(1, 2)` | `0` | `(0, 1)` |
| `'SHIFT-j3'` | `2` | `'terminal'` | `(-2, 4)` | `1` | `(-2, 4)` | `0` | `(1, 2)` | `0` | `(0, 1)` |
| `'LOW0-j0'` | `0` | `'seed'` | `(0, 1)` | `1` | `(12, 8)` | `12` | `(1, 2)` | `0` | `(2, 3)` |
| `'LOW0-j0'` | `1` | `'K'` | `(20, 8)` | `14` | `(24, 14)` | `-88` | `(13, 14)` | `0` | `(0, 2)` |
| `'LOW0-j0'` | `2` | `'reset-query'` | `(24, 14)` | `1` | `(12, 8)` | `-24` | `(1, 2)` | `0` | `(2, 3)` |
| `'LOW0-j0'` | `3` | `'terminal'` | `(12, 8)` | `1` | `(12, 8)` | `0` | `(1, 2)` | `0` | `(2, 3)` |
| `'LOW0-j1'` | `0` | `'seed'` | `(0, 1)` | `3` | `(6, 14)` | `6` | `(3,)` | `2` | `(0, 1)` |
| `'LOW0-j1'` | `1` | `'K'` | `(20, 14)` | `3` | `(6, 14)` | `-196` | `(3,)` | `2` | `(0, 1)` |
| `'LOW0-j1'` | `2` | `'terminal'` | `(6, 14)` | `3` | `(6, 14)` | `0` | `(3,)` | `2` | `(0, 1)` |
| `'LOW0-j2'` | `0` | `'seed'` | `(0, 1)` | `11` | `(-20, 10)` | `-20` | `(7, 11)` | `0` | `(0, 3)` |
| `'LOW0-j2'` | `1` | `'K'` | `(-10, 10)` | `11` | `(-20, 10)` | `-100` | `(11,)` | `0` | `(4, 3)` |
| `'LOW0-j2'` | `2` | `'terminal'` | `(-20, 10)` | `11` | `(-20, 10)` | `0` | `(11,)` | `0` | `(4, 3)` |
| `'LOW0-j3'` | `0` | `'seed'` | `(0, 1)` | `3` | `(-20, 6)` | `-20` | `(3,)` | `2` | `(0, 3)` |
| `'LOW0-j3'` | `1` | `'K'` | `(-14, 6)` | `3` | `(-20, 6)` | `-36` | `(3,)` | `2` | `(0, 1)` |
| `'LOW0-j3'` | `2` | `'terminal'` | `(-20, 6)` | `3` | `(-20, 6)` | `0` | `(3,)` | `2` | `(0, 1)` |
| `'LOW1-j0'` | `0` | `'seed'` | `(0, 1)` | `10` | `(4, 4)` | `4` | `(10,)` | `0` | `(5, 1)` |
| `'LOW1-j0'` | `1` | `'K'` | `(8, 4)` | `21` | `(16, 18)` | `-80` | `(21, 23)` | `0` | `(0, 3)` |
| `'LOW1-j0'` | `2` | `'terminal'` | `(16, 18)` | `21` | `(16, 18)` | `0` | `(21,)` | `0` | `(2, 1)` |
| `'LOW1-j1'` | `0` | `'seed'` | `(0, 1)` | `2` | `(2, 2)` | `2` | `(2,)` | `14` | `(0, 1)` |
| `'LOW1-j1'` | `1` | `'K'` | `(4, 2)` | `29` | `(20, 18)` | `-32` | `(29,)` | `5` | `(0, 1)` |
| `'LOW1-j1'` | `2` | `'reset-query'` | `(20, 18)` | `2` | `(2, 2)` | `-4` | `(2,)` | `14` | `(0, 2)` |
| `'LOW1-j1'` | `3` | `'terminal'` | `(2, 2)` | `2` | `(2, 2)` | `0` | `(2,)` | `14` | `(0, 1)` |
| `'LOW1-j2'` | `0` | `'seed'` | `(0, 1)` | `29` | `(-34, 18)` | `-34` | `(29,)` | `0` | `(0, 2)` |
| `'LOW1-j2'` | `1` | `'K'` | `(-16, 18)` | `29` | `(-34, 18)` | `-324` | `(29,)` | `0` | `(4, 2)` |
| `'LOW1-j2'` | `2` | `'reset-query'` | `(-34, 18)` | `23` | `(-32, 16)` | `-32` | `(23,)` | `0` | `(2, 4)` |
| `'LOW1-j2'` | `3` | `'terminal'` | `(-32, 16)` | `23` | `(-32, 16)` | `0` | `(23,)` | `0` | `(2, 4)` |
| `'LOW1-j3'` | `0` | `'seed'` | `(0, 1)` | `21` | `(-34, 16)` | `-34` | `(21,)` | `9` | `(0, 1)` |
| `'LOW1-j3'` | `1` | `'K'` | `(-18, 16)` | `21` | `(-34, 16)` | `-256` | `(21,)` | `9` | `(0, 1)` |
| `'LOW1-j3'` | `2` | `'terminal'` | `(-34, 16)` | `21` | `(-34, 16)` | `0` | `(21,)` | `9` | `(0, 1)` |
| `'HIGH2-j0'` | `0` | `'seed'` | `(0, 1)` | `None` | `None` | `None` | `()` | `None` | `None` |
| `'HIGH2-j1'` | `0` | `'seed'` | `(0, 1)` | `2` | `(2, 2)` | `2` | `(2,)` | `1` | `(0, 1)` |
| `'HIGH2-j1'` | `1` | `'K'` | `(4, 2)` | `2` | `(2, 2)` | `-4` | `(2,)` | `1` | `(0, 1)` |
| `'HIGH2-j1'` | `2` | `'terminal'` | `(2, 2)` | `2` | `(2, 2)` | `0` | `(2,)` | `1` | `(0, 1)` |
| `'HIGH2-j2'` | `0` | `'seed'` | `(0, 1)` | `5` | `(-2, 4)` | `-2` | `(3, 5)` | `0` | `(0, 2)` |
| `'HIGH2-j2'` | `1` | `'K'` | `(2, 4)` | `5` | `(-2, 4)` | `-16` | `(5,)` | `0` | `(0, 2)` |
| `'HIGH2-j2'` | `2` | `'reset-query'` | `(-2, 4)` | `3` | `(-2, 2)` | `-4` | `(3,)` | `0` | `(0, 3)` |
| `'HIGH2-j2'` | `3` | `'terminal'` | `(-2, 2)` | `3` | `(-2, 2)` | `0` | `(3,)` | `0` | `(0, 3)` |
| `'HIGH2-j3'` | `0` | `'seed'` | `(0, 1)` | `6` | `(-6, 4)` | `-6` | `(6,)` | `1` | `(0, 1)` |
| `'HIGH2-j3'` | `1` | `'K'` | `(-2, 4)` | `6` | `(-6, 4)` | `-16` | `(6,)` | `1` | `(0, 1)` |
| `'HIGH2-j3'` | `2` | `'terminal'` | `(-6, 4)` | `6` | `(-6, 4)` | `0` | `(6,)` | `1` | `(2, 1)` |
| `'HIGH3-j0'` | `0` | `'seed'` | `(0, 1)` | `1` | `(2, 2)` | `2` | `(1,)` | `0` | `(2, 1)` |
| `'HIGH3-j0'` | `1` | `'K'` | `(4, 2)` | `3` | `(4, 4)` | `-8` | `(3, 7)` | `0` | `(0, 1)` |
| `'HIGH3-j0'` | `2` | `'terminal'` | `(4, 4)` | `1` | `(2, 2)` | `0` | `(1, 3, 7)` | `0` | `(2, 1)` |
| `'HIGH3-j1'` | `0` | `'seed'` | `(0, 1)` | `2` | `(2, 2)` | `2` | `(2,)` | `7` | `(0, 1)` |
| `'HIGH3-j1'` | `1` | `'K'` | `(4, 2)` | `2` | `(2, 2)` | `-4` | `(2,)` | `7` | `(0, 1)` |
| `'HIGH3-j1'` | `2` | `'terminal'` | `(2, 2)` | `2` | `(2, 2)` | `0` | `(2,)` | `7` | `(0, 1)` |
| `'HIGH3-j2'` | `0` | `'seed'` | `(0, 1)` | `7` | `(-8, 4)` | `-8` | `(7,)` | `0` | `(0, 1)` |
| `'HIGH3-j2'` | `1` | `'K'` | `(-4, 4)` | `7` | `(-8, 4)` | `-16` | `(7,)` | `0` | `(0, 1)` |
| `'HIGH3-j2'` | `2` | `'terminal'` | `(-8, 4)` | `7` | `(-8, 4)` | `0` | `(7,)` | `0` | `(0, 1)` |
| `'HIGH3-j3'` | `0` | `'seed'` | `(0, 1)` | `6` | `(-6, 4)` | `-6` | `(6,)` | `1` | `(0, 1)` |
| `'HIGH3-j3'` | `1` | `'K'` | `(-2, 4)` | `6` | `(-6, 4)` | `-16` | `(6,)` | `1` | `(0, 1)` |
| `'HIGH3-j3'` | `2` | `'reset-query'` | `(-6, 4)` | `3` | `(-4, 2)` | `-4` | `(3,)` | `2` | `(0, 1)` |
| `'HIGH3-j3'` | `3` | `'terminal'` | `(-4, 2)` | `3` | `(-4, 2)` | `0` | `(3,)` | `2` | `(2, 1)` |
| `'NONMAX-j0'` | `0` | `'seed'` | `(0, 1)` | `2` | `(2, 2)` | `2` | `(2, 6, 7)` | `0` | `(3, 1)` |
| `'NONMAX-j0'` | `1` | `'K'` | `(4, 2)` | `6` | `(2, 4)` | `-12` | `(6, 7)` | `0` | `(0, 1)` |
| `'NONMAX-j0'` | `2` | `'terminal'` | `(2, 4)` | `7` | `(2, 4)` | `0` | `(6, 7)` | `0` | `(2, 1)` |
| `'NONMAX-j1'` | `0` | `'seed'` | `(0, 1)` | `4` | `(2, 2)` | `2` | `(4, 5)` | `5` | `(0, 2)` |
| `'NONMAX-j1'` | `1` | `'K'` | `(4, 2)` | `4` | `(2, 2)` | `-4` | `(4, 5)` | `5` | `(0, 2)` |
| `'NONMAX-j1'` | `2` | `'terminal'` | `(2, 2)` | `4` | `(2, 2)` | `0` | `(4, 5)` | `5` | `(0, 2)` |
| `'NONMAX-j2'` | `0` | `'seed'` | `(0, 1)` | `7` | `(-6, 2)` | `-6` | `(7,)` | `0` | `(0, 1)` |
| `'NONMAX-j2'` | `1` | `'K'` | `(-4, 2)` | `7` | `(-6, 2)` | `-4` | `(7,)` | `0` | `(0, 1)` |
| `'NONMAX-j2'` | `2` | `'terminal'` | `(-6, 2)` | `7` | `(-6, 2)` | `0` | `(7,)` | `0` | `(0, 1)` |
| `'NONMAX-j3'` | `0` | `'seed'` | `(0, 1)` | `6` | `(-6, 2)` | `-6` | `(6,)` | `1` | `(0, 1)` |
| `'NONMAX-j3'` | `1` | `'K'` | `(-4, 2)` | `6` | `(-6, 2)` | `-4` | `(6,)` | `1` | `(0, 1)` |
| `'NONMAX-j3'` | `2` | `'terminal'` | `(-6, 2)` | `6` | `(-6, 2)` | `0` | `(6,)` | `1` | `(0, 1)` |
| `'CHOICE-j0'` | `0` | `'seed'` | `(0, 1)` | `1` | `(2, 2)` | `2` | `(1, 2)` | `0` | `(2, 1)` |
| `'CHOICE-j0'` | `1` | `'K'` | `(4, 2)` | `1` | `(2, 2)` | `-4` | `(1, 2)` | `0` | `(2, 1)` |
| `'CHOICE-j0'` | `2` | `'terminal'` | `(2, 2)` | `1` | `(2, 2)` | `0` | `(1, 2)` | `0` | `(2, 1)` |
| `'CHOICE-j1'` | `0` | `'seed'` | `(0, 1)` | `3` | `(4, 2)` | `4` | `(3,)` | `0` | `(2, 1)` |
| `'CHOICE-j1'` | `1` | `'K'` | `(6, 2)` | `3` | `(4, 2)` | `-4` | `(3,)` | `0` | `(2, 1)` |
| `'CHOICE-j1'` | `2` | `'terminal'` | `(4, 2)` | `3` | `(4, 2)` | `0` | `(3,)` | `0` | `(2, 1)` |
| `'CHOICE-j2'` | `0` | `'seed'` | `(0, 1)` | `6` | `(-4, 4)` | `-4` | `(5, 6)` | `0` | `(0, 2)` |
| `'CHOICE-j2'` | `1` | `'K'` | `(0, 4)` | `6` | `(-4, 4)` | `-16` | `(5, 6)` | `0` | `(0, 2)` |
| `'CHOICE-j2'` | `2` | `'terminal'` | `(-4, 4)` | `6` | `(-4, 4)` | `0` | `(5, 6)` | `0` | `(0, 2)` |
| `'CHOICE-j3'` | `0` | `'seed'` | `(0, 1)` | `3` | `(-2, 2)` | `-2` | `(3, 4)` | `0` | `(2, 1)` |
| `'CHOICE-j3'` | `1` | `'K'` | `(0, 2)` | `3` | `(-2, 2)` | `-4` | `(3, 4)` | `0` | `(2, 1)` |
| `'CHOICE-j3'` | `2` | `'terminal'` | `(-2, 2)` | `3` | `(-2, 2)` | `0` | `(3,)` | `0` | `(2, 1)` |


## ORACLE-086 — Terminal raw-pair, terminal-shore, seed and tie traps

**Classification:** `BRANCH_ORACLE` / `LOCAL_CONTRACT_FIXTURE`.
**Coverage:** ST4--ST5, ST7--ST10.

For EQUALITY, all nonempty proper shores belong to D3. A singleton has (c,h)=(-2,2)
and an adjacent two-vertex shore has (-4,4), so every source ratio is -1. At seed 0,
minimal c is -4. The first ordered family forces vertex 0 in and vertex 1 out, and
its selected minimizing shore is U=5. K is (0,4); the next query again chooses U=5,
with residual -16, and updates to (-4,4). At that terminal parameter every D3 residual
is zero. In the first family, the least ordinary minimizing shore is now U=1.
Therefore the exact return is BranchResult((-4,4),1), NOT BranchResult((-2,2),1),
NOT BranchResult((-1,1),1), and NOT BranchResult((-4,4),5).

RICH-j0 separately changes shore 6 to shore 5 while retaining the same (4,6) terms.
NONMAX-j0 at the seed has tied shores (2,6,7) with h=(2,4,4); the shipped choice is
shore 2. Max-h is not the implementation rule, though a legal argmin substitution may
incidentally or deliberately choose a larger h in the separate mathematical-freedom test.
ZERO-j2 has a feasible zero seed, still makes K and terminal queries, and returns (0,2).
SHIFT-j3 starts from negative numerator -2 but +1 yields positive K numerator 2.

### Fixture table: U13_TIE_TRAPS

| id | solve | step | submitted_pair | selected_U | selected_pair | purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `'terminal-scale'` | `'EQUALITY-j3'` | `2` | `(-4, 4)` | `1` | `(-2, 2)` | `'Return submitted pair and current shore, not terminal c/h or old shore.'` |
| `'terminal-shore'` | `'RICH-j0'` | `2` | `(4, 6)` | `5` | `(4, 6)` | `'Previous update selected U=6; terminal selects U=5.'` |
| `'seed-nonmax-h'` | `'NONMAX-j0'` | `0` | `(0, 1)` | `2` | `(2, 2)` | `'Seed argmins (2,6,7); h=(2,4,4); no maximum-h selection.'` |
| `'zero-seed'` | `'ZERO-j2'` | `0` | `(0, 1)` | `1` | `(0, 2)` | `'Zero seed continues through K=(2,2); returned root stays (0,2).'` |
| `'positive-K-from-negative'` | `'SHIFT-j3'` | `1` | `(2, 4)` | `1` | `(-2, 4)` | `'Negative seed c=-2 becomes positive initial numerator 2.'` |


## ORACLE-087 — All legal argmin paths on named tie fixtures

**Classification:** `BRANCH_ORACLE`. **Coverage:** ST8--ST10 and historical A4 for
Standard only. These are legal oracle substitutions, NOT alternate production modes.

Every listed sequence includes the seed, K and the terminal query. For each row of a
sequence, the selected shore attains the independently enumerated residual minimum.
Every terminal shore attains the same numerical source-domain optimum for that solve.
Raw representations, intermediate parameters, query counts, and attaining shores need
not agree between different legal policies. The SHIPPED expectation stays ORACLE-085.

CHOICE has exactly two D3 shores: U=3 with (c,h)=(-2,2), and U=4 with (-2,4).
Both minimize c at the seed. Seed U=3 gives K=(0,2), at which either shore is legal.
Choosing U=3 then terminates in three total queries; choosing U=4 requires a fourth.
Seed U=4 gives K=(2,4), selects U=4, then U=3, then terminates: also four queries.
All three paths return numerical root -1. This is a concrete counterexample to requiring
identical trajectories or statistics for all mathematically legal argmin choices.

The table lists the entire finite choice tree for CHOICE-j3, EQUALITY-j3, NONMAX-j0,
RICH-j0 and RICH-j3, not a selected subset of policies. The broader exhaustive core
choice census appears separately below; overlapping cases are not disjoint coverage.

### Fixture table: U13_LEGAL_PATHS

| solve | path_id | parameter_and_shore_sequence | returned_root | terminal_U | t_outer_updates |
| --- | --- | --- | --- | --- | --- |
| `'CHOICE-j3'` | `0` | `(((0, 1), 3), ((0, 2), 3), ((-2, 2), 3))` | `(-2, 2)` | `3` | `(3, 2, 1)` |
| `'CHOICE-j3'` | `1` | `(((0, 1), 3), ((0, 2), 4), ((-2, 4), 3), ((-2, 2), 3))` | `(-2, 2)` | `3` | `(4, 3, 2)` |
| `'CHOICE-j3'` | `2` | `(((0, 1), 4), ((2, 4), 4), ((-2, 4), 3), ((-2, 2), 3))` | `(-2, 2)` | `3` | `(4, 3, 2)` |
| `'EQUALITY-j3'` | `0` | `(((0, 1), 3), ((0, 4), 3), ((-4, 4), 1))` | `(-4, 4)` | `1` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `1` | `(((0, 1), 3), ((0, 4), 3), ((-4, 4), 2))` | `(-4, 4)` | `2` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `2` | `(((0, 1), 3), ((0, 4), 3), ((-4, 4), 3))` | `(-4, 4)` | `3` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `3` | `(((0, 1), 3), ((0, 4), 3), ((-4, 4), 4))` | `(-4, 4)` | `4` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `4` | `(((0, 1), 3), ((0, 4), 3), ((-4, 4), 5))` | `(-4, 4)` | `5` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `5` | `(((0, 1), 3), ((0, 4), 3), ((-4, 4), 6))` | `(-4, 4)` | `6` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `6` | `(((0, 1), 3), ((0, 4), 5), ((-4, 4), 1))` | `(-4, 4)` | `1` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `7` | `(((0, 1), 3), ((0, 4), 5), ((-4, 4), 2))` | `(-4, 4)` | `2` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `8` | `(((0, 1), 3), ((0, 4), 5), ((-4, 4), 3))` | `(-4, 4)` | `3` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `9` | `(((0, 1), 3), ((0, 4), 5), ((-4, 4), 4))` | `(-4, 4)` | `4` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `10` | `(((0, 1), 3), ((0, 4), 5), ((-4, 4), 5))` | `(-4, 4)` | `5` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `11` | `(((0, 1), 3), ((0, 4), 5), ((-4, 4), 6))` | `(-4, 4)` | `6` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `12` | `(((0, 1), 3), ((0, 4), 6), ((-4, 4), 1))` | `(-4, 4)` | `1` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `13` | `(((0, 1), 3), ((0, 4), 6), ((-4, 4), 2))` | `(-4, 4)` | `2` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `14` | `(((0, 1), 3), ((0, 4), 6), ((-4, 4), 3))` | `(-4, 4)` | `3` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `15` | `(((0, 1), 3), ((0, 4), 6), ((-4, 4), 4))` | `(-4, 4)` | `4` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `16` | `(((0, 1), 3), ((0, 4), 6), ((-4, 4), 5))` | `(-4, 4)` | `5` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `17` | `(((0, 1), 3), ((0, 4), 6), ((-4, 4), 6))` | `(-4, 4)` | `6` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `18` | `(((0, 1), 5), ((0, 4), 3), ((-4, 4), 1))` | `(-4, 4)` | `1` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `19` | `(((0, 1), 5), ((0, 4), 3), ((-4, 4), 2))` | `(-4, 4)` | `2` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `20` | `(((0, 1), 5), ((0, 4), 3), ((-4, 4), 3))` | `(-4, 4)` | `3` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `21` | `(((0, 1), 5), ((0, 4), 3), ((-4, 4), 4))` | `(-4, 4)` | `4` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `22` | `(((0, 1), 5), ((0, 4), 3), ((-4, 4), 5))` | `(-4, 4)` | `5` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `23` | `(((0, 1), 5), ((0, 4), 3), ((-4, 4), 6))` | `(-4, 4)` | `6` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `24` | `(((0, 1), 5), ((0, 4), 5), ((-4, 4), 1))` | `(-4, 4)` | `1` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `25` | `(((0, 1), 5), ((0, 4), 5), ((-4, 4), 2))` | `(-4, 4)` | `2` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `26` | `(((0, 1), 5), ((0, 4), 5), ((-4, 4), 3))` | `(-4, 4)` | `3` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `27` | `(((0, 1), 5), ((0, 4), 5), ((-4, 4), 4))` | `(-4, 4)` | `4` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `28` | `(((0, 1), 5), ((0, 4), 5), ((-4, 4), 5))` | `(-4, 4)` | `5` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `29` | `(((0, 1), 5), ((0, 4), 5), ((-4, 4), 6))` | `(-4, 4)` | `6` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `30` | `(((0, 1), 5), ((0, 4), 6), ((-4, 4), 1))` | `(-4, 4)` | `1` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `31` | `(((0, 1), 5), ((0, 4), 6), ((-4, 4), 2))` | `(-4, 4)` | `2` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `32` | `(((0, 1), 5), ((0, 4), 6), ((-4, 4), 3))` | `(-4, 4)` | `3` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `33` | `(((0, 1), 5), ((0, 4), 6), ((-4, 4), 4))` | `(-4, 4)` | `4` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `34` | `(((0, 1), 5), ((0, 4), 6), ((-4, 4), 5))` | `(-4, 4)` | `5` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `35` | `(((0, 1), 5), ((0, 4), 6), ((-4, 4), 6))` | `(-4, 4)` | `6` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `36` | `(((0, 1), 6), ((0, 4), 3), ((-4, 4), 1))` | `(-4, 4)` | `1` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `37` | `(((0, 1), 6), ((0, 4), 3), ((-4, 4), 2))` | `(-4, 4)` | `2` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `38` | `(((0, 1), 6), ((0, 4), 3), ((-4, 4), 3))` | `(-4, 4)` | `3` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `39` | `(((0, 1), 6), ((0, 4), 3), ((-4, 4), 4))` | `(-4, 4)` | `4` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `40` | `(((0, 1), 6), ((0, 4), 3), ((-4, 4), 5))` | `(-4, 4)` | `5` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `41` | `(((0, 1), 6), ((0, 4), 3), ((-4, 4), 6))` | `(-4, 4)` | `6` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `42` | `(((0, 1), 6), ((0, 4), 5), ((-4, 4), 1))` | `(-4, 4)` | `1` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `43` | `(((0, 1), 6), ((0, 4), 5), ((-4, 4), 2))` | `(-4, 4)` | `2` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `44` | `(((0, 1), 6), ((0, 4), 5), ((-4, 4), 3))` | `(-4, 4)` | `3` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `45` | `(((0, 1), 6), ((0, 4), 5), ((-4, 4), 4))` | `(-4, 4)` | `4` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `46` | `(((0, 1), 6), ((0, 4), 5), ((-4, 4), 5))` | `(-4, 4)` | `5` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `47` | `(((0, 1), 6), ((0, 4), 5), ((-4, 4), 6))` | `(-4, 4)` | `6` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `48` | `(((0, 1), 6), ((0, 4), 6), ((-4, 4), 1))` | `(-4, 4)` | `1` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `49` | `(((0, 1), 6), ((0, 4), 6), ((-4, 4), 2))` | `(-4, 4)` | `2` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `50` | `(((0, 1), 6), ((0, 4), 6), ((-4, 4), 3))` | `(-4, 4)` | `3` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `51` | `(((0, 1), 6), ((0, 4), 6), ((-4, 4), 4))` | `(-4, 4)` | `4` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `52` | `(((0, 1), 6), ((0, 4), 6), ((-4, 4), 5))` | `(-4, 4)` | `5` | `(3, 2, 1)` |
| `'EQUALITY-j3'` | `53` | `(((0, 1), 6), ((0, 4), 6), ((-4, 4), 6))` | `(-4, 4)` | `6` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `0` | `(((0, 1), 2), ((4, 2), 6), ((2, 4), 6))` | `(2, 4)` | `6` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `1` | `(((0, 1), 2), ((4, 2), 6), ((2, 4), 7))` | `(2, 4)` | `7` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `2` | `(((0, 1), 2), ((4, 2), 7), ((2, 4), 6))` | `(2, 4)` | `6` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `3` | `(((0, 1), 2), ((4, 2), 7), ((2, 4), 7))` | `(2, 4)` | `7` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `4` | `(((0, 1), 6), ((6, 4), 6), ((2, 4), 6))` | `(2, 4)` | `6` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `5` | `(((0, 1), 6), ((6, 4), 6), ((2, 4), 7))` | `(2, 4)` | `7` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `6` | `(((0, 1), 6), ((6, 4), 7), ((2, 4), 6))` | `(2, 4)` | `6` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `7` | `(((0, 1), 6), ((6, 4), 7), ((2, 4), 7))` | `(2, 4)` | `7` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `8` | `(((0, 1), 7), ((6, 4), 6), ((2, 4), 6))` | `(2, 4)` | `6` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `9` | `(((0, 1), 7), ((6, 4), 6), ((2, 4), 7))` | `(2, 4)` | `7` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `10` | `(((0, 1), 7), ((6, 4), 7), ((2, 4), 6))` | `(2, 4)` | `6` | `(3, 2, 1)` |
| `'NONMAX-j0'` | `11` | `(((0, 1), 7), ((6, 4), 7), ((2, 4), 7))` | `(2, 4)` | `7` | `(3, 2, 1)` |
| `'RICH-j0'` | `0` | `(((0, 1), 1), ((4, 2), 5), ((4, 6), 5))` | `(4, 6)` | `5` | `(3, 2, 1)` |
| `'RICH-j0'` | `1` | `(((0, 1), 1), ((4, 2), 5), ((4, 6), 6))` | `(4, 6)` | `6` | `(3, 2, 1)` |
| `'RICH-j0'` | `2` | `(((0, 1), 1), ((4, 2), 6), ((4, 6), 5))` | `(4, 6)` | `5` | `(3, 2, 1)` |
| `'RICH-j0'` | `3` | `(((0, 1), 1), ((4, 2), 6), ((4, 6), 6))` | `(4, 6)` | `6` | `(3, 2, 1)` |
| `'RICH-j0'` | `4` | `(((0, 1), 2), ((4, 2), 5), ((4, 6), 5))` | `(4, 6)` | `5` | `(3, 2, 1)` |
| `'RICH-j0'` | `5` | `(((0, 1), 2), ((4, 2), 5), ((4, 6), 6))` | `(4, 6)` | `6` | `(3, 2, 1)` |
| `'RICH-j0'` | `6` | `(((0, 1), 2), ((4, 2), 6), ((4, 6), 5))` | `(4, 6)` | `5` | `(3, 2, 1)` |
| `'RICH-j0'` | `7` | `(((0, 1), 2), ((4, 2), 6), ((4, 6), 6))` | `(4, 6)` | `6` | `(3, 2, 1)` |
| `'RICH-j3'` | `0` | `(((0, 1), 15), ((-6, 4), 15), ((-10, 4), 5), ((-6, 2), 5))` | `(-6, 2)` | `5` | `(4, 3, 2)` |
| `'RICH-j3'` | `1` | `(((0, 1), 15), ((-6, 4), 15), ((-10, 4), 5), ((-6, 2), 6))` | `(-6, 2)` | `6` | `(4, 3, 2)` |
| `'RICH-j3'` | `2` | `(((0, 1), 15), ((-6, 4), 15), ((-10, 4), 6), ((-6, 2), 5))` | `(-6, 2)` | `5` | `(4, 3, 2)` |
| `'RICH-j3'` | `3` | `(((0, 1), 15), ((-6, 4), 15), ((-10, 4), 6), ((-6, 2), 6))` | `(-6, 2)` | `6` | `(4, 3, 2)` |


## ORACLE-088 — Exact diagnostic sums, maximum and mathematical independence

**Classification:** `LOCAL_CONTRACT_FIXTURE`. **Coverage:** ST2, ST4, ST14--ST15.

Each seven-tuple is a normally constructed BranchOracleStats in its closed field order:
(atomic_families_examined, atomic_families_feasible, parity_cut_calls,
ordinary_min_cut_calls, flow_augmentations, flow_bfs_scans, flow_peak_generated_value).
The nonzero and zero streams replace diagnostics ONLY while preserving the complete
legal LOW0-j0 mathematical reply stream. These are deliberately synthetic, valid
standalone stats; they are NOT measurements and need not describe feasible physical
backend work. Their variation must not affect seed/K handling, comparisons, termination,
returned root or shore, or query order. A zero diagnostic stream must not make the
solver confuse its mathematical initial-state flag with an iteration counter.

Aggregate the first six fields by addition and the seventh by maximum. The nonzero
peak 401 occurs at K, not at the last call; this catches last-value or sum substitutions.
The infeasible-injected stream tests inclusion of one returned seed diagnostic record
without manufacturing a successful result. It is also synthetic, not Q1's physical work.
The exact zero-descriptor seed has all-zero stats but still oracle_calls=1.
max_flow_calls remains the closed alias of aggregate ordinary_min_cut_calls.

### Fixture table: U13_DIAGNOSTIC_ROWS

| stream | solve | step | parameter | U | injected_BranchOracleStats |
| --- | --- | --- | --- | --- | --- |
| `'nonzero'` | `'LOW0-j0'` | `0` | `(0, 1)` | `1` | `(11, 2, 2, 3, 5, 7, 101)` |
| `'nonzero'` | `'LOW0-j0'` | `1` | `(20, 8)` | `14` | `(13, 3, 3, 17, 19, 23, 401)` |
| `'nonzero'` | `'LOW0-j0'` | `2` | `(24, 14)` | `1` | `(29, 5, 5, 31, 37, 41, 211)` |
| `'nonzero'` | `'LOW0-j0'` | `3` | `(12, 8)` | `1` | `(43, 7, 7, 47, 53, 59, 307)` |
| `'zero'` | `'LOW0-j0'` | `0` | `(0, 1)` | `1` | `(0, 0, 0, 0, 0, 0, 0)` |
| `'zero'` | `'LOW0-j0'` | `1` | `(20, 8)` | `14` | `(0, 0, 0, 0, 0, 0, 0)` |
| `'zero'` | `'LOW0-j0'` | `2` | `(24, 14)` | `1` | `(0, 0, 0, 0, 0, 0, 0)` |
| `'zero'` | `'LOW0-j0'` | `3` | `(12, 8)` | `1` | `(0, 0, 0, 0, 0, 0, 0)` |
| `'infeasible-injected'` | `'Q1-j0'` | `0` | `(0, 1)` | `None` | `(5, 3, 3, 7, 11, 13, 17)` |
| `'infeasible-zero-descriptors'` | `'Q1-j1'` | `0` | `(0, 1)` | `None` | `(0, 0, 0, 0, 0, 0, 0)` |


### Fixture table: U13_DIAGNOSTIC_TOTALS

| stream | returned_root | terminal_U | t_outer_updates | aggregate_BranchOracleStats | max_flow_calls |
| --- | --- | --- | --- | --- | --- |
| `'nonzero'` | `(12, 8)` | `1` | `(4, 3, 2)` | `(96, 17, 17, 98, 114, 130, 401)` | `98` |
| `'zero'` | `(12, 8)` | `1` | `(4, 3, 2)` | `(0, 0, 0, 0, 0, 0, 0)` | `0` |
| `'infeasible-injected'` | `None` | `None` | `(1, 0, 0)` | `(5, 3, 3, 7, 11, 13, 17)` | `7` |
| `'infeasible-zero-descriptors'` | `None` | `None` | `(1, 0, 0)` | `(0, 0, 0, 0, 0, 0, 0)` | `0` |


## ORACLE-089 — Accepted structural record declarations

**Classification:** `LOCAL_CONTRACT_FIXTURE`. **Coverage:** ST1--ST2.

Expression vocabulary for this and the rejection tables: Z means the exact record
BranchOracleStats(0,0,0,0,0,0,0); S means BranchOracleStats(1,1,1,7,2,9,11).
Q1_instance is the normally constructed canonical INPUTS Q1, Q1_context its exact
BranchOracleContext. R means BranchOracleResult. IntSub, TupleSub, StatsSub, ResultSub,
and ContextSub are test-local ordinary subclasses of int, tuple, BranchOracleStats,
BranchOracleResult, and BranchOracleContext respectively. No object bypasses its constructor.
Hostile is a test-local object whose conversion, comparison, arithmetic, iteration and
attribute-probing methods raise sentinels if invoked; exact-type rejection must precede them.
Fraction and ExactValue are TEST-SIDE values, not permitted production imports.

Both new records must be frozen, slotted, hashable with structural equality, no ordering
and no defaults. Field order and signatures remain DESIGN 4.10.2. Store a passed root
verbatim; do not infer a numerical ordering or a reduced representative from record equality.
Standalone StandardBranchStats does not enforce successful-run equations. Existing-field
mutation raises the normal frozen-dataclass exception without changing the record; no
new guarantee about adding nonexistent slotted attributes is imposed.

These are prospective declaration oracles, not evidence that an absent constructor has run.

### Fixture table: U13_VALID_RECORDS

| target | args_expression | meaning |
| --- | --- | --- |
| `'BranchResult'` | `'((1,1),1)'` | `'positive root'` |
| `'BranchResult'` | `'((-4,4),1)'` | `'signed unreduced root'` |
| `'BranchResult'` | `'((0,7),2)'` | `'zero keeps denominator'` |
| `'BranchResult'` | `'((4,4),1)'` | `'not equal as record to ((2,2),1)'` |
| `'BranchResult'` | `'((2,2),1)'` | `'equal quotient but distinct raw record'` |
| `'BranchResult'` | `'((1,1),1<<130)'` | `'no instance-aware upper shore bound'` |
| `'StandardBranchStats'` | `'(0,0,0,Z)'` | `'all zero standalone'` |
| `'StandardBranchStats'` | `'(9,0,99,Z)'` | `'no inter-field execution equations in constructor'` |
| `'StandardBranchStats'` | `'(3,2,1,S)'` | `'retain supplied exact immutable oracle stats'` |


## ORACLE-090 — Exact public rejections, validation precedence and Python arity

**Classification:** `NEGATIVE` / `LOCAL_CONTRACT_FIXTURE`. **Coverage:** ST1--ST3.

Each expression is the POSITIONAL ARGUMENT TUPLE for its target, not executable production
code. A consuming test creates the vocabulary objects locally. Every ValueError means
exact built-in ValueError, not merely a matching superclass; TypeError is ordinary wrong
positional arity. No exception-message prose is part of the contract. BranchResult checks
root before shore. StandardBranchStats checks counters 0,1,2 before exact oracle_stats.
The solve validates exact context, then exact branch, before graph/family/optimizer work,
even on Q1's empty domains. Combine two bad inputs to verify the first guard by local
sentinels/source inspection, not by comparing unstable error strings. Frozen mutation
is distinct from public-data rejection.

No row requires constructor-bypassing forged state, coercion, silently repaired data,
new API overloads, or edits to any closed constructor. ExactValue(-1,1) is a VALID closed
record, and is rejected as a root because it is not a RawPair, not because its N is negative.

### Fixture table: U13_REJECTIONS

| id | target | args_expression | exception | first_guard |
| --- | --- | --- | --- | --- |
| `'RJ001'` | `'BranchResult'` | `'(None,1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ002'` | `'BranchResult'` | `'(True,1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ003'` | `'BranchResult'` | `'(1,1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ004'` | `'BranchResult'` | `'(1.0,1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ005'` | `'BranchResult'` | `"('1',1)"` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ006'` | `'BranchResult'` | `'([1,1],1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ007'` | `'BranchResult'` | `'(iter((1,1)),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ008'` | `'BranchResult'` | `'(TupleSub((1,1)),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ009'` | `'BranchResult'` | `'(ExactValue(1,1),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ010'` | `'BranchResult'` | `'(ExactValue(-1,1),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ011'` | `'BranchResult'` | `'(Fraction(1,1),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ012'` | `'BranchResult'` | `'((),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ013'` | `'BranchResult'` | `'((1,),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ014'` | `'BranchResult'` | `'((1,1,1),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ015'` | `'BranchResult'` | `'((True,1),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ016'` | `'BranchResult'` | `'((IntSub(1),1),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ017'` | `'BranchResult'` | `'((1.0,1),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ018'` | `'BranchResult'` | `"(('1',1),1)"` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ019'` | `'BranchResult'` | `'((1,True),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ020'` | `'BranchResult'` | `'((1,IntSub(1)),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ021'` | `'BranchResult'` | `'((1,1.0),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ022'` | `'BranchResult'` | `"((1,'1'),1)"` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ023'` | `'BranchResult'` | `'((1,0),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ024'` | `'BranchResult'` | `'((1,-1),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ025'` | `'BranchResult'` | `'((0,0),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ026'` | `'BranchResult'` | `'((-1,-1),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ027'` | `'BranchResult'` | `'(Hostile(),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ028'` | `'BranchResult'` | `'((Hostile(),1),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ029'` | `'BranchResult'` | `'((1,Hostile()),1)'` | `'ValueError'` | `'root: closed validate_pair before shore'` |
| `'RJ030'` | `'BranchResult'` | `'((1,1),0)'` | `'ValueError'` | `'shore: exact built-in int > 0'` |
| `'RJ031'` | `'BranchResult'` | `'((1,1),-1)'` | `'ValueError'` | `'shore: exact built-in int > 0'` |
| `'RJ032'` | `'BranchResult'` | `'((1,1),True)'` | `'ValueError'` | `'shore: exact built-in int > 0'` |
| `'RJ033'` | `'BranchResult'` | `'((1,1),1.0)'` | `'ValueError'` | `'shore: exact built-in int > 0'` |
| `'RJ034'` | `'BranchResult'` | `'((1,1),IntSub(1))'` | `'ValueError'` | `'shore: exact built-in int > 0'` |
| `'RJ035'` | `'BranchResult'` | `'((1,1),None)'` | `'ValueError'` | `'shore: exact built-in int > 0'` |
| `'RJ036'` | `'BranchResult'` | `"((1,1),'1')"` | `'ValueError'` | `'shore: exact built-in int > 0'` |
| `'RJ037'` | `'BranchResult'` | `'((1,1),Fraction(1,1))'` | `'ValueError'` | `'shore: exact built-in int > 0'` |
| `'RJ038'` | `'BranchResult'` | `'((1,1),Hostile())'` | `'ValueError'` | `'shore: exact built-in int > 0'` |
| `'RJ039'` | `'StandardBranchStats'` | `'(-1,0,0,Z)'` | `'ValueError'` | `'counter 0: exact built-in nonnegative int'` |
| `'RJ040'` | `'StandardBranchStats'` | `'(True,0,0,Z)'` | `'ValueError'` | `'counter 0: exact built-in nonnegative int'` |
| `'RJ041'` | `'StandardBranchStats'` | `'(1.0,0,0,Z)'` | `'ValueError'` | `'counter 0: exact built-in nonnegative int'` |
| `'RJ042'` | `'StandardBranchStats'` | `'(IntSub(1),0,0,Z)'` | `'ValueError'` | `'counter 0: exact built-in nonnegative int'` |
| `'RJ043'` | `'StandardBranchStats'` | `'(None,0,0,Z)'` | `'ValueError'` | `'counter 0: exact built-in nonnegative int'` |
| `'RJ044'` | `'StandardBranchStats'` | `"('1',0,0,Z)"` | `'ValueError'` | `'counter 0: exact built-in nonnegative int'` |
| `'RJ045'` | `'StandardBranchStats'` | `'(Fraction(1,1),0,0,Z)'` | `'ValueError'` | `'counter 0: exact built-in nonnegative int'` |
| `'RJ046'` | `'StandardBranchStats'` | `'(Hostile(),0,0,Z)'` | `'ValueError'` | `'counter 0: exact built-in nonnegative int'` |
| `'RJ047'` | `'StandardBranchStats'` | `'(0,-1,0,Z)'` | `'ValueError'` | `'counter 1: exact built-in nonnegative int'` |
| `'RJ048'` | `'StandardBranchStats'` | `'(0,True,0,Z)'` | `'ValueError'` | `'counter 1: exact built-in nonnegative int'` |
| `'RJ049'` | `'StandardBranchStats'` | `'(0,1.0,0,Z)'` | `'ValueError'` | `'counter 1: exact built-in nonnegative int'` |
| `'RJ050'` | `'StandardBranchStats'` | `'(0,IntSub(1),0,Z)'` | `'ValueError'` | `'counter 1: exact built-in nonnegative int'` |
| `'RJ051'` | `'StandardBranchStats'` | `'(0,None,0,Z)'` | `'ValueError'` | `'counter 1: exact built-in nonnegative int'` |
| `'RJ052'` | `'StandardBranchStats'` | `"(0,'1',0,Z)"` | `'ValueError'` | `'counter 1: exact built-in nonnegative int'` |
| `'RJ053'` | `'StandardBranchStats'` | `'(0,Fraction(1,1),0,Z)'` | `'ValueError'` | `'counter 1: exact built-in nonnegative int'` |
| `'RJ054'` | `'StandardBranchStats'` | `'(0,Hostile(),0,Z)'` | `'ValueError'` | `'counter 1: exact built-in nonnegative int'` |
| `'RJ055'` | `'StandardBranchStats'` | `'(0,0,-1,Z)'` | `'ValueError'` | `'counter 2: exact built-in nonnegative int'` |
| `'RJ056'` | `'StandardBranchStats'` | `'(0,0,True,Z)'` | `'ValueError'` | `'counter 2: exact built-in nonnegative int'` |
| `'RJ057'` | `'StandardBranchStats'` | `'(0,0,1.0,Z)'` | `'ValueError'` | `'counter 2: exact built-in nonnegative int'` |
| `'RJ058'` | `'StandardBranchStats'` | `'(0,0,IntSub(1),Z)'` | `'ValueError'` | `'counter 2: exact built-in nonnegative int'` |
| `'RJ059'` | `'StandardBranchStats'` | `'(0,0,None,Z)'` | `'ValueError'` | `'counter 2: exact built-in nonnegative int'` |
| `'RJ060'` | `'StandardBranchStats'` | `"(0,0,'1',Z)"` | `'ValueError'` | `'counter 2: exact built-in nonnegative int'` |
| `'RJ061'` | `'StandardBranchStats'` | `'(0,0,Fraction(1,1),Z)'` | `'ValueError'` | `'counter 2: exact built-in nonnegative int'` |
| `'RJ062'` | `'StandardBranchStats'` | `'(0,0,Hostile(),Z)'` | `'ValueError'` | `'counter 2: exact built-in nonnegative int'` |
| `'RJ063'` | `'StandardBranchStats'` | `'(0,0,0,None)'` | `'ValueError'` | `'oracle_stats: exact BranchOracleStats'` |
| `'RJ064'` | `'StandardBranchStats'` | `'(0,0,0,(0,)*7)'` | `'ValueError'` | `'oracle_stats: exact BranchOracleStats'` |
| `'RJ065'` | `'StandardBranchStats'` | `'(0,0,0,[0]*7)'` | `'ValueError'` | `'oracle_stats: exact BranchOracleStats'` |
| `'RJ066'` | `'StandardBranchStats'` | `'(0,0,0,{})'` | `'ValueError'` | `'oracle_stats: exact BranchOracleStats'` |
| `'RJ067'` | `'StandardBranchStats'` | `'(0,0,0,StatsSub(0,0,0,0,0,0,0))'` | `'ValueError'` | `'oracle_stats: exact BranchOracleStats'` |
| `'RJ068'` | `'StandardBranchStats'` | `'(0,0,0,Hostile())'` | `'ValueError'` | `'oracle_stats: exact BranchOracleStats'` |
| `'RJ069'` | `'solve_branch_standard'` | `'(None,0)'` | `'ValueError'` | `'context exact type; no optimizer call'` |
| `'RJ070'` | `'solve_branch_standard'` | `'(0,0)'` | `'ValueError'` | `'context exact type; no optimizer call'` |
| `'RJ071'` | `'solve_branch_standard'` | `'(True,0)'` | `'ValueError'` | `'context exact type; no optimizer call'` |
| `'RJ072'` | `'solve_branch_standard'` | `'(Q1_instance,0)'` | `'ValueError'` | `'context exact type; no optimizer call'` |
| `'RJ073'` | `'solve_branch_standard'` | `'({},0)'` | `'ValueError'` | `'context exact type; no optimizer call'` |
| `'RJ074'` | `'solve_branch_standard'` | `'(ContextSub(Q1_instance),0)'` | `'ValueError'` | `'context exact type; no optimizer call'` |
| `'RJ075'` | `'solve_branch_standard'` | `'(Hostile(),0)'` | `'ValueError'` | `'context exact type; no optimizer call'` |
| `'RJ076'` | `'solve_branch_standard'` | `'(Q1_context,-1)'` | `'ValueError'` | `'branch exact int in (0,1,2,3); no optimizer call'` |
| `'RJ077'` | `'solve_branch_standard'` | `'(Q1_context,4)'` | `'ValueError'` | `'branch exact int in (0,1,2,3); no optimizer call'` |
| `'RJ078'` | `'solve_branch_standard'` | `'(Q1_context,True)'` | `'ValueError'` | `'branch exact int in (0,1,2,3); no optimizer call'` |
| `'RJ079'` | `'solve_branch_standard'` | `'(Q1_context,0.0)'` | `'ValueError'` | `'branch exact int in (0,1,2,3); no optimizer call'` |
| `'RJ080'` | `'solve_branch_standard'` | `'(Q1_context,IntSub(0))'` | `'ValueError'` | `'branch exact int in (0,1,2,3); no optimizer call'` |
| `'RJ081'` | `'solve_branch_standard'` | `'(Q1_context,None)'` | `'ValueError'` | `'branch exact int in (0,1,2,3); no optimizer call'` |
| `'RJ082'` | `'solve_branch_standard'` | `"(Q1_context,'0')"` | `'ValueError'` | `'branch exact int in (0,1,2,3); no optimizer call'` |
| `'RJ083'` | `'solve_branch_standard'` | `'(Q1_context,Fraction(0,1))'` | `'ValueError'` | `'branch exact int in (0,1,2,3); no optimizer call'` |
| `'RJ084'` | `'solve_branch_standard'` | `'(Q1_context,Hostile())'` | `'ValueError'` | `'branch exact int in (0,1,2,3); no optimizer call'` |
| `'RJ085'` | `'BranchResult'` | `'()'` | `'TypeError'` | `'wrong positional arity retains Python behavior'` |
| `'RJ086'` | `'BranchResult'` | `'((1,1),)'` | `'TypeError'` | `'wrong positional arity retains Python behavior'` |
| `'RJ087'` | `'BranchResult'` | `'((1,1),1,0)'` | `'TypeError'` | `'wrong positional arity retains Python behavior'` |
| `'RJ088'` | `'StandardBranchStats'` | `'(0,0,0)'` | `'TypeError'` | `'wrong positional arity retains Python behavior'` |
| `'RJ089'` | `'StandardBranchStats'` | `'(0,0,0,Z,0)'` | `'TypeError'` | `'wrong positional arity retains Python behavior'` |
| `'RJ090'` | `'solve_branch_standard'` | `'()'` | `'TypeError'` | `'wrong positional arity retains Python behavior'` |
| `'RJ091'` | `'solve_branch_standard'` | `'(Q1_context,)'` | `'TypeError'` | `'wrong positional arity retains Python behavior'` |
| `'RJ092'` | `'solve_branch_standard'` | `'(Q1_context,0,0)'` | `'TypeError'` | `'wrong positional arity retains Python behavior'` |


## ORACLE-091 — Consumed-response faults and guard-isolated internal failures

**Classification:** `NEGATIVE` / `LOCAL_CONTRACT_FIXTURE`. **Coverage:** ST11--ST12.

Use the legal DOUBLE-j0 stream as the baseline. Its parameters are seed (0,1),
K=(4,2), terminal=(2,2); normally R(1,2,2,raw) is returned. Replace only the named
boundary in each row, retaining correct preceding replies and supported record constructors.
Wrong tuple/result/stat shapes, shore 4 in an n=2 universe, and residual-binding failures
must raise RuntimeError before they authorize any result or update. The source/domain
correctness of normally returned Unit 12 records is still owned by that closed oracle;
these are adversarial substitutions, not claims that the real oracle returns these values.

F13--F15 deliberately use source-invalid but shape-valid returned terms with arithmetically
CONSISTENT raw residuals, to isolate forbidden signs rather than fail earlier binding checks.
F11 and F16 intentionally violate binding. F17--F18 substitute compare_pairs' returned
comparison with 0/+1 on the first negative reset; all mathematical replies stay legal.
With accurate scalar helpers and a correctly bound negative raw, a genuinely nondecreasing
fresh c/h is algebraically impossible. These two probes exercise the explicit defensive
progress guard; they do NOT assert an impossible source-domain fixture exists.

No failure returns a partial mathematical result or completed statistics. A later None
is an internal error; seed None is ordinary branch infeasibility. Seed residual zero or
positive is legal and must not trigger the loop's sign checks.

### Fixture table: U13_INTERNAL_FAILURES

| id | replace_at | replacement_expression | exception | isolated_violation |
| --- | --- | --- | --- | --- |
| `'F01'` | `'seed'` | `'[R(1,2,2,2),Z]'` | `'RuntimeError'` | `'response is not exact tuple'` |
| `'F02'` | `'seed'` | `'()'` | `'RuntimeError'` | `'response tuple arity 0'` |
| `'F03'` | `'seed'` | `'(R(1,2,2,2),)'` | `'RuntimeError'` | `'response tuple arity 1'` |
| `'F04'` | `'seed'` | `'(R(1,2,2,2),Z,0)'` | `'RuntimeError'` | `'response tuple arity 3'` |
| `'F05'` | `'seed'` | `'TupleSub((R(1,2,2,2),Z))'` | `'RuntimeError'` | `'tuple subclass'` |
| `'F06'` | `'seed'` | `'(0,Z)'` | `'RuntimeError'` | `'wrong result exact type'` |
| `'F07'` | `'seed'` | `'(ResultSub(1,2,2,2),Z)'` | `'RuntimeError'` | `'result subclass'` |
| `'F08'` | `'seed'` | `'(R(1,2,2,2),None)'` | `'RuntimeError'` | `'wrong stats exact type'` |
| `'F09'` | `'seed'` | `'(R(1,2,2,2),StatsSub(0,0,0,0,0,0,0))'` | `'RuntimeError'` | `'stats subclass'` |
| `'F10'` | `'seed'` | `'(R(4,2,2,2),Z)'` | `'RuntimeError'` | `'positive shore 4 outside n=2 universe'` |
| `'F11'` | `'seed'` | `'(R(1,2,2,3),Z)'` | `'RuntimeError'` | `'bound raw should equal 2, not 3'` |
| `'F12'` | `'K'` | `'(None,Z)'` | `'RuntimeError'` | `'infeasible result after feasible seed'` |
| `'F13'` | `'K'` | `'(R(1,4,2,0),Z)'` | `'RuntimeError'` | `'internally bound zero violates strict-negative K'` |
| `'F14'` | `'K'` | `'(R(1,5,2,2),Z)'` | `'RuntimeError'` | `'internally bound positive violates strict-negative K'` |
| `'F15'` | `'terminal'` | `'(R(1,3,2,2),Z)'` | `'RuntimeError'` | `'internally bound positive later loop residual'` |
| `'F16'` | `'terminal'` | `'(R(1,2,2,1),Z)'` | `'RuntimeError'` | `'terminal raw binding mismatch'` |
| `'F17'` | `'K'` | `'normal reply; compare_pairs substituted to return 0'` | `'RuntimeError'` | `'explicit nondecreasing-progress guard'` |
| `'F18'` | `'K'` | `'normal reply; compare_pairs substituted to return 1'` | `'RuntimeError'` | `'explicit nondecreasing-progress guard'` |


## ORACLE-092 — Dependency exceptions, reuse and label independence

**Classification:** `LOCAL_CONTRACT_FIXTURE`. **Coverage:** ST3, ST13, ST15--ST16.

At each EXCEPTIONS boundary substitute a dependency that raises a particular sentinel
exception instance. The SAME instance propagates unchanged; no generic ValueError,
RuntimeError translation, None, partial result, or fallback solver is allowed. These
are exceptions RAISED by dependencies, distinct from the normally returned malformed
data explicitly checked by ORACLE-091. Patches are test-local module binding substitutions
and are restored; closed module files and expected deterministic policies are never edited.

The REUSE sequence shares one exact RICH context. Mathematical records, raw query
parameters and per-solve counts reproduce their isolated SOLVES/TRACES rows. Direct
queries do not carry a cached parameter, incumbent, or aggregate into a later solve.
Instance and every family tuple remain unchanged; preparation occurs once before solves,
not once per solve/query. LABELS changes only metadata and must not alter any result,
query trace or real repeated-run diagnostic record. No speculative clock/timing equality.

Require exactly the DESIGN 4.10 public surface and direct-import whitelist. Package root
remains export-free. Flow/family modules may be imported TRANSITIVELY by the closed
oracle; their presence in sys.modules does not by itself violate the DIRECT-import rule.
Expected data must not be loaded from private files by tests or production.

### Fixture table: U13_EXCEPTIONS

| id | dependency | boundary |
| --- | --- | --- |
| `'X01'` | `'exact_branch_min'` | `'seed'` |
| `'X02'` | `'exact_branch_min'` | `'K'` |
| `'X03'` | `'exact_branch_min'` | `'terminal'` |
| `'X04'` | `'residual_numerator'` | `'seed binding'` |
| `'X05'` | `'make_pair'` | `'initial seed pair'` |
| `'X06'` | `'pair_add_one'` | `'initial K'` |
| `'X07'` | `'make_pair'` | `'first negative reset'` |
| `'X08'` | `'compare_pairs'` | `'first negative reset'` |
| `'X09'` | `'validate_pair'` | `'BranchResult construction'` |


### Fixture table: U13_REUSE

| index | operation | expected_reference |
| --- | --- | --- |
| `0` | `'solve RICH branch 0'` | `'RICH-j0'` |
| `1` | `'direct RICH branch 1 query at (0,1)'` | `'first row of RICH-j1'` |
| `2` | `'solve RICH branch 3'` | `'RICH-j3'` |
| `3` | `'solve RICH branch 0'` | `'RICH-j0'` |
| `4` | `'solve RICH branch 2'` | `'RICH-j2'` |
| `5` | `'solve RICH branch 1'` | `'RICH-j1'` |


### Fixture table: U13_LABELS

| input | labels |
| --- | --- |
| `'RICH'` | `('zeta', 'alpha', 'middle', 'omega', 'beta')` |
| `'RICH'` | `(90, -7, 400, 2, 0)` |
| `'LOW0'` | `('v3', 'v2', 'v1', 'v0')` |


## ORACLE-093 — Exhaustive tiny Standard corpus and arbitrary-choice census

**Classification:** `BRANCH_ORACLE` / `LOCAL_CONTRACT_FIXTURE`.
**Coverage:** ST4, ST6--ST10, ST14, ST17--ST19 (future implementation audit basis).

Use the SAME input-generation definition as ORACLE-079, without changing its historical
fixed-parameter expectations: n=2 then n=3; unordered pairs lexicographically; multiplicities
in {0,1,2} in product order with zeros omitted; discard isolated-vertex patterns; enumerate
f(v) in 1..d_q(v) in product order. There are 5+324=329 active inputs. Serial starts at 0.
For each visit branches 0,1,2,3. Instead of ten fixed parameters, derive one complete shipped
Standard trace from literal zero seed, K, fresh source resets and exact-zero termination.

The 1,316 branch solves include 1,137 feasible and 179 infeasible cases. The shipped
reference has 3,635 optimizer invocations, 2,319 loop invocations and 1,182 updates.
The expected 42,302 ordinary calls are structural predictions for that future trace,
NOT observed production branch calls or new collected pytest cases. This corpus has
no zero roots; ZERO-j2 and the separate large Z family supply that required boundary.
Of the 179 infeasible solves, 24 have zero descriptors and 155 have all-empty nonzero
cover tuples. The explicit census also includes full-shore returns and raw terminal ties.

Independently traverse EVERY legal residual argmin choice at the seed, each loop step,
and at termination, in increasing original-mask enumeration order. The resulting finite
choice tree has 5,374 complete paths, including one trivial path for each infeasible
solve. Fifty-four solves admit differing legal path lengths. No preferred h is imposed.
The candidate-ratio strict-decrease proof, not an arbitrary numerical cap, justifies
termination of this private enumeration. An exponential private oracle is not a production
complexity claim. All finite counts are overlapping views, not disjoint experiment samples.

The fingerprint encodings use exact compact JSON followed by LF per row. Default rows
are defined in the table; each query row is
(parameter,U,source_pair,raw,all_argmins,retained_family,retained_GR_pair).
An all-choice path is a tuple of (parameter,U) entries, including seed and terminal.
Private JSON array encoding and Python tuple values have the same documented JSON stream;
this fingerprint is not a change from structural tuple semantics in production.

### Fixture table: U13_CORPUS_COUNTS

| metric | value |
| --- | --- |
| `'all_empty_infeasible'` | `155` |
| `'all_legal_paths'` | `5374` |
| `'domain_memberships'` | `3354` |
| `'family_examinations'` | `17704` |
| `'feasible_family_calls'` | `10374` |
| `'feasible_solves'` | `1137` |
| `'full_shore_returns'` | `219` |
| `'infeasible_solves'` | `179` |
| `'instances'` | `329` |
| `'n2_instances'` | `5` |
| `'n3_instances'` | `324` |
| `'negative_roots'` | `629` |
| `'newton_updates'` | `1182` |
| `'oracle_calls'` | `3635` |
| `'outer_iterations'` | `2319` |
| `'positive_roots'` | `508` |
| `'solves'` | `1316` |
| `'specified_ordinary_calls'` | `42302` |
| `'terminal_pair_distinctions'` | `116` |
| `'updates_1'` | `1092` |
| `'updates_2'` | `45` |
| `'variable_path_length_solves'` | `54` |
| `'zero_descriptor_infeasible'` | `24` |


### Fixture table: U13_CORPUS_BY_BRANCH

| j | counts |
| --- | --- |
| `0` | `{'all_empty_infeasible': 68, 'all_legal_paths': 2128, 'domain_memberships': 1038, 'family_examinations': 851, 'feasible_family_calls': 783, 'feasible_solves': 261, 'full_shore_returns': 67, 'infeasible_solves': 68, 'newton_updates': 261, 'oracle_calls': 851, 'outer_iterations': 522, 'positive_roots': 261, 'solves': 329, 'specified_ordinary_calls': 10125, 'terminal_pair_distinctions': 23, 'updates_1': 261}` |
| `1` | `{'all_empty_infeasible': 60, 'all_legal_paths': 1243, 'domain_memberships': 567, 'family_examinations': 9620, 'feasible_family_calls': 3708, 'feasible_solves': 247, 'infeasible_solves': 82, 'newton_updates': 247, 'oracle_calls': 823, 'outer_iterations': 494, 'positive_roots': 247, 'solves': 329, 'specified_ordinary_calls': 8028, 'terminal_pair_distinctions': 19, 'updates_1': 247, 'zero_descriptor_infeasible': 22}` |
| `2` | `{'all_empty_infeasible': 25, 'all_legal_paths': 719, 'domain_memberships': 839, 'family_examinations': 1801, 'feasible_family_calls': 1727, 'feasible_solves': 302, 'full_shore_returns': 152, 'infeasible_solves': 27, 'negative_roots': 302, 'newton_updates': 327, 'oracle_calls': 958, 'outer_iterations': 629, 'solves': 329, 'specified_ordinary_calls': 11705, 'terminal_pair_distinctions': 14, 'updates_1': 277, 'updates_2': 25, 'variable_path_length_solves': 30, 'zero_descriptor_infeasible': 2}` |
| `3` | `{'all_empty_infeasible': 2, 'all_legal_paths': 1284, 'domain_memberships': 910, 'family_examinations': 5432, 'feasible_family_calls': 4156, 'feasible_solves': 327, 'infeasible_solves': 2, 'negative_roots': 327, 'newton_updates': 347, 'oracle_calls': 1003, 'outer_iterations': 674, 'solves': 329, 'specified_ordinary_calls': 12444, 'terminal_pair_distinctions': 60, 'updates_1': 307, 'updates_2': 20, 'variable_path_length_solves': 24}` |


### Fixture table: U13_CORPUS_FINGERPRINTS

| stream | encoding | sha256 |
| --- | --- | --- |
| `'default'` | `'compact JSON [serial,n,edges,f,j,members,comparison_pair,optimizers,rows,root,U,counts,structural_counts] plus LF'` | `'a3dc3671383fbcc55c463ad5c791325a60ddca3124a741cebbd9dcd738c8abd4'` |
| `'any-argmin'` | `'compact JSON [serial,j,all_paths] plus LF'` | `'22b204da65bf0f8642115b33b49c53ce2f3a078e22bb5d9f8485c530cf7e815b'` |


## ORACLE-094 — Symbolic magnitude families, signed/zero roots and exact reset carriers

**Classification:** `BRANCH_ORACLE` / `LOCAL_CONTRACT_FIXTURE`.
**Coverage:** ST5, ST8--ST9, ST17--ST18.

For each family and k in (1,2,7,31,127,1024,4096), instantiate the exact expressions in
LARGE_SYMBOLS. All inputs are active and have constant support. Every chosen focus branch
has one negative update and three calls, including seed and terminal, for all k>=1.

L: q=2^k is even, f=(1,1). Its D0 consists of two singleton shores, both (c,h)=(q,q).
N: q=2^k is even, f=(q,q). Its D3 consists of two singleton shores, both (-2,q).
Z: q=2^k+1 is odd, f=(q,q). Its D2 consists of two singleton shores, both (0,q-1).
NEG: a triangle with every edge multiplicity q=2^k and f=(1,1,1). D2 has just the full
shore U=7, with (c,h)=(-6q,2). These facts derive from the literal domain predicates and
source sums; no unit-copy enumeration is needed. Shipped singleton choice is U=1 under
source order; NEG's focus shore is uniquely U=7. K is always exactly (c+h,h).

The finite sweep checks all FOUR branches of every family, not only the focus branch:
112 branch solves, 49 feasible and 63 infeasible, 210 query invocations. Each LARGE_SWEEP
block hash covers four rows (family,k,j,query_rows,root,U,counts,structural_counts) in j order.
The symbolic focus formulas govern every k>=1 by the preceding derivation, whereas the
recorded bit maxima/fingerprints concern only the declared finite k values.

Let Q=sum(q_e), C=3Q+2, H=2Q+1. For every submitted Standard pair (A,B),
abs(A)<=C+H=5Q+3 and 1<=B<=H; after a negative reset abs(A)<=C. For every source-domain
shore, abs(c)<=C, 1<=h<=H and
abs(B*c-A*h)<=B*C+abs(A)*H<=H*(2*C+H)=(2Q+1)*(8Q+5).
Both routes check these inequalities on every actual parameter and every domain shore.
They also check the EXACT integer-scaled WYZ change of variables: with K=(c0+h0)/h0,
aI(U)=(c0+h0)*h(U)-h0*c(U), bI(U)=h0*h(U), delta=K-lambda,
aI-delta*bI=-h0*(c-lambda*h), bI>0, and aI(U0)=h0^2>0.

No production magnitude cutoff, denominator-product accumulation, full peak_integer_bits
instrumentation, wall-time assertion, or universal strong-polynomiality proof is inferred.
The family-specific constant oracle-call count follows from the explicit path. No flatness
claim is made for every flow counter or arbitrary constant-support magnitude change.

### Fixture table: U13_LARGE_SYMBOLS

| family | q | n | edges | f | focus_branch | root | terminal_U | parameters | counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `'L'` | `'2**k'` | `2` | `'((0,1,q),)'` | `'(1,1)'` | `0` | `'(q,q)'` | `1` | `'((0,1),(2*q,q),(q,q))'` | `(3, 2, 1)` |
| `'N'` | `'2**k'` | `2` | `'((0,1,q),)'` | `'(q,q)'` | `3` | `'(-2,q)'` | `1` | `'((0,1),(q-2,q),(-2,q))'` | `(3, 2, 1)` |
| `'Z'` | `'2**k+1'` | `2` | `'((0,1,q),)'` | `'(q,q)'` | `2` | `'(0,q-1)'` | `1` | `'((0,1),(q-1,q-1),(0,q-1))'` | `(3, 2, 1)` |
| `'NEG'` | `'2**k'` | `3` | `'((0,1,q),(0,2,q),(1,2,q))'` | `'(1,1,1)'` | `2` | `'(-6*q,2)'` | `7` | `'((0,1),(-6*q+2,2),(-6*q,2))'` | `(3, 2, 1)` |


### Fixture table: U13_LARGE_SWEEP

| family | k | four_branch_counts | peak_parameter_entry_bits | block_sha256 |
| --- | --- | --- | --- | --- |
| `'L'` | `1` | `((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0))` | `3` | `'282784ebb7cf3bfb07035ecaa8e1d9c15170fe21f44597090d3f4f20828d3161'` |
| `'L'` | `2` | `((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0))` | `4` | `'4f5dd450b1a7a63ef48d3a67538ed2ca68ffe9b8a24f44b1ff6527bb90e8213a'` |
| `'L'` | `7` | `((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0))` | `9` | `'c85cfb49ac82381d16aae5c162521b7ec8203a3fa2f8135b373c451b497aa945'` |
| `'L'` | `31` | `((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0))` | `33` | `'1e9cabd52acf6b4b3f5957ac405b538988c40803dfffb416241e3b0f0c2ffda6'` |
| `'L'` | `127` | `((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0))` | `129` | `'a972293ea791dd247a0f53399a6b1dec86108b4e3dd4ef191cac38870bcb70f8'` |
| `'L'` | `1024` | `((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0))` | `1026` | `'38cbaf79fc70728f3de9bae5f5a8437c77b6266f12f08071b8aacbcbeafde644'` |
| `'L'` | `4096` | `((3, 2, 1), (1, 0, 0), (1, 0, 0), (1, 0, 0))` | `4098` | `'009a920679c036da483a2a96472dfcb8c43f58d53f14da399bbfbd3e1a01c401'` |
| `'N'` | `1` | `((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1))` | `2` | `'89ebb92a02fe98a6ac30b7e4f7db805d070dc0aba5844f80283024076757c7c4'` |
| `'N'` | `2` | `((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1))` | `3` | `'8ad13174640e7841abff45cf928a71fdc221bef33fa28d403025e5e7c31a6763'` |
| `'N'` | `7` | `((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1))` | `8` | `'6f7ca6a04f0c998282a359bfc45630edd65d25a74c4a768b523e17ffbaf47c28'` |
| `'N'` | `31` | `((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1))` | `32` | `'1ecb6171c543b6b8e460fe67f6e88074739c540130a1d2461e49b0e93c90dda9'` |
| `'N'` | `127` | `((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1))` | `128` | `'5889542364c12016b1655a48fe3492a220a9c1f9ec85c84b441d92a1ca51d623'` |
| `'N'` | `1024` | `((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1))` | `1025` | `'13961c991941e6f267e4b339977b5e9bf2146b44d466cc5d88c4c43296ffefdd'` |
| `'N'` | `4096` | `((1, 0, 0), (1, 0, 0), (1, 0, 0), (3, 2, 1))` | `4097` | `'d2248dac4b1fc2abf39c0c9524b5283031695664fc4fd9f5fbf9017fc3a72fd4'` |
| `'Z'` | `1` | `((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0))` | `2` | `'ec74180ea28187a0da218a92ce6dd8787e398759d3495ec6538567966c6742ae'` |
| `'Z'` | `2` | `((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0))` | `3` | `'bc06c4b4afc06ee8e711558f8cfcb75c762458fc33784c844ffece7f91ce7a81'` |
| `'Z'` | `7` | `((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0))` | `8` | `'3cf10dbb48cde2e1c237962b53d07fe3729549d08f06f7230f94af072541288a'` |
| `'Z'` | `31` | `((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0))` | `32` | `'fb8256e8eaa8446920933d85e44ac9cb7c201c0f4fa732ef0966fd9a299a38dd'` |
| `'Z'` | `127` | `((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0))` | `128` | `'7e6f5a81bd489f3ce9101c7b5ab22ca89b7642b4c13f4385a28205ea58130351'` |
| `'Z'` | `1024` | `((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0))` | `1025` | `'69a3b1df01ba74ecb9cc8843d168645eccdade2fd80ebf80228590e4dd8c5e0b'` |
| `'Z'` | `4096` | `((1, 0, 0), (1, 0, 0), (3, 2, 1), (1, 0, 0))` | `4097` | `'2cb108b2b829072fac890134655c903430fef8617b4325c8b401d65ff79d2b8b'` |
| `'NEG'` | `1` | `((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1))` | `4` | `'54548b453ecd35d0fb09e98e87dc24489f5a49e0dd4ef853f75e9526e1ed14e1'` |
| `'NEG'` | `2` | `((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1))` | `5` | `'eea1c56c4e7387927b42249cb6d055f3c213fc3adb9da85b8cb0af6e4c894da1'` |
| `'NEG'` | `7` | `((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1))` | `10` | `'226a262c0852065dc84c91516a11ace9dcfcd5f22eb7ae5a7937453ae8cf1ca5'` |
| `'NEG'` | `31` | `((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1))` | `34` | `'fd4197d5af27a5cbf779eb5788e4b85ae548f590327a72608ac2c282e6203c6d'` |
| `'NEG'` | `127` | `((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1))` | `130` | `'d49a9eb67f7029e4538dcf84b2e162c2aeff943debc5d69f6abe3565f01cef78'` |
| `'NEG'` | `1024` | `((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1))` | `1027` | `'d4c203c6ab6aa4400e644dc91384d94c6d18b4941179fa3120477168845a5c20'` |
| `'NEG'` | `4096` | `((3, 2, 1), (3, 2, 1), (3, 2, 1), (3, 2, 1))` | `4099` | `'28af42e213057470abfb0e5ade059a8b7e47ef8d3246c9795062f674addeb9c7'` |


### Fixture table: U13_LARGE_COUNTS

| metric | value |
| --- | --- |
| `'feasible_solves'` | `49` |
| `'infeasible_solves'` | `63` |
| `'oracle_calls'` | `210` |
| `'solves'` | `112` |


### Fixture table: U13_CARRIER_COUNTS

| metric | value |
| --- | --- |
| `'residual_checks'` | `11353` |
| `'wyz_checks'` | `7634` |


## ORACLE-095 — Work, isolation and no premature complexity promotion

**Classification:** `LOCAL_CONTRACT_FIXTURE`. **Coverage:** ST16--ST20.

The source invokes thm:WYZ for t=O(M^2 log M), M=n+m+1, including constant seed overhead.
Combined with closed Unit 12, the per-solve integer-operation carrier is
O(t*(1+r_j*(n+3)^3*(m+n)^2)); preparation O(n+m+R_all) is paid separately once.
The r_j term counts all descriptors, including empty positions; it is not a flow count
and is not replaced by Q. The count formulas totalize r_j=0. Number-size control follows
the literal initialization/resets and the closed query/capacity carrier, not finite timings.

The future production wrapper retains O(1) integer records beyond prepared context and
closed oracle workspace. It must not keep an unbounded trace/cache/visited collection,
expand q copies, enumerate original shores, recurse, use float/Fraction/division/gcd,
reflect a Standard parameter, add a user budget, or terminate by diagnostic counters.
Private exhaustive references and test-side Fraction are expressly outside that production
path. No direct optimizer/backend override or public trace callback is added by these fixtures.

A later implementation audit must derive its source optima independently of consuming tests,
private expected JSON and production helpers. It may use a closed oracle only as a checked
dependency, never to manufacture expected optima. Its code-mutation controls must actually
reject faulty production variants. The present private fixture-evidence mutation controls
(if supplied in the package) are NOT that future ST19 implementation audit.

## ORACLE-096 — Coverage crosswalk and oracle-only completion boundary

**Classification:** `LOCAL_CONTRACT_FIXTURE`.

| Prospective obligation | Pre-implementation fixture basis |
| --- | --- |
| ST1: public result surface/raw structure | ORACLE-089--090; ORACLE-086 terminal-pair trap |
| ST2: separate structural statistics | ORACLE-088--090 |
| ST3: validation before graph/optimizer | ORACLE-090 and ORACLE-092 sentinel declarations |
| ST4: one mandatory seed/None | ORACLE-084--086, ORACLE-088, ORACLE-093 |
| ST5: literal Standard K | ORACLE-085--086, ORACLE-094 |
| ST6: independent original-domain minima | ORACLE-083--084, ORACLE-093--094 |
| ST7: entire ordered query sequence | ORACLE-085; independent residual/cut routes |
| ST8: strict fresh resets/exact zero | ORACLE-085--087, ORACLE-091, ORACLE-094 |
| ST9: terminal parameter and shore | ORACLE-086 EQUALITY/RICH traps |
| ST10: legal argmin freedom/default determinism | ORACLE-085--087 and all-choice census ORACLE-093 |
| ST11: checked response shape/raw binding | ORACLE-091 F01--F11/F16 |
| ST12: later None/forbidden signs | ORACLE-091 F12--F15 |
| ST13: dependency exception identity | ORACLE-092 EXCEPTIONS |
| ST14: seed/K/terminal sum/max accounting | ORACLE-085 and ORACLE-088 |
| ST15: diagnostic independence/reuse/labels | ORACLE-088 and ORACLE-092 |
| ST16: exactness/import/control-flow boundaries | ORACLE-092 and ORACLE-095; later source checks |
| ST17: literal input-sized resets/large integers | ORACLE-094 |
| ST18: source work bound vs finite counters | ORACLE-085, ORACLE-093--095 |
| ST19: independent future implementation audit | ORACLE-083--095 as prior source basis; audit still future |
| ST20: scoped conformance | DESIGN 4.10.15 / TEST_PLAN section 32; no promotion now |

Completion requires separate review, catalogue-only application left unstaged, an independent
fixture audit, unchanged 497-test regression and actual repository Ruff, followed by catalogue-only
staging, local commit and approved-hash remote closure. Only then may tests-first RED begin.
These entries do not implement Standard, Accelerated, global solve, H2, unit/witness reconstruction,
certificates, serialization, CLI, full telemetry, or experiments. They do not reopen Unit 12,
its frozen R1 tests, or the withdrawn R2 artifact. Every CONFORMANCE row/status is unchanged.
