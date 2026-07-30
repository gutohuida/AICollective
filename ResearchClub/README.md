# ResearchClub

Research and reusable material on **how to build software with AI coding agents** —
specifications, workflows, and the tooling landscape. Transferred here from the
ResearchClub working repo.

## Contents

| Folder | What's inside |
|---|---|
| [`ai-development-workflow/`](ai-development-workflow/) | The practical guide: spec-first vs. incremental, managing specs at scale, the "one spec any LLM can rebuild from" question, a best-practice checklist, and the agent-agnostic **`spec-rebuild`** skill. |
| [`spec-driven-development/`](spec-driven-development/) | The underlying research: full 2025–2026 Spec-Driven Development landscape report (Spec Kit, AGENTS.md, CLAUDE.md, Cursor, Windsurf, Cline, Amazon Kiro), a synthesized do's-and-don'ts checklist, and WHATWG HTML spec conventions. |
| [`agent-operating-model/`](agent-operating-model/) | When one agent beats several, how multi-agent work should be coordinated, and whether permanent agent "roles" make sense. |
| [`ai-delivery-pipeline/`](ai-delivery-pipeline/) | Automating documentation → spec → tickets → AI implementation → AI review → approval: the 2026 tooling landscape, the spec-to-ticket traceability design, and when to build versus rent as platforms absorb the orchestration layer. |

## Start here

- New to the topic? Read
  [`ai-development-workflow/how-to-develop-with-ai.md`](ai-development-workflow/how-to-develop-with-ai.md).
- Want the deep tooling survey? Read
  [`spec-driven-development/sdd-landscape-report.md`](spec-driven-development/sdd-landscape-report.md).
- Automating the delivery chain into Jira/GitHub? Read
  [`ai-delivery-pipeline/`](ai-delivery-pipeline/).
- Have a project and want a rebuild plan? Use the
  [`spec-rebuild`](ai-development-workflow/skills/spec-rebuild/) skill.

## The one-line takeaway

*Spec the shape, build in verifiable slices, review what matters, let code correct the
spec.* Tests are the real executable contract.

Applied to a delivery pipeline, that becomes: *start with the reviewer, not the
implementer — and rent the substrate, own the conventions.*
