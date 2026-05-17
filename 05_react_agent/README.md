# Example 5: ReAct Agent from Scratch

## What This Demonstrates

How to build a **ReAct (Reasoning + Acting) agent from scratch** -- no frameworks, just pure Python and an LLM. This helps you understand what's happening inside every agent framework.

## How It Works

```
┌─────────────────────────────────────────────────────┐
│                 THE ReAct LOOP                       │
│                                                      │
│   ┌──────────┐                                      │
│   │ OBSERVE  │  ← see the current state / result    │
│   └────┬─────┘                                      │
│        │                                             │
│   ┌────▼─────┐                                      │
│   │  THINK   │  ← reason about what to do next      │
│   └────┬─────┘                                      │
│        │                                             │
│   ┌────▼─────┐                                      │
│   │   ACT    │  ← call a tool or give final answer  │
│   └────┬─────┘                                      │
│        │                                             │
│        └──────── loop back to OBSERVE ──────────┘   │
│                                                      │
│   Repeat until the agent decides it has the answer   │
└─────────────────────────────────────────────────────┘
```

## Key Concepts

1. **Thought**: The LLM reasons about what it knows and what it needs
2. **Action**: The LLM chooses a tool and provides inputs
3. **Observation**: The tool result is fed back to the LLM
4. **Final Answer**: When the LLM has enough info, it produces a response

This is the **foundational pattern** that LangChain, CrewAI, and every other framework builds upon.

## Files

- `main.py` - A ReAct agent built from scratch with prompt engineering
- `requirements.txt` - Dependencies

## Run It

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"
python main.py
```

## Why Build From Scratch?

Understanding the ReAct loop helps you:
- Debug agent behavior in any framework
- Know when to use a framework vs. build custom
- Understand what's actually happening when an agent "thinks"
- Optimize agent performance by tuning the loop
