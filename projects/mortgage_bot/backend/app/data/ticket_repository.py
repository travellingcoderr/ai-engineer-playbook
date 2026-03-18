from sqlmodel import Session, select

from ..models.ticket import Ticket, TicketCreate


class TicketRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_tickets(self) -> list[Ticket]:
        statement = select(Ticket).order_by(Ticket.created_at.desc())
        return self.session.exec(statement).all()

    def create_ticket(self, ticket_create: TicketCreate) -> Ticket:
        ticket = Ticket.model_validate(ticket_create)
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return ticket
