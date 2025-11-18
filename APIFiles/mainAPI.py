''''''

# import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fastapi
from pydantic import BaseModel
from typing import Any, List, Dict
from pymongo import MongoClient
from dotenv import load_dotenv

from LoginandSignUp import login
from LoginandSignUp import signUp
# from LoginandSignUp import login, signUp
from UtilsFuncs import (
    usersUtils,
    festsEventsUtils,
    artistUtils,
    orgUtils,
    crewMemUtils,
    jobsUtils
)

from APIFiles.apiData import (
    LoginData,
    SignUpData,
    updateUserName,
    updateEmail,
    updateCity,
    FestId,
    ArtistId,
    FestDetails,
    PostJob,
    ApplicationDetails,
    ApplicationStatus
)

from fastapi.middleware.cors import CORSMiddleware

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
app = fastapi.FastAPI()
app.state.active_user = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

'''Basic Login, SignUp and User Functions'''

def fetch_details_(userId, role):
    
    details = {}
    
    if role == "Users":
        
        details = usersUtils.fetch_user_details(userId = userId, db = db)
    
    elif role == "Organizers":
        
        details = orgUtils.fetch_org_details(userId = userId, role = 'Organizers', db = db)
    
    elif role == 'Artists':
        
        details = artistUtils.fetch_artist_details(artistId = userId, role = 'Artists', db = db)
    
    elif role == 'CrewMember':
        
        details = crewMemUtils.fetch_cm_details(userId = userId, role = 'CrewMember', db = db)
    
    if details['status'] != 'success':
        return details
    
    return { 'status' : 'success', 'message' : 'Details fetched successfully', 'data' : details }

@app.post("/login")
def login_(data: LoginData):
    
    '''This function is used to handle API call for login in user and this 
    function also serves to fetch user(Users, Organizers, CrewMember, Artists)
    details, so that these details can be stored and be used in future'''
    
    res = login.login_user(data.username, True, data.password)
    
    
    if res['status'] != 'success':
        print(res)
        return res
    
    loginData = res['data']
    
    print("Login data is", loginData)
    
    details = {}
    
    if loginData.get('Collection', '') == "Users":
        
        details = usersUtils.fetch_user_details(userId = loginData['AccountId'], db = db)
    
    elif loginData.get('Collection', '') == "Organizers":
        
        details = orgUtils.fetch_org_details(orgId = loginData['UserId'], role = 'Organizers', db = db)
    
    elif loginData.get('Collection', '') == 'Artists':
        
        details = artistUtils.fetch_artist_details(artistId = loginData['UserId'], role = 'Artists', db = db)
    
    elif loginData.get('Collection', '') == 'CrewMember':
        
        details = crewMemUtils.fetch_cm_details(userId = loginData['UserId'], role = 'CrewMember', db = db)
    
    print("details", details)
    if details['status'] != 'success':
        return details
    
    print(details)
    
    app.state.active_user = details['data']
    print("app.state.active_user : ", app.state.active_user)
    
    if 'Role' not in list(app.state.active_user.keys()):
        app.state.active_user.update({ 'Role' : loginData.get('Collection', '') })
    
    return { 'status' : res['status'], 'message' : res['message'], 'data' : app.state.active_user }

@app.post("/signup_user")
def signup_user_(data: SignUpData):
    
    '''This function Handles API calls for signing up user, The
    user can be any one a normal user, artist, organizer, crewmember,
    even in future expansions we are planning to add sponsors
    as users. The data for each user may differ but common details :
    
        UserName
        Password
        Email
        ContactNo
        Role
        City

    These all be same, so we have a seperate collection called Accounts to 
    handle this information and beside it for role specific information we
    have different collections
    '''
    
    res = signUp.singup_user(accountDetails = data.accntDetails,
                            roleDetails = data.roleDetails)
    
    return res

@app.put("/update_username")
def update_username_(data: updateUserName):
    
    '''This function handles API calls for updating username'''
    print(app.state.active_user)
    if not app.state.active_user or 'AccountId' not in app.state.active_user:
        return { 'status' : 'failed', 'message' : 'Not Logged In' }
    
    res = usersUtils.update_username(accntId = app.state.active_user['AccountId'],
                                    userName = app.state.active_user['UserName'],
                                    newUserName = data.newUserName,
                                    password = data.password)
    
    if res['status'] == 'failed':
        return res
    
    app.state.active_user['UserName'] = data.newUserName
    
    # fetch_details_(userId = app.state.active_user['UserId'], role = app.state.active_user['Role'])
    
    res['data'] = app.state.active_user
    
    return res

@app.put("/update_email")
def update_email_(data: updateEmail):
    
    '''This function handles API calls for updating user email'''

    if not app.state.active_user or 'AccountId' not in app.state.active_user:
        return { 'status' : 'failed', 'message' : 'Not Logged In' }
    
    res = usersUtils.update_email(accntId = app.state.active_user['AccountId'],
                                password = data.password,
                                newEmail = data.newEmail,
                                db = db)
    
    if res['status'] == 'failed':
        return res
    
    app.state.active_user['Email'] = data.newEmail
    
    # fetch_details_(userId = app.state.active_user['UserId'], role = app.state.active_user['Role'])
    
    res.update({ "data": app.state.active_user })
    return res

@app.put("/update_city")
def update_city_(data: updateCity):
    
    '''This function handles API calls for updating user city'''

    if not app.state.active_user or 'AccountId' not in app.state.active_user:
        return { 'status' : 'failed', 'message' : 'Not Logged In' }
    
    res = usersUtils.update_city(accntId = app.state.active_user['AccountId'],
                                    password = data.password,
                                    newCity = data.newCity,
                                    db = db)
    
    if res['status'] == 'failed':
        return res
    
    app.state.active_user['City'] = data.newCity
    
    # fetch_details_(userId = app.state.active_user['UserId'], role = app.state.active_user['Role'])
    
    res.update({ "data": app.state.active_user })
    return res

@app.post("/flag_fest")
def flag_fest_(data: FestId):
    
    if app.state.active_user.get('Role') != 'Users':
        return { 'status' : 'failed', 'message' : 'You are not authorized for this Operation!!' }
    
    res = usersUtils.flag_fest(userId = app.state.active_user['UserId'], festId = data.festId, db = db)
    
    if res['status'] == 'success':
        app.state.active_user['FlagFests'].append(data.festId)
    
    return res

@app.put("/unflag_fest")
def unflag_fest_(data: FestId):
    
    if app.state.active_user.get('Role') != 'Users':
        return { 'status' : 'failed', 'message' : 'You are not authorized for this Operation!!' }
    
    res = usersUtils.unflag_fest(userId = app.state.active_user['UserId'], festId = data.festId, db = db)
    
    if res['status'] == 'success' and data.festId in app.state.active_user['FlagFests']:
        app.state.active_user['FlagFests'].remove(data.festId)
    
    return res

@app.post("/mark_artist_fav")
def mark_artist_fav_(data: ArtistId):
    
    if app.state.active_user.get('Role') != 'Users':
        return { 'status' : 'failed', 'message' : 'You are not authorized for this Operation!!' }
    
    res = usersUtils.mark_artist_fav(userId = app.state.active_user['UserId'], artistId = data.artistId, db = db)
    
    if res['status'] == 'success':
        app.state.active_user['favArtist'].append(data.artistId)
    
    return res

@app.put("/remove_artist_fav")
def remove_artist_fav_(data: ArtistId):
    
    if app.state.active_user.get('Role') != 'Users':
        return { 'status' : 'failed', 'message' : 'You are not authorized for this Operation!!' }
    
    res = usersUtils.remove_artist_fav(userId = app.state.active_user['UserId'], artistId = data.artistId, db = db)
    
    if res['status'] == 'success' and data.artistId in app.state.active_user['favArtist']:
        app.state.active_user['favArtist'].remove(data.artistId)
    
    return res

@app.get("/get_fav_artists")
def get_fav_artists_():
    
    res = usersUtils.get_fav_artists(userId = app.state.active_user['UserId'], db = db)
    return res

@app.get('/fetch_artists_carousel_details')
def fetch_artists_carousel_details_():
    
    if app.state.active_user.get('Role') != 'Users':
        return { 'status' : 'failed', 'message' : 'You are not authorized for this Operation!!' }
    
    res = artistUtils.fetch_artists_carousel_details(limit = 10, db = db)
    
    if res['status'] != 'success':
        return res
    
    return res

@app.get('/suggest_artists_city')
def suggest_artists_city_(carousel: bool = True):
    
    res = usersUtils.suggest_artists_city(favArtists = app.state.active_user['favArtist'], city = app.state.active_user['City'], db = db)
    
    if res['status'] != 'success':
        return res
    
    if carousel:
        
        filteredData = [artistUtils.filter_artist_details_for_carousel(artistDetails = x) for x in res]
    
    return { 'status' : 'success', 'message' : 'Artists that belongs to user city!!', 'data' : filteredData }

@app.get('/suggest_artists_genres')
def suggest_artists_genres_(carousel: bool = True):
    
    res = usersUtils.suggest_artists_genres(favArtists = app.state.active_user['favArtist'], favGenres = app.state.active_user['FavGenre'], db = db)
    
    if res['status'] != 'success':
        return res
    
    if carousel:
        
        filteredData = [artistUtils.filter_artist_details_for_carousel(artistDetails = x) for x in res]
    
    return { 'status' : 'success', 'message' : 'Artists that belongs to user city!!', 'data' : filteredData }

'''Fest Event Functions APIs'''

@app.post('/insert_fest')
def insert_fest_(data: FestDetails):
    
    res = festsEventsUtils.insert_fest(
        festName = data.festName,
        eventsDetails = data.eventsDetails,
        ticketsAva = data.ticketsAva,
        genres = data.genres,
        description = data.description,
        startDate = data.startDate,
        endDate = data.endDate,
        tier = data.tier,
        facilities = data.facilities,
        city = data.city,
        db = db
    )
    
    return res

@app.get('/fetch_fest_user_viewed')
def fetch_fest_user_viewed_(carousel: bool = True):
    
    if app.state.active_user.get('FestsViewed', []) == []:
        return { 'status' : 'failed', 'message' : 'No Fests Viewed' }
    
    res = festsEventsUtils.fetch_fest_user_viewed(viewedFestIds = app.state.active_user['FestsViewed'], db = db)
    
    # print(res)
    if res['status'] != 'success':
        print(res)
        return res
    
    if carousel:
        
        fests = res['data']
        
        filteredDetails = [festsEventsUtils.filter_details_for_carousel(festDetails = x) for x in fests]
        
        # res['data'] = festsEventsUtils.filter_details_for_carousel(festDetails = res['data'])
        # res['message'] = 'Successfully fetch fests and filtered details for carousel'
    
    return { 'status' : 'success', 'message' : 'Successfully fetch fests and filtered details for carousel', 'data' : filteredDetails }

@app.get('/fetch_fest_user_city')
def fetch_fest_user_city_(carousel: bool = True):
    
    
    res = festsEventsUtils.fetch_fest_user_city(city = app.state.active_user['City'], db = db)
    print(app.state.active_user['City'])
    print(res)
    if res['status'] != 'success':
        return res
    
    if carousel:
        fests = res['data']
        
        filteredDetails = [festsEventsUtils.filter_details_for_carousel(festDetails = x) for x in fests]
        
        # res['data'] = festsEventsUtils.filter_details_for_carousel(festDetails = res['data'])
        # res['message'] = 'Successfully fetch fests and filtered details for carousel'
    
    return { 'status' : 'success', 'message' : 'Successfully fetch fests and filtered details for carousel', 'data' : filteredDetails }

@app.get('/fetch_fest_user_fav_genre')
def fetch_fest_user_fav_genre_(carousel: bool = True):
    
    res = festsEventsUtils.fetch_fest_user_fav_genre(favGenres = app.state.active_user['FavGenre'], db = db)

    print(res)
    if res['status'] != 'success':
        return res
    
    if carousel:
        fests = res['data']
        
        filteredDetails = [festsEventsUtils.filter_details_for_carousel(festDetails = x) for x in fests]
        
        # res['data'] = festsEventsUtils.filter_details_for_carousel(festDetails = res['data'])
        # res['message'] = 'Successfully fetch fests and filtered details for carousel'
    
    return { 'status' : 'success', 'message' : 'Successfully fetch fests and filtered details for carousel', 'data' : filteredDetails }

@app.get('/fetch_fest_user_fav_artist')
def fetch_fest_user_fav_artist_(carousel: bool = True):
    
    res = festsEventsUtils.fetch_fest_user_fav_artist(favArtists = app.state.active_user['favArtist'], db = db)

    print(res)
    if res['status'] != 'success':
        return res
    
    if carousel:
        fests = res['data']
        
        filteredDetails = [festsEventsUtils.filter_details_for_carousel(festDetails = x) for x in fests]
        
        # res['data'] = festsEventsUtils.filter_details_for_carousel(festDetails = res['data'])
        # res['message'] = 'Successfully fetch fests and filtered details for carousel'
    
    return { 'status' : 'success', 'message' : 'Successfully fetch fests and filtered details for carousel', 'data' : filteredDetails }

'''Jobs and Applications APIs'''
@app.post('/post_job')
def post_job_(data : PostJob):
    
    if app.state.active_user.get('Role', '') != 'Organizers':
        return { 'status' : 'failed', 'message' : 'Not Authorized!!' }
    
    res = jobsUtils.post_job(jobDetails = data.jobDetails, orgId = app.state.active_user['UserId'], db = db)
    
    return res

@app.post('/post_job_applications')
def post_job_applications_(data: ApplicationDetails):
    
    if app.state.active_user.get('Role', '') != 'CrewMember':
        return { 'status' : 'failed', 'message' : 'Not Authorized!!' }
    
    res = jobsUtils.post_job_application(applicationDetails = data.applicationDetails, jobId = data.JobId, crewId = data.CrewId, db = db)

    return res

@app.get('/get_user_applications')
def get_user_applicaitons_(sortFilter, inc: int = 1):
    
    if app.state.active_user.get('Role', '') != 'CrewMember':
        return { 'status' : 'failed', 'message' : 'Not Authorized!!' }
    
    res = jobsUtils.get_user_applications(crewId = app.state.active_user['UserId'], sortFilter = sortFilter, inc = inc, db = db)
    
    return res

@app.put('/change_application_status')
def change_application_status_(data: ApplicationStatus):
    
    if app.state.active_user.get('Role', '') != 'Organizers':
        return { 'status' : 'failed', 'message' : 'Not Authorized!!' }
    
    res = jobsUtils.change_application_status(applicationId = data.applicationId, status = data.status, db = db)
    
    return res

@app.get('/list_jobs')
def list_jobs_(filter: str = None):
    
    res = jobsUtils.list_jobs(
        crewMemDetails = app.state.active_user,
        filter = filter,
        db = db
    )
    
    return res

@app.delete('/delete_jobs/{jobId}')
def delete_jobs_(jobId: str):   
    
    if app.state.active_user.get('Role', '') != 'Organizers':
        return { 'status' : 'failed', 'message' : 'Not Authorized!!' }
    
    res = jobsUtils.delete_jobs(jobId = jobId, orgId = app.state.active_user['UserId'], db = db)
    
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "mainAPI:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )