import time
from functools import wraps

def retry(times=2, delay=0.15, backoff=1.5, exceptions=(Exception,)):
    """
    Reintenta una función ante excepciones.
    - times: reintentos (además del primer intento)
    - delay: espera inicial entre intentos (seg)
    - backoff: multiplica el delay en cada intento
    """
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            t, d = times, delay
            while True:
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    if t <= 0: raise
                    time.sleep(d)
                    d *= backoff
                    t -= 1
        return wrapper
    return deco
