import grpc
from models import db, Usuario as UsuarioModel, Tienda as TiendaModel
import stock_pb2
import stock_pb2_grpc
from app import app
import logging

class UsuarioService(stock_pb2_grpc.UsuarioServiceServicer):

    def GetUsuario(self, request, context):
        logging.debug("Received GetUsuario request: %s", request)
        try:
            with app.app_context():
                usuario = UsuarioModel.query.get(request.id_usuario)  # Changed from request.id to request.id_usuario
                if usuario:
                    return stock_pb2.Usuario(
                        id_usuario=usuario.id,
                        username=usuario.username,
                        password=usuario.password,
                        habilitado=usuario.habilitado,
                        tienda_idtienda=usuario.tienda_id
                    )
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Usuario no encontrado")
                    return stock_pb2.Usuario()
        except Exception as e:
            logging.error("Error al obtener usuario: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.Usuario()

    def CreateUsuario(self, request, context):
        logging.debug("Received CreateUsuario request: %s", request)
        try:
            with app.app_context():
                tienda = TiendaModel.query.get(request.tienda_idtienda)
                if not tienda:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Tienda no encontrada")
                    return stock_pb2.Usuario()

                nuevo_usuario = UsuarioModel(
                    username=request.username,
                    password=request.password,
                    habilitado=True,  # Asumimos que un nuevo usuario está habilitado por defecto
                    tienda_id=request.tienda_idtienda
                )
                db.session.add(nuevo_usuario)
                db.session.commit()

                return stock_pb2.Usuario(
                    id_usuario=nuevo_usuario.id,
                    username=nuevo_usuario.username,
                    password=nuevo_usuario.password,
                    habilitado=nuevo_usuario.habilitado,
                    tienda_idtienda=nuevo_usuario.tienda_id
                )
        except Exception as e:
            logging.error("Error al crear usuario: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.Usuario()

    def ListUsuarios(self, request, context):
        logging.debug("Received ListUsuarios request")
        try:
            with app.app_context():
                usuarios = UsuarioModel.query.all()
                usuarios_list = stock_pb2.UsuariosList()
                for usuario in usuarios:
                    usuarios_list.usuarios.add(
                        id_usuario=usuario.id,
                        username=usuario.username,
                        password=usuario.password,
                        habilitado=usuario.habilitado,
                        tienda_idtienda=usuario.tienda_id
                    )
                return usuarios_list
        except Exception as e:
            logging.error("Error al listar usuarios: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.UsuariosList()
