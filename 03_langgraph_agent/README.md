# Example 3: LangGraph Stateful Workflow Agent

## What This Demonstrates

How to build a **production-grade stateful agent** using LangGraph -- the most popular framework for agent workflows in production (34.5M monthly downloads). This shows the graph-based approach to agent orchestration.

## How It Works

```
                    ┌──────────────┐
                    │    START     │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
              ┌─────│   research   │─────┐
              │     │   (agent)    │     │
              │     └──────────────┘     │
              │                          │
        needs tools              done researching
              │                          │
     ┌────────▼────────┐         ┌───────▼───────┐
     │   use_tools     │         │    write       │
     │   (execute)     │         │   (draft)      │
     └────────┬────────┘         └───────┬────────┘
              │                          │
              └──────────┐   ┌───────────┘
                         │   │
                  ┌──────▼───▼─────┐
                  │    review      │
                  │   (quality)    │
                  └──────┬─────────┘
                         │
                  ┌──────▼─────────┐
                  │      END       │
                  └────────────────┘
```

## Key Concepts

1. **State Graph**: Agent workflow as a directed graph with typed state
2. **Nodes**: Each node is a function that transforms the state
3. **Conditional Edges**: Route between nodes based on state (e.g., "needs more tools?" → loop back)
4. **Checkpointing**: Save and resume agent state at any point

## Files

- `main.py` - A research agent that gathers info, writes a report, and reviews it
- `requirements.txt` - Dependencies

## Run It

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"
python main.py
```
