"""Deja el repositorio listo para tu propio CV.

Reemplaza los datos del CV por el ejemplo, restaura la configuración por
defecto y borra las imágenes personales dejando un avatar placeholder.

    python -m scripts.reset

Es destructivo sobre el árbol de trabajo, no sobre git: si te arrepientes,
`git checkout -- src/data src/static` lo devuelve todo.
"""
import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models import Resume  # noqa: E402
from src.storage import (  # noqa: E402
    CONFIG_PATH,
    DEFAULT_CONFIG,
    EXAMPLE_PATH,
    RESUME_PATH,
    write_json,
)

IMG_DIR = Path("src/static/img")
AVATAR = IMG_DIR / "avatar.svg"
DOCS_DIR = Path("docs")

# El avatar es lo único que sobrevive en src/static/img: es al que apunta el
# CV de ejemplo.
KEEP_IMAGES = {AVATAR.name}


def personal_images() -> list[Path]:
    if not IMG_DIR.is_dir():
        return []
    return sorted(p for p in IMG_DIR.iterdir() if p.is_file() and p.name not in KEEP_IMAGES)


def plan() -> list[str]:
    steps = [
        f"{RESUME_PATH} <- {EXAMPLE_PATH}",
        f"{CONFIG_PATH} <- valores por defecto {DEFAULT_CONFIG}",
    ]
    images = personal_images()
    steps.append(
        f"{IMG_DIR}/ <- eliminar {len(images)} imagen(es): {', '.join(p.name for p in images)}"
        if images else f"{IMG_DIR}/ <- sin imágenes personales que eliminar"
    )
    if DOCS_DIR.exists():
        steps.append(f"{DOCS_DIR}/ <- eliminar el sitio generado")
    return steps


def main() -> int:
    parser = argparse.ArgumentParser(description="Reinicia el repo con datos de ejemplo")
    parser.add_argument("-y", "--yes", action="store_true", help="no preguntar")
    args = parser.parse_args()

    if not EXAMPLE_PATH.exists():
        print(f"No se encuentra {EXAMPLE_PATH}. ¿Estás en la raíz del repositorio?")
        return 1

    print("\nSe va a hacer lo siguiente:\n")
    for step in plan():
        print(f"  · {step}")

    if not args.yes:
        print()
        if input("¿Continuar? [s/N] ").strip().lower() not in ("s", "si", "sí", "y", "yes"):
            print("Cancelado. No se tocó nada.")
            return 1

    # Validar el ejemplo antes de pisar nada.
    resume = Resume.model_validate_json(EXAMPLE_PATH.read_text())

    shutil.copy(EXAMPLE_PATH, RESUME_PATH)
    write_json(CONFIG_PATH, dict(DEFAULT_CONFIG))

    for image in personal_images():
        image.unlink()

    if not AVATAR.exists():
        print(f"\n  Aviso: falta {AVATAR}, que es la foto del CV de ejemplo.")

    shutil.rmtree(DOCS_DIR, ignore_errors=True)

    print(f"\n  Listo. {resume.basics.name} es ahora el CV de ejemplo en {RESUME_PATH}.\n")
    print("  Siguiente paso:\n")
    print("      pip install -r requirements-dev.txt")
    print("      python -m src.editor\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
