from pathlib import Path

# ---------- Config ----------
# tiempo maximo de espera por operaciones de UI (ms). Si no responde, muere. 
TIMEOUT_MS = 5000
# backend de automatizacion. "uia" funciona con la mayoría de apps Qt/QML en Windows.
BACKEND = "uia"

# Rutas de evidencia.
REPORTS_DIR = Path("reports")
SCREEN_DIR = REPORTS_DIR / "screenshots"
LOGS_DIR   = REPORTS_DIR / "logs"