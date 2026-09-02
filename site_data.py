"""Editable content for the Xiang Ye personal website.

Most routine text changes can be made in this file without touching the HTML
templates.  Run ``python build.py`` after editing to regenerate ``docs/``.
"""

SITE = {
    "name": "Xiang Ye",
    "name_cn": "叶翔",
    "role": "PhD Candidate",
    "affiliation": "King Abdullah University of Science and Technology (KAUST)",
    "group": "Bayesian Computational Statistics and Modeling Research Group",
    "supervisor": "Professor Håvard Rue",
    "email": "xiang.ye@kaust.edu.sa",
    "location": "Thuwal, Saudi Arabia",
    "office": "Building 1, King Abdullah University of Science and Technology (KAUST)",
    "description": (
        "Bayesian computational statistician working on latent variable models, "
        "principled priors, directional statistics, and scalable inference with INLA."
    ),
    "github": "https://github.com/XiangYEstats",
    "scholar": "https://scholar.google.com/citations?user=08io_8cAAAAJ&hl=en&oi=sra",
    "linkedin": "https://www.linkedin.com/in/xiang-ye-228648191/",
    # After deploying the small counter in ``like-counter/``, paste its
    # public ``/likes`` endpoint here. An empty value keeps the heart local.
    "like_api_url": "",
}

NAVIGATION = [
    {"key": "home", "label": "Home", "href": "index.html"},
    {"key": "research", "label": "Research", "href": "research.html"},
    {"key": "publications", "label": "Publications", "href": "publications.html"},
    {"key": "resources", "label": "Resources", "href": "resources.html"},
    {"key": "notes", "label": "Notes", "href": "notes.html"},
    {"key": "activity", "label": "Activity", "href": "activity.html"},
    {"key": "about", "label": "About", "href": "about_me.html"},
    {"key": "contact", "label": "Contact", "href": "contact.html"},
]

SOCIAL_LINKS = [
    {"label": "Email", "href": f"mailto:{SITE['email']}", "external": False},
    {"label": "GitHub", "href": SITE["github"], "external": True},
    {"label": "Google Scholar", "href": SITE["scholar"], "external": True},
    {"label": "LinkedIn", "href": SITE["linkedin"], "external": True},
]

# ---------------------------------------------------------------------------
# POETRY & SCHOLARLY MARGINALIA
# ---------------------------------------------------------------------------
# These verses appear as quiet decoration throughout the site.  To change a
# Chinese line, its English rendering, or its attribution, edit only this
# dictionary and rebuild the website with ``python build.py``.
#
# The translations are interpretive rather than word-for-word: they preserve
# the thought and cadence of the originals while reading naturally in English.
POETRY = {
    "motto": {
        "chinese": "志存高远，脚踏实地",
        "english": "Aim high, stay grounded.",
        "source": "Personal motto",
    },
    # Homepage hero
    "living_source": {
        "chinese_lines": [
            "问渠哪得清如许？",
            "为有源头活水来。",
        ],
        "english_lines": [
            "How does the channel stay so clear?",
            "From its living source, fresh waters appear.",
        ],
        "source": "Zhu Xi · 朱熹 · 《观书有感二首·其一》",
    },
    # Homepage About-me card
    "wide_reading": {
        "chinese": ("海不辞水，故能成其大；山不辞土石，故能成其高。"),
        "english": (
            "No water is refused, and the sea grows wide; "
            "no earth or stone is spurned, and the mountain rises high."
        ),
        "source": "Guanzi · 《管子·形势解》",
    },
    # About page — 余白
    "about_growth": {
        "chinese_lines": [
            "博观而约取，",
            "厚积而薄发。",
        ],
        "english_lines": [
            "Range widely, choose with care;",
            "gather deeply, and let achievement ripen in its time.",
        ],
        "source": "Su Shi · 苏轼 · 《稼说送张琥》",
    },
    # Research page
    "research_precision": {
        "chinese_lines": [
            "致广大而尽精微。",
        ],
        "english_lines": [
            "Embrace the vast; pursue the finest detail.",
        ],
        "source": "The Doctrine of the Mean · 《礼记·中庸》",
    },
    # Resources page
    "tools_for_work": {
        "chinese_lines": [
            "工欲善其事，",
            "必先利其器。",
        ],
        "english_lines": [
            "To do good work,",
            "one must first sharpen one's tools.",
        ],
        "source": "Confucius · 孔子 · 《论语·卫灵公》",
    },
    # Notes page
    "notes_and_writing": {
        "chinese_lines": [
            "读书破万卷，",
            "下笔如有神。",
        ],
        "english_lines": [
            "Read through ten thousand volumes;",
            "then the brush moves as if inspired.",
        ],
        "source": "Du Fu · 杜甫 · 《奉赠韦左丞丈二十二韵》",
    },
    # Education
    "long_road": {
        "chinese_lines": [
            "路漫漫其修远兮，",
            "吾将上下而求索。",
        ],
        "english_lines": [
            "The road is long, its reaches far;",
            "still I shall seek where answers are.",
        ],
        "source": "Qu Yuan · 屈原 · 《离骚》",
    },
    # Publications
    "writing": {
        "chinese_lines": [
            "奇文共欣赏，",
            "疑义相与析。",
        ],
        "english_lines": [
            "Fine works we share in common delight;",
            "subtle questions we examine and bring to light.",
        ],
        "source": "Tao Yuanming · 陶渊明 · 《移居二首·其一》",
    },
    # Contact
    "kindred_minds": {
        "chinese_lines": [
            "海内存知己，",
            "天涯若比邻。",
        ],
        "english_lines": [
            "A kindred mind within the seas",
            "makes farthest shores feel near with ease.",
        ],
        "source": "Wang Bo · 王勃 · 《送杜少府之任蜀州》",
    },
    # Activity
    "wide_roads": {
        "chinese_lines": [
            "读万卷书，",
            "行万里路。",
        ],
        "english_lines": [
            "Read ten thousand volumes; journey ten thousand miles;",
            "knowledge grows on pages, and along the roads beneath wide skies.",
        ],
        "source": "Dong Qichang · 董其昌 · 《画禅室随笔·卷二》",
    },
    # Professional experience
    "practice": {
        "chinese_lines": [
            "纸上得来终觉浅，",
            "绝知此事要躬行。",
        ],
        "english_lines": [
            "What books alone can teach remains but shallow;",
            "true understanding comes through practice.",
        ],
        "source": "Lu You · 陆游 · 《冬夜读书示子聿》",
    },
}

# Add questions here whenever they are ready.  The entire homepage panel is
# hidden while this list is empty and appears automatically after the rebuild.
CURRENT_QUESTIONS = []

INTRO_PARAGRAPHS = [
    (
        "I am a PhD candidate in the Bayesian Computational Statistics and "
        "Modeling Research Group at King Abdullah University of Science and "
        "Technology (KAUST), under the supervision of Professor Håvard Rue."
    ),
    (
        "My PhD research focuses on Bayesian latent variable models and joint modelling, from "
        "prior specification and model construction to computation and "
        "applications. I develop these ideas for directional and circular "
        "statistics and implement the resulting methodology for Integrated "
        "Nested Laplace Approximation (INLA)."
    ),
    (
        "Looking ahead, I am interested in the theory, methodology, and "
        "applications of fast Bayesian inference, particularly for increasingly "
        "complex and high-dimensional models. I am also interested in bringing "
        "Bayesian ideas into modern deep learning, especially generative models, "
        "to improve uncertainty quantification and computational efficiency, while "
        "encouraging more structured, transparent, and reliable reasoning."
    ),
]
EDUCATION = [
    {
        "degree": "PhD in Statistics",
        "institution": "King Abdullah University of Science and Technology",
        "place": "Jeddah, Saudi Arabia",
        "years": "2023—2026",
    },
    {
        "degree": "MSc in Statistics",
        "institution": "Lancaster University",
        "place": "Lancaster, United Kingdom",
        "years": "2021—2022",
    },
    {
        "degree": "BSc in Applied Mathematics",
        "institution": "University of Liverpool & Xi’an Jiaotong-Liverpool University",
        "place": "Suzhou, China",
        "years": "2017—2021",
    },
]

RESEARCH_INTERESTS = [
    {
        "number": "01",
        "title": "Scalable probabilistic modeling",
        "text": (
            "Structured latent representations and hierarchical Bayesian models "
            "for high-dimensional data."
        ),
    },
    {
        "number": "02",
        "title": "Bayesian deep learning",
        "text": (
            "Bayesian principles for accurate, efficient, and statistically robust "
            "neural learning methods."
        ),
    },
    {
        "number": "03",
        "title": "Principled prior specification",
        "text": (
            "Prior constructions that improve model stability, interpretability, "
            "and inferential accuracy."
        ),
    },
    {
        "number": "04",
        "title": "Uncertainty quantification",
        "text": (
            "Frameworks for model and predictive uncertainty and better calibration in "
            "complex systems."
        ),
    },
    {
        "number": "05",
        "title": "Directional statistics",
        "text": (
            "Statistical methodology for circular, spherical, and other "
            "manifold-valued observations."
        ),
    },
]

# ---------------------------------------------------------------------------
# RESEARCH PAGE
# ---------------------------------------------------------------------------
# Each item below is one research-direction window. Add a URL to ``href`` when
# its dedicated website is ready; a compact "Website" button then appears next
# to the direction title. Related papers can be added to ``articles`` and
# optional learning material can be added to ``tutorials``. Each record accepts
# an optional ``href``; entries without one remain readable, non-clickable text.
RESEARCH_DIRECTIONS = [
    {
        "number": "01",
        "mark": "向",
        "title": "Directional Statistics",
        "title_cn": "方向统计",
        "summary": (
            "Bayesian methodology for circular observations and models with "
            "directional components, from principled prior specification, model construction "
            "to fast computation and reusable software."
        ),
        "href": None,
        "projects": [
            {
                "number": "01",
                "title": "Circular PC priors",
                "text": (
                    "Principled, interpretable prior distributions for the "
                    "parameters of circular models."
                ),
                "href": None,
            },
            {
                "number": "02",
                "title": "Joint circular regressions",
                "text": (
                    "Latent-variable regression frameworks that connect circular "
                    "and linear variables while carrying uncertainty through the "
                    "joint model."
                ),
                "href": None,
            },
            {
                "number": "03",
                "title": "R package INLAcircular",
                "text": (
                    "Accessible implementations of circular regression and joint "
                    "models using Integrated Nested Laplace Approximation."
                ),
                "href": None,
            },
        ],
        "articles": [],
        "tutorials": [
            {
                "title": "A first look at circular data",
                "description": (
                    "Temporary preview entry; the complete tutorial and its "
                    "materials will be linked here later."
                ),
                "href": None,
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# RESOURCES PAGE
# ---------------------------------------------------------------------------
# Packages are the main focus of the Resources page.  Add one dictionary per
# package; ``href`` should point to its documentation, repository, or website.
# ``language`` and ``status`` are optional short labels.
PACKAGES = []

# These are general tutorials that do not belong to one research direction.
# Direction-specific tutorials should instead be added to the matching
# ``RESEARCH_DIRECTIONS`` item above.
RESOURCE_TUTORIALS = []

TOOLS = ["R", "INLA", "Stan", "Python", "C++", "MATLAB"]

ACTIVITIES = [
    {
        "year": "2026",
        "items": [
            {
                "type": "Conference poster presentation",
                "title": "A Bayesian Regression Framework for Circular Models",
                "event": "ISBA Conference 2026",
                "place": "Nagoya, Japan",
                "date": "28 June-3 July",
            },
            {
                "type": "Conference poster presentation",
                "title": "A Bayesian Regression Framework for Circular Models",
                "event": "NORDSTAT Conference 2026",
                "place": "Helsinki, Finland",
                "date": "1—4 June",
            },
            {
                "type": "Research visit",
                "title": "Bayesian inference and computation for circular models",
                "event": "Aalto University research visit",
                "place": "Espoo, Finland",
                "date": "2 May—6 June",
            },
        ],
    },
    {
        "year": "2025",
        "items": [
            {
                "type": "Workshop poster presentation",
                "title": "Bayesian Regression Framework for Models with Circular Components",
                "event": (
                    "KAUST Statistics Workshop — Statistics for Learning from Complex "
                    "Data: Foundations and Applications"
                ),
                "place": "Thuwal, Saudi Arabia",
                "date": "2—6 November",
            },
            {
                "type": "Conference poster presentation",
                "title": "Principled priors for Bayesian inference of circular models",
                "event": "Objective Bayes Methodology Conference",
                "place": "Athens, Greece",
                "date": "6—12 June",
            },
            {
                "type": "Workshop poster presentation",
                "title": "Principled priors for Bayesian inference of circular models",
                "event": "INLA: past, present, and future",
                "place": "Glasgow, United Kingdom",
                "date": "21—23 May",
            },
        ],
    },
    {
        "year": "2024",
        "items": [
            {
                "type": "Workshop poster presentation",
                "title": "Principled priors for Bayesian inference of circular models",
                "event": (
                    "KAUST Statistics Workshop — Statistics for Learning from Complex "
                    "Data: Foundations and Applications"
                ),
                "place": "Thuwal, Saudi Arabia",
                "date": "17—21 November",
            },
            {
                "type": "Summer school",
                "title": "",
                "event": "VIBASS7 — València International Bayesian Summer School",
                "place": "València, Spain",
                "date": "8—12 July",
            },
        ],
    },
    {
        "year": "2023",
        "items": [
            {
                "type": "Workshop",
                "title": "",
                "event": (
                    "KAUST Statistics Workshop — Frontier Statistics & Data Science "
                    "for a Sustainable World"
                ),
                "place": "Thuwal, Saudi Arabia",
                "date": "17—21 November",
            }
        ],
    },
]

DISTINCTIONS = [
    {
        "year": "2022",
        "title": "Master Dissertation Award",
        "text": (
            "Department Prize for Best Computational Dissertation for “Spatial "
            "Statistical Modeling with INLA”."
        ),
    },
    {
        "year": "2020",
        "title": "Meritorious Winner & Student Advisor",
        "text": "Mathematical Contest in Modeling (MCM).",
    },
    {
        "year": "2017—2019",
        "title": "Excellent Team Member",
        "text": "ENACTUS.",
    },
]

EXPERIENCE = [
    {
        "role": "Research and Development Intern",
        "organisation": "Tech View Info Limited Liability Company",
        "place": "Guangzhou, China",
        "year": "2023",
    },
    {
        "role": "Project Marketing Intern",
        "organisation": "Guangdong Zhujiang Investment Co. Ltd.",
        "place": "Guangzhou, China",
        "year": "2019",
    },
]

ABOUT_ITEMS = [
    {
        "mark": "游",
        "title": "Sports",
        "text": (
            "I enjoy football, basketball, and table tennis. Swimming is my "
            "favourite sport, and I practise it weekly."
        ),
    },
    {
        "mark": "艺",
        "title": "Arts",
        "text": (
            "I enjoy drawing. In 2011, I received First Class Prize at the National "
            "Drawing Contest for Middle School Students of China—an early chapter "
            "I remember fondly."
        ),
    },
    {
        "mark": "乐",
        "title": "Music",
        "text": (
            "I enjoy music and singing. I have learned violin, piano, and saxophone, "
            "and taught myself the Chinese bamboo flute."
        ),
    },
    {
        "mark": "读",
        "title": "Reading",
        "text": (
            "I enjoy reading, with The Count of Monte Cristo and One Hundred Years "
            "of Solitude among my favourites."
        ),
    },
    {
        "mark": "弈",
        "title": "Games",
        "text": (
            "I enjoy competitive MOBA and FPS games, including League of Legends "
            "and Counter-Strike, especially their teamwork and strategy."
        ),
    },
    {
        "mark": "味",
        "title": "Cooking",
        "text": (
            "I enjoy cooking many kinds of Chinese dishes and experimenting with "
            "new cuisines."
        ),
    },
]
