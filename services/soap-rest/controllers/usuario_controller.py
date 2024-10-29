# controllers/usuario_controller.py

from flask import Blueprint, jsonify, render_template, request
from services.usuario_service import UsuarioService
import os

usuario_bp = Blueprint('usuario', __name__)
usuario_service = UsuarioService()
@usuario_bp.route('/cargar_usuarios', methods=['GET', 'POST'])
def cargar_usuarios_csv():
    if request.method == 'POST':
        # Guardar archivo temporalmente
        if 'csvFile' not in request.files:
            return jsonify({"mensaje": "No se encontró el archivo CSV", "errores": ["Archivo no proporcionado"]}), 400
        
        csv_file = request.files['csvFile']
        if csv_file.filename == '':
            return jsonify({"mensaje": "No se seleccionó ningún archivo"}), 400

        # Guardar el archivo en una carpeta temporal para procesarlo
        file_path = os.path.join('data', csv_file.filename)
        
        try:
            csv_file.save(file_path)

            # Procesar el archivo CSV
            errores, total_creados = usuario_service.cargar_usuarios_desde_csv(file_path)

        finally:
            # Intentar eliminar el archivo temporal después de procesarlo
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except PermissionError as e:
                    print(f"Error al eliminar el archivo: {e}")

        # Retornar el resultado como JSON
        return jsonify({
            "mensaje": f"Usuarios cargados: {total_creados}.",
            "errores": errores
        })

    # Método GET: mostrar formulario de carga
    return render_template('cargar_usuarios.html')
