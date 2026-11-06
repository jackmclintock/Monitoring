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
   Recurred 4 Nov 2026: Semafor's report on OpenAI rolling out its
   "compute campuses" push to a skeptical Congress was set aside as
   "covered in 2 Nov sent edition"; the 2 November edition carried the
   plan, and the rollout and the congressional reception are new facts.
   The sent edition ran it in Power.
   Recurred 5 Nov 2026: Meta's debut euro bond (EUR 9 billion, a record
   EUR 53 billion of orders) was held as a "minor follow-up to the 4 Nov
   sent Meta bond bullet"; the sent edition ran it in Enterprise &
   Investment. A record figure on a continuing story is a new story, not
   a minor follow-up.
11. **Follow-ups from Tier 1 outlets and overnight Reuters, Bloomberg,
   WSJ and FT items are decoded and read by default.** Six of the
   sixteen misses on 29 October were Tier 1 pieces published after
   midnight UTC that the sweep listed but the desks never opened. Decode
   every Reuters, Bloomberg, WSJ and FT item in the window from the
   sweep, and read them through Tavily advanced.

12. **The reuse gate reads the sent edition only.** A story that ran in a
   generated edition but not in the edition the team sent was never shown
   to the client and is not "covered". Check reuse against `brief.md`
   with `source: reviewer-final` and the rebuilt register, never against
   `brief_generated.md` or the previous run's candidates. (Set 30 Oct
   2026: the run dropped Space42, Viasat and Terrestar as "covered in the
   29 October generated edition"; the sent 29 October edition did not
   carry it and the sent 30 October edition did. Second day of an
   over-strict reuse reading after the GSA and Terra drops on 29 October.)
   Recurred 3 Nov 2026: South Korea's 2027 AI budget was dropped as
   "appeared Monday" when only the 2 November generated edition had
   carried it; the sent 2 November edition did not, and the sent 3
   November edition ran it. A reuse drop in `candidates.md` must name the
   sent edition date and the register entry it matched; "appeared" with
   no sent-edition citation is not a valid disposition.
13. **Gulf press items at the window edge are eligible.** A piece from The
   National, Gulf News, Khaleej Times, ZAWYA or WAM dated the day before
   the window opens goes into consideration if no sent edition carried
   it; the 24-hour window stays strict for the general sweep. This widens
   learning 9 beyond the G42 ecosystem. (Set 30 Oct 2026: the sent edition
   carried The National's 28 October Ellison piece; third day running a
   Gulf-press item was lost at the window edge, after Scale AI Dubai on 28
   October and the Emarat MoU on 29 October.)
14. **Abu Dhabi & Gulf runs four or five bullets and is cut last.** Signed
   op-eds by UAE officials or institution heads on UAE AI policy count as
   news for this section, and a Gulf item is never dropped "for length"
   while Enterprise & Investment carries more than four bullets. (Set 30
   Oct 2026: the run left out the Al Shamsi and Al Hammadi algo-diplomacy
   op-ed as "opinion" while running six Enterprise & Investment bullets;
   on 29 October it ranked out Data Center World and Scale AI Doha.)
   Extended 6 Nov 2026: an event close-out (ADIPEC, GITEX, Ai Everything)
   that names a G42 ecosystem or Inception42 agreement as a leading deal
   is an Abu Dhabi & Gulf bullet, not SCN material only. The run read The
   National's ADIPEC wrap and used it only in the SCN; the sent edition
   ran the $67 billion close, with ADNOC, OpenAI, G42 and Inception42 as
   the leading agreement, as a Gulf bullet and in the Top Line.

15. **A Monday edition covers the weekend: Friday 06:45 to Monday 06:45
   GST.** Friday and Saturday developments that the Friday sent edition did
   not carry are in window for Monday, and the weekend-recap conventions
   apply ("Over the weekend..."). Until the window default changes, create
   the Friday-to-Monday recap entry in the dashboard planner (the
   mechanism Stage 1 already supports); if no entry exists, treat Friday
   and Saturday items not in the Friday sent edition as eligible and log
   that basis. (Set 2 Nov 2026: the Sunday-only window kept out 11 of the
   21 stories the sent Monday edition carried, among them the OpenAI round
   cut, the MGX anchor, the $900 billion Big Tech loss and the Blackstone
   rating, several of them listed in candidates as out of window. The
   window gate has now removed sent stories on four editions: Scale AI
   Dubai on 28 October, the Emarat MoU on 29 October, the Ellison piece on
   30 October and the weekend on 2 November. The 26 October sent Monday
   edition also used weekend framing, see learning 4.)
16. **A failed read of a WAM or Reuters item triggers a copy search
   before the item is marked unverifiable.** Search the headline facts
   for a syndicated or same-facts copy (ZAWYA, Gulf Business, Gulf News,
   The National or Khaleej Times for WAM; CNBC, Bloomberg, Investing.com,
   a regional Reuters copy or the company's own release for Reuters), read
   it, and cite the original first per learning 8. "Unverifiable, not
   used" is only valid once that search has failed, and the run log names
   what was tried. (Set 3 Nov 2026: Palantir's results (Reuters) and the
   DIFC AI adoption item (WAM) were marked unverifiable after three Tavily
   failures; the sent edition carried both, the DIFC item cited to ZAWYA.
   Same failure on 2 November with the ADIPEC opening, where Gulf Business
   carried the WAM facts and was not tried.)
   Extended 4 Nov 2026 to FT, Bloomberg and WSJ paywalls and to earnings
   stories: Apple's margin guidance (FT paywall; only a headline-only
   Forbes Middle East copy tried) and AMD's $1.07 billion warrant charge
   (Reuters, three failures) were dropped though both earnings were
   reported widely by CNBC, Bloomberg and the companies' own releases and
   calls. For an earnings or filing story, the company release or
   transcript and a CNBC or Bloomberg copy are the first copies to try.
17. **One story per bullet: distinct companies' news gets its own
   bullet.** The sent editions merge outlets on one story (learning 3) but
   do not fold two companies' announcements into one bullet. Oracle's
   raise and Alphabet's euro bond are two bullets; Grok's limits and the
   ChatGPT tab merge are two bullets. When length is tight, cut the
   lowest-ranked story rather than merging. (Set 3 Nov 2026 from two
   merged bullets that the sent edition split; also seen 30 October with
   Cohere's Series E folded into a Power bullet.)
   Extended 5 Nov 2026 to holding a story because another bullet "already
   carried the angle": OpenAI's Chris Lehane essay on the 2028 election
   was held because Power carried the congressional result; it is a
   different actor's news and the sent edition ran it as its own bullet.
18. **Yesterday's generated-but-not-sent stories are carried forward as
   candidates.** The reviewer sometimes holds a generated story for a day
   and runs it in the next sent edition. Before ranking, list every story
   in the previous `brief_generated.md` that the previous sent edition did
   not carry, and consider each one again today regardless of the window
   or the reuse register; it was never shown to the client. (Set 4 Nov
   2026: Goldman restricting coding tools ran in the 3 November generated
   edition, not the 3 November sent one, and led an Enterprise &
   Investment sub-bullet in the 4 November sent edition; today's run never
   saw it because it was dated 2 November. Same pattern on 30 October
   with Space42 and Terrestar and on 3 November with the South Korea
   budget, both lost to the reuse gate; see learning 12.)
19. **UAE government and AI Office programs outrank Gulf deal talks in
   Abu Dhabi & Gulf.** A UAE AI Office, ministry or federal program item
   (hackathons, award categories, skills programs, governance
   initiatives) carried by ZAWYA, WAM or The National is selected ahead of
   regional business items that are only at the talks stage, even when
   the underlying event was a few days earlier and a newer write-up of it
   appears in the window. (Set 4 Nov 2026: the UAE AI Office and Emirates
   NBD UAE Codes hackathon was set aside as "undated release on a 29
   October event" while the section ran the EQT talks and the Salalah
   data park talks; the sent edition carried it with a new ZAWYA story.
   Same class on 2 November with the Dubai Chambers Agentic AI award,
   cut for length behind Gulf business announcements.)
20. **Named-figure statements on AI risk and policy are news.** An
   interview, essay or speech in which a recognized figure (a Big Tech
   founder, a lab or platform CEO, a lab's policy chief, a head of state
   or faith leader) sets out a position on AI safety, regulation or the
   AI economy is a candidate for Power or Regulation & Trust, ranked
   with hard news, not set aside as "opinion" or "analysis". Read FT,
   WIRED, Semafor and TechCrunch interviews and essays in the window as
   candidates. (Set 5 Nov 2026: the sent edition carried Bill Gates on
   AI self-regulation (FT), Clément Delangue on open models and risk
   (WIRED) and Chris Lehane's 2028 essay (TechCrunch); the run never
   found the first two and held the third. Same class on 30 October with
   Ellison on universal income (The National) and the UAE algo-diplomacy
   op-ed, and on 2 November with Pope Leo XIV on AI institutions.)
   Extended 6 Nov 2026 to lab executives on the AI economy: Greg
   Brockman on OpenAI's 2027 IPO readiness and enterprise revenue
   (TechCrunch) was listed and not opened while the run carried
   Anthropic's IPO; when one frontier lab's listing is covered, a rival
   lab executive's statement on its own listing or revenue is opened and
   ranked as news.
21. **A length cut never takes a frontier-lab launch from a thin section.**
   When the draft runs long, cut first from the section with the most
   bullets (usually Enterprise & Investment at six) and the weakest
   sourced items (a single short report, an undated release), never a
   Reuters or Tier 1 reported launch by OpenAI, Anthropic, Google or Meta
   from a section left at two bullets. Learning 14 still protects the
   Gulf floor of four bullets, but a fifth Gulf bullet from a press
   release is cut before a lab launch. (Set 6 Nov 2026: Claude Personal
   Finance (TechCrunch, Reuters) was written and cut for length, leaving
   AI & Innovation at two bullets while Enterprise & Investment ran six;
   the sent edition carried it. Same class on 5 November with Google's
   $15 billion Malaysia investment cut while thin partnership items
   stayed, and on 2 November with the Dubai Chambers award.)

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

### 2026-10-30 (benchmark, generated against sent)
- Verdict behind: 10 of 19 sent stories carried by the matcher (53
  percent). Two of the nine misses are the same stories told differently
  (the Alphabet selloff, cited to CNBC and a different WSJ piece, and the
  Cohere Series E, merged into the Power Cohere bullet), so substantive
  coverage is 12 of 19 (63 percent). Tier 1 and 2 share 71 against 69
  percent; 1,483 words against 1,445; 10 of 26 sent links shared.
- Misses by cause:
  - not-found (3): Pew survey on AI in medical and coverage decisions
    (Bloomberg); Alphabet 10-Q, $98.5 billion contingent commitments and
    agents acting outside intended scope (Bloomberg), which also carried
    a Watch Out and the sent SCN opening. Neither was in candidates.
  - rule-dropped (2): Space42, Viasat and Terrestar (reuse gate read the
    29 October generated edition, which the client never saw; the gate
    reading was wrong, now learning 12); Ellison on universal income (The
    National, URL dated 28 October; not in candidates, most likely removed
    by the window filter; now learning 13).
  - not-selected (1): UAE-US algo-diplomacy op-ed (The National), set
    aside as opinion; now learning 14.
  - judgment (3): Alphabet selloff (covered, matcher missed it on links;
    outlet-choice gap: the sent edition added FT and Semafor); Cohere
    Series E (covered inside the Power bullet; the sent edition split it
    and added the 165 percent ARR figure); Cohere C$7 billion Watch Out.
- Extras: better (2): Amazon cash burn and capex (Reuters), Microsoft's
  first bond sale since 2017 (Bloomberg). Fine (11): AI industry and the
  midterms, Iluvatar CoreX, Accenture agent on a DOD network, Alphabet
  selloff (same story as the sent one), AI credit limits and HSBC,
  ServiceNow, Samsung, Nvidia in Meta's offering, GCC AI Strategy, data
  center ballot Watch Out, GDP Watch Out. Weaker (1): Google winding down
  Jules.
- Outlet choice: Orange Cyberdefense cited to Techzine where the sent
  edition cited Reuters (Reuters unreadable after three Tavily tries);
  Huang story led on the NYT where the sent edition used Semafor and
  TechCrunch.
- Fixes: sweep topics "Public opinion and surveys" and "Big Tech filings
  and disclosures" added to `config/sweep_queries.json`; standing
  preferences 12 (reuse gate reads the sent edition), 13 (Gulf press at
  the window edge) and 14 (Abu Dhabi & Gulf cut last, UAE op-eds count).

### 2026-11-02 (benchmark, generated against sent)
- Two sends: "Daily Media Monitoring 2nd November" at 08:59 GST and
  "Updated Daily Media Monitoring Report 2nd November" at 09:38 GST, both
  to the full client list. The updated edition is the record of the day
  and is now `brief.md`: it adds an Inception42 note above the Top Line,
  two Abu Dhabi & Gulf bullets on the OpenAI agreements (Inception42
  five-year partnership; ADNOC, Inception42 and OpenAI) from the Abu Dhabi
  Media Office, a revised Top Line close and a revised SCN.
- Verdict behind: 4 of 25 sent stories carried by the matcher (16
  percent). Counting the Altman and Samsung meeting, carried in the
  generated Alliances section, substantive coverage is 5 of 25 (20
  percent). Tier 1 and 2 share 42 against 62 percent; 1,502 words
  against 1,732; 3 of 37 sent links shared.
- Misses by cause:
  - rule-dropped, window (11): Anthropic as SpaceX's largest customer
    (Semafor, 30 Oct); Washington Post on the slowdown pledge not
    holding (29 Oct); Pope Leo XIV on AI institutions (Washington Post,
    30 Oct); the IETF training opt-out (The Verge; candidate SEJ marked
    out of window); xAI must face the NAACP suit (TechCrunch, 31 Oct;
    candidate Engadget dropped on date); the $900 billion Big Tech loss
    (FT, Semafor, 30 Oct); OpenAI's round cut to $20 billion (FT; listed
    as out of window); Blackstone's junk-rating expectation for
    Anthropic (FT, TechCrunch, 30 Oct) and its Watch Out; Apple
    Intelligence in China on Alibaba models (SCMP, TechCrunch, 31 Oct;
    flagged in the run log); the MGX-led UAE consortium in OpenAI's
    round (FT, CNBC). The gate worked as written; the written rule is
    wrong for Mondays. Now learning 15.
  - not-found (5): the Abu Dhabi Media Office release on Sheikh Khaled
    meeting Sam Altman and the four OpenAI agreements, carried as the
    Inception42 note and two Gulf bullets (published after the 06:45
    run; the reviewer's own first send at 08:59 did not have it either);
    the Binance theft attributed to North Korea (Semafor and TechCrunch,
    1 Nov, in window; the AI keyword filter likely cut it); Murata's
    $6.3 billion capacitor investment (Nikkei Asia, which the sweep did
    not cover at all).
  - unreadable (2): the White House testing framework refusal (The
    Information; paywalled headline only); ADIPEC opening (WAM failed
    three times; Gulf Business carried the same facts and was not tried,
    so learning 8's syndicated-copy path was not applied).
  - not-selected (1): the Dubai Chambers Agentic AI award category
    (ZAWYA, read, cut for length while Abu Dhabi & Gulf ran RTA, Nad
    Zabeel and the Mumtalakat bank). The sent edition used it in the SCN;
    inferred rationale: UAE items on AI governance and oversight carry
    the SCN and rank above Gulf business announcements.
  - judgment (2): memory makers out-earning Big Tech plus Altman's
    Samsung meeting (the generated Alliances bullet carried the Altman
    meetings from Seoul Economic Daily and Tom's Hardware; outlet-choice
    gap against Nikkei Asia and Bloomberg); the midterm data center
    Watch Out (the generated edition carried the same TechCrunch story in
    Power and chose a Prop 45 Watch Out).
- Extras: better (1): South Korea's record 2027 budget nearly doubling
  AI and chip spending (Straits Times, Bloomberg). Fine (14): Trump on
  Huang; the Australian public-service AI deadlock; Suleyman on AI
  consciousness; California Prop 45; record Taiwan outflows (the same
  selloff from a Sunday angle); Nvidia, AMD and Broadcom in Meta's sale;
  SK Hynix shelving the Solidigm listing; Anthropic's internal Claude use;
  Altman's SK and Samsung meetings; the ENACT Majlis; Nad Zabeel; the RTA
  AI strategy; both Watch Outs (Prop 45, the Korea budget). Weaker (3):
  SemiAnalysis GDPx; HD Hyundai Robotics and Palantir (single weak
  source); the Mumtalakat and ARP AI bank.
- Fixes: standing preference 15 (Monday window covers the weekend);
  sweep queries added to `config/sweep_queries.json`: outlet "Nikkei
  Asia", regional "Abu Dhabi Media Office", topic "Cyber incidents and AI
  security". No fix for the after-run release beyond the new query.

### 2026-11-03 (benchmark, generated against sent)
- Sent by Kavya Sreeram at 09:00 GST, "Daily Media Monitoring 3rd
  November", to the full client list. It opens with an Inception42 note
  (1,107 mentions of the OpenAI agreements, Tier 1 and regional pickup)
  in place of mention bullets, and runs no Alliances section.
- Verdict behind: 9 of 19 sent stories carried by the matcher (47
  percent). Three of the ten misses are the same stories in the generated
  edition (Anthropic's Q3 financials, the Alphabet euro bond inside the
  Oracle bullet, the ChatGPT Chat and Work merge inside the Grok bullet),
  so substantive coverage is 12 of 19 (63 percent). Tier 1 and 2 share
  71 against 75 percent; 1,511 words against 1,440; 14 of 36 sent links
  shared.
- Misses by cause:
  - rule-dropped (1): South Korea's record 2027 AI and chip budget
    (Straits Times, CNBC). The reuse gate read the 2 November generated
    edition, not the sent one; the gate reading was wrong (learning 12,
    second recurrence; amended).
  - unreadable (2): Palantir's Q3 results (Reuters failed three times, no
    copy tried); Emirates NBD and DIFC AI adoption (WAM failed; the sent
    edition cited ZAWYA). Now learning 16.
  - not-selected (1): the Nasdaq 100 correction (Bloomberg), read and used
    in the Top Line only; the sent edition put it first in Enterprise &
    Investment. Inferred rationale: a market move that carries the Top
    Line also earns a body bullet with the index figures.
  - not-found (1): HSBC's Hong Kong AI institute and the HKMA's Project
    SAGE know-your-agent guardrails (Reuters, ZAWYA); not in candidates
    and no sweep digest kept. Fix: sweep topic "Banks and financial
    regulators on AI".
  - judgment (5): Anthropic Q3 financials (covered; outlet-choice gap,
    the sent edition cited FT and Axios where the run cited Reuters,
    Bloomberg and CNBC, the FT read returned a paywall page); the Alphabet
    euro bond and the ChatGPT tab merge (covered inside merged bullets;
    now learning 17); the Anthropic listing Watch Out (generated Watch Out
    on the same listing, valuation angle); the US election Watch Out
    (generated Watch Out on the same vote, data center ballot angle).
- Extras: better (0). Fine (16): Koshy in TokenPost on Alpha; Putin's
  foreign data center decree; Merz on digital sovereignty; data center
  ballots and OpenAI Grid Protectors; publishers v Brave; Anthropic Q3
  financials (same story as a sent one); DRAM prices doubling; Goldman
  restricting coding tools; MIT editing Qwen weights with GPT-6 Astra;
  the Brookfield, KB and Naver GPU loan; Tencent Cloud in Riyadh; Altman
  at ADIPEC; Al Olama on consolidation and data center standards; the
  Annual Government Challenge; both Watch Outs (ballots, valuation).
  Weaker (0).
- Fixes: sweep topics "Banks and financial regulators on AI" and "AI
  earnings" added to `config/sweep_queries.json`; learning 12 amended
  (reuse drops must cite the sent edition); standing preferences 16
  (copy search before "unverifiable", second day) and 17 (one story per
  bullet, second day).

### 2026-11-04 (benchmark, generated against sent)
- Sent by Kavya Sreeram at 09:00 GST, "Daily Media Monitoring 4th
  November", to the full client list. It opens with an Inception42 note
  (1,250+ mentions of the OpenAI agreements, Forbes analysis of the ADNOC
  deal, the CNN Business Arabic interview with Ashish Koshy), runs no
  Alliances section and three Abu Dhabi & Gulf bullets.
- Verdict behind: 7 of 18 sent stories carried by the matcher (39
  percent). HUMAIN and CNTXT is the same story in the generated edition
  (Middle East AI News where the sent edition cited the ZAWYA release),
  so substantive coverage is 8 of 18 (44 percent). Tier 1 and 2 share 76
  against 67 percent; 1,734 words against 1,417 (benchmark count); 6 of
  24 sent links shared.
- Misses by cause:
  - not-found (5): the Inception42 note (Forbes ADNOC analysis, CNN
    Business Arabic; the mention count comes from the team's monitoring
    tool, not the sweep); the Koshy CNN Business Arabic interview in Abu
    Dhabi & Gulf (Arabic-language, no Arabic mention query); Canva
    restructuring 22% of staff (Bloomberg); Revolut moving engineers to
    Z.ai's GLM (Dealroom News). None in candidates. Fix: sweep queries.
  - rule-dropped (2): OpenAI's compute campuses rollout (Semafor), reuse
    gate read as "covered 2 Nov" though the rollout and Congress's
    reception are new (learning 10, amended); Goldman restricting coding
    tools (Bloomberg, 2 Nov), out of window today after the 3 November
    generated edition carried it and the sent one did not (learning 18).
  - unreadable (2): Apple's margin guidance on memory prices (FT paywall,
    headline-only copy); the AMD warrant charge Watch Out (Reuters failed
    three times; the generated AMD bullet lacks the $1.07 billion charge).
    Learning 16 extended to paywalls and earnings stories.
  - not-selected (1): UAE AI Office and Emirates NBD UAE Codes hackathon
    (ZAWYA), read and set aside as an undated release on a 29 October
    event. Now learning 19.
  - judgment (2): HUMAIN and CNTXT (covered; outlet choice); the Nvidia
    51% Watch Out (the generated edition carried the story in Power and
    chose Texas and EU court Watch Outs).
- Outlet choice: Meta's bond cited at the marketing stage ($20 to $25
  billion sought) where the sent edition had the priced $15 billion and
  $58 billion of orders from Reuters (Reuters unreadable); Google schools
  cited to The Verge where the sent edition used TechCrunch, The
  Washington Post and The Straits Times.
- Extras: better (2): Apple's 10-K warning on AI agents (CNBC); the EU
  advocate general on Gemini and press copyright (Reuters, WSJ). Fine
  (14): Muscat Journal and Gulf News Inception42 mentions; NCSC 2028
  warning; Florida and Texas results; Binance post-mortem; Apollo
  originations; Fal's $16 billion round; Siri opening to apps; Brookfield,
  QIA and Drax; ADNOC's 200 AI applications; Altman and Al Jaber at
  ADIPEC; EQT Gulf talks; HUMAIN and CNTXT (same story as a sent one);
  both Watch Outs (Texas permitting, EU court ruling). Weaker (2): Samsung
  Taylor memory for AMD and Nvidia (one short Verge post on a Korean
  report); the Salalah AI data park talks (Oman Observer).
- Fixes: sweep queries added to `config/sweep_queries.json`: outlet
  "Dealroom News", regional "CNN Business Arabic", mention "Inception42
  (Arabic)", topics "AI workforce restructuring", "Enterprise model
  switching" and "ADNOC and Abu Dhabi OpenAI agreements pickup".
  Learning 10 amended (third reuse over-reading of a continuing story);
  learning 16 extended (paywalls and earnings, fourth day of unreadable
  Tier 1 items without a real copy search); standing preferences 18
  (carry forward generated-not-sent stories, third day of the pattern)
  and 19 (UAE government items outrank Gulf deal talks, second day).

### 2026-11-05 (benchmark, generated against sent)
- Sent by Kavya Sreeram at 09:00 GST, "Daily Media Monitoring 5th
  November", to the full client list. It opens with an Inception42 note
  (1,950+ mentions of the OpenAI agreements, Koshy's AGBI interview),
  runs no Alliances section and two Abu Dhabi & Gulf bullets.
- Verdict behind: 11 of 23 sent stories carried by the matcher (48
  percent). The Koshy AGBI bullet is in the generated Abu Dhabi & Gulf
  section with the same link (the matcher paired that link with the
  sent Inception42 note), and the Democratic committees story is the
  generated Power bullet on the same result (Politico, WSJ against The
  National, Bloomberg), so substantive coverage is 13 of 23 (57 percent).
  Tier 1 and 2 share 67 against 75 percent; 1,648 words against 1,647;
  15 of 36 sent links shared.
- Misses by cause:
  - not-found (5): Bill Gates on AI self-regulation and bioweapons (FT);
    Clément Delangue on open models and catastrophe risk (WIRED);
    Accenture correcting a report after GPTZero found 15 false citations
    (FT); hackers raising refrigeration temperatures at European
    supermarkets and French blood banks (Semafor, no AI keyword, so the
    cyber topic missed it); UK consumer AI subscriptions passing GBP 1
    billion with Claude's share quadrupling (Bloomberg, 5 Nov). None in
    candidates and no sweep digest kept. Fix: sweep topics; standing
    preference 20.
  - not-selected (3): Chris Lehane's 2028 election essay (TechCrunch),
    held because Power carried the congressional angle (learning 17
    extended); Meta's EUR 9 billion euro bond, held as a minor follow-up
    (learning 10, recurrence); Google's $15 billion Malaysia investment
    (Bloomberg), cut for length while Alliances ran a reported AP deal
    from a short Verge post and a Korea and AMD steering meeting.
    Inferred rationale: a hyperscaler's country-scale capex commitment
    outranks thin partnership items, and the sent edition used it in the
    SCN to frame the UAE.
  - judgment (4): the Democratic committees bullet (covered; outlet
    choice); the Koshy AGBI Gulf bullet (covered, matcher artifact); the
    Meta Brazil Watch Out and the Senate ratepayer bill Watch Out (the
    generated edition carried Brazil in the body and chose Pentagon task
    force and Texas approvals Watch Outs). The National's Democrats
    piece was read and held as analysis; the sent edition used it for
    both the Power bullet and a Watch Out.
- Outlet choice: data center ballots led on CNBC where the sent edition
  led on Semafor, The Washington Post, WSJ and ZAWYA; Meta in Brazil led
  on The Straits Times AFP copy where the sent edition cited Semafor;
  UAE Codes cited to the ZAWYA press release where the sent edition used
  the ZAWYA special coverage story.
- Extras: better (1): the Pentagon CTO on publishing the laws that
  apply to US AI labs within two weeks (Reuters, Straits Times copy).
  Fine (11): the Koshy ADIPEC panel; the Democratic sweep (same story as
  a sent one); Nvidia China RTX orders at 1%; the Big Tech rally and
  data center stock falls; Texas governor-elect's approvals ban; Google
  buyouts; midterms and Gulf chip access (AGBI, Semafor); AIQ in India;
  Terra Invest and AIREV; both Watch Outs (Pentagon task force, Texas).
  Weaker (2): Anthropic and AP licensing (single short report citing
  Adweek); the Korea science ministry and AMD steering meeting.
- Fixes: sweep topics added to `config/sweep_queries.json`: "AI safety
  and risk voices", "AI company policy agendas and essays", "AI errors
  in professional work", "Consumer AI spending and market share",
  "Infrastructure and operational cyberattacks". Learning 10 amended
  (record follow-up held as minor, fourth recurrence); learning 17
  extended (holding a different actor's story under a related bullet);
  standing preference 20 (named-figure statements on AI risk and policy
  are news, third day of the class).

### 2026-11-06 (benchmark, generated against sent)
- Sent by Kavya Sreeram at 09:00 GST, "Daily Media Monitoring 6th
  November", to the full client list. No Inception42 coverage bullets and
  no Alliances section; a short edition (1,145 words by the benchmark
  count) that names Inception42 in the Top Line and in an Abu Dhabi &
  Gulf bullet as well as the SCN.
- Verdict behind: 7 of 14 sent stories carried by the matcher (50
  percent). The Oliver Wyman UAE survey is in the generated Abu Dhabi &
  Gulf section (The National and Zawya where the sent edition cited
  Khaleej Times), so substantive coverage is 8 of 14 (57 percent). Tier 1
  and 2 share 76 against 83 percent; 1,621 words against 1,145; 7 of 23
  sent links shared.
- Misses by cause:
  - not-found (2): Blue Owl expecting higher AI lending returns as
    supply tightens (Bloomberg); new detail on the SpaceX chip financing
    ($8.3 billion Goldman-led debt, $7 billion lease prepayment, no
    residual value guarantee; Bloomberg). Neither in candidates. Fix:
    sweep topic "AI infrastructure credit and lenders".
  - not-selected (3): Claude Personal Finance (TechCrunch), written and
    cut for length while Enterprise & Investment ran six bullets and AI &
    Innovation was left at two (now standing preference 21, third day of
    the class); Brockman on OpenAI's 2027 IPO readiness (TechCrunch),
    listed and not opened (learning 20 extended); the ADIPEC close with
    $67 billion of deals and ADNOC, OpenAI, G42 and Inception42 as the
    leading agreement, read from The National and used in the SCN only
    (learning 14 extended). The sent edition cited CNN Business Arabic,
    whose sweep query returned nothing; the query now also matches
    "أديبك" and "أدنوك", and a topic "Event close-out tallies" is added.
  - judgment (2): the Oliver Wyman survey (covered, matcher artifact,
    outlet choice); the Nscale listing Watch Out (the generated edition
    carried Microsoft and Nscale in the body and chose the Anthropic
    roadshow Watch Out).
- Outlet choice: the Huang briefing led on CNBC where the sent edition
  cited Axios and Reuters (Reuters failed in Tavily, learning 16); the
  Nasdaq rout cited Reuters and WSJ where the sent edition used The
  Straits Times, FT and Reuters; the generated edition led on a 5.5%
  Nasdaq fall where the sent edition led on the Nasdaq 100 at 6.4%.
- Extras: better (1): governors-elect in states with about 40% of
  planned US capacity pledging pauses (Bloomberg), the sharpest
  statement of the political risk the sent Top Line priced. Fine (13): the Koshy ADIPEC quote
  (Zawya, carried forward under learning 18); Sanders and Ansari on a
  moratorium; the Gemini school lawsuit; the federal refrigeration
  warning; Meta delaying its business terms; the Asian chip selloff;
  Anthropic's IPO valuation pushback; China blocking SoftBank and ABB;
  Google's $17 billion Wyoming site; METR on Anthropic's capability pace;
  Presight and Quartermaster; the Oliver Wyman survey (same story as a
  sent one); the Anthropic roadshow Watch Out. Weaker (3): the Mistral,
  G42 and Inception42 talks (single paywalled newsletter, unconfirmed,
  client item the reviewer left out); AIQ Genesis and tNavigator
  (undated release); the Dubai RTA traffic signals.
- Fixes: sweep topics "AI infrastructure credit and lenders" and "Event
  close-out tallies" added to `config/sweep_queries.json`, and the CNN
  Business Arabic query widened. Learning 14 extended (event close-outs
  naming a G42 ecosystem deal are Gulf bullets); learning 20 extended
  (lab executives on listings and revenue); standing preference 21
  (length cuts never take a frontier-lab launch from a thin section,
  third day of the class).
