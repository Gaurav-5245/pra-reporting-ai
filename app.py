
import streamlit as st
from openai import OpenAI
from pypdf import PdfReader
from db import fetch_context
from engine import build_knowledge_base
import os
import time
import pandas as pd

# --- 1. DATABASE INITIALIZATION ---
DB_PATH = "./pra_knowledge_base"
PDF_NAME = "OwnFundsPRA.pdf"

db_status = st.empty() 

if not os.path.exists(DB_PATH):
    if os.path.exists(PDF_NAME):
        with db_status.container():
            with st.spinner("🛠️ Initializing Regulatory Database..."):
                build_knowledge_base(PDF_NAME)
                st.success("✅ Database Ready!")
                time.sleep(2)
        db_status.empty() 
    else:
        st.error(f"❌ Critical Error: {PDF_NAME} missing!")
        st.stop()
else:
    db_status.empty()

# --- 2. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="PRA AI Assistant", page_icon="🏦", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #0f172a; }
    .card {
        background: #020617;
        padding: 24px;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(0,0,0,.35);
        border-left: 5px solid #38bdf8;
        color: #e5e7eb;
        margin-bottom: 20px;
    }
    .header { font-size: 36px; font-weight: 800; color: white; }
    .sub { color: #94a3b8; margin-bottom: 30px; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info(f"Active Source: **{PDF_NAME}**")
    uploaded_file = st.file_uploader("Ingest New Regulation (PDF)", type="pdf")
    if uploaded_file:
        st.success("File received. Ready for indexing.")
    st.markdown("---")
    st.caption("PRA Smart-Mapper v1.0")

# --- 4. API SETUP ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

# ---------------- HEADER ----------------
st.markdown("<div class='header'>🏦 PRA AI Assistant: COREP Edition</div>", unsafe_allow_html=True)
st.markdown("<p class='sub'>Automated Regulatory Mapping & Compliance Validation Engine</p>", unsafe_allow_html=True)

# ---------------- UI LAYOUT ----------------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔎 Query Engine")
    query = st.text_area(
        "",
        placeholder="Example: We have £10m in software licenses. How to report?",
        height=150
    )
    run = st.button("Analyze & Map to COREP")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📋 AI Rulebook Analysis")

    if run:
        if not query.strip():
            st.warning("Please enter a scenario first.")
        else:
            with st.spinner("Analyzing Rulebook..."):
                try:
                    # 1. Retrieval
                    context = fetch_context(query)
                    
                    # 2. Final Prompt
                    prompt = f"""
                    Act as a Senior PRA Regulatory Expert and COREP Reporting Assistant. 
                    Map the user scenario to the C 01.00 (Own Funds) template.

                    CONTEXT: {context}
                    SCENARIO: {query}

                    STRICT INSTRUCTIONS:
            - Do NOT use placeholders like "[To be determined]".
            - Based on the context provided, identify the specific treatment (e.g., 20% deduction for software assets under Article 33).
            - If a value is missing, write "DATA REQUIRED" and explain why.

                    STRICT OUTPUT FORMAT:
                    ### 📊 COREP Template Extract (C 01.00)
                    | Row/Col ID | Item Description | Reported Value (£m) | Validation Status |
                    |------------|------------------|----------------------|-------------------|

                    ### 📜 Audit Log & Validation
                    - **Validation Rules**: [e.g. PASSED]
                    - **Rule Reference**: [e.g. Article 92(2)]
                    - **Treatment**: [Calculation details]
                    - **Basis**: [Direct quote]
                    """
                    
                    # 3. API Call
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b:free",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.1,
                    )
                    
                    st.markdown(response.choices[0].message.content)
                    st.success("COREP Report Generated")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("Results will appear here after analysis.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Smart-Mapper Prototype | Powered by OpenAI & RAG Architecture")