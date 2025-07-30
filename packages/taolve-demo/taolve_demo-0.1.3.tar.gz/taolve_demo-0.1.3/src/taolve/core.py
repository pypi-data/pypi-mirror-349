from typing import Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("taolve-demo")

@mcp.tool(description="将自定义的图片或者文案推送微信社群")
def promote(send_content: int) -> str:
    return "[自定义内容已推送]" + send_content


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')