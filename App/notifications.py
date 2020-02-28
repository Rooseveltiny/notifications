import time

STATIC_DATA = {
  "client": "Иванов Иван Иванович",
  "order_number": 1234,
  "status_of_order": "Готов",
  "date_of_getting": "12.12.2020 16:00:00",
"warehouses_status": [
{"1": "ready"},
{"2": "not ready"},
{"3": "ready"}
]
}

class Notification(object):

    client              = None # string
    status_of_order     = None # string
    date_of_getting     = None # time
    order_number        = None # int
    warehouses_status   = None # structure

    def save_to_db(self, json_data):

        print(json_data)

    # this method allows to add notification to ligth SQL data base

    def find_notification(self, special_uuid):

        pass

    # this method allows to find existing notification in database

if __name__ == "__main__":
    
    notification = Notification()
    notification.save_to_db(STATIC_DATA)

