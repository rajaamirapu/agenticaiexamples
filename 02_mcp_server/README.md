# Example 2: MCP Server & Client

## What This Demonstrates

How to build a **Model Context Protocol (MCP)** server -- the emerging standard for exposing tools to AI agents. Think of MCP as the "USB-C of AI": one protocol that lets any agent connect to any tool.

## How It Works

```
┌─────────────────┐        MCP Protocol         ┌─────────────────┐
│                 │  ────────────────────────▶   │                 │
│   MCP Client    │    JSON-RPC over stdio       │   MCP Server    │
│   (AI Agent)    │  ◀────────────────────────   │   (Your Tools)  │
│                 │                               │                 │
│ - Discovers     │                               │ - Exposes tools │
│   available     │                               │ - Handles calls │
│   tools         │                               │ - Returns       │
│ - Calls tools   │                               │   results       │
└─────────────────┘                               └─────────────────┘
```

## Key Concepts

1. **MCP Server**: Exposes tools, resources, and prompts via a standard protocol
2. **MCP Client**: Discovers and calls tools on the server
3. **Tool Discovery**: Client can list all available tools without hardcoding
4. **Transport**: Uses stdio (local) or HTTP+SSE (remote) for communication

## Files

- `server.py` - An MCP server exposing note-taking and calculation tools
- `client.py` - A standalone MCP client that connects and uses the tools
- `requirements.txt` - Dependencies

## Run It

```bash
pip install -r requirements.txt

# Run the server directly (for testing)
python server.py

# Or run the client which spawns the server automatically
python client.py
```

## Why MCP Matters

- **9,400+ MCP servers** on GitHub as of 2026
- Supported by Claude, Cursor, Windsurf, Cline, and more
- Backed by Anthropic, now governed by the Linux Foundation
- Lets you write a tool ONCE and use it with ANY agent
