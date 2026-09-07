# Xiang Ye — Maintenance notes

[Back to the repository overview](README.md).

Python and Jinja build the static site in `docs/`, which is served by GitHub
Pages. The frontend uses HTML, CSS, and JavaScript.

Website: <https://xiangyestats.github.io/XiangYe/>

The site defaults to English and remembers the reader's language choice.
The `中文` / `EN` switch covers page text, metadata, and accessibility labels;
bilingual headings and poems stay in both languages. The build checks required
Chinese translations before replacing `docs/`.

## Local setup

The commands below are for Linux/Fedora.

```bash
cd /home/xiang/websites/XiangYe
code .
```

Create the Python environment once:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Build and validate the site:

```bash
python build.py
python validate.py
```

The Publications page uses the Google Scholar profile in
`site_data.py` → `SITE["scholar"]`. GitHub Actions checks it daily at 03:17 UTC,
rebuilds the site, and commits when publication records change. Publication
titles link to their Google Scholar records.

To run the same synchronization locally before building:

```bash
python scripts/sync_scholar.py
python build.py
python validate.py
```

The cache in `data/publications.json` is updated only after a complete Scholar
response has been parsed. Network errors, rate limits, and CAPTCHAs leave the
cached records in place.

Preview it locally:

```bash
python -m http.server 8000 --directory docs
```

Then open <http://localhost:8000>. Stop the preview with `Ctrl+C`.

In VS Code, use `Terminal` → `Run Task`:

- `Website: Build`
- `Website: Preview`
- `Website: Validate`

## Where to edit

| What you want to change | File or section |
| --- | --- |
| Name, role, email, links, biography, Chinese copy | `site_data.py` → `SITE`, `INTRO_PARAGRAPHS` |
| Poems and English translations | `site_data.py` → `POETRY` |
| Homepage research questions | `site_data.py` → `CURRENT_QUESTIONS` |
| Education and research interests | `site_data.py` → `EDUCATION`, `RESEARCH_INTERESTS` |
| Research directions, projects, articles, tutorials, and direction websites | `site_data.py` → `RESEARCH_DIRECTIONS` |
| Packages and the Resources tutorial index | `site_data.py` → `PACKAGES`, `RESOURCE_TUTORIALS` |
| Notes | create Markdown files in `content/notes/` |
| Google Scholar profile used for Publications | `site_data.py` → `SITE["scholar"]` |
| Activities, prizes, and experience | `site_data.py` → `ACTIVITIES`, `DISTINCTIONS`, `EXPERIENCE` |
| Interests outside research | `site_data.py` → `ABOUT_ITEMS` |
| Page titles, character labels, and descriptions | `build.py` → `PAGES` |
| Homepage structure | `templates/index.html` |
| Header, navigation, footer, seal character | `templates/base.html` |
| Research / Resources / Notes / Activity / About / Contact structure | matching file under `templates/` |
| Colours | top of `static/css/site.css` → `:root` |
| Spacing, typography, responsive layout | labelled sections in `static/css/site.css` |
| Language/theme toggles, menu, reveal, portrait motion | `static/js/site.js` |
| Portrait | `static/images/profile.jpg` |
| Homepage background image | `static/images/decoration/song-shoreline.webp` |
| Portrait border and decorative dots | `.moon-window` and `.qin-lines` in `static/css/site.css` |
| Vertical Chinese-name calligraphy | `static/images/identity/xiang-ye-calligraphy.png` |
| CV | `files/cv.pdf` |

Run `python build.py` after editing source files. Do not edit `docs/` by hand;
the next build will overwrite it.

### Homepage background

The background image is `static/images/decoration/song-shoreline.webp`.
Its opacity and dark-mode styling are set in `static/css/site.css`.

## Add packages, tutorials, questions, and direction websites

Edit `site_data.py`, then run `python build.py` and `python validate.py`.

Add a package to `PACKAGES`:

```python
PACKAGES = [
    {
        "name": "INLAcircular",
        "description": "Package description.",
        "description_cn": "软件包的简洁中文说明。",
        "href": "https://example.com/package",
        "language": "R",       # optional
        "status": "Active",    # optional
        "status_cn": "维护中", # optional
    },
]
```

Add a tutorial to the Resources page through `RESOURCE_TUTORIALS`:

```python
RESOURCE_TUTORIALS = [
    {
        "title": "Tutorial title",
        "title_cn": "教程标题",
        "description": "A short explanation.",  # optional
        "description_cn": "简短的中文说明。",    # optional
        "href": "https://example.com/tutorial",
    },
]
```

To list a tutorial under a research direction, add it to that direction's
`tutorials` list in `RESEARCH_DIRECTIONS`. Empty lists are hidden:

```python
"tutorials": [
    {
        "title": "Circular regression with INLA",
        "title_cn": "使用 INLA 进行圆周回归",
        "description": "A practical walkthrough.",  # optional
        "description_cn": "一份实用的中文指南。",    # optional
        "href": "https://example.com/tutorial",     # optional
    },
],
```

Set the direction's `href` to its website URL to show a Website link beside the
title. Use `None` to hide it.

Add English and Chinese entries to `CURRENT_QUESTIONS` to show research
questions on the homepage. The section is hidden when the list is empty:

```python
CURRENT_QUESTIONS = [
    {
        "text": "Research question.",
        "text_cn": "研究问题。",
    },
]
```

## Add a new note

Notes are Markdown files in `content/notes/`.

1. Copy `content/notes/_template.md` to a lowercase, hyphenated filename such
   as `content/notes/a-note-on-priors.md`. Files beginning with `_` are ignored.
2. Edit the paired `Title` / `Title-ZH`, `Summary` / `Summary-ZH`, optional
   comma-separated `Tags` / `Tags-ZH`, and `Date` fields at the top. Keep the
   date in `YYYY-MM-DD` format.
3. Write the English note below the metadata and the Chinese note below the
   `<!-- zh-Hans -->` marker. Both bodies use Markdown. To add an image, place it
   under `static/images/notes/` and reference it as
   `![Useful alternative text](assets/images/notes/image-name.png)`.
4. Run `python build.py` and `python validate.py`.

The build creates the Notes archive and individual pages, sorted by date.
The latest five notes appear on the homepage. Empty archives display no entries.

## Site pages

- `index.html` — Home
- `research.html` — Research directions, projects, and related articles (`研`)
- `publications.html` — Publications synchronized from Google Scholar (`文`)
- `resources.html` — Packages and tutorials (`器`)
- `notes.html` — Notes and generated Markdown articles (`记`)
- `activity.html` — Activity (`行`)
- `about_me.html` — About Me (`闲`)
- `contact.html` — Contact (`信`)

Keep these filenames when editing pages so existing links continue to work.

## Publish

1. Copy these project files into the root of the `XiangYe` repository, keeping
   the repository's existing `.git` folder.
2. Run `python build.py` and `python validate.py`.
3. Commit and push the source files together with the generated `docs/` folder.
4. In GitHub, open `Settings` → `Pages` and keep the source set to the `main`
   branch and `/docs` folder.

The build script preserves an existing `docs/CNAME` file when regenerating the
site.
