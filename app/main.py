from fastapi import FastAPI, Depends, HTTPException, status  # Add status import here
from sqlalchemy.orm import Session
from db import get_db
from models import User
from schemas import UserRegister, UserLogin, UserResponse
from auth import register_user, authenticate_user, get_current_user
from typing import List

app = FastAPI()

# Route to register a new user
@app.post("/register/")
def register(user: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, user.username, user.email, user.password, user.phone_number)
    return {"message": "User created successfully", "username": user.username}

# Route to log in and get a token
@app.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user.username, user.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "User logged in successfully", "username": user.username}

# Route to get current user details (requires a valid token)
@app.get("/users/me")
def get_user_me(current_user: dict = Depends(get_current_user)):
    return current_user

# New Route to get all users
@app.get("/users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()  # Query all users from the database
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users  # Return a list of users
