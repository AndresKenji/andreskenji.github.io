import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.models import Resume

def render_resume(resume: Resume, output_path="docs/index.html"):
    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("layout.html")
    rendered_html = template.render(resume=resume)

    # Escribe el HTML
    Path(output_path).write_text(rendered_html)

    # Copiar el CSS
    css_src = Path("src/static/css/styles.css")
    css_dst = Path("docs/static/css/styles.css")
    css_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(css_src, css_dst)
    # Copiar imágenes
    img_src = Path("src/static/img")
    img_dst = Path("docs/static/img")
    if img_src.exists():
        shutil.copytree(img_src, img_dst, dirs_exist_ok=True)

