from datetime import datetime

from sqlmodel import Session, select

from ..models.worker_job import WorkerJob


class WorkerJobRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_job(
        self,
        *,
        job_id: str,
        queue_name: str,
        task_name: str,
        document_id: str | None = None,
        payload: dict | None = None,
    ) -> WorkerJob:
        job = WorkerJob(
            job_id=job_id,
            queue_name=queue_name,
            task_name=task_name,
            status="queued",
            document_id=document_id,
            payload=payload or {},
        )
        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job

    def get_by_job_id(self, job_id: str) -> WorkerJob | None:
        statement = select(WorkerJob).where(WorkerJob.job_id == job_id)
        return self.session.exec(statement).first()

    def update_status(
        self,
        *,
        job_id: str,
        status: str,
        error_message: str | None = None,
    ) -> WorkerJob | None:
        job = self.get_by_job_id(job_id)
        if not job:
            return None

        now = datetime.utcnow()
        job.status = status
        job.updated_at = now
        job.error_message = error_message

        if status == "processing" and not job.started_at:
            job.started_at = now
        if status in {"completed", "failed"}:
            job.completed_at = now

        self.session.add(job)
        self.session.commit()
        self.session.refresh(job)
        return job

    def list_recent(self, limit: int = 100) -> list[WorkerJob]:
        statement = select(WorkerJob).order_by(WorkerJob.enqueued_at.desc()).limit(limit)
        return self.session.exec(statement).all()
