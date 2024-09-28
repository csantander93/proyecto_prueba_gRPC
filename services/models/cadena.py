from .database import db

class Cadena(db.Model):
    __tablename__ = 'cadena'
    id_cadena = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))

    def __repr__(self):
        return f'<Cadena {self.id_cadena}, Nombre: {self.nombre}>'
