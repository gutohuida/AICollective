# Why the WHATWG HTML Living Standard Is a Model Specification

Source: [html.spec.whatwg.org](https://html.spec.whatwg.org/multipage/introduction.html) (WHATWG HTML Living Standard), fetched 2026-07-20.

The HTML spec is widely cited as one of the best-engineered specifications in
software, because it was written explicitly to eliminate the ambiguity that
plagued earlier HTML/DOM specs and caused browsers to diverge. Its founding
principle (from §1.6 History):

> "The WHATWG was based on several core principles, in particular that
> technologies need to be backwards compatible, that specifications and
> implementations need to match even if this means changing the
> specification rather than the implementations, and that specifications
> need to be **detailed enough that implementations can achieve complete
> interoperability without reverse-engineering each other**."

That last clause — detailed enough to prevent reverse-engineering — is the
single most important goal for a spec meant to be executed by an AI agent,
not just read by a human.

## 1. Explicit conformance classes: producers vs. consumers (§1.9.1)

The spec draws a hard line between requirements on **producers** (authors —
what content is *allowed*) and requirements on **consumers** (browsers — how
software must *act*):

> "a requirement on a producer states what is allowed, while a requirement
> on a consumer states how software is to act... **Requirements on producers
> have no bearing whatsoever on consumers.**"

**Transfer to AI specs:** Separate "what the user/system is allowed to
input" from "what the agent must do in response." Conflating the two is a
common source of ambiguity — this maps directly to Spec Kit's "what/why"
(spec) vs. "how" (plan) split, but goes further by also distinguishing
input-validation rules from processing/behavior rules.

## 2. Typographic conventions mark *what kind* of text you're reading (§1.9.2)

The spec visually/semantically distinguishes:
- **Definitions/requirements/explanations** (normative)
- **Notes** (non-normative asides)
- **Examples**
- **Open issues**
- **Warnings**
- Algorithm steps, with special marking (⌛) for steps that run in a
  synchronous section

Every defined term is a hyperlink to its own definition; every use of that
term elsewhere links back to it.

**Transfer to AI specs:** Explicitly label non-normative content ("Note:",
"Example:") so an agent doesn't treat rationale or illustrative examples as
binding requirements. Cross-reference/anchor every defined term once and
reuse it consistently (avoid synonyms for the same concept — a frequent
cause of LLM misinterpretation).

## 3. Algorithms as numbered, unambiguous steps

Behavior is specified as literal ordered-step algorithms ("To do X: 1. ...
2. ... 3. If condition, return to step 1.") rather than prose description.
This is effectively pseudocode that leaves no room for interpretation about
sequencing, branching, or loop conditions.

**Transfer to AI specs:** Wherever behavior has more than one possible
ordering or a conditional branch, write it as a numbered algorithm, not a
paragraph. This is the same instinct behind EARS syntax (`WHEN/IF ... THEN
... SHALL ...`, used by Amazon Kiro) and Spec Kit's `FR-001: System MUST...`
— HTML's algorithms are a more rigorous, fully-general version of the same
idea.

## 4. Defines its own scope and non-goals up front (§1.5 Scope)

The spec states plainly what it does *not* cover (media-specific
presentation, being an entire OS, high-end workstation applications) before
diving into details.

**Transfer to AI specs:** State explicit non-goals/out-of-scope items in the
spec itself, not just implicitly by omission — this prevents an agent from
"helpfully" expanding scope.

## 5. Conformance requirements for authors are justified, not just asserted (§1.11)

Every restriction (e.g., "presentational markup is disallowed") is
accompanied by a documented *reason* (accessibility, maintainability,
document size, error-handling implications, streaming compatibility,
performance). Section 1.11.2 even walks through categories of syntax errors
and precisely why each category is disallowed.

**Transfer to AI specs:** This matches Cline's documented best practice
("include the why... when a rule might seem arbitrary, explain the
reason") but HTML shows it at much greater rigor — every single
disallowed pattern has a traceable justification, which both helps an
agent generalize correctly to unseen edge cases and gives humans a way to
challenge/revise the rule later.

## 6. "How to read this spec" is itself specified (§1.9.1)

The spec tells its reader to read it cover-to-cover, then backwards, then by
following cross-references at random — acknowledging that a single linear
read is insufficient for a document this dense, and that the network of
cross-references is where the real precision lives.

**Transfer to AI specs:** For any non-trivial spec, an explicit index/map of
sections and how they depend on each other helps an agent (or human) know
which sections must be read together before acting on any one of them.

## Caveats

**HTML is not automatically the best agent-input format.** HTML is valuable when its
semantic containers, rich tables, and browser rendering serve a real review or
interoperability need. For ordinary agent context, Markdown usually expresses the same
headings, lists, code, IDs, and cross-links with less markup overhead and simpler diffs.
Use a Markdown source/map alongside an HTML review artifact when both audiences matter;
see [`format-selection.md`](./format-selection.md) for the evidence and decision rule.

The HTML spec optimizes for **long-term, multi-implementer interoperability**
over decades, at the cost of being extremely long, dense, and slow to read
in full — the opposite of the "concise, token-efficient" advice from
Cline/Copilot for agent instruction files. It is a good model for a single
**canonical, authoritative spec document** (e.g. a `spec.md`/`design.md` for
a complex feature), not for lightweight day-to-day agent instruction files
(`AGENTS.md`, `.cursorrules`), which need the opposite properties: short,
scannable, link-out-for-detail.
