import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage

class TeamState(TypedDict):
    """
    The central memory of the Agent Team. 
    It tracks the entire message history and the supervisor's routing decisions.
    """
    # operator.add ensures that returned messages from workers are appended to the main history
    messages: Annotated[Sequence[BaseMessage], operator.add]
    
    # The supervisor explicitly injects the next worker into the state
    next: str
