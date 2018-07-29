import threading

from database_services.database_objects.item import Item
from database_services.database_objects.price import Price
from web_data_services.item_services.get_item_from_id import get_item_from_id, get_item_from_id_thread


def add_item_to_database_by_id_thread(id: int, session_lock: threading.Lock, get_lock: threading.Lock):
    print(threading.get_ident())
    item = Item()
    thread = threading.Thread(target=get_item_from_id_thread, args=(id, item, get_lock))
    thread.start()
    thread.join()
    # get_item_from_id(id, lock=get_lock)
    thread = threading.Thread(target=item.add_to_database_thread, args=(session_lock,))
    thread.start()
    thread.join()


if __name__ == '__main__':
    pass
