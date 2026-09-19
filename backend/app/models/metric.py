import uuid
from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.types import GUID
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Metric(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "metrics"

    name: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. total_loc, file_count, todo_count
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str | None] = mapped_column(String(30), nullable=True)

    analysis_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("analyses.id", ondelete="CASCADE"))
    analysis: Mapped["Analysis"] = relationship(back_populates="metrics")
