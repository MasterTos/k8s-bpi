from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
import uuid


# Create the database
Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/ping", summary="Check that the service is operational")
def pong():
    """
    Sanity check - this will let the user know that the service is operational.
    It is also used as part of the HEALTHCHECK. Docker uses curl to check that the API service is still running, by exercising this endpoint.
    """
    return {"ping": "pong!"}

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def get_all_users(session: Session = Depends(get_session)):
  # get the todo item with the given id
    users = session.query(models.User).all()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not users:
        raise HTTPException(status_code=404, detail=f"No users")

    return users

@app.get("/{uuid}", response_model=schemas.User)
def get_user(uuid: str, session: Session = Depends(get_session)):
  # get the todo item with the given id
    user = session.query(models.User).get(uuid)

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not user:
        raise HTTPException(status_code=404, detail=f"User {uuid} not found")

    return user

@app.post("/create",response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
  # create an instance of the ToDo database model
    userdb = models.User(uuid = str(uuid.uuid4())[:8], first_name = user.first_name, last_name=user.last_name)

    # add it to the session and commit it
    session.add(userdb)
    session.commit()
    session.refresh(userdb)

    # return the todo object
    return userdb

@app.put("/update/{uuid}")
def update_user(uuid: str, user: schemas.UserCreate, session: Session = Depends(get_session)):
  # get the todo item with the given id
    user_obj = session.query(models.User).get(uuid)

    # update todo item with the given task (if an item with the given id was found)
    if user_obj:
      user_obj.first_name = user.first_name
      user_obj.last_name = user.last_name
      session.commit()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not user_obj:
        raise HTTPException(status_code=404, detail=f"User {uuid} not found")

    return user_obj

@app.delete("/delete/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(uuid: str, session: Session = Depends(get_session)):
  # get the todo item with the given id
    user = session.query(models.User).get(uuid)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"User {uuid} not found")

    return None
