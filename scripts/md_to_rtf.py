#!/usr/bin/env python3
"""Convert the package's Markdown and plain-text files to RTF for reviewers.

  md_to_rtf.py briefs/2026-10-29            # converts every .md and .txt in the folder
  md_to_rtf.py briefs/2026-10-29/brief.md   # converts one file

Writes <name>.rtf next to each source (folder mode skips email.txt, subject.txt, recipients.txt, whatsapp.txt and candidates.md, which stay in the repository; the send details are in README.rtf). The Markdown files stay in the repo
as the canonical, diffable text; the RTF files are what goes to SharePoint.

Handles: YAML front matter (dropped), # / ## / ### headings, bullet lists
(- or *), numbered lists, bold (**x**), italic (*x*), inline code, links
(clickable HYPERLINK fields showing the link text), tables (rendered as
tab-separated rows), and blank-line paragraph breaks. Watch Outs bullets
are red, matching the email. Font Aptos 11pt with Calibri fallback.
"""
import os
import re
import sys

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
ITAL_RE = re.compile(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])")
CODE_RE = re.compile(r"`([^`]+)`")
FM_RE = re.compile(r"\A---\n.*?\n---\n", re.S)
# stay in the repository only: email.txt is the plain-text source of the
# internal copy; subject, recipients and whatsapp are inside README.rtf;
# candidates is a long working record that the run log links to
SKIP = {"email.txt", "subject.txt", "recipients.txt", "whatsapp.txt", "candidates.md"}

HEADER = (
    r"{\rtf1\ansi\ansicpg1252\deff0\deflang2057"
    r"{\fonttbl{\f0\fswiss\fcharset0 Aptos;}{\f1\fswiss\fcharset0 Calibri;}}"
    r"{\colortbl;\red0\green0\blue0;\red192\green0\blue0;\red5\green99\blue193;}"
    "\n"
    r"\viewkind4\uc1\pard\f0\fs22\sa160\sl276\slmult1 "
    "\n"
)


def esc(text):
    out = []
    for ch in text:
        o = ord(ch)
        if ch == "\\":
            out.append(r"\\")
        elif ch == "{":
            out.append(r"\{")
        elif ch == "}":
            out.append(r"\}")
        elif o < 128:
            out.append(ch)
        elif o < 0x10000:
            out.append(r"\u%d?" % (o - 0x10000 if o > 32767 else o))
        else:
            # surrogate pair for characters outside the BMP
            o -= 0x10000
            hi, lo = 0xD800 + (o >> 10), 0xDC00 + (o & 0x3FF)
            out.append(r"\u%d?\u%d?" % (hi - 0x10000, lo - 0x10000))
    return "".join(out)


def inline(text):
    """Markdown inline formatting to RTF, links as clickable fields."""
    parts = []
    pos = 0
    for m in LINK_RE.finditer(text):
        parts.append(_fmt(text[pos:m.start()]))
        label, url = m.group(1), m.group(2)
        parts.append(
            r'{\field{\*\fldinst{HYPERLINK "%s"}}{\fldrslt{\cf3\ul %s}}}'
            % (esc(url).replace('"', ""), _fmt(label))
        )
        pos = m.end()
    parts.append(_fmt(text[pos:]))
    return "".join(parts)


def _fmt(text):
    text = esc(text)
    text = CODE_RE.sub(lambda m: r"{\f1 %s}" % m.group(1), text)
    text = BOLD_RE.sub(lambda m: r"{\b %s}" % m.group(1), text)
    text = ITAL_RE.sub(lambda m: r"{\i %s}" % m.group(1), text)
    return text


def convert(md):
    md = FM_RE.sub("", md.replace("\r\n", "\n"))
    out = [HEADER]
    red = False
    num = 0
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            num = 0
            i += 1
            continue
        hm = re.match(r"^(#{1,6})\s+(.*)$", line)
        if hm:
            level = len(hm.group(1))
            title = hm.group(2).strip()
            red = title.lower().startswith("watch out")
            size = {1: 32, 2: 26, 3: 24}.get(level, 22)
            out.append(r"{\pard\sb240\sa120\keepn\b\fs%d %s\par}" % (size, inline(title)) + "\n")
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            for r_i, cells in enumerate(rows):
                txt = r"\tab ".join(inline(c) for c in cells)
                if r_i == 0:
                    txt = r"{\b %s}" % txt
                out.append(r"{\pard\sa60\tx3600\tx7200 %s\par}" % txt + "\n")
            continue
        bm = re.match(r"^\s*[-*]\s+(.*)$", line)
        nm = re.match(r"^\s*(\d+)[.)]\s+(.*)$", line)
        if bm or nm:
            text = (bm or nm).group(1 if bm else 2)
            # continuation lines indented under the bullet
            while i + 1 < len(lines) and lines[i + 1].startswith("  ") and lines[i + 1].strip() and not re.match(r"^\s*[-*]\s+", lines[i + 1]) and not re.match(r"^\s*\d+[.)]\s+", lines[i + 1]):
                i += 1
                text += " " + lines[i].strip()
            if nm:
                num += 1
                marker = "%d." % num
            else:
                marker = "\\" + "u8226?"  # bullet character
            color = r"\cf2 " if red else ""
            out.append(
                r"{\pard\fi-360\li720\sa160 %s%s\tab %s\par}" % (color, marker, inline(text)) + "\n"
            )
            i += 1
            continue
        # paragraph: gather until blank line or block start
        para = [line.strip()]
        while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^(#{1,6}\s|\s*[-*]\s|\s*\d+[.)]\s|\|)", lines[i + 1]):
            i += 1
            para.append(lines[i].strip())
        color = r"\cf2 " if red else ""
        out.append(r"{\pard\sa160 %s%s\par}" % (color, inline(" ".join(para))) + "\n")
        i += 1
    out.append("}\n")
    return "".join(out)


def convert_file(path):
    src = open(path, encoding="utf-8").read()
    if path.endswith(".txt") and not path.endswith("email.txt"):
        # plain text: keep line breaks as paragraphs
        src = "\n\n".join(l for l in src.split("\n"))
    rtf = convert(src)
    dest = os.path.splitext(path)[0] + ".rtf"
    open(dest, "w", encoding="ascii", newline="\r\n").write(rtf)
    return dest


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    target = sys.argv[1]
    if os.path.isdir(target):
        files = sorted(
            os.path.join(target, f) for f in os.listdir(target)
            if (f.endswith(".md") or f.endswith(".txt")) and f not in SKIP
        )
    else:
        files = [target]
    for f in files:
        print("wrote", convert_file(f))


if __name__ == "__main__":
    main()
