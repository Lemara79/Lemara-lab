import pytest
import yaml  #专门用来写配置和测试数据的文件格式
import requests
import os  #专门用来和操作系统打交道
import allure
from logger_config import log  # 导入日志



def load_test_data():
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, "test_data.yaml")  #yaml_path是YAML文件在电脑上的完整地址。

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["login_test_data"]


@pytest.mark.parametrize("test_case", load_test_data())
def test_login_data_driven(test_case):
    log.info(f"开始执行测试用例:{test_case['description']}")

    url = "https://fakestoreapi.com/auth/login"
    payload = {
        "username": test_case["username"],
        "password": test_case["password"]
    }

    with allure.step(f"发送登录请求: {test_case['description']}"):
        response = requests.post(url, json=payload)

    with allure.step(f"验证状态码为 {test_case['expected_status']}"):
        assert response.status_code == test_case["expected_status"]

    print(f"✅ {test_case['description']} - 通过")