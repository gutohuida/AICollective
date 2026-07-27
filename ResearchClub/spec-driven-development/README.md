# Spec-Driven Development (SDD) for AI Coding Agents — Research

Research into how specifications are written for/consumed by AI coding
agents: current tools, conventions, and what makes a spec good.

## Contents

- [`sdd-landscape-report.md`](./sdd-landscape-report.md) — Survey of the
  2025–2026 tooling landscape: GitHub Spec Kit, AGENTS.md, CLAUDE.md,
  Cursor rules, Windsurf/Devin Desktop rules, Cline, Amazon Kiro, and
  documented best practices. Verified against available first-party docs on
  2026-07-27; product details remain version-sensitive.
- [`html-spec-conventions.md`](./html-spec-conventions.md) — Notes on why the
  WHATWG HTML Living Standard is considered an exemplary specification, and
  which of its conventions (producer vs. consumer requirements, algorithmic
  steps, typographic markers) transfer to specs written for AI agents.
- [`dos-and-donts.md`](./dos-and-donts.md) — Synthesized, actionable
  checklist distilled from the above two sources.

- [`spec-decomposition.md`](./spec-decomposition.md) - Practical system/epic/feature decomposition guidance, with current primary sources.
- [`format-selection.md`](./format-selection.md) - Evidence-based Markdown vs. HTML guidance: Markdown for agent-facing source specs, HTML for human-facing review when rendering adds value.

## Status

Initial research pass completed 2026-07-20 and refreshed 2026-07-27. The
decomposition guidance is now applied to the local `spec-rebuild` skill and is
being trialed in AgentWeave's AW-Spec workflow.

**Validation pass — 2026-07-27.** Every checkable claim was re-verified against live
first-party sources. The large majority confirmed, including all direct quotes, the Spec Kit
pipeline and templates, the WHATWG section references, and the vendor instruction-file
conventions. Corrections applied to `sdd-landscape-report.md`:

| Finding | Correction |
|---|---|
| Windsurf listed as a Spec Kit integration | Retired ("absorbed into Cognition Devin", CHANGELOG #3213); removed from the catalog list |
| Kiro steering had three inclusion modes | Docs now list four — `auto` (semantic matching) added |
| `lu-valencia/Introducing-SDD` cited as an SDD presentation | Unrelated Spanish-language repo; citation removed |
| pdfme `CLAUDE.md` "21 KB" | Actually ~14 KB (spec-kit's own `AGENTS.md` is ~25 KB) |
| Kiro EARS variants, tasks.md rules, gate mechanism names | Attested only by the recovered `Spec_Prompt.txt`; now flagged inline, as the report's own limitations section requires |
| "Martin Fowler's article" | Authored by Birgitta Böckeler on martinfowler.com; "lifecycle" → "implementation levels" |
| `github.github.com/spec-kit/...` links | Canonical domain is `github.github.io` |

The applied form of this research is the [`html-spec`](../../skills/html-spec/) skill.
