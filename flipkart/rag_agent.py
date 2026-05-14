from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

from flipkart.config import Config


class RAGAgentBuilder:

    def __init__(self, vector_store):

        self.vector_store = vector_store

        self.llm = ChatGroq(
            groq_api_key=Config.GROQ_API_KEY,
            model_name=Config.RAG_MODEL,
            temperature=0.3
        )

    def build_agent(self):

        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 2}
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False
        )

        return qa_chain