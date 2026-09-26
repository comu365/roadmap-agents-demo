# unitconv — roadmap agents demo

A deliberately tiny unit converter that shows the builder → reviewer loop from
[claude-roadmap-agents](https://github.com/comu365/claude-roadmap-agents) running on a real roadmap.

## Where to look

1. [`ROADMAP.md`](ROADMAP.md) — machine-readable items with checkable acceptance criteria.
2. [`.claude/agents/`](.claude/agents) — the two agent templates, filled in for this repo.
3. **The P1-1 pull request** (Pull requests → closed) — the full run, reports pasted verbatim:
   - builder implements length conversion (76 tests, breaks the code once on purpose to prove the tests can fail)
   - reviewer (read-only, Opus) recomputes every factor without importing the code → **CHANGES REQUESTED**
     (wrong done-marker; `OverflowError` leaking instead of `ValueError`)
   - builder reworks on the same branch → reviewer re-checks only the new diff → **PASS**
4. [`docs/roadmap-log.md`](docs/roadmap-log.md) — what was decided, how it was verified, what risk remains.

The first builder run also found that `CLAUDE.md` and the builder's own instructions disagreed about who marks an item done.
It flagged the conflict instead of guessing; the rule was fixed on `main` (see commit history) and the fix went back into the template.

## Run it

```bash
python3 -m venv .venv && .venv/bin/pip install -q -U pip && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest -q
```

MIT licensed.
