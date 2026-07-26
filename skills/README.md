# Skills

Agent skills — a folder containing a `SKILL.md` with YAML frontmatter (`name`,
`description`) and the instructions the agent follows when the skill is invoked.

| Skill | Invoke | Pairs with |
|---|---|---|
| [`handoff`](handoff/) | `/handoff` | `/resume` |
| [`resume`](resume/) | `/resume [path]` | `/handoff` |

Both are written to be **agent-agnostic**: no vendor-specific commands, no assumption about
which CLI is running them. A session started under one agent can be handed off and resumed
under another.

## Where skills are discovered

Several CLI agents converged on the same `SKILL.md` format but not on the same search
paths. Verified against the installed binaries (Claude Code 1.x, Codex 0.145, Kimi 0.28,
OpenCode 1.18):

| Agent | User-level | Project-level |
|---|---|---|
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` |
| **Codex** | `$CODEX_HOME/skills` → `~/.codex/skills/` | *none — user-level only* |
| **Kimi** | `~/.kimi-code/skills/`, `~/.agents/skills/` | `.kimi-code/skills/`, `.agents/skills/` |
| **OpenCode** | `~/.config/opencode/skill{,s}/` | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` |

Two useful facts fall out of that table:

- **`.agents/skills/` is the closest thing to a neutral convention** — Kimi and OpenCode
  both honor it, at user and project level. Claude Code and Codex do not.
- **Codex has no project-level discovery.** A skill only reaches Codex by living in
  `~/.codex/skills/`, so anything you want Codex to have must be installed per-machine,
  not per-repo.

Minimum sets that cover all four:

```
~/.claude/skills/   +  ~/.codex/skills/   +  <project>/.agents/skills/
```

or, if you'd rather keep everything user-level:

```
~/.claude/skills/   +  ~/.codex/skills/   +  ~/.agents/skills/
```

## Install

`install.sh` copies both skills into every agent it detects on the machine:

```bash
./skills/install.sh            # user-level, all detected agents
./skills/install.sh /path/to/repo   # also installs <repo>/.agents/skills/
```

It re-runs safely — copy over an older version any time the skills change here. On Windows,
run it from Git Bash.

Manual equivalent:

```bash
cp -r skills/handoff skills/resume ~/.claude/skills/
cp -r skills/handoff skills/resume ~/.codex/skills/
cp -r skills/handoff skills/resume <project>/.agents/skills/
```

Symlinks keep one source of truth instead of N copies, and are worth it if you're iterating
on the skills:

```bash
ln -s "$PWD/skills/handoff" ~/.claude/skills/handoff
```

```powershell
# Windows: junctions work without admin rights or Developer Mode
cmd /c mklink /J "$HOME\.claude\skills\handoff" "$PWD\skills\handoff"
```

Start a new session afterwards, then invoke `/handoff` to confirm it loaded.

## Notes on the handoff/resume pair

- Handoffs are written to `.handoffs/` in the repo you're working in, with `LATEST.md`
  pointing at the newest so `/resume` has a fixed entry point. If `.claude/handoffs/` or
  `.agents/handoffs/` already exists, the skill keeps using it instead — the chain must not
  split across directories.
- `/resume` searches all three locations, so a handoff written by Claude Code is found by
  Codex and vice versa.
- Handoffs are session notes; gitignoring the directory is usually right.
- Run `/handoff` early — around 50–70% context used, not 95%. The model writing the summary
  is at its least capable exactly when the window is fullest.
- `/handoff` never resets the context itself. It recommends the move and stops; clearing
  stays a user decision.

## Adding a skill here

1. `mkdir skills/<name>` and write `SKILL.md` with `name` + `description` frontmatter.
2. Make the `description` trigger-rich — it's what the agent matches against to decide the
   skill applies. List the phrases a user would actually say.
3. Avoid naming vendor-specific commands in the body if the skill should travel.
4. Add a row to the table above and to the root [`README.md`](../README.md).
