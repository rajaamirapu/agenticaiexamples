"""
Example 2: MCP Client -- Connecting to an MCP Server

This client demonstrates how to:
1. Connect to an MCP server (spawning it as a subprocess)
2. Discover available tools
3. Call tools and get results

This is what AI agents (Claude, Cursor, etc.) do under the hood when
they connect to MCP servers.
"""

import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Configure the server to connect to (our server.py)
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"],
    )

    print("Connecting to MCP server...\n")

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # ---------------------------------------------------------------
            # Step 1: Discover available tools
            # ---------------------------------------------------------------
            print("=" * 60)
            print("STEP 1: Discovering available tools")
            print("=" * 60)

            tools_result = await session.list_tools()
            for tool in tools_result.tools:
                print(f"\n  Tool: {tool.name}")
                print(f"  Description: {tool.description}")
                if tool.inputSchema and "properties" in tool.inputSchema:
                    params = list(tool.inputSchema["properties"].keys())
                    print(f"  Parameters: {', '.join(params)}")

            # ---------------------------------------------------------------
            # Step 2: Call tools
            # ---------------------------------------------------------------
            print(f"\n{'=' * 60}")
            print("STEP 2: Calling tools")
            print("=" * 60)

            # Add some notes
            print("\n--- Adding notes ---")
            result = await session.call_tool(
                "add_note",
                arguments={"title": "Agentic AI", "content": "Agentic AI refers to systems that can autonomously execute tasks by sensing, planning, and acting."},
            )
            print(f"  {result.content[0].text}")

            result = await session.call_tool(
                "add_note",
                arguments={"title": "MCP Protocol", "content": "Model Context Protocol is the emerging standard for AI tool integration, with 9400+ servers on GitHub."},
            )
            print(f"  {result.content[0].text}")

            # List notes
            print("\n--- Listing notes ---")
            result = await session.call_tool("list_notes", arguments={})
            print(f"  {result.content[0].text}")

            # Get a specific note
            print("\n--- Getting a note ---")
            result = await session.call_tool(
                "get_note",
                arguments={"title": "Agentic AI"},
            )
            print(f"  {result.content[0].text}")

            # Use the calculator
            print("\n--- Calculator ---")
            result = await session.call_tool(
                "calculate",
                arguments={"expression": "(2 ** 10) + 42"},
            )
            print(f"  {result.content[0].text}")

            # Summarize text
            print("\n--- Summarize ---")
            result = await session.call_tool(
                "summarize_text",
                arguments={
                    "text": (
                        "AI agents are transforming how software is built. "
                        "They can write code, debug issues, and deploy applications. "
                        "The market is projected to reach $183 billion by 2033. "
                        "Most enterprises are still in early adoption phases. "
                        "Security and governance remain major challenges."
                    ),
                    "max_sentences": 2,
                },
            )
            print(f"  {result.content[0].text}")

            # ---------------------------------------------------------------
            # Step 3: Read resources
            # ---------------------------------------------------------------
            print(f"\n{'=' * 60}")
            print("STEP 3: Reading resources")
            print("=" * 60)

            resources_result = await session.list_resources()
            for resource in resources_result.resources:
                print(f"\n  Resource: {resource.uri}")
                print(f"  Name: {resource.name}")

            result = await session.read_resource("notes://all")
            print(f"\n  All Notes:\n  {result.contents[0].text}")

            print(f"\n{'=' * 60}")
            print("Done! The MCP client successfully connected to the server,")
            print("discovered tools, called them, and read resources.")
            print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
