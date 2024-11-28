from certifi import where
from httpx import delete
from sqlalchemy.orm import Session
from sqlalchemy import insert, and_, delete, values, update
from sqlalchemy.orm.sync import update

# Local imports
import models
import schemas
from models import Subscriber, Groups
from schemas import Group


# # ###################### Remove when done used for autocomplet ##############
# def get_db() :
#     db = SessionLocal()
#     try :
#         yield db
#     finally :
#         db.close()
#
#
# db: Session = Depends(get_db)

def get_subscribers(db: Session, skip: int = 0, limit: int = 100) :
    subscribers = (
        db.query(models.Subscriber)
        .with_entities(models.Subscriber.username, models.Subscriber.email_address, models.Groups.state)
        .join(Groups, and_(models.Subscriber.username == models.Groups.username), isouter=True)
        .all()
    )
    return subscribers


def get_subscriber(db: Session, username: str) :
    subscriber = (
        db.query(models.Subscriber)
        .with_entities(models.Subscriber.username, models.Subscriber.email_address, models.Groups.state)
        .join(Groups, and_(models.Subscriber.username == models.Groups.username), isouter=True)
        .filter(models.Subscriber.username == username)
        .all()
    )
    return subscriber


def delete_subscriber(db: Session, username: str) :
    db.execute(delete(Subscriber).where(Subscriber.username == username))
    db.execute(delete(Groups).where(Groups.username == username))
    db.commit()
    return True


def add_subscriber(db: Session, username: str, password: str, email_address: str, state: schemas.SubscriberState) :
    db.execute(insert(Groups).values(username=username,
                                     domain="105.29.88.68",
                                     state=state
                                     ))
    subscriber = db.execute(insert(Subscriber).values(username=username,
                                                      password=password,
                                                      domain="105.29.88.68",
                                                      email_address=email_address
                                                      ))
    db.commit()
    return subscriber


def update_subscriber(db: Session, username: str, subscriberinfo: schemas.SubscriberUpdate) :
    subscriber = (
        db.query(models.Subscriber)
        .join(Groups, and_(models.Subscriber.username == models.Groups.username), isouter=True)
        .filter(models.Subscriber.username == username)
        .first()
    )
    print(subscriber.username)
    subscriber_data = subscriberinfo.model_dump(exclude_unset=True)
    print(subscriber_data)
    for key, value in subscriber_data.items() :
        setattr(subscriber, key, value)
    if subscriberinfo.state :
        db.query(Groups).filter(Groups.username == username).update({Groups.state : subscriberinfo.state})
    db.commit()
    print(subscriber_data)


def validate_auth_key(db: Session, authkey: schemas.AuthResponse) :
    keyinfo = db.query(models.Users).filter(models.Users.api_key == authkey).first()
    return keyinfo
