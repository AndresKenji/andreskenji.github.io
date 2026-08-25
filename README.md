# andreskenji.github.io

Generador de CV bilingüe (EN/ES) con editor local. El contenido vive como datos
validados en `src/data/resume.json`, Jinja2 los renderiza con el tema activo y
GitHub Pages publica el resultado.

Este repo es a la vez el CV de Oscar A. Rodriguez y una plantilla reutilizable:
si quieres el tuyo, salta a [Úsalo para tu propio CV](#úsalo-para-tu-propio-cv).

## Editar el CV

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m src.editor
```

Abre `http://127.0.0.1:8000`: formulario a la izquierda, vista previa real del CV
a la derecha. Los campos traducidos se editan en **EN y ES lado a lado**, así no
hay forma de que los idiomas se desincronicen.

Los cambios viven en memoria como *borrador* — `src/data/resume.json` solo se
toca al pulsar **Guardar**, que además regenera `docs/`. Después:

```bash
git add src/data/resume.json && git commit -m "..." && git push
```

El push dispara el workflow y redespliega el sitio.

## Úsalo para tu propio CV

1. Pulsa **«Use this template» → Create a new repository** en GitHub. Eso crea un
   repo nuevo **sin el historial de commits** de este, así no te llevas datos
   ajenos ni siquiera en el pasado de git.
   Si prefieres clonar o hacer fork, funciona igual, pero el historial viaja
   contigo.

2. Deja el repo en su punto de partida:

   ```bash
   python -m scripts.reset
   ```

   Reemplaza el CV por el de ejemplo (`src/data/resume.example.json`, que
   ejercita las 12 secciones), restaura `config.json`, borra las fotos personales
   dejando `src/static/img/avatar.svg`, y elimina el `docs/` generado.
   Es destructivo sobre el árbol de trabajo, no sobre git: `git checkout --
   src/data src/static` lo revierte.

3. Edita, guarda y publica:

   ```bash
   pip install -r requirements-dev.txt
   python -m src.editor
   ```

   Sube tu foto a `src/static/img/` y apunta ahí el campo **Foto**.

4. En **Settings → Pages**, pon *Source* en **«GitHub Actions»**. Luego renombra
   el repo a `<tu-usuario>.github.io` si quieres que sea tu sitio principal.

> Si `src/data/resume.json` no existe, el generador cae al CV de ejemplo. El repo
> recién clonado funciona sin configurar nada.

## Estructura

| Ruta | Qué es |
|---|---|
| `src/data/resume.json` | El CV. Los campos traducidos son `{"en": ..., "es": ...}`; un string plano significa "igual en ambos idiomas". |
| `src/data/resume.example.json` | CV de ejemplo. Punto de partida y fallback. |
| `src/data/config.json` | Tema activo e idiomas a generar. |
| `src/models.py` | Esquema Pydantic. `I18nStr` marca los campos traducibles. |
| `src/render.py` | Renderizado. Registra el filtro Jinja `loc`, que resuelve un `I18nStr` al idioma en curso. |
| `src/themes/<id>/` | Un tema: `theme.json`, `templates/`, `static/css/styles.css`. |
| `src/templates/partials/` | Macros compartidos entre temas. |
| `src/static/img/` | Imágenes, compartidas por todos los temas. |
| `src/editor/` | El editor local (FastAPI + JS sin build step). |
| `scripts/reset.py` | Deja el repo listo para un CV nuevo. |
| `docs/` | Salida generada. **No se versiona.** |

## Construir sin el editor

```bash
pip install -r requirements.txt
python main.py     # genera docs/
```

`requirements.txt` son solo Jinja2 y Pydantic — es lo que instala el CI. FastAPI
y uvicorn viven en `requirements-dev.txt` porque solo los necesita el editor.

## Agregar un tema

1. `src/themes/<id>/theme.json` con `id`, `name` y `description`.
2. `src/themes/<id>/templates/layout.html` (más los includes que quieras).
3. `src/themes/<id>/static/css/styles.css`.

Aparece solo en el selector del editor. Los templates reciben `resume`, `t`
(traducciones de UI), `lang`, `theme` y `static_prefix`, y disponen del filtro
`loc` y de los macros de `src/templates/partials/macros.html`.

Se publica únicamente el tema indicado en `config.json`.

## Despliegue

`.github/workflows/deploy.yml` construye el sitio y lo sube como artifact de
GitHub Pages. Requiere que en **Settings → Pages** la fuente sea
**«GitHub Actions»** (no «Deploy from a branch»).
