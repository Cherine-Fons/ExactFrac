# ExactFrac

ExactFrac is an exact, certificate-producing implementation of the compact
positive-integer-multiplicity modified set-pair density problem under the active
hypothesis \(f(v)\le d_q(v)\).

ExactFrac targets compact-multiplicity instances whose support graph is small enough for
exact parity-family enumeration, while permitting multiplicities with large binary
encodings. Practical support-size limits are established experimentally rather than
asserted in advance.

The solver returns the exact modified set-pair density together with a compact attaining
witness whenever the admissible family is nonempty. That exact value may also serve as a
certified fractional lower bound in applications; it is not an exact integral block
count.

## Project status

This is the private development repository.

A public release will be prepared only after the dedicated release-candidate audit
defined by the project design.

The implementation is currently being developed from a frozen mathematical
specification with independently hand-derived oracle cases and a pre-registered test
plan established before solver code.

## Mathematical model

The compact input consists of:

- a finite nonempty loopless support graph \(H=(V,S)\);
- a positive integer multiplicity \(q_e\) for each support edge;
- a positive integer capacity \(f(v)\) for each vertex;
- the active condition \(f(v)\le d_q(v)\) for every vertex.

A compact witness consists of a nonempty shore \(U\subseteq V\) and a boundary-count
vector \(y\) satisfying

\[
0\le y_e\le q_e
\]

on support edges crossing \(U\), with nonboundary coordinates zero in the dense internal
representation.

The admissibility conditions are

\[
f(U)+Y(y)\ \text{odd}
\]

and

\[
f(U)+Y(y)\ge3.
\]

The attained value is

\[
\frac{2(e_q(U)+Y(y))}
     {f(U)+Y(y)-1}.
\]

ExactFrac preserves raw witness-attaining numerator and denominator pairs in the
production solver and performs exact comparisons without floating-point tolerances.

## Verification architecture

Correctness is intentionally checked through multiple independent layers:

1. a frozen mathematical specification;
2. a proof-to-code contract;
3. hand-derived oracle cases fixed before implementation;
4. a pre-registered adversarial test plan;
5. an independent brute verifier derived directly from the compact definition;
6. the production strongly polynomial solver;
7. an independently checkable certificate verifier;
8. a theorem-obligation-to-test conformance map.

The independent verifier is structurally isolated from the production solver and imports
nothing from `exactfrac`.

## Repository structure

- `exactfrac/` — production solver package;
- `exactfrac_verify/` — independent reference verifier;
- `tests/` — regression, conformance, adversarial, and isolation tests;
- `docs/` — governing design, contract, oracle catalog, test plan, and conformance map;
- `instances/` — versioned test and benchmark instances with hashed manifest;
- `experiments/` — later reproduction and empirical-analysis scripts.

## Arithmetic and dependencies

The reference solver and independent verifier use Python's standard library only.

Production correctness paths use exact integer/rational arithmetic. Floating-point
tolerances are not used for mathematical decisions.

Development tooling is declared separately and currently includes:

- `pytest` for testing;
- `ruff` for linting and static-quality checks.

Minimum supported Python:

- Python 3.11.

Development may use newer interpreters. Release validation tests both the declared
minimum interpreter and the development interpreter.

## Determinism

Algorithmic enumeration orders are fixed and documented.

No algorithmic path relies on iteration order from a Python `set`.

Where the mathematics permits multiple correct outputs, deterministic implementation
choices are treated as reproducibility policy rather than as additional mathematical
tie-breaking requirements.

## Governing artifacts

The repository pins the frozen mathematical source by cryptographic hash rather than
committing the private source manuscript itself.

Key repository-facing control documents are:

- `docs/SPEC_LOCK.md`;
- `docs/DESIGN.md`;
- `docs/CONTRACT.md`;
- `docs/CONFORMANCE.md`;
- `docs/ORACLE_CATALOG.md`;
- `docs/TEST_PLAN.md`.

`GOVERNING_SHA256SUMS.txt` records the authenticated governing-document baseline.

## Release discipline

No public-release claim is made from the development branch merely because code runs or
tests pass.

Before public release, the project undergoes a dedicated audit including:

- privacy and repository-history review;
- secret and path scanning;
- license confirmation;
- theorem-source status review;
- README and benchmark-claim review;
- artifact inventory;
- clean-environment test reproduction;
- validation on the minimum supported Python version and the development interpreter.

A private delay is preferable to a premature public release.
