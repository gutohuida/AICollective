# Spec → Ticket Traceability

How to get from a structured specification to issue-tracker tickets without losing the
thread back to the requirement — and why this is the one stage of the AI delivery
pipeline worth building yourself.

---

## The problem

Two ecosystems approach the same gap from opposite sides and neither closes it:

- **Spec-driven tooling** (Spec Kit, Kiro, and friends) produces excellent structured
  requirements and task lists, and leaves them in the repository as files.
- **Issue trackers** generate tickets from prose with an LLM. Fast, and structurally
  blind: nothing guarantees every requirement produced a ticket, or that a ticket traces
  back to anything.

The consequence is that the *review* stage — the highest-value part of the pipeline —
has nothing solid to check against. "Does this PR implement its ticket?" is only a useful
question if the ticket faithfully represents a requirement.

**Traceability is not bureaucracy here.** It is the data structure that makes automated
review possible.

---

## The chain

```text
requirement (FR-1)  →  task (T1, traces FR-1)  →  ticket (labelled, carries FR-1 text
  as acceptance criteria)  →  branch/PR (references ticket key)  →  AI review
  (fetches ticket, checks diff against acceptance criteria)  →  human approval
```

Every arrow is a link an automated reviewer can follow. Break any one and the reviewer
degrades to generic code-quality commentary.

---

## What the spec must carry

The prerequisites are unglamorous and mostly about discipline, not format. A spec is
ready to generate tickets when it has:

**Stable requirement IDs.** `FR-1` must mean the same requirement for the life of the
document. Once a ticket references an ID, renaming it silently breaks the chain. IDs are
append-only; retire, never renumber.

**Testable requirements.** RFC 2119 modal verbs (MUST / MUST NOT / SHOULD / MAY) or EARS
form:

```text
WHEN <condition or event> THE SYSTEM SHALL <expected behaviour>
```

A requirement that cannot fail a test cannot become a ticket with meaningful acceptance
criteria. This is the single highest-leverage constraint in the whole pipeline: vague
requirements produce vague tickets produce useless review.

**Acceptance criteria as Given/When/Then, one per behaviour.** Binary pass/fail,
independently testable, measurable. These map directly onto the acceptance-criteria field
that coding agents and review tools read.

**Tasks that trace.** Every task references at least one requirement ID that exists in
the document; every requirement is referenced by at least one task. Both directions
matter — an unreferenced requirement is unimplemented, and an untraced task is
unjustified scope.

**An explicit approval state.** Ticket generation is gated on human approval of the spec,
so the spec needs somewhere to record that decision.

See [`../spec-driven-development/dos-and-donts.md`](../spec-driven-development/dos-and-donts.md)
for the underlying conventions, and
[`../../skills/html-spec/conventions.md`](../../skills/html-spec/conventions.md) for a
worked machine contract that carries all of the above.

---

## Generation rules

**Dry run first, always.** Emit the planned tickets for inspection before writing
anything. Ticket creation is difficult to undo, noisy for the team, and the first few
runs will be wrong.

**Idempotency by construction.** Re-running must update, not duplicate. The cheap
mechanism: label every generated ticket with the spec name and carry the task ID in a
stable field. Look before creating. Assume the tool will be run repeatedly against an
evolving spec, because it will be.

**One task, one ticket.** Resist aggregating. The task granularity was already decided
when the spec was written; re-deciding it at generation time destroys the trace.

**Copy the requirement text into the ticket.** Do not merely link. Downstream tools read
the ticket's own fields — a link to a wiki page the reviewer cannot fetch is not
traceability. Duplication is acceptable here precisely because the spec is the source of
truth and the ticket is a projection of it.

**Never generate non-coding tasks.** Sign-off, training, and comms belong to humans and
pollute an agent's task list.

**Carry the requirement ID into the ticket body.** This is what lets a reviewer, or a
human, walk the chain backwards from a diff.

---

## Drift is the steady state

A spec, its tickets, and the published documentation will diverge. Treat this as normal
and detectable rather than preventable.

The three divergences worth detecting:

| Drift | Signal |
|---|---|
| Spec changed after tickets were generated | Spec version/hash newer than generation record |
| Ticket edited away from its requirement | Ticket acceptance criteria no longer matches `FR-n` text |
| Published doc changed under the spec | Wiki page version number moved since last read |

Wiki APIs expose a monotonic page version number, and their query languages support
"modified since" filters — so change detection is a stored version number and a
comparison, not a diffing engine.

**Report drift; do not auto-resolve it.** Which side is right is a human judgement, and a
tool that silently reconciles will eventually overwrite the wrong one.

---

## Source of truth

The pipeline touches three surfaces that can each plausibly claim to hold the spec: the
repository, a rendered review document, and the organisation's wiki. Pick one, or you
will build drift into the design.

The defensible split:

- **Repository is canonical.** Versioned, diffable, reviewable, and the format agents
  read best. Consistent with
  [`../spec-driven-development/format-selection.md`](../spec-driven-development/format-selection.md):
  Markdown as the canonical agent-facing source.
- **Rendered HTML is generated, never hand-edited.** It is a review and approval surface.
  Machine-contract attributes are emitted from the source, so a round-trip is never
  needed.
- **The wiki is where business intent arrives, and where approved specs are published
  back.** It is the organisation's window into the process, not the process's memory.

The flow, then, is: intent arrives in the wiki → agent drafts a spec in the repository →
human approves → publish a mirror back to the wiki → generate tickets.

**Do not build a bidirectional format translator.** Two editable representations of one
document is precisely the drift the pipeline exists to detect.

---

## Why build this one yourself

The rest of the pipeline is rentable and improving fast. This stage is not, for a
structural reason: it depends on your specification conventions and your tracker's field
configuration, and neither is standard enough for a vendor to package profitably.

It is also small. This is a skill with a script, not a system — which keeps it cheap to
own and cheap to discard when the ecosystem eventually catches up. See
[`platform-or-tool.md`](./platform-or-tool.md) for when that distinction matters.
