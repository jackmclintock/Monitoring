# Routine prompts

The two platform routines are created once at claude.ai/code/routines (see
SETUP.md section 5). Their names must be exactly:

- `Inception42 Morning Brief`
- `Inception42 Morning Brief (second edition)`

because the Morning Brief Operations dashboard finds them by name to adjust
their days and times. Paste the matching prompt file as the routine's
prompt. Attach the **Microsoft 365** connector to both; without it a run
cannot read the Signal AI alerts or upload to SharePoint.
