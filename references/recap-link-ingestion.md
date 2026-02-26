# Recap Link Ingestion

Last reviewed: 2026-02-24

## Purpose

Define how to accept a Teams recap sharing URL as input and convert it into stable Graph API lookup paths for summary generation and OneNote publishing.

## Expected URL Shape

Typical input:

`https://teams.microsoft.com/l/meetingrecap?...&driveId=...&driveItemId=...&fileUrl=...&iCalUid=...&threadId=...`

Common useful query parameters:

1. `driveId`
2. `driveItemId`
3. `fileUrl`
4. `sitePath`
5. `iCalUid`
6. `threadId`
7. `organizerId`
8. `tenantId`
9. `callId`
10. `meetingType`

## Resolution Strategy

1. Parse URL and normalize percent-encoded values.
2. Choose primary artifact resolver:
- Use `/drives/{driveId}/items/{driveItemId}` when both are present.
- Otherwise use `/shares/{encodedSharingUrl}/driveItem` based on `fileUrl`.
3. Collect meeting correlators:
- Use `iCalUid` and `organizerId` to locate calendar event/meeting context.
- Use `threadId` as conversation-level fallback correlation key.
4. Attempt Copilot Meeting Insights retrieval when meeting id mapping is resolved.
5. If Insights unavailable, fetch transcript artifacts and run custom summarization.
6. Build OneNote payload with source metadata and summary body.

## Error Handling Rules

1. If URL parse fails, return `Not feasible as requested` unless alternative identifiers are supplied.
2. If parse succeeds but artifact access is denied, return `Feasible with constraints` and list required permission changes.
3. If drive item resolves but transcript/insights do not, continue with best available source and mark data gaps explicitly.
4. Never log full URL in plaintext where logs can be exported; redact sensitive query values.

## Recommended JSON Contract

Use this shape internally:

```json
{
  "sourceUrl": "https://teams.microsoft.com/l/meetingrecap?...",
  "identifiers": {
    "driveId": "...",
    "driveItemId": "...",
    "fileUrl": "...",
    "iCalUid": "...",
    "threadId": "...",
    "organizerId": "...",
    "tenantId": "..."
  },
  "resolution": {
    "driveItemPath": "/v1.0/drives/{drive-id}/items/{item-id}",
    "sharePath": "/v1.0/shares/{encodedSharingUrl}/driveItem",
    "meetingContextResolved": false
  }
}
```

## Utility Script

Use `scripts/parse_teams_recap_url.py` for deterministic parsing and endpoint hint generation.
