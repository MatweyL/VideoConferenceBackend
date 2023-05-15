import datetime
from typing import Optional

from fastapi import Depends
from jose import jwt, JWTError

from user.crud import user_crud
from user.errors import UserNotExistingError, AuthenticationError
from user.schemas import UserCredentialsDTO, AccessTokenPayload, AccessToken
from core import SECRET_KEY, ALGORITHM, pwd_context, oauth2_scheme
from models import User
from schemas import UserDTO


def create_user(user: UserCredentialsDTO) -> UserDTO:
    user_to_create = User(username=user.username, password_hashed=get_password_hash(user.password))
    user_db: User = user_crud.create(user_to_create)
    return UserDTO(username=user_db.username)


def create_access_token(username: str, expires_delta_minutes: float = 86400) -> AccessToken:
    payload = {
        'sub': AccessTokenPayload(username=username).json(),
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=expires_delta_minutes)
    }

    return AccessToken(token=jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM), type='bearer')


def get_jwt_token_payload(token: str) -> AccessTokenPayload:
    return AccessTokenPayload.parse_raw(jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get('sub'))


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_credentials(user: UserCredentialsDTO) -> Optional[User]:
    try:
        user_db = user_crud.read(user.username)
    except UserNotExistingError:
        raise AuthenticationError()
    else:
        if _verify_password(user.password, user_db.password_hashed):
            return user_db
        raise AuthenticationError()


def get_user_by_jwt_token(token: str = Depends(oauth2_scheme)) -> User:
    try:
        access_token_payload = get_jwt_token_payload(token)
    except JWTError:
        raise AuthenticationError()
    else:
        username: str = access_token_payload.username
        try:
            user_db: User = user_crud.read(username)
        except UserNotExistingError:
            raise AuthenticationError()
        else:
            return user_db
