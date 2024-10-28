from confluent_kafka import Consumer
import json

from models import db, NovedadProducto
from app import app

def consumir_novedades():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'casa_central_consumer',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe(['novedades'])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f'Error: {msg.error()}')
                continue

            mensaje = json.loads(msg.value().decode('utf-8'))
            procesar_novedad(mensaje)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def procesar_novedad(mensaje):
    with app.app_context():
        codigo_producto = mensaje['codigo_producto']
        talles_colores = mensaje['talles_colores']
        urls_fotos = mensaje['urls_fotos']

        # Verificar si la novedad ya existe
        novedad_existente = NovedadProducto.query.filter_by(codigo_producto=codigo_producto).first()
        if not novedad_existente:
            nueva_novedad = NovedadProducto(
                codigo_producto=codigo_producto,
                talles_colores=json.dumps(talles_colores),
                urls_fotos=json.dumps(urls_fotos)
            )
            db.session.add(nueva_novedad)
            db.session.commit()
            print(f'Novedad de producto {codigo_producto} almacenada.')
        else:
            print(f'Novedad de producto {codigo_producto} ya existe.')

if __name__ == '__main__':
    consumir_novedades()


