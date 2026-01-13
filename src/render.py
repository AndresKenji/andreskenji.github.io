import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.models import Resume
from src.data.translations import TRANSLATIONS


def render_resume(resume: Resume, lang: str = "en", output_path: str = None):
    """Renderiza el CV en el idioma especificado."""

    if output_path is None:
        output_path = "docs/index.html" if lang == "en" else "docs/es/index.html"

    static_prefix = "" if lang == "en" else "../"

    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("layout.html")

    rendered_html = template.render(
        resume=resume,
        t=TRANSLATIONS[lang],
        static_prefix=static_prefix
    )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered_html)

    if lang == "en":
        _copy_static_assets()


def _copy_static_assets():
    """Copia CSS e imágenes a docs/static/"""
    css_src = Path("src/static/css/styles.css")
    css_dst = Path("docs/static/css/styles.css")
    css_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(css_src, css_dst)

    img_src = Path("src/static/img")
    img_dst = Path("docs/static/img")
    if img_src.exists():
        shutil.copytree(img_src, img_dst, dirs_exist_ok=True)
