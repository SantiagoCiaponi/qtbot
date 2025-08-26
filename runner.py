import shlex, time
from pathlib import Path
from typing import List

from .drivers import app as appdrv
from .drivers.uia import tune_timings
from .actions import widgets, keyboard, mouse as mouse_act
from .query import waits
from .report import evidence
from .report.junit import JUnitReporter
from .errors import QtBotError
from .utils.files import screenshot_to
from .utils.logging import info, fail
from .utils.banner import print_banner


def _sleep_ms(ms: str) -> None:
    """Sleep en ms (con log)."""
    time.sleep(int(ms) / 1000.0)
    info(f"WAIT {ms}ms")


def run_test(file_path: str) -> bool:
    """Lee un .test y despacha comandos línea a línea (con JUnit)."""
    print_banner()
    name = Path(file_path).stem
    print(f"\n=== RUN {name} ===")
    reporter = JUnitReporter(suite_name=name)
    start = time.time()
    errors: List[str] = []

    try:
        lines = Path(file_path).read_text(encoding="utf-8").splitlines()
        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            toks = shlex.split(line, posix=False)
            cmd = toks[0].upper()

            try:
                if cmd == "LAUNCH":
                    tune_timings()
                    appdrv.launch(" ".join(toks[1:]))
                elif cmd == "WAIT":
                    _sleep_ms(toks[1])
                elif cmd == "PRESS_KEYS":
                    keyboard.press_keys(" ".join(toks[1:]).strip('"'))
                elif cmd == "FOCUS_WINDOW":
                    keyboard.focus_window()
                elif cmd == "FOCUS_FIRST_EDIT":
                    keyboard.focus_first_edit()
                elif cmd == "TAB_TYPE":
                    keyboard.tab_type(" ".join(toks[1:]).strip('"'))
                elif cmd == "CLICK_TEXT":
                    widgets.click_text(" ".join(toks[1:]).strip('"'))
                elif cmd == "CLICK_TEXT_MOUSE":
                    widgets.click_text_mouse(" ".join(toks[1:]).strip('"'))
                elif cmd == "CLICK_AUTOID":
                    widgets.click_autoid(toks[1].strip('"'))
                elif cmd == "CLICK_AT":
                    mouse_act.click_at(int(toks[1]), int(toks[2]))
                elif cmd == "WAIT_TITLE_VISIBLE":
                    waits.wait_title_visible(toks[1].strip('"'), int(toks[2]))
                elif cmd == "WAIT_TITLE_GONE":
                    waits.wait_title_gone(toks[1].strip('"'), int(toks[2]))
                elif cmd == "WAIT_TITLE_ENABLED":
                    waits.wait_title_enabled(toks[1].strip('"'), int(toks[2]))
                elif cmd == "WAIT_APP_ALIVE":
                    waits.wait_app_alive(int(toks[1]))
                elif cmd == "WAIT_APP_EXIT":
                    waits.wait_app_exit(int(toks[1]))
                elif cmd == "LOG_ALL":
                    evidence.log_all(" ".join(toks[1:]).strip('"') or "state")
                elif cmd == "SPY_TIMELINE":
                    evidence.spy_timeline(toks[1].strip('"'), int(toks[2]), int(toks[3]))
                elif cmd == "EXPECT_TEXT_CONTAINS":
                    evidence.expect_text_contains(" ".join(toks[1:]).strip('"'))
                elif cmd == "SCREENSHOT":
                    evidence.screenshot(toks[1].strip('"'))
                elif cmd == "CLOSE":
                    appdrv.close()
                else:
                    raise QtBotError(f"Comando desconocido: {cmd}")

            except QtBotError as e:
                png = screenshot_to(f"FAIL-{name}", appdrv.top_window())
                fail(str(e))
                errors.append(f"{line}\n -> {e}\n evidence: {png}")
                break
            except Exception as e:
                # cualquier otra excepción la tratamos como error del framework
                png = screenshot_to(f"FAIL-{name}", appdrv.top_window())
                fail(str(e))
                errors.append(f"{line}\n -> {e}\n evidence: {png}")
                break

        # resultado
        if errors:
            reporter.add_fail(name, errors[-1], time.time() - start, stdout="\n".join(errors))
            ok = False
        else:
            reporter.add_ok(name, time.time() - start)
            ok = True

    finally:
        try:
            appdrv.close()
        except Exception:
            pass
        out = reporter.write()
        info(f"JUnit -> {out}")

    print(f"=== {name}: {'OK' if ok else 'FAIL'} ===")
    if errors:
        for e in errors:
            print("  ", e)
    return ok
