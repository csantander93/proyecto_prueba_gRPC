# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import tienda_pb2 as tienda__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in tienda_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TiendaServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CrearTienda = channel.unary_unary(
                '/tienda.TiendaService/CrearTienda',
                request_serializer=tienda__pb2.CrearTiendaRequest.SerializeToString,
                response_deserializer=tienda__pb2.TiendaResponse.FromString,
                _registered_method=True)
        self.ModificarTienda = channel.unary_unary(
                '/tienda.TiendaService/ModificarTienda',
                request_serializer=tienda__pb2.ModificarTiendaRequest.SerializeToString,
                response_deserializer=tienda__pb2.TiendaResponse.FromString,
                _registered_method=True)
        self.BorrarTienda = channel.unary_unary(
                '/tienda.TiendaService/BorrarTienda',
                request_serializer=tienda__pb2.BorrarTiendaRequest.SerializeToString,
                response_deserializer=tienda__pb2.TiendaResponse.FromString,
                _registered_method=True)
        self.BuscarTienda = channel.unary_unary(
                '/tienda.TiendaService/BuscarTienda',
                request_serializer=tienda__pb2.BuscarTiendaRequest.SerializeToString,
                response_deserializer=tienda__pb2.TiendaResponse.FromString,
                _registered_method=True)
        self.EnlistarTiendas = channel.unary_unary(
                '/tienda.TiendaService/EnlistarTiendas',
                request_serializer=tienda__pb2.EnlistarTiendasRequest.SerializeToString,
                response_deserializer=tienda__pb2.TiendasResponse.FromString,
                _registered_method=True)
        self.BuscarTiendaPorNombre = channel.unary_unary(
                '/tienda.TiendaService/BuscarTiendaPorNombre',
                request_serializer=tienda__pb2.BuscarTiendaPorNombreRequest.SerializeToString,
                response_deserializer=tienda__pb2.TiendaResponse.FromString,
                _registered_method=True)


class TiendaServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CrearTienda(self, request, context):
        """CRUD Methods
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModificarTienda(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BorrarTienda(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BuscarTienda(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EnlistarTiendas(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BuscarTiendaPorNombre(self, request, context):
        """Nuevo método para buscar por nombre
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TiendaServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CrearTienda': grpc.unary_unary_rpc_method_handler(
                    servicer.CrearTienda,
                    request_deserializer=tienda__pb2.CrearTiendaRequest.FromString,
                    response_serializer=tienda__pb2.TiendaResponse.SerializeToString,
            ),
            'ModificarTienda': grpc.unary_unary_rpc_method_handler(
                    servicer.ModificarTienda,
                    request_deserializer=tienda__pb2.ModificarTiendaRequest.FromString,
                    response_serializer=tienda__pb2.TiendaResponse.SerializeToString,
            ),
            'BorrarTienda': grpc.unary_unary_rpc_method_handler(
                    servicer.BorrarTienda,
                    request_deserializer=tienda__pb2.BorrarTiendaRequest.FromString,
                    response_serializer=tienda__pb2.TiendaResponse.SerializeToString,
            ),
            'BuscarTienda': grpc.unary_unary_rpc_method_handler(
                    servicer.BuscarTienda,
                    request_deserializer=tienda__pb2.BuscarTiendaRequest.FromString,
                    response_serializer=tienda__pb2.TiendaResponse.SerializeToString,
            ),
            'EnlistarTiendas': grpc.unary_unary_rpc_method_handler(
                    servicer.EnlistarTiendas,
                    request_deserializer=tienda__pb2.EnlistarTiendasRequest.FromString,
                    response_serializer=tienda__pb2.TiendasResponse.SerializeToString,
            ),
            'BuscarTiendaPorNombre': grpc.unary_unary_rpc_method_handler(
                    servicer.BuscarTiendaPorNombre,
                    request_deserializer=tienda__pb2.BuscarTiendaPorNombreRequest.FromString,
                    response_serializer=tienda__pb2.TiendaResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tienda.TiendaService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('tienda.TiendaService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TiendaService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CrearTienda(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tienda.TiendaService/CrearTienda',
            tienda__pb2.CrearTiendaRequest.SerializeToString,
            tienda__pb2.TiendaResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ModificarTienda(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tienda.TiendaService/ModificarTienda',
            tienda__pb2.ModificarTiendaRequest.SerializeToString,
            tienda__pb2.TiendaResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def BorrarTienda(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tienda.TiendaService/BorrarTienda',
            tienda__pb2.BorrarTiendaRequest.SerializeToString,
            tienda__pb2.TiendaResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def BuscarTienda(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tienda.TiendaService/BuscarTienda',
            tienda__pb2.BuscarTiendaRequest.SerializeToString,
            tienda__pb2.TiendaResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def EnlistarTiendas(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tienda.TiendaService/EnlistarTiendas',
            tienda__pb2.EnlistarTiendasRequest.SerializeToString,
            tienda__pb2.TiendasResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def BuscarTiendaPorNombre(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/tienda.TiendaService/BuscarTiendaPorNombre',
            tienda__pb2.BuscarTiendaPorNombreRequest.SerializeToString,
            tienda__pb2.TiendaResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
