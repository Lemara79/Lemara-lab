import requests
import allure


def test_jw_login():
    url = "https://jw.gxstnu.edu.cn/jsxsd/xk/LoginToXk"

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
        "encoded": "MTj3EQ6ZwP1N97aT2MAh9y74MMTDooiE9MJxcbOe83QX6=o08=4A2%0m%72%g2UdTr5Fo0y34eMAmT5Uj48zXc01jj6RH08iNU8EXuMkc27j4dHTkdp4p811OmL0G48g50cH6AD7Af=cx%35%W3%Y28I8WA9y=3pS=f9"
    }

    session = requests.Session()

    with allure.step("发送教务系统登录请求"):
        session.get("https://jw.gxstnu.edu.cn/jsxsd/xk/LoginToXk", headers=headers)
        response = session.post(url, data=payload, headers=headers)

    with allure.step("验证登录结果"):
        print(f"状态码: {response.status_code}")
        assert response.status_code ==200

        #访问成绩查询接口
    with allure.step("获取考试成绩"):
        grade_url="https://jw.gxstnu.edu.cn/jsxsd/kscj/cjcx_list"
        params={
            "pageNum":1,
            "pageSize": 20,
            "kksj":"2025-2026-2",
            "kcxz":"",
            "kcxs":"",
            "kcmc":"",
            "xsf":"all",
            "xsfxscq":1

        }
        grade_response=session.get(grade_url,headers=headers,params=params)
        print(f"成绩查询状态码：{grade_response.status_code}")
        assert grade_response.status_code==200
        print(f"返回内容（前500字符）：{grade_response.text[:500]}")

    print("✅ 教务系统登录测试完成,且成功后访问成绩查询接口")