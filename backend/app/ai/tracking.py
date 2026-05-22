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
        _make_object("robot_1", "Robot 1", "robot", robot_1_x, robot_1_y, robot_width, robot_height),
        _make_object("robot_2", "Robot 2", "robot", robot_2_x, robot_2_y, robot_width, robot_height),
        _make_object("ball", "Ball", "ball", ball_x, ball_y, ball_size, ball_size),
    ]


def _make_object(
    object_id: str,
    label: str,
    object_type: str,
    x: int,
    y: int,
    width: int,
    height: int,
) -> dict:
    return {
        "id": object_id,
        "label": label,
        "type": object_type,
        "bbox": [x, y, width, height],
        "centroid": [x + width // 2, y + height // 2],
    }


def _moving_position(frame_index: int, start: int, speed: int, limit: int) -> int:
    if limit <= 0:
        return 0

    raw_position = start + frame_index * speed
    return raw_position % limit
