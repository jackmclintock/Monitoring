#!/usr/bin/env python3
"""Turn an overnight Signal AI alert email into a clean candidate list.

Input: the JSON returned by the Microsoft 365 connector's read_resource for
the Signal email (mail:///messages/...), or the raw HTML body saved to a
file. Output: JSON (and a readable markdown table) of candidate articles
with Signal's tracking redirects resolved to the real article URLs.

  parse_signal_email.py signal_corp.json --out work/candidates_corp.json [--no-resolve]

What it does:
  * walks Signal's table of contents sections (e.g. "Inception mentions",
    "G42 companies", "OpenAI", "Gulf/UAE region", or the AI & Themes topics)
  * keeps outlet, medium, date, headline, snippet, "+ N similar" count
  * drops "Article unavailable" licence stubs
  * resolves click.email.signal-ai.com redirects (HEAD/GET follow) in
    parallel and records the final URL; unresolved links are kept with
    resolved=null so the run can fall back to a headline search
  * flags items whose date is outside the window passed with --window-start
    / --window-end (ISO, UTC) so stale resurfaced pieces are visible

The output is a shortlist for the run to verify, never a source of truth:
every candidate still has to be fetched and checked before it is used.
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import html
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser

MONTHS = {m.lower(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], 1)}
UA = {"User-Agent": "Mozilla/5.0 (compatible; Inception42MorningBrief/1.0)"}


class Items(HTMLParser):
    """Class-aware walk of Signal's MJML email: item-meta, item-title-link,
    item-summary blocks, section anchors (<a name=uuid>Section</a>) and the
    toc-item-title cells."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items, self.toc = [], []
        self.section = None
        self.stack = []          # class names of open elements
        self.buf = {}            # class -> text being collected
        self.cur = None
        self.anchor_pending = False
        self.skip = 0

    def _cls(self, attrs):
        return (dict(attrs).get("class") or "").split()

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script", "head"):
            self.skip += 1
            return
        cls = self._cls(attrs)
        self.stack.append(cls)
        if "item-meta" in cls:
            self.cur = {"meta": "", "title": "", "href": None, "summary": ""}
            self.buf["meta"] = ""
        elif "item-title-link" in cls and self.cur is not None:
            self.cur["href"] = html.unescape(dict(attrs).get("href", "") or "")
            self.buf["title"] = ""
        elif "item-summary" in cls and self.cur is not None:
            self.buf["summary"] = ""
        elif "toc-item-title" in cls:
            self.buf["toc"] = ""
        elif tag == "a" and dict(attrs).get("name") and not dict(attrs).get("href"):
            self.anchor_pending = True
            self.buf["section"] = ""

    def handle_endtag(self, tag):
        if tag in ("style", "script", "head"):
            if self.skip:
                self.skip -= 1
            return
        cls = self.stack.pop() if self.stack else []
        if "item-meta" in cls and self.cur is not None:
            self.cur["meta"] = self.buf.pop("meta", "").strip()
        elif "item-title-link" in cls and self.cur is not None:
            self.cur["title"] = self.buf.pop("title", "").strip()
        elif "item-summary" in cls and self.cur is not None:
            self.cur["summary"] = self.buf.pop("summary", "").strip()
            self.cur["section"] = self.section
            self.items.append(self.cur)
            self.cur = None
        elif "toc-item-title" in cls:
            t = self.buf.pop("toc", "").strip()
            if t:
                self.toc.append(t)
        elif self.anchor_pending and tag in ("div", "td", "p", "h1", "h2", "h3"):
            t = self.buf.pop("section", "").strip()
            if t:
                self.section = t
            self.anchor_pending = False

    def handle_data(self, data):
        if self.skip:
            return
        t = re.sub(r"\s+", " ", data)
        for k in ("meta", "title", "summary", "toc", "section"):
            if k in self.buf:
                if k == "section" and not self.anchor_pending:
                    continue
                self.buf[k] += t


META_RE = re.compile(
    r"^(?P<outlet>.+?)\s*[•·]\s*(?P<medium>[A-Za-z ]+?)\s*[•·]\s*(?P<date>\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+(?:\s+\d{4})?)\s*$")
SIMILAR_RE = re.compile(r"\s*\(\+\s*(\d+)\s+similar\s+articles?\)\s*$", re.I)


def parse_date(s, ref_year):
    m = re.match(r"(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)(?:\s+(\d{4}))?", s.strip())
    if not m or m.group(2).lower() not in MONTHS:
        return None
    year = int(m.group(3)) if m.group(3) else ref_year
    try:
        return dt.date(year, MONTHS[m.group(2).lower()], int(m.group(1)))
    except ValueError:
        return None


def slug_match(headline, url):
    """Rough check that the resolved URL belongs to the headline: at least
    two significant headline words appear in the URL path."""
    if not url:
        return None
    words = [w for w in re.findall(r"[a-z0-9]{4,}", headline.lower())
             if w not in ("with", "from", "that", "this", "says", "after", "over", "into", "amid")]
    path = url.lower()
    hits = sum(1 for w in set(words) if w in path)
    return hits >= 2 if len(words) >= 2 else None


def extract(markup, ref_year):
    p = Items()
    p.feed(markup)
    p.close()
    items = []
    for it in p.items:
        m = META_RE.match(it["meta"])
        outlet, medium, date_s = (m.group("outlet").strip(), m.group("medium").strip(), m.group("date")) if m else (it["meta"], "", "")
        headline = it["title"]
        similar = 0
        sm = SIMILAR_RE.search(headline)
        if sm:
            similar = int(sm.group(1))
            headline = SIMILAR_RE.sub("", headline).strip()
        unavailable = headline.lower().startswith("article unavailable") or \
            "only visible to people with the relevant content licenses" in it["summary"]
        if unavailable or not headline:
            continue
        d = parse_date(date_s, ref_year) if date_s else None
        items.append({
            "section": it["section"],
            "outlet": outlet,
            "medium": medium,
            "date": d.isoformat() if d else None,
            "headline": headline,
            "snippet": it["summary"],
            "similar": similar,
            "signal_url": it["href"],
            "resolved_url": None,
        })
    return items, p.toc


def resolve(url, timeout=20):
    if not url:
        return None, "no link"
    try:
        req = urllib.request.Request(url, headers=UA, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            final = r.geturl()
    except Exception:
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                final = r.geturl()
        except urllib.error.HTTPError as e:
            # the destination answered (bot wall, paywall): the redirect
            # still told us where it points
            final = e.geturl() if hasattr(e, "geturl") else None
            if final and "signal-ai.com" not in final:
                return final, f"destination http {e.code}"
            return None, f"http {e.code}"
        except Exception as e:
            return None, type(e).__name__
    if final and "signal-ai.com" in final:
        return None, "redirect not followed"
    return final, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", required=True, help="JSON output path")
    ap.add_argument("--md", help="optional markdown table output path")
    ap.add_argument("--no-resolve", action="store_true")
    ap.add_argument("--window-start", help="ISO UTC; items dated before this are flagged stale")
    ap.add_argument("--window-end", help="ISO UTC")
    a = ap.parse_args()

    raw = open(a.input, encoding="utf-8", errors="replace").read()
    subject, received = "", ""
    if raw.lstrip().startswith("{"):
        j = json.loads(raw)
        markup = j.get("body", {}).get("content", "")
        subject = j.get("subject", "")
        received = j.get("receivedDateTime") or j.get("sentDateTime") or ""
    else:
        markup = raw
    ref_year = int(received[:4]) if received[:4].isdigit() else dt.date.today().year
    items, toc = extract(markup, ref_year)

    if not a.no_resolve:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            futs = {ex.submit(resolve, it["signal_url"]): it for it in items}
            for f in cf.as_completed(futs):
                it = futs[f]
                it["resolved_url"], it["resolve_status"] = f.result()

    ws = a.window_start[:10] if a.window_start else None
    for it in items:
        d = it["date"]
        it["stale"] = bool(ws and d and d < ws)
        it["url_matches_headline"] = slug_match(it["headline"], it["resolved_url"])

    out = {"subject": subject, "received": received, "sections": toc, "count": len(items), "items": items}
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if a.md:
        lines = [f"# {subject}", "", f"{len(items)} usable items (licence stubs dropped)", ""]
        for it in items:
            flag = (" (STALE)" if it["stale"] else "") + (" (URL/HEADLINE MISMATCH, verify)" if it["url_matches_headline"] is False else "")
            url = it["resolved_url"] or f"unresolved: {it.get('resolve_status')}"
            lines.append(f"- [{it['section']}] {it['date']}{flag} | {it['outlet']} | {it['headline']}"
                         + (f" (+{it['similar']} similar)" if it["similar"] else "") + f"\n  {url}")
        open(a.md, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"{len(items)} candidates from {len(toc)} sections -> {a.out}")
    unresolved = [it for it in items if not it["resolved_url"]]
    if unresolved and not a.no_resolve:
        print(f"{len(unresolved)} links did not resolve; search those headlines instead", file=sys.stderr)


if __name__ == "__main__":
    main()
