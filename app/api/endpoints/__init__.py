from fastapi import APIRouter
from app.api.endpoints.expression import router as expression_router
from app.api.endpoints.auth import router as user_router

api_router = APIRouter()

api_router.include_router(expression_router)
api_router.include_router(user_router)
