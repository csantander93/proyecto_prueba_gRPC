from confluent_kafka import Consumer, Producer, KafkaException
from models import db, ArticuloProveedor, OrdenDespacho, OrdenCompraProveedor
from app_proveedor import app
from datetime import datetime, timedelta
import json
from flask import Flask, request, jsonify
import json
# Configuración de Kafka
KAFKA_BROKER = 'localhost:9092'
TOPIC_ORDENES = 'orden-de-compra'

# Configuración del consumidor
consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'proveedor-consumer-group',
    'auto.offset.reset': 'earliest'
}

# Configuración del productor
producer_conf = {
    'bootstrap.servers': KAFKA_BROKER
}

# Inicializar consumidor y productor
consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

def enviar_a_kafka(topic, mensaje):
    """Envía un mensaje a un tópico de Kafka."""
    producer.produce(topic, json.dumps(mensaje).encode('utf-8'))
    producer.flush()


# @app.route('/reprocesar_orden', methods=['POST'])
# def reprocesar_orden():
#     """Endpoint para reprocesar una orden pausada."""
#     orden = request.get_json()
#     codigo_tienda = orden.get("codigo_tienda")
#     orden_id = orden.get("id_orden")
#     items = orden.get("items", [])
    
#     # Llamar a la función de procesamiento de la orden con la lógica existente
#     try:
#         procesar_orden(json.dumps(orden))
#         return jsonify({"message": f"Orden {orden_id} procesada exitosamente."}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# def procesar_orden(mensaje):
#     with app.app_context():
#         orden = json.loads(mensaje)
#         codigo_tienda = orden.get("codigo_tienda")
#         orden_id = orden.get("id_orden")
#         items = orden.get("items", [])

#         observaciones = []
#         estado_orden = "ACEPTADA"
#         stock_suficiente = True

#         # Validar cada item de la orden
#         for item in items:
#             codigo_articulo = item.get("codigo_articulo")
#             cantidad = item.get("cantidad_solicitada")

#             # Validaciones de artículo
#             articulo = ArticuloProveedor.query.filter_by(codigo_articulo=codigo_articulo).first()
#             if not articulo:
#                 observaciones.append(f"Artículo {codigo_articulo}: no existe")
#                 estado_orden = "RECHAZADA"
#             elif cantidad < 1:
#                 observaciones.append(f"Artículo {codigo_articulo}: cantidad mal informada")
#                 estado_orden = "RECHAZADA"
#             elif articulo.stock < cantidad:
#                 observaciones.append(f"Artículo {codigo_articulo}: stock insuficiente")
#                 stock_suficiente = False

#         # Procesar estado de la orden
#         if estado_orden == "RECHAZADA":
#             # Publicar el estado rechazado con las observaciones
#             enviar_a_kafka(
#                 f"/{codigo_tienda}/solicitudes",
#                 {"estado": estado_orden, "observaciones": observaciones, "id_orden": orden_id}
#             )
#         else:
#             if not stock_suficiente:
#                 observaciones.append("Orden aceptada, pero con faltante de stock en algunos artículos.")
#                 # Aquí puedes decidir si quieres pausar la orden hasta que haya stock suficiente
#                 # En este ejemplo, simplemente informamos a la tienda
#             else:
#                 # Reducir el stock de los artículos si la orden es completamente aceptada
#                 for item in items:
#                     codigo_articulo = item["codigo_articulo"]
#                     cantidad = item["cantidad_solicitada"]
#                     articulo = ArticuloProveedor.query.filter_by(codigo_articulo=codigo_articulo).first()
#                     articulo.stock -= cantidad
#                 db.session.commit()

#                 # Generar una orden de despacho
#                 nueva_orden_despacho = OrdenDespacho(
#                     id_orden_compra=orden_id,
#                     fecha_estimada_envio=datetime.utcnow() + timedelta(days=2)  # Fecha estimada de envío
#                 )
#                 db.session.add(nueva_orden_despacho)
#                 db.session.commit()

#                 # Publicar la orden de despacho
#                 enviar_a_kafka(
#                     f"{codigo_tienda}_despacho",
#                     {
#                         "id_orden_despacho": nueva_orden_despacho.id,
#                         "id_orden_compra": orden_id,
#                         "fecha_estimacion_envio": nueva_orden_despacho.fecha_estimada_envio.isoformat()
#                     }
#                 )

#             # Publicar el estado aceptado con las observaciones (incluso si hay faltantes)
#             enviar_a_kafka(
#                 f"{codigo_tienda}_solicitudes",
#                 {"estado": estado_orden, "observaciones": observaciones, "id_orden": orden_id}
#             )
# def procesar_orden(mensaje):
#     with app.app_context():
#         orden_data = json.loads(mensaje)
#         codigo_tienda = orden_data.get("codigo_tienda")
#         orden_id = orden_data.get("id_orden")
#         items = orden_data.get("items", [])
#         fecha_solicitud = orden_data.get("fecha_solicitud")

#         observaciones = []
#         estado_orden = "ACEPTADA"
#         stock_suficiente = True

#         # Validar cada item de la orden
#         for item in items:
#             codigo_articulo = item.get("codigo_articulo")
#             cantidad = item.get("cantidad_solicitada")

#             # Validaciones de artículo
#             articulo = ArticuloProveedor.query.filter_by(codigo_articulo=codigo_articulo).first()
#             if not articulo:
#                 observaciones.append(f"Artículo {codigo_articulo}: no existe")
#                 estado_orden = "RECHAZADA"
#             elif cantidad < 1:
#                 observaciones.append(f"Artículo {codigo_articulo}: cantidad mal informada")
#                 estado_orden = "RECHAZADA"
#             elif articulo.stock < cantidad:
#                 observaciones.append(f"Artículo {codigo_articulo}: stock insuficiente")
#                 stock_suficiente = False

#         # Buscar la orden en la base de datos
#         orden_proveedor = OrdenCompraProveedor.query.filter_by(id_orden=orden_id).first()

#         if orden_proveedor:
#             # Si la orden ya existe, actualizar su estado y observaciones
#             orden_proveedor.estado = "ACEPTADA" if estado_orden == "ACEPTADA" else "RECHAZADA"
#             orden_proveedor.observaciones = "; ".join(observaciones) if observaciones else orden_proveedor.observaciones
#             db.session.commit()
#         else:
#             # Si la orden no existe, crear una nueva entrada
#             orden_proveedor = OrdenCompraProveedor(
#                 id_orden=orden_id,
#                 codigo_tienda=codigo_tienda,
#                 estado="",
#                 observaciones="",
#                 items=json.dumps(items),
#                 fecha_creacion=datetime.utcnow()
#             )
#             db.session.add(orden_proveedor)

#         # Procesar estado de la orden
#         if estado_orden == "RECHAZADA":
#             db.session.commit()

#             # Publicar el estado rechazado con las observaciones
#             enviar_a_kafka(
#                 f"{codigo_tienda}_solicitudes",
#                 {"estado": estado_orden, "observaciones": observaciones, "id_orden": orden_id}
#             )
#         else:
#             if not stock_suficiente:
#                 orden_proveedor.estado = "PAUSADA"
#                 orden_proveedor.observaciones = "; ".join(observaciones)
#                 db.session.commit()

#                 # Informar a la tienda sobre los artículos con faltante
#                 enviar_a_kafka(
#                     f"{codigo_tienda}_solicitudes",
#                     {"estado": orden_proveedor.estado, "observaciones": observaciones, "id_orden": orden_id}
#                 )
#             else:
#                 # Reducir el stock de los artículos
#                 for item in items:
#                     codigo_articulo = item["codigo_articulo"]
#                     cantidad = item["cantidad_solicitada"]
#                     articulo = ArticuloProveedor.query.filter_by(codigo_articulo=codigo_articulo).first()
#                     if articulo:
#                         articulo.stock -= cantidad
#                 db.session.commit()

#                 # Generar orden de despacho
#                 nueva_orden_despacho = OrdenDespacho(
#                     id_orden_compra=orden_id,
#                     fecha_estimada_envio=datetime.utcnow() + timedelta(days=2)
#                 )
#                 db.session.add(nueva_orden_despacho)

#                 # Actualizar estado de la orden
#                 orden_proveedor.estado = "PROCESADA"
#                 orden_proveedor.observaciones = "Orden aceptada y procesada"
#                 db.session.commit()

#                 # Publicar la orden de despacho y notificar a la tienda
#                 enviar_a_kafka(
#                     f"{codigo_tienda}_solicitudes",
#                     {
#                         "estado": orden_proveedor.estado,
#                         "observaciones": observaciones,
#                         "id_orden": orden_id,
#                         "id_orden_despacho": nueva_orden_despacho.id
#                     }
#                 )

#                 enviar_a_kafka(
#                     f"{codigo_tienda}_despacho",
#                     {
#                         "id_orden_despacho": nueva_orden_despacho.id,
#                         "id_orden_compra": orden_id,
#                         "fecha_estimacion_envio": nueva_orden_despacho.fecha_estimada_envio.isoformat()
#                     }
#                 )

#         print(f"Orden {orden_id} procesada con estado {orden_proveedor.estado}")
def procesar_orden(mensaje):
    with app.app_context():
        orden_data = json.loads(mensaje)
        codigo_tienda = orden_data.get("codigo_tienda")
        orden_id = orden_data.get("id_orden")
        items = orden_data.get("items", [])
        fecha_solicitud = orden_data.get("fecha_solicitud")

        observaciones = []
        estado_orden = "ACEPTADA"
        stock_suficiente = True

        # Validar cada item de la orden
        for item in items:
            codigo_articulo = item.get("codigo_articulo")
            cantidad = item.get("cantidad_solicitada")

            # Validaciones de artículo
            articulo = ArticuloProveedor.query.filter_by(codigo_articulo=codigo_articulo).first()
            if not articulo:
                observaciones.append(f"Artículo {codigo_articulo}: no existe")
                estado_orden = "RECHAZADA"
            elif cantidad < 1:
                observaciones.append(f"Artículo {codigo_articulo}: cantidad mal informada")
                estado_orden = "RECHAZADA"
            elif articulo.stock < cantidad:
                observaciones.append(f"Artículo {codigo_articulo}: stock insuficiente")
                stock_suficiente = False

        # Buscar la orden en la base de datos
        orden_proveedor = OrdenCompraProveedor.query.filter_by(id_orden=orden_id).first()

        # Si la orden no existe, crear una nueva entrada
        if not orden_proveedor:
            orden_proveedor = OrdenCompraProveedor(
                id_orden=orden_id,
                codigo_tienda=codigo_tienda,
                estado="",
                observaciones="",
                items=json.dumps(items),
                fecha_creacion=datetime.utcnow()
            )
            db.session.add(orden_proveedor)
            db.session.commit()  # Guardar la nueva orden antes de continuar

        # Procesar estado de la orden
        if estado_orden == "RECHAZADA":
            orden_proveedor.estado = "RECHAZADA"
            orden_proveedor.observaciones = "; ".join(observaciones)
            db.session.commit()

            # Publicar el estado rechazado con las observaciones
            enviar_a_kafka(
                f"{codigo_tienda}_solicitudes",
                {"estado": estado_orden, "observaciones": observaciones, "id_orden": orden_id}
            )
        else:
            if not stock_suficiente:
                orden_proveedor.estado = "PAUSADA"
                orden_proveedor.observaciones = "; ".join(observaciones)
                db.session.commit()

                # Informar a la tienda sobre los artículos con faltante
                enviar_a_kafka(
                    f"{codigo_tienda}_solicitudes",
                    {"estado": orden_proveedor.estado, "observaciones": observaciones, "id_orden": orden_id}
                )
            else:
                # Reducir el stock de los artículos
                for item in items:
                    codigo_articulo = item["codigo_articulo"]
                    cantidad = item["cantidad_solicitada"]
                    articulo = ArticuloProveedor.query.filter_by(codigo_articulo=codigo_articulo).first()
                    if articulo:
                        articulo.stock -= cantidad
                db.session.commit()

                # Generar orden de despacho
                nueva_orden_despacho = OrdenDespacho(
                    id_orden_compra=orden_id,
                    fecha_estimada_envio=datetime.utcnow() + timedelta(days=2)
                )
                db.session.add(nueva_orden_despacho)

                # Actualizar estado de la orden
                orden_proveedor.estado = "PROCESADA"
                orden_proveedor.observaciones = "Orden aceptada y procesada"
                db.session.commit()

                # Publicar la orden de despacho y notificar a la tienda
                enviar_a_kafka(
                    f"{codigo_tienda}_solicitudes",
                    {
                        "estado": orden_proveedor.estado,
                        "observaciones": observaciones,
                        "id_orden": orden_id,
                        "id_orden_despacho": nueva_orden_despacho.id
                    }
                )

                enviar_a_kafka(
                    f"{codigo_tienda}_despacho",
                    {
                        "id_orden_despacho": nueva_orden_despacho.id,
                        "id_orden_compra": orden_id,
                        "fecha_estimacion_envio": nueva_orden_despacho.fecha_estimada_envio.isoformat()
                    }
                )

        print(f"Orden {orden_id} procesada con estado {orden_proveedor.estado}")

def main():
    consumer.subscribe([TOPIC_ORDENES])

    print("Proveedor en espera de órdenes de compra...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
                continue

            print(f"Orden recibida: {msg.value().decode('utf-8')}")
            procesar_orden(msg.value().decode('utf-8'))

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    with app.app_context():
        main()