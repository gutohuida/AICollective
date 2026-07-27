# Spec-Driven Development (SDD) for AI Coding Agents: 2025–2026 Research Report

## Summary

Spec-Driven Development (SDD) for AI coding agents has emerged as the dominant paradigm for structuring autonomous software engineering in 2025–2026. Rather than supplying ad-hoc prompts, teams now author *structured specification artifacts* — requirements documents, implementation plans, and task lists — that serve as the primary source of truth, with AI agents treating code as a derived, regenerable output. This report covers the canonical tooling (GitHub Spec Kit), the emerging cross-tool AGENTS.md standard, all major vendor-specific instruction files, Amazon Kiro's competing spec-driven IDE, and documented best practices.

---

## 1. GitHub Spec Kit (`github/spec-kit`)

### Overview

**Repository:** [`github/spec-kit`](https://github.com/github/spec-kit) (MIT License, actively maintained as of July 2026)

GitHub Spec Kit is an open-source toolkit for implementing Spec-Driven Development with any AI coding agent. It is bootstrapped via the **`specify-cli`** Python package and is heavily influenced by the research of [John Lam](https://github.com/jflam).

**Self-description** (`github/spec-kit:README.md:1-9`):
> *"An open source toolkit for building high-quality software with any AI coding agent — a ready-to-use spec-driven process (or bring your own), endlessly extensible, community-driven, and built for your whole organization."*

> *"Spec-Driven Development flips the script on traditional software development. For decades, code has been king — specifications were just scaffolding we built and discarded once the 'real work' of coding began. Spec-Driven Development changes this: **specifications become executable**, directly generating working implementations rather than just guiding them."*
>
> — `github/spec-kit:README.md:39-41`

### Installation

```bash
uv tool install specify-cli   # from PyPI
specify init my-project --integration copilot   # scaffold a project
```
(`github/spec-kit:README.md:45-66`)

### Core Workflow Commands

Spec Kit exposes slash commands (and agent-skill equivalents) for a fully ordered pipeline (`github/spec-kit:docs/reference/agentic-sdd.md:8`):

```
/speckit.constitution → /speckit.specify → /speckit.clarify → /speckit.plan
  → /speckit.checklist → /speckit.tasks → /speckit.analyze → /speckit.implement → /speckit.converge
```

| Command | Purpose |
|---|---|
| `/speckit.constitution` | Create or update project governing principles ("constitutional articles") |
| `/speckit.specify` | Transform a natural-language description into a structured `spec.md` |
| `/speckit.clarify` | Ask up to 5 targeted questions to resolve ambiguity before planning |
| `/speckit.plan` | Generate an implementation plan (`plan.md`) from the spec, given tech-stack constraints |
| `/speckit.checklist` | "Unit tests for your requirements" — validate spec completeness |
| `/speckit.tasks` | Generate a dependency-ordered `tasks.md` task list |
| `/speckit.analyze` | Read-only cross-artifact consistency check (spec ↔ plan ↔ tasks) |
| `/speckit.implement` | Execute the task list, phase by phase |
| `/speckit.converge` | Assess codebase against spec/plan/tasks; append remaining work if gaps found |

For agents using a skills/CLI model (e.g. OpenAI Codex), the same commands are invoked as `$speckit-*` or `/skill:speckit-*`. Source: `github/spec-kit:README.md:157-184`; `github/spec-kit:docs/reference/agentic-sdd.md`.

### Directory Structure Generated

When you run `/speckit.specify` for a feature, Spec Kit creates:

```
specs/
└── 003-chat-system/
    ├── spec.md          ← human intent: user stories + acceptance criteria
    ├── plan.md          ← technical plan: architecture, data model, dependencies
    ├── research.md      ← technology/library research
    ├── data-model.md    ← entity definitions
    ├── contracts/       ← API contracts, OpenAPI specs
    ├── quickstart.md    ← key validation scenarios
    └── tasks.md         ← actionable task checklist
```
(`github/spec-kit:spec-driven.md:127-142`)

### Spec Template Structure (`templates/spec-template.md`)

The spec template enforces a specific structure designed to constrain LLM output (`github/spec-kit:templates/spec-template.md`):

```markdown
# Feature Specification: [FEATURE NAME]
**Status**: Draft

## User Scenarios & Testing  ← mandatory; independently testable user stories
### User Story 1 - [Brief Title] (Priority: P1)
**Acceptance Scenarios**:
1. **Given** [initial state], **When** [action], **Then** [expected outcome]

## Requirements  ← mandatory
### Functional Requirements
- **FR-001**: System MUST [specific capability]
- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method...]

### Key Entities  ← if feature involves data

## Success Criteria  ← mandatory; measurable outcomes
- **SC-001**: [Measurable metric, e.g., "Users can complete X in under 2 minutes"]

## Assumptions
```

**Key anti-patterns the template explicitly prevents:**
- `✅ Focus on WHAT users need and WHY` / `❌ Avoid HOW to implement (no tech stack, APIs, code structure)`
- `[NEEDS CLARIFICATION]` markers for any unspecified details (prevents LLM guessing)
- No speculative features — every feature must trace back to a concrete user story
(`github/spec-kit:spec-driven.md:169-260`)

### Task Template Structure (`templates/tasks-template.md`)

Tasks are organized **by user story** into phases:

```markdown
## Phase 1: Setup (Shared Infrastructure)
## Phase 2: Foundational (Blocking Prerequisites)
## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP
- [ ] T010 [P] [US1] Contract test for [endpoint]    # [P] = can run in parallel
- [ ] T012 [P] [US1] Create [Entity1] model
- [ ] T014 [US1] Implement [Service] (depends on T012, T013)
## Phase N: Polish & Cross-Cutting Concerns
```
(`github/spec-kit:templates/tasks-template.md`)

### The Constitution (`templates/constitution-template.md`)

The constitution is a file of immutable architectural principles that gates every planning step. The built-in nine articles of Spec Kit's own constitution include:

- **Article I: Library-First** — every feature starts as a standalone library
- **Article II: CLI Interface** — every library exposes text-based CLI interface (stdin→stdout, JSON support)
- **Article III: Test-First (NON-NEGOTIABLE)** — TDD: tests written, approved, and confirmed failing *before* implementation
- **Articles VII & VIII: Simplicity & Anti-Abstraction** — max 3 projects; YAGNI; no unnecessary abstractions
- **Article IX: Integration-First** — prefer real databases over mocks; contract tests before implementation
(`github/spec-kit:spec-driven.md:278-393`)

Articles IV, V, VI are intentionally left for each project to define.

### Spec Persistence Models

Spec Kit documents three official models for how spec artifacts evolve (`github/spec-kit:docs/concepts/spec-persistence.md`):

| Model | Rule | Best For |
|---|---|---|
| **Flow-back** | Edit any artifact, reconcile manually | Fast iteration, small teams |
| **Flow-forward** | New feature directory per change; old dirs immutable | Audit trails |
| **Living spec** | `spec.md` is the only source; plan/tasks are regenerated | Spec-as-contract |

This mirrors terminology from Martin Fowler's article at `martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html` (referenced in `github/spec-kit:docs/concepts/spec-persistence.md`), which frames the lifecycle as: Spec-first → Spec-anchored → Spec-as-source.

### Supported Agents

As of July 2026, Spec Kit's catalog (`github/spec-kit:integrations/catalog.json`) supports **35 agents**, including:

Claude Code, Cline, GitHub Copilot, Gemini CLI, Cursor, Codex CLI, Devin, opencode, Qwen Code, Junie (JetBrains), Auggie, Amp, Zed, Goose (Block), Grok Build (xAI), RovoDev (Atlassian), IBM Bob, Trae, Tabnine, Kilo Code, Kimi Code (Moonshot AI), ZCode (Z.AI), Hermes (Nous Research), Windsurf (via generic), Antigravity, Mistral Vibe, Firebender (Android Studio), and a `generic` integration for any agent.

---

## 2. AGENTS.md Convention

### What It Is

**Website:** [agents.md](https://agents.md)
**Repository:** [`agentsmd/agents.md`](https://github.com/agentsmd/agents.md)

AGENTS.md is an **open, vendor-neutral standard** for providing instructions to AI coding agents — described as *"a README for agents: a dedicated, predictable place to provide context and instructions to help AI coding agents work on your project."*

(`agentsmd/agents.md:README.md:1-5`)

> *"Think of AGENTS.md as a README for agents."*

### How It Differs from README.md

| Feature | README.md | AGENTS.md |
|---|---|---|
| Audience | Human contributors | AI coding agents |
| Focus | Project overview, getting started | Dev environment tips, test commands, PR workflow |
| Placement | Root of repository | Root, or any directory (nearest ancestor wins) |
| Format | Freeform markdown | Structured sections with machine-actionable commands |

### Canonical Sections

The reference example from `agentsmd/agents.md:README.md:16-46`:

```markdown
## Dev environment tips
- Use `pnpm dlx turbo run where <project_name>` to jump to a package...

## Testing instructions
- Run `pnpm turbo run test --filter <project_name>` to run tests.
- Fix any test or type errors until the whole suite is green.
- Add or update tests for the code you change, even if nobody asked.

## PR instructions
- Title format: [<project_name>] <Title>
- Always run `pnpm lint` and `pnpm test` before committing.
```

### Which Tools Honor AGENTS.md

- **OpenAI Codex CLI** — reads AGENTS.md natively; Codex's own AGENTS.md in `openai/codex` is extensive (`openai/codex:AGENTS.md`)
- **GitHub Copilot** — explicitly supports AGENTS.md as one of its three custom instruction types; nearest ancestor in the directory tree takes precedence (source: GitHub Docs, fetched 2026-07-20)
- **Cline** — reads `AGENTS.md` at project root and `~/.agents/AGENTS.md` for global rules (`cline/cline:docs/customization/cline-rules.mdx`)
- **Spec Kit** — the `github/spec-kit` repo itself ships an `AGENTS.md` (21 KB) for agent contributors working on the toolkit (`github/spec-kit:AGENTS.md`)

GitHub's docs explicitly state: *"You can create one or more AGENTS.md files, stored anywhere within the repository. When Copilot is working, the nearest AGENTS.md file in the directory tree will take precedence."* — [GitHub Docs on custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions), fetched 2026-07-20.

---

## 3. Vendor-Specific Instruction Files

### 3a. CLAUDE.md (Anthropic / Claude Code)

**Tool:** [Claude Code](https://github.com/anthropics/claude-code) CLI by Anthropic
**File:** `CLAUDE.md` (at project root, or `.claude/CLAUDE.md`)

Claude Code reads a **4-level memory hierarchy**:
1. **Enterprise** — `/Library/Application Support/ClaudeCode/CLAUDE.md` (org-wide)
2. **Project** — `CLAUDE.md` at repository root (team-shared)
3. **User** — `~/.claude/CLAUDE.md` (personal preferences across all projects)
4. **Sub-directory** — `.claude/` directory files

(Source: community CLAUDE.md examples, e.g. `VAMFI/claude-user-memory:CLAUDE.md`)

**What a well-structured CLAUDE.md contains** (from real-world example `pdfme/pdfme:CLAUDE.md`):

```markdown
# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
[Brief description of what the project does]

## Environment Requirements
- Node.js: Version 16+ (recommended: 18+)
- Package Manager: npm 8+

## Common Development Commands
```bash
npm install         # Install dependencies
npm run build       # Build all packages
npm run test        # Run tests
npm run lint        # Lint
```

## Architecture and Code Structure
- packages/common: Core types and utilities
- packages/ui: React components

## Key Files to Understand
- packages/common/src/types.ts: Core type definitions
```

**Spec Kit integration:** Spec Kit provides an opt-in `agent-context` extension that manages a `<!-- SPECKIT START -->` / `<!-- SPECKIT END -->` section in `CLAUDE.md`, keeping it synchronized with the active spec context (`github/spec-kit:AGENTS.md:177-193`).

---

### 3b. `.cursorrules` / `.cursor/rules/*.mdc` (Cursor IDE)

**Tool:** [Cursor](https://cursor.sh/) AI code editor
**File evolution:** Legacy `.cursorrules` → Modern `.cursor/rules/*.mdc`

**Community resource:** [`PatrickJS/awesome-cursorrules`](https://github.com/PatrickJS/awesome-cursorrules) (the largest curated collection)

Modern Cursor uses **`.mdc` (Markdown with Config)** files in `.cursor/rules/`:

```markdown
---
description: One-line summary of what this rule does
globs: **/*.ts, **/*.tsx
alwaysApply: false
---

# Rule Content Here

- Use TypeScript for all new files
- Prefer composition over inheritance
```

**Frontmatter fields:**
- `description` — explains the rule to Cursor and contributors
- `globs` — file patterns where the rule auto-attaches
- `alwaysApply: false` — keeps rule scoped to matching context; `true` for universal guidance

(Source: `PatrickJS/awesome-cursorrules:README.md`, fetched 2026-07-20)

Cline also automatically detects `.cursorrules` files for compatibility (`cline/cline:docs/customization/cline-rules.mdx`).

---

### 3c. `.windsurfrules` (Windsurf / Codeium)

**Tool:** [Windsurf](https://codeium.com/windsurf) IDE by Codeium
**File:** `.windsurfrules` at project root (also `.windsurfrules.md` variant seen in the wild)

Windsurf rules follow a similar convention to `.cursorrules` — a flat markdown file at the project root containing agent behavior instructions. From community examples (`mrbizarro/phosphene:.windsurfrules`; `Rick-te-Molder/bfsi-insights:.windsurfrules`):

```markdown
# BFSI Insights Coding Practices (.windsurfrules)
Project-specific rules for AI assistants (Windsurf/Cursor).
These rules exist because bugs, incidents, and CI failures happened.

**Quality System**: This file implements controls from [docs/architecture/quality-system.md].
```

Cline also automatically detects `.windsurfrules` files (`cline/cline:docs/customization/cline-rules.mdx`).

---

### 3d. `.github/copilot-instructions.md` (GitHub Copilot)

**Tool:** GitHub Copilot (IDE, github.com/copilot, coding agent)
**Files:** Three types of custom instructions supported as of 2026:

#### Type 1: Repository-Wide Instructions
**File:** `.github/copilot-instructions.md`

Applies to all requests in the context of the repository. GitHub even provides a prompt to have Copilot's cloud agent generate this file automatically. The official recommended prompt instructs it to document:
- Build/test/run/lint commands (validated by running them)
- Project structure and key file locations
- CI/CD and validation pipeline details
- Dependencies not obvious from file structure

(Source: [GitHub Docs on repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions), fetched 2026-07-20)

#### Type 2: Path-Specific Instructions
**Files:** `.github/instructions/NAME.instructions.md` with YAML frontmatter:

```markdown
---
applyTo: "app/models/**/*.rb"
excludeAgent: "code-review"
---
# Ruby model conventions...
```

#### Type 3: Agent Instructions (AGENTS.md)
AGENTS.md files stored anywhere in the repository, with nearest-ancestor precedence. Also supports single `CLAUDE.md` or `GEMINI.md` at root.

**Priority order:** Personal instructions > Repository instructions > Organization instructions.

---

### 3e. `.clinerules` (Cline)

**Tool:** [Cline](https://github.com/cline/cline) — open-source VS Code + JetBrains + CLI coding agent
**File:** `.clinerules/` directory (multiple markdown files) or `.clinerules` single file

Source: `cline/cline:docs/customization/cline-rules.mdx`

**Key features:**
- All `.md` and `.txt` files inside `.clinerules/` are combined into unified rules
- Supports **YAML frontmatter** for conditional (path-based) activation:

```yaml
---
paths:
  - "src/components/**"
  - "src/hooks/**"
---
# React Component Guidelines
- Use functional components with React hooks
- Extract reusable logic into custom React hooks
```

- **Cross-tool compatibility:** Also reads `.cursorrules`, `.windsurfrules`, and `AGENTS.md` automatically
- **Global rules:** `~/Documents/Cline/Rules` directory (personal, across all projects)
- **Skill-based activation:** Rules can be toggled on/off per-task via UI

**Documented Best Practices** (`cline/cline:docs/customization/cline-rules.mdx`):
> *"Be specific, not vague. 'Use descriptive variable names' is too broad. 'Use camelCase for variables, PascalCase for classes, UPPER_SNAKE for constants' gives Cline something concrete to follow."*

> *"Include the why. When a rule might seem arbitrary, explain the reason."*

> *"Rules consume context tokens. Avoid lengthy explanations or pasting entire style guides. Keep rules concise."*

---

## 4. Amazon Kiro — Spec-Driven AI IDE

### What It Is

Amazon Kiro is a spec-driven AI IDE/agent launched by AWS in July 2025. Its differentiating feature is that it natively enforces a 3-phase spec workflow before any code is written. This is not an add-on but the default mode of operation.

(Source: analysis of `IsHexx/system-prompts-and-models-of-ai-tools-chinese:Kiro/Spec_Prompt.txt`, which contains Kiro's full system prompt; `hscale/ai-instructions-template:ai-agents/spec-agent.md`)

### Kiro's Directory Structure

```
.kiro/
├── specs/
│   └── {feature_name}/
│       ├── requirements.md     ← Phase 1: EARS-format requirements
│       ├── design.md           ← Phase 2: technical design
│       └── tasks.md            ← Phase 3: implementation task list
├── steering/
│   └── *.md                    ← Agent Steering files (always/conditional/manual)
└── settings/
    └── mcp.json
```
(Source: `IsHexx/system-prompts-and-models-of-ai-tools-chinese:Kiro/Spec_Prompt.txt:224-237`)

### Kiro's Spec Workflow

Kiro uses a **3-phase iterative workflow** with mandatory human approval gates (`Kiro/Spec_Prompt.txt:319-615`):

**Phase 1: Requirements Gathering**
- Generates `requirements.md` with EARS (Easy Approach to Requirements Syntax) format
- Each requirement: user story + numbered acceptance criteria
- Format: `WHEN [event] THEN [system] SHALL [response]`
- Must ask: *"Do the requirements look good? If so, we can move on to the design."*
- MUST NOT proceed without explicit approval

```markdown
# Requirements Document
## Requirements
### Requirement 1
**User Story:** As a [role], I want [feature], so that [benefit]
#### Acceptance Criteria
1. WHEN [event] THEN [system] SHALL [response]
2. IF [precondition] THEN [system] SHALL [response]
```

**Phase 2: Design Document**
- Creates `design.md` with mandatory sections: Overview, Architecture, Components and Interfaces, Data Models, Error Handling, Testing Strategy
- Uses Mermaid for diagrams where applicable
- Must ask: *"Does the design look good? If so, we can move on to the implementation plan."*

**Phase 3: Task List**
- Creates `tasks.md` — a numbered checkbox list, maximum 2 levels of hierarchy
- Each task references specific requirements from `requirements.md`
- Format: `- [ ] 1. Set up project structure and core interfaces` with `_Requirements: 1.1_`
- Only includes coding tasks (no deployment, user testing, business process tasks)
- Prioritizes test-driven development
- Must stop workflow here — implementation is separate

**Kiro EARS keyword usage** (from Spec_Prompt.txt:374-400):
```
WHEN [event] THEN [system] SHALL [response]
IF [precondition] THEN [system] SHALL [response]
WHEN [event] AND [condition] THEN [system] SHALL [response]
```

### Kiro Agent Steering Files (`.kiro/steering/*.md`)

Steering files are Kiro's equivalent of `.cursorrules` / `CLAUDE.md` (`Spec_Prompt.txt:218-237`):

> *"Steering allows for including additional context and instructions in all or some of the user interactions with Kiro. Common uses: standards and norms for a team, useful information about the project, additional information how to achieve tasks."*

Three inclusion modes:
- **Always** (default): included in every interaction
- **File-match** (`inclusion: fileMatch`, `fileMatchPattern: 'README*'`): included when matching files are in context
- **Manual** (`inclusion: manual`): only when user explicitly references via `#` in chat

Steering files support `#[[file:<relative_file_name>]]` references to pull in external specs (e.g. OpenAPI specs).

### Kiro vs. GitHub Spec Kit

| Aspect | Kiro | GitHub Spec Kit |
|---|---|---|
| Deployment | Native IDE (AWS product) | CLI tool + any agent |
| Spec format | requirements.md (EARS) + design.md + tasks.md | spec.md + plan.md + tasks.md |
| Requirements syntax | EARS (WHEN/IF/THEN/SHALL) | FR-001 MUST/SHOULD + Given/When/Then |
| Gate mechanism | Built-in userInput tool with `spec-requirements-review`, `spec-design-review`, `spec-tasks-review` | Manual approval + `/speckit.clarify`, `/speckit.checklist`, `/speckit.analyze` |
| Constitutional governance | Via Steering files | Via constitution.md template |
| Agent support | Kiro's own agent | 35+ agents |

---

## 5. Broader SDD Methodology Discussions

### Community Repositories

Several community projects build on or reference the SDD methodology:

- **`attilaszasz/sdd-pilot`** (85 ⭐, Feb 2026): *"Replace chaotic AI code generation with a disciplined, spec-driven workflow. SDD Pilot enforces structured development phases and quality gates."* Supports Claude Code, Codex, Copilot, Gemini CLI, opencode, Windsurf.

- **`loulanyue/spec-kit-zh`** (263 ⭐, Mar 2026): Chinese-localized SDD toolkit for Codex, Claude Code, Cursor, and other AI coding agents.

- **`specdd/specdd`** (23 ⭐, Apr 2026): *"Gives humans and AI agents small, local instructions right where the code lives. Increases productivity, reduces implementation errors, and helps keep changes aligned with the project's intended design."* Topics: BDD, agentic-development, specification-driven-development.

- **`joaoariedi/ai-assisted-development-framework`**: *"A systematic Claude Code configuration for spec-driven development (SDD) with quality gates, custom agents, automated hooks, security guardrails, and a full specification pipeline."*

- **`lu-valencia/Introducing-SDD`**: Presentation repo: *"Transition from 'vibe coding' to structured agentic workflows where intent is the source of truth."*

### "Vibe Coding" as the Anti-Pattern

A recurring theme in the SDD community (2025-2026) is positioning SDD as the opposite of "vibe coding" — the practice of issuing freeform natural language prompts to AI agents without structured specifications. The spec-kit README explicitly frames this contrast (`github/spec-kit:README.md:39-41`), and multiple community repos use "vibe coding" in their descriptions as the problem being solved.

### Martin Fowler Article Reference

The `github/spec-kit:docs/concepts/spec-persistence.md` document directly references a Martin Fowler article at `martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html`, framing the spec lifecycle in three levels: **Spec-first** (write spec, then discard), **Spec-anchored** (keep spec after implementation), and **Spec-as-source** (spec is the only human-edited artifact; code is regenerated).

### GitHub Blog — "Spec Converts to Production Code in Minutes" (May 2025)

From the GitHub blog post announcing the new Copilot coding agent (May 19, 2025):
> *"The GitHub Copilot coding agent fits into our existing workflow and converts specifications to production code in minutes."*
>
> — Alex Devkar, Senior Vice President of Engineering and Analytics, Carvana

Source: [GitHub Blog: GitHub Copilot — Meet the New Coding Agent](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/), May 19, 2025.

---

## 6. Best Practices for Writing Specs for AI Coding Agents

Drawing on the documented best practices across all tools:

### 6a. Structural Principles

**Separate "What" from "How" (Strict)**
- Specs describe user-facing behavior, goals, and constraints — *what* and *why*
- Plans describe technology choices, architecture, data models — *how*
- This prevents the LLM from jumping to implementation details in the spec phase, keeping specs stable across tech stack changes
- (`github/spec-kit:spec-driven.md:169-178`): *"✅ Focus on WHAT users need and WHY. ❌ Avoid HOW to implement (no tech stack, APIs, code structure)"*

**Acceptance Criteria Must Be Independently Testable**
- Spec Kit: `Each user story must be independently testable — if you implement just ONE, you should still have a viable MVP`
- Kiro: Uses EARS syntax (`WHEN [event] THEN [system] SHALL [response]`)
- Both enforce BDD-style Given/When/Then scenarios

**Use [NEEDS CLARIFICATION] Markers, Never Guess**
- Spec Kit explicitly: `Mark all ambiguities: Use [NEEDS CLARIFICATION: specific question]`
- Example: `- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]`
- Prevents LLM from making plausible but incorrect assumptions
- (`github/spec-kit:spec-driven.md:185-191`)

**Requirements as Testable Assertions (RFC 2119 / EARS)**
- Use modal verbs MUST/SHOULD/MAY (RFC 2119 style) or EARS syntax
- Spec Kit: `FR-001: System MUST [specific capability]`
- Kiro: `WHEN [event] THEN [system] SHALL [response]`
- This creates unambiguous, verifiable requirements

**Task Decomposition and Parallelism Marking**
- Mark independent tasks with `[P]` for parallel execution
- Organize by user story priority (P1 → P2 → P3)
- Separate foundational (blocking) phases from story-specific phases
- Each story should be independently deliverable as an MVP increment
- (`github/spec-kit:templates/tasks-template.md`)

### 6b. Token Efficiency

- Cline docs warn: *"Rules consume context tokens. Avoid lengthy explanations or pasting entire style guides. Keep rules concise and link to external documentation when detailed reference is needed."* (`cline/cline:docs/customization/cline-rules.mdx`)
- GitHub Copilot's generated instructions are limited to ~2 pages
- Spec Kit enforces hierarchical detail management: *"Any code samples, detailed algorithms, or extensive technical specifications must be placed in the appropriate `implementation-details/` file"*
- Split rules by concern (one rule file per topic in Cline) to enable selective loading

### 6c. Constitutional Governance

- A project **constitution** (equivalent to `.kiro/steering/` or `.github/copilot-instructions.md`) provides immutable architectural principles
- Gates built into the plan template enforce compliance before any implementation:
  - Simplicity Gate: ≤3 projects? No future-proofing?
  - Anti-Abstraction Gate: Using framework directly? Single model representation?
  - Integration-First Gate: Contracts defined? Contract tests written?
- (`github/spec-kit:spec-driven.md:355-376`)

### 6d. Versioning and Lifecycle

- Spec artifacts should be version-controlled alongside code (in the same repo)
- Branch-per-feature: Spec Kit creates `specs/003-chat-system/` in a feature branch
- Kiro creates `.kiro/specs/{feature_name}/` per feature
- Choose a spec persistence model early and document it in the constitution:
  - **Flow-back**: small teams, fast iteration
  - **Flow-forward**: audit trails, compliance
  - **Living spec**: stable requirements, regeneratable code
- (`github/spec-kit:docs/concepts/spec-persistence.md`)

### 6e. Anti-Patterns to Avoid

| Anti-Pattern | Description | Source |
|---|---|---|
| Vague requirements | "Use descriptive variable names" | Cline docs |
| Premature implementation details in spec | Tech stack choices in spec.md | Spec Kit spec-driven.md |
| Silent assumptions | LLM guesses at unspecified details | Spec Kit spec-template.md |
| Speculative features | "might need later" items | Spec Kit spec-driven.md |
| Non-coding tasks in task lists | Deployment, user training, marketing | Kiro Spec_Prompt.txt |
| Monolithic specs | Large, non-decomposable specs | Spec Kit (user story per phase) |
| Rules without "why" | Rules that seem arbitrary without context | Cline docs |
| Outdated rules | Stale constraints that no longer apply | Cline docs |
| Cross-agent context leakage | Context files getting corrupted by multiple agents | Spec Kit AGENTS.md |

### 6f. Metadata and Traceability

Best practice from Kiro and Spec Kit alike:
- Each task MUST reference specific requirements by ID (e.g., `_Requirements: 1.1, 3.3_`)
- Success criteria must be measurable (not "system is fast" but "system handles 1000 concurrent users without degradation")
- Checklist items should be binary pass/fail, not subjective
- (`github/spec-kit:templates/spec-template.md`; `Kiro/Spec_Prompt.txt:530-541`)

---

## Key File Reference Table

| Tool | Instruction File | Location | Format | Notes |
|---|---|---|---|---|
| Claude Code | `CLAUDE.md` | Repo root, `~/.claude/`, enterprise path | Markdown | 4-level hierarchy; 21 KB pdfme example |
| GitHub Copilot | `copilot-instructions.md` | `.github/copilot-instructions.md` | Markdown | ≤2 pages recommended |
| GitHub Copilot (path-specific) | `NAME.instructions.md` | `.github/instructions/` | Markdown + frontmatter | `applyTo:` glob filter |
| GitHub Copilot (agent) | `AGENTS.md` | Anywhere in repo | Markdown | Nearest ancestor wins |
| Cursor | `.cursorrules` (legacy) | Repo root | Markdown | Being superseded |
| Cursor | `*.mdc` | `.cursor/rules/` | Markdown + frontmatter | `description`, `globs`, `alwaysApply` |
| Windsurf | `.windsurfrules` | Repo root | Markdown | Codeium's equivalent to `.cursorrules` |
| Cline | `*.md` or `*.txt` | `.clinerules/` directory | Markdown ± frontmatter | `paths:` for conditional activation |
| Amazon Kiro | Steering files | `.kiro/steering/*.md` | Markdown + frontmatter | `inclusion: always/fileMatch/manual` |
| Amazon Kiro | Spec files | `.kiro/specs/{feature}/` | Markdown | requirements.md, design.md, tasks.md |
| OpenAI Codex | `AGENTS.md` | Repo root | Markdown | Skills-based via `.agents/skills/` |
| GitHub Spec Kit | `spec.md` / `plan.md` / `tasks.md` | `specs/{feature}/` | Markdown | Spec Kit's generated artifacts |
| GitHub Spec Kit | `constitution.md` | `.specify/memory/` or root | Markdown | Immutable architectural principles |

---

## Repositories and Sources Discovered

| Repository | Stars | Description |
|---|---|---|
| [`github/spec-kit`](https://github.com/github/spec-kit) | N/A (official) | The canonical SDD toolkit by GitHub |
| [`agentsmd/agents.md`](https://github.com/agentsmd/agents.md) | — | Open AGENTS.md standard website + reference |
| [`openai/codex`](https://github.com/openai/codex) | — | OpenAI Codex CLI (reads AGENTS.md) |
| [`anthropics/claude-code`](https://github.com/anthropics/claude-code) | — | Anthropic's Claude Code CLI (reads CLAUDE.md) |
| [`cline/cline`](https://github.com/cline/cline) | — | Cline open-source agent (.clinerules) |
| [`PatrickJS/awesome-cursorrules`](https://github.com/PatrickJS/awesome-cursorrules) | — | Community .mdc rules for Cursor |
| [`IsHexx/system-prompts-and-models-of-ai-tools-chinese`](https://github.com/IsHexx/system-prompts-and-models-of-ai-tools-chinese) | — | Contains Kiro's system/spec prompts |
| [`loulanyue/spec-kit-zh`](https://github.com/loulanyue/spec-kit-zh) | 263 | Chinese SDD toolkit based on Spec Kit |
| [`attilaszasz/sdd-pilot`](https://github.com/attilaszasz/sdd-pilot) | 85 | SDD workflow enforcer with quality gates |
| [`specdd/specdd`](https://github.com/specdd/specdd) | 23 | Alternative SDD framework |

---

## Gaps and Uncertainties

1. **Martin Fowler article** (`martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html`) — access was denied; the article exists (referenced in Spec Kit's own docs) but its full contents could not be fetched.

2. **Official Kiro documentation** — No public Kiro docs repository was found at `aws/kiro-docs`. The Kiro system prompt analysis (from `IsHexx/system-prompts-and-models-of-ai-tools-chinese`) is authoritative (contains the actual system prompt) but the official docs site `kiro.dev` was inaccessible during research.

3. **Anthropic's official CLAUDE.md docs** — `code.claude.com/docs/en/memory` and `docs.anthropic.com/en/docs/claude-code/memory` were inaccessible. The CLAUDE.md convention is well-attested through community examples and integration behavior.

4. **Official Cursor rules docs** (`docs.cursor.com/context/rules`) — inaccessible. Documentation was reconstructed from the `PatrickJS/awesome-cursorrules` community source.

5. **Official Windsurf rules docs** (`docs.codeium.com/windsurf/context/rules`) — inaccessible. Windsurf rules documented through community `.windsurfrules` examples.

6. **GitHub Blog announcement for Spec Kit** — Multiple URL patterns tried; no official launch blog post found. The repo was active as of the current research date (July 2026) with the `acknowledgements` section crediting John Lam.

7. **Tessl** — The URL `tessl.io` was inaccessible during research. Tessl is a company building a "code-less" development platform with AI; further research would require a working fetch.

8. **Spec Kit star count** — The GitHub API did not return star count in the searched form; the repo is actively maintained (3,526+ issues/PRs based on commit message numbers) and appears to have significant adoption (the Chinese fork alone has 263 stars).
