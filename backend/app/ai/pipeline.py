from pathlib import Path

import cv2


def process_video(input_path: str, output_path: str) -> dict:
    """Read a video with OpenCV, add simple overlays, and write an output file."""
    capture = cv2.VideoCapture(input_path)
    if not capture.isOpened():
        raise ValueError("OpenCV could not open the uploaded video.")

    # TODO: Send selected frames to the SAM 3 integration for segmentation.
    # TODO: Track FutBotMX robots and the ball across frames.
    # TODO: Draw model masks, boxes, labels, and movement paths on output frames.

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

    while True:
        has_frame, frame = capture.read()
        if not has_frame:
            break

        frames_processed += 1

        # Simple prototype overlay. SAM 3 and tracking are intentionally not
        # enabled in this milestone.
        cv2.putText(
            frame,
            "AstraVision",
            (24, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            f"Frame {frames_processed}",
            (24, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            "Prototype analysis",
            (24, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

        writer.write(frame)

    capture.release()
    writer.release()

    return {
        "pipeline_status": "opencv_processed",
        "opencv_enabled": True,
        "sam_3_enabled": False,
        "tracking_enabled": False,
        "overlays_enabled": True,
        "frame_count": frame_count,
        "duration_seconds": duration_seconds,
        "fps": fps,
        "width": width,
        "height": height,
        "frames_processed": frames_processed,
    }
