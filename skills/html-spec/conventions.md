# HTML spec conventions — the rubric

Every rule below traces to a primary source, verified 2026-07-27: the WHATWG HTML Living
Standard, GitHub Spec Kit's templates and docs, Amazon Kiro's first-party spec docs, or
vendor instruction-file documentation. Recovered/leaked vendor system prompts circulating in
community repos are **not** used as authority; where a practice is only attested by one, it
is marked as such.

Research background lives in this repo under
[`ResearchClub/spec-driven-development/`](../../ResearchClub/spec-driven-development/).

---

## 0. Document kinds

Declare the kind in `<head>`; review expectations scale with it.

```html
<meta name="spec-kind" content="change-spec">   <!-- change-spec | roadmap | system-map | baseline -->
```

| Kind | Holds | Tasks? | Approval gate? |
|---|---|---|---|
| `change-spec` | One change: requirements, acceptance criteria, design, tasks | Yes | Yes |
| `roadmap` | Slice rows: ID, intent, in/deferred boundary, dependencies, status, child link | No | No |
| `system-map` | Durable constraints, bounded contexts, shared contracts, rules for child specs | No | No |
| `baseline` | Detailed living behavioral spec for a whole system | No | No |

A project that already uses a prefix (`aw-spec-kind`, `aw-spec-status`) keeps it. Never
rename a metadata key that tooling parses.

---

## 1. Why HTML at all

Markdown is the right default for agent-facing source text — it is what AGENTS.md, CLAUDE.md,
Cursor rules and Spec Kit's own `spec.md` use, and it costs fewer tokens. Choose HTML only
when you need what Markdown cannot give:

- **A human-reviewable artifact.** One file, opened in a browser, read top to bottom, and
  explicitly approved before code is written.
- **Machine-readable state in the document.** Approval status and per-task completion live in
  `<meta>` and `data-*` attributes, so no companion state file can drift from the spec.
- **Real semantic structure.** Sections, definition lists, ordered algorithms, typographic
  markers for normative vs. informative text, and an anchor for every defined thing.

The cost is real — HTML is heavier to read and to diff. Keep the prose lean; the markup is
there to carry state and traceability, not decoration.

---

## 2. Content rules

### A. Separate WHAT/WHY from HOW
Requirements and acceptance criteria describe user-facing behavior, goals, and constraints.
Tech stack, architecture, and data model live in Design. Spec Kit states the rule as
"Focus on WHAT users need and WHY / Avoid HOW to implement (no tech stack, APIs, code
structure)" (`templates/commands/specify.md`). It keeps requirements stable when the
implementation changes.

### B. Producer vs. consumer conformance
WHATWG §1.9.1 splits requirements on *producers* (what input is allowed) from requirements on
*consumers* (how software must act) and states plainly: "Requirements on producers have no
bearing whatsoever on consumers." Conflating input validation with processing behavior is a
top source of ambiguity — and of specs that never say what happens on malformed input.

### C. Requirements are testable assertions with stable IDs
Modal verbs per RFC 2119 (MUST / MUST NOT / SHOULD / MAY), or EARS as Kiro documents it:

```
WHEN <condition or event> THE SYSTEM SHALL <expected behavior>
```

Kiro's bugfix specs add `SHALL CONTINUE TO` for behavior that must not regress. The broader
`IF … THEN …` / `WHEN … AND …` keyword family comes from the general EARS literature, not
first-party Kiro docs — usable, but do not cite it as a vendor rule.

Give each requirement an element `id` (`id="FR-1"`) so criteria and tasks can link to it.

### D. Acceptance criteria as Given/When/Then, one per behavior
Binary pass/fail, independently testable, measurable ("completes within 2 seconds under 50
concurrent sessions", not "is fast"). Spec Kit's rule for user stories applies here: if you
implemented just one, you should still have something demonstrable.

### E. Ordered or conditional behavior is a numbered algorithm
```html
<ol class="algorithm">
  <li>Parse the refresh token.</li>
  <li>If the token is expired, respond 401 and stop.</li>
  <li>Otherwise, mint a new access token and respond 200.</li>
</ol>
```
Prose leaves room to reorder steps or drop a branch. A list does not.

### F. Explicit non-goals
Out-of-scope items are stated, not implied by omission. Without them an agent expands scope
"helpfully".

### G. Justify non-obvious rules
A rule with a stated reason generalizes correctly to edge cases the spec did not anticipate.
Cline's own rule-writing guidance puts it as "include the why".

### H. Label non-normative content
```html
<p class="note"><strong>Note:</strong> non-normative background.</p>
<p class="example"><strong>Example:</strong> illustrative only.</p>
<p class="warning"><strong>Warning:</strong> hazard or common mistake.</p>
<p class="issue"><strong>Open issue:</strong> unresolved; do not treat as settled.</p>
```
WHATWG §1.9.2 does exactly this. Rationale that reads as binding is as damaging as a binding
rule that reads as commentary.

### I. Mark unresolved ambiguity, never guess
Every open question is a visible `[NEEDS CLARIFICATION: …]` in an Open Questions section
(Spec Kit's marker). The spec must not be approved while any remain.

### J. One anchor per defined thing, and use one name for it
Each requirement and term gets a single `id` and is linked from everywhere else. Avoid
synonyms for the same concept — alternating between "session", "conversation", and "thread"
is a reliable way to get three different implementations.

### K. State the evidence and its limits
Name what you actually checked — tests, contracts, fixtures, schemas and migrations,
configuration, runbooks — and what remains unverified. A passing suite demonstrates only the
behavior it covers. "Regenerable from this document" is a claim almost no spec can support.

---

## 3. Lifecycle: name the persistence model

From Spec Kit's `docs/concepts/spec-persistence.md` and Birgitta Böckeler's article on
martinfowler.com. None is a default; picking silently is how specs go stale.

| Model | Rule | Best for |
|---|---|---|
| **Flow-back** | Any artifact may be edited; the spec is corrected to match reality | Fast iteration, small teams |
| **Flow-forward** | New immutable change directory per change | Audit trails |
| **Living spec** | The spec is the source; downstream artifacts are derived | Spec-as-contract |

State the model **and** the reconciliation rule: who updates what, when, after implementation.

---

## 4. Machine contract (change specs)

```html
<meta name="spec-name" content="add-token-refresh">
<meta name="spec-status" content="draft">        <!-- draft | approved -->
<meta name="spec-approved-by" content="">
<meta name="spec-approved-at" content="">
```

```html
<li class="task"
    data-task-id="T1"
    data-status="pending"              <!-- pending | done -->
    data-role="backend_dev"
    data-agent="claude"
    data-requirements="FR-1,FR-3">
  <input type="checkbox" disabled>
  <span class="task-desc">Implement the token-refresh endpoint.</span>
  <span class="req-refs">(FR-1, FR-3)</span>
</li>
```

- Every task traces to at least one requirement ID that exists in the document.
- Tasks are small, independently deliverable units; mark parallelizable ones
  (`data-parallel="true"`).
- No non-coding tasks (sign-off, training, marketing) in an agent's task list.
- Status flips to `approved` only on an explicit human decision, and only with Open Questions
  empty.

---

## 5. Rendering contract

- **Self-contained.** Inline `<style>` and `<script>` only; no CDN, font, or image URL. The
  file must render identically offline.
- **Navigable.** Sticky table of contents with one link per section, active-section
  highlighting, collapsible on narrow viewports.
- **Theme-aware, in three layers, in this order:** `:root` light defaults →
  `@media (prefers-color-scheme: dark)` → explicit `:root[data-theme="light"|"dark"]`
  overrides, so an embedding viewer's toggle wins over the OS preference.
- **Iframe-safe anchors.** Intercept every `a[href^="#"]` click and `scrollIntoView` manually.
  A sandboxed iframe without `allow-same-origin` can blank out on native hash navigation and
  need a manual reload.
- **Consistent visual language.** Distinct styling for note / example / warning / issue,
  MUST/SHOULD/MAY badges, completed tasks struck through.

---

## 6. Decomposition

- One spec covers one vertical capability with its own acceptance criteria. Never slice by
  frontend / API / database layer.
- Multiple independently demonstrable outcomes → a shallow roadmap first, then one child spec
  per ready row, with links in both directions.
- Durable constraints, bounded contexts, and shared contracts live in a system map, referenced
  by ID from child specs rather than restated.
- A cross-context interface change is specified once, in one place, and referenced by every
  sibling that consumes it.
- Decompose only when a slice is not independently testable or cannot be implemented in one
  cycle. Spec Kit's own guidance is to reach for decomposition after lighter context-scoping
  options are insufficient.
