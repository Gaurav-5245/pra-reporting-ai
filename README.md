# 🏦 PRA AI Assistant: Regulatory Compliance & COREP Mapper

An intelligent **RAG (Retrieval-Augmented Generation)** engine designed to automate regulatory mapping for COREP (C 01.00) reporting under Prudential Regulation Authority (PRA) rules.

---

## 🚀 Overview
Regulatory reporting (COREP) is often manual and prone to errors. This tool bridges the gap by using AI to interpret complex banking scenarios and map them directly to regulatory templates. 

It specifically handles nuanced treatments like **Article 33 (Software Asset Deductions)** with built-in audit trails.

---

## ✨ Key Features
* **🧠 Smart Document Intelligence:** Uses `PyPDF` and `LangChain` to ingest and understand official PRA rulebooks.
* **📊 Automated COREP Mapping:** Automatically identifies relevant Row IDs (e.g., C01.01, C02.00) based on user-provided banking scenarios.
* **🔢 Regulatory Logic Engine:** Applies mandatory deductions (e.g., 20% for intangible software assets) as per PRA standards.
* **🚩 Validation & Flagging:** Features a "Validation Status" that identifies missing data and flags it as `DATA REQUIRED`.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **AI Framework:** LangChain
* **Embeddings:** HuggingFace (`sentence-transformers`)
* **Vector Database:** ChromaDB
* **LLM:** OpenAI (via OpenRouter API)

---

## ⚙️ Setup & Installation

Follow these steps to get the **PRA Reporting AI** running on your local machine:

```bash
# 1. Clone the repository
git clone [https://github.com/Gaurav-5245/pra-reporting-ai.git](https://github.com/Gaurav-5245/pra-reporting-ai.git)

# 2. Go into the project directory
cd pra-reporting-ai

# 3. Install required libraries
pip install -r requirements.txt

# 4. Configure Secrets (Create .streamlit/secrets.toml)
# Add your OpenRouter API key inside this file:
# OPENROUTER_API_KEY = "your_api_key_here"

# 5. Run the application
streamlit run app.py



📂 Project Structure
File / Folder,Description
📄 app.py,Streamlit Frontend - Handles UI components and user interaction logic.
🧠 engine.py,"RAG Engine - Contains logic for retrieval, prompt engineering, and LLM orchestration."
🗄️ db.py,Vector Database - Manages document ingestion and ChromaDB operations.
📑 OwnFundsPRA.pdf,Source Document - Official PRA Rulebook used as the knowledge base for RAG.
📋 requirements.txt,Dependencies - List of Python libraries needed to run the project.
⚙️ .gitignore,Security - Ensures sensitive files like secrets.toml are not pushed to GitHub.
