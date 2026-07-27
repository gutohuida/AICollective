# AI Development Workflow

How to build software with AI coding agents: the spec-first vs. incremental question,
how to manage specs as they grow, and a reusable skill for rebuilding any project from
its specs.

## Contents

- [`how-to-develop-with-ai.md`](./how-to-develop-with-ai.md) — The main guide. Consolidated,
  evidence-backed answer to: *should I write the full spec first or build incrementally?*
  Covers the three approaches (vibe coding / spec-driven / hybrid) with hard data, the
  recommended hybrid workflow for a PoC → product, how to manage specs at scale (layered
  constitution + feature specs), whether "one spec any LLM can rebuild from" is realistic,
  a best-practice spec-writing checklist, and the 2025–2026 tooling landscape. Fully
  sourced.
- [`skills/spec-rebuild/`](./skills/spec-rebuild/) — An agent-agnostic skill that locates
  the specs of any project (asking or searching), assesses how rebuildable they are, and
  emits a concrete, best-practice **Rebuild Brief** with tests as the executable contract.

## The one-line answer

*Spec the shape, build in verifiable slices, review what matters, let code correct the
spec.* Neither pure "vibe coding" nor "full spec then generate once" wins for work that
becomes real.

## Related

- [`../spec-driven-development/`](../spec-driven-development/) — The underlying research:
  full 2025–2026 SDD landscape report, do's-and-don'ts checklist, and WHATWG HTML spec
  conventions that inform the best practices used here.

## Using the skill

The skill follows the `SKILL.md` convention (YAML frontmatter + instructions) used by
Claude Code, Codex, Kimi, OpenCode, and other agents. To make it available to an agent,
copy `skills/spec-rebuild/` into that agent's skills directory (e.g. `~/.claude/skills/`,
`~/.codex/skills/`, or a repo's `.agents/skills/`), then invoke it by asking to "rebuild
this project from its specs."
