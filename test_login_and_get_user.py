#这个文件目的：测一个完整的业务流程——登录→获取用户信息
import pytest #提供框架
import allure #提供测试报告步骤
import yaml #读取这个文件的测试数据
import os #处理路径
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
        assert len(token) > 0, "token为空字符串"

        headers = {"Authorization": f"Bearer {token}"}
        user_response = client.get("/users/1", headers=headers)
        assert user_response.status_code == 200, f"获取用户信息失败，状态码为{user_response.status_code}"

        user_data = user_response.json()
        assert 'id' in user_data, "用户信息中没有id字段"
        assert isinstance(user_data.get('id'), int), f"id字段类型不是整数，实际为{type(user_data.get('id'))}"
        assert user_data.get('id') == 1, f"用户ID不匹配，期望1，实际{user_data.get('id')}"
        assert 'username' in user_data, "用户信息中没有username字段"
        assert user_data.get('username') == 'johnd', f"用户名不匹配，期望johnd，实际{user_data.get('username')}"

        print(f"✅ 用户信息获取成功，用户名：{user_data.get('username')}")