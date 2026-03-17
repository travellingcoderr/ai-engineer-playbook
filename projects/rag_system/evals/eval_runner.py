import json
import os
import sys
from typing import List, Dict

# Add root and project to path for imports
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_ROOT = os.path.join(ROOT, "projects", "rag_system")
sys.path.insert(0, ROOT)
sys.path.insert(0, PROJECT_ROOT)

from app.services.rag import RAGService

def score_response(response: str, keywords: List[str]) -> float:
    """Simple keyword-based scoring for faithfulness."""
    if not response:
        return 0.0
    
    found = sum(1 for kw in keywords if kw.lower() in response.lower())
    return found / len(keywords)

def run_eval():
    print("🚀 Starting RAG Evaluation...")
    
    # Initialize RAG manually to bypass remote DB connection
    try:
        from app.services.rag import RAGService
        from app.services.embedding_factory import EmbeddingFactory
        from packages.core.config import get_config
        from langchain_chroma import Chroma
        
        config = get_config()
        
        # 1. Initialize Embeddings
        embeddings = EmbeddingFactory.create_embeddings(
            provider=config.embeddings.provider,
            model_name=config.embeddings.model,
            openai_api_key=config.llm.openai_api_key
        )
        
        # 2. Setup Local persistent vector store for evals
        persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
        vector_store = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings,
            collection_name="eval_collection"
        )
        
        # 3. Create RAG instance and patch it
        # We create a dummy instance and set its members to avoid the remote init
        rag = RAGService.__new__(RAGService)
        rag.config = config
        rag.embeddings = embeddings
        rag.vector_store = vector_store
        
        # Initialize LLM
        from packages.core.services import LLMFactory
        rag.llm = LLMFactory.create_llm(
            provider=config.llm.provider,
            model_name=config.llm.model,
            openai_api_key=config.llm.openai_api_key,
            gemini_api_key=config.llm.gemini_api_key
        )
        
        print(f"📦 Using local evaluation DB at {persist_dir}")
        
        # Check if DB is empty, if so, ingest a sample document
        if not rag.vector_store.get()["ids"]:
            print("📥 Evaluation DB is empty. Ingesting README.md for context...")
            readme_path = os.path.join(ROOT, "README.md")
            if os.path.exists(readme_path):
                rag.ingest_document(readme_path)
            else:
                print("⚠️ README.md not found, evaluation may fail due to lack of context.")

    except Exception as e:
        print(f"❌ Failed to initialize Evaluation Environment: {e}")
        import traceback
        traceback.print_exc()
        return

    # Load Dataset
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset.json")
    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    results = []
    total_score = 0.0

    for item in dataset:
        print(f"📝 Evaluating Q: {item['question']}")
        
        try:
            answer = rag.ask_question(item['question'])
            score = score_response(answer, item['expected_keywords'])
            
            results.append({
                "id": item["id"],
                "question": item["question"],
                "answer": answer,
                "score": score,
                "status": "PASS" if score > 0.5 else "FAIL"
            })
            total_score += score
            print(f"✅ Score: {score:.2f}")
        except Exception as e:
            print(f"❌ Error evaluating {item['id']}: {e}")
            results.append({
                "id": item["id"],
                "error": str(e),
                "status": "ERROR"
            })

    # Summary
    avg_score = total_score / len(dataset) if dataset else 0
    summary = {
        "average_score": avg_score,
        "total_evaluated": len(dataset),
        "results": results
    }

    output_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)

    print("-" * 30)
    print(f"📊 Final Average Score: {avg_score:.2f}")
    print(f"📂 Results saved to {output_path}")

if __name__ == "__main__":
    run_eval()
