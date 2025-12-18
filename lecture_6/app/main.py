"""
main.py

Minimal FastAPI application for Docker.

"""

from fastapi import FastAPI

app = FastAPI(title="Healthcheck API")


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    """
    Healthcheck endpoint.

    Returns a JSON response with service status.
    """
    return {"status": "ok"}
