from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from packages.core.services import LLMFactory
import logging

logger = logging.getLogger(__name__)

def coder_node(state: dict):
    """
    Worker Agent 2: The Coder.
    It synthesizes pure requirements and outputs clean code based on the researcher's context.
    """
    llm = LLMFactory.create_llm()

    logger.info("Coder node starting")

    # The coder doesn't require specific web tools right now, just strict persona enforcement.
    coding_agent = create_react_agent(
        model=llm,
        tools=[],
        prompt="You are an Expert Staff Software Engineer. You write bulletproof, highly scalable, PEP-8 compliant Python code. Generate accurate implementations based purely on the Researcher's retrieved documentation. Do not guess syntaxes."
    )

    result = coding_agent.invoke({"messages": state["messages"]})
    
    last_msg = result["messages"][-1]
    logger.info("Coder node completed")
    return {
        "messages": [
            HumanMessage(content=last_msg.content, name="Coder")
        ]
    }
