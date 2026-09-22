import streamlit as st

from research_agent import run_research


st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 AI Research Agent")
st.write(
    "Enter a topic and let the AI research it using "
    "DuckDuckGo and GPT-OSS 120B."
)

topic = st.text_area(
    "Research Topic",
    placeholder="Example: Impact of Artificial Intelligence on Education",
    height=120,
)

if st.button("🔍 Start Research", type="primary"):
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    try:
        groq_api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        st.error(
            "GROQ_API_KEY was not found in Streamlit Secrets. "
            "Add it in your Streamlit Cloud app settings."
        )
        st.stop()

    with st.spinner("Researching your topic..."):
        try:
            report = run_research(
                topic=topic.strip(),
                groq_api_key=groq_api_key,
            )

            st.success("Research completed!")
            st.markdown("---")
            st.markdown("## Research Report")
            st.markdown(str(report))

        except Exception as e:
            st.error(f"An error occurred: {e}")
