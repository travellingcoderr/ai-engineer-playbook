from sqlmodel import create_engine, Session, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://saga_user:saga_password@localhost:5432/saga_db")

engine = create_engine(DATABASE_URL)

def init_db():
    # Import models here to ensure they are registered with SQLModel.metadata
    from .models.ticket import Ticket
    from .models.knowledge import KnowledgeDocument, KnowledgeChunk
    
    # Ensure pgvector extension is enabled
    from sqlalchemy import text
    with Session(engine) as session:
        session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        session.commit()
        
    SQLModel.metadata.create_all(engine)

    # Ensure uploads directory exists
    os.makedirs("/app/uploads", exist_ok=True)

def get_session():
    with Session(engine) as session:
        yield session
