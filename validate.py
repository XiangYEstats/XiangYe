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
        self.duplicate_ids: set[str] = set()
        self.links: list[tuple[str, str]] = []
        self.missing_alt = 0
        self.title_count = 0
        self.title_is_localized = False
        self.html_lang: str | None = None
        self.default_language: str | None = None
        self.viewport_present = False
        self.language_toggle_count = 0
        self.language_toggle_missing_label = 0
        self.language_content_counts = {"en": 0, "zh": 0}
        self.invalid_language_content: list[str] = []
        self.invalid_language_only: list[str] = []
        self.unpaired_localized_attributes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)

        if tag == "html":
            self.html_lang = values.get("lang")
            self.default_language = values.get("data-language")
        if tag == "title":
            self.title_count += 1
            self.title_is_localized = bool(values.get("data-title-en") and values.get("data-title-zh"))
        if tag == "meta" and values.get("name") == "viewport":
            self.viewport_present = True
        if tag == "img" and not values.get("alt"):
            self.missing_alt += 1

        if "data-language-toggle" in values:
            self.language_toggle_count += 1
            if tag != "button" or not values.get("aria-label"):
                self.language_toggle_missing_label += 1

        language_content = values.get("data-language-content")
        if language_content:
            if language_content in self.language_content_counts:
                self.language_content_counts[language_content] += 1
            else:
                self.invalid_language_content.append(language_content)
            if tag in {"a", "button", "input", "select", "textarea"}:
                self.invalid_language_content.append(f"focusable <{tag}>")

        language_only = values.get("data-language-only")
        if language_only:
            if language_only not in {"en", "zh"}:
                self.invalid_language_only.append(f"<{tag}> value {language_only!r}")
            expected_lang = "zh-Hans" if language_only == "zh" else language_only
            if values.get("lang") != expected_lang:
                self.invalid_language_only.append(
                    f"<{tag}> expected lang={expected_lang!r}"
                )
            if tag in {"a", "button", "input", "select", "textarea"}:
                self.invalid_language_only.append(f"focusable <{tag}>")

        for english_attribute, chinese_attribute in (
            ("data-label-en", "data-label-zh"),
            ("data-alt-en", "data-alt-zh"),
            ("data-content-en", "data-content-zh"),
            ("data-title-en", "data-title-zh"),
        ):
            if bool(values.get(english_attribute)) != bool(values.get(chinese_attribute)):
                self.unpaired_localized_attributes.append(
                    f"<{tag}> {english_attribute}/{chinese_attribute}"
                )

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

    build_sources = [ROOT / "build.py", ROOT / "site_data.py"]
    build_sources.extend((ROOT / "templates").glob("*.html"))
    build_sources.extend((ROOT / "content" / "notes").glob("*.md"))
    build_sources.append(ROOT / "data" / "publications.json")
    latest_source_mtime = max(path.stat().st_mtime_ns for path in build_sources if path.exists())
    stale_pages = [page for page in pages if page.stat().st_mtime_ns < latest_source_mtime]
    if stale_pages:
        errors.append(
            "generated HTML is stale; rebuild pages: "
            + ", ".join(page.name for page in stale_pages)
        )

    for page, parser in parsed.items():
        label = page.relative_to(ROOT)
        if parser.html_lang != "en":
            errors.append(f"{label}: expected default html lang='en', found {parser.html_lang!r}")
        if parser.default_language != "en":
            errors.append(
                f"{label}: expected default data-language='en', found {parser.default_language!r}"
            )
        if not parser.viewport_present:
            errors.append(f"{label}: missing viewport metadata")
        if parser.title_count != 1:
            errors.append(f"{label}: expected one title element, found {parser.title_count}")
        elif not parser.title_is_localized:
            errors.append(f"{label}: title is missing an English/Chinese metadata pair")
        if parser.missing_alt:
            errors.append(f"{label}: {parser.missing_alt} image(s) missing alt text")
        if parser.duplicate_ids:
            errors.append(f"{label}: duplicate ids: {', '.join(sorted(parser.duplicate_ids))}")
        if parser.language_toggle_count != 1:
            errors.append(
                f"{label}: expected one language toggle, found {parser.language_toggle_count}"
            )
        if parser.language_toggle_missing_label:
            errors.append(f"{label}: language toggle is missing an accessible label")
        if parser.language_content_counts["en"] != parser.language_content_counts["zh"]:
            errors.append(
                f"{label}: language node count mismatch "
                f"({parser.language_content_counts['en']} English, "
                f"{parser.language_content_counts['zh']} Chinese)"
            )
        if not parser.language_content_counts["en"]:
            errors.append(f"{label}: no localized content pairs found")
        if parser.invalid_language_content:
            errors.append(
                f"{label}: invalid language content markers: "
                f"{', '.join(parser.invalid_language_content)}"
            )
        if parser.invalid_language_only:
            errors.append(
                f"{label}: invalid language-only markers: "
                f"{', '.join(parser.invalid_language_only)}"
            )
        if parser.unpaired_localized_attributes:
            errors.append(
                f"{label}: unpaired localized attributes: "
                f"{', '.join(parser.unpaired_localized_attributes)}"
            )

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

    for source, generated in (
        (ROOT / "static" / "css" / "site.css", DOCS / "assets" / "css" / "site.css"),
        (ROOT / "static" / "js" / "site.js", DOCS / "assets" / "js" / "site.js"),
    ):
        if not generated.is_file() or source.read_bytes() != generated.read_bytes():
            errors.append(f"{generated.relative_to(ROOT)}: generated asset is stale")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(
        f"Validated {len(pages)} bilingual HTML pages with complete required language pairs, "
        "intentional single-language content, and no broken local links."
    )


if __name__ == "__main__":
    validate()
