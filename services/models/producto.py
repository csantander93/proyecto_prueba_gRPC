from .database import db

class Producto(db.Model):
    __tablename__ = 'producto'
    id_producto = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)  # Agregado: Nombre del producto
    talle = db.Column(db.String(45))
    foto = db.Column(db.String(45))
    color = db.Column(db.String(45))
    stock = db.Column(db.Integer)

    # Relación con Tienda
    id_tienda = db.Column(db.Integer, db.ForeignKey('tienda.id_tienda'), nullable=False)  # Clave foránea a tienda
    tienda = db.relationship('Tienda', backref=db.backref('productos', lazy=True))  # Relación con Tienda
    
    def __repr__(self):
        return f'<Producto {self.codigo}, Talle: {self.talle}, Color: {self.color}>'
