from flask import Blueprint, jsonify, request
from models import db
from models import CatalogoProducto, Producto
from zeep import Client  # Para consumir servicios SOAP
import os

catalogo_bp = Blueprint('catalogo', __name__)

# Endpoint REST para crear un catálogo
@catalogo_bp.route('/catalogos', methods=['POST'])
def crear_catalogo():
    data = request.json
    nuevo_catalogo = CatalogoProducto(titulo=data['titulo'], id_tienda=data['id_tienda'])
    db.session.add(nuevo_catalogo)
    db.session.commit()
    return jsonify({'message': 'Catálogo creado con éxito'}), 201

# Endpoint REST para obtener todos los catálogos
@catalogo_bp.route('/catalogos', methods=['GET'])
def obtener_catalogos():
    catalogos = CatalogoProducto.query.all()
    catalogo_list = [{'id': c.id, 'titulo': c.titulo, 'id_tienda': c.id_tienda} for c in catalogos]
    return jsonify(catalogo_list), 200

# Endpoint REST para actualizar un catálogo por ID
@catalogo_bp.route('/catalogos/<int:id>', methods=['PUT'])
def actualizar_catalogo(id):
    data = request.json
    catalogo = CatalogoProducto.query.get_or_404(id)
    catalogo.titulo = data.get('titulo', catalogo.titulo)
    db.session.commit()
    return jsonify({'message': 'Catálogo actualizado con éxito'}), 200

# Endpoint REST para eliminar un catálogo por ID
@catalogo_bp.route('/catalogos/<int:id>', methods=['DELETE'])
def eliminar_catalogo(id):
    catalogo = CatalogoProducto.query.get_or_404(id)
    db.session.delete(catalogo)
    db.session.commit()
    return jsonify({'message': 'Catálogo eliminado con éxito'}), 200

### Configuración SOAP ###
SOAP_WSDL_URL = os.getenv('SOAP_WSDL_URL')  # URL del WSDL del servicio SOAP

# Ejemplo de consumir un servicio SOAP para obtener un catálogo por ID
@catalogo_bp.route('/catalogos/soap/<int:id>', methods=['GET'])
def obtener_catalogo_soap(id):
    client = Client(SOAP_WSDL_URL)
    response = client.service.obtenerCatalogo(id=id)
    return jsonify(response), 200

# Ejemplo de enviar datos a un servicio SOAP para crear un catálogo
@catalogo_bp.route('/catalogos/soap', methods=['POST'])
def crear_catalogo_soap():
    data = request.json
    client = Client(SOAP_WSDL_URL)
    response = client.service.crearCatalogo(titulo=data['titulo'], id_tienda=data['id_tienda'])
    return jsonify({'message': response}), 201
