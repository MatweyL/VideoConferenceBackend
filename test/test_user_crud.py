import datetime

from starlette.testclient import TestClient

from main import app

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
