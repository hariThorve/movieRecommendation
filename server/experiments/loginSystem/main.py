import os 
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlmodel import select
from model import create_db_and_table, Student, sessionDependency
from contextlib import asynccontextmanager
from hashing import Bcrypt

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/sign-up")
def signup(student: Student, session: sessionDependency) -> Student:
    student.password = Bcrypt.hash_password(student.password)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.post("/login")
def login(student: Student, session: sessionDependency) -> Student:
    statement = select(Student).where(Student.email == student.email)
    stud = session.exec(statement=statement).first()
    if stud:
        return {"id":stud.id, "name": stud.name, "email": stud.email}
    else:
        return {"error": "no user found"}