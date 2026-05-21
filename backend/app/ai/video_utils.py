from pathlib import Path
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "output_videos"


def generate_output_path(input_path: str) -> str:
    """Create a safe output path without overwriting previous results."""
    input_file = Path(input_path)
    safe_stem = input_file.stem.replace(" ", "_")
    suffix = input_file.suffix or ".mp4"
    output_name = f"{safe_stem}_analyzed_{uuid4().hex[:8]}{suffix}"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return str(OUTPUT_DIR / output_name)
