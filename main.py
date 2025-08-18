import json
import logging
import os
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

    data: dict = json.loads(Path(path).read_text(encoding='utf-8'))
    return Resume(**data)

def main() -> None:

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--web':
        from app import app
        logger.info("Starting CV Builder Web Application...")
        logger.info("Open http://localhost:5000 in your browser to create your CV")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:

        logger.info("Generating CV from resume.json...")
        resume: Resume = load_resume()
        render_resume(resume)
        logger.info("CV generated successfully at docs/index.html")
        logger.info("Tip: Use 'python main.py --web' to start the interactive CV builder")

if __name__ == "__main__":
    main()
