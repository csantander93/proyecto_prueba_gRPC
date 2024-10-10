from proveedor_service import ProveedorService

if __name__ == '__main__':
    # Simulación de una orden de compra recibida
    orden_compra = {
        'id_orden': 1,
        'codigo_tienda': 'T123',
        'items': [
            {'codigo_articulo': 'AAAB', 'color': 'Rojo', 'talle': 'M', 'cantidad': 5},
            {'codigo_articulo': 'XXZZ', 'color': 'Azul', 'talle': 'L', 'cantidad': 0}
        ]
    }
    
    # Procesar la orden de compra
    proveedor_service = ProveedorService()
    proveedor_service.procesar_orden(orden_compra)
