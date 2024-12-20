from pydantic import BaseModel, EmailStr, FutureDatetime, model_validator
from typing_extensions import Self
from typing import Optional
from enum import Enum
import datetime

class SubscriberState(str, Enum) :
    active= 'active'
    suspended= 'suspended'

class SubscriptionState(str, Enum) :
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

class SubscriptionBase(BaseModel) :
    destination: str

class Subscription(SubscriptionBase) :
    username: str
    state:  Optional[SubscriptionState] | None = None
    start_date: datetime.datetime
    end_date: datetime.datetime


class SubscriptionUpdate(BaseModel) :
    state: Optional[SubscriptionState] | None = None
    start_date: Optional[datetime.datetime] | None = None
    end_date: Optional[FutureDatetime] | None = None

    @model_validator(mode='after')
    def check_start_before_end_date(self) -> Self:
        if not self.start_date and not self.end_date:
            return self
        if self.start_date and not self.end_date:
            raise ValueError('if modifying start_date end_date is required')
        if self.end_date and not self.start_date:
            raise ValueError('if modifying end_date start_date is required')
        if self.start_date > self.end_date:
            raise ValueError('end_date must be greater than start_date')
        return self

class SubscriptionAdd(SubscriptionBase) :
    state:  Optional[SubscriptionState] | None = None
    start_date: datetime.datetime
    end_date: FutureDatetime

    @model_validator(mode='after')
    def check_start_before_end_date(self) -> Self:
        if self.start_date > self.end_date:
            raise ValueError('end_date must be greater than start_date')
        return self

class GenericError(BaseModel) :
    detail: str = 'Error Description'