"""Editor local del CV.

Levanta un servidor en localhost con un formulario a la izquierda y un preview
real del CV a la derecha. Los cambios viven en memoria como *borrador* hasta que
se pulsa Guardar: hasta ese momento `src/data/resume.json` no se toca y el
`git status` sigue limpio.
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

import main as builder
from src.models import Fluency, Resume, SkillLevel, StudyType
from src.render import THEMES_DIR, list_themes, render_html
from src.storage import (
    RESUME_PATH,
    is_example_data,
    load_config,
    load_resume_dict,
    resume_to_dict,
    save_config,
    save_resume,
)

EDITOR_DIR = Path(__file__).parent
SHARED_IMG_DIR = Path("src/static/img")

app = FastAPI(title="Resume Editor", docs_url=None, redoc_url=None)
app.mount("/assets", StaticFiles(directory=EDITOR_DIR / "static"), name="assets")
app.mount("/preview/static/img", StaticFiles(directory=SHARED_IMG_DIR), name="preview-img")


class Draft:
    """Estado en memoria del borrador. Un solo usuario, un solo proceso."""

    def __init__(self):
        self.data = load_resume_dict()
        self.dirty = False

    def set(self, data: dict) -> Resume:
        resume = Resume.model_validate(data)  # lanza ValidationError si no cuadra
        self.data = data
        self.dirty = resume_to_dict(resume) != load_resume_dict()
        return resume

    def resume(self) -> Resume:
        return Resume.model_validate(self.data)


draft = Draft()


def validation_response(exc: ValidationError) -> JSONResponse:
    """Traduce los errores de Pydantic a algo que el formulario pueda anclar."""
    return JSONResponse(
        status_code=422,
        content={
            "errors": [
                {"path": [str(p) for p in err["loc"]], "message": err["msg"]}
                for err in exc.errors()
            ]
        },
    )


@app.get("/", response_class=HTMLResponse)
def index():
    return (EDITOR_DIR / "templates" / "editor.html").read_text()


@app.get("/api/schema")
def schema():
    """Valores de los enums, para poblar los <select> del formulario."""
    return {
        "study_type": [e.value for e in StudyType],
        "skill_level": [e.value for e in SkillLevel],
        "fluency": [e.value for e in Fluency],
        "languages": load_config()["languages"],
    }


@app.get("/api/resume")
def get_resume():
    return {
        "resume": draft.data,
        "dirty": draft.dirty,
        "is_example": is_example_data(),
        "path": str(RESUME_PATH),
    }


@app.put("/api/draft")
def put_draft(payload: dict):
    try:
        draft.set(payload)
    except ValidationError as exc:
        return validation_response(exc)
    return {"ok": True, "dirty": draft.dirty}


@app.get("/api/themes")
def get_themes():
    return {"themes": list_themes(), "active": load_config()["theme"]}


def resolve_theme(theme: str) -> str:
    """Valida el tema pedido y cae al configurado si no viene ninguno."""
    theme = theme or load_config()["theme"]
    if not (THEMES_DIR / theme / "templates").is_dir():
        raise HTTPException(status_code=404, detail=f"Tema desconocido: {theme}")
    return theme


@app.put("/api/config")
def put_config(payload: dict):
    theme = payload.get("theme")
    if theme and not (THEMES_DIR / theme).is_dir():
        raise HTTPException(status_code=400, detail=f"Tema desconocido: {theme}")
    save_config({k: v for k, v in payload.items() if k in ("theme", "default_language")})
    return load_config()


@app.post("/api/save")
def save():
    """Escribe el borrador a disco y regenera docs/."""
    try:
        resume = draft.resume()
    except ValidationError as exc:
        return validation_response(exc)

    save_resume(resume)
    builder.build()
    draft.data = load_resume_dict()
    draft.dirty = False

    config = load_config()
    written = [str(RESUME_PATH)] + [
        f"docs/index.html" if lang == "en" else f"docs/{lang}/index.html"
        for lang in config["languages"]
    ]
    return {
        "ok": True,
        "written": written,
        "theme": config["theme"],
        "is_example": is_example_data(),
    }


@app.get("/preview/static/css/styles.css")
def preview_css(theme: str = ""):
    css = THEMES_DIR / resolve_theme(theme) / "static" / "css" / "styles.css"
    if not css.exists():
        raise HTTPException(status_code=404, detail=f"Tema sin CSS: {theme}")
    # El navegador no debe cachear el CSS: cambia al cambiar de tema.
    return FileResponse(css, media_type="text/css", headers={"Cache-Control": "no-store"})


@app.get("/preview/{lang}/", response_class=HTMLResponse)
def preview(lang: str, theme: str = ""):
    config = load_config()
    if lang not in config["languages"]:
        raise HTTPException(status_code=404, detail=f"Idioma no configurado: {lang}")
    theme = resolve_theme(theme)

    try:
        resume = draft.resume()
    except ValidationError:
        # El preview no debe romperse mientras se escribe: se cae al último
        # estado guardado en disco y el formulario ya muestra los errores.
        resume = Resume.model_validate(load_resume_dict())

    html = render_html(resume, lang=lang, theme=theme, static_prefix="../")
    # El switcher de idioma del tema apunta a rutas de docs/, que no existen
    # aquí. El editor tiene su propio selector, así que se esconde.
    html += "<style>.lang-switcher{display:none !important}</style>"
    return HTMLResponse(html, headers={"Cache-Control": "no-store"})
