from sqlmodel import SQLModel, Session, Field, create_engine
from fastapi import Depends
from typing import Annotated
import os
from dotenv import load_dotenv

load_dotenv()

engine = os.getenv("MYSQL_URL")

class Movie(SQLModel, table=True):
    movieId : int | None = Field(default=None, primary_key=True)
    movie_name : str
    genre : str
    movie_ratings : str
    voting_count : str

def create_table():
    SQLModel.metadata.create_all(engine)

def getSessions():
    with Session(engine) as session:
        yield session

sessionDependency = Annotated[Session, Depends(getSessions)]
    