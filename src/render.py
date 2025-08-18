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

def render_resume_to_pdf(
    resume: Resume,
    template_name: str = "creative_pro",
    output_path: str = "docs/resume.pdf"
) -> None:
    """
    Genera un PDF directamente desde HTML usando Playwright.
    Playwright renderiza exactamente como Chrome, preservando todos los estilos.
    """
    # Cargar el template
    env: Environment = Environment(loader=FileSystemLoader("src/templates"))
    template: Template = env.get_template(template_name + ".html")

    # Renderizar HTML con los datos del resume
    html_content: str = template.render(resume=resume)

    # Crear el directorio de salida si no existe
    output_file: Path = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Crear archivo temporal HTML
    temp_html = Path("temp_resume.html")
    temp_html.write_text(html_content, encoding='utf-8')

    try:
        from playwright.sync_api import sync_playwright

        logger.info(f"Generating PDF with Playwright: {output_path}")

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            page.goto(f"file://{temp_html.absolute()}")
            page.wait_for_load_state('networkidle')

            page.pdf(
                path=output_path,
                format='A4',
                margin={
                    'top': '0',
                    'right': '0',
                    'bottom': '0',
                    'left': '0'
                },
                print_background=True,  # Incluir colores y gradientes
                prefer_css_page_size=True
            )

            browser.close()

        logger.info(f"PDF generated successfully with Playwright: {output_path}")

    except ImportError:
        logger.error("Playwright not installed. Install with: pip install playwright")
        logger.error("Then run: playwright install chromium")
        raise
    except Exception as e:
        logger.error(f"Error generating PDF with Playwright: {e}")
        logger.error("Make sure to run 'playwright install chromium' after installing playwright")
        raise
    finally:
        if temp_html.exists():
            temp_html.unlink()

