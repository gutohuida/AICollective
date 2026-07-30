# AgentWeave Strategy Discussion — 2026-07-29

A pressure-testing session, following on from
[`single-vs-multi-agent-research.md`](./single-vs-multi-agent-research.md), applying that
research's conclusions specifically to AgentWeave: is it built the wrong way, and if so, what
to do about it.

## How this started

While resuming a Hub Spec Navigation session, unrelated uncommitted work turned up in the
tree (an agent-heartbeat "stalled" status feature). Untangling what it was led to the real
topic: the user has been feeling friction using AgentWeave — specifically, having to design
roles before implementing anything — and suspected the friction was evidence the tool's whole
premise might be wrong, not just a rough edge.

## Diagnosed root cause (grounded in code, not just feeling)

`agentweave init` (`src/agentweave/cli.py:266-271`) defaults `mode="hierarchical"` and writes
a role file for every agent in the roster **before any task exists**. Step one of using
AgentWeave is "define your org chart." That is the exact inversion the research document
warns against: designing the team before there is anything to delegate, instead of starting
with one agent and adding a worker only once a specific task passes the delegation test
(independent / bounded / verifiable / non-overlapping / compressible / worthwhile — see
§3.5 of the research doc).

Also confirmed: `src/agentweave/roles.py` + `constants.py` define roles as **job-title
personas** (`tech_lead`, `architect`, `backend_dev`, `frontend_dev`, `qa_engineer`, each
mapped to a markdown behavioral guide) with **no tool/permission/scope binding** attached to
the role itself. This is the "persona, not capability boundary" anti-pattern the research
doc's §4.3 describes — confirmed to be true of AgentWeave's actual implementation, not a
hypothetical risk.

## What's still sound

The durable substrate — task ledger with acceptance criteria, ownership, messages/handoffs,
cross-session checkpoints, scheduled jobs, heterogeneous-agent interop, transport layer
(local/git-plumbing/http) — matches exactly what the research doc calls "valuable" and lists
conditions for (cross-machine/cross-vendor coordination, work spanning sessions, audit trail,
several independent async projects). The problem is not this substrate; it is the *default
posture* built on top of it.

## Does scale (big companies) change the calculus?

No. What's showing up as "enterprise multi-agent orchestration" (Google Gemini Enterprise,
Microsoft Foundry, IBM watsonx) is concentrated in IT ops, finance reconciliation, onboarding,
customer support, claims — high-volume, **independently verifiable, bounded units**. That's
Google Research's "alignment principle" again: multi-agent helps when a task decomposes into
independent paths. Those platforms are governance/identity/lifecycle layers for running many
bounded, non-conversing agent instances in parallel — "distributed execution, not collective
reasoning" (the research doc's own phrase). Scale widens the fan-out; it doesn't relax the
delegation test.

## Does "agents build everything, humans just write specs" change the calculus?

No — a spec is a task contract, not an org-chart decision. It defines what "done" means; it
doesn't dictate whether one continuous agent executes it or several. A good spec with clear
acceptance criteria is exactly the raw material the delegation test needs, regardless of who's
holding the pen. Even in a maximally spec-driven, autonomous future, every source reviewed
still puts one accountable reader of the actual diff/test results at the gate — "the agent
says it's done" isn't evidence anywhere.

## Other industries — what's the actual variable?

Not "industry." **Task decomposability.** Every high-adoption non-coding domain found
(customer support, IT helpdesk, finance back-office, insurance claims, legal contract review,
healthcare admin, SOC alert triage, research/report generation) is naturally decomposable
per-unit (one ticket, one invoice, one clause, one alert). Software feature work is unusually
sequential and tightly coupled by comparison — that's *why* coding is a worse fit for
multi-agent defaults, not because coding is special in some other way.

## Where AgentWeave could reposition, if it repositions at all

Reframed away from "simulate your dev team" and toward: **the vendor-neutral control plane
for running many independently spec'd, verifiable units of work across sessions and
machines, with audit** — structurally similar to what Foundry/watsonx/Gemini Enterprise sell
enterprises, but self-hosted, lightweight, and not locked to one vendor's agent runtime.

## Market check: is any of this open ground?

| Candidate direction | Built asset overlap | Market status |
|---|---|---|
| Multi-harness coordination / task board for looping agents | Hub task board, multi-runner support | **Crowded** — vibe-kanban, amux, Superset, Nimbalyst, swarm-protocol, ralphy |
| Agent-agnostic session handoff/continuity | `/handoff`, `/resume`, session sync | **Crowded** — `ai-memory` explicitly does "facilitate handoff between different agent vendors"; also `agent-handoff`, `agent-config` |
| Spec-driven-development platform | OpenSpec integration | **Crowded, and awkward** — GitHub Spec Kit, AWS Kiro, Tessl, BMAD-METHOD, Cursor Plan Mode; AgentWeave currently builds *on* OpenSpec rather than replacing it |
| Oversight/governance/audit layer (approval gates, human Q&A, review states) | Task lifecycle (`pending→...→under_review→approved`), Q&A API | **Less covered** — the scrappy OSS tools above optimize for solo speed, not review; the enterprise platforms that do own this are vendor-locked and priced for large orgs |
| Living spec+task+chat dashboard (navigable spec viewer, just shipped) | `SpecNavigator`, `SpecFrame`, `SpecDocumentPicker`, `SpecWorkspace`, `specBridge` | **Open** — nothing found combines a navigable authored spec, task/acceptance traceability, and live agent chat in one self-hosted page |
| Skills/role template library | `roles.json`, role guides, skill templates | **Newly risky** — Tessl repositioned itself in Jan 2026 as "the package manager for agent skills" with $125M raised |
| AI spec creator + navigable UI, standalone | Navigation UI built; authoring is not (today it's just "chat with an agent that happens to edit spec files") | **Open** — heavyweight requirements-traceability tools (Visure, Productboard Spark, Xebrio) are the wrong shape/buyer; Tessl's Spec Registry solves a different problem (library specs, not project specs) |

Two candidates are genuinely uncontested: **spec navigator + AI authoring**, and the
**review/approval queue**. Not coincidentally, both lean on what the Hub already does that
the scrappy competitor tools don't bother with (DB-backed state, approval semantics, a real
web UI).

## The meta-question: decompose, pivot, or fix?

Verdict reached: **neither decompose nor pivot, yet.** Both are packaging/scope decisions
being made before there is evidence of real pull — everything pointing at "open ground" this
session came from desk research and the user's own friction, not from sustained usage
(by the user or anyone else) proving a capability is load-bearing. This is the same discipline
the source research applies to agent delegation ("don't add a worker until the task proves it
needs one"), just one level up, applied to product scope instead of task scope.

The diagnosed problem is also narrower than either option assumes: it's a **default-ordering
bug** (`mode`/roles chosen before a task exists), not proof the substrate is wrong. The CLI
core, task ledger, transport layer, and Hub plumbing were never implicated in the diagnosis.

**Recommendation on the table before the side-project question came up:**

1. Fix the actual diagnosed default — single-agent-first at `init`, delegation introduced
   per-task rather than chosen once for the whole session.
2. Keep dogfeeding the Hub on real work already in flight (including finishing T10/T11 on
   the spec-navigation change itself), which forces real usage of the review/approval queue
   and the spec navigator, not just building them.
3. Watch, honestly, which parts get reached for versus routed around. That's the real signal
   — stronger than any competitive scan.
4. Revisit decompose/pivot/stay-one-thing once there's a few weeks of real usage data instead
   of research and friction as the only inputs.

## Resolved: side project instead of decomposing or pivoting

**Conclusion:** yes — a small, from-scratch side project is the better move, and not really a
third alternative to decompose/pivot so much as a faster way to buy the usage evidence that
decision actually needs. Dogfeeding the existing Hub for weeks (the earlier recommendation)
and a days-scale side project both serve the same goal — real usage evidence before a
packaging decision — but the side project gets there faster and without risking AgentWeave's
working substrate.

Conditions attached to keep it cheap and actually informative, rather than becoming a second
half-finished project:

1. **Build it disconnected from AgentWeave's code, not extracted from it.** Lifting
   `SpecFrame`/`SpecNavigator`/`specBridge` wholesale would require untangling them from Hub's
   auth, task/agent backend, and manifest conventions — that untangling *is* the decomposition
   surgery cost this path is meant to avoid. A fresh build (point it at a folder of
   markdown/HTML, no server, no DB, possibly local-first) is faster to get to something usable
   and a truer test, since it doesn't inherit AgentWeave's assumptions about what a "spec" is.
2. **Scope it at the riskiest unknown, not the whole feature set.** Navigation/reading is
   already proven — it shipped in AgentWeave this week. The unvalidated part is **authoring**:
   does AI-assisted spec creation in a UI beat chatting with an agent that happens to edit
   files? Build the smallest version of that, not a full re-implementation of the navigator,
   history browser, and Ctrl+K picker.
3. **Decide the pull signal before starting, not after.** Fast build time doesn't answer how
   you'll know it worked. Pick in advance what counts as real pull (reaching for it unprompted
   for a real spec, someone else asking to use it) so there's a clean end condition instead of
   a quiet second project to maintain forever.

If it gets real pull, that's the evidence base for whether it folds back into AgentWeave,
spins out formally, or stays its own small thing. If not, the cost was days, and AgentWeave's
core was never touched.

## Sources referenced this session

- [Google Research — Towards a Science of Scaling Agent Systems](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Enterprise AI Agents in Production (tothenew, 2026)](https://www.tothenew.com/insights/article/enterprise-ai-agent-trends-2026)
- [7 Enterprise AI Agent Trends Defining 2026 — Beam AI](https://beam.ai/agentic-insights/enterprise-ai-agent-trends-2026)
- [AI Agent Orchestration in 2026 — Viston](https://viston.tech/ai-agent-orchestration-in-2026-moving-from-pilots-to-enterprise-wide-execution/)
- [Spec-Driven Development — Microsoft for Developers](https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/)
- [Spec-Driven Development Is Eating Software Engineering — map of 30+ frameworks](https://medium.com/@visrow/spec-driven-development-is-eating-software-engineering-a-map-of-30-agentic-coding-frameworks-6ac0b5e2b484)
- [awesome-agent-orchestrators (vibe-kanban, amux, ralphy, swarm-protocol, etc.)](https://github.com/andyrewlee/awesome-agent-orchestrators)
- [ai-memory — long-term memory + handoff between agent vendors](https://github.com/akitaonrails/ai-memory)
- [Tessl launches spec-driven framework and registry](https://tessl.io/blog/tessl-launches-spec-driven-framework-and-registry/)
- [Tessl — Announcing Tessl's Products to Unlock the Power of Agents](https://tessl.io/blog/announcing-tessls-products-to-unlock-the-power-of-agents/)
- [AI Requirement Management Tools: A 2026 Selection Guide](https://ones.com/blog/tool-guide/ai-requirement-management-tools-a-4/?primary_category=tool-guide)
