from flask import Flask, render_template, request, redirect, url_for
from models import db, NovedadProducto, Producto
from app import app

@app.route('/novedades')
def listar_novedades():
    novedades = NovedadProducto.query.filter_by(procesado=False).all()
    return render_template('listar_novedades.html', novedades=novedades)

@app.route('/novedades/procesar/<int:id>', methods=['GET', 'POST'])
def procesar_novedad(id):
    novedad = NovedadProducto.query.get_or_404(id)
    if request.method == 'POST':
        talles_seleccionados = request.form.getlist('talles[]')
        colores_por_talle = {}
        for talle in talles_seleccionados:
            colores = request.form.getlist(f'colores_{talle}[]')
            colores_por_talle[talle] = colores

        # Crear los productos seleccionados en el sistema
        for talle, colores in colores_por_talle.items():
            for color in colores:
                nuevo_producto = Producto(
                    codigo_producto=novedad.codigo_producto,
                    nombre=f'{novedad.codigo_producto} - Talle {talle} - Color {color}',
                    talle=talle,
                    color=color,
                    # Otros campos según tu modelo
                )
                db.session.add(nuevo_producto)
        novedad.procesado = True
        db.session.commit()
        return redirect(url_for('listar_novedades'))
    else:
        talles_colores = novedad.get_talles_colores()
        return render_template('procesar_novedad.html', novedad=novedad, talles_colores=talles_colores)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos si no existen
    app.run(debug=True, port=5003)
