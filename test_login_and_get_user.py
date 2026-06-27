import pytest
import allure
import yaml
import os
from api_client import APIClient

def load_test_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, "test_data.yaml")
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["login_test_data"]

@pytest.mark.parametrize("test_case", load_test_data())
def test_login_and_get_user(test_case):
    username = test_case["username"]
    password = test_case["password"]
    expected_status = test_case["expected_status"]

    client = APIClient()

    with allure.step(f"登录：{username}"):
        login_payload = {
            "username": username,
            "password": password
        }
        login_response = client.post("/auth/login", json=login_payload)
        assert login_response.status_code == expected_status, f"登录失败，状态码为{login_response.status_code}"

    if expected_status == 201:
        token = login_response.json().get("token")
        assert token is not None, "登录响应中没有token"

        with allure.step(f"获取用户信息，token前20字符：{token[:20]}..."):
            headers = {"Authorization": f"Bearer {token}"}
            user_response = client.get("/users/1", headers=headers)
            assert user_response.status_code == 200, f"获取用户信息失败，状态码为{user_response.status_code}"

            user_data = user_response.json()
            assert user_data.get("id") == 1, f"用户ID不匹配，期望1，实际{user_data.get('id')}"
            print(f"✅ 用户信息获取成功，用户名：{user_data.get('username')}")