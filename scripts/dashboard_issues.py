#!/usr/bin/env python3
"""Turn the audit result (and anything else the run could not settle) into
dashboard issue documents, one per item, so the dashboard's counts and the
audit's counts are the same list.

  dashboard_issues.py <edition id> --audit work/audit.json [--extra work/extra_issues.json]
                      [--settled bot-wall="Read through Tavily extract; content verified"]
                      --out work/issue_writes.json

Writes a JSON file in the shape the ArtifactData "batch" action takes
(`{"writes": [...]}`, at most 50 per file; a second file `-2.json` is
written when there are more). Each audit warning becomes
`issues/<edition id>-a<n>` with kind "audit", severity "low" (hard
failures that were left unfixed become severity "high"). A `--settled`
code is one the run dealt with itself during the run: those items are
written already resolved, with the given text as the resolution, so the
reviewer sees them counted but not waiting.

`--extra` is a JSON list of `{title, detail, severity}` for items that are
not audit findings (an article left out, a missing Signal email, a failed
upload); they become `issues/<edition id>-<n>` with kind "run".
"""
import argparse
import datetime as dt
import json
import os
import sys

LABELS = {
    "length": "Bullet over length",
    "temporal": "Temporal marker to rephrase",
    "bot-wall": "Source probe bot-walled",
    "reuse": "Link reused from an earlier edition",
    "dead-link": "Dead link",
    "link": "Link problem",
    "style": "House style",
    "banned": "Banned phrase",
    "em-dash": "Em dash",
    "spelling": "US spelling",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edition")
    ap.add_argument("--audit", required=True)
    ap.add_argument("--extra")
    ap.add_argument("--settled", action="append", default=[], help='code="resolution text"')
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    settled = {}
    for s in a.settled:
        code, _, text = s.partition("=")
        settled[code.strip()] = text.strip().strip('"')

    audit = json.load(open(a.audit, encoding="utf-8"))
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    docs = []
    n = 0
    for sev, items in (("high", audit.get("hard", [])), ("low", audit.get("warnings", []))):
        for code, msg in items:
            n += 1
            doc_id = f"{a.edition}-a{n}"
            section, _, rest = msg.partition(": ")
            d = {
                "id": doc_id, "run_id": a.edition, "kind": "audit", "code": code,
                "severity": sev, "status": "open", "source": "routine", "created_at": now,
                "title": f"{LABELS.get(code, code)} in {section}" if rest else f"{LABELS.get(code, code)}: {msg[:90]}",
                "detail": rest or msg,
            }
            if code in settled and sev != "high":
                d.update({"status": "resolved", "resolved_at": now, "resolved_by": "routine",
                          "resolution": settled[code]})
            docs.append(d)
    if a.extra:
        for i, e in enumerate(json.load(open(a.extra, encoding="utf-8")), 1):
            d = {"id": f"{a.edition}-{i}", "run_id": a.edition, "kind": "run",
                 "severity": e.get("severity", "medium"), "status": "open", "source": "routine",
                 "created_at": now, "title": e["title"], "detail": e.get("detail", "")}
            docs.append(d)

    writes = [{"op": "set", "collection": "issues", "doc_id": d["id"], "data": d} for d in docs]
    base, ext = os.path.splitext(a.out)
    for k in range(0, max(len(writes), 1), 50):
        path = a.out if k == 0 else f"{base}-{k // 50 + 1}{ext}"
        json.dump({"writes": writes[k:k + 50]}, open(path, "w", encoding="utf-8"), indent=1)
        print("wrote", path, len(writes[k:k + 50]), "writes")
    open_n = sum(1 for d in docs if d["status"] == "open")
    print(f"{len(docs)} issues ({open_n} open, {len(docs) - open_n} settled by the run)")
    print(json.dumps({"audit_items": len(docs), "open": open_n}))


if __name__ == "__main__":
    main()
