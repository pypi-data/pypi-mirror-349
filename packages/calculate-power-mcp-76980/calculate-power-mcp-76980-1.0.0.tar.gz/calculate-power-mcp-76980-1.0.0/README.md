# MCP Power Server

这是一个基于 Model Context Protocol 的幂运算服务器实现。

## 安装

```bash
pip install mcp-server
```

## 使用方法

### 服务器端

```python
from mcp_server import MCPPowerServer

server = MCPPowerServer()
server.run(transport='stdio')
```

### 客户端

```python
from fastmcp import Client
import asyncio

async def main():
    client = Client("server.py")
    async with client:
        result = await client.call_tool(
            "calculate_power",
            arguments={"base": 8.0, "exponent": 2.5}
        )
        print(f"计算结果: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 功能

- 提供幂运算功能
- 支持浮点数计算
- 使用 stdio 传输协议

## 依赖

- Python >= 3.7
- fastmcp

## 许可证

MIT License