# models/orden_compra.py

class OrdenCompra:
    def __init__(self, id: int, codigo_tienda: str, estado: str, observaciones: str,
                 orden_despacho: str, fecha_solicitud: str, fecha_recepcion: str, total_cantidad: int = 0):
        self.id = id
        self.codigo_tienda = codigo_tienda
        self.estado = estado
        self.observaciones = observaciones
        self.orden_despacho = orden_despacho
        self.fecha_solicitud = fecha_solicitud
        self.fecha_recepcion = fecha_recepcion
        self.total_cantidad = total_cantidad
