# Editorial learnings

Running record of what reviewer edits to generated briefs changed, the
inferred rationale for each change, and the standing preferences derived
from them. Maintained by the run per Stage 1.2 of the morning-brief skill.
Standing preferences are applied while writing every edition and checked by
the Stage 3.5 adversarial review. Inferred rationales are labeled inferences,
not facts. Nothing in this file can relax the accuracy gates (no fabrication,
in-window only, verification, no reuse). You can edit this file directly;
your edits are authoritative.

## Standing preferences

1. **Inception42 coverage bullets sit above the Top Line with no heading.**
   The written spec confines Inception42 to Abu Dhabi & Gulf and the SCN;
   every October 2026 sent edition opens with mention bullets before the Top
   Line. The sent editions are the standard. (Seeded 28 Oct 2026 from the
   October editions.)
2. **A Watch Out may re-cite the source of a story covered in the body.**
   The spec says no duplicate citations; the sent editions consistently
   link the Watch Out to the same article as its body bullet. (Seeded 28 Oct
   2026 from the 26 and 28 October editions.)
3. **Several outlets on a big story, wire or Tier 1 first, separated by
   " / ".** Seen throughout October: Reuters / Bloomberg / CNBC on the
   Oracle chip story, BBC / Bloomberg / FT / Reuters on the UK biosecurity
   lab. (Seeded 28 Oct 2026.)
4. **"Since Thursday..." / "Over the weekend..." framing for continuing
   Inception42 coverage**, naming the outlets that have picked the story up
   since the last edition rather than re-reporting it. (Seeded 28 Oct 2026
   from the 26 October edition.)
5. **No bullet is ever written from general knowledge.** Replaces the
   written spec's fallback for failed fetches. An unreadable article is
   listed in the run log for the reviewer instead. (Set 28 Oct 2026 by Jack
   McLintock when the system was built.)

6. **An Inception42 mention is never dropped at the window edge.** A
   Signal "Inception mentions" hit published shortly before the window
   opens (the Scale AI Dubai piece, 19 minutes early on 27 October) goes
   into Inception42 coverage if the previous edition did not already cite
   that article. The window rule is for the general sweep, not for client
   coverage. (Set 28 Oct 2026 from the comparison of the generated 28
   October edition with the sent one, which carried the item.)
7. **Target length is about 1,500 words of body text (the audit warns over 1,750 or under 1,250).** The sent
   editions from 20 to 28 October run 1,367 to 1,659 words; the first
   generated edition ran 2,283. Hold Power, Regulation & Trust and AI &
   Innovation to three or four bullets each, Enterprise & Investment to
   five or six, and keep the Strategic Counter Narrative inside its range.
   Cut the fourth-ranked story before shortening the first-ranked one.
   (Set 28 Oct 2026 from the same comparison.)

8. **Tier 1 originals are read through Tavily at advanced depth and cited
   directly.** The sent editions cite Reuters, Bloomberg, FT, WSJ,
   Politico and The Verge as primary links; a brief that cites TimesLIVE
   or Investing.com where the client expects Reuters reads as second
   rate. Tavily at advanced depth with two retries reads most of these
   in full; when an original still cannot be read, the syndicated copy of
   the same wire text verifies it and the original stays the first link.
   (Set 29 Oct 2026 from the comparison of the generated and sent 29
   October editions: 6 of 32 links shared, mostly because the run cited
   readable copies where Kavya cited the originals.)
9. **The Emarat and G42 MoU rule: a G42 ecosystem agreement is covered
   when the Gulf press picks it up, even if the release came a day or two
   earlier.** The window rule is for the general sweep; G42 ecosystem,
   Inception42 and Abu Dhabi institutional items are covered the first
   time they appear in the sweep if no earlier edition carried them.
   (Set 29 Oct 2026: the run dropped the Emarat MoU as out of window; the
   sent edition led Abu Dhabi & Gulf with it.)
10. **A new in-window source with new detail on a story from the previous
   edition passes the reuse gate, and a new data point on a continuing
   story is a new story.** The reuse register bars re-citing the same
   link, not the subject. (Set 29 Oct 2026: the run dropped the GSA
   expansion and the GPT-6.1 Terra pricing as already covered; the sent
   edition carried both with new sources and new facts.)
11. **Follow-ups from Tier 1 outlets and overnight Reuters, Bloomberg,
   WSJ and FT items are decoded and read by default.** Six of the
   sixteen misses on 29 October were Tier 1 pieces published after
   midnight UTC that the sweep listed but the desks never opened. Decode
   every Reuters, Bloomberg, WSJ and FT item in the window from the
   sweep, and read them through Tavily advanced.

## Observations

### 2026-10-28 (seeding)
- The written spec lists justine.judge@inceptionai.ai as a recipient; the
  28 October send went to alan.griffin, newton.rebello, sean.phelps,
  swetha.ramesh, dya.mrini and daniel.bestwick, cc Inception@ and the
  Digital Farm address. Config follows the send. Inferred rationale:
  structure (recipient list maintained by the team outside the spec).

### 2026-10-28 (generated edition compared with the sent edition)
- Same core: 13 of the sent edition's 28 links appear in the generated
  one, including every Top Line story bar the China profits item, the
  Oracle Watch Out, and the same Trump, Netherlands, Altman, Home Office,
  Infineon, Genie 4, Oracle-OpenAI, Apple M6 and Nvidia-Meta bullets.
- Missed: the Scale AI Dubai item (Inception42 coverage; dropped as 19
  minutes before the window, now learning 6), Beijing's Xiong'an Vision
  (SCMP refused the fetch and the document dated 25 October), Anthropic's
  training delay over weight theft (S-1 detail not surfaced by the sweep),
  China industrial profits and the STAR50 fall (the register showed STAR50
  cited on 26 October), and Kavya's second Watch Out on Anthropic's share
  count.
- Added beyond the sent edition: Alibaba's Pentagon injunction, AI
  election spending, RBC blocking agents, the Apple v OpenAI discovery
  order, Meta's $25 billion share sale, Physical Intelligence's raise,
  Liquid AI LFM3, Anthropic's drug results, the GSA OneGov expansion, and
  a four-bullet Abu Dhabi & Gulf section (Apollo, Blackstone, M42, PDO).
  The sent edition had no Gulf section that day and folded Scale AI into
  the SCN instead; the house format keeps the section.
- Length: 2,283 words against 1,514. Now learning 7.

### 2026-10-29 (first scheduled run compared with the sent edition)
- Length: 1,603 words against about 1,650 for the sent edition; both at
  target. Section counts within one bullet of each other except Alliances
  (1 against 2) and Abu Dhabi & Gulf (4 against 6).
- Same core: Microsoft results and the OpenAI revenue line, Alphabet's
  fall, the New York chatbot law, the DOJ and Nvidia-Hugging Face, the
  UK AISI funding, Gemini 4 Carbon, Nemotron Transcribe, Anthropic's
  reporting tools, M42 trials, the Dubai AI sandbox. Both Top Lines took
  the same thesis: investors sorting AI spenders by cash generation.
- Missed by the run: OpenAI buying Google TPUs (Bloomberg follow-up),
  DeepSeek and Moonshot distillation (Reuters), the FT cryptography piece,
  OpenAI's election operations center (Politico), the Reuters "cash is
  king" piece, Google AI Mode ads (TechCrunch), the Nscale IPO (Bloomberg),
  GPT-6.1 Terra pricing (Axios), the Oracle-OpenAI expansion (WSJ), the
  Emarat-G42 MoU (dropped on the window rule), Data Center World Abu Dhabi
  (Zawya), Scale AI's Doha office (Middle East AI News) and the UAE
  delegation to Vietnam.
- Added by the run and absent from the sent edition: China's draft AI
  export curbs, the Malaysia chip seizure, the PHP flaw exploitation, the
  Oracle investor day follow-up, the bond record and Texas data center
  loan delay, Anthropic's 85 percent gross margin, the Shield AI MoU in
  Qatar, Terrestar and Space42, and the S&P data center build costs.
- Links: 6 of the sent edition's 32 shared. Most of the difference is
  outlet choice for the same story (the run cited CNBC, TechCrunch, The
  National and syndicated copies where the sent edition cited Bloomberg,
  Reuters, WSJ and FT). Now learnings 8 and 9.
- Alliances ran one bullet because the run excluded the GSA deal as
  already cited on 28 October; the sent edition carried it with the
  Anthropic release as the source. A new source on a continuing story is
  allowed under the reuse gate; the run was too strict.

### 2026-10-29 (benchmark, generated against sent)
- Verdict behind: 11 of 27 sent stories carried (41 percent), 11 extras
  of which five are stories the sent edition should have had, Tier 1 and
  2 share 72 against 76 percent, 1,567 words against 1,910.
- Misses by cause: 6 not found (Tier 1 overnight items not opened, one
  WAM syndication), 3 unreadable (Politico and Bloomberg candidates not
  sent to Tavily), 4 rule-dropped (window, reuse, continuing story), 3
  not selected (AI Mode ads, Data Center World, Scale AI Doha), 2 Watch
  Out judgment calls.
- Fixes: learnings 9, 10 and 11; Tavily at advanced depth with retries;
  sweep topics for frontier and China labs and for UAE government
  delegations.
