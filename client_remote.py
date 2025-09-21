from mcp import ClientSession
from mcp.client.sse import sse_client

# Create server parameters for remote connection of mcp server
server_url = "http://127.0.0.1:8000/sse"


async def list_tools():
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools_result = await session.list_tools()
            tools = tools_result.tools
            # convert tools to a dictionary
            available_tools = []
            for tool in tools:
                available_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    }
                })
                
            return available_tools    


async def execute_tool(tool_name: str, arguments: dict):
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # Call a tool
            result = await session.call_tool(tool_name, arguments=arguments)
            return result.content


if __name__ == "__main__":
    import asyncio

    result = asyncio.run(list_tools())
    print(f'result:\n {result}')
    
    result = asyncio.run(execute_tool("add", {"a": 1, "b": 2}))