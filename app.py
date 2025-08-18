import json
import os
import shutil
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Dict, Any, Literal

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_cors import CORS
from flask.wrappers import Response
from dotenv import load_dotenv

from src.models import Resume
from src.render import render_resume_with_template
from src.template_manager import TemplateManager

load_dotenv()

app: Flask = Flask(__name__,
           template_folder='app/templates',
           static_folder='app/static')
CORS(app)

template_manager: TemplateManager = TemplateManager()

@app.route('/')
def index() -> str:
    """Main page with CV editor interface"""
    templates = template_manager.get_available_templates()
    return render_template('index.html', templates=templates)

@app.route('/api/templates')
def get_templates() -> Response:

    return jsonify(template_manager.get_available_templates())

@app.route('/api/preview', methods=['POST'])
def preview_cv() -> Response | tuple[Response, Literal[400]]:

    try:
        data: Any | None = request.json
        if not data:
            return jsonify({
            'success': False,
            'error': "No se recibio data"
        }), 400
        resume_data: dict = data.get('resume_data')
        template_name: str = data.get('template', 'classic')

        resume: Resume = Resume(**resume_data)

        html_content: str = render_resume_with_template(resume, template_name)

        return jsonify({
            'success': True,
            'html': html_content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/download-project', methods=['POST'])
def download_project() -> Response | tuple[Response, Literal[400]]:

    try:
        data = request.json
        if not data:
            return jsonify({
            'success': False,
            'error': "No se recibio data"
        }), 400
        resume_data: Dict = data.get('resume_data')
        template_name: str = data.get('template', 'classic')
        project_name: str = data.get('project_name', 'my-cv-project')

        resume: Resume = Resume(**resume_data)

        temp_dir: Path = Path(f'/tmp/{project_name}')
        temp_dir.mkdir(exist_ok=True)

        project_zip: BytesIO = create_project_package(resume, template_name, project_name, temp_dir)

        return send_file(
            project_zip,
            as_attachment=True,
            download_name=f'{project_name}.zip',
            mimetype='application/zip'
        )

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/export-pdf', methods=['POST'])
def export_pdf() -> Response | tuple[Response, Literal[400]]:
    """Export CV as PDF"""
    try:
        data: Any | None = request.json
        if not data:
            return jsonify({
            'success': False,
            'error': "No se recibio data"
        }), 400

        resume_data: Dict = data.get('resume_data')
        template_name: str = data.get('template', 'classic')

        resume: Resume = Resume(**resume_data)

        pdf_buffer: BytesIO = generate_pdf(resume, template_name)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name='resume.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def create_project_package(resume: Resume, template_name: str, project_name: str, temp_dir: Path) -> BytesIO:
    """Create a complete project package for download"""

    project_dir: Path = temp_dir / project_name
    project_dir.mkdir(exist_ok=True)

    base_files: list[str] = [
        'main.py',
        'requirements.txt',
        'LICENSE',
    ]

    for file in base_files:
        if Path(file).exists():
            shutil.copy(file, project_dir / file)

    src_dir: Path = project_dir / 'src'
    src_dir.mkdir(exist_ok=True)

    shutil.copytree('src/models.py', src_dir / 'models.py', dirs_exist_ok=True)
    shutil.copytree('src/logging_config.py', src_dir / 'logging_config.py', dirs_exist_ok=True)

    data_dir: Path = src_dir / 'data'
    data_dir.mkdir(exist_ok=True)

    with open(data_dir / 'resume.json', 'w', encoding='utf-8') as f:
        json.dump(resume.model_dump(), f, indent=2, ensure_ascii=False)

    template_dir: Path = src_dir / 'templates'
    template_dir.mkdir(exist_ok=True)

    template_path: Path = template_manager.get_template_path(template_name)
    shutil.copytree(template_path, template_dir, dirs_exist_ok=True)

    static_dir: Path = src_dir / 'static'
    template_static: Path = template_manager.get_template_static_path(template_name)
    if template_static.exists():
        shutil.copytree(template_static, static_dir, dirs_exist_ok=True)

    create_render_file(src_dir, template_name)

    create_project_readme(project_dir, project_name, template_name)

    zip_buffer: BytesIO = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in project_dir.rglob('*'):
            if file_path.is_file():
                arcname: Path = file_path.relative_to(temp_dir)
                zip_file.write(file_path, arcname)

    zip_buffer.seek(0)

    shutil.rmtree(temp_dir)

    return zip_buffer

def create_render_file(src_dir: Path, template_name: str) -> None:
    """Create a simplified render.py file for the user's project"""
    render_content = f'''import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.models import Resume

def render_resume(resume: Resume, output_path="docs/index.html"):
    """Render resume using the {template_name} template"""
    env = Environment(loader=FileSystemLoader("src/templates"))
    template = env.get_template("layout.html")
    rendered_html = template.render(resume=resume)

    # Write HTML
    Path(output_path).write_text(rendered_html, encoding='utf-8')

    # Copy CSS
    css_src = Path("src/static/css")
    css_dst = Path("docs/static/css")
    if css_src.exists():
        css_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(css_src, css_dst, dirs_exist_ok=True)

    # Copy images
    img_src = Path("src/static/img")
    img_dst = Path("docs/static/img")
    if img_src.exists():
        shutil.copytree(img_src, img_dst, dirs_exist_ok=True)
'''

    with open(src_dir / 'render.py', 'w', encoding='utf-8') as f:
        f.write(render_content)

def create_project_readme(project_dir: Path, project_name: str, template_name: str) -> None:
    """Create README for the user's project"""
    readme_content: str = f'''# {project_name}

This is your personalized CV project generated from the CV Builder tool.

## Template Used
- **{template_name.title()}**: A professional CV template

## How to Use

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Customize Your Data
Edit `src/data/resume.json` with your personal information.

### 3. Generate Your CV
```bash
python main.py
```

This will generate your CV as `docs/index.html`.

### 4. Deploy to GitHub Pages

1. Create a new repository on GitHub
2. Push this code to your repository
3. Go to Settings > Pages
4. Select "Deploy from a branch"
5. Choose "main" branch and "/docs" folder
6. Your CV will be available at `https://yourusername.github.io/repository-name`

## File Structure

- `src/data/resume.json` - Your CV data
- `src/templates/` - HTML templates
- `src/static/` - CSS and images
- `docs/` - Generated website files
- `main.py` - Main script to generate CV

## Customization

You can modify the template files in `src/templates/` and styles in `src/static/css/` to customize the appearance of your CV.

Generated by CV Builder - https://github.com/AndresKenji/andreskenji.github.io
'''

    with open(project_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

def generate_pdf(resume: Resume, template_name: str) -> BytesIO:

    try:
        import weasyprint

        html_content: str = render_resume_with_template(resume, template_name)

        pdf_buffer: BytesIO = BytesIO()
        weasyprint.HTML(string=html_content).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)

        return pdf_buffer
    except ImportError:
        raise Exception("WeasyPrint is required for PDF generation. Please install it.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
