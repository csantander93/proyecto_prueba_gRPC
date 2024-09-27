import grpc
from models import db, Usuario, Tienda
import stock_pb2
from app import app
import logging

class UsuarioService(stock_pb2.StockearteServiceServicer):

    def CrearUsuario(self, request, context):
        logging.debug("Received CrearUsuario request: %s", request)
        try:
            with app.app_context():
                tienda = Tienda.query.filter_by(codigo=request.tienda).first()
                if not tienda:
                    context.set_details("Tienda no encontrada")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return stock_pb2.UsuarioResponse(mensaje="Tienda no encontrada")

                # Verificar si la tienda es 'casa_central'
                habilitado = tienda.codigo == 'casa_central'

                nuevo_usuario = Usuario(
                    nombre_usuario=request.nombre_usuario,
                    contrasena=request.contrasena,
                    nombre=request.nombre,
                    apellido=request.apellido,
                    tienda=tienda,
                    habilitado=habilitado  # Establecer el valor de habilitado
                )
                db.session.add(nuevo_usuario)
                db.session.commit()
                logging.info("Usuario creado exitosamente: %s", request.nombre_usuario)
                return stock_pb2.UsuarioResponse(mensaje="Usuario creado exitosamente")
        except Exception as e:
            logging.error("Error al crear usuario: %s", str(e), exc_info=True)
            context.set_details("Error interno del servidor")
            context.set_code(grpc.StatusCode.INTERNAL)
            return stock_pb2.UsuarioResponse(mensaje="Error interno del servidor")

    def AutenticarUsuario(self, request, context):
        logging.debug("Received AutenticarUsuario request: %s", request)
        try:
            with app.app_context():
                usuario = Usuario.query.filter_by(nombre_usuario=request.nombre_usuario, contrasena=request.contrasena).first()
                if usuario:
                    logging.info("Autenticación exitosa para usuario: %s", request.nombre_usuario)
                    return stock_pb2.LoginResponse(mensaje="Autenticación exitosa")
                
                logging.warning("Autenticación fallida para usuario: %s", request.nombre_usuario)
                return stock_pb2.LoginResponse(mensaje="Autenticación fallida")
        except Exception as e:
            logging.error("Error al autenticar usuario: %s", str(e), exc_info=True)
            context.set_details("Error interno del servidor")
            context.set_code(grpc.StatusCode.INTERNAL)
            return stock_pb2.LoginResponse(mensaje="Error interno del servidor")
