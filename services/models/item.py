# models/item.py
from .database import db

# class Item(db.Model):
#     __tablename__ = 'items'
    
#     id = Column(Integer, primary_key=True)
#     #codigo_articulo = Column(String(50), nullable=False)
#     # color = Column(String(50), nullable=False)
#     # talle = Column(String(50), nullable=False)
#     codigo_articulo = db.relationship('Producto', backref='item', lazy=True)

#     cantidad_solicitada = Column(Integer, nullable=False)
#     orden_compra_id = Column(Integer, ForeignKey('ordenes_compra.id'), nullable=False)

#     def __repr__(self):
#         return f'<Item {self.codigo_articulo} - Cantidad: {self.cantidad_solicitada}>'

# class ItemModel(db.Model):
#     __tablename__ = 'items'

#     id_item = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     # codigo_articulo = db.Column(db.String(50), nullable=False)
#     orden_compra_id = db.Column(db.Integer, db.ForeignKey('ordenes_compra.id'), nullable=False)
#     color = db.Column(db.String(20), nullable=False)
#     talle = db.Column(db.String(5), nullable=False)
#     cantidad = db.Column(db.Integer, nullable=False)
#     # codigo_articulo = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
#     ordenes_compra = db.relationship("OrdenCompraModel", back_populates="items")
#     codigo_articulo = db.Column(db.String(10), db.ForeignKey('producto.codigo'), nullable=False)  

#     producto = db.relationship("Producto", back_populates="items")
        


#     def __repr__(self):
#         return f'<Item {self.id_item}, Codigo Articulo: {self.codigo_articulo}>'
class ItemModel(db.Model):
    __tablename__ = 'items'

    id_item = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orden_compra_id = db.Column(db.Integer, db.ForeignKey('ordenes_compra.id'), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    talle = db.Column(db.String(5), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    codigo_articulo = db.Column(db.String(10), db.ForeignKey('producto.codigo'), nullable=False)

    # Relaciones
    producto = db.relationship("Producto", back_populates="items")
    ordenes_compra = db.relationship("OrdenCompraModel", back_populates="items")

    def __repr__(self):
        return f'<Item {self.id_item}, Codigo Articulo: {self.codigo_articulo}>'
    

# def to_dict(self):
#         """Convierte una instancia de ItemModel a un diccionario"""
#         return {
#             'id_item': self.id_item,
#             'codigo_articulo': self.codigo_articulo,
#             'color': self.color,
#             'talle': self.talle,
#             'cantidad': self.cantidad
#         }