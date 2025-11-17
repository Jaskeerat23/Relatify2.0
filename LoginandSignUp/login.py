import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
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

def login_user(authType : str, userName : bool, enteredPassword : str, db = db):
    
    collection = db['Accounts']
    
    if userName:
        result = collection.find_one({"UserName" : authType}, { "_id" : 1, "Password" : 1, "Role" : 1 })
    elif not userName:
        result = collection.find_one({"Email" : authType}, { "_id" : 1, "password" : 1, "Role" : 1 })
    
    if result == None:
        if userName:
            return { "status" : "failed", "message" : "UserName Invalid" }  # -1 is returned when userName is not valid
        elif not userName:
            return { "status" : "failed", "message" : "Email Invalid" } # -2 is returned when email is used for login is invalid
    
    corrPass = result['Password']
    
    if enteredPassword == corrPass:
        
        userRole = result['Role']
        _id = result['Role'].id
        collection = result['Role'].collection
        
        return { 
                    "status" : "success",
                    "message" : "UserName Logged-In", 
                    "data" : {
                        "AccountId" : str(result["_id"]),
                        "UserId" : str(_id), 
                        "Collection" : collection
                        } 
                    }
    else:
        return { "status" : "failed", "message" : "Incorrect Password or UserName" } # 0 is returned when password is incorrect

if __name__ == "__main__":
    
    print(login_user(authType = "neha_m", userName = True, enteredPassword = "hashPass"))