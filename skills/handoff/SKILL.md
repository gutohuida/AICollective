---
name: handoff
description: Compact the session by writing a durable, structured handoff file to disk before clearing or compacting. Use when context is filling up, when finishing a work chunk, before clearing/compacting the session, or when the user says "handoff", "save context", "compact", "wrap up this session", or "I'm going to start a fresh session". Pairs with /resume.
---

Write a durable handoff artifact so this session's state survives a context reset.

**Core principle:** the handoff file on disk is the real memory — the context window is
scratch space. In-place summarization is lossy and compounds (a summary of a summary of a
summary); a structured file re-derived from the *live* session each time does not.

Agent-agnostic: works in any CLI agent that can read and write files. Where this file says
"reset the context", use whatever your CLI calls it — `/clear`, `/compact`, `/new`; the
names vary by agent.

## Step 0 — Pick the right move

Choose one, state which you chose and why in one line, then proceed:

| Situation | Move |
|---|---|
| Finished a chunk of work; next step is a different task | **Full handoff → then clear.** Best quality: fresh window, zero rot. |
| Mid-task, deep in one thread, lots of stale debugging noise | **Full handoff → then compact with steering.** Keeps conversational flow. |
| Context is fine (<50%) and everything loaded is still relevant | **Do nothing.** Say so and stop. Compaction is not free. |
| User explicitly asked for a handoff | **Full handoff**, regardless of the above. |

Do this **early** — around 50–70% context used, not at 95%. The model writing the summary
is at its least capable exactly when the window is fullest, which is the single most common
cause of a bad compaction. If the user invoked this late, still do it, but be extra careful
with Step 3's checklist.

## Step 1 — Gather hard state (deterministic, cheap, no guessing)

Run these and use the real output. Do not recall git state from memory:

```bash
git branch --show-current
git status --short
git log --oneline -8
git diff --stat HEAD
git log origin/$(git branch --show-current)..HEAD --oneline 2>/dev/null || echo "no upstream"
```

Also check for a prior handoff to chain from — check every location, since a previous
session may have run under a different agent:

```bash
ls -t .handoffs/*.md .claude/handoffs/*.md .agents/handoffs/*.md 2>/dev/null | head -5
```

If a prior handoff exists, **read it** and carry forward anything still true. Never let a
fact survive only as your own recollection of a previous summary.

## Step 2 — Write the file

**Directory:** if any of `.handoffs/`, `.claude/handoffs/`, or `.agents/handoffs/` already
contains handoffs, keep using that one — splitting the chain across directories is how a
resumed session silently loads the wrong history. If none exists, create `.handoffs/`.

**Filename:** `YYYY-MM-DD-HHMM-<short-slug>.md`, using the real current date/time. Also
write/overwrite `LATEST.md` in the same directory containing just the relative path of the
newest handoff, so `/resume` has a fixed entry point.

If the user names a different location, use theirs. If the repo tracks the chosen directory,
check whether handoffs should be gitignored and mention it once — they are session notes,
so ignoring them is usually right.

### Template — every section is required; write "None." rather than deleting a heading

```markdown
# Handoff: <one-line task title>

**Date:** <ISO datetime> · **Branch:** <branch> · **HEAD:** <short sha>
**Agent:** <which CLI/model wrote this>
**Previous handoff:** <relative path, or "none — first handoff in this chain">
**Status:** <in progress | blocked | chunk complete>

## Goal
What we are ultimately trying to achieve, in 1–3 sentences. Include the *why*, not just
the *what* — the why is what lets the next session make judgment calls.

## Current state
Where things actually stand right now. What works. What is half-done and in what way.
Be concrete: "the parser handles nested blocks but not escapes" beats "parser mostly done".

## Files touched
One line per file: full path — what changed in it and whether it is finished.
This is the #1 thing summaries silently lose. Never write "various files" or "several
components". List every path. Cross-check against `git status` / `git diff --stat` output.

## Key decisions
Each: the decision, the reason, and — critically — the alternatives rejected and why.
A rejected alternative with no recorded reason will be re-proposed and re-tried.

## Constraints and user directives (verbatim)
Quote the user's explicit instructions, preferences, and prohibitions **word for word**.
Includes things stated early in the session that feel "settled" — those are precisely
what compaction erases. E.g. "no new dependencies", "don't touch the migration files",
"always run ruff before committing".

## Dead ends
Things tried that did not work, and the symptom. Prevents the next session from paying
for the same failure twice. Include near-misses that looked correct but weren't.

## Verification
What was actually run (exact commands) and the actual result. Then, separately and
explicitly: **what was NOT tested.** Never imply verification that did not happen.

## Git state
Branch, HEAD sha, clean/dirty, uncommitted paths, unpushed commits. From Step 1's output.

## Next steps
Numbered. Step 1 must be immediately executable with no further decisions — a specific
file and a specific change, not "continue the refactor".

## Open questions for the user
Anything genuinely blocked on a human decision. Empty is a fine and common answer.

## Read on resume
3–6 file paths worth reloading, each with a reason. Paths only — do not paste contents.
Pointers are cheap and always current; pasted excerpts are expensive and go stale.
```

## Step 3 — Validate before you finish

Re-read what you wrote and fix any of these:

- [ ] Every file path mentioned actually exists (or is explicitly marked "to be created").
- [ ] `## Files touched` accounts for everything in `git status --short` and `git diff --stat`.
- [ ] No dangling references: no "the fix we discussed", "that approach", "the bug" without
      the content stated inline. The next session cannot see this conversation.
- [ ] Constraints are quoted, not paraphrased.
- [ ] Verification section distinguishes ran-and-passed from not-run. No implied testing.
- [ ] Next step 1 is executable as written by someone with zero prior context — including
      a different agent, which may not share this one's tools or conventions.
- [ ] Nothing important lives *only* in the conversation. If it does, it is now lost.

Bias to **recall over brevity** on the first pass: it is far cheaper to include a fact that
turns out irrelevant than to lose one that mattered. Trim only obvious redundancy.

## Step 4 — Report and hand back control

Print:
1. The handoff file path.
2. A 3–5 bullet digest of what it captured.
3. The recommended next move, exactly one of:
   - **Clear the context, then run `/resume`** — for a task boundary (preferred; cleanest
     window).
   - **Compact with explicit steering** — for staying mid-thread. Always supply the
     steering text, e.g. "keep the auth refactor, drop the test debugging". An unsteered
     compact guesses at where the work is heading and guesses badly.

Name the actual command for the CLI you are running in if you know it; otherwise describe
the move and let the user pick the command.

**Do not reset the context yourself** — the user decides when the window resets. State the
recommendation and stop.
