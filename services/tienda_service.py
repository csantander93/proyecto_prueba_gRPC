import grpc
from models import db, Tienda as TiendaModel, Usuario as UsuarioModel
import stock_pb2
import stock_pb2_grpc
from app import app
import logging

class TiendaService(stock_pb2_grpc.TiendaServiceServicer):

    def GetTienda(self, request, context):
        logging.debug("Received GetTienda request: %s", request)
        try:
            with app.app_context():
                tienda = TiendaModel.query.get(request.id_tienda)
                if tienda:
                    return stock_pb2.Tienda(
                        id_tienda=tienda.id,
                        codigo=tienda.codigo,
                        nombre=tienda.nombre,
                        direccion=tienda.direccion,
                        ciudad=tienda.ciudad,
                        provincia=tienda.provincia,
                        habilitada=tienda.habilitada,
                        casa_central=tienda.casa_central,
                        cadena_id_cadena=tienda.cadena_id
                    )
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Tienda no encontrada")
                    return stock_pb2.Tienda()
        except Exception as e:
            logging.error("Error al obtener tienda: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.Tienda()

    def CreateTienda(self, request, context):
        logging.debug("Received CreateTienda request: %s", request)
        try:
            with app.app_context():
                nueva_tienda = TiendaModel(
                    codigo=request.codigo,
                    nombre=request.nombre,
                    direccion=request.direccion,
                    ciudad=request.ciudad,
                    provincia=request.provincia,
                    habilitada=request.habilitada,
                    casa_central=request.casa_central,
                    cadena_id=request.cadena_id_cadena
                )
                db.session.add(nueva_tienda)
                db.session.commit()
                logging.info("Tienda creada exitosamente: %s", request.codigo)
                return stock_pb2.Tienda(
                    id_tienda=nueva_tienda.id,
                    codigo=nueva_tienda.codigo,
                    nombre=nueva_tienda.nombre,
                    direccion=nueva_tienda.direccion,
                    ciudad=nueva_tienda.ciudad,
                    provincia=nueva_tienda.provincia,
                    habilitada=nueva_tienda.habilitada,
                    casa_central=nueva_tienda.casa_central,
                    cadena_id_cadena=nueva_tienda.cadena_id
                )
        except Exception as e:
            logging.error("Error al crear tienda: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.Tienda()

    def CrearTiendaHabilitado(self, request, context):
        logging.debug("Received CrearTiendaHabilitado request: %s", request)

        # Verificar si el usuario está habilitado
        usuario = self.verificar_usuario_habilitado(request.usuario_id, context)
        if not usuario:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("El usuario no está habilitado para crear tiendas")
            return stock_pb2.Tienda()

        try:
            with app.app_context():
                nueva_tienda = TiendaModel(
                    codigo=request.codigo,
                    nombre=request.nombre,
                    direccion=request.direccion,
                    ciudad=request.ciudad,
                    provincia=request.provincia,
                    habilitada=request.habilitada,
                    casa_central=request.casa_central,
                    cadena_id=request.cadena_id_cadena
                )
                db.session.add(nueva_tienda)
                db.session.commit()
                logging.info("Tienda creada exitosamente: %s", request.codigo)
                return stock_pb2.Tienda(
                    id_tienda=nueva_tienda.id,
                    codigo=nueva_tienda.codigo,
                    nombre=nueva_tienda.nombre,
                    direccion=nueva_tienda.direccion,
                    ciudad=nueva_tienda.ciudad,
                    provincia=nueva_tienda.provincia,
                    habilitada=nueva_tienda.habilitada,
                    casa_central=nueva_tienda.casa_central,
                    cadena_id_cadena=nueva_tienda.cadena_id
                )
        except Exception as e:
            logging.error("Error al crear tienda: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.Tienda()

    def verificar_usuario_habilitado(self, usuario_id, context):
        """Verifica si el usuario está habilitado."""
        with app.app_context():
            usuario = UsuarioModel.query.get(usuario_id)
            if usuario and usuario.habilitado:
                return usuario
            else:
                logging.warning("Usuario no habilitado o no encontrado: %s", usuario_id)
                return None

    def ListTiendas(self, request, context):
        logging.debug("Received ListTiendas request")
        try:
            with app.app_context():
                tiendas = TiendaModel.query.all()
                tiendas_list = stock_pb2.TiendasList()
                for tienda in tiendas:
                    tiendas_list.tiendas.add(
                        id_tienda=tienda.id,
                        codigo=tienda.codigo,
                        nombre=tienda.nombre,
                        direccion=tienda.direccion,
                        ciudad=tienda.ciudad,
                        provincia=tienda.provincia,
                        habilitada=tienda.habilitada,
                        casa_central=tienda.casa_central,
                        cadena_id_cadena=tienda.cadena_id
                    )
                return tiendas_list
        except Exception as e:
            logging.error("Error al listar tiendas: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.TiendasList()

    def AlternarHabilitadaTienda(self, request, context):
        logging.debug("Received AlternarHabilitadaTienda request: %s", request)
        try:
            with app.app_context():
                tienda = TiendaModel.query.filter_by(codigo=request.codigo).first()
                if tienda:
                    tienda.habilitada = not tienda.habilitada
                    db.session.commit()
                    estado = "habilitada" if tienda.habilitada else "deshabilitada"
                    logging.info("Tienda %s cambiada a: %s", request.codigo, estado)
                    return stock_pb2.Tienda(
                        id_tienda=tienda.id,
                        codigo=tienda.codigo,
                        nombre=tienda.nombre,
                        direccion=tienda.direccion,
                        ciudad=tienda.ciudad,
                        provincia=tienda.provincia,
                        habilitada=tienda.habilitada,
                        casa_central=tienda.casa_central,
                        cadena_id_cadena=tienda.cadena_id
                    )
                
                logging.warning("Tienda no encontrada: %s", request.codigo)
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Tienda no encontrada")
                return stock_pb2.Tienda()
        except Exception as e:
            logging.error("Error al alternar habilitada de tienda: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.Tienda()
