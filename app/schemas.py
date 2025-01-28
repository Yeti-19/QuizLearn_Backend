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

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries
        
