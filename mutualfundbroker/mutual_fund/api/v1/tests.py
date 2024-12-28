import pytest
import requests

BASE_URL = "http://localhost:8000"
SIGNIN_ENDPOINT = f"{BASE_URL}/users/api/v1/signin/"
MUTUAL_FUNDS_ENDPOINT = f"{BASE_URL}/users/api/v1/mutual-funds/"
HEADERS = {}


@pytest.fixture
def auth_token():
    """
    Fixture to get authentication token and set it in headers.
    """
    # Test user credentials
    credentials = {
        "email": "test@gmail.com",
        "password": "Stark@123",
    }

    # Get auth token
    response = requests.post(SIGNIN_ENDPOINT, json=credentials)

    # Verify successful signin
    assert response.status_code == 200, "Failed to sign in"

    data = response.json()
    assert "token" in data, "No token in response"
    assert data["is_success"] is True, "Sign in was not successful"

    # Set token in headers
    HEADERS["Authorization"] = f"Token {data['token']}"

    return data["token"]


def test_mutual_fund_families(auth_token):
    """
    Test to verify the mutual fund families API endpoint.
    """
    response = requests.get(
        f"{BASE_URL}/mutualfund/api/v1/fund-families/", headers=HEADERS
    )

    # Verify successful response
    assert response.status_code == 200, "Failed to get mutual fund families"

    # Verify response structure
    data = response.json()
    assert "is_success" in data, "Response missing is_success field"
    assert data["is_success"] is True, "API request was not successful"
    assert "mf_houses" in data, "Response missing mf_houses field"

    # Verify fund families data structure
    fund_families = data["mf_houses"]
    assert isinstance(fund_families, list), "Fund families should be a list"

    if len(fund_families) > 0:
        # Verify structure of individual fund family
        assert isinstance(fund_families[0], str), "Fund family name should be string"


def test_mutual_fund_schemes(auth_token):
    """
    Test to verify the mutual fund schemes API endpoint for a specific fund family.
    """
    # First get fund families to use a real fund family name
    response = requests.get(
        f"{BASE_URL}/mutualfund/api/v1/fund-families/", headers=HEADERS
    )

    assert response.status_code == 200, "Failed to get fund families"
    fund_families = response.json()["mf_houses"]
    assert len(fund_families) > 0, "No fund families available for testing"

    # Use the first fund family for testing schemes
    fund_family_name = fund_families[0]

    # Test schemes endpoint with the fund family name
    response = requests.get(
        f"{BASE_URL}/mutualfund/api/v1/fund-schemes/?fund_family={fund_family_name}",
        headers=HEADERS,
    )

    # Verify successful response
    assert response.status_code == 200, "Failed to get mutual fund schemes"

    # Verify response structure
    data = response.json()
    assert "is_success" in data, "Response missing is_success field"
    assert data["is_success"] is True, "API request was not successful"
    assert "schemes" in data, "Response missing schemes field"

    # Verify schemes data structure
    schemes = data["schemes"]
    assert isinstance(schemes, list), "schemes should be a list"

    if len(schemes) > 0:
        # Verify structure of individual schema
        schema = schemes[0]
        assert "scheme_code" in schema, "scheme_code missing"
        assert "scheme_name" in schema, "scheme_name missing"
        assert "net_asset_value" in schema, "net_asset_value missing"
        assert isinstance(schema["scheme_code"], str), "Schema_code should be integer"
        assert isinstance(schema["scheme_name"], str), "Schema_name should be string"
        assert isinstance(
            schema["net_asset_value"], int
        ), "net_asset_value should be string"
