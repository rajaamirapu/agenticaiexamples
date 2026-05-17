"""
Example 1: Basic Tool-Calling Agent using OpenAI Function Calling

This demonstrates the fundamental pattern behind all agentic AI:
1. Define tools as JSON schemas
2. Let the LLM decide which tools to call
3. Execute the tools
4. Feed results back to the LLM for a final response

Works with: OpenAI GPT-4o, GPT-4o-mini, or any model supporting function calling.
"""

import json
import os

from openai import OpenAI

# ---------------------------------------------------------------------------
# 1. Define your tools (these are the "actions" the agent can take)
# ---------------------------------------------------------------------------

def get_weather(city: str) -> dict:
    """Simulate a weather API call."""
    weather_data = {
        "Tokyo": {"temp_c": 22, "condition": "Partly Cloudy", "humidity": 65},
        "New York": {"temp_c": 18, "condition": "Sunny", "humidity": 45},
        "London": {"temp_c": 14, "condition": "Rainy", "humidity": 80},
        "Mumbai": {"temp_c": 32, "condition": "Hot & Humid", "humidity": 85},
    }
    result = weather_data.get(city)
    if result:
        return {"city": city, **result}
    return {"city": city, "error": f"No weather data available for {city}"}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Simulate a currency conversion API call."""
    rates = {
        ("USD", "JPY"): 148.50,
        ("USD", "EUR"): 0.92,
        ("USD", "GBP"): 0.79,
        ("EUR", "USD"): 1.09,
        ("JPY", "USD"): 0.0067,
        ("USD", "INR"): 83.50,
    }
    rate = rates.get((from_currency, to_currency))
    if rate:
        converted = round(amount * rate, 2)
        return {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "rate": rate,
            "result": converted,
        }
    return {"error": f"No rate available for {from_currency} -> {to_currency}"}


def search_web(query: str) -> dict:
    """Simulate a web search."""
    return {
        "query": query,
        "results": [
            {"title": f"Top result for: {query}", "snippet": "This is a simulated search result."},
            {"title": f"Related: {query}", "snippet": "Another simulated result with more details."},
        ],
    }


# ---------------------------------------------------------------------------
# 2. Map tool names to functions (so we can call them dynamically)
# ---------------------------------------------------------------------------

TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "convert_currency": convert_currency,
    "search_web": search_web,
}

# ---------------------------------------------------------------------------
# 3. Define tool schemas (tells the LLM what tools are available and how to call them)
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g. 'Tokyo', 'New York'",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert an amount from one currency to another",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "The amount to convert"},
                    "from_currency": {"type": "string", "description": "Source currency code (e.g. USD)"},
                    "to_currency": {"type": "string", "description": "Target currency code (e.g. JPY)"},
                },
                "required": ["amount", "from_currency", "to_currency"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"},
                },
                "required": ["query"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# 4. The agent loop: send message -> handle tool calls -> repeat
# ---------------------------------------------------------------------------

def run_agent(user_message: str) -> str:
    """Run the tool-calling agent for a single user message."""
    client = OpenAI()
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant with access to tools. "
                "Use the available tools to answer the user's question. "
                "You can call multiple tools if needed."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    print(f"\n{'='*60}")
    print(f"User: {user_message}")
    print(f"{'='*60}")

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
        )

        choice = response.choices[0]

        # If the model wants to call tools
        if choice.finish_reason == "tool_calls":
            assistant_message = choice.message
            messages.append(assistant_message)

            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                print(f"\n🔧 Calling tool: {func_name}({func_args})")

                func = TOOL_FUNCTIONS.get(func_name)
                if func:
                    result = func(**func_args)
                else:
                    result = {"error": f"Unknown tool: {func_name}"}

                print(f"   Result: {json.dumps(result, indent=2)}")

                # Feed the tool result back to the model
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )
        else:
            # Model is done -- return the final response
            final_response = choice.message.content
            print(f"\nAssistant: {final_response}")
            return final_response


# ---------------------------------------------------------------------------
# 5. Run example queries
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY environment variable to run this example.")
        print("   export OPENAI_API_KEY='your-key-here'")
        print("\nShowing the tool definitions instead:\n")
        for tool in TOOLS:
            fn = tool["function"]
            print(f"  Tool: {fn['name']}")
            print(f"  Description: {fn['description']}")
            params = fn["parameters"]["properties"]
            print(f"  Parameters: {', '.join(params.keys())}")
            print()
    else:
        # Single tool call
        run_agent("What's the weather like in Tokyo?")

        # Multiple tool calls in one request
        run_agent("What's the weather in London and how much is 100 USD in EUR?")

        # Tool call with follow-up reasoning
        run_agent("Search the web for 'agentic AI trends 2026' and summarize what you find.")
