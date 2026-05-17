"""
Example 2: MCP Server -- Exposing Tools via Model Context Protocol

This server exposes a set of tools (notes, calculator) that any MCP-compatible
agent can discover and call. This is the standard way to make your tools
available to AI agents in 2025-2026.

Run directly:  python server.py
Or connect via an MCP client (see client.py)
"""

from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP(
    name="example-notes-server",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# In-memory note storage
# ---------------------------------------------------------------------------

notes: dict[str, str] = {}


# ---------------------------------------------------------------------------
# Tools -- these are automatically exposed via MCP
# ---------------------------------------------------------------------------

@mcp.tool()
def add_note(title: str, content: str) -> str:
    """Create or update a note with the given title and content."""
    notes[title] = content
    return f"Note '{title}' saved successfully. Total notes: {len(notes)}"


@mcp.tool()
def get_note(title: str) -> str:
    """Retrieve a note by its title."""
    if title in notes:
        return f"Title: {title}\nContent: {notes[title]}"
    return f"Note '{title}' not found. Available notes: {list(notes.keys())}"


@mcp.tool()
def list_notes() -> str:
    """List all saved notes."""
    if not notes:
        return "No notes saved yet."
    result = "Saved notes:\n"
    for title, content in notes.items():
        preview = content[:50] + "..." if len(content) > 50 else content
        result += f"  - {title}: {preview}\n"
    return result


@mcp.tool()
def delete_note(title: str) -> str:
    """Delete a note by its title."""
    if title in notes:
        del notes[title]
        return f"Note '{title}' deleted."
    return f"Note '{title}' not found."


@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely.

    Supports basic arithmetic: +, -, *, /, **, (), and common math functions.
    Examples: '2 + 3', '(10 * 5) / 2', '2 ** 10'
    """
    allowed_chars = set("0123456789+-*/().% ")
    if not all(c in allowed_chars for c in expression):
        return f"Error: Expression contains invalid characters. Only basic arithmetic is allowed."

    try:
        result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


@mcp.tool()
def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Provide a simple extractive summary of the given text.

    Returns the first N sentences as a summary.
    """
    sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
    selected = sentences[:max_sentences]
    return ". ".join(selected) + "." if selected else "No content to summarize."


# ---------------------------------------------------------------------------
# Resources -- expose data that agents can read
# ---------------------------------------------------------------------------

@mcp.resource("notes://all")
def all_notes_resource() -> str:
    """A resource that returns all notes as formatted text."""
    if not notes:
        return "No notes available."
    return "\n\n".join(f"# {title}\n{content}" for title, content in notes.items())


# ---------------------------------------------------------------------------
# Run the server
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Starting MCP Notes Server...")
    print("This server exposes the following tools:")
    print("  - add_note(title, content)")
    print("  - get_note(title)")
    print("  - list_notes()")
    print("  - delete_note(title)")
    print("  - calculate(expression)")
    print("  - summarize_text(text, max_sentences)")
    print("\nConnect with an MCP client or run client.py")
    mcp.run()
