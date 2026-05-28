from pathlib import Path
from shutil import which
import subprocess


VIDEO_CODEC_TARGET = "h264"


def transcode_to_browser_mp4(intermediate_path: str, final_path: str) -> dict:
    """Convert OpenCV output to a browser-friendly MP4 when ffmpeg is available."""
    ffmpeg_path = which("ffmpeg")
    if ffmpeg_path is None:
        return {
            "web_compatible_video": False,
            "video_codec_target": VIDEO_CODEC_TARGET,
            "transcoding_enabled": False,
            "transcoding_warning": "ffmpeg is not installed or not available on PATH. Keeping OpenCV output video.",
        }

    intermediate_file = Path(intermediate_path)
    final_file = Path(final_path)
    transcoded_file = final_file.with_name(f"{final_file.stem}_h264{final_file.suffix}")

    command = [
        ffmpeg_path,
        "-y",
        "-i",
        str(intermediate_file),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-an",
        str(transcoded_file),
    ]

    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        return {
            "web_compatible_video": False,
            "video_codec_target": VIDEO_CODEC_TARGET,
            "transcoding_enabled": True,
            "transcoding_warning": f"ffmpeg transcoding failed. Keeping OpenCV output video. {error}",
        }

    transcoded_file.replace(final_file)
    return {
        "web_compatible_video": True,
        "video_codec_target": VIDEO_CODEC_TARGET,
        "transcoding_enabled": True,
        "transcoding_warning": None,
    }
