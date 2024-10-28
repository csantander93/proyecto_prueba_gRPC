import grpc
from concurrent import futures
from datetime import datetime
import json
from confluent_kafka import Producer

from models import db, OrdenDeCompra, Item, EstadoOrden

import generated.orden_compra_pb2
import generated.orden_compra_pb2_grpc  # Importa el modelo Tienda y la conexión de base de datos (SQLAlchemy)
from app import app  # La app Flask configurada


def enviar_a_kafka(topic, mensaje):
    # Configuración del productor de Kafka
    producer = Producer({
        'bootstrap.servers': 'localhost:9092'  # Cambia esto si tu servidor Kafka está en otra dirección
    })
    
    # Envío del mensaje al tópico especificado
    producer.produce(topic, json.dumps(mensaje).encode('utf-8'))
    producer.flush()  # Asegúrate de que el mensaje se envía inmediatamente


# class OrdenCompraService(generated.orden_compra_pb2_grpc.OrdenCompraServiceServicer):
    # def CrearOrdenDeCompra(self, request, context):
    #     try:
    #         with app.app_context():
    #             orden = request.orden

    #             # Establecer fecha de solicitud y estado
    #             orden.fecha_solicitud = datetime.now().isoformat()
    #             orden.estado = EstadoOrden.SOLICITADA.value

    #             # Guardar en la base de datos
    #             nueva_orden = OrdenDeCompra(
    #                 codigo_tienda=orden.codigo_tienda,
    #                 estado=orden.estado,
    #                 observaciones=orden.observaciones,
    #                 fecha_solicitud=datetime.now()
    #             )
    #             db.session.add(nueva_orden)
    #             db.session.commit()

    #             # Añadir items a la orden
    #             for item in orden.items:
    #                 nuevo_item = Item(
    #                     orden_id=nueva_orden.id,
    #                     codigo_articulo=item.codigo_articulo,
    #                     color=item.color,
    #                     talle=item.talle,
    #                     cantidad_solicitada=item.cantidad_solicitada
    #                 )
    #                 db.session.add(nuevo_item)
    #             db.session.commit()

    #             # Enviar mensaje a Kafka
    #             mensaje = {
    #                 "codigo_tienda": orden.codigo_tienda,
    #                 "id_orden": nueva_orden.id,
    #                 "items": [
    #                     {
    #                         "codigo_articulo": item.codigo_articulo,
    #                         "color": item.color,
    #                         "talle": item.talle,
    #                         "cantidad_solicitada": item.cantidad_solicitada
    #                     } for item in orden.items
    #                 ],
    #                 "fecha_solicitud": orden.fecha_solicitud
    #             }
    #             enviar_a_kafka("orden-de-compra", mensaje)

    #             return generated.orden_compra_pb2.CrearOrdenResponse(exito=True, mensaje="Orden creada exitosamente")
        
    #     except Exception as e:
    #         context.set_details(str(e))
    #         context.set_code(grpc.StatusCode.INTERNAL)
    #         return generated.orden_compra_pb2.CrearOrdenResponse(exito=False, mensaje="Error al crear la orden")

class OrdenCompraService(generated.orden_compra_pb2_grpc.OrdenCompraServiceServicer):

    def CrearOrdenDeCompra(self, request, context):
        try:
            with app.app_context():
                orden = request.orden

                # Establecer fecha de solicitud y estado
                orden.fecha_solicitud = datetime.now().isoformat()
                orden.estado = EstadoOrden.SOLICITADA.value

                # Guardar en la base de datos
                nueva_orden = OrdenDeCompra(
                    codigo_tienda=orden.codigo_tienda,
                    estado=orden.estado,
                    observaciones=orden.observaciones,
                    fecha_solicitud=datetime.now()
                )
                db.session.add(nueva_orden)
                db.session.commit()

                # Añadir items a la orden
                for item in orden.items:
                    nuevo_item = Item(
                        orden_id=nueva_orden.id,
                        codigo_articulo=item.codigo_articulo,
                        color=item.color,
                        talle=item.talle,
                        cantidad_solicitada=item.cantidad_solicitada
                    )
                    db.session.add(nuevo_item)
                db.session.commit()

                # Enviar mensaje a Kafka
                mensaje = {
                    "codigo_tienda": orden.codigo_tienda,
                    "id_orden": nueva_orden.id,
                    "observaciones": orden.observaciones,
                    "items": [
                        {
                            "codigo_articulo": item.codigo_articulo,
                            "color": item.color,
                            "talle": item.talle,
                            "cantidad_solicitada": item.cantidad_solicitada
                        } for item in orden.items
                    ],
                    "fecha_solicitud": orden.fecha_solicitud
                }
                enviar_a_kafka("orden-de-compra", mensaje)

                return generated.orden_compra_pb2.CrearOrdenResponse(exito=True, mensaje="Orden creada exitosamente")
        
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return generated.orden_compra_pb2.CrearOrdenResponse(exito=False, mensaje="Error al crear la orden")

    # Método para obtener una orden por ID
    def ObtenerOrdenDeCompra(self, request, context):
        try:
            with app.app_context():
                orden = OrdenDeCompra.query.get(request.id_orden)
                if orden is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Orden no encontrada")
                    return generated.orden_compra_pb2.ObtenerOrdenResponse()
                
                orden_data = generated.orden_compra_pb2.Orden(
                    id_orden=orden.id,
                    codigo_tienda=orden.codigo_tienda,
                    estado=orden.estado,
                    observaciones=orden.observaciones,
                    fecha_solicitud=orden.fecha_solicitud.isoformat(),
                    items=[generated.orden_compra_pb2.Item(
                        codigo_articulo=item.codigo_articulo,
                        color=item.color,
                        talle=item.talle,
                        cantidad_solicitada=item.cantidad_solicitada
                    ) for item in orden.items]
                )
                return generated.orden_compra_pb2.ObtenerOrdenResponse(orden=orden_data)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return generated.orden_compra_pb2.ObtenerOrdenResponse()

    # Método para modificar una orden
    def ModificarOrdenDeCompra(self, request, context):
        try:
            with app.app_context():
                orden = OrdenDeCompra.query.get(request.id_orden)
                if orden is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Orden no encontrada")
                    return generated.orden_compra_pb2.ModificarOrdenResponse(exito=False, mensaje="Orden no encontrada")
                
                orden.estado = request.estado
                orden.observaciones = request.observaciones
                db.session.commit()
                
                return generated.orden_compra_pb2.ModificarOrdenResponse(exito=True, mensaje="Orden modificada exitosamente")
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return generated.orden_compra_pb2.ModificarOrdenResponse(exito=False, mensaje="Error al modificar la orden")

    # Método para eliminar una orden por ID
    def BorrarOrdenDeCompra(self, request, context):
        try:
            with app.app_context():
                orden = OrdenDeCompra.query.get(request.id_orden)
                if orden is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Orden no encontrada")
                    return generated.orden_compra_pb2.BorrarOrdenResponse(exito=False, mensaje="Orden no encontrada")
                
                db.session.delete(orden)
                db.session.commit()
                
                return generated.orden_compra_pb2.BorrarOrdenResponse(exito=True, mensaje="Orden eliminada exitosamente")
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return generated.orden_compra_pb2.BorrarOrdenResponse(exito=False, mensaje="Error al eliminar la orden")