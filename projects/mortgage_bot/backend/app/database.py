from sqlmodel import create_engine, Session, SQLModel, select
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://saga_user:saga_password@localhost:5432/saga_db",
)

engine = create_engine(DATABASE_URL)


def seed_loans():
    from .models.loan import Loan

    sample_loans = [
        Loan(
            loan_id="LN-1001",
            borrower_name="Ava Thompson",
            property_address="1428 Cedar Grove Ln, Charlotte, NC",
            loan_type="Conventional",
            loan_amount=425000,
            status="processing",
            milestone="underwriting",
            assigned_officer="Mia Rodriguez",
            external_loan_id="LOS-9001",
            source_system="mock-los",
            additional_metadata={"fico_band": "740+", "occupancy": "primary"},
        ),
        Loan(
            loan_id="LN-1002",
            borrower_name="Noah Patel",
            property_address="88 Harbor View Dr, Tampa, FL",
            loan_type="FHA",
            loan_amount=315000,
            status="condition_review",
            milestone="appraisal",
            assigned_officer="Daniel Kim",
            external_loan_id="LOS-9002",
            source_system="mock-los",
            additional_metadata={"fico_band": "680-719", "occupancy": "primary"},
        ),
        Loan(
            loan_id="LN-1003",
            borrower_name="Sophia Martinez",
            property_address="517 Willow Bend Rd, Austin, TX",
            loan_type="VA",
            loan_amount=510000,
            status="clear_to_close",
            milestone="closing",
            assigned_officer="Harper Lee",
            external_loan_id="LOS-9003",
            source_system="mock-los",
            additional_metadata={"fico_band": "720-739", "occupancy": "primary"},
        ),
    ]

    with Session(engine) as session:
        for sample_loan in sample_loans:
            existing_loan = session.exec(
                select(Loan).where(Loan.loan_id == sample_loan.loan_id)
            ).first()
            if existing_loan:
                continue

            session.add(sample_loan)

        session.commit()

def init_db():
    # Import models here to ensure they are registered with SQLModel.metadata
    from .models.ticket import Ticket
    from .models.loan import Loan
    from .models.knowledge import KnowledgeDocument, KnowledgeChunk
    
    # Ensure pgvector extension is enabled
    from sqlalchemy import text
    with Session(engine) as session:
        session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        session.commit()
        
    SQLModel.metadata.create_all(engine)
    seed_loans()

    # Ensure uploads directory exists
    os.makedirs("/app/uploads", exist_ok=True)

def get_session():
    with Session(engine) as session:
        yield session
