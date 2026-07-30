# Repository Skills and the AI-Assisted Development Cycle

**Research date:** 2026-07-29

This note answers two practical questions:

1. What kinds of agent skills are developers checking into repositories?
2. What development cycle do those skills support?

## Short answer

The useful repository skills are not broad personas. They are repeatable,
evidence-producing workflows at important points in the development cycle:

```text
frame → investigate → specify → plan → implement → verify → review
      → ship → deploy-check → learn
```

Do not create a skill for every step merely to complete the diagram. Add one when a
workflow recurs, requires a non-obvious sequence or rubric, and benefits from consistent
inputs and outputs.

## 1. What people are packaging as skills

Current official and popular public skill repositories cluster around these families.

| Skill family | Examples seen in public repositories | Why it earns a skill |
|---|---|---|
| **Problem framing and specification** | idea interrogation, executable spec creation, engineering/design plan review, spec-to-implementation | Repeats a questioning and artifact format before code begins |
| **Investigation and debugging** | root-cause investigation, log triage, Sentry analysis, repository exploration | Enforces evidence gathering before proposing a fix |
| **Framework or platform workflows** | ASP.NET Core, WinUI, Hugging Face CLI, Stripe/API integration, Figma-to-code | Packages domain-specific commands, conventions, references, and tool sequences |
| **Migration and modernization** | migration planning, dependency/API upgrades, repeated transformation playbooks | Applies a canonical pattern with preflight and verification steps |
| **Test and browser QA** | Playwright testing, live browser QA, screenshot comparison, accessibility checks | Requires tool setup, an interaction loop, and observable evidence |
| **Code and PR review** | checklist-based review, addressing review comments, second-opinion review | Gives review a consistent scope, severity model, and output contract |
| **Security** | best-practice review, threat modeling, security ownership mapping, OWASP/STRIDE audit | Uses a specialized rubric and demands exact evidence |
| **CI repair** | inspect GitHub Actions failures, diagnose, patch, rerun | Has a stable fetch-diagnose-fix-verify loop |
| **Release and deployment** | release notes, versioning, PR creation, deploy, canary checks | Coordinates a predictable sequence with explicit safety gates |
| **Documentation** | documentation generation, release documentation, document/PDF workflows | Uses established templates and output standards |
| **Operations and reporting** | incident summary, telemetry analysis, commit/standup summary | Compresses noisy inputs into a stable artifact |
| **Context continuity** | context save/restore, handoff/resume, decision capture | Preserves state across sessions without carrying an entire chat |
| **Safety and scope** | read-only audit, directory edit freeze, destructive-action guard | Enforces a stable operational boundary |

This categorization comes from:

- OpenAI's current curated skills, which include GitHub CI repair and comment handling,
  Playwright, Sentry, security threat modeling, security ownership, deployment, Figma,
  and spec-to-implementation workflows
  ([openai/skills](https://github.com/openai/skills/tree/main/skills/.curated)).
- Anthropic's public skills repository, which includes web application testing, MCP
  generation, design, communication, and production document workflows
  ([anthropics/skills](https://github.com/anthropics/skills)).
- GitHub's own documentation, which uses GitHub Actions failure debugging as its
  project-skill example and supports `.agents/skills`, `.github/skills`, and
  `.claude/skills`
  ([GitHub agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)).
- The popular public `gstack` workflow, which packages product framing, plan review,
  investigation, browser QA, review, shipping, deployment checks, security, performance,
  and context continuity as separate skills
  ([gstack skill catalog](https://github.com/garrytan/gstack/blob/main/AGENTS.md)).

These repositories demonstrate adoption and design patterns, not comparative proof that
every listed skill improves outcomes. Large catalogs can create discovery noise and
ceremony. The goal is to extract the useful workflow boundaries.

## 2. What belongs in the repository

Use the smallest customization surface that matches the information.

| Information or behavior | Correct home |
|---|---|
| One task's goal, constraints, and done conditions | Current prompt, issue, or feature spec |
| Durable repository facts, commands, and invariants | `AGENTS.md` or equivalent project directives |
| Repeatable judgment/process with variable inputs | Repository skill |
| Deterministic check or transformation | Script, test, formatter, linter, or CI job |
| Enforcement around commands or edits | Hook, sandbox, permissions, or CI protection |
| Live external data and controlled actions | MCP server or connector |
| Personal workflow used across unrelated repositories | User-level skill |
| Installable bundle of related skills and integrations | Plugin |

A repository skill is justified when all are true:

1. the team will run it repeatedly;
2. it needs more than a short instruction;
3. its input and deliverable can be named;
4. its method or rubric is repository- or domain-specific;
5. success can be checked;
6. versioning it with the code benefits other contributors or agents.

Do not turn these into skills:

- “write good TypeScript” — this is a vague convention;
- “always run tests” — this belongs in `AGENTS.md` and CI;
- one feature's requirements — this belongs in its spec;
- a command that should execute deterministically — make it a script;
- broad roles such as “senior engineer” — give the primary agent a task and evidence
  standard instead.

OpenAI's current Codex guidance makes the same distinction: use `AGENTS.md` for durable
guidance, skills for repeated workflows, MCP for external context and actions, and
scheduled tasks only after the underlying workflow is reliable. It recommends keeping
each skill to one job, beginning with two or three concrete use cases, and improving the
skill from real failures rather than anticipating every edge case
([Codex skill documentation](https://developers.openai.com/codex/skills/)).

## 3. A lean skill set for this repository

This repository already contains:

- `handoff` and `resume` for context continuity;
- `html-spec` for creating and auditing testable specifications;
- `spec-rebuild` for assessing whether a project can be rebuilt from its artifacts.

That covers continuity and part of the specification phase. The next useful skills would
be:

### 3.1 `investigate`

**Trigger:** a bug, regression, unexplained behavior, or failing test.

**Workflow:**

1. reproduce or establish the symptom;
2. gather logs, history, and relevant execution paths;
3. distinguish observation from hypothesis;
4. test competing hypotheses;
5. identify the smallest supported cause;
6. produce a diagnosis and proposed verification;
7. do not implement unless the task includes a fix.

**Deliverable:** evidence-backed root-cause report or a verified reproduction.

### 3.2 `implement-slice`

Only add this if your desired feature loop contains repository-specific gates that are
not already clear in `AGENTS.md`.

**Trigger:** an approved feature spec or bounded issue.

**Workflow:** locate requirement IDs, inspect analogous code, prepare a short plan, write
or update tests, implement the thinnest vertical slice, run focused and regression
checks, update the spec if behavior changed.

**Deliverable:** a reviewable patch plus requirement-to-test evidence.

If this remains a generic “write code well” workflow, keep it in the primary agent's
normal operating instructions instead of making a skill.

### 3.3 `verify-change`

**Trigger:** implementation is claimed complete.

**Workflow:**

1. derive required checks from changed files and feature acceptance criteria;
2. run fail-to-pass and relevant pass-to-pass tests;
3. run build, type, lint, and static checks;
4. verify visual or browser behavior when applicable;
5. inspect whether tests were weakened or the scope expanded;
6. report commands, outcomes, and unresolved risk.

**Deliverable:** structured verification record, not code changes by default.

### 3.4 `review-change`

**Trigger:** a diff, commit, or PR is ready for review.

**Workflow:** inspect the diff without first accepting the author's narrative; prioritize
correctness, security, regressions, missing tests, and architectural violations; cite
exact evidence; omit style findings handled by automation.

**Deliverable:** severity-ranked findings, each with evidence and a concrete failure
scenario.

### 3.5 `browser-qa`

Add when the repository contains web UI.

**Trigger:** a changed user journey or visual component.

**Workflow:** start the application, exercise the real interaction, capture screenshots,
check responsive and failure states, record reproducible defects, and re-run after fixes.

**Deliverable:** screenshots and a pass/fail table mapped to acceptance criteria.

### 3.6 `ship`

Add only after the preceding steps are stable.

**Trigger:** a verified change approved for delivery.

**Workflow:** confirm clean scope, run required gates, generate the commit/PR summary,
link requirements, identify risk and rollback, then stop at the configured approval
boundary.

**Deliverable:** review-ready PR or release artifact. Deployment remains explicitly
gated.

### 3.7 Later, only when repeated friction appears

- `fix-ci` if CI diagnosis recurs;
- `migration-playbook` for repeated dependency or schema migrations;
- `threat-model` for security-sensitive features;
- `release-notes` if releases have a stable format;
- `deploy-check` or `canary` when production observability is available;
- a framework-specific skill only when the repository has conventions the model cannot
  reliably infer.

Do not build this entire list upfront. Start with `investigate`, `verify-change`, and
`review-change`, because they improve the evidence loop without dictating how every
feature must be implemented.

## 4. Recommended development cycle

### Phase 0: Keep the harness healthy

Before feature work, the agent must be able to:

- install and start the project predictably;
- find the relevant code;
- run focused tests quickly;
- run the full required checks;
- understand failures;
- work inside a bounded environment.

When the same environment failure happens twice, improve the setup, script, project
directive, or skill.

### Phase 1: Frame the outcome

**Human:** owns the problem, priority, risk tolerance, and product acceptance.

**Primary agent:** turns rough intent into:

- goal and user outcome;
- context;
- constraints and non-goals;
- open questions;
- done conditions.

Use `html-spec` or another specification skill when the behavior is non-trivial. Keep
small fixes as clear issues rather than manufacturing a large spec.

**Gate:** the requested outcome is understandable and testable.

### Phase 2: Investigate the existing system

The primary agent reads the relevant implementation, tests, history, and documentation.
Use the `investigate` skill for defects. Temporary read-only workers are acceptable for
independent repository surveys; they return cited evidence.

**Gate:** current behavior and likely change surface are known.

### Phase 3: Plan the smallest vertical slice

Create a short plan that identifies:

- files and interfaces likely to change;
- acceptance criteria and tests;
- risks and decisions;
- dependencies;
- what will not be changed.

Use a second proposal or specialist review only for consequential architectural,
security, or design decisions.

**Human gate:** approve decisions that are expensive to reverse.

### Phase 4: Establish the verification target

Before or alongside implementation:

- reproduce the bug;
- add a failing behavioral test;
- define an expected screenshot or interaction;
- establish a benchmark threshold;
- define a migration dry-run.

The target should fail before the change where practical.

**Gate:** the agent has a feedback signal stronger than “looks done.”

### Phase 5: Implement one coherent slice

The primary agent normally implements the slice in the same context that investigated
and planned it.

Use parallel agents only when modules and contracts are already separable. Each worker
gets:

- explicit ownership;
- a separate worktree or read-only scope;
- a task packet;
- local verification;
- a required artifact.

**Gate:** focused checks pass and the diff remains within scope.

### Phase 6: Verify independently of the implementation narrative

Invoke `verify-change`:

- run focused and regression tests;
- build, type-check, lint, and scan;
- exercise UI behavior;
- inspect changed tests;
- compare results to the acceptance criteria.

The verifier should report evidence. It should not silently fix failures because that
mixes verification with authorship.

**Gate:** every done condition has evidence or is explicitly unresolved.

### Phase 7: Review according to risk

Invoke `review-change` in a fresh context for larger or riskier changes. Add targeted
security, performance, accessibility, or browser QA only when the change warrants it.

The human reviews:

- product behavior;
- architectural judgment;
- sensitive code;
- unresolved risk;
- whether the change should ship.

**Gate:** material findings are resolved and the change is understandable.

### Phase 8: Integrate and ship

Invoke `ship` after verification, not as a replacement for it:

- run the canonical pre-merge checks;
- create a concise PR with requirement and test links;
- let CI repeat deterministic checks;
- require approval proportional to risk;
- merge a small reviewable batch.

Parallel agent output that has not passed review is inventory, not completed work.

### Phase 9: Deploy and observe

For production changes:

- use staged rollout where appropriate;
- verify health, error, and product signals;
- exercise the changed path;
- keep rollback available;
- run a bounded canary or deploy-check workflow.

**Gate:** production evidence matches the expected behavior.

### Phase 10: Learn and encode

After a failure or repeated correction, decide where the learning belongs:

```text
repository fact or invariant  → AGENTS.md
repeated reasoning workflow   → skill
deterministic prevention      → test/script/CI/hook
architectural decision        → ADR/spec
session continuity            → handoff/checkpoint
one-off fact                  → task notes only
```

Do not grow instructions from every preference. Encode high-value patterns demonstrated
by actual friction.

## 5. The cycle in one operating policy

> One primary agent carries each coherent outcome from investigation through
> implementation. Repository skills standardize recurring judgment-heavy checkpoints:
> specification, diagnosis, verification, review, browser QA, shipping, and continuity.
> Tests, scripts, hooks, and CI enforce deterministic rules. Temporary agents are used
> only for bounded parallel or independent work. Humans approve product intent,
> irreversible decisions, sensitive changes, and release risk.
