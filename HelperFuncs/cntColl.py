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

prefix_collections = {
    'Accounts' : 'acc',
    'Users' : 'user',
    'Artists' : 'artist',
    'Organizers' : 'org',
    'CrewMember' : 'crew',
    'Fests' : 'fest',
    'EventsInFests' : 'evt',
    'Stage' : 'stage',
    'Tickets' : 'tkt',
    'Sponsors' : 'spon',
    'Jobs' : 'job',
    'Applications' : 'app'
}

def insert_docs(cnts):
    
    collection = db['CountCollections']
    
    for items in prefix_collections.items():
        
        collection.insert_one(
            {
                "CollectionName" : items[0],
                "Counts" : cnts[items[0]],
                "_idPrefix" :items[1]
            }
        )

def get_cnts_of_collections():
    
    cnts = {}
    
    for collections in prefix_collections.keys():
        
        collection = db[collections]
        
        cnt = collection.count_documents({})
        
        print(f"{collections} have {cnt} documents")
        
        cnts.update({collections : cnt})
        
    return cnts

if __name__ == "__main__":
    
    cnts = get_cnts_of_collections()
    insert_docs(cnts)