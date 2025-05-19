import re
import datetime
import time
import motor.motor_asyncio
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import DB_NAME, DB_URI

client = MongoClient(DB_URI)
db = client[DB_NAME]
col = db["CaptionSaving"]

async def save_message(caption, file_id, message_id, file_size):
    msg = {
        'msg_id': message_id,
        'file_id': file_id,
        'caption': caption,
        'duration': file_size
    }
    try:
        col.insert_one(msg)
        return True, 1
    except DuplicateKeyError:
        return False, 0

async def get_search_results(query, duration=5, file_type=None, max_results=10, offset=0, filter=False):
    """For given query return (results, next_offset)"""
    
    query = query.strip()
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]') 
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        regex = query
    filter = {'caption': regex}
    files = []
    cursor = col.find(filter).sort('$natural', -1).skip(offset).limit(max_results)
    for file in cursor:
        if duration == 5:
            if file["duration"] <= 300:
                files.append(file)
        else:
            if file["duration"] >= 300:
                files.append(file)
    
    return files
    

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.users = self.db.uersz

    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            plan = False,
            free_used = 0,
            date = None,
            pre_used = 0
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        return self.col.find({})
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def set_plan(self, id, plan):
        await self.col.update_one({'id': int(id)}, {'$set': {'plan': plan}})

    async def get_plan(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user['plan']

    async def set_date(self, id, date):
        await self.col.update_one({'id': int(id)}, {'$set': {'date': date}})

    async def get_date(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user['date']

    async def set_free_used(self, id, free_used):
        await self.col.update_one({'id': int(id)}, {'$set': {'free_used': free_used}})

    async def get_free_used(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user['free_used']

    async def set_pre_used(self, id, pre_used):
        await self.col.update_one({'id': int(id)}, {'$set': {'pre_used': pre_used}})

    async def get_pre_used(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user['pre_used']

    async def get_user(self, user_id):
        user_data = await self.users.find_one({"id": user_id})
        return user_data
        
    async def update_user(self, user_data):
        await self.users.update_one({"id": user_data["id"]}, {"$set": user_data}, upsert=True)

    async def has_premium_access(self, user_id):
        user_data = await self.get_user(user_id)
        if user_data:
            expiry_time = user_data.get("expiry_time")
            if expiry_time is None:
                await self.set_plan(user_id, plan=False)
                return False
            elif isinstance(expiry_time, datetime.datetime) and datetime.datetime.now() <= expiry_time:
                return True
            else:
                await self.set_plan(user_id, plan=False)
                await self.users.update_one({"id": user_id}, {"$set": {"expiry_time": None}})
        return False
        
    async def update_one(self, filter_query, update_data):
        try:
            result = await self.users.update_one(filter_query, update_data)
            return result.matched_count == 1
        except Exception as e:
            print(f"Error updating document: {e}")
            return False

    async def get_expired(self, current_time):
        expired_users = []
        if data := self.users.find({"expiry_time": {"$lt": current_time}}):
            async for user in data:
                expired_users.append(user)
        return expired_users

    async def remove_premium_access(self, user_id):
        return await self.users.update_one(
            {"id": user_id}, {"$set": {"expiry_time": None}}
        )

db = Database(DB_URI, DB_NAME)
