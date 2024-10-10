import grpc
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
            return order_pb2.Order()


