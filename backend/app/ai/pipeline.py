from pathlib import Path

import cv2

from app.ai.overlays import draw_tracked_objects
from app.ai.tracking import get_prototype_tracked_objects


def process_video(input_path: str, output_path: str) -> dict:
    """Read a video with OpenCV, add simple overlays, and write an output file."""
    capture = cv2.VideoCapture(input_path)
    if not capture.isOpened():
        raise ValueError("OpenCV could not open the uploaded video.")

    # TODO: Send selected frames to the SAM 3 integration for segmentation.
    # TODO: Replace prototype tracking with model-backed robot and ball tracking.

    fps = capture.get(cv2.CAP_PROP_FPS)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    if width <= 0 or height <= 0:
        capture.release()
        raise ValueError("OpenCV could not read the video width or height.")

    if fps <= 0:
        fps = 30.0

    duration_seconds = None
    if frame_count > 0 and fps > 0:
        duration_seconds = frame_count / fps

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_file), fourcc, fps, (width, height))
    if not writer.isOpened():
        capture.release()
        raise ValueError("OpenCV could not create the processed output video.")

    frames_processed = 0
    trails = {}
    max_trail_points = 30

    while True:
        has_frame, frame = capture.read()
        if not has_frame:
            break

        frames_processed += 1
        tracked_objects = get_prototype_tracked_objects(frames_processed, width, height)

        for tracked_object in tracked_objects:
            object_id = tracked_object["id"]
            trails.setdefault(object_id, []).append(tracked_object["centroid"])
            trails[object_id] = trails[object_id][-max_trail_points:]

        draw_tracked_objects(frame, tracked_objects, trails)
        writer.write(frame)

    capture.release()
    writer.release()

    return {
        "pipeline_status": "opencv_processed",
        "opencv_enabled": True,
        "sam_3_enabled": False,
        "tracking_enabled": True,
        "overlays_enabled": True,
        "frame_count": frame_count,
        "duration_seconds": duration_seconds,
        "fps": fps,
        "width": width,
        "height": height,
        "frames_processed": frames_processed,
        "detected_objects": {
            "robots": 2,
            "ball": 1,
        },
        "prototype_tracking": True,
    }
