from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

'''
Some models are presented here!
'''

class Order(db.Model):

    uuid = db.Column(db.String(32), unique=True, nullable=False, primary_key=True, default = uuid.uuid4().hex)
    client_name = db.Column(db.String(120), nullable=False)
    status_of_order = db.Column(db.Boolean, nullable=False)
    date_of_getting = db.Column(db.String(40), nullable=False)
    order_number = db.Column(db.Integer, nullable=False)

    def get_warehouse_statuses(self):

        return WarehousesStatus.find_all_statuses_by_order(self.uuid)

    def find_order_by_uuid(self):

        return self.query.filter_by(uuid = self.uuid)

    def get_updated_data(self):
        
        updated_data = {
                "client_name": self.client_name,
                "status_of_order": self.status_of_order,
                "date_of_getting": self.date_of_getting,
                "order_number": self.order_number
                }

        return updated_data

    def save(self):

        order = self.find_order_by_uuid()
        if order.first():
            order.update(self.get_updated_data())
            db.session.commit()
        else:
            db.session.add(self)
            db.session.commit()

class WarehousesStatus(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    order_uuid = db.Column(db.String(32), db.ForeignKey('order.uuid')) # one to many
    warehouse_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    @staticmethod
    def find_all_statuses_by_order(order_uuid):
        return WarehousesStatus.query.filter_by(order_uuid = order_uuid).all()

    @staticmethod
    def delete_previous_data(order_uuid):

        warehousestatuses = WarehousesStatus.find_all_statuses_by_order(order_uuid)
        for element in warehousestatuses:
            db.session.delete(element)
        db.session.commit()
        
    def save(self):

        db.session.add(self)
        db.session.commit()
    
if __name__ == "__main__":
    
    pass