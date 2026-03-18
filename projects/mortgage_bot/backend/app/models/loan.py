from datetime import datetime
from typing import Optional
import uuid

from sqlmodel import SQLModel, Field, Column, JSON


class LoanBase(SQLModel):
    loan_id: str
    borrower_name: str
    property_address: Optional[str] = None
    loan_type: Optional[str] = None
    loan_amount: Optional[float] = None
    status: str = "new"
    milestone: str = "application"
    assigned_officer: Optional[str] = None
    external_loan_id: Optional[str] = None
    source_system: str = "internal"


class Loan(LoanBase, table=True):
    __tablename__ = "loans"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    additional_metadata: dict = Field(default_factory=dict, sa_column=Column("metadata", JSON))


class LoanCreate(LoanBase):
    additional_metadata: dict = Field(default_factory=dict)
