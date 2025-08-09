import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.models import Resume
from src.template_manager import TemplateManager

def render_resume(resume: Resume, output_path="docs/index.html"):
    """Render resume using the default template"""
    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("layout.html")
    rendered_html = template.render(resume=resume)

    # Write HTML
    Path(output_path).write_text(rendered_html, encoding='utf-8')

    # Copy CSS
    css_src = Path("src/static/css/styles.css")
    css_dst = Path("docs/static/css/styles.css")
    css_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(css_src, css_dst)

    # Copy images
    img_src = Path("src/static/img")
    img_dst = Path("docs/static/img")
    if img_src.exists():
        shutil.copytree(img_src, img_dst, dirs_exist_ok=True)

def render_resume_with_template(resume: Resume, template_name: str = "classic") -> str:
    """Render resume with a specific template and return HTML string"""
    template_manager = TemplateManager()

    if not template_manager.template_exists(template_name):
        # Fallback to classic template or use the old method
        return render_resume_legacy(resume)

    try:
        env = template_manager.get_template_environment(template_name)
        template = env.get_template("layout.html")
        return template.render(resume=resume)
    except Exception as e:
        print(f"Error rendering template {template_name}: {e}")
        return render_resume_legacy(resume)

def render_resume_legacy(resume: Resume) -> str:
    """Legacy render method for backward compatibility"""
    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("layout.html")
    return template.render(resume=resume)

