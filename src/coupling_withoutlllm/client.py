import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Define how to run our server process
    server_params = StdioServerParameters(
        command="python", # You might need adjusting if your virutal env python isn't the default in your shell
        args=["src/server.py"]
    )

    print(f"Connecting to the server process...")
    
    # 1. Start the server process and establish a stdio connection
    async with stdio_client(server_params) as (read_stream, write_stream):
        
        # 2. Create an MCP session over this connection
        async with ClientSession(read_stream, write_stream) as session:
            
            # 3. Initialize the connection (Mandatory in MCP before doing anything else)
            await session.initialize()
            print("Connected and initialized successfully!\n")

            # 4. Discover what tools the server provides
            print("--- Available Tools ---")
            tools_response = await session.list_tools()
            for tool in tools_response.tools:
                print(f"Name: {tool.name}")
                print(f"Description: {tool.description}")
            print("-----------------------\n")

            # 5. Call our specific tool
            print("Calling 'get_system_status' tool...")
            
            # Call the tool with its name and an empty dictionary for arguments
            result = await session.call_tool("get_system_status", arguments={})
            
            # 6. Print the content returned by the tool
            print("\n--- Tool Output ---")
            for content in result.content:
                # The content usually has a type (like 'text') and the actual text
                if content.type == "text":
                    print(content.text)

if __name__ == "__main__":
    asyncio.run(main())
