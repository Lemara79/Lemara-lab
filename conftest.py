import pytest
from api_client import APIClient
from config import LOGIN_USERNAME, LOGIN_PASSWORD

@pytest.fixture(scope="session")
def api_client():
    """返回一个可复用的 API 客户端"""
    return APIClient()

@pytest.fixture(scope="session")
def auth_token(api_client):
    """自动登录，返回 token（所有测试用例共享）"""
    payload = {
        "username": LOGIN_USERNAME,
        "password": LOGIN_PASSWORD
    }
    response = api_client.post("/auth/login", json=payload)
    assert response.status_code == 201, "登录失败，无法获取 token"
    token = response.json().get('token')
    assert token, "返回数据中没有 token"
    return token