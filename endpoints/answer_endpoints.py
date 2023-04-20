from typing import List
from fastapi import APIRouter, Depends, HTTPException

from models.answer import Answer, AnswerCreate, AnswerRead, AnswerUpdate
from models.question import Question
from db.db import session
from auth.auth import AuthHandler
from sqlmodel import select

answer_router = APIRouter()
auth_handler = AuthHandler()


@answer_router.post('/answers/', response_model=AnswerRead, tags=['Answer'])
async def create_answer(*,
    answer: AnswerCreate,
    user=Depends(auth_handler.auth_wrapper)
):
    # question check
    q = session.get(Question, answer.question_id)
    if not q:
        raise HTTPException(status_code=400, detail='Question does not exist')        

    db_ans = Answer.from_orm(answer)
    session.add(db_ans)
    session.commit()
    session.refresh(db_ans)
    return db_ans

@answer_router.get('/answers/', response_model=List[AnswerRead], tags=['Answer'])
async def get_all_answers():
    answers = session.exec(select(Answer)).all()
    return answers
 
@answer_router.get('/answers/{id}/', response_model=AnswerRead, tags=['Answer'])
async def get_answer(id: int):
    answer = session.get(Answer, id)
    if not answer:
        raise HTTPException(status_code=404, detail='Answer not found')
    return answer

@answer_router.patch('/answers/{id}/', response_model=Answer, tags=['Answer'])
async def update_answer(
    id: int,
    answer: AnswerUpdate,
    user=Depends(auth_handler.auth_wrapper)
):
    answer = session.get(Answer, id)
    if not answer:
        raise HTTPException(status_code=404, detail='Answer not found')
    update_data = answer.dict(exclude_unset=True)
    for key, val in update_data.items():
        answer.__setattr__(key, val)
    session.commit()
    return answer

@answer_router.delete('/answers/{id}/', tags=['Answer'])
async def delete_answer(
    id: int,
    user=Depends(auth_handler.auth_wrapper)
):
    answer = session.get(Answer, id)
    if not answer:
        raise HTTPException(status_code=404, detail='Answer not found')
    session.delete(answer)
    session.commit()
    return {"ok": True}
