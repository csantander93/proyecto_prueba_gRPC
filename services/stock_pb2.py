# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: stock.proto
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
    'stock.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bstock.proto\x12\x06\x63\x61\x64\x65na\"+\n\x06\x43\x61\x64\x65na\x12\x11\n\tid_cadena\x18\x01 \x01(\x05\x12\x0e\n\x06nombre\x18\x02 \x01(\t\"\xc5\x01\n\x08Producto\x12\x13\n\x0bid_producto\x18\x01 \x01(\x05\x12\x0e\n\x06nombre\x18\x02 \x01(\t\x12\x0e\n\x06\x63odigo\x18\x03 \x01(\t\x12\r\n\x05talle\x18\x04 \x01(\t\x12\x0c\n\x04\x66oto\x18\x05 \x01(\t\x12\r\n\x05\x63olor\x18\x06 \x01(\t\x12*\n\x05stock\x18\x07 \x03(\x0b\x32\x1b.cadena.Producto.StockEntry\x1a,\n\nStockEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"\xb5\x01\n\x06Tienda\x12\x11\n\tid_tienda\x18\x01 \x01(\x05\x12\x0e\n\x06\x63odigo\x18\x02 \x01(\t\x12\x0e\n\x06nombre\x18\x03 \x01(\t\x12\x11\n\tdireccion\x18\x04 \x01(\t\x12\x0e\n\x06\x63iudad\x18\x05 \x01(\t\x12\x11\n\tprovincia\x18\x06 \x01(\t\x12\x12\n\nhabilitada\x18\x07 \x01(\x08\x12\x14\n\x0c\x63\x61sa_central\x18\x08 \x01(\x08\x12\x18\n\x10\x63\x61\x64\x65na_id_cadena\x18\t \x01(\x05\"\x90\x01\n\x07Usuario\x12\x12\n\nid_usuario\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x12\n\nhabilitado\x18\x04 \x01(\x08\x12\x17\n\x0ftienda_idtienda\x18\x05 \x01(\x05\x12\x0e\n\x06nombre\x18\x06 \x01(\t\x12\x10\n\x08\x61pellido\x18\x07 \x01(\t\"\x07\n\x05\x45mpty\"\x16\n\x08\x43\x61\x64\x65naId\x12\n\n\x02id\x18\x01 \x01(\x05\"\x18\n\nProductoId\x12\n\n\x02id\x18\x01 \x01(\x05\"\x16\n\x08TiendaId\x12\n\n\x02id\x18\x01 \x01(\x05\"\x17\n\tUsuarioId\x12\n\n\x02id\x18\x01 \x01(\x05\".\n\x0b\x43\x61\x64\x65nasList\x12\x1f\n\x07\x63\x61\x64\x65nas\x18\x01 \x03(\x0b\x32\x0e.cadena.Cadena\"4\n\rProductosList\x12#\n\tproductos\x18\x01 \x03(\x0b\x32\x10.cadena.Producto\".\n\x0bTiendasList\x12\x1f\n\x07tiendas\x18\x01 \x03(\x0b\x32\x0e.cadena.Tienda\"1\n\x0cUsuariosList\x12!\n\x08usuarios\x18\x01 \x03(\x0b\x32\x0f.cadena.Usuario2\xd2\x01\n\rCadenaService\x12-\n\tGetCadena\x12\x10.cadena.CadenaId\x1a\x0e.cadena.Cadena\x12.\n\x0c\x43reateCadena\x12\x0e.cadena.Cadena\x1a\x0e.cadena.Cadena\x12/\n\x0c\x44\x65leteCadena\x12\x10.cadena.CadenaId\x1a\r.cadena.Empty\x12\x31\n\x0bListCadenas\x12\r.cadena.Empty\x1a\x13.cadena.CadenasList2\xe9\x01\n\x0fProductoService\x12\x33\n\x0bGetProducto\x12\x12.cadena.ProductoId\x1a\x10.cadena.Producto\x12\x34\n\x0e\x43reateProducto\x12\x10.cadena.Producto\x1a\x10.cadena.Producto\x12\x34\n\x0eUpdateProducto\x12\x10.cadena.Producto\x1a\x10.cadena.Producto\x12\x35\n\rListProductos\x12\r.cadena.Empty\x1a\x15.cadena.ProductosList2\xd2\x01\n\rTiendaService\x12-\n\tGetTienda\x12\x10.cadena.TiendaId\x1a\x0e.cadena.Tienda\x12.\n\x0c\x43reateTienda\x12\x0e.cadena.Tienda\x1a\x0e.cadena.Tienda\x12/\n\x0c\x44\x65leteTienda\x12\x10.cadena.TiendaId\x1a\r.cadena.Empty\x12\x31\n\x0bListTiendas\x12\r.cadena.Empty\x1a\x13.cadena.TiendasList2\x90\x02\n\x0eUsuarioService\x12\x30\n\nGetUsuario\x12\x11.cadena.UsuarioId\x1a\x0f.cadena.Usuario\x12\x31\n\rCreateUsuario\x12\x0f.cadena.Usuario\x1a\x0f.cadena.Usuario\x12\x31\n\rUpdateUsuario\x12\x0f.cadena.Usuario\x1a\x0f.cadena.Usuario\x12\x31\n\rDeleteUsuario\x12\x11.cadena.UsuarioId\x1a\r.cadena.Empty\x12\x33\n\x0cListUsuarios\x12\r.cadena.Empty\x1a\x14.cadena.UsuariosList2A\n\x0cStockService\x12\x31\n\x0bUpdateStock\x12\x10.cadena.Producto\x1a\x10.cadena.Productob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stock_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PRODUCTO_STOCKENTRY']._loaded_options = None
  _globals['_PRODUCTO_STOCKENTRY']._serialized_options = b'8\001'
  _globals['_CADENA']._serialized_start=23
  _globals['_CADENA']._serialized_end=66
  _globals['_PRODUCTO']._serialized_start=69
  _globals['_PRODUCTO']._serialized_end=266
  _globals['_PRODUCTO_STOCKENTRY']._serialized_start=222
  _globals['_PRODUCTO_STOCKENTRY']._serialized_end=266
  _globals['_TIENDA']._serialized_start=269
  _globals['_TIENDA']._serialized_end=450
  _globals['_USUARIO']._serialized_start=453
  _globals['_USUARIO']._serialized_end=597
  _globals['_EMPTY']._serialized_start=599
  _globals['_EMPTY']._serialized_end=606
  _globals['_CADENAID']._serialized_start=608
  _globals['_CADENAID']._serialized_end=630
  _globals['_PRODUCTOID']._serialized_start=632
  _globals['_PRODUCTOID']._serialized_end=656
  _globals['_TIENDAID']._serialized_start=658
  _globals['_TIENDAID']._serialized_end=680
  _globals['_USUARIOID']._serialized_start=682
  _globals['_USUARIOID']._serialized_end=705
  _globals['_CADENASLIST']._serialized_start=707
  _globals['_CADENASLIST']._serialized_end=753
  _globals['_PRODUCTOSLIST']._serialized_start=755
  _globals['_PRODUCTOSLIST']._serialized_end=807
  _globals['_TIENDASLIST']._serialized_start=809
  _globals['_TIENDASLIST']._serialized_end=855
  _globals['_USUARIOSLIST']._serialized_start=857
  _globals['_USUARIOSLIST']._serialized_end=906
  _globals['_CADENASERVICE']._serialized_start=909
  _globals['_CADENASERVICE']._serialized_end=1119
  _globals['_PRODUCTOSERVICE']._serialized_start=1122
  _globals['_PRODUCTOSERVICE']._serialized_end=1355
  _globals['_TIENDASERVICE']._serialized_start=1358
  _globals['_TIENDASERVICE']._serialized_end=1568
  _globals['_USUARIOSERVICE']._serialized_start=1571
  _globals['_USUARIOSERVICE']._serialized_end=1843
  _globals['_STOCKSERVICE']._serialized_start=1845
  _globals['_STOCKSERVICE']._serialized_end=1910
# @@protoc_insertion_point(module_scope)
