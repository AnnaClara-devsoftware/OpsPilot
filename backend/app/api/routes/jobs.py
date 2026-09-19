from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.job import Job
from app.models.project import Project
from app.models.analysis import Analysis
from app.models.user import User
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobRead

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[JobRead])
def list_jobs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    stmt = (
        select(Job)
        .join(Analysis, Job.analysis_id == Analysis.id)
        .join(Project, Analysis.project_id == Project.id)
        .where(Project.owner_id == user.id)
        .order_by(Job.created_at.desc())
    )
    return list(db.execute(stmt).scalars().all())


@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    repo = JobRepository(db)
    job = repo.get(job_id)
    if not job or job.analysis.project.owner_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job nao encontrado")
    return job
