---
name: tavily-extract
description: |
  Extract clean markdown or text content from specific URLs via the Tavily CLI. Use this skill when one or more URLs need their content retrieved, especially bot-walled or JavaScript-rendered news pages that plain WebFetch cannot read. Handles JavaScript-rendered pages, returns LLM-optimized markdown, and supports query-focused chunking for targeted extraction. Can process up to 20 URLs in a single call. In this repository it is the reader path for the morning-brief skill's Stage 2 Phase B: one batched, basic-depth extraction of already-selected articles only.
allowed-tools: Bash(tvly *)
---

# tavily extract

Extract clean markdown or text content from one or more URLs.

Vendored from the official Tavily skills repository
(https://github.com/tavily-ai/skills, MIT license), adapted for unattended
runs: authentication is via the `TAVILY_API_KEY` environment variable, never
interactive login, and only the extract command is vendored because the
morning-brief credit discipline bans the CLI's search, map, crawl,
and research commands (see "House rules" below).

## Before running any command

If `tvly` is not found on PATH, install it first (verified working in the
routine environment):

```bash
pip install tavily-cli
```

Alternative installers: `curl -fsSL https://cli.tavily.com/install.sh | bash`
or `uv tool install tavily-cli`.

Authentication is the `TAVILY_API_KEY` environment variable (format
`tvly-...`), set on the Claude Code environment. Never run `tvly login`
(interactive, browser OAuth) in an unattended session, and never commit a
key to the repository. If the variable is missing, report that extraction
is unavailable and fall back per the calling skill; do not prompt for a key.

Install lazily: only install the CLI at the moment a non-empty batch of
URLs actually needs extraction, not during capability checks.

## When to use

- You have specific URLs (already selected) and need their body content
- The URLs are bot-walled or JavaScript-rendered so plain WebFetch fails
- Never for discovery, search, or candidate screening

## Quick start

```bash
# Batched extraction (the normal call in this repo): all URLs in one command
tvly extract "https://example.com/page1" "https://example.com/page2" --json

# Query-focused extraction (returns relevant chunks only)
tvly extract "https://example.com/docs" --query "ceasefire statement" --chunks-per-source 3 --json

# Save to file
tvly extract "https://example.com/article" -o article.md
```

## Options

| Option | Description |
|--------|-------------|
| `--query` | Rerank chunks by relevance to this query |
| `--chunks-per-source` | Chunks per URL (1-5, requires `--query`) |
| `--extract-depth` | `advanced` in this repository (reads paywalled and JS pages); `basic` is the CLI default |
| `--format` | `markdown` (default) or `text` |
| `--include-images` | Include image URLs |
| `--timeout` | Max wait time (1-60 seconds) |
| `-o, --output` | Save output to file |
| `--json` | Structured JSON output |

Exit codes: 0 = success, 2 = bad input, 3 = auth error, 4 = API error.

## Tips

- **Max 20 URLs per request**; batch the whole list into one call.
- **Always quote URLs**: the shell interprets `?` and `&`.
- **Use `--query` + `--chunks-per-source`** to get only relevant content.
- **Use `--json`** so results are machine-checkable.

## House rules in this repository (credit discipline)

The morning-brief skill (`.claude/skills/morning-brief/SKILL.md`,
Stage 2) governs every use of this CLI. Tavily bills basic extract at 1
credit per 5 URLs; the rules below keep a full report edition at 1 to 2
credits.

- **Extract only.** Never `tvly search`, `tvly map`, `tvly crawl`, or
  `tvly research`: search costs 1 credit per query and duplicates the free
  built-in WebSearch; map, crawl, and research are the expensive endpoints
  and nothing in this repository needs them.
- **Selected articles only.** Extraction happens once per run, after the
  story list is final, covering only selected article URLs that are bot-walled
  to WebFetch and still missing needed body detail.
- **Batched calls, advanced depth, with retries.** All URLs in one
  `tvly extract --extract-depth advanced` command (20 per call), then a
  retry call for the failures, then a third after a 30-second pause.
  Advanced depth costs 2 credits per 5 URLs instead of 1, which is a few
  cents per edition, and it is what reads FT, Politico, The Verge and
  most Reuters pages in full; basic depth misses several of them. A URL
  that still fails falls back to the calling skill's copy-verified or
  snippet-plus-corroboration rule.
