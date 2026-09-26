# ROADMAP — unitconv

A **machine-readable roadmap** that the `roadmap-builder` / `roadmap-reviewer` agents read and update.
How it runs: see "Roadmap loop" in `CLAUDE.md`.

## How to read

- **Status**: ⬜ todo · 🔨 in progress (builder) · 🔍 in review (branch pushed) · ✅ done (once merged) · ⛔ on hold
- **Run**: 🤖 an agent may implement it · 🙋 human only (agents don't touch it; they say "this one is yours")
- **Acceptance criteria** must be *checkable sentences*. If they are vague, the builder asks instead of implementing.
- An item is **one branch, one review**. If it doesn't fit in one review, split it.

## Decisions

| Decision | Current default |
|---|---|
| Python version | 3.9+ |
| Dependencies | standard library only (pytest for tests) |
| Unit definitions | exact SI definitions from NIST SP 811, Appendix B — no rounded factors |
| Unknown unit / mixed dimensions | raise `ValueError` with the offending unit in the message |

## Phase 1 — core conversions

### P1-1 Length conversion
- Status: ⬜ · Run: 🤖 · Depends on: —
- Goal: `unitconv.convert(value, from_unit, to_unit)` converts between length units.
- Units: `m`, `km`, `cm`, `mm`, `in`, `ft`, `yd`, `mi`
- Acceptance criteria:
  - [ ] `convert(1, "mi", "m") == 1609.344` (international mile, exact)
  - [ ] `convert(1, "ft", "in") == 12` and `convert(1, "in", "cm") == 2.54`
  - [ ] every pair of units round-trips: `convert(convert(x, a, b), b, a)` equals `x` within 1e-12 relative
  - [ ] unknown unit (e.g. `"parsec"`) raises `ValueError` naming the unit
  - [ ] `math.nan` / `math.inf` input raises `ValueError` (no silent NaN output)

### P1-2 Temperature conversion
- Status: ⬜ · Run: 🤖 · Depends on: P1-1
- Goal: `convert` also handles `C`, `F`, `K` (affine, not just a factor).
- Acceptance criteria:
  - [ ] `convert(100, "C", "F") == 212` and `convert(0, "C", "K") == 273.15`
  - [ ] temperatures below absolute zero raise `ValueError`
  - [ ] converting between a length and a temperature raises `ValueError`

### P1-3 Command-line interface
- Status: ⬜ · Run: 🤖 · Depends on: P1-2
- Goal: `python -m unitconv 5 mi km` prints the result.
- Acceptance criteria:
  - [ ] `python -m unitconv 1 mi m` prints `1609.344` and exits 0
  - [ ] an unknown unit prints the error to stderr and exits 2

### P1-4 Publish to PyPI
- Status: ⬜ · Run: 🙋 · Depends on: P1-3
- Goal: a human creates the PyPI account and token, and decides the package name.

## Backlog

- B-1 Area and volume units — only when the user asks
