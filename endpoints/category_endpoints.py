from typing import List
from fastapi import APIRouter, Depends, HTTPException

from models.category import Category, CategoryCreate, CategoryRead, CategoryUpdate
from db.db import session
from auth.auth import AuthHandler
from sqlmodel import select

category_router = APIRouter()
auth_handler = AuthHandler()


@category_router.post('/categories/', response_model=CategoryRead, tags=['Categories'])
async def create_Category(*,
    category: CategoryCreate,
    user=Depends(auth_handler.auth_wrapper)
):
    db_category = Category.from_orm(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@category_router.get('/categories/', response_model=List[CategoryRead], tags=['Categories'])
async def get_all_Categories():
    categories = session.exec(select(Category)).all()
    return categories
 
@category_router.get('/categories/{id}/', response_model=CategoryRead, tags=['Categories'])
async def get_Category(id: int):
    category = session.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    return category

@category_router.patch('/categories/{id}/', response_model=CategoryRead, tags=['Categories'])
async def update_category(
    id: int,
    category: CategoryUpdate,
    user=Depends(auth_handler.auth_wrapper)
):
    category_found = session.get(Category, id)
    if not category_found:
        raise HTTPException(status_code=404, detail='Category not found')
    update_data = category.dict(exclude_unset=True)
    for key, val in update_data.items():
        category_found.__setattr__(key, val)
    session.commit()
    return category_found

@category_router.delete('/categories/{id}/', tags=['Categories'])
async def delete_Category(
    id: int,
    user=Depends(auth_handler.auth_wrapper)
):
    category_found = session.get(Category, id)
    if not category_found:
        raise HTTPException(status_code=404, detail='Category not found')
    session.delete(category_found)
    session.commit()
    return {"ok": True}
