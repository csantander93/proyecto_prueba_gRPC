# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: producto.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'producto.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eproducto.proto\x12\x08producto\"\x8d\x01\n\x08Producto\x12\x13\n\x0bid_producto\x18\x01 \x01(\x05\x12\x0e\n\x06\x63odigo\x18\x02 \x01(\t\x12\x0e\n\x06nombre\x18\x03 \x01(\t\x12\r\n\x05talle\x18\x04 \x01(\t\x12\x0c\n\x04\x66oto\x18\x05 \x01(\t\x12\r\n\x05\x63olor\x18\x06 \x01(\t\x12\r\n\x05stock\x18\x07 \x01(\x05\x12\x11\n\tid_tienda\x18\x08 \x01(\x05\"\x84\x01\n\x14\x43rearProductoRequest\x12\x0e\n\x06\x63odigo\x18\x01 \x01(\t\x12\x0e\n\x06nombre\x18\x02 \x01(\t\x12\r\n\x05talle\x18\x03 \x01(\t\x12\x0c\n\x04\x66oto\x18\x04 \x01(\t\x12\r\n\x05\x63olor\x18\x05 \x01(\t\x12\r\n\x05stock\x18\x06 \x01(\x05\x12\x11\n\tid_tienda\x18\x07 \x01(\x05\"\x9d\x01\n\x18ModificarProductoRequest\x12\x13\n\x0bid_producto\x18\x01 \x01(\x05\x12\x0e\n\x06\x63odigo\x18\x02 \x01(\t\x12\x0e\n\x06nombre\x18\x03 \x01(\t\x12\r\n\x05talle\x18\x04 \x01(\t\x12\x0c\n\x04\x66oto\x18\x05 \x01(\t\x12\r\n\x05\x63olor\x18\x06 \x01(\t\x12\r\n\x05stock\x18\x07 \x01(\x05\x12\x11\n\tid_tienda\x18\x08 \x01(\x05\",\n\x15\x42orrarProductoRequest\x12\x13\n\x0bid_producto\x18\x01 \x01(\x05\"\'\n\x15\x42uscarProductoRequest\x12\x0e\n\x06nombre\x18\x01 \x01(\t\"\x1a\n\x18\x45nlistarProductosRequest\"8\n\x10ProductoResponse\x12$\n\x08producto\x18\x01 \x01(\x0b\x32\x12.producto.Producto\":\n\x11ProductosResponse\x12%\n\tproductos\x18\x01 \x03(\x0b\x32\x12.producto.Producto2\xa7\x03\n\x0fProductoService\x12K\n\rCrearProducto\x12\x1e.producto.CrearProductoRequest\x1a\x1a.producto.ProductoResponse\x12S\n\x11ModificarProducto\x12\".producto.ModificarProductoRequest\x1a\x1a.producto.ProductoResponse\x12M\n\x0e\x42orrarProducto\x12\x1f.producto.BorrarProductoRequest\x1a\x1a.producto.ProductoResponse\x12M\n\x0e\x42uscarProducto\x12\x1f.producto.BuscarProductoRequest\x1a\x1a.producto.ProductoResponse\x12T\n\x11\x45nlistarProductos\x12\".producto.EnlistarProductosRequest\x1a\x1b.producto.ProductosResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'producto_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PRODUCTO']._serialized_start=29
  _globals['_PRODUCTO']._serialized_end=170
  _globals['_CREARPRODUCTOREQUEST']._serialized_start=173
  _globals['_CREARPRODUCTOREQUEST']._serialized_end=305
  _globals['_MODIFICARPRODUCTOREQUEST']._serialized_start=308
  _globals['_MODIFICARPRODUCTOREQUEST']._serialized_end=465
  _globals['_BORRARPRODUCTOREQUEST']._serialized_start=467
  _globals['_BORRARPRODUCTOREQUEST']._serialized_end=511
  _globals['_BUSCARPRODUCTOREQUEST']._serialized_start=513
  _globals['_BUSCARPRODUCTOREQUEST']._serialized_end=552
  _globals['_ENLISTARPRODUCTOSREQUEST']._serialized_start=554
  _globals['_ENLISTARPRODUCTOSREQUEST']._serialized_end=580
  _globals['_PRODUCTORESPONSE']._serialized_start=582
  _globals['_PRODUCTORESPONSE']._serialized_end=638
  _globals['_PRODUCTOSRESPONSE']._serialized_start=640
  _globals['_PRODUCTOSRESPONSE']._serialized_end=698
  _globals['_PRODUCTOSERVICE']._serialized_start=701
  _globals['_PRODUCTOSERVICE']._serialized_end=1124
# @@protoc_insertion_point(module_scope)
