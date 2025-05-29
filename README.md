# Prerequisites
- python 3.10 

# Install dependencies
```shell
pip install -e .
```


# Test

## Way 1: Test locally with Claude Desktop by running:
```shell
mcp install server.py
```
after installed successfully, you will see the tools in Claude Desktop, 
and you can send a question like "1+2=?"
<img src="images/claude-demo.png" width="500" alt="图片描述">
<img src="images/1+2.png" width="500" alt="图片描述">

## Way 2: Test with  MCP Inspector
```shell
mcp dev server.py
```
after MCP inspector started sucessfully:
- open http://127.0.0.1:6274, 
- refill the Command with "mcp", Arguments with "run server.py",
- then click connect, and test the tools, resources, prompts, etc.
![图片描述](images/image.png)


# Reference
- [python sdk](https://github.com/modelcontextprotocol/python-sdk)
- [MCP: Build Rich-Context AI Apps with Anthropic](https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic/)

