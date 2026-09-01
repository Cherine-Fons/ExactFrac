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
