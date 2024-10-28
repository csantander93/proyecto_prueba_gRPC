# /soap_rest/controllers/orden_compra_controller.py

from flask import Blueprint, jsonify
from services.orden_compra_service import OrdenCompraService

# Inicializa el blueprint para el controlador de órdenes de compra
orden_compra_bp = Blueprint('orden_compra', __name__)
orden_compra_service = OrdenCompraService()

@orden_compra_bp.route('/api/ordenes_compra', methods=['GET'])
def obtener_ordenes_compra():
    resultado = orden_compra_service.obtener_ordenes_compra()
    
    # Convertir el resultado a un formato JSON amigable
    return jsonify([{
        'codigo_tienda': orden.codigo_tienda,
        'estado': orden.estado,
        'total_cantidad': orden.total_cantidad
    } for orden in resultado])