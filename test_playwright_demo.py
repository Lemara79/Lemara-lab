from playwright.sync_api import sync_playwright
import pytest

@pytest.fixture(scope="function")
def browser_page():
    """每个测试用例启动一个独立的浏览器页面"""
    with sync_playwright() as p:
        browser =p.chromium.launch(headless=False)
        page=browser.new_page()
        yield page
        browser.close()

def test_sauce_login(browser_page):
    """测试 Sauce Demo 登录功能"""
    page=browser_page
    page.goto("https://www.saucedemo.com/")
    print("✅ 页面加载完成")

    page.fill('#user-name','standard_user')
    page.fill('#password','secret_sauce')
    page.click('#login-button')

    # 等待登录成功，检查商品列表是否出现
    page.wait_for_selector('.inventory_list',timeout=5000)
    assert page.title()=="Swag Labs","登录后标题不匹配"
    print("✅ 登录成功")

