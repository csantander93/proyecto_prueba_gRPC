# services/usuario_service.py

import mysql.connector
import csv

class UsuarioService:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'database': 'stockearte'
        }

    def cargar_usuarios_desde_csv(self, file_path):
        errores = []
        usuarios_creados = 0
        
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor(dictionary=True)

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')

            for line_number, row in enumerate(csv_reader, start=1):
                if len(row) < 3:
                    errores.append(f"Línea {line_number}: Número insuficiente de campos.")
                    continue
                
                username, password, codigo_tienda = row

                # Validar campos vacíos
                if not username or not password or not codigo_tienda:
                    errores.append(f"Línea {line_number}: Campos vacíos.")
                    continue

                # Validar duplicidad de usuario
                cursor.execute("SELECT * FROM usuario WHERE username = %s", (username,))
                if cursor.fetchone():
                    errores.append(f"Línea {line_number}: Usuario '{username}' ya existe.")
                    continue

                # Validar existencia y estado de la tienda
                cursor.execute("SELECT id_tienda, habilitada FROM tienda WHERE codigo = %s", (codigo_tienda,))
                tienda = cursor.fetchone()
                if not tienda:
                    errores.append(f"Línea {line_number}: Código de tienda '{codigo_tienda}' no existe.")
                    continue
                if not tienda['habilitada']:
                    errores.append(f"Línea {line_number}: Tienda '{codigo_tienda}' está deshabilitada.")
                    continue

                # Insertar usuario
                cursor.execute("""
                    INSERT INTO usuario (username, password, habilitado, tienda_idtienda) 
                    VALUES (%s, %s, %s, %s)
                """, (username, password, True, tienda['id_tienda']))
                usuarios_creados += 1

        connection.commit()
        cursor.close()
        connection.close()
        
        return errores, usuarios_creados
