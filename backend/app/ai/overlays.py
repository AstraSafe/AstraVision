import cv2

from app.ai.tracking import get_court_roi_pixels


OBJECT_COLORS = {
    "robot": (0, 255, 255),
    "ball": (0, 180, 255),
    "candidate": (255, 120, 0),
}
TRAIL_COLOR = (255, 255, 255)
WATERMARK_COLOR = (0, 255, 0)


def draw_tracked_objects(
    frame,
    tracked_objects: list[dict],
    trails: dict[str, list[list[int]]],
    draw_court_roi_enabled: bool = True,
):
    """Draw demo tracking boxes, labels, centroids, and movement trails."""
    if draw_court_roi_enabled:
        draw_court_roi(frame)
    draw_movement_trails(frame, trails)

    for tracked_object in tracked_objects:
        draw_bounding_box(frame, tracked_object)
        draw_label(frame, tracked_object)
        draw_centroid(frame, tracked_object)

    draw_watermark(frame)
    return frame


def draw_segmentation_masks(frame, masks):
    """Future placeholder for SAM 3 mask overlays.

    Real mask drawing will be added after SAM 3 returns mask data. Keeping this
    no-op function now gives the pipeline a clear extension point.
    """
    return frame


def draw_court_roi(frame):
    frame_height, frame_width = frame.shape[:2]
    x_min, y_min, x_max, y_max = get_court_roi_pixels(frame_width, frame_height)
    color = (255, 255, 0)
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
    cv2.putText(
        frame,
        "Court ROI",
        (x_min, max(18, y_min - 8)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
        cv2.LINE_AA,
    )
    return frame


def draw_bounding_box(frame, tracked_object: dict):
    x, y, width, height = tracked_object["bbox"]
    color = _object_color(tracked_object)
    cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
    return frame


def draw_label(frame, tracked_object: dict):
    x, y, _, _ = tracked_object["bbox"]
    label = _display_label(tracked_object)
    color = _object_color(tracked_object)
    label_position = (x, max(18, y - 8))
    cv2.putText(
        frame,
        label,
        label_position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
        cv2.LINE_AA,
    )
    return frame


def draw_centroid(frame, tracked_object: dict):
    centroid_x, centroid_y = tracked_object["centroid"]
    color = _object_color(tracked_object)
    cv2.circle(frame, (centroid_x, centroid_y), 4, color, -1)
    return frame


def draw_movement_trails(frame, trails: dict[str, list[list[int]]]):
    for points in trails.values():
        if len(points) < 2:
            continue

        for index in range(1, len(points)):
            previous_point = tuple(points[index - 1])
            current_point = tuple(points[index])
            cv2.line(frame, previous_point, current_point, TRAIL_COLOR, 1, cv2.LINE_AA)

    return frame


def draw_watermark(frame):
    cv2.putText(
        frame,
        "AstraVision",
        (24, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        WATERMARK_COLOR,
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "Prototype tracking",
        (24, 78),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    return frame


def _object_color(tracked_object: dict) -> tuple[int, int, int]:
    return OBJECT_COLORS.get(tracked_object["type"], (255, 255, 255))


def _display_label(tracked_object: dict) -> str:
    if tracked_object.get("is_demo"):
        return f"{tracked_object['label']} [prototype demo]"

    return f"{tracked_object['label']} [{tracked_object.get('source', 'unknown')}]"
