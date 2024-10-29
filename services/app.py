from flask import Flask
from models.database import db
from models.tienda import Tienda
from models.producto import Producto
from models.order import OrdenDeCompra
from models.usuario import Usuario
from routes.catalogo_routes import catalogo_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:giuli123@localhost/stockearte'  # Cambia esto por tus credenciales
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Registrar Blueprints
app.register_blueprint(catalogo_bp)

@app.route('/')
def index():
    return app.send_static_file('catalogo.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear tablas
    app.run(debug=True)