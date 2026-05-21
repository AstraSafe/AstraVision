# AstraVision Backend

Minimal FastAPI backend for the AstraVision FutBotMX computer vision project.

## What this backend does

This backend is the starting point for uploading FutBotMX videos and sending them through an AI video pipeline.

For now, the pipeline is only a skeleton. It accepts a video upload, saves it in `input_videos/`, creates a planned output path in `output_videos/`, and returns simulated metadata.

## Current status

Skeleton only.

SAM 3, OpenCV video processing, segmentation, tracking, overlays, training, databases, authentication, Docker, queues, and background jobs are not implemented yet.

## Install dependencies later

When you are ready to run the backend, create or activate a Python environment and install:

```bash
pip install -r requirements.txt
```

Do not install dependencies until you are ready to test the backend locally.

## Run later

From the `backend/` directory:

```bash
uvicorn app.main:app --reload
```

## Available endpoints

- `GET /health`
- `POST /videos/analyze`

## Future AI work

SAM 3 is not implemented yet. It will be added later inside `app/ai/sam_client.py`, then connected to `app/ai/pipeline.py` together with OpenCV frame reading, segmentation, robot and ball tracking, and video overlays.
