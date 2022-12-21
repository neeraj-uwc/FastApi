import json
import os
from typing import Optional, List
from fastapi_pagination import Page, paginate, add_pagination


from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import crud, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

add_pagination(app)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/classes/", response_model=schemas.ClassDetail)
def create_class(class_: schemas.ClassDetail, db: Session = Depends(get_db)):
    return crud.create_class(db=db, class_=class_)


@app.post("/classes/{class_id}/students/")
def create_student(
        class_id: int, student: schemas.StudentBase, db: Session = Depends(get_db)):
    student_id = crud.create_student(db=db, student=student, class_id=class_id)
    return {"name":student.name}


@app.get("/students/{class_id}")
def read_student_by_class_id(class_id: int, db: Session = Depends(get_db)):
    db_students = crud.get_student(db, class_id=class_id)
    if db_students is None:
        raise HTTPException(status_code=404, detail="Student not found")
    students = []
    for s in db_students:
        students.append({"name":s.name, "age":s.age, "id":s.id})
    return {"students":students}


@app.get("/students/", response_model=Page[schemas.StudentDetail])
def list_students(db: Session = Depends(get_db)):
    result = crud.list_student(db)
    return paginate(result)


@app.patch("/students/edit", response_model=schemas.StudentDetail)
def update_student(student_id: int, student: schemas.StudentBase, db: Session = Depends(get_db)):
    existing_student = crud.get_students(db=db, student_id=student_id)
    if existing_student is None:
       
        pass
    crud.update__student(db=db, student_id=existing_student, updates=student)
    return JSONResponse(status_code=200, content={"message": "Student updated successfully."})


@app.delete("/students/{student_id}/delete", response_model=schemas.StudentDetail)
def delete_student_byID(student_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_student(db, student_id=student_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Student is not deleted")
    return JSONResponse(status_code=200, content={"message": "Student deleted successfully."})


@app.get("/search/", response_model=List[schemas.StudentDetail])
def search_student(search_term: str, db: Session = Depends(get_db)):
    db_search = crud.search_student(db=db, search_term=search_term)
    return db_search


@app.get("/students/sort/", response_model=List[schemas.StudentDetail])
def sort_student(sort_by: str, sort_dir: str, db: Session = Depends(get_db)):
    db_sort = crud.sort_students(db,  sort_by=sort_by, sort_dir=sort_dir)
    return db_sort    
