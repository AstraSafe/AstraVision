from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, videos


app = FastAPI(title="AstraVision Backend")

# Local frontend development URLs. Add more origins here when the frontend
# runs on a different port or is deployed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(videos.router)


@app.get("/")
def root():
    return {
        "project": "AstraVision Backend",
        "status": "running",
    }
