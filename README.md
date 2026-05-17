# Agentic AI Examples

Practical, runnable code examples covering the key patterns in the agentic AI ecosystem (2025-2026). Each example is self-contained with its own README and requirements.

## What's Inside

| # | Example | Pattern | Key Concept |
|---|---------|---------|-------------|
| 1 | [Basic Tool-Calling Agent](01_tool_calling_agent/) | Function Calling | How LLMs use tools via structured function calls |
| 2 | [MCP Server & Client](02_mcp_server/) | Model Context Protocol | Building and consuming an MCP server (the "USB-C of agents") |
| 3 | [LangGraph Workflow Agent](03_langgraph_agent/) | Stateful Graph Workflows | Multi-step agent with state, branching, and human-in-the-loop |
| 4 | [CrewAI Multi-Agent Team](04_crewai_agents/) | Multi-Agent Collaboration | Role-based agents working together on a task |
| 5 | [ReAct Agent from Scratch](05_react_agent/) | Reasoning + Acting | Build a ReAct loop from scratch to understand agent internals |

## Prerequisites

- Python 3.10+
- An OpenAI API key (set as `OPENAI_API_KEY` environment variable)
- Each example has its own `requirements.txt`

## Quick Start

```bash
# Clone the repo
git clone https://github.com/rajaamirapu/agenticaiexamples.git
cd agenticaiexamples

# Pick an example
cd 01_tool_calling_agent

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENAI_API_KEY="your-key-here"

# Run it
python main.py
```

## How These Examples Connect to the Agentic AI Landscape

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR APPLICATION                      │
├──────────┬──────────┬──────────┬──────────┬─────────────┤
│ Example 5│ Example 1│ Example 3│ Example 4│  Example 2  │
│  ReAct   │  Tool    │ LangGraph│  CrewAI  │    MCP      │
│  Loop    │  Calling │ Workflow │  Team    │   Server    │
│(internals│(basic    │(stateful │(multi-   │(standard    │
│ of how   │ agent-   │ agent    │ agent    │ tool        │
│ agents   │ tool     │ pipelines│ collab)  │ protocol)   │
│ think)   │ pattern) │)         │          │             │
└──────────┴──────────┴──────────┴──────────┴─────────────┘
     ↑           ↑          ↑         ↑            ↑
  Foundation  Building   Production Production  Ecosystem
              Block      Workflows  Teams       Standard
```

## Learning Path

**Recommended order:**

1. **Start with Example 5 (ReAct)** -- Understand how agents actually think (the observe-think-act loop)
2. **Then Example 1 (Tool Calling)** -- See how modern LLMs handle this natively with function calling
3. **Then Example 2 (MCP)** -- Learn the protocol standard for exposing tools to any agent
4. **Then Example 3 (LangGraph)** -- Build production-grade stateful workflows
5. **Finally Example 4 (CrewAI)** -- Orchestrate multiple agents working as a team

## License

MIT
