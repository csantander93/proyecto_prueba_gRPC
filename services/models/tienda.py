from .database import db
from sqlalchemy import event

class Tienda(db.Model):
    __tablename__ = 'tienda'
    id_tienda = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), nullable=False)
    nombre = db.Column(db.String(45))
    direccion = db.Column(db.String(45))
    ciudad = db.Column(db.String(45))
    provincia = db.Column(db.String(45))
    habilitada = db.Column(db.Boolean)  # TINYINT en MySQL
    casa_central = db.Column(db.Boolean)  # TINYINT en MySQL
    
    def __repr__(self):
        return f'<Tienda {self.codigo}, Nombre: {self.nombre}, Habilitada: {self.habilitada}>'