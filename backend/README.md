# AstraVision Backend

Minimal FastAPI backend for the AstraVision FutBotMX computer vision project.

## What this backend does

This backend accepts FutBotMX video uploads and sends them through a simple AI pipeline prototype.

The current milestone uses OpenCV to read the uploaded video, copy each frame,
try simple heuristic detection, draw tracking overlays, and export a processed
video into `output_videos/`.

## Current status

OpenCV prototype with experimental heuristic detection and demo tracking
overlays.

The backend now tries beginner-friendly HSV/contour heuristics to detect bright
or colorful regions in each frame. This is experimental and imperfect. If no
useful heuristic regions are found, the backend can fall back to deterministic
prototype objects so the demo output stays stable.

SAM 3, segmentation, real robot tracking, real ball tracking, training,
databases, authentication, Docker, queues, and background jobs are not
implemented yet.

## Install dependencies

When you are ready to run the backend, create or activate a Python environment and install the existing requirements:

```bash
pip install -r requirements.txt
```

## Run the backend

From the `backend/` directory:

```bash
uvicorn app.main:app --reload
```

## Available endpoints

- `GET /health`
- `POST /videos/analyze`
- `GET /videos/output/{filename}`
- `GET /videos/sample-frames/{analysis_id}/{filename}`

## Test video analysis

Use a short demo video for this prototype. A 10-30 second clip is ideal while
the API still processes videos synchronously inside the request.

From another terminal, send a multipart upload using the field name `file`:

```bash
curl -X POST \
  -F "file=@input_videos/example.mp4" \
  http://127.0.0.1:8000/videos/analyze
```

The response includes an output URL when OpenCV finishes processing:

```json
{
  "status": "success",
  "output": {
    "filename": "example_generated-id_analyzed.mp4",
    "video_url": "/videos/output/example_generated-id_analyzed.mp4",
    "ready": true
  }
}
```

The processed output video shows:

- heuristic candidate boxes or prototype robot and ball boxes
- labels and centroid points
- short movement trails
- an AstraVision prototype watermark

Labels include the detection source, for example `candidate_1 [heuristic]` or
`ball [prototype demo]`.

Open the processed video in the browser:

```text
http://127.0.0.1:8000/videos/output/example_generated-id_analyzed.mp4
```

Uploads larger than 200 MB are rejected with a clear JSON error response. Large
videos should be handled later with background jobs, queues, or offline
processing so the HTTP request does not stay open for too long.

## Heuristic Detection Tuning

The current heuristic detector is experimental. It uses HSV thresholds and
simple contour filters in `app/ai/tracking.py` to find bright or colorful
regions in each frame.

Heuristic detections are labeled as candidates, such as
`candidate_1 [heuristic]`. They are not final robot or ball detections yet. If
the detector does not find useful candidates, the backend keeps using prototype
fallback objects like `robot_1 [prototype demo]`, `robot_2 [prototype demo]`,
and `ball [prototype demo]` so the demo video remains readable.

For tuning, test with real FutBotMX clips that are 10-30 seconds long. Start by
adjusting the HSV threshold constants and contour filter constants in
`app/ai/tracking.py`, then compare the processed video and metadata counters.

## Court ROI Tuning

The detector also has a simple Court ROI filter in `app/ai/tracking.py`. The
ROI is a rectangle defined with normalized ratios from `0.0` to `1.0`, so it
adapts to different video sizes.

Use the Court ROI to focus heuristic detection on the playing field and ignore
people, hands, heads, crowd areas, goal posts, and other background noise. The
output video draws the ROI rectangle and labels it as `Court ROI` so you can
quickly see whether it covers the field.

Tune these constants first when real clips detect too much background:

- `COURT_ROI_X_MIN_RATIO`
- `COURT_ROI_Y_MIN_RATIO`
- `COURT_ROI_X_MAX_RATIO`
- `COURT_ROI_Y_MAX_RATIO`

These detections are still heuristic candidates, not real SAM 3 robot or ball
detections. Prototype fallback remains enabled for demo stability.

## Prototype Fallback

Heuristic detection is experimental. It attempts real frame-derived candidates,
but it can still miss robots and the ball or detect visual noise.

Prototype fallback is demo-only. It draws fake deterministic objects when the
heuristic detector finds no usable candidates. This keeps the output video
visually understandable for demos, but it does not represent real detection.

The pipeline exposes this clearly in metadata:

- `heuristic_frames`
- `prototype_fallback_frames`
- `prototype_fallback_used`
- `detection_mode`
- `warning`

Many `prototype_fallback_frames` means the real heuristic detector is failing,
too strict, or the Court ROI is filtering out too much. To evaluate real
detection honestly, temporarily set `USE_PROTOTYPE_FALLBACK = False` in
`app/ai/pipeline.py`. The next major milestone is SAM 3 integration.

## SAM 3 Integration Plan

SAM 3 is not active yet and is not required to run this backend. The integration
boundary lives in `app/ai/sam_client.py` as `SamClient`.

For now, `SamClient.is_available()` returns `False`, and
`SamClient.segment_frame()` returns an empty result with a clear message. This
lets the OpenCV pipeline stay stable while the SAM 3 dependency and model setup
are still pending.

When SAM 3 dependencies are installed later, the first real test should run only
on selected frames using `SAM3_FRAME_INTERVAL` in `app/ai/pipeline.py`. Do not
run SAM 3 on every frame at first. Heuristic detection and prototype fallback
remain in place as fallback paths while SAM 3 is being evaluated.

## Sample Frames

Each successful analysis saves a small number of sample frames. They are written
to:

```text
output_videos/sample_frames/{analysis_id}/
```

By default, the pipeline saves at most 5 frames, one every 30 frames. This keeps
storage usage small while still giving us representative images for manual SAM 3
experiments, frontend display, demos, and debugging.

The backend saves two versions for each sampled frame:

- `raw_sample_frame_urls` points to clean frames copied from the original video
  before boxes, labels, trails, the Court ROI, or the watermark are drawn. Use
  these raw frames for future SAM 3 testing.
- `overlay_sample_frame_urls` points to frames after the current OpenCV overlays
  are drawn. Use these overlay frames for frontend display, demos, and debugging.
- `sample_frame_urls` remains available for frontend compatibility and points to
  the same overlay frames as `overlay_sample_frame_urls`.

SAM 3 is still not active. These sample frames are preparation only; no SAM 3
inference runs during video analysis.

You can open a saved frame through the API:

```text
http://127.0.0.1:8000/videos/sample-frames/{analysis_id}/raw_sample_01_frame_000030.jpg
http://127.0.0.1:8000/videos/sample-frames/{analysis_id}/overlay_sample_01_frame_000030.jpg
```

The analysis response includes sample-frame metadata. Each URL already points to
the sample-frame endpoint:

```json
{
  "sample_frames_saved": 2,
  "sample_frames_dir": "output_videos/sample_frames/{analysis_id}",
  "sample_frame_urls": [
    "/videos/sample-frames/{analysis_id}/overlay_sample_01_frame_000030.jpg",
    "/videos/sample-frames/{analysis_id}/overlay_sample_02_frame_000060.jpg"
  ],
  "raw_sample_frame_urls": [
    "/videos/sample-frames/{analysis_id}/raw_sample_01_frame_000030.jpg",
    "/videos/sample-frames/{analysis_id}/raw_sample_02_frame_000060.jpg"
  ],
  "overlay_sample_frame_urls": [
    "/videos/sample-frames/{analysis_id}/overlay_sample_01_frame_000030.jpg",
    "/videos/sample-frames/{analysis_id}/overlay_sample_02_frame_000060.jpg"
  ]
}
```

Generated sample frames live under `output_videos/`, which is ignored by Git
except for the `.gitkeep` placeholder.

## Future AI work

SAM 3 is not implemented yet. It will be added later inside
`app/ai/sam_client.py`, then connected to `app/ai/pipeline.py` with real
segmentation, robot and ball tracking, and richer video overlays. The current
heuristic detector is only a visual demo validation step before that work.
