from typing import Optional

from pydantic import BaseModel


class BaseEntity(BaseModel):
    pass


class User(BaseEntity):
    username: str
    password_hashed: Optional[str]


class UserInfo(BaseEntity):
    first_name: Optional[str]
    last_name: Optional[str]
