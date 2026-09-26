# Roadmap log

One entry per roadmap item: what was decided and why, how the reviewer verified it, and what risk remains.

## P1-1 Length conversion — merged via #1 (2026-09-27)

- **Decision:** store factors as `fractions.Fraction` and convert to float once at the end. Plain float math gave
  `convert(1, "ft", "in") == 12.000000000000002`, failing the exact-equality criterion.
- **Decision:** overflow (`convert(1e308, "km", "mm")`) raises `ValueError`, not `OverflowError`, so callers only catch one type.
- **Rule fix found by the run:** `CLAUDE.md` said only a human sets ✅ while the builder was told to set ✅. Clarified on `main`
  (00410ff, 97a98b6): in this no-deployment repo the builder marks ✅ on its branch, and it lands only through the merge.
- **How it was verified:** the reviewer (Opus) recomputed every factor from the definitions with `Fraction`, without importing
  the code (mi = 1609.344 m, worst round-trip error 1.4e-16), re-ran the suite (77 passed), and probed the overflow edges.
  The builder broke the code on purpose twice to prove the tests can fail.
- **Rounds:** 1 rework (limit 2). Human merge, because the policy doesn't settle whether *adding* the first factors counts
  as "a conversion factor changed".
- **Remaining risk:** factors were checked against NIST SP 811 Appendix B from memory, not a freshly fetched copy. No CI yet.
