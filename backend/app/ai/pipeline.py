def process_video(input_path: str, output_path: str) -> dict:
    """Return placeholder metadata until real video processing is implemented."""

    # TODO: Open the video with OpenCV and read frames.
    # TODO: Send selected frames to the SAM 3 integration for segmentation.
    # TODO: Track FutBotMX robots and the ball across frames.
    # TODO: Draw masks, boxes, labels, and movement paths on output frames.
    # TODO: Write the processed frames into output_path as a new video file.

    # Keep all unimplemented values as false or null so the frontend can render
    # a predictable response without pretending that analysis output is ready.
    return {
        "pipeline_status": "simulated",
        "opencv_enabled": False,
        "sam_3_enabled": False,
        "tracking_enabled": False,
        "overlays_enabled": False,
        "frame_count": None,
        "duration_seconds": None,
        "fps": None,
        "width": None,
        "height": None,
    }
