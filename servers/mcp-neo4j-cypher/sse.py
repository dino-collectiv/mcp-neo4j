import uvicorn
from mcp_neo4j_cypher.server import mcp

def create_app():
    # This creates a Starlette/FastAPI app compatible with SSE
    return mcp.create_sse_server()

if __name__ == "__main__":
    uvicorn.run("sse:create_app", factory=True, host="0.0.0.0", port=8000)
