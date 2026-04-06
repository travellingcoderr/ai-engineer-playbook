import os
import logging
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchField,
    SearchFieldDataType,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticSearch,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    ExhaustiveKnnAlgorithmConfiguration
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def provision_search_index():
    load_dotenv()

    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "sentinel-index")

    if not endpoint or not key:
        logger.error("AZURE_SEARCH_ENDPOINT or AZURE_SEARCH_KEY not found in environment.")
        return

    client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # 1. Define Fields
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="parent_id", type=SearchFieldDataType.String, filterable=True),
        SearchableField(name="title", type=SearchFieldDataType.String, searchable=True),
        SearchableField(name="content", type=SearchFieldDataType.String, searchable=True),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,  # Standard for text-embedding-3-small
            vector_search_profile_name="sentinel-vector-profile"
        ),
        SimpleField(name="metadata", type=SearchFieldDataType.String, filterable=True)
    ]

    # 2. Configure Vector Search
    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(name="sentinel-hnsw"),
            ExhaustiveKnnAlgorithmConfiguration(name="sentinel-knn")
        ],
        profiles=[
            VectorSearchProfile(
                name="sentinel-vector-profile", 
                algorithm_configuration_name="sentinel-hnsw"
            )
        ]
    )

    # 3. Configure Semantic Search
    semantic_config = SemanticConfiguration(
        name="sentinel-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            content_fields=[SemanticField(field_name="content")]
        )
    )
    semantic_search = SemanticSearch(configurations=[semantic_config])

    # 4. Create Index Object
    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search
    )

    try:
        logger.info(f"Creating/Updating search index: {index_name}...")
        result = client.create_or_update_index(index)
        logger.info(f"Index {result.name} provisioned successfully.")
    except Exception as e:
        logger.error(f"Failed to provision index: {e}")

if __name__ == "__main__":
    provision_search_index()
