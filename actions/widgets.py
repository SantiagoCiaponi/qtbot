import time
from pywinauto import mouse
from ..drivers.app import top_window
from ..query.finders import by_title_any, by_auto_id, bubble_to_clickable
from ..utils.geometry import center_of
from ..utils.logging import info
from ..utils.retry import retry
from ..errors import ActionFailed


@retry(times=2, delay=0.2, backoff=1.6, exceptions=(Exception,))
def click_text(text: str):
    """Click en control por título, con reintentos."""
    ctrl = by_title_any(text) # re-resuelve cada intento
    target = bubble_to_clickable(ctrl)
    try: top_window().set_focus()
    except Exception: pass
    for fn in (getattr(target,"click_input",None), getattr(target,"invoke",None)):
        try:
            if callable(fn): fn(); info(f"CLICK_TEXT '{text}'"); return
        except Exception: pass
    # fallback mouse
    x,y = center_of(target)
    try:
        mouse.click(button="left", coords=(x,y)); info(f"CLICK_TEXT(mouse@{x},{y}) '{text}'")
        return
    except Exception as e:
        raise ActionFailed(f"No se pudo clickear '{text}' ({e})")

def click_text_mouse(text: str):
    """Click por mouse al centro del control (buscado por título)."""
    ctrl = by_title_any(text)
    target = bubble_to_clickable(ctrl)
    x,y = center_of(target)
    mouse.click(button="left", coords=(x,y))
    info(f"CLICK_TEXT_MOUSE '{text}' @ ({x},{y})")

@retry(times=2, delay=0.2, backoff=1.6, exceptions=(Exception,))
def click_autoid(auto_id: str, post_sleep_ms: int = 120):
    """Click por auto_id, con reintentos."""
    try: top_window().set_focus()
    except Exception: pass
    ctrl = by_auto_id(auto_id)
    try:
        ctrl.click_input(); time.sleep(post_sleep_ms/1000.0); info(f"CLICK_AUTOID '{auto_id}'"); return
    except Exception:
        x,y = center_of(ctrl)
        mouse.click(button="left", coords=(x,y))
        time.sleep(post_sleep_ms/1000.0)
        info(f"CLICK_AUTOID(mouse@{x},{y}) '{auto_id}'")
