from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    source_type: str = Field(default="zip", pattern="^(zip|path)$")
    source_reference: str = Field(min_length=1, max_length=500)


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    source_type: str
    source_reference: str
    created_at: datetime
    updated_at: datetime
