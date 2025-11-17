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

def filter_artist_details_for_role(artistDetails, accntDetails, role):
    # Always visible
    data = {
        "AccountId": accntDetails["_id"],
        "UserId": artistDetails["_id"],
        "StageName" : artistDetails['StageName'],
        "Name": artistDetails["Name"],
        "Genre": artistDetails["Genre"],
        "ProfilePicture": accntDetails["ProfilePicture"],
        "Followers": artistDetails["Followers"],
        "Description": accntDetails.get("Description", "")
    }

    if role == "organizer":
        data.update({
            "Contact": accntDetails.get("Contact"),
            "PerformanceHistory": artistDetails.get("PerformanceHistory"),
            "Fee": artistDetails.get("Fee")
        })

    elif role == "artist":  # maybe show stats or own analytics
        data.update({
            "Bookings": artistDetails.get("Bookings"),
            "Revenue": artistDetails.get("Revenue")
        })

    # Regular user sees only public info
    return data


def fetch_artists_carousel_details(limit = 10, db = db):
    
    artists = db['Artists']
    
    try:
    
        result = artists.aggregate(
            { "$sample" : { "size" : limit } },
            { "$project" : { "_id" : 1, "Name" : 1, "Followers" : 1, "ProfilePicture" : 1 } }
        )
        
        serialized = [ serialize_doc(x) for x in result]
        
        if not result:
            return { "status" : "failed", "message" : "Error Fetching Artist!!" }
        else:
            return { "status" : "success", "message" : "Artist Info Fetched Successfully", "data" : result }
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def fetch_artist_details(artistId, role, db = db):
    
    artists = db['Artists']
    accnts = db['Accounts']
    
    try:
        
        accntDetails = serialize_doc( accnts.find_one(
            { "Role" : { "$eq" : DBRef('Artists', artistId) } }
        ))
        
        
        artistDetails = serialize_doc(artists.find_one({
            "_id" : artistId
        }))
        
        filtered_data = filter_artist_details_for_role(artistDetails, accntDetails, role)
        
        if not artistDetails:
            return { "status" : "failed", "message" : "Error Fetching Artist!!" }
        else:
            return { "status" : "success",
                    "message" : "Artist Details Fetched Successfully",
                    "data" : filtered_data
                }
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }