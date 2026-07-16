import pytest
import allure
@pytest.mark.usefixtures("logged_in_client_with_cleanup")
def test_add_to_cart(logged_in_client_with_cleanup):
    client, token, headers = logged_in_client_with_cleanup

    cart_payload = {
        "userId": 1,
        "date": "2026-07-12",
        "products": [
            {"productId": 1, "quantity": 1}
        ]
    }

    with allure.step("添加商品到购物车"):
        response = client.post("/carts", json=cart_payload, headers=headers)

    with allure.step("验证添加购物车成功"):
        assert response.status_code == 201, f"添加购物车失败，状态码为 {response.status_code}"
        cart_data = response.json()

        assert 'id' in cart_data, "返回数据中没有id字段"
        assert 'userId' in cart_data, "返回数据中没有userId字段"
        assert 'products' in cart_data, "返回数据中没有products字段"

        assert cart_data.get('userId') == 1, f"userId不匹配，期望1，实际 {cart_data.get('userId')}"
        assert len(cart_data.get('products')) == 1, f"products数量不匹配，期望1，实际 {len(cart_data.get('products'))}"

        product = cart_data['products'][0]
        assert product.get('productId') == 1, f"productId不匹配，期望1，实际 {product.get('productId')}"
        assert product.get('quantity') == 1, f"quantity不匹配，期望1，实际 {product.get('quantity')}"

    print("✅ 添加购物车测试通过")