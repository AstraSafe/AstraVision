from app.ai.pipeline import process_video
from app.ai.video_utils import generate_output_path


def analyze_video(input_path: str) -> dict:
    output_path = generate_output_path(input_path)
    metadata = process_video(input_path=input_path, output_path=output_path)

    return {
        "status": "success",
        "input_path": input_path,
        "output_path": output_path,
        "message": "Video analysis finished using the placeholder AI pipeline.",
        "metadata": metadata,
    }
