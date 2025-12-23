# fast api server for hashing testing
import os
from fastapi import FastAPI
from dotenv import load_dotenv



app = FastAPI()

@app.post("/sign_up")
def signup(username : str, password : str):
    pass