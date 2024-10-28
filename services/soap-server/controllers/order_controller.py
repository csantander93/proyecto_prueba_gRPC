from flask import request, Response
from zeep import Client
from order_service import OrderService
from xml.etree import ElementTree as ET

class OrderController:
    def __init__(self):
        self.service = OrderService()

    def get_orders(self):
        # Leer los parámetros de la solicitud SOAP
        soap_body = request.data
        # Procesar el cuerpo SOAP para extraer los parámetros
        params = self.parse_soap_body(soap_body)

        # Llamar al servicio de órdenes
        resultados = self.service.get_orders(**params)

        # Crear la respuesta SOAP
        response = self.create_soap_response(resultados)
        return Response(response=response, content_type='text/xml')

    def parse_soap_body(self, soap_body):
        # Utiliza ElementTree para extraer los parámetros del cuerpo SOAP
        root = ET.fromstring(soap_body)
        params = {
            'codigo_producto': root.find('.//codigo_producto').text,
            'fecha_inicio': root.find('.//fecha_inicio').text,
            'fecha_fin': root.find('.//fecha_fin').text,
            'estado': root.find('.//estado').text,
            'codigo_tienda': root.find('.//codigo_tienda').text
        }
        return params

    def create_soap_response(self, resultados):
        # Construye una respuesta SOAP en función de los resultados
        response_xml = "<Response>"
        for (codigo_producto, estado, codigo_tienda), cantidad in resultados.items():
            response_xml += f"<Order><CodigoProducto>{codigo_producto}</CodigoProducto><Estado>{estado}</Estado><CodigoTienda>{codigo_tienda}</CodigoTienda><Cantidad>{cantidad}</Cantidad></Order>"
        response_xml += "</Response>"
        return response_xml
