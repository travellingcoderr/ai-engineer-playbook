from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from ..data.loan_repository import LoanRepository
from ..database import get_session
from ..models.loan import Loan, LoanCreate
from packages.core.services.observability import ObservabilityClient
from packages.core.enums.observability import LogLevel

router = APIRouter()
obs_client = ObservabilityClient(service_name="mortgage_bot_backend")


def get_loan_repository(
    session: Session = Depends(get_session),
) -> LoanRepository:
    return LoanRepository(session)


@router.get("/", response_model=List[Loan])
async def list_loans(
    repository: LoanRepository = Depends(get_loan_repository),
):
    loans = repository.list_loans()
    obs_client.log(
        f"/api/loans returned {len(loans)} loans",
        level=LogLevel.INFO,
    )
    return loans


@router.get("/{loan_id}", response_model=Loan)
async def get_loan(
    loan_id: str,
    repository: LoanRepository = Depends(get_loan_repository),
):
    loan = repository.get_by_loan_id(loan_id)
    if not loan:
        obs_client.log(
            f"/api/loans/{loan_id} returned 404",
            level=LogLevel.ERROR,
        )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")

    obs_client.log(
        f"/api/loans/{loan_id} returned loan data",
        level=LogLevel.INFO,
    )
    return loan


@router.post("/", response_model=Loan, status_code=status.HTTP_201_CREATED)
async def create_or_update_loan(
    loan_create: LoanCreate,
    repository: LoanRepository = Depends(get_loan_repository),
):
    try:
        existing_loan = repository.get_by_loan_id(loan_create.loan_id)
        if existing_loan:
            loan = repository.update_loan(existing_loan, loan_create)
            obs_client.log(
                f"/api/loans upsert updated loan_id='{loan.loan_id}'",
                level=LogLevel.INFO,
            )
            return loan

        loan = repository.create_loan(loan_create)
        obs_client.log(
            f"/api/loans created loan_id='{loan.loan_id}'",
            level=LogLevel.INFO,
        )
        return loan
    except SQLAlchemyError as exc:
        repository.session.rollback()
        obs_client.log(
            f"/api/loans failed for loan_id='{loan_create.loan_id}' with {exc.__class__.__name__}",
            level=LogLevel.ERROR,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist loan",
        ) from exc
