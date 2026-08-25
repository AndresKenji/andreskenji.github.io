"""Genera el sitio estático del CV en docs/ a partir de src/data/resume.json."""
from src.render import copy_static_assets, render_resume
from src.storage import load_config, load_resume


def build(output_dir: str = "docs") -> None:
    config = load_config()
    resume = load_resume()
    theme = config["theme"]

    for lang in config["languages"]:
        output = render_resume(resume, lang=lang, theme=theme, output_dir=output_dir)
        print(f"Generated: {output} ({lang.upper()}, theme={theme})")

    copy_static_assets(theme=theme, output_dir=output_dir)


if __name__ == "__main__":
    build()
