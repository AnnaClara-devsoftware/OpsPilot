from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    analysis_id: UUID
    job_type: str
    status: str
    progress: int
    attempts: int
    duration_seconds: float | None
    logs: str | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime
