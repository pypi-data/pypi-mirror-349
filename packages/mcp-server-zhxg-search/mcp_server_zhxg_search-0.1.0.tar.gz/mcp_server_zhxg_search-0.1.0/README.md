# MCP 搜索服务器

基于 MCP 协议实现的搜索服务，支持关键词搜索和健康状态检查。

## 功能特点

- 支持布尔运算的关键词搜索（OR、AND）
- 支持时间范围过滤
- 支持自定义返回结果数量
- 提供服务健康状态检查

## 快速开始

### 1. 环境要求

- Python 3.12
- NPX

### 2. 启动服务

有两种方式可以提供 API Key：

1. 通过命令行参数：

```shell
npx -y @modelcontextprotocol/inspector uv run ./src/mcp_server_zhxg_search/server.py --api-key <YOUR_API_KEY>
```

2. 通过环境变量：

```shell
export MCP_API_KEY=<YOUR_API_KEY>
npx -y @modelcontextprotocol/inspector uv run ./src/mcp_server_zhxg_search/server.py
```

### 3. 使用示例

#### 搜索示例

输入示例：
```
我想找一些关于人工智能在医疗领域应用的文章
```

关键词格式：
```
人工智能 AND 医疗 AND 应用
```

## API 说明

### 1. simple_search

搜索文档接口，支持以下参数：

- `keywords`: 搜索关键词，支持布尔运算（OR、AND 必须大写）
- `start_time`: 开始时间（可选），格式：YYYY-MM-DD HH:MM:SS
- `end_time`: 结束时间（可选），格式：YYYY-MM-DD HH:MM:SS
- `size`: 返回结果数量（可选），默认为 10

返回数据包含：
- 文章 URL 和类型
- 网站信息（名称、域名）
- 文档内容
- 转发内容（如果有）
- 用户信息（认证状态、用户名）

### 2. health_check

检查服务器健康状态，无需参数。

## 错误处理

服务会在以下情况返回错误信息：
- API 密钥缺失或无效
- 搜索请求失败
- 服务器异常

## 开发说明

如需调试，可使用以下命令启动服务：

```shell
npx -y @modelcontextprotocol/inspector uv run ./src/mcp_server_zhxg_search/server.py --api-key <YOUR_API_KEY>
```

## 注意事项

1. 请确保在启动服务前设置有效的 API Key
2. 布尔运算符（OR、AND）必须使用大写
3. 时间格式必须严格遵循 YYYY-MM-DD HH:MM:SS
