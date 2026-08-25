"""Punto de entrada: python -m src.editor"""
import argparse
import socket
import threading
import webbrowser

import uvicorn

DEFAULT_PORT = 8000


def is_free(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
            return True
        except OSError:
            return False


def pick_port(host: str, preferred: int, attempts: int = 20) -> int:
    """El puerto pedido, o el siguiente libre.

    El 8000 lo suele tomar Docker u otro servicio local; caer al siguiente
    evita un 'address already in use' que no aporta nada.
    """
    for port in range(preferred, preferred + attempts):
        if is_free(host, port):
            if port != preferred:
                print(f"  El puerto {preferred} está ocupado; usando el {port}.")
            return port
    raise SystemExit(f"No hay puertos libres entre {preferred} y {preferred + attempts - 1}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Editor local del CV")
    parser.add_argument("--port", type=int, default=None,
                        help=f"puerto fijo; por defecto {DEFAULT_PORT} o el siguiente libre")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--reload", action="store_true", help="recarga en caliente al editar el código")
    args = parser.parse_args()

    # Un --port explícito se respeta tal cual: si está ocupado, que falle.
    port = args.port if args.port is not None else pick_port(args.host, DEFAULT_PORT)

    url = f"http://{args.host}:{port}"
    if not args.no_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    print(f"\n  Editor del CV en {url}\n")
    uvicorn.run("src.editor.app:app", host=args.host, port=port, reload=args.reload)


if __name__ == "__main__":
    main()
