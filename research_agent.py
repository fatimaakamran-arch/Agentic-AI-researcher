import litellm

# Groq does not accept CrewAI's cache_breakpoint
# metadata in chat messages.
litellm.cache = None
litellm.drop_params = True

_original_completion = litellm.completion


def _completion_without_cache_breakpoint(*args, **kwargs):
    kwargs["caching"] = False

    messages = kwargs.get("messages", [])

    for message in messages:
        if isinstance(message, dict):
            message.pop("cache_breakpoint", None)

            content = message.get("content")

            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict):
                        block.pop("cache_breakpoint", None)

    return _original_completion(*args, **kwargs)


litellm.completion = _completion_without_cache_breakpoint


from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import tool
from ddgs import DDGS


@tool("DuckDuckGo Search")
def duckduckgo_search(query: str) -> str:
    """Search DuckDuckGo for current information about a research topic."""

    try:
        results = DDGS().text(query, max_results=5)

        if not results:
            return "No search results were found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            title = result.get("title", "No title")
            body = result.get("body", "No description available.")
            url = result.get("href", "No URL available.")

            formatted_results.append(
                f"SOURCE {index}\n"
                f"Title: {title}\n"
                f"Description: {body}\n"
                f"URL: {url}"
            )

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"DuckDuckGo search error: {e}"


def create_llm(groq_api_key: str) -> LLM:
    return LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=groq_api_key,
        temperature=0.2,
    )


def create_research_agent(groq_api_key: str) -> Agent:
    llm = create_llm(groq_api_key)

    return Agent(
        role="Research Analyst",
        goal=(
            "Research the user's topic using web search, analyze "
            "information from multiple sources, and produce a clear, "
            "factual, well-structured research report."
        ),
        backstory=(
            "You are an experienced research analyst. You investigate "
            "topics carefully using web sources, compare information, "
            "identify important findings, and explain them clearly. "
            "You never invent facts or sources."
        ),
        tools=[duckduckgo_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def run_research(topic: str, groq_api_key: str):
    researcher = create_research_agent(groq_api_key)

    research_task = Task(
        description=f"""
Research the following topic:

{topic}

Use the DuckDuckGo Search tool to perform web research.

Research process:
1. Understand the topic.
2. Create useful search queries.
3. Search DuckDuckGo for relevant information.
4. Review information from multiple sources.
5. Compare information when appropriate.
6. Identify important facts and findings.
7. Avoid unsupported claims.
8. Produce the final report.

The final report must contain:

# {topic}

## Executive Summary
Give a concise summary of the most important findings.

## Introduction
Explain the topic and why it is relevant.

## Key Findings
List the most important findings.

## Detailed Analysis
Explain the topic using information collected from the research.

## Important Facts and Statistics
Include useful statistics or factual information when reliable
sources provide them. Do not invent statistics.

## Advantages and Opportunities
Explain important benefits or opportunities when applicable.

## Challenges and Limitations
Explain important challenges, risks, or limitations.

## Conclusion
Summarize the main findings.

## Sources
List the sources used. For each source include:
- Source title
- URL

Rules:
- Use factual and neutral language.
- Do not invent facts.
- Do not invent sources.
- Do not create fake URLs.
- Use multiple sources where possible.
- Prefer reliable and authoritative sources.
- Clearly indicate uncertainty when information is unclear.
- Keep the report understandable for a general reader.
""",
        expected_output=(
            "A complete research report containing an executive summary, "
            "introduction, key findings, detailed analysis, facts or "
            "statistics, advantages or opportunities, challenges or "
            "limitations, conclusion, and sources."
        ),
        agent=researcher,
    )

    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True,
    )

    return crew.kickoff()
