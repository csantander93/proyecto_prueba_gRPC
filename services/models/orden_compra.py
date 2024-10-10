from .database import db
from datetime import datetime

import json
# from flask_sqlalchemy import event

class OrdenCompraModel(db.Model):
    __tablename__ = 'ordenes_compra'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo_tienda = db.Column(db.Integer, db.ForeignKey('tienda.id_tienda'), nullable=False)  

    estado = db.Column(db.Enum('SOLICITADA', 'RECHAZADA', 'ACEPTADA', 'RECIBIDA'), default='SOLICITADA')
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # fecha_recepcion = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    fecha_recepcion = db.Column(db.DateTime, default=None, nullable=True)

    observaciones = db.Column(db.String(255))
    orden_despacho = db.Column(db.String(255))



    store = db.relationship("Tienda", back_populates="ordenes_compra", lazy=True)
    items = db.relationship("ItemModel", back_populates="ordenes_compra", cascade="all, delete-orphan")
    # tienda = db.relationship('Tienda', backref='ordenes_compra', lazy=True)

    # # Relación con los items
    # items = db.relationship('ItemModel', backref='orden_compra', lazy=True)

    def __repr__(self):
        return f'<OrdenCompra {self.id}, Estado: {self.estado}, Tienda: {self.codigo_tienda}>'


# def enviar_mensaje_a_topic(self):
#         mensaje = {
#             'codigo_tienda': self.codigo_tienda,
#             'id_orden': self.id,
#             'items_solicitados': [item.to_dict() for item in self.items],  # Asume que tienes un método to_dict en ItemModel
#             'fecha_solicitud': self.fecha_solicitud.isoformat(),
#         }

#         # Configura el productor de Kafka
#         producer = KafkaProducer(
#             bootstrap_servers='localhost:9092',  # Dirección del broker de Kafka
#             value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializador para JSON
#         )

#         # Envío del mensaje al topic '/orden-de-compra'
#         producer.send('orden-de-compra', mensaje)
#         producer.flush()  # Asegurarse de que el mensaje se envía antes de cerrar

#         print(f"Mensaje enviado al topic 'orden-de-compra': {json.dumps(mensaje)}")

#     # Configura el productor de Kafka
#         producer = KafkaProducer(
#             bootstrap_servers='localhost:9092',  # Dirección del broker de Kafka
#             value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializador para JSON
#         )

#         # Envío del mensaje al topic '/orden-de-compra'
#         producer.send('orden-de-compra', mensaje)
#         producer.flush()  # Asegurarse de que el mensaje se envía antes de cerrar

#         print(f"Mensaje enviado al topic 'orden-de-compra': {json.dumps(mensaje)}")


# # Evento que se ejecuta después de que una nueva orden se haya guardado en la base de datos
# @event.listens_for(OrdenCompraModel, 'after_insert')
# def after_insert(mapper, connection, target):
#     target.enviar_mensaje_a_topic()