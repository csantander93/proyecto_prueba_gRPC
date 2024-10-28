import xml.etree.ElementTree as ET
from flask import Blueprint, Response, jsonify, render_template
from services.orden_compra_service import OrdenCompraService
import os

orden_compra_bp = Blueprint('orden_compra', __name__)
orden_compra_service = OrdenCompraService()

@orden_compra_bp.route('/api/ordenes_compra', methods=['GET'])
def obtener_ordenes_compra():
    try:
        xml_data = orden_compra_service.obtener_ordenes_compra()
        
        # Convertir el XML a JSON
        json_data = xml_to_json(xml_data)
        
        return jsonify(json_data)  # Retorna JSON en vez de XML
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@orden_compra_bp.route('/ordenes_compra', methods=['GET'])
def mostrar_ordenes_compra():
    # Servir el archivo HTML para mostrar las órdenes de compra
    return render_template('ordenes_compra.html')  # Asumiendo que el HTML está en la carpeta templates

def xml_to_json(xml_string):
    root = ET.fromstring(xml_string)
    ordenes = []
    for orden in root.findall('OrdenCompra'):
        orden_data = {child.tag: child.text for child in orden}
        ordenes.append(orden_data)
    return ordenes
