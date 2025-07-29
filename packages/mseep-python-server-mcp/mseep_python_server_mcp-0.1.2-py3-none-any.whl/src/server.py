from mcp.server.fastmcp import FastMCP
import logging

from src.core.config import settings
from src.tools import register_all_tools
from src.resources import register_all_resources

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_server(name=settings.NAME):
    """
    Create and configure the MCP server instance.

    Args:
        name: Server name

    Returns:
        Configured MCP server instance
    """
    server = FastMCP(name)

    # Register all tools and resources
    register_all_tools(server)
    register_all_resources(server)

    return server


async def run_server(transport="stdio"):
    """
    Run the MCP server with the specified transport.

    Args:
        transport: Transport type ("stdio" or "sse")
    """
    server = create_server()
    logger.info(f"Starting weather MCP server with {transport} transport")
    # Use run_async instead of run to avoid nested event loops
    await server.run_async(transport=transport)


def main():
    """Entry point for running the server."""
    # Create and run the server directly without asyncio.run
    server = create_server()
    logger.info("Starting weather MCP server with stdio transport")
    server.run(transport="stdio")
