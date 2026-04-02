import numpy as np

# 🧠 Mocking a Vector Database (like Chroma or Pinecone)
class FinancialVectorDB:
    def __init__(self):
        # Sample "Documents" - Investment Policies
        self.documents = {
            "policy_tech": "Tech sector exposure must not exceed 40% of the total portfolio.",
            "policy_crypto": "No cryptocurrency assets are allowed in 'Moderate Risk' portfolios.",
            "policy_esg": "At least 10% of assets must be in high-ranking ESG (Environmental, Social, Governance) funds.",
            "policy_cash": "Maintain a minimum cash reserve of 5% for liquidity."
        }
        # In a real system, these would be high-dimensional vectors (Embeddings)
        self.keywords = {
            "tech": "policy_tech",
            "crypto": "policy_crypto",
            "risk": "policy_crypto",
            "esg": "policy_esg",
            "money": "policy_cash",
            "cash": "policy_cash"
        }

    def query(self, query_text):
        """
        Simulates a semantic search by matching keywords.
        In production, this would use Cosine Similarity on embeddings.
        """
        query_text = query_text.lower()
        results = []
        for kw, doc_id in self.keywords.items():
            if kw in query_text:
                results.append(self.documents[doc_id])
        
        return list(set(results)) # Unique matches

# 🏦 The RAG Engine
class FinancialRAG:
    def __init__(self):
        self.db = FinancialVectorDB()

    def get_context(self, user_prompt):
        print(f"🔍 [RAG] Searching for policies related to: '{user_prompt}'")
        relevant_docs = self.db.query(user_prompt)
        
        if not relevant_docs:
            return "No specific policy constraints found."
        
        # Format the context for the LLM
        context = "\n".join([f"- {doc}" for doc in relevant_docs])
        return f"RELEVANT INVESTMENT POLICIES:\n{context}"

# 🧪 Demo
if __name__ == "__main__":
    rag = FinancialRAG()
    prompt = "I want to invest heavily in Bitcoin and Tech stocks."
    context = rag.get_context(prompt)
    
    print("\n--- Context for LLM ---")
    print(context)
    print("\n💡 Interview Tip: Explain that RAG reduces 'hallucinations'")
    print("by giving the LLM a 'ground truth' document to read from.")
