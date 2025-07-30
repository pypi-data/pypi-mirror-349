
def main():
    """
    Main entry point for the mcp-server-qdrant script defined
    in pyproject.toml. It runs the MCP server with a specific transport
    protocol.
    """

    # Import is done here to make sure environment variables are loaded
    # only after we make the changes.
    from mcp_server_rash.server import mcp

    mcp.run(transport="stdio")
