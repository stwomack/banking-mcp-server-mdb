#!/bin/bash
set -e

# Absolute path to your project root
PROJECT_DIR="/Users/swomack/workspace/banking-mcp-server-mdb-temporal"

cd "$PROJECT_DIR"

# (Optional) Ensure dependencies are installed
uv pip install -r requirements.txt

# Run the MCP server using uv, as a module
uv run -m mcp_server.main 
