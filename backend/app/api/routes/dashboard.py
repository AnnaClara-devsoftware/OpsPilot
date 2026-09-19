from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.analysis import Analysis
from app.models.job import Job
from app.models.project import Project
from app.models.metric import Metric
from app.models.user import User
from app.schemas.dashboard import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project_ids_stmt = select(Project.id).where(Project.owner_id == user.id)
    project_ids = [row[0] for row in db.execute(project_ids_stmt).all()]

    if not project_ids:
        return DashboardStats(
            total_projects=0, total_analyses=0, jobs_pending=0, jobs_processing=0,
            jobs_completed=0, jobs_failed=0, total_loc_analyzed=0, recent_analyses=[],
        )

    analysis_ids_stmt = select(Analysis.id).where(Analysis.project_id.in_(project_ids))
    analysis_ids = [row[0] for row in db.execute(analysis_ids_stmt).all()]

    def count_jobs(status: str) -> int:
        if not analysis_ids:
            return 0
        stmt = select(func.count(Job.id)).where(Job.analysis_id.in_(analysis_ids), Job.status == status)
        return db.execute(stmt).scalar_one()

    total_loc = 0
    if analysis_ids:
        loc_stmt = select(func.coalesce(func.sum(Metric.value), 0)).where(
            Metric.analysis_id.in_(analysis_ids), Metric.name == "total_loc"
        )
        total_loc = int(db.execute(loc_stmt).scalar_one())

    recent_stmt = (
        select(Analysis)
        .where(Analysis.project_id.in_(project_ids))
        .order_by(Analysis.created_at.desc())
        .limit(5)
    )
    recent = db.execute(recent_stmt).scalars().all()

    return DashboardStats(
        total_projects=len(project_ids),
        total_analyses=len(analysis_ids),
        jobs_pending=count_jobs("pending"),
        jobs_processing=count_jobs("processing"),
        jobs_completed=count_jobs("completed"),
        jobs_failed=count_jobs("failed"),
        total_loc_analyzed=total_loc,
        recent_analyses=[
            {"id": str(a.id), "status": a.status, "created_at": a.created_at.isoformat()}
            for a in recent
        ],
    )
