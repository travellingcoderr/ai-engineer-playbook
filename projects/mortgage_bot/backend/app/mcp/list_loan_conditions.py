from langchain_core.tools import tool

from .tool_helpers import load_loan_with_tickets, log_tool_call
from packages.core.enums.observability import LogLevel


@tool
def list_loan_conditions(loan_id: str):
    """Returns underwriting or processing conditions for a loan."""
    log_tool_call("list_loan_conditions", f"called for loan_id='{loan_id}'")
    loan, _ = load_loan_with_tickets(loan_id)

    if not loan:
        log_tool_call(
            "list_loan_conditions",
            f"no loan record found for loan_id='{loan_id}'",
            level=LogLevel.ERROR,
        )
        return {"loan_id": loan_id, "conditions": [], "open_condition_count": 0, "message": "Loan not found."}

    conditions = loan.additional_metadata.get("conditions", [])
    open_conditions = [condition for condition in conditions if condition.get("status") == "open"]
    return {
        "loan_id": loan_id,
        "conditions": conditions,
        "open_condition_count": len(open_conditions),
        "message": "Conditions loaded from mock LOS metadata.",
    }
