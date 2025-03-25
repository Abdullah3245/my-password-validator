# test_main.py
import pytest
from main import app


@pytest.fixture
def client():
    """
    Pytest fixture that creates a Flask test client from the 'app' in main.py.
    """
    with app.test_client() as client:
        yield client


def test_root_endpoint(client):
    """
    Test the GET '/' endpoint to ensure it returns
    the greeting and a 200 status code.
    """
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello from my Password Validator!" in resp.data


# Not that this test only makes sense for the starter code,
# in practice we would not test for a 501 status code!

def test_incorrect_passoword(client):
    """
    Test the POST '/v1/checkPassword' endpoint to ensure
    it returns false when incorrect password.
    """
    resp = client.post("/v1/checkPassword", json={"password": "whatever"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("reason") == "Password must contain at least one uppercase letter."
    assert data.get("valid") is False

def test_correct_password(client):
    """
    Test the POST '/v1/checkPassword' endpoint to ensure
    it returns true when correct password.
    """
    resp = client.post("/v1/checkPassword", json={"password": "Abdullah1234!"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("reason") == ""
    assert data.get("valid") is True