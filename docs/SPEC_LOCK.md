# SPEC_LOCK — governing mathematical specification

Status:    SOLE READ-ONLY CANONICAL MATHEMATICAL SPECIFICATION — V2.1
Held in:   private research archive (not in this repository)
Note:      manuscript-visible metadata reads "refreeze v2" by design; V2.1 is the
           package-level patch identity (three Edmonds–Karp citation carriers only)

Frozen package:        Theorem_B_Canonical_Frozen_2026-08-25_v2_1
Package zip SHA-256:   849745ea3601e68a7b532fa3e405b7d5cf322c9006aa1bab033ef35328e43dcd

Governing source:      Theorem_B_Strongly_Polynomial_Proof_Canonical_Synchronized.tex
Source SHA-256:        f2440587b966e2aa6192a5e029434e9f71259dd49c30e4eb397bdc59347523e4
Governing PDF:         Theorem_B_Strongly_Polynomial_Proof_Canonical_Synchronized.pdf
PDF SHA-256:           c9d1b3fa0b3bf9eadf80eee95a7d7ad2fb7ff1766fd421d6da5d67587906e302
Rendered pages:        38

Algorithm environments (SHA-256 of \begin{algorithm}...\end{algorithm}):
  ExactBranchMin          8788a5b48f149a46b8da9c29ac2eb5d5973911ad2e126c59ebacd02d29ee8d25
  SolveBranchAccelerated  d59308559f96d4289895015ae16e11967972e5a8281b925115084f96feaa7611
  SolveBranchStandard     b9a9a3c0d4041acd533e5fdec522468223adaff8b9e50898e47916e69a900446
  StrongCompactMSPD       7362cc0796164e9dd90c9691ffd246aed2041d2d82eb19c2ccb49217726b3933

Contract crosswalk:    docs/CONTRACT.md  (verbatim copy of the package's
                       audit/EXACTFRAC_MATHEMATICAL_CONTRACT_CROSSWALK.md;
                       must hash to the value below)
Crosswalk SHA-256:     d19709904be7e0b6e0f78f704d016b0b0a4395ac6833dbc367f20db0d2e25b68
Design of record:      docs/DESIGN.md
Obligation map:        docs/CONFORMANCE.md  (committed in the same commit as this file)

Rules
- The governing copy is never edited in place. Any amendment produces a new
  versioned package and a new SPEC_LOCK.
- Code, tests, and docs cite the source by LaTeX label — exactly as they appear
  in the source: alg:branch-min, alg:branch (SolveBranchAccelerated),
  alg:standard-branch (SolveBranchStandard), alg:global (StrongCompactMSPD),
  prop:branch-invariant, prop:global-invariant, thm:main — never by theorem number.
- The returned quotient (N, D) is the EXACT modified set-pair density, with a
  compact witness (U*, y*) whenever the admissible family is nonempty; the empty
  family returns ((0,1), Empty). The value may serve as a certified fractional
  lower bound on integral blocks or rounds; it is never described as an exact
  block count.
