"""Lightweight validation for the generated static website."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[tuple[str, str]] = []
        self.missing_alt = 0
        self.title_count = 0
        self.lang_present = False
        self.viewport_present = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.add(element_id)

        if tag == "html" and values.get("lang"):
            self.lang_present = True
        if tag == "title":
            self.title_count += 1
        if tag == "meta" and values.get("name") == "viewport":
            self.viewport_present = True
        if tag == "img" and not values.get("alt"):
            self.missing_alt += 1

        for attribute in ("href", "src"):
            reference = values.get(attribute)
            if reference:
                self.links.append((attribute, reference))


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def validate() -> None:
    if not DOCS.is_dir():
        raise SystemExit("docs/ does not exist. Run `python build.py` first.")

    pages = sorted(DOCS.glob("*.html"))
    parsed = {page.resolve(): parse_page(page) for page in pages}
    errors: list[str] = []

    for page, parser in parsed.items():
        label = page.relative_to(ROOT)
        if not parser.lang_present:
            errors.append(f"{label}: missing html lang attribute")
        if not parser.viewport_present:
            errors.append(f"{label}: missing viewport metadata")
        if parser.title_count != 1:
            errors.append(f"{label}: expected one title element, found {parser.title_count}")
        if parser.missing_alt:
            errors.append(f"{label}: {parser.missing_alt} image(s) missing alt text")

        for attribute, reference in parser.links:
            parts = urlsplit(reference)
            if parts.scheme in {"http", "https", "mailto", "tel", "data"} or parts.netloc:
                continue

            relative_path = unquote(parts.path)
            target = (page.parent / relative_path).resolve() if relative_path else page
            if not target.exists():
                errors.append(f"{label}: broken {attribute} reference {reference!r}")
                continue

            if parts.fragment and target.suffix.lower() == ".html":
                target_parser = parsed.get(target)
                if target_parser is None:
                    target_parser = parse_page(target)
                    parsed[target] = target_parser
                if unquote(parts.fragment) not in target_parser.ids:
                    errors.append(f"{label}: missing fragment target {reference!r}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"Validated {len(pages)} HTML pages with no broken local links.")


if __name__ == "__main__":
    validate()

