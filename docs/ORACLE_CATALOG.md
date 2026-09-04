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
