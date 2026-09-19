from fastapi import APIRouter

from app.api.routes import analyses, auth, dashboard, jobs, projects, reports, uploads

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(uploads.router)
api_router.include_router(analyses.router)
api_router.include_router(jobs.router)
api_router.include_router(reports.router)
api_router.include_router(dashboard.router)
