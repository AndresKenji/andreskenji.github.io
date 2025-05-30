from jinja2 import Environment, FileSystemLoader
from src.models import Resume
from pathlib import Path

def render_resume(resume: Resume, output_path="docs/index.html"):
    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("resume.html")
    rendered_html = template.render(resume=resume)
    Path(output_path).write_text(rendered_html)

