from pymongo import MongoClient

url = "mongodb+srv://jaskeerat23006:waheguru1313@cluster0.qhch8uk.mongodb.net/?appName=Cluster0"

client = MongoClient(url)

db = client['festdb']

print(db.list_collection_names())