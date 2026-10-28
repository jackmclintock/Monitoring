#!/usr/bin/env python3
"""Programmatic audit of a generated brief.md before it is packaged.

  audit_brief.py briefs/2026-10-29/brief.md [--registers registers] [--no-network] [--json out.json]

Hard failures (exit 1) and warnings (exit 0, listed) follow the house rules in
.claude/skills/morning-brief/reference/style_rules.md. The run fixes hard
failures and re-audits; warnings go in the run log for the reviewer.

Hard:
  structure      brief-format check passes; Top Line and SCN present; sections in order
  em-dash        no U+2014, and no U+2013 used as a dash
  signal-link    no Signal AI redirect or tracking links
  dup-link       no URL cited twice in the brief (a Watch Out may re-cite a story's source)
  reuse          no URL already in registers/do_not_reuse_register.md
  banned-phrase  none of the banned phrases or "according to"
  watch-outs     at most 2 bullets, each with a link, none starting "Watch whether"
  inception42    "Inception42" (or Jais, Ashish Koshy, Ibrahim Al Jallaf) appears only in
                 Inception42 coverage, Abu Dhabi & Gulf, Strategic Counter Narrative
  american       British spellings outside proper nouns and quotes
  dead-link      HTTP 404/410 on a cited URL (403/401/429 are bot walls: warning only)
Warnings:
  length         Top Line 4-6 sentences / 130-200 words; SCN 5-8 sentences / 150-230 words;
                 bullets over 70 words
  tics           "not X but Y" constructions, rhetorical question endings
  temporal       "today", "this week", "yesterday" in body text
  bot-wall       a cited URL answered 401/403/429 to the liveness probe
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brief_format_check import parse, PROSE  # noqa: E402

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
BANNED = [
    "widening gap", "defining story", "defining tension", "consequential",
    "the sharpest story", "reached by design", "the question the industry is only now learning to ask",
    "governance, not raw model capability, is the story", "broke ground", "according to",
    "delve", "navigate the complexities", "in today's rapidly evolving", "it's worth noting",
    "this matters because", "crucial", "leverage", "moreover", "game-changer", "game changer",
    "paradigm shift", "underscores", "testament to", "closer to home", "back in abu dhabi",
]
BRITISH = {
    "organise", "organised", "organisation", "organisations", "recognise", "recognised", "stabilise",
    "normalise", "prioritise", "prioritised", "emphasise", "characterise", "mobilise", "authorise",
    "authorised", "criticise", "criticised", "analyse", "analysed", "paralyse", "behaviour",
    "behaviours", "favour", "favours", "favoured", "labour", "harbour", "honour", "neighbour",
    "neighbours", "armour", "rumour", "rumours", "centre", "centres", "metre", "litre", "calibre",
    "defence", "offence", "licence", "licences", "practise", "programme", "programmes", "travelled",
    "traveller", "cancelled", "fuelled", "modelled", "labelled", "whilst", "amongst", "towards",
    "grey", "manoeuvre", "aluminium", "sceptical", "catalogue", "dialogue", "tonne", "tonnes",
    "per cent", "digitalisation", "digitalised", "capitalise", "capitalised", "specialise", "specialised",
    "optimise", "optimised", "minimise", "maximise", "realise", "realised", "utilise", "summarise",
}
PROPER_OK = {"labour party", "ministry of defence", "defence ministry", "centre for", "programme for",
             "financial conduct authority", "ofcom", "bank of england", "centre of"}
INCEPTION_TERMS = ["inception42", "inception 42", "jais", "ashish koshy", "al jallaf", "aljallaf", "inceptionclaw"]
INCEPTION_OK = {"Inception42 coverage", "Abu Dhabi & Gulf", "Strategic Counter Narrative"}
UA = {"User-Agent": "Mozilla/5.0 (compatible; Inception42MorningBrief/1.0)"}


def sentences(text):
    plain = LINK_RE.sub(lambda m: m.group(1), text)
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“(])", plain.strip()) if s.strip()]


def words(text):
    plain = LINK_RE.sub("", text)
    return len(re.findall(r"[A-Za-z0-9$£€%][\w'’$£€%.,-]*", plain))


def probe(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=UA, method=method)
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (405, 403, 400):
                continue
            return e.code
        except Exception:
            if method == "HEAD":
                continue
            return None
    return None


def load_register(path, own_date=None):
    """URLs from every edition in the register except the brief's own."""
    urls = set()
    if not os.path.exists(path):
        return urls
    for block in open(path, encoding="utf-8").read().split("\n## ")[1:]:
        head, _, body = block.partition("\n")
        if own_date and head.strip().startswith(own_date):
            continue
        for m in re.finditer(r"https?://[^\s)|>]+", body):
            urls.add(m.group(0).rstrip(".,"))
    return urls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("--registers", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "registers"))
    ap.add_argument("--no-network", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()

    hard, warn = [], []
    parsed, problems = parse(a.brief)
    for p in problems:
        hard.append(("structure", p))
    if parsed is None:
        report(hard, warn, a.json)
        sys.exit(1)
    s = parsed["sections"]
    fm = parsed["front_matter"]
    if fm.get("source") == "generated":
        for req_sec in ("Top Line", "Strategic Counter Narrative"):
            if req_sec not in s:
                hard.append(("structure", f"missing section '{req_sec}'"))

    body_text = "\n".join("\n".join(v) for v in s.values())
    # em dashes
    for sec, lines in s.items():
        for l in lines:
            if "—" in l:
                hard.append(("em-dash", f"{sec}: {l[:80]}"))
            if re.search(r"\s–\s", l):
                hard.append(("em-dash", f"{sec} (en dash used as dash): {l[:80]}"))
    # links
    all_links = []
    for sec, lines in s.items():
        for l in lines:
            for m in LINK_RE.finditer(l):
                all_links.append((sec, m.group(1), m.group(2)))
    seen = {}
    for sec, name, url in all_links:
        if "signal-ai.com" in url:
            hard.append(("signal-link", f"{sec}: {url[:90]}"))
        key = url.rstrip("/").split("?")[0] if "?srnd=" in url or "?utm" in url else url.rstrip("/")
        # Watch Outs legitimately re-cite the source of a story covered above
        if key in seen and seen[key] != sec and "Watch Outs" not in (sec, seen[key]):
            hard.append(("dup-link", f"{url[:90]} cited in both {seen[key]} and {sec}"))
        elif key in seen and seen[key] == sec:
            hard.append(("dup-link", f"{url[:90]} cited twice in {sec}"))
        seen.setdefault(key, sec)
    own_date = fm.get("date", "")
    reg = load_register(os.path.join(a.registers, "do_not_reuse_register.md"), own_date)
    for sec, name, url in all_links:
        if url.rstrip("/") in {u.rstrip("/") for u in reg}:
            hard.append(("reuse", f"{sec}: {url[:90]} already used in a prior edition"))
    # banned phrases
    low = body_text.lower()
    for b in BANNED:
        if b in low:
            hard.append(("banned-phrase", f"'{b}'"))
    # watch outs
    wo = [l for l in s.get("Watch Outs", []) if l.startswith("- ")]
    if len(wo) > 2:
        hard.append(("watch-outs", f"{len(wo)} bullets, maximum is 2"))
    for l in wo:
        if not LINK_RE.search(l):
            hard.append(("watch-outs", f"bullet without a source link: {l[:80]}"))
        if re.match(r"- (watch whether|watch for|monitor whether|keep an eye)", l.lower()):
            hard.append(("watch-outs", f"imperative framing: {l[:80]}"))
    # Inception42 placement
    for sec, lines in s.items():
        if sec in INCEPTION_OK:
            continue
        for l in lines:
            ll = l.lower()
            if any(t in ll for t in INCEPTION_TERMS):
                hard.append(("inception42", f"Inception42 reference outside allowed sections, in {sec}: {l[:80]}"))
    # American English
    for sec, lines in s.items():
        for l in lines:
            plain = LINK_RE.sub(lambda m: m.group(1), l)
            # drop quoted spans
            plain_noq = re.sub(r"[\"“][^\"”]*[\"”]", "", plain)
            for w in re.findall(r"[A-Za-z']+(?: cent)?", plain_noq):
                if w.lower() in BRITISH:
                    ctx = plain_noq.lower()
                    if any(ok in ctx for ok in PROPER_OK) and w[0].isupper():
                        continue
                    hard.append(("american", f"{sec}: '{w}' in: {plain[:70]}"))
    # lengths
    for sec, lo_s, hi_s, lo_w, hi_w in (("Top Line", 4, 6, 130, 200), ("Strategic Counter Narrative", 5, 8, 150, 230)):
        if sec in s:
            text = " ".join(l for l in s[sec] if l.strip())
            ns, nw = len(sentences(text)), words(text)
            if not (lo_s <= ns <= hi_s):
                warn.append(("length", f"{sec}: {ns} sentences (target {lo_s}-{hi_s})"))
            if not (lo_w <= nw <= hi_w):
                warn.append(("length", f"{sec}: {nw} words (target {lo_w}-{hi_w})"))
    for sec, lines in s.items():
        if sec in PROSE:
            continue
        for l in lines:
            if l.startswith("- ") and words(l) > 70:
                warn.append(("length", f"{sec}: bullet of {words(l)} words: {l[2:60]}"))
    # tics and temporal markers
    for sec, lines in s.items():
        for l in lines:
            plain = LINK_RE.sub(lambda m: m.group(1), l)
            if re.search(r"\bnot\b[^.]{3,60}\bbut\b", plain, re.I) and re.search(r"\bnot (a|an|the|just|only|about|merely)\b", plain, re.I):
                warn.append(("tics", f"{sec}: possible 'not X but Y': {plain[:80]}"))
            if plain.rstrip().endswith("?"):
                warn.append(("tics", f"{sec}: rhetorical question ending: {plain[-80:]}"))
            if re.search(r"\b(today|this week|yesterday|tonight|this morning)\b", plain, re.I) and sec not in ("Inception42 coverage",):
                warn.append(("temporal", f"{sec}: temporal marker: {plain[:80]}"))
    # liveness
    if not a.no_network and all_links:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            res = list(ex.map(lambda t: (t, probe(t[2])), all_links))
        for (sec, name, url), code in res:
            if code in (404, 410):
                hard.append(("dead-link", f"{sec}: HTTP {code} {url[:90]}"))
            elif code in (401, 402, 403, 429, 503):
                warn.append(("bot-wall", f"{sec}: HTTP {code} on probe (verify by other means) {url[:90]}"))
            elif code is None:
                warn.append(("bot-wall", f"{sec}: no answer to probe {url[:90]}"))
    report(hard, warn, a.json)
    sys.exit(1 if hard else 0)


def report(hard, warn, out):
    print(f"AUDIT: {len(hard)} hard failure(s), {len(warn)} warning(s)")
    for k, msg in hard:
        print(f"  FAIL [{k}] {msg}")
    for k, msg in warn:
        print(f"  warn [{k}] {msg}")
    if out:
        json.dump({"hard": hard, "warnings": warn}, open(out, "w"), indent=1)


if __name__ == "__main__":
    main()
