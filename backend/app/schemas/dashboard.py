from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_projects: int
    total_analyses: int
    jobs_pending: int
    jobs_processing: int
    jobs_completed: int
    jobs_failed: int
    total_loc_analyzed: int
    recent_analyses: list[dict]
