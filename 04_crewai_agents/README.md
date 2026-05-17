# Example 4: CrewAI Multi-Agent Team

## What This Demonstrates

How to build a **team of specialized AI agents** that collaborate on a task using CrewAI. This is the "role-based multi-agent" pattern used by 60% of Fortune 500 companies.

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                     CREW                                 │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │  Researcher  │───▶│   Analyst    │───▶│   Writer   │ │
│  │              │    │              │    │            │ │
│  │ Gathers raw  │    │ Analyzes &   │    │ Produces   │ │
│  │ information  │    │ finds        │    │ final      │ │
│  │ using tools  │    │ insights     │    │ report     │ │
│  └──────────────┘    └──────────────┘    └────────────┘ │
│                                                          │
│  Each agent has:                                         │
│  - A role & goal                                         │
│  - A backstory (personality)                             │
│  - Access to specific tools                              │
│  - A task to complete                                    │
└─────────────────────────────────────────────────────────┘
```

## Key Concepts

1. **Agents**: Autonomous entities with roles, goals, and backstories
2. **Tasks**: Specific assignments given to agents with expected outputs
3. **Crew**: Orchestrates agents working together sequentially or in parallel
4. **Tools**: Functions that agents can use to gather information

## Files

- `main.py` - A research crew with researcher, analyst, and writer agents
- `requirements.txt` - Dependencies

## Run It

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"
python main.py
```
