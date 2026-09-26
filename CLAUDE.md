# unitconv

A tiny unit converter. It exists to demonstrate the builder → reviewer roadmap loop from
[claude-roadmap-agents](https://github.com/comu365/claude-roadmap-agents); the converter itself is deliberately small.

## Principles

- **Exact definitions only.** Every conversion factor comes from NIST SP 811 Appendix B and carries a source comment.
- **No silent failures.** Bad input raises `ValueError`; nothing returns NaN, `None`, or a guess.
- Standard library only.

## Commands

- Setup: `python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"`
- Tests: `.venv/bin/pytest -q`

## Roadmap loop

When asked to "work on the next roadmap item", the main session orchestrates; it does not write the code itself.

1. **Pick**: if no item was named, choose the first item in `ROADMAP.md` with status ⬜, run 🤖, and all dependencies ✅.
   Tell the user *"Working on P?-?"*. Backlog items (B-x) only on request.
2. **Build**: call `roadmap-builder` with `isolation: "worktree"` for that one item. Pass the model name for the commit trailer.
   If the builder stops (🙋, unmet dependency, vague criteria), relay its reason to the user as-is.
3. **Review**: call `roadmap-reviewer` with the item ID, branch, and the builder's worktree path.
   `CHANGES REQUESTED` → send the findings back to the **same** builder; at most **2** rework rounds, then report to the user.
   `BLOCK` → stop and report immediately.
4. **Report**: summarize for the user and append an entry to `docs/roadmap-log.md` — the decision and its reason,
   how the reviewer verified it, and remaining risks.
5. **Merge**: follow the merge policy below. Only after merge does the item become ✅.

### Merge policy

**Claude may merge** only when the reviewer ran on Opus and returned PASS, the full test suite passes, and no
"human merges" condition applies.

**A human merges** when any applies: `CLAUDE.md` / `.claude/` / ROADMAP legend or Decisions changed; a new dependency;
linked to a 🙋 item; BLOCK or more than 2 rework rounds; `.github/workflows/` changed; **a conversion factor changed**.

### Guardrails

- Agents never push or merge to `main`, never handle credentials, never touch 🙋 items.
- Only a human merge turns an item ✅. Agents go as far as 🔍.
