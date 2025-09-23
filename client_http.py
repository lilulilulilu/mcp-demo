import asyncio
from urllib.parse import quote
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
from mcp.types import ResourceTemplateReference

# when server is running with streamable-http, use /mcp
server_url = "http://127.0.0.1:8001/mcp" 

async def call_resource():
    async with streamablehttp_client(server_url) as (read, write, get_session_id):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # First, test if server is responding by listing tools
            try:
                tools_result = await session.list_tools()
                print(f"Server is responding. Available tools: {len(tools_result.tools)}")
                for tool in tools_result.tools:
                    print(f"  Tool: {tool.name} - {tool.description}")
            except Exception as e:
                print(f"Error listing tools: {e}")
                return None
            
            # List available resource templates
            try:
                templates = await session.list_resource_templates()
                print(f"Available resource templates: {len(templates.resourceTemplates)}")
                for i, template in enumerate(templates.resourceTemplates):
                    print(f"  {i}: {template.uriTemplate}")
                
                # Use the first available template (should be greeting://{name})
                if templates.resourceTemplates:
                    template = templates.resourceTemplates[0]
                    print(f"Using template: {template.uriTemplate}")
                    
                    # Try using read_resource instead of complete
                    resource_uri = template.uriTemplate.replace("{name}", quote("jack ma"))
                    print(f"Reading resource: {resource_uri}")
                    
                    result = await session.read_resource(resource_uri)
                    print(f"Read resource result: {result}")
                    
                    # complete is not supported in streamable-http
                    completion_result = await session.complete(
                        ref=ResourceTemplateReference(type="ref/resource", uri=template.uriTemplate), 
                        argument={"name": "name", "value": "jack ma"}
                    )
                    print(f"Complete result: {completion_result}") # nError with resources: Method not found
                    return completion_result
                else:
                    print("No resource templates available")
                    return None
            except Exception as e:
                print(f"Error with resources: {e}")
                return None

asyncio.run(call_resource())
 