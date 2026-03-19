from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..data.worker_job_repository import WorkerJobRepository
from ..database import get_session

router = APIRouter()


def get_worker_job_repository(
    session: Session = Depends(get_session),
) -> WorkerJobRepository:
    return WorkerJobRepository(session)


@router.get("/")
async def list_jobs(
    limit: int = 100,
    repository: WorkerJobRepository = Depends(get_worker_job_repository),
):
    return repository.list_recent(limit=limit)


@router.get("/{job_id}")
async def get_job(
    job_id: str,
    repository: WorkerJobRepository = Depends(get_worker_job_repository),
):
    job = repository.get_by_job_id(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job
