# /soap_rest/services/orden_compra_service.py

import mysql.connector
from typing import List  # Asegúrate de importar List
from models.orden_compra import OrdenCompra  # Asegúrate de que este modelo esté bien definido

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

        # Consulta para obtener todas las órdenes de compra
        query = """
            SELECT id, codigo_tienda, estado, observaciones, orden_despacho, fecha_solicitud, fecha_recepcion
            FROM orden_de_compra
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
            total_cantidad=fila.get('total_cantidad', 0)  # Si 'total_cantidad' no está en el resultado, asignar 0
        ) for fila in resultados]
