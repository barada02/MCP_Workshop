import platform
import datetime
from mcp.server.fastmcp import FastMCP

# Initialize the server using FastMCP
mcp = FastMCP("system-notes-assistant")

# --- PHASE 2: TOOLS ---
@mcp.tool()
def get_system_status() -> str:
    """
    Get the current system status, including OS details and current time.
    """
    os_info = platform.system() + " " + platform.release()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"System: {os_info}\nCurrent Time: {current_time}\nStatus: All systems operational."

if __name__ == "__main__":
    # mcp.run() automatically sets up the stdio transport and asyncio loop
    mcp.run()