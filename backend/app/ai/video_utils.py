from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "output_videos"


def generate_output_path(input_path: str) -> str:
    """Create the planned placeholder output path for a processed video."""
    input_file = Path(input_path)
    safe_stem = input_file.stem.replace(" ", "_")
    suffix = input_file.suffix or ".mp4"
    output_name = f"{safe_stem}_analyzed{suffix}"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return str(OUTPUT_DIR / output_name)
