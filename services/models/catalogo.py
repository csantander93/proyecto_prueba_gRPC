from .database import db

class CatalogoProducto(db.Model):
    __tablename__ = 'catalogo_producto'
    id_catalogo = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)  # Título del catálogo
    id_tienda = db.Column(db.Integer, db.ForeignKey('tienda.id_tienda'), nullable=False)  # Relación con la tienda

    tienda = db.relationship('Tienda', backref=db.backref('catalogos', lazy=True))
    productos = db.relationship('Producto', secondary='catalogo_producto_rel', lazy='subquery',
                                backref=db.backref('catalogos', lazy=True))

    def __repr__(self):
        return f'<CatalogoProducto {self.id_catalogo}, Título: {self.titulo}>'
