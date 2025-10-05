import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import TemplateNotFound

from eleventh.services.logging.repo import InMemoryLogs, Logs


route = APIRouter(
    prefix="/log",
    tags=["logging", "helper", "admin", "health"],
)

logs: Logs = InMemoryLogs()


templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent / "static"
)


def get_logs() -> Logs:
    """Dependency provider for the Logs instance.

    Tests may override this dependency (app.dependency_overrides[get_logs]) to
    provide a fresh store per app without touching internal attributes.
    """
    return logs


@route.get("/")
async def read_logs(logs: Logs = Depends(get_logs)) -> dict[str, list[str]]:
    return {"logs": await logs.all()}


@route.post("/")
async def write_log(message: str | dict[str, Any], logs: Logs = Depends(get_logs)) -> None:
    if isinstance(message, dict):
        message = json.dumps(jsonable_encoder(message), ensure_ascii=False, indent=4)

    await logs.log(message)


@route.get("/ui")
async def view_logs_ui(request: Request):
    """Serve a simple webpage that shows logs and updates in real time (polling)."""

    try:
        templates.env.get_template("logs.html")
    except TemplateNotFound:
        return HTMLResponse("<h1>Logs UI not found</h1>", status_code=404)

    return templates.TemplateResponse("logs.html", {"request": request})
