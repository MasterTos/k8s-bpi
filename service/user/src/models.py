from sqlalchemy import Column, Integer, String
from database import Base
import uuid

class User(Base):
    __tablename__ = 'users'
    uuid = Column(String, primary_key=True)
    first_name = Column(String(256))
    last_name = Column(String(256))