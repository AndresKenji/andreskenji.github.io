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
from pydantic import ValidationError

from src.models import Resume
from src.render import render_resume, render_resume_to_pdf
from src.template_manager import TemplateManager


load_dotenv()

# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).parent.parent.parent
TEMPLATE_DIR = BASE_DIR / "src" / "app" / "templates"
STATIC_DIR = BASE_DIR / "src" / "app" / "static"

app: Flask = Flask(__name__,
                   template_folder=str(TEMPLATE_DIR),
                   static_folder=str(STATIC_DIR))

CORS(app)

template_manager: TemplateManager = TemplateManager()

@app.route('/')
def index()-> str:
    # Lista de templates disponibles desde /src/templates
    templates = get_available_templates()
    return render_template('index.html', templates=templates)

@app.route('/api/templates')
def get_templates() -> Response:
    return jsonify(get_available_templates())

def get_available_templates():
    """Obtiene la lista de templates disponibles en /src/templates"""
    templates_dir = Path("src/templates")
    templates = []

    if templates_dir.exists():
        for template_file in templates_dir.glob("*.html"):
            if template_file.stem != "layout" and template_file.stem != "sidebar" and template_file.stem != "main":
                templates.append({
                    "id": template_file.stem,
                    "name": template_file.stem.replace("_", " ").title(),
                    "description": f"Template {template_file.stem}"
                })

    return templates

@app.route('/api/load-data', methods=['GET'])
def load_data():
    """Carga los datos del archivo src/data/resume.json"""
    try:
        data_file = Path("src/data/resume.json")

        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return jsonify({
                    'success': True,
                    'data': data
                })
        else:
            return jsonify({
                'success': False,
                'error': 'No data file found'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/save-data', methods=['POST'])
def save_data():
    """Guarda los datos en src/data/resume.json"""
    try:
        data = request.get_json()
        resume_data = data['resume_data']

        # Crear el directorio src/data si no existe
        data_dir = Path("src/data")
        data_dir.mkdir(exist_ok=True)

        # Guardar datos en formato JSON
        data_file = data_dir / "resume.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(resume_data, f, indent=2, ensure_ascii=False)

        return jsonify({
            'success': True,
            'message': 'Data saved successfully'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/preview', methods=['POST'])
def preview_resume():
    """Genera una vista previa del CV con el template seleccionado"""
    try:
        data = request.get_json()

        # Validar datos usando el modelo Pydantic
        resume = Resume(**data['resume_data'])
        template_name = data.get('template', 'classic')

        # Renderizar el template seleccionado para vista previa
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader("src/templates"))
        template = env.get_template(f"{template_name}.html")
        rendered_html = template.render(resume=resume)

        return jsonify({
            'success': True,
            'html': rendered_html,
            'template': template_name
        })

    except ValidationError as e:
        return jsonify({
            'success': False,
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate', methods=['POST'])
def generate_resume():
    """Genera el CV final y lo guarda en /docs/index.html"""
    try:
        data = request.get_json()

        # Validar datos usando el modelo Pydantic
        resume = Resume(**data['resume_data'])
        template_name = data.get('template', 'classic')

        # Renderizar y guardar en /docs/index.html
        render_resume(resume=resume, template_name=template_name, output_path="docs/index.html")

        return jsonify({
            'success': True,
            'message': 'CV generado exitosamente en docs/index.html',
            'template': template_name
        })

    except ValidationError as e:
        return jsonify({
            'success': False,
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    """Genera un PDF del CV"""
    try:
        data = request.get_json()

        # Validar datos usando el modelo Pydantic
        resume = Resume(**data['resume_data'])
        template_name = data.get('template', 'creative_pro')

        # Generar PDF
        render_resume_to_pdf(resume=resume, template_name=template_name)

        return jsonify({
            'success': True,
            'message': 'PDF generado exitosamente en docs/resume.pdf'
        })

    except ValidationError as e:
        return jsonify({
            'success': False,
            'errors': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)