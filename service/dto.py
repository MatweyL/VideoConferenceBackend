from typing import Optional

from pydantic import BaseModel


class BaseDTOEntity(BaseModel):
    pass


class UserDTO(BaseDTOEntity):
    username: str
    password: str


class UserInfoDTO(BaseDTOEntity):
    first_name: Optional[str]
    last_name: Optional[str]


class AccessToken(BaseDTOEntity):
    token: str
    type: str
