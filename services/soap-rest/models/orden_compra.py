# /soap_rest/models/orden_compra.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class OrdenCompra:
    id: int
    codigo_tienda: str
    estado: str
    observaciones: str
    orden_despacho: str
    fecha_solicitud: datetime
    fecha_recepcion: datetime
    total_cantidad: int  # Agregamos el total_cantidad para que se pueda usar en la respuesta
