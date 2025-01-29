from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    phone_number: str

class UserLogin(BaseModel):
    username: str
    password: str

# UserResponse schema to return selected fields (e.g., excluding the password)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str
class UserProgressResponse(BaseModel):
    username: str
    tokens_earned: int
    experience_gained: int
    rank: int
    level: int
    badge: str  # Add badge field to the response

class UpdateProgressRequest(BaseModel):
    tokens_earned: int
    experience_gained: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries

class UserRankResponse(BaseModel):
    username: str
    experience_gained: int
    rank: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries

        
