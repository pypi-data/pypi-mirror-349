"""
ChatApp Package

A Streamlit-based app that refines user queries using prior chat history
and a reference instruction document. Powered by OpenAI and LangChain.
"""
__version__ = "0.1.0"

from langchain_openai import ChatOpenAI
from sqlcoder import SQLCodeGenerator

class DCAI:
    def __init__(self, api_key: str, reference_document: str, model: str = "gpt-4", temperature: float = 0.3):
        self.llm = ChatOpenAI(api_key=api_key, model=model, temperature=temperature)
        self.reference_document = reference_document
        self.sql_generator = SQLCodeGenerator(max_retries=5)  # ✅ USE IT IF NEEDED
    