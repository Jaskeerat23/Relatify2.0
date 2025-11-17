import os
import pymongo
from pymongo import MongoClient
from bson.dbref import DBRef
from dotenv import load_dotenv
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Successfully connected to database")
except Exception as e:
    print(e)
    exit()

db = client['festdb']

def createId(db, collection, session = None):
    
    cntCollection = db['CountCollections']
    
    result = cntCollection.find_one(
        { "CollectionName" : collection }, session = session 
    )
    
    prefix = result['_idPrefix']
    cnt = result['Counts']
    
    newId = prefix + str(cnt + 1)
    
    cntCollection.find_one_and_update(
        { "CollectionName" : collection },
        { "$inc" : { "Counts" : 1 } }, session=session
    )

    return newId
