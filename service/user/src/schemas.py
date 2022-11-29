from pydantic import BaseModel

# Create User Schema (Pydantic Model)
class UserCreate(BaseModel):
    first_name: str
    last_name: str

# Complete User Schema (Pydantic Model)
class User(BaseModel):
    uid: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True