from fastapi import APIRouter

router = APIRouter()

@router.get("/status", tags=["root"], summary="Root endpoint", description="Root endpoint of the API service.")
async def root():
    return {
        "status": "online",
        "output": "Welcome to the Mountain API Service! 🏔️",
        "message": (
            "Or perhaps you're looking for the answer to the ultimate question of life, "
            "the universe, and everything? 🌌"
        ),
    }