from flask import Flask
from models.database import db
from models.tienda import Tienda
from models.producto import Producto
from models.usuario import Usuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/stockearte'  # Cambia esto por tus credenciales
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()  # Crea todas las tablas

if __name__ == '__main__':
    app.run(debug=True)
