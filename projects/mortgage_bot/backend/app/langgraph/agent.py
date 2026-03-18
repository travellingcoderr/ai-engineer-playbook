from typing import Annotated, TypedDict, List, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from .tools import search_knowledge, get_loan_details
from packages.core.services.llm_factory import LLMFactory

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    loan_id: str
    context: dict

def create_mortgage_bot_agent():
    tools = [search_knowledge, get_loan_details]
    llm = LLMFactory.create_llm().bind_tools(tools)
    
    workflow = StateGraph(AgentState)
    
    def call_model(state: AgentState):
        # ReAct "Reason" step:
        # the model reads the running conversation and decides whether to answer
        # directly or request one of the bound tools.
        messages = state['messages']
        response = llm.invoke(messages)
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
            return "tools"
        return END

    # ReAct loop:
    # agent -> tools -> agent lets the model reason, act with tools,
    # observe tool outputs, and then reason again before answering.
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()
