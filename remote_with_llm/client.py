import asyncio
import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI
from mcp import ClientSession
from mcp.client.sse import sse_client

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
# Base URL and API Key are automatically pulled from OPENAI_BASE_URL and OPENAI_API_KEY env variables
openai_client = AsyncOpenAI()
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")

def convert_mcp_to_openai_tools(mcp_tools) -> list:
    """
    Helper function to convert MCP tool definitions into the format 
    that the OpenAI API expects.
    """
    openai_tools = []
    for tool in mcp_tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                # MCP uses JSON Schema for inputs, which matches OpenAI closely
                "parameters": tool.inputSchema
            }
        })
    return openai_tools

async def chat_with_mcp(session: ClientSession, user_prompt: str):
    """
    The main interaction loop between the User, the LLM, and the MCP Server.
    """
    print(f"\nUser: {user_prompt}")
    
    # 1. Ask the MCP server what tools it has available
    tools_response = await session.list_tools()
    
    # 2. Convert those tools to OpenAI's expected format
    available_openai_tools = convert_mcp_to_openai_tools(tools_response.tools)
    print(f"[Client] Found {len(available_openai_tools)} tool(s) on MCP Server.")

    messages = [{"role": "user", "content": user_prompt}]

    # 3. Send the prompt and the available tools to the LLM
    print(f"[Client] Sending prompt to {MODEL_NAME}...")
    response = await openai_client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=available_openai_tools,
        tool_choice="auto" # Let the LLM decide if it wants to use a tool
    )
    
    response_message = response.choices[0].message
    messages.append(response_message)

    # 4. Check if the LLM decided to call a tool
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            
            print(f"[Client] LLM wants to call tool '{tool_name}' with args: {tool_args}")
            print(f"[Client] Executing '{tool_name}' on remote MCP Server...")
            
            # 5. Call the tool on the MCP server
            result = await session.call_tool(tool_name, arguments=tool_args)
            
            # Combine the content returned by the server (often just text)
            tool_result_str = ""
            for content in result.content:
                if content.type == "text":
                    tool_result_str += content.text
                    
            print(f"[Client] Server returned: {tool_result_str.strip()}")
            
            # 6. Add the tool's result to the conversation history for the LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": tool_result_str
            })
            
        print("[Client] Sending tool results back to LLM for final answer...")
        
        # 7. Get final conversational response from LLM
        final_response = await openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )
        print(f"\nAI: {final_response.choices[0].message.content}")
    else:
        # LLM answered the question directly without tools
        print(f"\nAI: {response_message.content}")

async def main():
    print("Connecting to remote MCP server via SSE...")
    async with sse_client(url="http://localhost:8000/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("Connected and initialized successfully!")

            # Example Interaction
            await chat_with_mcp(session, "Can you check my system status right now?")

if __name__ == "__main__":
    asyncio.run(main())
