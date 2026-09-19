from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnalysisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    status: str
    summary: dict | None
    created_at: datetime
    updated_at: datetime


class AnalysisCreate(BaseModel):
    project_id: UUID
