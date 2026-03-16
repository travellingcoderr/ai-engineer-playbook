from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel
from typing import Literal
from packages.core.llm_factory import LLMFactory

# Defines our autonomous workforce
MEMBERS = ["Researcher", "Coder"]

def supervisor_node(state: dict):
    """
    The orchestrator node. It takes the entire message history, evaluates progress, 
    and outputs exactly one string determining who should act next, or 'FINISH'.
    """
    llm = LLMFactory.create_llm()
    
    # We must explicitly type Literal to force the LLM to pick exactly one of these strings
    # We dynamically create the signature since MEMBERS can change
    options = ["FINISH"] + MEMBERS
    
    # A bit of python class metaprogramming to create the Pydantic type dynamically
    class RouteResponse(BaseModel):
        next: Literal[tuple(options)] # type: ignore
        
    structured_router = llm.with_structured_output(RouteResponse)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are a Senior Project Manager orchestrating a team consisting of the following workers: {members}. "
         "Given the following ongoing conversation and user request, your job is to route to the correct worker. "
         "Each worker will perform a task and respond with their findings. "
         "When the final goal has been fully resolved and the answer is complete, route to FINISH. "
         "DO NOT answer the user's prompt directly. Your ONLY job is to route to a specialized worker or finish."
        ),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    supervisor_chain = prompt | structured_router
    
    result = supervisor_chain.invoke({
        "messages": state["messages"],
        "members": ", ".join(MEMBERS)
    })
    
    return {"next": result.next}
