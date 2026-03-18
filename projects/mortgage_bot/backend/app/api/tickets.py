from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError

from ..database import get_session
from ..data.ticket_repository import TicketRepository
from ..models.ticket import Ticket, TicketCreate, TicketCreateResponse

router = APIRouter()

def get_ticket_repository(
    session: Session = Depends(get_session),
) -> TicketRepository:
    # FastAPI creates a fresh database session per request.
    # We build the repository from that session so each request gets isolated DB state.
    return TicketRepository(session)

@router.get("/", response_model=List[Ticket])
async def list_tickets(
    repository: TicketRepository = Depends(get_ticket_repository),
):
    return repository.list_tickets()

@router.post("/", response_model=TicketCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket: TicketCreate,
    repository: TicketRepository = Depends(get_ticket_repository),
):
    try:
        db_ticket = repository.create_ticket(ticket)
    except SQLAlchemyError as exc:
        # The repository and the route share the same request-scoped session,
        # so rolling back here safely clears the failed transaction.
        repository.session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "ticket_id": None,
                "message": f"Failed to create ticket: {exc.__class__.__name__}",
            },
        ) from exc

    return TicketCreateResponse(
        success=True,
        ticket_id=db_ticket.id,
        message="Ticket created successfully",
    )
