from xml.etree.ElementTree import Element, SubElement, ElementTree
from pathlib import Path
from ..utils.timeutils import ts
from ..utils.files import ensure_dirs
from ..config import REPORTS_DIR


class JUnitReporter:
    """
    Genera reportes en formato JUnit XML.
    
    Este formato es estándar en herramientas de CI/CD (Jenkins, GitLab, GitHub Actions, etc.)
    y permite visualizar resultados de tests en dashboards con estadísticas, tiempos y fallos.
    """

    def __init__(self, suite_name="qtbot"):
        """
        Inicializa un nuevo reporter.
        - suite_name: nombre del test suite (ej. "login_dni_ok").
        """
        self.suite_name = suite_name
        self.tests = []  # lista de resultados (status, name, time, extra)

    def add_ok(self, name: str, time_s: float = 0.0):
        """
        Registra un test exitoso.
        - name: nombre del caso de test.
        - time_s: duración en segundos.
        """
        self.tests.append(("ok", name, time_s, None))

    def add_fail(self, name: str, message: str, time_s: float = 0.0, stdout: str = None):
        """
        Registra un test fallido.
        - name: nombre del caso de test.
        - message: mensaje de error resumido.
        - time_s: duración en segundos.
        - stdout: detalle adicional (logs, evidencias, paths de screenshots, etc.).
        """
        self.tests.append(("fail", name, time_s, (message, stdout)))

    def write(self, filename: str = None) -> Path:
        """
        Genera el archivo junit.xml con todos los resultados acumulados.
        - filename: ruta opcional para guardar; si no se da, se crea en REPORTS_DIR con timestamp.
        - return: Path al archivo generado.
        """
        ensure_dirs()

        # nodo raíz <testsuite>
        root = Element("testsuite", name=self.suite_name, tests=str(len(self.tests)))

        # por cada test registrado, agregar un <testcase>
        for status, name, dur, extra in self.tests:
            case = SubElement(root, "testcase", name=name, time=f"{dur:.3f}")
            if status == "fail":
                msg, out = extra or ("", "")
                fail = SubElement(case, "failure", message=msg)
                fail.text = out or ""

        # serializar a XML
        tree = ElementTree(root)
        p = Path(filename) if filename else REPORTS_DIR / f"junit-{ts()}.xml"
        tree.write(p, encoding="utf-8", xml_declaration=True)
        return p
