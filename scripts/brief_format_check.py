#!/usr/bin/env python3
"""Structural check of a brief.md against docs/brief-format.md.

Usage: brief_format_check.py briefs/2026-10-28/brief.md [...]
Exit 0 when every file parses cleanly, 1 otherwise. Prints one line per
problem. Used by the seeding transcription and by the audit.
"""
import re
import sys

SECTIONS = [
    "Inception42 coverage",
    "Top Line",
    "Power",
    "Regulation & Trust",
    "Enterprise & Investment",
    "AI & Innovation",
    "Alliances and Partnerships",
    "Abu Dhabi & Gulf",
    "Strategic Counter Narrative",
    "Watch Outs",
]
PROSE = {"Top Line", "Strategic Counter Narrative"}
REQUIRED_FM = ["date", "weekday", "edition", "subject", "source"]
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def parse(path):
    text = open(path, encoding="utf-8").read()
    problems = []
    if not text.startswith("---\n"):
        return None, ["missing front matter"]
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, ["unterminated front matter"]
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    for k in REQUIRED_FM:
        if k not in fm:
            problems.append(f"front matter missing '{k}'")
    body = text[end + 5:]
    sections = {}
    order = []
    current = None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            if current not in SECTIONS:
                problems.append(f"unknown section heading '{current}'")
            if current in sections:
                problems.append(f"duplicate section '{current}'")
            sections[current] = []
            order.append(current)
        elif current is not None:
            sections[current].append(line)
    if "Good morning team," not in body.split("## ", 1)[0]:
        problems.append("opener 'Good morning team,' missing before first section")
    expected = [s for s in SECTIONS if s in sections]
    if order != expected:
        problems.append(f"sections out of order: {order}")
    for name, lines in sections.items():
        content = [l for l in lines if l.strip()]
        if not content:
            problems.append(f"section '{name}' is empty")
            continue
        if name in PROSE:
            if any(l.startswith("- ") for l in content):
                problems.append(f"section '{name}' should be prose, has bullets")
            if len(content) > 1:
                problems.append(f"section '{name}' has {len(content)} paragraphs, expected 1")
        else:
            for l in content:
                if not l.startswith("- "):
                    problems.append(f"section '{name}': non-bullet line: {l[:60]}")
                elif not LINK_RE.search(l):
                    problems.append(f"section '{name}': bullet without a link: {l[:60]}")
        for l in content:
            for m in re.finditer(r"\((https?://[^)\s]*signal-ai\.com[^)\s]*)\)", l):
                problems.append(f"section '{name}': Signal redirect link {m.group(1)[:60]}")
            for m in re.finditer(r"\]\(([^)]*)\)", l):
                url = m.group(1)
                if not url.startswith("http"):
                    problems.append(f"section '{name}': malformed link target '{url[:60]}'")
    if "Top Line" not in sections and fm.get("source") == "generated":
        problems.append("generated brief must have a Top Line")
    return {"front_matter": fm, "sections": sections, "order": order}, problems


def main(paths):
    bad = 0
    for p in paths:
        parsed, problems = parse(p)
        for pr in problems:
            print(f"{p}: {pr}")
        if problems:
            bad += 1
        else:
            print(f"{p}: ok")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
