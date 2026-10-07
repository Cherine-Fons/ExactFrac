# ExactFrac

ExactFrac is an exact, certificate-producing solver for the compact
positive-integer-multiplicity modified set-pair density under the active
hypothesis $f(v)\le d_q(v)$.
It implements the strongly polynomial compact-multiplicity algorithm proved in the
project's governing mathematical source.

ExactFrac targets compact-multiplicity instances whose support graph is small enough for
exact parity-family enumeration, while permitting multiplicities with large binary
encodings. Practical support-size limits are established experimentally rather than
asserted in advance.

**Candidate status:** version `0.1.0` is a private release candidate. A successful
private release audit does not publish the repository, upload an artifact, create a
public tag, or authorize external distribution. Publication remains a separate,
explicit author decision.

## Mathematical model

The compact input consists of:

- a finite nonempty loopless support graph $H=(V,S)$;
- a positive integer multiplicity $q_e$ for each support edge;
- a positive integer capacity $f(v)$ for each vertex;
- the active condition $f(v)\le d_q(v)$ for every vertex.

A compact witness consists of a nonempty shore $U\subseteq V$ and a boundary-count
vector $y$ satisfying

$$
0\le y_e\le q_e
$$

on support edges crossing $U$, with nonboundary coordinates zero in the dense internal
representation.

The admissibility conditions are

$$
f(U)+Y(y)\ \text{odd}
$$

and

$$
f(U)+Y(y)\ge 3.
$$

The attained value is

$$
\frac{2(e_q(U)+Y(y))}{f(U)+Y(y)-1}.
$$

Here $d_q$ is the multiplicity-weighted support degree, and $q_e$ represents $q_e$
individually selectable unit copies rather than an indivisible weighted demand.

ExactFrac returns the maximum of this quantity over the admissible compact pairs. If
the admissible family is empty, it returns the literal value $(0,1)$ and `Empty`.
For a nonempty family, it returns a raw numerator-denominator pair $(N,D)$ and a
compact attaining witness $(U,y)$. Raw pairs are preserved rather than silently
normalized whenever the raw fields are the evidence of literal attainment.

The same exact parameter value may serve as a certified fractional lower bound in an
application. It is not an exact integral block count, schedule, or coloring.

## Algorithmic scope

The global solver combines the unit lower bound, four transformed branches
$D_0,D_1,D_2,D_3$, the direct $H_2$ endpoint, exact global comparison, and compact
witness reconstruction. Each branch may be solved by either the `Standard` or
`Accelerated` route. Both routes use the exact residual oracle, whose decomposition
runs through atomic families, sign routing, parity-constrained cuts, ordinary minimum
cuts, and exact max flow.

The theorem gives a strongly polynomial bound on the number of arithmetic and
comparison operations in the support dimensions, independent of the magnitudes of
$q$ and $f$, while intermediate bit lengths remain polynomial in the binary input
length. Exact-arithmetic wall-clock time can still grow with operand bit length. The
software's finite tests and telemetry are implementation evidence; the universal
complexity and correctness claims come from the mathematical argument.

The active compact-multiplicity regime excludes indivisible weighted demands,
arbitrary rational edge weights, the non-active standalone parameter, and the
`fg` extension.

## Installation

ExactFrac requires Python 3.11 or later and uses the Python standard library on its
solver and independent-verifier correctness paths.

From a source distribution or checkout:

```sh
python -m pip install .
```

Development and full-source verification additionally use the declared `dev`
dependencies:

```sh
python -m pip install -e '.[dev]'
```

The release process validates the full applicable source-distribution suite in fresh
Python 3.11 and Python 3.14.6 environments and separately exercises the installed
wheel from outside the source checkout.

## Command-line use

Show the fixed grammar:

```sh
python -m exactfrac.cli --help
```

Solve with the default `Accelerated` route:

```sh
python -m exactfrac.cli solve instance.json > certificate.json
```

Select the `Standard` route explicitly:

```sh
python -m exactfrac.cli solve --solver Standard instance.json > certificate.json
```

Verify one detached certificate:

```sh
python -m exactfrac.cli verify instance.json certificate.json
```

Successful verification is silent. The instance or certificate may be read from
standard input with `-`, but `verify` permits at most one stdin operand.

A minimal active triangle instance is:

```json
{"format":"exactfrac-instance/1","n":3,"edges":[[0,1,1],[0,2,1],[1,2,1]],"f":[1,1,1]}
```

For this instance, the whole shore attains the raw value $(6,2)$ and one canonical
certificate is:

```json
{"format":"exactfrac-certificate/1","empty":false,"N":6,"D":2,"U":[0,1,2],"y":[]}
```

Certificates are canonical single-line JSON terminated by a newline; verify the file
written by `solve`, not a re-typed copy.

## Certificate boundary

The detached checker consumes exactly two byte strings: the instance and the
certificate. It imports nothing from the production solver.

For a nonempty result, the certificate establishes:

- that the compact witness is admissible for the supplied instance; and
- that the witness literally attains the reported raw pair $(N,D)$.

For the genuine Empty case, it validates the specified Empty representation. Global
optimality of a nonempty result belongs to the mathematical algorithm and its proof,
with independent finite reference comparisons used during implementation validation.
The certificate is therefore deliberately precise about what it proves.

## Verification architecture

ExactFrac was built under a layered verification regime:

1. a canonical, versioned, hash-pinned mathematical source;
2. a proof-to-code contract translating hypotheses, proof objects, representation
   rules, and forbidden transformations into implementation obligations;
3. data representations selected so exactness, admissibility, witness consistency,
   raw attainment, and endpoint reconstruction remain externally observable;
4. implementation boundaries aligned with the structural joints of the proof;
5. mathematical invariants fixed before acceptance of the corresponding code;
6. hand-derived expectations and independently implemented reference routes fixed
   before they were permitted to judge production behavior;
7. a preregistered adversarial test plan with RED required before GREEN;
8. a detached certificate checker and an independent brute-force verifier;
9. proof-derived telemetry that exposes the realized operation structure; and
10. a theorem-obligation-to-test conformance map that never promotes finite tests
    into a proof of a universal theorem.

Production output is never its own oracle. Where two reference routes are registered,
they must agree before either serves as acceptance evidence. Fault injection and
negative controls establish that critical tests reach the failure mechanisms they
claim to detect.

The telemetry records proof-derived quantities such as $r_j$, $s_j$, $A_j$,
and observed oracle-call counts $C_j$. Registered finite identities include:

- `atomic_families_examined` $= C_j r_j$;
- `atomic_families_feasible` $=$ `parity_cut_calls` $= C_j s_j$; and
- `ordinary_min_cut_calls` $=$ `max_flow_calls` $= C_j A_j$.

These observations can expose an implementation that returns the expected value while
performing the wrong structural work. They remain finite execution evidence, not a
replacement for the complexity proof.

## Authorship and development

ExactFrac originates in Cherine Fons's mathematics. She proved the underlying theorem, designed the strongly polynomial algorithm, and authored the mathematical specification against which the implementation was required to conform.

Before the production build commenced, the author implemented the problem's
fundamental computational objects in an independently authored, 214-commit,
test-gated codebase containing no AI-written code. That pre-build foundation included
a from-first-principles brute-force checker implementing the manuscript's definitions
directly, with a hand-proved lemma serving as its independent oracle. It culminated in
a timed mock assessment and the Exit Test of the pre-build foundation. This work
established the author's independently demonstrated command of the computational
objects on which she later specified, challenged, and judged the production system.

The author then designed and administered the production build's formal regime. She
froze the mathematical source as a versioned, hash-pinned authority; translated
hypotheses and lemmas into executable interface contracts; selected compact witnesses
$(U,y)$, raw $(N,D)$ pairs, and specified Empty semantics; prohibited floating
point and normalization that would destroy literal checkability; and decomposed the
implementation along the proof's branch domains $D_0$–$D_3$, atomic families,
sign-routing, parity-cut, oracle, solver, witness, and certificate boundaries. She
designed and enforced the invariants that govern these components and their
composition.

She authored the verification specification as well. The preregistered `TEST_PLAN`
obligations were written before the corresponding production code; independent oracle
expectations were derived in advance; production output was barred from certifying
itself; and every test was assigned a concrete failure mechanism to expose. Those
mechanisms included parity and feasibility boundaries, Empty and infeasible families,
ties, endpoint monotonicity, malformed inputs, dependency failures, representation
violations, witness inconsistencies, and incorrect execution structure.

RED-before-GREEN was a binding admission gate, not a coding custom. The author
personally ran every live gate, read every RED and GREEN, and issued every acceptance,
STOP, correction, amendment, and continuation ruling. She held the rules even against
a faster or more convenient path: a clean mock did not waive the Exit Test of the
pre-build foundation. The 143 declared fault families belong specifically to the
Unit 21B irregular campaign, `U21BF001`–`U21BF143` under `TEST_PLAN` obligation
`IRR2-6`; they are not presented as a project-wide total.

The author likewise designed the certificate boundary, the independently checkable
evidence model, and the proof-derived complexity telemetry built around $r_j$, $s_j$,
and $A_j$, together with the conformance map, preregistered empirical protocols,
scientific claim boundaries, and provenance system. She adjudicated authorities before
repository admission; personally operated
the recorded conformance, staging, isolated-tree, commit, and push transitions; and
preserved failed attempts instead of rewriting them as though they had not occurred.
When a gate stopped on live-context lint, a tracking-reference mismatch, a preloaded
module collision, or an incorrect helper assumption about repository state, she
diagnosed the defect, routed it for separate review, authorized the correction, and
continued only through the operations permitted by the governing record. Her rulings
fixed the Accelerated solver as part of the core system, required the global solver to
be exercised under both branch solvers, prohibited premature hash-freezing of files
reserved for population by later units, and required experimental campaigns to run
from a fresh root without timeout.

She managed the build as a controlled multi-system research project. Separate drafting
and reviewing systems had different roles; the reviewing route independently
recomputed oracles and campaign results; the author's Mac remained the authoritative
execution environment; she established continuation protocols and state blocks, set
model-tier routing and data budgets, and maintained authenticated upload ledgers binding
artifacts between systems; and byte-pinned authorities, append-only records, source
fingerprints, controlled amendments, and private audit/checkpoint evidence made the
history reconstructible. She also corrected errors introduced by the surrounding systems when
they attempted to add an unauthorized protocol step, misstated a commit sequence, or
misread the attained repository state.

The author retained control of scientific interpretation and release terms. She kept
mathematical theorem, implementation conformance, certificate evidence, finite oracle
comparison, empirical observation, and release readiness as distinct claims. She
fixed the tested strata before measurement, retained unfavorable results, and forbade
pilot/main pooling. She authorized the Unit 21B pilot, examined its diagnostics,
prospectively revised the main scope on cost grounds, dated F7, authorized the main
campaign, and executed it to completion. She also determined the language by which the
results and this contribution account may be represented.

Within this regime, an AI system generated the production implementation and supporting
infrastructure to the author's mathematical specification. A separate AI system
reviewed the generated packages and independently recomputed oracles and campaign
results. Every artifact entered the repository only through the author's acceptance:
against her theorem, under her specification, and at a live gate that only she
operated.

## Research basis and source status

The public research arc consists of:

- **Expanded full manuscript:** Cherine Fons, *A Strongly Polynomial Algorithm for
  The Modified Set-Pair Density Under Compact Multiplicities*, 24-page public SSRN
  preprint 7476581, posted September 19, 2026.
- **Priority note:** Cherine Fons, *A Strongly Polynomial Algorithm for the Modified
  Set-Pair Density under Compact Multiplicities*, 14-page public SSRN preprint 7190218,
  posted August 6, 2026. SSRN currently groups this record with the expanded manuscript;
  no substantive September revision of the priority-note text is asserted here.
- **Earlier explicit-copy algorithm:** Cherine Fons, *Polynomial-Time Computation of
  the Modified Set-Pair Density for the Fractional f-Chromatic Index*, 97-page public
  SSRN preprint 7107518, posted July 15, 2026 and last revised July 16, 2026.

The implementation is governed by the private, hash-pinned v2.2 mathematical source
identified in `docs/SPEC_LOCK.md`. The private manuscript is not packaged with the
software. `docs/CONTRACT.md` states the implementation contract, and the public-source
crosswalk is reviewed as part of the release audit.

## Empirical characterization

The retained empirical work is reported as two distinct preregistered studies.

The initial `unit21-v1` campaign contains 655 registered recipe identities. Each recipe
was run through both solvers with one warmup and three measured repetitions per route,
for 5,240 actual solver calls and 5,240 certificate checks. The retained output contains
1,317 files. These are instrumented solve measurements under the frozen protocol, not
universal runtime claims.

The Unit 21B irregular follow-up preserves its pilot and main stages separately. The
pilot includes the $n=16$ stratum. The balanced main campaign contains 36 cells over
$n\in\{6,8,12\}$, 720 original `s`-token recipes, both solver routes, one warmup and
three measured repetitions per route and recipe, for 5,760 actual calls. The main
campaign was fixed through a dated, cost-based prospective revision before execution;
pilot and main measurements are not pooled.

Among the 509 of 720 main-campaign recipes eligible under the preregistered Unit 21B
rule, the retained Accelerated-minus-Standard oracle-call differences comprise 303
negative, 87 zero, and 119 positive outcomes, with pooled paired oracle-call median −1.
Cell medians are negative, zero, and positive in 24, 9, and 3 cells respectively; the
three positive cells remain visible in the evidence. The registered H5-prime rule was
supported at its stated scope. This finite result does not
establish universal acceleration, a practical frontier, or an isolated causal benefit
from look-ahead. Hardware-dependent timings and operation-count diagnostics are reported
with their actual measurement labels.

Reproduction commands, fixed schedules, exact result identities, and interpretation
boundaries are documented under `experiments/` and the retained conformance record.
Ordinary tests do not rerun or retime either archived campaign.

## Repository structure

- `exactfrac/` — production solver package;
- `exactfrac_verify/` — independent brute-force and certificate verification;
- `tests/` — regression, conformance, adversarial, isolation, and release tests;
- `docs/` — governing authority, contract, oracle, conformance, and release records;
- `instances/` — versioned inputs with authenticated manifests;
- `results/` — retained, versioned empirical evidence;
- `experiments/` — guarded reproduction entry points and protocol documentation;
- `release_audit.py` — offline release-candidate inspection tool included in the
  source distribution but not in the runtime wheel.

The governing documents `docs/DESIGN.md`, `docs/TEST_PLAN.md`,
`docs/ORACLE_CATALOG.md`, `docs/CONFORMANCE.md`, `docs/SPEC_LOCK.md`, and
`docs/CONTRACT.md` are append-only authority records and retain their LaTeX source
notation; this README and `docs/RELEASE.md` use GitHub Markdown math delimiters for
presentation.

## Determinism and arithmetic

Production mathematical decisions use exact integer and rational arithmetic; no
floating-point tolerance selects a result. Algorithmic enumeration orders are fixed,
and no algorithmic path relies on iteration order from a Python `set`. When the
mathematics permits multiple correct outputs, deterministic implementation choices are
reproducibility policy rather than additional mathematical tie-breaking requirements.

## Release discipline

The release audit independently examines the candidate source tree, full accessible Git
history, source distribution, wheel, notices, metadata, mathematical and empirical
claims, artifact inventories, archive safety, interpreter compatibility, installed
imports, and unresolved findings. It records complete or incomplete coverage rather
than converting an interrupted or partial inspection into a clean result.

A passing audit is evidence about the exact inspected candidate. It does not make the
private repository public and does not authorize package publication or external
deposit. Any public release requires a separate author instruction naming the exact
artifact, version, destination, and visibility action.

## License

ExactFrac is licensed under the MIT License. See `LICENSE`.

## Citation

Use the software citation in `CITATION.cff`. Research claims should also cite the
corresponding manuscript listed under **Research basis and source status**.
