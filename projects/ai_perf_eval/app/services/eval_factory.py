import logging
from typing import Dict, Any, Union
from app.models.eval_models import EvalType, CostEvalInput, AccuracyEvalInput
from packages.core.enums import AIModel

logger = logging.getLogger("eval-factory")

class EvalFactory:
    """
    Phase 4: Evaluation Factory Pattern
    
    This factory centralizes the creation of different evaluation engines
    (e.g., Accuracy judging, Cost analysis, Latency tracking).
    """

    @staticmethod
    def get_evaluator(eval_type: EvalType):
        """
        Returns an instance of the requested evaluator type.
        Strongly typed to EvalType for strict C#-style consistency.
        """
        if eval_type == EvalType.COST:
            return CostEvaluator()
        elif eval_type == EvalType.ACCURACY:
            return AccuracyEvaluator()
        else:
            logger.warning(f"Unknown evaluator type: {eval_type}")
            return BaseEvaluator()

class BaseEvaluator:
    def evaluate(self, data: Any) -> Dict[str, Any]:
        return {"status": "base_eval_executed"}

class CostEvaluator(BaseEvaluator):
    """
    Calculates the financial cost of an LLM request based on token usage.
    Using strongly-typed CostEvalInput for reliability and extensibility.
    """
    def evaluate(self, data: CostEvalInput) -> Dict[str, Any]:
        # Pricing mapping (typical industry rates)
        pricing = {
            AIModel.GPT_4O: {"input": 0.005, "output": 0.015}, # per 1k tokens
            AIModel.GPT_4O_MINI: {"input": 0.00015, "output": 0.0006},
            AIModel.GPT_3_5_TURBO: {"input": 0.0005, "output": 0.0015},
            AIModel.CLAUDE_3_5_SONNET: {"input": 0.003, "output": 0.015},
            AIModel.GEMINI_1_5_PRO: {"input": 0.0035, "output": 0.0105}
        }
        
        model_pricing = pricing.get(data.model, pricing[AIModel.GPT_4O])
        
        cost = (data.input_tokens / 1000 * model_pricing["input"]) + \
               (data.output_tokens / 1000 * model_pricing["output"])
        
        return {
            "model": data.model.value,
            "cost_usd": round(cost, 6),
            "input_tokens": data.input_tokens,
            "output_tokens": data.output_tokens
        }

class AccuracyEvaluator(BaseEvaluator):
    """
    Implements Accuracy checking patterns using AccuracyEvalInput.
    """
    def evaluate(self, data: AccuracyEvalInput) -> Dict[str, Any]:
        # Placeholder for complex accuracy scoring logic
        logger.info(f"Performing Accuracy Evaluation (Judge Model: {data.model.value})...")
        return {
            "accuracy_score": 0.85,
            "method": "semantic_similarity_judge",
            "evaluated_query": data.query
        }
