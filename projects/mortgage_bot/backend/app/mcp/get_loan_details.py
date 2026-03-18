from langchain_core.tools import tool

from .tool_helpers import load_loan_with_tickets, log_tool_call
from packages.core.enums.observability import LogLevel


@tool
def get_loan_details(loan_id: str):
    """Returns live loan details for a loan and enriches them with related ticket context."""
    log_tool_call("get_loan_details", f"called for loan_id='{loan_id}'")
    loan, tickets = load_loan_with_tickets(loan_id)

    if not loan:
        log_tool_call(
            "get_loan_details",
            f"no loan record found for loan_id='{loan_id}'",
            level=LogLevel.ERROR,
        )
        return {
            "loan_id": loan_id,
            "status": "unknown",
            "milestone": "unknown",
            "borrower_name": None,
            "property_address": None,
            "loan_type": None,
            "loan_amount": None,
            "assigned_officer": None,
            "last_updated": None,
            "ticket_count": len(tickets),
            "open_ticket_count": sum(
                1 for ticket in tickets if ticket.status.lower() not in {"resolved", "closed"}
            ),
            "recent_ticket_subjects": [ticket.subject for ticket in tickets[:3]],
            "message": "No loan record was found for this loan ID.",
        }

    latest_ticket = tickets[0] if tickets else None
    open_ticket_count = sum(
        1 for ticket in tickets if ticket.status.lower() not in {"resolved", "closed"}
    )
    recent_ticket_subjects = [ticket.subject for ticket in tickets[:3]]
    log_tool_call(
        "get_loan_details",
        f"found loan record and {len(tickets)} related tickets for loan_id='{loan_id}'",
    )
    return {
        "loan_id": loan_id,
        "borrower_name": loan.borrower_name,
        "property_address": loan.property_address,
        "loan_type": loan.loan_type,
        "loan_amount": loan.loan_amount,
        "status": loan.status,
        "milestone": loan.milestone,
        "assigned_officer": loan.assigned_officer,
        "source_system": loan.source_system,
        "last_updated": loan.updated_at.isoformat(),
        "ticket_count": len(tickets),
        "open_ticket_count": open_ticket_count,
        "recent_ticket_subjects": recent_ticket_subjects,
        "latest_ticket_id": str(latest_ticket.id) if latest_ticket else None,
        "latest_reported_by": latest_ticket.user_name if latest_ticket else None,
        "message": "Loan details were loaded from the loans table and enriched with ticket context.",
    }
