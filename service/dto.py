from typing import Optional

from pydantic import BaseModel


class BaseDTOEntity(BaseModel):
    pass


class UserCredentialsDTO(BaseDTOEntity):
    username: str
    password: str
    grant_type: str = "password"


class UserInfoDTO(BaseDTOEntity):
    first_name: Optional[str]
    last_name: Optional[str]


class UserDTO(UserInfoDTO):
    username: str


class AccessToken(BaseDTOEntity):
    token: str
    type: str


class AccessTokenPayload(BaseDTOEntity):
    username: str
