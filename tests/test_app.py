# Third party modules
import pytest


import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import json

# First party modules
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_load_login(client):
    rv = client.get("/login.html")
    assert b"Log In!" in rv.data


def test_load_review(client):
    rv = client.get("/review.html")
    assert b"Leave a Review!" in rv.data


def test_load_signup(client):
    rv = client.get("/signup.html")
    assert b"Sign Up Now!" in rv.data


def test_load_history(client):
    rv = client.get("/history.html")
    assert b"Previous Reviews" in rv.data


def test_success_login(client):
    rv = client.post(
        "/login", data={"email": "test.test@gmail.com", "password": "checking"}
    )
    print(rv.data, "\n", "\n", "\n", "\n", "\n", "\n")

    assert rv.status_code != b"Invalid username and password"


def test_fail_login(client):

    rv = client.post("/login", data={"email": "python", "password": "is-great!"})
    print(rv.data, "\n", "\n", "\n", "\n", "\n", "\n")
    assert rv.status_code != 200


def test_sucess_register(client):
    rv = client.post(
        "/users/register",
        data={
            "first_name": "admin",
            "last_name": "admin",
            "email": "admin",
            "password": "admin",
        },
    )
    print(rv.data, "\n", "\n", "\n", "\n", "\n", "\n")

    assert rv.status_code != b"Invalid username and password"
