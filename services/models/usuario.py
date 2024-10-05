from .database import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(500))
    habilitado = db.Column(db.Boolean)  # TINYINT en MySQL
    tienda_idtienda = db.Column(db.Integer, db.ForeignKey('tienda.id_tienda'))

    def __repr__(self):
        return f'<Usuario {self.username}, Habilitado: {self.habilitado}>'
