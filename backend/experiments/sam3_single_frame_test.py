"""Safe single-frame SAM 3 experiment script.

This script does not change the FastAPI app or the main OpenCV pipeline. It is
only for testing whether SAM 3 can be imported and later run on one image.
"""

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Load one image and safely check whether SAM 3 is available."
    )
    parser.add_argument("image_path", help="Path to a saved sample frame image.")
    args = parser.parse_args()

    image_path = Path(args.image_path).expanduser().resolve()
    if not image_path.exists() or not image_path.is_file():
        print(f"Image not found: {image_path}")
        return 1

    image_metadata = load_image_metadata(image_path)
    if image_metadata is None:
        print("Could not load the image with OpenCV or PIL.")
        print(f"File path: {image_path}")
        return 1

    print("Image metadata:")
    print(f"  file_path: {image_path}")
    print(f"  width: {image_metadata['width']}")
    print(f"  height: {image_metadata['height']}")
    print(f"  channels: {image_metadata['channels']}")
    print(f"  loader: {image_metadata['loader']}")

    try:
        import sam3  # noqa: F401
    except ImportError:
        print("")
        print("SAM 3 is not installed or not importable in this environment.")
        print("This is expected until SAM 3 dependencies are installed manually.")
        print("The backend API and OpenCV pipeline are not affected.")
        return 0

    print("")
    print("SAM 3 import succeeded.")
    print("Next step: add a tiny one-frame inference test here before touching SamClient.")
    return 0


def load_image_metadata(image_path: Path) -> dict | None:
    metadata = load_with_opencv(image_path)
    if metadata is not None:
        return metadata

    return load_with_pil(image_path)


def load_with_opencv(image_path: Path) -> dict | None:
    try:
        import cv2
    except ImportError:
        return None

    image = cv2.imread(str(image_path))
    if image is None:
        return None

    height, width = image.shape[:2]
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    return {
        "width": width,
        "height": height,
        "channels": channels,
        "loader": "opencv",
    }


def load_with_pil(image_path: Path) -> dict | None:
    try:
        from PIL import Image
    except ImportError:
        return None

    try:
        with Image.open(image_path) as image:
            width, height = image.size
            channels = len(image.getbands())
    except OSError:
        return None

    return {
        "width": width,
        "height": height,
        "channels": channels,
        "loader": "pil",
    }


if __name__ == "__main__":
    raise SystemExit(main())
