from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from packages.core.llm_factory import LLMFactory
from packages.core.tool_factory import ToolFactory
from app.core.config import get_research_config
from app.agent.state import ResearchState
from app.agent.prompts import RESEARCHER_SYSTEM_PROMPT, WRITER_SYSTEM_PROMPT

def create_research_graph() -> StateGraph:
    """
    Builds and compiles the LangGraph state machine representing the autonomous agent.
    """
    config = get_research_config()
    
    # Instantiate LLM and Tools using our standardized factories
    llm = LLMFactory.create_llm(
        provider=config.llm.provider,
        model_name=config.llm.model,
        openai_api_key=config.llm.openai_api_key
    )
    tools = ToolFactory.create_tools()
    
    # Bind the tools to the LLM so it knows *how* to call them
    llm_with_tools = llm.bind_tools(tools)
    
    # ---------------------------
    # Node 1: The Researcher
    # ---------------------------
    def researcher_node(state: ResearchState):
        messages = state["messages"]
        topic = state["topic"]
        loop_count = state.get("loop_count", 0)
        
        # On the very first loop, set the system prompt
        if loop_count == 0:
            sys_msg = SystemMessage(content=RESEARCHER_SYSTEM_PROMPT.format(topic=topic))
            messages = [sys_msg] + messages
            
        # Get the LLM's next action (either a tool call, or text output)
        response = llm_with_tools.invoke(messages)
        return {"messages": [response], "loop_count": loop_count + 1}
        
    # ---------------------------
    # Node 2: The Tool Executor
    # ---------------------------
    # LangGraph provides a built-in ToolNode that executes the tools requested by the LLM
    tool_node = ToolNode(tools)
    
    # ---------------------------
    # Node 3: The Writer
    # ---------------------------
    def writer_node(state: ResearchState):
        topic = state["topic"]
        # Extract all tool responses and LLM thoughts to pass as context
        research_context = "\n".join([m.content for m in state["messages"] if hasattr(m, "content") and m.content])
        
        prompt = WRITER_SYSTEM_PROMPT.format(topic=topic, research=research_context)
        
        # Notice we use the raw LLM here, NOT the one bound with tools. 
        # The writer's *only* job is writing, not searching.
        response = llm.invoke([HumanMessage(content=prompt)])
        
        return {"final_report": response.content}
        
    # ---------------------------
    # Edge Logic (Routing)
    # ---------------------------
    def should_continue(state: ResearchState):
        """
        Determines the next step based on the Researcher LLM's output.
        - If it called a tool -> go to tool node.
        - If it output "DONE" -> go to writer node.
        - If it hit the max loop config bounds -> force go to writer node.
        """
        last_message = state["messages"][-1]
        
        if state.get("loop_count", 0) >= config.agent.max_loops:
            return "writer"
            
        # If the LLM returned tool calls, route to the tools
        if hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0:
            return "tools"
            
        # If it didn't call a tool, assume it feels done researching
        return "writer"

    # ---------------------------
    # Construct the Graph
    # ---------------------------
    workflow = StateGraph(ResearchState)
    
    # Add our 3 nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("writer", writer_node)
    
    # Define the execution flow
    workflow.set_entry_point("researcher")
    
    # The researcher decides whether to use tools or write
    workflow.add_conditional_edges(
        "researcher",
        should_continue,
        {
            "tools": "tools",
            "writer": "writer"
        }
    )
    
    # After using tools, ALWAYS go back to the researcher to evaluate the new data
    workflow.add_edge("tools", "researcher")
    
    # The writer is the final step
    workflow.add_edge("writer", END)
    
    return workflow.compile()
