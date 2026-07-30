# AI Delivery Pipeline

Research on automating the chain from **documentation → specification → tickets →
AI implementation → AI review → human approval**, and on deciding what to build versus
what to rent when the platforms underneath are moving.

## Contents

| Document | What's inside |
|---|---|
| [`pipeline-landscape.md`](./pipeline-landscape.md) | The 2026 tooling survey, stage by stage: who covers what, which capabilities are GA versus preview, why requirements-traceability review is the differentiator, and the evidence on whether any of it works. |
| [`spec-to-ticket-traceability.md`](./spec-to-ticket-traceability.md) | The design for the one stage nothing packages well: turning a structured spec into traceable tickets, the generation rules, drift detection, and picking a single source of truth. |
| [`platform-or-tool.md`](./platform-or-tool.md) | When to build and when to bridge, now that hosting platforms are absorbing scheduling, task state, approval, audit, and agent distribution. Skills versus systems. |

## Start here

- Choosing tools? [`pipeline-landscape.md`](./pipeline-landscape.md).
- Building the spec→ticket bridge? [`spec-to-ticket-traceability.md`](./spec-to-ticket-traceability.md).
- Wondering whether to fold this into a tool you already built?
  [`platform-or-tool.md`](./platform-or-tool.md).

## The one-line takeaways

**On the pipeline:** *Start with the reviewer, not the implementer* — it is GA, it cannot
break production, and it produces the evidence needed to justify everything after it.

**On traceability:** *Traceability is not bureaucracy; it is the data structure that makes
automated review possible.* Stable requirement IDs are the whole trick.

**On building:** *Rent the substrate, own the conventions.*

## Related

- [`../spec-driven-development/`](../spec-driven-development/) — the spec conventions this
  builds on: decomposition, format selection, testable requirements with stable IDs.
- [`../ai-development-workflow/`](../ai-development-workflow/) — the hybrid spec-first vs.
  incremental guidance, and the quality evidence cited here.
- [`../agent-operating-model/`](../agent-operating-model/) — single vs. multi-agent
  research, and the strategy discussion that [`platform-or-tool.md`](./platform-or-tool.md)
  follows on from.
- [`../../skills/html-spec/`](../../skills/html-spec/) — the applied spec format, including
  the machine contract that makes ticket generation deterministic.

---

*Research pass completed 2026-07-30. Product status claims are version-sensitive and were
verified against first-party documentation on that date.*
