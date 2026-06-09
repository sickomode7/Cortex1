from fastapi import APIRouter

from app.api.routes import (
    assessment,
    curriculum,
    dashboard,
    health,
    lessons,
    onboarding,
    quizzes,
    tutor,
    users,
    admin,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(users.router)
api_router.include_router(onboarding.router)
api_router.include_router(assessment.router)
api_router.include_router(curriculum.router)
api_router.include_router(lessons.router)
api_router.include_router(quizzes.router)
api_router.include_router(tutor.router)
api_router.include_router(dashboard.router)
api_router.include_router(admin.router)
