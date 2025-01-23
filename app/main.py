from fastapi import FastAPI
from app.routes.audio_routes import router as audio_router

app = FastAPI()

# Registrar rutas
app.include_router(audio_router, prefix="/api")