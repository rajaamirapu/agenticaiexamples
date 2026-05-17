"""
Example 5: ReAct Agent from Scratch

Build the Reasoning + Acting (ReAct) loop from scratch using only an LLM
and prompt engineering. No frameworks -- just the core pattern that every
agent framework implements under the hood.

The ReAct pattern:
1. THOUGHT  → LLM reasons about what it knows and needs
2. ACTION   → LLM picks a tool and provides inputs
3. OBSERVATION → Tool result is fed back
4. Repeat until FINAL ANSWER

Paper: "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022)
"""

import json
import os
import re

from openai import OpenAI

# ---------------------------------------------------------------------------
# 1. Define available tools
# ---------------------------------------------------------------------------

def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    allowed_chars = set("0123456789+-*/().% ")
    if not all(c in allowed_chars for c in expression):
        return "Error: Only basic arithmetic is allowed."
    try:
        result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def lookup(topic: str) -> str:
    """Look up information about a topic."""
    knowledge = {
        "python": "Python is a high-level programming language created by Guido van Rossum in 1991. It emphasizes code readability and supports multiple programming paradigms.",
        "javascript": "JavaScript is a programming language that conforms to the ECMAScript specification. It is high-level, often just-in-time compiled, and multi-paradigm.",
        "react": "React is a JavaScript library for building user interfaces, maintained by Meta. It uses a virtual DOM and component-based architecture.",
        "langchain": "LangChain is a framework for developing applications powered by LLMs. It provides tools for chains, agents, and retrieval-augmented generation.",
        "mcp": "Model Context Protocol (MCP) is a standard for AI tool integration with 9,400+ servers. Created by Anthropic, now governed by the Linux Foundation.",
        "agentic ai": "Agentic AI refers to systems that autonomously execute tasks. The market reached $10.9B in 2026. Key patterns: tool calling, ReAct loops, multi-agent teams.",
        "rust": "Rust is a systems programming language focused on safety, speed, and concurrency. Created by Mozilla, it prevents memory errors at compile time.",
        "population of france": "The population of France is approximately 68.4 million people as of 2025.",
        "population of germany": "The population of Germany is approximately 84.5 million people as of 2025.",
        "speed of light": "The speed of light in vacuum is approximately 299,792,458 meters per second (about 3 × 10^8 m/s).",
    }
    topic_lower = topic.lower().strip()
    for key, value in knowledge.items():
        if key in topic_lower or topic_lower in key:
            return value
    return f"No information found for '{topic}'. Try: {', '.join(knowledge.keys())}"


def string_length(text: str) -> str:
    """Count the number of characters in a string."""
    return str(len(text))


TOOLS = {
    "calculator": {
        "function": calculator,
        "description": "Evaluate a math expression. Input: a mathematical expression string.",
    },
    "lookup": {
        "function": lookup,
        "description": "Look up information about a topic. Input: topic name.",
    },
    "string_length": {
        "function": string_length,
        "description": "Count the number of characters in a string. Input: the string to measure.",
    },
}


# ---------------------------------------------------------------------------
# 2. The ReAct prompt template
# ---------------------------------------------------------------------------

REACT_SYSTEM_PROMPT = """You are a helpful assistant that solves problems step by step using tools.

You have access to the following tools:
{tool_descriptions}

You MUST follow this exact format for each step:

Thought: [reason about what you need to do next]
Action: [tool_name]
Action Input: [input to the tool]

After receiving an observation, continue with another Thought/Action cycle.

When you have enough information to answer, use:

Thought: [I now have enough information to answer]
Final Answer: [your complete answer to the question]

Important rules:
- Always start with a Thought
- Only use one Action per step
- Wait for the Observation before your next Thought
- Use Final Answer when you're done (don't use an Action and Final Answer in the same step)

Begin!"""


def format_tool_descriptions() -> str:
    """Format tool descriptions for the system prompt."""
    lines = []
    for name, info in TOOLS.items():
        lines.append(f"- {name}: {info['description']}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 3. Parse the LLM output to extract thought, action, and final answer
# ---------------------------------------------------------------------------

def parse_agent_output(text: str) -> dict:
    """Parse the LLM output to extract structured components."""
    result = {"thought": None, "action": None, "action_input": None, "final_answer": None}

    # Extract thought
    thought_match = re.search(r"Thought:\s*(.+?)(?=\n(?:Action|Final Answer)|\Z)", text, re.DOTALL)
    if thought_match:
        result["thought"] = thought_match.group(1).strip()

    # Check for final answer
    final_match = re.search(r"Final Answer:\s*(.+)", text, re.DOTALL)
    if final_match:
        result["final_answer"] = final_match.group(1).strip()
        return result

    # Extract action and input
    action_match = re.search(r"Action:\s*(.+?)(?:\n|$)", text)
    input_match = re.search(r"Action Input:\s*(.+?)(?:\n|$)", text)

    if action_match:
        result["action"] = action_match.group(1).strip()
    if input_match:
        result["action_input"] = input_match.group(1).strip()

    return result


# ---------------------------------------------------------------------------
# 4. The ReAct loop
# ---------------------------------------------------------------------------

def react_agent(question: str, max_steps: int = 8) -> str:
    """Run the ReAct loop for a given question.

    Args:
        question: The user's question
        max_steps: Maximum number of think-act cycles (safety limit)

    Returns:
        The final answer string
    """
    client = OpenAI()

    system_prompt = REACT_SYSTEM_PROMPT.format(
        tool_descriptions=format_tool_descriptions()
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")

    for step in range(1, max_steps + 1):
        print(f"\n--- Step {step} ---")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0,
            max_tokens=500,
        )

        output = response.choices[0].message.content
        messages.append({"role": "assistant", "content": output})

        parsed = parse_agent_output(output)

        if parsed["thought"]:
            print(f"💭 Thought: {parsed['thought']}")

        # Check if we have a final answer
        if parsed["final_answer"]:
            print(f"\n✅ Final Answer: {parsed['final_answer']}")
            return parsed["final_answer"]

        # Execute the action
        if parsed["action"] and parsed["action_input"]:
            tool_name = parsed["action"].strip()
            tool_input = parsed["action_input"].strip()

            print(f"🔧 Action: {tool_name}({tool_input})")

            tool_info = TOOLS.get(tool_name)
            if tool_info:
                observation = tool_info["function"](tool_input)
            else:
                observation = f"Error: Unknown tool '{tool_name}'. Available: {list(TOOLS.keys())}"

            print(f"👁  Observation: {observation}")

            # Feed the observation back
            messages.append({"role": "user", "content": f"Observation: {observation}"})
        else:
            print(f"⚠️  Could not parse action from output: {output[:100]}...")
            messages.append({
                "role": "user",
                "content": "Observation: I couldn't understand your action. Please use the exact format: Action: tool_name\\nAction Input: input",
            })

    return "Agent reached maximum steps without a final answer."


# ---------------------------------------------------------------------------
# 5. Run example queries
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY environment variable to run this example.")
        print("   export OPENAI_API_KEY='your-key-here'")
        print("\nThis example builds a ReAct agent FROM SCRATCH.")
        print("The ReAct loop: Thought → Action → Observation → repeat")
        print("\nAvailable tools:")
        for name, info in TOOLS.items():
            print(f"  - {name}: {info['description']}")
        print("\nExample questions it can answer:")
        print('  - "What is Python and how many characters is its description?"')
        print('  - "What is the population of France and Germany combined?"')
        print('  - "What is MCP and calculate 9400 * 12"')
    else:
        # Simple single-tool question
        react_agent("What is MCP in the context of AI?")

        # Multi-step question requiring multiple tools
        react_agent(
            "What is the population of France and Germany? "
            "What is their combined population?"
        )

        # Question requiring tool chaining
        react_agent(
            "Look up information about Python, then tell me "
            "how many characters are in the description you found."
        )
