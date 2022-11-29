from typing import List
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter, Response
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
import logging
import uuid


# Create the database
Base.metadata.create_all(engine)

app = FastAPI()

router = APIRouter(tags=["Users"])

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@router.get("/healthz/livez", include_in_schema=False, status_code=status.HTTP_204_NO_CONTENT)
def livez():
  pass

@router.get("/healthz/readyz", include_in_schema=False, status_code=status.HTTP_204_NO_CONTENT)
def readyz(session: Session = Depends(get_session)):
  if not session:
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

@router.get("/")
def get_all_users(session: Session = Depends(get_session)):
    users = session.query(models.User).all()

    if not users:
        raise HTTPException(status_code=404, detail=f"No users")

    return users

@router.get("/{uid}", response_model=schemas.User)
def get_user(uid: str, session: Session = Depends(get_session)):
    user = session.query(models.User).get(uid)

    if not user:
        raise HTTPException(status_code=404, detail=f"User {uid} not found")

    return user

@router.post("/create",response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    userdb = models.User(uid = str(uuid.uuid4())[:8], first_name = user.first_name, last_name=user.last_name)

    session.add(userdb)
    session.commit()
    session.refresh(userdb)

    return userdb

@router.put("/update/{uid}")
def update_user(uid: str, user: schemas.UserCreate, session: Session = Depends(get_session)):
    user_obj = session.query(models.User).get(uid)

    if user_obj:
      user_obj.first_name = user.first_name
      user_obj.last_name = user.last_name
      session.commit()

    if not user_obj:
        raise HTTPException(status_code=404, detail=f"User {uid} not found")

    return user_obj

@router.delete("/delete/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(uid: str, session: Session = Depends(get_session)):
    user = session.query(models.User).get(uid)

    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"User {uid} not found")

    return None


app.include_router(router)


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/healthz") == -1

# Filter out /healthz
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())