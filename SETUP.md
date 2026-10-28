# Setup: the Inception42 Morning Brief routine

One-time setup, then day-to-day operation. Everything runs under Jack's
claude.ai account for now (decision of 28 October 2026); move it to a
service account later if commits and uploads should not carry an
individual's identity.

## 1. Repository

- GitHub: `jackmclintock/Monitoring`, default branch `main`. Runs clone
  `main`, so merge the working branch into `main` before scheduling.
- The run lands every edition on `main`: it pushes there directly when the
  routine's credentials allow it, otherwise it pushes its session branch and
  opens and merges its own pull request into `main`. No routine setting is
  needed for this; the run log records which path it took.

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
creates folders and files under `Monitoring Testing`. It never sends
mail, never deletes, moves or renames anything.

## 4. SharePoint output folder

`config/brief_config.json` points at the Monitoring folder Ines shared
(`Inception / Account Management / Monitoring / Jack`) as the parent. The
first run creates `Monitoring Testing` under it and records the new
folder id back into the config. To use a different parent, put that
folder's item id in `sharepoint.monitoring_folder_item_id` (visible in
the `file:///<drive>/<item id>` URI the connector returns for the folder).

## 5. The routines (claude.ai/code/routines)

Two routines, created once from the routines page so the Microsoft 365
connector is attached (a routine created any other way runs without it and
cannot read the Signal alerts or upload to SharePoint). Two placeholder
routines with these names already exist, switched off and without the
connector; either open each one, attach Microsoft 365, paste the prompt and
switch it on, or delete them and create fresh ones with the same names.

| | Morning | Second edition |
|---|---|---|
| Name (exact) | `Inception42 Morning Brief` | `Inception42 Morning Brief (second edition)` |
| Schedule | Monday to Friday, 06:45 Gulf Standard Time | Monday to Friday, 14:00 GST, switched **off** |
| Repository | jackmclintock/Monitoring (branch main) | same |
| Environment | `Monitoring` (Full network access) | same |
| Model | Claude Opus 5.5 (`claude-opus-5-5`) | same |
| Connectors | Microsoft 365 only | Microsoft 365 only |
| Prompt | `routines/morning.prompt.txt`, pasted as is | `routines/second-edition.prompt.txt`, pasted as is |

Model: every routine runs on Claude Opus 5.5. Pick it in the routine's
model selector when creating or editing the routine; a scheduled task
created another way is set with its model field. Interactive sessions on
this repository should also be started on Opus 5.5.

The names matter: the dashboard finds the routines by name and rewrites
their days and times when the Schedule page is saved, switches the second
edition on and off, and starts an extra run from the Overview button. After
that first set-up nobody needs to open the routines page again.

**Test with Run now** on the morning routine before trusting the schedule.
Check: a dated subfolder appeared under Monitoring Testing with every file,
the edition appears on the dashboard with its run log saying every audit
check passed, the brief reads as the next chapter after the previous
edition, and the commit landed on `main`.

## 5a. The dashboard

https://claude.ai/artifact/VFwMYy1yXEhvyDreV2DQqD (private; share it from
the page's Share menu with the reviewers' claude.ai accounts). On first
open it asks you to create the passphrase. Enter the Tavily and ElevenLabs
keys under Settings if you prefer not to put them in the environment; the
environment wins when both are set. The routine needs the Artifact data
tools available in its session (they are part of Claude Code on the web)
to read the settings and write the run records; if they are missing the
run proceeds on the config alone and says so.

For two editions a day during a period, add an override on the dashboard's
Schedule page with mode "Two editions a day" and save: the second-edition
routine is switched on for you and off again when the override ends.
Saving also needs the Claude Code Remote connector on the saver's claude.ai
account; without it the settings are saved but the routines are not touched,
and the page says so.

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
