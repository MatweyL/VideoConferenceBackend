import datetime
from typing import Optional, Union

from pydantic import BaseModel


class BaseDTOEntity(BaseModel):
    created: Optional[datetime.datetime]

    class Config:
        arbitrary_types_allowed = True


class UserInfoDTO(BaseDTOEntity):
    first_name: Optional[str]
    last_name: Optional[str]


class UserDTO(BaseDTOEntity):
    username: str


class UserVerboseInfoDTO(BaseDTOEntity):
    user: UserDTO
    user_info: UserInfoDTO


class UserCredentialsDTO(BaseDTOEntity):
    username: str
    password: str
    grant_type: str = "password"

