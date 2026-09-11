# 使用官方 Python 镜像作为基础
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件（如果有 requirements.txt）
COPY requirements.txt .

# 安装依赖（包括 Pytest 和 Playwright）
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

# 复制项目代码
COPY . .

# 运行测试命令
CMD ["python", "-m", "pytest", "test_login_data_driven.py", "-v"]