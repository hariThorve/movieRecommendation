import os
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
from sqlmodel import SQLModel, Field, Session, create_engine
load_dotenv()


mysqlUrl = os.getenv("MYSQL_URL")

class Student(SQLModel, table=True):
    id : int | None= Field(default=None, primary_key=True)
    name : str 
    password : str

engine = create_engine(mysqlUrl)
def create_db_and_table():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

sessionDependency = Annotated[Session, Depends(get_session)]