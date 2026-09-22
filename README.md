# 🔎 AI Research Agent

A beginner-friendly single-agent AI research application built with:

- Python
- CrewAI
- Groq
- GPT-OSS 120B
- DuckDuckGo
- Streamlit

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

In Streamlit Cloud, add this secret:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

The application reads it with:

```python
st.secrets["GROQ_API_KEY"]
```

Never commit your API key to GitHub.

## Important Dependency

CrewAI needs its LiteLLM extra for the Groq provider used by this project.

The dependency is installed through:

```text
crewai[litellm]
```

The LLM configuration is:

```python
LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=groq_api_key,
)
```

Groq's actual model ID is:

```text
openai/gpt-oss-120b
```

## Deployment

1. Push these files to GitHub.
2. Open Streamlit Community Cloud.
3. Select the GitHub repository.
4. Set `app.py` as the main file.
5. Add `GROQ_API_KEY` in Streamlit Secrets.
6. Deploy.
