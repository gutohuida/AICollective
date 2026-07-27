#!/usr/bin/env python3
"""Structural validator for a self-contained HTML specification.

Usage:  python validate.py <spec.html> [more.html ...]

Stdlib only; runs on Python 3.6+. Exit code 1 if any ERROR is reported
(warnings alone do not fail the run).

ERRORs are contract breaks - a spec with one cannot be trusted by a tool or a
reader: unbalanced tags, duplicate ids, dead in-document anchors, external
resource references (the file must render offline), tasks missing the
machine-readable attributes, requirement references that point at nothing, and
an approved spec that still carries unresolved clarification markers.

WARNINGs are quality signals from the spec-driven-development research: missing
non-goals, no producer/consumer split, requirements without a modal verb,
acceptance criteria that are not Given/When/Then, branching behavior written as
prose instead of a numbered algorithm, unlabelled non-normative text, and vague
unfalsifiable wording.
"""

import io
import re
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

# Heuristic: phrases that cannot be turned into a passing or failing test.
# Kept narrow on purpose - bare "fast"/"slow" appear in legitimate technical
# prose ("slow consumers"), so only unfalsifiable *claims* are listed.
VAGUE = ["as fast as possible", "reasonably fast", "should be fast", "must be fast",
         "robust", "scalable", "user-friendly", "intuitive", "seamless",
         "highly performant", "as needed", "and so on", "where appropriate",
         "if necessary", "handled properly", "best effort"]

MODALS = re.compile(r"\b(MUST NOT|MUST|SHALL NOT|SHALL|SHOULD NOT|SHOULD|MAY)\b", re.I)


class Structure(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.stack = []
        self.ids = {}
        self.hrefs = []          # (fragment, line)
        self.external = []       # (url, line)
        self.tasks = []          # (attrs dict, line)
        self.errors = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        line = self.getpos()[0]
        if "id" in d:
            self.ids[d["id"]] = self.ids.get(d["id"], 0) + 1
        href = d.get("href", "")
        if href.startswith("#"):
            self.hrefs.append((href[1:], line))
        for attr in ("href", "src", "action", "data"):
            val = d.get(attr, "")
            if re.match(r"^(https?:)?//", val):
                self.external.append((val, line))
        if "task" in d.get("class", "").split():
            self.tasks.append((d, line))
        if tag not in VOID:
            self.stack.append((tag, line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("stray </%s> at line %d" % (tag, self.getpos()[0]))
            return
        open_tag, line = self.stack.pop()
        if open_tag != tag:
            self.errors.append("<%s> opened at line %d closed by </%s> at line %d"
                               % (open_tag, line, tag, self.getpos()[0]))


def strip_tags(html):
    html = re.sub(r"(?s)<(script|style|pre|code)\b.*?</\1>", " ", html)
    return re.sub(r"<[^>]+>", " ", html)


def check(path):
    src = io.open(path, encoding="utf-8").read()
    errors, warnings = [], []

    p = Structure()
    p.feed(src)
    p.close()
    errors.extend(p.errors)
    if p.stack:
        errors.append("unclosed at EOF: %s" % ", ".join(
            "<%s> (line %d)" % (t, l) for t, l in p.stack))

    dupes = sorted(i for i, n in p.ids.items() if n > 1)
    if dupes:
        errors.append("duplicate ids: %s" % ", ".join(dupes))

    dead = sorted({"#%s (line %d)" % (f, l) for f, l in p.hrefs if f and f not in p.ids})
    if dead:
        errors.append("dead in-document anchors: %s" % ", ".join(dead))

    if p.external:
        errors.append("external resources (spec must render offline): %s" % ", ".join(
            "%s (line %d)" % (u, l) for u, l in p.external[:5]))

    # --- machine-readable task contract -------------------------------------
    req_ids = {i for i in p.ids if re.match(r"^(FR|NFR|SM|RM)[-.]", i, re.I)}
    for attrs, line in p.tasks:
        tid = attrs.get("data-task-id")
        if not tid:
            errors.append("task at line %d has no data-task-id" % line)
        if attrs.get("data-status") not in ("pending", "done"):
            errors.append("task %s (line %d) has data-status=%r; expected pending|done"
                          % (tid or "?", line, attrs.get("data-status")))
        refs = [r.strip() for r in attrs.get("data-requirements", "").split(",") if r.strip()]
        if not refs:
            errors.append("task %s (line %d) traces to no requirement (data-requirements)"
                          % (tid or "?", line))
        for r in refs:
            if req_ids and r not in p.ids:
                errors.append("task %s (line %d) references unknown requirement %s"
                              % (tid or "?", line, r))

    task_ids = [a.get("data-task-id") for a, _ in p.tasks if a.get("data-task-id")]
    if len(set(task_ids)) != len(task_ids):
        errors.append("duplicate data-task-id values")

    # --- approval gate ------------------------------------------------------
    status = re.search(r'name="(?:[a-z]+-)?spec-status"\s+content="([^"]*)"', src)
    status = status.group(1) if status else None
    unresolved = len(re.findall(r"NEEDS CLARIFICATION", src))
    if status == "approved" and unresolved:
        errors.append("status=approved but %d [NEEDS CLARIFICATION] marker(s) remain" % unresolved)
    elif unresolved:
        warnings.append("%d [NEEDS CLARIFICATION] marker(s) - resolve before approval" % unresolved)

    # --- rendering contract -------------------------------------------------
    if "<style" not in src:
        warnings.append("no inline <style> - spec should carry its own presentation")
    if 'data-theme="dark"' not in src:
        warnings.append('no :root[data-theme="dark"] layer - viewer theme toggles will not apply')
    if "prefers-color-scheme" not in src:
        warnings.append("no prefers-color-scheme layer - dark mode will not work standalone")
    if 'a[href^="#"]' not in src:
        warnings.append("no same-document anchor-click interceptor - hash navigation can blank a sandboxed iframe")

    # --- content conventions ------------------------------------------------
    # Expectations scale with the document kind: a system map has no acceptance
    # criteria, a roadmap has no conformance split. Declare it in <head> with
    # <meta name="spec-kind" content="change-spec|system-map|roadmap|baseline">.
    # A project-specific prefix (e.g. aw-spec-kind) is accepted too.
    kind = re.search(r'name="(?:[a-z]+-)?spec-kind"\s+content="([^"]*)"', src)
    kind = kind.group(1) if kind else "change-spec"

    text = strip_tags(src)
    low = text.lower()

    if not re.search(r"non-?goals?|out of scope|deferred", low):
        warnings.append("no Non-Goals / out-of-scope section - scope is being inferred from omission")
    if kind in ("change-spec", "system-map") and not (
            re.search(r"producer", low) and re.search(r"consumer", low)):
        warnings.append("no producer/consumer conformance split (WHATWG 1.9.1)")
    if not re.search(r"\bmust\b", low):
        warnings.append("no MUST-level requirement - nothing here is binding")
    if 'class="algorithm"' not in src and "<ol" not in src:
        warnings.append("no numbered algorithm - ordered or conditional behavior belongs in an <ol>")
    if not re.search(r'class="[^"]*\b(note|example|warning|issue)\b', src):
        warnings.append("no labelled note/example/warning blocks - non-normative text is indistinguishable")
    if kind == "change-spec":
        if not re.search(r"\bgiven\b.*\bwhen\b.*\bthen\b", low, re.S):
            warnings.append("no Given/When/Then acceptance criteria found")
        if not p.tasks:
            warnings.append("no li.task elements - a change spec carries its own task list")

    # Requirement blocks that state no modal verb. Only elements that declare
    # themselves as requirements are checked: a class containing "requirement",
    # or a table row whose id is an FR/NFR identifier. Registry tables (a list of
    # contracts, terms, or entities keyed by ID) are legitimately modal-free.
    for m in re.finditer(r'(?s)<(tr|div|li|p)([^>]*\bid="([A-Z]+[-.][A-Za-z0-9.-]+)"[^>]*)>(.*?)</\1>', src):
        tag, attrs, rid, inner = m.group(1), m.group(2), m.group(3), m.group(4)
        is_req = "requirement" in attrs or (tag == "tr" and re.match(r"^(FR|NFR)[-.]", rid, re.I))
        placeholder = re.search(r"(XXX|NNN|000)\b", rid)  # legend/template rows
        if not is_req or placeholder:
            continue
        if not MODALS.search(strip_tags(inner)):
            warnings.append("requirement %s states no MUST/SHOULD/MAY/SHALL" % rid)

    hits = sorted({w for w in VAGUE if re.search(r"\b%s\b" % re.escape(w), low)})
    if hits:
        warnings.append("unfalsifiable wording: %s" % ", ".join(hits))

    return errors, warnings, {
        "ids": len(p.ids), "anchors": len(p.hrefs), "tasks": len(p.tasks),
        "requirements": len(req_ids), "status": status or "n/a",
    }


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    failed = False
    for path in argv[1:]:
        errors, warnings, stats = check(path)
        print("== %s" % path)
        print("   %d ids | %d in-doc anchors | %d requirement anchors | %d tasks | status=%s"
              % (stats["ids"], stats["anchors"], stats["requirements"], stats["tasks"], stats["status"]))
        for e in errors:
            print("   ERROR   %s" % e)
        for w in warnings:
            print("   warning %s" % w)
        if not errors and not warnings:
            print("   clean")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
