import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.data.translations import TRANSLATIONS
from src.models import I18nStr, Resume

THEMES_DIR = Path("src/themes")
PARTIALS_DIR = Path("src/templates/partials")
SHARED_IMG_DIR = Path("src/static/img")
DEFAULT_THEME = "classic"


def list_themes() -> list[dict]:
    """Descubre los temas disponibles leyendo src/themes/*/theme.json."""
    themes = []
    for theme_file in sorted(THEMES_DIR.glob("*/theme.json")):
        meta = json.loads(theme_file.read_text())
        meta.setdefault("id", theme_file.parent.name)
        themes.append(meta)
    return themes


def _build_env(theme: str, lang: str) -> Environment:
    theme_templates = THEMES_DIR / theme / "templates"
    if not theme_templates.is_dir():
        available = ", ".join(t["id"] for t in list_themes()) or "ninguno"
        raise ValueError(f"Tema desconocido: {theme!r}. Disponibles: {available}")

    env = Environment(
        loader=FileSystemLoader([str(theme_templates), str(PARTIALS_DIR)]),
        autoescape=select_autoescape(["html"]),
    )
    # Resuelve un I18nStr al idioma que se está renderizando. Deja pasar
    # cualquier otro valor sin tocarlo, así los campos no traducidos
    # (nombres, fechas, URLs) también pueden llevar el filtro sin romperse.
    env.filters["loc"] = lambda value: value.get(lang) if isinstance(value, I18nStr) else value
    return env


def render_html(
    resume: Resume,
    lang: str = "en",
    theme: str = DEFAULT_THEME,
    static_prefix: str | None = None,
) -> str:
    """Renderiza el CV a un string. No toca el disco.

    `static_prefix` se calcula según el idioma para la salida en docs/, pero el
    editor lo fija a mano porque sirve el preview desde otra estructura de rutas.
    """
    if static_prefix is None:
        static_prefix = "" if lang == "en" else "../"

    env = _build_env(theme, lang)
    template = env.get_template("layout.html")
    return template.render(
        resume=resume,
        t=TRANSLATIONS[lang],
        lang=lang,
        theme=theme,
        static_prefix=static_prefix,
    )


def render_resume(
    resume: Resume,
    lang: str = "en",
    theme: str = DEFAULT_THEME,
    output_dir: str | Path = "docs",
    output_path: str | Path | None = None,
) -> Path:
    """Renderiza el CV en el idioma indicado y lo escribe en disco."""
    output_dir = Path(output_dir)
    if output_path is None:
        output_path = output_dir / "index.html" if lang == "en" else output_dir / lang / "index.html"

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(resume, lang=lang, theme=theme))
    return output


def copy_static_assets(theme: str = DEFAULT_THEME, output_dir: str | Path = "docs") -> None:
    """Copia el CSS del tema activo y las imágenes compartidas a la salida."""
    output_dir = Path(output_dir)

    css_dst = output_dir / "static" / "css" / "styles.css"
    css_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(THEMES_DIR / theme / "static" / "css" / "styles.css", css_dst)

    if SHARED_IMG_DIR.exists():
        shutil.copytree(SHARED_IMG_DIR, output_dir / "static" / "img", dirs_exist_ok=True)
