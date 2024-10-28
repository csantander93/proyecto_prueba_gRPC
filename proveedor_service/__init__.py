# models/__init__.py
from .database import db  # Importa la instancia db
from models import ArticuloProveedor
from models import OrdenDespacho
from models import OrdenCompraProveedor
__all__ = ['ArticuloProveedor','OrdenDespacho','OrdenCompraProveedor','db']  # Esto permite que se importen las clases
