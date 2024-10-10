# models/__init__.py

from .tienda import Tienda  # Importa la clase Tienda desde su módulo correspondiente
from .producto import Producto  # Importa la clase Producto desde su módulo correspondiente
from .usuario import Usuario  # Importa la clase Usuario desde su módulo correspondiente
from .orden_compra import OrdenCompraModel
from .item import ItemModel
from .database import db  # Importa la instancia db



__all__ = ['Cadena', 'Tienda', 'Producto', 'Usuario','OrdenCompraModel','ItemModel', 'db']  # Esto permite que se importen las clases
