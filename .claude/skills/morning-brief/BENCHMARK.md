# Daily benchmark: generated edition against the sent edition

The target is that every generated edition is at or better than the one
the team sends. This runs once a day after the client email has gone
(10:30 GST on weekdays, the "Inception42 Morning Brief (benchmark)"
routine), and it is the loop that turns each day's gap into a rule the
next run reads.

## Steps

1. **Find the sent edition.** Search the mailbox for today's "Daily Media
   Monitoring" email from a hawthornadvisors.com sender (subject "Daily
   Media Monitoring <D>th <Month>"). If none has arrived, write one line
   ("no sent edition yet for <date>") and stop; the routine runs again the
   next day and the morning run's learning step covers any gap.
2. **Transcribe it.** Save the HTML body to `work/sent.html` and run
   `python3 scripts/email_to_brief.py work/sent.html --out briefs/<date>/brief_sent.md --subject "<subject>" --sent <ISO> --sender <address> --source reviewer-final`.
   If `briefs/<date>/brief.md` has `source: generated`, copy it to
   `briefs/<date>/brief_generated.md` (if not already there) and copy
   `brief_sent.md` over `brief.md`, so the sent edition is the prior and
   the register is rebuilt from it (`python3 scripts/registers.py rebuild`).
3. **Score.**
   `python3 scripts/benchmark.py briefs/<date>/brief_generated.md briefs/<date>/brief_sent.md --date <date> --out briefs/<date>/benchmark.json --md briefs/<date>/benchmark.md`.
   The script matches stories by shared link or shared entities, and
   reports coverage (sent stories the generated edition carried), missed,
   extra, shared links, Tier 1 and 2 share, length and a mechanical
   verdict: "at or better" needs 80 percent coverage, a Tier 1 and 2
   share within 15 points of the sent edition, and 1,250 to 1,750 words.
4. **Classify every miss.** For each story in `missed`, find out why,
   using `briefs/<date>/candidates.md`, the sweep digest if it was kept,
   and the run log. Exactly one of:
   - `not-found`: the story was not in the sweep, Signal or search
     results. Fix: a query or feed to add to `config/sweep_queries.json`
     (do it, if the outlet or topic is identifiable).
   - `not-selected`: it was a candidate and the desks ranked it out. Fix:
     a selection rule (which kinds of story the sent edition values
     more) for the learnings.
   - `rule-dropped`: a gate removed it (window, reuse, tier, placement).
     Fix: say which gate and whether the gate or its reading was wrong.
   - `unreadable`: it was selected but could not be read, so it was not
     written. Fix: a reading path (Tavily depth, a syndicated copy).
   - `judgment`: the sent edition's choice is arguable and the generated
     choice was reasonable. No fix.
   Also classify each `extra` story as `better` (a story the sent edition
   should have had), `fine` (legitimate alternative) or `weaker` (the
   sent edition's choice was better); and note any outlet-choice gap
   (same story, lower-tier link).
5. **Record.** Append a dated Observations entry to
   `registers/editorial_learnings.md` with the verdict, the numbers, the
   classified misses and extras, and the fixes made. Promote a fix to a
   numbered standing preference when the same class of miss has appeared
   on two or more days. Apply config fixes (`sweep_queries.json`) in the
   same commit. Never argue with or revert the reviewer's choices in the
   sent edition.
6. **Dashboard.** Update `runs/<date>` (ArtifactData `update`, pinned to
   the version read) with a `benchmark` object:
   `{verdict, coverage, covered, missed_count, extra_count, shared_links, tier_generated, tier_sent, length_generated, length_sent, missed: [{section, story, why, fix}], extra: [{section, story, grade}], note, at}`.
   Keep `missed` and `extra` to the first 160 characters of each story.
7. **Commit and land on `main`** (same rule as the morning run: direct
   push, else branch plus merged pull request). The next morning run reads
   the learnings, the register and the config from `main`.
8. **Final message.** Verdict, coverage, the classified misses in one
   line each, and the fixes made.

## What "at or better" means in practice

Coverage is the first measure because the client reads the sent edition
as the record of the day; a generated edition that carries 80 percent of
those stories plus its own verified additions is at parity or better.
Sourcing is the second: the client expects Reuters, Bloomberg, FT and
WSJ on the big stories. Length is the third. Judgment calls (the same
day told with different stories) are not misses; the classification
step exists to tell the two apart.
