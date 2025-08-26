from pywinauto.keyboard import send_keys
from ..drivers.app import top_window
from ..utils.logging import info, warn

def press_keys(seq: str):
    """Envía teclas. Ej: '^a{DEL}', 'hello{ENTER}'."""
    try: top_window().set_focus()
    except Exception: pass
    send_keys(seq, pause=0.05, with_spaces=True)
    info(f"PRESS_KEYS {seq}")

def _find_edits_sorted():
    """Inputs Edit ordenados (arriba→abajo, izq→der)."""
    edits = top_window().descendants(control_type="Edit")
    if not edits: raise RuntimeError("No se encontraron campos Edit")
    edits.sort(key=lambda c: (c.rectangle().top, c.rectangle().left))
    return edits

def focus_first_edit():
    """Click en el primer Edit."""
    _find_edits_sorted()[0].click_input()
    info("FOCUS_FIRST_EDIT")

def tab_type(value: str):
    """Escribe valor y manda TAB."""
    send_keys("^a{BACKSPACE}")
    send_keys(value, with_spaces=True)
    send_keys("{TAB}")
    info(f"TAB_TYPE '{value}'")

def focus_window():
    """Da foco a la ventana (WARN si falla)."""
    try:
        top_window().set_focus(); info("FOCUS_WINDOW")
    except Exception:
        warn("No se pudo hacer focus en la ventana")
