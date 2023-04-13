import datetime
import uuid
from hashlib import md5
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from service.crud import crud_manager
from service.exceptions import UserNotExistingError, AuthenticationError
from service.models import AccessToken, User, UserDTO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = uuid.uuid4().hex
ALGORITHM = "HS256"


def create_access_token(username: str, expires_delta_minutes: float = 86400) -> AccessToken:
    payload = {
        'sub': username,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=expires_delta_minutes)
    }
    return AccessToken(token=jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM), type='bearer')


def _get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user: UserDTO) -> Optional[User]:
    try:
        user_db = crud_manager.crud_manager(User).read(user.username)
    except UserNotExistingError:
        raise AuthenticationError()
    else:
        if _verify_password(user.password, user_db.password_hashed):
            return user_db
        raise AuthenticationError()
