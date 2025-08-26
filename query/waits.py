import time
from ..config import TIMEOUT_MS
from .finders import exists_title_any_now
from ..drivers.app import is_alive
from ..utils.logging import info
from ..errors import WaitTimeout

def wait_title_visible(text: str, timeout_ms: int = TIMEOUT_MS):
    """Espera a que aparezca un título."""
    deadline = time.time() + timeout_ms/1000.0
    while time.time() < deadline:
        # si existe el control y es visible, logueamos y retornamos
        if exists_title_any_now(text): info(f"WAIT_TITLE_VISIBLE ok: '{text}'"); return
        time.sleep(0.05)
    raise WaitTimeout(f"Timeout visible: '{text}' ({timeout_ms} ms)")

def wait_title_gone(text: str, timeout_ms: int = TIMEOUT_MS):
    """Espera a que desaparezca un título."""
    deadline = time.time() + timeout_ms/1000.0
    while time.time() < deadline:
        # si no existe el control, logueamos y retornamos
        if not exists_title_any_now(text): info(f"WAIT_TITLE_GONE ok: '{text}'"); return
        time.sleep(0.05)
    raise WaitTimeout(f"Timeout gone: '{text}' ({timeout_ms} ms)")

def wait_title_enabled(text: str, timeout_ms: int = TIMEOUT_MS):
    """Espera a que el título esté habilitado (o asume ok si no expone estado)."""
    deadline = time.time() + timeout_ms/1000.0
    while time.time() < deadline:
        # si existe el control y es enabled, logueamos y retornamos
        c = exists_title_any_now(text)
        if c is not None:
            try:
                if c.is_enabled(): info(f"WAIT_TITLE_ENABLED ok: '{text}'"); return
            except Exception:
                info(f"WAIT_TITLE_ENABLED ok*: '{text}'"); return
        time.sleep(0.05)
    raise WaitTimeout(f"Timeout enabled: '{text}' ({timeout_ms} ms)")

def wait_app_alive(timeout_ms: int = TIMEOUT_MS):
    """Espera a que la app esté viva (ventana visible)."""
    deadline = time.time() + timeout_ms/1000.0
    while time.time() < deadline:
        if is_alive(): info("WAIT_APP_ALIVE ok"); return
        time.sleep(0.05)
    raise WaitTimeout(f"Timeout app viva ({timeout_ms} ms)")

def wait_app_exit(timeout_ms: int = TIMEOUT_MS):
    """Espera a que la app termine (ventana ya no visible)."""
    deadline = time.time() + timeout_ms/1000.0
    while time.time() < deadline:
        if not is_alive(): info("WAIT_APP_EXIT ok"); return
        time.sleep(0.05)
    raise WaitTimeout(f"Timeout app cerrada ({timeout_ms} ms)")
