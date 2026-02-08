from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from db import DATA_DIR, embeddings
from langchain_community.vectorstores import Chroma

def build_knowledge_base(file_path):
    """PDF ko chunks mein tod kar DB mein save karta hai"""
    loader = PyPDFLoader(file_path)
    raw_docs = loader.load()
    
    # Text splitting for precise retrieval (COREP requirements ke liye)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=70)
    final_chunks = text_splitter.split_documents(raw_docs)
    
    # ChromaDB indexing
    Chroma.from_documents(
        documents=final_chunks,
        embedding=embeddings,
        persist_directory=DATA_DIR
    )
    return "✅ Knowledge Base Ready"