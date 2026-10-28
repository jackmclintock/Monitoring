# Style rules for the Inception42 Morning Brief

Source: Ines Deval's "Inception42 Daily Monitoring Overview" (October 2026),
sections 4.1 to 4.9, reconciled with the October 2026 sent editions in
`briefs/`. Where the written spec and the sent editions differ, the sent
editions win and the difference is noted.

## The product in one line

A daily AI intelligence brief for Inception42's C-suite and senior
stakeholders that says what the day's AI news means for the sector and for
Abu Dhabi, not just what happened. The readers are inside G42 and
Inception42: they know their own news already.

## Structure (in this order; a section with nothing in it is omitted, never padded)

| Element | Length | Content |
|---|---|---|
| "Good morning team," | 1 line | Fixed opener |
| Inception42 coverage | bullets, no heading in the email | Mentions of Inception42, its executives or products in the window; each bullet names the outlets with inline links. Sent editions put these above the Top Line. One bullet per story cluster; when a story has been running for days, say so ("Since Thursday...") |
| Top Line | about 165 words, 5 sentences (4 to 6) | One prose paragraph. A sharp directional thesis on the biggest story, then 3 or 4 headline stories of the brief linked in one logical thread. Few statistics. No sources, no links |
| Power | as many bullets as relevant | AI geopolitics, government policy, national security, power shifts between major AI actors |
| Regulation & Trust | bullets | Legislation, court rulings, regulators, safety incidents, deepfakes, privacy, cybersecurity, agent-control incidents, opinion polls |
| Enterprise & Investment | bullets | Earnings, funding, M&A, enterprise adoption, market moves, data center capex, macro and financial-stability angles |
| AI & Innovation | bullets | Model and product launches (always here), capabilities, benchmarks, research, agentic AI, standards, robotics, world models, custom chips |
| Alliances and Partnerships | bullets | Named agreements between parties: partnerships, JVs, MoUs, compute and data center deals. Not product launches |
| Abu Dhabi & Gulf | bullets | UAE and Gulf AI ecosystem: G42 group, data centers, sovereign funds, UAE/Saudi/Qatar policy, digital government, any Ashish Koshy or Ibrahim Al Jallaf mention (its own bullet) |
| Strategic Counter Narrative | about 185 words, 5 sentences (5 to 8) | Prose. Global dynamic, then the Gulf and Abu Dhabi, then Inception42 only if a real link exists |
| Watch Outs | max 2 bullets, 1 to 2 sentences each | Pending decisions or risks, hyper-specific (dates, names, thresholds, amounts), each with an inline source link. Rendered in red in the email |

## Bullets

- Two sentences, about 45 to 60 words: the fact, then the implication. No third clause. Minor stories: one sentence of 35 to 50 words. Abu Dhabi & Gulf bullets may run slightly fuller but stay inside about 60 words.
- Every bullet ends with inline links on the publication names: `[Reuters](url) / [Bloomberg](url)`. Several sources are separated by " / ". The link text is the publication name as the house writes it (Reuters, Bloomberg, Financial Times, The National, Khaleej Times, South China Morning Post, WAM, Zawya).
- Never a Signal AI redirect or tracking link. Never a homepage or placeholder.
- When several outlets carry a story, cite the highest tier available (see `monitoring_scope.md`, Sources).
- A Watch Out may re-cite the source of a story covered above; nothing else cites the same URL twice.

## Placement

- One article goes in its single best section. It may appear in two sections only with two genuinely distinct angles, never to fill a section.
- Product and model launches always go in AI & Innovation.
- A named bilateral agreement goes in Alliances and Partnerships. A G42-ecosystem entity as direct party, or regional policy with no specific deal, goes in Abu Dhabi & Gulf.
- Merge two articles in one bullet only when they are directly linked (same event, one drives the other, same conclusion) and keep the merged bullet inside the word count.
- Include every relevant story. There is no cap on bullets per section. Leave out only what is not relevant to AI or to Inception42.
- Follow-ups to a story already covered: a short factual update with no fresh analysis, referring precisely to the earlier edition ("yesterday's brief", "Monday's brief"), never "last week" by default.
- Roundup or year-in-review pieces may stay, framed explicitly as a recap with no added analysis.

## Tone and language

- Authoritative, opinionated, analytical. Every bullet states the implication for the AI sector, not just the event.
- US English throughout, applied silently: program, organization, license, defense, center, behavior, favor, percent, labor, analyze. The audit scans for British forms; the only exceptions are proper nouns and official names (Labour Party, Ministry of Defence), verbatim quotes, and URLs.
- No em dashes anywhere. Use commas or restructure. The audit fails on a single one.
- No "according to" attributions; no accusatory or negative framing; neutral, factual phrasing.
- No temporal markers ("today", "this week") unless accurate to the 09:00 GST distribution time; when unsure, drop them.
- Banned phrases (reframe genuinely, do not swap synonyms): "widening gap", "defining story", "defining tension", "consequential", "the sharpest story", "reached by design", "the question the industry is only now learning to ask", "governance, not raw model capability, is the story", "this is X not Y", "broke ground". Also the general AI tells: "delve", "navigate the complexities", "in today's rapidly evolving", "moreover", "it's worth noting", "this matters because", "crucial", "leverage", "underscores", "testament to".
- No AI-sounding tics: no "not X but Y" constructions, no rhetorical-question endings, no vague abstractions.
- Vary the Top Line's sentence structure from edition to edition; avoid geography-first openers and formulas like "The sharpest story today is".
- Monday edition covers Friday afternoon to Sunday. The Top Line signals a weekend recap with varied phrasing each week ("Over the weekend..." is preferred; never "Between Friday afternoon and Sunday night"). All elements may run slightly longer.
- Length check: count the Top Line and the Strategic Counter Narrative as a whole before delivering; sentence-by-sentence drafting drifts long.

## Inception42 rules

- Inception42 may be mentioned only in the Inception42 coverage bullets, Abu Dhabi & Gulf and the Strategic Counter Narrative. Never force an Inception42 angle into other sections. The audit enforces this.
- Always write "Inception42" (formerly Inception AI).
- Executive interviews or quotes (Ashish Koshy, Ibrahim Al Jallaf) always get a dedicated bullet, framed as "was featured in an interview" or "was quoted in", not leading with the quote.
- Inception42's own event participation is included when the editor supplies that detail in a note; the run never infers it.
- Partner nations or companies (Humain, Saudi Arabia) are described factually, never judged; pivot to the Abu Dhabi comparison instead.
- Unconfirmed stories about G42 or Inception42: note they are circulating in media without official confirmation and will be monitored; do not present the lack of confirmation as news. Keep confirmation levels distinct (a CEO's LinkedIn post is confirmed; a media report on talks is not).
- Inception42 is an OpenAI partner: OpenAI setbacks are never used as a selling point.
- Damaging or critical pieces about G42, its leadership, Inception42 or its executives stay out of the brief entirely and go to `sensitive_articles.md` in the package for the comms team to decide on.

## Strategic Counter Narrative

- Opens on one concrete, self-explanatory anchor fact (who, what, when in full) that deepens the Top Line thesis without restating it. Never opens with "Today's news".
- Moves from the global dynamic to the Gulf to Inception42. Must not rest only on Gulf stories.
- Never built around another G42 company (Core42, Presight); they may be mentioned, the focus stays on Inception42.
- The Inception42 sentence is one short, simple line tied to a concrete news item of the day. If no item genuinely links, drop it. No stock positioning line, no "Microsoft partner" or "part of the G42/MGX ecosystem" labels, no word "judged".
- When a major event is running (AI Everything, GITEX, ADIPEC), close with a sober, general, international sentence about it, without unverifiable claims or repeated figures.

## Watch Outs

- Max 2, each 1 to 2 sentences, hyper-specific, each with an inline source link.
- Written informationally with a conditional, forward-looking clause ("should X happen, Y is likely to..."), never as an imperative or "Watch whether...".
- Never reintroduce a prior Watch Out as new; if nothing changed, say so briefly and confirm monitoring.

## ElevenLabs audio script (script.txt)

Produced from the final validated brief, as oral prose of about 630 words in 3 to 5 threads ordered by importance.

- Opening: "Good morning and here's today's news for [weekday], the [ordinal] of [month] [year]." On Mondays, signal a weekend recap with varied phrasing.
- First paragraph: the Top Line, near-verbatim and in order.
- Strategic read: introduced with "The strategic read this morning is this." and followed directly by the closing line.
- Closing: "That's all for today, have a great day ahead!" No Watch Outs in the script.
- Transitions: the Gulf thread always opens with "Across the Gulf..." (never "Closer to home" or "Back in Abu Dhabi"); others vary ("Turning to...", "On the talent front...") and do not repeat on consecutive days.
- For text-to-speech: numbers and versions written in full ("one point three billion", "five point five"); acronyms that read badly expanded on first use (AWS, IRGC, NSA, IPO, AGI, G20); ADNOC written "Adnock", TAMM written "Tamm"; quotes introduced with "quote" / "unquote".
- No bullets, headers, markdown, links or em dashes. Paragraph breaks become one-second pauses in the audio.

## Quality control (what the run checks before packaging)

1. US English: every British spelling converted.
2. Links: each URL live and pointing to the exact article (article ID, section path and slug match the live page). No homepage, placeholder or Signal links.
3. Integrity: no duplicate citations, numbers consistent across sections, publication names correct, section placement logical, attributed claims accurate to the fetched text.
4. Freshness: publication date inside the monitoring window (Signal and aggregators resurface old pieces).
5. Length: Top Line and Strategic Counter Narrative word and sentence counts checked as a whole.

Nothing goes into the package unless every bullet rests on fetched article text. The written spec once allowed a bullet to be written "from general knowledge" when a fetch failed; this system does not. If an article cannot be read by fetch, by Tavily extract, or through a readable second source, the bullet is not written and the candidate is listed in the run log for the reviewer.
