from app import schemas
import pytest
from jose import jwt
from app.config import settings


# All tests need to be INDEPENDENT of each other


def test_create_user(client):
    res = client.post("/users/", json= {"email": "hello@gmail.com", "password": "password123"})
    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data= {"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    payload_id = payload.get("user_id")

    assert test_user["id"] == payload_id
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code",[
    ("jimmy@gmail.com","wrongPassword",403), ("wrongemail","password",403), (None,"passwoed", 422), ("jimmy@gmail.com", None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data= {"username": email, "password": password})
    assert res.status_code == status_code

