import os
import pymongo
from pymongo import MongoClient
from bson.dbref import DBRef
import datetime
from HelperFuncs import getNewId
from dotenv import load_dotenv
from HelperFuncs.serializeDoc import serialize_doc
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!(jobsUtils.py)")
except Exception as e:
    print("Connection failed:", e)
    exit()

db = client['festdb']

def change_application_status(applicationId, status, db = db):
    
    applications = db['Applications']
    
    try:
        
        result = applications.update_one(
                { "_id" : applicationId },
                { "$set" : { "Status" : status } }
            )
    
        
        if result.modified_count > 0:
            return { "status" : "success", "message" : "Application Status successfully" }
        
        elif result.matched_count == 0:
            return { "status" : "failed", "message" : "Application Not found!!" }
        
        elif result.modified_count == 0:
            return { "status" : "failed", "message" : "Application Status Not Updated!!" }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }
    
def delete_jobs(jobId, orgId, db = db):
    
    if not jobId or not orgId:
        return {"status": "failed", "message": "Invalid Job or Organizer ID"}
    
    jobs = db['Jobs']
    
    try:
        
        result = jobs.delete_one({
            "JobId" : jobId,
            "OrganizerId" : DBRef('Organizers', orgId)
        })
        
        if result.deleted_count > 0:
            return { "status" : "success", "message" : "Job deleted successfully" }
        else:
            return { "status" : "failed", "message" : "You are not Authorized to Delete Record!!" }

    except Exception as e:
        return { "status" : "failed", "message" : str(e) }
    
    
def list_jobs(crewMemDetails, filter = 'City', db = db):
    
    jobs = db['Jobs']
    
    try:
        
        crewMemFilter = crewMemDetails.get(filter, None)
        
        if not crewMemFilter:
            return { "status" : "failed", "message" : "Try Using Other Filter!!" }
        
        result = serialize_doc(list(jobs.find({
            filter : crewMemFilter
        }).sort([('DatePosted', -1)])))
        
        if not result:
            return { "status" : "success", "message" : "No Applications Found", "data" : [] }
        
        else:
            return { "status" : "success",
                    "message" : "Jobs fetched successfully",
                    "data" : result    
                }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def get_user_applications(crewId, sortFilter = 'DatePosted', inc = True, db = db):
    
    application = db['Applications']
    
    try:
        
        sortFilterNum = 1 if inc else -1
        
        result = serialize_doc(list(application.find({
            "CrewId" : { "$eq" : DBRef('CrewMember', crewId) }
        }).sort([(sortFilter, sortFilterNum)])))
        
        if not result:
            return { "status" : "success", "message" : "No Applications Found", "data" : [] }
        
        else:
            return { "status" : "success",
                    "message" : "Applications fetched successfully",
                    "data" : result    
                }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }
        
def post_job_application(applicationDetails, jobId, crewId, db = db):
    
    application = db['Applications']
    
        
    with client.start_session() as session:
        with session.start_transaction():
            try:
            
                newAppId = getNewId.createId(collection = 'Applications', session = session)
                
                result = application.insert_one({
                    "_id" : newAppId,
                    "JobId" : DBRef('Jobs', jobId),
                    "CrewId" : DBRef('CrewMember', crewId),
                    "DatePosted" : datetime.datetime.now(),
                    "Description" : applicationDetails.get('Description', ''),
                    "Status" : "Pending"
                }, session = session)
                
                if not result.inserted_id:
                    return { "status" : "failed", "message" : "Some Error Occured!!" }
                return { "status" : "success", "message" : "Application Posted Successfully" }
        
            except Exception as e:
                return { "status" : "failed", "message" : str(e) }


def get_doc_for_fulltime(jobDetails, newId, orgId):
    
    return {
        "_id" : newId,
        "OrganizerId" : orgId,
        "Title" : jobDetails['Title'],
        "Description" : jobDetails['Description'],
        "JobType" : 'Full-Time',
        "Payment" : jobDetails['Payment'],
        "City" : jobDetails['City'],
        "DatePosted" : datetime.datetime.now(),
        "SkillsRequired" : jobDetails['SkillsRequired']
    }

def get_doc_for_freelance(jobDetails, newId, orgId):
    
    return {
        "_id" : newId,
        "OrganizerId" : orgId,
        "Title" : jobDetails['Title'],
        "Description" : jobDetails['Description'],
        "JobType" : 'Freelance',
        "NumDays" : jobDetails['NumDays'],
        "Payment" : jobDetails['Payment'],
        "City" : jobDetails['City'],
        "DatePosted" : datetime.datetime.now(),
        "SkillsRequired" : jobDetails['SkillsRequired']
    }

def post_job(jobDetails, orgId, db = db):
    
    jobs = db['Jobs']
    # accnts = db['Accounts']
    
    with client.start_session() as session:
        with session.start_transaction():
            try:
                
                newJobId = getNewId.createId(collection = "Jobs", session = session)
                
                # orgIdRef = accnts.find_one(
                #     { "UserName" : userName },
                #     { "Role" : 1 }
                # )['Role']
                
                # orgId = orgIdRef.id if isinstance(orgIdRef, DBRef) else orgIdRef
                
                if jobDetails['JobType'] == 'Freelance':
                    doc = get_doc_for_freelance(jobDetails, newJobId, orgId)
                else:
                    doc = get_doc_for_fulltime(jobDetails, newJobId, orgId)
                
                result = jobs.insert_one(doc, session=session)
                
                if not result.inserted_id:
                    return { "status" : "failed", "message" : "Some Error Occured!!" }
                return { "status" : "success", "message" : "Job Posted Successfully" }
        
            except Exception as e:
                return { "status" : "failed", "message" : str(e) }

