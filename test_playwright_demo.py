import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def browser_page():
    """每个测试用例启动一个独立的浏览器页面"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()


def test_login_success(browser_page):
    """测试正确账号登录成功"""
    page = browser_page
    page.goto("https://www.saucedemo.com/")
    page.fill('#user-name', 'standard_user')
    page.fill('#password', 'secret_sauce')
    page.click('#login-button')

    page.wait_for_selector('.inventory_list', timeout=5000)
    assert page.title() == "Swag Labs"
    print("✅ 正确账号登录成功")


def test_login_fail(browser_page):
    """测试错误账号登录失败"""
    page = browser_page
    page.goto("https://www.saucedemo.com/")
    page.fill('#user-name', 'locked_out_user')
    page.fill('#password', 'secret_sauce')
    page.click('#login-button')

    # 等待错误信息出现
    error_msg = page.locator('[data-test="error"]')
    assert error_msg.is_visible()
    assert "locked out" in error_msg.inner_text()
    print("✅ 错误账号登录失败，错误信息正确")


def test_add_to_cart(browser_page):
    """测试登录后添加商品到购物车"""
    page = browser_page
    page.goto("https://www.saucedemo.com/")
    page.fill('#user-name', 'standard_user')
    page.fill('#password', 'secret_sauce')
    page.click('#login-button')
    page.wait_for_selector('.inventory_list', timeout=5000)

    # 点击第一个商品的“Add to cart”按钮
    page.click('[data-test="add-to-cart-sauce-labs-backpack"]')

    # 验证购物车徽章变为1
    cart_badge = page.locator('.shopping_cart_badge')
    assert cart_badge.inner_text() == "1"
    print("✅ 添加商品到购物车成功")
