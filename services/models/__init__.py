# models/__init__.py

from .tienda import Tienda  # Importa la clase Tienda desde su módulo correspondiente
from .producto import Producto  # Importa la clase Producto desde su módulo correspondiente
from .usuario import Usuario  # Importa la clase Usuario desde su módulo correspondiente
from .orden_compra import OrdenCompraModel
from .item import ItemModel
from .database import db  # Importa la instancia db
from .order import OrdenDeCompra
from .order import Item
from .order import EstadoOrden
from .proveedor import ArticuloProveedor
from .proveedor import OrdenDespacho
from .novedad import NovedadProducto
__all__ = ['Cadena', 'Tienda', 'Producto', 'Usuario', 'OrdenDeCompra','Item','EstadoOrden', 'ArticuloProveedor','OrdenDespacho', 'NovedadProducto','db']  # Esto permite que se importen las clases
