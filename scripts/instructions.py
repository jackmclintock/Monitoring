#!/usr/bin/env python3
"""Editor instructions from the dashboard's `instructions` collection.

  instructions.py plan --dir work/db [--today YYYY-MM-DD] --out work/instructions.md
  instructions.py outcomes --dir work/db --run <edition id> --summaries work/instruction_outcomes.json \
      [--today YYYY-MM-DD] --out work/instruction_writes.json

`--dir` is the folder ArtifactData wrote the documents to with
`out_dir` (it creates `<dir>/instructions/<id>.json`, one file per doc,
each `{"id", "data", "version", ...}`).

plan: lists the instructions in force today (status active, valid_from
on or before today, valid_until empty or on or after today) as Markdown
for the writer, newest last, each with its id. Writes "(none)" when
there are none.

outcomes: after the run, takes `{"<id>": "<one or two sentences on how the
instruction changed the report, or why it did not apply>"}` and emits
ArtifactData batch writes that append the outcome to each instruction
(run id, summary, timestamp), mark next-run-only instructions as used,
and mark dated instructions whose end date has passed as expired. Every
instruction that was in force must have a summary; the script refuses to
write otherwise, so nothing is silently dropped.
"""
import argparse
import datetime as dt
import glob
import json
import os
import sys


def load(d):
    docs = []
    for path in sorted(glob.glob(os.path.join(d, "instructions", "*.json"))):
        try:
            j = json.load(open(path, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        data = j.get("data", j)
        docs.append({"id": data.get("id") or j.get("id") or os.path.basename(path)[:-5], "version": j.get("version"), "data": data})
    return docs


def in_force(data, today):
    if data.get("status", "active") != "active":
        return False
    vf, vu = (data.get("valid_from") or ""), (data.get("valid_until") or "")
    if vf and today < vf:
        return False
    if vu and today > vu:
        return False
    return True


def plan(a):
    today = a.today or dt.datetime.now(dt.timezone(dt.timedelta(hours=4))).strftime("%Y-%m-%d")
    docs = [x for x in load(a.dir) if in_force(x["data"], today)]
    docs.sort(key=lambda x: str(x["data"].get("created_at", "")))
    lines = [f"# Editor instructions in force on {today}", ""]
    if not docs:
        lines.append("(none)")
    for x in docs:
        d = x["data"]
        scope = f"until {d['valid_until']}" if d.get("valid_until") else "next run only"
        src = " (from a resolved issue)" if d.get("source") == "issue" else ""
        lines.append(f"- [{x['id']}] ({scope}{src}) {d.get('text', '').strip()}")
    open(a.out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"{len(docs)} instruction(s) in force -> {a.out}")


def outcomes(a):
    today = a.today or dt.datetime.now(dt.timezone(dt.timedelta(hours=4))).strftime("%Y-%m-%d")
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    summaries = json.load(open(a.summaries, encoding="utf-8"))
    docs = [x for x in load(a.dir) if in_force(x["data"], today)]
    missing = [x["id"] for x in docs if not str(summaries.get(x["id"], "")).strip()]
    if missing:
        sys.exit("no summary for instruction(s): " + ", ".join(missing))
    writes = []
    for x in docs:
        d = x["data"]
        outs = list(d.get("outcomes") or [])
        outs.append({"run_id": a.run, "summary": str(summaries[x["id"]]).strip(), "at": now})
        status = "active"
        if not d.get("valid_until"):
            status = "used"
        elif d["valid_until"] < today or (d["valid_until"] == today and a.last_of_day):
            status = "expired"
        w = {"op": "update", "collection": "instructions", "doc_id": x["id"],
             "data": {"outcomes": outs, "status": status, "last_used_run": a.run, "last_used_at": now}}
        if x.get("version"):
            w["if_version"] = x["version"]
        writes.append(w)
    # also expire dated instructions whose window has passed without a run using them
    for x in load(a.dir):
        d = x["data"]
        if d.get("status", "active") == "active" and d.get("valid_until") and d["valid_until"] < today and x["id"] not in [w["doc_id"] for w in writes]:
            w = {"op": "update", "collection": "instructions", "doc_id": x["id"], "data": {"status": "expired"}}
            if x.get("version"):
                w["if_version"] = x["version"]
            writes.append(w)
    json.dump({"writes": writes}, open(a.out, "w", encoding="utf-8"), indent=1)
    print(f"{len(writes)} instruction write(s) -> {a.out}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("--dir", required=True); p.add_argument("--today"); p.add_argument("--out", required=True)
    o = sub.add_parser("outcomes"); o.add_argument("--dir", required=True); o.add_argument("--run", required=True); o.add_argument("--summaries", required=True); o.add_argument("--today"); o.add_argument("--out", required=True); o.add_argument("--last-of-day", action="store_true", help="this is the last run of the day: an instruction ending today expires now")
    a = ap.parse_args()
    (plan if a.cmd == "plan" else outcomes)(a)


if __name__ == "__main__":
    main()
