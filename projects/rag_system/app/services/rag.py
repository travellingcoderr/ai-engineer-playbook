from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

from packages.core.config import get_config
from packages.core.llm_factory import LLMFactory
from app.services.embedding_factory import EmbeddingFactory
from app.services.vector_factory import VectorStoreFactory
from app.services.loader_factory import LoaderFactory
from app.services.splitter_factory import SplitterFactory

class RAGService:
    """
    The main coordinator for the Retrieval-Augmented Generation pipeline.
    It builds the unified chain using all configured factories.
    """
    def __init__(self):
        self.config = get_config()
        
        # 1. Initialize Embeddings
        self.embeddings = EmbeddingFactory.create_embeddings(
            provider=self.config.embeddings.provider,
            model_name=self.config.embeddings.model,
            openai_api_key=self.config.llm.openai_api_key
        )
        
        # 2. Initialize Vector Store
        self.vector_store = VectorStoreFactory.create_vector_store(
            provider=self.config.vector_store.provider,
            collection_name=self.config.vector_store.collection_name,
            embeddings=self.embeddings,
            host=self.config.vector_store.host,
            port=self.config.vector_store.port
        )
        
        # 3. Initialize LLM
        self.llm = LLMFactory.create_llm(
            provider=self.config.llm.provider,
            model_name=self.config.llm.model,
            openai_api_key=self.config.llm.openai_api_key,
            gemini_api_key=self.config.llm.gemini_api_key
        )

    def ingest_document(self, file_path: str) -> List[Document]:
        """
        Loads a document, splits it into chunks, and saves it to the vector db.
        """
        # Load
        loader = LoaderFactory.create_loader(
            file_path, 
            strategy=self.config.loader.strategy
        )
        docs = loader.load()
        
        # Split
        splitter = SplitterFactory.create_splitter(
            strategy=self.config.splitter.strategy,
            chunk_size=self.config.splitter.chunk_size,
            chunk_overlap=self.config.splitter.chunk_overlap
        )
        chunks = splitter.split_documents(docs)
        
        # Store
        self.vector_store.add_documents(chunks)
        # Assuming persist is needed for some vector DBs (like old Chroma API)
        if hasattr(self.vector_store, "persist"):
            self.vector_store.persist()
            
        return chunks

    def ask_question(self, question: str) -> str:
        """
        Takes a user question, retrieves context, and returns the LLM's answer.
        """
        # Create a basic prompt template
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. "
            "Use three sentences maximum and keep the answer concise.\n\n"
            "{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        # Create the chains
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        # Execute
        response = rag_chain.invoke({"input": question})
        return response["answer"]
