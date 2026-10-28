# Inception42 Morning Brief: automated monitoring

Daily production of the Inception42 Morning Brief (the "Daily Media
Monitoring" email Hawthorn Advisors sends to Inception42's leadership at
09:00 GST) by a scheduled Claude Code cloud routine. The routine collects
the overnight Signal AI alerts and sweeps the outlet list, verifies every
article it uses, writes the brief to the house rules, audits it, produces
the ElevenLabs audio script and bulletin, and delivers a review-ready
package into a dated SharePoint folder. A person reviews and sends.

- **Setup and operation:** [SETUP.md](SETUP.md)
- **Run playbook (the spec every run executes):** [.claude/skills/morning-brief/SKILL.md](.claude/skills/morning-brief/SKILL.md)
- **What is monitored:** [.claude/skills/morning-brief/reference/monitoring_scope.md](.claude/skills/morning-brief/reference/monitoring_scope.md)
- **House style:** [.claude/skills/morning-brief/reference/style_rules.md](.claude/skills/morning-brief/reference/style_rules.md)
- **Discovery notes (how we got here):** [docs/00-discovery-notes.md](docs/00-discovery-notes.md)
- **Operations dashboard (private, passphrase-gated):** https://claude.ai/artifact/VFwMYy1yXEhvyDreV2DQqD

## The dashboard

Morning Brief Operations is a Hawthorn-branded page on claude.ai, shared
only with the accounts that need it and gated by a passphrase. It shows
the last editions with their audit results and run logs, the open issues,
and the next scheduled runs, and it holds the settings the routine reads
at the start of every run: run days and times, pauses, holidays, temporary
overrides (a conference week with two editions, a weekend that needs
cover, a fortnight with none), the Tavily, ElevenLabs and Graph
credentials, recipients, and notes for the next run. The routine writes
each edition and any issue it could not settle back to the page. The page
cannot change when the platform routine fires; it decides what a fired run
does.

## What a run produces

A folder `Monitoring Testing/<YYYY-MM-DD>/` in SharePoint (Inception /
Account Management / Monitoring) and the same files committed under
`briefs/<YYYY-MM-DD>/` here:

| File | Purpose |
|---|---|
| `README.md` | What is in the package and the reviewer checklist |
| `brief.md` | The brief in canonical markdown (source of everything else) |
| `email.html` | Client email body, house formatting, paste-ready |
| `subject.txt`, `recipients.txt` | Subject line and To/Cc from `config/brief_config.json` |
| `Inception42 Daily News D Mon.mp3` | Audio bulletin (when the ElevenLabs key is set) |
| `script.txt` | The ElevenLabs script the audio came from |
| `whatsapp.txt` | Message to post with the audio in the client WhatsApp group |
| `domyn_fior.txt` | Internal copy for the Domyn and Fior teams |
| `sensitive_articles.md` | Damaging or critical G42 or Inception42 items held out of the brief, for the comms team |
| `candidates.md` | Every article considered and what happened to it |
| `run_log.md` | Window, inputs, verification per story, audit result, delivery |

Human input: open the folder, read the run log, review the brief, send the
email at 09:00, post the WhatsApp message with the audio, forward the
internal copy, and decide on anything in the sensitive file. Nothing is
sent by the routine.

## How it works

| Stage | What happens |
|---|---|
| 0 Capability check | Web search and fetch work; Microsoft 365 connector present; Tavily and ElevenLabs keys noted; priors and config readable |
| 1 Window and learning | Window runs from the previous edition's end to now (so Mondays, holidays and extra editions need no configuration). The last sent email is diffed against the generated draft and the differences logged as editorial learnings |
| 2 Collect | Signal AI emails parsed (`scripts/parse_signal_email.py`: stubs dropped, redirects resolved, stale dates flagged); outlet sweep by built-in web search; explicit Inception42 and executive mention search; every candidate fetched and date-checked; one batched Tavily extract for the bot-walled remainder |
| 3 Write | Canonical `brief.md` to the house rules |
| 3.5 Review | One adversarial pass against the rules and the learnings |
| 4 Audit | `scripts/audit_brief.py`: structure, em dashes, Signal links, duplicates, reuse, banned phrases, Watch Out rules, Inception42 placement, US English, dead links |
| 5 Package | `scripts/build_outputs.py`, the audio script, `scripts/elevenlabs_tts.py`, the sensitive file, the run log |
| 6 Deliver | SharePoint folder via the connector (audio via Graph when configured), commit to `main`, run log in the session |

## Repository layout

| Path | Purpose |
|---|---|
| `.claude/skills/morning-brief/` | The run playbook and its two reference files |
| `.claude/skills/tavily-extract/` | Vendored Tavily reader skill (extract only) |
| `briefs/<date>/` | Every edition: seeded transcriptions of sent emails (`source: outlook-sent`) and generated packages. The continuity record |
| `registers/do_not_reuse_register.md` | Every link ever cited; rebuilt from `briefs/` |
| `registers/editorial_learnings.md` | Standing preferences and the observation log |
| `config/brief_config.json` | Recipients, templates, voice, SharePoint ids |
| `scripts/` | Parser, transcriber, format check, audit, package builder, registers, audio, Graph upload |
| `docs/` | Discovery notes and the brief format spec |
| `templates/` | Run log and sensitive-items templates |

## Seeded history

October 2026 editions are seeded from the emails that went to the client:
14 to 28 October with every link; 1 to 9 October as text only (the
SharePoint copies are .eml files whose rendering drops hyperlinks); 12 and
13 October are not yet seeded for the same reason. Forwarding those nine
emails to a mailbox the connector can read, or dropping the .eml files into
`briefs/<date>/`, lets `scripts/email_to_brief.py` complete them.

## Things to watch

- **Green is not success.** The run log at the end of each session is the
  verdict, not the routine's status colour. Read it with the brief.
- **Continuity lives on `main`.** Anything not merged there does not exist
  for the next run.
- **The MP3 is bigger than the connector allows.** Until the Graph upload
  credentials are set, the audio is attached to the run session rather
  than the SharePoint folder (see SETUP.md).
- **Bot walls are normal.** Reuters, Bloomberg, the FT and the WSJ refuse
  automated fetching; stories from them are verified through the search
  snippet plus a second readable source, then read through Tavily once
  the selection is final.
- **The registers only grow.** `editorial_learnings.md` needs occasional
  human tidying.
