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
    
    if __name__ == "__main__":
        print("Successfully connected to database")
except Exception as e:
    
    if __name__ == "__main__":
        print(e)
    exit()

db = client['festdb']

def filter_cm_details_for_role(accntDetails, userDetails, role):
    
    data = {
        "AccountId" : accntDetails['_id'],
        "UserId" : userDetails['_id'],
        "ProfilePicture" : accntDetails['ProfilePicture'],
        "UserName" : accntDetails['UserName'],
        "Name" : userDetails['Name'],
        "Description" : accntDetails.get('Description', ""),
        "Experience" : userDetails.get("Experience", ""),
        "City" : userDetails.get("City", ""),
        "Email" : userDetails.get("Email", ""),
        "Contact" : userDetails.get("ContactNo", [])
    }
    
    return data

def fetch_cm_details(userId, role, db = db):
    
    accnts = db['Accounts']
    crewMember = db['CrewMember']
    
    try:
        
        accntDetails = serialize_doc(accnts.find_one({
            "Role" : DBRef('CrewMember', userId)
        }))
        
        if not accntDetails:
            return { "status" : "failed", "message" : "Invalid Account!!" }
        
        userDetails = serialize_doc(crewMember.find_one({
            "_id" : userId
        }))
        
        if not userDetails:
            return { "status" : "failed", "message" : "Invalid User" }
        
        filteredInfo = filter_cm_details_for_role(accntDetails, userDetails, role)
        
        return { "status" : "success", "message" : "CreeMember details Fetched Successfully", "data" : filteredInfo }

    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

# def fetch_cm_details(userName):
    
#     crewMember = db['CrewMember']
    
#     accntDetails = fetch_accnt_details(userName = userName)
    
#     if accntDetails['status'] == 'failed':
#         return accntDetails
    
#     try:
        
#         cmIdRef = accntDetails['data']['Role']
#         cmId = cmIdRef.id
        
#         cmDetails = crewMember.find_one({
#             "_id" : cmId
#         })
        
#         if not cmDetails:
#             return { "status" : "failed", "message" : "Error Fetching Artist!!" }
#         else:
#             return { "status" : "success",
#                     "message" : "CrewMember Details Fetched Successfully",
#                     "data" : {
#                         "AccountDetails" : serialize_doc(accntDetails['data']),
#                         "CrewMemberDetails" : serialize_doc(cmDetails)
#                     }
#                 }
#     except Exception as e:
#         return { "status" : "failed", "message" : str(e) }