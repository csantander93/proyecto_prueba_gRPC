# /soap_rest/services/orden_compra_service.py

import mysql.connector
from typing import List
from models.orden_compra import OrdenCompra

class OrdenCompraService:
    def __init__(self):
        # Configuración de conexión a MySQL
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'database': 'stockearte'
        }

    def obtener_ordenes_compra(self) -> List[OrdenCompra]:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor(dictionary=True)

        # Consulta para obtener todas las órdenes de compra y la suma de cantidad_solicitada
        query = """
            SELECT oc.id, oc.codigo_tienda, oc.estado, oc.observaciones, oc.orden_despacho, 
                   oc.fecha_solicitud, oc.fecha_recepcion, 
                   COALESCE(SUM(i.cantidad_solicitada), 0) AS total_cantidad
            FROM orden_de_compra oc
            LEFT JOIN item i ON oc.id = i.orden_id
            GROUP BY oc.id
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        # Convertir los resultados en una lista de objetos OrdenCompra
        return [OrdenCompra(
            id=fila['id'],
            codigo_tienda=fila['codigo_tienda'],
            estado=fila['estado'],
            observaciones=fila['observaciones'],
            orden_despacho=fila['orden_despacho'],
            fecha_solicitud=fila['fecha_solicitud'],
            fecha_recepcion=fila['fecha_recepcion'],
            total_cantidad=fila['total_cantidad']  # Ahora 'total_cantidad' se obtiene de la consulta
        ) for fila in resultados]
