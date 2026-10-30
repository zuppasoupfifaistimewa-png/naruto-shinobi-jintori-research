#!/usr/bin/env python3
"""Metadata-only YouTube source check; never downloads or plays audiovisual media."""
from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, urlsplit
from urllib.request import Request, urlopen

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com",
                 "youtu.be", "www.youtu.be",
                 "youtube-nocookie.com", "www.youtube-nocookie.com"}
USER_AGENT = ("NarutoJintoriResearch/1.0 (metadata-only source checker; "
              "https://github.com/zuppasoupfifaistimewa-png/"
              "naruto-shinobi-jintori-research)")


class InputError(ValueError):
    pass


def parse_video_url(value: str) -> tuple[str, str]:
    """Return the YouTube video ID and a canonical watch URL."""
    raw = value.strip()
    if not raw:
        raise InputError("URL kosong.")
    parsed = urlsplit(raw)
    if parsed.scheme not in {"http", "https"}:
        raise InputError("URL harus memakai http:// atau https://.")
    host = (parsed.hostname or "").lower()
    if host not in YOUTUBE_HOSTS:
        raise InputError("Host bukan domain YouTube yang didukung.")
    parts = [part for part in parsed.path.split("/") if part]
    if host.endswith("youtu.be"):
        video_id = parts[0] if parts else ""
    elif parsed.path.rstrip("/") == "/watch":
        video_id = parse_qs(parsed.query).get("v", [""])[0]
    elif len(parts) >= 2 and parts[0] in {"embed", "shorts", "live"}:
        video_id = parts[1]
    else:
        video_id = ""
    if not VIDEO_ID_RE.fullmatch(video_id):
        raise InputError("ID video YouTube tidak ditemukan atau formatnya tidak valid.")
    return video_id, f"https://www.youtube.com/watch?v={video_id}"


def classify_oembed(status_code: int, payload: object) -> dict:
    """Never infer player or caption availability from metadata response."""
    if status_code != 200:
        return {"access_state": "METADATA_ENDPOINT_BLOCKED",
                "http_status": status_code, "title": None, "channel": None}
    if not isinstance(payload, dict):
        return {"access_state": "UNEXPECTED_RESPONSE",
                "http_status": status_code, "title": None, "channel": None}
    title = payload.get("title")
    channel = payload.get("author_name")
    if not isinstance(title, str) or not title.strip():
        return {"access_state": "UNEXPECTED_RESPONSE",
                "http_status": status_code, "title": None, "channel": None}
    return {"access_state": "METADATA_ONLY", "http_status": status_code,
            "title": title.strip(),
            "channel": channel.strip() if isinstance(channel, str) and channel.strip() else None}


def request_oembed(canonical_url: str) -> dict:
    """Query YouTube's public oEmbed endpoint for metadata only."""
    endpoint = ("https://www.youtube.com/oembed?url=" +
                quote(canonical_url, safe="") + "&format=json")
    request = Request(endpoint, headers={"User-Agent": USER_AGENT,
                                         "Accept": "application/json"})
    try:
        with urlopen(request, timeout=15) as response:
            status_code = int(response.status)
            raw = response.read(256_000)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            payload = None
        return classify_oembed(status_code, payload)
    except HTTPError as exc:
        return classify_oembed(int(exc.code), None)
    except (URLError, TimeoutError, OSError) as exc:
        reason = getattr(exc, "reason", exc)
        return {"access_state": "NETWORK_ERROR", "http_status": None,
                "title": None, "channel": None,
                "error_type": type(reason).__name__}


def safe_markdown(value: object) -> str:
    """Keep remote metadata from injecting report structure."""
    text = str(value or "").replace("\r", " ").replace("\n", " ").strip()
    return text.replace(chr(96), "'").replace("[", "(").replace("]", ")")[:500]


def build_report(video_id: str, canonical_url: str, result: dict) -> str:
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    lines = [
        "# YouTube source access check", "",
        f"- Checked at (UTC): {checked_at}",
        f"- Video ID: {video_id}",
        f"- Source: {canonical_url}",
        f"- Access state: {result['access_state']}",
        f"- Metadata HTTP status: {result.get('http_status')}",
        "- Official player playback: NOT_TESTED",
        "- Captions/transcript: NOT_TESTED",
        "- Frame/audio inspection: NOT_STARTED", "",
    ]
    if result.get("title"):
        lines.extend([f"- Title (oEmbed): {safe_markdown(result['title'])}",
                      f"- Channel (oEmbed): {safe_markdown(result.get('channel') or 'not returned')}", ""])
    if result.get("error_type"):
        lines.extend([f"- Network error class: {safe_markdown(result['error_type'])}", ""])
    lines.extend([
        "## Interpretation", "",
        "- METADATA_ONLY means the public oEmbed endpoint returned basic metadata.",
        "- It does NOT prove that the video player can play, or that audio, frames,",
        "  captions, or gameplay content are accessible.",
        "- This check does not download, stream, play, extract, or store video/audio.",
        "- Game rules must not be inferred from metadata, title, or thumbnail.", "",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Public YouTube video URL")
    parser.add_argument("--output", default="reports/youtube_source_access/latest.md")
    args = parser.parse_args(argv)
    try:
        video_id, canonical_url = parse_video_url(args.url)
    except InputError as exc:
        print(f"INVALID_INPUT: {exc}", file=sys.stderr)
        return 2
    result = request_oembed(canonical_url)
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_report(video_id, canonical_url, result), encoding="utf-8")
    print(f"YOUTUBE_SOURCE_CHECK={result['access_state']}")
    print(f"VIDEO_ID={video_id}")
    print(f"REPORT={destination.as_posix()}")
    print("AV_MEDIA_DOWNLOADED=no")
    print("PLAYER_TESTED=no")
    print("CAPTIONS_TESTED=no")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
