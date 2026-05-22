from pathlib import Path

import cv2

from app.ai.overlays import draw_tracked_objects
from app.ai.sam_client import SamClient
from app.ai.tracking import (
    USE_COURT_ROI,
    get_court_roi_metadata,
    get_heuristic_detection_result,
    get_prototype_tracked_objects,
)


# Attempts real frame-derived candidates using simple OpenCV HSV and contour
# heuristics. This is experimental and not final robot or ball detection.
USE_HEURISTIC_DETECTION = True

# Draws fake deterministic objects only when heuristics find nothing. Keep this
# on for demo stability; turn it off to evaluate real detection honestly.
USE_PROTOTYPE_FALLBACK = True

# Draws the Court ROI rectangle on output frames so tuning is visible.
DRAW_COURT_ROI = True

# SAM 3 will later run on selected frames only. It stays disabled by default so
# the backend does not require SAM 3 dependencies today.
USE_SAM3 = False
SAM3_FRAME_INTERVAL = 30

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
    prototype_fallback_used = False
    sam_client = SamClient()
    sam_3_available = sam_client.is_available()
    sam_3_frames_attempted = 0
    sam_3_detections = 0
    debug_frames_dir = output_file.parent / "debug_frames"

    if EXPORT_DEBUG_FRAMES:
        debug_frames_dir.mkdir(parents=True, exist_ok=True)

    while True:
        has_frame, frame = capture.read()
        if not has_frame:
            break

        frames_processed += 1
        sam_masks = []
        if _should_attempt_sam3(frames_processed, sam_3_available):
            sam_3_frames_attempted += 1
            sam_result = sam_client.segment_frame(frame)
            sam_masks = sam_result["masks"]
            sam_3_detections += len(sam_masks)

        if sam_masks:
            # TODO: Convert real SAM 3 masks into tracked objects.
            tracked_objects = []
        elif USE_HEURISTIC_DETECTION:
            detection_result = get_heuristic_detection_result(frame, frames_processed, width, height)
            tracked_objects = detection_result["objects"]
            detections_filtered_by_roi += detection_result["filtered_by_roi"]
        else:
            tracked_objects = []

        if not tracked_objects and USE_PROTOTYPE_FALLBACK:
            tracked_objects = get_prototype_tracked_objects(frames_processed, width, height)
            prototype_fallback_used = True

        heuristic_detection_count = _count_heuristic_detections(tracked_objects)

        if heuristic_detection_count > 0:
            heuristic_frames += 1
        elif _uses_prototype_fallback(tracked_objects):
            prototype_fallback_frames += 1

        total_heuristic_detections += heuristic_detection_count
        max_detections_in_frame = max(max_detections_in_frame, heuristic_detection_count)

        for tracked_object in tracked_objects:
            object_id = tracked_object["id"]
            trails.setdefault(object_id, []).append(tracked_object["centroid"])
            trails[object_id] = trails[object_id][-max_trail_points:]

        draw_tracked_objects(
            frame,
            tracked_objects,
            trails,
            draw_court_roi_enabled=DRAW_COURT_ROI and USE_COURT_ROI,
        )

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
        "sam_3_enabled": USE_SAM3,
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
        "prototype_tracking": USE_PROTOTYPE_FALLBACK,
        "heuristic_detection_enabled": USE_HEURISTIC_DETECTION,
        "prototype_fallback_enabled": USE_PROTOTYPE_FALLBACK,
        "detection_source_summary": {
            "heuristic_frames": heuristic_frames,
            "prototype_fallback_frames": prototype_fallback_frames,
        },
        "prototype_fallback_used": prototype_fallback_used,
        "prototype_fallback_frames": prototype_fallback_frames,
        "heuristic_frames": heuristic_frames,
        "detection_mode": _detection_mode(),
        "warning": _fallback_warning(prototype_fallback_used),
        "total_heuristic_detections": total_heuristic_detections,
        "average_detections_per_frame": _average_detections(
            total_heuristic_detections,
            frames_processed,
        ),
        "max_detections_in_frame": max_detections_in_frame,
        "court_roi_enabled": USE_COURT_ROI,
        "court_roi": get_court_roi_metadata(),
        "detections_filtered_by_roi": detections_filtered_by_roi,
        "sam_3_available": sam_3_available,
        "sam_3_frame_interval": SAM3_FRAME_INTERVAL,
        "sam_3_frames_attempted": sam_3_frames_attempted,
        "sam_3_detections": sam_3_detections,
        "detection_priority": "sam3_then_heuristic_then_prototype",
    }


def _count_heuristic_detections(tracked_objects: list[dict]) -> int:
    return sum(1 for tracked_object in tracked_objects if tracked_object.get("source") == "heuristic")


def _uses_prototype_fallback(tracked_objects: list[dict]) -> bool:
    return any(tracked_object.get("source") == "prototype" for tracked_object in tracked_objects)


def _should_attempt_sam3(frame_index: int, sam_3_available: bool) -> bool:
    return USE_SAM3 and sam_3_available and frame_index % SAM3_FRAME_INTERVAL == 0


def _average_detections(total_detections: int, frames_processed: int) -> float:
    if frames_processed == 0:
        return 0.0

    return round(total_detections / frames_processed, 2)


def _detection_mode() -> str:
    if USE_HEURISTIC_DETECTION and USE_PROTOTYPE_FALLBACK:
        return "heuristic_with_prototype_fallback"
    if USE_HEURISTIC_DETECTION:
        return "heuristic_only"
    if USE_PROTOTYPE_FALLBACK:
        return "prototype_fallback_only"
    return "no_detection"


def _fallback_warning(prototype_fallback_used: bool) -> str | None:
    if not prototype_fallback_used:
        return None

    return "Prototype fallback is demo-only and does not represent real detection."
