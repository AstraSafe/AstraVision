import cv2
import numpy as np


MAX_HEURISTIC_OBJECTS = 3


def get_prototype_tracked_objects(frame_index: int, width: int, height: int) -> list[dict]:
    """Return deterministic demo objects for the current frame.

    This is not real AI tracking. It gives the hackathon demo stable moving
    boxes for two robots and one ball until SAM 3 and real tracking are added.
    """
    robot_width = max(36, width // 10)
    robot_height = max(28, height // 8)
    ball_size = max(18, min(width, height) // 18)

    robot_1_x = _moving_position(frame_index, start=width // 8, speed=3, limit=width - robot_width)
    robot_1_y = _moving_position(frame_index, start=height // 4, speed=1, limit=height - robot_height)

    robot_2_x = _moving_position(frame_index, start=width // 2, speed=2, limit=width - robot_width)
    robot_2_y = _moving_position(frame_index, start=height // 2, speed=-1, limit=height - robot_height)

    ball_x = _moving_position(frame_index, start=width // 3, speed=5, limit=width - ball_size)
    ball_y = _moving_position(frame_index, start=height // 3, speed=2, limit=height - ball_size)

    return [
        _make_object("robot_1", "robot_1", "robot", robot_1_x, robot_1_y, robot_width, robot_height, 0.5, "prototype"),
        _make_object("robot_2", "robot_2", "robot", robot_2_x, robot_2_y, robot_width, robot_height, 0.5, "prototype"),
        _make_object("ball", "ball", "ball", ball_x, ball_y, ball_size, ball_size, 0.5, "prototype"),
    ]


def get_heuristic_tracked_objects(frame, frame_index: int, width: int, height: int) -> list[dict]:
    """Detect simple bright or colorful regions with OpenCV.

    This is an experiment, not real AI. It looks for high-saturation or bright
    regions in HSV color space, converts useful contours into tracked objects,
    and falls back to prototype tracking when the frame has no stable candidates.
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    saturated_mask = cv2.inRange(
        hsv_frame,
        np.array([0, 70, 90]),
        np.array([179, 255, 255]),
    )
    bright_mask = cv2.inRange(
        hsv_frame,
        np.array([0, 0, 210]),
        np.array([179, 80, 255]),
    )
    mask = cv2.bitwise_or(saturated_mask, bright_mask)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = _contours_to_candidates(contours, width, height)

    if not candidates:
        return get_prototype_tracked_objects(frame_index, width, height)

    return _make_heuristic_objects(candidates[:MAX_HEURISTIC_OBJECTS])


def _make_object(
    object_id: str,
    label: str,
    object_type: str,
    x: int,
    y: int,
    width: int,
    height: int,
    confidence: float,
    source: str,
) -> dict:
    return {
        "id": object_id,
        "label": label,
        "type": object_type,
        "bbox": [x, y, width, height],
        "centroid": [x + width // 2, y + height // 2],
        "confidence": confidence,
        "source": source,
    }


def _moving_position(frame_index: int, start: int, speed: int, limit: int) -> int:
    if limit <= 0:
        return 0

    raw_position = start + frame_index * speed
    return raw_position % limit


def _contours_to_candidates(contours, frame_width: int, frame_height: int) -> list[dict]:
    frame_area = frame_width * frame_height
    min_area = max(80, frame_area * 0.0008)
    max_area = frame_area * 0.25
    candidates = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area or area > max_area:
            continue

        x, y, box_width, box_height = cv2.boundingRect(contour)
        if box_width <= 4 or box_height <= 4:
            continue

        confidence = min(0.95, max(0.25, area / (frame_area * 0.03)))
        candidates.append(
            {
                "x": x,
                "y": y,
                "width": box_width,
                "height": box_height,
                "area": area,
                "confidence": round(confidence, 2),
            }
        )

    candidates.sort(key=lambda candidate: candidate["area"], reverse=True)
    return candidates


def _make_heuristic_objects(candidates: list[dict]) -> list[dict]:
    object_slots = [
        ("robot_1", "robot_1", "robot"),
        ("robot_2", "robot_2", "robot"),
        ("ball", "ball", "ball"),
    ]
    tracked_objects = []

    for index, candidate in enumerate(candidates):
        object_id, label, object_type = object_slots[index]
        tracked_objects.append(
            _make_object(
                object_id,
                label,
                object_type,
                candidate["x"],
                candidate["y"],
                candidate["width"],
                candidate["height"],
                candidate["confidence"],
                "heuristic",
            )
        )

    return tracked_objects
