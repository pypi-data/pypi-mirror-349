from mcp.server.fastmcp import FastMCP
import random
# 初始化MCP服务器
mcp = FastMCP("SimpleExample")

# 添加工具
@mcp.tool()
async def say_hello(name: str) -> str:
    """一个简单的打招呼工具"""
    return f"Hello, {name}!"

@mcp.tool()
async def roll_dice(sides: int = 6) -> int:
    """掷骰子"""
    return random.randint(1, sides)

# 运行服务器
if __name__ == "__main__":
    mcp.run(transport='stdio')
