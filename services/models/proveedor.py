from .database import db


class ArticuloProveedor(db.Model):
    _tablename_ = 'articulo_proveedor'
    id = db.Column(db.Integer, primary_key=True)
    codigo_articulo = db.Column(db.String(45), unique=True, nullable=False)
    nombre = db.Column(db.String(255))
    talle=db.Column(db.String(255))
    color=db.Column(db.String(255))
    stock = db.Column(db.Integer, default=0)

    def _repr_(self):
        return f'<ArticuloProveedor {self.codigo_articulo} - Stock: {self.stock}>'
    

    INVENTARIO = {
    "A123": {
        "color": "rojo",
        "talle": "M",
        "stock": 100
    },
    "B456": {
        "color": "azul",
        "talle": "L",
        "stock": 50
    },
    "A125": {
        "color": "verde",
        "talle": "S",
        "stock": 200
    }

}
    
class OrdenDespacho(db.Model):
    _tablename_ = 'orden_despacho'
    id = db.Column(db.Integer, primary_key=True)
    id_orden_compra = db.Column(db.Integer, nullable=False)
    fecha_estimada_envio = db.Column(db.DateTime, nullable=False)

    def _repr_(self):
        return f'<OrdenDespacho {self.id} - OrdenCompra: {self.id_orden_compra}>'