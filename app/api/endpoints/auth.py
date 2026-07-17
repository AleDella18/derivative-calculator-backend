from fastapi import APIRouter, HTTPException, Response, Request
from app.schemas.user import User
from app.repository.users import check_user_password, save_user
from jose import jwt
from datetime import datetime, timedelta, timezone
import os
from app.utils.utils import is_valid_password
from app.utils.security import hash_password, verify_password

router = APIRouter(tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "BrUJTuTS28idUj5sfo2370BkUREjY3M2CJjp01UVrNm")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

fake_users = {}


@router.post("/signin")
def signin(user: User, response: Response, request: Request):
    db = request.app.state.db

    stored_password_hash = check_user_password(user.username, db)
    
    
    if stored_password_hash is None:
        raise HTTPException(status_code=400, detail="User doesn't exist")

    if not verify_password(user.password, stored_password_hash):
        raise HTTPException(status_code=400, detail="Invalid password")

    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    token = jwt.encode(
        {"sub": user.username, "exp": expire.timestamp()},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    

    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
    )

    return {"message": "Login completed"}


@router.post("/signup")
def signup(user: User, request: Request):
    db = request.app.state.db

    password = check_user_password(user.username, db)
    if password:
        raise HTTPException(status_code=400, detail="User already exists")

    if not is_valid_password(user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid password: must be at least 8 characters and contain lowercase, uppercase, number, and special character",
        )

    hashed_password = hash_password(user.password)
    save_user(user.username, hashed_password, db)
    return {"message": "User successfully registered"}
