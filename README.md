# 🔎 AI Research Agent

A beginner-friendly single-agent AI research application built with:

- Python
- CrewAI
- Groq
- GPT-OSS 120B
- DuckDuckGo
- Streamlit

## How It Works

The user enters a research topic.

The CrewAI research agent:

1. Understands the research topic.
2. Uses DuckDuckGo as a research tool.
3. Reviews information from multiple search results.
4. Analyzes the information using GPT-OSS 120B through Groq.
5. Generates a structured research report.
6. Displays the report in Streamlit.

## Architecture

User
↓
Streamlit
↓
CrewAI
↓
Single Research Agent
↓
DuckDuckGo Search Tool
↓
GPT-OSS 120B via Groq
↓
Research Report

## Project Structure

```text
ai-research-agent/
├── app.py
├── research_agent.py
├── requirements.txt
├── README.md
└── .gitignore
```

## API Key

The Groq API key is not stored in the source code.

For Streamlit Cloud, add the following secret:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

The application reads it using:

```python
st.secrets["GROQ_API_KEY"]
```

Never commit your API key to GitHub.

## Deployment

1. Push all project files to GitHub.
2. Open Streamlit Community Cloud.
3. Select this GitHub repository.
4. Set `app.py` as the main file.
5. Add `GROQ_API_KEY` in Streamlit Secrets.
6. Deploy the application.

## Model

The application uses:

```text
openai/gpt-oss-120b
```

through Groq.

## Research Tool

DuckDuckGo is exposed to the CrewAI agent as a tool.

## Agent Architecture

This project intentionally uses one agent.

The agent is responsible for deciding when to use the DuckDuckGo search tool, analyzing the research results, and producing the final report.
