from fastapi import APIRouter
from app.api.endpoints import chat, documents, voice, history, compliance

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(documents.router, prefix="/upload", tags=["documents"])
api_router.include_router(voice.router, prefix="/voice", tags=["voice"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
api_router.include_router(compliance.router, prefix="/compliance", tags=["compliance"])
