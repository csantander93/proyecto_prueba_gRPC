import grpc
from tienda_pb2 import TiendaResponse, TiendasResponse, Tienda  # Importa los mensajes
import tienda_pb2_grpc  # Importa el servicio gRPC
from models import db, Tienda as TiendaModel  # Importa el modelo Tienda y la conexión de base de datos (SQLAlchemy)
from app import app  # La app Flask configurada
import datetime


class TiendaService(tienda_pb2_grpc.TiendaServiceServicer):

    def CrearTienda(self, request, context):
        try:
            with app.app_context():
                # Crear una nueva tienda en la base de datos
                nueva_tienda = TiendaModel(
                    codigo=request.codigo,
                    nombre=request.nombre,
                    direccion=request.direccion,
                    ciudad=request.ciudad,
                    provincia=request.provincia,
                    habilitada=request.habilitada,
                    casa_central=request.casa_central
                )
                db.session.add(nueva_tienda)
                db.session.commit()

                print("Tienda creada con exito")

                return TiendaResponse(tienda=Tienda(
                    codigo=nueva_tienda.codigo,
                    nombre=nueva_tienda.nombre,
                    direccion=nueva_tienda.direccion,
                    ciudad=nueva_tienda.ciudad,
                    provincia=nueva_tienda.provincia,
                    habilitada=nueva_tienda.habilitada,
                    casa_central=nueva_tienda.casa_central
                ))
        except Exception as e:
            print(f"Error al crear tienda: {e}")  # Agrega esta línea para ver el error
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al crear tienda")
            return TiendaResponse()

    def ModificarTienda(self, request, context):
        try:
            with app.app_context():
                # Buscar la tienda por ID
                tienda = TiendaModel.query.get(request.id_tienda)
                if tienda:
                    # Modificar los datos de la tienda
                    tienda.codigo = request.codigo
                    tienda.nombre = request.nombre
                    tienda.direccion = request.direccion
                    tienda.ciudad = request.ciudad
                    tienda.provincia = request.provincia
                    tienda.habilitada = request.habilitada
                    tienda.casa_central = request.casa_central
                    db.session.commit()

                    print("Tienda modificada con exito")

                    return TiendaResponse(tienda=Tienda(
                        codigo=tienda.codigo,
                        nombre=tienda.nombre,
                        direccion=tienda.direccion,
                        ciudad=tienda.ciudad,
                        provincia=tienda.provincia,
                        habilitada=tienda.habilitada,
                        casa_central=tienda.casa_central
                    ))
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Tienda no encontrada")
                    return TiendaResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al modificar tienda")
            return TiendaResponse()

    def BorrarTienda(self, request, context):
        try:
            with app.app_context():
                # Buscar la tienda por ID y eliminarla
                tienda = TiendaModel.query.get(request.id_tienda)

                if tienda:
                    db.session.delete(tienda)
                    db.session.commit()

                    print("Tienda ",tienda.nombre, "eliminada con exito")

                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Tienda no encontrada")
                    return TiendaResponse()
        except Exception as e:
            print(f"Error borrando tienda: {str(e)}")  # Esto te dará más información sobre el error
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al borrar tienda")
            return TiendaResponse()
        
    
    # def CrearOrdenDeCompra(self, request, context):
    #     try:
    #         with app.app_context():
    #             nueva_orden = OrdenCompraModel(
    #                 codigo_tienda=request.codigo_tienda,
    #                 estado='SOLICITADA',
    #                 fecha_solicitud=datetime.now(),
    #                 # Aquí agregas los items, observaciones, etc.
    #             )
    #             db.session.add(nueva_orden)
    #             db.session.commit()

    #             # Preparar el mensaje para Kafka
    #             mensaje = {
    #                 'codigo_tienda': nueva_orden.codigo_tienda,
    #                 'id_orden': nueva_orden.id,
    #                 'items': request.items,  # Los items se mandan como lista
    #                 'fecha_solicitud': nueva_orden.fecha_solicitud.isoformat()
    #             }

    #             # Enviar el mensaje al topic de Kafka
    #             # producer.send('orden-de-compra', mensaje)

    #             print(f"Orden de compra {nueva_orden.id} creada y enviada a Kafka")

    #             # Retornar la respuesta del gRPC
    #             return TiendaResponse(
    #                 tienda=Tienda(
    #                     codigo=nueva_orden.codigo_tienda,
    #                     estado=nueva_orden.estado,
    #                     # Otros campos de la respuesta
    #                 )
    #             )
    #     except Exception as e:
    #         print(f"Error al crear orden de compra: {str(e)}")
    #         context.set_code(grpc.StatusCode.INTERNAL)
    #         context.set_details("Error al crear orden de compra")
    #         return TiendaResponse()
        
    def BuscarTiendaPorNombre(self, request, context):
        try:
            with app.app_context():
                # Buscar la tienda por nombre (búsqueda parcial)
                # Usamos % para buscar cualquier coincidencia que contenga el texto proporcionado
                tienda = TiendaModel.query.filter(TiendaModel.nombre.ilike(f"%{request.nombre}%")).first()
                print("tienda encontrada... ", tienda)
                if tienda:
                    response = TiendaResponse(
                        tienda=Tienda(
                            codigo=tienda.codigo,
                            nombre=tienda.nombre,
                            direccion=tienda.direccion,
                            ciudad=tienda.ciudad,
                            provincia=tienda.provincia,
                            habilitada=tienda.habilitada,
                            casa_central=tienda.casa_central
                        )
                    )
                    return response
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"Tienda con nombre '{request.nombre}' no encontrada")
                    return TiendaResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error al buscar tienda: {str(e)}")
        return TiendaResponse()



    def BuscarTienda(self, request, context):
        try:
            with app.app_context():
                # Buscar la tienda por ID
                tienda = TiendaModel.query.get(request.id_tienda)
                if tienda:
                    return TiendaResponse(tienda=Tienda(
                            codigo=tienda.codigo,
                            nombre=tienda.nombre,
                            direccion=tienda.direccion,
                            ciudad=tienda.ciudad,
                            provincia=tienda.provincia,
                            habilitada=tienda.habilitada,
                            casa_central=tienda.casa_central
                    ))
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Tienda no encontrada")
                    return TiendaResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al buscar tienda")
            return TiendaResponse()

    def EnlistarTiendas(self, request, context):
        try:
            with app.app_context():
                # Listar todas las tiendas
                tiendas = TiendaModel.query.all()
                response = TiendasResponse()
                for tienda in tiendas:
                    response.tiendas.add(
                        codigo=tienda.codigo,
                        nombre=tienda.nombre,
                        direccion=tienda.direccion,
                        ciudad=tienda.ciudad,
                        provincia=tienda.provincia,
                        habilitada=tienda.habilitada,
                        casa_central=tienda.casa_central
                    )
                return response
        except Exception as e:
            print(f"Error: {e}")  # Log the error for debugging purposes
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error al enlistar tiendas: {str(e)}")  # Include the error details
            return TiendasResponse()

    # def validar_orden(orden):
    #     """Validar si la orden de compra puede ser aceptada o debe ser rechazada."""
    #     for item in orden['items']:
    #         # Simulación: Verificar si el stock del artículo es suficiente
    #         if not verificar_stock(item['codigo'], item['cantidad']):
    #             return False, f"Artículo {item['codigo']} no disponible o stock insuficiente"
    #     return True, "Orden aceptada"

    # def verificar_stock(codigo_articulo, cantidad_solicitada):
    #     """Simular la verificación de stock en el sistema del proveedor."""
    #     # Supongamos que el stock es insuficiente si la cantidad solicitada es mayor a 10
    #     stock_disponible = 10
    #     return cantidad_solicitada <= stock_disponible
