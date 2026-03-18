from langchain_core.tools import tool

from .tool_helpers import load_loan_with_tickets, log_tool_call
from packages.core.enums.observability import LogLevel


@tool
def get_borrower_profile(loan_id: str):
    """Returns borrower profile details stored with the mock mortgage loan record."""
    log_tool_call("get_borrower_profile", f"called for loan_id='{loan_id}'")
    loan, _ = load_loan_with_tickets(loan_id)

    if not loan:
        log_tool_call(
            "get_borrower_profile",
            f"no loan record found for loan_id='{loan_id}'",
            level=LogLevel.ERROR,
        )
        return {"loan_id": loan_id, "borrower_profile": None, "message": "Loan not found."}

    return {
        "loan_id": loan_id,
        "borrower_name": loan.borrower_name,
        "borrower_profile": loan.additional_metadata.get("borrower_profile", {}),
        "message": "Borrower profile loaded from mock LOS metadata.",
    }
