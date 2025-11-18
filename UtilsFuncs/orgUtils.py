import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from HelperFuncs.serializeDoc import serialize_doc
from HelperFuncs.fetchAccntDetails import fetch_accnt_details
from bson.dbref import DBRef
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

def filter_org_details_for_role(orgDetails, accntDetails, role):
    
    data = {
        "AccountId" : accntDetails['_id'],
        "UserId" : orgDetails['_id'],
        "ProfilePicture" : accntDetails['ProfilePicture'],
        "UserName" : accntDetails['UserName'],
        "About" : accntDetails['About'],
        "City" : accntDetails['City'],
        "FestsHosted" : orgDetails['FestsHosted']
    }
    
    if role == 'Artists':
        
        data.update({
            "Email" : accntDetails['Email']
        })
    
    elif role == 'Organizers':
        data.update({
            "Email" : accntDetails['Email'],
            "ContactNo" : accntDetails['ContactNo']
        })
    
    return data

def fetch_org_details(orgId, role, db = db):
    
    orgs = db['Organizers']
    accnts = db['Accounts']
    
    try:
        
        accntDetails = serialize_doc( accnts.find_one(
            { "Role" : { "$eq" : DBRef('Organizers', orgId) } }
        ))
        
        
        orgDetails = serialize_doc(orgs.find_one({
            "_id" : orgId
        }))
        
        filtered_data = filter_org_details_for_role(orgDetails, accntDetails, role)
        
        if not orgDetails:
            return { "status" : "failed", "message" : "Error Fetching org!!" }
        else:
            return { "status" : "success",
                    "message" : "org Details Fetched Successfully",
                    "data" : filtered_data
                }
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }