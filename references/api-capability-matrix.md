# API Capability Matrix

Last reviewed: 2026-02-24

## Purpose

Use this file to map user requirements to supported Microsoft APIs and known constraints.

## Capability Table

| Requirement | Primary API | Status | Key constraints |
| --- | --- | --- | --- |
| Parse Teams recap sharing URL into usable IDs | Local parser plus URL query extraction | Available | URL alone is not authorization; extracted IDs still require Graph and SharePoint permissions |
| Resolve meeting artifact from recap `fileUrl` | Microsoft Graph Shares (`/v1.0/shares/{encodedSharingUrl}/driveItem`) | Available | Requires building encoded sharing URL token and caller must have access to underlying file |
| Resolve recording/transcript item from `driveId` and `driveItemId` | Microsoft Graph Drives (`/v1.0/drives/{drive-id}/items/{item-id}`) | Available | Access is subject to SharePoint/OneDrive ACL and tenant controls |
| Retrieve Copilot-generated meeting summary/action items | Microsoft Graph Copilot Meeting Insights (`/beta/copilot/.../aiInsights`) | Available in beta preview | Requires specific meeting prerequisites, delegated permission model, preview changes possible |
| Retrieve raw Teams transcript text | Microsoft Graph onlineMeeting transcripts (`/v1.0/users/{id}/onlineMeetings/{meetingId}/transcripts`) | Available | Requires transcription to be enabled and transcript to exist |
| Create OneNote page with structured summary | Microsoft Graph OneNote pages (`/v1.0/me/onenote/pages` or user/group variants) | Available | Requires OneNote Graph permissions and HTML payload formatting |
| Trigger on meeting completion automatically | Event workflow via Graph subscriptions or scheduler pattern | Partial | Trigger strategy depends on tenant policy and event source support |

## Notes For Decision Making

1. Prefer Meeting Insights when user wants Copilot-style outputs and prerequisites are met.
2. Prefer transcript plus custom summarization when Insights API constraints block coverage.
3. Keep hybrid fallback for reliability in production flows.
4. Separate source acquisition from OneNote publishing so fallback is easy.
5. In recap URL mode, treat URL parameters as hints and always validate by calling Graph before assuming artifact availability.

## Practical Permission Planning

1. Start with least-privilege delegated scopes in proof-of-concept.
2. Move to app permissions only where endpoint supports them.
3. Document exact scopes per endpoint and user role assumptions before implementation.
