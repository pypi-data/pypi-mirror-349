"""
Plaid MCP Server Implementation.

This module implements a Model Context Protocol (MCP) server for Plaid API integration.
It allows AI assistants to interact with Plaid's financial data APIs through the MCP protocol.
"""

# Standard library imports
import logging
from typing import Any, Dict, List

import mcp.types as types
# Third-party imports
import plaid
from mcp.server import Server
from plaid.api import plaid_api

from mcp_server_plaid.clients.bill import AskBillClient
# Local imports
from mcp_server_plaid.tools import register_all_tools

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("plaid-mcp-server")

# Constants
__version__ = "0.0.1"
REQUEST_TIMEOUT = 30.0


async def serve(client_id: str, secret: str, enabled_categories: str) -> Server:
    """Initialize and configure the MCP server with Plaid tools."""
    server = Server("plaid")

    ask_bill_client = AskBillClient()

    configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox,
        api_key={
            "clientId": client_id,
            "secret": secret,
        },
    )
    plaid_client = plaid_api.PlaidApi(plaid.ApiClient(configuration))

    tool_registry = register_all_tools(enabled_categories)

    @server.list_tools()
    async def handle_list_tools() -> List[types.Tool]:
        """Handler for the call_tool MCP method."""
        return tool_registry.get_tools()

    @server.call_tool()
    async def handle_call_tool(
            name: str, arguments: Dict[str, Any] | None
    ) -> List[types.TextContent]:
        """Handler for the call_tool MCP method."""
        # Validate tool exists
        if not tool_registry.has_tool(name):
            raise ValueError(f"Unknown tool: {name}")

        # Get the handler for the tool
        handler = tool_registry.get_handler(name)
        if handler is None:
            raise ValueError(f"No handler registered for tool: {name}")

        # Call the handler with the arguments and context
        return await handler(
            arguments or {},  # Ensure arguments is not None
            bill_client=ask_bill_client,
            plaid_client=plaid_client,
        )

    return server

#
# def main():
#     """Entry point for the MCP server."""
#     # Read configurations from environment variables
#     client_id = os.environ.get("PLAID_CLIENT_ID")
#     secret = os.environ.get("PLAID_SECRET")
#     enabled_categories = os.environ.get("TOOLS_TO_ENABLE", "")
#
#     # Validate required environment variables
#     if not client_id or not secret:
#         logger.error(
#             "PLAID_CLIENT_ID and PLAID_SECRET environment variables must be set"
#         )
#         sys.exit(1)
#
#     async def _run():
#         logger.info("Setting up stdio communication channels")
#         async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
#             server = await serve(client_id, secret, enabled_categories)
#             await server.run(
#                 read_stream,
#                 write_stream,
#                 InitializationOptions(
#                     server_name="plaid",
#                     server_version=__version__,
#                     capabilities=server.get_capabilities(
#                         notification_options=NotificationOptions(),
#                         experimental_capabilities={},
#                     ),
#                 ),
#             )
#
#     asyncio.run(_run())
