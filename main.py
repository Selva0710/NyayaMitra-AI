import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.router import api_router
from app.db.session import engine, Base

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the DB (Optional auto-migrate for dev, prefer Alembic for prod)
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        # Warning: In production, use Alembic and disable this
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Startup complete.")
    yield
    # Shutdown
    logger.info("Shutting down...")
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS middleware
# In production, specify exact origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to NyayaMitra AI API"}
