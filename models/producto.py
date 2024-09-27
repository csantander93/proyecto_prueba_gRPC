from .database import db

class Producto(db.Model):
    __tablename__ = 'producto'
    id_producto = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False)
    talle = db.Column(db.String(45))
    foto = db.Column(db.String(45))
    color = db.Column(db.String(45))
    stock = db.Column(db.Integer)
    habilitada = db.Column(db.Boolean, default=True)  # Si necesitas un campo habilitada

    def __repr__(self):
        return f'<Producto {self.codigo}, Talle: {self.talle}, Color: {self.color}>'
