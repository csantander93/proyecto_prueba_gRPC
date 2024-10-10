import grpc
from generated.producto_pb2 import ProductoResponse, ProductosResponse, Producto
import generated.producto_pb2_grpc
from models import db, Producto as ProductoModel  # Modelo de Producto y base de datos
from app import app  # La aplicación Flask configurada

class ProductoService(producto_pb2_grpc.ProductoServiceServicer):

    def CrearProducto(self, request, context):
        try:
            with app.app_context():
                # Crear un nuevo producto en la base de datos
                nuevo_producto = ProductoModel(
                    codigo=request.codigo,
                    nombre=request.nombre,  # Agregado: nombre del producto
                    talle=request.talle,
                    foto=request.foto,
                    color=request.color,
                    stock=request.stock,
                    id_tienda=request.id_tienda  # Agregado: ID de la tienda
                )
                db.session.add(nuevo_producto)
                db.session.commit()

                return ProductoResponse(producto=Producto(
                    id_producto=nuevo_producto.id_producto,
                    codigo=nuevo_producto.codigo,
                    nombre=nuevo_producto.nombre,  # Agregado: nombre del producto
                    talle=nuevo_producto.talle,
                    foto=nuevo_producto.foto,
                    color=nuevo_producto.color,
                    stock=nuevo_producto.stock,
                    id_tienda=nuevo_producto.id_tienda  # Agregado: ID de la tienda
                ))
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al crear producto")
            return ProductoResponse()

    def ModificarProducto(self, request, context):
        try:
            with app.app_context():
                # Buscar el producto por ID
                producto = ProductoModel.query.get(request.id_producto)
                if producto:
                    # Modificar los datos del producto
                    producto.codigo = request.codigo
                    producto.nombre = request.nombre  # Agregado: nombre del producto
                    producto.talle = request.talle
                    producto.foto = request.foto
                    producto.color = request.color
                    producto.stock = request.stock
                    producto.id_tienda = request.id_tienda  # Agregado: ID de la tienda
                    db.session.commit()

                    return ProductoResponse(producto=Producto(
                        id_producto=producto.id_producto,
                        codigo=producto.codigo,
                        nombre=producto.nombre,  # Agregado: nombre del producto
                        talle=producto.talle,
                        foto=producto.foto,
                        color=producto.color,
                        stock=producto.stock,
                        id_tienda=producto.id_tienda  # Agregado: ID de la tienda
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
                        id_producto=producto.id_producto,
                        codigo=producto.codigo,
                        nombre=producto.nombre,  # Agregado: nombre del producto
                        talle=producto.talle,
                        foto=producto.foto,
                        color=producto.color,
                        stock=producto.stock,
                        id_tienda=producto.id_tienda  # Agregado: ID de la tienda
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
                        id_producto=producto.id_producto,
                        codigo=producto.codigo,
                        nombre=producto.nombre,  # Agregado: nombre del producto
                        talle=producto.talle,
                        foto=producto.foto,
                        color=producto.color,
                        stock=producto.stock,
                        id_tienda=producto.id_tienda  # Agregado: ID de la tienda
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
                        id_producto=producto.id_producto,
                        codigo=producto.codigo,
                        nombre=producto.nombre,  # Agregado: nombre del producto
                        talle=producto.talle,
                        foto=producto.foto,
                        color=producto.color,
                        stock=producto.stock,
                        id_tienda=producto.id_tienda  # Agregado: ID de la tienda
                    )
                return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error al enlistar productos")
            return ProductosResponse()
