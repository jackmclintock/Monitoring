# Canonical brief format

Every edition of the Inception42 Morning Brief is stored in the repository
as `briefs/<YYYY-MM-DD>/brief.md` (a second edition on the same day uses
`briefs/<YYYY-MM-DD>-<HHMM>/`). This markdown is the continuity record
that future runs read, the input the email and audio builders consume,
and the thing the audit checks. Seeded editions transcribed from sent
emails use exactly the same shape.

## Shape

```
---
date: 2026-10-28
weekday: Wednesday
edition: morning          # morning | afternoon | special | extra | test
label:                    # special and extra editions only, e.g. Post-ADIPEC special report
subject: Daily Media Monitoring 28th October
sent_at: 2026-10-28T05:00:45Z
sender: k.sreeram@hawthornadvisors.com
source: outlook-sent
window_start: 2026-10-27T05:00:00Z
window_end: 2026-10-28T02:45:00Z
---

Good morning team,

## Inception42 coverage
- One bullet per Inception42 mention, verbatim as sent. [Outlet](https://...)

## Top Line
One prose paragraph.

## Power
- Bullet text. Second sentence with the implication. [Reuters](https://...) / [Bloomberg](https://...)

## Regulation & Trust
- ...

## Enterprise & Investment
- ...

## AI & Innovation
- ...

## Alliances and Partnerships
- ...

## Abu Dhabi & Gulf
- ...

## Strategic Counter Narrative
One prose paragraph.

## Watch Outs
- Bullet with an inline link. [Outlet](https://...)
```

## Rules

- Front matter keys are fixed. `source` is `outlook-sent` for a seeded
  transcription of an email that went to the client, `generated` for a
  routine draft, `reviewer-final` for a reviewer's edited version.
  `window_*` are optional on seeded editions (unknown) and required on
  generated ones.
- Section headings are exactly the strings above, in that order. A
  section that did not appear in the edition is omitted entirely, never
  left empty.
- "Inception42 coverage" holds the bullets that the sent emails place
  above the Top Line without a heading. The email builder renders them
  without a heading to match the house format.
- Bullets start with `- `. Prose sections are a single paragraph.
- Links are markdown `[Outlet Name](URL)`; several sources on one bullet
  are separated by ` / `. The outlet name is the publication as the
  email showed it. URLs are copied exactly, never shortened, never a
  Signal AI redirect.
- Seeded transcriptions are verbatim. Do not correct spelling, style, or
  links; the sent email is the record of what the client received.
- No em dashes in generated editions. A seeded edition keeps whatever the
  email contained.
