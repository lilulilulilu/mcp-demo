import asyncio
import json
import gradio as gr
from autogen_agentchat.agents import AssistantAgent
import os
from openai import OpenAI
from dotenv import load_dotenv
from client_stdio import list_tools, execute_tool
from qwen import ask_llm

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

async def chat_async(query: str, history_messages: list) -> tuple[str, list]:
    available_tools = await list_tools()
    history_messages.append({"role": "user", "content": query})
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=history_messages,
        tools=available_tools,
        tool_choice="auto"
    )
    if response.choices[0].finish_reason == 'tool_calls':
        print(f'function calling....')
        tool_name = response.choices[0].message.tool_calls[0].function.name
        arguments = response.choices[0].message.tool_calls[0].function.arguments
        tool_result = await execute_tool(tool_name, json.loads(arguments))
        print(f'tool_result for function call: {tool_result}')
        history_messages_copy = history_messages.copy()
        history_messages_copy.append({"role": "assistant", "content": tool_result[0].text})
        history_messages_str = str(history_messages_copy)
        messages = [
            {"role": "system", "content": f"You are a helpful assistant. Here is some chat history: {history_messages_str}"},
            {"role": "user", "content": query}
        ]
        content = await ask_llm(messages=messages)
        history_messages.append({"role": "assistant", "content": content})
        return content, history_messages
    elif response.choices[0].finish_reason == 'stop':
        content = response.choices[0].message.content
        history_messages.append({"role": "assistant", "content": content})
        return content, history_messages

def chat_gradio_wrapper(message, history):
    global chat_history
    result = asyncio.run(chat_async(message, chat_history))
    content, chat_history = result
    return chat_history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(height=400, type="messages")
    textbox = gr.Textbox(placeholder="Ask something...", container=False)
    clear_btn = gr.Button("Clear")

    def reset():
        global chat_history
        chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
        return []

    textbox.submit(chat_gradio_wrapper, inputs=[textbox, chatbot], outputs=chatbot)
    clear_btn.click(fn=reset, outputs=chatbot)

demo.launch()
