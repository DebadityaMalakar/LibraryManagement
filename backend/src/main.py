from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .models import User, SessionLocal
import hashlib
import random
import string

app = FastAPI()

# Allow CORS for frontend requests
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_salt():
    letters = ''.join(random.choices(string.ascii_letters, k=3))
    numbers = ''.join(random.choices(string.digits, k=3))
    return letters + numbers

def hash_password(password: str, salt: str):
    return hashlib.sha256((password + salt).encode()).hexdigest()

class UserCredentials(BaseModel):
    username: str
    password: str

@app.post("/check_user/")
async def check_user(credentials: UserCredentials, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    hashed_password = hash_password(credentials.password, user.salt)
    if hashed_password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    return {
        "status": "success",
        "message": "User authenticated",
        "user": {
            "_id": user._id,
            "username": user.username
        }
    }


@app.post("/create_user/")
async def create_user(username: str, name: str, email: str, password: str, db: Session = Depends(get_db)):
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    user = User(username=username, name=name, email=email, password=hashed_password, salt=salt)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"status": "User created successfully"}

@app.get("/api/{user}/books")
async def getBooks(user:str):
    return {"user":user}