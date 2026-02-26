---
name: sync-teams-insights-onenote
description: Assess feasibility and design or implement automation that summarizes Microsoft Teams meeting transcripts, Teams recap share links, or Copilot meeting insights and syncs results into OneNote using Microsoft Graph or local OneNote COM workflows. Use when requests mention Teams meeting notes, recap URLs, transcript recap, Microsoft 365 Copilot meeting summaries, OneNote handoff, tag-based notebook routing, or workflow automation between Teams and OneNote.
---

# Sync Teams Insights Onenote

## Overview

Produce a clear feasibility verdict and an implementation path for Teams-to-OneNote meeting summary workflows. Prefer official Microsoft Graph capabilities, call out preview and licensing constraints, and provide a fallback plan when Copilot APIs are unavailable.

## Workflow

1. Confirm the requested target behavior:
- Ask whether the user wants no-code automation (Power Automate), coded integration (Graph API), or both.
- Ask whether summary generation must come from Microsoft 365 Copilot output, transcript-based custom summarization, or either.
- Ask whether the user provides meeting identifiers directly or a Teams recap sharing URL.
- Ask whether chat-text mode with required manufacturer tags and date should be used.

2. Run feasibility gates before proposing build steps:
- Gate A: Tenant and licensing readiness.
- Gate B: Meeting type and data availability readiness.
- Gate C: API permission model readiness.
- Gate D: Destination OneNote notebook/section readiness.
- Gate E: URL-origin metadata readiness (when recap URL is provided).

3. If input is a recap sharing URL, resolve identifiers first:
- Parse query parameters and extract `driveId`, `driveItemId`, `fileUrl`, `iCalUid`, `threadId`, `organizerId`, `tenantId`, and `callId` when present.
- Use SharePoint/OneDrive identifiers to resolve recording/transcript related artifacts if applicable.
- Use `iCalUid` and organizer context to map to calendar event and online meeting identifiers when needed.
- Continue only after at least one reliable source path is confirmed.

4. Choose the summary source strategy:
- Strategy 1: Use Meeting Insights API first when available and acceptable.
- Strategy 2: Use Teams transcript API plus custom summarization when Insights API is unavailable, unsupported, or too restrictive.
- Strategy 3: Hybrid mode that attempts Insights first and falls back to transcript summarization.
- Strategy 4: Chat-text ingestion mode (no Graph) that writes directly via OneNote COM using tag routing rules.

5. Map output to OneNote:
- Convert summary into stable HTML sections for page creation.
- Include metadata block with meeting id, meeting date/time, source type, and generation timestamp.
- Include `sourceUrl` and extracted recap identifiers in a traceability block when URL mode is used.
- Create one page per meeting unless the user explicitly requests aggregation.

6. Return deliverables in this order:
- Feasibility verdict: `Feasible`, `Feasible with constraints`, or `Not feasible as requested`.
- Blocking constraints and why they block.
- Recommended architecture and fallback path.
- Minimal implementation backlog with phases.
- Validation checklist and monitoring points.

## Feasibility Rules

Apply these rules consistently:

1. Mark "not feasible as requested" when the user requires direct built-in Microsoft 365 Copilot invocation where no supported API path exists for that exact operation.
2. Mark "feasible with constraints" when APIs exist but preview status, delegated-only permission models, or meeting-type limits apply.
3. Mark "feasible" only when required APIs, permissions, and meeting prerequisites are all satisfied.
4. Always include a fallback architecture that uses transcript retrieval and custom summarization if Copilot-generated insights are unavailable.
5. State uncertainty explicitly when Microsoft preview behavior may change.
6. In recap URL mode, mark "feasible with constraints" if identifier mapping succeeds but artifact access depends on per-file SharePoint permissions.
7. In chat-text mode, enforce tag/date rules and route by primary tag. If no tag is supplied, infer with threshold gating and candidate fallback.

## Recommended Output Format

Use this concise structure:

1. `Goal`
2. `Feasibility verdict`
3. `Constraints`
4. `Architecture options`
5. `Recommended plan`
6. `Permissions and security`
7. `Next actions`

## References

Load only when needed:
- [references/api-capability-matrix.md](references/api-capability-matrix.md): Current API options, constraints, and permission expectations.
- [references/feasibility-checklist.md](references/feasibility-checklist.md): Stepwise go/no-go checks and decision tree.
- [references/recap-link-ingestion.md](references/recap-link-ingestion.md): Teams recap sharing URL parse and resolution flow.
- `scripts/parse_teams_recap_url.py <url>`: Extract recap URL identifiers into JSON for downstream Graph API mapping.
