"""ClouDiamond - Security toolkit for Scratch and TurboWarp."""

from __future__ import annotations

import secrets
import time
from typing import Any, Dict, Optional

__version__ = "0.0.2"


class ClouDiamond:
    """Create and validate basic ClouDiamond requests."""

    def __init__(self, *, max_request_age: int = 30):
        if max_request_age <= 0:
            raise ValueError("max_request_age must be positive")
        self.version = __version__
        self.max_request_age = max_request_age

    def info(self) -> Dict[str, str]:
        return {
            "name": "ClouDiamond",
            "version": self.version,
            "status": "development",
        }

    def create_request(
        self,
        *,
        action: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a request with a unique ID and current Unix timestamp."""
        if not isinstance(action, str) or not action.strip():
            raise ValueError("action must be a non-empty string")
        if data is not None and not isinstance(data, dict):
            raise TypeError("data must be a dictionary or None")

        return {
            "request_id": secrets.token_hex(8),
            "action": action,
            "data": {} if data is None else data,
            "timestamp": int(time.time()),
        }

    def validate_request(
        self,
        request: Dict[str, Any],
        *,
        allowed_actions: Optional[set[str]] = None,
        now: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Validate request shape, action and timestamp."""
        if not isinstance(request, dict):
            return {"ok": False, "error": "request must be a dictionary"}

        required = ("request_id", "action", "data", "timestamp")
        missing = [key for key in required if key not in request]
        if missing:
            return {"ok": False, "error": "missing fields: " + ", ".join(missing)}

        request_id = request["request_id"]
        action = request["action"]
        data = request["data"]
        timestamp = request["timestamp"]

        if not isinstance(request_id, str) or len(request_id) != 16:
            return {"ok": False, "error": "invalid request_id"}
        if not isinstance(action, str) or not action.strip():
            return {"ok": False, "error": "invalid action"}
        if not isinstance(data, dict):
            return {"ok": False, "error": "data must be a dictionary"}
        if not isinstance(timestamp, int) or isinstance(timestamp, bool):
            return {"ok": False, "error": "invalid timestamp"}

        if allowed_actions is not None and action not in allowed_actions:
            return {"ok": False, "error": "action is not allowed"}

        current_time = int(time.time()) if now is None else now
        if abs(current_time - timestamp) > self.max_request_age:
            return {"ok": False, "error": "request expired"}

        return {
            "ok": True,
            "request_id": request_id,
            "action": action,
            "data": data,
        }


__all__ = ["ClouDiamond", "__version__"]
