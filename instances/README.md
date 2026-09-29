# Initial corpus: `unit20-v1`

This directory contains reproducible input data, not experimental results. DESIGN
§13 (D20-C1–D20-C10), TEST_PLAN §§45–46, and the Unit 20 tables in
`docs/ORACLE_CATALOG.md` define its engineering and mathematical contracts.

## Recipe inventory

The suite preserves 655 qualified identities, including different recipe IDs that
produce equal bytes. There are 55 two-vertex and 324 three-vertex microinstances,
120 structural-family recipes, 120 fixed-support bit-sweep recipes, and 36 seeded
recipes. The five structural families are path, cycle, complete, bipartite, and
matching. The adopted vertex counts are at most eight; the bit sweep extends to
16,384-bit multiplicities. These finite bounds describe this version's inventory,
not limits of the solvers.

Microinstances explicitly enumerate their adopted positive capacities. Other
recipes first sort the support lexicographically. Flat multiplicities are
`2**bits - 1`; ramp multiplicities are
`2**(bits-1) + ((edge_ref + seed) % 2**(bits-1))`. Capacity modes are unit,
ceiling-half degree, `max(1, degree-1)`, degree, and alternating unit/degree at
even/odd dense vertex indices. Not every combination belongs to this finite
version: only `recipe_ids()` is accepted by `generate_instance()`.

Seeded support retains the cycle backbone and includes each other pair when the
first SHA-256 digest byte of the exact five-line D20-C4 message is less than 64.
Seeds are explicitly 1 or 73. This is a deterministic recipe, not a claim of
independent uniform sampling. Disconnected matching support is intentional;
isolated vertices and multiplicity expansion are not.

## Reproduce into a fresh directory

Run this Python snippet from the repository root. The destination must not exist.
The snippet is a caller-side example, not a filesystem interface in the generator.
Change the destination name rather than overwriting any existing data.

```python
from pathlib import Path
from exactfrac.corpus import build_corpus

records = build_corpus()  # Complete in memory or raise; no partial successful build.
destination = Path("reproduced-unit20-v1")
destination.mkdir(exist_ok=False)
for relative_path, raw in records:
    target = destination / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as stream:
        stream.write(raw)
```

`build_corpus()` returns exactly 656 immutable records: the initial MANIFEST,
then the 655 owned payloads in ASCII path order. Payloads are compact ASCII
`exactfrac-instance/1` JSON with keys `format`, `n`, `edges`, `f` in that order
and exactly one LF. Integer encoding converts at most nine decimal digits at
a time and does not change interpreter settings. The generator uses only the
standard library and performs no filesystem, environment, clock, random-state,
subprocess, network, solver, checker, or catalogue access.

A caller-side filesystem failure can leave a partially written fresh directory;
it must not be treated as a completed corpus. Never use this example to overwrite
a live aggregate or a previously materialized suite. Generation failures
propagate without returning a truncated successful build.

## Integrity and later extensions

The versioned paths `unit20-v1/{recipe}.json` are immutable owned data. The
independent Phase C tables register every identity, exact length and digest,
plus finite mathematical expectations. The consuming test independently
reconstructs the inputs and checks the actual files; the generator's own
MANIFEST is not its oracle.

The root MANIFEST uses `exactfrac-corpus-manifest/1`. Its entries are strictly
ordered by ASCII path, with unique suite/recipe identities and paths. The
Unit 20 projection must contain its complete registered inventory and match
the owned payloads exactly. Missing, extra, redirected, executable, nested,
renamed, or changed owned files fail. Duplicate decoded JSON keys, malformed
paths and noninteger byte counts also fail.

The **live aggregate MANIFEST is extensible**, not permanently pinned to its
initial whole-file hash. Later authorized suites may add their own namespaces
and correctly sorted rows; this README and unrelated root documentation may
also evolve. Aggregate whitespace and object-key order may vary. Neither a
global directory hash nor a global file/row count is an enduring Unit 20 rule.
Each foreign suite needs its own substantive authority and integrity checks.

## What the verification establishes

The finite endpoint reference covers all 655 recipes. The 379 microinstances
also compare compact boundary vectors, scalar totals, expanded unit-copy
subsets, and endpoints. The implementation audit subset is those microinstances
plus five `bits-{family}-n04-b16384-qramp-fdegree` stress recipes: 384 inputs,
768 solves across Standard and Accelerated, and 768 independently checked
certificates per execution of that audit. Repetition controls are separately
counted. The C0 checker establishes admissibility and attainment (or valid
Empty status); optimality comparisons come from the independent finite
reference, not the certificate checker alone.

Finite tests do not prove universal correctness, strong polynomiality,
practical scalability, application validity, favorable timing, or release
readiness. No execution path or look-ahead coverage is promised by a recipe
name. Unit 21 owns experimental campaigns and results; Unit 22 owns release
and minimum-interpreter reproduction. No experiment or release artifact is
provided by this corpus.

## Irregular follow-up owning suite: `unit21-v2`

DESIGN D21B-I2--I6 and TEST_PLAN IR2--IR6 authorize a separate 1,200-identity
input extension under `unit21-v2/`. The 48 fixed cells use n in {6, 8, 12, 16},
support thresholds 64 and 128, bit parameters 1, 8 and 64, and alternating or
random capacity rules. Each cell retains the five disjoint pilot tokens p01--p05
and twenty main tokens s01--s20. The names encode deterministic SHA-256 recipe
domains, not a claim of probabilistic independence. Equal payloads remain distinct
registered identities.

`exactfrac.corpus_irregular.build_corpus()` returns this suite's own initial
MANIFEST and its 1,200 payloads. Its own MANIFEST must never overwrite the live
aggregate. This authorized extension adds its sorted entries while preserving
every Unit 20 entry and payload. Each consumer validates the complete metadata
schema but opens only its own suite's files. The live aggregate remains extensible;
the present 1,855-entry count is a phase-local inventory, not an enduring global
limit or hash pin. All 1,200 new bytes match the independently registered Phase C
input fixtures. Materialization does not execute a solver, pilot or campaign.

`experiments/README_irregular.md` describes the separate guarded runner and its
prospective sequencing. The original Unit 20 instructions and historical results
remain unchanged.
