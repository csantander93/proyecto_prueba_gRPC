from .database import db
import json
from datetime import datetime

class NovedadProducto(db.Model):
    __tablename__ = 'novedad_producto'
    id = db.Column(db.Integer, primary_key=True)
    codigo_producto = db.Column(db.String(45), unique=True, nullable=False)
    talles_colores = db.Column(db.Text, nullable=False)
    urls_fotos = db.Column(db.Text, nullable=False)
    fecha_recepcion = db.Column(db.DateTime, default=datetime.utcnow)
    procesado = db.Column(db.Boolean, default=False)

    def get_talles_colores(self):
        return json.loads(self.talles_colores)

    def get_urls_fotos(self):
        return json.loads(self.urls_fotos)

    def __repr__(self):
        return f'<NovedadProducto {self.codigo_producto}>'

