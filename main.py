import json
from src.models import Resume
from pathlib import Path
from src.render import render_resume

def load_resume(path: str = "src/data/resume.json") -> Resume:
    data = json.loads(Path(path).read_text())
    return Resume(**data)

if __name__ == "__main__":
    resume = load_resume()
    render_resume(resume)
