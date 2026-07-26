# Skills

[Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills). Each directory
holds a `SKILL.md` with YAML frontmatter (`name`, `description`) and the instructions
Claude follows when the skill is invoked.

| Skill | Invoke | Pairs with |
|---|---|---|
| [`handoff`](handoff/) | `/handoff` | `/resume` |
| [`resume`](resume/) | `/resume [path]` | `/handoff` |

## Install

Skills are picked up from `~/.claude/skills/` (available in every project) or
`<project>/.claude/skills/` (that project only).

**Copy** — simple, but you maintain two copies:

```bash
# macOS / Linux
cp -r skills/handoff skills/resume ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse skills\handoff, skills\resume $HOME\.claude\skills\
```

**Symlink** — edits here take effect immediately, which is what you want if you're
iterating on the skills themselves:

```bash
# macOS / Linux
ln -s "$PWD/skills/handoff" ~/.claude/skills/handoff
ln -s "$PWD/skills/resume"  ~/.claude/skills/resume
```

```powershell
# Windows (PowerShell, needs Developer Mode or an elevated shell)
New-Item -ItemType SymbolicLink -Path $HOME\.claude\skills\handoff -Target (Resolve-Path skills\handoff)
New-Item -ItemType SymbolicLink -Path $HOME\.claude\skills\resume  -Target (Resolve-Path skills\resume)
```

Start a new Claude Code session afterwards, then run `/handoff` to confirm it's loaded.

## Notes on the handoff/resume pair

- Handoffs are written to `.claude/handoffs/YYYY-MM-DD-HHMM-<slug>.md` inside whatever
  repo you're working in, with `.claude/handoffs/LATEST.md` pointing at the newest one so
  `/resume` has a fixed entry point.
- If the repo tracks `.claude/`, decide whether handoffs belong in git — they're session
  notes, so gitignoring `.claude/handoffs/` is usually right.
- Run `/handoff` early (around 50–70% context used, not 95%). The model writing the
  summary is at its least capable exactly when the window is fullest.
- `/handoff` never runs `/clear` or `/compact` itself; it recommends one and stops. The
  window reset stays a user decision.

## Adding a skill here

1. `mkdir skills/<name>` and write `SKILL.md` with `name` + `description` frontmatter.
2. Make the `description` trigger-rich — it's what Claude matches against to decide the
   skill applies. List the phrases a user would actually say.
3. Add a row to the table above and to the root [`README.md`](../README.md).
