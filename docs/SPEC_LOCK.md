# SPEC_LOCK — governing mathematical specification

Status:    SOLE READ-ONLY CANONICAL MATHEMATICAL SPECIFICATION — V2.2
Effective: upon this file's controlled commit to the ExactFrac repository
Held in:   private ExactFrac authority archive (not in this repository)

Canonical package:      ExactFrac_Mathematical_Specification_v2_2_CANONICAL_2026-09-02
Package ZIP SHA-256:    400c4e23a7683571f7181b98bc009954d431f4ac355a247fb22327a609b4f9ce

Governing source:       Theorem_B_Strongly_Polynomial_Proof_ExactFrac_Spec_v2_2.tex
Source SHA-256:         4cceb9984bc6d24b78f0eeff1f9014650fc490de2210e748f0fcae85d1ffcaa6
Governing PDF:          Theorem_B_Strongly_Polynomial_Proof_ExactFrac_Spec_v2_2.pdf
PDF SHA-256:            d7f6055dc0e7aa161e584c8f83da468f331deef480c895055797c023fcd50186
Rendered pages:         38
V2.1-to-V2.2 diff:      V2_1_TO_V2_2_ZERO_ARC.diff
Diff SHA-256:           e515f9718213505555999475085f5d9a31ef4ec90aaa814301fb3fe93d7a2b48

Immutable parent:
- V2.1 package SHA-256: 849745ea3601e68a7b532fa3e405b7d5cf322c9006aa1bab033ef35328e43dcd
- V2.1 source SHA-256:  f2440587b966e2aa6192a5e029434e9f71259dd49c30e4eb397bdc59347523e4

Author adoption:
- Author: Cherine Fons
- Date: 2026-09-02
- Record: AUTHOR_ADOPTION_RECORD.md inside the canonical package
- Candidate R1 SHA-256: 7109819aa958226a66b9753a64851817eee84e3038b33b5109cc6867ed67a403

Amended labels/carriers only:
- proof of thm:GR: residual-reachability recovery is O(N+E), including E=0;
- lem:ek: explicit zero-arc return, uniform O(N+NE^2) carrier, and zero-safe generated-number bound;
- proof of thm:branch-oracle: explicit zero-safe dimension substitution.

Algorithm environments (SHA-256 of \begin{algorithm}...\end{algorithm}):
- ExactBranchMin:          8788a5b48f149a46b8da9c29ac2eb5d5973911ad2e126c59ebacd02d29ee8d25
- SolveBranchAccelerated:  d59308559f96d4289895015ae16e11967972e5a8281b925115084f96feaa7611
- SolveBranchStandard:     b9a9a3c0d4041acd533e5fdec522468223adaff8b9e50898e47916e69a900446
- StrongCompactMSPD:       7362cc0796164e9dd90c9691ffd246aed2041d2d82eb19c2ccb49217726b3933

Protected theorem/invariant blocks:
- thm:main:                eefc7f6ab43844d5842116e66aae48b10fa516203b5df5676a1f1db0a9948b93
- prop:branch-invariant:   de74c11f3f27e64a842350b6b30d81d3e1d16c451f1a5179f739961d4764b448
- prop:global-invariant:   dabe1d09046484cb655ffc69a6280a45cce04eb9abb7e39fdf1f898ef0c12f14

Contract crosswalk:
- docs/CONTRACT.md SHA-256: d19709904be7e0b6e0f78f704d016b0b0a4395ac6833dbc367f20db0d2e25b68
- Mathematical meaning unchanged by V2.2.

Rules:
- V2.1 remains immutable parent history.
- The V2.2 source and package are never edited in place.
- Any later amendment creates a new versioned package and a new SPEC_LOCK.
- Code, tests, and docs cite source labels exactly as printed.
- Stage-2 flow code is not authorized until DESIGN, TEST_PLAN, CONFORMANCE, and the governing checksum manifest are synchronized in the same authority commit as this lock.
- The returned exact quotient and compact witness contract remains unchanged; the empty family returns ((0,1), Empty).
