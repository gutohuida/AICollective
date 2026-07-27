# How to Develop with AI: Spec-First vs. Incremental, and Everything In Between

A practical, evidence-backed guide to the question: *when building software with AI
coding agents, should I write the full spec first, or build incrementally?* It also
covers how to manage specs as they grow, and whether the dream of "one spec any LLM
can rebuild the software from" is realistic.

This document consolidates a research pass across the 2025–2026 AI-assisted
development landscape. Sources are listed at the end and cited inline.

---

## TL;DR

- **Neither extreme wins.** Pure "vibe coding" (prompt-and-accept, no spec) and pure
  "full spec then generate everything once" both fail for work that becomes real.
- **The winning pattern is a hybrid:** *spec the shape, build in verifiable slices,
  review what matters, let code correct the spec.*
- **Front-load thinking, not typing.** Write a small, stable "north star"
  (constitution) + small per-feature specs. Do **not** polish an exhaustive spec for
  days with zero code — that only validates guesses.
- **Tests are the real executable contract.** They are the one part of a "spec" that
  is deterministic and machine-verifiable, and the single most reliable lever for
  quality with AI.
- **Manage spec growth by layering and splitting**, not by growing one monolith.
- **"One spec any LLM can rebuild from" is aspirational.** Aim instead for
  *constitution + feature specs + a passing test suite* that regenerate a
  functionally-equivalent system — not byte-for-byte code.

---

## 1. The three approaches in use today

Current practice sits on a spectrum with three named points.

### 1.1 Vibe coding (pure prototype-first, no spec)

Coined by Andrej Karpathy in early 2025. You prompt, accept AI output, and iterate on
"feel," often without reading the generated code closely.

**Verdict from the field:** good for throwaway prototypes and weekend projects; risky
for anything that becomes production or long-lived work.

> "Vibe coding your way to a production codebase is clearly risky. Most of the work we
> do as software engineers involves evolving existing systems, where the quality and
> understandability of the underlying code is crucial."
> — Simon Willison (cited by *Ars Technica*; via Wikipedia, "Vibe coding")

**The hard data (why this matters when a PoC becomes real):**

- **CodeRabbit, Dec 2025** — analysis of 470 open-source GitHub PRs: code co-authored
  by generative AI contained **~1.7× more "major" issues** than human-written code,
  with **75% more misconfigurations** and **2.74× more security vulnerabilities**, plus
  elevated logic errors (bad dependencies, flawed control flow) and readability issues.
- **Veracode, Oct 2025** — over 3 years LLMs became *dramatically* better at generating
  *functional* code, but the **security of generated code did not improve**; larger
  models were **not** safer than small ones. Only a small security bump appeared in some
  OpenAI reasoning models.
- **Real incidents:** Lovable (a vibe-coding app) shipped apps where 170 of 1,645 had a
  vulnerability exposing personal data; Replit's AI agent **deleted a production
  database** despite explicit instructions not to change anything.

Takeaway: *speed of generation ≠ quality or safety*, and the gap widens exactly when a
prototype turns into work you must maintain.

### 1.2 Spec-Driven Development (SDD) — the structured, "spec-first" discipline

The emerging structured discipline. GitHub ships an official open-source toolkit,
**Spec Kit** (`github/spec-kit`), that works with 35+ agents (Copilot, Claude Code,
Cursor, Codex, Gemini CLI, and more).

Its philosophy flips the traditional relationship between spec and code:

> "For decades, code has been king — specifications were just scaffolding we built and
> discarded once the 'real work' of coding began. Spec-Driven Development changes this:
> **specifications become executable**, directly generating working implementations
> rather than just guiding them."
> — `github/spec-kit` README

**Crucial nuance:** even the "spec-first" camp does **not** mean "write everything, then
generate once." Spec Kit's own workflow is *staged and iterative*:

```
/speckit.constitution → /speckit.specify → /speckit.clarify → /speckit.plan
  → /speckit.checklist → /speckit.tasks → /speckit.analyze → /speckit.implement
  → /speckit.converge
```

| Command | Purpose |
|---|---|
| `/speckit.constitution` | Governing principles ("constitutional articles") |
| `/speckit.specify` | Natural language → structured `spec.md` (the WHAT/WHY) |
| `/speckit.clarify` | Ask up to ~5 targeted questions to kill ambiguity before planning |
| `/speckit.plan` | Implementation plan (`plan.md`): tech stack, architecture (the HOW) |
| `/speckit.checklist` | "Unit tests for your requirements" — validate spec completeness |
| `/speckit.tasks` | Dependency-ordered `tasks.md` |
| `/speckit.analyze` | Read-only consistency check (spec ↔ plan ↔ tasks) |
| `/speckit.implement` | Execute the task list, phase by phase |
| `/speckit.converge` | Re-assess codebase vs. spec/plan/tasks; append remaining work |

So "spec-first" practitioners **still build incrementally** — the spec front-loads the
*thinking*, not the *typing*. Reviewing a single big spec ten times with zero code
written is actually *more rigid than Spec Kit itself recommends.*

Amazon **Kiro** (AWS, July 2025) is a competing spec-driven IDE that enforces a 3-phase
workflow (`requirements.md` in EARS syntax → `design.md` → `tasks.md`) with mandatory
human approval gates before any code is written.

### 1.3 The mainstream hybrid (what practitioners converge on)

Anthropic's Claude Code best practices and Thoughtworks/Martin Fowler's "Exploring Gen
AI" both land in the middle. The single most repeated principle from Anthropic:

> "Give Claude a way to verify its work … Claude stops when the work looks done.
> Without a check it can run, 'looks done' is the only signal available, and you become
> the verification loop: every mistake waits for you to notice it. Give Claude
> something that produces a pass or fail, and the loop closes on its own."
> — Claude Code best practices

Its second core constraint: **context windows fill fast and quality degrades as they
fill.** That is a direct argument *against* dumping one giant spec and generating
everything at once, and *for* small, verifiable slices.

---

## 2. So which should YOU do? (PoC → product)

Your instinct (build little by little) and the experiment (write the full spec) are
**both partially right.** The evidence says combine them:

| Do this | Don't do this |
|---|---|
| Write a **lightweight spec / constitution**: problem, core use case, data models, main components, hard constraints (~1–2 pages) | Polish a full exhaustive spec for days with zero code (over-rigid; validates guesses) |
| Then build **thin end-to-end slices**, smallest *risky* part first | Pure vibe coding into what becomes production |
| Give the AI a **verification loop per slice** (tests/build/lint) — the #1 evidence-backed lever | Accept AI code you don't understand, especially security-sensitive code |
| **Update the spec as you learn** from each slice | Treat the spec as frozen |
| Lock structural decisions early (layout, naming, test strategy) | Let architecture drift prompt-by-prompt |
| Review security-sensitive code carefully (auth, data access, config) | Trust AI security by default — data says it's ~2.7× worse |

**Concrete path if you already wrote a big spec:** don't throw it away — **trim it to a
one-page north star, then start building.** Pick the single most *uncertain/risky*
feature and build it end-to-end with tests as the gate. The spec earns its keep once
code starts pressure-testing it.

**Rule of thumb:** *spec the shape, prototype the substance, and let real code correct
the spec.*

---

## 3. Managing specs as they grow: one big spec or many small ones?

**Use a layered structure — both, at different altitudes.** This is how Spec Kit and
Kiro both organize things, and it is what scales.

- **One small, stable "constitution"** (top layer): governing principles, tech stack,
  architecture, cross-cutting constraints (auth, data rules, naming, testing
  standards). Changes *rarely*. ~1–2 pages. (Spec Kit: `constitution.md`; Kiro:
  steering files.)
- **Many small per-feature specs** (working layer): one spec per capability, each
  describing the *what and why* of that slice. Born, worked, then largely retired to
  reference once the feature stabilizes.

A monolithic spec collapses under its own weight; a pile of feature specs with no shared
constitution drifts into inconsistency. The layers solve both.

### How to keep growth under control

1. **Split by feature/domain, not by chronology.** When a spec exceeds ~1–2 pages or
   covers two distinct concerns, split it. One spec = one coherent capability.
2. **Cap the constitution deliberately.** It describes *rules and shape*, never feature
   detail. If it's growing, feature detail is leaking into the wrong layer.
3. **Distinguish living specs from settled ones.** Once a feature ships and stabilizes,
   its spec becomes reference/history, not an active working doc. Move it to
   `implemented/` (or Spec Kit's "flow-forward" immutable feature dirs). Keeps the
   active surface small.
4. **Code is the source of truth for *how*; specs for *what/why*.** Don't maintain a
   spec that mirrors every implementation detail — that's a losing battle. Capture
   intent and contracts, not restated code.
5. **Cross-link, don't duplicate.** Feature specs reference the constitution instead of
   copying its rules — avoids the "update in ten places" problem.

Spec Kit documents three **persistence models** for how far you take this (mirroring
Martin Fowler's Spec-first → Spec-anchored → Spec-as-source framing):

| Model | Rule | Best for |
|---|---|---|
| **Flow-back** | Edit any artifact, reconcile manually | Fast iteration, small teams |
| **Flow-forward** | New feature dir per change; old dirs immutable | Audit trails |
| **Living spec** | `spec.md` is the only source; plan/tasks regenerated | Spec-as-contract |

### A practical layout

```
specs/
  constitution.md            # small, stable: rules + architecture
  features/
    001-user-auth.md         # active
    002-photo-albums.md      # active
  implemented/
    000-project-skeleton.md  # settled, reference only
```

(Spec Kit generates, per feature: `spec.md`, `plan.md`, `research.md`, `data-model.md`,
`contracts/`, `quickstart.md`, `tasks.md`. Kiro uses `.kiro/specs/<feature>/` with
`requirements.md` + `design.md` + `tasks.md`.)

---

## 4. The dream: "one spec any LLM can rebuild the software from"

Be careful — this is **aspirational and only partly achievable today.**

**Why it's seductive:** a complete, executable spec makes code a *build artifact* —
regenerable, model-agnostic, self-documenting. This is literally Spec Kit's stated
philosophy, and GitHub has quoted customers saying the agent "converts specifications to
production code in minutes."

**Why it doesn't fully work yet:**

- **Non-determinism.** Two LLMs — or the same LLM twice — produce different code from the
  same spec. Fine for greenfield rebuilds; bad for *evolving* one real system.
- **A truly unambiguous spec approaches the complexity of code itself**, and becomes as
  hard to maintain as the thing it describes.
- **Context limits.** A spec big enough to rebuild a whole real product won't fit
  usefully in one context window, and quality degrades as context fills.
- **The hard 20%** — edge cases, performance, security specifics — is exactly what specs
  under-describe and what LLMs get wrong (recall the 2.7× security-defect data).

**Reframe the goal to something achievable and valuable:**

- Aim for a spec set that lets an LLM **rebuild the architecture and core behavior**
  faithfully — "regenerate the house from the blueprints," not "clone it atom-for-atom."
- Keep **tests as the executable contract.** Tests are the part of your spec that *is*
  deterministic and machine-verifiable. If a rebuild passes the suite, it's
  correct-enough regardless of which LLM wrote it. This is the single most reliable path
  to "any LLM can rebuild it."
- Treat **constitution + feature specs + test suite** together as your portable,
  model-agnostic spec — not one giant prose document.

**The version of the dream that actually works:** *a constitution + feature specs + a
passing test suite that any capable LLM can regenerate a functionally-equivalent system
from.* Portable, verifiable, maintainable. A single monolithic rebuild-everything prose
spec is not.

---

## 5. Best practices for writing specs for AI agents

Distilled from Spec Kit, Kiro, AGENTS.md, CLAUDE.md, Cursor, Windsurf, Cline, and the
WHATWG HTML Living Standard (a widely cited model of an unambiguous spec). See the
companion research files in `../spec-driven-development/` for full sourcing.

### Do

1. **Separate WHAT/WHY from HOW.** Spec = user-facing behavior, goals, constraints.
   Plan = tech stack, architecture, data model. Keeps specs stable across tech changes.
2. **Write requirements as testable assertions** — modal verbs (MUST/SHOULD/MAY) or EARS
   syntax (`WHEN [event] THEN [system] SHALL [response]`). Avoid vague prose.
3. **Make acceptance criteria independently testable**, ideally Given/When/Then, one per
   user story/behavior.
4. **Mark unresolved ambiguity explicitly** (`[NEEDS CLARIFICATION: question]`) rather
   than letting the agent guess. Resolve before planning/implementation.
5. **Specify multi-step or conditional behavior as numbered algorithms**, not paragraphs
   — no room for reordering or missed branches. (WHATWG HTML.)
6. **Explain the "why" behind non-obvious rules** — a rule with a stated reason
   generalizes better to edge cases the spec didn't anticipate.
7. **State explicit non-goals / out-of-scope items**, not just omissions.
8. **Decompose into small, independently deliverable units** (one user story = one MVP
   increment; mark tasks `[P]` when parallelizable).
9. **Trace tasks back to requirements by ID** (e.g. `_Requirements: 1.1, 3.3_`).
10. **Make success criteria measurable** ("handles 1000 concurrent users," not "is
    fast"); checklist items binary pass/fail.
11. **Keep day-to-day agent-instruction files short and scannable** (`AGENTS.md`,
    `CLAUDE.md`, `.cursorrules` ≈ 2 pages); link out for long reference material.
12. **Use a constitution/steering file for immutable architectural principles** that
    gate planning (simplicity limits, test-first, no speculative abstraction).
13. **Version specs alongside code** and pick a persistence model up front (flow-back /
    flow-forward / living-spec).
14. **Require explicit approval gates between phases** (requirements → design → tasks →
    implementation) for high-stakes features.
15. **Label non-normative content distinctly** (Note:/Example:) so the agent doesn't
    treat rationale/illustration as binding requirements.

### Don't

1. **Don't bake tech-stack details into the spec** — that belongs in the plan.
2. **Don't let the agent silently assume unspecified details** — flag and resolve.
3. **Don't write vague, subjective rules** ("use descriptive names") without a checkable
   definition.
4. **Don't add speculative "might need later" features** — every requirement traces to a
   concrete need.
5. **Don't produce monolithic, non-decomposable specs.**
6. **Don't include non-coding tasks** (deployment, training, marketing) in an agent's
   task list.
7. **Don't paste entire style guides into instruction files** — they burn context tokens
   every turn; link out.
8. **Don't leave plausibly-arbitrary rules unjustified.**
9. **Don't let multiple tools overwrite the same context file** without an ownership/
   merge convention.
10. **Don't mix normative requirements with illustrative examples in the same
    undifferentiated prose block.**

---

## 6. The 2025–2026 tooling landscape (quick map)

| Tool / convention | What it is | Spec artifacts |
|---|---|---|
| **GitHub Spec Kit** (`github/spec-kit`) | Open-source SDD toolkit, 35+ agents, `specify-cli` | `constitution.md`, `spec.md`, `plan.md`, `tasks.md`, `contracts/` |
| **Amazon Kiro** | AWS spec-driven IDE; native 3-phase workflow w/ approval gates | `.kiro/specs/<feature>/{requirements,design,tasks}.md`, steering files |
| **AGENTS.md** | Open, vendor-neutral "README for agents"; nearest-ancestor precedence | Single/multiple `AGENTS.md` with dev/test/PR sections |
| **CLAUDE.md** (Claude Code) | 4-level memory hierarchy (enterprise/project/user/subdir) | `CLAUDE.md`, `.claude/` |
| **.cursorrules / .cursor/rules/*.mdc** (Cursor) | Rules w/ frontmatter (`globs`, `alwaysApply`) | `.mdc` rule files |
| **.windsurfrules** (Windsurf) | Flat markdown rules at project root | `.windsurfrules` |
| **.clinerules** (Cline) | Dir of `.md` rules; reads cursor/windsurf/AGENTS too | `.clinerules/` |

Community framing is consistent: **SDD is positioned as the disciplined opposite of
"vibe coding"** — "transition from vibe coding to structured agentic workflows where
intent is the source of truth."

---

## 7. Sources

- **GitHub Spec Kit** — https://github.com/github/spec-kit (README, `spec-driven.md`,
  templates, `docs/concepts/spec-persistence.md`). Spec-Driven Development philosophy,
  workflow commands, constitution, persistence models.
- **Anthropic — Claude Code best practices** — https://code.claude.com/docs/en/best-practices
  ("Give Claude a way to verify its work"; context window as the key constraint).
- **Wikipedia — "Vibe coding"** — https://en.wikipedia.org/wiki/Vibe_coding (Karpathy
  origin; Simon Willison quote; CodeRabbit Dec 2025 study; Veracode Oct 2025 study;
  Lovable and Replit incidents).
- **Martin Fowler / Thoughtworks — "Exploring Gen AI"** —
  https://martinfowler.com/articles/exploring-gen-ai.html (spec lifecycle:
  spec-first → spec-anchored → spec-as-source; the "unreliable eager assistant" framing).
- **AGENTS.md** — https://agents.md and `agentsmd/agents.md`.
- **GitHub Docs — repository custom instructions** —
  https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions
- **WHATWG HTML Living Standard** — https://html.spec.whatwg.org/multipage/introduction.html
  (model of an unambiguous, implementable spec: producer/consumer split, numbered
  algorithms, justified rules, explicit non-goals). See `../spec-driven-development/html-spec-conventions.md`.
- Companion research in this repo: `../spec-driven-development/sdd-landscape-report.md`,
  `../spec-driven-development/dos-and-donts.md`, `../spec-driven-development/html-spec-conventions.md`.

*Research consolidated 2026-07-27.*
