from typing import Optional

from pydantic import BaseModel


class BaseEntity(BaseModel):
    pass


class User(BaseEntity):
    username: str
    password: str


class UserInfo(User):
    first_name: Optional[str]
    last_name: Optional[str]




