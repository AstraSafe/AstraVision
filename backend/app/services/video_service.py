from pathlib import Path
from uuid import uuid4

from app.ai.pipeline import process_video
from app.ai.video_utils import generate_output_path


def analyze_video(input_path: str) -> dict:
    analysis_id = str(uuid4())
    output_path = generate_output_path(input_path, analysis_id)
    input_file = Path(input_path)
    output_file = Path(output_path)

    try:
        metadata = process_video(
            input_path=input_path,
            output_path=output_path,
            analysis_id=analysis_id,
        )
        status = "success"
        message = "Video analysis finished using the OpenCV prototype pipeline."
        output_ready = True
    except ValueError as error:
        # Keep the response readable for the frontend instead of crashing the API.
        metadata = _empty_error_metadata(str(error))
        status = "error"
        message = str(error)
        output_ready = False

    # The response shape stays stable as the AI pipeline becomes more capable.
    return {
        "analysis_id": analysis_id,
        "status": status,
        "message": message,
        "input": {
            "filename": input_file.name,
            "saved_path": f"input_videos/{input_file.name}",
        },
        "output": {
            "filename": output_file.name,
            "video_url": f"/videos/output/{output_file.name}",
            "ready": output_ready,
        },
        "metadata": metadata,
    }


def _empty_error_metadata(error_message: str) -> dict:
    return {
        "pipeline_status": "error",
        "opencv_enabled": True,
        "sam_3_enabled": False,
        "tracking_enabled": False,
        "overlays_enabled": False,
        "frame_count": None,
        "duration_seconds": None,
        "fps": None,
        "width": None,
        "height": None,
        "frames_processed": 0,
        "error": error_message,
    }
