from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.celery_app import celery_app
from app.models.analysis import Analysis
from app.models.job import Job
from app.models.user import User
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.analysis import AnalysisCreate, AnalysisRead
from app.workers.analysis_worker import run_analysis_pipeline

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisRead, status_code=status.HTTP_201_CREATED)
def create_analysis(payload: AnalysisCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project_repo = ProjectRepository(db)
    project = project_repo.get(payload.project_id)
    if not project or project.owner_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Projeto nao encontrado")

    analysis_repo = AnalysisRepository(db)
    analysis = analysis_repo.create(Analysis(project_id=project.id, status="pending"))

    job = Job(analysis_id=analysis.id, job_type="full_pipeline", status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)

    is_zip = project.source_type == "zip"
    async_result = run_analysis_pipeline.delay(
        str(job.id), str(analysis.id), project.source_reference, is_zip
    )
    job.celery_task_id = async_result.id
    db.commit()

    return analysis


@router.get("", response_model=list[AnalysisRead])
def list_analyses(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project_ids = [p.id for p in ProjectRepository(db).list(owner_id=user.id)]
    if not project_ids:
        return []
    from sqlalchemy import select

    stmt = select(Analysis).where(Analysis.project_id.in_(project_ids)).order_by(Analysis.created_at.desc())
    return list(db.execute(stmt).scalars().all())


@router.get("/{analysis_id}", response_model=AnalysisRead)
def get_analysis(analysis_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    repo = AnalysisRepository(db)
    analysis = repo.get(analysis_id)
    if not analysis or analysis.project.owner_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Analise nao encontrada")
    return analysis
