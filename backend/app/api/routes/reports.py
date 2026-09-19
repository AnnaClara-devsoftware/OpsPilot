from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.analysis import Analysis
from app.models.project import Project
from app.models.report import Report
from app.models.user import User
from app.repositories.report_repository import ReportRepository
from app.schemas.report import ReportRead

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=list[ReportRead])
def list_reports(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    stmt = (
        select(Report)
        .join(Analysis, Report.analysis_id == Analysis.id)
        .join(Project, Analysis.project_id == Project.id)
        .where(Project.owner_id == user.id)
        .order_by(Report.created_at.desc())
    )
    return list(db.execute(stmt).scalars().all())


@router.get("/{report_id}/download")
def download_report(report_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    repo = ReportRepository(db)
    report = repo.get(report_id)
    if not report or report.analysis.project.owner_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Relatorio nao encontrado")

    media_types = {"html": "text/html", "json": "application/json", "csv": "text/csv"}
    return FileResponse(
        report.file_path,
        media_type=media_types.get(report.format, "application/octet-stream"),
        filename=f"report_{report.id}.{report.format}",
    )
