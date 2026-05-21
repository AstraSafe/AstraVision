from pathlib import Path
from shutil import copyfileobj

from fastapi import APIRouter, File, UploadFile

from app.services import video_service


router = APIRouter(prefix="/videos", tags=["videos"])

BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_DIR = BASE_DIR / "input_videos"


@router.post("/analyze")
def analyze_video(file: UploadFile = File(...)):
    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_filename = Path(file.filename or "uploaded_video.mp4").name
    input_path = INPUT_DIR / safe_filename

    # Save the uploaded video locally so the AI pipeline can read it later.
    with input_path.open("wb") as buffer:
        copyfileobj(file.file, buffer)

    result = video_service.analyze_video(str(input_path))
    return result
