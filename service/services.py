import datetime
from typing import Optional, Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from crud import crud_manager
from dto import AccessToken, UserCredentialsDTO, UserDTO, AccessTokenPayload
from exceptions import UserNotExistingError, AuthenticationError
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth")
SECRET_KEY = "q34t8ghavejdkzSFPODGBIDNJK4982AWDQDECNWIAEFNJCWEIFUIwnevjsdkxdaeE"
ALGORITHM = "HS256"


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
        user_db = crud_manager.crud(User).read(user.username)
    except UserNotExistingError:
        raise AuthenticationError()
    else:
        if _verify_password(user.password, user_db.password_hashed):
            return user_db
        raise AuthenticationError()


def get_user_by_jwt_token(token: str = Depends(oauth2_scheme)):
    try:
        access_token_payload = get_jwt_token_payload(token)
    except JWTError:
        raise AuthenticationError()
    else:
        username: str = access_token_payload.username
        try:
            user_db: User = crud_manager.crud(User).read(username)
        except UserNotExistingError:
            raise AuthenticationError()
        else:
            user_dto = UserDTO.parse_obj(user_db)
            return user_dto
