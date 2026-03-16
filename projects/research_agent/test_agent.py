import sys
import os

# Ensure the root directory is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from projects.research_agent.agent import run

if __name__ == "__main__":
    topic = "What are the top 3 biggest AI news stories from March 2026?"
    print(f"Testing Research Agent with topic: '{topic}'\n")
    
    try:
        final_report = run(topic)
        print("\n================== FINAL REPORT ==================")
        print(final_report)
    except Exception as e:
        print(f"\nError occurred: {e}")
