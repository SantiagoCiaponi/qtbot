class QtBotError(Exception): """Base del framework."""; pass
class ControlNotFound(QtBotError): """No se encontró un control."""; pass
class WaitTimeout(QtBotError): """Timeout en una espera."""; pass
class ActionFailed(QtBotError): """Falla al ejecutar una acción."""; pass
