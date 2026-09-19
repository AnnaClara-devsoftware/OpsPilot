from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    analysis_id: UUID
    format: str
    file_path: str
    created_at: datetime
