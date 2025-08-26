from pywinauto import timings
from ..config import TIMEOUT_MS

def tune_timings():
    """Ajusta timeouts/pausas de pywinauto para UIA."""
    timings.Timings.window_find_timeout = TIMEOUT_MS/1000
    timings.Timings.after_clickinput_wait = 0.2
    timings.Timings.after_sendkeys_key_wait = 0.02
