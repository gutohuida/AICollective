# Platform or Tool: What to Build When the Substrate Is Moving

A decision note on where to put effort when building AI development workflows — and
specifically on when *not* to build, because the host platform is about to give you the
same thing.

Written 2026-07-30, following on from
[`../agent-operating-model/agentweave-strategy-discussion.md`](../agent-operating-model/agentweave-strategy-discussion.md).

---

## The observation

The AI coding ecosystem spent 2025 and early 2026 filling a genuine gap. Agents were
stateless, forgot everything between sessions, couldn't be scheduled, couldn't hand work
to each other, and left no audit trail. A generation of tools appeared to fix this:
task boards for agents, session handoff utilities, multi-agent orchestrators, schedulers,
approval queues.

By mid-2026 the code hosting platforms are absorbing that layer directly.

| Capability an orchestration tool provides | Platform-native equivalent |
|---|---|
| Cron / scheduled agent runs | Agent automations (schedule, issue-created, PR-opened, PR-updated triggers) |
| Task ledger with ownership and state | Issues, plus assigning an issue to an agent |
| Approval gates | Pull request review and merge rulesets |
| Agent/skill distribution across repos | Org- and enterprise-level agent definition repositories |
| Session audit — "what did the agent actually do" | Agent session logs and audit-log streaming |
| Tool access | MCP, configured per repository or per organisation |

This is not a prediction. Each row is a shipped or shipping feature at the time of
writing.

---

## The implication

**Anything you build in that column is a depreciating asset.** Not worthless — it may be
better than the platform version today, and it may serve you well for a year. But it is
depreciating, and the maintenance is permanent while the advantage is temporary.

This is uncomfortable if you have built one of these tools. It is more uncomfortable to
keep investing in one after the platform has made the decision for you.

The useful move is to be precise about *which parts* are being absorbed. Substrate —
scheduling, state, approval, audit, distribution — is going to the platform. Anything
that depends on **your** conventions, **your** document formats, or **your** organisation's
field configuration is not, because it is not standardisable enough for a vendor to
package.

---

## The decision, when you already have a tool

Three options usually present themselves, and the instinct is to pick the first two.

**Absorb the new work into the existing tool.** Tempting because the substrate is already
there — the scheduler, the task store, the approval states. The problem is that you would
be maintaining a private implementation of exactly the column above, and inheriting all
of its assumptions.

**Extract a library from the existing tool.** Usually the worst option. Untangling a
component from its host's auth, storage, and conventions *is* the decomposition surgery
you were hoping to avoid, and it produces a second thing to maintain rather than a
smaller one.

**Build the small new thing standalone.** Usually correct, and usually smaller than it
first appears once you stop assuming it needs the substrate.

The tiebreaker question: **would the platform plausibly give me this within twelve
months?** If yes, don't build it — bridge to it. If no, and it depends on your own
conventions, build it, and build it small.

---

## Skills, not systems

The unit of work that survives this shift is the **skill**: an instruction file plus,
where needed, a small script. `SKILL.md` and its equivalents have converged across
agent vendors, which makes them unusually portable for something so young.

The properties that matter:

| Skill | System |
|---|---|
| No install, no server, no database | Deployment, storage, migrations |
| Portable across agents and platforms | Bound to its own runtime |
| Reviewable as a text diff | Reviewable only by its author |
| Disposable — delete it and lose nothing | Accretes users, then obligations |
| No vendor review required | Needs one, in most organisations |

The last row decides it in a corporate setting. A skill is a document in a repository;
it goes through the same code review as anything else. A system is a piece of
infrastructure someone must own, support, and defend to an auditor.

**Design the distribution mechanism to be deleted.** If skills need bootstrapping before
platform-native distribution exists, write the thinnest possible installer — no state, no
version negotiation, no update channel. When the platform mechanism arrives, the
bootstrap disappears and nothing is lost. Package it as a product with a changelog and
users, and it will outlive its usefulness by years.

---

## The organisational dimension

For work done inside a company, two constraints dominate technical merit:

**Key-person risk.** A pipeline that works because one person understands it is a
dependency, not an asset. In regulated settings this is an explicit operational
resilience concern, and "a colleague built it" is a poor answer to an auditor asking what
controls a change.

**Procurement asymmetry.** A commercial tool arrives with a contract, a data processing
agreement, a support commitment, and certifications. An internal tool of equal or better
quality arrives with none of these. Excellent internal tools routinely lose to mediocre
commercial ones on this basis alone, and the decision is not irrational.

Neither argument says don't build. They say **be deliberate about which side of the merge
path your work sits on.** Tooling that produces artefacts for humans to approve is cheap
to own. Tooling that sits in the path between a commit and production is expensive to own,
and that expense is mostly not engineering time.

---

## Where personal tools still belong

None of this makes a self-built orchestrator worthless. It relocates it:

- **As a personal tool**, where key-person risk is the point rather than the problem.
- **As a prototype**, to demonstrate a workflow end-to-end before anyone is asked to fund
  or approve anything.
- **As the place to explore the parts the platform genuinely doesn't cover** — in
  practice, spec authoring, requirement traceability, and approval over documents rather
  than over diffs.
- **As the source of requirements** for choosing commercial tooling. Having built one is
  the cheapest way to know what to ask vendors.

---

## The one-line takeaway

*Rent the substrate, own the conventions.* Build skills where your organisation is
genuinely particular, bridge to the platform everywhere else, and design every bridge to
be thrown away.
