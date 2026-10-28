#!/usr/bin/env python3
"""Transcribe a sent Daily Media Monitoring email into the canonical brief.md.

Input is one of:
  * the JSON object returned by the Microsoft 365 connector's read_resource
    for a mail:///messages/... URI (has subject, body.content, sentDateTime,
    sender), or
  * a raw .eml file (MIME; the text/html part is used), or
  * a bare HTML file (then --subject and --sent are required).

Usage:
  email_to_brief.py INPUT --out briefs/2026-10-28/brief.md [--subject S] [--sent ISO] [--sender ADDR]

The transcription is verbatim: text and links are kept exactly as sent.
Sections are recognised by their bold heading paragraphs; bullets above
the Top Line become the "Inception42 coverage" section.
"""
import argparse
import datetime as dt
import email
import email.policy
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

SECTION_ALIASES = {
    "top line": "Top Line",
    "topline": "Top Line",
    "power": "Power",
    "regulation & trust": "Regulation & Trust",
    "regulation and trust": "Regulation & Trust",
    "enterprise & investment": "Enterprise & Investment",
    "enterprise and investment": "Enterprise & Investment",
    "ai & innovation": "AI & Innovation",
    "ai and innovation": "AI & Innovation",
    "alliances and partnerships": "Alliances and Partnerships",
    "alliances & partnerships": "Alliances and Partnerships",
    "abu dhabi & gulf": "Abu Dhabi & Gulf",
    "abu dhabi and gulf": "Abu Dhabi & Gulf",
    "abu dhabi and the gulf": "Abu Dhabi & Gulf",
    "strategic counter narrative": "Strategic Counter Narrative",
    "strategic counter-narrative": "Strategic Counter Narrative",
    "watch outs": "Watch Outs",
    "watch out": "Watch Outs",
    "watch-outs": "Watch Outs",
}
ORDER = ["Inception42 coverage", "Top Line", "Power", "Regulation & Trust",
         "Enterprise & Investment", "AI & Innovation", "Alliances and Partnerships",
         "Abu Dhabi & Gulf", "Strategic Counter Narrative", "Watch Outs"]
PROSE = {"Top Line", "Strategic Counter Narrative"}
BULLET_MARKS = ("·", "•", "-", "•", "o ")


class Block:
    def __init__(self, kind):
        self.kind = kind          # 'p' or 'li'
        self.parts = []           # list of str (text) or (text, href)
        self.bold_chars = 0
        self.total_chars = 0
        self.is_bullet_para = False

    def text(self):
        out = []
        for p in self.parts:
            if isinstance(p, tuple):
                t, href = p
                t = t.strip()
                if href and t:
                    out.append(f"[{t}]({href})")
                elif t:
                    out.append(t)
            else:
                out.append(p)
        s = "".join(out)
        s = re.sub(r"[ \t ]+", " ", s)
        s = re.sub(r"\s+([,.;:])", r"\1", s)
        s = s.replace(") /[", ") / [").replace(")/ [", ") / [").replace(")/[", ") / [")
        return s.strip()

    def plain(self):
        return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", self.text())


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []
        self.cur = None
        self.href = None
        self.link_text = []
        self.bold = 0
        self.in_style = False
        self.in_signature = False
        self.pstyle = ""

    def _open(self, kind, attrs):
        if self.cur is not None:
            self._close()
        self.cur = Block(kind)
        self.pstyle = dict(attrs).get("style", "") or ""
        self.cur.is_bullet_para = "text-indent" in self.pstyle and "-" in self.pstyle

    def _close(self):
        if self.cur is not None and self.cur.text():
            self.blocks.append(self.cur)
        self.cur = None

    def handle_starttag(self, tag, attrs):
        if tag == "style":
            self.in_style = True
        elif tag in ("p", "div", "li", "td"):
            self._open("li" if tag == "li" else "p", attrs)
        elif tag == "br" and self.cur is not None:
            self.cur.parts.append("\n")
        elif tag == "a":
            href = dict(attrs).get("href", "")
            if href.startswith("http"):
                self.href = html.unescape(href)
                self.link_text = []
        elif tag in ("b", "strong"):
            self.bold += 1

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
        elif tag in ("p", "div", "li", "td"):
            self._close()
        elif tag == "a" and self.href is not None:
            if self.cur is None:
                self.cur = Block("p")
            self.cur.parts.append(("".join(self.link_text), self.href))
            self.href = None
            self.link_text = []
        elif tag in ("b", "strong") and self.bold:
            self.bold -= 1

    def handle_data(self, data):
        if self.in_style:
            return
        if self.href is not None:
            self.link_text.append(data)
            return
        if self.cur is None:
            if not data.strip():
                return
            self.cur = Block("p")
        self.cur.parts.append(data)
        n = len(data.strip())
        self.cur.total_chars += n
        if self.bold:
            self.cur.bold_chars += n


def html_to_blocks(markup):
    p = Parser()
    p.feed(markup)
    p.close()
    out = []
    for b in p.blocks:
        t = b.text()
        if not t or t.strip() in ("\xa0",):
            continue
        out.append(b)
    return out


def classify(blocks):
    """Return dict section -> list of lines, plus opener flag."""
    sections = {}
    current = None
    opener = False
    pre_topline_bullets = []
    for b in blocks:
        plain = b.plain().strip()
        low = plain.lower().rstrip(":").strip()
        # signature / end detection
        if re.fullmatch(r"[A-Z][A-Z .'-]{3,}", plain) and len(plain.split()) <= 4 and current:
            break
        if low.startswith("+971") or "hawthornadvisors.com" in low and len(plain) < 40:
            if current:
                break
            continue
        if low in ("good morning team", "good morning team,", "good morning,", "good morning team!"):
            opener = True
            continue
        if low in SECTION_ALIASES and b.bold_chars >= max(1, b.total_chars - 2):
            current = SECTION_ALIASES[low]
            sections.setdefault(current, [])
            continue
        text = b.text()
        # strip leading bullet glyphs
        stripped = text
        for m in BULLET_MARKS:
            if stripped.startswith(m):
                stripped = stripped[len(m):].strip()
                break
        is_bullet = b.kind == "li" or b.is_bullet_para or stripped != text
        stripped = re.sub(r"\s+", " ", stripped.replace("\n", " ")).strip()
        if not stripped:
            continue
        if current is None:
            if is_bullet or re.search(r"\]\(https?://", stripped):
                pre_topline_bullets.append("- " + stripped)
            continue
        if current in PROSE:
            sections[current].append(stripped)
        else:
            sections[current].append("- " + stripped if not stripped.startswith("- ") else stripped)
    if pre_topline_bullets:
        sections["Inception42 coverage"] = pre_topline_bullets
    for k in list(sections):
        if k in PROSE and len(sections[k]) > 1:
            sections[k] = [" ".join(sections[k])]
    return sections, opener


def load(path):
    raw = open(path, "rb").read()
    text = raw.decode("utf-8", errors="replace")
    stripped = text.lstrip()
    meta = {}
    if stripped.startswith("{"):
        j = json.loads(stripped)
        meta["subject"] = j.get("subject", "")
        meta["sent"] = j.get("sentDateTime") or j.get("receivedDateTime") or ""
        s = j.get("sender") or {}
        meta["sender"] = s.get("address", "") if isinstance(s, dict) else str(s)
        body = j.get("body", {}).get("content", "")
        return body, meta
    if re.match(r"(?im)^(From|Received|Return-Path|MIME-Version|Subject):", stripped[:4000]):
        msg = email.message_from_bytes(raw, policy=email.policy.default)
        meta["subject"] = str(msg.get("subject", ""))
        d = msg.get("date")
        try:
            meta["sent"] = email.utils.parsedate_to_datetime(d).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if d else ""
        except Exception:
            meta["sent"] = ""
        meta["sender"] = email.utils.parseaddr(str(msg.get("from", "")))[1]
        part = msg.get_body(preferencelist=("html", "plain"))
        body = part.get_content() if part is not None else ""
        return body, meta
    return text, meta


def ordinal_date_from_subject(subject):
    m = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)(?:\s+(\d{4}))?", subject or "", re.I)
    if not m:
        return None
    day = int(m.group(1))
    month = dt.datetime.strptime(m.group(2)[:3], "%b").month
    year = int(m.group(3)) if m.group(3) else 2026
    return dt.date(year, month, day)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", required=True)
    ap.add_argument("--subject")
    ap.add_argument("--sent", help="ISO timestamp of the send, UTC")
    ap.add_argument("--sender")
    ap.add_argument("--source", default="outlook-sent")
    a = ap.parse_args()

    body, meta = load(a.input)
    subject = a.subject or meta.get("subject") or ""
    sent = a.sent or meta.get("sent") or ""
    sender = a.sender or meta.get("sender") or ""
    date = ordinal_date_from_subject(subject)
    if date is None and sent:
        date = dt.datetime.fromisoformat(sent.replace("Z", "+00:00")).date()
    if date is None:
        sys.exit("cannot determine the edition date; pass --subject or --sent")

    blocks = html_to_blocks(body)
    sections, opener = classify(blocks)
    if not sections:
        sys.exit("no sections recognised; inspect the input")

    lines = ["---",
             f"date: {date.isoformat()}",
             f"weekday: {date.strftime('%A')}",
             "edition: morning",
             f"subject: {subject}",
             f"sent_at: {sent}",
             f"sender: {sender}",
             f"source: {a.source}",
             "---", "", "Good morning team,", ""]
    for name in ORDER:
        if name in sections and sections[name]:
            lines.append(f"## {name}")
            lines.extend(sections[name])
            lines.append("")
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write("\n".join(lines).rstrip() + "\n")
    found = [s for s in ORDER if s in sections]
    print(f"wrote {a.out}: {len(blocks)} blocks, sections: {', '.join(found)}")
    if not opener:
        print("note: opener 'Good morning team,' not detected in the source", file=sys.stderr)


if __name__ == "__main__":
    main()
