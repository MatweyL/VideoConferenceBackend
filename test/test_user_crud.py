import datetime

from starlette.testclient import TestClient

from auth.crud import user_crud
from main import app
from models import User

client = TestClient(app)
datetime_now = datetime.datetime.now()
username = f'test_user_{datetime_now}'
password = f'test_password_{datetime_now}'
user = {'username': username,
        'password': password}


class TestUserCRUD:
    """ basic test case for user basic operations """
    def test_user_firstname_updating(self):
        pass

    def test_user_creation(self):
        user_crud.create(User(username=f'test_user_crud_{datetime.datetime.now()}', password_hashed=hash(password)))
