class SamClient:
    """Safe boundary for future SAM 3 segmentation.

    SAM 3 is not imported here yet. This keeps the backend runnable on machines
    that only have the current OpenCV prototype dependencies installed.
    """

    def __init__(self):
        # Later this is where model loading, device selection, and any SAM 3
        # configuration should be initialized.
        self._available = False

    def is_available(self) -> bool:
        return self._available

    def segment_frame(self, frame, prompts=None) -> dict:
        # Later this method will run real SAM 3 inference for a selected frame.
        # For now it returns a stable empty result so the pipeline can keep
        # falling back to heuristic detection and prototype demo objects.
        return {
            "masks": [],
            "message": "SAM 3 is not available yet. Skipping segmentation.",
        }
