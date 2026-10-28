#!/usr/bin/env python3
"""Build the deliverable files for one edition from its brief.md.

  build_outputs.py briefs/2026-10-29/brief.md [--config config/brief_config.json]

Writes, next to the brief:
  email.html        the client email body in the house format (paste-ready)
  email.txt         plain-text version of the brief (used for the Domyn/Fior copy)
  subject.txt       "Daily Media Monitoring, 29th October"
  recipients.txt    To / Cc lines from the config
  whatsapp.txt      the WhatsApp message to accompany the audio
  domyn_fior.txt    the internal forward: standard line plus the plain brief
  README.md         what is in the package and the reviewer checklist

The HTML mirrors the sent emails: "Good morning team," then the Inception42
coverage bullets with no heading, bold section headings, bullets with 8pt
paragraph spacing, prose for Top Line and Strategic Counter Narrative,
Watch Outs in red (#C00000), inline links on the publication names.
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brief_format_check import parse, SECTIONS, PROSE  # noqa: E402

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
FONT = "font-family:Aptos,Calibri,Arial,sans-serif;font-size:11pt;"
P = f'<p style="{FONT}margin:0 0 8pt 0;">'
H = f'<p style="{FONT}margin:12pt 0 8pt 0;"><b>'
LI = f'<li style="{FONT}margin:0 0 8pt 0;">'
LI_RED = f'<li style="{FONT}margin:0 0 8pt 0;color:#C00000;">'


def ordinal(n):
    return f"{n}{'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def md_inline_to_html(text, red=False):
    out, pos = [], 0
    for m in LINK_RE.finditer(text):
        out.append(html.escape(text[pos:m.start()]))
        color = ' style="color:#C00000;"' if red else ""
        out.append(f'<a href="{html.escape(m.group(2), quote=True)}"{color}>{html.escape(m.group(1))}</a>')
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return "".join(out)


def md_inline_to_text(text):
    return LINK_RE.sub(lambda m: f"{m.group(1)} ({m.group(2)})", text)


def build_html(parsed):
    s = parsed["sections"]
    parts = [f'<div style="{FONT}">', f"{P}Good morning team,</p>"]
    if "Inception42 coverage" in s:
        parts.append("<ul style=\"margin:0 0 8pt 0;\">")
        for l in s["Inception42 coverage"]:
            if l.strip():
                parts.append(f"{LI}{md_inline_to_html(l[2:].strip())}</li>")
        parts.append("</ul>")
    for name in SECTIONS:
        if name == "Inception42 coverage" or name not in s:
            continue
        parts.append(f"{H}{html.escape(name)}</b></p>")
        lines = [l for l in s[name] if l.strip()]
        if name in PROSE:
            for l in lines:
                parts.append(f"{P}{md_inline_to_html(l.strip())}</p>")
        else:
            red = name == "Watch Outs"
            parts.append("<ul style=\"margin:0 0 8pt 0;\">")
            for l in lines:
                li = LI_RED if red else LI
                parts.append(f"{li}{md_inline_to_html(l[2:].strip(), red=red)}</li>")
            parts.append("</ul>")
    parts.append("</div>")
    return "\n".join(parts) + "\n"


def build_text(parsed):
    s = parsed["sections"]
    out = ["Good morning team,", ""]
    if "Inception42 coverage" in s:
        for l in s["Inception42 coverage"]:
            if l.strip():
                out.append("- " + md_inline_to_text(l[2:].strip()))
        out.append("")
    for name in SECTIONS:
        if name == "Inception42 coverage" or name not in s:
            continue
        out.append(name.upper() if False else name)
        out.append("")
        for l in s[name]:
            if not l.strip():
                continue
            out.append(("- " + md_inline_to_text(l[2:].strip())) if l.startswith("- ") else md_inline_to_text(l.strip()))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("--config", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "brief_config.json"))
    a = ap.parse_args()
    parsed, problems = parse(a.brief)
    if problems:
        for p in problems:
            print(f"{a.brief}: {p}", file=sys.stderr)
        sys.exit("brief.md does not pass the format check; fix it before building")
    cfg = json.load(open(a.config, encoding="utf-8"))
    fm = parsed["front_matter"]
    date = dt.date.fromisoformat(fm["date"])
    folder = os.path.dirname(os.path.abspath(a.brief))
    day = ordinal(date.day)
    month = date.strftime("%B")

    html_body = build_html(parsed)
    text_body = build_text(parsed)
    subject = cfg["email"]["subject_template"].format(day=day, month=month)
    whatsapp = cfg["whatsapp"]["message_template"].format(month=month, day=date.day, year=date.year)
    domyn = cfg["internal_copy"]["message"] + "\n\n" + text_body
    recipients = ("To: " + "; ".join(cfg["email"]["to"]) + "\n" + "Cc: " + "; ".join(cfg["email"]["cc"]) + "\n")
    audio_name = cfg["audio"]["filename_template"].format(day=date.day, month=date.strftime("%b"))

    files = {
        "email.html": html_body,
        "email.txt": text_body,
        "subject.txt": subject + "\n",
        "recipients.txt": recipients,
        "whatsapp.txt": whatsapp + "\n",
        "domyn_fior.txt": domyn,
    }
    for name, content in files.items():
        open(os.path.join(folder, name), "w", encoding="utf-8").write(content)

    readme = f"""# Inception42 Morning Brief package, {date.strftime('%A %d %B %Y')}

Generated draft for review. Nothing in this folder has been sent.

| File | Use |
|------|-----|
| brief.rtf | The brief, formatted for Word or Outlook (brief.md in the repository is the canonical source) |
| email.html | Client email body. Open in a browser, select all, copy, paste into a new Outlook message |
| subject.rtf | Email subject: `{subject}` |
| recipients.rtf | To and Cc lists for the client email |
| {audio_name} | Audio bulletin to attach to the email and post on WhatsApp (if produced) |
| script.rtf | The ElevenLabs script the audio was made from |
| whatsapp.rtf | Message to post with the audio in the Inception42 x Hawthorn group |
| domyn_fior.rtf | Internal copy for domyn@ and fior@ (written brief only, no audio) |
| sensitive_articles.rtf | Items held out of the brief for the comms team to decide on; share manually |
| candidates.rtf | Everything that was considered, with where it came from |
| run_log.rtf | What the run did, every check result, anything it could not verify |

Reviewer checklist (about 15 minutes):
1. Read run_log.rtf first: it lists any bullet that is snippet-verified rather than fetch-verified, any unresolved link, and any audit warning.
2. Read the brief for judgment calls: Top Line thesis, placement, the Strategic Counter Narrative's Inception42 line, Watch Outs.
3. Spot-check two or three links.
4. Listen to the audio opening and the Gulf transition.
5. Send the email at 09:00 GST, post the WhatsApp message with the audio, forward domyn_fior.rtf, then deal with sensitive_articles.rtf.
"""
    open(os.path.join(folder, "README.md"), "w", encoding="utf-8").write(readme)
    print(f"built {len(files) + 1} files in {folder}")


if __name__ == "__main__":
    main()
