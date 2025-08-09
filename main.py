import logging
import json

from pathlib import Path

from src.logging_config import setup_logger
from src.models import Resume
from src.render import render_resume


logger: logging.Logger = setup_logger(
    name="cv_creator",
    level=logging.INFO,
    format_string='%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    include_file_handler=False,
)

def load_resume(path: str = "src/data/resume.json") -> Resume:
    data = json.loads(Path(path).read_text())
    return Resume(**data)

if __name__ == "__main__":
    resume = load_resume()
    render_resume(resume)
