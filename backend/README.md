# AstraVision Backend

Minimal FastAPI backend for the AstraVision FutBotMX computer vision project.

## What this backend does

This backend accepts FutBotMX video uploads and sends them through a simple AI pipeline prototype.

The current milestone uses OpenCV to read the uploaded video, copy each frame, add basic overlay text, and export a processed video into `output_videos/`.

## Current status

OpenCV prototype only.

SAM 3, segmentation, robot tracking, ball tracking, training, databases, authentication, Docker, queues, and background jobs are not implemented yet.

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

Open the processed video in the browser:

```text
http://127.0.0.1:8000/videos/output/example_generated-id_analyzed.mp4
```

Uploads larger than 200 MB are rejected with a clear JSON error response. Large
videos should be handled later with background jobs, queues, or offline
processing so the HTTP request does not stay open for too long.

## Future AI work

SAM 3 is not implemented yet. It will be added later inside `app/ai/sam_client.py`, then connected to `app/ai/pipeline.py` with segmentation, robot and ball tracking, and richer video overlays.
