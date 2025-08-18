import logging
import shutil

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template

from src.models import Resume
from src.template_manager import TemplateManager
from src.logging_config import setup_logger

logger: logging.Logger = setup_logger(
    name="cv_creator",
    level=logging.INFO,
    format_string='%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    include_file_handler=False,
)

def render_resume(
    resume: Resume,
    output_path="docs/index.html",
    template_name: str = "classic",
    ) -> None:

    env: Environment = Environment(loader=FileSystemLoader("src/templates"))
    template: Template = env.get_template(template_name + ".html")
    rendered_html: str = template.render(resume=resume)

    Path(output_path).write_text(rendered_html, encoding='utf-8')

    css_src: Path = Path("src/static/css/styles.css")
    css_dst: Path = Path("docs/static/css/styles.css")
    css_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(css_src, css_dst)

    img_src: Path = Path("src/static/img")
    img_dst: Path = Path("docs/static/img")
    if img_src.exists():
        shutil.copytree(img_src, img_dst, dirs_exist_ok=True)

def render_resume_with_template(resume: Resume, template_name: str = "classic") -> str:
    template_manager: TemplateManager = TemplateManager()

    if not template_manager.template_exists(template_name):
        return render_resume_legacy(resume)

    try:
        env: Environment = template_manager.get_template_environment(template_name)
        template: Template = env.get_template("layout.html")
        html_content: str = template.render(resume=resume)

        css_path: Path = Path(f"app/cv-templates/{template_name}/static/css/styles.css")
        if css_path.exists():
            css_content: str = css_path.read_text(encoding='utf-8')
            html_content = html_content.replace(
                '<link rel="stylesheet" href="static/css/styles.css">',
                f'<style>{css_content}</style>'
            )

        return html_content
    except Exception as e:
        logger.error(f"Error rendering template {template_name}: {e}")
        return render_resume_legacy(resume)

def render_resume_legacy(resume: Resume) -> str:
    env: Environment = Environment(loader=FileSystemLoader("src/templates"))
    template: Template = env.get_template("layout.html")
    return template.render(resume=resume)

