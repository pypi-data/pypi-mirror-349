FROM python:3.11-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# 安装依赖
COPY pyproject.toml /app/
COPY README.md /app/
COPY LICENSE /app/

# 安装项目
RUN pip install --no-cache-dir .

# 复制应用代码
COPY . /app/

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "weather_mcp.main:app", "--host", "0.0.0.0", "--port", "8000"]