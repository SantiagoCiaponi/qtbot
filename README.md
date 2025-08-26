# QtBot

Framework para testing E2E (end-to-end) de aplicaciones Qt/QML en Windows, usando automatización de UI con [pywinauto](https://pywinauto.readthedocs.io/).

## ¿Qué hace?

QtBot permite automatizar pruebas funcionales sobre aplicaciones Qt/QML, simulando acciones de usuario (clicks, teclas, espera de controles, etc.), generando evidencia (screenshots, logs) y reportes en formato JUnit para integración continua.

## Características principales

- **Automatización de UI**: Interactúa con controles de la app (botones, textos, campos de edición, etc.).
- **Comandos de alto nivel**: Ejecuta scripts `.test` con comandos como `LAUNCH`, `CLICK_TEXT`, `PRESS_KEYS`, `WAIT`, etc.
- **Evidencia forense**: Captura screenshots, árbol de controles y estado de la UI en cada paso.
- **Reportes JUnit**: Genera archivos XML compatibles con CI/CD.
- **Reintentos y manejo de errores**: Robustez ante fallos de UI o sincronización.

## Estructura del proyecto

```
qtbot/
│
├── actions/      # Acciones sobre la UI (mouse, teclado, widgets)
├── drivers/      # Lanzamiento y manejo de la app
├── query/        # Búsqueda y espera de controles
├── report/       # Evidencia y reportes JUnit
├── utils/        # Utilidades (logs, archivos, geometría, retry, banner)
├── runner.py     # Motor principal que ejecuta los tests
├── config.py     # Configuración global (timeouts, rutas)
├── errors.py     # Excepciones propias del framework
├── cli.py        # (Opcional) CLI para ejecutar tests desde terminal
└── README.md     # Este archivo
```

## Instalación

1. **Requisitos**
	- Windows 10/11
	- Python 3.8+
	- pip

2. **Dependencias**
	- pywinauto
	- pyfiglet

	Instala las dependencias con:

	```powershell
	pip install pywinauto pyfiglet
	```

3. **Clona el proyecto**

	```powershell
	git clone https://github.com/SantiagoCiaponi/qtbot.git
	cd qtbot
	```

## Uso básico

1. **Prepara un archivo de test**  
	Crea un archivo `.test` con comandos, por ejemplo:

	```
	LAUNCH "C:\Ruta\A\TuApp.exe"
	WAIT 1000
	CLICK_TEXT "Aceptar"
	PRESS_KEYS "usuario{TAB}clave{ENTER}"
	WAIT_TITLE_VISIBLE "Bienvenido" 5000
	SCREENSHOT "login_ok"
	CLOSE
	```

2. **Ejecuta el test**

	```powershell
	python runner.py ruta/al/test.test
	```

	El resultado y la evidencia se guardan en la carpeta `reports/`.

## Comandos soportados

- `LAUNCH <exe>`: Lanza la app.
- `WAIT <ms>`: Espera en milisegundos.
- `CLICK_TEXT <texto>`: Click en control por texto.
- `PRESS_KEYS <secuencia>`: Envía teclas.
- `FOCUS_WINDOW`: Da foco a la ventana.
- `FOCUS_FIRST_EDIT`: Click en el primer campo de edición.
- `TAB_TYPE <valor>`: Escribe y manda TAB.
- `WAIT_TITLE_VISIBLE <texto> <ms>`: Espera que aparezca un título.
- `WAIT_TITLE_GONE <texto> <ms>`: Espera que desaparezca un título.
- `LOG_ALL <tag>`: Captura screenshot + árbol de controles + botones.
- `SPY_TIMELINE <tag> <dur_ms> <step_ms>`: Timelapse de evidencia.
- `EXPECT_TEXT_CONTAINS <texto>`: Asserción de texto visible.
- `SCREENSHOT <nombre>`: Captura screenshot.
- `CLOSE`: Cierra la app.

## Reportes y evidencia

- **Screenshots**: En `reports/screenshots/`
- **Logs**: En `reports/logs/`
- **JUnit XML**: En `reports/junit-*.xml`

## Extensión y personalización

Puedes agregar nuevos comandos o modificar la lógica en los módulos de `actions/`, `query/`, etc. El framework está pensado para ser simple y hackeable.

## Autor

Santiago Ciaponi  
Contacto: santiagociaponi3@gmail.com

---

¿Dudas, sugerencias o bugs? Abrí un issue o mandame un WhatsApp.

---

