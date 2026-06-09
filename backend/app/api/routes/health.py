from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Root endpoint")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the Cortex API"}


@router.get("/health", summary="Health check")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

