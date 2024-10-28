import grpc
<<<<<<< HEAD
import json
from datetime import datetime
from confluent_kafka import Producer
from app import app  # La aplicación Flask configurada
from models import db, OrdenCompraModel, ItemModel
import generated.order_pb2
import generated.order_pb2_grpc


class OrderService(generated.order_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        # Configuración de Kafka
        self.producer = Producer({'bootstrap.servers': 'localhost:9092'})

    def CreateOrder(self, request, context):
        try:
            with app.app_context():
                # Crear una nueva orden de compra
                fecha_actual = datetime.utcnow()
                nueva_orden = OrdenCompraModel(
                    codigo_tienda=request.codigo_tienda,
                    estado='SOLICITADA',  # Establecer el estado inicial como SOLICITADA
                    observaciones=request.observaciones,
                    orden_despacho=request.orden_despacho,
                    fecha_solicitud=fecha_actual,  # Establecer la fecha de solicitud actual
                    fecha_recepcion=None
                )

                # Guardar la orden en la base de datos
                db.session.add(nueva_orden)
                db.session.commit()

                # Guardar los ítems de la orden
                for item in request.items:
                    nuevo_item = ItemModel(
                        orden_compra_id=nueva_orden.id,
                        codigo_articulo=item.codigo_articulo,
                        color=item.color,
                        talle=item.talle,
                        cantidad=item.cantidad
                    )
                    db.session.add(nuevo_item)

                db.session.commit()

                # Preparar el mensaje para Kafka
                mensaje = {
                    'codigo_tienda': nueva_orden.codigo_tienda,
                    'id_orden': nueva_orden.id,
                    'items': [
                        {
                            'codigo_articulo': item.codigo_articulo,
                            'color': item.color,
                            'talle': item.talle,
                            'cantidad': item.cantidad
                        } for item in nueva_orden.items
                    ],
                    'fecha_solicitud': nueva_orden.fecha_solicitud.isoformat()
                }

                # Enviar mensaje al topic "orden-de-compra"
                self.producer.produce('orden-de-compra', json.dumps(mensaje).encode('utf-8'))
                self.producer.flush()  # Asegurarse de que el mensaje se envíe

                return generated.order_pb2.CreateOrderResponse(id=nueva_orden.id)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error al crear la orden: {str(e)}')
            return generated.order_pb2.CreateOrderResponse()

    def GetOrder(self, request, context):
        try:
            with app.app_context():
                # Obtener la orden de compra por ID
                orden = OrdenCompraModel.query.get(request.id)

                if orden is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('Orden de compra no encontrada')
                    return generated.order_pb2.GetOrderResponse()

                # Convertir la orden a un mensaje de respuesta
                response = generated.order_pb2.GetOrderResponse(
                    order=generated.order_pb2.Order(
                        id=orden.id,
                        codigo_tienda=orden.codigo_tienda,
                        estado=orden.estado,
                        fecha_solicitud=orden.fecha_solicitud.isoformat(),
                        fecha_recepcion=orden.fecha_recepcion.isoformat() if orden.fecha_recepcion else '',
                        observaciones=orden.observaciones,
                        orden_despacho=orden.orden_despacho
                    )
                )

                # Agregar los ítems a la respuesta
                for item in orden.items:
                    response.order.items.add(
                        codigo_articulo=item.codigo_articulo,
                        color=item.color,
                        talle=item.talle,
                        cantidad=item.cantidad
                    )

                return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error al obtener la orden: {str(e)}')
            return generated.order_pb2.GetOrderResponse()

    def UpdateOrder(self, request, context):
        try:
            with app.app_context():
                # Obtener la orden de compra existente
                orden = OrdenCompraModel.query.get(request.id)

                if orden is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('Orden de compra no encontrada')
                    return generated.order_pb2.Order()

                # Actualizar los campos
                orden.codigo_tienda = request.codigo_tienda
                orden.estado = request.estado
                orden.observaciones = request.observaciones
                orden.orden_despacho = request.orden_despacho
                orden.fecha_recepcion = datetime.fromisoformat(request.fecha_recepcion) if request.fecha_recepcion else None

                db.session.commit()

                return generated.order_pb2.Order(id=orden.id)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error al actualizar la orden: {str(e)}')
            return generated.order_pb2.Order()

    def DeleteOrder(self, request, context):
        try:
            with app.app_context():
                # Eliminar la orden de compra por ID
                orden = OrdenCompraModel.query.get(request.id)

                if orden is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('Orden de compra no encontrada')
                    return generated.order_pb2.Order()

                db.session.delete(orden)
                db.session.commit()

                return generated.order_pb2.Order()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error al eliminar la orden: {str(e)}')
            return generated.order_pb2.Order()


=======
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
>>>>>>> master
