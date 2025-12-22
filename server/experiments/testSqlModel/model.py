import os
from typing import Annotated
from dotenv import load_dotenv
from contextlib import asynccontextmanager 
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
load_dotenv()

mysqlUrl = os.getenv("MYSQL_URL")


class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secretName: str
    age: int | None = None

# rahulData = Person(name = "Rahul", secretName= "rahulya", age = 21)
# hariData = Person(name = "Hariprasad", secretName= "hari", age = 21)
# sohamData = Person(name = "Soham", secretName= "somya", age = 21)

# engine = create_engine(mysqlUrl)

# SQLModel.metadata.create_all(engine)

# with Session(engine) as session:
#     session.add(rahulData)
#     session.add(hariData)
#     session.add(sohamData)
#     session.commit()


engine = create_engine(mysqlUrl)

def create_tables_and_db():
    SQLModel.metadata.create_all(engine)

def get_sessions():
    with Session(engine) as session:
        yield session       # yield turns a function into a generator.

sessionDp = Annotated[Session, Depends(get_sessions)]

# What yield actually does
# When Python hits yield:
# It returns a value
# It pauses the function’s state
# Execution resumes from the same point on the next call
# Unlike return, the function does not exit.


# since on_event function is deprecated and we need to create tables when the connection is made
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup")
    create_tables_and_db()
    yield
    print("Shutdown")


app = FastAPI(lifespan=lifespan)

@app.post("/heros")
def create_hero(hero: Person, session: sessionDp) -> Person:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


