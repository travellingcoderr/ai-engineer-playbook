from typing import Annotated, TypedDict, List, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from ..mcp.server import MCP_TOOLS
from packages.core.enums.observability import LogLevel
from packages.core.services.llm_factory import LLMFactory
from packages.core.services.observability import ObservabilityClient

obs_client = ObservabilityClient(service_name="mortgage_bot_backend")

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    loan_id: str
    context: dict

def create_mortgage_bot_agent():
    tools = MCP_TOOLS
    llm = LLMFactory.create_llm().bind_tools(tools)
    
    workflow = StateGraph(AgentState)
    
    def call_model(state: AgentState):
        # ReAct "Reason" step:
        # the model reads the running conversation and decides whether to answer
        # directly or request one of the bound tools.
        messages = state['messages']
        latest_message = messages[-1] if messages else None
        if latest_message:
            obs_client.log(
                message=(
                    "LangGraph agent reason step started with "
                    f"message_type={latest_message.__class__.__name__}"
                ),
                level=LogLevel.INFO,
            )
        response = llm.invoke(messages)
        if getattr(response, "tool_calls", None):
            tool_names = [tool_call.get("name", "unknown_tool") for tool_call in response.tool_calls]
            obs_client.log(
                message=f"LangGraph agent requested tool calls: {', '.join(tool_names)}",
                level=LogLevel.INFO,
            )
        else:
            obs_client.log(
                message="LangGraph agent produced a final answer without additional tool calls",
                level=LogLevel.INFO,
            )
        return {"messages": [response]}
    
    workflow.add_node("agent", call_model)
    # ReAct "Act" step:
    # when the model emits tool calls, LangGraph executes them through this node.
    workflow.add_node("tools", ToolNode(tools))
    
    workflow.set_entry_point("agent")
    
    def should_continue(state: AgentState):
        messages = state['messages']
        last_message = messages[-1]
        # This conditional is the ReAct decision point.
        # If the model asked for tools, continue to the action node.
        # Otherwise, stop and return the final answer.
        if last_message.tool_calls:
            obs_client.log(
                message="LangGraph agent transitioning from reason step to tool execution",
                level=LogLevel.INFO,
            )
            return "tools"
        obs_client.log(
            message="LangGraph agent finished the ReAct loop and is returning the response",
            level=LogLevel.INFO,
        )
        return END

    # ReAct loop:
    # agent -> tools -> agent lets the model reason, act with tools,
    # observe tool outputs, and then reason again before answering.
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()
