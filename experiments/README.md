# Unit 21: reproduce the initial experiment campaign

This directory provides the guarded entry point to the fixed `unit21-v1`
campaign. Its implementation is `exactfrac.experiments.main`. Importing either
module does not start an experiment. The governing engineering contract is
DESIGN §14 (D21-E1–D21-E16), with prospective tests in TEST_PLAN §§47–48.

## Invocation

From the source checkout, with its compatible Python environment:

```sh
python experiments/reproduce.py --help
python experiments/reproduce.py --all
```

The defaults are the source checkout's `instances/` and `results/unit21-v1/`,
regardless of the working directory. An explicit path is relative to the caller's
working directory unless absolute:

```sh
python experiments/reproduce.py --all --instances /path/to/instances --output /path/to/new-run
```

The output directory must not exist, including as an empty directory, file,
or symlink. Do not delete or overwrite a prior campaign to rerun this command.
Use a new disjoint output leaf. Output inside the source tree is restricted to
a new child of `results/`. Output must neither overlap inputs nor contain the
source tree. Parent traversal and symlink redirections are rejected.

There are no subset, seed, repetition, resume, force, timeout, or scheduling
options. `--all` must occur first and exactly once. Each optional flag may occur
once in either order. Help returns zero; invalid grammar emits fixed non-echoing
usage on binary stderr and returns two. Successful campaign execution is silent
and returns zero. Contract violations and operational exceptions are not silently
converted into successful partial output.

## Fixed inputs and schedule

All 655 registered Unit 20 recipe identities are retained, including identities
whose payload bytes coincide. The source generator is used to authenticate the
owned input projection; this campaign does not generate replacement input files.
The evolving aggregate MANIFEST may contain valid other-suite entries. Only the
exact immutable Unit 20 projection and its owned files are consumed; foreign
payloads are not opened. The observed aggregate digest is provenance, not a
permanent whole-MANIFEST acceptance pin.

Recipes are traversed in ASCII order. For each recipe index `i`, rounds are
`r = -1, 0, 1, 2`. Round -1 is one untimed warmup per solver. The remaining
rounds are three measured repetitions per solver. Standard precedes Accelerated
exactly when `(i + r) % 2 == 0`; the order is reversed otherwise.

A complete invocation therefore requires 1,310 warmup solves and 3,930 measured
solves: 5,240 actual instrumented solver calls and 5,240 certificate checks.
Each repetition is a new call. These are schedule requirements, not a claim
that an invocation has already completed or that any specific branch executed.
Execution is serial in a single process without adaptive stopping, data-dependent
subsampling, timeouts, garbage-collector changes, affinity changes, or interpreter
limit changes.

## Timing, certificates, and diagnostic records

For measured calls, `perf_counter_ns` is sampled immediately before and after
one `solve_with_telemetry` call. Parsing, metadata discovery, certificate creation,
serialization, independent verification, report reduction, and file output are
outside the interval. Warmups have null elapsed values and no clock samples.
Zero measured durations are retained. These are timings of instrumented solves,
not measurements of an uninstrumented solver.

Every returned solve result and its actual `AlgorithmStats` are retained. Every
call builds and serializes a C0 certificate and independently checks it against
the same retained input bytes. Each actual `RunRecord` has environment/provenance
metadata separate from arithmetic diagnostics. Raw structural integer pairs are
not silently reduced. Repetitions of one solver must agree in result, diagnostics,
and certificate bytes. Between solvers, numerical equality is cross-multiplied;
different admissible witnesses and equivalent raw pairs may remain distinct.

A C0 certificate establishes admissibility and attainment, or the valid Empty
case. It is not by itself a global-optimality certificate. Independent finite
optimality checks use separately registered expectations, outside the producer.

Counters and diagnostic widths remain integer JSON tokens, including integers
larger than the interpreter's decimal-conversion limit. Decimal conversion uses
bounded chunks rather than changing that limit. Environmental durations and clock
resolution are the only floating-point fields in the experiment's wire records.

## Artifacts and provenance

A completed output has only the following top-level files and one subdirectory:

- `run-info.json`: protocol, observed environment, 22-source-file fingerprint,
  and input provenance.
- `warmups.jsonl` and `runs.jsonl`: raw records in filtered global call order.
- `certificates/`: one independently checked warmup certificate per recipe/route;
  all repeated certificate bytes must agree with it.
- `summary.csv`, `branches.csv`, and `comparison.csv`: deterministic reductions
  of the retained, validated measured records, not another solve pass.
- `COMPLETE.json`: the last-written count and file-identity record.

The exact source fingerprint covers the closed Python modules and the two new
entry-point/implementation files, in ASCII path order. It does not cover future
results, mutable documentation, tests, or the whole evolving repository. Loaded
project-module file and import-spec origins are checked against the fingerprint's
source root. The fingerprint must match the actual source files used; an editable
installation or another checkout cannot silently supply project modules.

Environment recording is limited to Python version, platform description, CPU
string or null, clock attributes, decimal/recursion limits, and the explicitly
observed hash seed. It does not gather usernames, private absolute paths,
hostnames as a separate field, Git remotes, or the full environment.

For a complete 655-recipe invocation, the owned namespace contains 1,317 files:
1,310 certificates and seven top-level artifacts. `summary.csv` has 1,310 rows;
`comparison.csv` has 655. `branches.csv` retains all four branches, including
infeasible branches, for each nonempty recipe/route, and has no nonbranch pseudo-row.
Row counts and completion counts are validated from actual retained execution.

Summary times are the exact middle of three sorted integer nanosecond values.
Repeated-identical event counts are reported once, not summed over repetitions.
Work composition uses sums for event counts and maxima for peak quantities.
Standard-specific and Accelerated-specific native fields are not dropped to
make their schemas look identical.

## Failure and completion boundaries

Outputs are created exclusively and checked for short/invalid binary writes,
flush failures, and close failures. Before completion, source and input identities
are rechecked, the owned output membership and every artifact's bytes are checked,
and the ledger binds every non-marker file. The marker does not contain its own
hash. No later file is written after a successful marker close.

A failed invocation may leave partial files, and a marker write/flush/close failure
may even leave a parseable marker. Neither is successful completion. Require a
successful invocation and an independent content/count/provenance audit. The
runner does not claim filesystem transactionality, atomic multi-file publication,
crash durability, or authentication against a hostile concurrent filesystem actor.
It does not repair, resume, remove, or overwrite failed output.

## Tests and interpretation

Ordinary tests use synthetic observations, scripted clocks, and fault injection.
A bounded composition test additionally uses three registered tiny real inputs;
it is not the initial full campaign. Existing historical `results/unit21-v1`
output, when present, is checked read-only by a separate consumer test, without
calling the producer to manufacture its own expectations or rerunning timings.

Actual campaign observations must be read from their bound raw records and tables.
In particular, an Accelerated schedule entry or an `n > 3` family does not prove
that look-ahead ran. Inspect `lookahead_queries`, retaining zero counts and
unfavorable comparisons. Look-ahead activity and evidence of benefit are distinct.
Never substitute scripted telemetry or another machine's timing for the current
campaign's measurements.

Successful finite tests and a complete campaign do not prove universal correctness,
strong polynomiality, runtime scalability, minimum-interpreter compatibility,
release readiness, or an empirical hypothesis merely by family labels. Releasing,
repackaging, or publishing artifacts is outside this unit's execution command.
