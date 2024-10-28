# controllers/orden_compra_controller.py

from flask import Blueprint, jsonify
from flask_restx import Namespace, Resource, fields
from services.orden_compra_service import OrdenCompraService
import xml.etree.ElementTree as ET

orden_compra_bp = Blueprint('orden_compra', __name__)
orden_compra_service = OrdenCompraService()

# Namespace para los endpoints
api = Namespace('api', description='Operaciones de Órdenes de Compra')

# Definición del modelo de orden para Swagger
orden_model = api.model('OrdenCompra', {
    'codigo_tienda': fields.String(description='Código de la tienda'),
    'estado': fields.String(description='Estado de la orden de compra'),
    'fecha_recepcion': fields.String(description='Fecha de recepción de la orden'),
    'fecha_solicitud': fields.String(description='Fecha de solicitud de la orden'),
    'id': fields.Integer(description='ID de la orden de compra'),
    'observaciones': fields.String(description='Observaciones de la orden de compra'),
    'orden_despacho': fields.String(description='Orden de despacho asociada'),
    'total_cantidad': fields.Integer(description='Cantidad total de productos')
})

@api.route('/ordenes_compra')
class OrdenesCompraResource(Resource):
    @api.doc(description="Obtener todas las órdenes de compra")
    @api.marshal_list_with(orden_model)
    def get(self):
        """Retorna todas las órdenes de compra en formato JSON."""
        try:
            xml_data = orden_compra_service.obtener_ordenes_compra()
            json_data = xml_to_json(xml_data)
            return json_data
        except Exception as e:
            api.abort(500, e.__doc__, status="Error al obtener las órdenes de compra", statusCode="500")

def xml_to_json(xml_string):
    root = ET.fromstring(xml_string)
    ordenes = []
    for orden in root.findall('OrdenCompra'):
        orden_data = {child.tag: child.text for child in orden}
        ordenes.append(orden_data)
    return ordenes
