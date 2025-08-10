"""FastAPI application exposing AgentCellPhone functionality.

The GUI interacts with this API rather than talking directly to the
underlying :mod:`agent_cell_phone` module.  This provides a clean
separation between presentation and core logic and enables remote
operation.  The API also exposes a status endpoint that returns recent
events published on the internal :mod:`EventBus`.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from .agent_service import LocalAgentService
from .event_bus import event_bus


app = FastAPI(title="AgentCellPhone API")


# Local service instance that performs the actual work
service = LocalAgentService()


class Message(BaseModel):
    """Model representing a message request."""

    target: str
    message: str
    tag: Optional[str] = "NORMAL"


@app.post("/send")
def send_message(msg: Message):
    """Send a message to a specific agent."""

    success, detail = service.send_message(msg.target, msg.message, msg.tag)
    event_bus.publish(
        {
            "type": "send",
            "target": msg.target,
            "message": msg.message,
            "tag": msg.tag,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
    return {"success": success, "detail": detail}


@app.post("/broadcast")
def broadcast_message(msg: Message):
    """Broadcast a message to all agents."""

    success, detail = service.send_message("all", msg.message, msg.tag)
    event_bus.publish(
        {
            "type": "broadcast",
            "message": msg.message,
            "tag": msg.tag,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
    return {"success": success, "detail": detail}


@app.get("/status")
def status():
    """Return current system status along with recent events."""

    data = service.get_system_status()
    data.update(
        {
            "events": event_bus.get_events(limit=20),
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
    return data


# To run: ``uvicorn src.services.api:app``

