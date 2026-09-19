import uuid
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.types import GUID
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Report(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "reports"

    format: Mapped[str] = mapped_column(String(10), nullable=False)  # html | json | csv
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    content_preview: Mapped[str | None] = mapped_column(Text, nullable=True)

    analysis_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("analyses.id", ondelete="CASCADE"))
    analysis: Mapped["Analysis"] = relationship(back_populates="reports")
