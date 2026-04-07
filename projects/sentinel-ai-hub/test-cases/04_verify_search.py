import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# TEST CASE 4: Verify Embeddings (Azure AI Search)
# Goal: Programmatically check the search index for Chicago data and vector population.

def check_embeddings():
    load_dotenv()
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    key = os.getenv("AZURE_SEARCH_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "sentinel-index")

    client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(key))
    
    # Search for Chicago specifically
    results = client.search(search_text="Chicago")
    
    print("\n--- TEST CASE 4: SEARCH INDEX VERIFICATION ---")
    found = False
    for result in results:
        found = True
        print(f"Found Doc: {result['title']}")
        # Check if vector field exists (not null)
        if result.get("content_vector"):
            print(f"✅ Vector Embedding: POPULATED (Length: {len(result['content_vector'])})")
        else:
            print("❌ Vector Embedding: MISSING")
    
    if not found:
        print("❌ No documents found for 'Chicago'.")
    print("--- TEST CASE 4 COMPLETE ---\n")

if __name__ == "__main__":
    check_embeddings()
