# 接口自动化测试框架

## 项目简介
基于 Python + Pytest 的接口自动化测试框架，支持数据驱动、日志记录、测试报告和自动清理。

## 技术栈
- Python 3.11
- Pytest
- Requests
- PyYAML
- loguru
- pytest-html
- playwright

## 项目结构
- api_client.py # 封装 HTTP 请求
- config.py # 配置文件
- conftest.py # Pytest fixture
- logger_config.py # 日志配置
- test_data.yaml # 测试数据
- test_login_data_driven.py # 数据驱动登录测试
- test_add_to_cart.py # 购物车流程测试
- test_grade_query.py # 教务系统成绩查询（已实现，待网络恢复后验证）
- test_playwright_demo.py # UI 自动化测试（登录成功、登录失败、添加购物车）

## 运行测试

```bash
pytest test_login_data_driven.py -v -s
pytest test_add_to_cart.py -v -s
```

## 接口测试
```bash
pytest test_login_data_driven.py -v -s
pytest test_add_to_cart.py -v -s
```
## UI测试
```bash
pytest test_playwright_demo.py -v -s
```

## 测试报告

### 1.接口测试报告
```bash
pytest test_login_data_driven.py --html=report.html --self-contained-html
```

### 2.UI测试报告
```bash
pytest test_playwright_demo.py --html=ui_report.html --self-contained-html
```
## 项目亮点
- 数据驱动设计：测试数据与代码分离
- 自动清理：使用 yield fixture 保持测试环境干净
- 日志与报告：集成 loguru 和 pytest-html
- 可复用客户端：封装 APIClient，避免重复编写请求代码