from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from packages.core.llm_factory import LLMFactory
from packages.core.tool_factory import ToolFactory

def researcher_node(state: dict):
    """
    Worker Agent 1: The Researcher.
    It receives the full conversation state but is equipped with web execution tools.
    """
    llm = LLMFactory.create_llm()
    tools = ToolFactory.create_research_tools()
    
    # LangGraph gives us a handy prebuilt ReAct agent template
    research_agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier="You are a Senior Technical Researcher. You must use your web search tools to find the exact, accurate information required. If your first search fails, refine your queries and try again until you succeed."
    )
    
    # The react agent runs internally until its thought-action-observation loop finishes
    result = research_agent.invoke({"messages": state["messages"]})
    
    # We take the final result from the researcher and append it back to the main State as a "HumanMessage"
    # labeled with a custom name so the Supervisor knows exactly who said what.
    last_msg = result["messages"][-1]
    return {
        "messages": [
            HumanMessage(content=last_msg.content, name="Researcher")
        ]
    }
