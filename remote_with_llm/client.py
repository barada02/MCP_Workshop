import asyncio
import json
from mcp import ClientSession
from mcp.client.sse import sse_client

# For the LLM part, you would typically use OpenAI, Anthropic, or similar.
# This pseudo-client demonstrates how to connect to the SSE server and simulate the LLM loop.

async def main():
    print("Connecting to remote MCP server via SSE...")
    
    # Connect via HTTP/SSE instead of a background process
    async with sse_client(url="http://localhost:8000/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("Connected and initialized successfully!\n")

            # 1. Ask the server what tools it has
            tools_response = await session.list_tools()
            
            # --- MOCK LLM INTERACTION ---
            print("--- LLM receives prompt and tool definitions ---")
            print("User Prompt: 'Can you check my system status?'")
            
            # In a real scenario, you pass tools_response to the LLM.
            # The LLM decides to call the 'get_system_status' tool.
            
            print("\nLLM decides to call: 'get_system_status'")
            
            # 2. Call the tool on the remote server
            result = await session.call_tool("get_system_status", arguments={})
            
            # 3. Retrieve content and return it to the LLM
            server_response = ""
            for content in result.content:
                if content.type == "text":
                    server_response += content.text
            
            print("\n--- Server responds with: ---")
            print(server_response)
            
            print("\n--- LLM formats the final answer ---")
            print(f"AI: Based on the system check, you are running {server_response.splitlines()[0]}, and everything is operational!")

if __name__ == "__main__":
    asyncio.run(main())
