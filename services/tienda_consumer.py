# from confluent_kafka import Consumer
# import json
# from models import db, OrdenDeCompra, OrdenDespacho, ArticuloProveedor  # Asumiendo que tienes un modelo Proveedor

# def consumir_respuestas():
#     codigo_tienda = 'T123'  # Código de la tienda; puede ser dinámico
#     topic_solicitudes = f"{codigo_tienda}_solicitudes"
#     topic_despacho = f"{codigo_tienda}_despacho"

#     conf = {
#         'bootstrap.servers': 'localhost:9092',
#         'group.id': f'grupo_tienda_{codigo_tienda}',
#         'auto.offset.reset': 'earliest'
#     }
#     consumer = Consumer(conf)
#     consumer.subscribe([topic_solicitudes, topic_despacho])

#     try:
#         while True:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 continue
#             if msg.error():
#                 print(f'Error: {msg.error()}')
#                 continue

#             mensaje = json.loads(msg.value().decode('utf-8'))

#             if msg.topic() == topic_solicitudes:
#                 procesar_mensaje_solicitudes(mensaje)
#             elif msg.topic() == topic_despacho:
#                 procesar_mensaje_despacho(mensaje)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         consumer.close()

# def procesar_mensaje_solicitudes(mensaje):
#     id_orden = mensaje['id_orden']
#     estado = mensaje['estado']
#     observaciones = mensaje.get('observaciones', '')
#     id_orden_despacho = mensaje.get('id_orden_despacho')

#     orden = OrdenDeCompra.query.get(id_orden)
#     if orden:
#         orden.estado = estado
#         orden.observaciones = observaciones
#         if id_orden_despacho: 
#             orden.orden_despacho = id_orden_despacho
#         db.session.commit()
#         print(f"Orden {id_orden} actualizada a estado {estado}")
#     else:
#         print(f"Orden {id_orden} no encontrada en la tienda")

# def procesar_mensaje_despacho(mensaje):
#     id_orden_despacho = mensaje['id_orden_despacho']
#     id_orden_compra = mensaje['id_orden_compra']
#     fecha_estimada_envio = mensaje['fecha_estimada_envio']
    
#     # Actualizar la orden de compra con el ID de la orden de despacho
#     orden = OrdenDeCompra.query.get(id_orden_compra)
#     if orden:
#         orden.orden_despacho = id_orden_despacho
#         db.session.commit()
#         print(f"Orden de despacho {id_orden_despacho} asociada a la orden de compra {id_orden_compra}")

#         # Actualizar stock del proveedor
#         # restar_stock_proveedor(orden)
#     else:
#         print(f"Orden {id_orden_compra} no encontrada en la tienda")

# # def restar_stock_proveedor(orden):
# #     for item in orden.articulos:  # Asumiendo que tienes una relación de artículos en la orden
# #         proveedor = Proveedor.query.get(item.id_proveedor)  # Asumiendo que cada artículo tiene un proveedor
# #         if proveedor:
# #             proveedor.stock -= item.cantidad  # Restar la cantidad solicitada
# #             db.session.commit()
# #             print(f"Stock del proveedor {proveedor.id} actualizado: nueva cantidad {proveedor.stock}")
# #         else:
# #             print(f"Proveedor no encontrado para el artículo {item.id}")

# # Iniciar la función de consumo
# if __name__ == "__main__":
#     consumir_respuestas()
from confluent_kafka import Consumer
import json
from models import db, OrdenDeCompra, OrdenDespacho, ArticuloProveedor  # Asumiendo que tienes un modelo Proveedor
from flask import Flask
from app import app  # Importa tu aplicación Flask desde donde esté definida

def consumir_respuestas():
    codigo_tienda = 'T123'  # Código de la tienda; puede ser dinámico
    topic_solicitudes = f"{codigo_tienda}_solicitudes"
    topic_despacho = f"{codigo_tienda}_despacho"

    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': f'grupo_tienda_{codigo_tienda}',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe([topic_solicitudes, topic_despacho])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f'Error: {msg.error()}')
                continue

            mensaje = json.loads(msg.value().decode('utf-8'))

            if msg.topic() == topic_solicitudes:
                procesar_mensaje_solicitudes(mensaje)
            elif msg.topic() == topic_despacho:
                procesar_mensaje_despacho(mensaje)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def procesar_mensaje_solicitudes(mensaje):
    id_orden = mensaje['id_orden']
    estado = mensaje['estado']
    observaciones = mensaje.get('observaciones', '')
    id_orden_despacho = mensaje.get('id_orden_despacho')

    orden = OrdenDeCompra.query.get(id_orden)
    if orden:
        orden.estado = estado
        # orden.observaciones = observaciones
        orden.observaciones = ', '.join(mensaje['observaciones']) if isinstance(mensaje['observaciones'], list) else mensaje['observaciones']

        if id_orden_despacho: 
            orden.orden_despacho = id_orden_despacho
        db.session.commit()
        print(f"Orden {id_orden} actualizada a estado {estado}")
    else:
        print(f"Orden {id_orden} no encontrada en la tienda")




def procesar_mensaje_despacho(mensaje):
    id_orden_despacho = mensaje['id_orden_despacho']
    id_orden_compra = mensaje['id_orden_compra']
    fecha_estimada_envio = mensaje['fecha_estimacion_envio']
    
    orden = OrdenDeCompra.query.get(id_orden_compra)
    if orden:
        orden.orden_despacho = id_orden_despacho
        db.session.commit()
        print(f"Orden de despacho {id_orden_despacho} asociada a la orden de compra {id_orden_compra}")
    else:
        print(f"Orden {id_orden_compra} no encontrada en la tienda")

if __name__ == "__main__":
    with app.app_context():
        consumir_respuestas()
