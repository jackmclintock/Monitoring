# Routine prompts

The two platform routines are created once at claude.ai/code/routines (see
SETUP.md section 5). Their names must be exactly:

- `Inception42 Morning Brief`
- `Inception42 Morning Brief (second edition)`

because the Morning Brief Operations dashboard finds them by name to adjust
their days and times. Paste the matching prompt file as the routine's
prompt. Attach the **Microsoft 365** connector to both; without it a run
cannot read the Signal AI alerts or upload to SharePoint.

All routines run on Claude Opus 5.5 (`claude-opus-5-5`).

## Inception42 Morning Brief (benchmark)

Runs weekdays at 10:30 GST (`CRON_TZ=Asia/Dubai 30 10 * * 1-5`), prompt
`routines/benchmark.prompt.txt`, Microsoft 365 connector attached, Opus
5.5 at medium effort. Transcribes the edition the team sent, scores the
generated one against it (`scripts/benchmark.py`), classifies every
miss, fixes what can be fixed (sweep queries, learnings) and writes the
result to the dashboard edition. See `.claude/skills/morning-brief/BENCHMARK.md`.
