import time

from ..channels import ValarSocketSender
from ..channels.utils import channel_wrapper
from ..data.utils import get_dao

@channel_wrapper
def save_many_handler(data, sender: ValarSocketSender):
    start_time = time.time()
    entity, array, db = data.get("entity"), data.get("array",[]), data.get("db")
    dao = get_dao(db, entity)
    index, length = 1, len(array)
    for item in array:
        item['saved'] = True
        dao.save_one(item)
        current_time = time.time()
        time_span = current_time - start_time
        if time_span > 1:
            start_time = current_time
            send(index, length, sender)
        index += 1



def send(index, length, sender):
    percentage = round(index * 100 / length)
    tick = {'length': length, 'index': index, 'percentage': percentage}
    sender.to_clients(tick, sender.client)