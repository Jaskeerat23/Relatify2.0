import os
import pymongo
from pymongo import MongoClient
from bson.dbref import DBRef
from dotenv import load_dotenv
from HelperFuncs import getNewId
from HelperFuncs.serializeDoc import serialize_doc
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Successfully connected to database(festsEventsUtils.py)")
except Exception as e:
    print(e)
    exit()

db = client['festdb']

# def serialize_doc(doc):
#     if not isinstance(doc, dict):
#         return doc

#     serialized = {}
#     for k, v in doc.items():
#         if isinstance(v, DBRef):
#             serialized[k] = {"collection": v.collection, "id": v.id}
#         elif isinstance(v, list):
#             serialized[k] = [
#                 {"collection": x.collection, "id": x.id} if isinstance(x, DBRef)
#                 else serialize_doc(x) if isinstance(x, dict)
#                 else x
#                 for x in v
#             ]
#         elif isinstance(v, dict):
#             serialized[k] = serialize_doc(v)
#         else:
#             serialized[k] = v
#     return serialized


def filter_details_for_carousel(festDetails, db = db):
    
    fests = db['Fests']
    
    return {
        "BannerImage" : festDetails.get('BannerImage', ''),
        "FestName" : festDetails.get('FestName', ''),
        "StartDate" : festDetails.get('StartDate', ''),
        "EndDate" : festDetails.get('EndDate', ''),
        "City" : festDetails.get('City', '')
    }

def fetch_fest_user_viewed(viewedFestIds, db = db):
    
    fests = db['Fests']
    
    try:
        
        result = [serialize_doc(x) for x in fests.find({
            "_id" : { "$in" : viewedFestIds }
        })]
        
        if not result:
            return { "status" : "failed", "message" : "Some Error Occured!!" }
        else:
            return { "status" : "success", "message" : "Fests You Viewed Recently", "data" : result }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def fetch_fest_user_city(city, db = db):
    
    fests = db['Fests']
    
    try:
        
        result = [serialize_doc(x) for x in fests.find({
            "City" : { "$eq" : city }
        })]
        
        return { "status" : "success", "message" : "Fests in your city", "data" : result }

    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def fetch_fest_user_fav_genre(favGenres, db = db):
    
    fests = db['Fests']
    
    try:
        
        result = [serialize_doc(x) for x in fests.find({
            "Genres" : { "$in" : favGenres }
        })]
        
        return { "status" : "success", "message" : "Fests You might Like", "data" : result }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def fetch_fest_user_fav_artist(favArtists, db = db):
    
    fests = db['Fests']
    events = db['EventsInFests']
    
    try:
        
        print('fav artists', favArtists)
        
        evtsFavArtist = list(events.find({
            "ArtistsPerforming" : { "$in" : favArtists }
            },
            { "FestId" : 1 }
        ))
        
        print("DBRef fests id of fav artist", evtsFavArtist)
        
        festIds = list({ evt['FestId'].id if isinstance(evt['FestId'], DBRef) else evt['FestId']
                        for evt in evtsFavArtist if 'FestId' in evt })

        print("FestIds of fav artist", festIds)
        
        result = [serialize_doc(x) for x in fests.find({
            "_id" : { "$in" : festIds }
        })]
        
        return { "status" : "success", "message" : "Your Favourites Artist's Fests", "data" : result }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def fetch_events_details(eventIds : list, db = db):
    
    events = db['EventsInFests']
    
    try:
        
        result = [serialize_doc(x) for x in events.find(
            { "_id" : { "$in" : eventIds } }
        )]
        
        if result:
            return { "status" : "success", "message" : "Events Details", "data" : result }
        else:
            return { "status" : "failed", "message" : "No Events found!!" }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def fetch_fest_details(festId, db = db):
    
    collection = db['Fests']
    
    try:
        
        result = serialize_doc(collection.find_one(
            { "_id" : festId }
        ))
        
        if result:
            return { "status" : "success", "message" : "Fest Details", "data" : result }
        else:
            return { "status" : "failed", "message" : "No fest found!!" }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def fetch_fest_events_details(festId, db = db):
    
    fest_details = fetch_fest_details(festId)
    
    if fest_details['status'] != 'success':
        return fest_details
    
    events_details = fetch_events_details(fest_details['data'].get('Events', []))
    
    return { "status" : "success",
            "message" : "Fest and it's Events Details",
            "data" : { 
                "fest_details" : fest_details['data'],
                "events_details" : events_details['data'] 
            } 
        }

def insert_events(eventDetails, festId, session, db = db):
    
    events = db['EventsInFests']
    
    evtCnt = len(eventDetails)
    insertedEvtsIds = []
    
    try:
        for eventDetail in eventDetails:
            
            _id = getNewId.createId(collection = 'EventsInFests', session = session)
            insertedEvtsIds.append(_id)
            
            eventName = eventDetail['EventName']
            festRef = DBRef('Fests', festId)
            artistsPerforming = [DBRef('Artists', artistId) for artistId in eventDetail['ArtistsPerforming']]
            desc = eventDetail['Description']
            eventDate = eventDetail['EventDate']
            stageId = DBRef("Stage", eventDetail['StageId'])    
            crewMembers = [DBRef('CrewMember', crewid) for crewid in eventDetail['crewMembers']]
            startTime = eventDetail['StartTime']
            endTime = eventDetail['EndTime']
            
            events.insert_one({
                "_id" : _id,
                "EventName" : eventName,
                "FestId" : festRef,
                "ArtistsPerforming" : artistsPerforming,
                "Description" : desc,
                "EventDate" : eventDate,
                "StageId" : stageId,
                "Crewmembers" : crewMembers,
                "StartTime" : startTime,
                "EndTime" : endTime
            }, session=session)
        
        return {"status" : "success", "message" : "Inserted Events Successfully", "data" : insertedEvtsIds }
    
    except Exception as e:
    
        return { "status" : "failed", "message" : str(e) }

def insert_fest(
        festName,
        eventsDetails,
        ticketsAva,
        genres,
        description,
        startDate,
        endDate,
        tier,
        facilities,
        city,
        db = db
    ):
    
    fests = db['Fests']
    
    totalAva = 0
    for tiers in tier.items():
        
        totalAva+=tiers[1].get("available", 0)
    
    if totalAva != ticketsAva:
        return { "status" : "failed", "message" : "Tickets Availability is incosistent" }
    
    try:
        
        with client.start_session() as session:
            with session.start_transaction():
                
                newId = getNewId.createId(collection = 'Fests', session = session)
                
                result = insert_events(eventsDetails, newId, session)
    
                if result['status'] == 'failed':
                    raise Exception(result['message'])
                
                insertedEvtsIds = result['data']
                
                fests.insert_one(
                    {
                        "_id" : newId,
                        "FestName" : festName,
                        "Events" : insertedEvtsIds,
                        "TicketsAva" : ticketsAva,
                        "Description" : description,
                        "StartDate" : startDate,
                        "EndDate" : endDate,
                        "Genres" : genres,
                        "City" : city,
                        "Tier" : tier,
                        "Facilities" : facilities
                    }, session=session
                )
                
                return { "status" : "success", "message": "Fest and Event Added Successfully" }
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }