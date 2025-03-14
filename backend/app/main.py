from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import Base, User, Game
from .schemas import UserCreate, UserResponse
from db import get_db, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = user.password + "notsecure" # Replace with actual hashing
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/games")
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    games = db.query(Game).offset(skip).limit(limit).all()
    return games