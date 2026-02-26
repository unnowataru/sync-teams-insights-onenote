#!/usr/bin/env python3
"""Parse Teams meeting recap URL and emit normalized identifiers.

This script does not call Microsoft Graph. It only extracts and normalizes
query parameters, then prints endpoint hints for later API resolution.
"""

from __future__ import annotations

import argparse
import base64
import json
from typing import Dict
from urllib.parse import parse_qs
from urllib.parse import unquote
from urllib.parse import urlparse


def encode_share_url(url: str) -> str:
    """Encode a sharing URL for Graph /shares/{encodedSharingUrl} format."""
    encoded = base64.urlsafe_b64encode(url.encode("utf-8")).decode("ascii")
    encoded = encoded.rstrip("=")
    return f"u!{encoded}"


def first_value(values: Dict[str, list[str]], key: str) -> str | None:
    data = values.get(key)
    if not data:
        return None
    return data[0]


def normalize_value(value: str | None) -> str | None:
    if value is None:
        return None
    return unquote(value)


def parse_recap_url(url: str) -> dict:
    parsed = urlparse(url)
    query = parse_qs(parsed.query, keep_blank_values=True)

    identifiers = {
        "driveId": normalize_value(first_value(query, "driveId")),
        "driveItemId": normalize_value(first_value(query, "driveItemId")),
        "fileUrl": normalize_value(first_value(query, "fileUrl")),
        "sitePath": normalize_value(first_value(query, "sitePath")),
        "iCalUid": normalize_value(first_value(query, "iCalUid")),
        "threadId": normalize_value(first_value(query, "threadId")),
        "organizerId": normalize_value(first_value(query, "organizerId")),
        "tenantId": normalize_value(first_value(query, "tenantId")),
        "callId": normalize_value(first_value(query, "callId")),
        "meetingType": normalize_value(first_value(query, "meetingType")),
        "subType": normalize_value(first_value(query, "subType")),
    }

    graph_hints = {}
    if identifiers["driveId"] and identifiers["driveItemId"]:
        graph_hints["driveItem"] = (
            f"/v1.0/drives/{identifiers['driveId']}/items/{identifiers['driveItemId']}"
        )

    if identifiers["fileUrl"]:
        encoded_share = encode_share_url(identifiers["fileUrl"])
        graph_hints["shareDriveItem"] = f"/v1.0/shares/{encoded_share}/driveItem"
        graph_hints["encodedSharingUrl"] = encoded_share

    if identifiers["organizerId"] and identifiers["iCalUid"]:
        graph_hints["eventByICalUid"] = (
            "/v1.0/users/"
            f"{identifiers['organizerId']}/events?$filter=iCalUId eq '{identifiers['iCalUid']}'"
        )

    if identifiers["organizerId"]:
        graph_hints["onlineMeetingsRoot"] = (
            f"/v1.0/users/{identifiers['organizerId']}/onlineMeetings"
        )

    warnings: list[str] = []
    if parsed.netloc.lower() != "teams.microsoft.com":
        warnings.append("URL host is not teams.microsoft.com")
    if not identifiers["driveId"] and not identifiers["fileUrl"]:
        warnings.append("Neither driveId nor fileUrl found; artifact resolution may fail")
    if not identifiers["iCalUid"] and not identifiers["threadId"]:
        warnings.append("Missing iCalUid and threadId; meeting correlation may fail")

    return {
        "sourceUrl": url,
        "urlMeta": {
            "scheme": parsed.scheme,
            "host": parsed.netloc,
            "path": parsed.path,
        },
        "identifiers": identifiers,
        "graphHints": graph_hints,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse Teams recap sharing URL and print normalized JSON."
    )
    parser.add_argument("url", help="Teams recap sharing URL")
    args = parser.parse_args()

    result = parse_recap_url(args.url)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
