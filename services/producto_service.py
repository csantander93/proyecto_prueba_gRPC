import grpc
from models import db, Producto
import stock_pb2
from app import app
import logging

class ProductoService(stock_pb2.StockearteServiceServicer):

    def CrearProducto(self, request, context):
        logging.debug("Received CrearProducto request: %s", request)
        try:
            with app.app_context():
                producto_existente = Producto.query.filter_by(codigo=request.codigo).first()
                if producto_existente:
                    context.set_details("Producto con ese código ya existe")
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    return stock_pb2.ProductoResponse(mensaje="El producto ya existe")

                nuevo_producto = Producto(
                    nombre=request.nombre,
                    codigo=request.codigo,
                    talle=request.talle,
                    color=request.color,
                    stock=request.stock
                )
                db.session.add(nuevo_producto)
                db.session.commit()
                logging.info("Producto creado exitosamente: %s", request.codigo)
                
                return stock_pb2.ProductoResponse(
                    mensaje="Producto creado exitosamente",
                    codigo=request.codigo
                )
        except Exception as e:
            logging.error("Error al crear producto: %s", str(e), exc_info=True)
            context.set_details("Error interno del servidor: " + str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return stock_pb2.ProductoResponse(mensaje="Error interno del servidor")

    def ModificarProducto(self, request, context):
        logging.debug("Received ModificarProducto request: %s", request)
        try:
            with app.app_context():
                producto = Producto.query.filter_by(codigo=request.codigo).first()
                if producto:
                    producto.nombre = request.nombre
                    producto.talle = request.talle
                    producto.color = request.color
                    producto.stock = request.stock
                    db.session.commit()
                    logging.info("Producto modificado exitosamente: %s", request.codigo)
                    return stock_pb2.ProductoResponse(mensaje="Producto modificado exitosamente")
                
                logging.warning("Producto no encontrado: %s", request.codigo)
                return stock_pb2.ProductoResponse(mensaje="Producto no encontrado")
        except Exception as e:
            logging.error("Error al modificar producto: %s", str(e), exc_info=True)
            context.set_details("Error interno del servidor")
            context.set_code(grpc.StatusCode.INTERNAL)
            return stock_pb2.ProductoResponse(mensaje="Error interno del servidor")

    def AlternarHabilitadaProducto(self, request, context):
        logging.debug("Received AlternarHabilitadaProducto request: %s", request)
        try:
            with app.app_context():
                producto = Producto.query.filter_by(codigo=request.codigo).first()
                if producto:
                    producto.habilitada = not producto.habilitada
                    db.session.commit()
                    estado = "habilitado" if producto.habilitada else "deshabilitado"
                    logging.info("Producto %s cambiado a: %s", request.codigo, estado)
                    return stock_pb2.ProductoResponse(mensaje=f"Producto {estado} exitosamente")
                
                logging.warning("Producto no encontrado: %s", request.codigo)
                return stock_pb2.ProductoResponse(mensaje="Producto no encontrado")
        except Exception as e:
            logging.error("Error al alternar habilitada de producto: %s", str(e), exc_info=True)
            context.set_details("Error interno del servidor")
            context.set_code(grpc.StatusCode.INTERNAL)
            return stock_pb2.ProductoResponse(mensaje="Error interno del servidor")
