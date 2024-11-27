from pydantic import BaseModel
from typing import Optional
#from sqlalchemy import Bool


class AuthResponse(BaseModel) :
    i_customer: int
    disable: int

class Subscriber(BaseModel) :
    username: str
    password: str
    email_address: Optional[str]
    enabled: bool

class Group(BaseModel) :
    username: str
    grp: str

class SubscriberList(BaseModel) :
    username: str
    email_address: Optional[str]

class DependancyError(BaseModel) :
    detail: str