from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

from auth.auth import AuthHandler
from models.user import User, UserCreate, UserRead, UserUpdate
from db.db import session

user_router = APIRouter()
auth_handler = AuthHandler()

@user_router.post('/register/', response_model=UserRead, tags=['Users'], description='Register new user')
async def register(*, user: UserCreate):
    users = session.exec(select(User)).all()
    # checking for username
    if any(x['username'] == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')

    hashed_pwd = auth_handler.get_password_hash(user.password)
    db_user = User(
        username=user.username,
        password=hashed_pwd,
        email=user.email,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@user_router.get('/users/', response_model=List[UserRead], tags=['Users'])
async def get_all_users(user=Depends(auth_handler.auth_wrapper)):
    users = session.exec(select(User)).all()
    return users

@user_router.get('/users/{id}/', response_model=UserRead, tags=['Users'])
async def get_user(id: int, user=Depends(auth_handler.auth_wrapper)):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.patch('/users/{id}/', response_model=UserRead, tags=['Users'])
async def update_user(id: int, user_up: UserUpdate, user=Depends(auth_handler.auth_wrapper)):
    user_found = session.get(User, id)
    if not user_found:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user_up.dict(exclude_unset=True)
    for key, val in user_data.items():
        user_found.__setattr__(key, val)
    session.commit()
    session.refresh(user_found)
    return user_found

@user_router.delete('/users/{id}/', tags=['Users'])
async def delete_user(id: int, user=Depends(auth_handler.auth_wrapper)):
    user_found = session.get(User, id)
    if not user_found:
        raise HTTPException(status_code=404, detail='User not found')
    session.delete(user_found)
    session.commit()

    return {"ok": True}
