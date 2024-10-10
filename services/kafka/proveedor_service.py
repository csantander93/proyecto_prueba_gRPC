from confluent_kafka import Producer, KafkaException
import json
from datetime import datetime

class ProveedorService:
    def __init__(self):
        # Configuración del productor de Kafka
        self.producer = Producer({'bootstrap.servers': 'localhost:9092'})

    def procesar_orden(self, orden_compra):
        """
        Procesa la orden de compra según las reglas de negocio del proveedor.
        """
        try:
            codigo_tienda = orden_compra['codigo_tienda']
            items = orden_compra['items']
            errores = []
            stock_insuficiente = []

            # Simulación de validación de artículos
            for item in items:
                if not self.proveer_articulo(item):
                    errores.append(f"Artículo {item['codigo_articulo']}: no existe")
                elif item['cantidad'] < 1:
                    errores.append(f"Artículo {item['codigo_articulo']}: cantidad mal informada")
                elif not self.stock_suficiente(item):
                    stock_insuficiente.append(item['codigo_articulo'])

            if errores:
                # Orden RECHAZADA, enviar errores a Kafka
                self.enviar_solicitud_rechazada(codigo_tienda, orden_compra, errores)
            elif stock_insuficiente:
                # Orden ACEPTADA con faltante de stock
                self.enviar_aceptada_con_faltante(codigo_tienda, orden_compra, stock_insuficiente)
            else:
                # Orden ACEPTADA, generar orden de despacho
                self.enviar_orden_despacho(codigo_tienda, orden_compra)
        
        except KafkaException as e:
            print(f"Error al enviar mensaje a Kafka: {str(e)}")

    def proveer_articulo(self, item):
        """
        Simula si el proveedor tiene el artículo disponible.
        """
        # Aquí iría la lógica para validar si el proveedor provee el artículo.
        return True

    def stock_suficiente(self, item):
        """
        Simula la verificación del stock disponible para un artículo.
        """
        # Aquí iría la lógica para verificar si hay stock suficiente del artículo.
        return item['cantidad'] <= 10  # Simulación de stock suficiente

    def enviar_solicitud_rechazada(self, codigo_tienda, orden_compra, errores):
        """
        Envía una orden rechazada al topic correspondiente.
        """
        mensaje = {
            'id_orden': orden_compra['id_orden'],
            'estado': 'RECHAZADA',
            'observaciones': errores
        }
        topic = f'/{codigo_tienda}/solicitudes'
        self.producer.produce(topic, json.dumps(mensaje).encode('utf-8'))
        self.producer.flush()
        print(f"Orden RECHAZADA enviada al topic {topic}")

    def enviar_aceptada_con_faltante(self, codigo_tienda, orden_compra, stock_insuficiente):
        """
        Envía una orden aceptada con faltante de stock al topic correspondiente.
        """
        mensaje = {
            'id_orden': orden_compra['id_orden'],
            'estado': 'ACEPTADA',
            'observaciones': f'Faltante de stock para artículos: {", ".join(stock_insuficiente)}'
        }
        topic = f'/{codigo_tienda}/solicitudes'
        self.producer.produce(topic, json.dumps(mensaje).encode('utf-8'))
        self.producer.flush()
        print(f"Orden ACEPTADA con faltante enviada al topic {topic}")

    def enviar_orden_despacho(self, codigo_tienda, orden_compra):
        """
        Genera y envía una orden de despacho asociada a la orden de compra.
        """
        orden_despacho = {
            'id_orden_despacho': 1234,  # Generar un ID único para la orden de despacho
            'id_orden_compra': orden_compra['id_orden'],
            'fecha_estimada_envio': datetime.utcnow().isoformat()
        }
        topic = f'/{codigo_tienda}-despacho'
        self.producer.produce(topic, json.dumps(orden_despacho).encode('utf-8'))
        self.producer.flush()
        print(f"Orden de despacho enviada al topic {topic}")
