from typing import List, Union
from typing import Optional
from pydantic import BaseModel


class StudentBase(BaseModel):
    name: str
    age: int


class StudentDetail(StudentBase):
    id: int
   # class_id: int

    class Config:
        orm_mode = True


class ClassDetail(BaseModel):
    id: int
    name: str
    description:str

    class Config:
        orm_mode = True


