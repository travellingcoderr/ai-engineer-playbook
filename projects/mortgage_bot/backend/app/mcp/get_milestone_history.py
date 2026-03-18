from langchain_core.tools import tool

from .tool_helpers import load_loan_with_tickets, log_tool_call
from packages.core.enums.observability import LogLevel


@tool
def get_milestone_history(loan_id: str):
    """Returns milestone progression history for a mortgage loan."""
    log_tool_call("get_milestone_history", f"called for loan_id='{loan_id}'")
    loan, _ = load_loan_with_tickets(loan_id)

    if not loan:
        log_tool_call(
            "get_milestone_history",
            f"no loan record found for loan_id='{loan_id}'",
            level=LogLevel.ERROR,
        )
        return {"loan_id": loan_id, "milestone_history": [], "message": "Loan not found."}

    return {
        "loan_id": loan_id,
        "current_milestone": loan.milestone,
        "milestone_history": loan.additional_metadata.get("milestone_history", []),
        "message": "Milestone history loaded from mock LOS metadata.",
    }
