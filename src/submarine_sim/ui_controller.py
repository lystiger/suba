from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import SubmarineApp


@dataclass
class UIState:
    environment_mode: str = "base"
    noise_enabled: bool = False
    emergency_surface: bool = False


class UIController:
    def __init__(self) -> None:
        self.state = UIState()
        self._app: SubmarineApp | None = None

    def attach_app(self, app: SubmarineApp) -> None:
        self._app = app

    def _require_app(self) -> SubmarineApp:
        if self._app is None:
            raise RuntimeError("UIController is not attached to a SubmarineApp instance.")
        return self._app

    def toggle_environment_mode(self) -> str:
        self.state.environment_mode = "real" if self.state.environment_mode == "base" else "base"
        self.state.noise_enabled = self.state.environment_mode == "real"
        return self.state.environment_mode

    def set_environment_mode(self, mode: str) -> str:
        if mode not in {"base", "real"}:
            raise ValueError("Environment mode must be 'base' or 'real'.")
        self.state.environment_mode = mode
        self.state.noise_enabled = mode == "real"
        return self.state.environment_mode

    def set_noise_enabled(self, enabled: bool) -> None:
        self.state.noise_enabled = enabled

    def trigger_emergency_surface(self) -> None:
        self.state.emergency_surface = True

    def load_case(self, json_path: str | Path) -> None:
        self._require_app().load_case(json_path)

    def run_simulation(self, steps: int) -> list[dict]:
        return self._require_app().run(steps=steps)

    def save_report(self, output_path: str | Path) -> None:
        self._require_app().save_report(output_path)
