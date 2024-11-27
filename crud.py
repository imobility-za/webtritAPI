from sqlalchemy.orm import Session
from sqlalchemy import  insert

# Local imports
import models
import schemas
from models import Subscriber, Groups


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
        .all()
    )
    return subscribers

def add_subscriber(db: Session, username: str , password: str, email_address: str, enabled:bool) :
    if enabled == False:
        db.execute(insert(Groups).values(username=username,
            domain="105.29.88.68",
            grp="BLOCK"
            ))
    subscriber = db.execute(insert(Subscriber).values(username=username,
                                                      password=password,
                                                      domain="105.29.88.68",
                                                      email_address=email_address
                                                      ))
    db.commit()
    return subscriber

def validate_auth_key(db: Session, authkey: schemas.AuthResponse) :
    keyinfo = db.query(models.Users).filter(models.Users.api_key == authkey).first()
    return keyinfo

