# ExactFrac mathematical contract crosswalk - carried forward into v2.1

| Contract element | Canonical requirement |
|---|---|
| Input | Finite nonempty loopless support graph `H=(V,S)`, positive binary multiplicities `q`, positive binary capacities `f` |
| Multiplicity semantics | `q_e` distinct, individually selectable unit copies; not an indivisible weight |
| Active condition | `f(v) <= d_q(v)` for every vertex |
| Compact object | `(U,y) in A_q(H)` with `0 <= y_e <= q_e` and total `Y(y)` |
| Objective | Exact maximum `2(e_q(U)+Y(y))/(f(U)+Y(y)-1)` over admissible compact pairs; value zero if empty |
| Branch domains | `D_0,D_1,D_2,D_3` plus the direct `H2` endpoint |
| Oracle input | Branch `j` and exact rational `lambda=A/B`, `B>0` |
| Oracle objective | Raw integer residual `Bc_j-Ah_j` |
| Oracle return | Infeasible or **any exact minimizer**; no preferred tie-breaking |
| Shift handling | Remove sign-routing/contraction constants and re-evaluate the raw residual before global comparison |
| Supergradient | Every exact argmin returns `-h_j(U)` as a valid supergradient |
| Accelerated outer loop | `SolveBranchAccelerated`; stored residual `r`; exact zero test; look-ahead acceptance by residual sign |
| Standard fallback | `SolveBranchStandard`; exact Newton update; WYZ `O(M^2 log M)` bound |
| Global solver | `StrongCompactMSPD`; exact branch comparison and endpoint reconstruction |
| Empty family | Return `((0,1), Empty)` |
| Witness | Return a compact optimal pair only when the admissible family is nonempty |
| Arithmetic | Exact integer/rational arithmetic and cross multiplication; no tolerances |
| Complexity | Accelerated `O(M log M R (n+3)^3(m+n)^2)` arithmetic/comparison operations; polynomial intermediate bit lengths |
| Exclusions | Non-active standalone parameter, indivisible weighted demands, arbitrary rational edge weights, and `fg` extension |

## Refreeze-v2 clarification

The former formal maximum-denominator scalarization is **not part of the canonical publication or ExactFrac contract**. It is not an optional API mode, not an oracle precondition, and not an implementation obligation. The only retained maximum-denominator language explains that the representative selected inside the DKNV proof is analytical rather than required from the oracle.

## Notation

- Explicit-copy boundary set: `F`.
- Compact count vector: `y`.
- Compact total: `Y(y)`.
- Attainable total-only dummy: `x`.
- Branch residual function: `F_j`.
- Stored residual value: `r`.

**Contract status: frozen and implementation-complete.**


## V2.1 documentary micro-refreeze

The Edmonds--Karp citation-role and pinpoint synchronization changes no contract element. All rows above carry forward byte-for-byte in mathematical meaning.
