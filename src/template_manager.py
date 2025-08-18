import logging
import json
from pathlib import Path
from typing import Dict, List, Any
from jinja2 import Environment, FileSystemLoader

from src.logging_config import setup_logger

logger: logging.Logger = setup_logger(
    name="cv_creator",
    level=logging.INFO,
    format_string='%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    include_file_handler=False,
)

class TemplateManager:

    def __init__(self, templates_dir: str = "app/cv-templates"):
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)

    def get_available_templates(self) -> List[Dict[str, Any]]:
        templates = []

        if not self.templates_dir.exists():
            return []

        for template_dir in self.templates_dir.iterdir():
            if template_dir.is_dir() and (template_dir / "template.json").exists():
                metadata = self._load_template_metadata(template_dir)
                if metadata:
                    templates.append(metadata)

        return templates

    def _load_template_metadata(self, template_dir: Path) -> Dict[str, Any]:
        try:
            metadata_file: Path = template_dir / "template.json"
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            metadata['id'] = template_dir.name
            metadata['preview_image'] = f"static/img/templates/{template_dir.name}-preview.png"

            return metadata
        except Exception as e:
            logger.error(f"Error loading template metadata for {template_dir.name}: {e}")
            return None

    def get_template_path(self, template_id: str) -> Path:
        return self.templates_dir / template_id

    def get_template_static_path(self, template_id: str) -> Path:
        return self.templates_dir / template_id / "static"

    def template_exists(self, template_id: str) -> bool:
        template_path = self.get_template_path(template_id)
        return template_path.exists() and (template_path / "template.json").exists()

    def get_template_environment(self, template_id: str) -> Environment:
        if not self.template_exists(template_id):
            raise ValueError(f"Template '{template_id}' not found")

        template_path: Path = self.get_template_path(template_id)
        return Environment(loader=FileSystemLoader(str(template_path)))
