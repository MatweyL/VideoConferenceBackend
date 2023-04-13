from typing import Optional

from pydantic import BaseModel


class BaseEntity(BaseModel):
    pass


class User(BaseEntity):
    username: str
    password_hashed: str


class UserInfo(User):
    first_name: Optional[str]
    last_name: Optional[str]


class BaseDTOEntity(BaseModel):
    pass


class UserDTO(BaseEntity):
    username: str
    password: str


class UserInfoDRO(UserDTO):
    first_name: Optional[str]
    last_name: Optional[str]


class AccessToken(BaseDTOEntity):
    token: str
    type: str
