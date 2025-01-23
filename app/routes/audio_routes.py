from fastapi import APIRouter, UploadFile, HTTPException
from app.services.audio_processing import process_audio
from app.services.database import save_to_database

router = APIRouter()

@router.post("/process-audio/")
async def process_audio_endpoint(file: UploadFile):
    try:
        audio_data = await file.read()
        json_data = process_audio(audio_data, file.filename)
        save_to_database(json_data, audio_data)
        return {"status": "success", "message": "Audio procesado y guardado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))