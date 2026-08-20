#!/usr/bin/env python3
"""Synchronize the publications cache with a public Google Scholar profile.

The live site never contacts Scholar. This script runs during the scheduled
GitHub Actions build, validates the complete response, and replaces the cache
only after a successful parse.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_data import SITE  # noqa: E402


DEFAULT_OUTPUT = ROOT / "data" / "publications.json"
SCHOLAR_ORIGIN = "https://scholar.google.com"
PAGE_SIZE = 100
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


class ScholarSyncError(RuntimeError):
    """Raised when Scholar cannot be fetched or parsed safely."""


class ScholarRowsParser(HTMLParser):
    """Extract publication rows from Google Scholar's author-profile HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[dict[str, object]] = []
        self.current: dict[str, object] | None = None
        self.gray_index = 0
        self.capture_field: str | None = None
        self.capture_depth = 0

    @staticmethod
    def _classes(attrs: list[tuple[str, str | None]]) -> set[str]:
        value = dict(attrs).get("class") or ""
        return set(value.split())

    def _capture(self, field: str) -> None:
        self.capture_field = field
        self.capture_depth = 1
        assert self.current is not None
        self.current.setdefault(field, [])

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = self._classes(attrs)

        if tag == "tr" and "gsc_a_tr" in classes:
            self.current = {}
            self.gray_index = 0
            self.capture_field = None
            self.capture_depth = 0
            return

        if self.current is None:
            return

        if self.capture_field is not None:
            self.capture_depth += 1
            return

        values = dict(attrs)
        if tag == "a" and "gsc_a_at" in classes:
            self.current["href"] = values.get("href") or ""
            self._capture("title")
        elif tag == "div" and "gs_gray" in classes:
            field = "authors" if self.gray_index == 0 else "venue"
            self.gray_index += 1
            self._capture(field)
        elif tag == "span" and "gsc_a_h" in classes:
            self._capture("year")

    def handle_data(self, data: str) -> None:
        if self.current is None or self.capture_field is None:
            return
        parts = self.current[self.capture_field]
        assert isinstance(parts, list)
        parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return

        if self.capture_field is not None:
            self.capture_depth -= 1
            if self.capture_depth == 0:
                self.capture_field = None

        if tag == "tr":
            self.rows.append(self.current)
            self.current = None
            self.capture_field = None
            self.capture_depth = 0


def clean_text(parts: object) -> str:
    if not isinstance(parts, list):
        return ""
    return re.sub(r"\s+", " ", "".join(str(part) for part in parts)).strip()


def profile_id_from_url(profile_url: str) -> str:
    profile_id = parse_qs(urlsplit(profile_url).query).get("user", [""])[0]
    if not re.fullmatch(r"[-_0-9A-Za-z]{12}", profile_id):
        raise ScholarSyncError(f"Invalid Google Scholar profile URL: {profile_url}")
    return profile_id


def citation_url(profile_id: str, href: object) -> str:
    query = parse_qs(urlsplit(str(href)).query)
    citation_id = query.get("citation_for_view", [""])[0]
    if not citation_id.startswith(f"{profile_id}:"):
        raise ScholarSyncError(f"Invalid Scholar citation link: {href!r}")
    citation_query = urlencode(
        {
            "view_op": "view_citation",
            "hl": "en",
            "user": profile_id,
            "citation_for_view": citation_id,
        }
    )
    return f"{SCHOLAR_ORIGIN}/citations?{citation_query}"


def parse_page(source: str, profile_id: str) -> list[dict[str, str]]:
    lowered = source.lower()
    block_markers = ("unusual traffic", "not a robot", "g-recaptcha", "/sorry/")
    if any(marker in lowered for marker in block_markers):
        raise ScholarSyncError("Google Scholar returned an anti-automation page")
    if "</html>" not in lowered:
        raise ScholarSyncError("Google Scholar returned an incomplete HTML response")

    parser = ScholarRowsParser()
    parser.feed(source)
    publications: list[dict[str, str]] = []

    for row in parser.rows:
        title = clean_text(row.get("title"))
        year = clean_text(row.get("year"))
        authors = clean_text(row.get("authors"))
        venue = clean_text(row.get("venue"))
        if not title:
            raise ScholarSyncError("A Scholar publication row has no title")
        if year:
            venue = re.sub(rf",\s*{re.escape(year)}$", "", venue).strip()

        publications.append(
            {
                "title": title,
                "authors": authors,
                "venue": venue,
                "year": year,
                "scholar_url": citation_url(profile_id, row.get("href")),
            }
        )

    return publications


def request_page(profile_id: str, start: int) -> str:
    query = urlencode(
        {
            "view_op": "list_works",
            "hl": "en",
            "user": profile_id,
            "cstart": start,
            "pagesize": PAGE_SIZE,
        }
    )
    request = Request(
        f"{SCHOLAR_ORIGIN}/citations?{query}",
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except (HTTPError, URLError, TimeoutError) as error:
        raise ScholarSyncError(f"Unable to fetch Google Scholar: {error}") from error


def fetch_all(profile_id: str) -> list[dict[str, str]]:
    publications: list[dict[str, str]] = []
    start = 0

    while True:
        page = parse_page(request_page(profile_id, start), profile_id)
        if start == 0 and not page:
            raise ScholarSyncError("The Scholar profile returned no publication rows")
        publications.extend(page)
        if len(page) < PAGE_SIZE:
            break
        start += PAGE_SIZE
        time.sleep(2)

    return publications


def sorted_publications(publications: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    for publication in publications:
        url = publication["scholar_url"]
        if url in seen:
            raise ScholarSyncError(f"Duplicate Scholar record: {url}")
        seen.add(url)

    return sorted(
        publications,
        key=lambda item: (
            -(int(item["year"]) if item["year"].isdigit() else -1),
            item["title"].casefold(),
        ),
    )


def existing_cache(path: Path) -> dict[str, object] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ScholarSyncError(f"Cannot read existing cache {path}: {error}") from error
    return value if isinstance(value, dict) else None


def write_cache(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile-id", help="Override the profile ID from site_data.py")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--source-file",
        type=Path,
        help="Parse a saved Scholar HTML response instead of making a network request",
    )
    args = parser.parse_args()

    profile_url = SITE["scholar"]
    profile_id = args.profile_id or profile_id_from_url(profile_url)
    if args.profile_id:
        profile_query = urlencode({"user": profile_id, "hl": "en"})
        profile_url = f"{SCHOLAR_ORIGIN}/citations?{profile_query}"

    try:
        if args.source_file:
            source = args.source_file.read_text(encoding="utf-8")
            publications = parse_page(source, profile_id)
        else:
            publications = fetch_all(profile_id)
        publications = sorted_publications(publications)
    except (OSError, ScholarSyncError) as error:
        print(f"Scholar synchronization failed: {error}", file=sys.stderr)
        print("The existing publications cache was not changed.", file=sys.stderr)
        return 1

    current = existing_cache(args.output)
    unchanged = (
        current is not None
        and current.get("profile_id") == profile_id
        and current.get("profile_url") == profile_url
        and current.get("publications") == publications
    )
    if unchanged:
        print(f"Google Scholar is unchanged ({len(publications)} publications).")
        return 0

    data: dict[str, object] = {
        "schema_version": 1,
        "source": "Google Scholar",
        "profile_id": profile_id,
        "profile_url": profile_url,
        "synced_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "publications": publications,
    }
    write_cache(args.output, data)
    print(f"Updated {args.output} with {len(publications)} publications.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
