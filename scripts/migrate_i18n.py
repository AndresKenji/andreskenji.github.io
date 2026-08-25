"""Unifica resume.json (EN) y resume_es.json (ES) en un único resume.json bilingüe.

Script de un solo uso. Recorre ambos archivos en paralelo guiado por la definición
de `src.models.Resume`: cada campo declarado como `I18nStr` se convierte en
{"en": ..., "es": ...} y el resto debe coincidir en ambos archivos.

Se apoya en el modelo en vez de en una lista de campos escrita a mano para que no
pueda desalinearse cuando models.py cambie.
"""
import json
import shutil
import sys
from pathlib import Path
from typing import Union, get_args, get_origin

from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.models import I18nStr, Resume  # noqa: E402
from src.storage import write_json, resume_to_dict  # noqa: E402

EN_PATH = Path("src/data/resume.json")
ES_PATH = Path("src/data/resume_es.json")
LEGACY_DIR = Path("src/data/_legacy")

# Valores que hoy significan "sigo aquí" y pasan a ser null.
ONGOING = {"current", "actual", "present", "actualidad", "presente", ""}

problems: list[str] = []


def unwrap_optional(annotation):
    """Optional[X] -> X. Deja el resto igual."""
    if get_origin(annotation) is Union:
        args = [a for a in get_args(annotation) if a is not type(None)]
        if len(args) == 1:
            return args[0]
    return annotation


def list_item_type(annotation):
    """List[X] -> X, o None si no es una lista."""
    annotation = unwrap_optional(annotation)
    if get_origin(annotation) in (list, "list"):
        args = get_args(annotation)
        return args[0] if args else None
    return None


def is_model(annotation) -> bool:
    return isinstance(annotation, type) and issubclass(annotation, BaseModel)


def merge_lists(item_type, en, es, path: str):
    en = en or []
    es = es or []
    if len(en) != len(es):
        problems.append(
            f"{path}: EN tiene {len(en)} elementos y ES tiene {len(es)}. "
            "No se pueden emparejar por índice."
        )
        return None
    return [
        merge_value(item_type, a, b, f"{path}[{i}]")
        for i, (a, b) in enumerate(zip(en, es))
    ]


def merge_value(annotation, en, es, path: str):
    annotation = unwrap_optional(annotation)

    if annotation is I18nStr:
        if en is None and es is None:
            return None
        return {"en": en, "es": es}

    item_type = list_item_type(annotation)
    if item_type is not None:
        return merge_lists(item_type, en, es, path)

    if is_model(annotation):
        return merge_model(annotation, en or {}, es or {}, path)

    if en != es:
        problems.append(f"{path}: valor no traducible difiere — EN={en!r} ES={es!r}")
    return en


def merge_model(model_cls, en: dict, es: dict, path: str) -> dict:
    out = {}
    for name, field in model_cls.model_fields.items():
        if name not in en and name not in es:
            # Campo con valor por defecto que no está en los archivos originales
            # (p. ej. Skill.color, Skill.level_percent). Se omite para que
            # Pydantic aplique el default en vez de escribir un null.
            continue

        value_en, value_es = en.get(name), es.get(name)

        if name == "end_date":
            # "Current" / "Actual" -> null. Se comparan por separado porque es
            # justo el campo que legítimamente difiere entre los dos archivos.
            out[name] = None if str(value_en or "").strip().lower() in ONGOING else value_en
            continue

        out[name] = merge_value(field.annotation, value_en, value_es, f"{path}.{name}")
    return out


def main() -> int:
    if not ES_PATH.exists():
        print(f"No existe {ES_PATH}: parece que la migración ya se corrió.")
        return 1

    en = json.loads(EN_PATH.read_text())
    es = json.loads(ES_PATH.read_text())

    merged = merge_model(Resume, en, es, "resume")

    if problems:
        print("La migración encontró diferencias que no sabe resolver:\n")
        for p in problems:
            print(f"  - {p}")
        print("\nNo se escribió nada. Resuelve los campos de arriba y vuelve a correr.")
        return 1

    # Validar antes de tocar el disco.
    resume = Resume.model_validate(merged)

    LEGACY_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(EN_PATH, LEGACY_DIR / "resume.en.json")
    shutil.move(str(ES_PATH), LEGACY_DIR / "resume.es.json")

    write_json(EN_PATH, resume_to_dict(resume))

    print(f"Escrito {EN_PATH} (bilingüe).")
    print(f"Originales guardados en {LEGACY_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
