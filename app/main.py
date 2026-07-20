from fastapi import FastAPI
from app.api.endpoints import api_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.db_manager import DBManager
from app.core.logging_config import setup_logging
from app.utils.vercel_blob import get_blob_token
import logging
from dotenv import load_dotenv

load_dotenv()

setup_logging()
logger = logging.getLogger(__name__)

db = DBManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_blob_token()
    db.connect()
    app.state.db = db
    yield
    db.close()


app = FastAPI(lifespan=lifespan)

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
