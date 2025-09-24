class AlreadyExistsError(Exception):
    """Recurso duplicado (ej. usuario ya registrado)."""
    pass
class AlreadyExists(Exception):
    """Recurso duplicado (ej. usuario ya registrado)."""
    pass

class NotFoundError(Exception):
    """Recurso no encontrado en la base de datos."""
    pass

class PermissionDeniedError(Exception):
    """Acceso no autorizado a un recurso."""
    pass
# app/services/portfolio_assets_service.py

class NotOwner(Exception):
    """El portfolio no pertenece al usuario (o no existe para ese usuario)."""

class NotFound(Exception):
    """Recurso no encontrado (portfolio, asset o symbol)."""

class InvalidInput(Exception):
    """Entrada inválida de dominio (negocio)."""
