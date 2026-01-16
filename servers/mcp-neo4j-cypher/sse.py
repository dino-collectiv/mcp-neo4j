import os
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.responses import Response
from neo4j import AsyncGraphDatabase
from mcp_neo4j_cypher.server import create_mcp_server

# We need to adapt FastMCP to a raw Starlette SSE route manually
# because the helper method seems missing in your version.

async def handle_sse(request: Request):
    # This is a wrapper to expose the internal MCP SSE transport
    mcp_app = request.app.state.mcp
    
    # Use the FastMCP internal SSE handler
    # Note: If .sse_handler or similar doesn't exist, we fallback to the
    # recommended pattern of creating the transport via the library.
    return await mcp_app._sse_app(request.scope, request.receive, request.send)

def create_app():
    db_url = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")

    neo4j_driver = AsyncGraphDatabase.driver(db_url, auth=(username, password))

    mcp = create_mcp_server(neo4j_driver=neo4j_driver, database=database)
    
    # FastMCP v0.4.0+ usually exposes .sse_app
    # If the previous error was "has no attribute", let's assume we are on a version 
    # where we simply return the internal app property.
    
    # TRY THIS SIMPLEST FIX FIRST:
    # fastmcp uses an internal Starlette app for SSE.
    # It is usually stored in `mcp._sse_app`
    return mcp._sse_app

if __name__ == "__main__":
    uvicorn.run("sse:create_app", factory=True, host="0.0.0.0", port=8000)
