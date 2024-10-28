from database import db
from datetime import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

# class ArticuloProveedor(db.Model):
#     __tablename__ = 'articulo_proveedor'  
#     id = db.Column(db.Integer, primary_key=True)
#     codigo_articulo = db.Column(db.String(45), unique=True, nullable=False)
#     nombre = db.Column(db.String(255))
#     talle = db.Column(db.String(255))
#     color = db.Column(db.String(255))
#     stock = db.Column(db.Integer, default=0)

#     def __repr__(self):
#         return f'<ArticuloProveedor {self.codigo_articulo} - Stock: {self.stock}>'


class ArticuloProveedor(db.Model):
    __tablename__ = 'articulo_proveedor'
    id = db.Column(db.Integer, primary_key=True)
    codigo_articulo = db.Column(db.String(45), unique=True, nullable=False)
    nombre = db.Column(db.String(255))
    # Eliminamos los campos 'talle' y 'color' individuales
    # Agregamos los nuevos campos
    talles_colores = db.Column(MutableList.as_mutable(PickleType), default=[])
    urls_fotos = db.Column(MutableList.as_mutable(PickleType), default=[])
    stock = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<ArticuloProveedor {self.codigo_articulo} - Stock: {self.stock}>'


class OrdenDespacho(db.Model):
    __tablename__ = 'orden_despacho'  # Doble guion bajo al inicio y al final
    id = db.Column(db.Integer, primary_key=True)
    id_orden_compra = db.Column(db.Integer, nullable=False)
    fecha_estimada_envio = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<OrdenDespacho {self.id} - OrdenCompra: {self.id_orden_compra}>'

class OrdenCompraProveedor(db.Model):
    __tablename__ = 'orden_compra_proveedor'
    id = db.Column(db.Integer, primary_key=True)
    id_orden = db.Column(db.Integer, nullable=False, unique=True)  # ID de la orden de compra original
    codigo_tienda = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    observaciones = db.Column(db.Text)
    items = db.Column(db.Text)  # Almacenar los items en formato JSON
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<OrdenCompraProveedor {self.id_orden} - Estado: {self.estado}>'
