import re
from ..drivers.app import top_window
from ..errors import ControlNotFound

_CTYPES = ("Button","Text","Hyperlink","MenuItem","SplitButton","Custom","Pane","ListItem","TreeItem")

def bubble_to_clickable(ctrl, max_depth=8):
    """Sube por padres hasta un contenedor clickeable (Button/Custom/Pane...)."""
    cur = ctrl; d = 0
    while cur and d < max_depth:
        ct = getattr(cur.element_info, "control_type", "")
        if ct in ("Button","Hyperlink","SplitButton","MenuItem","Custom","Pane"):
            return cur
        try: cur = cur.parent()
        except Exception: break
        d += 1
    return ctrl

def by_title_any(text: str):
    """Busca control por título (exacto por tipo → regex → Text visibles)."""
    wnd = top_window()
    norm = text.replace("&","").strip()
    for ct in _CTYPES:
        try:
            c = wnd.child_window(title=norm, control_type=ct)
            c.wait("exists visible"); return c
        except Exception: pass
    try:
        c = wnd.child_window(title_re=rf".*{re.escape(norm)}.*")
        c.wait("exists visible"); return c
    except Exception: pass
    for t in wnd.descendants(control_type="Text"):
        try:
            if t.is_visible() and norm in (t.window_text() or ""): return t
        except Exception: pass
    raise ControlNotFound(f"No se encontró control con title='{text}'")

def by_auto_id(auto_id: str):
    """Busca control por automation id (UIA: auto_id)."""
    wnd = top_window()
    c = wnd.child_window(auto_id=auto_id)
    c.wait("exists visible")
    return c

def exists_title_any_now(text: str):
    """Devuelve control por título si ya está visible; sino None (no espera)."""
    wnd = top_window()
    for kw in (dict(title=text, control_type="Button"),
               dict(title=text, control_type="Text"),
               dict(title=text)):
        try:
            c = wnd.child_window(**kw)
            if c.exists() and c.is_visible(): return c
        except Exception: pass
    return None

def exists_auto_id_now(auto_id: str):
    """Devuelve control por automation id si ya está visible; sino None (no espera)."""
    wnd = top_window()
    try:
        c = wnd.child_window(auto_id=auto_id)
        if c.exists() and c.is_visible(): return c
    except Exception: pass
    return None

def exists_title_regex_now(pattern: str):
    """Devuelve control por título regex si ya está visible; sino None (no espera)."""
    wnd = top_window()
    try:
        c = wnd.child_window(title_re=pattern)
        if c.exists() and c.is_visible(): return c
    except Exception: pass
    return None