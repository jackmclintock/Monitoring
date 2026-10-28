#!/usr/bin/env python3
"""Free outlet sweep through Google News RSS: no web-search budget, 100
results per query, real timestamps. Replaces most of the WebSearch calls in
Stage 2b and 2c; WebSearch is then only for gap-filling.

  feed_sweep.py sweep --start 2026-10-28T02:45:00Z --end 2026-10-29T02:45:00Z \
      --out work/sweep.json [--queries config/sweep_queries.json] [--md work/sweep.md]
  feed_sweep.py decode --sweep work/sweep.json --ids r12,r40,t3 [--all] [--limit 150]

sweep: runs every query in the config (outlets, topics, mentions) as one
RSS request each, keeps items published inside the window, dedupes by
title, and writes JSON plus a Markdown digest grouped by query with a
short id per item. Links are Google News redirect links at this stage.

decode: resolves the Google News links of the chosen items to the real
article URLs (two paced requests each; keep it to the items that are
actually candidates, or --all with --limit for a whole sweep). Writes the
URL back into the sweep file and prints id, outlet, URL.

Run with python3 -I. Network: plain HTTPS to news.google.com only.
"""
import argparse
import datetime as dt
import email.utils
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}
RSS = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
# outlet-group items must mention one of these in the title (topic and
# mention queries are already specific and keep everything)
KEYWORDS = re.compile(r"\b(ai|a\.i\.|artificial intelligence|chips?|semiconductor|nvidia|openai|anthropic|chatgpt|gemini|copilot|claude|grok|deepseek|llm|model|models|agent|agents|agentic|robot|robots|robotics|data cent(?:er|re)s?|gigawatt|gpu|gpus|compute|supercomputer|g42|mubadala|mgx|humain|stargate|jais|microsoft|google|meta|alphabet|amazon|apple|intel|amd|tsmc|broadcom|oracle|xai|mistral|cohere|superintelligence|machine learning|neural|automation|autonomous)\b", re.I)


def get(url, data=None, headers=None, timeout=25):
    req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "ignore")


def parse_iso(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return dt.datetime.fromisoformat(s).astimezone(dt.timezone.utc)


def norm_title(t):
    t = re.sub(r"\s+-\s+[^-]+$", "", t)  # strip " - Outlet" suffix
    return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()


def run_query(q, days):
    url = RSS.format(q=urllib.parse.quote(f"{q} when:{days}d"))
    try:
        xml = get(url)
    except Exception as e:  # noqa: BLE001
        return None, str(e)
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        return None, f"parse: {e}"
    items = []
    for it in root.findall(".//item"):
        title = (it.findtext("title") or "").strip()
        pub = it.findtext("pubDate") or ""
        try:
            when = email.utils.parsedate_to_datetime(pub).astimezone(dt.timezone.utc)
        except Exception:  # noqa: BLE001
            continue
        items.append({
            "title": title,
            "source": (it.findtext("source") or "").strip(),
            "published": when.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "gnews": (it.findtext("link") or "").strip(),
        })
    return items, None


def sweep(a):
    start, end = parse_iso(a.start), parse_iso(a.end)
    days = max(1, int((dt.datetime.now(dt.timezone.utc) - start).total_seconds() // 86400) + 1)
    cfg = json.load(open(a.queries, encoding="utf-8"))
    out = {"window": {"start": a.start, "end": a.end}, "groups": [], "errors": []}
    seen = {}
    prefix = {"outlets": "o", "topics": "t", "mentions": "m"}
    counter = {"o": 0, "t": 0, "m": 0}
    for group in ("outlets", "topics", "mentions"):
        for name, q in cfg.get(group, {}).items():
            items, err = run_query(q, days)
            time.sleep(a.pace)
            if err:
                out["errors"].append({"group": group, "name": name, "error": err})
                continue
            kept = []
            for it in items:
                when = parse_iso(it["published"])
                if not (start <= when < end):
                    continue
                if group == "outlets" and not a.no_filter and not KEYWORDS.search(it["title"]):
                    continue
                key = norm_title(it["title"])
                if key in seen:
                    if name not in seen[key]["also"]:
                        seen[key]["also"].append(name)
                    continue
                counter[prefix[group]] += 1
                it["id"] = f"{prefix[group]}{counter[prefix[group]]}"
                it["also"] = []
                seen[key] = it
                kept.append(it)
            out["groups"].append({"group": group, "name": name, "query": q, "total": len(items), "in_window": len(kept), "items": kept})
            print(f"{group:8} {name:32} {len(items):3} results, {len(kept):3} in window", file=sys.stderr)
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    n = sum(g["in_window"] for g in out["groups"])
    if a.md:
        lines = [f"# Feed sweep {a.start} to {a.end}", "", f"{n} unique items in window across {len(out['groups'])} queries. Ids: o = outlet, t = topic, m = mention. Links are Google News redirects until decoded.", ""]
        for g in out["groups"]:
            if not g["items"]:
                continue
            lines.append(f"## {g['name']} ({g['group']}, {g['in_window']} in window)")
            for it in g["items"]:
                also = f" (also: {', '.join(it['also'])})" if it["also"] else ""
                lines.append(f"- {it['id']} | {it['published'][5:16].replace('T',' ')} | {it['source']} | {it['title']}{also}")
            lines.append("")
        if out["errors"]:
            lines.append("## Query errors")
            lines += [f"- {e['group']}/{e['name']}: {e['error']}" for e in out["errors"]]
        open(a.md, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"{n} unique in-window items, {len(out['errors'])} query errors -> {a.out}")


def decode_one(link):
    aid = re.search(r"/articles/([^?]+)", link).group(1)
    html = get(f"https://news.google.com/rss/articles/{aid}")
    sg = re.search(r'data-n-a-sg="([^"]+)"', html)
    ts = re.search(r'data-n-a-ts="([^"]+)"', html)
    if not (sg and ts):
        return None
    inner = json.dumps(["garturlreq", [["X", "X", ["X", "X"], None, None, 1, 1, "US:en", None, 1, None, None, None, None, None, 0, 1], "X", "X", 1, [1, 1, 1], 1, 1, None, 0, 0, None, 0], aid, int(ts.group(1)), sg.group(1)])
    data = urllib.parse.urlencode({"f.req": json.dumps([[["Fbv4je", inner, None, "generic"]]])}).encode()
    body = get("https://news.google.com/_/DotsSplashUi/data/batchexecute", data=data, headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"})
    m = re.search(r'garturlres\\",\\"(https?://[^\\"]+)', body) or re.search(r'"garturlres","(https?://[^"]+)"', body)
    return m.group(1) if m else None


def decode(a):
    data = json.load(open(a.sweep, encoding="utf-8"))
    want = set(x.strip() for x in (a.ids or "").split(",") if x.strip())
    done = 0
    for g in data["groups"]:
        for it in g["items"]:
            if it.get("url"):
                continue
            if not (a.all or it["id"] in want):
                continue
            if done >= a.limit:
                break
            for attempt in range(3):
                try:
                    url = decode_one(it["gnews"])
                    break
                except Exception as e:  # noqa: BLE001
                    url = None
                    if "429" in str(e):
                        time.sleep(10 * (attempt + 1))
                    else:
                        break
            it["url"] = url or ""
            done += 1
            print(f"{it['id']}\t{it['source']}\t{url or 'UNRESOLVED'}")
            time.sleep(a.pace)
    json.dump(data, open(a.sweep, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"decoded {done} links", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sweep")
    s.add_argument("--start", required=True)
    s.add_argument("--end", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--md")
    s.add_argument("--queries", default="config/sweep_queries.json")
    s.add_argument("--pace", type=float, default=1.0)
    s.add_argument("--no-filter", action="store_true", help="keep outlet items that do not mention an AI keyword")
    d = sub.add_parser("decode")
    d.add_argument("--sweep", required=True)
    d.add_argument("--ids")
    d.add_argument("--all", action="store_true")
    d.add_argument("--limit", type=int, default=150)
    d.add_argument("--pace", type=float, default=2.0)
    a = ap.parse_args()
    (sweep if a.cmd == "sweep" else decode)(a)


if __name__ == "__main__":
    main()
