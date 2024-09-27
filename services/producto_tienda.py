from . import db

class ProductoTienda(db.Model):
    __tablename__ = 'producto_has_tienda'
    producto_idproducto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), primary_key=True)
    tienda_idtienda = db.Column(db.Integer, db.ForeignKey('tienda.id_tienda'), primary_key=True)
