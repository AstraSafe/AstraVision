import cv2
import numpy as np


# Saturated HSV range: finds colorful regions such as bright jerseys, markers,
# or objects with strong color contrast.
SATURATED_HSV_LOWER = np.array([0, 70, 90])
SATURATED_HSV_UPPER = np.array([179, 255, 255])

# Bright HSV range: finds light/white regions that may not be saturated.
BRIGHT_HSV_LOWER = np.array([0, 0, 210])
BRIGHT_HSV_UPPER = np.array([179, 80, 255])

# Minimum contour area: increase this to ignore more tiny noise.
MIN_CONTOUR_AREA = 80

# Maximum contour area ratio: lower this if the background is being detected as
# one huge object.
MAX_CONTOUR_AREA_RATIO = 0.25

# Maximum detections per frame: keeps the demo readable and stable.
MAX_DETECTIONS_PER_FRAME = 3

# Minimum box size: increase these if tiny boxes clutter the output video.
MIN_BBOX_WIDTH = 5
MIN_BBOX_HEIGHT = 5

# Court ROI ratios define the playing field area as percentages of the frame.
# Use values from 0.0 to 1.0 so the same settings work on different video sizes.
# Increase the min ratios to crop more from the left/top. Decrease the max
# ratios to crop more from the right/bottom.
USE_COURT_ROI = True
COURT_ROI_X_MIN_RATIO = 0.08
COURT_ROI_Y_MIN_RATIO = 0.20
COURT_ROI_X_MAX_RATIO = 0.92
COURT_ROI_Y_MAX_RATIO = 0.88


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
    """Return only the detected objects for callers that do not need debug info."""
    return get_heuristic_detection_result(frame, frame_index, width, height)["objects"]


def get_heuristic_detection_result(frame, frame_index: int, width: int, height: int) -> dict:
    """Detect simple bright or colorful regions with OpenCV.

    This is an experiment, not real AI. It looks for high-saturation or bright
    regions in HSV color space, converts useful contours into tracked objects,
    and falls back to prototype tracking when the frame has no stable candidates.
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    saturated_mask = cv2.inRange(
        hsv_frame,
        SATURATED_HSV_LOWER,
        SATURATED_HSV_UPPER,
    )
    bright_mask = cv2.inRange(
        hsv_frame,
        BRIGHT_HSV_LOWER,
        BRIGHT_HSV_UPPER,
    )
    mask = cv2.bitwise_or(saturated_mask, bright_mask)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = _contours_to_candidates(contours, width, height)
    valid_candidates, filtered_by_roi = _filter_candidates_by_court_roi(candidates, width, height)

    if not valid_candidates:
        return {
            "objects": get_prototype_tracked_objects(frame_index, width, height),
            "filtered_by_roi": filtered_by_roi,
            "used_prototype_fallback": True,
        }

    return {
        "objects": _make_heuristic_objects(valid_candidates[:MAX_DETECTIONS_PER_FRAME]),
        "filtered_by_roi": filtered_by_roi,
        "used_prototype_fallback": False,
    }


def get_court_roi_pixels(width: int, height: int) -> tuple[int, int, int, int]:
    x_min = int(width * COURT_ROI_X_MIN_RATIO)
    y_min = int(height * COURT_ROI_Y_MIN_RATIO)
    x_max = int(width * COURT_ROI_X_MAX_RATIO)
    y_max = int(height * COURT_ROI_Y_MAX_RATIO)
    return x_min, y_min, x_max, y_max


def get_court_roi_metadata() -> dict:
    return {
        "x_min_ratio": COURT_ROI_X_MIN_RATIO,
        "y_min_ratio": COURT_ROI_Y_MIN_RATIO,
        "x_max_ratio": COURT_ROI_X_MAX_RATIO,
        "y_max_ratio": COURT_ROI_Y_MAX_RATIO,
    }


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
    max_area = frame_area * MAX_CONTOUR_AREA_RATIO
    candidates = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < MIN_CONTOUR_AREA or area > max_area:
            continue

        x, y, box_width, box_height = cv2.boundingRect(contour)
        if box_width < MIN_BBOX_WIDTH or box_height < MIN_BBOX_HEIGHT:
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


def _filter_candidates_by_court_roi(
    candidates: list[dict],
    frame_width: int,
    frame_height: int,
) -> tuple[list[dict], int]:
    if not USE_COURT_ROI:
        return candidates, 0

    x_min, y_min, x_max, y_max = get_court_roi_pixels(frame_width, frame_height)
    valid_candidates = []
    filtered_by_roi = 0

    for candidate in candidates:
        centroid_x = candidate["x"] + candidate["width"] // 2
        centroid_y = candidate["y"] + candidate["height"] // 2

        if x_min <= centroid_x <= x_max and y_min <= centroid_y <= y_max:
            valid_candidates.append(candidate)
        else:
            filtered_by_roi += 1

    return valid_candidates, filtered_by_roi


def _make_heuristic_objects(candidates: list[dict]) -> list[dict]:
    tracked_objects = []

    for index, candidate in enumerate(candidates):
        object_number = index + 1
        object_id = f"candidate_{object_number}"
        label = f"candidate_{object_number}"
        tracked_objects.append(
            _make_object(
                object_id,
                label,
                "candidate",
                candidate["x"],
                candidate["y"],
                candidate["width"],
                candidate["height"],
                candidate["confidence"],
                "heuristic",
            )
        )

    return tracked_objects
