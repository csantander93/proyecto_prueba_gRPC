import grpc
from concurrent import futures
import tienda_pb2_grpc
from tienda_service import TiendaService  # Importa el servicio que acabamos de crear
import usuario_pb2_grpc
from usuario_service import UsuarioService  # Importa el servicio Usuario
import producto_pb2_grpc
from producto_service import ProductoService  # Importa el servicio Producto


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    tienda_pb2_grpc.add_TiendaServiceServicer_to_server(TiendaService(), server)
    usuario_pb2_grpc.add_UsuarioServiceServicer_to_server(UsuarioService(), server)
    producto_pb2_grpc.add_ProductoServiceServicer_to_server(ProductoService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC corriendo en el puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
