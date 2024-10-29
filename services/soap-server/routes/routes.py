from flask import Blueprint
from controllers import OrderController

order_bp = Blueprint('order', __name__)
controller = OrderController()

@order_bp.route('/soap/order', methods=['POST'])
def get_orders():
    return controller.get_orders()
