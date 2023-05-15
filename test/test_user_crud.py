import datetime

from starlette.testclient import TestClient

from user.crud import user_crud
from main import app
from models import User, UserInfo
from user_info.crud import user_info_crud

client = TestClient(app)
datetime_now = datetime.datetime.now()
username = f'test_user_{datetime_now}'
password = f'test_password_{datetime_now}'
user_data = {'username': username,
             'password': password}


class TestUserCRUD:
    """ basic test case for user basic operations """

    def test_user_firstname_updating(self):
        pass

    def test_user_info_updating(self):
        user = user_crud.create(User(username=username, password_hashed=hash(password)))
        user_id = user.id
        user_info = user_info_crud.read(user_id)
        user_info_updated = user_info_crud.update(UserInfo(id=user_info.id,
                                                           user_id=user_info.user_id,
                                                           first_name='Ivan',
                                                           last_name='Ivanov'))
        assert user_info_updated.first_name == 'Ivan'
        assert user_info_updated.last_name == 'Ivanov'
        user_info_updated = user_info_crud.update(UserInfo(id=user_info.id,
                                                           user_id=user_info.user_id,
                                                           first_name='Ivan',
                                                           last_name='Ivanov2'))
        assert user_info_updated.first_name == 'Ivan'
        assert user_info_updated.last_name == 'Ivanov2'
