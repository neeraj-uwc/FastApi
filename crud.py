from sqlalchemy.orm import Session
from sqlalchemy import desc

import models, schemas


def create_class(db: Session, class_: schemas.ClassDetail):
    db_user = models.Class(name=class_.name, description=class_.description)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_student(db: Session, student: schemas.StudentBase, class_id: int):
    db_item = models.Student(**student.dict(), class_id=class_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_student(db: Session, class_id: int):
    return db.query(models.Student).filter(models.Student.class_id == class_id).all()


def list_student(db:Session):
    return db.query(models.Student).all()


def get_students(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def update__student(db: Session, student_id: models.Student, updates: schemas.StudentDetail):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student_id, key, value)
    db.commit()


def delete_student(db: Session, student_id: int):
    db.query(models.Student).filter(models.Student.id == student_id).delete()
    db.commit()
    return True


def search_student(db: Session, search_term: str):
    return db.query(models.Student).filter(models.Student.name == search_term).all()


def sort_students(db: Session, sort_by: str, sort_dir: str):
    sort_column = getattr(models.Student, sort_by)
    if sort_dir == "desc":
        sort_column = sort_column.desc()
    data = db.query(models.Student).order_by(sort_column).all()
    return data
