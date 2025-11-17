#This file is depreceated and is not being used in the project but is kept 
#for future potentiel use

import os
import pymongo
from pymongo import MongoClient
from serializeDoc import serialize_doc
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

def fetch_accnt_details(userName):
    
    accnts = db['Accounts']
    
    try:
        
        result = accnts.find_one(
            { "UserName" : { "$eq" : userName } },
            { "UserName" : 1, "ContactNo" : 1, "Email" : 1 })
        
        if not result:
            return { "status" : "failed", "message" : "No user found!!" }
        
        else:
            return { "status" : "success", "message" : "Account Info Fetched Successfully", "data" : result }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }