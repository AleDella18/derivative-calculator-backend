from pathlib import Path
from fastapi import FastAPI
from app.api.endpoints import api_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.db_manager import DBManager
from fastapi.staticfiles import StaticFiles
from app.core.logging_config import setup_logging
import logging
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMGS_DIR = PROJECT_ROOT / "imgs"

setup_logging()
logger = logging.getLogger(__name__)

db = DBManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    app.state.db = db
    yield
    db.close()


app = FastAPI(lifespan=lifespan)

app.mount("/imgs", StaticFiles(directory=str(IMGS_DIR)), name="imgs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.app-derivative-calculator.duckdns.org",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
