# services/__init__.py

from .usuario_service import UsuarioService  # Asegúrate de que el nombre del archivo y la clase son correctos
from .tienda_service import TiendaService    # Asegúrate de que el nombre del archivo y la clase son correctos
from .producto_service import ProductoService  # Asegúrate de que el nombre del archivo y la clase son correctos

# Aquí puedes inicializar otros componentes o variables si es necesario

__all__ = ['UsuarioService', 'TiendaService', 'ProductoService']  # Esto permite que se importen las clases
