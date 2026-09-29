# Irregular follow-up: `unit21-v2`

This is the separate Unit 21B experiment defined by DESIGN D21B-I1--I16 and
TEST_PLAN IR1--IR24. It does not replace the historical `unit21-v1` campaign.
Materializing inputs or installing this runner is not a pilot, an F7 date, main
authorization, a result, or full Unit 21B closure.

## Entry point and exact invocation

From the authenticated source-tree root, the guarded wrapper exposes:

```text
python experiments/reproduce_irregular.py --help
python experiments/reproduce_irregular.py --pilot [--instances PATH] [--output PATH]
python experiments/reproduce_irregular.py --all [--instances PATH] [--output PATH]
```

The default input directory is `instances`. The default fresh output directories
are `results/unit21-v2-pilot/` and `results/unit21-v2/`, respectively. The public
entry point is `exactfrac.experiments_irregular.main(argv=None)`. It accepts only
the adopted grammar; there is no resume, timeout, subset, repeat, or seed option.
Help and invalid usage do not discover environment, load inputs, or solve.

These are interface descriptions, not permission to execute both commands. After
the production and tests are accepted, the controlled continuation invokes the
disjoint pilot. It independently audits and reports the pilot, then stops for the
author's explicit diagnostic review, F7 date and authorization before main. The
CLI is not a human-approval access-control system. No private BUILD, LEARNING or
planning file is read or hashed as an execution condition. No numeric pilot-time
gate or automatic main launch is introduced.

## Fixed input domains and schedules

The 48 cells combine n in {6, 8, 12, 16}, tau in {64, 128}, b in {1, 8, 64} and
two capacity modes. Pilot uses p01--p05 in each cell: 240 recipes, one call per
route and recipe, 480 calls total, no warmup and no measured triplicate. Main uses
the separate s01--s20 tokens: 960 recipes, one untimed warmup and three measured
repeats per route, 1,920 warmup and 5,760 measured calls. Each invocation is serial
and single-process. Recipe order is ASCII; route order alternates by the adopted
recipe index and round, without outcome-dependent skipping or deduplication.

Every call uses the closed public telemetry solver exactly once. Raw native
records retain losing and infeasible branches and the route-specific fields.
Geometry is computed independently from the input support, not inferred by
dividing observed work. H2 uses all oracle queries and the reduced cut carriers.
Each exact certificate is built and serialized by the public APIs and checked
against the retained input bytes; only a normal `None` verifier return succeeds.
C0 establishes attainment, not optimality. The separate independent audit compares
values to the registered Phase C references without a second production solve.

Same-route result, native statistics and certificate bytes must agree across
warmup and repeats. Cross-route quotients must agree numerically; tied raw pairs
and witnesses are not forced to match.

## Timing and observation

A measured solve interval contains only the public telemetry call. Input parsing,
geometry, metadata, certificate work, verification, output and hashing lie outside
that interval. Warmups have no solve-clock reads. Environment is discovered once.
Valid zero intervals are retained. Pilot-cell timing uses its own clock pair,
starting before the cell's first Instance/geometry work and ending after its final
row and certificate have been flushed; it is not a sum of solve intervals.

`run-info.json` records the finite observed environment, protocol, owned-input
projection and exact 25-path source fingerprint, using the
`exactfrac-unit21b-source/1` prefix and `exactfrac-source-sha256:` version label.
Loaded project origins and source/input bytes are checked again before completion.
The fixed runtime source roster excludes tests, configuration, results and private
evidence. It does not impose an enduring whole-repository freeze.

## Distinct outputs and failure preservation

Pilot writes `run-info.json`, `pilot.jsonl`, one certificate per recipe/route,
`pilot-solves.csv`, `pilot-cells.csv`, and `COMPLETE.json`. Its 480 raw records are
labeled campaign `unit21-v2-pilot`, phase `pilot`; they are operational diagnostics,
not main repeats or an H5 support verdict. Main writes `run-info.json`,
`warmups.jsonl`, `runs.jsonl`, certificates, `summary.csv`, `branches.csv`,
`comparison.csv`, `coverage.csv`, `findings.json`, and `COMPLETE.json`.

Summaries use median solve time over three measured observations, but per-call
counters are not summed over repeats. H5 uses its registered look-ahead coverage
and exact paired call-count median, retaining unfavorable examples and the
untestable case. Timing wins do not redefine that primary predicate. Separate
paper-level H3 estimation is not fitted or emitted by this runner.

All tables are reconstructed from retained checked raw rows. `COMPLETE.json` is
written last after prior handles close, output checks and conservation succeed.
Successful return and independently audited evidence are both required; a marker
alone does not establish success, durability, or hostile-race safety. Native
exceptions propagate; invalid normal dependency promises are rejected.

Every output root must be fresh. A failed invocation and any partially written
marker remain evidence: do not resume, truncate, rename, overwrite or clean them
automatically. An expressly authorized retry must use a separate fresh root.

## Preservation and claim limits

D21B-I2 and I16 retain both observed pilot and main output trees in the complete
Phase H repository candidate. Pilot output stays labeled and separate and is
never pooled into campaign tables. Private handoff audits and checkpoints are
separate from these designated repository output trees. Routine regressions,
isolation and postcommit checks read retained campaign evidence; they do not
retime either new run or the historical `unit21-v1` campaign.

Pre-F7 tests and source-fault controls use scripted 21B telemetry. The only new
bounded actual-composition inputs are the two expressly permitted old micro
instances, one call per route per such scenario. Passing a finite test or campaign
is not proof of strong polynomiality, universal correctness, practical scalability
or release readiness. Phase G/H and Unit 22 retain their existing separate scope.


## Prospective balanced main revision R2 — September 26, 2026

DESIGN D21B-R2-I1--I8 and TEST_PLAN IRR2-1--IRR2-8 supersede the original
main-domain counts above. They preserve the complete 1,200-recipe corpus and
its independent mathematical references. Main `--all` now selects exactly the
720 original s-token recipes at n=6,8,12, both thresholds, all three bit settings,
both capacity modes and twenty seeds per cell. The original order and route
parity of each retained recipe are unchanged.

The revised 36-cell invocation has 1,440 warmup and 4,320 measured calls (5,760
total), with 1,440 distinct certificate files. A successful main output has
1,449 files. The H5 coverage criterion is at least 18 active cells of 36 plus
the unchanged negative eligible-pair oracle median; empty remains untestable.
All 240 complete H3 bit triples per route retain the same estimator. H2 applies
to every executed call. These are planned counts, never reported executions.

The completed 48-cell pilot remains unchanged, including all n=16 observations.
Its source fingerprint is bound to the inert historical snapshot at
`experiments/provenance/unit21-v2-pilot-r1-source.zip`, not to amended live code.
That snapshot is outside the fixed 25-path execution roster and is never imported.
Original pilot fingerprint:
`01428190bdac17bbde27aba5682503ff93a57bb0925e09fd4ec392a0a517469f`.
Do not relabel pilot rows, rewrite its completion marker, pool pilot/main results,
or rerun the original pilot to make source identities equal. Main source identity
is computed independently from the actual amended 25-file source roster.

No new CLI subset/seed/repetition/timeout option is introduced. The change is
prospective and cost-based; it is not pilot outcome tuning. Preserve every
historical result and every registered fault family. No real main-recipe preview
is allowed before the author freeze. During Mac verification only, carry the
recorded resolved TMPDIR spelling into verification subprocesses; do not relax
symlink rejection or change shell/global settings.

The revision date is not F7. Main execution still requires the author's explicit
F7 date and execution authorization after adoption and successful validation.
