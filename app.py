import json
import os
import shutil
import zipfile
from pathlib import Path
from typing import Dict, Any
from io import BytesIO

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv

from src.models import Resume
from src.render import render_resume_with_template
from src.template_manager import TemplateManager

# Load environment variables
load_dotenv()

app = Flask(__name__,
           template_folder='app/templates',
           static_folder='app/static')
CORS(app)

# Initialize template manager
template_manager = TemplateManager()

@app.route('/')
def index():
    """Main page with CV editor interface"""
    templates = template_manager.get_available_templates()
    return render_template('index.html', templates=templates)

@app.route('/api/templates')
def get_templates():
    """API endpoint to get available templates"""
    return jsonify(template_manager.get_available_templates())

@app.route('/api/preview', methods=['POST'])
def preview_cv():
    """Generate preview of CV with selected template"""
    try:
        data = request.json
        resume_data = data.get('resume_data')
        template_name = data.get('template', 'classic')

        # Validate resume data
        resume = Resume(**resume_data)

        # Generate HTML
        html_content = render_resume_with_template(resume, template_name)

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
def download_project():
    """Generate and download complete project with user's data"""
    try:
        data = request.json
        resume_data = data.get('resume_data')
        template_name = data.get('template', 'classic')
        project_name = data.get('project_name', 'my-cv-project')

        # Validate resume data
        resume = Resume(**resume_data)

        # Create temporary directory for project
        temp_dir = Path(f'/tmp/{project_name}')
        temp_dir.mkdir(exist_ok=True)

        # Generate project files
        project_zip = create_project_package(resume, template_name, project_name, temp_dir)

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
def export_pdf():
    """Export CV as PDF"""
    try:
        data = request.json
        resume_data = data.get('resume_data')
        template_name = data.get('template', 'classic')

        # Validate resume data
        resume = Resume(**resume_data)

        # Generate PDF
        pdf_buffer = generate_pdf(resume, template_name)

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

    # Create project structure
    project_dir = temp_dir / project_name
    project_dir.mkdir(exist_ok=True)

    # Copy base project files
    base_files = [
        'main.py',
        'requirements.txt',
        'LICENSE',
    ]

    for file in base_files:
        if Path(file).exists():
            shutil.copy(file, project_dir / file)

    # Create src directory structure
    src_dir = project_dir / 'src'
    src_dir.mkdir(exist_ok=True)

    # Copy source files
    shutil.copytree('src/models.py', src_dir / 'models.py', dirs_exist_ok=True)
    shutil.copytree('src/logging_config.py', src_dir / 'logging_config.py', dirs_exist_ok=True)

    # Create data directory and save user's resume
    data_dir = src_dir / 'data'
    data_dir.mkdir(exist_ok=True)

    with open(data_dir / 'resume.json', 'w', encoding='utf-8') as f:
        json.dump(resume.model_dump(), f, indent=2, ensure_ascii=False)

    # Copy selected template
    template_dir = src_dir / 'templates'
    template_dir.mkdir(exist_ok=True)

    template_path = template_manager.get_template_path(template_name)
    shutil.copytree(template_path, template_dir, dirs_exist_ok=True)

    # Copy static files for the template
    static_dir = src_dir / 'static'
    template_static = template_manager.get_template_static_path(template_name)
    if template_static.exists():
        shutil.copytree(template_static, static_dir, dirs_exist_ok=True)

    # Create render.py adapted for single template
    create_render_file(src_dir, template_name)

    # Create README for the user
    create_project_readme(project_dir, project_name, template_name)

    # Create ZIP file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in project_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(temp_dir)
                zip_file.write(file_path, arcname)

    zip_buffer.seek(0)

    # Clean up temp directory
    shutil.rmtree(temp_dir)

    return zip_buffer

def create_render_file(src_dir: Path, template_name: str):
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

def create_project_readme(project_dir: Path, project_name: str, template_name: str):
    """Create README for the user's project"""
    readme_content = f'''# {project_name}

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
    """Generate PDF from resume data"""
    try:
        import weasyprint

        html_content = render_resume_with_template(resume, template_name)

        # Create PDF
        pdf_buffer = BytesIO()
        weasyprint.HTML(string=html_content).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)

        return pdf_buffer
    except ImportError:
        raise Exception("WeasyPrint is required for PDF generation. Please install it.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
