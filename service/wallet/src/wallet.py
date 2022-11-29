from typing import List
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter, Response
from prometheus_fastapi_instrumentator import Instrumentator
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
import logging
import uuid


# Create the database
Base.metadata.create_all(engine)

app = FastAPI()

router = APIRouter(tags=["Wallet"])

Instrumentator().instrument(app).expose(app, include_in_schema=False)

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

@router.get("/{user_uid}", response_model=schemas.Wallet)
def get_user_balance(user_uid: str, session: Session = Depends(get_session)):
    wallet = session.query(models.Wallet).filter_by(user_uid=user_uid).first()
    if not wallet:
        raise HTTPException(status_code=404, detail=f"User {user_uid} not found")
    return wallet

@router.post("/create",response_model=schemas.Wallet, status_code=status.HTTP_201_CREATED)
def create_wallet(wallet: schemas.WalletCreate, session: Session = Depends(get_session)):
    wallet = models.Wallet(uid = str(uuid.uuid4())[:8], user_uid = wallet.user_uid, balance=wallet.balance)

    session.add(wallet)
    session.commit()
    session.refresh(wallet)

    return wallet

@router.put("/update/{user_uid}", response_model=schemas.Wallet)
def update_balance(user_uid: str, wallet: schemas.WalletUpdate, session: Session = Depends(get_session)):
    wallet_obj = session.query(models.Wallet).filter_by(user_uid=wallet.user_uid).first()

    if wallet_obj:
      wallet_obj.balance = wallet.balance
      session.commit()

    if not wallet_obj:
        raise HTTPException(status_code=404, detail=f"User {user_uid} not found")

    return wallet_obj

@router.delete("/delete/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wallet(uid: str, session: Session = Depends(get_session)):
    wallet = session.query(models.Wallet).get(uid)

    if wallet:
        session.delete(wallet)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Wallet {uid} not found")

    return None


app.include_router(router)


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/healthz") == -1

# Filter out /healthz
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())