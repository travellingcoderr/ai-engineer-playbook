from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from datetime import datetime
import uuid

class TicketBase(SQLModel):
    user_id: str
    user_email: str
    user_name: str
    subject: str
    description: str
    category: str
    severity: str = "medium"
    status: str = "open"
    loan_id: Optional[str] = None

class Ticket(TicketBase, table=True):
    __tablename__ = "support_tickets"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    context: dict = Field(default={}, sa_column=Column(JSON))

class TicketCreate(TicketBase):
    pass
