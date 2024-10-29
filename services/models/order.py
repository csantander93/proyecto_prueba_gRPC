from .database import db
from enum import Enum
from datetime import datetime

class EstadoOrden(Enum):
    SOLICITADA = 'SOLICITADA'
    RECHAZADA = 'RECHAZADA'
    ACEPTADA = 'ACEPTADA'
    RECIBIDA = 'RECIBIDA'

class OrdenDeCompra(db.Model):
    _tablename_ = 'orden_de_compra'
    id = db.Column(db.Integer, primary_key=True)
    # codigo_tienda = db.Column(db.String(10), nullable=False)
    codigo_tienda = db.Column(db.Integer, db.ForeignKey('tienda.id'))

    estado = db.Column(db.String(20), default=EstadoOrden.SOLICITADA.value)
    observaciones = db.Column(db.String(255))
    orden_despacho = db.Column(db.String(255))
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_recepcion = db.Column(db.DateTime)
    items = db.relationship('Item', backref='orden_de_compra', lazy=True)

    def _repr_(self):
        return f'<OrdenDeCompra {self.id}, Tienda: {self.codigo_tienda}, Estado: {self.estado}>'

class Item(db.Model):
    _tablename_ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('orden_de_compra.id'), nullable=False)
    codigo_articulo = db.Column(db.String(45))
    color = db.Column(db.String(45))
    talle = db.Column(db.String(10))
    cantidad_solicitada = db.Column(db.Integer)

    def _repr_(self):
        return f'<Item {self.codigo_articulo}, Cantidad: {self.cantidad_solicitada}>'