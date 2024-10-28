# config/swagger_config.py
from flask_restx import Api
from controllers.orden_compra_controller import api as orden_compra_ns

def create_api(app):
    api = Api(
        app,
        version="1.0",
        title="API de Órdenes de Compra",
        description="Documentación de la API para manejar las órdenes de compra",
        doc="/swagger"  # Ruta donde se desplegará Swagger
    )
    
    # Agregar el namespace del controlador de ordenes de compra
    api.add_namespace(orden_compra_ns)
    
    return api
