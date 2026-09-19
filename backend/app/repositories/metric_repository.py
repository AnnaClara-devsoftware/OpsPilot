from sqlalchemy.orm import Session

from app.models.metric import Metric
from app.repositories.base import BaseRepository


class MetricRepository(BaseRepository[Metric]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Metric)
