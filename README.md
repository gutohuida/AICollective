# AICollective

A personal — and hopefully shareable — collection of AI material that actually earns its
keep: agent skills, prompts, configs, and notes that have proven useful in real work.

Everything here is meant to be self-contained and copy-pasteable. If a piece of it needs a
long explanation to be useful, that explanation lives next to it.

## What's here

| Section | Contents |
|---|---|
| [`skills/`](skills/) | Claude Code skills (`/slash-command` workflows) |
| [`ResearchClub/`](ResearchClub/) | Research on building software with AI agents: spec-driven development, the spec-first vs. incremental question, and a `spec-rebuild` skill. |

Planned sections, added when there's something real to put in them: `prompts/`,
`agents/` (subagent definitions), `configs/` (settings, hooks, MCP servers), `notes/`.

## Skills

| Skill | What it does |
|---|---|
| [`handoff`](skills/handoff/) | Write a durable, structured handoff file to disk before `/clear` or `/compact`, so session state survives a context reset. |
| [`resume`](skills/resume/) | Rehydrate from a handoff file, verify it still matches the repo, and continue the work. |
| [`html-spec`](skills/html-spec/) | Audit and improve an HTML specification, or write one from scratch — testable requirements with stable IDs, traceability from requirement to task, and a bundled structural validator. |

`handoff` and `resume` are a pair. The idea behind them: the file on disk is the real
memory and the context window is scratch space. In-place summarization is lossy and
compounds — a summary of a summary of a summary — while a structured file re-derived from
the live session each time does not.

Both are agent-agnostic. Claude Code, Codex, Kimi, and OpenCode have all converged on the
same `SKILL.md` format, so the *files* are portable — but each looks in different
directories, and Codex only reads user-level ones. `skills/install.sh` handles the spread:

```bash
./skills/install.sh                  # every agent detected on this machine
./skills/install.sh /path/to/repo    # plus that repo's .agents/skills/
```

Because they don't name any vendor-specific command, a session handed off under one agent
can be resumed under another. See [`skills/README.md`](skills/README.md) for the full
discovery table and manual install.

`html-spec` is the applied end of [`ResearchClub/`](ResearchClub/): the conventions the
research validated, packaged as a rubric an agent can run against a real document —
plus `validate.py`, which catches the structural failures (dead anchors, untraced tasks,
external resources, an approved spec with open questions) that a careful read usually misses.

## Contributing

Not accepting drive-by additions yet, but if something here is broken or you have a
sharper version of it, an issue is welcome.

## License

[MIT](LICENSE) — use it, change it, ship it. Attribution appreciated, not enforced.
