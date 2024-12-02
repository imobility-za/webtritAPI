# Econet API

from fastapi import HTTPException, status, Security, FastAPI, Depends, Query, Request, Response
from fastapi.security import APIKeyHeader
from typing import Annotated, List
from sqlalchemy.orm import Session
from asgi_correlation_id import CorrelationIdMiddleware

import config
import crud
import opensips
import models
import schemas
from logs import logger
from database import engine, SessionLocal


def get_db() :
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()


tags_metadata = [
    {
        "name" : "Users",
        "description" : "Operations on Users",
    },
]

description = """
Econet Call Home Provisioning API
"""

app = FastAPI(
    root_path=config.api_root_path,
    title="Econet Call Home Provisioning API",
    description=description,
    version="0.0.1",
    contact={
        "name" : "iMobility",
        "url" : "https://www.imgroup.co.za",
        "email" : "technical@imgroup.co.za",
    },
)
app.add_middleware(CorrelationIdMiddleware)
models.Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

api_key_header = APIKeyHeader(name="Authentication", auto_error=False)


def get_api_key(db: db_dependency,
                api_key_header: schemas.AuthResponse = Security(api_key_header),
                ) -> schemas.AuthResponse :
    """Function for check if API key matches entry in DB"""
    authkey = crud.validate_auth_key(authkey=api_key_header, db=db)
    if authkey is None :
        logger.info(f"failed login key used {api_key_header}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    if authkey.disabled is True :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Api Key Disabled",
        )
    return authkey


@app.get("/subscribers",
         response_model=List[schemas.SubscriberList],
         tags=["Subscribers"])
def list_subscribers(
        request: Request,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(le=100)] = 10,
        api_key: schemas.AuthResponse = Security(get_api_key),
        db: Session = Depends(get_db)) :
    """ Method to list subscribers"""
    logger.info(f"new request for {request.url.path}, query: {request.query_params} src_ip: {request.client.host}")
    subscribers = crud.get_subscribers(db, skip=skip, limit=limit)
    return subscribers


@app.get("/subscriber/{username}",
         response_model=schemas.SubscriberList,
         tags=["Subscribers"],
         responses={
             404 : { "model" : schemas.NoSubscriberError, "description" : "Raised if no subscriber is found" }
         })
def get_subscriber(
        request: Request,
        username: str,
        api_key: schemas.AuthResponse = Security(get_api_key),
        db: Session = Depends(get_db)) :
    """ Method to get subscriber"""
    logger.info(f"new request for {request.url.path}, query: {request.query_params} src_ip: {request.client.host}")
    subscriber = crud.get_subscriber(db, username=username)
    if subscriber is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no subscriber found')
    return subscriber


@app.post("/subscriber",
          status_code=status.HTTP_201_CREATED,
          # response_model=schemas.ValidationCreateResponse,
          tags=["Subscribers"],
          responses={
              424 : { "model" : schemas.DependancyError, "description" : "Raised if dependencies aren't met" }
          })
def add_subscriber(
        request: Request,
        subscriber_info: schemas.Subscriber,
        api_key: schemas.AuthResponse = Security(get_api_key),
        db: Session = Depends(get_db)
) :
    """Method for provisioning a new subscriber"""
    logger.info(
        f"new request for POST {request.url.path}, data:{{ {subscriber_info} }} src_ip: {request.client.host}")
    insert = crud.add_subscriber(db,
                                 subscriber_info.username,
                                 subscriber_info.password,
                                 subscriber_info.email_address,
                                 subscriber_info.state
                                 )
    logger.info(f"sending response")
    return "Success"


@app.delete("/subscriber/{username}",
            status_code=status.HTTP_204_NO_CONTENT,
            # response_model=schemas.ValidationCreateResponse,
            tags=["Subscribers"],
            responses={
                404 : { "model" : schemas.NoSubscriberError, "description" : "Raised if no subscriber is found" }
            })
def delete_subscriber(
        request: Request,
        username: str,
        api_key: schemas.AuthResponse = Security(get_api_key),
        db: Session = Depends(get_db)
) :
    """Method for removiong a subscriber"""
    logger.info(
        f"new request for DELETE {request.url.path}, data:{{ {username} }} src_ip: {request.client.host}")
    t = crud.validate_subscriber(db, username)
    if t is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no subscriber found')
    crud.delete_subscriber(db, username)
    logger.info(f"sending response")
    return "Success"


@app.patch("/subscriber/{username}",
           status_code=status.HTTP_204_NO_CONTENT,
           tags=["Subscribers"],
            responses={
                404 : { "model" : schemas.NoSubscriberError, "description" : "Raised if no subscriber is found" }
            })
def update_subscriber(
        request: Request,
        username: str,
        subscriberInfo: schemas.SubscriberUpdate,
        api_key: schemas.AuthResponse = Security(get_api_key),
        db: Session = Depends(get_db)
) :
    """Method for updating a subscriber"""
    logger.info(
        f"new request for DELETE {request.url.path}, data:{{ {username} }} src_ip: {request.client.host}")
    t = crud.validate_subscriber(db, username)
    if t is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no subscriber found')
    crud.update_subscriber(db, username, subscriberInfo)
    logger.info(f"sending response")
    return "Success"
