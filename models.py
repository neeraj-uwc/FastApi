from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Class(Base):
    __tablename__= "class"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, index=True)

    students = relationship("Student", back_populates="class_")

class Student(Base):
    __tablename__= "student"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)

    class_id = Column(Integer, ForeignKey("class.id"))
    class_ = relationship("Class", back_populates="students")