import pytest
import requests

BASE_URL = "http://localhost:8000"
SIGNUP_ENDPOINT = f"{BASE_URL}/users/api/v1/signup/"


def test_user_signup():
    """
    Test to verify the user signup API endpoint.
    """
    # Test user data
    user_data = {
        "first_name": "Zee",
        "last_name": "Zee",
        "email": "zeezee@y.com",
        "password1": "TestPass@123",
    }

    # Make signup request
    response = requests.post(SIGNUP_ENDPOINT, json=user_data)

    # Verify successful signup
    assert response.status_code == 201, "Failed to sign up user"

    # Verify response structure
    data = response.json()
    assert "is_success" in data, "Response missing is_success field"
    assert data["is_success"] is True, "Signup was not successful"
    assert "token" in data, "Response missing token field"
    assert isinstance(data["token"], str), "Token should be string"
    assert data["message"] == "Signed up successfully", "Unexpected success message"

    # Test duplicate signup
    response = requests.post(SIGNUP_ENDPOINT, json=user_data)

    # Verify duplicate signup is rejected
    assert response.status_code == 400, "Duplicate signup should be rejected"
    data = response.json()
    assert data["is_success"] is False, "Duplicate signup should not succeed"
    assert "User with this email id already exists!" in data["message"]


# Add signin endpoint
SIGNIN_ENDPOINT = f"{BASE_URL}/users/api/v1/signin/"


def test_user_signin():
    """
    Test to verify the user signin API endpoint.
    """
    # Test user credentials
    credentials = {
        "email": "zeezee@y.com",
        "password": "TestPass@123",
    }

    # Make signin request
    response = requests.post(SIGNIN_ENDPOINT, json=credentials)

    # Verify successful signin
    assert response.status_code == 200, "Failed to sign in"

    # Verify response structure
    data = response.json()
    assert "is_success" in data, "Response missing is_success field"
    assert data["is_success"] is True, "Sign in was not successful"
    assert "token" in data, "Response missing token field"
    assert isinstance(data["token"], str), "Token should be string"

    # Test invalid credentials
    invalid_credentials = {
        "email": "zeezee@y.com",
        "password": "WrongPassword",
    }
    response = requests.post(SIGNIN_ENDPOINT, json=invalid_credentials)

    # Verify invalid signin is rejected
    assert response.status_code == 400, "Invalid signin should be rejected"
    data = response.json()
    assert data["is_success"] is False, "Invalid signin should not succeed"
    assert "Invalid Username or Password" in data["message"]


# Add signout endpoint
SIGNOUT_ENDPOINT = f"{BASE_URL}/users/api/v1/signout/"


def test_user_signout():
    """
    Test to verify the user signout API endpoint.
    """
    # First signin to get auth token
    credentials = {"email": "zeezee@y.com", "password": "TestPass@123"}
    signin_response = requests.post(SIGNIN_ENDPOINT, json=credentials)
    assert signin_response.status_code == 200
    token = signin_response.json()["token"]

    # Set auth header
    headers = {"Authorization": f"Token {token}"}

    # Test signout
    response = requests.post(SIGNOUT_ENDPOINT, headers=headers)

    # Verify successful signout
    assert response.status_code == 200, "Failed to sign out"
    data = response.json()
    assert "is_success" in data, "Response missing is_success field"
    assert data["is_success"] is True, "Sign out was not successful"
    assert "message" in data, "Response missing message field"
    assert "Signed out successfully" in data["message"]

    # Verify token is invalidated by trying to use it again
    response = requests.post(SIGNOUT_ENDPOINT, headers=headers)
    assert response.status_code == 401, "Should not allow reuse of invalidated token"
