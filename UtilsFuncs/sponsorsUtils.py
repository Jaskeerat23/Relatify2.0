#Left For Future Expansion ;)


import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from serializeDoc import serialize_doc
from fetchAccntDetails import fetch_accnt_details
load_dotenv()

uri = os.getenv("MONGO_URI")

client = MongoClient(uri)

try:
    client.admin.command('ping')
    
    if __name__ == "__main__":
        print("Successfully connected to database")
except Exception as e:
    
    if __name__ == "__main__":
        print(e)
    exit()

db = client['festdb']

def fetch_sponsors_details(userName):
    
    sponsors = db['sponsors']
    
    accntDetails = fetch_accnt_details(userName = userName)
    
    if accntDetails['status'] == 'failed':
        return accntDetails
    
    try:
        
        sponsIdRef = accntDetails['data']['Role']
        sId = sponsIdRef.id
        
        cmDetails = sponsors.find_one({
            "_id" : sId
        })
        
        if not cmDetails:
            return { "status" : "failed", "message" : "Error Fetching Artist!!" }
        else:
            return { "status" : "success",
                    "message" : "Sponsors Details Fetched Successfully",
                    "data" : {
                        "AccountDetails" : serialize_doc(accntDetails['data']),
                        "SponsorsDetails" : serialize_doc(cmDetails)
                    }
                }
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }