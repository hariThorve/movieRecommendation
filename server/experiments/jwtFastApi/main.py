# Implementing Jwt with FastApi
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext


SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30

app = FastAPI()

# fake Database testing purpose

fake_db = {
    "hari": {
        "username": "hari",
        "email" : "hariprasadthorve@gmail.com",
        "hashedPass" : "",
        "disabled": False
    }
}

# Inherit from base model, defines how will the token be
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : str or None = None

class User(BaseModel):
    username: str or None = None
    email: str or None = None
    disabled : bool or None = None

class UserInDb(User):
    hashedPass : str
