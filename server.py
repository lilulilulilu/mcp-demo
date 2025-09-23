# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo", port=8001, host="0.0.0.0")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool(description="Subtract two numbers")
def sub(a: int, b: int) -> int:
    return a - b


@mcp.tool(description="Multiply two numbers")
def mul(a: int, b: int) -> int:
    return a * b
    


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.resource("file://documents/{name}")
def read_document(name: str) -> str:
    """Read a document by name."""
    # This would normally read from disk
    return f"Content of {name}"


@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"


if __name__ == "__main__":
    mcp.run(transport="sse") # or mcp.run_sse_async()
    # mcp.run(transport="streamable-http")
   

'''
we can also run the server with stdio transport
1. mcp.run(transport="stdio")
执行python client.py时，客户端会自动启动服务器进程，不需要单独启动服务器
2. mcp.run(transport="sse")
执行python client_remote.py时，客户端访问的remote server，需提前执行python server.py启动服务器
'''
