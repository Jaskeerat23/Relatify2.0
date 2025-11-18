import os
import pymongo
from pymongo import MongoClient
from bson.dbref import DBRef
import datetime
from dotenv import load_dotenv
from HelperFuncs.serializeDoc import serialize_doc
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print("Connection failed:", e)
    exit()

db = client['festdb']

def fetch_user_details(userId, db = db):
    
    collection = db['Accounts']
    
    accountDetails = collection.find_one({ "_id" : userId })
    
    if __name__ == "__main__":
        
        print(accountDetails)
    
    if accountDetails == None:
        return { "status" : "failed", "message" : "User Not Found!!" } # returned when user with provided userName is not found
    
    ref = accountDetails['Role']
    
    collection = db['Users']
    
    userDetails = db[ref.collection].find_one({ "_id" : ref.id })
    
    # favArtists = userDetails['favArtist']
    # flagFests = userDetails['FlagFests']
    # bookedTickets = userDetails['FestsTickets']
    # gender = userDetails['Gender']
    # email = accountDetails['Email']
    # contact = accountDetails['ContactNo']
    # city = accountDetails['City']
    
    return serialize_doc({
            "status" : "success",
            "message" : "User Details fetched successfully",
            "data" : { 
                "Accountid" : accountDetails['_id'],
                "UserId" : userDetails['_id'],
                "UserName" : accountDetails['UserName'],
                "Name" : userDetails['Name'],
                "favArtist" : userDetails['favArtist'],
                "FavGenre" : userDetails['FavGenre'],
                "FlagFests" : userDetails['FlagFests'],
                "FestsViewed" : userDetails['FestsViewed'],
                "ArtistViewed" : userDetails['ArtistViewed'],
                "FestTickets" : userDetails['FestsTickets'],
                "Gender" : userDetails['Gender'],
                "Email" : accountDetails['Email'],
                "Contact" : accountDetails['ContactNo'],
                "City" : accountDetails['City']
                }
            })

def update_email(accntId, password, newEmail, db = db):
    
    activeTrans = db['ActiveTransactions']
    accnts = db['Accounts']
    
    result = activeTrans.find_one({ "_id" : accntId, "Operation" : "update_email" })

    if result:
        return { "status" : "failed", "message" : "Unable To Update Account Information" }
    
    try:
        
        activeTrans.insert_one({
            "_id" : accntId,
            "Operation" : "update_email",
            "Time" : datetime.datetime.now()
        })
        
        accntSearchRes = accnts.find_one(
            { "_id" : accntId },
            { "Password" : 1 }
        )
        
        if not accntSearchRes:
            return { "status" : "failed", "message" : "Invalid Account!!" }
        
        if password == accntSearchRes['Password']:
            
            result = accnts.update_one(
                { "_id" : accntId },
                { "$set" : { "Email" : newEmail } }
            )
            
            if result.modified_count == 0:
                return { "status" : "failed", "message" : "Unable to change Information!!" }
            else:
                return { "status" : "success", "message" : "Email updated successfully" }
        
        else:
            return { "status" : "failed", "message" : "Wrong Password" }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

    finally:
        activeTrans.delete_one({ "_id" : accntId, "Operation" : "update_email" })

def update_city(accntId, password, newCity, db = db):
    
    activeTrans = db['ActiveTransactions']
    accnts = db['Accounts']
    
    result = activeTrans.find_one({ "_id" : accntId, "Operation" : "update_city" })

    if result:
        return { "status" : "failed", "message" : "Unable To Update Account Information" }
    
    try:
        
        activeTrans.insert_one({
            "_id" : accntId,
            "Operation" : "update_city",
            "Time" : datetime.datetime.now()
        })
        
        accntSearchRes = accnts.find_one(
            { "_id" : accntId },
            { "Password" : 1 }
        )
        
        if not accntSearchRes:
            return { "status" : "failed", "message" : "Invalid Account!!" }
        
        if password == accntSearchRes['Password']:
            
            result = accnts.update_one(
                { "_id" : accntId },
                { "$set" : { "City" : newCity } }
            )
            
            if result.modified_count == 0:
                return { "status" : "failed", "message" : "Unable to change Information!!" }
            else:
                return { "status" : "success", "message" : "City updated successfully" }
        
        else:
            return { "status" : "failed", "message" : "Wrong Password" }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

    finally:
        activeTrans.delete_one({ "_id" : accntId, "Operation" : "update_city" })
    
def update_username(accntId, userName, newUserName, password, db = db):
    
    activeTrans = db['ActiveTransactions']
    accnts = db['Accounts']
    
    result = activeTrans.find_one({ "_id" : accntId })
    
    if result:
        return { "status" : "failed", "message" : "Username already in progress" }
    try:
        activeTrans.insert_one({
            "_id" : accntId,
            "Operation" : "update_username",
            "Time" : datetime.datetime.now()
        })
        
        accntSearchRes = accnts.find_one({ "_id" : accntId })
        
        if password == accntSearchRes['Password']:
            
            result = accnts.update_one(
                { "_id" : accntId },
                { "$set" : { "UserName" : newUserName } },
            )
            
            if result.modified_count == 0:
                return { "status": "failed", "message": "Username was not updated." }
            
            return { "status" : "success", "message" : "UserName updated successfully" }
        
        else:
            return { "status" : "failed", "message" : "Incorrect Password" }
    
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }
    
    finally:
        activeTrans.delete_one({ "_id" : accntId })

def flag_fest(userId, festId, db = db):
    
    '''We are not performing checks for unavailability of fest or user
    since this function is only called when we will have user id as well as
    fest id, so if any of them is missing it will be handled by fetch_fest_details for fests
    and by fetch_user_details for users'''
    
    users = db['Users']
    
    result = users.update_one(
        { "_id" : userId },
        { "$addToSet" : { "FlagFests" : festId } }
    )
    
    return { "status" : "success", "message" : "fest flagged" }

def unflag_fest(userId, festId, db = db):
    
    '''Unlike flag_fest function we will have to perform
    some checks here'''
    
    users = db['Users']
    
    result = users.find_one(
        { "_id" : userId, "FlagFests" : { "$elemMatch" : { "$eq" : festId } } },
        { "_id" : 1 }
    )
    
    if not result:
        return { "status" : "failed", "message" : "The Fest is not Flagged" }
    
    try:
        
        result = users.update_one(
            { "_id" : userId },
            { "$pull" : { "FlagFests" : festId } }
        )
        
        if result.modified_count > 0:
            return { "status" : "success", "message" : "The fest is successfully unflagged" }
        
        else:
            return { "status" : "failed", "message" : "Some Error occured please try again later...." }
        
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def mark_artist_fav(userId, artistId, db = db):
    
    # accounts = db['Accounts']
    users = db['Users']
    
    # artistRes = accounts.find_one({ "UserName" : artistUserName }, { "Role" : 1 })
    
    # if not artistRes:
    #     return { "status" : "failed", "message" : "Artist not found!!" }
    
    # artistIdRef = artistRes['Role']
    
    # collection = artistIdRef.collection
    # artistId = artistIdRef.id
    
    try:
        result = users.update_one(
            { "_id" : userId },
            { "$addToSet" : { "favArtist" : artistId} }
        )
        
        if result.modified_count > 0:
            return { "status" : "success", "message" : "Artist Successfully added to favorites" }
        else:
            return { "status" : "failed", "message" : "Some Error Occured occured tru again later...." }
    
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def remove_artist_fav(userId, artistId, db = db):
    
    # accounts = db['Accounts']
    users = db['Users']
    
    # artistRes = accounts.find_one({ "UserName" : artistUserName }, { "Role" : 1 })
    
    # if not artistRes:
    #     return { "status" : "failed", "message" : "Artist not found!!" }
    
    # artistIdRef = artistRes['Role']
    
    # collection = artistIdRef.collection
    # artistId = artistIdRef.id
    
    try:
        
        result = users.update_one(
            { "_id" : userId },
            { "$pull" : { "favArtist" : artistId } }
        )
        
        if result.modified_count > 0:
            return { "status" : "success", "message" : "Artist Successfully removed from favorites" }
        else:
            return { "status" : "failed", "message" : "Some Error Occured occured tru again later...." }
    
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }

def get_fav_artists(userId, db = db):
    
    users = db['Users']
    
    try:
        result = serialize_doc(users.find_one({ "_id" : userId }, { "favArtist" : 1, "_id" : 0 }))
        
        if not result:
            return { "status": "failed", "message": "User not found" }
        
        favArtist = result.get("favArtist", [])
        
        if not favArtist:
            return { "status" : "failed", "message" : "You have no Artist in Fav-List" }
        else:
            return { "status" : "success", "message" : "Artists Fetched Successfully", "data" : result }
        
    
    except Exception as e:
        return { "status" : "failed", "message" : str(e) }
    
if __name__ == "__main__":
    
    print(f"Testing Function fetch_user_details()")
    
    res = fetch_user_details(userId = 'acc1')
    
    for items in res['data'].items():
        
        print(items)
    
    print(f"\n1/9 Passed\n")
    
    print(f"Testing Function update_email()")
    
    res = update_email(accntId = 'acc1', password = 'pass123', newEmail = 'jas236@gmail.com')
    
    if res['status'] == 'failed':
        print(res['message'])
        raise 'Error'
        exit()
    
    print(f"\n2/9 Passed\n")
    
    print(f"Testing Function update_city()")
    
    res = update_city(accntId = 'acc1', password = 'pass123', newCity = 'Dehradun')
    
    if res['status'] == 'failed':
        print(res['message'])
        raise 'Error'
        exit()
    
    print(f"\n3/9 Passed\n")
    
    print("Testing Function update_username()")
    
    res = update_username(accntId = 'acc1', userName = 'user_1', newUserName = 'Jas_23', password = 'pass123')
    
    if res['status'] == 'failed':
        print(res['message'])
        raise 'Error'
        exit()
    
    print(f"\n4/9 Passed\n")
    
    print(f"Testing Function flag_fest()")
    
    res = flag_fest(userId = 'user1', festId = 'fest1')
    
    if res['status'] == 'failed':
        print(res['message'])
        raise 'Error'
        exit()
    
    print(f"\n5/9 Passed\n") 
    
    print(f"Testing Function unflag_fest()")
    
    res = unflag_fest(userId = 'user1', festId = 'fest2')
    
    if res['status'] == 'failed':
        print(res['message'])
        raise 'Error'
        exit()
    
    print(f"\n6/9 Passed\n")
    
    print(f"Testing Function mark_artist_fav()")
    
    res = mark_artist_fav(userId = 'user1', artistUserName = 'artist_3')
    
    if res['status'] == 'failed':
        print(res['message'])
        raise 'Error'
        exit()
    
    print(f"\n7/9 Passed\n")
    
    print(f"Testing Function remove_artist_fav()")
    
    res = remove_artist_fav(userId = 'user1', artistUserName = 'artist_24')
    
    if res['status'] == 'failed':
        print(res['message'])
        raise 'Error'
        exit()
    
    print(f"\n8/9 Passed\n")
    
    print(f"Testing Function get_fav_artists()")
    
    res = get_fav_artists(userId = 'user1')
    
    if res['status'] == 'failed':
        print(res['message'])
        raise 'Error'
        exit()
        
    
    for items in res['data'].items:
        print(items)
    
    print(f"\n9/9 Passed\n")