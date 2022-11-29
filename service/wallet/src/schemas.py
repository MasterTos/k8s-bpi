from pydantic import BaseModel

# Create User Schema (Pydantic Model)
class UserCreate(BaseModel):
    first_name: str
    last_name: str

class WalletCreate(BaseModel):
    user_uid: str
    balance: float

# Complete User Schema (Pydantic Model)
class User(BaseModel):
    uid: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

# Complete Wallet Schema (Pydantic Model)
class Wallet(BaseModel):
    uid: str
    user_uid: str
    balance: float

    class Config:
        orm_mode = True