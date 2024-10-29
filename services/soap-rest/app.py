# app.py

from flask import Flask
from flask_restx import Api
from config.swagger_config import create_api
from controllers.orden_compra_controller import orden_compra_bp
from controllers.usuario_controller import usuario_bp  # Asegúrate de importar el controlador de usuarios

app = Flask(__name__)

# Crear la instancia de Swagger usando la configuración de Swagger
api = create_api(app)

# Registra los blueprints
app.register_blueprint(orden_compra_bp)
app.register_blueprint(usuario_bp)  # Asegúrate de registrar el blueprint de usuario

if __name__ == '__main__':
    app.run(debug=True)
