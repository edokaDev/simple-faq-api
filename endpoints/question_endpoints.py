from typing import List
from fastapi import APIRouter, Depends, HTTPException

from models.question import Question, QuestionCreate, QuestionRead, QuestionUpdate, QuestionWithCategory, QuestionFull
from models.category import Category
from db.db import session
from auth.auth import AuthHandler
from sqlmodel import select

question_router = APIRouter()
auth_handler = AuthHandler()


@question_router.post('/questions/', response_model=QuestionRead, tags=['Questions'])
async def create_question(*,
    question: QuestionCreate,
    user=Depends(auth_handler.auth_wrapper)
):
    # category check
    cat = session.get(Category, question.category_id)
    if not cat:
        raise HTTPException(status_code=400, detail='Category does not exist')        

    db_q = Question.from_orm(question)
    session.add(db_q)
    session.commit()
    session.refresh(db_q)
    return db_q

@question_router.get('/questions/', response_model=List[QuestionWithCategory], tags=['Questions'])
async def get_all_questions():
    questions = session.exec(select(Question)).all()
    return questions
 
@question_router.get('/questions/{id}/', response_model=QuestionFull, tags=['Questions'])
async def get_question(id: int):
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail='Question not found')
    return question

@question_router.patch('/questions/{id}/', response_model=Question, tags=['Questions'])
async def update_question(
    id: int,
    question: QuestionUpdate,
    user=Depends(auth_handler.auth_wrapper)
):
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail='Question not found')
    update_data = question.dict(exclude_unset=True)
    for key, val in update_data.items():
        question.__setattr__(key, val)
    session.commit()
    return question

@question_router.delete('/questions/{id}/', tags=['Questions'])
async def delete_question(
    id: int,
    user=Depends(auth_handler.auth_wrapper)
):
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail='Question not found')
    session.delete(question)
    session.commit()
    return {"ok": True}
