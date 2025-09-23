import asyncio
import re
from urllib.parse import quote
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
from mcp.types import ResourceTemplateReference

# when server is running with sse, use /sse
server_url = "http://127.0.0.1:8001/sse"

async def call_all():
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
        
            try:
                await call_tools(session)
                print("\n--------------------------------\n")
                await call_resource_templates(session)
                print("\n--------------------------------\n")
                await call_prompts(session)
                               
            except Exception as e:
                print(f"Error with resources: {e}")
                return None


async def call_resource_templates(session):
    templates = await session.list_resource_templates()
    print(f"Available resource templates: {len(templates.resourceTemplates)}")
    for i, template in enumerate(templates.resourceTemplates):
        print(f"  {i}: {template.uriTemplate}")
    
    # Use the first available template (should be greeting://{name})
    if templates.resourceTemplates:
        template = templates.resourceTemplates[0]
        print(f"Using template: {template.uriTemplate}")
        resource_uri = template.uriTemplate.replace("{name}", quote("jack ma"))
        print(f"Reading resource uri: {resource_uri}")
        
        result = await session.read_resource(resource_uri) 
        print(f"Read resource result: {result}")
    else:
        print("No resource templates available")



async def call_prompts(session):
    # List available prompts
    try:
        prompts_result = await session.list_prompts()
        print(f"Available prompts: {len(prompts_result.prompts)}")
        for i, prompt in enumerate(prompts_result.prompts):
            print(f"  {i}: {prompt.name} - {prompt.description}")
        
        # Try to get a prompt
        if prompts_result.prompts:
            prompt = prompts_result.prompts[0]
            print(f"\nTrying to get prompt: {prompt.name}")
            
            result = await session.get_prompt(
                name=prompt.name,
                arguments={"code": "print('hello world')"}
            )
            print(f"Prompt result: {result}")
            
    except Exception as e:
        print(f"Prompt method failed: {e}")


async def call_tools(session):
    tools_result = await session.list_tools()
    print(f"Server is responding. Available tools: {len(tools_result.tools)}")
    for tool in tools_result.tools:
        print(f"  Tool: {tool.name} - {tool.description}")
    
    result = await session.call_tool("add", arguments={"a": 1, "b": 2})
    print(f"Tool result: {result}")


if __name__ == "__main__":
    asyncio.run(call_all())
