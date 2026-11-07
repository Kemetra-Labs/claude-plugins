# claude-plugins

Cross-project [Claude Code](https://code.claude.com) skills for Kemetra repositories.
Marketplace name: **`kemetra`**.

| Plugin | Skills (invoked as `kemetra-dev:<skill>`) |
| --- | --- |
| `kemetra-dev` | `reviewing-pull-requests`, `triaging-pr-comments`, `requesting-external-review`, `handling-git-and-prs-safely` |

## Skills

| Skill | Use when | Builds on |
| --- | --- | --- |
| `reviewing-pull-requests` | Reviewing a branch, diff or PR (code, tests, migrations, CI, specs, docs) before push, PR or merge | `code-review:code-review` for a plain review; this skill adds severity rules, hunt patterns, a fixed report shape and inline posting |
| `triaging-pr-comments` | Addressing review threads from bots or humans | `superpowers:receiving-code-review` |
| `requesting-external-review` | Getting an independent second opinion on code or a decision | `superpowers:requesting-code-review` |
| `handling-git-and-prs-safely` | Stacked or squash-merged PRs, pruning, worktree removal, stash, reverts | `superpowers:finishing-a-development-branch`, `superpowers:using-git-worktrees` |

The skills are thin overlays: each names the official skill it builds on and adds only what that
skill lacks. A repository's own rules (`CLAUDE.md`) always win over a skill.

## Requires

The overlays point at skills from the official marketplace (`claude-plugins-official`, known to
Claude Code by default): `superpowers@claude-plugins-official` and
`code-review@claude-plugins-official`. Enable them too, in the same `enabledPlugins` block.

## Enable it in a repository (recommended for teams)

Commit this to the repository's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "kemetra": { "source": { "source": "github", "repo": "Kemetra-Labs/claude-plugins" } }
  },
  "enabledPlugins": {
    "kemetra-dev@kemetra": true,
    "superpowers@claude-plugins-official": true,
    "code-review@claude-plugins-official": true
  }
}
```

Anyone who opens the repository in Claude Code and trusts the folder is offered the marketplace
and the plugin.

## Install for yourself

```
/plugin install kemetra-dev --marketplace Kemetra-Labs/claude-plugins
```

or `claude plugin marketplace add Kemetra-Labs/claude-plugins`, then
`claude plugin install kemetra-dev@kemetra`. Run `/reload-plugins` in an open session.

## Develop

```bash
claude --plugin-dir ./plugins/kemetra-dev          # load from disk
claude plugin validate ./plugins/kemetra-dev
claude plugin validate .
python -m unittest discover -s tests -v            # script tests (stdlib only)
```

Rules for changes are in [CLAUDE.md](CLAUDE.md). Every change to a skill is tested without and
with the skill before it ships (`superpowers:writing-skills`); record the runs in
[tests/scenarios.md](tests/scenarios.md). Bump `version` in `plugin.json` on every change, because
installs are cached by version.

## License

MIT, see [LICENSE](LICENSE).
