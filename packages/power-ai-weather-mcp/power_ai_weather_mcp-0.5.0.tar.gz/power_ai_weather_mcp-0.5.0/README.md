# MCP Weather Service (Internal Use Only)

基于 Model Context Protocol (MCP)的天气服务实现（仅限内部使用）

## 功能特性

- 实时天气查询
- 天气预报（小时级和天级）
- 空气质量查询
- 生活指数建议
- 日出日落时间
- 气象灾害预警
- 台风信息
- 降水预报

## MCP 使用

### 安装 uv

uv 是一款高性能的 python 环境管理工具，可以参考[官方教程](https://github.com/astral-sh/uv)安装并熟悉使用。

### MCP 配置

首先配置环境变量 UV_INDEX、WEATHER_ENDPOINT、APP_ID、APP_SECRET：

```bash
export UV_INDEX=xxxx
export WEATHER_ENDPOINT=xxxx
export APP_ID=xxxx
export APP_SECRET=xxxx
```

然后，使用 uvx 启动 MCP 服务，服务将通过 streamable-http 协议在 http://localhost:8000/mcp 启动。

```
uvx power-ai-weather-mcp
```

## 数据结构说明

服务返回的数据使用了以字段描述为键（key）的字典结构，这样能更直观地理解返回数据的含义。例如：

```json
{
  "天气状况": "晴",
  "温度": 25.6,
  "体感温度": 24.8,
  "相对湿度": 45
}
```

而不是传统的以字段名为键的结构：

```json
{
  "text": "晴",
  "temperature": 25.6,
  "feels_like": 24.8,
  "humidity": 45
}
```

## 许可证

MIT License
