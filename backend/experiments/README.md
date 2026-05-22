# AstraVision Experiments

This folder is for safe backend experiments only. Scripts here should not change
the FastAPI app, the main OpenCV video pipeline, or the stable API response.

## SAM 3 Single-Frame Test

The first goal is to test SAM 3 on one saved sample frame from:

```text
output_videos/sample_frames/{analysis_id}/
```

Run the experiment from the `backend/` directory:

```bash
python experiments/sam3_single_frame_test.py output_videos/sample_frames/{analysis_id}/sample_01_frame_000030.jpg
```

For now, the script only loads the image, prints width, height, channels, and
file path, then safely checks whether SAM 3 can be imported. If SAM 3 is not
installed, it prints a clear message and exits without crashing.

Once SAM 3 works here on a single frame, move the proven loading and inference
logic into `app/ai/sam_client.py`. Keep full-video SAM 3 processing out of the
main pipeline until single-frame behavior is stable.
