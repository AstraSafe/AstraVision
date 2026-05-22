from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "output_videos"


def generate_output_path(input_path: str, analysis_id: str) -> str:
    """Create a unique output path using the input name and analysis ID."""
    input_file = Path(input_path)
    safe_stem = input_file.stem.replace(" ", "_")
    output_name = f"{safe_stem}_{analysis_id}_analyzed.mp4"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return str(OUTPUT_DIR / output_name)
