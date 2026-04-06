import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import (
    VectorizedQuery,
    VectorFilterMode
)
from openai import AzureOpenAI, OpenAI

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentinelSearchClient:
    def __init__(self):
        load_dotenv()
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.key = os.getenv("AZURE_SEARCH_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "sentinel-index")
        
        if not self.endpoint or not self.key:
            raise ValueError("Azure Search credentials missing.")

        self.client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=AzureKeyCredential(self.key)
        )

        # Embedding Client (Using OpenAI SDK as it's the stable recommendation)
        # Assuming Azure OpenAI or direct OpenAI
        self.aoai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if self.aoai_endpoint:
            self.emb_client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                api_version="2023-05-15",
                azure_endpoint=self.aoai_endpoint
            )
        else:
            self.emb_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_embedding(self, text: str) -> List[float]:
        """Convert text to vector using OpenAI text-embedding-3-small."""
        logger.info(f"Generating embedding for query: {text[:50]}...")
        response = self.emb_client.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def search_hybrid(
        self, 
        query: str, 
        top: int = 5, 
        filter_str: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Performs Hybrid Search (Vector + Keyword + Semantic Ranking).
        """
        logger.info(f"Performing hybrid search for: {query}")
        
        vector_query = VectorizedQuery(
            vector=self.get_embedding(query), 
            k_nearest_neighbors=top, 
            fields="content_vector"
        )

        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            select=["id", "title", "content", "metadata"],
            filter=filter_str,
            top=top,
            query_type="semantic",
            semantic_configuration_name="sentinel-semantic-config"
        )

        output = []
        for result in results:
            output.append({
                "id": result["id"],
                "title": result["title"],
                "content": result["content"],
                "score": result["@search.score"],
                "reranker_score": result["@search.reranker_score"]
            })
            
        return output

if __name__ == "__main__":
    # Quick test
    try:
        searcher = SentinelSearchClient()
        print("Search Client initialized.")
    except Exception as e:
        print(f"Error: {e}")
