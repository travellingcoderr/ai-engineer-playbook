from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from packages.core.config import get_config
from packages.core.services import LLMFactory
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
        # Helper to format documents
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

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
        
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        
        # LCEL Chain
        # This is a simple RAG chain that uses the retriever to get the context
        # and then passes it to the LLM to generate the answer.
        # The retriever is a Runnable that returns a list of Documents.
        # The format_docs function is a Runnable that takes a list of Documents
        # and returns a string of context.
        # The prompt is a ChatPromptTemplate that takes the context and the question.
        # The LLM is a Runnable that takes the prompt and returns the answer.
        # The StrOutputParser is a Runnable that takes the LLM's answer and returns a string.
        rag_chain = (
            {
                "context": retriever | format_docs, 
                "input": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain.invoke(question)
