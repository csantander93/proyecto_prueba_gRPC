import grpc
from concurrent import futures
import stock_pb2_grpc
from app import app
from models.cadena import Cadena
from models.tienda import Tienda
from models.database import db
from services import UsuarioService, TiendaService, ProductoService

import random
import string
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generar_codigo_tienda():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def inicializar_cadena_y_tiendas():
    with app.app_context():
        cadena_existente = db.session.query(Cadena).filter_by(nombre='CadenaEjemplo').first()
        if not cadena_existente:
            nueva_cadena = Cadena(nombre='CadenaEjemplo')
            db.session.add(nueva_cadena)
            db.session.commit()
            logging.info("Cadena inicializada: CadenaEjemplo")
            cadena_id = nueva_cadena.id_cadena

            codigo_tienda = generar_codigo_tienda()
            nueva_tienda = Tienda(
                codigo=codigo_tienda, 
                nombre='Tienda Ejemplo',
                direccion='Calle Falsa 123',
                ciudad='Ciudad Ejemplo',
                provincia='Provincia Ejemplo',
                habilitada=True,
                casa_central=False,
                cadena_id_cadena=cadena_id
            )
            db.session.add(nueva_tienda)
            db.session.commit()
            logging.info(f"Tienda inicializada: {codigo_tienda}")
        else:
            logging.info("La cadena ya existe: CadenaEjemplo")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    stock_pb2_grpc.add_StockearteServiceServicer_to_server(UsuarioService(), server)
    stock_pb2_grpc.add_StockearteServiceServicer_to_server(TiendaService(), server)
    stock_pb2_grpc.add_StockearteServiceServicer_to_server(ProductoService(), server)
    
    server.add_insecure_port('[::]:50051')
    inicializar_cadena_y_tiendas()  # Inicializar dentro del contexto de la app
    
    logging.info("Servidor gRPC corriendo en el puerto 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
