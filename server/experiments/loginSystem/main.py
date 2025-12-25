import os 
from fastapi import FastAPI
from dotenv import load_dotenv
from model import create_db_and_table, Student, sessionDependency
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield

app = FastAPI(lifespan=lifespan)

