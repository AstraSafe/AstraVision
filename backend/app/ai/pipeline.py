from pathlib import Path


def process_video(input_path: str, output_path: str) -> dict:
    """Placeholder video pipeline for the first backend version."""
    input_file = Path(input_path)

    # TODO: Open the video with OpenCV and read frames.
    # TODO: Send selected frames to the SAM 3 integration for segmentation.
    # TODO: Track FutBotMX robots and the ball across frames.
    # TODO: Draw masks, boxes, labels, and movement paths on output frames.
    # TODO: Write the processed frames into output_path as a new video file.

    return {
        "pipeline_status": "simulated",
        "sam_3_enabled": False,
        "opencv_enabled": False,
        "tracking_enabled": False,
        "overlays_enabled": False,
        "input_filename": input_file.name,
        "planned_output_path": output_path,
    }
