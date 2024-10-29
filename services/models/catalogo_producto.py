from .database import db

catalogo_producto_rel = db.Table(
    'catalogo_producto_rel',
    db.Column('id_catalogo', db.Integer, db.ForeignKey('catalogo_producto.id_catalogo'), primary_key=True),
    db.Column('id_producto', db.Integer, db.ForeignKey('producto.id_producto'), primary_key=True)
)
