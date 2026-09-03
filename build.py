"""Build the static GitHub Pages website into ``docs/``."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import re
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from site_data import (
    ABOUT_ITEMS,
    ACTIVITIES,
    DISTINCTIONS,
    EDUCATION,
    EXPERIENCE,
    INTRO_PARAGRAPHS,
    NAVIGATION,
    CURRENT_QUESTIONS,
    PACKAGES,
    POETRY,
    RESEARCH_DIRECTIONS,
    RESEARCH_INTERESTS,
    RESOURCE_TUTORIALS,
    SITE,
    SOCIAL_LINKS,
    TOOLS,
)


ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
FILES_DIR = ROOT / "files"
OUTPUT_DIR = ROOT / "docs"
PUBLICATIONS_FILE = ROOT / "data" / "publications.json"
NOTES_DIR = ROOT / "content" / "notes"
BASE_URL = "https://xiangyestats.github.io/XiangYe"
NOTE_LANGUAGE_MARKER = "\n<!-- zh-Hans -->\n"


PAGES = [
    {
        "template": "index.html",
        "output": "index.html",
        "active": "home",
        "title": "Home",
        "title_cn": "首页",
        "description": SITE["description"],
        "description_cn": SITE["description_cn"],
    },
    {
        "template": "research.html",
        "output": "research.html",
        "active": "research",
        "title": "Research",
        "title_cn": "研究",
        "description": "Research directions, projects, and related articles by Xiang Ye.",
        "description_cn": "介绍叶翔的研究方向、项目及相关论文。",
        "mark": "研",
        "verse": "research_precision",
    },
    {
        "template": "publications.html",
        "output": "publications.html",
        "active": "publications",
        "title": "Publications",
        "title_cn": "学术论文",
        "description": "Publications by Xiang Ye, synchronized from Google Scholar.",
        "description_cn": "收录叶翔的学术论文，并与 Google Scholar 保持同步。",
        "mark": "文",
        "verse": "writing",
    },
    {
        "template": "resources.html",
        "output": "resources.html",
        "active": "resources",
        "title": "Resources",
        "title_cn": "资源",
        "description": "Software packages and tutorials by Xiang Ye.",
        "description_cn": "汇集叶翔开发的软件包与教程。",
        "mark": "器",
        "verse": "tools_for_work",
    },
    {
        "template": "notes.html",
        "output": "notes.html",
        "active": "notes",
        "title": "Notes",
        "title_cn": "随笔",
        "description": "Notes on research, learning, methods, and ideas by Xiang Ye.",
        "description_cn": "收录叶翔关于研究、学习、方法与思考的随笔。",
        "mark": "记",
        "verse": "notes_and_writing",
    },
    {
        "template": "activity.html",
        "output": "activity.html",
        "active": "activity",
        "title": "Activity",
        "title_cn": "学术活动",
        "description": "Research activities and distinctions of Xiang Ye.",
        "description_cn": "记录叶翔的学术活动与所获荣誉。",
        "mark": "行",
        "verse": "wide_roads",
    },
    {
        "template": "about.html",
        "output": "about_me.html",
        "active": "about",
        "title": "About Me",
        "title_cn": "研究之外",
        "description": "A little more about Xiang Ye beyond research.",
        "description_cn": "记录叶翔研究之外的兴趣与日常。",
        "mark": "闲",
        "verse": "wide_reading",
    },
    {
        "template": "contact.html",
        "output": "contact.html",
        "active": "contact",
        "title": "Contact",
        "title_cn": "联系我",
        "description": "Contact Xiang Ye about research and collaboration.",
        "description_cn": "欢迎联系叶翔，交流研究想法与合作机会。",
        "mark": "信",
        "verse": "kindred_minds",
    },
    {
        "template": "404.html",
        "output": "404.html",
        "active": "",
        "title": "Page not found",
        "title_cn": "页面未找到",
        "description": "The requested page could not be found.",
        "description_cn": "未找到您访问的页面。",
    },
]


def bilingual_text(english: object, chinese: object | None = None) -> Markup:
    """Render one non-focusable text node for each supported language.

    CSS removes the inactive node from layout and the accessibility tree. The
    English node comes first so the no-JavaScript experience remains English.
    """

    if chinese is None or not str(chinese).strip():
        raise ValueError(f"Missing Chinese translation for {str(english)!r}")
    return Markup(
        '<span data-language-content="en" lang="en">{}</span>'
        '<span data-language-content="zh" lang="zh-Hans">{}</span>'
    ).format(english, chinese)


def require_translation(record: dict, field: str, label: str) -> None:
    """Fail the build before output cleanup when required Chinese copy is absent."""

    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: missing required Chinese field {field!r}")


def validate_translation_data() -> None:
    """Check every populated translatable record used by the current site."""

    for field in (
        "role_cn",
        "affiliation_cn",
        "group_cn",
        "supervisor_cn",
        "location_cn",
        "office_cn",
        "description_cn",
    ):
        require_translation(SITE, field, "SITE")

    for index, item in enumerate(NAVIGATION, 1):
        require_translation(item, "label_cn", f"NAVIGATION[{index}]")
    for index, item in enumerate(SOCIAL_LINKS, 1):
        require_translation(item, "label_cn", f"SOCIAL_LINKS[{index}]")
    for index, item in enumerate(INTRO_PARAGRAPHS, 1):
        require_translation(item, "text_cn", f"INTRO_PARAGRAPHS[{index}]")

    for index, item in enumerate(EDUCATION, 1):
        for field in ("degree_cn", "institution_cn", "place_cn"):
            require_translation(item, field, f"EDUCATION[{index}]")

    for index, item in enumerate(RESEARCH_INTERESTS, 1):
        for field in ("title_cn", "text_cn"):
            require_translation(item, field, f"RESEARCH_INTERESTS[{index}]")

    for direction_index, direction in enumerate(RESEARCH_DIRECTIONS, 1):
        direction_label = f"RESEARCH_DIRECTIONS[{direction_index}]"
        for field in ("title_cn", "summary_cn"):
            require_translation(direction, field, direction_label)
        for project_index, project in enumerate(direction.get("projects", []), 1):
            project_label = f"{direction_label}.projects[{project_index}]"
            for field in ("title_cn", "text_cn"):
                require_translation(project, field, project_label)
        for tutorial_index, tutorial in enumerate(direction.get("tutorials", []), 1):
            tutorial_label = f"{direction_label}.tutorials[{tutorial_index}]"
            require_translation(tutorial, "title_cn", tutorial_label)
            if tutorial.get("description"):
                require_translation(tutorial, "description_cn", tutorial_label)

    for index, item in enumerate(CURRENT_QUESTIONS, 1):
        require_translation(item, "text_cn", f"CURRENT_QUESTIONS[{index}]")

    for index, item in enumerate(PACKAGES, 1):
        package_label = f"PACKAGES[{index}]"
        require_translation(item, "description_cn", package_label)
        if item.get("status"):
            require_translation(item, "status_cn", package_label)

    for index, item in enumerate(RESOURCE_TUTORIALS, 1):
        tutorial_label = f"RESOURCE_TUTORIALS[{index}]"
        require_translation(item, "title_cn", tutorial_label)
        if item.get("description"):
            require_translation(item, "description_cn", tutorial_label)

    for group_index, group in enumerate(ACTIVITIES, 1):
        for item_index, item in enumerate(group.get("items", []), 1):
            item_label = f"ACTIVITIES[{group_index}].items[{item_index}]"
            for field in ("type_cn", "place_cn", "date_cn"):
                require_translation(item, field, item_label)

    for index, item in enumerate(DISTINCTIONS, 1):
        for field in ("title_cn", "text_cn"):
            require_translation(item, field, f"DISTINCTIONS[{index}]")

    for index, item in enumerate(EXPERIENCE, 1):
        for field in ("role_cn", "organisation_cn", "place_cn"):
            require_translation(item, field, f"EXPERIENCE[{index}]")

    for index, item in enumerate(ABOUT_ITEMS, 1):
        for field in ("title_cn", "text_cn"):
            require_translation(item, field, f"ABOUT_ITEMS[{index}]")

    for index, page in enumerate(PAGES, 1):
        for field in ("title_cn", "description_cn"):
            require_translation(page, field, f"PAGES[{index}]")


def load_notes() -> list[dict]:
    """Load dated Markdown notes, newest first.

    Files whose names begin with an underscore are instructional templates and
    are deliberately ignored.  The Markdown dependency is loaded only when a
    published note exists, so an empty Notes section remains a valid build.
    """

    if not NOTES_DIR.is_dir():
        return []

    source_files = sorted(
        path for path in NOTES_DIR.glob("*.md") if not path.name.startswith("_")
    )
    if not source_files:
        return []

    try:
        import markdown
    except ImportError as error:
        raise RuntimeError(
            "Markdown is required when notes are present. Run "
            "`python -m pip install -r requirements.txt`."
        ) from error

    notes = []
    for path in source_files:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", path.stem):
            raise ValueError(
                f"{path}: note filenames must contain lowercase letters, numbers, and hyphens only"
            )

        source = path.read_text(encoding="utf-8")
        if NOTE_LANGUAGE_MARKER in source:
            english_source, chinese_source = source.split(NOTE_LANGUAGE_MARKER, 1)
        else:
            raise ValueError(
                f"{path}: missing bilingual body marker {NOTE_LANGUAGE_MARKER.strip()!r}"
            )
        if not chinese_source.strip():
            raise ValueError(f"{path}: Chinese note body is empty")

        converter = markdown.Markdown(extensions=["extra", "meta", "sane_lists"])
        body_html = converter.convert(english_source)
        metadata = {
            key.lower(): values[0].strip()
            for key, values in converter.Meta.items()
            if values
        }

        missing = [key for key in ("title", "date", "summary") if not metadata.get(key)]
        if missing:
            missing_fields = ", ".join(missing)
            raise ValueError(f"{path}: missing note metadata: {missing_fields}")

        try:
            published = date.fromisoformat(metadata["date"])
        except ValueError as error:
            raise ValueError(f"{path}: date must use YYYY-MM-DD") from error

        title_cn = metadata.get("title-zh") or metadata.get("title_zh")
        summary_cn = metadata.get("summary-zh") or metadata.get("summary_zh")
        if not title_cn or not summary_cn:
            raise ValueError(f"{path}: missing Title-ZH or Summary-ZH metadata")

        tags = [tag.strip() for tag in metadata.get("tags", "").split(",") if tag.strip()]
        tags_cn = [
            tag.strip()
            for tag in (metadata.get("tags-zh") or metadata.get("tags_zh") or "").split(",")
            if tag.strip()
        ]
        if tags and not tags_cn:
            raise ValueError(f"{path}: Tags-ZH metadata is required when Tags is present")
        if len(tags_cn) != len(tags):
            raise ValueError(f"{path}: Tags and Tags-ZH must contain the same number of entries")

        chinese_converter = markdown.Markdown(extensions=["extra", "sane_lists"])
        body_html_cn = chinese_converter.convert(chinese_source)

        notes.append(
            {
                "slug": path.stem,
                "title": metadata["title"],
                "title_cn": title_cn,
                "summary": metadata["summary"],
                "summary_cn": summary_cn,
                "published": published,
                "date_iso": published.isoformat(),
                "date_label": f"{published.strftime('%B')} {published.day}, {published.year}",
                "date_label_cn": f"{published.year}年{published.month}月{published.day}日",
                "tags": tags,
                "tags_cn": tags_cn,
                "body_html": body_html,
                "body_html_cn": body_html_cn,
                "output": f"note-{path.stem}.html",
            }
        )

    return sorted(notes, key=lambda note: note["published"], reverse=True)


def load_publication_data() -> dict:
    """Load the last successful Google Scholar synchronization."""

    if not PUBLICATIONS_FILE.is_file():
        return {
            "profile_url": SITE["scholar"],
            "synced_at": None,
            "publications": [],
        }

    data = json.loads(PUBLICATIONS_FILE.read_text(encoding="utf-8"))
    if not isinstance(data.get("publications"), list):
        raise ValueError(f"Invalid publications cache: {PUBLICATIONS_FILE}")
    data.setdefault("profile_url", SITE["scholar"])
    return data


def clean_output() -> None:
    """Clear only the repository's known output directory, preserving CNAME."""

    if OUTPUT_DIR.parent != ROOT or OUTPUT_DIR.name != "docs":
        raise RuntimeError(f"Refusing to clean unexpected path: {OUTPUT_DIR}")

    cname = None
    cname_path = OUTPUT_DIR / "CNAME"
    if cname_path.exists():
        cname = cname_path.read_bytes()

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    if cname is not None:
        cname_path.write_bytes(cname)


def build() -> None:
    validate_translation_data()
    notes = load_notes()
    clean_output()

    shutil.copytree(STATIC_DIR, OUTPUT_DIR / "assets")
    shutil.copytree(FILES_DIR, OUTPUT_DIR / "files")

    environment = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    environment.globals["t"] = bilingual_text

    shared_context = {
        "site": SITE,
        "navigation": NAVIGATION,
        "current_questions": CURRENT_QUESTIONS,
        "poetry": POETRY,
        "social_links": SOCIAL_LINKS,
        "intro_paragraphs": INTRO_PARAGRAPHS,
        "education": EDUCATION,
        "research_interests": RESEARCH_INTERESTS,
        "research_directions": RESEARCH_DIRECTIONS,
        "packages": PACKAGES,
        "resource_tutorials": RESOURCE_TUTORIALS,
        "notes": notes,
        "latest_notes": notes[:5],
        "publication_data": load_publication_data(),
        "scholar_profile_url": SITE["scholar"],
        "tools": TOOLS,
        "activities": ACTIVITIES,
        "distinctions": DISTINCTIONS,
        "experience": EXPERIENCE,
        "about_items": ABOUT_ITEMS,
        "current_year": date.today().year,
        "base_url": BASE_URL,
    }

    for page in PAGES:
        template = environment.get_template(page["template"])
        rendered = template.render(**shared_context, page=page)
        (OUTPUT_DIR / page["output"]).write_text(rendered, encoding="utf-8")

    note_template = environment.get_template("note.html")
    note_pages = []
    for note in notes:
        page = {
            "output": note["output"],
            "active": "notes",
            "title": note["title"],
            "title_cn": note["title_cn"],
            "description": note["summary"],
            "description_cn": note["summary_cn"],
            "og_type": "article",
            "published_time": note["date_iso"],
            "is_note": True,
            "last_modified": note["date_iso"],
        }
        rendered = note_template.render(**shared_context, page=page, note=note)
        (OUTPUT_DIR / note["output"]).write_text(rendered, encoding="utf-8")
        note_pages.append(page)

    public_pages = [page for page in PAGES if page["output"] != "404.html"] + note_pages
    sitemap = environment.get_template("sitemap.xml").render(
        pages=public_pages,
        base_url=BASE_URL,
        last_modified=date.today().isoformat(),
    )
    (OUTPUT_DIR / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (OUTPUT_DIR / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / ".nojekyll").touch()

    print(f"Built {len(PAGES) + len(note_pages)} pages in {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
