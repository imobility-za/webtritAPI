from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class SubscriberState(str, Enum) :
    active= 'active'
    suspended= 'suspended'

class AuthResponse(BaseModel) :
    i_customer: int
    disable: int

class Subscriber(BaseModel) :
    username: str
    password: str
    email_address: EmailStr
    state: SubscriberState

class SubscriberUpdate(BaseModel) :
    password: Optional[str] | None = None
    email_address: Optional[EmailStr] | None = None
    state: Optional[SubscriberState] | None = None

class Group(BaseModel) :
    username: str
    state: str

class SubscriberList(BaseModel) :
    username: str
    email_address: Optional[str]
    state: SubscriberState

class DependancyError(BaseModel) :
    detail: str


class NoSubscriberError(BaseModel) :
    detail: str = 'no subscriber found'