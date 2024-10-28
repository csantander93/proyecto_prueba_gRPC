# from flask import Flask, render_template, request, redirect, url_for
# from models import db, ArticuloProveedor
# from app_proveedor import app
# import json
# from datetime import datetime
# import requests
# @app.route('/')
# def index():
#     return redirect(url_for('listar_productos'))

# # PROVEEDOR_SERVICE_URL = 'http://localhost:5001/reprocesar_orden' 

# @app.route('/productos')
# def listar_productos():
#     productos = ArticuloProveedor.query.all()
#     return render_template('listar_productos.html', productos=productos)

# @app.route('/productos/nuevo', methods=['GET', 'POST'])
# def nuevo_producto():
#     if request.method == 'POST':
#         codigo_articulo = request.form['codigo_articulo']
#         nombre = request.form['nombre']
#         talle = request.form['talle']
#         color = request.form['color']
#         stock = int(request.form['stock'])

#         nuevo_producto = ArticuloProveedor(
#             codigo_articulo=codigo_articulo,
#             nombre=nombre,
#             talle=talle,
#             color=color,
#             stock=stock
#         )
#         db.session.add(nuevo_producto)
#         db.session.commit()
#         return redirect(url_for('listar_productos'))
#     return render_template('nuevo_producto.html')

# @app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
# def editar_producto(id):
#     producto = ArticuloProveedor.query.get_or_404(id)
#     if request.method == 'POST':
#         producto.codigo_articulo = request.form['codigo_articulo']
#         producto.nombre = request.form['nombre']
#         producto.talle = request.form['talle']
#         producto.color = request.form['color']
#         producto.stock = int(request.form['stock'])
#         db.session.commit()
#         return redirect(url_for('listar_productos'))
#     return render_template('editar_producto.html', producto=producto)

# def editar_producto(id):
#     producto = ArticuloProveedor.query.get_or_404(id)
#     if request.method == 'POST':
#         producto.codigo_articulo = request.form['codigo_articulo']
#         producto.nombre = request.form['nombre']
#         producto.talle = request.form['talle']
#         producto.color = request.form['color']
#         producto.stock = int(request.form['stock'])
        
#         db.session.commit()
        
#         # Reprocesar órdenes pausadas al actualizar el stock del producto
#         reprocesar_ordenes_pausadas(producto)

#         return redirect(url_for('listar_productos'))
#     return render_template('editar_producto.html', producto=producto)

# def reprocesar_ordenes_pausadas(producto):
#     """Reprocesa órdenes de compra pausadas que contengan el producto actualizado."""
#     # Obtener las órdenes pausadas que contengan el producto actualizado
#     ordenes_pausadas = OrdenCompra.query.filter_by(estado='PAUSADA').all()
    
#     for orden in ordenes_pausadas:
#         items = orden.items  # Supongamos que los items son una lista de dict con 'codigo_articulo' y 'cantidad_solicitada'
#         # Verificar si el producto está en la orden
#         for item in items:
#             if item['codigo_articulo'] == producto.codigo_articulo:
#                 # Enviar la orden a reprocesar al servicio que maneja las órdenes
#                 payload = {
#                     "codigo_tienda": orden.codigo_tienda,
#                     "id_orden": orden.id,
#                     "items": items
#                 }
#                 try:
#                     response = requests.post(f"{PROVEEDOR_SERVICE_URL}", json=payload)
#                     if response.status_code == 200:
#                         print(f"Orden {orden.id} reprocesada exitosamente.")
#                     else:
#                         print(f"Error al reprocesar la orden {orden.id}: {response.text}")
#                 except requests.exceptions.RequestException as e:
#                     print(f"Error al conectar con el servicio de ordenes: {e}")

# @app.route('/productos/eliminar/<int:id>', methods=['POST'])
# def eliminar_producto(id):
#     producto = ArticuloProveedor.query.get_or_404(id)
#     db.session.delete(producto)
#     db.session.commit()
#     return redirect(url_for('listar_productos'))

# if __name__ == '__main__':
#     app.run(debug=True, port=5002)
from flask import Flask, render_template, request, redirect, url_for
from models import db, ArticuloProveedor, OrdenCompraProveedor
import json
import requests
from app_proveedor import app
from proveedor_service import procesar_orden
from flask import Flask, render_template, request, redirect, url_for
from models import db, ArticuloProveedor
from proveedor_service import enviar_a_kafka  


@app.route('/')
def index():
    return redirect(url_for('listar_productos'))

@app.route('/productos')
def listar_productos():
    productos = ArticuloProveedor.query.all()
    return render_template('listar_productos.html', productos=productos)

# @app.route('/productos/nuevo', methods=['GET', 'POST'])
# def nuevo_producto():
#     if request.method == 'POST':
#         codigo_articulo = request.form['codigo_articulo']
#         nombre = request.form['nombre']
#         talle = request.form['talle']
#         color = request.form['color']
#         stock = int(request.form['stock'])

#         nuevo_producto = ArticuloProveedor(
#             codigo_articulo=codigo_articulo,
#             nombre=nombre,
#             talle=talle,
#             color=color,
#             stock=stock
#         )
#         db.session.add(nuevo_producto)
#         db.session.commit()
#         return redirect(url_for('listar_productos'))
#     return render_template('nuevo_producto.html')

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        codigo_articulo = request.form['codigo_articulo']
        nombre = request.form['nombre']
        stock = int(request.form['stock'])

        # Obtener los talles y colores
        talles = []
        index = 0
        while True:
            talle_key = f'talles[{index}][talle]'
            colores_key = f'talles[{index}][colores][]'
            if talle_key not in request.form:
                break
            talle = request.form[talle_key]
            colores = request.form.getlist(colores_key)
            talles.append({'talle': talle, 'colores': colores})
            index += 1

        # Obtener las URLs de las fotos
        urls_fotos = request.form.getlist('urls_fotos[]')

        nuevo_producto = ArticuloProveedor(
            codigo_articulo=codigo_articulo,
            nombre=nombre,
            talles_colores=talles,
            urls_fotos=urls_fotos,
            stock=stock
        )
        db.session.add(nuevo_producto)
        db.session.commit()

        # Enviar mensaje al tópico '/novedades'
        mensaje = {
            'codigo_producto': codigo_articulo,
            'talles_colores': talles,
            'urls_fotos': urls_fotos
        }
        enviar_a_kafka('novedades', mensaje)

        return redirect(url_for('listar_productos'))
    return render_template('nuevo_producto.html')

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = ArticuloProveedor.query.get_or_404(id)
    if request.method == 'POST':
        producto.codigo_articulo = request.form['codigo_articulo']
        producto.nombre = request.form['nombre']
        producto.talle = request.form['talle']
        producto.color = request.form['color']
        nuevo_stock = int(request.form['stock'])
        stock_incremento = nuevo_stock - producto.stock  # Calcular la diferencia de stock

        producto.stock = nuevo_stock
        db.session.commit()

        # Reprocesar órdenes pausadas
        reprocesar_ordenes_pausadas(producto.codigo_articulo)

        return redirect(url_for('listar_productos'))
    return render_template('editar_producto.html', producto=producto)

#def reprocesar_ordenes_pausadas(codigo_articulo_actualizado):
    # Obtener las órdenes pausadas que contienen el artículo actualizado
    # ordenes_pausadas = OrdenCompraProveedor.query.filter_by(estado='PAUSADA').all()
    # for orden in ordenes_pausadas:
    #     items = json.loads(orden.items)
    #     contiene_articulo = any(item['codigo_articulo'] == codigo_articulo_actualizado for item in items)
    #     if contiene_articulo:
    #         # Reintentar procesar la orden
    #         mensaje_orden = {
    #             "codigo_tienda": orden.codigo_tienda,
    #             "id_orden": orden.id_orden,
    #             "items": items,
    #             "fecha_solicitud": orden.fecha_creacion.isoformat()
    #         }
    #         # Puedes llamar directamente a procesar_orden o enviar el mensaje a Kafka
    #         procesar_orden(json.dumps(mensaje_orden))
def reprocesar_ordenes_pausadas(codigo_articulo_actualizado):
    # Obtener las órdenes pausadas que contienen el artículo actualizado
    ordenes_pausadas = OrdenCompraProveedor.query.filter_by(estado='PAUSADA').all()
    for orden in ordenes_pausadas:
        items = json.loads(orden.items)
        contiene_articulo = any(item['codigo_articulo'] == codigo_articulo_actualizado for item in items)
        
        if contiene_articulo:
            # Reintentar procesar la orden
            mensaje_orden = {
                "codigo_tienda": orden.codigo_tienda,
                "id_orden": orden.id_orden,
                "items": items,
                "fecha_solicitud": orden.fecha_creacion.isoformat()
            }
            # Llamar al método de procesar_orden para intentar procesar la orden con el nuevo stock
            procesar_orden(json.dumps(mensaje_orden))

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = ArticuloProveedor.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('listar_productos'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
