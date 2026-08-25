"""Lectura y escritura del resume.json bilingüe."""
import json
import os
import tempfile
from pathlib import Path

from src.models import Resume

RESUME_PATH = Path("src/data/resume.json")
EXAMPLE_PATH = Path("src/data/resume.example.json")
CONFIG_PATH = Path("src/data/config.json")

DEFAULT_CONFIG = {"theme": "classic", "default_language": "en", "languages": ["en", "es"]}


def collapse_i18n(value):
    """Colapsa {"en": x, "es": x} a x cuando todos los idiomas coinciden.

    `I18nStr` vuelve a expandir un string plano al leer, así que el ciclo es
    reversible. Sirve para que resume.json siga siendo legible y los diffs de
    git no se llenen de pares repetidos.
    """
    if isinstance(value, dict):
        if set(value) == {"en", "es"} and all(isinstance(v, str) for v in value.values()):
            if value["en"] == value["es"]:
                return value["en"]
            return value
        return {k: collapse_i18n(v) for k, v in value.items()}
    if isinstance(value, list):
        return [collapse_i18n(v) for v in value]
    return value


def resume_to_dict(resume: Resume) -> dict:
    return collapse_i18n(resume.model_dump(mode="json", exclude={"skills": {"__all__": {"level_percent"}}}))


def resolve_resume_path(path: Path = RESUME_PATH) -> Path:
    """El CV a usar, cayendo al de ejemplo si aún no hay uno propio.

    Así el repositorio funciona recién clonado, antes de correr
    `python -m scripts.reset` o de escribir el CV propio.
    """
    path = Path(path)
    return path if path.exists() else EXAMPLE_PATH


def load_resume(path: Path = RESUME_PATH) -> Resume:
    return Resume.model_validate_json(resolve_resume_path(path).read_text())


def load_resume_dict(path: Path = RESUME_PATH) -> dict:
    return json.loads(resolve_resume_path(path).read_text())


def is_example_data(path: Path = RESUME_PATH) -> bool:
    """True mientras el CV siga siendo el de ejemplo, sin editar."""
    if not EXAMPLE_PATH.exists():
        return False
    if not Path(path).exists():
        return True
    return load_resume_dict(path) == json.loads(EXAMPLE_PATH.read_text())


def write_json(path: Path, data: dict) -> None:
    """Escritura atómica: si algo falla a mitad, el archivo original queda intacto."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def save_resume(resume: Resume, path: Path = RESUME_PATH) -> None:
    write_json(Path(path), resume_to_dict(resume))


def load_config() -> dict:
    if CONFIG_PATH.exists():
        return {**DEFAULT_CONFIG, **json.loads(CONFIG_PATH.read_text())}
    return dict(DEFAULT_CONFIG)


def save_config(config: dict) -> None:
    write_json(CONFIG_PATH, {**load_config(), **config})
