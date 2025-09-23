from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.types import CompletionArgument, PromptReference, ResourceTemplateReference

# Create server parameters for remote connection of mcp server
server_url = "http://127.0.0.1:8001/sse"


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

async def list_resources():
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # List available resources
            templates = await session.list_resource_templates()
            resources = templates.resourceTemplates
            return resources


async def list_prompts():
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # List available prompts
            prompts_result = await session.list_prompts()
            prompts = prompts_result.prompts
            return prompts



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

    result = asyncio.run(list_resources())
    print(f'\n1. resources:\n {result}')

    result = asyncio.run(list_prompts())
    print(f'\n2. prompts:\n {result}')

    result = asyncio.run(list_tools())
    print(f'\n3. tools:\n {result}')
    
    result = asyncio.run(execute_tool("add", {"a": 1, "b": 2}))
    print(f'\n4. execute_tool:\n {result}')