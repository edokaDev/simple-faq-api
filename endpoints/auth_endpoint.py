from fastapi import APIRouter, HTTPException
from sqlmodel import select

from auth.auth import AuthHandler
from models.user import User, UserLogin
from db.db import session

user_router = APIRouter()
auth_handler = AuthHandler()


auth_router = APIRouter()
auth_handler = AuthHandler()

@auth_router.post('/login/', tags=['Authentication'])
async def login(*, user: UserLogin):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user:
        # username not found
        raise HTTPException(status_code=401, detail="User not fount")
    verified = auth_handler.verify_password(user.password, db_user.password)
    if not verified:
        # password mismatch
        raise HTTPException(status_code=401, detail="Invalid password")
    token = auth_handler.encode_token(db_user.username)
    return {'token': token}
