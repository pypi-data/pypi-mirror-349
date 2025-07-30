from django.db.models import QuerySet
from pymongo.synchronous.cursor import Cursor

from .orm.values import to_dict
from ..data.mon import MongoDao
from ..data.orm import OrmDao






def get_dao(db,entity):
    if db == 'orm':
        return OrmDao(entity)
    elif db == 'mon':
        return MongoDao(entity)
    else:
        raise ValueError('Invalid database %s' % db)

def transform(db, results, code=None):
    if isinstance(results, Cursor):
        return [to_item(db, bean) for bean in results]
    elif isinstance(results, QuerySet):
        return to_dict(results, code)
    else:
        return to_item(db, results)

def to_item(db, bean):
    if db == 'orm':
        return bean.full
    elif db == 'mon':
        bean['id'] = str(bean['_id'])
        del bean['_id']
        return bean


def array2tree(data, mapping):
    mapping = mapping or {}
    lookup = {}
    for array in data:
        for i in range(len(array)):
            key = '/'.join(array[0:i+1])
            item = mapping.get(key, {})
            value = item.get('value', array[i])
            label = item.get('label', value)
            display = item.get('display')
            item = lookup.get(key, {'value': value,'label':label,'display':display})
            if i < len(array) -1:
                item['children'] = item.get('children', [])
            lookup[key] = item
            if i > 0:
                parent =   '/'.join(array[0:i])
                lookup[parent]['children'].append(lookup[key])
    return [lookup[root] for root in [*set([array[0] for array in data])]]



    # for parent, child in data:
    #     if parent not in lookup:
    #         lookup[parent] = {'label': parent, 'value':parent, 'children': []}
    #     if child not in lookup:
    #         lookup[child] = {'label': child, 'value':child, 'children': []}
    #     lookup[parent]['children'].append(lookup[child])
    # children_set = {child for _, child in data}
    # root_nodes = [node for name, node in lookup.items() if name not in children_set]
    # return root_nodes



