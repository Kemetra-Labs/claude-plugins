# claude-plugins — agent instructions

Kemetra's cross-project Claude Code skills marketplace (`kemetra`). Project-only skills live in
each repository's own `.claude/skills/`; machine-only notes stay in a person's `~/.claude/`.

## Rules for skills here

- **Thin overlays.** Each skill names the official skill it builds on (`superpowers:*`,
  `code-review:*`, ...) and never copies that skill's text. Add only what the official skill lacks.
- **Names:** verb-ing + object (`reviewing-pull-requests`), letters, digits and hyphens.
  Descriptions start with "Use when" and list triggers, not the workflow.
- **No secrets, no personal or laptop paths, no single-machine workarounds** (signing agents,
  local shells, OS ACL fixes). Those belong in a personal overlay.
- **No repository policy.** Merge rules, required checks and approval rules belong to the
  consuming repository's `CLAUDE.md`. A skill must not contradict them.
- **Tested before shipping.** Run each changed skill's scenarios without and with the skill
  (`superpowers:writing-skills`) and record both in `tests/scenarios.md`.
- **`reviewing-pull-requests` is evaluated in rounds.** Change its text only in an evaluation
  round; defects it missed are logged for the next round, not patched ad hoc.
- Bump `plugins/<name>/.claude-plugin/plugin.json` `version` on any change.

## Verify before claiming done

`claude plugin validate ./plugins/kemetra-dev`, `claude plugin validate .`,
`python -m unittest discover -s tests -v`, and a `claude --plugin-dir ./plugins/kemetra-dev`
session that lists the `kemetra-dev:*` skills.

## Git

Commit format `<type>: <description>` (feat, fix, refactor, docs, test, chore, perf, ci).
Stage explicit paths, never `git add -A`. Changes land by PR to `main`; no force-push to `main`.
