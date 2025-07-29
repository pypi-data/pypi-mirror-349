# 天气查询MCP服务部署指南

本文档提供了部署和运行天气查询MCP服务的详细说明。

## 目录

- [环境要求](#环境要求)
- [安装方法](#安装方法)
  - [从PyPI安装](#从pypi安装)
  - [从源码安装](#从源码安装)
- [配置说明](#配置说明)
  - [环境变量配置](#环境变量配置)
  - [.env文件配置](#env文件配置)
- [运行服务](#运行服务)
  - [命令行运行](#命令行运行)
  - [使用Docker运行](#使用docker运行)
  - [作为WSGI应用运行](#作为wsgi应用运行)
- [验证部署](#验证部署)
- [MCP集成](#mcp集成)
- [故障排除](#故障排除)

## 环境要求

- Python 3.8 或更高版本
- 和风天气API账号和密钥

## 安装方法

### 从PyPI安装

```bash
pip install weather-mcp
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/zishu-co/weather-mcp.git
cd weather-mcp

# 安装依赖
pip install -e .
```

## 配置说明

在运行服务前，需要配置和风天气API的相关参数。

### 环境变量配置

设置以下环境变量：

```bash
export WEATHER_PRIVATE_KEY="你的私钥"
export WEATHER_PROJECT_ID="你的项目ID"
export WEATHER_KEY_ID="你的密钥ID"
export WEATHER_API_HOST="你的API主机地址"
export WEATHER_BEARER_TOKEN="你的Bearer令牌" # 用于MCP接口认证
```

### .env文件配置

或者，创建一个`.env`文件在项目根目录：

```
WEATHER_PRIVATE_KEY=你的私钥
WEATHER_PROJECT_ID=你的项目ID
WEATHER_KEY_ID=你的密钥ID
WEATHER_API_HOST=你的API主机地址
WEATHER_BEARER_TOKEN=你的Bearer令牌

# 可选配置
HOST=0.0.0.0
PORT=8000
DEBUG=True
JWT_DEFAULT_EXPIRY=900
```

## 运行服务

### 命令行运行

安装后，可以直接使用命令行工具启动服务：

```bash
weather-mcp
```

或者使用Python模块：

```bash
python -m weather_mcp
```

### 使用Docker运行

```bash
# 构建Docker镜像
docker build -t weather-mcp .

# 运行容器
docker run -p 8000:8000 \
  -e WEATHER_PRIVATE_KEY="你的私钥" \
  -e WEATHER_PROJECT_ID="你的项目ID" \
  -e WEATHER_KEY_ID="你的密钥ID" \
  -e WEATHER_API_HOST="你的API主机地址" \
  -e WEATHER_BEARER_TOKEN="你的Bearer令牌" \
  weather-mcp
```

### 作为WSGI应用运行

在生产环境中，可以使用Gunicorn或Uvicorn作为WSGI服务器：

```bash
uvicorn weather_mcp.main:app --host 0.0.0.0 --port 8000
```

或者使用Gunicorn：

```bash
gunicorn weather_mcp.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 验证部署

服务启动后，可以通过以下方式验证：

1. 访问API文档：`http://服务器地址:端口/docs`
2. 测试主页接口：`curl http://服务器地址:端口/`

## MCP集成

本服务实现了MCP接口，可以被支持MCP的AI助手直接调用。

1. 在AI助手中配置MCP服务：
   - 服务URL：`http://服务器地址:端口`
   - 认证方式：Bearer Token
   - Token值：配置的`WEATHER_BEARER_TOKEN`值

2. 调用示例：
   ```
   使用天气MCP查询北京的天气
   ```

## 故障排除

### 常见问题

1. **API密钥错误**
   - 确认环境变量或.env文件中的密钥信息正确
   - 检查和风天气账号是否有效

2. **服务无法启动**
   - 检查端口是否被占用
   - 确认Python版本是否满足要求

3. **MCP调用失败**
   - 验证Bearer Token是否正确
   - 检查网络连接是否正常

如有其他问题，请提交Issue到GitHub仓库。