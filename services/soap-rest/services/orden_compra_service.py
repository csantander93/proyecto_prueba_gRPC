# /soap_rest/services/orden_compra_service.py

import mysql.connector
from typing import List
from models.orden_compra import OrdenCompra
from .soap_client import SoapClient  # Importa el cliente SOAP
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom  # Agregar esta importación

class OrdenCompraService:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'database': 'stockearte'
        }
        self.soap_client = SoapClient('static/orden_compra_service.wsdl')  # Proporciona la URL de tu WSDL

    def obtener_ordenes_compra(self) -> str:  # Cambié el tipo de retorno a str para el XML
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor(dictionary=True)

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
        cursor.close()
        connection.close()

        # Llamar al servicio SOAP si necesitas datos adicionales
        # Por ejemplo, obtener información relacionada con las órdenes de compra
        # datos_soap = self.soap_client.obtener_datos()  # Descomenta si necesitas usar datos del SOAP

        # Crear el XML para devolver
        return self._convertir_a_xml(resultados)

    def _convertir_a_xml(self, ordenes: List[dict]) -> str:
        root = Element('OrdenesCompra')
        for orden in ordenes:
            orden_elem = SubElement(root, 'OrdenCompra')
            SubElement(orden_elem, 'id').text = str(orden['id'])
            SubElement(orden_elem, 'codigo_tienda').text = orden['codigo_tienda']
            SubElement(orden_elem, 'estado').text = orden['estado']
            SubElement(orden_elem, 'observaciones').text = orden['observaciones']
            SubElement(orden_elem, 'orden_despacho').text = orden['orden_despacho']
            
            SubElement(orden_elem, 'fecha_solicitud').text = orden['fecha_solicitud'].isoformat() if orden['fecha_solicitud'] else ''
            SubElement(orden_elem, 'fecha_recepcion').text = orden['fecha_recepcion'].isoformat() if orden['fecha_recepcion'] else ''

            SubElement(orden_elem, 'total_cantidad').text = str(orden['total_cantidad'])

        # Convertir a string y luego formatear el XML
        xml_string = tostring(root, encoding='utf-8').decode('utf-8')
        # Usar minidom para formatear el XML
        xml_pretty = minidom.parseString(xml_string).toprettyxml(indent="    ")

        return xml_pretty
