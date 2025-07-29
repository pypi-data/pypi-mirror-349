"""MCP Server Markets"""

from mcp.server import FastMCP

app = FastMCP("Market Data Server", "1.0.0")

def main():
    """Main function to start the MCP server for markets."""

    app.run()

if __name__ == "__main__":
    main()
