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
useful heuristic regions are found, the backend falls back to deterministic
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

- heuristic or prototype robot and ball boxes
- labels and centroid points
- short movement trails
- an AstraVision prototype watermark

Labels include the detection source, for example `robot_1 [heuristic]` or
`ball [prototype]`.

Open the processed video in the browser:

```text
http://127.0.0.1:8000/videos/output/example_generated-id_analyzed.mp4
```

Uploads larger than 200 MB are rejected with a clear JSON error response. Large
videos should be handled later with background jobs, queues, or offline
processing so the HTTP request does not stay open for too long.

## Future AI work

SAM 3 is not implemented yet. It will be added later inside
`app/ai/sam_client.py`, then connected to `app/ai/pipeline.py` with real
segmentation, robot and ball tracking, and richer video overlays. The current
heuristic detector is only a visual demo validation step before that work.
