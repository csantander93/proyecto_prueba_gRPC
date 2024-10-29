from flask import Flask
from routes import order_bp  # Asegúrate de que la ruta sea correcta

def create_app():
    app = Flask(__name__)
    app.register_blueprint(order_bp)  # Registra tu blueprint

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)  # Puedes usar otro puerto si el 5000 ya está ocupado
