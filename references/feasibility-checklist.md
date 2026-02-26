# Feasibility Checklist

Last reviewed: 2026-02-24

## Step 1: Clarify User Constraint

1. Confirm whether built-in Microsoft 365 Copilot output is mandatory.
2. Confirm whether transcript-based custom summary is acceptable fallback.
3. Confirm whether no-code only implementation is required.

## Step 2: Tenant And Licensing Checks

1. Confirm Microsoft 365 Copilot entitlement for required users.
2. Confirm Teams meeting transcription policy allows transcript generation.
3. Confirm OneNote destination notebook and permission ownership model.

## Step 3: Meeting Coverage Checks

1. Confirm target meeting types are supported by selected source API.
2. Confirm expected data freshness and retention window requirements.
3. Confirm channel meeting handling requirements and whether fallback is needed.
4. If recap URL is input, confirm query includes enough identifiers (`driveId`/`driveItemId` or `fileUrl`, plus meeting metadata).

## Step 4: API Permission Checks

1. List required Graph scopes for transcript/insights retrieval.
2. List required Graph scopes for OneNote write operations.
3. Confirm delegated vs application permission compatibility.

## Step 5: Automation Design Checks

1. Select trigger model: scheduled pull, event-driven, or manual run.
2. Define idempotency key: meeting id plus summary version.
3. Define failure handling: retry, dead-letter, and operator alert route.
4. Define URL-input sanitization and PII-safe logging rules for shared recap links.

## Step 6: Verdict Criteria

Mark `Feasible` when all checks pass with supported APIs and acceptable constraints.

Mark `Feasible with constraints` when APIs exist but constraints remain:
- Preview-only endpoint risk
- Meeting-type exclusions
- Delegated permission limitations
- Tenant policy blockers requiring admin change

Mark `Not feasible as requested` when user disallows all available fallback paths.
