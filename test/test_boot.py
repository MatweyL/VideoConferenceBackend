import datetime

from fastapi.testclient import TestClient

from service.main import app

client = TestClient(app)


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
            json={"username": f"random_user_{datetime.datetime.now().timestamp()}", "password": "heh555heh"}
        )
        assert response.status_code == 201
