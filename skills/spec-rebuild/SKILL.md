---
name: spec-rebuild
description: Locate the specifications of any project (asking where they live or searching the repo) and produce a concrete, best-practice plan for how an AI agent should rebuild the software from them. Use when the user says "rebuild from spec", "how would you rebuild this", "regenerate this project from its specs", "read the specs and tell me how to build it", "spec rebuild", "reconstruct this from the spec", or wants a portable, model-agnostic build brief derived from existing specs, requirements, plans, or design docs.
---

Read a project's specifications and turn them into a concrete, ordered plan for
rebuilding the software from scratch — following spec-driven best practices, and using
tests as the executable contract.

**Core principle:** a spec set can only rebuild *architecture and core behavior*
faithfully, not byte-for-byte code. The reliable contract is **constitution + feature
specs + a passing test suite**. Your job is to find those pieces, judge how rebuildable
they are, and emit a plan that closes the gaps.

Agent-agnostic: works in any CLI agent that can read files and run shell commands. Where
this file says "search the repo", use whatever search tools you have (glob/grep/find).

## Step 0 — Locate the specs

Do not guess where specs live. Establish it deterministically:

1. **If the user named a location, use it.** Otherwise search the repo for the usual
   homes, in roughly this priority:

   ```
   specs/            .specify/         .kiro/specs/       docs/specs/
   spec.md  plan.md  tasks.md  requirements.md  design.md  constitution.md
   AGENTS.md  CLAUDE.md  GEMINI.md  .cursor/rules/  .cursorrules  .clinerules  .windsurfrules
   .github/copilot-instructions.md   docs/   ADR*/  adr/  README.md
   ```

2. **Report what you found** as a short inventory before doing anything else.

3. **If nothing spec-like is found, ask the user** exactly one question: where the
   specs reside, or whether they want you to *derive* a spec from the existing code
   instead (a different mode — say so). Do not fabricate a spec location.

## Step 1 — Inventory and classify

For each artifact found, classify it into one of these roles (a project rarely has all):

| Role | Typical files | Answers |
|---|---|---|
| **Constitution / principles** | `constitution.md`, steering files, `AGENTS.md`, `CLAUDE.md`, rules files | Architectural rules, tech stack, non-negotiables |
| **Feature specs (WHAT/WHY)** | `spec.md`, `requirements.md`, user stories | User-facing behavior, acceptance criteria |
| **Plans / design (HOW)** | `plan.md`, `design.md`, `data-model.md`, `contracts/` | Architecture, data model, APIs |
| **Task lists** | `tasks.md` | Ordered, dependency-aware work items |
| **Executable contract** | test suites, fixtures, OpenAPI/contract tests | Machine-verifiable correctness |
| **Reference / history** | ADRs, `implemented/`, changelogs | Decisions already settled |

List every file by path with its role and a one-line summary. Note anything that is
**missing** — especially a test suite, since that is the load-bearing part of a
rebuildable spec.

## Step 2 — Assess rebuildability

Score the spec set honestly against this checklist. For each, mark ✅ / ⚠️ / ❌ and give a
one-line reason:

- [ ] **WHAT/WHY separated from HOW** — specs describe behavior; tech choices live in a plan.
- [ ] **Requirements are testable assertions** — MUST/SHOULD or EARS (`WHEN … THEN … SHALL …`), not vague prose.
- [ ] **Acceptance criteria are independently testable** — Given/When/Then per behavior.
- [ ] **Ambiguities are marked, not guessed** — `[NEEDS CLARIFICATION]` or equivalent; none left unresolved.
- [ ] **Non-goals / out-of-scope stated explicitly.**
- [ ] **Success criteria are measurable** (binary pass/fail, concrete numbers).
- [ ] **Decomposed into small, independently deliverable units.**
- [ ] **A layered structure exists** — a stable constitution + per-feature specs, not one monolith.
- [ ] **An executable contract exists** — a test suite (or contract tests) the rebuild can be checked against.
- [ ] **Non-obvious rules are justified** — a stated "why" so edge cases generalize correctly.

Summarize as a **rebuildability verdict**: *High* (specs + tests can regenerate a
functionally-equivalent system), *Medium* (architecture/behavior recoverable but edge
cases and security will drift), or *Low* (specs are aspirational prose; a rebuild would
diverge significantly). State the top 3 gaps driving the verdict.

## Step 3 — Produce the rebuild plan

Write an ordered, model-agnostic plan a *fresh* agent could follow with no prior context.
Follow these best practices explicitly:

1. **Establish the constitution first.** Restate (or, if missing, propose) the immutable
   principles: tech stack, architecture style, testing standard, security constraints,
   simplicity limits. This gates everything after it.
2. **Rebuild in thin, vertical, end-to-end slices** — smallest *riskiest* capability
   first, not layer-by-layer. Each slice is independently demonstrable.
3. **Give every slice a verification loop.** State the exact check that closes the loop
   (run the test suite / build / lint / contract test). If no tests exist, the plan's
   **first task is to write the characterizing tests** — they are the contract.
4. **Order by dependency**, mark parallelizable work `[P]`, and trace each task back to a
   requirement ID where one exists.
5. **Call out the hard 20% for human review** — auth, data access, payments, config,
   anything security-sensitive. AI-generated code here is materially more defect-prone;
   do not let it pass on "looks done" alone.
6. **Flag every ambiguity** you must resolve to proceed, as an explicit question — never
   silently assume.

## Step 4 — Output

Produce a single **Rebuild Brief** with these sections:

```markdown
# Rebuild Brief: <project name>

## Spec sources found
<inventory from Step 1 — paths + roles>

## Rebuildability verdict: <High | Medium | Low>
<one paragraph + top 3 gaps>

## Constitution (the non-negotiables)
<restated or proposed>

## Rebuild plan (ordered, verifiable slices)
1. <slice> — build: <what> · verify: <exact check> · requirements: <ids>
2. ...

## Human-review checkpoints
<security/data/config items that must not pass on "looks done">

## Open questions (blockers)
<explicit clarifications needed before starting>
```

Keep the brief self-contained: a different agent, with different tools, should be able to
execute step 1 immediately with no access to this conversation. Do not start writing
application code as part of this skill — the deliverable is the brief. Offer to proceed
with implementation as a separate, explicit next step.

See `../../ResearchClub/ai-development-workflow/how-to-develop-with-ai.md` and
`../../ResearchClub/spec-driven-development/` for the research and best-practice sourcing
behind this skill.
