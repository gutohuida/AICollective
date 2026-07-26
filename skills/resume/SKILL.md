---
name: resume
description: Rehydrate context from a handoff file written by /handoff and continue the work. Use at the start of a fresh session, after clearing or compacting, or when the user says "resume", "pick up where we left off", "continue from the handoff", or points at a handoff file. Pairs with /handoff.
---

Restore working context from a durable handoff file, verify it still describes reality, and
continue.

**Usage:** `/resume` (loads the latest) or `/resume <path-to-handoff.md>`.

Agent-agnostic: the handoff is plain markdown, so a session started by one CLI agent can be
resumed by another. The handoff records which agent wrote it — note it if the tooling
assumptions differ from yours.

## Step 1 — Locate the handoff

If a path was given as an argument, use it. Otherwise search every known location — the
previous session may have run under a different agent:

```bash
cat .handoffs/LATEST.md .claude/handoffs/LATEST.md .agents/handoffs/LATEST.md 2>/dev/null
ls -t .handoffs/*.md .claude/handoffs/*.md .agents/handoffs/*.md 2>/dev/null | head -5
```

Read the newest one. If several are recent, read the newest and check its
`**Previous handoff:**` link — follow the chain back only as far as you need for the current
next-step, usually zero or one hop.

If handoffs turn up in more than one directory, say so — the chain has been split, and the
newest file may not be the newest *work*. Reconcile by timestamp before trusting either.

If no handoff exists anywhere, say so plainly and ask what the user wants to work on. Do not
invent context or guess from git history alone.

## Step 2 — Verify the handoff against reality

A handoff is a snapshot; the tree may have moved. Check before trusting it:

```bash
git branch --show-current
git log --oneline -5
git status --short
```

Compare against the handoff's `## Git state`:

- **Same branch, same HEAD, same dirty files** → trustworthy, proceed.
- **HEAD moved forward** → someone (possibly another session, possibly another agent)
  committed since. Run `git log <handoff-sha>..HEAD --stat` and reconcile: the handoff's
  "next steps" may already be done. Flag anything that no longer applies.
- **Different branch** → say so before doing anything. Confirm which branch the work belongs on.
- **Files listed as touched are now clean/absent** → the work was committed, stashed, or
  reverted. Determine which; do not assume.

Also verify the paths in `## Files touched` and `## Read on resume` still exist.

State any drift you found in one or two lines. Silent reconciliation is how a resumed session
redoes finished work.

## Step 3 — Reload only what the next step needs

Read the files under `## Read on resume`, plus any file that next-step-1 will edit.

**Do not** bulk-read everything the handoff mentions. The point of a fresh window is that it
is fresh — refilling it with context you will not use recreates the exact problem the handoff
solved. Load lazily; you can always read more later.

## Step 4 — Re-establish the guardrails

Before touching anything, internalize `## Constraints and user directives` and `## Dead ends`
from the handoff. These are the two sections whose loss causes the most damage: without them
a resumed session cheerfully violates a stated rule or re-tries a known failure. Treat quoted
user directives as still binding — they were not withdrawn, just forgotten.

## Step 5 — Confirm and continue

Report back, briefly:

1. **Where we are** — one or two sentences from `## Current state`.
2. **Drift** — anything that changed since the handoff, or "tree matches the handoff".
3. **Constraints still in force** — the quoted directives, condensed to a list.
4. **Next action** — restate next-step-1 concretely, as you are about to do it.

Then do it. If the handoff has entries under `## Open questions for the user`, or if drift
means the recorded next step no longer makes sense, ask **before** starting work rather than
proceeding on a guess.

## Chaining

When this resumed session in turn fills up, run `/handoff` again. It will read this handoff
and carry forward what is still true — so state is always re-derived from the live session
plus a durable file, never from a summary of a summary. That is what stops quality decaying
across a long chain of sessions, and it holds across agent switches too.
