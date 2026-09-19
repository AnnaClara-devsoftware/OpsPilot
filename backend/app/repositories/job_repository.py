from sqlalchemy.orm import Session

from app.models.job import Job
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository[Job]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Job)
