# servers/mcp-neo4j-cypher/sse.py
import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp_neo4j_cypher import mcp # Import the existing MCP instance from the package

# If the package doesn't expose 'mcp' directly, we might need to recreate it.
# But assuming the official repo follows FastMCP patterns:

def create_app():
    # This creates a Starlette/FastAPI app compatible with SSE
    return mcp.create_sse_server()

if __name__ == "__main__":
    # Run via python directly if needed
    uvicorn.run("sse:create_app", factory=True, host="0.0.0.0", port=8000)
