import json
import time
from confluent_kafka import Consumer, Producer

# Configuración del consumidor de Kafka
KAFKA_BROKER = 'localhost:9092'
TOPIC_ORDENES = 'ordenes_compra'
TOPIC_SOLICITUDES = '/{codigo_tienda}/solicitudes'
TOPIC_DESPACHO = '/{codigo_tienda}/despacho'

# Ejemplo de inventario del proveedor
INVENTARIO = {
    "A001": 100,
    "A002": 50,
    "A003": 200
}

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

def procesar_orden(mensaje):
    orden = json.loads(mensaje)
    codigo_tienda = orden.get("codigo_tienda")
    orden_id = orden.get("id_orden")
    items = orden.get("items", [])

    observaciones = []
    estado_orden = "ACEPTADA"
    stock_suficiente = True

    # Validar cada item de la orden
    for item in items:
        codigo_articulo = item.get("codigo_articulo")
        cantidad = item.get("cantidad_solicitada")

        # Validaciones de artículo
        if codigo_articulo not in INVENTARIO:
            observaciones.append(f"Artículo {codigo_articulo}: no existe")
            estado_orden = "RECHAZADA"
        elif cantidad < 1:
            observaciones.append(f"Artículo {codigo_articulo}: cantidad mal informada")
            estado_orden = "RECHAZADA"
        elif INVENTARIO[codigo_articulo] < cantidad:
            observaciones.append(f"Artículo {codigo_articulo}: stock insuficiente")
            stock_suficiente = False

    # Procesar estado de la orden
    if estado_orden == "RECHAZADA":
        # Publicar el estado rechazado con las observaciones
        producer.produce(
            f"/{codigo_tienda}/solicitudes",
            key=str(orden_id),
            value=json.dumps({"estado": estado_orden, "observaciones": observaciones})
        )
    else:
        if not stock_suficiente:
            estado_orden = "ACEPTADA"
            observaciones.append("Orden aceptada, pero con faltante de stock en algunos artículos.")
        else:
            # Reducir el stock de los artículos si la orden es completamente aceptada
            for item in items:
                codigo_articulo = item["codigo_articulo"]
                cantidad = item["cantidad_solicitada"]
                INVENTARIO[codigo_articulo] -= cantidad

            # Generar una orden de despacho
            id_despacho = f"DESP-{orden_id}"
            fecha_estimacion_envio = time.strftime("%Y-%m-%d", time.gmtime(time.time() + 86400))  # Estimación a 1 día

            # Publicar la orden de despacho
            producer.produce(
                f"/{codigo_tienda}/despacho",
                key=str(id_despacho),
                value=json.dumps({
                    "id_despacho": id_despacho,
                    "id_orden_compra": orden_id,
                    "fecha_estimacion_envio": fecha_estimacion_envio
                })
            )

        # Publicar el estado aceptado con las observaciones (incluso si hay faltantes)
        producer.produce(
            f"/{codigo_tienda}/solicitudes",
            key=str(orden_id),
            value=json.dumps({"estado": estado_orden, "observaciones": observaciones})
        )

    # Asegurar que los mensajes se envíen
    producer.flush()

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
    main()
