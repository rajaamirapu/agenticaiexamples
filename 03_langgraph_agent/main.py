"""
Example 3: LangGraph Stateful Workflow Agent

A research agent that demonstrates LangGraph's key patterns:
- State management with TypedDict
- Conditional routing between nodes
- Tool integration within a graph
- Multi-step workflow (research → write → review)

This is the pattern used by production agent systems at Klarna, Replit, LinkedIn, etc.
"""

import json
import operator
import os
from typing import Annotated

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

# ---------------------------------------------------------------------------
# 1. Define the agent state
# ---------------------------------------------------------------------------

class AgentState(dict):
    """State that flows through the graph.

    Keys:
        messages: conversation history
        research_notes: collected research data
        draft: written draft
        review_feedback: review comments
        step_count: tracks how many research iterations
    """

    messages: Annotated[list[BaseMessage], operator.add]
    research_notes: list[str]
    draft: str
    review_feedback: str
    step_count: int


# ---------------------------------------------------------------------------
# 2. Define tools the research agent can use
# ---------------------------------------------------------------------------

def search_knowledge_base(topic: str) -> str:
    """Simulated knowledge base search."""
    knowledge = {
        "agentic ai": (
            "Agentic AI refers to systems that autonomously execute tasks. "
            "The market reached $10.9B in 2026. Key players include Claude Code, "
            "Cursor, Devin, and GitHub Copilot. 30-40% of new code at adopting "
            "companies is AI-generated."
        ),
        "mcp protocol": (
            "Model Context Protocol (MCP) is the de facto standard for AI tool "
            "integration, with 9,400+ servers on GitHub. Originally by Anthropic, "
            "now governed by the Linux Foundation. Supported by Claude, Cursor, "
            "Windsurf, and more."
        ),
        "agent frameworks": (
            "LangGraph leads with 34.5M monthly downloads. CrewAI focuses on "
            "role-based multi-agent collaboration. OpenAI Agents SDK is lightweight. "
            "Mastra targets TypeScript developers. 11 credible frameworks exist as of 2026."
        ),
        "ai safety": (
            "40%+ of agentic AI projects may be canceled by 2027. EU AI Act "
            "enforcement begins August 2026. Most enterprise compliance frameworks "
            "are structurally inadequate for agent deployments. Security remains "
            "the biggest concern."
        ),
    }
    for key, value in knowledge.items():
        if key in topic.lower():
            return value
    return f"No specific data found for '{topic}'. Try: agentic ai, mcp protocol, agent frameworks, ai safety."


def get_statistics(category: str) -> str:
    """Return statistics about a category."""
    stats = {
        "market": "AI agent market: $10.9B (2026), projected $47-183B by 2030-2033. Q2 2026 VC: $42.6B across 312 rounds.",
        "adoption": "64% of teams have agentic AI on roadmap. 85% believe it becomes table stakes within 3 years. 31% pilot-to-production conversion.",
        "coding": "30-40% of new code is AI-generated at adopting companies. Claude Code ~$2B ARR. Cursor ~$2B ARR.",
        "ecosystem": "9,400+ MCP servers. 97M monthly MCP SDK downloads. 8,000+ MCP server repositories on GitHub.",
    }
    return stats.get(category.lower(), f"No stats for '{category}'. Try: market, adoption, coding, ecosystem.")


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search the knowledge base for information on a topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "The topic to search for"},
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_statistics",
            "description": "Get statistics about a category (market, adoption, coding, ecosystem)",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "The category to get stats for"},
                },
                "required": ["category"],
            },
        },
    },
]

TOOL_MAP = {
    "search_knowledge_base": search_knowledge_base,
    "get_statistics": get_statistics,
}


# ---------------------------------------------------------------------------
# 3. Define graph nodes
# ---------------------------------------------------------------------------

def research_node(state: dict) -> dict:
    """The research agent gathers information using tools."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    messages = state.get("messages", [])
    step_count = state.get("step_count", 0)

    if step_count == 0:
        messages = [
            SystemMessage(content=(
                "You are a research agent. Your job is to gather information about "
                "the user's topic using the available tools. Call tools to collect data. "
                "After gathering enough information (2-3 tool calls), respond with "
                "'RESEARCH COMPLETE' in your message to move to the writing phase."
            )),
            *messages,
        ]

    response = llm.invoke(messages, tools=TOOL_SCHEMAS)

    print(f"\n📚 Research Agent (step {step_count + 1}):")
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"   Calling: {tc['name']}({tc['args']})")
    else:
        print(f"   {response.content[:100]}...")

    return {
        "messages": [response],
        "step_count": step_count + 1,
    }


def execute_tools_node(state: dict) -> dict:
    """Execute tool calls from the research agent."""
    messages = state.get("messages", [])
    last_message = messages[-1]

    tool_messages = []
    research_notes = state.get("research_notes", [])

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        for tc in last_message.tool_calls:
            func = TOOL_MAP.get(tc["name"])
            if func:
                result = func(**tc["args"])
                research_notes.append(result)
                print(f"   🔧 {tc['name']} → {result[:80]}...")
                tool_messages.append(
                    ToolMessage(content=result, tool_call_id=tc["id"])
                )

    return {
        "messages": tool_messages,
        "research_notes": research_notes,
    }


def write_node(state: dict) -> dict:
    """Write a report based on research notes."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    research_notes = state.get("research_notes", [])
    notes_text = "\n".join(f"- {note}" for note in research_notes)

    messages = [
        SystemMessage(content=(
            "You are a technical writer. Based on the research notes below, "
            "write a concise, well-structured summary report (3-5 paragraphs). "
            "Include key statistics and actionable insights."
        )),
        HumanMessage(content=f"Research notes:\n{notes_text}\n\nWrite the report."),
    ]

    response = llm.invoke(messages)
    draft = response.content

    print(f"\n✍️  Writer Agent:")
    print(f"   Draft: {draft[:150]}...")

    return {"draft": draft, "messages": [response]}


def review_node(state: dict) -> dict:
    """Review the draft and provide feedback."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    draft = state.get("draft", "")

    messages = [
        SystemMessage(content=(
            "You are an editor reviewing a report. Provide a brief quality assessment "
            "(1-2 sentences) and a score from 1-10. Be concise."
        )),
        HumanMessage(content=f"Review this report:\n\n{draft}"),
    ]

    response = llm.invoke(messages)
    feedback = response.content

    print(f"\n📝 Review Agent:")
    print(f"   Feedback: {feedback[:150]}...")

    return {"review_feedback": feedback, "messages": [response]}


# ---------------------------------------------------------------------------
# 4. Define routing logic
# ---------------------------------------------------------------------------

def should_use_tools(state: dict) -> str:
    """Decide if we need to execute tools or move to writing."""
    messages = state.get("messages", [])
    last_message = messages[-1] if messages else None
    step_count = state.get("step_count", 0)

    if last_message and hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "use_tools"

    if step_count >= 4:
        return "write"

    if last_message and hasattr(last_message, "content") and "RESEARCH COMPLETE" in (last_message.content or ""):
        return "write"

    return "write"


# ---------------------------------------------------------------------------
# 5. Build the graph
# ---------------------------------------------------------------------------

def build_research_graph() -> StateGraph:
    """Build the research agent workflow graph."""
    workflow = StateGraph(dict)

    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("use_tools", execute_tools_node)
    workflow.add_node("write", write_node)
    workflow.add_node("review", review_node)

    # Set entry point
    workflow.set_entry_point("research")

    # Add conditional edges from research
    workflow.add_conditional_edges(
        "research",
        should_use_tools,
        {
            "use_tools": "use_tools",
            "write": "write",
        },
    )

    # After tools, go back to research
    workflow.add_edge("use_tools", "research")

    # After writing, go to review
    workflow.add_edge("write", "review")

    # After review, end
    workflow.add_edge("review", END)

    return workflow


# ---------------------------------------------------------------------------
# 6. Run the agent
# ---------------------------------------------------------------------------

def run_research_agent(topic: str) -> dict:
    """Run the full research workflow for a topic."""
    print(f"\n{'='*60}")
    print(f"🚀 Starting Research Agent")
    print(f"   Topic: {topic}")
    print(f"{'='*60}")

    graph = build_research_graph()
    app = graph.compile()

    initial_state = {
        "messages": [HumanMessage(content=f"Research this topic: {topic}")],
        "research_notes": [],
        "draft": "",
        "review_feedback": "",
        "step_count": 0,
    }

    final_state = app.invoke(initial_state)

    print(f"\n{'='*60}")
    print(f"✅ Research Complete!")
    print(f"{'='*60}")
    print(f"\n📄 Final Report:\n{final_state.get('draft', 'No draft generated')}")
    print(f"\n📝 Review: {final_state.get('review_feedback', 'No review')}")

    return final_state


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY environment variable to run this example.")
        print("   export OPENAI_API_KEY='your-key-here'")
        print("\nThis example builds a LangGraph workflow with these nodes:")
        print("  1. research  → Gathers info using tools")
        print("  2. use_tools → Executes tool calls")
        print("  3. write     → Drafts a report from research")
        print("  4. review    → Reviews the draft quality")
        print("\nThe graph routes conditionally between research and tools")
        print("until enough data is gathered, then flows to write → review.")
    else:
        run_research_agent("The current state of agentic AI in 2026")
