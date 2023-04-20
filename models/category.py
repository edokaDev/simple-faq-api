from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class CategoryBase(SQLModel):
    name: str


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    questions: List["Question"] = Relationship(back_populates='category')

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int


class CategoryUpdate(SQLModel):
    name: Optional[str] = None

# class CategoryWithQuestions(CategoryRead):
#     subs: List["Question"] = None
