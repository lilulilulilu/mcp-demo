import asyncio
import os
from openai import OpenAI
from dotenv import load_dotenv


async def ask_llm(messages: list) -> str:
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    response = client.chat.completions.create(
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model="qwen-plus",
        messages=messages
    )
    content = response.choices[0].message.content
    messages.append({"role": "assistant", "content": content})
    return content

    
if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
    print(asyncio.run(ask_llm(messages)))  # Example query