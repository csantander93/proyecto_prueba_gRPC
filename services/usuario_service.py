import grpc
from generated.usuario_pb2 import UsuarioResponse, UsuariosResponse, Usuario, AutenticarUsuarioResponse
import generated.usuario_pb2_grpc
from models import db, Usuario as UsuarioModel  # Importa el modelo Usuario y la base de datos
from app import app  # La app Flask configurada
from werkzeug.security import generate_password_hash, check_password_hash  # Para el manejo de contraseñas

class UsuarioService(usuario_pb2_grpc.UsuarioServiceServicer):

    def CrearUsuario(self, request, context):
        try:
            with app.app_context():
                # Verificar si ya existe un usuario con el mismo username
                usuario_existente = UsuarioModel.query.filter_by(username=request.username).first()
                if usuario_existente:
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    context.set_details(f"El usuario con el username '{request.username}' ya existe.")
                    return UsuarioResponse()

                # Si no existe, proceder a crear el nuevo usuario
                nuevo_usuario = UsuarioModel(
                    username=request.username,
                    password=generate_password_hash(request.password),
                    habilitado=request.habilitado,
                    tienda_idtienda=request.tienda_idtienda
                )
                db.session.add(nuevo_usuario)
                db.session.commit()

                return UsuarioResponse(usuario=Usuario(
                    username=nuevo_usuario.username,
                    habilitado=nuevo_usuario.habilitado,
                    tienda_idtienda=nuevo_usuario.tienda_idtienda
                ))

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al crear usuario: " + str(e))
            print(f"Error en CrearUsuario: {e}")
            return UsuarioResponse()

    def ModificarUsuario(self, request, context):
        try:
            with app.app_context():
                usuario = UsuarioModel.query.get(request.id_usuario)
                if usuario:
                    usuario.username = request.username
                    if request.password:
                        usuario.password = generate_password_hash(request.password)
                    usuario.habilitado = request.habilitado
                    usuario.tienda_idtienda = request.tienda_idtienda
                    db.session.commit()

                    return UsuarioResponse(usuario=Usuario(
                        username=usuario.username,
                        habilitado=usuario.habilitado,
                        tienda_idtienda=usuario.tienda_idtienda
                    ))
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Usuario no encontrado")
                    return UsuarioResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al modificar usuario")
            return UsuarioResponse()

    def BorrarUsuario(self, request, context):
        try:
            with app.app_context():
                usuario = UsuarioModel.query.get(request.id_usuario)
                if usuario:
                    db.session.delete(usuario)
                    db.session.commit()
                    return UsuarioResponse(usuario=Usuario(
                        username=usuario.username,
                        habilitado=usuario.habilitado,
                        tienda_idtienda=usuario.tienda_idtienda
                    ))
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Usuario no encontrado")
                    return UsuarioResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al borrar usuario")
            return UsuarioResponse()

    def BuscarUsuario(self, request, context):
        try:
            with app.app_context():
                print(f"Buscando usuario con username: {request.username}")  # Esto imprimirá el username recibido
                usuario = UsuarioModel.query.filter_by(username=request.username).first()
                if usuario:
                    return UsuarioResponse(usuario=Usuario(
                        id_usuario=usuario.id_usuario,
                        username=usuario.username,
                        password="",  # No devolver la contraseña por motivos de seguridad
                        habilitado=usuario.habilitado,
                        tienda_idtienda=usuario.tienda_idtienda
                    ))
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Usuario no encontrado")
                    return UsuarioResponse()
        except Exception as e:
            print(f"Error en BuscarUsuario: {e}")  # Depuración
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al buscar usuario")
            return UsuarioResponse()

    def EnlistarUsuarios(self, request, context):
        try:
            with app.app_context():
                usuarios = UsuarioModel.query.all()
                print(f'Enlistando usuarios: {usuarios}')  # Agrega esta línea para verificar la lista
                response = UsuariosResponse()
                for usuario in usuarios:
                    response.usuarios.add(
                        id_usuario=usuario.id_usuario,
                        username=usuario.username,
                        habilitado=usuario.habilitado,
                        tienda_idtienda=usuario.tienda_idtienda
                    )
                return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al enlistar usuarios")
        return UsuariosResponse()

    def AutenticarUsuario(self, request, context):
        try:
            with app.app_context():
                usuario = UsuarioModel.query.filter_by(username=request.username).first()

                if not usuario:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"Usuario '{request.username}' no encontrado.")
                    return AutenticarUsuarioResponse(autenticado=False, mensaje="Usuario no encontrado")

                if not check_password_hash(usuario.password, request.password):
                    context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                    context.set_details("Contraseña incorrecta.")
                    return AutenticarUsuarioResponse(autenticado=False, mensaje="Usuario o contraseña incorrectos")

                return AutenticarUsuarioResponse(autenticado=True, mensaje="Autenticación exitosa")

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error al autenticar usuario: {str(e)}")
            return AutenticarUsuarioResponse(autenticado=False, mensaje="Error interno")
