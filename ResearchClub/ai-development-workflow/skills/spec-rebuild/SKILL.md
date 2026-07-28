---
name: spec-rebuild
description: Locate the specifications of any project (asking where they live or searching the repo) and produce a concrete, best-practice plan for how an AI agent should rebuild the software from them. Use when the user says "rebuild from spec", "how would you rebuild this", "regenerate this project from its specs", "read the specs and tell me how to build it", "spec rebuild", "reconstruct this from the spec", or wants a portable, model-agnostic build brief derived from existing specs, requirements, plans, or design docs.
---

Read a project's specifications and turn them into a concrete, ordered plan for
rebuilding the software from scratch — following spec-driven best practices and using
tests, contracts, fixtures, and operational artifacts as evidence of intended behavior.

**Core principle:** a spec set can only rebuild *architecture and core behavior*
faithfully, not byte-for-byte code. The strongest available contract is **governing
principles + feature specs + executable checks + data/API/operational contracts**. A
passing test suite proves only the behavior it covers. Your job is to find this evidence,
judge how rebuildable it is, and emit a plan that closes the gaps.

Agent-agnostic: works in any CLI agent that can read files and run shell commands. Where
this file says "search the repo", use whatever search tools you have (glob/grep/find).

## Step 0 — Locate the specs

Do not guess where specs live. Establish it deterministically:

1. **If the user named a location, use it.** Otherwise search the repo for the usual
   homes, in roughly this priority:

   ```
   specs/            .specify/         .kiro/specs/       docs/specs/
   spec.md  plan.md  tasks.md  requirements.md  design.md  constitution.md
   AGENTS.md  CLAUDE.md  GEMINI.md  .cursor/rules/  .cursorrules  .clinerules
   .devin/rules/  .windsurf/rules/  .windsurfrules
   .github/copilot-instructions.md   docs/   ADR*/  adr/  README.md
   ```

2. **Distinguish specifications from agent instructions.** `AGENTS.md`, `CLAUDE.md`, and
   tool rule files may supply constraints and commands, but they are not automatically
   feature specifications. Report them separately as governing/context artifacts.

3. **Report what you found** as a short inventory before doing anything else.

4. **If nothing spec-like is found, ask the user** exactly one question: where the
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
| **Executable contract** | test suites, fixtures, OpenAPI/contract tests, schema/migration checks | Machine-verifiable behavior and compatibility |
| **Operational contract** | environment templates, IaC, deployment/runbooks, SLOs | Runtime assumptions and service behavior |
| **Reference / history** | ADRs, `implemented/`, changelogs | Decisions already settled |

List every file by path with its role and a one-line summary. Note anything that is
**missing** — especially executable checks, contracts, fixtures, or operational
configuration needed to validate a rebuild.

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
- [ ] **A system map and epic roadmaps exist where needed** — durable system context,
  shared contracts, and domain ownership are separate from feature-level work; each
  roadmap slice states intent, in/deferred scope, dependencies, status, and a child-spec link.
- [ ] **An executable contract exists** — a test suite (or contract tests) the rebuild can be checked against.
- [ ] **Coverage limits are known** — important untested behavior, fixtures, external integrations, and migration paths are identified.
- [ ] **Operational assumptions are captured** — configuration, deployment, observability, and data-migration needs are documented or explicitly out of scope.
- [ ] **Non-obvious rules are justified** — a stated "why" so edge cases generalize correctly.
- [ ] **Persistence model is explicit** — decide whether artifacts are living, flow-forward/immutable, or reconciled manually after changes.

Summarize as a **rebuildability verdict**: *High* (specs + tests can regenerate a
functionally-equivalent system), *Medium* (architecture/behavior recoverable but edge
cases and security will drift), or *Low* (specs are aspirational prose; a rebuild would
diverge significantly). State the top 3 gaps driving the verdict.

## Step 3 — Produce the rebuild plan

Write an ordered, model-agnostic plan a *fresh* agent could follow with no prior context.
Follow these best practices explicitly:

1. **Establish the governing constraints first.** Restate (or, if missing, propose) the
   durable principles: tech stack, architecture style, testing standard, security
   constraints, and simplicity limits. Version and change these deliberately; they guide
   the work but do not enforce themselves.
2. **Rebuild in thin, vertical, end-to-end slices** — smallest *riskiest* capability
   first, not layer-by-layer. Each slice is independently demonstrable.
   For a large system, first produce a shallow roadmap: keep the system map (vision,
   principles, domain map, quality attributes, and shared contracts) separate from
   ordered feature slices. Do not split into frontend/API/database specs. Give every
   slice an immutable ID, one-line intent, in/deferred boundary, dependencies, and a
   link to its own spec. Split again only when a slice is not independently testable or
   no longer fits safely in one implementation cycle.
3. **Give every slice a verification loop.** State the exact check that closes the loop
   (run the test suite / build / lint / contract test). If existing behavior is available,
   first write characterizing tests. If it is not, derive requirement tests from approved
   acceptance criteria and label their coverage as proposed rather than observed.
4. **Order by dependency**, mark parallelizable work `[P]`, and trace each task back to a
   requirement ID where one exists.
5. **Call out elevated-review areas** — auth, authorization, data access, payments,
   configuration, migrations, and privacy/security-sensitive behavior. Require an
   appropriate human review and evidence beyond a superficial code read.
6. **Choose and record the spec persistence model** — living artifacts, immutable
   flow-forward feature records, or a documented manual reconciliation process.
7. **Flag every ambiguity** you must resolve to proceed, as an explicit question — never
   silently assume.

## Step 4 — Output

Produce a single **Rebuild Brief** with these sections:

```markdown
# Rebuild Brief: <project name>

## Spec sources found
<inventory from Step 1 — paths + roles>

## Rebuildability verdict: <High | Medium | Low>
<one paragraph + top 3 gaps>

## Evidence and coverage limits
<which tests/contracts/fixtures/operational artifacts were checked, and what they do not prove>

## Constitution (the non-negotiables)
<restated or proposed>

## Rebuild plan (ordered, verifiable slices)
1. <slice> — build: <what> · verify: <exact check> · requirements: <ids>
2. ...

## Human-review checkpoints
<security/data/config items that must not pass on "looks done">

## Spec lifecycle
<chosen persistence model and how implementation changes update the artifacts>

## Open questions (blockers)
<explicit clarifications needed before starting>
```

Keep the brief self-contained: a different agent, with different tools, should be able to
execute step 1 immediately with no access to this conversation. Do not start writing
application code as part of this skill — the deliverable is the brief. Offer to proceed
with implementation as a separate, explicit next step.

See `../how-to-develop-with-ai.md` and `../../spec-driven-development/` for the research
and best-practice sourcing behind this skill.
