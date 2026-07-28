# Splitting System Specifications Without Losing the System

## Recommendation

Use a small hierarchy of linked artifacts rather than one feature-sized document for
the entire system:

```text
system intent + durable rules + domain map + shared contracts
└─ epic roadmap
   └─ independently deliverable feature specs
      ├─ requirements and acceptance scenarios (WHAT / WHY)
      ├─ plan (HOW)
      ├─ contracts and data-model changes
      └─ tasks
```

The system layer establishes stable context; a feature spec establishes one coherent,
reviewable change. Do not split a feature merely because its document is long. First
limit implementation to a phase or task batch. Split when a single phase is no longer
coherent, independently testable, or safely held in an agent's context.

## What belongs at each level

| Artifact | Owns | Must not own |
|---|---|---|
| System map | vision, glossary, durable principles, quality attributes, domain ownership, shared contracts | a feature's task list or implementation plan |
| Epic roadmap | ordered slices, intent, in/deferred boundary, dependencies, status, links | detailed design for every slice |
| Feature spec | one user-visible outcome, requirements, scenarios, non-goals, success criteria | unrelated sibling outcomes or stack decisions |
| Plan | architecture and migration decisions for that feature | product requirements duplicated from the feature spec |
| Shared contract | versioned API/event/schema compatibility across domains | a consumer's internal behavior |

## Boundary test

Make a separate feature spec only when the candidate slice has all of these:

1. A demonstrable user or operator outcome.
2. Independently testable acceptance criteria.
3. An explicit in-scope and deferred-to-sibling boundary.
4. A useful dependency position (it can follow a prerequisite without requiring all
   siblings).

Prefer a separate domain/context when its business language, rules, data ownership, or
rate of change differs materially. The same word may legitimately have different models
in different contexts; integrate through an explicit contract rather than forcing a
single mega-model.

Do not split by horizontal technical layer (frontend, API, database). That makes each
user outcome span several specs and recreates handoffs. Use a vertical capability slice;
put its technical detail in that slice's plan.

## Roadmap convention

Keep one shallow, version-controlled roadmap per epic:

```markdown
| ID | Slice | Intent | Scope boundary | Depends on | Status | Spec |
|----|-------|--------|----------------|------------|--------|------|
| B1 | Invoice history | View/download invoices | Read-only; no payments | — | planned | — |
| B2 | Payment methods | Manage saved cards | No plan changes | B1 | planned | — |
```

IDs never change once a child spec references them. Each feature links back to its
roadmap entry; the roadmap links forward to the feature spec. Update the roadmap first
when a boundary changes, then reconcile affected specs and contracts.

## Sources

- GitHub Spec Kit, [Spec of Specs](https://github.github.io/spec-kit/concepts/spec-of-specs.html), accessed 2026-07-27: roadmap pass, sharp slice boundaries, stable IDs, and a complete spec/plan/tasks cycle for every slice.
- GitHub Spec Kit, [Handling Complex Features](https://github.github.io/spec-kit/concepts/complex-features.html), accessed 2026-07-27: use decomposition only after lighter context-scoping options are insufficient.
- Martin Fowler, [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html), accessed 2026-07-27: large models require explicit context boundaries and relationships.
- Microsoft, [Identify microservice boundaries](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/microservice-boundaries), accessed 2026-07-27: prefer high cohesion, independent evolution, and domain-derived boundaries over technical-layer splits.
