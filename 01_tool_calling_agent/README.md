# Example 1: Basic Tool-Calling Agent

## What This Demonstrates

How modern LLMs (OpenAI, Anthropic, etc.) use **function calling** to interact with external tools. This is the foundational pattern behind every agentic AI system.

## How It Works

```
User: "What's the weather in Tokyo and convert 100 USD to JPY?"
  │
  ▼
┌─────────────┐
│   LLM sees  │ ── decides which tools to call
│   available │
│   tools     │
└──────┬──────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│ get_weather()│     │ convert_     │
│  → Tokyo     │     │ currency()   │
│  → 22°C      │     │ → 14,850 JPY │
└──────┬───────┘     └──────┬───────┘
       │                    │
       ▼                    ▼
┌─────────────────────────────────┐
│ LLM combines results into      │
│ natural language response       │
└─────────────────────────────────┘
```

## Key Concepts

1. **Tool Definitions**: You describe tools as JSON schemas that the LLM understands
2. **Tool Selection**: The LLM decides WHICH tools to call (and can call multiple)
3. **Tool Execution**: Your code runs the actual functions
4. **Response Synthesis**: The LLM combines tool results into a coherent answer

## Files

- `main.py` - The complete tool-calling agent
- `requirements.txt` - Dependencies

## Run It

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"
python main.py
```
