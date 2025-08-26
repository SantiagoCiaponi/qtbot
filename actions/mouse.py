from pywinauto import mouse
from ..utils.logging import info

def click_at(x: int, y: int):
    """Click izquierdo en coords absolutas (x,y)."""
    mouse.click(button="left", coords=(int(x), int(y)))
    info(f"CLICK_AT ({x},{y})")
