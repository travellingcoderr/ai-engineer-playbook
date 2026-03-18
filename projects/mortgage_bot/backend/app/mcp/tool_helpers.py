import os

from sqlmodel import Session, select

from ..database import engine
from ..models.loan import Loan
from ..models.ticket import Ticket
from packages.core.enums.observability import LogLevel
from packages.core.services.observability import ObservabilityClient
from packages.core.services.rag.rag_service import RAGService

obs_client = ObservabilityClient(service_name="mortgage_bot_backend")


def log_tool_call(tool_name: str, message: str, level: LogLevel = LogLevel.INFO) -> None:
    obs_client.log(
        f"MCP tool {tool_name}: {message}",
        level=level,
    )


def load_loan_with_tickets(loan_id: str) -> tuple[Loan | None, list[Ticket]]:
    with Session(engine) as session:
        loan = session.exec(select(Loan).where(Loan.loan_id == loan_id)).first()
        tickets = session.exec(
            select(Ticket).where(Ticket.loan_id == loan_id).order_by(Ticket.updated_at.desc())
        ).all()
    return loan, tickets


def get_rag_service() -> RAGService:
    connection_string = os.getenv("DATABASE_URL")
    return RAGService(connection_string=connection_string, collection_name="knowledge")
