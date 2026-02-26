# sync-teams-insights-onenote

This folder is an independent Codex skill package for planning Teams recap/transcript to OneNote workflows.
It is not an end-user app and not a runnable production integration.

## Current Scope

- Includes skill instructions, reference docs, and one local parser utility for agent workflows.
- Does not include Microsoft Graph execution code.
- Does not include OneNote publish execution code.

## Intended Consumer

- Primary consumer is Codex (agent runtime), not a human end user.
- The content is designed to support skill-driven feasibility analysis and architecture output.

## Repository Layout

```text
sync-teams-insights-onenote/
  SKILL.md
  README.md
  agents/
    openai.yaml
  references/
    api-capability-matrix.md
    feasibility-checklist.md
    recap-link-ingestion.md
  scripts/
    parse_teams_recap_url.py
```

## What Is Implemented

- Parse a Teams recap sharing URL locally.
- Normalize query parameters and extract identifiers:
  - `driveId`, `driveItemId`, `fileUrl`, `sitePath`
  - `iCalUid`, `threadId`, `organizerId`, `tenantId`, `callId`
  - `meetingType`, `subType`
- Generate Graph endpoint hints for next-step resolution.
- Return warnings when key identifiers are missing.

## What Is Not Implemented

- Direct Microsoft Graph calls.
- Transcript retrieval execution.
- Copilot Meeting Insights retrieval execution.
- OneNote page creation execution.

## Parser Usage

```powershell
python scripts/parse_teams_recap_url.py "https://teams.microsoft.com/l/meetingrecap?..."
```

Output JSON includes:

- `sourceUrl`
- `urlMeta`
- `identifiers`
- `graphHints`
- `warnings`

## References

- `references/api-capability-matrix.md`
- `references/feasibility-checklist.md`
- `references/recap-link-ingestion.md`
