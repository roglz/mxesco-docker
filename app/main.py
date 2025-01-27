from fastapi import FastAPI
from app.routes.audio_routes import router as audio_router

app = FastAPI(
    title="MXesco API",
    description="An API for uploading audio files, transcribing them, extracting phonemes, and storing data in MongoDB.",
    version="1.0.0"
)

# Register the audio router with the prefix "/api"
app.include_router(audio_router, prefix="/api")

"""
======================
This module sets up and runs the main FastAPI application instance.

Main Components:
- `FastAPI`: Creates and configures the FastAPI application.
- `audio_router`: A router defining the audio-related endpoints, imported from `app.routes.audio_routes`.

Key Points:
- All routes in the audio router are prefixed with `/api`.
- Additional routers can be added in a similar way to modularize the application.

Example of Execution:
======================
Run the server locally using:
    uvicorn main:app --reload

Interactive API Documentation:
==============================
Once the server is running, visit:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
"""