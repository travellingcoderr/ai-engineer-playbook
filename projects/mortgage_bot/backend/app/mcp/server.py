from .get_borrower_profile import get_borrower_profile
from .get_loan_details import get_loan_details
from .get_milestone_history import get_milestone_history
from .list_loan_conditions import list_loan_conditions
from .search_knowledge import search_knowledge

# This is a lightweight in-app MCP-style registry for learning.
# In a full remote MCP setup, these tool definitions would be exposed by a separate server process.
MCP_TOOLS = [
    search_knowledge,
    get_loan_details,
    list_loan_conditions,
    get_borrower_profile,
    get_milestone_history,
]
