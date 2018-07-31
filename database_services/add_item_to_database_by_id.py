import threading

from database_services.database_objects.item import Item
from database_services.database_objects.price import Price
from web_data_services.item_services.get_item_from_id import get_item_from_id_thread


def add_item_to_database_by_id_thread(id: int, session_lock: threading.Lock, get_lock: threading.Lock):
    # print(threading.get_ident())
    item = Item()
    get_item_from_id_thread(id, item, get_lock, second_delay=20)
    item.add_to_database_thread(session_lock)


if __name__ == '__main__':
    pass
