"""
Example 4: CrewAI Multi-Agent Team

Demonstrates the multi-agent collaboration pattern where specialized agents
work together on a complex task. Each agent has a distinct role, goal, and
set of tools.

This example creates a research crew that:
1. Researcher agent -- gathers raw information
2. Analyst agent -- finds patterns and insights
3. Writer agent -- produces a polished report

CrewAI is used by 60% of Fortune 500 companies for production agent workflows.
"""

import os

from crewai import Agent, Crew, Process, Task
from crewai.tools import tool


# ---------------------------------------------------------------------------
# 1. Define tools that agents can use
# ---------------------------------------------------------------------------

@tool("Search Industry Data")
def search_industry_data(query: str) -> str:
    """Search for industry data and statistics about AI and technology trends.

    Args:
        query: The search query about AI industry data
    """
    data = {
        "market size": (
            "The AI agent market crossed $10.9 billion in early 2026 (up 43% YoY). "
            "Projected to reach $47-52B by 2030 and $183B by 2033. "
            "Q2 2026 VC funding hit $42.6B across 312 rounds."
        ),
        "adoption": (
            "64% of product roadmaps include agentic AI. 85% of respondents believe "
            "agentic AI becomes table stakes within 3 years. Enterprise pilot-to-production "
            "conversion reached 31% in Q2 2026, nearly doubling from Q1."
        ),
        "coding agents": (
            "AI coding agents write 30-40% of new code at adopting companies. "
            "Claude Code reached ~$2B ARR. Cursor hit $2B ARR. "
            "GitHub reports 8,000+ MCP server repositories."
        ),
        "frameworks": (
            "LangGraph leads at 34.5M monthly downloads. CrewAI is used by 60% of "
            "Fortune 500. 11 credible frameworks exist as of 2026. MCP has 9,400+ "
            "servers and 97M monthly SDK downloads."
        ),
        "risks": (
            "40%+ of agentic AI projects may be canceled by 2027 (Gartner). "
            "EU AI Act enforcement begins August 2026. Security and governance "
            "remain structurally inadequate at most enterprises."
        ),
    }
    for key, value in data.items():
        if key in query.lower():
            return value
    return (
        f"General data for '{query}': The agentic AI ecosystem is rapidly maturing. "
        "Key trends include MCP standardization, coding agent dominance, and "
        "enterprise adoption acceleration. Available topics: market size, adoption, "
        "coding agents, frameworks, risks."
    )


@tool("Analyze Trends")
def analyze_trends(data_points: str) -> str:
    """Analyze data points and identify key trends and patterns.

    Args:
        data_points: Raw data or observations to analyze
    """
    return (
        f"Analysis of provided data:\n"
        f"1. GROWTH TRAJECTORY: The data shows exponential growth patterns consistent "
        f"with a technology transitioning from early adoption to mainstream.\n"
        f"2. CONSOLIDATION: The ecosystem is consolidating around key standards (MCP) "
        f"and a smaller number of production-grade frameworks.\n"
        f"3. RISK FACTORS: Regulatory pressure (EU AI Act) and high project failure "
        f"rates (40%+) suggest a correction is coming alongside growth.\n"
        f"4. SKILLS SHIFT: The data indicates a fundamental shift in developer roles "
        f"from code writing to agent orchestration and review.\n"
        f"Input analyzed: {data_points[:100]}..."
    )


# ---------------------------------------------------------------------------
# 2. Define specialized agents
# ---------------------------------------------------------------------------

def create_crew(topic: str) -> Crew:
    """Create a research crew with three specialized agents."""

    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Gather comprehensive, accurate data about: {topic}",
        backstory=(
            "You are a meticulous researcher with 15 years of experience in "
            "technology market analysis. You are known for finding reliable data "
            "and statistics that others miss. You always verify claims with data."
        ),
        tools=[search_industry_data],
        verbose=True,
        allow_delegation=False,
    )

    analyst = Agent(
        role="Strategic Insights Analyst",
        goal="Identify key patterns, trends, and actionable insights from the research data",
        backstory=(
            "You are a strategic thinker who excels at connecting dots across "
            "different data points. You have a talent for distilling complex "
            "information into clear, actionable insights. You focus on what "
            "matters most for decision-makers."
        ),
        tools=[analyze_trends],
        verbose=True,
        allow_delegation=False,
    )

    writer = Agent(
        role="Technical Report Writer",
        goal="Produce a clear, engaging, and well-structured report from the analysis",
        backstory=(
            "You are an award-winning technical writer who makes complex topics "
            "accessible. You structure information for maximum impact and always "
            "include concrete numbers and actionable takeaways. You write for "
            "a technical audience that values substance over fluff."
        ),
        tools=[],
        verbose=True,
        allow_delegation=False,
    )

    # -----------------------------------------------------------------------
    # 3. Define tasks for each agent
    # -----------------------------------------------------------------------

    research_task = Task(
        description=(
            f"Research the following topic thoroughly: {topic}\n\n"
            "You must:\n"
            "1. Search for market size and growth data\n"
            "2. Search for adoption statistics\n"
            "3. Search for key players and frameworks\n"
            "4. Search for risks and challenges\n\n"
            "Compile all findings into a structured research brief."
        ),
        expected_output=(
            "A detailed research brief with sections for: market data, "
            "adoption metrics, key players, and risks. Each section should "
            "include specific numbers and sources."
        ),
        agent=researcher,
    )

    analysis_task = Task(
        description=(
            "Analyze the research data and identify:\n"
            "1. The 3 most important trends\n"
            "2. Key opportunities for developers and businesses\n"
            "3. Major risks to watch\n"
            "4. Predictions for the next 12 months\n\n"
            "Use the analyze_trends tool to process the research findings."
        ),
        expected_output=(
            "A strategic analysis document with clearly labeled sections for "
            "trends, opportunities, risks, and predictions. Each point should "
            "be supported by data from the research."
        ),
        agent=analyst,
    )

    writing_task = Task(
        description=(
            "Using the research and analysis, write a polished report that:\n"
            "1. Opens with a compelling executive summary (2-3 sentences)\n"
            "2. Covers key findings with supporting data\n"
            "3. Includes a 'What This Means For You' section\n"
            "4. Ends with 3 concrete action items\n\n"
            "The report should be 400-600 words, professional but accessible."
        ),
        expected_output=(
            "A well-structured report with executive summary, findings, "
            "implications, and action items. Should be ready to share with "
            "a technical audience."
        ),
        agent=writer,
    )

    # -----------------------------------------------------------------------
    # 4. Assemble the crew
    # -----------------------------------------------------------------------

    crew = Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        process=Process.sequential,
        verbose=True,
    )

    return crew


# ---------------------------------------------------------------------------
# 5. Run the crew
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  Set OPENAI_API_KEY environment variable to run this example.")
        print("   export OPENAI_API_KEY='your-key-here'")
        print("\nThis example creates a CrewAI team with 3 agents:")
        print("  1. Researcher  → Gathers data using search tools")
        print("  2. Analyst     → Finds patterns and insights")
        print("  3. Writer      → Produces a polished report")
        print("\nThe agents work sequentially, each building on the previous output.")
        print("This is the same pattern used by Fortune 500 companies in production.")
    else:
        topic = "The state of agentic AI in 2026: market landscape, key players, and what developers should focus on"
        crew = create_crew(topic)

        print(f"\n{'='*60}")
        print(f"🚀 Starting CrewAI Research Team")
        print(f"   Topic: {topic}")
        print(f"{'='*60}\n")

        result = crew.kickoff()

        print(f"\n{'='*60}")
        print(f"✅ Crew Finished!")
        print(f"{'='*60}")
        print(f"\n📄 Final Report:\n{result}")
