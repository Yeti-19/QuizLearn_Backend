from passlib.context import CryptContext
from models import User
from db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from datetime import datetime, timedelta

# Secret key for JWT token encoding/decoding (if you are using JWTs)
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to register a new user
def register_user(db: Session, username: str, email: str, password: str, phone_number: str):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(password)
    new_user = User(username=username, email=email, password=hashed_password, phone_number=phone_number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Function to authenticate a user (verify email/password)
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return user

# Dependency to get the current user (if JWT is used or session management is in place)
def get_current_user(db: Session = Depends(get_db)):
    # This function can be expanded with authentication logic (JWT or session-based)
    user = db.query(User).first()  # Here, we're just fetching the first user for simplicity
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
