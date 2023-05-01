from schemas import BaseDTOEntity


class UserCredentialsDTO(BaseDTOEntity):
    username: str
    password: str
    grant_type: str = "password"


class AccessToken(BaseDTOEntity):
    token: str
    type: str


class AccessTokenPayload(BaseDTOEntity):
    username: str
