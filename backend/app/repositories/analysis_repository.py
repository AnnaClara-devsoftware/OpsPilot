from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.repositories.base import BaseRepository


class AnalysisRepository(BaseRepository[Analysis]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Analysis)
