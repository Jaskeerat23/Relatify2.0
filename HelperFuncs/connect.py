from pymongo import MongoClient

url = "<MONGODBURI>"

client = MongoClient(url)

db = client['festdb']

print(db.list_collection_names())