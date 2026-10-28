#!/usr/bin/env python3
"""Upload a file of any size to a SharePoint folder via Microsoft Graph.

  graph_upload.py <file> [--drive-id ID] [--folder-id ID] [--name NAME]

Needed because the Microsoft 365 connector's upload tool caps files at 1 MB,
and the daily MP3 is 6 to 9 MB. Uses an Entra app registration with
client-credentials (application permission Sites.Selected granted on the
Clients site, or Files.ReadWrite.All): set MS365_TENANT_ID, MS365_CLIENT_ID,
MS365_CLIENT_SECRET. Drive and folder default to SP_DRIVE_ID / SP_FOLDER_ID
environment variables, else the values in config/brief_config.json.

Files up to 4 MB go in one PUT; larger files use an upload session in 5 MB
chunks. Standard library only.

Exit codes: 0 uploaded, 78 not configured, 1 failure.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

GRAPH = "https://graph.microsoft.com/v1.0"
CHUNK = 5 * 1024 * 1024


def token(tenant, cid, secret):
    data = urllib.parse.urlencode({
        "grant_type": "client_credentials", "client_id": cid,
        "client_secret": secret, "scope": "https://graph.microsoft.com/.default"}).encode()
    with urllib.request.urlopen(urllib.request.Request(
            f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token", data=data)) as r:
        return json.load(r)["access_token"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--drive-id")
    ap.add_argument("--folder-id")
    ap.add_argument("--name")
    a = ap.parse_args()
    env = {k: os.environ.get(k, "") for k in ("MS365_TENANT_ID", "MS365_CLIENT_ID", "MS365_CLIENT_SECRET")}
    if not all(env.values()):
        print("Graph credentials (MS365_TENANT_ID, MS365_CLIENT_ID, MS365_CLIENT_SECRET) not set; "
              "large-file upload skipped", file=sys.stderr)
        sys.exit(78)
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "brief_config.json")
    cfg = json.load(open(cfg_path)).get("sharepoint", {}) if os.path.exists(cfg_path) else {}
    drive = a.drive_id or os.environ.get("SP_DRIVE_ID") or cfg.get("drive_id")
    folder = a.folder_id or os.environ.get("SP_FOLDER_ID") or cfg.get("output_folder_item_id")
    if not drive or not folder:
        sys.exit("drive id and folder id are required (flags, SP_DRIVE_ID/SP_FOLDER_ID, or config)")
    name = a.name or os.path.basename(a.file)
    data = open(a.file, "rb").read()
    tok = token(env["MS365_TENANT_ID"], env["MS365_CLIENT_ID"], env["MS365_CLIENT_SECRET"])
    base = f"{GRAPH}/drives/{drive}/items/{folder}:/{urllib.parse.quote(name)}:"
    hdr = {"Authorization": f"Bearer {tok}"}
    try:
        if len(data) <= 4 * 1024 * 1024:
            r = urllib.request.Request(base + "/content", data=data, method="PUT",
                                       headers={**hdr, "Content-Type": "application/octet-stream"})
            with urllib.request.urlopen(r, timeout=120) as resp:
                item = json.load(resp)
        else:
            r = urllib.request.Request(base + "/createUploadSession", data=json.dumps(
                {"item": {"@microsoft.graph.conflictBehavior": "replace", "name": name}}).encode(),
                method="POST", headers={**hdr, "Content-Type": "application/json"})
            with urllib.request.urlopen(r, timeout=60) as resp:
                url = json.load(resp)["uploadUrl"]
            item = None
            for start in range(0, len(data), CHUNK):
                chunk = data[start:start + CHUNK]
                end = start + len(chunk) - 1
                r = urllib.request.Request(url, data=chunk, method="PUT", headers={
                    "Content-Length": str(len(chunk)),
                    "Content-Range": f"bytes {start}-{end}/{len(data)}"})
                with urllib.request.urlopen(r, timeout=300) as resp:
                    body = resp.read()
                    if resp.status in (200, 201):
                        item = json.loads(body)
        print(f"uploaded {name} ({len(data)} bytes): {item.get('webUrl') if item else 'ok'}")
    except urllib.error.HTTPError as e:
        print(f"Graph error {e.code}: {e.read()[:400].decode(errors='replace')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
