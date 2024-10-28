# /soap_rest/app.py

from flask import Flask
from flask_restx import Api
from config.swagger_config import create_api
from controllers.orden_compra_controller import orden_compra_bp

app = Flask(__name__)

# Crear la instancia de Swagger usando la configuración de Swagger
api = create_api(app)

# Registra el blueprint
app.register_blueprint(orden_compra_bp)

if __name__ == '__main__':
    app.run(debug=True)
