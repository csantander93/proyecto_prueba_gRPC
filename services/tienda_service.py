import grpc
from models import db, Tienda
import stock_pb2
from app import app
import logging

class TiendaService(stock_pb2.StockearteServiceServicer):

    def CrearTienda(self, request, context):
        logging.debug("Received CrearTienda request: %s", request)
        try:
            with app.app_context():
                nueva_tienda = Tienda(
                    codigo=request.codigo,
                    direccion=request.direccion,
                    ciudad=request.ciudad,
                    provincia=request.provincia,
                    habilitada=request.habilitada
                )
                db.session.add(nueva_tienda)
                db.session.commit()
                logging.info("Tienda creada exitosamente: %s", request.codigo)
                return stock_pb2.TiendaResponse(mensaje="Tienda creada exitosamente")
        except Exception as e:
            logging.error("Error al crear tienda: %s", str(e), exc_info=True)
            context.set_details("Error interno del servidor")
            context.set_code(grpc.StatusCode.INTERNAL)
            return stock_pb2.TiendaResponse(mensaje="Error interno del servidor")

    def AlternarHabilitadaTienda(self, request, context):
        logging.debug("Received AlternarHabilitadaTienda request: %s", request)
        try:
            with app.app_context():
                tienda = Tienda.query.filter_by(codigo=request.codigo).first()
                if tienda:
                    tienda.habilitada = not tienda.habilitada
                    db.session.commit()
                    estado = "habilitada" if tienda.habilitada else "deshabilitada"
                    logging.info("Tienda %s cambiada a: %s", request.codigo, estado)
                    return stock_pb2.TiendaResponse(mensaje=f"Tienda {estado} exitosamente")
                
                logging.warning("Tienda no encontrada: %s", request.codigo)
                return stock_pb2.TiendaResponse(mensaje="Tienda no encontrada")
        except Exception as e:
            logging.error("Error al alternar habilitada de tienda: %s", str(e), exc_info=True)
            context.set_details("Error interno del servidor")
            context.set_code(grpc.StatusCode.INTERNAL)
            return stock_pb2.TiendaResponse(mensaje="Error interno del servidor")
