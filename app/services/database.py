from pymongo import MongoClient
import gridfs

# Initialize the MongoDB client
client = MongoClient("mongodb://mongo:27017/")
# Access the `mxesco` database
db = client.mxesco
# Initialize GridFS for handling binary files (e.g., audio)
fs = gridfs.GridFS(db)

def save_to_database(json_data: dict, audio_bytes: bytes) -> None:
    """
    Saves processed audio data and its metadata to the MongoDB database.

    Args:
        json_data (dict): A dictionary containing metadata and transcription data for the audio file.
        audio_bytes (bytes): The raw audio file in bytes format.
    """
    # Insert metadata and transcription data into the `documents` collection
    db.documents.insert_one(json_data)
    
    # Save raw audio bytes into GridFS with the filename from the metadata
    fs.put(audio_bytes, filename=json_data["audio"]["file"])

"""
======================
This module provides functionality to save processed audio metadata and raw audio files 
to a MongoDB database using GridFS for binary file storage.

Main Components:
- `MongoClient`: Connects to the MongoDB database.
- `GridFS`: Used to store and retrieve binary files (e.g., audio files).
- `save_to_database`: A function to save metadata and audio files.

Workflow:
1. Connects to the `mxesco` database on the MongoDB server.
2. Stores audio metadata in the `documents` collection.
3. Stores the raw audio file in GridFS with its corresponding filename.

Example of Execution:
======================
json_data = {
    "audio": {"file": "example_audio.wav", "duration": 12.34},
    "metadata": {"transcriber_model": "medium.en"}
}
audio_bytes = open("example_audio.wav", "rb").read()

save_to_database(json_data, audio_bytes)
"""