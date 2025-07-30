## Quickstart

Install `uv` (Python package manager), install with `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Claude Desktop

Go to Claude > Settings > Developer > Edit Config > claude_desktop_config.json to include the following:
```json
{
  "mcpServers": {
    "VCut": {
      "command": "uvx",
      "args": ["vcut"]
    }
  }
}
```

If you're using Windows, you will have to enable "Developer Mode" in Claude Desktop to use the MCP server. Click "Help" in the hamburger menu in the top left and select "Enable Developer Mode".

### Cursor
Go to Cursor -> Preferences -> Cursor Settings -> MCP -> Add new global MCP Server to add above config.

That's it. Your MCP client can now interact with VCut.

