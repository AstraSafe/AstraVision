from pathlib import Path

import cv2

from app.ai.overlays import draw_tracked_objects
from app.ai.tracking import (
    USE_COURT_ROI,
    get_court_roi_metadata,
    get_heuristic_detection_result,
    get_prototype_tracked_objects,
)


USE_HEURISTIC_DETECTION = True
EXPORT_DEBUG_FRAMES = False
DEBUG_FRAME_LIMIT = 5


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
    heuristic_frames = 0
    prototype_fallback_frames = 0
    total_heuristic_detections = 0
    max_detections_in_frame = 0
    detections_filtered_by_roi = 0
    debug_frames_dir = output_file.parent / "debug_frames"

    if EXPORT_DEBUG_FRAMES:
        debug_frames_dir.mkdir(parents=True, exist_ok=True)

    while True:
        has_frame, frame = capture.read()
        if not has_frame:
            break

        frames_processed += 1
        if USE_HEURISTIC_DETECTION:
            detection_result = get_heuristic_detection_result(frame, frames_processed, width, height)
            tracked_objects = detection_result["objects"]
            detections_filtered_by_roi += detection_result["filtered_by_roi"]
        else:
            tracked_objects = get_prototype_tracked_objects(frames_processed, width, height)

        heuristic_detection_count = _count_heuristic_detections(tracked_objects)

        if heuristic_detection_count > 0:
            heuristic_frames += 1
        else:
            prototype_fallback_frames += 1

        total_heuristic_detections += heuristic_detection_count
        max_detections_in_frame = max(max_detections_in_frame, heuristic_detection_count)

        for tracked_object in tracked_objects:
            object_id = tracked_object["id"]
            trails.setdefault(object_id, []).append(tracked_object["centroid"])
            trails[object_id] = trails[object_id][-max_trail_points:]

        draw_tracked_objects(frame, tracked_objects, trails)

        # Debug frame export is disabled by default. Turn it on only while
        # tuning HSV thresholds against real FutBotMX clips.
        if EXPORT_DEBUG_FRAMES and frames_processed <= DEBUG_FRAME_LIMIT:
            debug_frame_path = debug_frames_dir / f"frame_{frames_processed:04d}.jpg"
            cv2.imwrite(str(debug_frame_path), frame)

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
        "heuristic_detection_enabled": USE_HEURISTIC_DETECTION,
        "prototype_fallback_enabled": True,
        "detection_source_summary": {
            "heuristic_frames": heuristic_frames,
            "prototype_fallback_frames": prototype_fallback_frames,
        },
        "total_heuristic_detections": total_heuristic_detections,
        "average_detections_per_frame": _average_detections(
            total_heuristic_detections,
            frames_processed,
        ),
        "max_detections_in_frame": max_detections_in_frame,
        "court_roi_enabled": USE_COURT_ROI,
        "court_roi": get_court_roi_metadata(),
        "detections_filtered_by_roi": detections_filtered_by_roi,
    }


def _count_heuristic_detections(tracked_objects: list[dict]) -> int:
    return sum(1 for tracked_object in tracked_objects if tracked_object.get("source") == "heuristic")


def _average_detections(total_detections: int, frames_processed: int) -> float:
    if frames_processed == 0:
        return 0.0

    return round(total_detections / frames_processed, 2)
