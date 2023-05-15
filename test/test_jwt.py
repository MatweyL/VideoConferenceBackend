import datetime
import sys

from fastapi.testclient import TestClient

from service.user.service import create_access_token, get_jwt_token_payload

from service.main import app


client = TestClient(app)
datetime_now = datetime.datetime.now()
username = f'test_user_{datetime_now}'
password = f'test_password_{datetime_now}'
user = {'username': username,
        'password': password}


def test_jwt_creation_and_jwt_payload_extraction():
    token = create_access_token(username)
    access_token_payload = get_jwt_token_payload(token.token)
    assert access_token_payload.username == username


