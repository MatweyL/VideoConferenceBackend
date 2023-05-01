from typing import Optional

from pydantic import BaseModel


class BaseDTOEntity(BaseModel):
    pass


class UserInfoDTO(BaseDTOEntity):
    first_name: Optional[str]
    last_name: Optional[str]


class UserDTO(UserInfoDTO):
    username: str
