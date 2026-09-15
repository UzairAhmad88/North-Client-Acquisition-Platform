"""Platform Maintenance Window and Read-Only Mode Management."""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.administration.base import MaintenanceMode


class MaintenanceWindow(BaseModel):
    window_id: str
    title: str
    description: str
    mode: MaintenanceMode = MaintenanceMode.NORMAL
    is_active: bool = False
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    internal_banner: str = ""
    client_portal_banner: str = ""
    initiated_by: str = "system"
    affected_services: List[str] = Field(default_factory=list)


class MaintenanceManager:
    """Manages platform-wide maintenance states, banner announcements, and read-only mode enforcement."""

    def __init__(self):
        self._current_mode: MaintenanceMode = MaintenanceMode.NORMAL
        self._active_window: Optional[MaintenanceWindow] = None
        self._history: List[MaintenanceWindow] = []

    def get_current_mode(self) -> MaintenanceMode:
        """Return active platform operational mode."""
        return self._current_mode

    def get_active_window(self) -> Optional[MaintenanceWindow]:
        """Return currently active maintenance window if any."""
        return self._active_window

    def is_mutation_allowed(self) -> bool:
        """Evaluate if state-modifying database write operations are permitted."""
        return self._current_mode in [MaintenanceMode.NORMAL, MaintenanceMode.DEGRADED]

    def start_maintenance(
        self,
        mode: MaintenanceMode,
        title: str,
        description: str,
        initiated_by: str,
        internal_banner: str,
        client_banner: str = "",
        affected_services: Optional[List[str]] = None,
    ) -> MaintenanceWindow:
        """Initiate platform maintenance mode with broadcast banners."""
        window_id = f"MAINT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        window = MaintenanceWindow(
            window_id=window_id,
            title=title,
            description=description,
            mode=mode,
            is_active=True,
            start_time=datetime.now(timezone.utc),
            internal_banner=internal_banner,
            client_portal_banner=client_banner,
            initiated_by=initiated_by,
            affected_services=affected_services or ["ALL_SERVICES"],
        )
        self._current_mode = mode
        self._active_window = window
        self._history.append(window)
        return window

    def end_maintenance(self, ended_by: str) -> MaintenanceMode:
        """Restore platform to NORMAL operational mode."""
        if self._active_window:
            self._active_window.is_active = False
            self._active_window.end_time = datetime.now(timezone.utc)
        self._current_mode = MaintenanceMode.NORMAL
        self._active_window = None
        return self._current_mode
