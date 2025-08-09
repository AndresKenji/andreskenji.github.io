import logging
import sys
from typing import Optional


class ColoredFormatter(logging.Formatter):

    # Códigos de color ANSI
    COLORS: dict[str, str] = {
        'DEBUG': '\033[36m',
        'INFO': '\033[32m',
        'WARNING': '\033[33m',
        'ERROR': '\033[31m',
        'CRITICAL': '\033[35m',
    }

    BOLD = '\033[1m'
    RESET = '\033[0m'

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None) -> None:
        """
        Args:
            fmt: Formato del mensaje de log
            datefmt: Formato de fecha
        """
        if fmt is None:
            fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        if datefmt is None:
            datefmt = '%Y-%m-%d %H:%M:%S'

        super().__init__(fmt, datefmt)

    def format(self, record: logging.LogRecord) -> str:

        # Obtener el color para el nivel actual
        level_color = self.COLORS.get(record.levelname, '')

        # Crear una copia del record para no modificar el original
        colored_record = logging.makeLogRecord(record.__dict__)

        # Añadir color al nombre del nivel
        colored_record.levelname = f"{level_color}{self.BOLD}{record.levelname}{self.RESET}"

        # Formatear el mensaje base
        formatted_message = super().format(colored_record)

        # Si el nivel es ERROR o CRITICAL, colorear todo el mensaje
        if record.levelname in ['ERROR', 'CRITICAL']:
            formatted_message = f"{level_color}{formatted_message}{self.RESET}"

        return formatted_message


def setup_logger(
    name: str = __name__,
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    include_file_handler: bool = False,
    log_file_path: str = "app.log"
) -> logging.Logger:
    """
    Args:
        name: Nombre del logger
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Formato personalizado para los mensajes
        include_file_handler: Si incluir también logging a archivo
        log_file_path: Ruta del archivo de log (si include_file_handler=True)

    Returns:
        Logger
    """

    # Crear el logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicar handlers si el logger ya existe
    if logger.handlers:
        return logger

    # Configurar el formatter con colores
    colored_formatter = ColoredFormatter(fmt=format_string)

    # Handler para la consola con colores
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(colored_formatter)
    logger.addHandler(console_handler)

    # Handler para archivo (opcional, sin colores)
    if include_file_handler:
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Args:
        name: Nombre del logger

    Returns:
        Logger configurado
    """
    return setup_logger(name)


DEFAULT_LOGGER: logging.Logger = setup_logger("colored_logging")


def demo() -> None:
    """
    Función de demostración que muestra todos los niveles de logging con colores.
    """
    logger: logging.Logger = setup_logger("demo", level=logging.DEBUG)

    print("=== Demo de Logging con Colores ===\n")

    logger.debug("Esto es un mensaje de DEBUG - útil para información detallada")
    logger.info("Esto es un mensaje de INFO - información general")
    logger.warning("Esto es un mensaje de WARNING - algo que requiere atención")
    logger.error("Esto es un mensaje de ERROR - algo salió mal")
    logger.critical("Esto es un mensaje de CRITICAL - error grave del sistema")

    print("\n=== Ejemplo con logging a archivo también ===\n")

    # Logger que también guarda en archivo
    file_logger: logging.Logger = setup_logger(
        "file_demo",
        level=logging.DEBUG,
        include_file_handler=True,
        log_file_path="demo.log"
    )

    file_logger.info("Este mensaje aparece en consola Y en archivo")
    file_logger.error("Los errores también se guardan en ambos lugares")

    print(f"\nRevisa el archivo 'demo.log' para ver los logs sin colores.")


if __name__ == "__main__":
    demo()