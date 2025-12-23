import os 
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine
load_dotenv()

mysqlUrl = os.getenv("MYSQL_URL")

class Person(SQLModel,table = True):
    id : int | None = Field(default=None, primary_key=True)
    username : str 
    password : str

engine = create_engine(mysqlUrl)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_Sessions():
    with Session(engine) as session:
        yield session

sessionDependency = Annotated[Session, Depends(get_Sessions)]