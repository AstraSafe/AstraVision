class SamClient:
    """Future connection point for SAM 3 segmentation."""

    def __init__(self):
        # This is only a placeholder. Do not import SAM 3 here yet.
        self.enabled = False

    def segment_frame(self, frame):
        # TODO: Load SAM 3 later and return segmentation masks for one frame.
        return []
