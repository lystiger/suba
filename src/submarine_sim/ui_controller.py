from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UIState:
    environment_mode: str = "base"
    noise_enabled: bool = False
    emergency_surface: bool = False


class UIController:
    def __init__(self) -> None:
        self.state = UIState()

    def toggle_environment_mode(self) -> str:
        self.state.environment_mode = "real" if self.state.environment_mode == "base" else "base"
        self.state.noise_enabled = self.state.environment_mode == "real"
        return self.state.environment_mode

    def set_noise_enabled(self, enabled: bool) -> None:
        self.state.noise_enabled = enabled

    def trigger_emergency_surface(self) -> None:
        self.state.emergency_surface = True
