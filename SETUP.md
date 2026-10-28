# Setup: the Inception42 Morning Brief routine

One-time setup, then day-to-day operation. Everything runs under Jack's
claude.ai account for now (decision of 28 October 2026); move it to a
service account later if commits and uploads should not carry an
individual's identity.

## 1. Repository

- GitHub: `jackmclintock/Monitoring`, default branch `main`. Runs clone
  `main`, so merge the working branch into `main` before scheduling.
- Enable **Allow unrestricted branch pushes** for this repository in the
  routine settings so the run can push its edition to `main` directly.
  Without it the run opens and merges its own pull request, which also works.

## 2. Environment (claude.ai/code, cloud icon, Add environment)

Name it `morning-brief`.

- **Network access: Full.** The run fetches arbitrary news domains.
- **Environment variables:**

| Variable | Purpose | Where to get it |
|---|---|---|
| `TAVILY_API_KEY` | Reads bot-walled article bodies (one batched call per run, a few credits a day; the free tier is enough) | app.tavily.com |
| `ELEVENLABS_API_KEY` | Produces the MP3 through the API, voice Allistair | ElevenLabs account settings, API keys (use the Hawthorn account that owns the voice; never put the login in a document) |
| `MS365_TENANT_ID`, `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET` | Optional. Lets `scripts/graph_upload.py` put the MP3 (6 to 9 MB) in the SharePoint folder; the connector caps uploads at 1 MB | An Entra app registration with application permission `Sites.Selected` (granted on the Clients site) or `Files.ReadWrite.All`; needs a tenant admin |

- No setup script. All scripts use the Python standard library.

Until the Graph credentials exist, each run attaches the MP3 to the session
output and says so in the package README; the reviewer downloads it from
the run session (or regenerates it in ElevenLabs Studio from `script.txt`).

## 3. Connectors

The routine needs the **Microsoft 365** connector (mail and SharePoint,
already connected on Jack's account) and **GitHub**. Remove every other
connector from the routine: the run can use any tool of any connector it
holds without asking.

The run only reads mail (the Signal AI alerts and the last sent brief) and
creates folders and files under `Morning Brief Drafts`. It never sends
mail, never deletes, moves or renames anything.

## 4. SharePoint output folder

`config/brief_config.json` points at the Monitoring folder Ines shared
(`Inception / Account Management / Monitoring / Jack`) as the parent. The
first run creates `Morning Brief Drafts` under it and records the new
folder id back into the config. To use a different parent, put that
folder's item id in `sharepoint.monitoring_folder_item_id` (visible in
the `file:///<drive>/<item id>` URI the connector returns for the folder).

## 5. The routine (claude.ai/code/routines, New routine)

- **Name:** Inception42 Morning Brief
- **Schedule:** daily, Monday to Friday, 06:45 Gulf Standard Time (enter
  the equivalent in your device's timezone). The package is ready by about
  07:30, leaving the reviewer an hour before the 09:00 send.
- **Repository:** `jackmclintock/Monitoring`, environment `morning-brief`,
  connectors Microsoft 365 and GitHub.
- **Prompt (paste as is):**

```
Generate the Inception42 Morning Brief for today (Gulf Standard Time,
UTC+4). Follow .claude/skills/morning-brief/SKILL.md exactly, every stage
in order: capability check; compute the monitoring window from the
previous edition; learn from the last sent email if there is one; read the
overnight Signal AI alerts through the Microsoft 365 connector and parse
them with scripts/parse_signal_email.py; sweep the outlet list with the
built-in web search; search for Inception42 and executive mentions; verify
every candidate by fetching it (snippet plus a second readable source when
a site bot-walls, then one batched Tavily extract for the selected
articles WebFetch could not read; never use Tavily for search); write the
brief to the house rules; run the single adversarial review pass; run
scripts/audit_brief.py and fix every hard failure; build the package with
scripts/build_outputs.py; write script.txt and produce the audio with
scripts/elevenlabs_tts.py; write sensitive_articles.md, candidates.md and
run_log.md; create the dated subfolder under Morning Brief Drafts in
SharePoint and upload every file (the MP3 through scripts/graph_upload.py
when configured, otherwise attach it to the session and say so); append
the register, commit everything except the MP3 and land it on main.

Hard rules: nothing is written from memory; every fact and link comes from
an article read in this run; an unreadable article is listed in the run
log, not written up. Stay inside the monitoring window. US English, no em
dashes, no banned phrases. Inception42 only in the coverage bullets, Abu
Dhabi & Gulf and the Strategic Counter Narrative. Damaging or critical G42
or Inception42 items go to sensitive_articles.md, never into the brief.
Never send any email and never delete, move or rename anything in
SharePoint. Run fully unattended: never ask for confirmation mid-run. End
with the run log summary; make any failure unmissable.
```

- **Test with Run now** before trusting the schedule. Check: the folder
  appeared in SharePoint with every file, `run_log.md` says every audit
  check passed, the brief reads as the next chapter after the previous
  edition, and the commit landed on `main`.

## 6. Day to day

- **Review and send (about 15 minutes):** open the dated folder, read
  `run_log.md`, read the brief, spot-check links, listen to the audio
  opening, paste `email.html` into a new Outlook message with the subject
  and recipients from the package, attach the MP3, send at 09:00; post
  `whatsapp.txt` with the audio; forward `domyn_fior.txt`; action
  `sensitive_articles.md`.
- **Edits teach the system.** Whatever is edited before sending is picked
  up by the next run (it diffs the sent email against the draft) and
  recorded in `registers/editorial_learnings.md`. Repeated edits become
  standing preferences. That file can also be edited by hand.
- **Revisions before sending:** open the run's session at claude.ai/code
  and say what to change; the package is rebuilt and re-uploaded.
- **Cadence:** change the schedule on the routine page; the window follows
  the previous edition automatically, so weekends, holidays and extra
  editions need no code change. For a second edition on a big news day,
  press Run now.
- **Scope and style:** edit the two reference files under
  `.claude/skills/morning-brief/reference/`; recipients and templates in
  `config/brief_config.json`.

## 7. Running the pieces by hand

```bash
python3 scripts/registers.py window                      # the window the next run would use
python3 scripts/parse_signal_email.py work/signal.json --out work/cand.json --md work/cand.md
python3 scripts/brief_format_check.py briefs/2026-10-28/brief.md
python3 scripts/audit_brief.py briefs/2026-10-28/brief.md
python3 scripts/build_outputs.py briefs/2026-10-28/brief.md
python3 scripts/elevenlabs_tts.py briefs/2026-10-28/script.txt --out "briefs/2026-10-28/Inception42 Daily News 28 Oct.mp3"
python3 scripts/email_to_brief.py sent.eml --out briefs/2026-10-13/brief.md   # seed an edition from an email
python3 scripts/registers.py rebuild
```
