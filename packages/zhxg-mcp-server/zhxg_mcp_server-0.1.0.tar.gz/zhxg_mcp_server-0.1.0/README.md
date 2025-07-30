
# MCP Inspector

export ZHXG_API_KEY=<YOUR_API_KEY>

npx -y @modelcontextprotocol/inspector uv run ./src/zhxg_mcp_server/server.py

# MCP Servers Config

{
  "mcpServers": {
    "zhxg_mcp_server": {
      "command": "uvx",
      "args": [
        "zhxg_mcp_server"
      ],
      "env": {
        "ZHXG_API_KEY": "<YOUR_API_KEY>"
      }
    }
}