from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class LoginData(BaseModel):
    username: str
    password: str   

class SignUpData(BaseModel):

    class AccountDetails(BaseModel):
        userName : str
        password : str
        contactNo : List[str]
        email : str
        city : str
        role : str
        
    accntDetails : AccountDetails
    roleDetails : Dict[str, Any]

class updateUserName(BaseModel):
    
    newUserName : str
    password : str

class updateEmail(BaseModel):
    
    newEmail : str
    password : str

class updateCity(BaseModel):
    
    newCity : str
    password : str

class FestId(BaseModel):
    
    festId : str

class ArtistId(BaseModel):
    
    artistId : str

class FestDetails(BaseModel):
    
    festName : str
    eventsDetails : Dict[str, Any]
    ticketsAva : str
    genres : str
    description : str
    startDate : datetime
    endDate : datetime
    tier : Dict[str, Any]
    facilities : List[str]
    city : str

class PostJob(BaseModel):
    
    jobDetails : Dict[str, Any]

class ApplicationDetails(BaseModel):
    
    JobId : str
    CrewId : str
    applicationDetails : str

class ApplicationStatus(BaseModel):
    
    applicationId : str
    status : str



# class TwoIds(BaseModel):
#     userId : int
#     festId : int

# class UserIDandUserName(BaseModel):
#     userId : int
#     userName : str

# class ID(BaseModel):
#     userId : int

# class UpdateUserNameData(BaseModel):
#     accntId : int
#     userName : str
#     newUserName : str
#     password : str