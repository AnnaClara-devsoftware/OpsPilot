import uuid
from sqlalchemy import ForeignKey, String
from app.core.types import JSONEncoded
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.types import GUID
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Analysis(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "analyses"

    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    summary: Mapped[dict | None] = mapped_column(JSONEncoded, nullable=True)

    project_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("projects.id", ondelete="CASCADE"))
    project: Mapped["Project"] = relationship(back_populates="analyses")

    jobs: Mapped[list["Job"]] = relationship(back_populates="analysis", cascade="all, delete-orphan")
    reports: Mapped[list["Report"]] = relationship(back_populates="analysis", cascade="all, delete-orphan")
    metrics: Mapped[list["Metric"]] = relationship(back_populates="analysis", cascade="all, delete-orphan")
