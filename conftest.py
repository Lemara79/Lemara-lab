import pytest
from requests import delete
from api_client import APIClient
from config import LOGIN_USERNAME, LOGIN_PASSWORD
import  yaml
import os
@pytest.fixture(scope="session")
def api_client():
    """返回一个可复用的 API 客户端"""
    return APIClient()

#专门用来读取购物车测试的登录数据
def load_cart_login_data():
    current_dir=os.path.dirname(os.path.abspath(__file__))
    yaml_path=os.path.join(current_dir,"test_data.yaml")
    with open(yaml_path,"r",encoding="utf-8")as f:
        data=yaml.safe_load(f)
        return data["cart_login_data"]

@pytest.fixture(scope="session")
def auth_token(api_client):
    """自动登录，返回 token（所有测试用例共享）"""
    login_data=load_cart_login_data()
    payload = {
        "username":login_data["username"],
        "password": login_data["password"]
    }
    response = api_client.post("/auth/login", json=payload)
    assert response.status_code == 201, "登录失败，无法获取 token"
    token = response.json().get('token')
    assert token, "返回数据中没有 token"
    return token

@pytest.fixture#告诉Pytest这是一个前置/后置处理器
def logged_in_client_with_cleanup(api_client,auth_token):
    client=api_client
    token=auth_token
    headers = {"Authorization": f"Bearer {token}"}#构造请求头，把token放进去
    yield client,token,headers#把这三个值传给测试用例，测试用例在这里执行
    response = client.get("/carts", headers=headers)#测试结束后，获取该用户的所有购物车列表
    if response.status_code==200:
        carts=response.json()
        for cart in carts:
            if cart.get('userId')==1:
                delete_response=client.delete(f"/carts/{cart['id']}",headers=headers)
                if delete_response.status_code==200:
                    print(f"✅ 自动清理：购物车 {cart['id']} 已删除")

