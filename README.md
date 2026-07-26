# AICollective

A personal — and hopefully shareable — collection of AI material that actually earns its
keep: agent skills, prompts, configs, and notes that have proven useful in real work.

Everything here is meant to be self-contained and copy-pasteable. If a piece of it needs a
long explanation to be useful, that explanation lives next to it.

## What's here

| Section | Contents |
|---|---|
| [`skills/`](skills/) | Claude Code skills (`/slash-command` workflows) |

Planned sections, added when there's something real to put in them: `prompts/`,
`agents/` (subagent definitions), `configs/` (settings, hooks, MCP servers), `notes/`.

## Skills

| Skill | What it does |
|---|---|
| [`handoff`](skills/handoff/) | Write a durable, structured handoff file to disk before `/clear` or `/compact`, so session state survives a context reset. |
| [`resume`](skills/resume/) | Rehydrate from a handoff file, verify it still matches the repo, and continue the work. |

`handoff` and `resume` are a pair. The idea behind them: the file on disk is the real
memory and the context window is scratch space. In-place summarization is lossy and
compounds — a summary of a summary of a summary — while a structured file re-derived from
the live session each time does not.

See [`skills/README.md`](skills/README.md) for installation.

## Contributing

Not accepting drive-by additions yet, but if something here is broken or you have a
sharper version of it, an issue is welcome.

## License

[MIT](LICENSE) — use it, change it, ship it. Attribution appreciated, not enforced.
