from typing import Any
from mcp.server.fastmcp import FastMCP

class MCPPowerServer:
    def __init__(self):
        self.mcp = FastMCP("calculate_power")
        self._setup_tools()

    def _setup_tools(self):
        @self.mcp.tool()
        async def calculate_power(base: float, exponent: float) -> float:
            """
            计算一个数的乘方
            
            Args:
                base: 底数
                exponent: 指数
                
            Returns:
                float: 计算结果
            """
            return base ** exponent

    def run(self, transport='stdio'):
        """运行MCP服务器"""
        self.mcp.run(transport=transport) 