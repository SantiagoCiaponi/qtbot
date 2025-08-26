# logging.py
# --------------------------------------------------------
# Centraliza los niveles de log que usamos en el framework.
# La idea es tener un esquema simple que te diga:
#   - qué comandos se ejecutaron
#   - qué warnings hubo (no fatal pero ojo)
#   - qué falló (corta el test)
# --------------------------------------------------------

def info(msg: str):
    """
    [INFO] -> Logs de flujo normal / pasos esperados.
    Ejemplos:
      - "LAUNCH ..." al abrir la app
      - "CLICK_TEXT 'OK'" cuando se clickeó un botón
      - "WAIT_TITLE_VISIBLE ok: 'Ingresar DNI'" cuando una espera se cumplió
    
    Sirve para leer el reporte y reconstruir el paso a paso de la ejecución.
    """
    print(f"[INFO] {msg}")


def warn(msg: str):
    """
    [WARN] -> Situaciones no fatales pero sospechosas.
    Ejemplos:
      - No se pudo dar foco a la ventana, pero seguimos.
      - Se intentó un fallback (ej: click por coordenadas).
    
    El test sigue corriendo, pero queda marcado en el log para que sepas que algo no fue "ideal".
    """
    print(f"[WARN] {msg}")


def fail(msg: str):
    """
    [FAIL] -> Error que rompe el flujo del test.
    Ejemplos:
      - Timeout esperando que aparezca un control.
      - No se encontró un botón con el título buscado.
      - Excepción en un comando crítico.
    
    Siempre se considera que el test FALLÓ y se aborta.
    """
    print(f"[FAIL] {msg}")