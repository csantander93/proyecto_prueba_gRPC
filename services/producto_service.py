import grpc
from models import db, Producto as ProductoModel
import stock_pb2
import stock_pb2_grpc
from app import app
import logging

class ProductoService(stock_pb2_grpc.ProductoServiceServicer):

    def GetProducto(self, request, context):
        logging.debug("Received GetProducto request: %s", request)
        try:
            with app.app_context():
                producto = ProductoModel.query.get(request.id_producto)  # Changed to match proto
                if producto:
                    return stock_pb2.Producto(
                        id_producto=producto.id,
                        codigo=producto.codigo,
                        talle=producto.talle,
                        foto=producto.foto,
                        color=producto.color,
                        stock=producto.stock
                    )
                else:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Producto no encontrado")
                    return stock_pb2.Producto()
        except Exception as e:
            logging.error("Error al obtener producto: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.Producto()

    def CreateProducto(self, request, context):
        logging.debug("Received CreateProducto request: %s", request)
        try:
            with app.app_context():
                producto_existente = ProductoModel.query.filter_by(codigo=request.codigo).first()
                if producto_existente:
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    context.set_details("Producto con ese código ya existe")
                    return stock_pb2.Producto()

                nuevo_producto = ProductoModel(
                    codigo=request.codigo,
                    talle=request.talle,
                    foto=request.foto,
                    color=request.color,
                    stock=0  # Initial stock set to 0
                )
                db.session.add(nuevo_producto)
                db.session.commit()

                return stock_pb2.Producto(
                    id_producto=nuevo_producto.id,
                    codigo=nuevo_producto.codigo,
                    talle=nuevo_producto.talle,
                    foto=nuevo_producto.foto,
                    color=nuevo_producto.color,
                    stock=nuevo_producto.stock
                )
        except Exception as e:
            logging.error("Error al crear producto: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.Producto()

    def UpdateStock(self, request, context):  # New method to update stock
        logging.debug("Received UpdateStock request: %s", request)
        try:
            with app.app_context():
                producto = ProductoModel.query.get(request.id_producto)
                if not producto:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Producto no encontrado")
                    return stock_pb2.Producto()

                # Update stock based on the received request
                producto.stock = request.stock  # Assuming stock is passed in request
                db.session.commit()

                return stock_pb2.Producto(
                    id_producto=producto.id,
                    codigo=producto.codigo,
                    talle=producto.talle,
                    foto=producto.foto,
                    color=producto.color,
                    stock=producto.stock
                )
        except Exception as e:
            logging.error("Error al actualizar stock: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.Producto()

    def ListProductos(self, request, context):
        logging.debug("Received ListProductos request")
        try:
            with app.app_context():
                # Filter products based on user type
                query = ProductoModel.query

                if request.usuario_tipo == stock_pb2.UsuarioCasaCentral:  # Assuming you have such enum
                    # For Casa Central, no filtering
                    productos = query.all()
                elif request.usuario_tipo == stock_pb2.UsuarioTienda:  # Assuming you have such enum
                    # For Tienda, filter by tienda_id
                    productos = query.filter_by(tienda_id=request.tienda_id).all()
                else:
                    context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                    context.set_details("Tipo de usuario no permitido")
                    return stock_pb2.ProductosList()

                productos_list = stock_pb2.ProductosList()
                for producto in productos:
                    productos_list.productos.add(
                        id_producto=producto.id,
                        codigo=producto.codigo,
                        talle=producto.talle,
                        foto=producto.foto,
                        color=producto.color,
                        stock=producto.stock
                    )
                return productos_list
        except Exception as e:
            logging.error("Error al listar productos: %s", str(e), exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error interno del servidor")
            return stock_pb2.ProductosList()
