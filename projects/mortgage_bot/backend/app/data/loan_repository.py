from datetime import datetime

from sqlmodel import Session, select

from ..models.loan import Loan, LoanCreate


class LoanRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_loans(self) -> list[Loan]:
        statement = select(Loan).order_by(Loan.updated_at.desc())
        return self.session.exec(statement).all()

    def get_by_loan_id(self, loan_id: str) -> Loan | None:
        statement = select(Loan).where(Loan.loan_id == loan_id)
        return self.session.exec(statement).first()

    def create_loan(self, loan_create: LoanCreate) -> Loan:
        loan = Loan.model_validate(loan_create)
        self.session.add(loan)
        self.session.commit()
        self.session.refresh(loan)
        return loan

    def update_loan(self, loan: Loan, loan_update: LoanCreate) -> Loan:
        loan.borrower_name = loan_update.borrower_name
        loan.property_address = loan_update.property_address
        loan.loan_type = loan_update.loan_type
        loan.loan_amount = loan_update.loan_amount
        loan.status = loan_update.status
        loan.milestone = loan_update.milestone
        loan.assigned_officer = loan_update.assigned_officer
        loan.external_loan_id = loan_update.external_loan_id
        loan.source_system = loan_update.source_system
        loan.additional_metadata = loan_update.additional_metadata
        loan.updated_at = datetime.utcnow()
        self.session.add(loan)
        self.session.commit()
        self.session.refresh(loan)
        return loan
