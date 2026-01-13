import json
from src.models import Resume
from pathlib import Path
from src.render import render_resume


def load_resume(path: str) -> Resume:
    data = json.loads(Path(path).read_text())
    return Resume(**data)


if __name__ == "__main__":
    # Generar versión en inglés
    resume_en = load_resume("src/data/resume.json")
    render_resume(resume_en, lang="en")
    print("Generated: docs/index.html (EN)")

    # Generar versión en español
    resume_es = load_resume("src/data/resume_es.json")
    render_resume(resume_es, lang="es")
    print("Generated: docs/es/index.html (ES)")
