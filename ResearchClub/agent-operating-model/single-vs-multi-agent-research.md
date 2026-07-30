# AI Agent Operating Models for Software Development

**Research question:** How are people and companies using AI effectively for software
development? Is it better to work with one strong agent supported by specifications and
skills, or with multiple agents? If multiple agents are useful, how should they be
coordinated, and do fixed roles still add value?

**Research date:** 2026-07-29  
**Scope:** Interactive coding agents, autonomous coding agents, agent skills and project
instructions, parallel agent execution, and true multi-agent collaboration.  
**Primary recommendation:** **one principal, elastic delegation**.

---

## Executive conclusion

For an individual developer, the best default is:

1. **You own intent, priority, and acceptance.**
2. **One strong primary agent owns the continuous working context**: discovery, plan,
   implementation, verification, and explanation.
3. **Project directives hold durable facts and constraints.**
4. **Skills hold reusable procedures.**
5. **Specs and tests define the task and its evidence of completion.**
6. **Temporary subagents are created only when a task has a concrete reason to be
   isolated or parallelized.**
7. **The primary agent remains accountable for integration and the final claim that the
   work is done.**

This is not a rejection of multi-agent systems. It is a rejection of making a
multi-agent organization the starting point.

The strongest current evidence says agent count should follow task structure:

- Google Research evaluated 180 configurations and found multi-agent systems improved a
  parallelizable financial-reasoning task by about 81%, but degraded a sequential
  planning task by 39–70%. Increasing tool density also increased the coordination tax.
  Centralized coordination contained errors better than independent workers
  ([Google Research, 2026](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)).
- Anthropic reports that its production multi-agent research system uses about 15 times
  the tokens of ordinary chat, while explicitly warning that most coding tasks have
  fewer truly parallel paths than research and are not currently an ideal multi-agent
  domain. Its strongest gains came from breadth-first search over independent sources
  ([Anthropic Engineering, 2025](https://www.anthropic.com/engineering/multi-agent-research-system)).
- A Berkeley-led analysis of more than 1,600 multi-agent traces across seven frameworks
  found 14 recurring failure modes in system design, inter-agent alignment, and task
  verification. Better role descriptions and orchestration alone did not eliminate the
  failures
  ([Cemri et al., arXiv v3, 2025](https://arxiv.org/abs/2503.13657)).
- Anthropic's current Claude Code guidance says to keep work in the main conversation
  when phases share substantial context, the change is small, latency matters, or
  frequent refinement is needed. It recommends subagents for self-contained work,
  verbose output, restricted permissions, and independent parallel investigations
  ([Claude Code subagent documentation](https://code.claude.com/docs/en/sub-agents)).

The practical conclusion is sharper than “sometimes use multiple agents”:

> **Use multiple executions more often than you use a multi-agent organization.**

Running two independent implementation candidates, putting unrelated issues in separate
worktrees, or asking a fresh context to review a patch can be valuable. Those patterns do
not require persistent AI employees, a simulated PM/architect/developer hierarchy, or
continuous agent-to-agent conversation.

---

## 1. What the evidence actually says about AI development

### 1.1 AI coding can improve output, but the result is highly conditional

The evidence is not contradictory once task type and user population are separated.

| Evidence | Population and intervention | Result | What it supports |
|---|---|---:|---|
| Microsoft/Accenture/Fortune 100 field experiments | 4,867 developers; randomized access to an AI code-completion assistant | **26.08% more completed tasks** in the pooled estimate; less-experienced developers gained more | AI assistance can improve routine workplace throughput |
| METR early-2025 RCT | 16 highly experienced maintainers; 246 real tasks in repositories they knew deeply; mostly Cursor with Claude 3.5/3.7 | **19% longer** with AI | AI can slow experts on mature, context-heavy codebases |
| DORA 2025 | Large cross-industry survey and organizational analysis | AI is an **amplifier** of the surrounding engineering system | Tools do not repair weak tests, platforms, feedback loops, or priorities |
| Anthropic 2026 usage study | About 400,000 Claude Code sessions from about 235,000 people | Humans made most **what** decisions; the agent made most **how** decisions; domain expertise predicted success | Effective use is direction plus delegated execution, not abdication |

Sources:
[Microsoft Research field experiments](https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/),
[METR RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/),
[METR's 2026 follow-up caveat](https://metr.org/blog/2026-02-24-uplift-update/),
[DORA 2025](https://dora.dev/research/2025/dora-report/), and
[Anthropic's 2026 usage analysis](https://www.anthropic.com/research/claude-code-expertise).

Important limitations:

- The Microsoft experiments studied an assistant offering code completions, not an
  autonomous multi-agent system.
- The METR result is a snapshot of early-2025 tools in large, mature open-source
  repositories. METR later said late-2025 tools probably provide more benefit, but
  selection effects made its newer estimate unreliable.
- Vendor telemetry describes users who selected that vendor and product. It establishes
  observed workflow patterns, not a vendor-neutral causal productivity gain.
- Benchmark pass rates measure bounded tasks in controlled environments. They do not
  directly measure maintainability, product correctness, operational risk, or the human
  review burden.

The defensible conclusion is therefore:

> AI is most helpful when the task is bounded, the environment is legible, feedback is
> executable, and the human supplies relevant domain judgment. It is less predictably
> helpful when success depends on tacit repository knowledge, architectural continuity,
> or detecting that the requested change is conceptually wrong.

### 1.2 Effective companies improve the environment, not just the prompt

The common production pattern is “harness engineering”: make the repository and delivery
system easy for an agent to understand and hard for it to damage.

OpenAI's internal Codex guidance recommends:

- begin large changes with an investigation and implementation plan;
- scope tasks roughly like a clear issue or small pull request;
- provide file paths, analogous implementations, constraints, and a definition of done;
- improve startup scripts, dependencies, environment variables, and network access after
  every observed failure;
- keep durable repository context in `AGENTS.md`;
- use multiple candidates when comparing approaches is valuable.

OpenAI currently describes a strong task as one that might take a person about an hour or
a few hundred lines, while noting that the boundary moves as models improve
([How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/)).
Its agent-built internal product case study emphasizes depth-first construction,
repository-local skills, standard tools, and turning missing context into legible,
enforceable repository capabilities
([Harness engineering](https://openai.com/index/harness-engineering/)).

Anthropic's guidance converges on the same loop:

1. explore the relevant code;
2. plan before editing;
3. implement;
4. verify against tests or another observable target;
5. course-correct early;
6. commit a reviewable unit.

Anthropic especially recommends test-driven work and concrete visual or executable
targets because the agent otherwise stops when the output merely “looks done”
([Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)).

Stripe offers a complementary signal from tool infrastructure: in 2026 it reported that
agents generated 70% of CLI requests for API resources, while also observing that
credential management, service provisioning, and adjacent setup remained harder than
writing the integration code. Its response was to make those operations available
through structured CLI/skill interfaces with scoped credentials, spend controls, and
environment boundaries
([Stripe, 2026](https://stripe.com/blog/stripe-projects-adds-new-agents-providers-developer-controls)).

These examples lead to a durable principle:

> The highest-leverage “prompt engineering” is often ordinary engineering: fast tests,
> deterministic setup, useful error messages, discoverable commands, narrow
> permissions, stable interfaces, and written decisions.

### 1.3 The highest-value use cases

Current evidence and public production guidance support the following use cases most
strongly:

#### A. Codebase navigation and explanation

Use the agent to locate ownership, trace call paths, compare patterns, inspect history,
and produce a change map. This reduces cold-start cost without immediately risking code.
It is especially valuable before planning.

#### B. Small, bounded implementation slices

Examples include one endpoint, a local bug fix, one UI behavior, a small refactor, or a
testable feature slice. The request should name the goal, context, constraints, non-goals,
and done conditions.

#### C. Tests, fixtures, and verification

Agents are effective when they can close their own feedback loop: reproduce a bug, write
a failing test, implement, run focused tests, then run broader regression checks.
Tests must be reviewed because an agent can weaken assertions or overfit the
implementation.

#### D. Mechanical migrations and cleanup

Agents can apply a known pattern repeatedly: API upgrades, type migrations, deprecated
call replacement, documentation updates, or consistent configuration changes. A
canonical example, scripted checks, and non-overlapping work units make this one of the
best cases for parallel execution.

#### E. Alternative generation and design pressure-testing

Multiple independent proposals can reveal trade-offs without asking agents to negotiate.
“Best of N” is often simpler than a conversational agent team. The human or principal
agent compares the artifacts against the same rubric.

#### F. Review, security triage, and regression search

A fresh context can inspect a patch for correctness, missing tests, security, performance,
or violations of repository rules. Automated review complements deterministic checks and
human accountability; it should not merely rubber-stamp another output from the same
model.

#### G. Backlog and background work

Low-risk, well-specified issues can run asynchronously in isolated worktrees or cloud
environments. This is portfolio parallelism: multiple independent tasks in flight, each
ending in a reviewable artifact.

#### H. Prototyping

Agents dramatically reduce the cost of testing product ideas. Prototype speed should not
be confused with production readiness. Authentication, authorization, data handling,
payments, concurrency, migration safety, and operations need stronger gates.

### 1.4 Where AI remains structurally weak

- deciding what customers actually need;
- reconciling unstated political or organizational constraints;
- recognizing when a locally correct change damages system coherence;
- maintaining a reliable long causal chain through many lossy handoffs;
- validating non-functional properties without a realistic environment;
- reviewing more generated code than humans or automated gates can absorb;
- safely operating with broad production permissions.

DORA's “amplifier” finding matters here: faster generation can increase queues,
batch size, review load, and instability if testing and delivery systems do not scale
with it.

---

## 2. Four operating models that are often confused

“Single agent versus multi-agent” hides four materially different designs.

| Model | Description | Primary benefit | Primary cost |
|---|---|---|---|
| **One agent + skills** | One continuous context; procedures loaded as needed | Coherence and low coordination overhead | Context can become noisy or full |
| **Principal + temporary subagents** | One accountable context delegates bounded investigations or checks | Context isolation and selective parallelism | Delegation and synthesis tax |
| **Parallel independent sessions** | Several agents handle separate issues or candidates in separate worktrees | Wall-clock throughput | Human review and merge capacity |
| **True multi-agent system** | Agents exchange messages, maintain roles/state, negotiate, and coordinate over time | Dynamic decomposition across large, open-ended work | Tokens, latency, state, debugging, error propagation |

Most individual developers should use the first model constantly, the second selectively,
the third when they have a queue of independent work, and the fourth rarely.

This distinction also explains why “companies use multiple agents” can be misleading. A
company may run thousands of independent issue-to-PR jobs without any two agents talking
to one another. That is distributed execution, not collective reasoning.

---

## 3. Single agent versus multiple agents

### 3.1 Why one strong primary agent is the right default

A software change usually has sequential dependencies:

```text
understand intent
    → inspect current behavior
        → choose a design
            → edit interacting files
                → interpret failures
                    → revise the design
                        → verify the whole
```

Each arrow carries tacit context. Splitting the chain creates:

- repeated repository exploration;
- lossy summaries between workers;
- conflicting assumptions;
- duplicated work;
- more tokens spent restating context;
- more opportunities to modify the same files;
- a harder question of who is accountable for end-to-end correctness.

The single primary agent already changes “roles” internally as it moves from discovery to
planning, coding, testing, and explanation. A new identity and context window are not
required for each cognitive phase. Skills can provide the relevant procedure at the point
of need without discarding shared context.

One agent is usually best when:

- the task is small or medium;
- planning, implementation, and debugging share substantial context;
- the next step depends on the previous result;
- the change crosses tightly coupled components;
- the requirements are still being clarified with you;
- many tools are needed in a particular sequence;
- one coherent design judgment matters more than breadth;
- edits would overlap;
- latency or token cost matters.

### 3.2 What multiple agents are genuinely good for

Multiple contexts earn their cost through one or more of five mechanisms.

#### 1. Parallel breadth

Several independent search paths can cover more repositories, documents, modules, logs,
or candidate explanations in the same wall-clock time.

#### 2. Context isolation

Large test logs, documentation searches, static-analysis output, or repository surveys
can fill the principal context with low-value detail. A worker can compress that material
into a small evidence-bearing result. Anthropic's current subagent documentation calls
this one of the most effective uses of subagents.

#### 3. Artifact isolation

Separate worktrees prevent concurrent agents from overwriting the same checkout. Each
worker returns a patch, branch, report, or test result rather than a stream of chat.

#### 4. Meaningful diversity

Independent samples, different model families, different tool access, or a deliberately
different objective can reduce correlated blind spots. Merely assigning two instances of
the same model the labels “developer” and “reviewer” does not create reliable
independence.

#### 5. Least privilege

A read-only investigator, test runner, documentation retriever, or security scanner can
be given only the tools and files it needs. Specialization is then enforced by capability
boundaries, not role-play.

Multiple agents are most defensible when:

- work can be written as independent input/output contracts;
- workers do not need frequent back-and-forth;
- each result can be verified locally;
- subtask outputs are much smaller than their working context;
- workers own non-overlapping files or produce read-only reports;
- wall-clock time matters more than total token use;
- the expected value of broader search or independent checking exceeds the cost;
- the principal has time and evidence to integrate the results.

### 3.3 What current quantitative studies imply

Google's 2026 scaling study gives three useful design laws:

1. **Alignment principle:** multi-agent coordination helps when the task is naturally
   decomposable into independent paths.
2. **Sequential penalty:** coordination damages tasks requiring one continuous chain of
   state and reasoning.
3. **Tool-coordination trade-off:** the more tools an agentic task already requires, the
   less cognitive budget remains for agent-to-agent coordination.

It also found that a central orchestrator was a better error-containment mechanism than
uncoordinated parallel workers. Independent systems amplified errors by as much as
17.2× in its evaluation; centralized coordination reduced that measure to 4.4×. These
are benchmark-specific measurements, not universal constants, but the direction is
operationally credible.

Anthropic's production research system reinforces the economics:

- multi-agent performance was strong for breadth-first research;
- token use explained much of observed performance variance—in other words, some of the
  “intelligence” gain was simply much more inference;
- multi-agent research used roughly 15× the tokens of ordinary chat in that system;
- detailed delegation was necessary to stop duplicate or misdirected work;
- writing worker artifacts directly to external storage reduced “telephone game”
  information loss;
- Anthropic explicitly identifies most coding tasks as less suitable because they have
  more shared context and dependencies.

The correct interpretation is not “15× tokens is always bad.” If ten workers complete a
high-value migration overnight, cost may be trivial relative to human time. The point is
that multi-agent systems buy capability by spending additional compute, context, and
coordination. That purchase needs an explicit business case.

### 3.4 A simple decision equation

Use multiple agents only when:

```text
value of extra coverage
+ value of independent checking
+ value of reduced wall-clock time
+ value of context isolation

is greater than

extra inference cost
+ delegation/synthesis time
+ duplicated exploration
+ conflict and merge risk
+ extra review burden
+ probability of coordination failure × cost of that failure
```

This equation prevents a common mistake: optimizing token cost while ignoring human
attention, or optimizing wall-clock speed while ignoring review capacity.

### 3.5 The delegation test

Before adding a worker, answer all six questions:

1. **Independent:** Can it work without asking the principal repeated questions?
2. **Bounded:** Are inputs, owned files, and non-goals explicit?
3. **Verifiable:** Is there an objective way to check its result?
4. **Non-overlapping:** Can it avoid editing the same state as another worker?
5. **Compressible:** Will it return a small result relative to the context it consumes?
6. **Worthwhile:** Does parallelism, isolation, diversity, or permission separation have
   concrete value here?

If fewer than five answers are “yes,” keep the work in the primary context. If the
failure is only poor task definition, improve the task before deciding again.

---

## 4. Roles versus directives and tasks

### 4.1 Fixed human-company roles are usually the wrong abstraction

Frameworks often simulate a company:

```text
Product Manager → Architect → Project Manager → Developer → Tester → Reviewer
```

This was understandable when models needed strong prompt scaffolding. It is increasingly
counterproductive for general-purpose frontier agents because:

- every “employee” may be the same underlying model;
- the labels do not create different knowledge or incentives;
- artificial handoffs fragment a naturally sequential reasoning process;
- each worker reconstructs project context;
- intermediate prose can become ceremony rather than evidence;
- the hierarchy may force waterfall behavior even when code feedback should change the
  plan;
- agents can defer responsibility to one another or accept another agent's unsupported
  claim.

The Berkeley MAST study is relevant: multi-agent failures remained complex even after
interventions aimed at clearer role specification and improved orchestration. A better
persona prompt is not a substitute for system design and verification.

An early 2026 preprint argues that capable agents given a mission and a minimal protocol
can self-select roles more effectively than fixed hierarchies
([Dochkina, 2026](https://arxiv.org/abs/2603.28990)). It reports a large computational
experiment, but it is a single-author preprint using synthetic task protocols rather
than a production software-development field study. It is useful directional evidence,
not a basis for deploying 256 self-organizing coding agents.

### 4.2 Prefer task specialization over persona specialization

Compare:

**Weak assignment**

> You are the senior security engineer. Review the application.

**Strong assignment**

> Inspect authentication and session handling in `src/auth/**` and the corresponding
> tests. Do not edit files. Identify exploitable trust-boundary violations, cite exact
> file/line evidence, state a reproduction path, rank severity, and explicitly report
> “none found” if no finding survives verification. Ignore formatting and naming.

The second assignment works because it specifies:

- objective;
- scope;
- access mode;
- evidence standard;
- output schema;
- non-goals;
- termination condition.

The “security” label is optional. The task contract does the work.

### 4.3 When a persistent role is justified

A role is useful when it corresponds to a stable difference in the system, such as:

- **tools:** one worker has browser access; another can run production-safe diagnostics;
- **permissions:** a reviewer is read-only; a deployer has narrow environment rights;
- **context:** a worker loads a large domain corpus or repository subset;
- **model:** a cheaper model handles mechanical work; a stronger model integrates;
- **objective:** an adversarial checker is rewarded for finding counterexamples;
- **output contract:** a migration worker always produces the same structured artifact;
- **frequency:** the same bounded workflow recurs often enough to justify configuration.

Even then, name the role after the capability or recurring operation—`test-log-triage`,
`dependency-migration`, `auth-boundary-review`—rather than a broad job title such as
`senior-developer`.

### 4.4 Use project directives for durable truth

Project directives (`AGENTS.md`, `CLAUDE.md`, repository rules, or equivalent) should
contain facts and constraints that apply repeatedly:

- repository map and important boundaries;
- build, test, lint, and validation commands;
- architectural invariants and forbidden dependencies;
- security and data-handling rules;
- generated-file policy;
- definition of done;
- branch, commit, and review conventions;
- pointers to deeper documentation.

Keep them short, concrete, and maintained. Every always-loaded rule consumes attention
and can conflict with the current task.

### 4.5 Use skills for reusable procedures

A skill is preferable to a new agent when the same primary context should follow a known
workflow:

- write or audit a feature spec;
- perform a database migration;
- run a security review;
- investigate a failing test;
- generate a durable handoff;
- release a package;
- validate an HTML artifact.

Skills preserve shared context while loading procedural knowledge on demand. This directly
supports the model you are considering: one good agent, strong project directives, and a
library of precise workflows.

### 4.6 Use task packets for temporary work

Temporary agents should receive a task packet, not a career.

```markdown
# Objective
One observable outcome.

# Why this is separate
Parallel breadth / noisy context / independent review / isolated edits / least privilege.

# Inputs
Exact files, spec sections, issue, assumptions, and relevant prior decisions.

# Scope and ownership
Files or modules allowed; read-only or write; explicit non-goals.

# Method constraints
Required tools, source quality, patterns to follow, actions forbidden.

# Deliverable
Patch, branch, report, test list, or decision table; exact output shape.

# Verification
Commands or rubric the worker must run, with required evidence.

# Stop and escalate when
Conditions under which guessing would be unsafe.
```

This format is consistent with Anthropic's production lesson that workers need an
objective, output format, tool/source guidance, and clear task boundaries to avoid gaps
and duplication.

---

## 5. Recommended operating model: one principal, elastic delegation

### 5.1 Architecture

```text
You
  │  product intent, priorities, risk decisions, approval
  ▼
Primary agent
  │  continuous context; discovery → plan → implementation → verification
  │
  ├── project directives  durable repository truth
  ├── skills              reusable procedures loaded on demand
  ├── specs/ADRs/tests     requirements, decisions, executable evidence
  ├── task ledger          durable state and next work
  │
  └── temporary workers   only for bounded parallel/isolation/review needs
          │
          └── artifacts + evidence, returned to the primary agent
```

The principal is not a manager persona. It is the single point of context continuity and
accountability. It may write code directly and delegate only where the delegation test
passes.

### 5.2 Normal feature workflow

1. **Frame**
   - State the user outcome, constraints, non-goals, and risk.
   - Decide what evidence would prove completion.

2. **Explore**
   - The primary agent reads the relevant implementation, tests, and history.
   - Delegate only large, independent surveys or noisy investigations.

3. **Plan**
   - Produce a short implementation plan and identify uncertainties.
   - For high-risk decisions, compare independent proposals or require human approval.

4. **Specify the slice**
   - Keep a stable project constitution plus a small feature spec.
   - Trace acceptance criteria to tests.

5. **Implement**
   - The primary agent handles tightly coupled edits.
   - Parallel workers own non-overlapping modules or mechanical batches in separate
     worktrees.

6. **Verify**
   - Run focused tests first, then required regression, type, lint, security, and build
     gates.
   - A fresh review context is optional for high-risk or large diffs.

7. **Integrate**
   - The primary agent reads the actual artifacts and evidence, not only worker claims.
   - Resolve conflicts and confirm end-to-end behavior.

8. **Record**
   - Update specs/ADRs when intent or architecture changed.
   - Save a durable handoff or task state when work spans sessions.

### 5.3 Three valid multi-execution patterns

#### Pattern A: investigator fan-out

Use for broad research or repository mapping.

```text
principal
  ├── inspect authentication flow (read-only)
  ├── inspect data model and migrations (read-only)
  └── inspect UI/API contracts (read-only)
principal synthesizes one plan
```

No worker edits code. Results cite files and evidence. This is low-conflict and
compresses noisy discovery.

#### Pattern B: non-overlapping implementation fan-out

Use for a validated plan with explicit component boundaries.

```text
approved interface/contracts
  ├── worker A owns package A
  ├── worker B owns package B
  └── worker C owns tests/fixtures that do not rewrite A or B
principal integrates and runs end-to-end gates
```

Each worker has a separate worktree or branch. Shared contracts are fixed before the
fan-out. If workers must continuously renegotiate an interface, the task was not ready
to parallelize.

#### Pattern C: independent candidate or review

Use when diversity is the goal.

```text
same problem + same rubric
  ├── candidate A
  ├── candidate B
  └── optional adversarial review
principal/human compares artifacts and evidence
```

Do not let candidates see each other before producing an answer. For review, use a fresh
context and ideally a different model family or deterministic analyzer when the risk
justifies it.

### 5.4 Patterns to avoid

- a permanent PM/architect/developer/tester cast for every change;
- peer-to-peer agent chat without a single integration owner;
- concurrent writes to one checkout;
- delegating a vague objective and expecting agents to divide it cleanly;
- passing only summaries when workers could persist source artifacts;
- serial handoffs for phases that need the same context;
- reviewers that receive the author's confident explanation before inspecting the diff;
- testing agents allowed to make failing tests disappear without explaining why;
- unlimited agent spawning;
- measuring “tasks completed” without correctness, rework, or human-attention cost.

---

## 6. What this means for AgentWeave

AgentWeave's useful capabilities and a standing multi-agent organization should be
evaluated separately.

The durable parts are valuable:

- task objects with requirements and acceptance criteria;
- status and ownership;
- explicit messages and handoffs;
- cross-session checkpoints;
- scheduled background jobs;
- heterogeneous-agent interoperability.

The questionable default is treating every project as a society of persistent role
agents that must communicate to get ordinary software work done.

### Recommended AgentWeave posture

Use AgentWeave as an **optional control plane**, not as the cognitive architecture for
every task:

- keep one principal/pilot agent as your normal collaborator;
- put durable task state, acceptance criteria, and checkpoints in files or the task
  ledger;
- create collaborators only after decomposition exposes independent work;
- make them temporary and task-scoped;
- prefer artifact references over long message relays;
- keep implementation ownership non-overlapping;
- route completion through one principal integrator;
- archive or release task-specific workers when their contract is complete;
- use persistent configured roles only for stable capability or permission boundaries.

AgentWeave is likely worth retaining when you need:

- coordination across different vendors or machines;
- work that continues across sessions and schedules;
- an auditable task/message history;
- several independent projects or backlog items running asynchronously;
- explicit human/agent ownership and approval state.

It is probably overhead when:

- you are interactively building one feature with one capable agent;
- the work is a sequential inspect-plan-code-debug loop;
- roles differ only by prompt wording;
- communication volume approaches implementation volume;
- you spend more time managing status, messages, and context packets than reviewing
  code and product behavior.

The migration away from “AgentWeave everywhere” does not have to be all-or-nothing:

1. make direct primary-agent work the default;
2. retain the task and checkpoint layer;
3. add AgentWeave collaborators only through the delegation test;
4. measure whether each delegation reduced elapsed time or improved verified quality.

---

## 7. Governance, safety, and quality

Greater autonomy should come from stronger boundaries, not from fewer controls.

### 7.1 Contain the blast radius

Use:

- separate worktrees or disposable environments;
- filesystem and network allowlists;
- scoped credentials;
- read-only defaults for investigation and review;
- spend and time limits;
- no direct production access for ordinary coding work;
- explicit approval for deployments, destructive migrations, secrets, and external
  communication;
- audit logs for agent actions.

Anthropic reports that repeated permission prompts create approval fatigue—its telemetry
showed users approved about 93% of prompts—so hard environmental boundaries can be safer
than relying on a tired human to inspect every shell command
([Anthropic containment engineering, 2026](https://www.anthropic.com/engineering/how-we-contain-claude)).

### 7.2 Make completion evidence-based

“The agent says it is done” is not evidence. Require the strongest available combination:

- fail-to-pass tests for the requested behavior;
- pass-to-pass regression tests;
- type checking, linting, and static analysis;
- build/package success;
- screenshots or visual comparison;
- benchmark or performance thresholds;
- migration dry-runs and rollback tests;
- exact file/line citations for review findings;
- a small manual acceptance check for product behavior;
- human approval proportional to risk.

Anthropic's agent-evaluation guidance similarly recommends well-specified tasks, stable
environments, deterministic code graders, and model/human rubrics only where needed
([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)).

### 7.3 Control generated-work inventory

Agent throughput can exceed review throughput. Limit work in progress:

- cap simultaneous implementation agents to available review capacity;
- prefer small diffs;
- reject weak artifacts early;
- do not start dependent tasks before shared contracts pass;
- separate speculative candidates from merge-ready work;
- count unreviewed agent branches as inventory, not productivity.

---

## 8. A measurement plan for your own workflow

No public study exactly matches your repositories, skills, models, and working style.
Run a small within-person comparison instead of deciding from impressions.

### 8.1 Compare three modes

For 12–18 representative tasks, rotate:

- **Mode S:** one primary agent + project directives + skills;
- **Mode D:** primary agent + temporary delegation chosen by the agent;
- **Mode W:** standing AgentWeave multi-agent workflow.

Stratify tasks:

- small targeted change;
- sequential debugging;
- cross-cutting feature;
- mechanical multi-module change;
- broad research/design;
- independent review or security audit.

Do not compare different task classes as if they were equivalent.

### 8.2 Measure the full system

| Dimension | Metric |
|---|---|
| Outcome | Acceptance criteria passed; escaped defects; revert/rework |
| Time | Human active time; wall-clock time; time to first useful artifact |
| Cost | Total tokens/credits; tool/runtime cost |
| Coordination | Delegation messages; duplicated work; merge conflicts; blocked handoffs |
| Review | Review minutes; diff size; findings per review; false positives |
| Autonomy | Interventions required; unsafe or out-of-scope attempts |
| Maintainability | Human review score; architectural violations; follow-up cleanup |
| Experience | Your confidence, cognitive load, and ability to retain system understanding |

Use repository history, task timestamps, test results, and cost telemetry where possible.
Human perception alone is unreliable: METR's participants believed AI had sped them up
even when the measured result showed a slowdown.

### 8.3 Decision rule after the trial

Keep a more complex mode only if it provides a repeatable advantage on a named task
class. For example:

- investigator fan-out cuts broad research elapsed time by 40% without lowering source
  quality;
- parallel migration workers reduce wall time by 60% with no increase in rework;
- an independent security review finds high-value issues at acceptable false-positive
  cost.

Do not retain “multi-agent” as a general preference. Retain specific patterns with
measured value.

---

## 9. Final answers to the original questions

### Is it better to have one good AI agent and work directly with it?

**Yes, as the default for individual software development.** One primary context gives
you coherence, fast feedback, and a clear accountability path. Combine it with:

- concise project directives;
- layered specs and decisions;
- reusable skills;
- deterministic tools;
- tests and other completion evidence;
- durable handoffs when the session becomes long.

### Are multiple agents good despite overhead and token use?

**Yes, conditionally.** They are good when work is independently parallelizable, when a
noisy side task should be context-isolated, when separate environments prevent conflict,
when permissions should differ, or when independent candidates/reviews have real value.
They are usually harmful for tightly sequential, tool-heavy, ambiguity-rich work.

### How should multiple agents be handled?

Use a centralized principal-worker design:

- one integrator;
- task packets with explicit boundaries and outputs;
- separate worktrees or read-only scopes;
- artifact-based handoffs;
- objective local verification;
- bounded agent count and budget;
- no overlapping ownership;
- final end-to-end verification by the principal.

### Should agents have roles now that strong models can do almost everything?

**Use roles only when they encode a real system difference.** Different tools,
permissions, context, model, objective, or a frequently repeated output contract can
justify a persistent role. A generic “PM,” “architect,” or “senior developer” persona
usually cannot.

### Is it better to give project directives and a task?

**Yes.** The hierarchy of control should be:

1. project directives for durable truth;
2. skills for reusable procedures;
3. a spec/task for the current outcome;
4. a short plan for this implementation;
5. optional task-scoped workers where decomposition proves useful;
6. tests and evidence as the completion authority.

---

## 10. Recommended policy

Adopt this policy for the next month:

> Work with one primary agent by default. The primary may use skills freely. It may
> create a temporary worker only when it states the concrete benefit—parallel breadth,
> context isolation, independent verification, artifact isolation, or least privilege—
> and gives that worker a bounded, verifiable, non-overlapping task. One primary agent
> integrates all results and remains responsible for the final evidence of completion.
> Persistent roles require a stable difference in tools, permissions, context, model,
> objective, or recurring output contract.

This keeps the workflow simple without forbidding scale. As models improve, the policy
continues to work: stronger agents simply clear the threshold for direct execution more
often, while genuinely parallel projects can still expand elastically.

---

## Sources and evidence quality

### Strongest direct or controlled evidence

- Cui et al., **The Effects of Generative AI on High-Skilled Work** — randomized field
  experiments at three companies:
  https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/
- METR, **Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer
  Productivity** — randomized controlled trial:
  https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- Google Research, **Towards a Science of Scaling Agent Systems** — controlled
  evaluation of 180 agent configurations:
  https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/
- Cemri et al., **Why Do Multi-Agent LLM Systems Fail?** — annotated failure taxonomy
  across 1,600+ traces and seven frameworks:
  https://arxiv.org/abs/2503.13657

### Large observational and organizational evidence

- DORA, **State of AI-assisted Software Development 2025**:
  https://dora.dev/research/2025/dora-report/
- Anthropic, **Agentic coding and persistent returns to expertise** — analysis of about
  400,000 sessions:
  https://www.anthropic.com/research/claude-code-expertise

### Production engineering reports and current product guidance

- Anthropic, **How we built our multi-agent research system**:
  https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic, **Claude Code subagents**:
  https://code.claude.com/docs/en/sub-agents
- Anthropic, **Claude Code best practices**:
  https://www.anthropic.com/engineering/claude-code-best-practices
- Anthropic, **Demystifying evals for AI agents**:
  https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Anthropic, **How we contain Claude across products**:
  https://www.anthropic.com/engineering/how-we-contain-claude
- OpenAI, **How OpenAI uses Codex**:
  https://openai.com/business/guides-and-resources/how-openai-uses-codex/
- OpenAI, **Harness engineering**:
  https://openai.com/index/harness-engineering/
- Stripe, **Projects adds agent integrations and developer controls**:
  https://stripe.com/blog/stripe-projects-adds-new-agents-providers-developer-controls

### Emerging evidence; interpret cautiously

- Dochkina, **Drop the Hierarchy and Roles** — large synthetic computational experiment,
  single-author preprint, not a software-development field study:
  https://arxiv.org/abs/2603.28990
