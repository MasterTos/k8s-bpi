from sqlalchemy import Column, Float, String
from database import Base
import uuid

class User(Base):
    __tablename__ = 'users'
    uid = Column(String(8), primary_key=True)
    first_name = Column(String(256))
    last_name = Column(String(256))