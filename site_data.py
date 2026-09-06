"""Editable content for the Xiang Ye personal website.

Most routine text changes can be made in this file without touching the HTML
templates.  Run ``python build.py`` after editing to regenerate ``docs/``.
"""

SITE = {
    "name": "Xiang Ye",
    "name_cn": "叶翔",
    "role": "PhD Candidate",
    "role_cn": "统计学博士研究生",
    "affiliation": "King Abdullah University of Science and Technology (KAUST)",
    "affiliation_cn": "阿卜杜拉国王科技大学（KAUST）",
    "group": "Bayesian Computational Statistics and Modeling Research Group",
    "group_cn": "贝叶斯计算统计与建模研究组",
    "supervisor": "Professor Håvard Rue",
    "supervisor_cn": "Håvard Rue 教授",
    "email": "xiang.ye@kaust.edu.sa",
    "location": "Thuwal, Saudi Arabia",
    "location_cn": "沙特阿拉伯图瓦勒",
    "office": "Building 1, King Abdullah University of Science and Technology (KAUST)",
    "office_cn": "阿卜杜拉国王科技大学（KAUST）1号楼",
    "description": (
        "Bayesian computational statistician working on latent variable models, "
        "principled priors, directional statistics, and scalable inference with INLA."
    ),
    "description_cn": (
        "专注于贝叶斯计算统计，研究方向包括潜变量模型、有理论依据的先验构建、"
        "方向统计，以及基于 INLA 的可扩展推断。"
    ),
    "github": "https://github.com/XiangYEstats",
    "scholar": "https://scholar.google.com/citations?user=08io_8cAAAAJ&hl=en&oi=sra",
    "researchgate": "https://www.researchgate.net/profile/Xiang-Ye-16?ev=hdr_xprf",
    "linkedin": "https://www.linkedin.com/in/xiang-ye-228648191/",
}

NAVIGATION = [
    {"key": "home", "label": "Home", "label_cn": "首页", "href": "index.html"},
    {"key": "research", "label": "Research", "label_cn": "研究", "href": "research.html"},
    {
        "key": "publications",
        "label": "Publications",
        "label_cn": "学术论文",
        "href": "publications.html",
    },
    {"key": "resources", "label": "Resources", "label_cn": "资源", "href": "resources.html"},
    {"key": "notes", "label": "Notes", "label_cn": "随笔", "href": "notes.html"},
    {"key": "activity", "label": "Activity", "label_cn": "学术活动", "href": "activity.html"},
    {"key": "about", "label": "About", "label_cn": "研究之外", "href": "about_me.html"},
    {"key": "contact", "label": "Contact", "label_cn": "联系", "href": "contact.html"},
]

SOCIAL_LINKS = [
    {"label": "Email", "label_cn": "邮箱", "href": f"mailto:{SITE['email']}", "external": False},
    {"label": "GitHub", "label_cn": "GitHub", "href": SITE["github"], "external": True},
    {
        "label": "Google Scholar",
        "label_cn": "Google Scholar",
        "href": SITE["scholar"],
        "external": True,
    },
    {
        "label": "ResearchGate",
        "label_cn": "ResearchGate",
        "href": SITE["researchgate"],
        "external": True,
    },
    {"label": "LinkedIn", "label_cn": "LinkedIn", "href": SITE["linkedin"], "external": True},
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

# Add questions here as ``{"text": "...", "text_cn": "..."}`` records. The
# entire homepage panel is hidden while this list is empty.
CURRENT_QUESTIONS = []

INTRO_PARAGRAPHS = [
    {
        "text": (
            "I am a PhD candidate in the Bayesian Computational Statistics and "
            "Modeling Research Group at King Abdullah University of Science and "
            "Technology (KAUST), under the supervision of Professor Håvard Rue."
        ),
        "text_cn": (
            "我目前在阿卜杜拉国王科技大学（KAUST）攻读统计学博士学位，"
            "师从 Håvard Rue 教授，并在贝叶斯计算统计与建模研究组开展研究。"
        ),
    },
    {
        "text": (
            "My PhD research focuses on Bayesian latent variable models and joint modelling, from "
            "prior specification and model construction to computation and "
            "applications. I develop these ideas for directional and circular "
            "statistics and implement the resulting methodology for Integrated "
            "Nested Laplace Approximation (INLA)."
        ),
        "text_cn": (
            "我的博士研究围绕贝叶斯潜变量模型与联合建模展开，涵盖先验设定、模型构建、"
            "计算方法与实际应用。我将这些思想应用于方向统计与圆周统计，并在集成嵌套"
            "拉普拉斯近似（INLA）框架下实现相应方法。"
        ),
    },
    {
        "text": (
            "Looking ahead, I am interested in the theory, methodology, and "
            "applications of fast Bayesian inference, particularly for increasingly "
            "complex and high-dimensional models. I am also interested in bringing "
            "Bayesian ideas into modern deep learning, especially generative models, "
            "to improve uncertainty quantification and computational efficiency, while "
            "encouraging more structured, transparent, and reliable reasoning."
        ),
        "text_cn": (
            "未来，我希望继续探索快速贝叶斯推断的理论、方法与应用，尤其关注日益复杂的"
            "高维模型。我也期待将贝叶斯思想融入现代深度学习，特别是生成模型，在提升"
            "计算效率的同时，更好地量化不确定性，让推理过程更有条理、更透明、更可靠。"
        ),
    },
]
EDUCATION = [
    {
        "degree": "PhD in Statistics",
        "degree_cn": "统计学博士",
        "institution": "King Abdullah University of Science and Technology",
        "institution_cn": "阿卜杜拉国王科技大学",
        "place": "Jeddah, Saudi Arabia",
        "place_cn": "沙特阿拉伯吉达",
        "years": "2023—2026",
    },
    {
        "degree": "MSc in Statistics",
        "degree_cn": "统计学硕士",
        "institution": "Lancaster University",
        "institution_cn": "兰卡斯特大学",
        "place": "Lancaster, United Kingdom",
        "place_cn": "英国兰卡斯特",
        "years": "2021—2022",
    },
    {
        "degree": "BSc in Applied Mathematics",
        "degree_cn": "应用数学学士",
        "institution": "University of Liverpool & Xi’an Jiaotong-Liverpool University",
        "institution_cn": "利物浦大学与西交利物浦大学",
        "place": "Suzhou, China",
        "place_cn": "中国苏州",
        "years": "2017—2021",
    },
]

RESEARCH_INTERESTS = [
    {
        "number": "01",
        "title": "Scalable probabilistic modeling",
        "title_cn": "可扩展概率建模",
        "text": (
            "Structured latent representations and hierarchical Bayesian models "
            "for high-dimensional data."
        ),
        "text_cn": "面向高维数据，研究结构化潜在表示与层次贝叶斯模型。",
    },
    {
        "number": "02",
        "title": "Bayesian deep learning",
        "title_cn": "贝叶斯深度学习",
        "text": (
            "Bayesian principles for accurate, efficient, and statistically robust "
            "neural learning methods."
        ),
        "text_cn": "将贝叶斯原理融入神经网络，探索准确、高效且具统计稳健性的学习方法。",
    },
    {
        "number": "03",
        "title": "Principled prior specification",
        "title_cn": "有理论依据的先验设定",
        "text": (
            "Prior constructions that improve model stability, interpretability, "
            "and inferential accuracy."
        ),
        "text_cn": "构建有助于提升模型稳定性、可解释性与推断精度的先验分布。",
    },
    {
        "number": "04",
        "title": "Uncertainty quantification",
        "title_cn": "不确定性量化",
        "text": (
            "Frameworks for model and predictive uncertainty and better calibration in "
            "complex systems."
        ),
        "text_cn": "研究模型与预测不确定性的量化方法，并提升复杂系统中的预测校准度。",
    },
    {
        "number": "05",
        "title": "Directional statistics",
        "title_cn": "方向统计",
        "text": (
            "Statistical methodology for circular, spherical, and other "
            "manifold-valued observations."
        ),
        "text_cn": "针对圆周、球面及其他流形值观测的统计方法。",
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
        "summary_cn": (
            "围绕圆周数据及含方向分量的模型，研究贝叶斯方法，涵盖有理论依据的先验设定、"
            "模型构建、高效计算与可复用的软件工具。"
        ),
        "href": "https://xiangyestats.github.io/directional-statistics/",
        "projects": [
            {
                "number": "01",
                "title": "Circular PC priors",
                "title_cn": "圆周模型的 PC 先验",
                "text": (
                    "Principled, interpretable prior distributions for the "
                    "parameters of circular models."
                ),
                "text_cn": "为圆周模型参数构建兼具理论依据与可解释性的先验分布。",
                "href": None,
            },
            {
                "number": "02",
                "title": "Joint circular regressions",
                "title_cn": "联合圆周回归",
                "text": (
                    "Latent-variable regression frameworks that connect circular "
                    "and linear variables while carrying uncertainty through the "
                    "joint model."
                ),
                "text_cn": (
                    "通过潜变量回归框架联合建模圆周变量与线性变量，并在联合模型中完整传播不确定性。"
                ),
                "href": None,
            },
            {
                "number": "03",
                "title": "R package INLAcircular",
                "title_cn": "R 软件包 INLAcircular",
                "text": (
                    "Accessible implementations of circular regression and joint "
                    "models using Integrated Nested Laplace Approximation."
                ),
                "text_cn": (
                    "基于 INLA，为圆周回归与联合模型提供易于使用的软件实现。"
                ),
                "href": "https://github.com/XiangYEstats/INLAcircular",
                "link_label": "GitHub",
                "link_label_cn": "GitHub 仓库",
            },
        ],
        "articles": [
            {
                "year": "2026",
                "title": "Penalizing complexity priors for Bayesian inference of circular models",
                "authors": "Ye, X., Van Niekerk, J., & Rue, H.",
                "venue": "Statistical Modelling, 1471082X261453677.",
                "href": "https://journals.sagepub.com/doi/full/10.1177/1471082X261453677",
            },
            {
                "year": "2026",
                "title": "A Bayesian regression framework for circular models with INLA",
                "authors": "Ye, X., Van Niekerk, J., & Rue, H.",
                "venue": "arXiv preprint arXiv:2602.08413.",
                "href": "https://arxiv.org/abs/2602.08413",
            },
        ],
        "tutorials": [
            {
                "title": "Circular models in Stan",
                "title_cn": "圆周模型的 Stan 实现",
                "description": "Tutorials on implementing Bayesian circular models with Stan.",
                "description_cn": "使用 Stan 实现贝叶斯圆周模型的教程。",
                "href": "https://xiangyestats.github.io/directional-statistics/tutorials/",
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# RESOURCES PAGE
# ---------------------------------------------------------------------------
# Packages are the main focus of the Resources page. Add one dictionary per
# package; ``href`` should point to its documentation, repository, or website.
# Add ``description_cn`` and, when applicable, ``status_cn`` for the Chinese
# view. ``language`` and package names remain in their official form.
PACKAGES = []

# These are general tutorials that do not belong to one research direction.
# Add ``title_cn`` and ``description_cn`` to each record. Direction-specific
# tutorials should instead be added to the matching research direction above.
RESOURCE_TUTORIALS = []

TOOLS = ["R", "INLA", "Stan", "Python", "C++", "MATLAB"]

ACTIVITIES = [
    {
        "year": "2026",
        "items": [
            {
                "type": "Conference poster presentation",
                "type_cn": "会议海报展示",
                "title": "A Bayesian Regression Framework for Circular Models",
                "event": "ISBA Conference 2026",
                "place": "Nagoya, Japan",
                "place_cn": "日本名古屋",
                "date": "28 June-3 July",
                "date_cn": "6月28日至7月3日",
            },
            {
                "type": "Conference poster presentation",
                "type_cn": "会议海报展示",
                "title": "A Bayesian Regression Framework for Circular Models",
                "event": "NORDSTAT Conference 2026",
                "place": "Helsinki, Finland",
                "place_cn": "芬兰赫尔辛基",
                "date": "1—4 June",
                "date_cn": "6月1日至4日",
            },
            {
                "type": "Research visit",
                "type_cn": "学术访问",
                "title": "Bayesian inference and computation for circular models",
                "event": "Aalto University research visit",
                "place": "Espoo, Finland",
                "place_cn": "芬兰埃斯波",
                "date": "2 May—6 June",
                "date_cn": "5月2日至6月6日",
            },
        ],
    },
    {
        "year": "2025",
        "items": [
            {
                "type": "Workshop poster presentation",
                "type_cn": "研讨会海报展示",
                "title": "Bayesian Regression Framework for Models with Circular Components",
                "event": (
                    "KAUST Statistics Workshop — Statistics for Learning from Complex "
                    "Data: Foundations and Applications"
                ),
                "place": "Thuwal, Saudi Arabia",
                "place_cn": "沙特阿拉伯图瓦勒",
                "date": "2—6 November",
                "date_cn": "11月2日至6日",
            },
            {
                "type": "Conference poster presentation",
                "type_cn": "会议海报展示",
                "title": "Principled priors for Bayesian inference of circular models",
                "event": "Objective Bayes Methodology Conference",
                "place": "Athens, Greece",
                "place_cn": "希腊雅典",
                "date": "6—12 June",
                "date_cn": "6月6日至12日",
            },
            {
                "type": "Workshop poster presentation",
                "type_cn": "研讨会海报展示",
                "title": "Principled priors for Bayesian inference of circular models",
                "event": "INLA: past, present, and future",
                "place": "Glasgow, United Kingdom",
                "place_cn": "英国格拉斯哥",
                "date": "21—23 May",
                "date_cn": "5月21日至23日",
            },
        ],
    },
    {
        "year": "2024",
        "items": [
            {
                "type": "Workshop poster presentation",
                "type_cn": "研讨会海报展示",
                "title": "Principled priors for Bayesian inference of circular models",
                "event": (
                    "KAUST Statistics Workshop — Statistics for Learning from Complex "
                    "Data: Foundations and Applications"
                ),
                "place": "Thuwal, Saudi Arabia",
                "place_cn": "沙特阿拉伯图瓦勒",
                "date": "17—21 November",
                "date_cn": "11月17日至21日",
            },
            {
                "type": "Summer school",
                "type_cn": "暑期学校",
                "title": "",
                "event": "VIBASS7 — València International Bayesian Summer School",
                "place": "València, Spain",
                "place_cn": "西班牙瓦伦西亚",
                "date": "8—12 July",
                "date_cn": "7月8日至12日",
            },
        ],
    },
    {
        "year": "2023",
        "items": [
            {
                "type": "Workshop",
                "type_cn": "研讨会",
                "title": "",
                "event": (
                    "KAUST Statistics Workshop — Frontier Statistics & Data Science "
                    "for a Sustainable World"
                ),
                "place": "Thuwal, Saudi Arabia",
                "place_cn": "沙特阿拉伯图瓦勒",
                "date": "17—21 November",
                "date_cn": "11月17日至21日",
            }
        ],
    },
]

DISTINCTIONS = [
    {
        "year": "2022",
        "title": "Master Dissertation Award",
        "title_cn": "硕士学位论文奖",
        "text": (
            "Department Prize for Best Computational Dissertation for “Spatial "
            "Statistical Modeling with INLA”."
        ),
        "text_cn": "凭借学位论文《Spatial Statistical Modeling with INLA》获系内最佳计算类论文奖。",
    },
    {
        "year": "2020",
        "title": "Meritorious Winner & Student Advisor",
        "title_cn": "优异奖得主兼学生顾问",
        "text": "Mathematical Contest in Modeling (MCM).",
        "text_cn": "美国大学生数学建模竞赛（MCM）。",
    },
    {
        "year": "2017—2019",
        "title": "Excellent Team Member",
        "title_cn": "优秀团队成员",
        "text": "ENACTUS.",
        "text_cn": "ENACTUS。",
    },
]

EXPERIENCE = [
    {
        "role": "Research and Development Intern",
        "role_cn": "研发实习生",
        "organisation": "Tech View Info Limited Liability Company",
        "organisation_cn": "和元达信息科技有限公司",
        "place": "Guangzhou, China",
        "place_cn": "中国广州",
        "year": "2023",
    },
    {
        "role": "Project Marketing Intern",
        "role_cn": "项目营销实习生",
        "organisation": "Guangdong Zhujiang Investment Co. Ltd.",
        "organisation_cn": "广东珠江投资股份有限公司",
        "place": "Guangzhou, China",
        "place_cn": "中国广州",
        "year": "2019",
    },
]

ABOUT_ITEMS = [
    {
        "mark": "游",
        "title": "Sports",
        "title_cn": "运动",
        "text": (
            "I enjoy football, basketball, and table tennis. Swimming is my "
            "favourite sport, and I practise it weekly."
        ),
        "text_cn": "平时喜欢足球、篮球和乒乓球，最喜欢游泳，也保持每周游泳的习惯。",
    },
    {
        "mark": "艺",
        "title": "Arts",
        "title_cn": "绘画",
        "text": (
            "I enjoy drawing. In 2011, I received First Class Prize at the National "
            "Drawing Contest for Middle School Students of China—an early chapter "
            "I remember fondly."
        ),
        "text_cn": (
            "喜欢画画。2011年曾在全国中学生绘画比赛中获得一等奖，"
            "算是一件有趣的往事。"
        ),
    },
    {
        "mark": "乐",
        "title": "Music",
        "title_cn": "音乐",
        "text": (
            "I enjoy music and singing. I have learned violin, piano, and saxophone, "
            "and taught myself the Chinese bamboo flute."
        ),
        "text_cn": "喜欢音乐和唱歌，学过小提琴、钢琴和萨克斯，也自学过洞箫。",
    },
    {
        "mark": "读",
        "title": "Reading",
        "title_cn": "阅读",
        "text": (
            "I enjoy reading, with The Count of Monte Cristo and One Hundred Years "
            "of Solitude among my favourites."
        ),
        "text_cn": "喜欢读书，《基督山伯爵》和《百年孤独》是其中两部最喜欢的作品。",
    },
    {
        "mark": "弈",
        "title": "Games",
        "title_cn": "游戏",
        "text": (
            "I enjoy competitive MOBA and FPS games, including League of Legends "
            "and Counter-Strike, especially their teamwork and strategy."
        ),
        "text_cn": (
            "喜欢玩《英雄联盟》和《反恐精英》等 MOBA 和 FPS 游戏，"
            "也喜欢和队友配合、研究战术。"
        ),
    },
    {
        "mark": "味",
        "title": "Cooking",
        "title_cn": "做饭",
        "text": (
            "I enjoy cooking many kinds of Chinese dishes and experimenting with "
            "new cuisines."
        ),
        "text_cn": "喜欢做饭，常做各种中式菜，也喜欢尝试不同菜系。",
    },
]
