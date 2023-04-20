from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class AnswerBase(SQLModel):
    response: str
    question_id: Optional[int] = Field(default=None, foreign_key='question.id')

class Answer(AnswerBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    question: Optional["Question"] = Relationship(back_populates="answer")


class AnswerCreate(AnswerBase):
    pass

class AnswerRead(AnswerBase):
    id: int


class AnswerUpdate(SQLModel):
    name: Optional[str] = None
    campus: Optional[str] = None
