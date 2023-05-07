import datetime
import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(os.path.join(Path(__file__).parent.parent, 'service'))

from main import app


client = TestClient(app)
datetime_now = int(datetime.datetime.now().timestamp())
username = f'test_user_{datetime_now}'
password = f'test_password_{datetime_now}'
user = {'username': username,
        'password': password}


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


class TestUserRegistration:
    """TestUserRegistration tests /users/register"""

    def test_get_request_returns_405(self):
        """registration endpoint does only expect a post request"""
        response = client.get("/users/register")
        assert response.status_code == 405

    def test_post_request_without_body_returns_422(self):
        """body should have username, password and fullname"""
        response = client.post("/users/register")
        assert response.status_code == 422

    def test_post_request_with_improper_body_returns_422(self):
        """all username, password and fullname is required"""
        response = client.post(
            "/users/register",
            json={"username": f"not_existed_user_{datetime.datetime.now().timestamp()}"}
        )
        assert response.status_code == 422

    def test_post_request_with_proper_body_returns_201(self):
        response = client.post(
            "/users/register",
            json=user
        )
        assert response.status_code == 201


class TestUserAuthentication:
    """TestUserAuthentication tests /users/auth"""

    def test_get_request_returns_405(self):
        """login endpoint does only expect a post request"""
        response = client.get('/users/auth')
        assert response.status_code == 405

    def test_post_request_without_body_returns_422(self):
        response = client.post('/users/auth')
        assert response.status_code == 422

    def test_post_request_with_improper_body_returns_422(self):
        response = client.post('/users/auth', json={'username': f'heh_{datetime.datetime.now().timestamp()}'})
        assert response.status_code == 422

    def test_post_request_with_proper_body_returns_200_with_jwt_token(self):
        response = client.post('/users/auth', json={"grant_type": "password", **user})
        assert response.status_code == 200, {"grant_type": "password", **user}


class TestJWTTokenPassing:
    """ Test users/me with jwt passing """
    def test_get_request_with_jwt_token(self):
        client.post('/users/register', json=user)
        response = client.post('/users/auth', json=user)
        assert response.status_code == 200
        response_json = response.json()
        jwt_token = f"{response_json['type']} {response_json['token']}"
        headers = {"Authorization": jwt_token}
        response = client.get('/users/me', headers=headers)
        assert response.status_code == 200
        assert response.json()['user']['username'] == username
