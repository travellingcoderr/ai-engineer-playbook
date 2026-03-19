from datetime import datetime
from typing import Optional
import uuid

from sqlmodel import Field, SQLModel, Column, JSON


class WorkerJobBase(SQLModel):
    job_id: str
    queue_name: str
    task_name: str
    status: str = "queued"
    document_id: Optional[str] = None
    error_message: Optional[str] = None
    payload: dict = Field(default_factory=dict, sa_column=Column(JSON))


class WorkerJob(WorkerJobBase, table=True):
    __tablename__ = "worker_jobs"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    enqueued_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
