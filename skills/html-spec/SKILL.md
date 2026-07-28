---
name: html-spec
description: Audit and improve an HTML specification, or write a new one from scratch. Use when the user says "review my spec", "improve this spec.html", "audit the spec", "is this spec good enough to implement", "write a spec for X", "turn this into an HTML spec", "convert the spec to HTML", or points at a spec.html / requirements doc and asks what is wrong with it. Applies verified spec-driven-development conventions — testable requirements with stable IDs, producer/consumer conformance, numbered algorithms, explicit non-goals, task-to-requirement traceability — and ships a structural validator.
---

Take an HTML specification and make it something an agent can execute without guessing —
or write one that starts that way.

Agent-agnostic: no vendor commands, no assumption about which CLI is running this. The
bundled files travel with the skill:

| File | Use |
|---|---|
| `conventions.md` | The rubric: every rule, why it exists, and where it comes from |
| `template.html` | Self-contained skeleton to generate from |
| `validate.py` | Structural checker — `python validate.py <spec.html>` |

## Step 0 — Which mode

| The user has | Mode |
|---|---|
| An existing `.html` spec | **Audit** → steps 1–5 |
| A Markdown spec / requirements doc / PRD | **Convert** → step 1 on the source, then steps 2–5 |
| Only an idea or a request | **Generate** → step G, then steps 3–5 |

Say which mode you picked in one line, then work. If the spec is large, do not read it
twice — read once, take notes as you go.

## Step 1 — Read the whole spec before judging any part of it

Read it end to end. While reading, build four lists — you will need them and re-reading
costs more than noting them now:

1. **Requirement IDs** and whether each has an element `id` to link to.
2. **Acceptance criteria** and which requirement each one covers.
3. **Tasks** and which requirements each one claims to satisfy.
4. **Claims that cannot be tested** — the sentences you could not write a failing test for.

Then note the document's *kind* (`change-spec`, `roadmap`, `system-map`, `baseline` — see
`conventions.md`). Expectations scale with it: a roadmap has no tasks, a system map has no
acceptance criteria. Do not report a missing section that the kind does not have.

## Step 2 — Run the validator

```bash
python validate.py path/to/spec.html
```

ERRORs are contract breaks — dead anchors, duplicate ids, external resources, tasks with no
requirement, an approved spec with unresolved clarification markers. Fix every one.
Warnings are quality signals; judge each against the document kind rather than silencing it.

The validator only sees structure. It cannot tell you whether a requirement is *true*, or
whether the spec describes the system the user actually wants. That is steps 3 and 4.

## Step 3 — Audit against the rubric

Work through `conventions.md`. The failures that matter most, in the order they bite:

1. **Untestable requirements.** "Robust", "user-friendly", "as needed", "handles errors
   gracefully". Rewrite each as an assertion with a modal verb (MUST / SHOULD / MAY, or
   `WHEN <condition> THE SYSTEM SHALL <behavior>`) and a binary outcome.
2. **Traceability holes.** A requirement no task implements; a task tracing to nothing; an
   acceptance criterion covering no requirement. Report both directions.
3. **HOW leaking into WHAT.** Tech-stack choices inside requirements make the requirements
   churn every time the implementation changes. Move them to a Design section.
4. **Behavior written as prose.** Anything with an order or a branch becomes a numbered
   `<ol class="algorithm">`. Prose lets an agent silently reorder or skip a branch.
5. **No non-goals.** Omission is not scope. An agent will happily expand into the gap.
6. **Producer and consumer requirements conflated.** What input is *allowed* is a different
   requirement from how the system *must behave* when it arrives — including when it is
   malformed.
7. **Unlabelled non-normative text.** Rationale and examples that look binding, or binding
   rules buried in a note.
8. **Ambiguity resolved by guessing.** Anything the spec had to invent becomes a visible
   `[NEEDS CLARIFICATION: …]` in an Open Questions section, not a confident sentence.
9. **Overclaimed coverage.** "Fully specified", "regenerable from this document", "verified
   by the test suite". State what evidence was actually checked and what is unverified.

## Step 4 — Report, then fix

Report first — a table of findings ordered by severity, each with the location, what breaks
because of it, and the concrete replacement text. Then apply the fixes.

Two rules while fixing:

- **Never invent domain facts.** If a requirement is vague because nobody decided yet, the
  fix is a `[NEEDS CLARIFICATION]` marker and a question to the user — not a plausible value.
  A specific-sounding invented number is worse than an admitted gap.
- **Never change an existing machine contract.** If the project already uses `aw-spec-status`,
  `data-task-id`, or its own ID scheme, keep those names exactly. Tooling parses them.

Ask the user before: renaming requirement IDs (breaks inbound links), changing approval
status, deleting a requirement, or restructuring a spec that is already approved.

## Step 5 — Re-validate and close

Re-run `validate.py`, confirm it is clean, and report what changed in one block: findings
fixed, findings deferred with reasons, and any open questions now waiting on the user.

Never mark a spec approved yourself. Approval is the user's decision, always.

## Step G — Generating a new spec

1. **Resolve ambiguity first.** List what you would have to invent and ask about the ones
   that block a testable requirement. Do not start writing around an unknown.
2. **Check the size.** If the request contains several independently demonstrable outcomes,
   write a shallow roadmap first (stable row IDs, intent, in/deferred boundary, dependencies,
   status, child-spec link) and specify one row at a time. Slice by vertical capability, never
   by frontend/API/database layer. Do not add a roadmap for a small change that merely has
   several tasks.
3. **Copy `template.html`** and fill every placeholder. Keep the section order; delete the
   sections your document kind does not use.
4. **Write requirements before tasks**, acceptance criteria before design, and derive tasks
   from requirement IDs. A task list written first will not trace.
5. Run steps 2–5 on your own draft before showing it. Your first draft has the same defects
   you would flag in someone else's.

## What this skill will not do

- It will not implement the spec. Improving and executing are separate jobs.
- It will not approve a spec, or fill in approval metadata, on the user's behalf.
- It will not pad a short spec. A small change deserves a small document; length is not rigor.
