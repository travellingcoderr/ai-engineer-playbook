import os
import logging
from typing import Dict, Any, Optional
from azure.identity import DefaultAzureCredential

# Setup logging
logger = logging.getLogger(__name__)

class SentinelSafetyEvaluator:
    """
    [RESPONSIBLE AI GUARDRAIL]
    Evaluates agent outputs for Content Safety (Hate, Violence) and 
    Groundedness (checking against source content).
    """
    
    def __init__(self):
        self.enabled = False
        try:
            from azure.ai.evaluation import ContentSafetyEvaluator, GroundednessEvaluator
            
            # Azure AI Project credentials
            self.project_config = {
                "subscription_id": os.getenv("AZURE_SUBSCRIPTION_ID"),
                "resource_group_name": os.getenv("AZURE_RESOURCE_GROUP_NAME"),
                "project_name": os.getenv("AZURE_PROJECT_NAME"),
            }
            
            if all(self.project_config.values()):
                self.credential = DefaultAzureCredential()
                self.content_safety = ContentSafetyEvaluator(
                    azure_ai_project=self.project_config,
                    credential=self.credential
                )
                self.groundedness = GroundednessEvaluator(
                    azure_ai_project=self.project_config,
                    credential=self.credential
                )
                self.enabled = True
                logger.info("AI-Assisted Safety Evaluators initialized successfully.")
            else:
                logger.warning("RAI Evaluation credentials missing. Using local fallback guardrails.")
                
        except ImportError:
            logger.warning("azure-ai-evaluation SDK not found. Using local fallback guardrails.")

    async def validate_response(self, query: str, response: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Runs safety and groundedness checks on a response.
        Returns a safety report.
        """
        if self.enabled:
            try:
                # 1. Content Safety Check
                safety_report = self.content_safety(query=query, response=response)
                
                # values > 3 are high risk in Azure AI Safety
                is_safe = all(score < 3 for score in safety_report.values() if isinstance(score, (int, float)))
                
                # 2. Groundedness check (if context exists)
                grounded_score = 1.0
                if context:
                    g_report = self.groundedness(query=query, response=response, context=context)
                    grounded_score = g_report.get("groundedness", 1.0)

                return {
                    "is_safe": is_safe,
                    "groundeded_score": grounded_score,
                    "full_report": safety_report,
                    "provider": "Azure AI Evaluation"
                }
            except Exception as e:
                logger.error(f"AI Evaluation failed: {e}. Falling back to local check.")

        # --- LOCAL FALLBACK GUARDRAIL ---
        # Minimalist keyword-based safety for demo purposes
        restricted_keywords = ["violence", "attack", "harm", "illegal", "hack"]
        found_restricted = [w for w in restricted_keywords if w in response.lower()]
        
        return {
            "is_safe": len(found_restricted) == 0,
            "groundeded_score": 1.0, # Cannot check without AI
            "violations": found_restricted,
            "provider": "Local Keyword Filter"
        }

if __name__ == "__main__":
    # Quick test
    evaluator = SentinelSafetyEvaluator()
    import asyncio
    async def test():
        res = await evaluator.validate_response("hi", "I am safe and helpful.")
        print(f"Safety Report: {res}")
    asyncio.run(test())
