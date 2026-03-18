from langchain_core.tools import tool
from sqlmodel import Session, select

from ..database import engine
from ..models.loan import Loan
from ..models.ticket import Ticket
from packages.core.services.rag.rag_service import RAGService
from packages.core.services.observability import ObservabilityClient
from packages.core.enums.observability import LogLevel
import os

obs_client = ObservabilityClient(service_name="mortgage_bot_backend")

@tool
def search_knowledge(query: str):
    """Searches the mortgage knowledge base for relevant guidelines and documentation."""
    obs_client.log(
        f"LangGraph tool search_knowledge called with query='{query}'",
        level=LogLevel.INFO,
    )
    connection_string = os.getenv("DATABASE_URL")
    rag = RAGService(connection_string=connection_string)
    results = rag.search(query, k=3)
    obs_client.log(
        f"LangGraph tool search_knowledge returned {len(results)} results",
        level=LogLevel.INFO,
    )
    return "\n\n".join([r.page_content for r in results])

@tool
def get_loan_details(loan_id: str):
    """Fetches loan details from the loans table and enriches them with ticket context."""
    obs_client.log(
        f"LangGraph tool get_loan_details called for loan_id='{loan_id}'",
        level=LogLevel.INFO,
    )

    with Session(engine) as session:
        loan_statement = select(Loan).where(Loan.loan_id == loan_id)
        loan = session.exec(loan_statement).first()
        statement = (
            select(Ticket)
            .where(Ticket.loan_id == loan_id)
            .order_by(Ticket.updated_at.desc())
        )
        tickets = session.exec(statement).all()

    if not loan:
        obs_client.log(
            f"LangGraph tool get_loan_details found no loan record for loan_id='{loan_id}'",
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
            "open_ticket_count": sum(1 for ticket in tickets if ticket.status.lower() not in {"resolved", "closed"}),
            "recent_ticket_subjects": [ticket.subject for ticket in tickets[:3]],
            "message": "No loan record was found for this loan ID.",
        }

    latest_ticket = tickets[0] if tickets else None
    open_ticket_count = sum(1 for ticket in tickets if ticket.status.lower() not in {"resolved", "closed"})
    recent_ticket_subjects = [ticket.subject for ticket in tickets[:3]]

    obs_client.log(
        f"LangGraph tool get_loan_details found a loan record and {len(tickets)} tickets for loan_id='{loan_id}'",
        level=LogLevel.INFO,
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
