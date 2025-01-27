from fastapi import APIRouter, UploadFile, HTTPException
from app.services.audio_processing import process_audio
from app.services.database import save_to_database

# Create the APIRouter instance for audio-related routes
router = APIRouter()

@router.post("/process-audio/")
async def process_audio_endpoint(file: UploadFile):
    """
    Endpoint to process an audio file.

    Args:
        file (UploadFile): The uploaded audio file to be processed.

    Returns:
        dict: A dictionary containing the status of the operation and a success message.

    Raises:
        HTTPException: If an error occurs during processing or saving, it raises an HTTP 500 error with details.
    """
    try:
        # Read the uploaded audio file
        audio_data = await file.read()

        # Process the audio file and extract relevant data
        json_data = process_audio(audio_data, file.filename)

        # Save the processed data and raw audio to the database
        save_to_database(json_data, audio_data)

        # Return a success response
        return {"status": "success", "message": "Audio processed and saved successfully."}
    except Exception as e:
        # Handle any exceptions and return a server error response
        raise HTTPException(status_code=500, detail=str(e))
    

"""
======================
This module defines the routes for handling audio file processing in the API.

Main Components:
- `process_audio_endpoint`: A POST endpoint for processing uploaded audio files.
- `process_audio`: A service function to analyze and extract data from the audio file.
- `save_to_database`: A service function to store processed audio data and metadata in the database.

Workflow:
1. The user uploads an audio file to the `/process-audio/` endpoint.
2. The `process_audio` service processes the audio file, extracting phonemes, transcription, and other relevant data.
3. The `save_to_database` service saves both the processed data and the raw audio into a database.

Example of Usage:
=================
1. Upload an audio file via the `/process-audio/` POST endpoint:
    curl -X POST "http://127.0.0.1:8000/api/process-audio/" \
        -F "file=@example_audio.mp3"

Expected Response:
    {
        "status": "success",
        "message": "Audio processed and saved successfully."
    }
"""