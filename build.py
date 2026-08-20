"""Build the static GitHub Pages website into ``docs/``."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

from site_data import (
    ABOUT_ITEMS,
    ACTIVITIES,
    DISTINCTIONS,
    EDUCATION,
    EXPERIENCE,
    INTRO_PARAGRAPHS,
    NAVIGATION,
    CURRENT_QUESTIONS,
    POETRY,
    RESEARCH_DIRECTIONS,
    RESEARCH_INTERESTS,
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
BASE_URL = "https://xiangyestats.github.io/XiangYe"


PAGES = [
    {
        "template": "index.html",
        "output": "index.html",
        "active": "home",
        "title": "Home",
        "description": SITE["description"],
    },
    {
        "template": "research.html",
        "output": "research.html",
        "active": "research",
        "title": "Research",
        "description": "Research directions, projects, and related articles by Xiang Ye.",
        "mark": "研",
        "verse": "research_precision",
    },
    {
        "template": "publications.html",
        "output": "publications.html",
        "active": "publications",
        "title": "Publications",
        "description": "Publications by Xiang Ye, synchronized from Google Scholar.",
        "mark": "文",
        "verse": "writing",
    },
    {
        "template": "activity.html",
        "output": "activity.html",
        "active": "activity",
        "title": "Activity",
        "description": "Research activities and distinctions of Xiang Ye.",
        "mark": "行",
        "verse": "wide_roads",
    },
    {
        "template": "about.html",
        "output": "about_me.html",
        "active": "about",
        "title": "About Me",
        "description": "A little more about Xiang Ye beyond research.",
        "mark": "闲",
        "verse": "wide_reading",
    },
    {
        "template": "contact.html",
        "output": "contact.html",
        "active": "contact",
        "title": "Contact",
        "description": "Contact Xiang Ye about research and collaboration.",
        "mark": "信",
        "verse": "kindred_minds",
    },
    {
        "template": "404.html",
        "output": "404.html",
        "active": "",
        "title": "Page not found",
        "description": "The requested page could not be found.",
    },
]


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
    clean_output()

    shutil.copytree(STATIC_DIR, OUTPUT_DIR / "assets")
    shutil.copytree(FILES_DIR, OUTPUT_DIR / "files")

    environment = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

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

    public_pages = [page for page in PAGES if page["output"] != "404.html"]
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

    print(f"Built {len(PAGES)} pages in {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
