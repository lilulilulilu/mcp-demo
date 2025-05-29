# Prerequisites
- python 3.10 

# Install dependencies
```shell
pip install -e .
```
# Test

## Way 1: install this server locally in Claude Desktop and interact with it right away by running:
```shell
mcp install server.py
```

## Way 2: Test with  MCP Inspector
```shell
mcp dev server.py
```
after MCP inspector started sucessfully:
- open http://127.0.0.1:6274, 
- refill the Command with "mcp", Arguments with "run server.py",
- then click connect, and test the tools, resources, prompts, etc.
![图片描述](images/image.png)

# Reference Doc
- [python sdk](https://github.com/modelcontextprotocol/python-sdk)
- [MCP: Build Rich-Context AI Apps with Anthropic](https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic/)

