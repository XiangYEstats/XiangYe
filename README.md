# Xiang Ye — Southern Song scholar portfolio

This is a Python-generated static website for GitHub Pages. Python and Jinja
templates generate the final HTML in `docs/`; the browser then uses ordinary
HTML, CSS, and JavaScript. It does not require R, RStudio, a database, or a
JavaScript build system.

The design develops one coherent Southern Song visual language: Ru-ware
celadon, warm paper, ink, restrained cinnabar, moon-window geometry, guqin-line
rules, one-corner composition, generous negative space, and small bilingual
poetic marginalia. The poetry supports the scholarly identity without becoming
the primary content.

The published address remains:

<https://xiangyestats.github.io/XiangYe/>

## Open and run in VS Code

The commands below are for Linux/Fedora.

```bash
cd XiangYe-southern-song-python
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

The Publications page is populated from the public Google Scholar profile in
`site_data.py` → `SITE["scholar"]`. A GitHub Actions workflow checks the profile
daily at 03:17 UTC, rebuilds the site, and commits only when the publication
records change. Each publication title links to its individual Google Scholar
record.

To run the same synchronization locally before building:

```bash
python scripts/sync_scholar.py
python build.py
python validate.py
```

The last successful copy is stored in `data/publications.json`. The sync writes
that cache only after it has parsed a complete Scholar response, so a temporary
network error, rate limit, or CAPTCHA does not remove publications from the
live site.

Preview it locally:

```bash
python -m http.server 8000 --directory docs
```

Then open <http://localhost:8000>. Stop the preview with `Ctrl+C`.

VS Code also includes these shortcuts under `Terminal` → `Run Task`:

- `Website: Build`
- `Website: Preview`
- `Website: Validate`

## Where to edit

Most future updates need only one or two files:

| What you want to change | File or section |
| --- | --- |
| Name, role, email, links, biography | `site_data.py` → `SITE`, `INTRO_PARAGRAPHS` |
| Poems and English translations | `site_data.py` → `POETRY` |
| Homepage research questions | `site_data.py` → `CURRENT_QUESTIONS` |
| Education and research interests | `site_data.py` → `EDUCATION`, `RESEARCH_INTERESTS` |
| Research directions, projects, articles, tutorials, and direction websites | `site_data.py` → `RESEARCH_DIRECTIONS` |
| Packages and general tutorials | `site_data.py` → `PACKAGES`, `RESOURCE_TUTORIALS` |
| Notes | create Markdown files in `content/notes/` |
| Google Scholar profile used for Publications | `site_data.py` → `SITE["scholar"]` |
| Activities, prizes, and experience | `site_data.py` → `ACTIVITIES`, `DISTINCTIONS`, `EXPERIENCE` |
| Interests outside research | `site_data.py` → `ABOUT_ITEMS` |
| Page titles, large characters, placeholder notes | `build.py` → `PAGES` |
| Homepage structure | `templates/index.html` |
| Header, navigation, footer, seal character | `templates/base.html` |
| Research / Resources / Notes / Activity / About / Contact structure | matching file under `templates/` |
| Celadon, paper, ink, and cinnabar colours | top of `static/css/site.css` → `:root` |
| Spacing, typography, responsive layout | labelled sections in `static/css/site.css` |
| Theme toggle, like button, menu, reveal, portrait motion | `static/js/site.js` |
| Portrait | `static/images/profile.jpg` |
| Vertical Chinese-name calligraphy | `static/images/identity/xiang-ye-calligraphy.png` |
| CV | `files/cv.pdf` |

The templates and stylesheet contain comments marking the main design regions.
After any edit, rerun `python build.py`; do not edit `docs/` by hand because it
is regenerated.

## Add packages, tutorials, questions, and direction websites

All of these additions are made in `site_data.py`, followed by `python build.py`
and `python validate.py`.

Add a package to `PACKAGES`:

```python
PACKAGES = [
    {
        "name": "INLAcircular",
        "description": "A concise description of the package.",
        "href": "https://example.com/package",
        "language": "R",       # optional
        "status": "Active",    # optional
    },
]
```

Add a general tutorial to `RESOURCE_TUTORIALS`:

```python
RESOURCE_TUTORIALS = [
    {
        "title": "Tutorial title",
        "description": "A short explanation.",  # optional
        "href": "https://example.com/tutorial",
    },
]
```

For a direction-specific tutorial, find that item in `RESEARCH_DIRECTIONS` and
add records to its `tutorials` list. The Tutorials row appears only when that
list contains at least one item:

```python
"tutorials": [
    {
        "title": "Circular regression with INLA",
        "description": "A practical walkthrough.",  # optional
        "href": "https://example.com/tutorial",     # optional
    },
],
```

Set that direction's `href` to its future website URL. A small Website button
will then appear beside the direction title; leaving `href` as `None` keeps the
button hidden.

`CURRENT_QUESTIONS` works the same way. It is currently empty, so the entire
homepage panel is hidden. Add one or more strings and the heading and questions
will return automatically in the same position.

## Add a new note

Notes are ordinary Markdown files, similar to small blog posts:

1. Copy `content/notes/_template.md` to a lowercase, hyphenated filename such
   as `content/notes/a-note-on-priors.md`. Files beginning with `_` are ignored.
2. Edit the `Title`, `Date`, `Summary`, and optional comma-separated `Tags` at
   the top. Keep the date in `YYYY-MM-DD` format.
3. Write the note below the blank line using Markdown. To add an image, place it
   under `static/images/notes/` and reference it as
   `![Useful alternative text](assets/images/notes/image-name.png)`.
4. Run `python build.py` and `python validate.py`.

The Notes archive and individual note page are generated automatically. Notes
are sorted by date, and the newest five appear in the homepage Notes ribbon.
When there are no notes, both layouts remain in place without dummy entries.

The header heart remembers a visitor's choice in that browser. When the shared
counter below is connected, its number is the total across visitors rather than
a device-local number.

## Enable the shared website-like count

The static GitHub Pages site cannot write a shared number by itself. The
`like-counter/` folder contains a small Cloudflare Worker and D1 database for
the count. It stores a random browser identifier—not a name, email address, or
IP address—so the same browser contributes at most one active like.

1. Sign in to a Cloudflare account, then from `like-counter/` run
   `npx wrangler@latest login`.
2. Run `npx wrangler@latest d1 create xiangye-like-counter` and paste the
   returned database ID into `like-counter/wrangler.jsonc`.
3. Run `npx wrangler@latest d1 execute xiangye-like-counter --remote --file=schema.sql`.
4. Run `npx wrangler@latest deploy` and copy the resulting Worker address.
5. Add `/likes` to that address and paste it into `SITE["like_api_url"]` in
   `site_data.py`, then rebuild and validate the website.

The Worker accepts requests only from the published GitHub Pages origin and
uses a small burst limit. Like any anonymous public counter, it discourages
ordinary duplicate clicks but cannot prove that every browser belongs to a
different human.

## Site pages

- `index.html` — Home
- `research.html` — Research directions, projects, and related articles (`研`)
- `publications.html` — Publications synchronized from Google Scholar (`文`)
- `resources.html` — Packages and tutorials (`器`)
- `notes.html` — Notes and generated Markdown articles (`记`)
- `activity.html` — Activity (`行`)
- `about_me.html` — About Me (`闲`)
- `contact.html` — Contact (`信`)

The old public filenames remain unchanged so existing links keep working.

## Publish through the existing GitHub repository

1. Copy these project files into the root of the `XiangYe` repository, keeping
   the repository's existing `.git` folder.
2. Run `python build.py` and `python validate.py`.
3. Commit and push the source files together with the generated `docs/` folder.
4. In GitHub, open `Settings` → `Pages` and keep the source set to the `main`
   branch and `/docs` folder.

The build script preserves an existing `docs/CNAME` file when regenerating the
site.
