# Markdown or HTML for Specifications?

## Recommendation

Use **Markdown as the canonical agent-facing source** for system maps, roadmaps,
feature specs, plans, contracts, and instructions. Generate or maintain **HTML as a
human-facing review view** when a self-contained, polished, approval-gated document is
valuable. Do not claim that HTML is universally better for LLM comprehension.

The decisive factor is semantic structure and clean retrieval, not the file extension.
Use stable headings, IDs, explicit labels, tables only where they clarify a mapping, and
small linked files. Avoid raw web-page HTML with navigation, styling, scripts, and
unrelated text in an agent's context.

## Decision table

| Need | Prefer | Why |
|---|---|---|
| Agent instructions, system map, roadmap, feature spec, plan, or task list | Markdown | Concise, diff-friendly, easy to search/link/review, and low markup overhead. |
| Versioned API/event/schema contract | OpenAPI, JSON Schema, AsyncAPI, or another machine-validated format; document it in Markdown | Validated schemas are stronger than prose or presentation markup. |
| Human review, formal approval, offline distribution, visual progress/status, rich tables or diagrams | HTML generated from, or paired with, Markdown | Browser-friendly presentation without making the rendered form the only workable agent input. |
| Complex tabular data or DOM/layout extraction | Clean semantic HTML, plus a concise Markdown summary where agents must reason across it | HTML preserves table/header and nested structure; it is not a general prose advantage. |
| Agent prompt with mixed instructions, examples, and untrusted/variable content | Markdown headings by default; XML-like delimiters only when strict boundaries materially reduce ambiguity | Structure helps; extra tags are a tool, not a default. |

## Evidence

Anthropic's current prompt guidance says XML tags can clarify complex prompts and make
boundaries parseable, but its 2026 best-practice guidance says clear headings, whitespace,
and explicit language work just as well for most modern-model use cases with less overhead.
This supports concise Markdown for routine specs and targeted XML/HTML-style structure for
exceptional boundary-sensitive inputs.

Microsoft Research found that representation affects table understanding and that HTML
outperformed delimiter-separated formats in its studied table setting. That is evidence for
semantic HTML when table relationships matter; it does not establish an advantage for HTML
over Markdown for general specifications.

There is no reliable universal benchmark establishing that raw HTML makes arbitrary system
specifications easier for frontier LLMs to reason over than equivalent well-structured
Markdown. Results vary by task, model, retrieval pipeline, and document cleanliness.

## Practical house rule

1. Author normative content in small Markdown files, organized as system map → epic
   roadmap → feature spec → plan/tasks.
2. Give requirements, roadmap rows, and shared contracts stable IDs and cross-links.
3. Generate an HTML review artifact only when humans need rendering, formal approval, or a
   richer navigation/progress experience. Preserve a clear source-of-truth rule.
4. When HTML is authoritative for a workflow, make it semantic and self-contained; keep a
   compact Markdown map/roadmap beside it so agents can load only the relevant slice.
5. Test the actual agent/model and representative spec corpus before adopting a format rule
   for the organization. Measure task success, token use, review time, and retrieval errors.

## Sources

- Anthropic, [Prompt engineering best practices for 2026](https://claude.com/blog/best-practices-for-prompt-engineering), accessed 2026-07-27: clear headings and whitespace generally replace XML-tag overhead for modern models; tags remain useful for unusually complex or boundary-sensitive prompts.
- Anthropic, [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), accessed 2026-07-27: descriptive tags can separate instructions, examples, documents, and metadata.
- Microsoft Research, [Improving LLM understanding of structured data](https://www.microsoft.com/en-us/research/blog/improving-llm-understanding-of-structured-data-and-exploring-advanced-prompting-methods/), accessed 2026-07-27: input representation affects table understanding; HTML outperformed delimiter-separated data in the reported evaluation.
- GitHub Spec Kit, [Spec of Specs](https://github.github.io/spec-kit/concepts/spec-of-specs.html), accessed 2026-07-27: links and shallow roadmaps keep independently specified slices navigable without a monolithic artifact.
