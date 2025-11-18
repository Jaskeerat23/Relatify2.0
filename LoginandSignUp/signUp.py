import os
import pymongo
from pymongo import MongoClient
from bson.dbref import DBRef
from dotenv import load_dotenv
from HelperFuncs import getNewId
load_dotenv()

uri = os.getenv("MONGO_URI")

client = MongoClient(uri)

try:
    client.admin.command('ping')
    if __name__ == "__main__":
        print("Successfully connected to the Database")
except Exception as e:
    if __name__ == "__main__":
        print(e)

db = client['festdb']

def insert_sponsor_data(sponsorDetails : dict, newRoleId, session=None):
    
    sponsors = db['Sponsors']
    
    sponsorName = sponsorDetails['SponsorName']
    
    try:
        
        result = sponsors.insert_one({
            "_id" : newRoleId,
            "Name" : sponsorName,
            "AmountContributed" : 0,
            "Sponsored" : []
        }, session=session)
        
        if result:
            return { "status" : "success", "message" : "Sponsor Registered Successfully!!" }

        else:
            return { "status" : "failed", "message" : "Some Error Occured!!" }
    
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def insert_artist_data(artistDetails : dict, newRoleId, session=None):
    
    artist = db['Artists']
    
    name = artistDetails['Name']
    stageName = artistDetails['StageName']
    contractFee = artistDetails['ContractFee']
    genre = artistDetails['Genre']
    
    try:
        
        result = artist.insert_one({
            "_id" : newRoleId,
            "Name" : name,
            "StageName" : stageName,
            "ContractFee" : contractFee,
            "Genre" : genre
        }, session=session)
        
        if result:
            return { "status" : "success", "message" : "Artist Inserted Successfully!!" }

        else:
            return { "status" : "failed", "message" : "Some Error Occured!!" }
    
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }


def insert_crew_data(crewMemDetails : dict, newRoleId, session=None):
    
    crewMem = db['CrewMember']
    
    name = crewMemDetails['Name']
    gender = crewMemDetails['Gender']
    
    try:
        
        result = crewMem.insert_one({
            "_id" : newRoleId,
            "Name" : name,
            "DOJ" : None,
            "Organization" : None,
            "Gender" : gender,
            "Role" : None
        }, session=session)
        
        if result:
            return { "status" : "success", "message" : "CrewMember Inserted Successfully!!" }

        else:
            return { "status" : "failed", "message" : "Some Error Occured!!" }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def insert_org_data(orgDetails : dict, newRoleId, session=None):
    
    org = db['Organizers']
    
    orgName = orgDetails['OrgName']
    
    try:
        
        result = org.insert_one({
            "_id" : newRoleId,
            "OrgName" : orgName,
            "FestsHosted" : []
        }, session=session)
        
        if result:
            return { "status" : "success", "message" : "Organization Registered Successfully!!" }

        else:
            return { "status" : "failed", "message" : "Some Error Occured!!" }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def insert_user_data(userDetails : dict, newRoleId, session=None):
    
    users = db['Users']
    
    name = userDetails['Name']
    dob = userDetails['DOB']
    gender = userDetails['Gender']
    
    try:

        result = users.insert_one({
            "_id" : newRoleId,
            "Name" : name,
            "FavArtist" : [],
            "FlagFests" : [],
            "FestsTickets": [],
            "ArtistsViewed" : [],
            "FestsViewed" : [],
            "DOB" : dob,
            "Gender" : gender
        }, session=session)
        
        if result:
            return { "status" : "success", "message" : "User Inserted Successfully!!" }

        else:
            return { "status" : "failed", "message" : "Some Error Occured!!" }
    
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def singup_user(accountDetails : dict, roleDetails : dict, db = db):
    
    
    '''In prototyping phase we are not going to hash
    the password of the account'''
    
    userName = accountDetails['UserName']
    password = accountDetails['Password']
    contactNo = accountDetails['ContactNo']
    email = accountDetails['Email']
    city = accountDetails['City']
    role = accountDetails['Role']
    
    try:
        with client.start_session() as session:
            with session.start_transaction():
            
                accounts = db['Accounts']
                roleCollection = db[role]
                
                newAccId = getNewId.createId(db =db, collection = 'Accounts', session=session)
                newRoleId = getNewId.createId(db = db, collection = role, session=session)
                
                if role == "Users":
                    inserted = insert_user_data(roleDetails, newRoleId, session=session)
                elif role == "Artists":
                    inserted = insert_artist_data(roleDetails, newRoleId, session=session)
                elif role == "Organizers":
                    inserted = insert_org_data(roleDetails, newRoleId, session=session)
                elif role == "CrewMember":
                    inserted = insert_crew_data(roleDetails, newRoleId, session=session)
                elif role == "Sponsors":
                    inserted = insert_sponsor_data(roleDetails, newRoleId, session=session)
                    
                if inserted['status'] == "failed":
                    return inserted
                
                accounts.insert_one({
                    "_id" : newAccId,
                    "UserName" : userName,
                    "Password" : password,
                    "ContactNo" : contactNo,
                    "Email" : email,
                    "City" : city,
                    "Role" : DBRef(role, newRoleId)
                }, session=session)
                
                session.commit_transaction()
                    
                return { "status" : "success", "message": "Account Successfully Registered" }
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

if __name__ == "__main__":
    
    accntDetails = {
        "UserName" : "Jaskeerat23006",
        "Password" : "hashPass",
        "ContactNo" : [ "1234567890", "1234567890" ],
        "Email" : "jaskeerat@gmail.com",
        "City" : "Dehradun",
        "Role" : "Users"
    }
    
    roleDetails = {
        "Name" : { "Fname" : "Jaskeerat", "Mname" : "", "Lname" : "Singh" },
        "DOB" : '2006/01/23',
        "Gender" : "Male"
    }
    
    print(singup_user(accountDetails = accntDetails, roleDetails = roleDetails))