from confluent_kafka import Consumer, KafkaException, KafkaError

def consumir_mensajes():
    conf = {
        'bootstrap.servers': 'localhost:9092',  # Dirección del broker de Kafka
        'group.id': 'mi-grupo',  # Identificador del grupo de consumidores
        'auto.offset.reset': 'earliest'  # Para leer mensajes desde el principio si no hay offset
    }

    # Crear el consumidor
    consumer = Consumer(conf)

    # Suscribirse al topic de Kafka
    consumer.subscribe(['/orden-de-compra'])

    print("Esperando mensajes del topic '/orden-de-compra'...")

    try:
        # Bucle infinito para consumir mensajes
        while True:
            # Esperar un mensaje (1 segundo de timeout)
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue  # No hay mensaje, continuar esperando
            if msg.error():
                # Si hay un error en el mensaje, manejarlo
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue  # Se alcanzó el final de la partición, no es un error grave
                else:
                    raise KafkaException(msg.error())  # Error grave
            # Mostrar el mensaje recibido
            print(f'Mensaje recibido: {msg.value().decode("utf-8")}')
    except KeyboardInterrupt:
        # Manejar la interrupción con Ctrl+C
        print("Consumidor interrumpido, cerrando...")
    finally:
        # Cerrar el consumidor de Kafka
        consumer.close()

if __name__ == '__main__':
    consumir_mensajes()
