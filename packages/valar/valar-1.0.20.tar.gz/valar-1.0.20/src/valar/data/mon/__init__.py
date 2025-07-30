from bson import ObjectId
from pymongo.results import InsertOneResult

from django.conf import settings
import pymongo

from ..query import Query

from pymongo import MongoClient
from typing import Dict, Any, List, Optional

try:
    MONGO = settings.MONGO_SETTINGS
except AttributeError:
    MONGO = {
        'host': 'localhost',
        'port': 27017,
    }
host, port, username, password = MONGO.get('host'), MONGO.get('port'), MONGO.get('username'), MONGO.get('password')

if username and password:
    uri = f'mongodb://{username}:{password}@{host}:{port}/'
else:
    uri = f'mongodb://{host}:{port}/'
mongo_params = {
    'maxPoolSize': 10,
    'minPoolSize': 0,
    'maxIdleTimeMS': 10000,
    'connectTimeoutMS': 10000,
    'socketTimeoutMS': 10000,
    'serverSelectionTimeoutMS': 10000,
}

def get_mongo_client():
    client = pymongo.MongoClient(uri, **mongo_params)
    client['admin'].command('ping')
    return client



class MongoDao:
    def __init__(self, ref):
        self.ref = ref
        db_name = settings.BASE_APP
        col_name = ref.replace('.', '_')
        self.client = get_mongo_client()
        self.collection = self.client[db_name][col_name]
    def save_one(self, item):
        _id = item.get('id', None)
        _id = None if isinstance(_id, int) else _id
        if _id is None:
            bean:InsertOneResult = self.collection.insert_one(item)
            _id = bean.inserted_id
            self.collection.update_one({'_id': _id}, {'$set': {'sort':str(_id)}})
        else:
            del item['id']
            _id = ObjectId(_id)
            self.collection.update_one({'_id': _id}, {'$set': item})
        return self.collection.find_one({'_id': _id})


    def update_many(self, query, template):
        self.collection.update_many(query.mon_conditions(), {'$set': template})


    def delete_one(self, _id):
        self.collection.delete_one({'_id': ObjectId(_id)})

    def delete_many(self, query):
        self.collection.delete_many(query.mon_conditions())


    def find_one(self, _id):
        return self.collection.find_one({'_id': ObjectId(_id)})

    def find_many(self, query: Query, size=0, page=1) :
        skip = (page - 1) * size
        condition = query.mon_conditions()
        total = self.collection.count_documents(condition)
        cursor = self.collection.find(condition)

        sort_fields = []
        for key, value in query.orders.items():
            sort_direction = pymongo.DESCENDING if value == -1 else pymongo.ASCENDING
            sort_fields.append((key, sort_direction))

        if sort_fields:
            cursor = cursor.sort(sort_fields)
            
        if size:
            cursor = cursor.skip(skip).limit(size)
            
        return cursor, total

    def meta(self):
        one = self.collection.find_one()
        return one

class MongoDBQuery:
    #Mongo的查询
    def __init__(self, connection_string: str, database_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        
    def find(self, collection: str, query: Dict[str, Any], 
             projection: Optional[Dict[str, Any]] = None,
             sort: Optional[List[tuple]] = None,
             limit: Optional[int] = None,
             skip: Optional[int] = None) -> List[Dict[str, Any]]:
        cursor = self.db[collection].find(query, projection)
        if sort:
            cursor = cursor.sort(sort) #好像有警告……但是能跑
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
        
    def count(self, collection: str, query: Dict[str, Any]) -> int:
        return self.db[collection].count_documents(query)
        
    def close(self):
        self.client.close()
