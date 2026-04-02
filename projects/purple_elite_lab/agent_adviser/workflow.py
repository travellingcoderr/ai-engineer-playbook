import time
import random

# 🤖 Agent 1: The Market Analyst
class MarketAnalyst:
    def analyze(self, data):
        print("🧠 [Analyst] Scanning Tech and Healthcare sectors...")
        time.sleep(1)
        # Randomly choose between a good and bad recommendation for demo
        return {
            "action": "BUY", 
            "assets": ["AAPL", "JNJ"], 
            "reason": "Strong earnings forecast and stable dividends.",
            "risk_score": random.randint(1, 10)
        }

# 🤖 Agent 2: The Risk Reviewer (The Governance Layer)
class RiskReviewer:
    def review(self, analysis):
        print(f"⚖️ [Reviewer] Auditing Analyst results (Risk Score: {analysis['risk_score']})...")
        time.sleep(1)
        if analysis['risk_score'] > 7:
            return "REJECTED: Risk exceeds individual investor threshold."
        return "APPROVED: Portfolio aligns with client risk profile."

# 🕸️ The LangGraph-style Workflow
class PortfolioAdvisoryWorkflow:
    def __init__(self):
        self.analyst = MarketAnalyst()
        self.reviewer = RiskReviewer()
        self.state = "START"
        self.history = []

    def run(self, user_request):
        print(f"🚀 [Workflow] Starting for request: {user_request}")
        
        # 1. State: ANALYSIS
        self.state = "ANALYSIS"
        analysis_result = self.analyst.analyze(user_request)
        self.history.append(analysis_result)

        # 2. State: REVIEW
        self.state = "REVIEW"
        review_result = self.reviewer.review(analysis_result)
        
        # 3. Final State: DECISION
        if "APPROVED" in review_result:
            self.state = "COMPLETED"
            print("✅ [Success] Final Investment Plan Ready!")
        else:
            self.state = "REJECTED"
            print("❌ [Failure] Analyst must retry with safer assets.")

        return {
            "final_state": self.state,
            "decision": review_result,
            "analyst_log": analysis_result
        }

# 🧪 Demo
if __name__ == "__main__":
    workflow = PortfolioAdvisoryWorkflow()
    result = workflow.run("Create a growth portfolio with $50k.")
    
    print("\n--- Workflow Execution Log ---")
    print(f"Status: {result['final_state']}")
    print(f"Decision: {result['decision']}")
    print("\n💡 Interview Tip: Mention that 'Stateful Agents' (like LangGraph)")
    print("allow for multi-step reasoning and human-in-the-loop validation,")
    print("which is critical for high-stakes financial services at Purple.")
