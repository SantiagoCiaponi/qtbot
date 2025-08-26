from pywinauto.application import Application
from ..config import BACKEND, TIMEOUT_MS
from ..utils.logging import info

_app = None

def launch(cmdline: str):
    """Lanza la app y espera ventana lista."""
    global _app
    cmd = cmdline.strip().strip('"')
    _app = Application(backend=BACKEND).start(cmd)
    top_window().wait("exists enabled visible ready", timeout=TIMEOUT_MS/1000)
    info(f"LAUNCH {cmd}")
    return _app

def top_window():
    """Ventana superior de la app."""
    return _app.top_window()

def is_alive() -> bool:
    """True si la ventana existe y es visible."""
    try:
        w = top_window()
        return w.exists() and w.is_visible()
    except Exception:
        return False

def close():
    """Cierra o mata la app (best-effort)."""
    try:
        top_window().close()
    except Exception:
        try:
            if _app: _app.kill()
        except Exception:
            pass
    info("CLOSE")
