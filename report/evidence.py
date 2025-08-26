import io, time
from contextlib import redirect_stdout
from ..drivers.app import top_window
from ..utils.files import screenshot_to, log_to
from ..utils.logging import info

def _dump_actionables():
    """Lista botones/textos visibles con rect y estado (para forense)."""
    lines = []
    wnd = top_window()
    def rects(c):
        r = c.rectangle(); return f"[{r.left},{r.top},{r.right},{r.bottom}]"
    for b in wnd.descendants(control_type="Button"):
        try: lines.append(f"Button  vis={b.is_visible()} en={b.is_enabled()}  title='{b.window_text()}'  rect={rects(b)}")
        except Exception: pass
    for t in wnd.descendants(control_type="Text"):
        try:
            if t.is_visible(): lines.append(f"Text    title='{t.window_text()}' rect={rects(t)}")
        except Exception: pass
    return "\n".join(lines) if lines else "(no controls)"

def log_all(tag: str):
    """Screenshot + árbol de controles + actionables (3 archivos)."""
    sp = screenshot_to(tag, top_window())
    buf = io.StringIO()
    with redirect_stdout(buf):
        top_window().print_control_identifiers()
    tp = log_to(f"{tag}_tree", buf.getvalue())
    ap = log_to(f"{tag}_actionables", _dump_actionables())
    info(f"LOG_ALL '{tag}' -> {sp}, {tp}, {ap}")

def spy_timeline(tag: str, dur_ms: int, step_ms: int):
    """Timelapse: captura periódica de screenshot + actionables."""
    t0 = time.time(); n = 0
    while (time.time() - t0) * 1000.0 < dur_ms:
        sfx = f"{tag}_t{n:02d}"
        try:
            screenshot_to(sfx, top_window())
            log_to(f"{sfx}_actionables", _dump_actionables())
        except Exception as e:
            log_to(f"{sfx}_error", f"{e}")
        time.sleep(max(0.01, step_ms/1000.0)); n += 1
    info(f"SPY_TIMELINE '{tag}' {dur_ms}ms step {step_ms}ms -> {n} frames")

def expect_text_contains(substr: str, timeout_s: float = 5.0):
    """Asserción: existe Text visible que contenga `substr`."""
    wnd = top_window()
    ctrl = wnd.child_window(title_re=f".*{substr}.*", control_type="Text")
    ctrl.wait("exists visible", timeout=timeout_s)
    info(f"EXPECT_TEXT_CONTAINS ok: '{substr}'")

def screenshot(name: str):
    """Captura screenshot con `name`."""
    p = screenshot_to(name, top_window())
    info(f"SCREENSHOT -> {p}")
