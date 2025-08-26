def center_of(ctrl):
    """
    Calcula el punto central (x, y) de un control de UI.

    Uso:
    - Cuando no podés invocar un control con `.invoke()` o `.click_input()`,se recurre al fallback de click por coordenadas.
    - Para eso se necesita un punto dentro del área del control, elegimos centro de su rectangulo.

    Parámetros: ctrl : pywinauto ElementWrapper. Control de UI del que queremos calcular la posición.
    
    Retorna: (int, int) Coordenadas absolutas (x, y) del centro del control en pantalla.
    """
    r = ctrl.rectangle()
    return int((r.left + r.right)/2), int((r.top + r.bottom)/2)