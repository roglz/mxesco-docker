from pymongo import MongoClient
import gridfs

client = MongoClient("mongodb://mongo:27017/")
db = client.mxesco
fs = gridfs.GridFS(db)

def save_to_database(json_data, audio_bytes):
    db.documents.insert_one(json_data)
    fs.put(audio_bytes, filename=json_data["audio"]["file"])