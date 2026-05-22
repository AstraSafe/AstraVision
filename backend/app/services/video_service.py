from pathlib import Path
from uuid import uuid4

from app.ai.pipeline import process_video
from app.ai.video_utils import generate_output_path


def analyze_video(input_path: str) -> dict:
    analysis_id = str(uuid4())
    output_path = generate_output_path(input_path)
    metadata = process_video(input_path=input_path, output_path=output_path)
    input_file = Path(input_path)
    output_file = Path(output_path)

    # This response is intentionally stable for the frontend while the real
    # OpenCV and SAM 3 pipeline is still a future implementation.
    return {
        "analysis_id": analysis_id,
        "status": "success",
        "message": "Video analysis finished using the placeholder AI pipeline.",
        "input": {
            "filename": input_file.name,
            "saved_path": f"input_videos/{input_file.name}",
        },
        "output": {
            "filename": output_file.name,
            "video_url": f"/videos/output/{output_file.name}",
            "ready": False,
        },
        "metadata": metadata,
    }
