import streamlit as st
from database.connection import get_engine
from database.schema_loader import get_schema_context
from database.executor import execute_query
from chains.sql_chain import sql_chain
from chains.analyst_chain import analyst_chain

# Page setup
st.set_page_config(page_title="Store BI Assistant", page_icon="📊", layout="centered")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #ffffff !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0 !important;
    }
    h2, h3 {
        color: #e0d7ff !important;
    }
    .stButton > button {
        background: rgba(255, 255, 255, 0.07) !important;
        color: #e0d7ff !important;
        border: 1px solid rgba(168, 159, 216, 0.4) !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: rgba(168, 159, 216, 0.25) !important;
        border-color: #a89fd8 !important;
        color: #ffffff !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #7c3aed, #4f46e5) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0.6rem 2rem !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #6d28d9, #4338ca) !important;
    }

/* ── Expander header ── */
    [data-testid="stExpander"] {
        border: 1px solid rgba(124, 58, 237, 0.5) !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.04) !important;
    }
    [data-testid="stExpander"] summary {
        background: rgba(124, 58, 237, 0.25) !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
    }
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary div {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    [data-testid="stExpander"] svg {
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }

    /* ── SQL code block — light background ── */
    .stCodeBlock,
    [data-testid="stCodeBlock"],
    [data-testid="stCodeBlock"] > div,
    div.stCodeBlock > div,
    .stCodeBlock > div > div {
        background: #f0eeff !important;
        border-radius: 10px !important;
        border: 1px solid rgba(124, 58, 237, 0.2) !important;
    }
    .stCodeBlock > div > div > div {
        background: #f0eeff !important;
    }
    [data-testid="stCodeBlock"] pre,
    [data-testid="stCodeBlock"] code,
    .stCodeBlock code,
    .stCodeBlock pre {
        background: #f0eeff !important;
        color: #1e1a3a !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }

    /* ── Summary info box ── */
    [data-testid="stAlert"] {
        background: rgba(124, 58, 237, 0.2) !important;
        border: 1px solid rgba(124, 58, 237, 0.5) !important;
        border-radius: 12px !important;
        padding: 1rem 1.25rem !important;
    }
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] div {
        color: #ffffff !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(168, 159, 216, 0.2) !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Warning / Error ── */
    .stWarning {
        background: rgba(251, 191, 36, 0.1) !important;
        border: 1px solid rgba(251, 191, 36, 0.3) !important;
        border-radius: 12px !important;
    }
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
    }

    /* ── Text input ── */
    div[data-testid="stTextInput"] input {
        background-color: #1e1a3a !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1px solid rgba(124, 58, 237, 0.5) !important;
        border-radius: 12px !important;
        caret-color: white !important;
    }
    div[data-testid="stTextInput"] input:focus {
        background-color: #1e1a3a !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1px solid #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.3) !important;
        outline: none !important;
    }
    div[data-testid="stTextInput"] input:-webkit-autofill,
    div[data-testid="stTextInput"] input:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0px 1000px #1e1a3a inset !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    div[data-testid="stTextInput"] > div,
    div[data-testid="stTextInput"] > div > div {
        background-color: #1e1a3a !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# Load database connection and schema once
@st.cache_resource
def load_resources():
    engine = get_engine()
    schema = get_schema_context(engine)
    return engine, schema

engine, schema = load_resources()

# Session state setup
if "question_text" not in st.session_state:
    st.session_state.question_text = ""
if "run_query" not in st.session_state:
    st.session_state.run_query = False

# Hero section
st.markdown("""
<div style='text-align:center; padding: 1.5rem 0 1rem 0;'>
    <div style='font-size:3rem;'>📊</div>
    <h1 style='color:white; font-size:2.5rem; font-weight:800; margin:0.5rem 0;'>
        Store BI Assistant
    </h1>
    <p style='color:#a89fd8; font-size:1rem; margin:0;'>
        Ask any business question in plain English — powered by Llama 3.2 running locally
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- Example questions ---
st.markdown("### 💡 Try one of these questions")
st.markdown("<p style='color:#a89fd8; font-size:0.9rem; margin-top:-10px;'>Click any question to instantly run it</p>", unsafe_allow_html=True)

example_questions = [
    "Which product category had the most revenue?",
    "Which region has the most customers?",
    "How many orders were returned vs completed?",
    "Which product has been ordered the most times?",
    "What is the total revenue per customer?"
]

col1, col2 = st.columns(2)
for i, q in enumerate(example_questions):
    if i % 2 == 0:
        if col1.button(q, use_container_width=True, key=f"ex_{i}"):
            st.session_state.question_text = q
            st.session_state.run_query = True
    else:
        if col2.button(q, use_container_width=True, key=f"ex_{i}"):
            st.session_state.question_text = q
            st.session_state.run_query = True

st.divider()

# --- Manual input ---
st.markdown("### ✍️ Or type your own question")

typed = st.text_input(
    "Your question",
    value=st.session_state.question_text,
    placeholder="e.g. What is the average order value by region?",
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Ask ▶", type="primary"):
    st.session_state.question_text = typed
    st.session_state.run_query = True

# --- Run the query ---
if st.session_state.run_query and st.session_state.question_text:
    st.session_state.run_query = False
    final_question = st.session_state.question_text

    st.markdown(f"<p style='color:#a89fd8; font-size:0.9rem;'>Running: <i>{final_question}</i></p>", unsafe_allow_html=True)

    # Step 1 — Generate SQL
    with st.spinner("🧠 Generating SQL query..."):
        sql = sql_chain.invoke({
            "schema": schema,
            "question": final_question
        })

    with st.expander("🔍 Generated SQL", expanded=True):
        st.code(sql, language="sql")

    # Step 2 — Run SQL
    with st.spinner("⚡ Running query against MySQL..."):
        df, error = execute_query(engine, sql)

    # Retry once if error
    if error:
        with st.spinner("🔄 Retrying with fix..."):
            retry_question = f"{final_question}. Previous SQL failed: {error}. Fix it."
            sql = sql_chain.invoke({
                "schema": schema,
                "question": retry_question
            })
            df, error = execute_query(engine, sql)

    # Show results
    if error:
        st.error(f"❌ Query failed: {error}")
    elif df is not None and not df.empty:
        st.markdown("### 📊 Results")
        st.dataframe(df, use_container_width=True)

        # Step 3 — Analyst summary
        with st.spinner("💡 Analysing results..."):
            summary = analyst_chain.invoke({
                "question": final_question,
                "sql": sql,
                "results": df.head(20).to_markdown(index=False)
            })

        st.markdown("### 💡 Summary")
        st.info(summary)
    else:
        st.warning("⚠️ Query returned no results.")

# Footer
st.divider()
st.markdown("""
<p style='text-align:center; color:#6b5ea8; font-size:0.8rem;'>
    Built with LangChain · Llama 3.2 · MySQL · Streamlit &nbsp;|&nbsp; MGS636 Capstone Project
</p>
""", unsafe_allow_html=True)