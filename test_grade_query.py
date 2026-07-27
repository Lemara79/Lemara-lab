import pytest
import requests
import yaml
import os
import allure


def load_grade_test_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, "test_data.yaml")
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["grade_query_data"]


@pytest.fixture(scope="session")
def logged_session():
    """登录教务系统，返回带登录态的 session"""
    login_url = "https://jw.gxstnu.edu.cn/jsxsd/xk/LoginToXk"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://jw.gxstnu.edu.cn/jsxsd/xk/LoginToXk",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {
        "loginMethod": "LoginToXk",
        "userLanguage": "0",
        "userAccount": "2405020119",
        "userPassword": "",
        "encoded": " 从浏览器重新抓取 encoded 值"
    }
    session = requests.Session()
    session.get(login_url, headers=headers)
    response = session.post(login_url, data=payload, headers=headers)
    assert response.status_code == 200, "登录失败"
    return session


@pytest.mark.parametrize("grade_data", load_grade_test_data())
def test_grade_query(logged_session, grade_data):
    """数据驱动：查询不同学期的成绩"""
    grade_url = "https://jw.gxstnu.edu.cn/jsxsd/kscj/cjcx_list"
    params = {
        "pageNum": grade_data["pageNum"],
        "pageSize": grade_data["pageSize"],
        "kksj": grade_data["kksj"],
        "kcxz": "",
        "kcxs": "",
        "kcmc": "",
        "xsf": "all",
        "xsfxscq": 1
    }

    with allure.step(f"查询成绩：{grade_data['description']}"):
        response = logged_session.get(grade_url, params=params)

    with allure.step("验证查询结果"):
        assert response.status_code == 200
        # 如果返回的是 JSON，可以进一步解析
        # 如果返回的是 HTML，检查是否包含“成绩”或“课程”
        assert "成绩" in response.text or "课程" in response.text

    print(f"✅ {grade_data['description']} 查询成功")