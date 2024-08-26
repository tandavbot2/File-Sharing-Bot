# (©)CodexBotz

import pymongo
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']
settings_data = database['settings']

async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})

async def full_userbase():
    user_docs = user_data.find()
    user_ids = [doc['_id'] for doc in user_docs]
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})

async def set_auto_delete(enabled: bool):
    settings_data.update_one(
        {'_id': 'auto_delete'},
        {'$set': {'enabled': enabled}},
        upsert=True
    )

async def get_auto_delete_status():
    setting = settings_data.find_one({'_id': 'auto_delete'})
    return setting['enabled'] if setting else False
