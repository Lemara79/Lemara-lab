import pytest
from api_client import APIClient
from config import LOGIN_USERNAME, LOGIN_PASSWORD

@pytest.fixture(scope="session")
#是"给这个函数贴个标签"，告诉Pytest："这是一个前置工具，不是普通的测试用例。"
#scope="session" 的意思是"整个测试运行期间只执行一次"。
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
#干什么的：提前把“登录拿 token”这一步准备好了。哪个用例需要token，就在参数里写auth_token，它自动就把token递给你。
#为什么这么干：10个用例都要登录，你不用在10个用例里各写一遍登录代码，只在这里写一次，所有用例都能用。
    response = api_client.post("/auth/login", json=payload)
    assert response.status_code == 201, "登录失败，无法获取 token"
    token = response.json().get('token')
    assert token, "返回数据中没有 token"
    return token