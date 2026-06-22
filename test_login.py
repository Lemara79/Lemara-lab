import pytest
import allure

def test_login_success(api_client):
    payload = {
        "username": "mor_2314",
        "password": "83r5^_"
    }
    with allure.step("发送登录请求"):
        response = api_client.post("/auth/login", json=payload)
    with allure.step("验证登录结果"):
        assert response.status_code == 201
        assert 'token' in response.json()

def test_login_fail(api_client):
    payload = {
        "username": "mor_2314",
        "password": "wrong_password"
    }
    with allure.step("发送错误登录请求"):
        response = api_client.post("/auth/login", json=payload)
    with allure.step("验证返回401"):
        assert response.status_code == 401

def test_get_user_info(api_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    with allure.step("发送获取用户信息请求"):
        response = api_client.get("/users/1", headers=headers)
    with allure.step("验证用户信息"):
        assert response.status_code == 200
        assert response.json().get('id') == 1
