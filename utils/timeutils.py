import datetime

def ts():
    """
    Genera un timestamp compacto en formato YYYYMMDD-HHMMSS.

    Uso:
    - Para nombrar archivos de evidencia (screenshots, logs, dumps).
    - Evita colisiones: cada ejecución/acción genera un nombre único.

    Retorna: str Un string con la fecha y hora actual, ej: "20250825-183045".
    """
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")