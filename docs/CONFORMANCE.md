# CONFORMANCE — theorem obligations discharged by tests

Governing source: see SPEC_LOCK.md. One row per obligation; the label is copied from
V2.1's \label{} set. A row is added when its unit lands; a unit is not done until its
row exists and its test is green.

| Obligation (V2.1 label) | What it promises | Discharging test | Status |
|---|---|---|---|
| prop:expanded-equivalence | compact objective equals the expanded-copy objective | tests/test_verify_brute.py::test_compact_expanded_agree | planned |
| lem:empty | Q = 1 single edge, f ≡ 1 → ((0,1), Empty) | tests/test_global.py::test_q1_empty_family | planned |
| lem:unit | constructive unit witness is admissible with ratio ≥ 1 | tests/test_global.py::test_unit_witness_admissible | planned |
| prop:domain-decomp | atomic families cover each branch domain | tests/test_families.py::test_cover | planned |
| lem:ek | reference max-flow: O(NE) augmentations, min cut recovered | tests/test_flow.py | planned |
| prop:branch-invariant | invariant holds after every branch iteration | tests/test_branch.py::test_invariant | planned |
| prop:standard-correct | standard loop terminates with the exact branch optimum | tests/test_branch.py::test_standard | planned |
| prop:branch-correct | accelerated loop terminates with the exact branch optimum | tests/test_branch.py::test_accelerated | planned |
| prop:global-invariant | global invariant holds across branches and the H2 scan | tests/test_global.py::test_invariant | planned |
| thm:main | value equals the brute-force optimum on every catalog instance | tests/test_global.py::test_catalog | planned |
