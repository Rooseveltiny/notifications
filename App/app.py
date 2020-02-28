import os
import sys
from models import db, Order, WarehousesStatus
import uuid

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from flask import Flask, render_template, request, redirect, escape, session, copy_current_request_context, jsonify

app = Flask(__name__, template_folder='templates')
app.secret_key = 'perokngsronsortv[troijvgdoitjbpoijb[otidj5u8-58he85-whghg049h-w49b-3tq-bw9-t98-39g-98t'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+file_dir+'/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def hello_world():

    return 'Hello, World!'

@app.route('/notification/<order_number>')
def notification_page(order_number):
    
    order = Order.query.filter_by(uuid = order_number).first()
    statuses = order.get_warehouse_statuses()

    context_data = dict()
    context_data["client_name"] = order.client_name
    context_data["order_number"] = str(order.order_number)
    context_data["status_of_order"] = "Ваш заказ готов" if order.status_of_order else "Заказ ещё в работе" 
    context_data["date_of_getting"] = order.date_of_getting
    context_data["bool_ready"] = order.status_of_order

    list_of_statuses = []
    for element in statuses:
        list_of_statuses.append(
            {"warehouse": element.warehouse_number,
            "status": "Готово" if element.status else "Не готов",
            "bool_status": element.status}
        )

    list_of_statuses = sorted(list_of_statuses, key=lambda x: x['warehouse'])
    context_data["warehousestatus"] = list_of_statuses

    return render_template('base.html', **context_data)

@app.route('/get_notifications', methods=["POST"])
def get_notifications():

    if request.headers['secret-key'] == app.secret_key:

        request_data = request.get_json(force=True)
        order = Order(
        uuid = request_data['uuid'], 
        client_name = request_data['client_name'], 
        order_number = request_data["order_number"],
        status_of_order = request_data["status_of_order"],
        date_of_getting = request_data["date_of_getting"]
        )   
        order.save()
        
        WarehousesStatus.delete_previous_data(request_data['uuid']) ### to refresh all statuses in all warehouses
        for warehouse in request_data['warehouses_status']:
            warehousestatus = WarehousesStatus(
            order_uuid = request_data["uuid"],
            warehouse_number = warehouse["warehouse"],
            status = warehouse["status"]
            )
            warehousestatus.save()

        return 'ok'

    return 'not ok)'
    
@app.route("/db_create")
def db_create_all():

    try:
        db.create_all()
    except Exception as err:
        return str(err), 200
    return 'success!', 200

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=False)
    # app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)


