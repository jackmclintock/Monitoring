# Inception42 Morning Brief: discovery notes

Prepared 28 October 2026 from three sources: the SMO Conflict Monitoring
repository (the zip Jack built earlier this year), Ines Deval's handover
folder on SharePoint (Clients / General / UAE / Inception / Account
Management / Monitoring / Jack), and the related Outlook traffic (the
"Monitoring" thread of 26 and 27 October, Kavya Sreeram's daily sends,
and the overnight Signal AI alerts).

This is a reading of the current state and a first cut at the target
state. Nothing here is built yet.

## 1. What Ines shared

| Item | Where | What it is |
|------|-------|------------|
| Inception42 Daily Monitoring Overview.docx (14 pages) | Monitoring/Jack | The master spec: what the brief is, categories, geographies, 15 entity groups, people and roles, source tiers, the 10-step daily process, the full agent instructions (structure, placement, tone, Inception42 rules, SCN, Watch Outs, ElevenLabs script, QC) and the six Meltwater Booleans in the appendix. |
| Monitoring emails/ (19 .eml files) | Monitoring/Jack | Every Daily Media Monitoring email sent to Inception42 in October (1 to 27 Oct, weekdays). Each is 8 to 11 MB because the MP3 is attached. |
| Daily Monitoring Procedure.docx | Monitoring/Tuto | The older, shorter procedure (by section flags, companies, the 10 steps). Superseded by the Overview but consistent with it. Note: it contains the ElevenLabs login in plain text. That should be moved to a password manager and rotated. |
| Eleven labs walkthrough.mp4 (1.2 GB) | Monitoring | Screen recording of the audio step. |
| Written Daily Monitoring/, Audio - Daily News MP4/ | Monitoring/Monitoring | The archive folders the process writes to. The written archive only has February populated; the audio archive holds the MP3s (Feb to July visible). |
| Other/Inception Weekly Report Boolean Keywords 0226 V1.docx | Monitoring/Monitoring/Other | Earlier Boolean set from February. |

The daily sends in Outlook (Kavya, 05:00 UTC, which is 09:00 GST) confirm
the live format: "Good morning team," then optional Inception42 mention
bullets, Top Line, Power, Regulation & Trust, Enterprise & Investment,
AI & Innovation, Alliances and Partnerships, Strategic Counter Narrative,
Watch Outs (red), signature, MP3 attached. Recipients: six at
inceptionai.ai, cc Inception@hawthornadvisors.com and the Digital Farm
address. The Overview lists justine.judge as a recipient; the 28 Oct send
did not include her and did include Daniel Bestwick. Treat the live
send as authoritative and confirm.

The two overnight Signal AI emails land in the Inception@ shared mailbox
(and in Jack's inbox) at 00:00 UTC: "Inception AI - corporate & regional
news" (sections: Inception mentions, G42 companies, OpenAI, Gulf/UAE
region) and "Inception AI - AI & Themes" (140 to 220 items). All article
links are click.email.signal-ai.com redirects; many items are "Article
unavailable" licence stubs. Signal also resurfaces old pieces, so dates
must be checked.

## 2. The current process, as a pipeline

1. Collect: read two Signal emails, sweep 16 outlets by hand, run a
   Meltwater check for Inception42 mentions, paste links into notes.
2. Draft: paste the list into the "Inception - Daily Monitoring v3"
   Claude Project with the standard prompt. Claude fetches and drafts.
3. Review: a person checks facts, links, analysis, and corrects.
4. Script: ask Claude for the ElevenLabs script.
5. Audio: ElevenLabs Studio, voice Allistair, manual pauses, export,
   rename "Inception42 Daily News XX Month".
6. Send at 09:00: Outlook email (formatting rules, Watch Outs in red,
   MP3 attached), WhatsApp group post with the audio, written-only copy
   to domyn@ and fior@.
7. Archive: email to Written Daily Monitoring, MP3 to Audio folder.

Rough human time today: collection is the heaviest step (an hour or
more), then review, then production and distribution. Only step 3 is
judgment work. Everything else is mechanical.

## 3. What transfers from the SMO conflict monitoring system

The SMO repo is the right skeleton. These parts carry over almost as is:

- The cloud routine deployment pattern (daily schedule, repo cloned
  fresh, `main` as the system of record, run log as the real verdict).
- Continuity: priors read before writing, do-not-reuse register, the
  "yesterday's brief" follow-up discipline the Overview already asks for.
- The learning loop: diff what was actually sent against the generated
  draft, infer rationale, promote repeated edits to standing preferences.
- Stage 3.5 single-pass adversarial review and the Stage 5 programmatic
  audit (em dashes, banned phrases, US English scan, link checks).
- The tavily-extract skill for bot-walled article bodies.
- The hard rule of never writing from background knowledge.

These parts need to change:

- Output is an HTML email body plus MP3, not a branded .docx. The build
  step becomes an Outlook draft with the exact formatting rules.
- Sourcing is broader. SMO bans Tavily search to save credits because
  built-in WebSearch suffices for one conflict theatre. The Inception
  brief sweeps six categories across 16 outlets daily; Tavily search
  with date filters and domain lists is the sensible replacement for
  the manual outlet sweep, so credit spend will be materially higher.
- Signal AI becomes a machine-read input (parse the two emails via the
  Microsoft 365 connector, resolve the redirect links, drop the licence
  stubs, de-duplicate "+ N similar articles").
- Meltwater has no usable connector (confirmed in the Overview). The
  Inception42 mention check can be covered by Signal's "Inception
  mentions" section plus a Tavily news search for Inception42, Ashish
  Koshy and Ibrahim Al Jallaf in the last 24 hours.
- One rule in the Overview conflicts with the SMO standard: section 4.1
  says that if a fetch fails the agent may write the bullet "from
  general knowledge" and flag it outside the brief. With a reliable
  reader in the loop this should be dropped in favour of the SMO rule
  (no fetch, no bullet) or at minimum the bullet is removed rather than
  written blind.

## 4. Target state (first cut)

Daily cloud routine at about 06:45 GST (02:45 UTC) so the draft is
waiting by 08:00 and a reviewer has an hour before the 09:00 send.
Monday edition covers Friday afternoon to Sunday. No run Saturday or
Sunday.

Stage 0: capability check (web, Tavily key, M365 connector, ElevenLabs
key, priors readable).

Stage 0.5: learn from yesterday. Read yesterday's sent email from the
Inception@ mailbox or Sent Items, diff it against yesterday's generated
draft in the repo, append to editorial learnings, promote repeated
patterns.

Stage 1: ingest priors (last three briefs, register, learnings, open
Watch Outs).

Stage 2: collect.
  a. Signal AI: read both overnight emails, extract item titles, outlet,
     date and resolved URL; filter to the window; drop stubs.
  b. Outlet sweep: Tavily search per category using the Overview's
     category definitions, source tiers and entity lists, restricted to
     the window and to the 16 outlets plus the Gulf tier.
  c. Inception42 and executive mentions: Tavily news search, all
     languages where possible, past 24 hours.
  d. Verify every candidate: fetch (WebFetch first, one batched Tavily
     extract for the bot-walled remainder), confirm headline, date and
     URL, prefer the highest citation tier, one article per story.
  e. Reputation filter: damaging or critical G42 or leadership pieces
     are routed to a separate internal flag for the comms team, never
     into the brief.

Stage 3: write to the Overview's agent instructions (sections 4.2 to
4.7), then the ElevenLabs script (4.8).

Stage 3.5: one adversarial review pass against the Overview rules and
the learnings file.

Stage 4: build.
  a. HTML email body with the exact house formatting (bullets, 8pt
     paragraph spacing, Watch Outs in red, inline source links).
  b. MP3 via the ElevenLabs API (voice Allistair, pauses between
     paragraphs encoded in the script), named "Inception42 Daily News
     DD Month".
  c. Markdown record of the brief committed to the repo.

Stage 5: audit (programmatic): US English, no em dashes, banned
phrases, every link live and pointing at the right slug, no Signal
redirect links, no duplicate citations, Top Line and SCN word and
sentence counts, max two Watch Outs each with a link, Inception42 only
in Abu Dhabi & Gulf and the SCN, every story in-window, no reuse of
prior links.

Stage 6: deliver to the reviewer, not to the client.
  a. Create an Outlook draft to the client recipients with the brief in
     the body and the MP3 attached, subject "Daily Media Monitoring,
     DDth Month".
  b. Create the Domyn and Fior draft (written only).
  c. Upload the MP3 and an HTML or .eml copy to the SharePoint archive
     folders.
  d. Commit and land on `main`; end with a pass/fail run log and a
     short "what to check" note for the reviewer.

Human input at 08:00: open the draft, read, listen, fix anything, press
send, then post the audio to WhatsApp (no sanctioned API for a consumer
WhatsApp group, so this step stays manual unless the client moves to a
WhatsApp Business channel or Teams).

## 5. Open questions

See the message accompanying these notes. The answers decide the
account the routine runs under, the Tavily plan, whether ElevenLabs is
automated, and how far the delivery step goes.
