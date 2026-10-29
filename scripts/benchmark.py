#!/usr/bin/env python3
"""Score a generated edition against the edition the team actually sent.

  benchmark.py briefs/2026-10-29/brief_generated.md briefs/2026-10-29/brief_sent.md \
      --date 2026-10-29 --out briefs/2026-10-29/benchmark.json --md briefs/2026-10-29/benchmark.md

Matches stories between the two briefs (same link, or the same story told
with different links: shared entities, numbers and distinctive words) and
reports:
  coverage      sent stories the generated edition also carried (count, share)
  missed        sent stories the generated edition did not carry, by section
  extra         generated stories the sent edition did not carry
  shared_links  links cited by both
  tier          share of links on Tier 1 or Tier 2 outlets, both editions
  length        body words, both editions
  sections      bullets per section, both editions
  verdict       "at or better" when coverage >= 0.8 and tier_gap <= 0.15 and
                length within 1,250 to 1,750; otherwise "behind", with reasons

The verdict is mechanical; the benchmark run adds the editorial judgment.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brief_format_check import parse  # noqa: E402

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
TIER12 = ("reuters.com", "bloomberg.com", "ft.com", "wsj.com", "washingtonpost.com", "nytimes.com",
          "techcrunch.com", "venturebeat.com", "wired.com", "technologyreview.com", "semafor.com",
          "theverge.com", "axios.com", "cnbc.com", "politico.com", "bbc.com", "bbc.co.uk")
STOP = set("the a an and or of to in on for with by from as at is are was were be been has have had its it this that these those will would can could after before over under more than about into out up down new said says say per also while amid across between".split())


def stories(parsed):
    out = []
    for sec, body in parsed["sections"].items():
        if sec in ("Top Line", "Strategic Counter Narrative"):
            continue
        for l in body:
            if not l.startswith("- "):
                continue
            links = [m.group(2) for m in LINK_RE.finditer(l)]
            text = LINK_RE.sub(lambda m: m.group(1), l[2:]).strip()
            out.append({"section": sec, "text": text, "links": links, "tokens": tokens(text)})
    return out


def tokens(text):
    t = set()
    for w in re.findall(r"[A-Za-z][A-Za-z0-9&'.-]+|\$?\d[\d,.]*%?", text):
        wl = w.lower().strip(".,'")
        if len(wl) < 3 or wl in STOP:
            continue
        if w[0].isupper() or any(c.isdigit() for c in w) or len(wl) > 7:
            t.add(wl)
    return t


def norm_url(u):
    u = re.sub(r"[?#].*$", "", u.strip().lower())
    u = re.sub(r"^https?://(www\.)?", "", u)
    return u.rstrip("/")


def similar(a, b):
    if set(map(norm_url, a["links"])) & set(map(norm_url, b["links"])):
        return 1.0
    ta, tb = a["tokens"], b["tokens"]
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    return inter / min(len(ta), len(tb))


def body_words(parsed):
    return sum(len(LINK_RE.sub(lambda m: m.group(1), l).split()) for body in parsed["sections"].values() for l in body)


def tier_share(parsed):
    links = [m.group(2) for body in parsed["sections"].values() for l in body for m in LINK_RE.finditer(l)]
    if not links:
        return 0.0, 0
    t = sum(1 for u in links if any(d in u for d in TIER12))
    return round(t / len(links), 2), len(links)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("generated")
    ap.add_argument("sent")
    ap.add_argument("--date", required=True)
    ap.add_argument("--threshold", type=float, default=0.34)
    ap.add_argument("--out", required=True)
    ap.add_argument("--md")
    a = ap.parse_args()
    g, _ = parse(a.generated)
    s, _ = parse(a.sent)
    if g is None or s is None:
        sys.exit("one of the briefs does not parse")
    gs, ss = stories(g), stories(s)
    matched_g = set()
    covered, missed = [], []
    for i, st in enumerate(ss):
        best, bj = 0.0, None
        for j, gt in enumerate(gs):
            if j in matched_g:
                continue
            sc = similar(st, gt)
            if sc > best:
                best, bj = sc, j
        if bj is not None and best >= a.threshold:
            matched_g.add(bj)
            covered.append({"section": st["section"], "story": st["text"][:160], "generated_section": gs[bj]["section"], "score": round(best, 2)})
        else:
            missed.append({"section": st["section"], "story": st["text"][:200], "links": st["links"]})
    extra = [{"section": gt["section"], "story": gt["text"][:200], "links": gt["links"]} for j, gt in enumerate(gs) if j not in matched_g]
    g_links = set(norm_url(u) for st in gs for u in st["links"])
    s_links = set(norm_url(u) for st in ss for u in st["links"])
    shared = sorted(g_links & s_links)
    g_tier, g_n = tier_share(g)
    s_tier, s_n = tier_share(s)
    g_words, s_words = body_words(g), body_words(s)
    coverage = round(len(covered) / len(ss), 2) if ss else 1.0
    reasons = []
    if coverage < 0.8:
        reasons.append(f"covered {len(covered)} of {len(ss)} sent stories ({int(coverage*100)}%, target 80%)")
    if s_tier - g_tier > 0.15:
        reasons.append(f"Tier 1 and 2 links {int(g_tier*100)}% against {int(s_tier*100)}% in the sent edition")
    if not 1250 <= g_words <= 1750:
        reasons.append(f"{g_words} words of body text (target about 1,500)")
    sec_counts = lambda p: {k: sum(1 for l in v if l.startswith("- ")) for k, v in p["sections"].items() if k not in ("Top Line", "Strategic Counter Narrative")}
    res = {
        "date": a.date, "verdict": "at or better" if not reasons else "behind", "reasons": reasons,
        "coverage": coverage, "covered": covered, "missed": missed, "extra": extra,
        "shared_links": shared, "links": {"generated": g_n, "sent": s_n, "shared": len(shared)},
        "tier": {"generated": g_tier, "sent": s_tier},
        "length": {"generated": g_words, "sent": s_words},
        "sections": {"generated": sec_counts(g), "sent": sec_counts(s)},
    }
    json.dump(res, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if a.md:
        L = [f"# Benchmark {a.date}: generated against sent", "",
             f"**Verdict: {res['verdict']}.** " + ("; ".join(reasons) if reasons else "Coverage, sourcing and length all at target."), "",
             f"- Coverage: {len(covered)} of {len(ss)} sent stories carried ({int(coverage*100)}%)",
             f"- Extra stories in the generated edition: {len(extra)}",
             f"- Links: generated {g_n} (Tier 1-2 {int(g_tier*100)}%), sent {s_n} (Tier 1-2 {int(s_tier*100)}%), {len(shared)} shared",
             f"- Length: generated {g_words} words, sent {s_words}", ""]
        if missed:
            L += ["## Missed (in the sent edition, not in the generated one)", ""] + [f"- {m['section']} | {m['story']} | " + " / ".join(m["links"]) for m in missed] + [""]
        if extra:
            L += ["## Extra (in the generated edition, not in the sent one)", ""] + [f"- {e['section']} | {e['story']}" for e in extra] + [""]
        L += ["## Covered", ""] + [f"- {c['section']} | {c['story']}" + (f" (placed in {c['generated_section']})" if c['generated_section'] != c['section'] else "") for c in covered]
        open(a.md, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(json.dumps({k: res[k] for k in ("verdict", "coverage", "links", "tier", "length")}))
    if reasons:
        print("behind: " + "; ".join(reasons))


if __name__ == "__main__":
    main()
