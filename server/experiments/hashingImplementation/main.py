# fast api server for hashing testing
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from schema import create_db_and_table, Person, sessionDependency
from contextlib import asynccontextmanager
from hashing import bcryptPass

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield



app = FastAPI(lifespan=lifespan)


@app.post("/sign_up")
def signup(person : Person, session : sessionDependency) -> Person:
    person.password = bcryptPass.hash_password(person.password)
    session.add(person)
    session.commit()
    session.refresh(person)
    return person