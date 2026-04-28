from mcp.server.fastmcp import FastMCP
import platform
import datetime

# Create server with a specific name
mcp = FastMCP("remote-system-notes")

@mcp.tool()
def get_system_status() -> str:
    """
    Get the current system status, including OS details and current time.
    """
    os_info = platform.system() + " " + platform.release()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"System: {os_info}\nCurrent Time: {current_time}\nStatus: All systems operational."

if __name__ == "__main__":
    # FastMCP supports 'sse' (Server-Sent Events) for acting as a remote HTTP server
    # Note: running this requires 'uvicorn' and 'starlette' (pip install uvicorn starlette)
    print("Starting Remote MCP Server on http://localhost:8000/sse")
    mcp.run(transport="sse", port=8000)
