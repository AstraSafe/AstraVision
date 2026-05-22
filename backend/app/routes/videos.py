from pathlib import Path
from shutil import copyfileobj

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.services import video_service


router = APIRouter(prefix="/videos", tags=["videos"])

BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_DIR = BASE_DIR / "input_videos"
OUTPUT_DIR = BASE_DIR / "output_videos"
SAMPLE_FRAMES_DIR = OUTPUT_DIR / "sample_frames"
MAX_UPLOAD_SIZE_MB = 200
BYTES_PER_MB = 1024 * 1024


@router.post("/analyze")
def analyze_video(file: UploadFile = File(...)):
    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_filename = Path(file.filename or "uploaded_video.mp4").name
    received_size_bytes = _get_upload_size_bytes(file)

    if received_size_bytes > MAX_UPLOAD_SIZE_MB * BYTES_PER_MB:
        return _large_upload_error_response(
            filename=safe_filename,
            received_size_bytes=received_size_bytes,
        )

    input_path = INPUT_DIR / safe_filename

    # Save the uploaded video locally so the OpenCV pipeline can read it.
    with input_path.open("wb") as buffer:
        copyfileobj(file.file, buffer)

    result = video_service.analyze_video(str(input_path))
    return result


@router.get("/output/{filename}")
def get_output_video(filename: str):
    safe_filename = Path(filename).name
    output_path = OUTPUT_DIR / safe_filename

    if not output_path.exists() or not output_path.is_file():
        raise HTTPException(status_code=404, detail="Output video not found.")

    return FileResponse(
        path=output_path,
        media_type="video/mp4",
        filename=safe_filename,
    )


@router.get("/sample-frames/{analysis_id}/{filename}")
def get_sample_frame(analysis_id: str, filename: str):
    safe_analysis_id = Path(analysis_id).name
    safe_filename = Path(filename).name
    sample_frame_path = SAMPLE_FRAMES_DIR / safe_analysis_id / safe_filename

    if not sample_frame_path.exists() or not sample_frame_path.is_file():
        raise HTTPException(status_code=404, detail="Sample frame not found.")

    return FileResponse(
        path=sample_frame_path,
        media_type="image/jpeg",
        filename=safe_filename,
    )


def _get_upload_size_bytes(file: UploadFile) -> int:
    current_position = file.file.tell()
    file.file.seek(0, 2)
    size_bytes = file.file.tell()
    file.file.seek(current_position)
    return size_bytes


def _large_upload_error_response(filename: str, received_size_bytes: int) -> dict:
    # Large videos should be processed later with background jobs, queues, or an
    # offline workflow. For the hackathon prototype, keep requests short enough
    # for safe synchronous processing.
    return {
        "analysis_id": None,
        "status": "error",
        "message": "Uploaded video is too large for synchronous processing. Please use a shorter demo video.",
        "input": {
            "filename": filename,
            "saved_path": None,
        },
        "output": {
            "filename": None,
            "video_url": None,
            "ready": False,
        },
        "metadata": {
            "max_upload_size_mb": MAX_UPLOAD_SIZE_MB,
            "received_size_mb": _bytes_to_readable_mb(received_size_bytes),
            "recommendation": "Use a short video clip for the current prototype.",
        },
    }


def _bytes_to_readable_mb(size_bytes: int) -> int | float:
    size_mb = round(size_bytes / BYTES_PER_MB, 2)
    if size_mb.is_integer():
        return int(size_mb)
    return size_mb
