"""Thin UI-facing layer around the core simulation app."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import SubmarineApp


@dataclass
class UIState:
    """State flags that drive environment behavior from UI controls."""

    environment_mode: str = "base"
    noise_enabled: bool = False
    emergency_surface: bool = False


class UIController:
    """Public methods used by CLI/text UI/GUI to control the app."""

    def __init__(self) -> None:
        self.state = UIState()
        self._app: SubmarineApp | None = None

    def attach_app(self, app: SubmarineApp) -> None:
        """Attach the main app instance after both objects are created."""

        self._app = app

    def _require_app(self) -> SubmarineApp:
        """Return attached app or raise a clear error."""

        if self._app is None:
            raise RuntimeError("UIController is not attached to a SubmarineApp instance.")
        return self._app

    def toggle_environment_mode(self) -> str:
        """Switch between base and real environment presets."""

        self.state.environment_mode = "real" if self.state.environment_mode == "base" else "base"
        self.state.noise_enabled = self.state.environment_mode == "real"
        return self.state.environment_mode

    def set_environment_mode(self, mode: str) -> str:
        """Set environment mode explicitly and sync related flags."""

        if mode not in {"base", "real"}:
            raise ValueError("Environment mode must be 'base' or 'real'.")
        self.state.environment_mode = mode
        self.state.noise_enabled = mode == "real"
        return self.state.environment_mode

    def set_noise_enabled(self, enabled: bool) -> None:
        """Turn sensor noise on or off."""

        self.state.noise_enabled = enabled

    def trigger_emergency_surface(self) -> None:
        """Flag that emergency surface was requested."""

        self.state.emergency_surface = True

    def load_case(self, json_path: str | Path) -> None:
        """Proxy: load a case through the app."""

        self._require_app().load_case(json_path)

    def run_simulation(self, steps: int) -> list[dict]:
        """Proxy: run simulation for N steps."""

        return self._require_app().run(steps=steps)

    def save_report(self, output_path: str | Path) -> None:
        """Proxy: save telemetry report to CSV."""

        self._require_app().save_report(output_path)
