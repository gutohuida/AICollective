# Do's and Don'ts for Writing Specs for AI Coding Agents

Synthesized from [`sdd-landscape-report.md`](./sdd-landscape-report.md) (GitHub
Spec Kit, AGENTS.md, CLAUDE.md, Cursor, Windsurf, Cline, Amazon Kiro) and
[`html-spec-conventions.md`](./html-spec-conventions.md) (WHATWG HTML Living
Standard). See those files for full sourcing/citations.

## Do

1. **Separate WHAT/WHY from HOW.** Spec = user-facing behavior, goals,
   constraints. Plan = tech stack, architecture, data model. Keeps specs
   stable across implementation/tech-stack changes. *(Spec Kit; HTML's
   producer/consumer split)*
2. **Write requirements as testable assertions**, using modal verbs
   (MUST/SHOULD/MAY) or EARS syntax (`WHEN [event] THEN [system] SHALL
   [response]`). Avoid vague prose. *(Spec Kit FR-00x; Kiro EARS)*
3. **Make acceptance criteria independently testable**, ideally as
   Given/When/Then scenarios, one per user story/behavior. *(Spec Kit,
   Kiro)*
4. **Mark unresolved ambiguity explicitly** (e.g. `[NEEDS CLARIFICATION:
   question]`) rather than letting the agent guess. Resolve before
   planning/implementation. *(Spec Kit)*
5. **Specify multi-step or conditional behavior as numbered algorithms**,
   not paragraphs — leaves no room for reordering or missed branches.
   *(WHATWG HTML)*
6. **Explain the "why" behind non-obvious rules.** A rule with a stated
   reason generalizes better to edge cases the spec didn't anticipate.
   *(Cline; WHATWG HTML §1.11)*
7. **State explicit non-goals/out-of-scope items**, not just omissions.
   *(WHATWG HTML §1.5)*
8. **Decompose by capability, not technical layer.** Keep durable system context
   (principles, domain map, quality attributes, shared contracts) separate from a
   shallow epic roadmap and independently deliverable feature specs. Each feature
   should have a demonstrable outcome, acceptance tests, an explicit boundary, and
   a dependency position; mark parallel tasks `[P]` only within that boundary.
   *(Spec Kit Spec of Specs; DDD bounded contexts)*
9. **Trace tasks back to requirements by ID** (e.g. `_Requirements: 1.1,
   3.3_`) for auditability. *(Spec Kit, Kiro)*
10. **Make success criteria measurable** ("handles 1000 concurrent users"
    not "is fast"); checklist items should be binary pass/fail. *(Spec Kit)*
11. **Keep day-to-day agent-instruction files (AGENTS.md/CLAUDE.md/
    .cursorrules) short and scannable**; push long reference material into
    linked files. *(Cline, Copilot docs — ~2 pages recommended)*
12. **Use a "constitution"/steering file for immutable architectural
    principles** that gate planning (e.g. simplicity limits,
    test-first, no speculative abstraction), separate from per-feature
    specs. *(Spec Kit constitution.md; Kiro steering files)*
13. **Version specs alongside code** and pick a persistence model up front
    (flow-back / flow-forward / living-spec) so it's clear whether the spec
    or the code is the source of truth after implementation. *(Spec Kit)*
14. **Require explicit approval gates between phases** (requirements →
    design → tasks → implementation) for high-stakes features. *(Kiro)*
15. **Label non-normative content distinctly** (notes, examples, warnings)
    so an agent doesn't treat rationale/illustration as binding
    requirements. *(WHATWG HTML typographic conventions)*

16. **Choose format by audience and job.** Prefer compact Markdown for agent-facing,
    versioned source specs; add semantic, self-contained HTML when humans benefit from
    rendered review, approval, navigation, or complex presentation. *(Anthropic 2026;
    Microsoft Research table-format study)*

## Don't

1. **Don't bake implementation/tech-stack details into the spec.** That
   belongs in the plan; premature commitment makes the spec brittle.
2. **Don't let the agent silently assume unspecified details** — flag and
   resolve them instead.
3. **Don't write vague, subjective rules** ("use descriptive names") without
   a concrete, checkable definition.
4. **Don't add speculative "might need later" features/requirements** —
   every requirement should trace to a concrete need.
5. **Don't produce monolithic, non-decomposable specs** — or split them into
   frontend/API/database documents. Use a roadmap of vertical, independently
   testable capability slices with explicit sibling boundaries instead.
6. **Don't include non-coding tasks** (deployment, user training, marketing)
   in an agent's task list — keep task lists scoped to what the agent
   actually executes.
7. **Don't paste entire style guides or long reference docs into
   instruction files** — they consume context tokens on every turn; link
   out instead.
8. **Don't leave rules without justification** if the rule could plausibly
   seem arbitrary — unexplained rules are more likely to be
   misapplied or dropped over time.
9. **Don't let multiple tools/agents silently overwrite the same context
   file** without a clear ownership/merge convention (a documented failure
   mode in multi-agent setups).
10. **Don't mix normative requirements and illustrative examples/notes in
    the same undifferentiated prose block.**
11. **Don't feed raw webpage HTML to agents as a default.** Strip presentation noise or
    provide the equivalent Markdown; use semantic HTML only where its structure is part
    of the information being reasoned about.
