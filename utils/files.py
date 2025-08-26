from pathlib import Path
from .timeutils import ts
from ..config import SCREEN_DIR, LOGS_DIR


def ensure_dirs():
    """
    Garantiza que existan los directorios de evidencia.

    Esto se llama siempre antes de guardar logs o screenshots.
    """
    SCREEN_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def screenshot_to(basename: str, win) -> Path:
    """
    Captura y guarda un screenshot de la ventana dada.

    Parámetros:
    - basename : str Texto base para el nombre del archivo (ej: 'before_ok').
    - win : pywinauto WindowSpecification. Ventana de la cual capturar la imagen.

    Retorna: 
    - Path Ruta completa al archivo PNG generado.
    """
    ensure_dirs()
    p = SCREEN_DIR / f"{ts()}-{basename}.png"
    win.capture_as_image().save(str(p))
    return p


def log_to(basename: str, text: str) -> Path:
    """
    Escribe un log de texto en el directorio de logs.

    Parámetros:
    - basename : str Texto base para el nombre del archivo (ej: 'tree_dump').
    - text : str Contenido a escribir en el archivo (ej: árbol de controles).

    Retorna:
    - Path Ruta completa al archivo TXT generado.
    """
    ensure_dirs()
    p = LOGS_DIR / f"{ts()}-{basename}.txt"
    p.write_text(text, encoding="utf-8")
    return p