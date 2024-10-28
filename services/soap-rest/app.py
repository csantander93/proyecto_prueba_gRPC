# /soap_rest/app.py

from flask import Flask
from controllers.orden_compra_controller import orden_compra_bp

app = Flask(__name__)

# Registra el blueprint
app.register_blueprint(orden_compra_bp)

if __name__ == '__main__':
    app.run(debug=True)
