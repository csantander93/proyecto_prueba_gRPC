import grpc
from producto_pb2 import ProductoResponse, ProductosResponse, Producto
import producto_pb2_grpc
from models import db, Producto as ProductoModel  # Modelo de Producto y base de datos
from app import app  # La aplicación Flask configurada

class ProductoService(producto_pb2_grpc.ProductoServiceServicer):

    def CrearProducto(self, request, context):
        try:
            with app.app_context():
                # Crear un nuevo producto en la base de datos
                nuevo_producto = ProductoModel(
                    codigo=request.codigo,
                    talle=request.talle,
                    foto=request.foto,
                    color=request.color,
                    stock=request.stock
                )
                db.session.add(nuevo_producto)
                db.session.commit()

                return ProductoResponse(producto=Producto(
                    id_producto=nuevo_producto.id,
                    codigo=nuevo_producto.codigo,
                    talle=nuevo_producto.talle,
                    foto=nuevo_producto.foto,
                    color=nuevo_producto.color,
                    stock=nuevo_producto.stock
                ))
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al crear producto")
            return ProductoResponse()

    def ModificarProducto(self, request, context):
        try:
            with app.app_context():
                # Buscar el producto por nombre
                producto = ProductoModel.query.get(request.nombre)
                if producto:
                    # Modificar los datos del producto
                    producto.codigo = request.codigo
                    producto.talle = request.talle
                    producto.foto = request.foto
                    producto.color = request.color
                    producto.stock = request.stock
                    db.session.commit()

                    return ProductoResponse(producto=Producto(
                        id_producto=producto.id,
                        codigo=producto.codigo,
                        talle=producto.talle,
                        foto=producto.foto,
                        color=producto.color,
                        stock=producto.stock
                    ))
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Producto no encontrado")
                    return ProductoResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al modificar producto")
            return ProductoResponse()

    def BorrarProducto(self, request, context):
        try:
            with app.app_context():
                # Buscar el producto por ID y eliminarlo
                producto = ProductoModel.query.get(request.id_producto)
                if producto:
                    db.session.delete(producto)
                    db.session.commit()

                    return ProductoResponse(producto=Producto(
                        id_producto=producto.id,
                        codigo=producto.codigo,
                        talle=producto.talle,
                        foto=producto.foto,
                        color=producto.color,
                        stock=producto.stock
                    ))
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Producto no encontrado")
                    return ProductoResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al borrar producto")
            return ProductoResponse()

    def BuscarProducto(self, request, context):
        try:
            with app.app_context():
                # Buscar el producto por ID
                producto = ProductoModel.query.get(request.id_producto)
                if producto:
                    return ProductoResponse(producto=Producto(
                        id_producto=producto.id,
                        codigo=producto.codigo,
                        talle=producto.talle,
                        foto=producto.foto,
                        color=producto.color,
                        stock=producto.stock
                    ))
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Producto no encontrado")
                    return ProductoResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al buscar producto")
            return ProductoResponse()

    def EnlistarProductos(self, request, context):
        try:
            with app.app_context():
                # Listar todos los productos
                productos = ProductoModel.query.all()
                response = ProductosResponse()
                for producto in productos:
                    response.productos.add(
                        id_producto=producto.id,
                        codigo=producto.codigo,
                        talle=producto.talle,
                        foto=producto.foto,
                        color=producto.color,
                        stock=producto.stock
                    )
                return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al enlistar productos")
            return ProductosResponse()
