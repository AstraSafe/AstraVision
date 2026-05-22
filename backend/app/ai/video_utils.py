from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "output_videos"
SAMPLE_FRAMES_DIR = OUTPUT_DIR / "sample_frames"


def generate_output_path(input_path: str, analysis_id: str) -> str:
    """Create a unique output path using the input name and analysis ID."""
    input_file = Path(input_path)
    safe_stem = input_file.stem.replace(" ", "_")
    output_name = f"{safe_stem}_{analysis_id}_analyzed.mp4"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return str(OUTPUT_DIR / output_name)


def create_sample_frames_dir(analysis_id: str) -> Path:
    """Create a folder for the selected sample frames of one analysis."""
    safe_analysis_id = Path(analysis_id).name
    sample_dir = SAMPLE_FRAMES_DIR / safe_analysis_id
    sample_dir.mkdir(parents=True, exist_ok=True)
    return sample_dir


def generate_sample_frame_filename(frame_index: int, sample_number: int) -> str:
    """Create a predictable filename for one saved sample frame."""
    return f"sample_{sample_number:02d}_frame_{frame_index:06d}.jpg"


def sample_frames_relative_dir(analysis_id: str) -> str:
    safe_analysis_id = Path(analysis_id).name
    return f"output_videos/sample_frames/{safe_analysis_id}"
