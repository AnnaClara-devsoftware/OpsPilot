"""Handles secure ZIP uploads for a project's source code."""
import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.repositories.project_repository import ProjectRepository

router = APIRouter(prefix="/uploads", tags=["uploads"])
settings = get_settings()

ALLOWED_CONTENT_TYPES = {"application/zip", "application/x-zip-compressed", "application/octet-stream"}


@router.post("/{project_id}/zip")
async def upload_project_zip(
    project_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    repo = ProjectRepository(db)
    project = repo.get(project_id)
    if not project or project.owner_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Projeto nao encontrado")

    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Apenas arquivos .zip sao aceitos")

    os.makedirs(settings.upload_dir, exist_ok=True)
    dest_filename = f"{project_id}_{uuid.uuid4().hex}.zip"
    dest_path = os.path.join(settings.upload_dir, dest_filename)

    size = 0
    with open(dest_path, "wb") as out:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > settings.max_upload_size_bytes:
                out.close()
                os.remove(dest_path)
                raise HTTPException(
                    status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    f"Arquivo excede o limite de {settings.max_upload_size_mb}MB",
                )
            out.write(chunk)

    project.source_type = "zip"
    project.source_reference = dest_path
    repo.update(project)

    return {"message": "Upload concluido", "file_path": dest_path, "size_bytes": size}
