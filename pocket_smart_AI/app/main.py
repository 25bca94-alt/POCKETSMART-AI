from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    """

    # Create database tables when the application starts.
    create_tables()

    yield

    # Application shutdown code can be added here later.


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="PocketSmartAI - AI powered smart planning application",
    debug=settings.debug,
    lifespan=lifespan,
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

frontend_path = Path(__file__).resolve