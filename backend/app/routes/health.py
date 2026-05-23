from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "astravision-backend",
        "version": "0.1.0",
        "message": "AstraVision backend is running",
    }
