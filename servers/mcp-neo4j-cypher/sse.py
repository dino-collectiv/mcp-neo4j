import os
import uvicorn
from neo4j import AsyncGraphDatabase
from mcp_neo4j_cypher.server import create_mcp_server

def create_app():
    # 1. Read config from Environment Variables (set in Railway)
    db_url = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")

    # 2. Initialize the Neo4j Driver manually
    # (The original main() function did this, so we must do it too)
    neo4j_driver = AsyncGraphDatabase.driver(
        db_url,
        auth=(username, password),
    )

    # 3. Create the MCP Server instance
    mcp = create_mcp_server(
        neo4j_driver=neo4j_driver,
        database=database
    )

    # 4. Return the Starlette/SSE app
    return mcp.create_sse_server()

if __name__ == "__main__":
    uvicorn.run("sse:create_app", factory=True, host="0.0.0.0", port=8000)
