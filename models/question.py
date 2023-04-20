from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from .category import Category
from .answer import Answer



class QuestionBase(SQLModel):
    prompt: str
    category_id: Optional[int] = Field(default=None, foreign_key='category.id')
    

    # class Config:
    #     orm_mode = True

class Question(QuestionBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    category: Optional["Category"] = Relationship(back_populates='questions')
    answer: Optional["Answer"] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates='question'
    )

class QuestionCreate(QuestionBase):
    pass

class QuestionRead(QuestionBase):
    id: int


class QuestionUpdate(SQLModel):
    prompt: Optional[str] = None
    category_id: Optional[int] = None

class QuestionWithCategory(QuestionRead):
    category: Optional["Category"] = None

class QuestionFull(QuestionWithCategory):
    answer: Optional["Answer"] = None
