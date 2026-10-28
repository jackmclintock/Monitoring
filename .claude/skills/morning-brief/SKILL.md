---
name: morning-brief
description: Produce the Inception42 Morning Brief as a review-ready package (email body, audio script and MP3, WhatsApp text, internal copy, sensitive-items file, run log) in a dated SharePoint folder. Use when asked to run, generate, or revise the Inception42 daily monitoring, the Daily Media Monitoring email, or the morning brief. Collects from the overnight Signal AI alerts and a live outlet sweep, verifies every article, writes to the house rules, audits programmatically, and delivers for a human to review and send.
---

# Inception42 Morning Brief: unattended run playbook

This skill runs as a Claude Code cloud routine on this repository, with the
Microsoft 365 connector attached (mail and SharePoint) and these environment
variables: `TAVILY_API_KEY` (bot-walled article bodies), `ELEVENLABS_API_KEY`
(audio), optionally `MS365_TENANT_ID` / `MS365_CLIENT_ID` /
`MS365_CLIENT_SECRET` (large-file upload to SharePoint). It can also be run
interactively ("run the morning brief for today").

The output is never sent to the client by the run. It is a package in a
SharePoint folder that a Hawthorn reviewer opens, checks, and sends at
09:00 GST. The standard the reviewer expects: every bullet rests on article
text the run actually read, every link points at the right live page, US
English, no em dashes, the house structure exactly. The reviewer should be
correcting judgment, not mechanics.

Read these before writing anything, every run:

- `reference/monitoring_scope.md`: categories, geographies, entities, people, sources, tiers.
- `reference/style_rules.md`: structure, bullets, placement, tone, Inception42 rules, SCN, Watch Outs, audio script, QC.
- `registers/editorial_learnings.md`: standing preferences learned from reviewer edits.
- The three most recent editions in `briefs/` (`python3 scripts/registers.py priors`).

## Critical rules

**Fully unattended.** Never ask the user to confirm, approve or review
mid-run. Every gate is a self-check recorded in the run log. The only
terminal states are a delivered package or a loud, clearly explained
failure. If a decision point arises the rules do not cover, make the call
that best serves accuracy, record it, and continue.

**Nothing from memory.** Every fact, figure, quote and link comes from an
article fetched in this run (WebFetch, Tavily extract, or a readable second
source carrying the same wire story). If an article cannot be read by any of
those routes, do not write its bullet; list it in the run log under "could
not verify" with the headline and URL so the reviewer can decide. Never
write "from general knowledge", never mark a bullet as inferred inside the
brief, never invent a URL.

**Window-bounded.** Only developments published inside the monitoring
window (see Stage 1). A story that broke after the window end waits for the
next edition. Signal AI resurfaces old articles: check every date.

**Tavily is a reader, not a search engine.** Discovery, verification and
selection use the free built-in WebSearch and WebFetch. The metered Tavily
extract is called once, after the story list is final, in one batched
basic-depth call, for the selected URLs that WebFetch could not read (see
`.claude/skills/tavily-extract/SKILL.md`). Never `tvly search`, `map`,
`crawl` or `research`.

**Sensitive items never enter the brief.** Damaging or critical coverage of
G42, its leadership, Inception42 or its executives goes to
`sensitive_articles.md` in the package with outlet, headline, URL and a
one-line note. The brief itself stays silent on it.

**Inception42 placement.** Inception42, Jais, Ashish Koshy and Ibrahim Al
Jallaf appear only in the Inception42 coverage bullets, Abu Dhabi & Gulf and
the Strategic Counter Narrative. The audit enforces this.

## Stage 0: capability check

1. **Web**: one WebSearch (e.g. "Reuters AI today") and WebFetch on two or
   three result URLs. If search fails, stop with a clear error. A site-side
   401/402/403/429 on a premium outlet is normal and not a policy problem;
   a uniform failure across every domain or an `x-deny-reason:
   host_not_allowed` header means the environment's network access is not
   Full: stop and report exactly that.
2. **Microsoft 365 connector**: confirm the mail search and SharePoint tools
   are available (`outlook_email_search`, `read_resource`,
   `sharepoint_create_folder`, `sharepoint_upload_file`). If mail is
   unavailable the Signal input is lost: continue on the outlet sweep alone
   and say so prominently in the run log. If SharePoint is unavailable the
   package is still committed to the repo and the run log says delivery
   failed.
3. **Readers and audio** (non-fatal): note whether `TAVILY_API_KEY` and
   `ELEVENLABS_API_KEY` are set. Do not call either now.
4. **Priors**: `briefs/` holds at least one edition and
   `registers/do_not_reuse_register.md` exists.
5. **Config**: read `config/brief_config.json` (recipients, folder ids,
   voice, templates).
6. **Dashboard settings.** Read the document `settings/main` from the
   Morning Brief Operations dashboard (`dashboard.url` in the config) with
   the ArtifactData tool (`action: get`, `collection: settings`,
   `doc_id: main`). If the tool or the document is unavailable, continue on
   the config and environment alone and say so in the run log. Otherwise:
   - **Cadence gate.** Let `today` be the current GST date and `now` the
     GST time. The run produces an edition only if
     `schedule.extra_edition_requested` is true, or a `planner.reports`
     entry has `run_at` within the 90 minutes before `now` (a planned
     special report; its window then applies, see Stage 1), or all of: `today` is not
     on or before `schedule.paused_until`, `today` is not in
     `schedule.holidays`, and either an override in `schedule.overrides`
     whose `from`..`to` range contains `today` allows it (`mode` `daily`
     or `weekends`: one edition at `schedule.time`; `twice`: an edition at
     `schedule.time` and one at the override's `second_time` or
     `schedule.second_time`; `skip`: none) or, with no override, the
     weekday is in `schedule.days` and `now` is within 90 minutes after
     `schedule.time` or `schedule.second_time`. A run that fails the gate
     writes one line to the run log ("no edition: <reason>"), writes
     nothing else, and ends cleanly. When `extra_edition_requested` was
     the reason to proceed, clear it (update `settings/main` with
     `schedule.extra_edition_requested: false`, pinned to the version read)
     before Stage 2.
   - **Keys.** For `TAVILY_API_KEY`, `ELEVENLABS_API_KEY`, `MS365_TENANT_ID`,
     `MS365_CLIENT_ID`, `MS365_CLIENT_SECRET`: the environment variable wins
     when set; otherwise use `keys.tavily`, `keys.elevenlabs`,
     `keys.ms365_tenant`, `keys.ms365_client`, `keys.ms365_secret` from the
     document, exporting them to the environment for the scripts. Never
     print a key in the run log or commit it.
   - **Recipients and delivery.** `recipients.to` / `recipients.cc`
     override the config when non-empty; `delivery.output_folder_id`
     overrides `sharepoint.output_folder_item_id` when set; a new folder
     id created in Stage 6 is written back to both the config and
     `delivery.output_folder_id`.
   - **Editor notes.** `notes_to_next_run`, if non-empty, is treated like
     `briefs/<today>/notes.md` (Stage 1.4). After the package is
     delivered, clear it (update with `notes_to_next_run: ""`), and record
     the note verbatim in the run log.

## Stage 1: window, priors and learning

1. **Window.** The monitoring window is always a fixed 24 hours by
   default: from the standard run time (06:45 GST, `schedule.time` on the
   dashboard) on the previous day to the same time on the day of the run.
   It is anchored to the clock, never to when the previous edition was
   sent, so a late start covers the same hours. Save the dashboard's
   `planner` object to `work/plan.json` and run
   `python3 scripts/registers.py window --planner work/plan.json --time <schedule.time>`:
   when a planner entry's `run_at` falls within the 90 minutes before now,
   the script returns that entry's `window_start` and `window_end`
   instead (an afternoon update, a Friday-to-Monday recap, a conference
   day covered twice). Record the basis line from the script's output in
   the run log. Only when the window is longer than about 48 hours apply
   the weekend-recap conventions (recap phrasing, slightly longer
   elements). Mondays are not merged automatically: without a planner
   entry a Monday edition covers Sunday 06:45 to Monday 06:45.
2. **Learn from the last send.** Search the mailbox for the most recent
   "Daily Media Monitoring" email that went to the client (sender at
   hawthornadvisors.com, received after the previous generated edition).
   If it exists and the matching `briefs/<date>/brief.md` has
   `source: generated`, transcribe the sent version with
   `scripts/email_to_brief.py` to `briefs/<date>/brief_sent.md`
   (`--source reviewer-final`), diff it against the generated brief
   section by section, and append an Observations entry to
   `registers/editorial_learnings.md`: what changed, with an inferred
   rationale from the fixed taxonomy (sourcing, relevance, accuracy, tone,
   structure, language; `unclear` if none fits). Promote to a Standing
   preference only when the same kind of edit has appeared in two or more
   editions, or when the edit enforces an existing rule. Then make
   `brief_sent.md` the authoritative prior for that edition (copy it over
   `brief.md`, keeping the generated draft as `brief_generated.md`) and
   rebuild the register (`python3 scripts/registers.py rebuild`). Never
   argue with or revert a reviewer's edit.
3. **Priors.** Read the three most recent editions in full. Note the
   latest Top Line thesis and the open Watch Outs
   (`python3 scripts/registers.py watchouts`). Each open Watch Out is
   consciously handled: it either moved (a follow-up bullet or a new Watch
   Out with the new state) or did not (then it is not reintroduced as new;
   a one-line "no change, still monitoring" is acceptable only if it is
   still live and material).
4. **Editor notes.** If `briefs/<today>/notes.md` exists (an upcoming
   Inception42 event, context not in the articles), use it as instructed.

## Stage 2: collect candidates

Create `briefs/<YYYY-MM-DD>/` (append `-HHMM` in GST if an edition already
exists for the date) and a `work/` subfolder for intermediate files.

### 2a. Signal AI emails

1. `outlook_email_search` with sender `alerts@email.signal-ai.com`,
   `afterDateTime` = window start, limit 10. Expect two emails per night:
   "Inception AI - corporate & regional news" and "Inception AI - AI &
   Themes". Over a weekend there may be several of each; read all inside
   the window.
2. For each, `read_resource` the message URI. Save the returned JSON to
   `work/signal_<n>.json` (write the whole object, with `body.content`
   intact) and run
   `python3 scripts/parse_signal_email.py work/signal_<n>.json --out work/cand_signal_<n>.json --md work/cand_signal_<n>.md --window-start <ISO>`.
   The script drops licence stubs, resolves the tracking redirects to real
   URLs, flags stale dates and headline/URL mismatches, and keeps the
   section (Inception mentions, G42 companies, OpenAI, Gulf/UAE region, the
   AI & Themes topics).
3. Read the markdown shortlist. Signal is wide: most "G42 companies" items
   are noise (M42 the US holding company, Analog the magazine, Falcon
   generic, Inception the film). Keep what fits the scope; a weak-outlet
   item on a real story is a lead to search for a Tier 1 or 2 source, not a
   citation.

### 2b. Outlet sweep (free WebSearch)

Run targeted WebSearch queries for the window, by category, against the
outlet list in `monitoring_scope.md`. Useful shapes: "<outlet> AI
<topic>", "site:reuters.com artificial intelligence <date>", "<entity>
<what happened>", and the categories' own keywords (export controls,
executive order, AI Act, lawsuit, funding round, data center, partnership,
MoU, model launch, benchmark). Cover every category and every core entity
group (G42 ecosystem, OpenAI, Nvidia, Microsoft, Gulf sovereigns, the UAE
institutions). Aim for breadth first: a candidate list of 40 to 80 items
on a normal weekday is typical before selection.

### 2c. Inception42 and executive mentions (replaces the Meltwater check)

WebSearch for "Inception42", "Inception AI" G42, "Jais", "Ashish Koshy",
"Ibrahim Al Jallaf" / "AlJallaf", "InceptionClaw", and the active product
names, restricted to the window. Combine with Signal's "Inception
mentions" section. Every genuine mention becomes an Inception42 coverage
bullet (clustered by story: one bullet per story, naming all the outlets),
except sensitive items, which go to `sensitive_articles.md`.

### 2d. Verify and select

For every candidate that may make the brief:

1. **WebFetch the URL.** Confirm headline, publication date and the facts
   you will use. Record "fetch-verified".
2. **If bot-walled** (Reuters, Bloomberg, FT, WSJ, WaPo often are): keep
   the candidate on the strength of the search snippet plus a readable
   second source carrying the same development (a syndicated copy, a
   trade-press or regional-paper writeup, the official release). Record
   "snippet-verified" and the second source. The link in the brief still
   goes to the original outlet.
3. **Date gate.** Publication time inside the window; otherwise drop it.
4. **Tier gate.** When several outlets carry the story, cite the highest
   tier; link two or three outlets on a big story, in the house order
   (wire or Tier 1 first).
5. **Reuse gate.** Not already cited in a prior edition
   (`registers/do_not_reuse_register.md`). A continuing story gets a
   follow-up bullet referring to the earlier edition, with a new in-window
   source.
6. **Placement.** One best section per story, per `style_rules.md`.

Then, once and only once the selection is final: collect the selected
URLs that are still snippet-verified and whose bullet needs body detail (an
exact figure, a quote), and if `TAVILY_API_KEY` is set run one batched
basic-depth `tvly extract` on them (up to 20 URLs; follow the
tavily-extract skill). Upgrade those stories to fetch-verified. At most one
retry batch for transient failures. If the key is missing, the stories
stand on snippet-plus-second-source verification; note the reduced depth.

Write `work/candidates.md`: every candidate considered, its source
(Signal section or search), its verification status, and its disposition
(section, dropped as out of scope, out of window, duplicate, unverifiable,
sensitive). This file ships in the package as `candidates.md`.

## Stage 3: write the brief

Write `briefs/<date>/brief.md` in the canonical format
(`docs/brief-format.md`) with front matter `source: generated`,
`window_start` and `window_end`, following `style_rules.md` exactly:

1. Inception42 coverage bullets (if any), then Top Line, the six category
   sections (omit any with no story; never pad), Strategic Counter
   Narrative, Watch Outs (max 2).
2. Every bullet: fact, implication, inline links. Word counts per the
   rules. Section-level: no cap on bullets; every relevant verified story
   goes in.
3. Top Line and SCN written as wholes and counted as wholes.
4. Follow-ups refer to the earlier edition precisely ("Monday's brief").
5. Monday or long-window editions use the weekend-recap conventions.

Run `python3 scripts/brief_format_check.py briefs/<date>/brief.md` and fix
any structural problem.

## Stage 3.5: adversarial review (exactly one pass)

Re-read the whole draft as the reviewer would, hunting for the problems
the team has fixed by hand before:

- Hard rules: in-window, verified, no reuse, placement, Inception42 only
  where allowed, no OpenAI setback used as a selling point, no judgment of
  partner nations, no em dashes, no banned phrases, no "according to", US
  English, Watch Outs conditional and specific with links, SCN moves global
  to Gulf to Inception42 and opens on a concrete anchor fact, Top Line
  structure varied from the last three editions.
- `registers/editorial_learnings.md`: every Standing preference satisfied;
  Observations patterns not repeated.
- Mechanics: outlet names right, links on the right outlets, numbers
  consistent across Top Line, bullets and SCN.

Produce a numbered findings list (empty is fine), apply each finding unless
it would require unverified material, record the dispositions for the run
log, and do not review again: the Stage 4 audit is the only later gate.

## Stage 4: programmatic audit

`python3 scripts/audit_brief.py briefs/<date>/brief.md --json briefs/<date>/work/audit.json`

Hard failures (structure, em dash, Signal link, duplicate link, reuse,
banned phrase, Watch Out rules, Inception42 placement, British spelling,
dead link) are fixed and the audit re-run until it exits 0.

### Stage 4.5: fix pass (mandatory)

A reviewer should only ever see what the model genuinely cannot settle.
After the audit exits 0, work through every warning and every item on the
"needs a person" list with one more pass, then re-run the audit. Up to
three rounds; the pass ends early when nothing is left that the rules
below can fix.

- **length**: rewrite the bullet to 70 words or fewer (Top Line and SCN
  to their ranges) without dropping a fact or a link.
- **temporal**: replace "yesterday", "today", "this week", "later this
  week" and similar with the date or the plain phrase ("the 27 October
  brief", "its upcoming investor day"). Never invent a date the source
  does not give.
- **tics**: rephrase the "not X but Y" or the rhetorical question.
- **bot-wall**: no rewrite. A probe that returns 401, 403 or 429 on a
  story already read in Stage 2 (directly, via a second source, or via
  the Tavily batch) is settled; write it as a resolved issue with that
  reason (`--settled bot-wall=...`). If the story was never actually
  read, it is not settled: find a readable source or drop the bullet.
- **single source**: run one targeted search for a second outlet; if one
  readable source is found, add it; if not, keep the bullet only when the
  single source is a wire or a major outlet, and log the issue.
- **dead or mismatched link**: one search for the correct URL of the same
  article; if found, replace; if not, replace the citation with a
  readable second source or drop the bullet, and log what was dropped.
- **missing audio key, missing Signal email, failed upload**: not
  fixable by rewriting; log as issues with the right severity.

The pass is one adversarial read, not a new draft: change only the lines
the warnings name and their direct consistency ripples. Record in the run
log what the pass changed and what it could not. Only the warnings that
survive the pass become open issue documents in Stage 6.

## Stage 5: build the package

1. `python3 scripts/build_outputs.py briefs/<date>/brief.md` writes
   `email.html`, `email.txt`, `subject.txt`, `recipients.txt`,
   `whatsapp.txt`, `domyn_fior.txt`, `README.md`.
2. **Audio script.** Write `briefs/<date>/script.txt` from the final brief
   per the ElevenLabs section of `style_rules.md` (about 630 words, oral
   prose, fixed opening and closing lines, "Across the Gulf..." for the
   Gulf thread, numbers in words, no Watch Outs, no markdown, no em
   dashes, blank line between paragraphs).
3. **Audio.** If `ELEVENLABS_API_KEY` is set:
   `python3 scripts/elevenlabs_tts.py briefs/<date>/script.txt --out "briefs/<date>/<audio filename from config>"`.
   Exit 78 means not configured (note it; the reviewer produces the audio
   in Studio from `script.txt`); exit 1 is a failure to report. The MP3 is
   never committed to git (ignored).
4. **Sensitive items.** Write `briefs/<date>/sensitive_articles.md`: a
   heading, then one bullet per held-out item (outlet, headline, URL, date,
   one-line note on why it was held and what it says), or the line "No
   sensitive items identified in this window." The file always exists.
5. **Run log.** Write `briefs/<date>/run_log.md`: window and basis;
   inputs read (Signal emails found, candidate counts per source); stories
   selected per section with verification status (fetch / snippet plus
   second source) and timestamps; Tavily call made (how many URLs, how many
   credits) or not; prior Watch Outs and how each was handled; learning
   step (what the last sent email changed, if anything); adversarial
   review findings and dispositions; audit result with remaining warnings;
   items that could not be verified; audio result; delivery result;
   anything the reviewer should look at first. Make failures unmissable.

## Stage 6: deliver

1. **SharePoint folder.** Using the connector: if
   `sharepoint.output_folder_item_id` in the config is null, create the
   folder named `sharepoint.output_folder_name` under
   `monitoring_folder_item_id` on `drive_id`, record the new id in the run
   log and in `config/brief_config.json`, and commit that change. Then
   create a subfolder named `<YYYY-MM-DD>` (or `<YYYY-MM-DD>-<HHMM>` for a
   second edition). Run `python3 scripts/md_to_rtf.py <edition folder>`
   to convert every Markdown and text file to RTF, then upload the RTF
   files and the HTML email (`sharepoint_upload_file` with `content`):
   `README.rtf`, `brief.rtf`, `email.html`, `subject.rtf`,
   `recipients.rtf`, `whatsapp.rtf`, `domyn_fior.rtf`, `script.rtf`,
   `sensitive_articles.rtf`, `candidates.rtf`, `run_log.rtf`. Reviewers
   open RTF in Word or Outlook; the `.md` and `.txt` files stay in the
   repository as the canonical text and are not uploaded.
2. **Audio file.** The connector caps uploads at 1 MB and the MP3 is 6 to
   9 MB. If the Graph credentials are set, run
   `python3 scripts/graph_upload.py "<mp3>" --folder-id <subfolder id>`.
   Otherwise, if the file is under 1,000,000 bytes, upload it base64
   through the connector; otherwise attach it to the session output
   (SendUserFile if available) and state plainly in the run log and
   `README.md` that the audio must be downloaded from the run session or
   regenerated from `script.txt` in ElevenLabs Studio.
3. **Commit and land on `main`.** Commit the edition folder (not the MP3),
   the register (`python3 scripts/registers.py append briefs/<date>/brief.md`),
   the learnings file, and any config change. Push to `main` directly if
   the routine has unrestricted pushes; otherwise push the session branch,
   open a pull request into `main` with the GitHub tools and merge it,
   confirming `main`'s head is the new commit. The next run only sees what
   is on `main`.
4. **No Outlook.** The run never creates a draft or sends anything. The
   package in SharePoint is the hand-off and the reviewer does the send.
5. **Dashboard record.** Write `runs/<edition id>` on the dashboard
   (ArtifactData `set`; `<edition id>` is the briefs folder name, e.g.
   `2026-10-29` or `2026-10-29-1400`) with: `id`, `date`, `weekday`,
   `edition` (`morning`, `afternoon`, `extra`), `status` (`delivered`,
   `warnings` when audit warnings or unverified items remain, `failed`),
   `source: generated`, `window_start`, `window_end`, `window_hours`,
   `sections`, `bullets`, `links`, `top_line` (first 600 characters),
   `watch_outs` (list), `audit` (`{hard, warnings, note}`), `audio` (the
   MP3 filename or null), `folder_url` (the SharePoint subfolder web URL),
   `reviewer_notes` (the two or three things to look at first),
   `brief_md` (the full canonical markdown), `run_log` (the full run log
   text), `sensitive` (the text of sensitive_articles.md), `created_at`.
   Keep the document under 200 KB (trim `run_log` first if needed).
   Issues are one list, and the dashboard counts from it, so every audit
   finding and everything the run could not settle must be written as an
   issue document: run `scripts/audit_brief.py ... --json work/audit.json`
   (the Stage 4 run already does), put the non-audit items (each
   unverifiable article left out, a dead or mismatched link the audit
   could not fix, a failed audio or upload step, a missing Signal email)
   in `work/extra_issues.json` as `[{title, detail, severity}]`
   (`high` for a failed delivery or a missing input, `medium` for content
   left out, `low` for warnings), then run
   `python3 scripts/dashboard_issues.py <edition id> --audit work/audit.json --extra work/extra_issues.json --settled bot-wall="Verified by Tavily extract during the run" --out work/issue_writes.json`
   and send each output file with ArtifactData `batch` (`writes` from the
   file). A `--settled` code marks warnings the run dealt with itself
   (bot-wall probes that Tavily read, for example); they are written
   already resolved so the reviewer sees them counted but not waiting.
   Never resolve a `temporal`, `length`, `reuse` or link warning this way.
   Set `audit.warnings` in the run document to the total number of audit
   issue documents written, and `status` to `warnings` when any issue is
   left open, otherwise `delivered`. On a failed run, still write the
   `runs/` document with `status: failed` and the reason in `run_log`.
6. **Final message.** End the session with the run log summary: edition,
   window, counts, audit result, delivery location (folder URL), and the
   three things the reviewer should look at first.

## Revisions

A reviewer may ask for changes in the run's session or a fresh one ("swap
the Power lead for the Reuters piece", "tighten the SCN"). Apply only the
requested change and its consistency ripples; replacement stories are
sourced under the full Stage 2 gates within the edition's original window;
re-run Stage 3.5 once and the Stage 4 audit in full; rebuild the package
with `build_outputs.py`; regenerate `script.txt` and the audio if the
brief text changed; re-upload to the same SharePoint subfolder with
`conflictBehavior` replace; commit; and log the instruction as an
editorial learning. If an instruction cannot be met honestly (no in-window
source for the requested angle), say so rather than inventing one.

## Changing cadence and scope

- **Time or days**: edit the routine's schedule at claude.ai/code/routines.
  The window computes itself from the previous edition, so weekends,
  holidays and skipped days need no code change.
- **Second edition on a big news day**: "Run now" on the routine (or ask
  an interactive session to run the morning brief). The window starts at
  the morning edition's end; the folder gets a `-HHMM` suffix; the subject
  stays the house subject and the reviewer decides how to send it.
- **Scope**: edit `reference/monitoring_scope.md` (entities, people,
  outlets) or `reference/style_rules.md` (format, tone); runs pick the
  change up next cycle. Recipients and templates live in
  `config/brief_config.json`.
