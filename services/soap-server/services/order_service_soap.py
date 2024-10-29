from zeep import Document
from models import OrdenCompraModel
from datetime import datetime
from flask import jsonify

class OrderService:
    def get_orders(self, codigo_producto=None, fecha_inicio=None, fecha_fin=None, estado=None, codigo_tienda=None):
        try:
            # Consultar órdenes de compra basadas en los filtros proporcionados
            query = OrdenCompraModel.query

            if codigo_producto:
                query = query.filter(OrdenCompraModel.codigo_producto == codigo_producto)

            if fecha_inicio and fecha_fin:
                query = query.filter(OrdenCompraModel.fecha_solicitud.between(fecha_inicio, fecha_fin))

            if estado:
                query = query.filter(OrdenCompraModel.estado == estado)

            if codigo_tienda:
                query = query.filter(OrdenCompraModel.codigo_tienda == codigo_tienda)

            ordenes = query.all()

            # Agrupar los resultados por producto y estado
            resultados = {}
            for orden in ordenes:
                key = (orden.codigo_producto, orden.estado, orden.codigo_tienda)
                if key not in resultados:
                    resultados[key] = 0
                resultados[key] += orden.cantidad

            return resultados
        except Exception as e:
            raise Exception(f'Error al obtener órdenes: {str(e)}')
