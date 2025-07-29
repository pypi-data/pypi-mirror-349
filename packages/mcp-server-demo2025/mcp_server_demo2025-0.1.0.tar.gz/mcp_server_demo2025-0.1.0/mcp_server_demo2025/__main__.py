import sys
import datetime
import traceback

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("请先安装 mcp 包: pip install mcp", file=sys.stderr)
    sys.exit(1)

mcp = FastMCP("MCP Demo Server 2025", instructions="这是一个演示用的MCP服务器2025版。")

@mcp.tool()
def hello(name: str = "World") -> str:
    """返回 Hello, {name}!"""
    print(f"调用 hello 工具, name={name}", file=sys.stderr)
    return f"Hello, {name}!"

@mcp.tool()
def get_time() -> str:
    """获取当前时间"""
    now = datetime.datetime.now()
    print("调用 get_time 工具", file=sys.stderr)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def main():
    try:
        print("MCP Demo Server 2025 启动中...", file=sys.stderr)
        mcp.run()
    except Exception as e:
        print(f"运行出错: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 