import chromadb
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Professional path and embedding setup
DATA_DIR = "./pra_knowledge_base"
# Embedding model jo text ko numbers (vectors) mein badalta hai
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_connection():
    """Database connection return karta hai"""
    return Chroma(persist_directory=DATA_DIR, embedding_function=embeddings)

def fetch_context(query):
    """Sahi regulatory text dhoondta hai"""
    vector_db = get_connection()
    # Relevant sections retrieve karna
    docs = vector_db.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])